import os
import sys
import argparse
import json
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import cohere

# Load environment variables
load_dotenv()

class SimpleRAGChatbot:
    def __init__(self):
        """Initialize the simple RAG chatbot without user context."""
        self.llm = None
        self.memory = None
        self.qa_chain = None
        self.vectorstore = None
        
        # Initialize components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all necessary components for the chatbot."""
        try:
            # Initialize OpenAI LLM
            self.llm = ChatOpenAI(temperature=0.7)
            
            # Create a conversation memory
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            # Create the conversation chain if vectorstore exists
            if os.path.exists("faiss_index") and os.listdir("faiss_index"):
                print("Loading existing vector store...")
                self.vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings(), 
                                                   allow_dangerous_deserialization=True)
                self._setup_qa_chain()
            
            print("Simple RAG Chatbot initialized successfully!")
        except Exception as e:
            print(f"Error initializing components: {e}")
            sys.exit(1)
    
    def _setup_qa_chain(self):
        """Set up the QA chain with the vector store."""
        if not self.vectorstore:
            print("Vector store not available. Please add a document first.")
            return
        
        # Simple prompt template
        qa_prompt = PromptTemplate.from_template("""
        You are a knowledgeable AI assistant that answers questions based on the provided documents.
        
        Guidelines for crafting your answer:
        - Use only the provided document context to answer; if context is insufficient, honestly say "I don't know" and offer general guidance.
        - Keep responses clear, conversational, and free of unnecessary jargon.
        - When explaining complex concepts, use examples or analogies.
        
        Document Context:
        {context}
        
        Conversation History:
        {chat_history}
        
        User Question:
        {question}
        
        Your Answer:
        """)
        
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 50}
        )
        
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": qa_prompt}
        )
    
    def load_document(self, filepath):
        """Load a document to be used for RAG."""
        try:
            print(f"Loading document from {filepath}...")
            
            # Load the document
            loader = TextLoader(filepath)
            documents = loader.load()
            
            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            texts = text_splitter.split_documents(documents)
            
            print(f"Split document into {len(texts)} chunks")
            
            # Create embeddings and vector store
            embeddings = OpenAIEmbeddings()
            self.vectorstore = FAISS.from_documents(texts, embeddings)
            
            # Save the vector store
            self.vectorstore.save_local("faiss_index")
            
            # Set up the QA chain
            self._setup_qa_chain()
            
            print(f"Successfully loaded and indexed document: {filepath}")
            return True
        except Exception as e:
            print(f"Error loading document: {e}")
            return False
    
    def rerank_results(self, query, results, k=15):
        """Use Cohere to rerank the search results."""
        try:
            if "CO_API_KEY" not in os.environ:
                print("Cohere API key not found. Skipping reranking.")
                return results[:k]
                
            co = cohere.ClientV2(os.getenv("CO_API_KEY"))
            
            # Extract text from documents for reranking
            docs_content = [doc.page_content for doc in results]
            
            # Rerank with Cohere
            response = co.rerank(
                model="rerank-v3.5",
                query=query,
                documents=docs_content,
                top_n=k
            )
            
            # Get reranked documents
            reranked_docs = []
            for item in response.results:
                original_index = item.index
                reranked_docs.append(results[original_index])
            
            return reranked_docs
        except Exception as e:
            print(f"Error in reranking: {e}")
            return results[:k]  # Fall back to regular results if reranking fails
    
    def chat(self, user_input):
        """Process user input and return a response."""
        if not self.vectorstore:
            return "I'm not ready yet. Please load a document first."
        
        try:
            # Get raw results from vector store
            raw_results = self.vectorstore.similarity_search(user_input, k=10)
            
            # Rerank results with Cohere
            reranked_docs = self.rerank_results(user_input, raw_results)
            
            # Extract context from reranked documents
            context = "\n\n".join([doc.page_content for doc in reranked_docs])
            
            # Get chat history
            chat_history = []
            if self.memory and hasattr(self.memory, "chat_memory"):
                chat_history = self.memory.chat_memory.messages
            
            # Format chat history for prompt
            formatted_history = ""
            if chat_history:
                for msg in chat_history:
                    if hasattr(msg, "type") and hasattr(msg, "content"):
                        role = "Human" if msg.type == "human" else "Assistant"
                        formatted_history += f"{role}: {msg.content}\n"
            
            # Create a custom prompt
            prompt = f"""
            Based on the following context and conversation history, please answer the user's question.
            Be conversational, helpful, and accurate. If the context doesn't contain relevant information,
            acknowledge this and try to provide general guidance.
            
            Context:
            {context}
            
            Conversation History:
            {formatted_history}
            
            User Question: {user_input}
            
            Answer:
            """
            
            # Get response from LLM
            response = self.llm.predict(prompt)
            
            # Update memory
            self.memory.save_context(
                {"input": user_input}, 
                {"output": response}
            )
            
            return response
        except Exception as e:
            print(f"Error in chat: {e}")
            return "I encountered an error processing your request. Please try again."

def main():
    """Main function to run the chatbot in interactive mode."""
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Simple RAG Chatbot with document loading')
    parser.add_argument('--file', '-f', type=str, required=True, 
                        help='Path to a text file to use as RAG data')
    
    args = parser.parse_args()
    
    # Validate the file path
    if not os.path.exists(args.file):
        print(f"Error: File {args.file} does not exist.")
        sys.exit(1)
    
    if not args.file.endswith('.txt'):
        print(f"Error: File {args.file} is not a .txt file. Please provide a valid text file.")
        sys.exit(1)
    
    # Initialize chatbot
    chatbot = SimpleRAGChatbot()
    
    # Load the document
    success = chatbot.load_document(args.file)
    if not success:
        print("Failed to load the document. Exiting...")
        sys.exit(1)
    
    print(f"Successfully loaded {args.file} for RAG")
    print("Simple RAG Chatbot is ready! Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        response = chatbot.chat(user_input)
        print(f"\nChatbot: {response}")

if __name__ == "__main__":
    main() 