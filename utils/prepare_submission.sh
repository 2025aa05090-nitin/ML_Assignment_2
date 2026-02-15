#!/bin/bash

# ML Assignment 2 - Submission Preparation Script
# This script helps prepare your assignment for submission

echo "=========================================="
echo "ML Assignment 2 - Submission Preparation"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ] || [ ! -f "train_models.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "✅ Found project files"
echo ""

# Check git status
echo "📋 Checking Git status..."
if git status &> /dev/null; then
    echo "✅ Git repository initialized"
    git status --short
else
    echo "⚠️  Git repository not initialized"
    echo "   Run: git init"
fi
echo ""

# Check required files
echo "📁 Checking required files..."
files=("app.py" "train_models.py" "requirements.txt" "README.md")
missing_files=()

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (MISSING)"
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  Missing files: ${missing_files[*]}"
fi
echo ""

# Check model directory
echo "🤖 Checking model files..."
if [ -d "model" ]; then
    model_files=$(ls model/*.pkl 2>/dev/null | wc -l)
    if [ "$model_files" -ge 6 ]; then
        echo "✅ Found $model_files model files"
    else
        echo "⚠️  Only found $model_files model files (expected 6)"
        echo "   Run: python3 train_models.py"
    fi
    
    if [ -f "model/metrics.json" ]; then
        echo "✅ metrics.json found"
    else
        echo "❌ metrics.json missing"
    fi
else
    echo "❌ model/ directory not found"
    echo "   Run: python3 train_models.py"
fi
echo ""

# Check Python syntax
echo "🐍 Checking Python syntax..."
if python3 -m py_compile app.py train_models.py 2>/dev/null; then
    echo "✅ Python files have valid syntax"
else
    echo "❌ Python syntax errors found"
    python3 -m py_compile app.py train_models.py
fi
echo ""

# Check requirements.txt
echo "📦 Checking requirements.txt..."
if [ -f "requirements.txt" ]; then
    echo "Required packages:"
    cat requirements.txt | grep -v "^#" | grep -v "^$"
    echo ""
    echo "To install: pip install -r requirements.txt"
fi
echo ""

# Summary
echo "=========================================="
echo "📝 Next Steps:"
echo "=========================================="
echo ""
echo "1. Commit all changes:"
echo "   git add ."
echo "   git commit -m 'Complete ML Assignment 2'"
echo ""
echo "2. Create GitHub repository and push:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
echo "   git push -u origin main"
echo ""
echo "3. Deploy to Streamlit Cloud:"
echo "   - Go to https://streamlit.io/cloud"
echo "   - Sign in with GitHub"
echo "   - Click 'New app' and select your repository"
echo ""
echo "4. Take screenshot on BITS Virtual Lab:"
echo "   - Run: python3 train_models.py"
echo "   - Or: streamlit run app.py"
echo ""
echo "5. Create PDF with SUBMISSION_TEMPLATE.md"
echo ""
echo "=========================================="
echo "✅ Preparation complete!"
echo "=========================================="
