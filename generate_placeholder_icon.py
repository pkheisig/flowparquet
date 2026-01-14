from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

def create_icon(size=1024):
    # Create a new image with a white background (or transparent)
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a rounded rectangle (Blue gradient-ish background)
    # Since we can't easily do complex gradients with basic PIL draw, we'll do a solid color
    # or a simple interpolated drawing.
    
    # Background color (Teal/Blue to match the "Flow" theme)
    bg_color = (44, 201, 133, 255) # Greenish #2CC985 from the UI
    bg_color_2 = (0, 122, 204, 255) # Blue
    
    # Draw a rounded square
    # For a 1024x1024 icon, a corner radius of ~180 is nice
    radius = 180
    rect_coords = [0, 0, size, size]
    
    # Draw circle mask for rounded corners
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(rect_coords, radius=radius, fill=255)
    
    # Create gradient background
    base = Image.new('RGBA', (size, size), bg_color_2)
    top = Image.new('RGBA', (size, size), bg_color)
    
    # Simple diagonal gradient simulation by masking
    gradient = Image.linear_gradient('L') # Vertical 256x256
    gradient = gradient.resize((size, size))
    gradient = gradient.rotate(45)
    
    # Composite
    final_bg = Image.composite(top, base, gradient)
    final_bg.putalpha(mask)
    
    img = final_bg
    draw = ImageDraw.Draw(img)
    
    # Add Text "FP"
    # Try to load a font, fallback to default
    try:
        # standard mac font
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=400)
    except:
        try:
             font = ImageFont.truetype("arial.ttf", size=400)
        except:
             font = ImageFont.load_default()

    text = "FP"
    
    # centered text
    # bbox = draw.textbbox((0, 0), text, font=font)
    # w = bbox[2] - bbox[0]
    # h = bbox[3] - bbox[1]
    # Text positioning can be tricky with default font, but let's try standard anchor
    
    draw.text((size/2, size/2), text, font=font, anchor="mm", fill="white")
    
    # Save
    img.save("icon_source.png")
    print("Icon created: icon_source.png")

if __name__ == "__main__":
    create_icon()
