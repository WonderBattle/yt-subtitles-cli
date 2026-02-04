# YouTube Subtitles CLI

A minimal Python script to download auto-generated captions from YouTube videos using yt-dlp.

## Installation

### Option 1: Using `uv` (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install `uv` (if you don't have it):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Navigate to the project directory and create a virtual environment:
```bash
uv venv
```

3. Activate the virtual environment:
```bash
# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

4. Install dependencies:
```bash
uv pip install -r requirements.txt
```

### Option 2: Using Python `venv`

```bash
python -m venv .venv

# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

### Option 3: Using DevContainer (Docker)

For a containerized environment, use the included `.devcontainer` setup.

**Prerequisites:** Docker and VS Code with the "Dev Containers" extension.

1. Open the project in VS Code
2. Click "Reopen in Container" when prompted, or use the command palette:
```
Dev Containers: Reopen in Container
```

The development environment will be automatically set up with all dependencies installed.

## Usage

### Option 1: CLI Mode (Command Line)

The most straightforward way to download captions:

```bash
python download_captions.py <youtube_url> [output_path] [language_code]
```

### Option 2: Web Interface (FastAPI + Uvicorn)

Launch the web-based interface for easier use:

```bash
python app.py
```

Then open your browser to `http://localhost:8000`

**Features:**
- User-friendly web interface
- No command-line knowledge required
- REST API for programmatic access
- Interactive API documentation at `/docs`

### Option 3: GitHub Codespaces (Cloud-based)

1. Open the project in GitHub Codespaces
2. The devcontainer will automatically configure and install dependencies
3. Run: `python app.py`
4. Click the notification to open the forwarded port
5. Access the web interface in your browser

### Basic CLI Usage

Downloads captions in Spanish (default) and saves to `captions/` directory:

```bash
python download_captions.py <youtube_url>
```

### With Custom Output Directory

```bash
python download_captions.py <youtube_url> <output_directory>
```

### With Custom Language

Specify a language code (ISO 639-1 format):

```bash
python download_captions.py <youtube_url> <output_directory> <language_code>
```

## REST API

When running with `python app.py`, the following endpoints are available:

### Web Interface
- **GET** `/` - Main web interface

### API Endpoints
- **POST** `/api/download` - Download captions
  ```json
  {
    "youtube_url": "https://youtu.be/...",
    "language": "es",
    "output_path": "captions"
  }
  ```

- **GET** `/api/status` - Get API status
- **GET** `/api/health` - Health check
- **GET** `/docs` - Interactive API documentation (Swagger UI)
- **GET** `/redoc` - ReDoc API documentation

## Examples

### CLI Examples

Download Spanish captions and save to default `captions/` directory:

```bash
python download_captions.py "https://youtu.be/eAMwDYz6PUE"
```

Download English captions:

```bash
python download_captions.py "https://youtu.be/eAMwDYz6PUE" captions en
```

Download to a custom directory:

```bash
python download_captions.py "https://youtu.be/eAMwDYz6PUE" ./my_captions es
```

Download French captions:

```bash
python download_captions.py "https://youtu.be/eAMwDYz6PUE" ./french_subs fr
```

### Web Interface Examples

1. **Start the server:**
```bash
python app.py
```

2. **Open in browser:**
```
http://localhost:8000
```

3. **Fill in the form:**
   - Enter YouTube URL
   - Select language
   - Click "Download Captions"

### API Examples

Using `curl`:

```bash
curl -X POST "http://localhost:8000/api/download" \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_url": "https://youtu.be/eAMwDYz6PUE",
    "language": "es",
    "output_path": "captions"
  }'
```

Using Python:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/download",
    json={
        "youtube_url": "https://youtu.be/eAMwDYz6PUE",
        "language": "es",
        "output_path": "captions"
    }
)

print(response.json())
```

## Output

The script downloads auto-generated captions in **both VTT and TXT formats**:
- **VTT format**: Standard WebVTT subtitle format with timing information
- **TXT format**: Plain text format with clean captions only (no timing data)

**No video files are downloaded**, only the captions.

Example files:
- `Kaotiko - Otra Noche.es.vtt` (12 KB)
- `Kaotiko - Otra Noche.es.txt` (3.3 KB)

## Features

- ✓ Downloads only auto-generated captions (not user-provided ones)
- ✓ Saves captions in **both VTT and TXT formats**
- ✓ **TXT format**: Clean plain text without timing information
- ✓ **VTT format**: Standard WebVTT with timestamps for media players
- ✓ Support for multiple languages (Spanish, English, French, etc.)
- ✓ Avoids downloading entire playlists (downloads single video only)
- ✓ **No video files downloaded** - captions only
- ✓ Creates output directory automatically
- ✓ Provides clear success/error messages
- ✓ Simple and minimal implementation
- ✓ Works with virtual environments (uv or venv)
- ✓ DevContainer support for isolated development environment

## Requirements

- Python 3.6+
- yt-dlp library
- Internet connection (for downloading from YouTube)

## Common Language Codes

| Language | Code |
|----------|------|
| Spanish  | `es` |
| English  | `en` |
| French   | `fr` |
| German   | `de` |
| Italian  | `it` |
| Portuguese | `pt` |
| Japanese | `ja` |
| Chinese  | `zh` |

For a complete list, see [ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).

## Troubleshooting

**Issue: HTTP Error 429 (Too Many Requests)**
- Wait a few moments and try again
- This is a rate limiting issue from YouTube

**Issue: No subtitles found**
- Not all videos have auto-generated captions
- Check if the video has captions available on YouTube first

**Issue: JavaScript runtime warning**
- This is a warning but doesn't affect caption downloading
- Install Node.js to suppress the warning: `apt-get install nodejs` (in containers)
