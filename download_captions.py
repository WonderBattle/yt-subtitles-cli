#!/usr/bin/env python3
"""
Download auto-generated captions from a YouTube video using yt-dlp.
"""

import yt_dlp
import sys
import re
from pathlib import Path


def vtt_to_txt(vtt_file_path):
    """
    Convert VTT subtitle file to plain text format.
    
    Args:
        vtt_file_path: Path to the VTT file
        
    Returns:
        Path to the generated TXT file
    """
    try:
        import re
        with open(vtt_file_path, 'r', encoding='utf-8') as f:
            vtt_content = f.read()
        
        # Remove VTT headers and timing information
        lines = vtt_content.split('\n')
        txt_lines = []
        skip_next = False
        
        for line in lines:
            # Skip empty lines, WEBVTT header, and metadata
            if not line.strip() or line.startswith('WEBVTT') or \
               line.startswith('Kind:') or line.startswith('Language:') or \
               line.startswith('NOTE'):
                continue
            
            # Skip timing lines (contain -->)
            if '-->' in line:
                skip_next = False
                continue
            
            # Clean up the line
            clean_line = line.strip()
            
            # Remove cue settings (align, position, etc.) that might be on same line
            if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}', clean_line):
                continue
            
            # Remove timestamps and formatting tags
            clean_line = re.sub(r'<c[^>]*>', '', clean_line)
            clean_line = re.sub(r'</c>', '', clean_line)
            clean_line = re.sub(r'<v[^>]*>', '', clean_line)
            clean_line = re.sub(r'</v>', '', clean_line)
            clean_line = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', clean_line)
            clean_line = re.sub(r'\[.*?\]', '', clean_line).strip()
            
            # Add the cleaned subtitle text
            if clean_line and not re.match(r'[\d:\.>]+', clean_line):
                txt_lines.append(clean_line)
        
        # Write to TXT file
        txt_file_path = vtt_file_path.with_suffix('.txt')
        with open(txt_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(txt_lines))
        
        return txt_file_path
    except Exception as e:
        print(f"✗ Error converting VTT to TXT: {e}", file=sys.stderr)
        return None


def download_captions(youtube_url, output_path="captions", language="es"):
    """
    Download auto-generated captions from a YouTube video.
    
    Args:
        youtube_url: The URL of the YouTube video
        output_path: Directory to save the caption files
        language: Language code for captions (default: 'es' for Spanish)
    """
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # Configure yt-dlp options
    ydl_opts = {
        'quiet': False,
        'no_warnings': False,
        'skip_download': True,       # Don't download the video file
        'skip_unavailable_fragments': True,
        'writesubtitles': True,      # Download subtitles
        'writeautomaticsub': True,   # Prioritize auto-generated subtitles
        'subtitleslangs': [language],  # Language code
        'subtitlesformat': 'vtt',    # Save as VTT format
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'socket_timeout': 30,
        'noplaylist': True,          # Download only the video, not playlist
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading captions from: {youtube_url}")
            info = ydl.extract_info(youtube_url, download=True)
            video_title = info.get('title', 'Unknown')
            print(f"✓ Successfully downloaded captions for: {video_title}")
            
            # Convert VTT to TXT
            vtt_file = Path(output_path) / f"{video_title}.{language}.vtt"
            if vtt_file.exists():
                txt_file = vtt_to_txt(vtt_file)
                if txt_file:
                    print(f"✓ Converted to TXT format")
                    print(f"✓ Saved files:")
                    print(f"  - {vtt_file.name}")
                    print(f"  - {txt_file.name}")
            else:
                print(f"✓ Saved to: {output_path}/")
            
            return True
    except Exception as e:
        print(f"✗ Error downloading captions: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_captions.py <youtube_url> [output_path] [language_code]")
        print("Example: python download_captions.py https://youtu.be/HFIwMQkDR4I captions es")
        print("Language codes: es=Spanish, en=English, fr=French, etc.")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "captions"
    language = sys.argv[3] if len(sys.argv) > 3 else "es"
    
    success = download_captions(youtube_url, output_path, language)
    sys.exit(0 if success else 1)
