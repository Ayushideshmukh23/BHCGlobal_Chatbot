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

# PowerConnect.AI fallback keywords
powerconnect_keywords = {
    "pcai", "powerconnect", "powerconnectai", "powerconnect.ai", "powerconnectai.com"
}

def is_powerconnect_query(user_input):
    user_input_lower = user_input.lower().replace(" ", "")
    return any(keyword in user_input_lower for keyword in powerconnect_keywords)

def clean_response(text):
    remove_phrases = [
        "According to the information provided,",
        "The passage states:",
        "The passage states that",
        "Based on the information provided,",
        "The text provided does not mention or define this term."
    ]
    for phrase in remove_phrases:
        text = text.replace(phrase, "")
    return text.strip(' "')

# Load scraped data
def load_data(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

# Convert data to LangChain documents
def convert_to_documents(data):
    documents = []
    for entry in data:
        content = entry.get("content", "")
        metadata = {key: value for key, value in entry.items() if key != "content"}
        documents.append(Document(page_content=content, metadata=metadata))
    return documents

# Store documents in vector DB
def store_in_vector_db(documents):
    embeddings = BedrockEmbeddings(
        region_name=os.getenv("AWS_DEFAULT_REGION"),
        model_id="amazon.titan-embed-text-v1"
    )
    vector_db = FAISS.from_documents(documents, embeddings)
    return vector_db

# Setup Claude 3.5 with vector retriever
def setup_qa_chain(vector_db):
    retriever = vector_db.as_retriever()
    llm = BedrockChat(
        region_name=os.getenv("AWS_DEFAULT_REGION"),
        model_id=os.getenv("BEDROCK_MODEL_ID"),
    )
    qa_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)
    return qa_chain

# Init data
json_file_path = "bhc_cleaned_data.json"
data = load_data(json_file_path)
documents = convert_to_documents(data)
vector_db = store_in_vector_db(documents)
qa_chain = setup_qa_chain(vector_db)

# Main question handler
def ask_bot(query):
    global chat_history

    # 🔁 PCAI fallback
    if is_powerconnect_query(query):
        fallback_answer = (
            "PowerConnect.AI (PCAI) is a digital assistant platform focused on customer service "
            "for utilities and other industries. Learn more at [powerconnect.ai](https://www.powerconnect.ai)."
        )
        chat_history.append((query, fallback_answer))
        return fallback_answer

    result = qa_chain({"question": query, "chat_history": chat_history})
    cleaned_answer = clean_response(result["answer"])
    chat_history.append((query, cleaned_answer))
    return cleaned_answer

# Optional: Run from CLI
if __name__ == "__main__":
    print("💬 BHC Global Chatbot (Claude 3.5 via Bedrock) is ready. Type 'exit' to quit.")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        answer = ask_bot(query)
        print("Bot:", answer)