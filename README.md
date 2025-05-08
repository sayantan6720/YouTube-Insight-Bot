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
