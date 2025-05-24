import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime
import urllib.parse
import re

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def hello_world():
    return "YouTube Transcript Summarizer API is working!"

@app.route('/time', methods=['GET'])
def get_time():
    x = datetime.now()
    return str(x)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

def get_transcript(video_id):
    """Get transcript from YouTube video"""
    try:
        # Try to get transcript in different languages
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US', 'auto'])
        transcript_text = ' '.join([item['text'] for item in transcript_list])
        return transcript_text
    except Exception as e:
        print(f"Error getting transcript for {video_id}: {e}")
        # Try getting available transcripts
        try:
            available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
            print(f"Available transcripts: {[t.language_code for t in available_transcripts]}")
            # Get the first available transcript
            transcript = next(iter(available_transcripts))
            transcript_list = transcript.fetch()
            transcript_text = ' '.join([item['text'] for item in transcript_list])
            return transcript_text
        except Exception as e2:
            print(f"Failed to get any transcript: {e2}")
            return None

def simple_summarize(text, max_sentences=5):
    """Simple extractive summarization"""
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    if len(sentences) <= max_sentences:
        return text
    
    # Score sentences based on word frequency
    word_freq = {}
    words = re.findall(r'\w+', text.lower())
    for word in words:
        if len(word) > 3:  # Skip short words
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Score sentences
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        words_in_sentence = re.findall(r'\w+', sentence.lower())
        score = sum(word_freq.get(word, 0) for word in words_in_sentence)
        sentence_scores[i] = score / len(words_in_sentence) if words_in_sentence else 0
    
    # Get top sentences
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:max_sentences]
    top_sentences = sorted(top_sentences, key=lambda x: x[0])  # Sort by original order
    
    summary = '. '.join([sentences[i] for i, score in top_sentences])
    return summary + '.'

@app.route('/summarize/api', methods=['GET'])
def get_summarize():
    try:
        # Get YouTube URL from query parameters
        youtube_url = request.args.get('youtube_url')
        full_transcript_flag = request.args.get('full_transcript', 'false').lower() == 'true'
        
        if not youtube_url:
            return jsonify({'error': 'youtube_url parameter is required'}), 400
        
        # Extract video ID from URL
        url_data = urllib.parse.urlparse(youtube_url)
        query = urllib.parse.parse_qs(url_data.query)
        
        if 'v' not in query:
            return jsonify({'error': 'Invalid YouTube URL - no video ID found'}), 400
        
        video_id = query['v'][0]
        print(f"Processing video ID: {video_id}")
        
        # Get transcript
        print(f"Attempting to get transcript for video: {video_id}")
        transcript = get_transcript(video_id)
        if not transcript:
            return jsonify({'error': 'Could not get transcript for this video. The video may not have captions/subtitles available, or there might be a temporary issue. Please try again.'}), 400
        
        print(f"Successfully got transcript. Length: {len(transcript)} characters")
        
        if full_transcript_flag:
            print("Returning full transcript as requested.")
            response_text = transcript
        else:
            print("Generating summary...")
            response_text = simple_summarize(transcript)
            print(f"Summary generated. Length: {len(response_text)} characters")
        
        return jsonify({
            'responseText': response_text,
            'video_id': video_id,
            'transcript_length': len(transcript)
        }), 200
        
    except Exception as e:
        print(f"Error in get_summarize: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting YouTube Transcript Summarizer...")
    print("Server will be available at: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)