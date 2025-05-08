# RAG Chatbot with YouTube Transcript Integration

This project integrates a **Retrieval-Augmented Generation (RAG) Chatbot** with a **YouTube Video Transcript Downloader**. The YouTube Transcript Downloader script allows you to fetch and save transcripts for YouTube videos in various formats (text, SRT, or JSON), while the RAG Chatbot leverages document-based knowledge to engage in conversational AI.

## YouTube Transcript Downloader

The **YouTube Transcript Downloader** allows you to download transcripts for YouTube videos. This script supports various formats such as text, SRT, and JSON, and allows you to choose the transcript's language(s).

### Key Features:
- Extract transcripts from YouTube videos by URL or video ID.
- Support for multiple languages.
- Export the transcript in different formats: `text`, `SRT`, or `JSON`.
- Save transcripts locally to a file.

### Requirements:
- Python 3.x
- youtube-transcript-api

### Installation:
To install the required dependencies, run the following command:

```bash
pip install youtube-transcript-api
