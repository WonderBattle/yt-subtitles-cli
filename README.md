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

### (No DevContainer)

This project no longer includes DevContainer/Codespaces configuration. Use a local virtual environment (recommended) to run the app.

## Usage

### Option 1: CLI Mode (Command Line)

The most straightforward way to download captions:

```bash
python download_captions.py <youtube_url> [output_path] [language_code]
```

### CLI only (no web UI)

This repository is trimmed to the minimal CLI tool. Use `download_captions.py` to download captions from the command line — no web server is required.

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

Only the CLI usage is supported in this trimmed repo; start with the CLI examples above.

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

<!-- Troubleshooting moved out; keep things minimal for local venv usage -->
