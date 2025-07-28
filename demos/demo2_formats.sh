#!/bin/bash
# Demo 2: Multi-Format Support Demo (3-4 minutes)

# Change to parent directory if running from demos/
if [[ $(basename "$PWD") == "demos" ]]; then
    cd ..
fi

echo "🎬 Setwise Multi-Format Demo"
echo "========================================="
sleep 2

echo ""
echo "📋 Step 1: Compare available formats"
sleep 1
setwise questions format-comparison
sleep 5

echo ""
echo "📚 Step 2: Get personalized format recommendation"
sleep 1
echo "Simulating interactive recommendation..."
echo "Are you comfortable with code? n"
echo "Do you use Excel/Sheets? y"
echo "Result: CSV format recommended!"
sleep 3

echo ""
echo "📂 Step 3: Create examples in all formats"
sleep 1
setwise questions create-examples --output-dir format_demo
sleep 2

echo ""
echo "📁 Step 4: See all format examples"
sleep 1
ls -la format_demo/
sleep 3

echo ""
echo "👀 Step 5: Compare YAML vs JSON format"
sleep 1
echo "--- YAML format (human-readable) ---"
head -10 format_demo/sample_questions.yaml
sleep 3

echo ""
echo "--- JSON format (web-friendly) ---"
head -10 format_demo/sample_questions.json
sleep 3

echo ""
echo "🔄 Step 6: Convert between formats"
sleep 1
setwise questions convert format_demo/sample_questions.py converted.yaml
echo "✅ Converted Python to YAML"
sleep 2

echo ""
echo "✨ Step 7: Generate quiz from YAML format"
sleep 1
setwise generate --questions-file converted.yaml --sets 1 --no-pdf
sleep 2

echo ""
echo "🎉 Multi-format support makes Setwise work with any workflow!"
sleep 3