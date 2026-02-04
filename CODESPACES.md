# GitHub Codespaces Configuration

This project is configured for GitHub Codespaces with automatic deployment.

## Quick Start in Codespaces

1. **Open in Codespaces:**
   - Click "Code" > "Codespaces" > "Create codespace on main"

2. **Wait for setup:**
   - The devcontainer will automatically install all dependencies
   - This takes about 1-2 minutes

3. **Start the web interface:**
   - Open the terminal and run: `python app.py`
   - Click the notification "Open in Browser" when it appears

4. **Access the application:**
   - A new window will open with the YouTube Subtitles web interface
   - Enter a YouTube URL and select a language
   - Download the captions!

## Available Commands

### Web Interface (Recommended)
```bash
python app.py
```
- Opens on `http://localhost:8000`
- Provides a user-friendly interface
- No technical knowledge required

### CLI Mode
```bash
python download_captions.py <youtube_url> [language]
```
Example:
```bash
python download_captions.py "https://youtu.be/..." es
```

### API Documentation
When the app is running, visit:
- `http://localhost:8000/docs` - Interactive Swagger UI
- `http://localhost:8000/redoc` - ReDoc documentation

## Troubleshooting

### Port already in use
If port 8000 is already in use, specify a different port:
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8001
```

### Dependencies not installing
If dependencies don't install automatically, run:
```bash
pip install -r requirements.txt
```

### Files not appearing
Downloaded captions are saved in the `captions/` directory within the Codespace.
They will be available in the current session but will be cleared when the Codespace is deleted.

## Environment Details

- **Image:** Python 3.11
- **Port:** 8000 (forwarded)
- **Framework:** FastAPI + Uvicorn
- **Auto-forwarding:** Enabled with notifications

## Extensions Pre-installed

- Python & Pylance (IntelliSense, debugging)
- GitHub Copilot & Copilot Chat
- GitHub Theme
- Ruff (Python linting)
- Remote Explorer
