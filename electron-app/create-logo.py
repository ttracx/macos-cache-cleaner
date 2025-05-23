#!/usr/bin/env python3
"""
Create a modern logo for the Cache Cleaner app
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    # Create a high-resolution logo (1024x1024 for various sizes)
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Color scheme - modern blue gradient
    primary_color = '#007AFF'  # Apple blue
    secondary_color = '#5856D6'  # Purple
    accent_color = '#34C759'  # Green
    
    # Draw background circle with gradient effect
    center = size // 2
    radius = int(size * 0.45)
    
    # Create gradient background
    for i in range(radius):
        alpha = int(255 * (1 - i / radius))
        color = f'#007AFF{alpha:02x}'
        draw.ellipse([
            center - radius + i,
            center - radius + i,
            center + radius - i,
            center + radius - i
        ], fill='#007AFF', outline=None)
    
    # Draw main broom/brush icon
    brush_width = int(size * 0.15)
    brush_height = int(size * 0.4)
    brush_x = center - brush_width // 2
    brush_y = center - brush_height // 2
    
    # Brush handle (brown/wood color)
    handle_color = '#8B4513'
    handle_width = int(brush_width * 0.3)
    handle_x = center - handle_width // 2
    handle_height = int(brush_height * 0.6)
    
    draw.rectangle([
        handle_x,
        brush_y + brush_height - handle_height,
        handle_x + handle_width,
        brush_y + brush_height
    ], fill=handle_color)
    
    # Brush bristles (gray/silver)
    bristle_color = '#696969'
    bristle_count = 12
    bristle_width = brush_width // bristle_count
    
    for i in range(bristle_count):
        bristle_x = brush_x + i * bristle_width
        draw.rectangle([
            bristle_x,
            brush_y,
            bristle_x + bristle_width - 2,
            brush_y + brush_height - handle_height + 10
        ], fill=bristle_color)
    
    # Brush ferrule (metal band)
    ferrule_color = '#C0C0C0'
    ferrule_height = int(size * 0.04)
    draw.rectangle([
        brush_x,
        brush_y + brush_height - handle_height - ferrule_height,
        brush_x + brush_width,
        brush_y + brush_height - handle_height + 5
    ], fill=ferrule_color)
    
    # Add sparkles for "cleaning" effect
    sparkle_positions = [
        (center - 120, center - 150),
        (center + 140, center - 100),
        (center - 80, center - 200),
        (center + 100, center - 180),
        (center - 160, center - 80),
        (center + 160, center - 50)
    ]
    
    sparkle_color = '#FFD700'  # Gold
    for x, y in sparkle_positions:
        # Create 4-pointed star
        points = [
            x, y - 15,      # top
            x + 4, y - 4,   # top-right
            x + 15, y,      # right
            x + 4, y + 4,   # bottom-right
            x, y + 15,      # bottom
            x - 4, y + 4,   # bottom-left
            x - 15, y,      # left
            x - 4, y - 4    # top-left
        ]
        draw.polygon(points, fill=sparkle_color)
    
    return img

def create_icon_sizes():
    """Create different icon sizes for the app"""
    logo = create_logo()
    
    # Icon sizes needed for macOS app
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    
    # Create assets directory if it doesn't exist
    assets_dir = 'assets'
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    # Save different sizes
    for size in sizes:
        resized = logo.resize((size, size), Image.Resampling.LANCZOS)
        
        # Save as PNG
        resized.save(f'{assets_dir}/icon-{size}.png', 'PNG')
        
        # Save the main icon sizes
        if size == 512:
            resized.save(f'{assets_dir}/icon.png', 'PNG')
        if size == 1024:
            resized.save(f'{assets_dir}/icon-1024.png', 'PNG')
    
    # Create iconset for macOS
    iconset_dir = f'{assets_dir}/AppIcon.iconset'
    if not os.path.exists(iconset_dir):
        os.makedirs(iconset_dir)
    
    # macOS iconset naming convention
    iconset_mapping = {
        16: 'icon_16x16.png',
        32: ['icon_16x16@2x.png', 'icon_32x32.png'],
        64: 'icon_32x32@2x.png',
        128: ['icon_128x128.png', 'icon_64x64@2x.png'],
        256: ['icon_128x128@2x.png', 'icon_256x256.png'],
        512: ['icon_256x256@2x.png', 'icon_512x512.png'],
        1024: 'icon_512x512@2x.png'
    }
    
    for size, names in iconset_mapping.items():
        resized = logo.resize((size, size), Image.Resampling.LANCZOS)
        if isinstance(names, list):
            for name in names:
                resized.save(f'{iconset_dir}/{name}', 'PNG')
        else:
            resized.save(f'{iconset_dir}/{names}', 'PNG')
    
    print("✅ Logo and icons created successfully!")
    print(f"📁 Files saved in: {assets_dir}/")
    print("📱 Icon sizes: 16, 32, 64, 128, 256, 512, 1024")
    print("🍎 macOS iconset created in: AppIcon.iconset/")

if __name__ == "__main__":
    try:
        create_icon_sizes()
    except ImportError:
        print("❌ PIL (Pillow) is required to create the logo")
        print("Install with: pip install Pillow")
    except Exception as e:
        print(f"❌ Error creating logo: {e}")