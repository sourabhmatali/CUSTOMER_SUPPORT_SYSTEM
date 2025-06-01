
#  FLIPKART_ECOMMERCE_RAGCHATBOT

🤖 Customer Support System using RAG
A customer support chatbot powered by Retrieval-Augmented Generation (RAG) that leverages custom data and LLMs to deliver accurate, context-rich responses for product-related queries.

📋 Project Overview
This project implements an end-to-end RAG-based system for customer support. It includes data scraping, vector-based retrieval, and dynamic response generation using LLMs with customized prompts.
## Features

✨ Features
🔍 Natural language question handling

🔗 Retrieval-Augmented response generation

🧠 Custom prompt design for contextual accuracy

🔧 Configurable via YAML settings

🧹 Modular pipeline for scraping, embedding, and serving

## Tech Stack

🛠️ Tech Stack
Python: Core programming language

FastAPI: API framework (via main.py)

Transformers: LLM and embeddings

Pandas: Data manipulation

YAML: Configuration management

LangChain : Prompt chaining and agent tools

Conda/venv: Environment management

DataBase:AstraDB

Cloud:Amazon AWS,ECR


## Deployment


🚀 Setup & Installation
🔧 Prerequisites
Python 3.9+

Conda or virtual environment

API keys for LLM providers (e.g., Google AI Studio, Groq)


## Installation



🔨 Installation Steps
# Clone the repository
git clone https://github.com/yourusername/customer-support-system.git
cd customer-support-system

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

🔐 Environment Variables
Create a .env file and add:

GOOGLE_API_KEY=your_google_key,
GROQ_API_KEY=your_groq_key,
ATRA_DB_API_ENDPOINT=your_Astra_db_end_point_key,
ASTRA_DB_APPLICATION_TOKEN=Astra_db_application_token_key,
ASTRA_DB_KEYSPAC=Astra_db_keyspace_key,



## Running Tests

To run tests, run the following command

🏃‍♂️ Running the App
Start the API server using:
uvicorn main:app --reload --port 8001

Then open your browser and go to: http://localhost:8000/docs


## 🔄 Workflow
Scraping: Collect product reviews using the Flipkart dataset

Embedding: Convert documents to vector space

Retrieval: Fetch relevant chunks using vector similarity

Prompting: Use predefined prompt templates to generate answers

Response: Serve the response via API
## Contributing

Contributions are always welcome!

🤝 Contribution
Want to improve this project?

Fork the repo

Create a new branch (feature-x)

Make changes and commit

Open a Pull Request

## Screenshots
Link's:
https://drive.google.com/file/d/1qCb2wVDtdcqQ6_2XZLFkLanLS_U92C3y/view?usp=drive_link

https://drive.google.com/file/d/1toS119m_0gIZ5ZABmRvP4PJBrFLjjwA9/view?usp=drive_link
## Demo
Demo Link
https://drive.google.com/file/d/1yUjVDkHy-Xeg9paQ2LR_ZBPYF089rKzR/view?usp=drive_link
