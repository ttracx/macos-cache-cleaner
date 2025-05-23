#!/usr/bin/env python3
"""
Create App Icon for macOS Cache Cleaner
Generates a modern, clean icon using Python PIL/Pillow

Created by: Tommy Xaypanya
GitHub: https://github.com/ttracx
Email: mail@tommytracx.com
Version: 1.0.0
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL/Pillow not available. Installing...")
    import subprocess
    import sys
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image, ImageDraw, ImageFont
        PIL_AVAILABLE = True
        print("✅ Pillow installed successfully")
    except:
        print("❌ Could not install Pillow. Creating simple icon instead.")

import os
import math
from pathlib import Path

def create_gradient_background(size, color1, color2):
    """Create a gradient background"""
    image = Image.new('RGBA', size, color1)
    draw = ImageDraw.Draw(image)
    
    for y in range(size[1]):
        # Calculate gradient ratio
        ratio = y / size[1]
        # Interpolate between colors
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        a = int(color1[3] * (1 - ratio) + color2[3] * ratio)
        
        draw.line([(0, y), (size[0], y)], fill=(r, g, b, a))
    
    return image

def create_sparkle(x, y, size, color):
    """Create a sparkle/star shape"""
    points = []
    for i in range(8):
        angle = (i * math.pi) / 4
        if i % 2 == 0:
            # Outer points
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
        else:
            # Inner points
            px = x + (size * 0.4) * math.cos(angle)
            py = y + (size * 0.4) * math.sin(angle)
        points.extend([px, py])
    return points

def create_cache_cleaner_icon(size=1024):
    """Create the main cache cleaner icon"""
    if not PIL_AVAILABLE:
        return create_simple_icon()
    
    # Create base image with gradient background
    bg_color1 = (240, 248, 255, 255)  # Light blue
    bg_color2 = (176, 224, 230, 255)  # Powder blue
    image = create_gradient_background((size, size), bg_color1, bg_color2)
    draw = ImageDraw.Draw(image)
    
    # Add rounded rectangle background
    margin = size // 16
    corner_radius = size // 8
    bg_rect = [margin, margin, size - margin, size - margin]
    
    # Create rounded rectangle mask
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(bg_rect, radius=corner_radius, fill=255)
    
    # Apply gradient with rounded corners
    rounded_bg = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    rounded_bg.paste(image, mask=mask)
    image = rounded_bg
    draw = ImageDraw.Draw(image)
    
    # Main cleaning brush
    brush_width = size // 6
    brush_height = size // 2
    brush_x = size // 2 - brush_width // 2
    brush_y = size // 2 - brush_height // 4
    
    # Brush handle (wooden brown)
    handle_color = (139, 69, 19, 255)  # Saddle brown
    handle_width = brush_width // 3
    handle_height = brush_height // 2
    handle_x = brush_x + (brush_width - handle_width) // 2
    handle_y = brush_y + brush_height - handle_height
    
    draw.rounded_rectangle([handle_x, handle_y, handle_x + handle_width, handle_y + handle_height],
                          radius=handle_width // 6, fill=handle_color)
    
    # Brush ferrule (metal band)
    ferrule_color = (192, 192, 192, 255)  # Silver
    ferrule_height = size // 32
    ferrule_y = brush_y + brush_height - handle_height - ferrule_height
    
    draw.rectangle([brush_x, ferrule_y, brush_x + brush_width, ferrule_y + ferrule_height],
                  fill=ferrule_color)
    
    # Brush bristles
    bristle_color = (105, 105, 105, 255)  # Dim gray
    bristle_count = 12
    bristle_width = brush_width // bristle_count
    bristle_height = brush_height // 2
    
    for i in range(bristle_count):
        bristle_x = brush_x + i * bristle_width
        # Add slight variation in height
        variation = (i % 3 - 1) * size // 64
        bristle_end_y = brush_y + bristle_height + variation
        
        draw.rectangle([bristle_x, brush_y, bristle_x + bristle_width - 2, bristle_end_y],
                      fill=bristle_color)
    
    # Add cleaning sparkles/effects
    sparkle_color = (255, 215, 0, 255)  # Gold
    sparkle_positions = [
        (size * 0.25, size * 0.25),
        (size * 0.75, size * 0.2),
        (size * 0.2, size * 0.6),
        (size * 0.8, size * 0.7),
        (size * 0.3, size * 0.8),
        (size * 0.7, size * 0.4),
    ]
    
    for x, y in sparkle_positions:
        sparkle_size = size // 40
        points = create_sparkle(x, y, sparkle_size, sparkle_color)
        draw.polygon(points, fill=sparkle_color)
    
    # Add circular cleaning motion lines
    motion_color = (70, 130, 180, 128)  # Steel blue with transparency
    center_x, center_y = size // 2, size // 3
    
    for radius in [size // 4, size // 3.5, size // 3]:
        # Create circular arc
        bbox = [center_x - radius, center_y - radius, 
                center_x + radius, center_y + radius]
        draw.arc(bbox, start=45, end=225, fill=motion_color, width=3)
    
    # Add subtle shadow/depth
    shadow_color = (0, 0, 0, 30)
    shadow_offset = size // 64
    
    # Shadow for brush
    draw.rounded_rectangle([handle_x + shadow_offset, handle_y + shadow_offset, 
                           handle_x + handle_width + shadow_offset, 
                           handle_y + handle_height + shadow_offset],
                          radius=handle_width // 6, fill=shadow_color)
    
    return image

def create_simple_icon():
    """Create a simple text-based icon if PIL is not available"""
    print("Creating simple SVG icon...")
    
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1024" height="1024" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#f0f8ff;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#b0e0e6;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect x="64" y="64" width="896" height="896" rx="128" ry="128" fill="url(#bg)"/>
  
  <!-- Brush handle -->
  <rect x="432" y="600" width="160" height="300" rx="20" ry="20" fill="#8B4513"/>
  
  <!-- Brush ferrule -->
  <rect x="400" y="580" width="224" height="32" fill="#C0C0C0"/>
  
  <!-- Brush bristles -->
  <rect x="408" y="300" width="16" height="280" fill="#696969"/>
  <rect x="432" y="300" width="16" height="280" fill="#696969"/>
  <rect x="456" y="300" width="16" height="280" fill="#696969"/>
  <rect x="480" y="300" width="16" height="280" fill="#696969"/>
  <rect x="504" y="300" width="16" height="280" fill="#696969"/>
  <rect x="528" y="300" width="16" height="280" fill="#696969"/>
  <rect x="552" y="300" width="16" height="280" fill="#696969"/>
  <rect x="576" y="300" width="16" height="280" fill="#696969"/>
  <rect x="600" y="300" width="16" height="280" fill="#696969"/>
  
  <!-- Sparkles -->
  <polygon points="256,256 268,268 256,280 244,268" fill="#FFD700"/>
  <polygon points="768,200 780,212 768,224 756,212" fill="#FFD700"/>
  <polygon points="200,600 212,612 200,624 188,612" fill="#FFD700"/>
  <polygon points="800,700 812,712 800,724 788,712" fill="#FFD700"/>
  <polygon points="300,800 312,812 300,824 288,812" fill="#FFD700"/>
  
  <!-- Motion lines -->
  <path d="M 400 300 A 100 100 0 0 1 600 300" stroke="#4682B4" stroke-width="6" fill="none" opacity="0.5"/>
  <path d="M 350 350 A 150 150 0 0 1 650 350" stroke="#4682B4" stroke-width="4" fill="none" opacity="0.3"/>
  
</svg>'''
    
    return svg_content

def create_iconset():
    """Create a complete .iconset directory with all required sizes"""
    script_dir = Path(__file__).parent
    iconset_dir = script_dir / "AppIcon.iconset"
    
    # Create iconset directory
    iconset_dir.mkdir(exist_ok=True)
    
    # Required icon sizes for macOS
    sizes = [
        (16, "icon_16x16.png"),
        (32, "icon_16x16@2x.png"),
        (32, "icon_32x32.png"),
        (64, "icon_32x32@2x.png"),
        (128, "icon_128x128.png"),
        (256, "icon_128x128@2x.png"),
        (256, "icon_256x256.png"),
        (512, "icon_256x256@2x.png"),
        (512, "icon_512x512.png"),
        (1024, "icon_512x512@2x.png"),
    ]
    
    if PIL_AVAILABLE:
        print("🎨 Creating icon files...")
        
        # Create master icon at highest resolution
        master_icon = create_cache_cleaner_icon(1024)
        
        # Generate all required sizes
        for size, filename in sizes:
            resized_icon = master_icon.resize((size, size), Image.Resampling.LANCZOS)
            resized_icon.save(iconset_dir / filename, "PNG")
            print(f"  ✅ Created {filename} ({size}x{size})")
            
        # Save master icon as well
        master_icon.save(iconset_dir.parent / "icon_1024.png", "PNG")
        
    else:
        print("🎨 Creating SVG icon...")
        svg_content = create_simple_icon()
        with open(iconset_dir.parent / "icon.svg", 'w') as f:
            f.write(svg_content)
        print("  ✅ Created icon.svg")
        print("  ℹ️  Convert to PNG using online tools or install Pillow for automatic generation")
    
    return iconset_dir

def create_icns_file(iconset_dir):
    """Convert iconset to .icns file using iconutil"""
    try:
        import subprocess
        
        icns_path = iconset_dir.parent / "AppIcon.icns"
        
        # Use iconutil to create .icns file
        result = subprocess.run([
            'iconutil', '-c', 'icns', str(iconset_dir), '-o', str(icns_path)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Created AppIcon.icns")
            return icns_path
        else:
            print(f"❌ iconutil failed: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("❌ iconutil not found (not on macOS?)")
        return None
    except Exception as e:
        print(f"❌ Error creating .icns file: {e}")
        return None

def update_app_bundle(icns_path):
    """Update the existing app bundle with the new icon"""
    script_dir = Path(__file__).parent
    app_bundle = script_dir / "Cache Cleaner.app"
    
    if app_bundle.exists() and icns_path and icns_path.exists():
        resources_dir = app_bundle / "Contents" / "Resources"
        resources_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy icon to app bundle
        import shutil
        shutil.copy2(icns_path, resources_dir / "AppIcon.icns")
        print(f"✅ Updated app bundle with new icon")
        
        # Remove placeholder text file
        placeholder = resources_dir / "AppIcon.txt"
        if placeholder.exists():
            placeholder.unlink()
            
        return True
    
    return False

def main():
    print("🎨 Cache Cleaner Icon Creator")
    print("============================")
    
    if not PIL_AVAILABLE:
        print("⚠️  Pillow not available - creating simple SVG icon")
        print("   For best results, install Pillow: pip install Pillow")
        print()
    
    # Create iconset
    iconset_dir = create_iconset()
    
    # Create .icns file (macOS only)
    if PIL_AVAILABLE:
        icns_path = create_icns_file(iconset_dir)
        
        # Update app bundle if it exists
        if update_app_bundle(icns_path):
            print("🎉 App bundle updated with new icon!")
        else:
            print("ℹ️  Run './create_app.sh' to create app bundle with new icon")
    
    print()
    print("Icon files created:")
    print(f"  📁 Iconset: {iconset_dir}")
    if PIL_AVAILABLE:
        print(f"  🖼️  Master: {iconset_dir.parent / 'icon_1024.png'}")
        if (iconset_dir.parent / "AppIcon.icns").exists():
            print(f"  📦 macOS: {iconset_dir.parent / 'AppIcon.icns'}")
    else:
        print(f"  📄 SVG: {iconset_dir.parent / 'icon.svg'}")
    
    print("\nNext steps:")
    if PIL_AVAILABLE:
        print("  1. Icon is ready to use!")
        print("  2. Run './create_app.sh' to rebuild app with icon")
    else:
        print("  1. Install Pillow: pip install Pillow")
        print("  2. Re-run this script for full icon generation")
        print("  3. Or convert icon.svg to PNG manually")

if __name__ == "__main__":
    main()