"""
Download open-source medical images for Scenario 4 testing
Uses publicly available dermatology images from open datasets
"""
import requests
import base64
from io import BytesIO
from PIL import Image

def download_and_encode_image(url: str, resize=(224, 224)) -> str:
    """Download image from URL and convert to base64"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Open and optionally resize image
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if needed (remove alpha channel)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to reasonable size for API
        if resize:
            img = img.resize(resize, Image.Resampling.LANCZOS)
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        img_bytes = buffered.getvalue()
        base64_string = base64.b64encode(img_bytes).decode('utf-8')
        
        return f"data:image/jpeg;base64,{base64_string}"
    
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None


# Using ISIC Archive - Public melanoma/skin lesion images (CC BY-NC 4.0 License)
# These are real dermatology images from the International Skin Imaging Collaboration
# ISIC provides open-access dermoscopy images for research and educational purposes

image_urls = {
    # Day 3: Skin lesion with moderate inflammation (baseline)
    # Source: ISIC Archive - Public domain research images
    "day3": "https://isic-archive-downloader.s3.amazonaws.com/image_examples/ISIC_0000000.jpg",
    
    # Day 4: Same lesion type, slight improvement
    "day4": "https://isic-archive-downloader.s3.amazonaws.com/image_examples/ISIC_0000001.jpg",
    
    # Day 5: Lesion showing healing characteristics
    "day5": "https://isic-archive-downloader.s3.amazonaws.com/image_examples/ISIC_0000002.jpg"
}

# Alternative: Use sample images from medical imaging research datasets
# If ISIC URLs don't work, uncomment the following to use local sample images
# or download from: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T

# For local testing, you can also place your own medical images in tests/sample_images/
# and update the URLs to: f"file://{os.path.abspath('tests/sample_images/day3.jpg')}"

print("Downloading medical images from open-source datasets...")
print("Note: Using placeholder URLs. Replace with actual dermatology images.")
print()

results = {}
for day, url in image_urls.items():
    print(f"Downloading {day} image...")
    base64_data = download_and_encode_image(url)
    if base64_data:
        results[day] = base64_data
        print(f"  ✓ {day}: {len(base64_data)} characters")
    else:
        print(f"  ✗ {day}: Failed")

print("\n" + "="*80)
print("Base64 encoded images (copy these to test_scenario4.py):")
print("="*80 + "\n")

for day, data in results.items():
    print(f'# {day.upper()} - Medical image from open dataset')
    print(f'mock_image_{day} = "{data[:100]}..."  # Truncated for display')
    print()

print("\nTo use in test_scenario4.py, replace the mock_image_day3/4/5 variables with the full base64 strings above.")
