# Quick Start - ML Assignment 2 Submission

## 🚀 Step-by-Step Submission Process

### Step 1: Commit Your Changes (Do this now!)

```bash
# Commit all changes
git commit -m "Complete ML Assignment 2: All models trained, Streamlit app ready with improvements"

# Verify commit
git log --oneline -1
```

---

### Step 2: Create GitHub Repository

1. **Go to GitHub**: https://github.com/new
2. **Repository name**: `ML_Assignment_2` (or your choice)
3. **Description**: "ML Assignment 2 - Adult Income Classification"
4. **Visibility**: ⚠️ **MUST BE PUBLIC** (for Streamlit free tier)
5. **DO NOT** check any boxes (README, .gitignore, license)
6. Click **"Create repository"**

---

### Step 3: Push to GitHub

After creating the repository, GitHub shows commands. Use these:

```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ML_Assignment_2.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**If you get authentication error:**
- Use Personal Access Token instead of password
- Generate token: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Use token as password when pushing

---

### Step 4: Deploy to Streamlit Cloud

1. **Go to**: https://streamlit.io/cloud
2. **Sign in** with your GitHub account
3. Click **"New app"** button
4. **Fill the form**:
   - Repository: Select `ML_Assignment_2`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: Leave default (or customize)
5. Click **"Deploy"**
6. **Wait 2-5 minutes**
7. Your app URL: `https://YOUR_APP_NAME.streamlit.app`

**Verify deployment:**
- App loads without errors ✅
- Model dropdown works ✅
- Metrics display correctly ✅
- CSV upload works ✅

---

### Step 5: Take Screenshot on BITS Virtual Lab

**Option A: Training Script (Recommended)**
```bash
# Run training
python3 train_models.py

# Take screenshot showing:
# - Terminal with BITS Virtual Lab prompt/identifier
# - Output showing "Training complete. Models and metrics saved in model/."
```

**Option B: Streamlit App**
```bash
# Run app
streamlit run app.py

# Take screenshot showing:
# - Terminal with "You can now view your Streamlit app..."
# - Browser window with app (optional)
```

**Screenshot Tips:**
- Include BITS Virtual Lab identifier/URL
- Show clear execution output
- Full terminal window visible
- Save as PNG or JPG

---

### Step 6: Create Submission PDF

**Method 1: Using SUBMISSION_TEMPLATE.md**

1. Open `SUBMISSION_TEMPLATE.md`
2. Replace placeholders:
   - `YOUR_USERNAME` → Your GitHub username
   - `YOUR_APP_NAME` → Your Streamlit app name
3. Insert your screenshot
4. Copy all content
5. Paste into:
   - **LibreOffice Writer** → Export as PDF
   - **Google Docs** → Download as PDF
   - **Word** → Save as PDF

**Method 2: Direct PDF Creation**

1. Create new document
2. Add sections in this order:
   - GitHub Repository Link
   - Live Streamlit App Link
   - Screenshot (with caption)
   - README Content (copy from README.md)
3. Export as PDF

**PDF Checklist:**
- [ ] GitHub link (clickable)
- [ ] Streamlit link (clickable)
- [ ] Screenshot inserted
- [ ] README content complete
- [ ] All sections in correct order

---

### Step 7: Submit

1. Go to assignment submission portal (Taxila/BITS Virtual Lab)
2. Upload the PDF
3. **⚠️ IMPORTANT: Click SUBMIT (not just upload)**
4. Verify submission confirmation

---

## ✅ Final Checklist

Before submitting, verify:

- [ ] All files committed to git
- [ ] GitHub repository is **PUBLIC**
- [ ] All files pushed to GitHub
- [ ] Streamlit app deployed and **accessible**
- [ ] App works without errors
- [ ] Screenshot taken on BITS Virtual Lab
- [ ] PDF contains all 4 sections in order
- [ ] All links in PDF are clickable
- [ ] README content included in PDF
- [ ] PDF submitted (not just uploaded as draft)

---

## 🆘 Troubleshooting

### Can't push to GitHub?
```bash
# Check remote
git remote -v

# If wrong, remove and re-add
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### Streamlit deployment fails?
- Check `requirements.txt` has all packages
- Verify repository is public
- Check `app.py` has no syntax errors
- Ensure `model/` directory is committed

### App shows "Models not found"?
- Verify `model/` directory is in repository
- Check all `.pkl` files are committed
- Verify file paths in `app.py` are relative

---

## 📞 Need Help?

- Check `SUBMISSION_GUIDE.md` for detailed instructions
- Run `./prepare_submission.sh` to check status
- Verify all files with `git status`

---

**Good luck with your submission! 🎓**
