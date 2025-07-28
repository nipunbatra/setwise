# Setwise Demo Recordings

This directory contains scripts for creating demo recordings of Setwise features.

## Quick Recording Setup

### 1. Install Requirements

```bash
# Install asciicinema
pip install asciinema

# Install agg for GIF conversion (optional)
curl -LO https://github.com/asciinema/agg/releases/latest/download/agg-x86_64-unknown-linux-gnu
chmod +x agg-x86_64-unknown-linux-gnu
sudo mv agg-x86_64-unknown-linux-gnu /usr/local/bin/agg

# For MP4 conversion, install ffmpeg
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

### 2. Record Demos

```bash
# Record each demo
asciicinema rec demo1_quickstart.cast -c "./demo1_quickstart.sh"
asciicinema rec demo2_formats.cast -c "./demo2_formats.sh"  
asciicinema rec demo3_validation.cast -c "./demo3_validation.sh"
asciicinema rec demo4_templates.cast -c "./demo4_templates.sh"
```

### 3. Convert to MP4

```bash
# Method 1: Using asciicinema-agg (recommended)
agg demo1_quickstart.cast demo1_quickstart.gif
ffmpeg -i demo1_quickstart.gif -pix_fmt yuv420p demo1_quickstart.mp4

# Method 2: Using asciinema2gif + ffmpeg
npm install -g asciinema2gif
asciinema2gif -t solarized-dark demo1_quickstart.cast demo1_quickstart.gif
ffmpeg -i demo1_quickstart.gif -pix_fmt yuv420p demo1_quickstart.mp4

# Method 3: Direct with svg-term + ffmpeg
npm install -g svg-term-cli
svg-term --in demo1_quickstart.cast --out demo1_quickstart.svg
# Then use online converter or Puppeteer to create MP4
```

## Demo Scripts

### demo1_quickstart.sh (2-3 minutes)
- Installation process
- Welcome guide
- First quiz generation
- Output exploration

**Key highlights:**
- Simple pip install
- No LaTeX required with --no-pdf
- Immediate results

### demo2_formats.sh (3-4 minutes)  
- Format comparison
- Format recommendation
- Creating examples in all formats
- Converting between formats
- Generating from different formats

**Key highlights:**
- 5 supported formats
- Seamless conversion
- Format-specific benefits

### demo3_validation.sh (2-3 minutes)
- Smart LaTeX validation
- Auto-fix capabilities  
- Enhanced error messages
- Quality improvement workflow

**Key highlights:**
- Intelligent error detection
- Automatic chemistry/math fixes
- Professional LaTeX output

### demo4_templates.sh (2-3 minutes)
- Template showcase
- Different template outputs
- Template selection guidance
- Use case recommendations

**Key highlights:**
- Professional layouts
- Space efficiency options
- Accessibility considerations

## Recording Tips

### Terminal Setup
```bash
# Set optimal terminal size (standardized)
resize -s 30 100

# Use a clean prompt
export PS1="$ "

# Clear screen before recording
clear
```

### Recording Settings
```bash
# Record with metadata
asciicinema rec demo.cast \
  --title "Setwise Demo" \
  --command "./demo_script.sh" \
  --idle-time-limit 3 \
  --overwrite
```

### Conversion Settings
```bash
# High quality MP4 conversion
ffmpeg -i demo.gif \
  -vf "scale=1200:800,fps=10" \
  -pix_fmt yuv420p \
  -crf 18 \
  demo.mp4
```

## Publishing

### GitHub Repository
- Add MP4 files to `assets/demos/` directory
- Link from README.md
- Include in documentation

### YouTube/Social Media
- Upload MP4 files directly
- Add captions for accessibility
- Include links in descriptions

### Website Integration
- Embed MP4 with HTML5 video tags
- Provide fallback GIF versions
- Add video controls and subtitles

## Example Conversion Commands

```bash
# Full workflow for all demos
for demo in demo1_quickstart demo2_formats demo3_validation demo4_templates; do
    echo "Recording $demo..."
    asciicinema rec ${demo}.cast -c "./${demo}.sh" --idle-time-limit 3 --overwrite
    
    echo "Converting $demo to GIF..."
    agg ${demo}.cast ${demo}.gif
    
    echo "Converting $demo to MP4..."
    ffmpeg -i ${demo}.gif -vf "scale=1200:800,fps=10" -pix_fmt yuv420p -crf 18 ${demo}.mp4
    
    echo "✅ $demo complete!"
done
```

## Customization

### Modify Scripts
- Edit timing with `sleep` commands
- Add your own examples
- Customize terminal colors
- Include your specific use cases

### Recording Variations
- **Quick version**: 1-2 minutes per demo
- **Detailed version**: 5-7 minutes with explanations  
- **Silent version**: No pauses, just commands
- **Narrated version**: Add voice-over post-production

### Themes
- Use consistent terminal theme (solarized-dark recommended)
- Match your organization's colors
- Consider accessibility (high contrast)

---

**Ready to record?** Run `./demo1_quickstart.sh` first to test, then use asciicinema to capture it!