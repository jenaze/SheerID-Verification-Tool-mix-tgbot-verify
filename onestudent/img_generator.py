"""Student Document Image Generators

Generates multiple types of student verification documents with:
- Consistent student information via StudentInfo class
- University-specific styling (colors, ID formats)
- Dynamic semester/date information
- Realistic visual effects

Document Types:
1. Tuition Receipt (PDF) - Highest success rate
2. Academic Transcript (PNG)
3. Student ID Card (PNG)
"""

import random
import sys
import os
from datetime import datetime, timedelta
from io import BytesIO
from typing import List, Tuple

# Add parent directory for utils imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise RuntimeError("Pillow required: pip install Pillow")

from .student_info import StudentInfo
from .name_generator import get_random_courses, get_document_date, generate_realistic_gpa
from utils.image_effects import apply_advanced_realism


def _image_to_pdf(img: Image.Image) -> bytes:
    """Convert PIL Image to PDF bytes"""
    buf = BytesIO()
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


def generate_tuition_receipt(student_info: StudentInfo) -> bytes:
    """
    Generate tuition fee receipt/invoice - HIGHEST SUCCESS RATE document
    
    Uses university-specific colors from StudentInfo
    Returns PDF bytes
    """
    w, h = 850, 1100
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Get colors from StudentInfo
    primary_color = student_info.primary_color
    secondary_color = student_info.secondary_color
    
    today = datetime.now()
    invoice_date = (today - timedelta(days=random.randint(5, 30))).strftime("%B %d, %Y")
    due_date = (today + timedelta(days=random.randint(14, 45))).strftime("%B %d, %Y")
    invoice_num = f"INV-{student_info.year}{random.randint(100000, 999999)}"
    
    try:
        font_header = ImageFont.truetype("arial.ttf", 28)
        font_title = ImageFont.truetype("arial.ttf", 20)
        font_text = ImageFont.truetype("arial.ttf", 14)
        font_bold = ImageFont.truetype("arialbd.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 11)
        font_large_bold = ImageFont.truetype("arialbd.ttf", 24)
    except:
        font_header = font_title = font_text = font_bold = font_small = font_large_bold = ImageFont.load_default()
    
    # Header with school name - university colors
    draw.rectangle([(0, 0), (w, 100)], fill=primary_color)
    draw.text((w//2, 35), student_info.school_name.upper(), fill=(255, 255, 255), font=font_header, anchor="mm")
    draw.text((w//2, 70), f"STUDENT ACCOUNTS - {student_info.portal_name.upper()}", fill=(200, 220, 255), font=font_title, anchor="mm")
    
    # Invoice title
    y = 130
    draw.text((w//2, y), "TUITION FEE STATEMENT", fill=primary_color, font=font_large_bold, anchor="mm")
    
    # Invoice info section
    y = 180
    draw.text((50, y), f"Invoice Number: {invoice_num}", fill=(0, 0, 0), font=font_bold)
    draw.text((w-50, y), f"Invoice Date: {invoice_date}", fill=(0, 0, 0), font=font_text, anchor="rm")
    y += 25
    draw.text((w-50, y), f"Due Date: {due_date}", fill=(150, 0, 0), font=font_bold, anchor="rm")
    
    # Student info box - CONSISTENT student_id from StudentInfo
    y += 40
    draw.rectangle([(50, y), (w-50, y+120)], outline=(200, 200, 200), width=1)
    draw.rectangle([(50, y), (w-50, y+30)], fill=(240, 245, 255))
    draw.text((w//2, y+15), "STUDENT INFORMATION", fill=primary_color, font=font_bold, anchor="mm")
    
    y += 45
    draw.text((70, y), f"Student Name: {student_info.full_name}", fill=(0, 0, 0), font=font_text)
    y += 22
    draw.text((70, y), f"Student ID: {student_info.student_id}", fill=(0, 0, 0), font=font_text)
    draw.text((400, y), f"Date of Birth: {student_info.birth_date}", fill=(0, 0, 0), font=font_text)
    y += 22
    draw.text((70, y), f"Academic Year: {student_info.academic_year}", fill=(0, 0, 0), font=font_text)
    draw.text((400, y), f"Term: {student_info.semester} {student_info.year}", fill=(0, 100, 0), font=font_bold)
    
    # Charges section
    y += 60
    draw.text((50, y), "CHARGES", fill=primary_color, font=font_bold)
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
        (f"Tuition - {student_info.semester} {student_info.year} (Full-Time)", f"${tuition:,.2f}"),
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
    
    # Payment status - mostly PAID
    y += 50
    draw.rectangle([(50, y), (w-50, y+40)], fill=(230, 250, 230), outline=(0, 150, 0), width=2)
    draw.text((w//2, y+20), "✓ PAID IN FULL", fill=(0, 120, 0), font=font_large_bold, anchor="mm")
    pay_date = (today - timedelta(days=random.randint(1, 20))).strftime("%B %d, %Y")
    y += 50
    draw.text((w//2, y), f"Payment received on {pay_date}", fill=(0, 100, 0), font=font_text, anchor="mm")
    
    # Enrollment confirmation
    y += 40
    draw.rectangle([(50, y), (w-50, y+50)], fill=(240, 250, 240), outline=(0, 100, 0), width=1)
    draw.text((w//2, y+15), "ENROLLMENT STATUS: CURRENTLY ENROLLED", fill=(0, 100, 0), font=font_bold, anchor="mm")
    draw.text((w//2, y+35), f"{student_info.semester} SEMESTER {student_info.year}", fill=(0, 80, 0), font=font_text, anchor="mm")
    
    # Footer
    draw.line([(50, h-100), (w-50, h-100)], fill=(200, 200, 200), width=1)
    draw.text((w//2, h-75), f"This statement is an official document of {student_info.school_name}", fill=(100, 100, 100), font=font_small, anchor="mm")
    draw.text((w//2, h-55), f"Generated on {today.strftime('%B %d, %Y')} | For academic year {student_info.academic_year}", fill=(100, 100, 100), font=font_small, anchor="mm")
    draw.text((w//2, h-35), f"Questions? Contact {student_info.portal_name}", fill=(100, 100, 100), font=font_small, anchor="mm")
    
    return _image_to_pdf(img)


def generate_academic_transcript(student_info: StudentInfo) -> bytes:
    """
    Generate academic transcript document with university-specific styling
    Returns PNG bytes
    """
    w, h = 850, 1100
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    primary_color = student_info.primary_color
    today = get_document_date()
    
    try:
        font_header = ImageFont.truetype("arial.ttf", 32)
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_text = ImageFont.truetype("arial.ttf", 16)
        font_bold = ImageFont.truetype("arialbd.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_header = font_title = font_text = font_bold = font_small = ImageFont.load_default()
    
    # Header with school colors
    draw.rectangle([(0, 0), (w, 120)], fill=(245, 245, 250))
    draw.text((w//2, 40), student_info.school_name.upper(), fill=primary_color, font=font_header, anchor="mm")
    draw.text((w//2, 80), "OFFICIAL ACADEMIC TRANSCRIPT", fill=(50, 50, 80), font=font_title, anchor="mm")
    draw.line([(50, 115), (w-50, 115)], fill=primary_color, width=3)
    
    # Document Info
    y = 135
    draw.text((w-50, y), f"Document Date: {today}", fill=(0, 100, 0), font=font_bold, anchor="rm")
    y += 25
    draw.text((w-50, y), f"Academic Year: {student_info.academic_year}", fill=(0, 0, 0), font=font_text, anchor="rm")
    
    # Student Info - CONSISTENT from StudentInfo
    y = 170
    draw.text((50, y), f"Student Name: {student_info.full_name}", fill=(0, 0, 0), font=font_bold)
    y += 30
    draw.text((50, y), f"Student ID: {student_info.student_id}", fill=(0, 0, 0), font=font_text)
    draw.text((w-300, y), f"Date of Birth: {student_info.birth_date}", fill=(0, 0, 0), font=font_text)
    y += 40
    
    # Current Enrollment Status
    draw.rectangle([(50, y), (w-50, y+50)], fill=(230, 245, 230), outline=(0, 100, 0), width=2)
    draw.text((w//2, y+15), "ENROLLMENT STATUS: CURRENTLY ENROLLED", fill=(0, 100, 0), font=font_bold, anchor="mm")
    draw.text((w//2, y+38), f"{student_info.semester} SEMESTER {student_info.year}", fill=(0, 80, 0), font=font_bold, anchor="mm")
    y += 75
    
    # Current semester courses
    draw.text((50, y), f"{student_info.semester} {student_info.year} - Course Schedule", font=font_bold, fill=primary_color)
    y += 30
    
    courses = get_random_courses(5)
    
    # Table header
    draw.rectangle([(50, y), (w-50, y+25)], fill=(240, 240, 250))
    draw.text((60, y+5), "Course Code", font=font_bold, fill=(0, 0, 0))
    draw.text((200, y+5), "Course Title", font=font_bold, fill=(0, 0, 0))
    draw.text((550, y+5), "Credits", font=font_bold, fill=(0, 0, 0))
    draw.text((650, y+5), "Status", font=font_bold, fill=(0, 0, 0))
    y += 30
    
    total_credits = 0
    for code, title, instructor in courses:
        credits = random.choice(["3.0", "3.0", "4.0"])
        total_credits += float(credits)
        
        draw.text((60, y), code, font=font_text, fill=(0, 0, 0))
        draw.text((200, y), title, font=font_text, fill=(0, 0, 0))
        draw.text((550, y), credits, font=font_text, fill=(0, 0, 0))
        draw.text((650, y), "In Progress", font=font_text, fill=(0, 100, 0))
        y += 28
    
    y += 10
    draw.line([(50, y), (w-50, y)], fill=(0, 0, 0), width=1)
    y += 20
    
    # Summary
    gpa = generate_realistic_gpa()
    draw.text((50, y), f"Total Credits This Semester: {total_credits}", font=font_text, fill=(0, 0, 0))
    draw.text((400, y), f"Cumulative GPA: {gpa}", font=font_bold, fill=(0, 0, 0))
    y += 25
    draw.text((50, y), "Academic Standing: Good Standing", font=font_text, fill=(0, 100, 0))
    
    # Footer
    draw.line([(50, h-100), (w-50, h-100)], fill=(200, 200, 200), width=1)
    draw.text((w//2, h-70), f"This is an official document of {student_info.school_name}", fill=(100, 100, 100), font=font_small, anchor="mm")
    draw.text((w//2, h-50), f"Generated on {today} | Valid for verification purposes", fill=(100, 100, 100), font=font_small, anchor="mm")
    draw.text((w//2, h-30), "This document is electronically generated and valid without signature.", fill=(150, 150, 150), font=font_small, anchor="mm")
    
    # Apply realism effects
    buf = BytesIO()
    img.save(buf, format="PNG")
    return apply_advanced_realism(buf.getvalue())


def generate_student_id_card(student_info: StudentInfo) -> bytes:
    """
    Generate student ID card with university-specific styling
    Returns PNG bytes
    """
    w, h = 650, 420
    bg_color = (random.randint(248, 255), random.randint(248, 255), random.randint(248, 255))
    img = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(img)
    
    primary_color = student_info.primary_color
    
    try:
        font_lg = ImageFont.truetype("arial.ttf", 24)
        font_md = ImageFont.truetype("arial.ttf", 16)
        font_sm = ImageFont.truetype("arial.ttf", 12)
        font_bold = ImageFont.truetype("arialbd.ttf", 18)
        font_name = ImageFont.truetype("arialbd.ttf", 22)
    except:
        font_lg = font_md = font_sm = font_bold = font_name = ImageFont.load_default()
    
    # Header with university color
    draw.rectangle([(0, 0), (w, 75)], fill=primary_color)
    draw.text((w//2, 25), student_info.school_name.upper(), fill=(255, 255, 255), font=font_lg, anchor="mm")
    draw.text((w//2, 55), "STUDENT IDENTIFICATION CARD", fill=(200, 220, 255), font=font_sm, anchor="mm")
    
    # Academic year badge
    draw.rectangle([(w-130, 85), (w-10, 115)], fill=(0, 100, 0), outline=(0, 80, 0))
    draw.text((w-70, 100), f"AY {student_info.academic_year}", fill=(255, 255, 255), font=font_sm, anchor="mm")
    
    # Photo placeholder
    draw.rectangle([(25, 95), (155, 260)], outline=(100, 100, 100), width=2, fill=(230, 230, 235))
    draw.text((90, 175), "PHOTO", fill=(150, 150, 150), font=font_md, anchor="mm")
    
    # Student Info - CONSISTENT from StudentInfo
    x_info = 175
    y = 100
    draw.text((x_info, y), student_info.full_name, fill=(0, 0, 0), font=font_name)
    y += 35
    
    # Info labels with CONSISTENT student_id
    labels = [
        ("Student ID:", student_info.student_id),
        ("Status:", "Active Student"),
        ("Issue Date:", student_info.issue_date),
        ("Expiration:", student_info.expiry_date),
    ]
    
    for label, value in labels:
        draw.text((x_info, y), label, fill=(80, 80, 80), font=font_sm)
        draw.text((x_info + 85, y), value, fill=(0, 0, 0), font=font_md)
        y += 28
    
    # Semester indicator
    y += 5
    draw.rectangle([(x_info, y), (x_info + 180, y + 25)], fill=(240, 250, 240), outline=(0, 100, 0))
    draw.text((x_info + 90, y + 12), f"{student_info.semester} {student_info.year}", fill=(0, 100, 0), font=font_bold, anchor="mm")
    
    # Barcode strip
    draw.rectangle([(0, 340), (w, 400)], fill=(255, 255, 255))
    barcode_start = 80
    for i in range(35):
        x = barcode_start + i * 14
        bar_width = random.choice([3, 5, 7])
        if random.random() > 0.25:
            draw.rectangle([(x, 350), (x + bar_width, 390)], fill=(0, 0, 0))
    
    # Card number with CONSISTENT student_id
    draw.text((w//2, 408), f"Card ID: {student_info.student_id[-6:]}", fill=(120, 120, 120), font=font_sm, anchor="mm")
    
    # Apply effects
    buf = BytesIO()
    img.save(buf, format="PNG")
    return apply_advanced_realism(buf.getvalue())


def generate_all_documents(student_info: StudentInfo) -> List[Tuple[bytes, str, str]]:
    """
    Generate ALL verification documents with consistent student info
    
    Args:
        student_info: StudentInfo instance with all student data
    
    Returns:
        List of tuples: (doc_bytes, filename, mime_type)
    """
    documents = []
    
    # 1. Tuition Receipt (PDF) - HIGHEST SUCCESS RATE, upload first
    receipt_bytes = generate_tuition_receipt(student_info)
    documents.append((receipt_bytes, "tuition_receipt.pdf", "application/pdf"))
    
    # 2. Academic Transcript (PNG)
    transcript_bytes = generate_academic_transcript(student_info)
    documents.append((transcript_bytes, "academic_transcript.png", "image/png"))
    
    # 3. Student ID Card (PNG)
    id_card_bytes = generate_student_id_card(student_info)
    documents.append((id_card_bytes, "student_id_card.png", "image/png"))
    
    return documents


# Legacy function for backward compatibility
def generate_student_document(first_name: str, last_name: str, school_name: str, birth_date: str, doc_type: str = None) -> tuple:
    """
    Generate student verification document (LEGACY - kept for compatibility)
    
    For new code, use generate_all_documents() with StudentInfo instead.
    """
    from .student_info import StudentInfo
    
    # Create a basic StudentInfo
    student_info = StudentInfo(
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        school_name=school_name,
        school_domain="university.edu",
    )
    
    # Select document type if not specified
    if doc_type is None:
        roll = random.random()
        if roll < 0.5:
            doc_type = "tuition_receipt"
        elif roll < 0.8:
            doc_type = "transcript"
        else:
            doc_type = "id_card"
    
    # Generate document
    if doc_type == "tuition_receipt":
        doc_bytes = generate_tuition_receipt(student_info)
        filename = "tuition_receipt.pdf"
    elif doc_type == "transcript":
        doc_bytes = generate_academic_transcript(student_info)
        filename = "academic_transcript.png"
    else:
        doc_bytes = generate_student_id_card(student_info)
        filename = "student_id.png"
    
    return doc_bytes, filename, doc_type


if __name__ == '__main__':
    # Test code
    from .student_info import StudentInfo
    
    print("Testing student document generation with StudentInfo...")
    
    student_info = StudentInfo(
        first_name="James",
        last_name="Smith",
        birth_date="2002-05-15",
        school_name="Massachusetts Institute of Technology",
        school_domain="mit.edu",
        primary_color=(163, 31, 52),
        portal_name="MIT Atlas",
        id_format="9_digits",
    )
    
    print(f"Student: {student_info.full_name}")
    print(f"ID: {student_info.student_id}")
    print(f"Email: {student_info.email}")
    
    documents = generate_all_documents(student_info)
    for doc_bytes, filename, mime_type in documents:
        print(f"  ✓ {filename}: {len(doc_bytes)/1024:.1f} KB ({mime_type})")
