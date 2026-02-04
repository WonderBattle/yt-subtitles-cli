# GitHub Codespaces Troubleshooting Guide

## Fixed Issues

### ✅ Container Creation Error (FIXED)
**Error:** `unable to find user codespace: no matching entries in passwd file`

**Cause:** The devcontainer specified a user that doesn't exist in the Python base image.

**Solution:** Removed the `remoteUser` setting to use the default user (root in Python container). Codespaces automatically manages the user context.

---

## Common Issues & Solutions

### Issue 1: Port Not Forwarding
**Symptoms:** 
- Port 8000 is not accessible
- "Cannot connect to localhost:8000"

**Solutions:**
1. Check if the app is running: `python app.py`
2. Wait for the notification "Open in Browser"
3. If port is occupied, use a different port:
   ```bash
   python -m uvicorn app:app --host 0.0.0.0 --port 8001
   ```

### Issue 2: Dependencies Not Installing
**Symptoms:**
- ModuleNotFoundError when running the app
- `No module named 'fastapi'`

**Solutions:**
1. Manually install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Upgrade pip:
   ```bash
   python -m pip install --upgrade pip
   ```
3. Check Python version:
   ```bash
   python --version
   ```

### Issue 3: Git Configuration Issues
**Symptoms:**
- Cannot push to GitHub
- "fatal: could not read config file"

**Solutions:**
1. Configure git:
   ```bash
   git config --global user.email "you@example.com"
   git config --global user.name "Your Name"
   ```
2. Authenticate with GitHub:
   ```bash
   gh auth login
   ```

### Issue 4: Captions Directory Permissions
**Symptoms:**
- "Permission denied" when saving captions
- Cannot write to `captions/` folder

**Solutions:**
1. Create the directory with proper permissions:
   ```bash
   mkdir -p captions
   chmod 755 captions
   ```
2. Or ensure the app is run from the correct directory:
   ```bash
   cd /workspaces/yt-subtitles-cli
   python app.py
   ```

---

## Codespaces Container Architecture

```
GitHub Codespaces
├── Container: Python 3.11
├── User: root (default)
├── Features:
│   ├── Git (latest from source)
│   └── GitHub CLI (v2.x)
├── Port Forward: 8000
└── Auto-installed Extensions:
    ├── Python
    ├── Pylance
    ├── GitHub Copilot
    └── Ruff Linter
```

---

## Quick Start Checklist

- [ ] Container created successfully
- [ ] No user/permission errors
- [ ] Dependencies installed (`pip list | grep fastapi`)
- [ ] App starts (`python app.py`)
- [ ] Port 8000 is accessible
- [ ] Web UI loads at `http://localhost:8000`
- [ ] API docs work at `http://localhost:8000/docs`

---

## Getting Help

If you encounter issues:

1. **Check the logs:**
   ```bash
   # View container details
   docker ps
   
   # View Python version
   python --version
   
   # Test imports
   python -c "import fastapi; print('✓ FastAPI installed')"
   ```

2. **Rebuild the container:**
   - Click "Codespaces" menu
   - Select "Rebuild container"
   - Wait for restart (2-3 minutes)

3. **Check GitHub Codespaces Status:**
   - Visit github.com/codespaces
   - View logs for your codespace
   - Check for any reported issues

---

## Performance Tips

- **Faster startup:** The container caches dependencies after first build
- **Reduce disk usage:** Run `rm -rf captions/*.mp4` to remove videos
- **Faster reinstalls:** `pip install --no-cache-dir` (saves space)

---

## Notes

- Captions are stored in the `captions/` folder within the container
- Files persist in the Codespace but are deleted when the Codespace is deleted
- Use GitHub Codespaces Settings to adjust container specs if needed
