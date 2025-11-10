# Quick Start - Todoist Integration

## 🚀 5-Minute Setup

### 1. Get API Token
Visit: https://todoist.com/prefs/integrations
Copy your **API token**

### 2. Configure
```bash
# Edit env.sh
nano env.sh

# Add this line:
export TODOIST_API_TOKEN=your_token_here

# Save (Ctrl+O, Enter, Ctrl+X)
```

### 3. Load Config
```bash
source env.sh
```

### 4. Test
```bash
.venv/bin/python3 test_todoist.py
```

### 5. Run
```bash
./run.sh
```

## ✅ What You Get

- ✓ Your Todoist tasks on e-paper display
- ✓ Priority indicators (🔴🟡🔵)
- ✓ Due dates and times
- ✓ Auto-sorted by date
- ✓ Updates every hour (cached)

## 🔧 Customize

### Change cache duration
```bash
# In env.sh - update every 30 minutes
export CALENDAR_TTL=1800
```

### Show more tasks
```python
# In screen-calendar-get.py, line 18
max_event_results = 20  # Change from 10 to 20
```

## 🤖 Automate

```bash
crontab -e

# Add this line (updates every 20 minutes):
*/20 * * * * cd /home/pi/waveshare-epaper-display && bash run.sh > run.log 2>&1
```

## 📝 Priority Mapping

| Todoist | Display |
|---------|---------|
| P1      | 🔴      |
| P2      | 🟡      |
| P3      | 🔵      |
| P4      | (none)  |

## 🐛 Troubleshooting

**Token not found?**
```bash
source env.sh
```

**No tasks showing?**
- Add due dates to tasks in Todoist
- Check you have tasks in your account

**API errors?**
- Verify token is correct
- Check internet connection

## 📚 More Info

- Full setup: `TODOIST_SETUP.md`
- All changes: `TODOIST_CHANGES.md`
- Main docs: `README.md`
