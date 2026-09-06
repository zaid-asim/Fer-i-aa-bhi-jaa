import os
from PIL import Image

products_dir = 'images/products'
files = [f for f in os.listdir(products_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

total_before = 0
total_after = 0

for filename in files:
    filepath = os.path.join(products_dir, filename)
    size_before = os.path.getsize(filepath)
    total_before += size_before

    try:
        with Image.open(filepath) as img:
            img = img.convert('RGB')
            # Resize if dimensions exceed 500px while maintaining aspect ratio
            w, h = img.size
            max_dim = 500
            if max(w, h) > max_dim:
                if w > h:
                    new_w = max_dim
                    new_h = int(h * (max_dim / w))
                else:
                    new_h = max_dim
                    new_w = int(w * (max_dim / h))
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Save optimized
            img.save(filepath, 'JPEG', quality=85, optimize=True, progressive=True)
            size_after = os.path.getsize(filepath)
            total_after += size_after
    except Exception as e:
        print(f"Error optimizing {filename}: {e}")

print(f"Optimized {len(files)} product images.")
print(f"Total size before: {total_before / (1024*1024):.2f} MB")
print(f"Total size after:  {total_after / (1024*1024):.2f} MB")
print(f"Saved: {((total_before - total_after) / total_before) * 100:.1f}%")
