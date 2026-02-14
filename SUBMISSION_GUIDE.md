# ML Assignment 2 - Submission Guide

This guide will help you complete all submission steps for ML Assignment 2.

## Step 1: Prepare GitHub Repository

### 1.1 Commit all changes
```bash
# Add all files
git add .

# Commit changes
git commit -m "Complete ML Assignment 2: All models trained and Streamlit app ready"

# Check status
git status
```

### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `ML_Assignment_2` (or your preferred name)
3. Description: "ML Assignment 2 - Adult Income Classification with Multiple Models"
4. Set to **Public** (required for Streamlit Community Cloud free tier)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### 1.3 Push to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ML_Assignment_2.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Streamlit Community Cloud

### 2.1 Prerequisites
- GitHub repository must be **Public**
- Repository must contain `app.py` and `requirements.txt`

### 2.2 Deployment Steps

1. Go to https://streamlit.io/cloud
2. Sign in with your **GitHub account**
3. Click **"New app"** button
4. Fill in the form:
   - **Repository**: Select your `ML_Assignment_2` repository
   - **Branch**: `main` (or `master`)
   - **Main file path**: `app.py`
   - **App URL**: Leave default or customize
5. Click **"Deploy"**
6. Wait 2-5 minutes for deployment
7. Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

### 2.3 Verify Deployment

- Check that the app loads without errors
- Test model selection dropdown
- Test CSV upload feature
- Verify all metrics display correctly

## Step 3: Take Screenshot on BITS Virtual Lab

### 3.1 What to Screenshot

You need **ONE screenshot** showing:
- Terminal/command line showing execution on BITS Virtual Lab
- OR Streamlit app running locally on BITS Virtual Lab
- OR Training script execution output

### 3.2 How to Take Screenshot

**Option A: Training Script Execution**
```bash
# Run the training script
python3 train_models.py

# Take screenshot of the terminal output showing "Training complete. Models and metrics saved in model/."
```

**Option B: Streamlit App Running**
```bash
# Run Streamlit app
streamlit run app.py

# Take screenshot of:
# - Terminal showing "You can now view your Streamlit app in your browser"
# - Browser window showing the app (optional but recommended)
```

**Option C: Both**
- Screenshot 1: Training output
- Screenshot 2: App running (combine into one image if needed)

### 3.3 Screenshot Tips

- Make sure BITS Virtual Lab identifier/URL is visible
- Include timestamp if possible
- Show clear execution output
- Use full-screen or clear terminal view

## Step 4: Create Submission PDF

### 4.1 Required Content (in order)

1. **GitHub Repository Link**
   - Format: `https://github.com/YOUR_USERNAME/ML_Assignment_2`
   - Make sure it's accessible and public

2. **Live Streamlit App Link**
   - Format: `https://YOUR_APP_NAME.streamlit.app`
   - Test the link before including

3. **Screenshot**
   - Insert the screenshot from Step 3
   - Add caption: "Screenshot of assignment execution on BITS Virtual Lab"

4. **README Content**
   - Copy the entire content from `README.md`
   - Include all sections:
     - Problem statement
     - Dataset description
     - Models used (Comparison Table)
     - Observations

### 4.2 PDF Creation Options

**Option A: Using LibreOffice Writer**
1. Open LibreOffice Writer
2. Copy-paste all content in order
3. Insert screenshot as image
4. Export as PDF: File → Export as PDF

**Option B: Using Google Docs**
1. Create new document
2. Add all content
3. Insert screenshot
4. Download as PDF: File → Download → PDF

**Option C: Using Markdown + Pandoc**
```bash
# Create submission.md with all content, then:
pandoc submission.md -o ML_Assignment_2_Submission.pdf
```

## Step 5: Final Checklist

Before submitting, verify:

- [ ] GitHub repository is **Public**
- [ ] All files are committed and pushed
- [ ] Streamlit app is deployed and **accessible**
- [ ] App works without errors
- [ ] Screenshot shows BITS Virtual Lab execution
- [ ] PDF contains all 4 required sections in order
- [ ] README content is complete in PDF
- [ ] All links in PDF are clickable and working

## Step 6: Submit

1. Go to your assignment submission portal (Taxila/BITS Virtual Lab)
2. Upload the PDF file
3. **DO NOT** submit as draft - make sure to **SUBMIT**
4. Verify submission confirmation

## Troubleshooting

### Streamlit Deployment Issues

**Problem**: App fails to deploy
- **Solution**: Check `requirements.txt` has all dependencies
- Verify `app.py` has no syntax errors
- Check repository is public

**Problem**: Models not found error
- **Solution**: Ensure `model/` directory and all `.pkl` files are committed
- Check file paths in `app.py` are relative

**Problem**: Import errors
- **Solution**: Verify all packages in `requirements.txt` are correct
- Check Python version compatibility

### GitHub Issues

**Problem**: Can't push to GitHub
- **Solution**: Check authentication (use Personal Access Token if needed)
- Verify remote URL is correct

**Problem**: Files too large
- **Solution**: Use Git LFS for large model files if needed
- Or exclude large files and regenerate on Streamlit Cloud

## Important Notes

- ⚠️ **Only ONE submission will be accepted** - no resubmissions
- ⚠️ **Deadline**: 15-Feb-2026 23:59 PM
- ⚠️ Make sure to **SUBMIT** not just upload as draft
- ⚠️ Test all links before including in PDF
- ⚠️ Repository must be public for Streamlit free tier

## Quick Command Reference

```bash
# Check git status
git status

# Add all files
git add .

# Commit
git commit -m "Complete ML Assignment 2"

# Push to GitHub
git push origin main

# Test Streamlit locally
streamlit run app.py

# Test training script
python3 train_models.py
```

Good luck with your submission! 🚀
