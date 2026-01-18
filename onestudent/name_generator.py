"""Name and Identity Generator for Student Verification"""

import random
from typing import Tuple
from datetime import datetime, timedelta

# 60+ American names for realistic identity generation
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


def generate_name() -> Tuple[str, str]:
    """Generate random American name"""
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def generate_email(first_name: str, last_name: str, domain: str) -> str:
    """
    Generate realistic .edu email address
    
    Patterns:
    - jsmith123@university.edu
    - john.smith45@university.edu
    - smithj789@university.edu
    """
    patterns = [
        f"{first_name[0].lower()}{last_name.lower()}{random.randint(100, 999)}",
        f"{first_name.lower()}.{last_name.lower()}{random.randint(10, 99)}",
        f"{last_name.lower()}{first_name[0].lower()}{random.randint(100, 999)}"
    ]
    return f"{random.choice(patterns)}@{domain}"


def generate_birth_date() -> str:
    """
    Generate birth date for 18-24 year old students
    Range: 2000-2006
    """
    year = random.randint(2000, 2006)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Safe for all months
    return f"{year}-{month:02d}-{day:02d}"


def get_current_semester() -> Tuple[str, int]:
    """
    Get current semester based on current date
    
    Returns:
        (semester_name, year)
        - SPRING: Jan-May
        - SUMMER: Jun-Jul
        - FALL: Aug-Dec
    """
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
    """
    Get current academic year (e.g., "2025-2026")
    Academic year starts in August
    """
    now = datetime.now()
    if now.month >= 8:  # Fall semester starts new academic year
        return f"{now.year}-{now.year + 1}"
    else:
        return f"{now.year - 1}-{now.year}"


def get_semester_dates() -> dict:
    """
    Get realistic semester dates based on current date
    
    Returns dict with:
        - semester: SPRING/SUMMER/FALL
        - year: semester year
        - start_date: formatted start date
        - end_date: formatted end date
        - academic_year: e.g., "2025-2026"
    """
    now = datetime.now()
    year = now.year
    
    if now.month >= 8:  # Fall semester (Aug-Dec)
        return {
            "semester": "FALL",
            "year": year,
            "start_date": f"August {random.randint(18, 26)}, {year}",
            "end_date": f"December {random.randint(10, 16)}, {year}",
            "academic_year": f"{year}-{year + 1}"
        }
    elif now.month <= 5:  # Spring semester (Jan-May)
        return {
            "semester": "SPRING",
            "year": year,
            "start_date": f"January {random.randint(10, 18)}, {year}",
            "end_date": f"May {random.randint(5, 12)}, {year}",
            "academic_year": f"{year - 1}-{year}"
        }
    else:  # Summer semester (Jun-Jul)
        return {
            "semester": "SUMMER",
            "year": year,
            "start_date": f"May {random.randint(15, 22)}, {year}",
            "end_date": f"August {random.randint(5, 12)}, {year}",
            "academic_year": f"{year - 1}-{year}"
        }


def get_recent_date(days_ago_max: int = 30) -> str:
    """Generate a recent date within the last N days"""
    days_ago = random.randint(1, days_ago_max)
    date = datetime.now() - timedelta(days=days_ago)
    return date.strftime("%Y-%m-%d")


def get_document_date() -> str:
    """Generate document date (0-14 days ago, not always today)"""
    days_ago = random.randint(0, 14)
    date = datetime.now() - timedelta(days=days_ago)
    return date.strftime("%Y-%m-%d")


# Enhanced course database with more realistic codes
COURSES = [
    # Computer Science
    ("CSCI 1101", "Introduction to Programming", "Dr. Sarah Mitchell"),
    ("CSCI 2201", "Data Structures and Algorithms", "Prof. Robert Chen"),
    ("CSCI 3315", "Database Management Systems", "Dr. Emily Rodriguez"),
    ("CSCI 3420", "Computer Architecture", "Prof. David Park"),
    
    # Mathematics
    ("MATH 2210", "Calculus III", "Dr. Jennifer Williams"),
    ("MATH 2415", "Linear Algebra", "Prof. Michael Thompson"),
    ("MATH 3320", "Differential Equations", "Dr. Lisa Anderson"),
    ("MATH 4340", "Probability and Statistics", "Prof. James Martinez"),
    
    # Physics
    ("PHYS 2326", "Electromagnetism and Waves", "Dr. Patricia Garcia"),
    ("PHYS 3425", "Modern Physics", "Prof. Christopher Lee"),
    ("PHYS 4310", "Quantum Mechanics I", "Dr. Amanda Wilson"),
    
    # English & Humanities
    ("ENGL 1302", "Rhetoric and Composition", "Prof. Thomas Jackson"),
    ("ENGL 2311", "Technical Writing", "Dr. Maria Hernandez"),
    ("HIST 1311", "United States History to 1877", "Prof. Richard Taylor"),
    ("PHIL 2303", "Introduction to Philosophy", "Dr. Barbara Moore"),
    
    # Economics & Business
    ("ECON 2301", "Principles of Microeconomics", "Prof. Daniel Brown"),
    ("ECON 2302", "Principles of Macroeconomics", "Dr. Jessica Davis"),
    ("ACCT 2301", "Financial Accounting", "Prof. Kevin White"),
    
    # Natural Sciences
    ("CHEM 1311", "General Chemistry I", "Dr. Rebecca Harris"),
    ("BIOL 1406", "General Biology I", "Prof. Steven Clark"),
    ("BIOL 2420", "Microbiology", "Dr. Michelle Lewis"),
    
    # Social Sciences
    ("PSYC 2301", "Introduction to Psychology", "Prof. Ashley Robinson"),
    ("SOCI 1301", "Introduction to Sociology", "Dr. Ryan Young"),
    ("POLS 2301", "American Government", "Prof. Laura Allen"),
]


def get_random_courses(count: int = 5) -> list:
    """Get random courses for schedule with varied statuses"""
    selected = random.sample(COURSES, min(count, len(COURSES)))
    return selected


def get_course_status() -> str:
    """Get realistic course status (not all In Progress)"""
    statuses = [
        "In Progress",  # 60%
        "In Progress",
        "In Progress",
        "Enrolled",     # 30%
        "Registered",   # 10%
    ]
    return random.choice(statuses)


def generate_realistic_gpa() -> float:
    """
    Generate realistic GPA (not always perfect)
    Most students: 2.8-3.9
    """
    # Weighted distribution
    if random.random() < 0.15:  # 15% high achievers
        return round(random.uniform(3.7, 4.0), 2)
    elif random.random() < 0.60:  # 60% average-good
        return round(random.uniform(3.0, 3.6), 2)
    else:  # 25% below average
        return round(random.uniform(2.5, 2.9), 2)
