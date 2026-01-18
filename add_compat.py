#!/usr/bin/env python3
"""Add compatibility functions to Boltnew img_generator.py"""

compatibility_code = '''

# ==============================================================================
# BOLTNEW BACKWARD COMPATIBILITY LAYER
# ==============================================================================

def generate_psu_email(first_name, last_name):
    """Backward compatibility: Generate email address for teacher"""
    district_key, _ = get_random_district()
    return generate_district_email(first_name, last_name, district_key)


def generate_images(first_name, last_name, school_id=None):
    """
    Backward compatibility: Generate teacher images in old format
    
    Returns list of dicts with 'file_name' and 'data' keys for Boltnew compatibility
    """
    png_data = generate_teacher_png(first_name, last_name)
    return [
        {
            'file_name': 'teacher_verification.png',
            'data': png_data
        }
    ]
'''

import os

# Add to Windows file
win_file = r'E:\CodeWorkstation\tgbot-verify\Boltnew\img_generator.py'
with open(win_file, '

', encoding='utf-8') as f:
    f.write(compatibility_code)

print(f"✓ Added compatibility functions to {win_file}")
