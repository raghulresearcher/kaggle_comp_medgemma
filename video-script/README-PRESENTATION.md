# MedAdhere Pro Presentation Guide

## 📁 Files

- **MedAdhere-Pro-Presentation.md** - Main Marp presentation (45 slides)

## 🎯 How to Use

### Option 1: Present Directly in VS Code (Recommended)

1. **Install Marp Extension:**
   - Open VS Code Extensions (Ctrl+Shift+X)
   - Search for "Marp for VS Code"
   - Install by marp-team

2. **Open Presentation:**
   - Open `MedAdhere-Pro-Presentation.md`
   - Click "Open Preview to the Side" (Ctrl+K V)
   - Or click Marp icon in status bar

3. **Present:**
   - Click "Open slide view" in preview
   - Use arrow keys to navigate
   - Press F11 for fullscreen

### Option 2: Export to PowerPoint

1. **Install Marp CLI:**
   ```bash
   npm install -g @marp-team/marp-cli
   ```

2. **Export to PPTX:**
   ```bash
   marp MedAdhere-Pro-Presentation.md --pptx -o MedAdhere-Pro.pptx
   ```

3. **Edit in PowerPoint:**
   - Open MedAdhere-Pro.pptx
   - Customize fonts, colors, layouts
   - Add speaker notes

### Option 3: Export to PDF

```bash
# Using Marp CLI
marp MedAdhere-Pro-Presentation.md --pdf -o MedAdhere-Pro.pdf

# Or in VS Code with Marp extension
# Right-click preview → "Export slide deck"
```

### Option 4: Export to HTML

```bash
# Standalone HTML (can present in browser)
marp MedAdhere-Pro-Presentation.md --html -o MedAdhere-Pro.html

# Open in browser and present
# Press P for presenter mode
```

## 📊 Presentation Structure

**Total Slides:** 45  
**Estimated Duration:** 25-30 minutes (detailed) or 10-12 minutes (fast)

### Slide Breakdown:

1. **Title Slide** (1)
2. **Problem/Crisis** (3 slides)
   - Statistics
   - Why solutions fail
   - Patient story
3. **Solution Overview** (3 slides)
   - System architecture
   - 5 agents
   - Why MedGemma
4. **Scenario Demonstrations** (9 slides)
   - Timing Conflict (3 slides)
   - Supplement Interference (3 slides)
   - Side Effects (3 slides)
5. **Impact Analysis** (4 slides)
   - Outcomes table
   - Scaling timeline
   - Economic model
6. **Production Roadmap** (3 slides)
   - Implementation phases
   - Architecture evolution
7. **Current Status** (5 slides)
   - What's built
   - Code quality
   - Technical validation
   - Validation plan
8. **Competition Assessment** (3 slides)
   - Criteria scorecard
   - Why we stand out
9. **Call to Action & Close** (2 slides)

## 🎨 Customization

### Change Theme Colors

Edit the `style` section at the top:

```css
h1 {
  color: #2c5aa0;  /* Change heading color */
}
.stat {
  color: #d32f2f;  /* Change statistics color */
}
```

### Add Your Logo

Add to any slide:

```markdown
![logo](path/to/logo.png)
```

### Change Background

Per-slide background:

```markdown
<!-- _backgroundColor: #f0f0f0 -->
# Your Slide Title
```

## 🎬 Presentation Tips

### For Competition Judges (10-12 minutes)
**Focus on these slides:**
1. Title (30 sec)
2. Problem statistics (1 min)
3. Solution + Architecture (2 min)
4. One scenario demo - pick Supplement Interference (2 min)
5. Impact metrics (2 min)
6. MedGemma validation (1 min)
7. Production roadmap (1.5 min)
8. Call to action (30 sec)

### For Technical Audience (25-30 minutes)
**Include all slides, emphasize:**
- Architecture details
- All 3 scenario demos
- MedGemma medical reasoning
- Code quality and documentation
- Validation methodology

### For Business Audience (15-20 minutes)
**Focus on:**
- Problem magnitude ($300B, 125K deaths)
- Patient stories (relatable)
- Impact metrics (ROI: 45:1)
- Scaling timeline
- Market opportunity ($28B market)

## 📝 Speaker Notes

### Key Messages to Emphasize

1. **Medical AI is Essential**
   - Not just reminders, actual medical reasoning
   - MedGemma provides accuracy general LLMs can't

2. **Working Prototype**
   - 100% functional, not mockups
   - All 3 scenarios tested successfully

3. **Quantified Impact**
   - 18,750 lives saved (conservative 15% improvement)
   - $45B annual cost savings
   - 45:1 ROI for payers

4. **Production Ready**
   - Complete roadmap with real integrations
   - HIPAA compliance path
   - Clinical validation planned

5. **Real-World Problem**
   - Patient stories demonstrate actual pain
   - $300B wasted annually (half of medication spending)
   - 125,000 preventable deaths

## 🔧 Troubleshooting

### Marp Extension Not Working?
1. Restart VS Code
2. Check extension is enabled
3. Open Command Palette (Ctrl+Shift+P) → "Marp: Open preview"

### Export Failed?
```bash
# Install dependencies
npm install -g @marp-team/marp-cli
npm install -g puppeteer

# Try export again
marp --version  # Should show version number
```

### Slides Look Different in Export?
- Fonts may differ between preview and export
- Test export early and adjust
- Use web-safe fonts (Arial, Helvetica, Verdana)

## 📤 Sharing

### For Competition Submission
✅ Export to PDF (universal format)  
✅ Include slide deck with video submission  
✅ Upload PPTX to Google Drive as backup

### For Social Media
✅ Export key slides as images (PNG)  
✅ Share impact metrics slide on LinkedIn  
✅ Create carousel post with problem → solution → impact

### For GitHub
✅ Keep markdown file in repo (version control)  
✅ Export PDF to releases  
✅ Link in README

## 🎯 Next Steps

1. **Review Presentation:** Read through all slides
2. **Practice Delivery:** Time yourself (aim for 10-12 min)
3. **Customize:** Add logo, adjust colors if needed
4. **Export:** Create PDF and PPTX versions
5. **Rehearse:** Practice with exported files
6. **Present:** Deliver with confidence!

---

**Good luck with your presentation!** 🚀

Questions? Check the Marp documentation: https://marpit.marp.app/
