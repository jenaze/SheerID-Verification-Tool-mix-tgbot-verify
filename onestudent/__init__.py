"""Google One (Gemini) Student Verification Module"""

from .config import PROGRAM_ID, SHEERID_BASE_URL, UNIVERSITIES
from .sheerid_verifier import GeminiStudentVerifier

__all__ = ['GeminiStudentVerifier', 'PROGRAM_ID', 'SHEERID_BASE_URL', 'UNIVERSITIES']
