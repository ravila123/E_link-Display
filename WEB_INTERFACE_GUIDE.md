# 🌐 Web Interface Guide

## Overview

The web interface provides a user-friendly dashboard to configure and manage your e-paper display without editing configuration files manually.

![Web Interface](screenshots/web-interface.png)

---

## ✨ Features

### 📋 Configuration Management
- **Todoist Integration** - Add/update your API token
- **Weather Settings** - Configure location and provider
- **Display Options** - Choose layout and version
- **Advanced Settings** - Cache duration, logging level

### 🎮 Quick Actions
- **Update Display Now** - Trigger immediate refresh
- **Clear Cache** - Force fresh data fetch
- **View Logs** - See recent activity and errors

### 📊 Status Dashboard
- Last update timestamp
- Cache file status
- Log file size
- Real-time system information

---

## 🚀 Installation

### Step 1: Install Flask

On your Raspberry Pi:

```bash
cd ~/waveshare-epaper-display

# Install web interface dependencies
.venv/bin/pip3 install -r requirements-web.txt
```

### Step 2: Start the Web Server

```bash
# Start the web interface
.venv/bin/python3 web_interface.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Running on http://192.168.1.100:5000
```

### Step 3: Access the Interface

Open a web browser and go to:
- **From the Pi:** http://localhost:5000
- **From another device:** http://raspberrypi.local:5000
- **Or use IP:** http://192.168.1.100:5000 (replace with your Pi's IP)

---

## 📖 Using the Interface

### 1. Configure Todoist

1. Go to https://todoist.com/prefs/integrations
2. Copy your API token
3. Paste it in the "Todoist API Token" field
4. Click "Save Configuration"

### 2. Configure Weather

**Option A: Met.no (Free, No API Key)**
1. Enter your email in "Met.no Email"
2. Enter your latitude and longitude
3. Choose temperature format (Celsius/Fahrenheit)
4. Click "Save Configuration"

**Option B: Other Providers**
- OpenWeatherMap, VisualCrossing, etc.
- Add fields in the form as needed

### 3. Configure Display

1. Select your Waveshare version (1, 2, or 2B)
2. Choose a screen layout (1-5)
3. Adjust cache duration if needed
4. Click "Save Configuration"

### 4. Update Display

Click "🔄 Update Display Now" to:
- Fetch fresh weather data
- Fetch fresh Todoist tasks
- Generate new display image
- Update the e-paper screen

### 5. View Logs

Click "📄 View Logs" to see:
- Recent activity
- Error messages
- Debug information

---

## 🔧 Advanced Usage

### Run as Background Service

Create a systemd service to run the web interface automatically:

```bash
sudo nano /etc/systemd/system/epaper-web.service
```

Add:
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
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable epaper-web
sudo systemctl start epaper-web
sudo systemctl status epaper-web
```

### Access from Anywhere

**Option 1: Port Forwarding**
- Forward port 5000 on your router to your Pi
- Access via your public IP

**Option 2: Tailscale/ZeroTier**
- Install a VPN solution
- Access securely from anywhere

**Option 3: Reverse Proxy (Nginx)**
```bash
sudo apt install nginx

sudo nano /etc/nginx/sites-available/epaper
```

Add:
```nginx
server {
    listen 80;
    server_name epaper.local;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/epaper /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

## 🔒 Security Considerations

### 1. Change Default Port

Edit `web_interface.py`:
```python
app.run(host='0.0.0.0', port=8080, debug=False)  # Change port
```

### 2. Add Authentication

Install Flask-Login:
```bash
.venv/bin/pip3 install Flask-Login
```

Add basic auth to `web_interface.py`:
```python
from flask import request
from functools import wraps

def check_auth(username, password):
    return username == 'admin' and password == 'your_password'

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return ('Unauthorized', 401, {
                'WWW-Authenticate': 'Basic realm="Login Required"'
            })
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
    # ... rest of code
```

### 3. Use HTTPS

Install certbot:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d epaper.yourdomain.com
```

### 4. Firewall Rules

```bash
sudo ufw allow 5000/tcp
sudo ufw enable
```

---

## 🎨 Customization

### Change Theme Colors

Edit `templates/index.html`, find the CSS section:

```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Change to your preferred gradient */
}

.btn-primary {
    background: #667eea;  /* Change button color */
}
```

### Add More Configuration Options

Edit `web_interface.py`:

1. Add field to `write_env_file()`:
```python
if config.get('NEW_OPTION'):
    f.write('export NEW_OPTION="{}"\n'.format(config.get('NEW_OPTION', '')))
```

2. Add HTML input in `templates/index.html`:
```html
<div class="form-group">
    <label for="NEW_OPTION">New Option</label>
    <input type="text" id="NEW_OPTION" name="NEW_OPTION" 
           value="{{ config.get('NEW_OPTION', '') }}">
</div>
```

---

## 🐛 Troubleshooting

### Web Interface Won't Start

**Check if port is in use:**
```bash
sudo lsof -i :5000
```

**Kill existing process:**
```bash
sudo kill -9 <PID>
```

**Check logs:**
```bash
.venv/bin/python3 web_interface.py
# Look for error messages
```

### Can't Access from Other Devices

**Check firewall:**
```bash
sudo ufw status
sudo ufw allow 5000/tcp
```

**Check Pi's IP:**
```bash
hostname -I
```

**Ping from other device:**
```bash
ping raspberrypi.local
```

### Configuration Not Saving

**Check file permissions:**
```bash
ls -la env.sh
chmod 644 env.sh
```

**Check disk space:**
```bash
df -h
```

### Display Not Updating

**Check run.sh permissions:**
```bash
chmod +x run.sh
```

**Test manually:**
```bash
./run.sh
```

**Check logs:**
```bash
tail -f run.log
```

---

## 📱 Mobile Responsive

The interface is fully responsive and works great on:
- 📱 Smartphones
- 📱 Tablets
- 💻 Laptops
- 🖥️ Desktops

---

## 🔄 API Endpoints

For advanced users, you can interact with the API directly:

### Save Configuration
```bash
curl -X POST http://raspberrypi.local:5000/save \
  -d "TODOIST_API_TOKEN=your_token" \
  -d "WEATHER_LATITUDE=51.5077"
```

### Update Display
```bash
curl -X POST http://raspberrypi.local:5000/update
```

### Clear Cache
```bash
curl -X POST http://raspberrypi.local:5000/clear-cache
```

### View Logs
```bash
curl http://raspberrypi.local:5000/logs
```

---

## 🎯 Best Practices

1. **Backup env.sh** before making changes
2. **Test configuration** with "Update Display Now" before automating
3. **Monitor logs** regularly for errors
4. **Keep Flask updated** for security patches
5. **Use HTTPS** if exposing to internet
6. **Set strong passwords** if adding authentication

---

## 🆘 Support

If you encounter issues:

1. Check the logs in the web interface
2. Review `run.log` file
3. Test `./run.sh` manually
4. Check GitHub issues
5. Verify all dependencies are installed

---

## 🎉 Features Coming Soon

- [ ] Dark mode toggle
- [ ] Multiple display profiles
- [ ] Scheduled updates configuration
- [ ] Weather provider auto-detection
- [ ] Task preview before updating
- [ ] Mobile app
- [ ] Email notifications
- [ ] Backup/restore configuration

---

**Created:** November 10, 2025  
**Version:** 1.0  
**Status:** Production Ready
