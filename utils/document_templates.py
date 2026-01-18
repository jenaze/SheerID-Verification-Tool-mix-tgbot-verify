"""Universal Document Templates for Student/Teacher Verification

Provides multiple document types and university/school district templates
to increase diversity and realism of generated verification documents.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from enum import Enum


class DocumentType(Enum):
    """Types of documents that can be generated"""
    CLASS_SCHEDULE = "class_schedule"
    TUITION_RECEIPT = "tuition_receipt"
    ENROLLMENT_VERIFICATION = "enrollment_verification"
    EMPLOYMENT_VERIFICATION = "employment_verification"
    PAYROLL_STUB = "payroll_stub"
    TEACHER_DASHBOARD = "teacher_dashboard"


# ============================================================================
# UNIVERSITY CONFIGURATIONS (for Student Verification)
# ============================================================================

UNIVERSITIES = {
    'mit': {
        'name': 'Massachusetts Institute of Technology',
        'short_name': 'MIT',
        'email_domain': 'mit.edu',
        'primary_color': '#A31F34',  # MIT Red
        'secondary_color': '#8A8B8C',  # MIT Gray
        'system_name': 'MIT Atlas',
        'logo_text': 'MIT',
        'id_format': '9_digits',  # 9-digit numeric ID
        'id_prefix': '',
        'id_length': 9,
        'portal_name': 'Student Financial Services',
    },
    'stanford': {
        'name': 'Stanford University',
        'short_name': 'Stanford',
        'email_domain': 'stanford.edu',
        'primary_color': '#8C1515',  # Cardinal Red
        'secondary_color': '#2E2D29',  # Cool Grey
        'system_name': 'Axess',
        'logo_text': 'Stanford',
        'id_format': '8_digits',  # 8-digit numeric ID
        'id_prefix': '',
        'id_length': 8,
        'portal_name': 'Student Services',
    },
    'berkeley': {
        'name': 'University of California, Berkeley',
        'short_name': 'UC Berkeley',
        'email_domain': 'berkeley.edu',
        'primary_color': '#003262',  # Berkeley Blue
        'secondary_color': '#FDB515',  # California Gold
        'system_name': 'CalCentral',
        'logo_text': 'Berkeley',
        'id_format': 'sid_8_digits',  # SID: + 8 digits (starts with 3)
        'id_prefix': '3',
        'id_length': 8,
        'portal_name': 'Cal Student Central',
    },
    'cmu': {
        'name': 'Carnegie Mellon University',
        'short_name': 'CMU',
        'email_domain': 'andrew.cmu.edu',
        'primary_color': '#C41230',  # Carnegie Red
        'secondary_color': '#4B4B4B',  # Gray
        'system_name': 'Student Information Online',
        'logo_text': 'CMU',
        'id_format': '7_digits',  # 7-digit numeric ID
        'id_prefix': '',
        'id_length': 7,
        'portal_name': 'The HUB',
    },
    'columbia': {
        'name': 'Columbia University',
        'short_name': 'Columbia',
        'email_domain': 'columbia.edu',
        'primary_color': '#B9D9EB',  # Columbia Blue
        'secondary_color': '#FFFFFF',
        'system_name': 'SSOL',
        'logo_text': 'Columbia',
        'id_format': 'uni_digits',  # uni + 4-6 digits
        'id_prefix': 'uni',
        'id_length': 6,  # variable length
        'portal_name': 'Student Financial Services',
    },
    'nyu': {
        'name': 'New York University',
        'short_name': 'NYU',
        'email_domain': 'nyu.edu',
        'primary_color': '#57068C',  # NYU Violet
        'secondary_color': '#333333',
        'system_name': 'Albert',
        'logo_text': 'NYU',
        'id_format': 'N_8_digits',  # N + 8 digits
        'id_prefix': 'N',
        'id_length': 8,
        'portal_name': 'Bursar',
    },
    'umich': {
        'name': 'University of Michigan',
        'short_name': 'U-M',
        'email_domain': 'umich.edu',
        'primary_color': '#00274C',  # Michigan Blue
        'secondary_color': '#FFCB05',  # Maize
        'system_name': 'Wolverine Access',
        'logo_text': 'Michigan',
        'id_format': '8_digits',  # 8-digit UMID
        'id_prefix': '',
        'id_length': 8,
        'portal_name': 'Office of the Registrar',
    },
    'gatech': {
        'name': 'Georgia Institute of Technology',
        'short_name': 'Georgia Tech',
        'email_domain': 'gatech.edu',
        'primary_color': '#003057',  # Tech Navy
        'secondary_color': '#B3A369',  # Tech Gold
        'system_name': 'OSCAR',
        'logo_text': 'GT',
        'id_format': '9_start_9',  # 9 digits starting with 9
        'id_prefix': '9',
        'id_length': 9,
        'portal_name': 'Bursar\'s Office',
    },
}


# ============================================================================
# SCHOOL DISTRICT CONFIGURATIONS (for Teacher Verification)
# ============================================================================

SCHOOL_DISTRICTS = {
    'springfield': {
        'name': 'Springfield School District',
        'short_name': 'Springfield SD',
        'email_domain': 'springfieldschools.org',
        'primary_color': '#0056b3',
        'secondary_color': '#6c757d',
        'system_name': 'Employee Access Center',
        'logo_text': 'SD',
        'id_prefix': 'E-',
        'id_length': 7,
    },
    'jefferson': {
        'name': 'Jefferson County Public Schools',
        'short_name': 'JCPS',
        'email_domain': 'jefferson.kyschools.us',
        'primary_color': '#1a5490',
        'secondary_color': '#f7941d',
        'system_name': 'Skyward Employee Access',
        'logo_text': 'JCPS',
        'id_prefix': 'T',
        'id_length': 6,
    },
    'oakland': {
        'name': 'Oakland Unified School District',
        'short_name': 'OUSD',
        'email_domain': 'ousd.org',
        'primary_color': '#00486C',
        'secondary_color': '#ED8B00',
        'system_name': 'PeopleSoft Portal',
        'logo_text': 'OUSD',
        'id_prefix': '',
        'id_length': 6,
    },
    'seattle': {
        'name': 'Seattle Public Schools',
        'short_name': 'Seattle PS',
        'email_domain': 'seattleschools.org',
        'primary_color': '#00573F',
        'secondary_color': '#E84A27',
        'system_name': 'Workforce Central',
        'logo_text': 'SPS',
        'id_prefix': 'EMP',
        'id_length': 5,
    },
    'boston': {
        'name': 'Boston Public Schools',
        'short_name': 'BPS',
        'email_domain': 'bostonpublicschools.org',
        'primary_color': '#003D7A',
        'secondary_color': '#FFB81C',
        'system_name': 'BPS Connect',
        'logo_text': 'BPS',
        'id_prefix': 'B',
        'id_length': 7,
    },
    'chicago': {
        'name': 'Chicago Public Schools',
        'short_name': 'CPS',
        'email_domain': 'cps.edu',
        'primary_color': '#2A4B9B',
        'secondary_color': '#C4122F',
        'system_name': 'CPS Portal',
        'logo_text': 'CPS',
        'id_prefix': '',
        'id_length': 6,
    },
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_university_id(university_key: str) -> str:
    """Generate a realistic student ID for the given university based on id_format"""
    config = UNIVERSITIES[university_key]
    id_format = config.get('id_format', '8_digits')
    
    if id_format == '9_digits':
        # MIT, etc: 9-digit numeric ID
        return ''.join([str(random.randint(0, 9)) for _ in range(9)])
    elif id_format == '8_digits':
        # Stanford, UMich: 8-digit numeric ID
        return ''.join([str(random.randint(0, 9)) for _ in range(8)])
    elif id_format == '7_digits':
        # CMU: 7-digit numeric ID
        return ''.join([str(random.randint(0, 9)) for _ in range(7)])
    elif id_format == 'uni_digits':
        # Columbia: uni + 4-6 random digits
        num_len = random.choice([4, 5, 6])
        numbers = ''.join([str(random.randint(0, 9)) for _ in range(num_len)])
        return f"uni{numbers}"
    elif id_format == 'N_8_digits':
        # NYU: N + 8 digits
        numbers = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return f"N{numbers}"
    elif id_format == 'sid_8_digits':
        # UC Berkeley: 8 digits starting with 3
        numbers = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        return f"3{numbers}"
    elif id_format == '9_start_9':
        # Georgia Tech: 9 digits starting with 9
        numbers = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return f"9{numbers}"
    else:
        # Default: 8-digit numeric ID
        return ''.join([str(random.randint(0, 9)) for _ in range(8)])


def generate_university_email(first_name: str, last_name: str, university_key: str) -> str:
    """Generate an email for the given university"""
    config = UNIVERSITIES[university_key]
    domain = config['email_domain']
    
    # Different universities have different email formats
    if university_key in ['mit', 'cmu']:
        # MIT/CMU often use first initial + last name
        email_user = f"{first_name[0].lower()}{last_name.lower()}"
    elif university_key == 'columbia':
        # Columbia uses first initial + last name + numbers
        digits = ''.join([str(random.randint(0, 9)) for _ in range(random.choice([3, 4]))])
        email_user = f"{first_name[0].lower()}{last_name.lower()}{digits}"
    else:
        # Most use firstname.lastname or variations
        separator = random.choice(['.', '_', ''])
        digits = ''.join([str(random.randint(0, 9)) for _ in range(random.choice([0, 2, 3]))])
        email_user = f"{first_name.lower()}{separator}{last_name.lower()}{digits}"
    
    return f"{email_user}@{domain}"


def generate_district_id(district_key: str) -> str:
    """Generate a random employee ID for the given school district"""
    config = SCHOOL_DISTRICTS[district_key]
    prefix = config['id_prefix']
    length = config['id_length']
    
    numbers = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return f"{prefix}{numbers}"


def generate_district_email(first_name: str, last_name: str, district_key: str) -> str:
    """Generate an email for the given school district"""
    config = SCHOOL_DISTRICTS[district_key]
    domain = config['email_domain']
    
    separator = random.choice(['.', '_'])
    email_user = f"{first_name.lower()}{separator}{last_name.lower()}"
    
    return f"{email_user}@{domain}"


def get_random_university() -> Tuple[str, Dict]:
    """Get a random university configuration"""
    key = random.choice(list(UNIVERSITIES.keys()))
    return key, UNIVERSITIES[key]


def get_random_district() -> Tuple[str, Dict]:
    """Get a random school district configuration"""
    key = random.choice(list(SCHOOL_DISTRICTS.keys()))
    return key, SCHOOL_DISTRICTS[key]


def get_random_major() -> str:
    """Get a random academic major"""
    majors = [
        'Computer Science (BS)',
        'Software Engineering (BS)',
        'Information Sciences and Technology (BS)',
        'Data Science (BS)',
        'Electrical Engineering (BS)',
        'Computer Engineering (BS)',
        'Mechanical Engineering (BS)',
        'Business Administration (BS)',
        'Economics (BA)',
        'Psychology (BA)',
        'Mathematics (BS)',
        'Physics (BS)',
        'Chemistry (BS)',
        'Biology (BS)',
        'Political Science (BA)',
        'English Literature (BA)',
    ]
    return random.choice(majors)


def get_random_term() -> Tuple[str, str]:
    """Get current academic term with realistic date ranges"""
    now = datetime.now()
    year = now.year
    month = now.month
    
    # Determine current semester based on date
    if month >= 8:  # Fall semester (Aug-Dec)
        semester = 'Fall'
        sem_year = year
        # Randomize start/end slightly for realism
        start_day = random.randint(18, 26)
        end_day = random.randint(10, 16)
        date_range = f'Aug {start_day} - Dec {end_day}'
    elif month >= 5:  # Summer semester (May-Aug)
        semester = 'Summer'
        sem_year = year
        start_day = random.randint(15, 22)
        end_day = random.randint(5, 12)
        date_range = f'May {start_day} - Aug {end_day}'
    else:  # Spring semester (Jan-May)
        semester = 'Spring'
        sem_year = year
        start_day = random.randint(10, 18)
        end_day = random.randint(5, 12)
        date_range = f'Jan {start_day} - May {end_day}'
    
    return (f'{semester} {sem_year}', date_range)


def get_random_courses(count: int = 5) -> List[Dict]:
    """Generate realistic course schedule with CRN, section numbers, etc."""
    # Course database with realistic 4-digit course codes
    course_database = [
        # Computer Science
        {'dept': 'CSCI', 'num': '1101', 'title': 'Introduction to Programming', 'units': 3},
        {'dept': 'CSCI', 'num': '2201', 'title': 'Data Structures and Algorithms', 'units': 4},
        {'dept': 'CSCI', 'num': '3315', 'title': 'Database Management Systems', 'units': 3},
        {'dept': 'CSCI', 'num': '3420', 'title': 'Computer Architecture', 'units': 3},
        {'dept': 'CSCI', 'num': '4510', 'title': 'Operating Systems', 'units': 3},
        # Mathematics
        {'dept': 'MATH', 'num': '2210', 'title': 'Calculus III', 'units': 4},
        {'dept': 'MATH', 'num': '2415', 'title': 'Linear Algebra', 'units': 3},
        {'dept': 'MATH', 'num': '3320', 'title': 'Differential Equations', 'units': 3},
        {'dept': 'STAT', 'num': '3180', 'title': 'Probability and Statistics', 'units': 3},
        # Physics
        {'dept': 'PHYS', 'num': '2211', 'title': 'Physics I: Mechanics', 'units': 4},
        {'dept': 'PHYS', 'num': '2326', 'title': 'Physics II: E&M', 'units': 4},
        # Humanities
        {'dept': 'ENGL', 'num': '1302', 'title': 'Rhetoric and Composition', 'units': 3},
        {'dept': 'ENGL', 'num': '2311', 'title': 'Technical Writing', 'units': 3},
        {'dept': 'PHIL', 'num': '2303', 'title': 'Introduction to Philosophy', 'units': 3},
        {'dept': 'HIST', 'num': '1311', 'title': 'United States History to 1877', 'units': 3},
        # Economics & Business
        {'dept': 'ECON', 'num': '2301', 'title': 'Principles of Microeconomics', 'units': 3},
        {'dept': 'ECON', 'num': '2302', 'title': 'Principles of Macroeconomics', 'units': 3},
        {'dept': 'ACCT', 'num': '2301', 'title': 'Financial Accounting', 'units': 3},
        # Natural Sciences
        {'dept': 'CHEM', 'num': '1311', 'title': 'General Chemistry I', 'units': 4},
        {'dept': 'BIOL', 'num': '1406', 'title': 'General Biology I', 'units': 4},
        # Social Sciences
        {'dept': 'PSYC', 'num': '2301', 'title': 'Introduction to Psychology', 'units': 3},
        {'dept': 'SOCI', 'num': '1301', 'title': 'Introduction to Sociology', 'units': 3},
    ]
    
    selected = random.sample(course_database, min(count, len(course_database)))
    
    # Real university building names
    buildings = [
        'Engineering Building', 'Science Hall', 'Liberal Arts', 'Business Building',
        'Library', 'Humanities Hall', 'Natural Sciences', 'McBryde Hall',
        'Whittemore Hall', 'Derring Hall', 'Pamplin Hall', 'Randolph Hall'
    ]
    
    # Add realistic schedule details
    for course in selected:
        # Generate section number (001-020) and CRN (10000-99999)
        section = f"{random.randint(1, 20):03d}"
        crn = random.randint(10000, 99999)
        
        # Build course code in format: DEPT NUM-SECTION
        course['code'] = f"{course['dept']} {course['num']}-{section}"
        course['section'] = section
        course['crn'] = crn
        course['class_number'] = crn  # Keep for backward compatibility
        
        # Generate realistic class times
        # MWF classes are 50 minutes, TR classes are 75 minutes
        days_options = ['MWF', 'TR', 'MW', 'TRF']
        days = random.choice(days_options)
        
        # Common class start times
        start_hours = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        start_minutes = [0, 30] if days in ['TR'] else [0, 10, 20]
        
        hour = random.choice(start_hours)
        minute = random.choice(start_minutes)
        
        # Calculate end time based on class pattern
        if days in ['MWF']:
            duration_mins = 50  # 50-minute classes
        elif days in ['TR']:
            duration_mins = 75  # 75-minute classes
        else:
            duration_mins = random.choice([50, 75])
        
        end_hour = hour + (minute + duration_mins) // 60
        end_minute = (minute + duration_mins) % 60
        
        course['time'] = f"{days} {hour:02d}:{minute:02d} - {end_hour:02d}:{end_minute:02d}"
        course['room'] = f"{random.choice(buildings)} {random.randint(100, 499)}"
    
    return selected


def get_random_tuition_amount() -> float:
    """Get a random tuition amount"""
    # Typical semester tuition ranges for US universities
    return random.uniform(15000, 35000)


def get_tuition_breakdown(total: float = None) -> List[Tuple[str, float]]:
    """
    Generate realistic tuition breakdown with line items
    
    Returns list of (item_name, amount) tuples
    """
    if total is None:
        total = get_random_tuition_amount()
    
    items = []
    
    # Main tuition (85-92% of total)
    tuition_pct = random.uniform(0.85, 0.92)
    tuition = total * tuition_pct
    items.append(("Tuition", round(tuition, 2)))
    
    remaining = total - tuition
    
    # Standard university fees
    fee_types = [
        ("Technology Fee", random.uniform(400, 600)),
        ("Student Services Fee", random.uniform(300, 450)),
        ("Recreation Center Fee", random.uniform(150, 250)),
        ("Health Services Fee", random.uniform(100, 200)),
        ("Campus Security Fee", random.uniform(50, 100)),
        ("Library Fee", random.uniform(50, 150)),
    ]
    
    # Randomly select 4-6 fees
    selected_fees = random.sample(fee_types, random.randint(4, min(6, len(fee_types))))
    
    # Calculate current fee total
    fee_total = sum(f[1] for f in selected_fees)
    
    # Adjust to match remaining amount
    if fee_total > 0:
        adjustment_factor = remaining / fee_total
        for name, amount in selected_fees:
            adjusted_amount = round(amount * adjustment_factor, 2)
            items.append((name, adjusted_amount))
    
    return items


def get_academic_year() -> str:
    """Get current academic year (e.g., '2025-2026')"""
    now = datetime.now()
    if now.month >= 8:  # Fall semester starts new academic year
        return f"{now.year}-{now.year + 1}"
    else:
        return f"{now.year - 1}-{now.year}"


# Export commonly used functions
__all__ = [
    'DocumentType',
    'UNIVERSITIES',
    'SCHOOL_DISTRICTS',
    'generate_university_id',
    'generate_university_email',
    'generate_district_id',
    'generate_district_email',
    'get_random_university',
    'get_random_district',
    'get_random_major',
    'get_random_term',
    'get_random_courses',
    'get_random_tuition_amount',
    'get_tuition_breakdown',
    'get_academic_year',
]
