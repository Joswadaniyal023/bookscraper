import mysql.connector

def setup_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bookscape_db")
    cursor.execute("USE bookscape_db")
    
    # Create table with all columns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id VARCHAR(255) PRIMARY KEY,
            search_key VARCHAR(255),
            book_title VARCHAR(255),
            book_subtitle TEXT,
            book_authors TEXT,
            book_description TEXT,
            industryIdentifiers TEXT,
            text_readingModes BOOLEAN,
            image_readingModes BOOLEAN,
            pageCount INT,
            categories TEXT,
            language VARCHAR(10),
            imageLinks TEXT,
            ratingsCount INT,
            averageRating DECIMAL(3, 2),
            country VARCHAR(10),
            saleability VARCHAR(50),
            isEbook BOOLEAN,
            amount_listPrice DECIMAL(10, 2),
            currencyCode_listPrice VARCHAR(10),
            amount_retailPrice DECIMAL(10, 2),
            currencyCode_retailPrice VARCHAR(10),
            buyLink TEXT,
            year TEXT
        )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "_main_":
    setup_database()