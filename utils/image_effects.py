"""Image Effects for Realistic Screenshot Simulation

Adds subtle visual noise and randomization to make generated screenshots
look more authentic and less artificially perfect.
"""

import random
from io import BytesIO
from typing import Tuple, Optional

try:
    from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def add_screenshot_noise(image_bytes: bytes, intensity: float = 0.01) -> bytes:
    """
    Add subtle noise to simulate real screenshot artifacts
    
    Args:
        image_bytes: Original PNG image bytes
        intensity: Noise intensity (0.005 - 0.02 recommended, default 0.01)
        
    Returns:
        Modified image bytes with noise
    """
    if not PIL_AVAILABLE:
        return image_bytes
    
    try:
        # Load image
        img = Image.open(BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Add subtle Gaussian noise
        pixels = img.load()
        width, height = img.size
        
        # Only add noise to a random subset of pixels (more efficient and realistic)
        noise_ratio = intensity * 100  # Convert to percentage
        
        for _ in range(int(width * height * noise_ratio)):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            
            r, g, b = pixels[x, y]
            
            # Add small random variation
            noise_r = random.randint(-10, 10)
            noise_g = random.randint(-10, 10)
            noise_b = random.randint(-10, 10)
            
            pixels[x, y] = (
                max(0, min(255, r + noise_r)),
                max(0, min(255, g + noise_g)),
                max(0, min(255, b + noise_b))
            )
        
        # Save with slight JPEG compression artifacts
        output = BytesIO()
        quality = random.randint(88, 95)  # Slight compression
        img.save(output, 'PNG', quality=quality, optimize=False)
        
        return output.getvalue()
        
    except Exception as e:
        # If anything fails, return original image
        print(f"Warning: Failed to add noise: {e}")
        return image_bytes


def add_subtle_blur(image_bytes: bytes, radius: float = 0.3) -> bytes:
    """
    Add very subtle blur to simulate slight screen capture blur
    
    Args:
        image_bytes: Original PNG image bytes
        radius: Blur radius (0.2 - 0.5 recommended)
        
    Returns:
        Slightly blurred image bytes
    """
    if not PIL_AVAILABLE:
        return image_bytes
    
    try:
        img = Image.open(BytesIO(image_bytes))
        
        # Apply very subtle Gaussian blur
        blurred = img.filter(ImageFilter.GaussianBlur(radius=radius))
        
        output = BytesIO()
        blurred.save(output, 'PNG')
        return output.getvalue()
        
    except Exception:
        return image_bytes


def adjust_brightness(image_bytes: bytes, factor: Optional[float] = None) -> bytes:
    """
    Slightly adjust brightness to simulate different monitor settings
    
    Args:
        image_bytes: Original PNG image bytes
        factor: Brightness factor (0.95 - 1.05 recommended). If None, random
        
    Returns:
        Brightness-adjusted image bytes
    """
    if not PIL_AVAILABLE:
        return image_bytes
    
    try:
        if factor is None:
            factor = random.uniform(0.97, 1.03)
        
        img = Image.open(BytesIO(image_bytes))
        enhancer = ImageEnhance.Brightness(img)
        adjusted = enhancer.enhance(factor)
        
        output = BytesIO()
        adjusted.save(output, 'PNG')
        return output.getvalue()
        
    except Exception:
        return image_bytes


def randomize_viewport() -> Tuple[int, int]:
    """
    Get randomized viewport dimensions for screenshot
    
    Returns:
        Tuple of (width, height)
    """
    # Base dimensions
    base_width = 1200
    base_height = 900
    
    # Add random variation (±50 pixels)
    width = base_width + random.randint(-50, 50)
    height = base_height + random.randint(-50, 50)
    
    return (width, height)


def get_random_zoom() -> float:
    """
    Get random browser zoom level
    
    Returns:
        Zoom factor (0.95 - 1.05)
    """
    return random.uniform(0.95, 1.05)


def apply_all_effects(
    image_bytes: bytes,
    noise_intensity: float = 0.01,
    blur_radius: float = 0.3,
    brightness_variation: bool = True
) -> bytes:
    """
    Apply all screenshot realism effects in sequence
    
    Args:
        image_bytes: Original PNG image bytes
        noise_intensity: Noise intensity (0.005 - 0.02)
        blur_radius: Blur radius (0.2 - 0.5)
        brightness_variation: Whether to randomize brightness
        
    Returns:
        Processed image bytes with all effects
    """
    result = image_bytes
    
    # Randomly decide which effects to apply (not all at once)
    apply_noise = random.choice([True, True, False])  # 66% chance
    apply_blur = random.choice([True, False, False])   # 33% chance
    apply_brightness = brightness_variation and random.choice([True, False])  # 50% if enabled
    
    if apply_noise:
        result = add_screenshot_noise(result, intensity=noise_intensity)
    
    if apply_blur:
        result = add_subtle_blur(result, radius=blur_radius)
    
    if apply_brightness:
        result = adjust_brightness(result)
    
    return result


def add_scan_artifacts(image_bytes: bytes) -> bytes:
    """
    Add realistic scanner artifacts
    - Slight rotation (paper not perfectly aligned)
    - Scan lines
    - Edge shadows
    """
    img = Image.open(BytesIO(image_bytes))
    
    # 1. Slight rotation (0.3-1.2 degrees)
    angle = random.uniform(-1.2, 1.2)
    img = img.rotate(angle, expand=True, fillcolor=(255, 255, 255))
    
    # 2. Add subtle scan lines (1-3 lines)
    draw = ImageDraw.Draw(img, 'RGBA')
    for _ in range(random.randint(1, 3)):
        y = random.randint(0, img.height)
        alpha = random.randint(10, 30)
        draw.line([(0, y), (img.width, y)], fill=(200, 200, 200, alpha), width=1)
    
    # 3. Edge shadow (paper depth)
    if random.random() > 0.5:
        # Darken edges slightly
        mask = Image.new('L', img.size, 255)
        mask_draw = ImageDraw.Draw(mask)
        for i in range(15):
            alpha = int(255 - (i * 8))
            mask_draw.rectangle([(i, i), (img.width-i-1, img.height-i-1)], outline=alpha)
        
        darkened = ImageEnhance.Brightness(img).enhance(0.95)
        img = Image.composite(img, darkened, mask)
    
    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


def add_jpeg_compression(image_bytes: bytes, quality: int = None) -> bytes:
    """
    Simulate phone camera JPEG compression artifacts
    
    Args:
        image_bytes: PNG image bytes
        quality: JPEG quality (70-92, lower = more artifacts)
        
    Returns:
        PNG bytes with JPEG compression artifacts
    """
    if quality is None:
        quality = random.randint(70, 88)  # Real phone photos are 70-90
    
    img = Image.open(BytesIO(image_bytes))
    
    # Convert to JPEG and back to simulate compression
    jpeg_buf = BytesIO()
    img.convert('RGB').save(jpeg_buf, format='JPEG', quality=quality)
    
    # Open JPEG and save as PNG
    jpeg_img = Image.open(jpeg_buf)
    png_buf = BytesIO()
    jpeg_img.save(png_buf, format='PNG')
    
    return png_buf.getvalue()


def add_paper_texture(image_bytes: bytes) -> bytes:
    """
    Add subtle paper texture/grain
    """
    img = Image.open(BytesIO(image_bytes)).convert('RGB')
    
    # Create texture layer with random dots (paper fibers)
    texture = Image.new('RGB', img.size, (255, 255, 255))
    pixels = texture.load()
    
    # Add random paper grain
    for _ in range(img.width * img.height // 800):  # Sparse dots
        x = random.randint(0, img.width-1)
        y = random.randint(0, img.height-1)
        gray = random.randint(248, 255)
        pixels[x, y] = (gray, gray, gray)
    
    # Very subtle blend
    img = Image.blend(img, texture, alpha=0.03)
    
    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


def add_perspective_distortion(image_bytes: bytes) -> bytes:
    """
    Add slight perspective distortion (simulates phone photo angle)
    """
    img = Image.open(BytesIO(image_bytes))
    width, height = img.size
    
    # Small random perspective shift (1-3% of width/height)
    shift = random.randint(int(width * 0.01), int(width * 0.03))
    
    # Random perspective direction
    if random.random() > 0.5:
        # Slight trapezoid effect
        coeffs = [
            1, random.uniform(-0.0003, 0.0003), random.uniform(-shift, shift),
            random.uniform(-0.0003, 0.0003), 1, random.uniform(-shift, shift),
            random.uniform(-0.00001, 0.00001), random.uniform(-0.00001, 0.00001)
        ]
        img = img.transform(img.size, Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    
    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


def apply_advanced_realism(image_bytes: bytes) -> bytes:
    """
    Apply all advanced anti-fraud effects
    
    Combines:
    1. Paper texture
    2. Scan artifacts
    3. Perspective distortion  
    4. Strong noise/blur
    5. JPEG compression
    """
    result = image_bytes
    
    # 1. Paper texture (always apply, very subtle)
    result = add_paper_texture(result)
    
    # 2. Scan artifacts (80% chance)
    if random.random() > 0.2:
        result = add_scan_artifacts(result)
    
    # 3. Perspective distortion (50% chance)
    if random.random() > 0.5:
        result = add_perspective_distortion(result)
    
    # 4. Enhanced noise and blur
    result = apply_all_effects(
        result,
        noise_intensity=random.uniform(0.018, 0.035),  # Stronger than before
        blur_radius=random.uniform(0.6, 1.2),          # More blur
        brightness_variation=True
    )
    
    # 5. JPEG compression (always apply, simulates phone photo)
    result = add_jpeg_compression(result, quality=random.randint(72, 86))
    
    return result


def get_random_screenshot_effects() -> dict:
    """
    Get randomized effect parameters for consistency
    
    Returns:
        Dictionary with effect parameters
    """
    return {
        'noise_intensity': random.uniform(0.008, 0.015),
        'blur_radius': random.uniform(0.25, 0.4),
        'brightness_variation': True,
        'viewport': randomize_viewport(),
        'zoom': get_random_zoom(),
    }


# Export main functions
__all__ = [
    'add_screenshot_noise',
    'add_subtle_blur',
    'adjust_brightness',
    'randomize_viewport',
    'get_random_zoom',
    'apply_all_effects',
    'get_random_screenshot_effects',
]
