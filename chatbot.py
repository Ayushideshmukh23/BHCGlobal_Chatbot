import json
import os
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain.embeddings import BedrockEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import BedrockChat

# Load environment variables
load_dotenv()

# Global chat history
chat_history = []

# Load JSON file containing scraped website data
def load_data(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

# Convert each entry to LangChain Document
def convert_to_documents(data):
    documents = []
    for entry in data:
        content = entry.get("content", "")
        metadata = {key: value for key, value in entry.items() if key != "content"}
        documents.append(Document(page_content=content, metadata=metadata))
    return documents

# Store documents in a FAISS vector database
def store_in_vector_db(documents):
    embeddings = BedrockEmbeddings(
        region_name=os.getenv("AWS_DEFAULT_REGION"),
        model_id="amazon.titan-embed-text-v1"
    )
    vector_db = FAISS.from_documents(documents, embeddings)
    return vector_db

# Set up ConversationalRetrievalChain with Claude 3.5
def setup_qa_chain(vector_db):
    retriever = vector_db.as_retriever()
    llm = BedrockChat(
        region_name=os.getenv("AWS_DEFAULT_REGION"),
        model_id=os.getenv("BEDROCK_MODEL_ID"),  # e.g., "anthropic.claude-3-sonnet-20240229-v1:0"
    )
    qa_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)
    return qa_chain

# Initialize once and reuse
json_file_path = "bhc_cleaned_data.json"
data = load_data(json_file_path)
documents = convert_to_documents(data)
vector_db = store_in_vector_db(documents)
qa_chain = setup_qa_chain(vector_db)

# Public function to use in Streamlit or CLI
def ask_bot(query):
    global chat_history
    result = qa_chain({"question": query, "chat_history": chat_history})
    chat_history.append((query, result["answer"]))
    return result["answer"]

# Optional: run in CLI mode
if __name__ == "__main__":
    print("💬 BHC Global Chatbot (Claude 3.5 via Bedrock) is ready. Type 'exit' to quit.")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        answer = ask_bot(query)
        print("Bot:", answer)
