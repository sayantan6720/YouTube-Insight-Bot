import os
import argparse
from youtube_transcript_api import YouTubeTranscriptApi, _errors

def extract_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    if "youtu.be" in youtube_url:
        return youtube_url.split("/")[-1].split("?")[0]
    elif "youtube.com/watch" in youtube_url:
        import urllib.parse as urlparse
        parsed_url = urlparse.urlparse(youtube_url)
        return urlparse.parse_qs(parsed_url.query)['v'][0]
    else:
        # If the input is just the ID
        return youtube_url

def get_transcript(video_id, languages=['en']):
    """Get transcript for a YouTube video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        return transcript
    except _errors.NoTranscriptFound:
        print(f"No transcript found for video {video_id} in the specified languages.")
        return None
    except _errors.TranscriptsDisabled:
        print(f"Transcripts are disabled for video {video_id}.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def format_transcript(transcript, format_type='text'):
    """Format the transcript in the specified format."""
    if not transcript:
        return ""
    
    if format_type == 'text':
        return '\n'.join([item['text'] for item in transcript])
    elif format_type == 'srt':
        srt_content = ""
        for i, item in enumerate(transcript, 1):
            start_seconds = item['start']
            duration = item.get('duration', 0)
            end_seconds = start_seconds + duration
            
            start_time = format_time(start_seconds)
            end_time = format_time(end_seconds)
            
            srt_content += f"{i}\n{start_time} --> {end_time}\n{item['text']}\n\n"
        return srt_content
    elif format_type == 'json':
        import json
        return json.dumps(transcript, indent=2)
    else:
        return '\n'.join([item['text'] for item in transcript])

def format_time(seconds):
    """Format seconds into SRT time format: HH:MM:SS,mmm"""
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

def save_transcript(content, output_file):
    """Save the transcript content to the specified file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Transcript saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving transcript: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Download YouTube video transcripts')
    parser.add_argument('url', help='YouTube video URL or ID')
    parser.add_argument('-l', '--language', nargs='+', default=['en'], 
                        help='Transcript language code(s) (default: en)')
    parser.add_argument('-f', '--format', choices=['text', 'srt', 'json'], default='text',
                        help='Output format (default: text)')
    parser.add_argument('-o', '--output', help='Output file (default: transcript.txt/srt/json)')
    
    args = parser.parse_args()
    
    # Extract video ID
    video_id = extract_video_id(args.url)
    print(f"Extracting transcript for video ID: {video_id}")
    
    # Get transcript
    transcript = get_transcript(video_id, args.language)
    
    if transcript:
        # Format transcript
        content = format_transcript(transcript, args.format)
        
        # Determine output file
        if args.output:
            output_file = args.output
        else:
            extension = args.format if args.format != 'text' else 'txt'
            output_file = f"transcript.{extension}"
        
        # Save transcript
        save_transcript(content, output_file)

if __name__ == "__main__":
    main()