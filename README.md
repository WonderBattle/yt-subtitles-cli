# YouTube Subtitles CLI

A minimal Python script to download auto-generated captions from YouTube videos using yt-dlp.

## Installation

1. Clone or navigate to this directory
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python download_captions.py <youtube_url>
```

### With Custom Output Directory

```bash
python download_captions.py <youtube_url> <output_directory>
```

## Examples

Download captions from the video and save to default `captions/` directory:

```bash
python download_captions.py "https://youtu.be/HFIwMQkDR4I?list=RDHFIwMQkDR4I"
```

Download captions and save to a custom directory:

```bash
python download_captions.py "https://youtu.be/HFIwMQkDR4I?list=RDHFIwMQkDR4I" "./my_captions"
```

## Output

The script downloads auto-generated captions in VTT format. Files are saved with the video title as the filename.

## Features

- Downloads only auto-generated captions (not user-provided ones)
- Saves captions in VTT format (WebVTT)
- Creates output directory automatically
- Provides clear success/error messages
- Simple and minimal implementation

## Requirements

- Python 3.6+
- yt-dlp library
# yt-subtitles-cli
