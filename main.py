import openai
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
import mysql.connector
from mysql.connector import Error
import pandas as pd
from few_shots import few_shots
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class SQLGenerator:
    # Configuration for database connection, loaded from environment variables
    DB_CONFIG = {
        "host": os.getenv('DB_HOST', 'localhost'),
        "port": int(os.getenv('DB_PORT', 3306)),
        "user": os.getenv('DB_USER', 'root'),
        "password": os.getenv('DB_PASSWORD', ''),
        "database": os.getenv('DB_NAME', 'book_inventory')
    }

    def __init__(self, api_key):
        """
        Initialize the SQLGenerator class.
        - Set up the OpenAI API key for GPT interaction.
        - Initialize embeddings and example selector for semantic similarity.
        - Create a prompt template for question-to-SQL transformation.
        """
        self.api_key = api_key
        openai.api_key = self.api_key
        self.example_selector = self.initialize_embeddings_and_selector()
        self.prompt = self.create_prompt_template()

    def initialize_embeddings_and_selector(self):
        """
        Initialize embeddings and the semantic similarity-based example selector.
        - Uses Hugging Face embeddings to represent the few-shot examples.
        - Builds a FAISS vector store to store the embeddings for similarity-based selection.
        """
        try:
            # Load Hugging Face model for embedding generation
            embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

            # Prepare text data for the few-shot examples
            texts = [
                f"Question: {ex['Question']} SQLQuery: {ex['SQLQuery']}"
                for ex in few_shots
            ]

            # Create a FAISS vector store for example selection
            vectorstore = FAISS.from_texts(texts, embeddings, metadatas=few_shots)

            # Initialize example selector using the vector store
            return SemanticSimilarityExampleSelector(
                vectorstore=vectorstore,
                k=2  # Select the top 2 most similar examples
            )

        except Exception as e:
            raise Exception(f"Error initializing embeddings: {str(e)}")

    def create_prompt_template(self):
        """
        Create a prompt template for transforming natural language questions into SQL queries.
        - Uses FewShotPromptTemplate for including examples dynamically based on similarity.
        """
        # Template for formatting individual examples
        example_prompt = PromptTemplate(
            input_variables=["Question", "SQLQuery"],
            template="Question: {Question}\nSQL: {SQLQuery}"
        )

        # Define the complete prompt structure with prefix, examples, and suffix
        return FewShotPromptTemplate(
            example_selector=self.example_selector,
            example_prompt=example_prompt,
            prefix="""Convert the following question about book inventory into a SQL query.
    Table: books (book_id, title, author_id, genre, price, stock_quantity)""",
            suffix="\nQuestion: {question}\nSQL:",
            input_variables=["question"],
            example_separator="\n\n"
        )

    def generate_sql(self, question):
        """
        Generate a SQL query from a natural language question using GPT-3.5-turbo.
        - Formats the prompt with the input question.
        - Sends the prompt to OpenAI API for SQL generation.
        - Cleans and validates the generated SQL query.
        """
        try:
            # Format the prompt with the input question
            prompt = self.prompt.format(question=question)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract and clean the generated SQL query
            clean_response = response['choices'][0]['message']['content'].strip()
            clean_response = clean_response.replace("SQL Query:[/INST]", "").replace("SQL Query:", "").strip()

            # Ensure the response contains a valid SQL SELECT query
            if 'SELECT' in clean_response:
                query = [line.strip() for line in clean_response.split('\n') if 'SELECT' in line][0]
                query = query.replace('\_', '_')  # Remove escape characters
                return query
            else:
                raise Exception("No valid SQL query generated")

        except Exception as e:
            raise Exception(f"Error generating SQL: {str(e)}")

    def execute_sql_query(self, query):
        """
        Execute the generated SQL query against the MySQL database.
        - Connects to the database using the provided configuration.
        - Executes the query and fetches results.
        - Returns results as a Pandas DataFrame for easy handling.
        """
        try:
            # Connect to the MySQL database
            connection = mysql.connector.connect(**self.DB_CONFIG)
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                results = cursor.fetchall()

                # If the query has a result set, return it as a DataFrame
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    return pd.DataFrame(results, columns=columns)
                return pd.DataFrame(results)  # Empty DataFrame for no result set

        except Error as e:
            raise Exception(f"Database Error: {e}")
        finally:
            # Ensure the database connection is closed
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
