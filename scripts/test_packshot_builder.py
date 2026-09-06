import math
from PIL import Image, ImageDraw, ImageFont

def create_sample_packshot(filename, bg_gradient, pack_type, brand, title, subtitle, badge, accent_color, pack_color):
    img = Image.new("RGB", (600, 600), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    # Subtle circular studio spotlight background
    for r in range(260, 0, -10):
        alpha = int(255 - (260 - r) * 0.2)
        color = (240 + int((r/260)*15), 245 + int((r/260)*10), 250)
        draw.ellipse([300 - r, 300 - r, 300 + r, 300 + r], fill=color)

    # Soft ambient shadow on ground
    for i in range(15):
        sh_w = 180 + i * 8
        sh_h = 20 + i * 2
        sh_alpha = 15 - i
        draw.ellipse([300 - sh_w, 510 - sh_h, 300 + sh_w, 510 + sh_h], fill=(210 - i*2, 215 - i*2, 225 - i*2))

    # Draw Packaging based on pack_type
    if pack_type == "bottle":
        # Neck
        draw.rounded_rectangle([275, 100, 325, 160], radius=6, fill=pack_color)
        # Cap
        draw.rounded_rectangle([270, 80, 330, 110], radius=5, fill=accent_color)
        # Body
        draw.rounded_rectangle([200, 150, 400, 500], radius=35, fill=pack_color)
        # 3D Highlight sheen (left side)
        draw.rounded_rectangle([215, 165, 235, 485], radius=10, fill=(255, 255, 255, 100))
        # Label area
        draw.rounded_rectangle([215, 220, 385, 440], radius=16, fill="#FFFFFF")
        label_box = [215, 220, 385, 440]
    elif pack_type == "pouch":
        # Top crimp
        draw.polygon([(170, 110), (430, 110), (410, 140), (190, 140)], fill=accent_color)
        # Pouch body
        draw.rounded_rectangle([180, 130, 420, 500], radius=24, fill=pack_color)
        # 3D side folds
        draw.polygon([(180, 130), (205, 150), (205, 480), (180, 500)], fill=(0, 0, 0, 30))
        # Center Label
        draw.rounded_rectangle([200, 170, 400, 470], radius=16, fill="#FFFFFF")
        label_box = [200, 170, 400, 470]
    else: # Box
        draw.rounded_rectangle([170, 120, 430, 490], radius=18, fill=pack_color)
        # Box bevel
        draw.rectangle([180, 130, 420, 150], fill=accent_color)
        # Center Label
        draw.rounded_rectangle([190, 165, 410, 475], radius=12, fill="#FFFFFF")
        label_box = [190, 165, 410, 475]

    # Content on Label
    # Brand Bar
    draw.rounded_rectangle([label_box[0] + 15, label_box[1] + 15, label_box[2] - 15, label_box[1] + 65], radius=8, fill=accent_color)
    draw.text((300, label_box[1] + 40), brand.upper(), fill="#FFFFFF", anchor="mm", font_size=24)

    # Product Title
    draw.text((300, label_box[1] + 105), title, fill="#0F172A", anchor="mm", font_size=20)
    draw.text((300, label_box[1] + 135), subtitle, fill="#64748B", anchor="mm", font_size=15)

    # Decorative icon / badge in center
    draw.ellipse([260, label_box[1] + 160, 340, label_box[1] + 240], fill=pack_color)
    draw.text((300, label_box[1] + 200), "★", fill="#FFFFFF", anchor="mm", font_size=38)

    # Bottom Badge Pill
    draw.rounded_rectangle([label_box[0] + 20, label_box[3] - 45, label_box[2] - 20, label_box[3] - 15], radius=15, fill=accent_color)
    draw.text((300, label_box[3] - 30), badge.upper(), fill="#FFFFFF", anchor="mm", font_size=13)

    img.save(filename, quality=92)
    print("Saved:", filename)

create_sample_packshot("images/products/sample_surf.jpg", None, "pouch", "SURF EXCEL", "Easy Wash Detergent", "Superior Stain Removal", "Fast Dissolve • 2kg", "#E11D48", "#1E40AF")
create_sample_packshot("images/products/sample_vim.jpg", None, "bottle", "VIM", "Dishwash Liquid Gel", "With Power of 100 Lemons", "Grease Buster • 750ml", "#16A34A", "#FACC15")
create_sample_packshot("images/products/sample_parachute.jpg", None, "bottle", "PARACHUTE", "100% Pure Coconut Oil", "Naturally Sourced Copra", "100% Edible • 600ml", "#0284C7", "#0369A1")
