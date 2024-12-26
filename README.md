![Untitled](https://github.com/user-attachments/assets/ec7ca53c-42f5-483f-b7c0-8919fad33808)

# YouTube Multi-Threaded Downloader (YT-MTDL)

A modern, feature-rich desktop application for downloading pretty much any video stream, with multi-threading support and a user-friendly dark-themed interface.

## Features

- **Multi-threaded Downloads**: Optimize download speeds with configurable thread count

- **Batch Processing**: Import multiple URLs from a text file for bulk downloads

- **Format Selection**: Choose between automatically scanned quality options and formats

- **Quality Options**: Select from multiple standard resolution options
  - Best
  - High
  - Medium
  - Low

- **Additional Options**:
  - Subtitle downloads
  - Playlist support
  - Custom output directory
  - Download speed limiting
  - Proxy support

## Requirements

- Python 3.6+
- PyQt6
- yt-dlp
- Concurrent Futures (included in Python standard library)

## Installation

1. Ensure Python 3.6 or higher is installed on your system
2. Install required dependencies:
```bash
pip install PyQt6 yt-dlp
```

## Usage

***Please keep in mind that some m3u8 downloads will download seperate audio and video channels. It will merge them at the end of the download.***

***[Test Downloading Capabilities](https://github.com/lolitemaultes/m3u8-urls)***

### Basic Download
1. Launch the application
2. Enter a YouTube or other video URL in the input field
3. Select desired format and quality options
4. Choose output directory (defaults to Downloads folder)
5. Click "Download" to start

### Batch Downloads
1. Create a text file with stream URLs (one per line)
2. Optional: Add episode identifiers before URLs (e.g., "EP01 https://youtube.com/...")
3. Click "Import URLs" and select your text file
4. Configure download options
5. Click "Download" to process all URLs sequentially

### Settings Configuration
1. Navigate to the "Settings" tab
2. Adjust download threads (1-32)
3. Set speed limits if needed
4. Configure proxy settings if required
5. Click "Save Settings" to persist your preferences

## Advanced Features

### Download Settings
- **Thread Count**: Higher values may improve download speed (default: 16)
- **Speed Limit**: Optional bandwidth throttling in KB/s
- **Proxy Support**: Configure proxy settings for network requirements

### Error Handling
- Built-in error logging system
- View logs through Tools > View Error Log
- Save logs for troubleshooting

### File Management
- Custom naming templates
- Automatic file organization
- Support for playlist downloads

## Interface Features

- Modern dark theme interface
- Progress tracking with detailed status updates
- Download speed and ETA display
- Resizable window with responsive design
- Persistent settings across sessions

## Technical Details

The application is built using:
- PyQt6 for the graphical interface
- yt-dlp for video downloading capabilities
- Python's concurrent.futures for multi-threading
- JSON for settings persistence
- Custom dark theme styling with QSS

## Notes

- Download speeds may vary based on:
  - YouTube's server response
  - Your internet connection
  - Selected thread count
  - System resources
- Some videos may have restrictions that prevent downloading
- Respect YouTube's terms of service and content creators' rights

## Troubleshooting

If you encounter issues:
1. Check your internet connection
2. Verify the YouTube URL is accessible
3. Review the error log (Tools > View Error Log)
4. Ensure you have adequate disk space
5. Try reducing thread count if downloads are unstable

## Settings Storage

The application stores settings in:
- `.ytdl_settings.json` for application preferences
- `.ytdl_errors.log` for error logging

Both files are stored in the user's home directory.

## License

This software is provided as-is, check the source code for licensing information.
