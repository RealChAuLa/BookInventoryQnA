# BookInventoryQnA

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-32CD32?style=for-the-badge&logo=chainlink&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![FAISS](https://img.shields.io/badge/FAISS-117ACA?style=for-the-badge&logo=facebook&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

BookInventoryQnA is a Python-based project that allows users to interact with their database using natural language questions. Built with OpenAI's GPT-3.5-turbo and Streamlit, this application converts natural language queries into SQL, executes them, and presents results in a user-friendly format.

## 📚 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [System Architecture](#system-architecture)
- [Database Schema](#database-schema)
- [Example Queries](#example-queries)

## 🔍 Overview

BookInventoryQnA bridges the gap between natural language and SQL databases by allowing users to ask questions in plain English about a book inventory. The system leverages modern AI technology to translate these questions into SQL queries, execute them against a MySQL database, and display the results in an intuitive interface.

This project was developed as part of the Emerging Technologies module at university, showcasing the practical application of natural language processing in database management.

## ✨ Features

- **Natural Language Querying**: Ask questions in plain English about book inventory
- **AI-Powered SQL Generation**: Automatic translation of natural language to SQL
- **Interactive Web Interface**: Clean, user-friendly Streamlit application
- **Example Queries**: Pre-populated examples to help users get started
- **Query History**: Track and revisit previous queries
- **Result Export**: Download query results as CSV files
- **Error Handling**: User-friendly error messages and suggestions
- **Voice Interaction**: Prototype design for voice-based queries (coming soon)

## 🛠️ Technology Stack

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **OpenAI GPT-3.5-turbo**: Natural language processing
- **LangChain**: Framework for LLM applications
- **HuggingFace Sentence-Transformers**: Embedding model (all-MiniLM-L6-v2)
- **FAISS**: Vector similarity search for few-shot example selection
- **MySQL**: Database management system
- **Pandas**: Data manipulation and display

## 📋 Installation

### Prerequisites

- Python 3.8 or higher
- MySQL server (local or remote)
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/RealChAuLa/BookInventoryQnA.git
cd BookInventoryQnA
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root with the following variables:
```Code
OPENAI_API_KEY=your_openai_api_key
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_database_password
DB_NAME=book_inventory
```
5. Set up the database:
Create a MySQL database named book_inventory
, Populate with sample data using book_inventory.sql
