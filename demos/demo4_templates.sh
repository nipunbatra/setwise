#!/bin/bash
# Demo 4: Template Showcase Demo (2-3 minutes)

# Change to parent directory if running from demos/
if [[ $(basename "$PWD") == "demos" ]]; then
    cd ..
fi

echo "🎬 Setwise Template Showcase Demo"
echo "========================================="
sleep 2

echo ""
echo "📋 Step 1: List available templates"
sleep 1
setwise list-templates
sleep 4

echo ""
echo "🎨 Step 2: Generate with different templates"
sleep 1

echo "--- Default Template (Professional) ---"
setwise generate --template default --sets 1 --no-pdf --output-dir demo_default
sleep 2

echo "--- Compact Template (Space-efficient) ---"
setwise generate --template compact --sets 1 --no-pdf --output-dir demo_compact
sleep 2

echo "--- Minimal Template (Clean) ---"
setwise generate --template minimal --sets 1 --no-pdf --output-dir demo_minimal  
sleep 2

echo ""
echo "📁 Step 3: Compare output files"
sleep 1
echo "File sizes comparison:"
ls -lh demo_*/quiz_set_1.tex | awk '{print $9 ": " $5}'
sleep 3

echo ""
echo "👀 Step 4: Preview template differences"
sleep 1
echo "--- Default Template Header ---"
head -15 demo_default/quiz_set_1.tex | grep -E "(documentclass|usepackage|title)"
sleep 2

echo ""
echo "--- Compact Template Header ---"
head -15 demo_compact/quiz_set_1.tex | grep -E "(documentclass|usepackage|multicol)"
sleep 2

echo ""
echo "📊 Step 5: Template usage recommendations"
sleep 1
echo "🏛️  Default: Formal exams, presentations (3-4 pages)"
echo "📄 Compact: Quick quizzes, printing (1-2 pages)" 
echo "⚪ Minimal: Simple assessments, accessibility (1-2 pages)"
sleep 3

echo ""
echo "🎯 Step 6: Smart template selection"
sleep 1
echo "For 20 questions → Use compact template"
setwise generate --template compact --mcq 15 --subjective 5 --sets 1 --no-pdf --output-dir smart_demo
sleep 2

echo ""
echo "🎉 Choose the right template for your needs!"
echo "📚 Same content, different presentation styles"
sleep 3

# Cleanup
rm -rf demo_default demo_compact demo_minimal smart_demo