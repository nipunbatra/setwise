#!/bin/bash
# Automated demo recording script

echo "🎬 Setwise Demo Recording Suite"
echo "================================"

# Check requirements
if ! command -v asciinema &> /dev/null; then
    echo "❌ asciinema not found. Install with: pip install asciinema"
    exit 1
fi

# Setup clean environment
export PS1="$ "
clear

# Demo configurations
declare -A DEMOS=(
    ["demo1_quickstart"]="Setwise Quick Start (2-3 min)"
    ["demo2_formats"]="Multi-Format Support (3-4 min)"  
    ["demo3_validation"]="Smart Validation (2-3 min)"
    ["demo4_templates"]="Template Showcase (2-3 min)"
)

echo "Available demos:"
for demo in "${!DEMOS[@]}"; do
    echo "  📹 $demo: ${DEMOS[$demo]}"
done
echo ""

# Recording function
record_demo() {
    local demo_name=$1
    local demo_title="${DEMOS[$demo_name]}"
    
    echo "🎬 Recording: $demo_title"
    echo "Script: ${demo_name}.sh"
    echo ""
    echo "Press Enter to start recording, or Ctrl+C to skip..."
    read -r
    
    # Record with asciicinema
    asciicinema rec "${demo_name}.cast" \
        --title "$demo_title" \
        --command "./${demo_name}.sh" \
        --idle-time-limit 3 \
        --overwrite
    
    if [ $? -eq 0 ]; then
        echo "✅ Recording complete: ${demo_name}.cast"
        
        # Optional: Convert to GIF immediately
        if command -v agg &> /dev/null; then
            echo "🔄 Converting to GIF..."
            agg "${demo_name}.cast" "${demo_name}.gif"
            echo "✅ GIF created: ${demo_name}.gif"
        fi
        
        echo ""
    else
        echo "❌ Recording failed for $demo_name"
    fi
}

# Record all demos
for demo in demo1_quickstart demo2_formats demo3_validation demo4_templates; do
    if [ -f "${demo}.sh" ]; then
        record_demo "$demo"
    else
        echo "⚠️  Script not found: ${demo}.sh"
    fi
done

echo "🎉 All recordings complete!"
echo ""
echo "Files created:"
ls -la *.cast *.gif 2>/dev/null | grep -E '\.(cast|gif)$' || echo "  No recordings found"

echo ""
echo "Next steps:"
echo "1. Review recordings: asciicinema play demo1_quickstart.cast"
echo "2. Convert to MP4: See README.md for ffmpeg commands"
echo "3. Upload to repository or video platform"