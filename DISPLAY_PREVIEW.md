# 🖼️ Todoist E-Paper Display - Visual Preview

## Generated SVG Previews

I've created three SVG files showing exactly how your Todoist tasks will appear on the e-paper display:

---

## 1. `todoist-display-preview.svg`
**Simple, clean preview with your actual tasks**

This shows:
- Current time (10:30 AM)
- Date (Monday, Nov 11, 2025)
- Weather icon and temperature
- Your first 4 Todoist tasks:
  1. Saturday - 278 examples and simulation using MKL46Z
  2. Sunday - More kinetics examples
  3. Tuesday 2:45 AM - Attorney appointment
  4. Today - Welcome to Todoist 👋

---

## 2. `todoist-display-detailed.svg`
**Detailed layout showing 5 tasks**

This shows:
- Larger, more readable fonts
- Better spacing
- First 5 tasks displayed
- "5 more tasks..." indicator at bottom
- Calendar icon
- Professional layout

---

## 3. `todoist-epaper-realistic.svg` ⭐ **MOST REALISTIC**
**Simulates actual e-paper display appearance**

This shows:
- E-paper texture/background (#F5F5F0 off-white)
- Black and white only (no colors)
- Device frame border
- Exact 800x480 resolution
- How it will actually look on the physical display

---

## Display Layout Breakdown

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  10:30 AM                              Monday                  │
│                                        Nov 11, 2025             │
│                                                                 │
│  ☀️                          │  📅 Calendar Icon               │
│  Weather Icon               │                                  │
│                             │  Saturday                        │
│  20°C/15°C                  │  278 examples and simulation...  │
│  Partly Cloudy              │                                  │
│                             │  Sunday                          │
│                             │  More kinetics examples          │
│                             │                                  │
│                             │  Tuesday 2:45 AM                 │
│                             │  Attorney appointment            │
│                             │                                  │
│                             │  Today                           │
│                             │  Welcome to Todoist 👋           │
│                             │                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Your Actual Tasks (As They Will Display)

### ✅ Tasks with Due Dates (3)
1. **Saturday** - 278 examples and simulation using MKL46Z
2. **Sunday** - More kinetics examples
3. **Tuesday 2:45 AM** - Attorney appointment

### ✅ Tasks without Due Dates (7 - shown as "Today")
4. **Today** - Welcome to Todoist 👋 Let's get you started with a few tips:
5. **Today** - Create a new task ➕
6. **Today** - Tap the checkbox to complete this task ✅
7. **Today** - Swipe left to schedule this task 📅
8. **Today** - Create your own project 🗒
9. **Today** - [Learn how to use Todoist with the Guide →]
10. **Today** - [Get organized at work with the apps →]

---

## Display Specifications

- **Resolution:** 800 x 480 pixels
- **Display Type:** E-Paper (Black & White)
- **Refresh Rate:** Updates every hour (configurable)
- **Font:** Sans-serif (system default)
- **Layout:** Template 1 (default)
- **Max Tasks Shown:** 10

---

## How to View the SVGs

### Option 1: Open in Browser
```bash
# On Mac
open todoist-epaper-realistic.svg

# On Linux
xdg-open todoist-epaper-realistic.svg

# On Windows
start todoist-epaper-realistic.svg
```

### Option 2: View in VS Code
Just click on any of the SVG files in VS Code to see the preview.

### Option 3: Convert to PNG
```bash
# If you have cairosvg installed
.venv/bin/cairosvg todoist-epaper-realistic.svg -o preview.png
```

---

## Customization Options

### Change Number of Tasks Displayed
Edit `screen-calendar-get.py`:
```python
max_event_results = 10  # Change to 15, 20, etc.
```

### Change Layout
Edit `env.sh`:
```bash
export SCREEN_LAYOUT=2  # Try layouts 1-5
```

### Change Font Size
Edit the SVG template files:
```bash
screen-template.1.svg  # Default layout
screen-template.2.svg  # More calendar entries
screen-template.3.svg  # Calendar on left
screen-template.4.svg  # Color version
screen-template.5.svg  # With month calendar
```

---

## What Happens on the Raspberry Pi

1. **Every hour** (or as configured):
   - `run.sh` executes
   - Weather data fetched from API
   - Todoist tasks fetched from API
   - Data cached for 1 hour

2. **SVG Generation**:
   - Template SVG loaded
   - Placeholders replaced with real data
   - Output SVG created

3. **Image Conversion**:
   - SVG converted to PNG (800x480)
   - PNG optimized for e-paper

4. **Display Update**:
   - PNG sent to e-paper display
   - Screen refreshes (takes ~6 seconds)
   - Display shows updated information

---

## Tips for Best Results

### 1. Add Due Dates
Tasks without due dates all show as "Today". Add specific dates for better organization.

### 2. Use Priorities
Set priorities in Todoist to see indicators:
- P1 → 🔴 Red circle
- P2 → 🟡 Yellow circle
- P3 → 🔵 Blue circle

### 3. Keep Task Names Short
Long task names may be truncated. Keep them under 50 characters for best display.

### 4. Update Old Tasks
Your first 3 tasks are from 2019. Update or complete them for a cleaner display.

### 5. Use Projects
Organize tasks in Todoist projects for better management (projects aren't shown on display, but help organization).

---

## Next Steps

1. ✅ Review the SVG previews
2. ✅ Verify the layout looks good
3. ✅ Deploy to Raspberry Pi
4. ✅ Run `./run.sh` to see it live
5. ✅ Set up cron for automatic updates

---

**Generated:** November 10, 2025  
**Status:** Ready for deployment  
**Preview Files:** 3 SVG files created
