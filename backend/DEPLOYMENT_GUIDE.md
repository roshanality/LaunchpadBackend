# Deployment Guide: PythonAnywhere (ZIP Method)

This guide provides the steps to deploy the LaunchPad backend to PythonAnywhere while preserving your local database.

---

## 1. Prepare the ZIP Archive (Local)
Run this command in your PowerShell terminal to create a complete package (excluding git history and cache):
```powershell
Get-Item -Path * -Exclude ".git", "__pycache__" | Compress-Archive -DestinationPath project.zip -Update
```

---

## 2. Upload and Extract (PythonAnywhere Dashboard)
1. **Upload**: Go to the **Files** tab and upload `project.zip` to your home directory (`/home/kgplaunchpad/`).
2. **Extract**: Open a **Bash Console** and run:
   ```bash
   # Create project directory
   mkdir -p /home/kgplaunchpad/MainSiteBackend
   
   # IMPORTANT: Remove any misplaced files in your home directory
   rm -f /home/kgplaunchpad/app.py 
   rm -f /home/kgplaunchpad/launchpad.db
   
   # Move and unzip
   mv /home/kgplaunchpad/project.zip /home/kgplaunchpad/MainSiteBackend/
   cd /home/kgplaunchpad/MainSiteBackend
   unzip -o project.zip
   rm project.zip
   ```

---

## 3. Environment Setup (PythonAnywhere Bash Console)
Inside the console, install your dependencies using Python 3.12 specifically:
```bash
python3.12 -m pip install --user -r requirements.txt
```

---

## 4. Web App Setup (PythonAnywhere Web Tab)
1. **Add Web App**: Click "Add a new web app" -> **Manual Configuration** -> **Python 3.12**.
2. **Paths**:
   - Source code: `/home/kgplaunchpad/MainSiteBackend`
   - Working directory: `/home/kgplaunchpad/MainSiteBackend`
3. **Virtualenv**:
   - Leave this section **empty**.

---

## 5. WSGI Configuration (Critical)
Click the **WSGI configuration file** link in the Web tab and replace everything with:

```python
import sys
import os

path = '/home/kgplaunchpad/MainSiteBackend'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

# Import Flask app
from app import app as application

# Auto-initialize DB structure and admin user
from app import init_db, init_admin
with application.app_context():
    init_db()
    init_admin()
```

---

## 6. Static Files (Optional)
If you serve files from `uploads/`, add this mapping in the **Web** tab:
- **URL**: `/uploads`
- **Directory**: `/home/kgplaunchpad/MainSiteBackend/uploads`

---

## 7. Reload and Confirm
Click the green **Reload** button on the Web tab. Your site will be live at:
`https://kgplaunchpad.pythonanywhere.com/`

**Test the Health Check**: Visit `https://kgplaunchpad.pythonanywhere.com/` to confirm the app is active and the database is connected.

### 💡 Troubleshooting
* **Check Logs**: If it fails, check the **Error Log** at the bottom of the Web tab.
* **Database Check**: Once live, log in with your existing Admin credentials to confirm the DB was preserved.
