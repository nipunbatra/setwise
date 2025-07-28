#!/bin/bash
# Demo 1: Quick Start Demo (2-3 minutes)

# Change to parent directory if running from demos/
if [[ $(basename "$PWD") == "demos" ]]; then
    cd ..
fi

echo "🎬 Setwise Quick Start Demo"
echo "========================================="
sleep 2

echo ""
echo "📦 Step 1: Install Setwise"
echo "pip install git+https://github.com/nipunbatra/setwise.git"
sleep 3

echo ""
echo "👋 Step 2: Welcome guide"
sleep 1
setwise welcome
sleep 5

echo ""
echo "🎯 Step 3: Generate your first quiz"
sleep 1
setwise generate --seed 42 --sets 2 --no-pdf
sleep 3

echo ""
echo "📁 Step 4: Check the output"
sleep 1
ls -la output/
sleep 2

echo ""
echo "📄 Step 5: Preview a LaTeX file"
sleep 1
head -20 output/quiz_set_1.tex
sleep 3

echo ""
echo "🎉 That's it! You've generated your first quiz with Setwise!"
echo "📚 For PDF generation, install LaTeX and remove --no-pdf flag"
sleep 3