import langchain
import openai
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
import mysql.connector
from mysql.connector import Error
import pandas as pd
from few_shots import few_shots
import os
from dotenv import load_dotenv

load_dotenv()
langchain.debug = True

class SQLGenerator:
    DB_CONFIG = {
        "host": os.getenv('DB_HOST', 'localhost'),
        "port": int(os.getenv('DB_PORT', 3306)),
        "user": os.getenv('DB_USER', 'root'),
        "password": os.getenv('DB_PASSWORD', ''),
        "database": os.getenv('DB_NAME', 'book_inventory')
    }

    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.example_selector = self.initialize_embeddings_and_selector()
        self.prompt = self.create_prompt_template()

    @staticmethod
    def initialize_embeddings_and_selector():
        try:
            embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

            texts = [
                f"Question: {ex['Question']} SQLQuery: {ex['SQLQuery']}"
                for ex in few_shots
            ]

            vectorstore = FAISS.from_texts(texts, embeddings, metadatas=few_shots)

            return SemanticSimilarityExampleSelector(
                vectorstore=vectorstore,
                k=2
            )

        except Exception as e:
            raise Exception(f"Error initializing embeddings: {str(e)}")

    def create_prompt_template(self):

        example_prompt = PromptTemplate(
            input_variables=["Question", "SQLQuery"],
            template="Question: {Question}\nSQL: {SQLQuery}"
        )

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
        try:
            prompt = self.prompt.format(question=question)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            clean_response = response['choices'][0]['message']['content'].strip()
            clean_response = clean_response.replace("SQL Query:[/INST]", "").replace("SQL Query:", "").strip()

            if 'SELECT' in clean_response:
                query = [line.strip() for line in clean_response.split('\n') if 'SELECT' in line][0]
                query = query.replace('\_', '_')  # Remove escape characters
                return query
            else:
                raise Exception("No valid SQL query generated")

        except Exception as e:
            raise Exception(f"Error generating SQL: {str(e)}")

    def execute_sql_query(self, query):
        try:
            connection = mysql.connector.connect(**self.DB_CONFIG)
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                results = cursor.fetchall()

                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    return pd.DataFrame(results, columns=columns)
                return pd.DataFrame(results)  # Empty DataFrame for no result set

        except Error as e:
            raise Exception(f"Database Error: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
