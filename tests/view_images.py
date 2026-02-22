"""
Extract and save the medical images from test_scenario4.py so you can view them
"""
import base64
import re

# Read the test file
with open('tests/test_scenario4.py', 'r') as f:
    content = f.read()

# Extract image data
pattern = r'mock_image_day(\d) = "data:image/jpeg;base64,([^"]+)"'
matches = re.findall(pattern, content)

for day, base64_data in matches:
    # Decode base64
    image_bytes = base64.b64decode(base64_data)
    
    # Save as JPEG
    filename = f'tests/sample_day{day}.jpg'
    with open(filename, 'wb') as f:
        f.write(image_bytes)
    
    print(f"✅ Saved {filename} ({len(image_bytes)} bytes)")

print("\n📁 Images saved to tests/ folder:")
print("   - sample_day3.jpg (severe rash)")
print("   - sample_day4.jpg (improving)")
print("   - sample_day5.jpg (healing)")
print("\nOpen these files to see the realistic medical images!")
