# ==============================================================================
# BOLTNEW BACKWARD COMPATIBILITY LAYER  
# ==============================================================================

def generate_psu_email(first_name, last_name):
    """Backward compatibility: Generate email address for teacher"""
    # Import here to avoid circular dependency
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.document_templates import get_random_district, generate_district_email
    
    # Use a random district for email generation
    district_key, _ = get_random_district()
    return generate_district_email(first_name, last_name, district_key)


def generate_images(first_name, last_name, school_id=None):
    """
    Backward compatibility: Generate teacher images in old format
    
    Returns list of dicts with 'file_name' and 'data' keys for Boltnew compatibility
    """
    # Generate PNG image
    png_data = generate_teacher_png(first_name, last_name)
    
    # Return in old format (list of assets)
    return [
        {
            'file_name': 'teacher_verification.png',
            'data': png_data
        }
    ]
