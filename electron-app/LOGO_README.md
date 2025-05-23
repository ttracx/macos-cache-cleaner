# Cache Cleaner Logo

This document describes the logo design and implementation for the macOS Cache Cleaner application.

## Logo Design

The Cache Cleaner logo features:

- **Modern cleaning brush icon** with realistic bristles and handle
- **Blue gradient background** following Apple's design language
- **Golden sparkles** representing the cleaning effect
- **Professional appearance** suitable for macOS applications

### Design Elements

1. **Color Scheme**:
   - Primary: Apple Blue (#007AFF)
   - Secondary: Purple (#5856D6) 
   - Accent: Gold (#FFD700) for sparkles
   - Handle: Brown (#8B4513) for realism
   - Bristles: Gray (#696969) for professional look

2. **Symbolism**:
   - **Brush**: Core cleaning functionality
   - **Sparkles**: Active cleaning in progress
   - **Gradient**: Modern, premium feel
   - **Rounded corners**: Friendly, approachable

## File Structure

```
assets/
├── icon.icns              # macOS bundle icon
├── icon.png               # Main 512px icon
├── icon-1024.png          # High-res version
├── icon-128.png           # About dialog
├── icon-64.png            # Header logo
├── icon-32.png            # Favicon
├── icon-16.png            # Small UI elements
└── AppIcon.iconset/       # Complete iconset for macOS
    ├── icon_16x16.png
    ├── icon_16x16@2x.png
    ├── icon_32x32.png
    ├── icon_32x32@2x.png
    ├── icon_128x128.png
    ├── icon_128x128@2x.png
    ├── icon_256x256.png
    ├── icon_256x256@2x.png
    ├── icon_512x512.png
    └── icon_512x512@2x.png
```

## Usage in App

### Header Logo
- **Size**: 48x48px
- **File**: `icon-64.png` (downscaled for crisp display)
- **Features**: Hover animation, click Easter egg

### About Dialog
- **Size**: 96x96px  
- **File**: `icon-128.png`
- **Features**: Shadow, rounded corners

### Loading Screen
- **Size**: 96x96px
- **File**: `icon-128.png`
- **Features**: Pulse animation during loading

### App Icon
- **File**: `icon.icns` (multiple sizes)
- **Usage**: Dock, Finder, system dialogs

## Regenerating the Logo

To recreate or modify the logo:

1. **Install Pillow** (if not already installed):
   ```bash
   pip install Pillow
   ```

2. **Run the logo generator**:
   ```bash
   python3 create-logo.py
   ```

3. **Create macOS iconset**:
   ```bash
   iconutil -c icns assets/AppIcon.iconset -o assets/icon.icns
   ```

## Customization

To modify the logo design, edit `create-logo.py`:

- **Colors**: Change color constants at the top
- **Size**: Modify the `size` parameter
- **Elements**: Add/remove visual elements
- **Effects**: Adjust sparkle positions or brush details

## Brand Guidelines

### Do's ✅
- Use the logo at recommended sizes
- Maintain proper spacing around the logo
- Use on light or dark backgrounds appropriately
- Keep the aspect ratio locked

### Don'ts ❌
- Don't stretch or distort the logo
- Don't use extremely small sizes (under 16px)
- Don't change colors without updating the design
- Don't add effects that compromise clarity

## Technical Specifications

- **Format**: PNG with transparency
- **Color Profile**: sRGB
- **Compression**: Optimized for file size
- **Transparency**: Alpha channel preserved
- **Naming**: Consistent with Apple conventions

## Integration Notes

The logo is integrated into the app through:

1. **HTML**: Direct `<img>` tags with appropriate `src` paths
2. **CSS**: Styling for hover effects and animations  
3. **JavaScript**: Click interactions and loading states
4. **Electron**: Bundle icon configuration in `package.json`

## Future Enhancements

Potential logo improvements:
- **Dark mode variant**: Adjust colors for dark themes
- **Animated version**: SVG with cleaning motion
- **Themed variants**: Seasonal or special edition versions
- **Vector format**: SVG for perfect scaling