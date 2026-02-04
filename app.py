#!/usr/bin/env python3
"""
FastAPI web interface for YouTube Subtitles CLI.
Provides a REST API for downloading captions from YouTube videos.
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from pathlib import Path
import json
from download_captions import download_captions

app = FastAPI(
    title="YouTube Subtitles CLI",
    description="Download auto-generated captions from YouTube videos",
    version="1.0.0"
)

# Create captions directory if it doesn't exist
Path("captions").mkdir(exist_ok=True)

# Status tracking for background tasks
download_status = {}


class DownloadRequest(BaseModel):
    """Request model for caption download"""
    youtube_url: str
    language: str = "es"
    output_path: str = "captions"


class DownloadResponse(BaseModel):
    """Response model for download requests"""
    message: str
    status: str
    task_id: str = None


@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serve the main web interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>YouTube Subtitles CLI</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 10px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
                max-width: 500px;
                width: 100%;
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
                text-align: center;
            }
            .subtitle {
                color: #666;
                text-align: center;
                margin-bottom: 30px;
                font-size: 14px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: 500;
            }
            input, select {
                width: 100%;
                padding: 10px 12px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                font-size: 14px;
                transition: border-color 0.3s;
            }
            input:focus, select:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            .status {
                margin-top: 20px;
                padding: 15px;
                border-radius: 5px;
                display: none;
            }
            .status.success {
                background: #e8f5e9;
                color: #2e7d32;
                border: 2px solid #4caf50;
                display: block;
            }
            .status.error {
                background: #ffebee;
                color: #c62828;
                border: 2px solid #f44336;
                display: block;
            }
            .status.loading {
                background: #e3f2fd;
                color: #1565c0;
                border: 2px solid #2196f3;
                display: block;
            }
            .spinner {
                display: inline-block;
                width: 16px;
                height: 16px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-right: 10px;
                vertical-align: middle;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .info {
                margin-top: 20px;
                padding: 15px;
                background: #f5f5f5;
                border-radius: 5px;
                font-size: 12px;
                color: #666;
            }
            a {
                color: #667eea;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📥 YouTube Subtitles</h1>
            <p class="subtitle">Download auto-generated captions</p>
            
            <form id="downloadForm">
                <div class="form-group">
                    <label for="url">YouTube URL:</label>
                    <input type="url" id="url" name="youtube_url" placeholder="https://youtu.be/..." required>
                </div>
                
                <div class="form-group">
                    <label for="language">Language:</label>
                    <select id="language" name="language">
                        <option value="es">Spanish (es)</option>
                        <option value="en">English (en)</option>
                        <option value="fr">French (fr)</option>
                        <option value="de">German (de)</option>
                        <option value="it">Italian (it)</option>
                        <option value="pt">Portuguese (pt)</option>
                        <option value="ja">Japanese (ja)</option>
                        <option value="zh">Chinese (zh)</option>
                    </select>
                </div>
                
                <button type="submit" id="submitBtn">Download Captions</button>
            </form>
            
            <div id="status" class="status"></div>
            
            <div class="info">
                <strong>ℹ️ Note:</strong> Captions are saved in both VTT and TXT formats.
                <br><br>
                <a href="/docs">API Documentation</a>
            </div>
        </div>
        
        <script>
            const form = document.getElementById('downloadForm');
            const statusDiv = document.getElementById('status');
            const submitBtn = document.getElementById('submitBtn');
            
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const url = document.getElementById('url').value;
                const language = document.getElementById('language').value;
                
                statusDiv.className = 'status loading';
                statusDiv.innerHTML = '<span class="spinner"></span>Downloading captions...';
                submitBtn.disabled = true;
                
                try {
                    const response = await fetch('/api/download', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            youtube_url: url,
                            language: language,
                            output_path: 'captions'
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        statusDiv.className = 'status success';
                        statusDiv.innerHTML = '✓ ' + data.message;
                        form.reset();
                    } else {
                        statusDiv.className = 'status error';
                        statusDiv.innerHTML = '✗ ' + (data.detail || data.message || 'Error downloading captions');
                    }
                } catch (error) {
                    statusDiv.className = 'status error';
                    statusDiv.innerHTML = '✗ Error: ' + error.message;
                } finally {
                    submitBtn.disabled = false;
                }
            });
        </script>
    </body>
    </html>
    """


@app.post("/api/download", response_model=DownloadResponse)
def download_captions_api(request: DownloadRequest):
    """Download captions from YouTube video"""
    try:
        success = download_captions(
            request.youtube_url,
            request.output_path,
            request.language
        )
        
        if success:
            return DownloadResponse(
                message=f"Successfully downloaded captions in {request.language}",
                status="success"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Failed to download captions. Check the URL and try again."
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )


@app.get("/api/status")
def get_status():
    """Get download status"""
    return {"status": "ready", "message": "API is running"}


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "YouTube Subtitles CLI"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
