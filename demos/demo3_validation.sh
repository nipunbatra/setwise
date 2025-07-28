#!/bin/bash
# Demo 3: Smart Validation & Auto-Fix Demo (2-3 minutes)

# Change to parent directory if running from demos/
if [[ $(basename "$PWD") == "demos" ]]; then
    cd ..
fi

echo "🎬 Setwise Smart Validation Demo"
echo "========================================="
sleep 2

echo ""
echo "📝 Step 1: Create a questions file with common issues"
sleep 1

cat > demo_questions.yaml << 'EOF'
mcq:
  - question: "What is the chemical formula for water H2O?"
    options: ["H2O", "H2O2", "HO2"]
    answer: "H2O"
    marks: 1
  - question: "Calculate x^2 + y^2 when x=3 and y=4"
    options: ["25", "24", "23"]
    answer: "25"
    marks: 2

subjective:
  - question: "A projectile is fired at 45 degrees angle. Calculate maximum height."
    answer: "Using kinematics equations with angle 45 degrees..."
    marks: 5
EOF

echo "✅ Created demo_questions.yaml with LaTeX issues"
sleep 2

echo ""
echo "🔍 Step 2: Validate with detailed feedback"
sleep 1
setwise questions validate demo_questions.yaml --verbose --auto-suggest
sleep 5

echo ""
echo "👀 Step 3: Preview automatic fixes"
sleep 1
setwise questions fix-latex demo_questions.yaml --dry-run
sleep 4

echo ""
echo "🛠️ Step 4: Apply automatic fixes"
sleep 1
setwise questions fix-latex demo_questions.yaml
sleep 2

echo ""
echo "✅ Step 5: Validate the fixed file"
sleep 1
setwise questions validate demo_questions.yaml --verbose
sleep 3

echo ""
echo "📊 Step 6: Check question statistics"
sleep 1
setwise questions stats demo_questions.yaml
sleep 3

echo ""
echo "🎯 Step 7: Generate quiz from improved questions"
sleep 1
setwise generate --questions-file demo_questions.yaml --sets 1 --no-pdf
sleep 2

echo ""
echo "🎉 Smart validation ensures high-quality LaTeX output!"
echo "🧠 Auto-fixes: H2O→H\$_2\$O, x^2→\$x^{2}\$, degrees→°"
sleep 3

# Cleanup
rm -f demo_questions.yaml