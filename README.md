# RAG Chatbot with YouTube Transcript Support

This project combines a Retrieval-Augmented Generation (RAG) chatbot with YouTube transcript extraction capabilities, creating a versatile tool for interacting with both text documents and YouTube content.

## Features

- **Document-based RAG Chatbot**: Ask questions about loaded text documents with AI-powered conversational responses
- **YouTube Transcript Extraction**: Download and format transcripts from YouTube videos
- **Multiple Output Formats**: Export YouTube transcripts as plain text, SRT, or JSON
- **Enhanced Retrieval**: Vector-based search with Cohere reranking for improved results
- **Conversational Memory**: Maintains context throughout chat sessions

## Components

The project consists of two main Python scripts:

1. **RAG_chatbot.py**: Implements a Retrieval-Augmented Generation system using LangChain and OpenAI
2. **youtube_transcript.py**: Downloads and processes YouTube video transcripts

## Requirements

- Python 3.8+
- OpenAI API key
- Cohere API key (optional, for reranking)
- Various Python packages (see Installation)

## Installation

1. Clone this repository:
   git clone https://github.com/yourusername/rag-chatbot.git
   cd rag-chatbot
2. Install the required packages:
pip install langchain langchain-openai langchain-community faiss-cpu python-dotenv cohere youtube-transcript-api

3. Create a `.env` file in the project root with your API keys:
OPENAI_API_KEY=your_openai_api_key
CO_API_KEY=your_cohere_api_key  # Optional

## Usage

### RAG Chatbot

The RAG chatbot loads text documents and answers questions based on their content:
python RAG_chatbot.py --file your_document.txt

Once running:
- Type your questions to get AI-powered responses
- Type 'exit' to quit the chatbot

### YouTube Transcript Extractor

Extract transcripts from YouTube videos:
python youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" [options]

Options:
- `-l`, `--language`: Specify language code(s) (default: 'en')
- `-f`, `--format`: Output format - 'text', 'srt', or 'json' (default: 'text')
- `-o`, `--output`: Output file path (default: 'transcript.txt/srt/json')

Examples:
Basic usage (saves as transcript.txt)
python youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
Save as SRT format with Spanish language
python youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" -l es -f srt
Save to custom file
python youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" -o my_transcript.txt

## Integrating YouTube Transcripts with the RAG Chatbot

To use YouTube transcripts with the RAG chatbot:

1. Extract a transcript:
python youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" -o video_transcript.txt

2. Load the transcript into the RAG chatbot:
python RAG_chatbot.py --file video_transcript.txt

3. Now you can ask questions about the YouTube video content!

## How It Works

### RAG Chatbot

1. Loads and splits text documents into chunks
2. Creates embeddings and stores them in a FAISS vector database
3. Retrieves relevant chunks using similarity search when users ask questions
4. Reranks results with Cohere (if API key is provided)
5. Sends context, question, and chat history to the LLM to generate responses
6. Maintains conversation history for context

### YouTube Transcript Extractor

1. Extracts video ID from YouTube URL
2. Downloads transcript using YouTube Transcript API
3. Formats transcript according to the requested output type
4. Saves the transcript to a file

## Extending the Project

- Add support for additional document types (PDF, DOCX, etc.)
- Implement streaming responses for the chatbot
- Add a web interface for easier interaction
- Include support for auto-translation of YouTube transcripts
- Expand to other video platforms beyond YouTube

## License

[MIT License](LICENSE)

## Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) for the RAG framework
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction
- [OpenAI](https://openai.com/) for the language model
- [Cohere](https://cohere.com/) for reranking capabilities
