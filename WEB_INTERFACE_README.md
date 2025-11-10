# 🌐 Web Interface for E-Paper Display

A beautiful, user-friendly web dashboard to configure and manage your Waveshare e-paper display with Todoist integration.

![Web Interface Preview](https://via.placeholder.com/800x400/667eea/ffffff?text=E-Paper+Display+Manager)

---

## ✨ Features

- 🎨 **Beautiful UI** - Modern, responsive design
- ⚙️ **Easy Configuration** - No need to edit files manually
- 🔄 **Live Updates** - Update display with one click
- 📊 **System Status** - Monitor cache, logs, and updates
- 📱 **Mobile Friendly** - Works on all devices
- 🔒 **Secure** - Optional authentication support

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ~/waveshare-epaper-display
.venv/bin/pip3 install -r requirements-web.txt
```

### 2. Start the Server

```bash
./start-web.sh
```

### 3. Open in Browser

Go to: **http://raspberrypi.local:5000**

---

## 📸 Screenshots

### Main Dashboard
- Configure Todoist API token
- Set weather location
- Choose display layout
- Adjust cache settings

### Actions Panel
- Update display instantly
- Clear cache files
- View system logs
- Monitor status

---

## 🎯 What You Can Do

### Configure Todoist
1. Enter your API token
2. Save configuration
3. Tasks appear automatically

### Set Weather Location
1. Enter latitude/longitude
2. Choose temperature format
3. Select weather provider

### Customize Display
1. Pick screen layout (1-5)
2. Choose Waveshare version
3. Adjust refresh intervals

### Manage System
1. Update display on demand
2. Clear cache when needed
3. View logs for debugging

---

## 🔧 Configuration Options

### Todoist Integration
- **API Token** - Your Todoist authentication token
- **Cache Duration** - How long to cache tasks (default: 1 hour)

### Weather Settings
- **Provider** - Met.no, OpenWeatherMap, etc.
- **Location** - Latitude and longitude
- **Format** - Celsius or Fahrenheit
- **Cache Duration** - How long to cache weather (default: 1 hour)

### Display Settings
- **Version** - Waveshare EPD 7.5" v1, v2, or v2B
- **Layout** - Choose from 5 different layouts
- **Log Level** - DEBUG, INFO, WARNING, ERROR

---

## 🌟 Advanced Features

### Run as Service

Make it start automatically on boot:

```bash
sudo nano /etc/systemd/system/epaper-web.service
```

Paste:
```ini
[Unit]
Description=E-Paper Display Web Interface
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/waveshare-epaper-display
ExecStart=/home/pi/waveshare-epaper-display/.venv/bin/python3 web_interface.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable epaper-web
sudo systemctl start epaper-web
```

### Add Authentication

For security, add basic authentication:

```python
# In web_interface.py, add:
from flask import request
from functools import wraps

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == 'admin' and auth.password == 'your_password'):
            return ('Unauthorized', 401, {
                'WWW-Authenticate': 'Basic realm="Login Required"'
            })
        return f(*args, **kwargs)
    return decorated

# Then add @requires_auth to routes
```

---

## 📱 Mobile Access

The interface is fully responsive and works perfectly on:
- iPhones and iPads
- Android phones and tablets
- Any modern web browser

---

## 🐛 Troubleshooting

### Can't Access Interface

**Check if server is running:**
```bash
ps aux | grep web_interface
```

**Check firewall:**
```bash
sudo ufw allow 5000/tcp
```

**Find Pi's IP:**
```bash
hostname -I
```

### Configuration Not Saving

**Check permissions:**
```bash
chmod 644 env.sh
```

**Check disk space:**
```bash
df -h
```

### Display Not Updating

**Test manually:**
```bash
./run.sh
```

**Check logs:**
```bash
tail -f run.log
```

---

## 🎨 Customization

### Change Colors

Edit `templates/index.html` and modify the CSS:

```css
body {
    background: linear-gradient(135deg, #your-color 0%, #your-color 100%);
}
```

### Add New Fields

1. Edit `web_interface.py` - Add to `write_env_file()`
2. Edit `templates/index.html` - Add form field
3. Restart server

---

## 📚 Files

- **`web_interface.py`** - Flask application
- **`templates/index.html`** - Web interface HTML
- **`start-web.sh`** - Quick start script
- **`requirements-web.txt`** - Python dependencies
- **`WEB_INTERFACE_GUIDE.md`** - Detailed documentation

---

## 🔐 Security Tips

1. **Change default port** if exposing to internet
2. **Add authentication** for public access
3. **Use HTTPS** with Let's Encrypt
4. **Keep Flask updated** for security patches
5. **Restrict firewall** to trusted IPs only

---

## 🎉 Benefits

### Before (Manual Configuration)
```bash
ssh pi@raspberrypi.local
nano env.sh
# Edit file manually
# Save and exit
source env.sh
./run.sh
```

### After (Web Interface)
1. Open browser
2. Change settings
3. Click "Save"
4. Click "Update Display"
5. Done! ✨

---

## 🆘 Support

Need help?

1. Check **WEB_INTERFACE_GUIDE.md** for detailed docs
2. View logs in the web interface
3. Test `./run.sh` manually
4. Check GitHub issues

---

## 🚀 Future Enhancements

- [ ] Dark mode
- [ ] Multiple profiles
- [ ] Scheduled updates UI
- [ ] Task preview
- [ ] Weather forecast graph
- [ ] Mobile app
- [ ] Email notifications
- [ ] Backup/restore

---

## 📄 License

Same as the main project - see LICENSE file

---

## 🙏 Credits

Built on top of the excellent [waveshare-epaper-display](https://github.com/mendhak/waveshare-epaper-display) project by mendhak.

---

**Made with ❤️ for the Raspberry Pi community**

**Version:** 1.0  
**Status:** Production Ready  
**Last Updated:** November 10, 2025
