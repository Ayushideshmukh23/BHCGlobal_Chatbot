#!/bin/bash

echo "🔧 Starting BHC Chatbot Setup & Launch..."

# Step 1: Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "📁 Creating virtual environment..."
  python3 -m venv venv
fi

# Step 2: Activate virtual environment
echo "💻 Activating virtual environment..."
source venv/bin/activate

# Step 3: Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Step 4: Install required packages
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Extra checks for packages sometimes missing from requirements.txt
pip install faiss-cpu
pip install langchain-community

# Step 5: Run the Streamlit app
echo "🚀 Launching chatbot at http://localhost:8501 ..."
streamlit run app.py
