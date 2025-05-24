# YouTube Transcript Summarizer

A Chrome extension that generates summaries of YouTube video transcripts using a Flask backend API.

## Features

- 🎥 Extract transcripts from YouTube videos
- 📝 Generate concise summaries using extractive summarization
- 🚀 Fast and lightweight (no heavy AI models)
- 🔧 Easy to set up and customize
- 🌐 Works with any YouTube video that has captions/subtitles

## How It Works

1. Navigate to any YouTube video with captions
2. Click the extension icon
3. Click "Generate Summary"
4. Get a concise summary of the video content

## Installation

### Prerequisites
- Python 3.7+
- Chrome browser
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/youtube-transcript-summarizer.git
   cd youtube-transcript-summarizer
   ```

2. **Install Python dependencies**
   ```bash
   pip install flask flask-cors youtube-transcript-api
   ```

3. **Start the Flask server**
   ```bash
   python app.py
   ```
   The server will be available at `http://127.0.0.1:5000`

### Chrome Extension Setup

1. **Enable Developer Mode**
   - Open Chrome and go to `chrome://extensions/`
   - Toggle "Developer mode" in the top right

2. **Load the Extension**
   - Click "Load unpacked"
   - Select the project folder
   - The extension should appear in your extensions list

3. **Pin the Extension**
   - Click the extensions icon (puzzle piece) in Chrome toolbar
   - Pin the "YouTube Transcript Summarizer" extension

## Usage

1. **Start the Backend**: Make sure the Flask server is running (`python app.py`)
2. **Navigate to YouTube**: Go to any YouTube video with captions
3. **Click Extension**: Click the extension icon in your toolbar
4. **Generate Summary**: Click the "Generate Summary" button
5. **View Results**: The summary will appear in the popup

## File Structure

```
youtube-transcript-summarizer/
├── app.py                 # Flask backend API
├── manifest.json          # Chrome extension manifest
├── popup.html             # Extension popup interface
├── popup.js               # Extension popup logic
├── popup.css              # Extension popup styling
├── background.js          # Extension background script
├── contentScript.js       # Extension content script
├── requirements.txt       # Python dependencies
├── reqd.png              # Extension icon
└── README.md             # This file
```

## API Endpoints

- `GET /` - Health check
- `GET /time` - Current server time
- `GET /summarize/api?youtube_url=<URL>` - Generate summary for YouTube video

## Troubleshooting

### Common Issues

1. **"Could not get transcript"**
   - Make sure the video has captions/subtitles
   - Some videos may not have accessible transcripts

2. **"Make sure the Flask server is running"**
   - Check if `python app.py` is running
   - Verify server is accessible at `http://127.0.0.1:5000`

3. **Extension not working**
   - Reload the extension in `chrome://extensions/`
   - Check browser console for errors

### Server Logs
The Flask server provides detailed logs:
```bash
Processing video ID: x3SZvxoOmi0
Successfully got transcript. Length: 21012 characters
Generating summary...
Summary generated. Length: 487 characters
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Future Enhancements

- [ ] Add AI-powered summarization (T5, GPT models)
- [ ] Support for multiple languages
- [ ] Adjustable summary length
- [ ] Save summaries locally
- [ ] Export summaries to different formats
- [ ] Batch processing of multiple videos

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: Chrome Extension (HTML/CSS/JavaScript)
- **Transcript API**: youtube-transcript-api
- **Summarization**: Extractive (frequency-based sentence scoring)

## Acknowledgments

- Original inspiration from [neelam4/Youtube-Transcript-Summarizer](https://github.com/neelam4/Youtube-Transcript-Summarizer)
- YouTube Transcript API library
- Flask web framework