"""StudentInfo - Consistent Student Data for Document Generation

Ensures all generated documents use the same student information:
- Name, DOB, Student ID
- Email
- Semester/Year dates
- University-specific styling
"""

import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Optional


def _generate_student_id(id_format: str, id_prefix: str = "") -> str:
    """Generate student ID based on university format"""
    if id_format == "9_digits":
        return ''.join([str(random.randint(0, 9)) for _ in range(9)])
    elif id_format == "8_digits":
        return ''.join([str(random.randint(0, 9)) for _ in range(8)])
    elif id_format == "7_digits":
        return ''.join([str(random.randint(0, 9)) for _ in range(7)])
    elif id_format == "N_8_digits":
        numbers = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return f"N{numbers}"
    elif id_format == "sid_8_digits":
        numbers = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        return f"3{numbers}"
    elif id_format == "9_start_9":
        numbers = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return f"9{numbers}"
    else:
        # Default: 8-digit numeric
        return ''.join([str(random.randint(0, 9)) for _ in range(8)])


def _get_current_semester() -> tuple:
    """Get current semester and year"""
    now = datetime.now()
    month = now.month
    year = now.year
    
    if month <= 5:
        return "SPRING", year
    elif month <= 7:
        return "SUMMER", year
    else:
        return "FALL", year


def _get_academic_year() -> str:
    """Get current academic year (e.g., 2025-2026)"""
    now = datetime.now()
    if now.month >= 8:
        return f"{now.year}-{now.year + 1}"
    else:
        return f"{now.year - 1}-{now.year}"


@dataclass
class StudentInfo:
    """Holds consistent student information across all documents"""
    
    # Basic info
    first_name: str
    last_name: str
    birth_date: str  # YYYY-MM-DD format
    
    # University info
    school_name: str
    school_domain: str
    
    # Generated IDs (computed once)
    student_id: str = field(default="")
    email: str = field(default="")
    
    # Semester info
    semester: str = field(default="")
    year: int = field(default=0)
    academic_year: str = field(default="")
    
    # Dates for ID card
    issue_date: str = field(default="")
    expiry_date: str = field(default="")
    
    # University styling (optional)
    primary_color: tuple = field(default=(0, 50, 100))
    secondary_color: tuple = field(default=(100, 100, 100))
    portal_name: str = field(default="Student Portal")
    id_format: str = field(default="8_digits")
    
    def __post_init__(self):
        """Initialize computed fields after object creation"""
        # Generate student ID if not provided
        if not self.student_id:
            self.student_id = _generate_student_id(self.id_format)
        
        # Generate email if not provided
        if not self.email:
            patterns = [
                f"{self.first_name[0].lower()}{self.last_name.lower()}{random.randint(100, 999)}",
                f"{self.first_name.lower()}.{self.last_name.lower()}{random.randint(10, 99)}",
                f"{self.last_name.lower()}{self.first_name[0].lower()}{random.randint(100, 999)}"
            ]
            self.email = f"{random.choice(patterns)}@{self.school_domain}"
        
        # Get semester info
        if not self.semester:
            self.semester, self.year = _get_current_semester()
        
        if not self.academic_year:
            self.academic_year = _get_academic_year()
        
        # Generate dates for ID card
        if not self.issue_date:
            today = datetime.now()
            issue = today - timedelta(days=random.randint(5, 30))
            self.issue_date = issue.strftime("%m/%d/%Y")
        
        if not self.expiry_date:
            self.expiry_date = f"05/31/{self.year + 1}"
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API submission"""
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "birthDate": self.birth_date,
            "email": self.email,
            "studentId": self.student_id,
            "school": self.school_name,
        }


def create_student_info(
    first_name: str,
    last_name: str,
    birth_date: str,
    university_config: Dict
) -> StudentInfo:
    """
    Factory function to create StudentInfo from university config
    
    Args:
        first_name: Student first name
        last_name: Student last name
        birth_date: Birth date (YYYY-MM-DD)
        university_config: University dict with name, domain, colors, etc.
    
    Returns:
        StudentInfo instance with all fields populated
    """
    # Parse hex colors if present
    primary_color = (0, 50, 100)  # Default dark blue
    secondary_color = (100, 100, 100)  # Default gray
    
    if "primary_color" in university_config:
        hex_color = university_config["primary_color"]
        if isinstance(hex_color, str) and hex_color.startswith("#"):
            primary_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    
    if "secondary_color" in university_config:
        hex_color = university_config["secondary_color"]
        if isinstance(hex_color, str) and hex_color.startswith("#"):
            secondary_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    
    return StudentInfo(
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        school_name=university_config.get("name", "University"),
        school_domain=university_config.get("domain", "university.edu"),
        primary_color=primary_color,
        secondary_color=secondary_color,
        portal_name=university_config.get("portal_name", "Student Portal"),
        id_format=university_config.get("id_format", "8_digits"),
    )
