"""
Google One (Gemini) Student Verification Tool
SheerID Student Verification for Google One AI Premium

Enhanced with:
- Success rate tracking per organization
- Weighted university selection
- Retry with exponential backoff
- Rate limiting avoidance
- Anti-detection with random User-Agents

Author: ThanhNguyxn
"""

import os
import re
import sys
import json
import time
import random
import hashlib
from pathlib import Path
from io import BytesIO
from typing import Dict, Optional, Tuple
from functools import wraps
from datetime import datetime, timedelta

try:
    import httpx
except ImportError:
    print("❌ Error: httpx required. Install: pip install httpx")
    sys.exit(1)

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
except ImportError:
    print("❌ Error: Pillow required. Install: pip install Pillow")
    sys.exit(1)

# Optional numpy for scan effects
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# Import anti-detection module
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from anti_detect import get_headers, get_fingerprint, get_random_user_agent, random_delay as anti_delay, create_session
    HAS_ANTI_DETECT = True
    print("[INFO] Anti-detection module loaded")
except ImportError:
    HAS_ANTI_DETECT = False
    print("[WARN] anti_detect.py not found, using basic headers")


# ============ CONFIG ============
PROGRAM_ID = "67c8c14f5f17a83b745e3f82"
SHEERID_API_URL = "https://services.sheerid.com/rest/v2"
MIN_DELAY = 300
MAX_DELAY = 800


# ============ STATS TRACKING ============
class Stats:
    """Track success rates by organization"""
    
    def __init__(self):
        self.file = Path(__file__).parent / "stats.json"
        self.data = self._load()
    
    def _load(self) -> Dict:
        if self.file.exists():
            try:
                return json.loads(self.file.read_text())
            except:
                pass
        return {"total": 0, "success": 0, "failed": 0, "orgs": {}}
    
    def _save(self):
        self.file.write_text(json.dumps(self.data, indent=2))
    
    def record(self, org: str, success: bool):
        self.data["total"] += 1
        self.data["success" if success else "failed"] += 1
        
        if org not in self.data["orgs"]:
            self.data["orgs"][org] = {"success": 0, "failed": 0}
        self.data["orgs"][org]["success" if success else "failed"] += 1
        self._save()
    
    def get_rate(self, org: str = None) -> float:
        if org:
            o = self.data["orgs"].get(org, {})
            total = o.get("success", 0) + o.get("failed", 0)
            return o.get("success", 0) / total * 100 if total else 50
        return self.data["success"] / self.data["total"] * 100 if self.data["total"] else 0
    
    def print_stats(self):
        print(f"\n📊 Statistics:")
        print(f"   Total: {self.data['total']} | ✅ {self.data['success']} | ❌ {self.data['failed']}")
        if self.data["total"]:
            print(f"   Success Rate: {self.get_rate():.1f}%")


stats = Stats()


# ============ UNIVERSITIES WITH WEIGHTS ============
# NOTE: As of Jan 2026, new Gemini student sign-ups are US-ONLY
# Other countries may work for existing users but new sign-ups restricted

UNIVERSITIES = [
    # =========== USA - HIGH PRIORITY ===========
    # These have highest success rates for new sign-ups
    {"id": 2565, "name": "Pennsylvania State University-Main Campus", "domain": "psu.edu", "weight": 100},
    {"id": 3499, "name": "University of California, Los Angeles", "domain": "ucla.edu", "weight": 98},
    {"id": 3491, "name": "University of California, Berkeley", "domain": "berkeley.edu", "weight": 97},
    {"id": 1953, "name": "Massachusetts Institute of Technology", "domain": "mit.edu", "weight": 95},
    {"id": 3113, "name": "Stanford University", "domain": "stanford.edu", "weight": 95},
    {"id": 2285, "name": "New York University", "domain": "nyu.edu", "weight": 96},
    {"id": 1426, "name": "Harvard University", "domain": "harvard.edu", "weight": 92},
    {"id": 590759, "name": "Yale University", "domain": "yale.edu", "weight": 90},
    {"id": 2626, "name": "Princeton University", "domain": "princeton.edu", "weight": 90},
    {"id": 698, "name": "Columbia University", "domain": "columbia.edu", "weight": 92},
    {"id": 3508, "name": "University of Chicago", "domain": "uchicago.edu", "weight": 88},
    {"id": 943, "name": "Duke University", "domain": "duke.edu", "weight": 88},
    {"id": 751, "name": "Cornell University", "domain": "cornell.edu", "weight": 90},
    {"id": 2420, "name": "Northwestern University", "domain": "northwestern.edu", "weight": 88},
    # More US Universities
    {"id": 3568, "name": "University of Michigan", "domain": "umich.edu", "weight": 95},
    {"id": 3686, "name": "University of Texas at Austin", "domain": "utexas.edu", "weight": 94},
    {"id": 1217, "name": "Georgia Institute of Technology", "domain": "gatech.edu", "weight": 93},
    {"id": 602, "name": "Carnegie Mellon University", "domain": "cmu.edu", "weight": 92},
    {"id": 3477, "name": "University of California, San Diego", "domain": "ucsd.edu", "weight": 93},
    {"id": 3600, "name": "University of North Carolina at Chapel Hill", "domain": "unc.edu", "weight": 90},
    {"id": 3645, "name": "University of Southern California", "domain": "usc.edu", "weight": 91},
    {"id": 3629, "name": "University of Pennsylvania", "domain": "upenn.edu", "weight": 90},
    {"id": 1603, "name": "Indiana University Bloomington", "domain": "iu.edu", "weight": 88},
    {"id": 2506, "name": "Ohio State University", "domain": "osu.edu", "weight": 90},
    {"id": 2700, "name": "Purdue University", "domain": "purdue.edu", "weight": 89},
    {"id": 3761, "name": "University of Washington", "domain": "uw.edu", "weight": 90},
    {"id": 3770, "name": "University of Wisconsin-Madison", "domain": "wisc.edu", "weight": 88},
    {"id": 3562, "name": "University of Maryland", "domain": "umd.edu", "weight": 87},
    {"id": 519, "name": "Boston University", "domain": "bu.edu", "weight": 86},
    {"id": 378, "name": "Arizona State University", "domain": "asu.edu", "weight": 92},
    {"id": 3521, "name": "University of Florida", "domain": "ufl.edu", "weight": 90},
    {"id": 3535, "name": "University of Illinois at Urbana-Champaign", "domain": "illinois.edu", "weight": 91},
    {"id": 3557, "name": "University of Minnesota Twin Cities", "domain": "umn.edu", "weight": 88},
    {"id": 3483, "name": "University of California, Davis", "domain": "ucdavis.edu", "weight": 89},
    {"id": 3487, "name": "University of California, Irvine", "domain": "uci.edu", "weight": 88},
    {"id": 3502, "name": "University of California, Santa Barbara", "domain": "ucsb.edu", "weight": 87},
    # Community Colleges (may have higher success)
    {"id": 2874, "name": "Santa Monica College", "domain": "smc.edu", "weight": 85},
    {"id": 2350, "name": "Northern Virginia Community College", "domain": "nvcc.edu", "weight": 84},
    
    # =========== OTHER COUNTRIES (Lower priority - may not work for new sign-ups) ===========
    # Canada
    {"id": 328355, "name": "University of Toronto", "domain": "utoronto.ca", "weight": 40},
    {"id": 328315, "name": "University of British Columbia", "domain": "ubc.ca", "weight": 38},
    # UK
    {"id": 273409, "name": "University of Oxford", "domain": "ox.ac.uk", "weight": 35},
    {"id": 273378, "name": "University of Cambridge", "domain": "cam.ac.uk", "weight": 35},
    # India (likely blocked for new sign-ups)
    {"id": 10007277, "name": "Indian Institute of Technology Delhi", "domain": "iitd.ac.in", "weight": 20},
    {"id": 3819983, "name": "University of Mumbai", "domain": "mu.ac.in", "weight": 15},
    # Australia
    {"id": 345301, "name": "The University of Melbourne", "domain": "unimelb.edu.au", "weight": 30},
    {"id": 345303, "name": "The University of Sydney", "domain": "sydney.edu.au", "weight": 28},
]






def select_university() -> Dict:
    """Weighted random selection based on success rates"""
    weights = []
    for uni in UNIVERSITIES:
        weight = uni["weight"] * (stats.get_rate(uni["name"]) / 50)
        weights.append(max(1, weight))
    
    total = sum(weights)
    r = random.uniform(0, total)
    
    cumulative = 0
    for uni, weight in zip(UNIVERSITIES, weights):
        cumulative += weight
        if r <= cumulative:
            return {**uni, "idExtended": str(uni["id"])}
    return {**UNIVERSITIES[0], "idExtended": str(UNIVERSITIES[0]["id"])}


# ============ UTILITIES ============
FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
    "Donald", "Steven", "Andrew", "Paul", "Joshua", "Kenneth", "Kevin", "Brian",
    "George", "Timothy", "Ronald", "Edward", "Jason", "Jeffrey", "Ryan",
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan",
    "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret", "Sandra",
    "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Dorothy", "Carol",
    "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura",
    "Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia"
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
    "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Turner", "Phillips", "Evans", "Parker", "Edwards"
]


def random_delay():
    time.sleep(random.randint(MIN_DELAY, MAX_DELAY) / 1000)


def generate_fingerprint() -> str:
    """Generate realistic browser fingerprint to avoid fraud detection"""
    # Realistic screen resolutions
    resolutions = ["1920x1080", "1366x768", "1536x864", "1440x900", "1280x720", "2560x1440"]
    # Common timezones
    timezones = [-8, -7, -6, -5, -4, 0, 1, 2, 3, 5.5, 8, 9, 10]
    # Common languages
    languages = ["en-US", "en-GB", "en-CA", "en-AU", "es-ES", "fr-FR", "de-DE", "pt-BR"]
    # Common platforms
    platforms = ["Win32", "MacIntel", "Linux x86_64"]
    # Browser vendors
    vendors = ["Google Inc.", "Apple Computer, Inc.", ""]
    
    components = [
        str(int(time.time() * 1000)),
        str(random.random()),
        random.choice(resolutions),
        str(random.choice(timezones)),
        random.choice(languages),
        random.choice(platforms),
        random.choice(vendors),
        str(random.randint(1, 16)),  # hardware concurrency (CPU cores)
        str(random.randint(2, 32)),  # device memory GB
        str(random.randint(0, 1)),   # touch support
    ]
    return hashlib.md5("|".join(components).encode()).hexdigest()


def generate_name() -> Tuple[str, str]:
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def generate_email(first: str, last: str, domain: str) -> str:
    patterns = [
        f"{first[0].lower()}{last.lower()}{random.randint(100, 999)}",
        f"{first.lower()}.{last.lower()}{random.randint(10, 99)}",
        f"{last.lower()}{first[0].lower()}{random.randint(100, 999)}"
    ]
    return f"{random.choice(patterns)}@{domain}"


def generate_birth_date() -> str:
    year = random.randint(2000, 2006)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"


# ============ STUDENT INFO CLASS ============
class StudentInfo:
    """Class to hold consistent student information across all documents"""
    
    def __init__(self, first: str = None, last: str = None, school: str = None, 
                 domain: str = None, dob: str = None, photo_path: str = None):
        self.first = first or random.choice(FIRST_NAMES)
        self.last = last or random.choice(LAST_NAMES)
        self.school = school or "University"
        self.domain = domain or "university.edu"
        self.dob = dob or generate_birth_date()
        self.student_id = generate_student_number()
        self.email = generate_email(self.first, self.last, self.domain)
        self.photo_path = photo_path
        
        # Generate consistent dates
        semester, year = get_current_semester()
        self.semester = semester
        self.year = year
        self.academic_year = get_academic_year()
        
        # Issue/expiry dates for ID card
        today = datetime.now()
        self.issue_date = (today - timedelta(days=random.randint(5, 30))).strftime("%m/%d/%Y")
        self.expiry_date = f"05/31/{year + 1}"
    
    def __repr__(self):
        return f"StudentInfo({self.first} {self.last}, {self.school}, ID: {self.student_id})"


def get_sample_photos() -> list:
    """Get list of available sample photos from assets folder"""
    assets_dir = Path(__file__).parent / "assets" / "photos"
    if assets_dir.exists():
        return list(assets_dir.glob("*.png")) + list(assets_dir.glob("*.jpg"))
    return []


def apply_photo_effect(img: Image.Image) -> Image.Image:
    """Apply camera photo effect to student ID card (not scanned document)
    - Slight perspective distortion simulation
    - Natural lighting variation
    - Slight blur for realism
    """
    # 1. Slight brightness variation (natural lighting)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(random.uniform(0.95, 1.05))
    
    # 2. Slight color temperature shift
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(random.uniform(0.95, 1.05))
    
    # 3. Very subtle blur (camera focus)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.2))
    
    # 4. Add slight vignette effect (darker corners)
    if HAS_NUMPY:
        arr = np.array(img, dtype=np.float32)
        rows, cols = arr.shape[:2]
        X = np.arange(0, cols)
        Y = np.arange(0, rows)
        X, Y = np.meshgrid(X, Y)
        center_x, center_y = cols / 2, rows / 2
        # Create radial gradient
        dist = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)
        max_dist = np.sqrt(center_x ** 2 + center_y ** 2)
        vignette = 1 - 0.15 * (dist / max_dist) ** 2  # Subtle vignette
        vignette = vignette[:, :, np.newaxis]
        arr = arr * vignette
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        img = Image.fromarray(arr)
    
    return img


def image_to_pdf(img: Image.Image) -> bytes:
    """Convert PIL Image to PDF bytes"""
    buf = BytesIO()
    # Convert to RGB if necessary (PDF doesn't support RGBA)
    if img.mode in ('RGBA', 'LA', 'P'):
        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = rgb_img
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    img.save(buf, format='PDF', resolution=100.0)
    return buf.getvalue()



def get_current_semester() -> Tuple[str, int]:
    """Get current semester and year based on current date"""
    now = datetime.now()
    month = now.month
    year = now.year
    
    if month <= 5:
        return "SPRING", year
    elif month <= 7:
        return "SUMMER", year
    else:
        return "FALL", year


def get_academic_year() -> str:
    """Get current academic year (e.g., 2025-2026)"""
    now = datetime.now()
    if now.month >= 8:  # Fall semester starts new academic year
        return f"{now.year}-{now.year + 1}"
    else:
        return f"{now.year - 1}-{now.year}"


def get_recent_date(days_ago_max: int = 30) -> str:
    """Generate a recent date within the last N days"""
    days_ago = random.randint(1, days_ago_max)
    date = datetime.now() - timedelta(days=days_ago)
    return date.strftime("%Y-%m-%d")


# ============ DOCUMENT ENHANCEMENT EFFECTS ============
def apply_scan_effect(img: Image.Image) -> Image.Image:
    """Apply scan effect to make document look more realistic
    - Slight rotation
    - Minor noise
    - Adjusted contrast
    - Paper texture simulation
    """
    # 1. Slight rotation (like imperfect scanner placement)
    angle = random.uniform(-0.3, 0.3)
    img = img.rotate(angle, expand=False, fillcolor=(255, 255, 255), resample=Image.Resampling.BILINEAR)
    
    # 2. Add slight noise if numpy available
    if HAS_NUMPY:
        arr = np.array(img, dtype=np.float32)
        noise = np.random.normal(0, 1.5, arr.shape)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(arr)
    
    # 3. Slight contrast adjustment
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(random.uniform(0.97, 1.03))
    
    # 4. Slight brightness adjustment (paper not perfectly white)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(random.uniform(0.98, 1.0))
    
    # 5. Very light blur to simulate scan
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    
    return img


def add_official_watermark(img: Image.Image, text: str = "OFFICIAL DOCUMENT") -> Image.Image:
    """Add diagonal watermark to document"""
    # Create transparent overlay
    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    # Calculate position for center diagonal
    w, h = img.size
    
    # Draw semi-transparent diagonal text
    # Position in center, rotated
    text_img = Image.new('RGBA', (w, 200), (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text((w//2, 100), text, fill=(200, 200, 200, 40), font=font, anchor="mm")
    text_img = text_img.rotate(30, expand=False, fillcolor=(255, 255, 255, 0))
    
    # Paste in center
    result = img.convert('RGBA')
    result.paste(text_img, (0, h//2 - 100), text_img)
    
    return result.convert('RGB')


def add_school_seal(draw: ImageDraw.Draw, x: int, y: int, school: str, size: int = 80):
    """Add a circular school seal/stamp effect"""
    # Draw outer circle
    draw.ellipse([(x-size, y-size), (x+size, y+size)], outline=(150, 0, 0), width=2)
    draw.ellipse([(x-size+5, y-size+5), (x+size-5, y+size-5)], outline=(150, 0, 0), width=1)
    
    # Draw star in center
    star_size = size // 3
    for i in range(5):
        angle = i * 72 - 90
        rad = angle * 3.14159 / 180
        x1 = x + int(star_size * 0.4 * (1 if i % 2 == 0 else 0.5) * (1.5 * (1 - abs(i - 2) / 2)))
    
    # Add text around the seal
    try:
        font = ImageFont.truetype("arial.ttf", 10)
    except:
        font = ImageFont.load_default()
    
    # Simplified seal with school name
    short_name = school.split()[0][:12].upper() if school else "UNIVERSITY"
    draw.text((x, y-size//2), short_name, fill=(150, 0, 0), font=font, anchor="mm")
    draw.text((x, y+size//2), "REGISTRAR", fill=(150, 0, 0), font=font, anchor="mm")
    draw.text((x, y), "★", fill=(150, 0, 0), font=font, anchor="mm")


def generate_student_number() -> str:
    """Generate realistic student ID number"""
    # Common formats: 8-10 digits, sometimes with prefix
    formats = [
        f"{random.randint(2020, 2024)}{random.randint(100000, 999999)}",  # Year + 6 digits
        f"S{random.randint(10000000, 99999999)}",  # S + 8 digits
        f"{random.randint(10000000, 99999999)}",  # 8 digits
        f"U{random.randint(1000000, 9999999)}",  # U + 7 digits
    ]
    return random.choice(formats)


# ============ DOCUMENT GENERATOR ============
def generate_transcript(first: str, last: str, school: str, dob: str,
                        student_info: StudentInfo = None, output_format: str = "pdf") -> bytes:
    """Generate fake academic transcript with dynamic dates
    
    Args:
        output_format: "pdf" or "png"
    """
    w, h = 850, 1100
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Use StudentInfo if provided
    if student_info:
        first = student_info.first
        last = student_info.last
        school = student_info.school
        dob = student_info.dob
        student_id_num = student_info.student_id
        semester = student_info.semester
        year = student_info.year
        academic_year = student_info.academic_year
    else:
        semester, year = get_current_semester()
        academic_year = get_academic_year()
        student_id_num = generate_student_number()
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    try:
        font_header = ImageFont.truetype("arial.ttf", 32)
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_text = ImageFont.truetype("arial.ttf", 16)
        font_bold = ImageFont.truetype("arialbd.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_header = font_title = font_text = font_bold = font_small = ImageFont.load_default()
    
    # 1. Header with school logo area
    draw.rectangle([(0, 0), (w, 120)], fill=(245, 245, 250))
    draw.text((w//2, 40), school.upper(), fill=(0, 0, 100), font=font_header, anchor="mm")
    draw.text((w//2, 80), "OFFICIAL ACADEMIC TRANSCRIPT", fill=(50, 50, 80), font=font_title, anchor="mm")
    draw.line([(50, 115), (w-50, 115)], fill=(0, 0, 100), width=3)
    
    # 2. Document Info - Right aligned date info (CRITICAL for SheerID)
    y = 135
    draw.text((w-50, y), f"Document Date: {today}", fill=(0, 100, 0), font=font_bold, anchor="rm")
    y += 25
    draw.text((w-50, y), f"Academic Year: {academic_year}", fill=(0, 0, 0), font=font_text, anchor="rm")
    
    # 3. Student Info - use consistent student_id
    y = 170
    draw.text((50, y), f"Student Name: {first} {last}", fill=(0, 0, 0), font=font_bold)
    y += 30
    draw.text((50, y), f"Student ID: {student_id_num}", fill=(0, 0, 0), font=font_text)
    draw.text((w-300, y), f"Date of Birth: {dob}", fill=(0, 0, 0), font=font_text)
    y += 40
    
    # 4. Current Enrollment Status (CRITICAL - dynamic semester)
    draw.rectangle([(50, y), (w-50, y+50)], fill=(230, 245, 230), outline=(0, 100, 0), width=2)
    draw.text((w//2, y+15), f"ENROLLMENT STATUS: CURRENTLY ENROLLED", fill=(0, 100, 0), font=font_bold, anchor="mm")
    draw.text((w//2, y+38), f"{semester} SEMESTER {year}", fill=(0, 80, 0), font=font_bold, anchor="mm")
    y += 75
    
    # 5. Courses for current semester
    draw.text((50, y), f"{semester} {year} - Course Schedule", font=font_bold, fill=(0,0,100))
    y += 30
    
    courses = [
        ("CS 301", "Data Structures & Algorithms", "4.0", "In Progress"),
        ("MATH 302", "Linear Algebra", "3.0", "In Progress"),
        ("ENG 201", "Technical Writing", "3.0", "In Progress"),
        ("PHYS 202", "Electromagnetism", "4.0", "In Progress"),
        ("ECON 101", "Microeconomics", "3.0", "In Progress")
    ]
    
    # Table Header
    draw.rectangle([(50, y), (w-50, y+25)], fill=(240, 240, 250))
    draw.text((60, y+5), "Course Code", font=font_bold, fill=(0,0,0))
    draw.text((200, y+5), "Course Title", font=font_bold, fill=(0,0,0))
    draw.text((550, y+5), "Credits", font=font_bold, fill=(0,0,0))
    draw.text((650, y+5), "Status", font=font_bold, fill=(0,0,0))
    y += 30
    
    for code, title, cred, status in courses:
        draw.text((60, y), code, font=font_text, fill=(0,0,0))
        draw.text((200, y), title, font=font_text, fill=(0,0,0))
        draw.text((550, y), cred, font=font_text, fill=(0,0,0))
        draw.text((650, y), status, font=font_text, fill=(0, 100, 0))
        y += 28
    
    y += 10
    draw.line([(50, y), (w-50, y)], fill=(0, 0, 0), width=1)
    y += 20
    
    # 6. Summary
    draw.text((50, y), f"Total Credits This Semester: 17.0", font=font_text, fill=(0,0,0))
    draw.text((400, y), f"Cumulative GPA: 3.85", font=font_bold, fill=(0,0,0))
    y += 25
    draw.text((50, y), f"Academic Standing: Good Standing", font=font_text, fill=(0,100,0))
    
    # 7. Add official seal
    add_school_seal(draw, w-120, h-200, school, size=60)
    
    # 8. Footer with date stamp
    draw.line([(50, h-100), (w-50, h-100)], fill=(200, 200, 200), width=1)
    draw.text((w//2, h-70), "This is an official document of " + school, fill=(100, 100, 100), font=font_small, anchor="mm")
    draw.text((w//2, h-50), f"Generated on {today} | Valid for verification purposes", fill=(100, 100, 100), font=font_small, anchor="mm")
    draw.text((w//2, h-30), "This document is electronically generated and valid without signature.", fill=(150, 150, 150), font=font_small, anchor="mm")
    
    # Apply scan effect for realism
    img = apply_scan_effect(img)
    
    # Output in requested format
    if output_format.lower() == "pdf":
        return image_to_pdf(img)
    else:
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

def generate_student_id(first: str, last: str, school: str, 
                        student_info: StudentInfo = None, photo_path: str = None) -> bytes:
    """Generate fake student ID card with real photo support
    
    Args:
        first: First name (used if student_info not provided)
        last: Last name (used if student_info not provided)
        school: School name (used if student_info not provided)
        student_info: StudentInfo object for consistent data across documents
        photo_path: Path to photo file to insert into ID card
    
    Returns:
        PNG bytes of the student ID card image
    """
    w, h = 650, 420
    # Randomize background color slightly
    bg_color = (random.randint(248, 255), random.randint(248, 255), random.randint(248, 255))
    img = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Use StudentInfo if provided, otherwise use individual params
    if student_info:
        first = student_info.first
        last = student_info.last
        school = student_info.school
        student_id_num = student_info.student_id
        semester = student_info.semester
        year = student_info.year
        academic_year = student_info.academic_year
        issue_date = student_info.issue_date
        expiry_date = student_info.expiry_date
        photo_path = photo_path or student_info.photo_path
    else:
        # Get dynamic dates (legacy mode)
        semester, year = get_current_semester()
        academic_year = get_academic_year()
        today = datetime.now()
        issue_date = (today - timedelta(days=random.randint(5, 30))).strftime("%m/%d/%Y")
        expiry_date = f"05/31/{year + 1}"
        student_id_num = generate_student_number()
    
    try:
        font_lg = ImageFont.truetype("arial.ttf", 24)
        font_md = ImageFont.truetype("arial.ttf", 16)
        font_sm = ImageFont.truetype("arial.ttf", 12)
        font_bold = ImageFont.truetype("arialbd.ttf", 18)
        font_name = ImageFont.truetype("arialbd.ttf", 22)
    except:
        font_lg = font_md = font_sm = font_bold = font_name = ImageFont.load_default()
    
    # Header color - school themed
    header_color = (random.randint(0, 40), random.randint(30, 80), random.randint(100, 160))
    
    # Header with school name
    draw.rectangle([(0, 0), (w, 75)], fill=header_color)
    draw.text((w//2, 25), school.upper(), fill=(255, 255, 255), font=font_lg, anchor="mm")
    draw.text((w//2, 55), f"STUDENT IDENTIFICATION CARD", fill=(200, 220, 255), font=font_sm, anchor="mm")
    
    # Academic year badge
    draw.rectangle([(w-130, 85), (w-10, 115)], fill=(0, 100, 0), outline=(0, 80, 0))
    draw.text((w-70, 100), f"AY {academic_year}", fill=(255, 255, 255), font=font_sm, anchor="mm")
    
    # Photo area - try to load real photo
    photo_box = (25, 95, 155, 260)  # left, top, right, bottom
    photo_width = photo_box[2] - photo_box[0]
    photo_height = photo_box[3] - photo_box[1]
    
    photo_loaded = False
    if photo_path:
        try:
            photo = Image.open(photo_path)
            # Resize to fit photo area while maintaining aspect ratio
            photo.thumbnail((photo_width, photo_height), Image.Resampling.LANCZOS)
            # Center the photo in the box
            paste_x = photo_box[0] + (photo_width - photo.width) // 2
            paste_y = photo_box[1] + (photo_height - photo.height) // 2
            # Convert RGBA to RGB if needed
            if photo.mode == 'RGBA':
                bg = Image.new('RGB', photo.size, (230, 230, 235))
                bg.paste(photo, mask=photo.split()[3])
                photo = bg
            elif photo.mode != 'RGB':
                photo = photo.convert('RGB')
            img.paste(photo, (paste_x, paste_y))
            photo_loaded = True
        except Exception as e:
            print(f"     ⚠️ Could not load photo: {e}")
    
    if not photo_loaded:
        # Draw placeholder
        draw.rectangle([(photo_box[0], photo_box[1]), (photo_box[2], photo_box[3])], outline=(100, 100, 100), width=2, fill=(230, 230, 235))
        draw.text((90, 175), "PHOTO", fill=(150, 150, 150), font=font_md, anchor="mm")
    else:
        # Draw border around photo
        draw.rectangle([(photo_box[0], photo_box[1]), (photo_box[2], photo_box[3])], outline=(100, 100, 100), width=2)
    
    # Student Info
    x_info = 175
    y = 100
    draw.text((x_info, y), f"{first} {last}", fill=(0, 0, 0), font=font_name)
    y += 35
    
    # Info labels and values - use consistent student_id
    labels = [
        ("Student ID:", student_id_num),
        ("Status:", "Active Student"),
        ("Issue Date:", issue_date),
        ("Expiration:", expiry_date),
    ]
    
    for label, value in labels:
        draw.text((x_info, y), label, fill=(80, 80, 80), font=font_sm)
        draw.text((x_info + 85, y), value, fill=(0, 0, 0), font=font_md)
        y += 28
    
    # Semester indicator
    y += 5
    draw.rectangle([(x_info, y), (x_info + 180, y + 25)], fill=(240, 250, 240), outline=(0, 100, 0))
    draw.text((x_info + 90, y + 12), f"{semester} {year}", fill=(0, 100, 0), font=font_bold, anchor="mm")
    
    # Barcode strip at bottom
    draw.rectangle([(0, 330), (w, 420)], fill=(255, 255, 255))
    
    # Add magnetic stripe effect
    draw.rectangle([(0, 280), (w, 320)], fill=(40, 40, 40))
    
    # Improved barcode - use consistent student_id
    barcode_start = 80
    for i in range(35):
        x = barcode_start + i * 14
        bar_width = random.choice([2, 4, 6])
        if random.random() > 0.25:
            draw.rectangle([(x, 340), (x + bar_width, 385)], fill=(0, 0, 0))
    
    # Barcode number under barcode - use consistent student_id
    draw.text((w//2, 395), student_id_num, fill=(0, 0, 0), font=font_sm, anchor="mm")
    
    # Card number at very bottom
    draw.text((w//2, 412), f"Card ID: {random.randint(100000, 999999)}", fill=(120, 120, 120), font=font_sm, anchor="mm")
    
    # Apply PHOTO effect (not scan effect) - makes it look like a photo of the card
    img = apply_photo_effect(img)
            
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_class_schedule(first: str, last: str, school: str,
                            student_info: StudentInfo = None, output_format: str = "pdf") -> bytes:
    """Generate fake class schedule document
    
    Args:
        output_format: "pdf" or "png"
    """
    w, h = 850, 700
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Use StudentInfo if provided
    if student_info:
        first = student_info.first
        last = student_info.last
        school = student_info.school
        student_id_num = student_info.student_id
        semester = student_info.semester
        year = student_info.year
    else:
        semester, year = get_current_semester()
        student_id_num = generate_student_number()
    
    today = datetime.now().strftime("%m/%d/%Y")
    
    try:
        font_header = ImageFont.truetype("arial.ttf", 28)
        font_title = ImageFont.truetype("arial.ttf", 20)
        font_text = ImageFont.truetype("arial.ttf", 14)
        font_bold = ImageFont.truetype("arialbd.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 11)
    except:
        font_header = font_title = font_text = font_bold = font_small = ImageFont.load_default()
    
    # Header
    draw.rectangle([(0, 0), (w, 90)], fill=(20, 50, 120))
    draw.text((w//2, 30), school.upper(), fill=(255, 255, 255), font=font_header, anchor="mm")
    draw.text((w//2, 65), f"{semester} {year} CLASS SCHEDULE", fill=(200, 220, 255), font=font_title, anchor="mm")
    
    # Student info and date - use consistent student_id
    y = 110
    draw.text((50, y), f"Student: {first} {last}", fill=(0, 0, 0), font=font_bold)
    draw.text((350, y), f"Student ID: {student_id_num}", fill=(0, 0, 0), font=font_text)
    draw.text((w-50, y), f"Printed: {today}", fill=(0, 100, 0), font=font_bold, anchor="rm")
    
    y += 40
    draw.line([(50, y), (w-50, y)], fill=(200, 200, 200), width=1)
    y += 20
    
    # Course schedule table
    courses = [
        ("CS 301", "Data Structures", "Dr. Smith", "MWF 9:00-9:50", "ENG 201", "3.0"),
        ("MATH 302", "Linear Algebra", "Prof. Johnson", "TTh 10:30-11:45", "MATH 105", "3.0"),
        ("ENG 201", "Technical Writing", "Dr. Williams", "MWF 11:00-11:50", "LIB 302", "3.0"),
        ("PHYS 202", "Electromagnetism", "Prof. Brown", "TTh 1:00-2:15", "SCI 401", "4.0"),
        ("ECON 101", "Microeconomics", "Dr. Davis", "MWF 2:00-2:50", "BUS 110", "3.0"),
    ]
    
    # Table header
    cols = [50, 130, 280, 400, 550, 680, 750]
    headers = ["Code", "Course Name", "Instructor", "Schedule", "Room", "Credits"]
    draw.rectangle([(45, y-5), (w-45, y+22)], fill=(240, 245, 255))
    for i, (col, header) in enumerate(zip(cols, headers)):
        draw.text((col, y), header, font=font_bold, fill=(0, 0, 80))
    y += 30
    
    # Course rows
    for i, (code, name, instructor, schedule, room, credits) in enumerate(courses):
        if i % 2 == 1:
            draw.rectangle([(45, y-3), (w-45, y+20)], fill=(250, 250, 255))
        draw.text((cols[0], y), code, font=font_text, fill=(0, 0, 0))
        draw.text((cols[1], y), name, font=font_text, fill=(0, 0, 0))
        draw.text((cols[2], y), instructor, font=font_small, fill=(60, 60, 60))
        draw.text((cols[3], y), schedule, font=font_text, fill=(0, 0, 0))
        draw.text((cols[4], y), room, font=font_text, fill=(0, 0, 0))
        draw.text((cols[5], y), credits, font=font_text, fill=(0, 0, 0))
        y += 28
    
    y += 15
    draw.line([(50, y), (w-50, y)], fill=(0, 0, 0), width=1)
    y += 15
    
    # Summary
    draw.text((50, y), f"Total Credits: 16.0", font=font_bold, fill=(0, 0, 0))
    draw.text((250, y), f"Enrollment Status: Full-Time", font=font_text, fill=(0, 100, 0))
    
    # Add registrar seal
    add_school_seal(draw, w-100, h-140, school, size=50)
    
    # Footer
    draw.line([(50, h-70), (w-50, h-70)], fill=(200, 200, 200), width=1)
    draw.text((w//2, h-50), f"This schedule was generated on {today} for {semester} {year}", fill=(100, 100, 100), font=font_small, anchor="mm")
    draw.text((w//2, h-30), f"{school} - Office of the Registrar", fill=(100, 100, 100), font=font_small, anchor="mm")
    
    # Apply scan effect
    img = apply_scan_effect(img)
    
    # Output in requested format
    if output_format.lower() == "pdf":
        return image_to_pdf(img)
    else:
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()


def generate_tuition_receipt(first: str, last: str, school: str, dob: str,
                             student_info: StudentInfo = None, output_format: str = "pdf") -> bytes:
    """Generate tuition fee receipt/invoice - HIGH SUCCESS RATE document type
    
    Args:
        output_format: "pdf" or "png"
    """
    w, h = 850, 1100
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Use StudentInfo if provided
    if student_info:
        first = student_info.first
        last = student_info.last
        school = student_info.school
        dob = student_info.dob
        student_id = student_info.student_id
        semester = student_info.semester
        year = student_info.year
        academic_year = student_info.academic_year
    else:
        semester, year = get_current_semester()
        academic_year = get_academic_year()
        student_id = generate_student_number()
    
    today = datetime.now()
    invoice_date = (today - timedelta(days=random.randint(5, 30))).strftime("%B %d, %Y")
    due_date = (today + timedelta(days=random.randint(14, 45))).strftime("%B %d, %Y")
    invoice_num = f"INV-{year}{random.randint(100000, 999999)}"
    
    try:
        font_header = ImageFont.truetype("arial.ttf", 28)
        font_title = ImageFont.truetype("arial.ttf", 20)
        font_text = ImageFont.truetype("arial.ttf", 14)
        font_bold = ImageFont.truetype("arialbd.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 11)
        font_large_bold = ImageFont.truetype("arialbd.ttf", 24)
    except:
        font_header = font_title = font_text = font_bold = font_small = font_large_bold = ImageFont.load_default()
    
    # Header with school name
    draw.rectangle([(0, 0), (w, 100)], fill=(25, 55, 125))
    draw.text((w//2, 35), school.upper(), fill=(255, 255, 255), font=font_header, anchor="mm")
    draw.text((w//2, 70), "STUDENT ACCOUNTS - BURSAR'S OFFICE", fill=(200, 220, 255), font=font_title, anchor="mm")
    
    # Invoice title
    y = 130
    draw.text((w//2, y), "TUITION FEE STATEMENT", fill=(25, 55, 125), font=font_large_bold, anchor="mm")
    
    # Invoice info section
    y = 180
    draw.text((50, y), f"Invoice Number: {invoice_num}", fill=(0, 0, 0), font=font_bold)
    draw.text((w-50, y), f"Invoice Date: {invoice_date}", fill=(0, 0, 0), font=font_text, anchor="rm")
    y += 25
    draw.text((w-50, y), f"Due Date: {due_date}", fill=(150, 0, 0), font=font_bold, anchor="rm")
    
    # Student info box - use consistent student_id
    y += 40
    draw.rectangle([(50, y), (w-50, y+120)], outline=(200, 200, 200), width=1)
    draw.rectangle([(50, y), (w-50, y+30)], fill=(240, 245, 255))
    draw.text((w//2, y+15), "STUDENT INFORMATION", fill=(25, 55, 125), font=font_bold, anchor="mm")
    
    y += 45
    draw.text((70, y), f"Student Name: {first} {last}", fill=(0, 0, 0), font=font_text)
    y += 22
    draw.text((70, y), f"Student ID: {student_id}", fill=(0, 0, 0), font=font_text)
    draw.text((400, y), f"Date of Birth: {dob}", fill=(0, 0, 0), font=font_text)
    y += 22
    draw.text((70, y), f"Academic Year: {academic_year}", fill=(0, 0, 0), font=font_text)
    draw.text((400, y), f"Term: {semester} {year}", fill=(0, 100, 0), font=font_bold)
    
    # Charges section
    y += 60
    draw.text((50, y), "CHARGES", fill=(25, 55, 125), font=font_bold)
    y += 25
    
    # Table header
    draw.rectangle([(50, y), (w-50, y+25)], fill=(245, 245, 250))
    draw.text((60, y+5), "Description", font=font_bold, fill=(0, 0, 0))
    draw.text((w-150, y+5), "Amount", font=font_bold, fill=(0, 0, 0))
    y += 30
    
    # Charges rows
    tuition = random.randint(8000, 25000)
    fees = random.randint(500, 2000)
    tech_fee = random.randint(100, 500)
    total = tuition + fees + tech_fee
    
    charges = [
        (f"Tuition - {semester} {year} (Full-Time)", f"${tuition:,.2f}"),
        ("Student Activity Fee", f"${fees:,.2f}"),
        ("Technology Fee", f"${tech_fee:,.2f}"),
    ]
    
    for desc, amount in charges:
        draw.text((60, y), desc, font=font_text, fill=(0, 0, 0))
        draw.text((w-150, y), amount, font=font_text, fill=(0, 0, 0))
        y += 25
    
    # Total line
    y += 10
    draw.line([(50, y), (w-50, y)], fill=(0, 0, 0), width=2)
    y += 15
    draw.text((60, y), "TOTAL DUE", font=font_bold, fill=(0, 0, 0))
    draw.text((w-150, y), f"${total:,.2f}", font=font_bold, fill=(0, 0, 0))
    
    # Payment status
    y += 50
    paid = random.choice([True, True, True, False])  # 75% paid
    if paid:
        draw.rectangle([(50, y), (w-50, y+40)], fill=(230, 250, 230), outline=(0, 150, 0), width=2)
        draw.text((w//2, y+20), "✓ PAID IN FULL", fill=(0, 120, 0), font=font_large_bold, anchor="mm")
        pay_date = (today - timedelta(days=random.randint(1, 20))).strftime("%B %d, %Y")
        y += 50
        draw.text((w//2, y), f"Payment received on {pay_date}", fill=(0, 100, 0), font=font_text, anchor="mm")
    else:
        draw.rectangle([(50, y), (w-50, y+40)], fill=(255, 245, 230), outline=(200, 100, 0), width=2)
        draw.text((w//2, y+20), "BALANCE DUE", fill=(180, 80, 0), font=font_large_bold, anchor="mm")
    
    # Enrollment confirmation
    y += 70
    draw.rectangle([(50, y), (w-50, y+50)], fill=(240, 250, 240), outline=(0, 100, 0), width=1)
    draw.text((w//2, y+15), "ENROLLMENT STATUS: CURRENTLY ENROLLED", fill=(0, 100, 0), font=font_bold, anchor="mm")
    draw.text((w//2, y+35), f"{semester} SEMESTER {year}", fill=(0, 80, 0), font=font_text, anchor="mm")
    
    # Add seal
    add_school_seal(draw, w-100, h-180, school, size=55)
    
    # Footer
    draw.line([(50, h-100), (w-50, h-100)], fill=(200, 200, 200), width=1)
    draw.text((w//2, h-75), f"This statement is an official document of {school}", fill=(100, 100, 100), font=font_small, anchor="mm")
    draw.text((w//2, h-55), f"Generated on {today.strftime('%B %d, %Y')} | For academic year {academic_year}", fill=(100, 100, 100), font=font_small, anchor="mm")
    draw.text((w//2, h-35), "Questions? Contact the Bursar's Office", fill=(100, 100, 100), font=font_small, anchor="mm")
    
    # Apply scan effect
    img = apply_scan_effect(img)
    
    # Output in requested format
    if output_format.lower() == "pdf":
        return image_to_pdf(img)
    else:
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    draw.text((70, y), f"Academic Year: {academic_year}", fill=(0, 0, 0), font=font_text)
    draw.text((400, y), f"Term: {semester} {year}", fill=(0, 100, 0), font=font_bold)
    
    # Charges section
    y += 60
    draw.text((50, y), "CHARGES", fill=(25, 55, 125), font=font_bold)
    y += 25
    
    # Table header
    draw.rectangle([(50, y), (w-50, y+25)], fill=(245, 245, 250))
    draw.text((60, y+5), "Description", font=font_bold, fill=(0, 0, 0))
    draw.text((w-150, y+5), "Amount", font=font_bold, fill=(0, 0, 0))
    y += 30
    
    # Charges rows
    tuition = random.randint(8000, 25000)
    fees = random.randint(500, 2000)
    tech_fee = random.randint(100, 500)
    total = tuition + fees + tech_fee
    
    charges = [
        (f"Tuition - {semester} {year} (Full-Time)", f"${tuition:,.2f}"),
        ("Student Activity Fee", f"${fees:,.2f}"),
        ("Technology Fee", f"${tech_fee:,.2f}"),
    ]
    
    for desc, amount in charges:
        draw.text((60, y), desc, font=font_text, fill=(0, 0, 0))
        draw.text((w-150, y), amount, font=font_text, fill=(0, 0, 0))
        y += 25
    
    # Total line
    y += 10
    draw.line([(50, y), (w-50, y)], fill=(0, 0, 0), width=2)
    y += 15
    draw.text((60, y), "TOTAL DUE", font=font_bold, fill=(0, 0, 0))
    draw.text((w-150, y), f"${total:,.2f}", font=font_bold, fill=(0, 0, 0))
    
    # Payment status
    y += 50
    paid = random.choice([True, True, True, False])  # 75% paid
    if paid:
        draw.rectangle([(50, y), (w-50, y+40)], fill=(230, 250, 230), outline=(0, 150, 0), width=2)
        draw.text((w//2, y+20), "✓ PAID IN FULL", fill=(0, 120, 0), font=font_large_bold, anchor="mm")
        pay_date = (today - timedelta(days=random.randint(1, 20))).strftime("%B %d, %Y")
        y += 50
        draw.text((w//2, y), f"Payment received on {pay_date}", fill=(0, 100, 0), font=font_text, anchor="mm")
    else:
        draw.rectangle([(50, y), (w-50, y+40)], fill=(255, 245, 230), outline=(200, 100, 0), width=2)
        draw.text((w//2, y+20), "BALANCE DUE", fill=(180, 80, 0), font=font_large_bold, anchor="mm")
    
    # Enrollment confirmation
    y += 70
    draw.rectangle([(50, y), (w-50, y+50)], fill=(240, 250, 240), outline=(0, 100, 0), width=1)
    draw.text((w//2, y+15), "ENROLLMENT STATUS: CURRENTLY ENROLLED", fill=(0, 100, 0), font=font_bold, anchor="mm")
    draw.text((w//2, y+35), f"{semester} SEMESTER {year}", fill=(0, 80, 0), font=font_text, anchor="mm")
    
    # Add seal
    add_school_seal(draw, w-100, h-180, school, size=55)
    
    # Footer
    draw.line([(50, h-100), (w-50, h-100)], fill=(200, 200, 200), width=1)
    draw.text((w//2, h-75), f"This statement is an official document of {school}", fill=(100, 100, 100), font=font_small, anchor="mm")
    draw.text((w//2, h-55), f"Generated on {today.strftime('%B %d, %Y')} | For academic year {academic_year}", fill=(100, 100, 100), font=font_small, anchor="mm")
    draw.text((w//2, h-35), "Questions? Contact the Bursar's Office", fill=(100, 100, 100), font=font_small, anchor="mm")
    
    # Apply scan effect
    img = apply_scan_effect(img)
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_enrollment_letter(first: str, last: str, school: str, dob: str,
                               student_info: StudentInfo = None, output_format: str = "pdf") -> bytes:
    """Generate official enrollment verification letter
    
    Args:
        output_format: "pdf" or "png"
    """
    w, h = 850, 1100
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Use StudentInfo if provided
    if student_info:
        first = student_info.first
        last = student_info.last
        school = student_info.school
        dob = student_info.dob
        student_id = student_info.student_id
        semester = student_info.semester
        year = student_info.year
        academic_year = student_info.academic_year
    else:
        semester, year = get_current_semester()
        academic_year = get_academic_year()
        student_id = generate_student_number()
    
    today = datetime.now()
    letter_date = today.strftime("%B %d, %Y")
    
    try:
        font_header = ImageFont.truetype("arial.ttf", 24)
        font_title = ImageFont.truetype("arial.ttf", 18)
        font_text = ImageFont.truetype("arial.ttf", 13)
        font_bold = ImageFont.truetype("arialbd.ttf", 13)
        font_small = ImageFont.truetype("arial.ttf", 11)
        font_italic = ImageFont.truetype("ariali.ttf", 12)
    except:
        font_header = font_title = font_text = font_bold = font_small = font_italic = ImageFont.load_default()
    
    # Letterhead
    y = 50
    draw.text((w//2, y), school.upper(), fill=(25, 55, 125), font=font_header, anchor="mm")
    y += 35
    draw.text((w//2, y), "Office of the Registrar", fill=(80, 80, 80), font=font_title, anchor="mm")
    y += 25
    draw.line([(100, y), (w-100, y)], fill=(25, 55, 125), width=2)
    
    # Address block
    y += 30
    draw.text((50, y), "123 University Avenue", fill=(60, 60, 60), font=font_small)
    y += 18
    # Generate random US city/state
    cities = ["Cambridge, MA 02139", "Berkeley, CA 94720", "Ann Arbor, MI 48109", 
              "Austin, TX 78712", "Seattle, WA 98105", "New York, NY 10027"]
    draw.text((50, y), random.choice(cities), fill=(60, 60, 60), font=font_small)
    y += 18
    draw.text((50, y), "Tel: (555) 123-4567", fill=(60, 60, 60), font=font_small)
    
    # Date
    y = 200
    draw.text((w-50, y), letter_date, fill=(0, 0, 0), font=font_text, anchor="rm")
    
    # Subject
    y += 50
    draw.text((50, y), "TO WHOM IT MAY CONCERN:", fill=(0, 0, 0), font=font_bold)
    
    # Body - use consistent student_id
    y += 40
    
    # Enrollment paragraph
    lines = [
        f"This letter is to certify that {first} {last} (Student ID: {student_id})",
        f"is currently enrolled as a full-time student at {school}",
        f"for the {semester} Semester {year} (Academic Year {academic_year}).",
        "",
        "Student Information:",
    ]
    
    for line in lines:
        draw.text((50, y), line, fill=(0, 0, 0), font=font_text)
        y += 22
    
    # Student details box
    y += 10
    draw.rectangle([(70, y), (w-200, y+100)], outline=(200, 200, 200), width=1)
    y += 15
    details = [
        f"Name: {first} {last}",
        f"Date of Birth: {dob}",
        f"Student ID: {student_id}",
        f"Enrollment Status: Full-Time Student",
    ]
    for detail in details:
        draw.text((90, y), detail, fill=(0, 0, 0), font=font_text)
        y += 22
    
    y += 30
    
    # More text
    more_lines = [
        f"The student is expected to remain enrolled through the end of the current",
        f"academic term ending in {['May', 'August', 'December'][['SPRING', 'SUMMER', 'FALL'].index(semester)]} {year if semester != 'FALL' else year + 1}.",
        "",
        "This letter is issued upon the student's request for verification purposes.",
        "If you have any questions regarding this enrollment verification, please",
        "contact the Office of the Registrar at the address above.",
        "",
        "Sincerely,",
    ]
    
    for line in more_lines:
        draw.text((50, y), line, fill=(0, 0, 0), font=font_text)
        y += 22
    
    # Signature area
    y += 30
    draw.line([(50, y), (250, y)], fill=(0, 0, 0), width=1)
    y += 10
    registrar_names = ["Dr. Sarah Johnson", "Dr. Michael Chen", "Dr. Emily Williams", "Dr. James Anderson"]
    draw.text((50, y), random.choice(registrar_names), fill=(0, 0, 0), font=font_bold)
    y += 20
    draw.text((50, y), "University Registrar", fill=(60, 60, 60), font=font_text)
    
    # Add seal
    add_school_seal(draw, w-120, y-30, school, size=50)
    
    # Reference number
    ref_num = f"REF-{year}{random.randint(1000, 9999)}"
    draw.text((w-50, h-50), f"Reference: {ref_num}", fill=(120, 120, 120), font=font_small, anchor="rm")
    
    # Apply scan effect
    img = apply_scan_effect(img)
    
    # Output in requested format
    if output_format.lower() == "pdf":
        return image_to_pdf(img)
    else:
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()


# ============ VERIFIER ============
class GeminiVerifier:
    """Gemini Student Verification with enhanced features"""
    
    def __init__(self, url: str, proxy: str = None):
        self.url = url
        self.vid = self._parse_id(url)
        self.fingerprint = generate_fingerprint()
        
        # Use enhanced anti-detection session
        if HAS_ANTI_DETECT:
            self.client, self.lib_name = create_session(proxy)
            print(f"[INFO] Using {self.lib_name} for HTTP requests")
        else:
            proxy_url = None
            if proxy:
                if not proxy.startswith("http"):
                    proxy = f"http://{proxy}"
                proxy_url = proxy
            self.client = httpx.Client(timeout=30, proxy=proxy_url)
            self.lib_name = "httpx"
        
        self.org = None
    
    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()
    
    @staticmethod
    def _parse_id(url: str) -> Optional[str]:
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _request(self, method: str, endpoint: str, body: Dict = None) -> Tuple[Dict, int]:
        random_delay()
        try:
            # Use anti-detect headers if available
            headers = get_headers(for_sheerid=True) if HAS_ANTI_DETECT else {"Content-Type": "application/json"}
            resp = self.client.request(method, f"{SHEERID_API_URL}{endpoint}", 
                                       json=body, headers=headers)
            try:
                parsed = resp.json() if resp.text else {}
            except Exception:
                parsed = {"_text": resp.text}
            return parsed, resp.status_code
        except Exception as e:
            raise Exception(f"Request failed: {e}")
    
    def _upload_s3(self, url: str, data: bytes, content_type: str = "image/png") -> bool:
        # Different session implementations accept different kw names
        # Try several variants to maximize compatibility (curl_cffi, httpx, requests)
        attempts = []
        # First try: common httpx signature
        attempts.append(lambda: self.client.put(url, content=data, headers={"Content-Type": content_type}, timeout=60))
        # Second try: requests-like signature
        attempts.append(lambda: self.client.put(url, data=data, headers={"Content-Type": content_type}, timeout=60))
        # Third try: generic request method
        attempts.append(lambda: self.client.request("PUT", url, data=data, headers={"Content-Type": content_type}, timeout=60))

        last_exc = None
        for fn in attempts:
            try:
                resp = fn()
                if hasattr(resp, "status_code"):
                    if 200 <= resp.status_code < 300:
                        return True
                    try:
                        body = resp.json()
                    except Exception:
                        body = getattr(resp, "text", str(resp))
                    print(f"     ❗ S3 upload failed: HTTP {resp.status_code} | {body}")
                    return False
                else:
                    # If resp is not a requests-like object, treat success if truthy
                    if resp:
                        return True
                    return False
            except TypeError as e:
                last_exc = e
                continue
            except Exception as e:
                last_exc = e
                continue

        print(f"     ❗ S3 upload failed after attempts. Last error: {last_exc}")
        return False
    
    def check_link(self) -> Dict:
        """Check if verification link is valid"""
        if not self.vid:
            return {"valid": False, "error": "Invalid URL"}
        
        data, status = self._request("GET", f"/verification/{self.vid}")
        if status != 200:
            return {"valid": False, "error": f"HTTP {status}"}
        
        step = data.get("currentStep", "")
        # Accept multiple valid steps - handle re-upload after rejection
        valid_steps = ["collectStudentPersonalInfo", "docUpload", "sso"]
        if step in valid_steps:
            return {"valid": True, "step": step}
        elif step == "success":
            return {"valid": False, "error": "Already verified"}
        elif step == "pending":
            return {"valid": False, "error": "Already pending review"}
        return {"valid": False, "error": f"Invalid step: {step}"}
    
    def verify(self) -> Dict:
        """Run full verification"""
        if not self.vid:
            return {"success": False, "error": "Invalid verification URL"}
        
        try:
            # Check current step first
            check_data, check_status = self._request("GET", f"/verification/{self.vid}")
            current_step = check_data.get("currentStep", "") if check_status == 200 else ""
            
            # Generate info using StudentInfo for consistency
            first, last = generate_name()
            self.org = select_university()
            dob = generate_birth_date()
            
            # Create StudentInfo object for consistent data across all documents
            student_info = StudentInfo(
                first=first, 
                last=last, 
                school=self.org["name"],
                domain=self.org["domain"],
                dob=dob
            )
            
            # Email from student_info for consistency
            email = student_info.email
            
            print(f"\n   🎓 Student: {first} {last}")
            print(f"   📧 Email: {email}")
            print(f"   🏫 School: {self.org['name']}")
            print(f"   🎂 DOB: {dob}")
            print(f"   🔖 Student ID: {student_info.student_id}")
            print(f"   🔑 Verification ID: {self.vid[:20]}...")
            print(f"   📍 Starting step: {current_step}")
            # Check for available photos in assets/photos
            photos = get_sample_photos()
            photo_path = None
            if photos:
                photo_path = str(random.choice(photos))
                student_info.photo_path = photo_path
                print(f"   📸 Photo: {Path(photo_path).name}")
            
            # Pre-generate student ID card with consistent StudentInfo
            # This ensures the same information is used whether we upload it or not
            print("\n   ▶ Pre-generating student ID card (for consistency)...")
            student_id_bytes = generate_student_id(first, last, self.org["name"], 
                                                   student_info=student_info, 
                                                   photo_path=photo_path)
            # Save to temp file
            temp_dir = Path(__file__).parent / "temp"
            temp_dir.mkdir(exist_ok=True)
            student_id_path = temp_dir / f"student_id_{self.vid[:8]}.png"
            with open(student_id_path, "wb") as f:
                f.write(student_id_bytes)
            print(f"     ✅ Student ID saved: {student_id_path.name} ({len(student_id_bytes)/1024:.1f} KB)")
            
            # Step 1: Generate tuition receipt (BEST SUCCESS RATE)
            # Focus on tuition receipt only as it has highest approval rate
            doc_type = "tuition_receipt"
            print("\n   ▶ Step 1/5: Generating tuition fee receipt (BEST - PDF)...")
            doc = generate_tuition_receipt(first, last, self.org["name"], dob, 
                                           student_info=student_info, output_format="pdf")
            filename = "tuition_receipt.pdf"
            mime_type = "application/pdf"
            print(f"     📄 Type: {doc_type} | Format: PDF | Size: {len(doc)/1024:.1f} KB")
            
            # Step 2: Submit info (skip if already past this step)
            if current_step == "collectStudentPersonalInfo":
                print("   ▶ Step 2/3: Submitting student info...")
                body = {
                    "firstName": first, "lastName": last, "birthDate": dob,
                    "email": email, "phoneNumber": "",
                    "organization": {"id": self.org["id"], "idExtended": self.org["idExtended"], 
                                    "name": self.org["name"]},
                    "deviceFingerprintHash": self.fingerprint,
                    "locale": "en-US",
                    "metadata": {
                        "marketConsentValue": False,
                        "verificationId": self.vid,
                        "refererUrl": f"https://services.sheerid.com/verify/{PROGRAM_ID}/?verificationId={self.vid}",
                        "flags": '{"collect-info-step-email-first":"default","doc-upload-considerations":"default","doc-upload-may24":"default","doc-upload-redesign-use-legacy-message-keys":false,"docUpload-assertion-checklist":"default","font-size":"default","include-cvec-field-france-student":"not-labeled-optional"}',
                        "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount"
                    }
                }
                
                data, status = self._request("POST", f"/verification/{self.vid}/step/collectStudentPersonalInfo", body)

                if status != 200:
                    stats.record(self.org["name"], False)
                    print(f"     ❗ Submit failed: HTTP {status}")
                    print(f"     ❗ Response body: {data}")
                    return {"success": False, "error": f"Submit failed: {status} - {data}"}
                
                if data.get("currentStep") == "error":
                    stats.record(self.org["name"], False)
                    return {"success": False, "error": f"Error: {data.get('errorIds', [])}"}
                
                print(f"     📍 Current step: {data.get('currentStep')}")
                current_step = data.get("currentStep", "")
            elif current_step in ["docUpload", "sso"]:
                print("   ▶ Step 2/3: Skipping (already past info submission)...")
            else:
                print(f"   ▶ Step 2/3: Unknown step '{current_step}', attempting to continue...")
            
            # Step 3: Skip SSO if needed (PastKing logic)
            if current_step in ["sso", "collectStudentPersonalInfo"]:
                print("   ▶ Step 3/4: Skipping SSO...")
                self._request("DELETE", f"/verification/{self.vid}/step/sso")
            
            # Step 4: Upload document
            print("   ▶ Step 4/5: Uploading document...")
            upload_body = {"files": [{"fileName": filename, "mimeType": mime_type, "fileSize": len(doc)}]}
            data, status = self._request("POST", f"/verification/{self.vid}/step/docUpload", upload_body)
            
            if not data.get("documents"):
                stats.record(self.org["name"], False)
                return {"success": False, "error": "No upload URL"}
            
            upload_url = data["documents"][0].get("uploadUrl")
            if not self._upload_s3(upload_url, doc, content_type=mime_type):
                stats.record(self.org["name"], False)
                return {"success": False, "error": "Upload failed"}
            
            print("     ✅ Document uploaded!")
            
            # Step 5: Complete document upload (PastKing logic)
            print("   ▶ Step 5/5: Completing upload...")
            data, status = self._request("POST", f"/verification/{self.vid}/step/completeDocUpload")
            print(f"     ✅ Upload completed: {data.get('currentStep', 'pending')}")
            
            stats.record(self.org["name"], True)
            
            return {
                "success": True,
                "message": "Verification submitted! Wait 24-48h for review.",
                "student": f"{first} {last}",
                "email": email,
                "school": self.org["name"],
                "redirectUrl": data.get("redirectUrl")
            }
            
        except Exception as e:
            if self.org:
                stats.record(self.org["name"], False)
            return {"success": False, "error": str(e)}


# ============ MAIN ============
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Google One (Gemini) Student Verification Tool")
    parser.add_argument("url", nargs="?", help="Verification URL")
    parser.add_argument("--proxy", help="Proxy server (host:port or http://user:pass@host:port)")
    args = parser.parse_args()
    
    print()
    print("╔" + "═" * 56 + "╗")
    print("║" + " 🤖 Google One (Gemini) Verification Tool".center(56) + "║")
    print("║" + " SheerID Student Discount".center(56) + "║")
    print("╚" + "═" * 56 + "╝")
    print()
    
    # Get URL
    if args.url:
        url = args.url
    else:
        url = input("   Enter verification URL: ").strip()
    
    if not url or "sheerid.com" not in url:
        print("\n   ❌ Invalid URL. Must contain sheerid.com")
        return
    
    # Show proxy info
    if args.proxy:
        print(f"   🔒 Using proxy: {args.proxy}")
    
    print("\n   ⏳ Processing...")
    
    verifier = GeminiVerifier(url, proxy=args.proxy)
    
    # Check link first
    check = verifier.check_link()
    if not check.get("valid"):
        print(f"\n   ❌ Link Error: {check.get('error')}")
        return
    
    result = verifier.verify()
    
    print()
    print("─" * 58)
    if result.get("success"):
        print("   🎉 SUCCESS!")
        print(f"   👤 {result.get('student')}")
        print(f"   📧 {result.get('email')}")
        print(f"   🏫 {result.get('school')}")
        print()
        print("   ⏳ Wait 24-48 hours for manual review")
    else:
        print(f"   ❌ FAILED: {result.get('error')}")
    print("─" * 58)
    
    stats.print_stats()


def test_document_generation():
    """Test all document generation functions and save to test_output folder"""
    import os
    
    output_dir = Path(__file__).parent / "test_output"
    output_dir.mkdir(exist_ok=True)
    
    # Create photos folder for sample photos
    photos_dir = Path(__file__).parent / "assets" / "photos"
    photos_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 60)
    print("🧪 Testing Document Generation")
    print("=" * 60)
    
    # Create StudentInfo for consistent data across all documents
    student_info = StudentInfo(
        first="John",
        last="Smith",
        school="University of California, Berkeley",
        domain="berkeley.edu",
        dob="2003-05-15"
    )
    
    print(f"\n📋 Using consistent student info:")
    print(f"   Name: {student_info.first} {student_info.last}")
    print(f"   Student ID: {student_info.student_id}")
    print(f"   DOB: {student_info.dob}")
    print(f"   School: {student_info.school}")
    
    # Test cases: (name, output_format, generate_func, extra_kwargs)
    test_cases = [
        ("tuition_receipt", "pdf", generate_tuition_receipt, 
         {"first": "", "last": "", "school": "", "dob": "", "student_info": student_info, "output_format": "pdf"}),
        ("transcript", "pdf", generate_transcript,
         {"first": "", "last": "", "school": "", "dob": "", "student_info": student_info, "output_format": "pdf"}),
        ("class_schedule", "pdf", generate_class_schedule,
         {"first": "", "last": "", "school": "", "student_info": student_info, "output_format": "pdf"}),
        ("student_id", "png", generate_student_id,
         {"first": "", "last": "", "school": "", "student_info": student_info}),
        ("enrollment_letter", "pdf", generate_enrollment_letter,
         {"first": "", "last": "", "school": "", "dob": "", "student_info": student_info, "output_format": "pdf"}),
    ]
    
    for name, output_format, func, kwargs in test_cases:
        try:
            print(f"\n📄 Generating {name} ({output_format.upper()})...")
            doc_bytes = func(**kwargs)
            
            # Save to file
            filepath = output_dir / f"{name}.{output_format}"
            with open(filepath, "wb") as f:
                f.write(doc_bytes)
            
            print(f"   ✅ Success! Size: {len(doc_bytes)/1024:.1f} KB")
            print(f"   📁 Saved to: {filepath}")
        except Exception as e:
            import traceback
            print(f"   ❌ Failed: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"✅ All documents generated in: {output_dir}")
    print(f"💡 To use custom photos for student ID, place photos in: {photos_dir}")
    print("=" * 60)



if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_document_generation()
    else:
        main()
