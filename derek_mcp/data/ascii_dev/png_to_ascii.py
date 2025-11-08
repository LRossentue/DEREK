from PIL import Image, ImageEnhance, ImageOps
import numpy as np
import os

# Get all uploaded images
upload_dir = '/mnt/user-data/uploads'
image_files = [f for f in os.listdir(upload_dir) if f.endswith('.png')]

print(f"Found {len(image_files)} images to process\n")

# ASCII with block characters
ASCII_CHARS = "█▓▒░ "

def resize_image(image, alpha_channel, new_width=60):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    
    resized_img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    resized_alpha = Image.fromarray(alpha_channel).resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return resized_img, np.array(resized_alpha)

def pixels_to_ascii(image, alpha_channel, threshold=50):
    pixels = np.array(image)
    ascii_str = ""
    
    for i, row in enumerate(pixels):
        for j, pixel in enumerate(row):
            if alpha_channel[i][j] < threshold:
                ascii_str += " "
            else:
                # Adjusted mapping for better contrast
                if pixel < 32:
                    ascii_str += ASCII_CHARS[0]  # █
                elif pixel < 96:
                    ascii_str += ASCII_CHARS[1]  # ▓
                elif pixel < 160:
                    ascii_str += ASCII_CHARS[2]  # ▒
                elif pixel < 224:
                    ascii_str += ASCII_CHARS[3]  # ░
                else:
                    ascii_str += ASCII_CHARS[4]  # space
        ascii_str += "\n"
    
    return ascii_str

# Process each image
for img_file in sorted(image_files):
    print(f"Processing {img_file}...")
    
    img_path = os.path.join(upload_dir, img_file)
    img = Image.open(img_path)
    
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    alpha = np.array(img.split()[-1])
    img_gray = img.convert('L')
    
    # Apply extreme contrast
    img_contrast = ImageEnhance.Contrast(img_gray).enhance(4.0)
    
    # Increase brightness slightly
    img_bright = ImageEnhance.Brightness(img_contrast).enhance(1.1)
    
    # Apply heavy sharpness
    img_sharp = ImageEnhance.Sharpness(img_bright).enhance(3.0)
    
    # Posterize to fewer levels
    img_cartoon = ImageOps.posterize(img_sharp, 2)
    
    # Create ASCII
    resized_img, resized_alpha = resize_image(img_cartoon, alpha, 60)
    ascii_art = pixels_to_ascii(resized_img, resized_alpha, threshold=50)
    
    # Save with original filename (replace .png with .txt)
    output_name = img_file.replace('.png', '_60.txt')
    output_path = os.path.join('/mnt/user-data/outputs', output_name)
    
    with open(output_path, 'w') as f:
        f.write(ascii_art)
    
    print(f"  ✓ Created {output_name}")

print("\n" + "="*60)
print("All images converted successfully!")
print("="*60)

# List all output files
output_files = sorted([f for f in os.listdir('/mnt/user-data/outputs') if f.endswith('_60.txt')])
print("\nOutput files:")
for f in output_files:
    print(f"  - {f}")