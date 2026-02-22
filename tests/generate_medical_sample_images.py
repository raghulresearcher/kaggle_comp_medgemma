"""
Generate realistic medical sample images for Scenario 4 testing
Creates synthetic dermatology images representing a healing progression
"""
import base64
from io import BytesIO
from PIL import Image, ImageDraw
import random

def create_rash_image(severity: float, size=(224, 224)) -> str:
    """
    Create a synthetic skin rash image
    
    Args:
        severity: 0.0 (healed) to 1.0 (severe inflammation)
        size: Image dimensions
    
    Returns:
        Base64 encoded JPEG image
    """
    img = Image.new('RGB', size, color=(255, 220, 200))  # Skin tone base
    draw = ImageDraw.Draw(img)
    
    # Determine rash characteristics based on severity
    num_lesions = int(15 + severity * 35)  # 15-50 spots
    lesion_size = int(3 + severity * 12)  # 3-15 pixel radius
    redness = int(180 + severity * 75)  # 180-255 red value
    
    # Draw random lesions/spots
    random.seed(42 + int(severity * 100))  # Deterministic but varied
    for _ in range(num_lesions):
        x = random.randint(lesion_size, size[0] - lesion_size)
        y = random.randint(lesion_size, size[1] - lesion_size)
        radius = random.randint(lesion_size - 2, lesion_size + 2)
        
        # Color based on severity (red with inflammation)
        red = min(255, redness + random.randint(-20, 20))
        green = max(50, 150 - int(severity * 100) + random.randint(-20, 20))
        blue = max(50, 150 - int(severity * 100) + random.randint(-20, 20))
        
        # Draw lesion with slight blur effect
        draw.ellipse(
            [(x - radius, y - radius), (x + radius, y + radius)],
            fill=(red, green, blue)
        )
    
    # Add some texture/noise for realism
    pixels = img.load()
    for i in range(0, size[0], 4):
        for j in range(0, size[1], 4):
            noise = random.randint(-10, 10)
            r, g, b = pixels[i, j]
            pixels[i, j] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise))
            )
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=85)
    img_bytes = buffered.getvalue()
    base64_string = base64.b64encode(img_bytes).decode('utf-8')
    
    return f"data:image/jpeg;base64,{base64_string}"


print("Generating synthetic medical images for Scenario 4...")
print("These are realistic open-source synthetic images (no copyright issues)")
print()

# Generate progression: Severe → Moderate → Mild (healing trajectory)
images = {
    "day3": create_rash_image(severity=0.75),  # Severe initial rash
    "day4": create_rash_image(severity=0.45),  # Moderate improvement
    "day5": create_rash_image(severity=0.20)   # Significant healing
}

print("Image generation complete!")
print(f"  Day 3: {len(images['day3'])} characters (severe rash)")
print(f"  Day 4: {len(images['day4'])} characters (improving)")
print(f"  Day 5: {len(images['day5'])} characters (healing)")
print()
print("="*80)
print("Updating test_scenario4.py with new medical images...")
print("="*80)

# Read current test file
test_file = "tests/test_scenario4.py"
with open(test_file, 'r') as f:
    content = f.read()

# Replace the mock image definitions
import re

# Find and replace Day 3 image
pattern_day3 = r'mock_image_day3 = "data:image/[^"]*"'
replacement_day3 = f'mock_image_day3 = "{images["day3"]}"'
content = re.sub(pattern_day3, replacement_day3, content)

# Find and replace Day 4 image
pattern_day4 = r'mock_image_day4 = "data:image/[^"]*"'
replacement_day4 = f'mock_image_day4 = "{images["day4"]}"'
content = re.sub(pattern_day4, replacement_day4, content)

# Find and replace Day 5 image
pattern_day5 = r'mock_image_day5 = "data:image/[^"]*"'
replacement_day5 = f'mock_image_day5 = "{images["day5"]}"'
content = re.sub(pattern_day5, replacement_day5, content)

# Update comment
content = content.replace(
    "# Use synthetic test images (1x1 pixel PNGs with different colors to simulate progression)",
    "# Realistic synthetic dermatology images showing healing progression (generated, open-source)"
)
content = content.replace(
    "# These are open-source, copyright-free synthetic images for testing purposes",
    "# These are programmatically generated synthetic medical images (no copyright issues)"
)

# Write back
with open(test_file, 'w') as f:
    f.write(content)

print("✅ Test file updated with realistic medical images!")
print()
print("Image characteristics:")
print("  Day 3: ~40-50 lesions, high redness, severe inflammation")
print("  Day 4: ~25-30 lesions, moderate redness, improving")  
print("  Day 5: ~18-20 lesions, low redness, significant healing")
print()
print("These images will now be sent to MedGemma Vision for REAL analysis!")
