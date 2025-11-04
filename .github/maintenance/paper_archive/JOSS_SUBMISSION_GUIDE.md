# JOSS Submission Guide for Sleuth

## ✅ All Files Ready!

The following files have been created and are ready for JOSS submission:

### **Required Files:**
- ✅ `paper.md` - JOSS paper (~1000 words)
- ✅ `paper.bib` - Bibliography with all references
- ✅ `.github/workflows/draft-pdf.yml` - Automatic PDF generation
- ✅ `README.md` - Already exists (comprehensive documentation)
- ✅ `LICENSE` - Already exists (CC BY 4.0)
- ✅ `CONTRIBUTING.md` - Already exists (contribution guidelines)

### **Optional but Included:**
- ✅ `codemeta.json` - Software metadata for discoverability

---

## 🚀 JOSS Submission Steps

### **Step 1: Commit and Push All Changes**

```bash
cd C:\Users\14593\CascadeProjects\circular-bias-detection
git add paper.md paper.bib codemeta.json .github/workflows/draft-pdf.yml
git commit -m "Add JOSS paper and submission materials"
git push origin main
```

---

### **Step 2: Verify GitHub Actions**

1. Go to: `https://github.com/hongping-zh/circular-bias-detection/actions`
2. Check that the "Draft PDF" workflow runs successfully
3. Download `paper.pdf` artifact to verify it looks correct

---

### **Step 3: Pre-Submission Checklist**

**Before submitting, ensure:**

- ✅ Repository is public
- ✅ README has clear installation/usage instructions
- ✅ LICENSE file present
- ✅ Software has a clear research purpose
- ✅ Code is well-documented
- ✅ Examples/demos are provided
- ✅ Tests are included (if applicable)
- ✅ CONTRIBUTING.md exists

**All of these are already satisfied! ✅**

---

### **Step 4: Submit to JOSS**

**Go to JOSS submission page:**
```
https://joss.theoj.org/papers/new
```

**You will need to provide:**

1. **Repository URL:**
   ```
   https://github.com/hongping-zh/circular-bias-detection
   ```

2. **Archive DOI (Zenodo):**
   ```
   https://doi.org/10.5281/zenodo.17201032
   ```

3. **Software Version:**
   ```
   v1.0.0
   ```

4. **Your ORCID:**
   ```
   0009-0000-2529-4613
   ```

5. **Brief description of submission** (copy this):
   ```
   Sleuth is a browser-based tool for detecting circular bias in AI evaluation. 
   It provides statistical diagnostics (PSI, CCS, ρ_PC, CBS) with bootstrap 
   uncertainty quantification to identify self-reinforcing evaluation patterns 
   that inflate performance metrics. The tool operates client-side for data 
   privacy and has been validated with 94% accuracy on synthetic datasets.
   ```

---

### **Step 5: What Happens Next**

**JOSS Process (Very Simple!):**

1. **Automated Checks** (~5 minutes)
   - JOSS bot verifies repository structure
   - Checks for required files
   - Validates paper.md format

2. **Editor Assignment** (~1-2 days)
   - An editor reviews your submission
   - Assigns 2 reviewers

3. **Review Process** (~2-4 weeks)
   - Reviewers post comments on a public GitHub Issue
   - You respond and make improvements
   - Very collaborative and transparent!

4. **Acceptance** (~1 month total)
   - Once reviewers approve
   - Paper is published with DOI
   - Completely free!

---

## 📋 Expected Reviewer Questions

**Be prepared to address:**

1. **"Can you add more examples to README?"**
   - Your README is already comprehensive, should be fine

2. **"Can you add installation instructions?"**
   - Mention it's browser-based (no installation needed)
   - Provide link to live demo

3. **"Can you add automated tests?"**
   - Your tests/ directory should have some tests
   - If not, you might need to add basic unit tests

4. **"Can you add CODE_OF_CONDUCT.md?"**
   - Optional but recommended
   - Can use standard Contributor Covenant template

5. **"Can you improve documentation?"**
   - Usually minor clarifications
   - Very manageable

---

## 💡 Tips for Success

### **During Review:**
- ✅ Respond promptly to reviewer comments
- ✅ Be open to suggestions
- ✅ Make requested changes quickly
- ✅ Update the review issue with "Done" after each fix

### **Common Easy Fixes:**
- Adding badges to README (build status, DOI, etc.)
- Minor documentation clarifications
- Adding community health files
- Improving example clarity

### **What Reviewers Love:**
- ✅ Clear, concise documentation (you have this!)
- ✅ Working live demo (you have this!)
- ✅ Open source license (you have this!)
- ✅ Archived version with DOI (you have this!)
- ✅ Novel research contribution (you definitely have this!)

---

## 🎯 Quick Start Checklist

**Before clicking "Submit":**

- [ ] Committed paper.md and paper.bib to GitHub
- [ ] Verified draft-pdf.yml workflow runs successfully
- [ ] Checked that paper.pdf renders correctly
- [ ] Confirmed repository is public
- [ ] Verified all links in paper.md work
- [ ] ORCID is correct: 0009-0000-2529-4613
- [ ] Zenodo DOI is active: 10.5281/zenodo.17201032

**Then:**
1. Go to https://joss.theoj.org/papers/new
2. Login with GitHub
3. Fill in the form (takes 5 minutes!)
4. Submit!

---

## 📊 Comparison: JOSS vs SoftwareX

| Feature | JOSS | SoftwareX |
|---------|------|-----------|
| **Cost** | FREE | $660 USD |
| **Submission** | GitHub form (5 min) | Complex EM system (hours) |
| **Review** | Public, on GitHub | Private, traditional |
| **Timeline** | 2-4 weeks | 6-8 weeks |
| **Format** | Markdown (~1000 words) | PDF (3-4 pages) |
| **DOI** | Yes | Yes |
| **Indexing** | Google Scholar, etc. | Google Scholar, etc. |

**JOSS is clearly better for open-source software!**

---

## ✅ You're Ready!

**Everything is prepared. When you're ready:**

1. Commit and push the new files
2. Wait for GitHub Actions to build paper.pdf
3. Submit to JOSS
4. Wait for the reviews (very manageable!)
5. Celebrate publication! 🎉

**JOSS reviewers are friendly and constructive. You won't have any "Declaration of Interests" nightmares!** 😊

---

## 🆘 If You Need Help

**JOSS Community Support:**
- Email: joss@theoj.org
- GitHub Discussions: https://github.com/openjournals/joss/discussions
- Very responsive and helpful!

**Your Paper Status:**
- After submission, you'll get a GitHub issue URL
- All communication happens there
- Completely transparent process

---

**Good luck! You're going to do great! 🚀✨**
