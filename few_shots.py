few_shots = [
    {
        "Question": "How many copies of '1984' do we have in stock?",
        "SQLQuery": "SELECT stock_quantity FROM books WHERE title = '1984';"
    },
    {
        "Question": "What's the total value of all fantasy books?",
        "SQLQuery": "SELECT SUM(price * stock_quantity) AS total_value FROM books WHERE genre = 'Fantasy';"
    },
    {
        "Question": "Show me the total inventory value for books by J.K. Rowling.",
        "SQLQuery": "SELECT SUM(price * stock_quantity) AS total_value FROM books JOIN authors ON books.author_id = authors.author_id WHERE authors.name = 'J.K. Rowling';"
    },
    {
        "Question": "What is the average price of books by genre?",
        "SQLQuery": "SELECT genre, AVG(price) AS average_price FROM books GROUP BY genre;"
    },
    {
        "Question": "List all books with stock quantity less than 5.",
        "SQLQuery": "SELECT title FROM books WHERE stock_quantity < 5;"
    },
    {
        "Question": "How many books are there by each author?",
        "SQLQuery": "SELECT authors.name, COUNT(books.book_id) AS book_count FROM books JOIN authors ON books.author_id = authors.author_id GROUP BY authors.name;"
    },
    {
        "Question": "What are the titles of all mystery books?",
        "SQLQuery": "SELECT title FROM books WHERE genre = 'Mystery';"
    },
    {
        "Question": "Which author has the highest number of books in stock?",
        "SQLQuery": "SELECT authors.name FROM books JOIN authors ON books.author_id = authors.author_id GROUP BY authors.name ORDER BY SUM(books.stock_quantity) DESC LIMIT 1;"
    },
    {
        "Question": "What is the total revenue from all orders?",
        "SQLQuery": "SELECT SUM(total_amount) AS total_revenue FROM orders;"
    },
    {
        "Question": "List all orders placed in the last month.",
        "SQLQuery": "SELECT * FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH);"
    }
]