import streamlit as st
from main import SQLGenerator
import time
from dotenv import load_dotenv
import os
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

def initialize_sql_generator():
    """Initialize SQL Generator with progress bar"""
    progress_text = "Initializing components..."
    my_bar = st.progress(0, text=progress_text)

    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)

        sql_generator = SQLGenerator(api_key)
        my_bar.empty()
        return sql_generator

    except Exception as e:
        my_bar.empty()
        raise e

def main():
    st.set_page_config(
        page_title="Book Inventory Query System",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    if 'sql_generator' not in st.session_state:
        try:
            with st.spinner('Initializing components...'):
                st.session_state.sql_generator = initialize_sql_generator()
            st.success("✅ System initialized successfully!")
        except Exception as e:
            st.error(f"Error initializing application: {str(e)}")
            st.stop()

    if 'question' not in st.session_state:
        st.session_state['question'] = ""

    # App UI
    st.title("Book Inventory Query System")

    # User info and timestamp in sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"**Current User:** RealChAuLa")
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        st.markdown(f"**Last Updated:** {current_time}")
        st.markdown("---")

        st.header("About")
        st.write("""
        This application helps you query book inventory data using natural language.
        Just type your question, and it will generate and execute the appropriate SQL query.
        """)

        st.header("Example Questions")
        example_questions = [
            "How many copies of 'To Kill a Mockingbird' do we have?",
            "What are the Fantasy books we have in our inventory?",
            "Show me the total stock value for books by J.K. Rowling",
            "What are the Books We have by Agatha Christie",
            "What is the average price of books by genre?",
            "List all books with stock quantity less than 100"
        ]

        for q in example_questions:
            if st.button(q, key=f"btn_{q}"):
                st.session_state['question'] = q

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        question = st.text_input(
            "Enter your question about book inventory:",
            value=st.session_state.get('question', ''),
            placeholder="e.g., How many copies of 'To Kill a Mockingbird' do we have?",
            key="question_input"
        )

        if question:
            try:
                with st.spinner("🤔 Generating SQL query and fetching results..."):
                    # Generate SQL query
                    sql_query = st.session_state.sql_generator.generate_sql(question)

                    # Display generated SQL
                    st.subheader("Generated SQL Query")
                    with st.expander("View SQL Query", expanded=True):
                        st.code(sql_query, language="sql")

                    # Execute query and display results
                    st.subheader("Query Results")
                    df = st.session_state.sql_generator.execute_sql_query(sql_query)

                    if df is not None and not df.empty:
                        st.dataframe(df, use_container_width=True)

                        # Add download button
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv,
                            file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            key="download_button"
                        )
                    else:
                        st.warning("⚠️ No results found for this query.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    with col2:
        # Help section
        with st.expander("ℹ️ Help & Instructions", expanded=True):
            st.markdown("""
            ### How to Use
            1. Type your question about the book inventory in natural language
            2. The system will generate an SQL query based on your question
            3. The query will be executed against the database
            4. Results will be displayed in a table format
            5. You can download the results as a CSV file

            ### Tips
            - Be specific about the title, author, and genre in your questions
            - You can ask about quantities, prices, and total values
            - Make sure to mention the specific attributes you're interested in

            ### Available Fields
            - title: The book title
            - author: The author of the book
            - genre: The genre of the book
            - price: Unit price
            - stock_quantity: Available quantity
            """)

        # Query History
        if 'query_history' not in st.session_state:
            st.session_state.query_history = []

        with st.expander("📚 Query History", expanded=True):
            if question and question not in [h[0] for h in st.session_state.query_history]:
                st.session_state.query_history.append((question, sql_query))

            if st.session_state.query_history:
                for i, (q, sql) in enumerate(reversed(st.session_state.query_history[-5:])):
                    st.markdown(f"**Q{i + 1}:** {q}")
                    st.code(sql, language="sql")
                    st.markdown("---")
            else:
                st.write("No queries yet. Start by asking a question!")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Powered by OpenAI GPT-3.5-turbo, LangChain, and Hugging Face's all-MiniLM-L6-v2 | Developed by RealChAuLa</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
