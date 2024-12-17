import streamlit as st  # type: ignore
import mysql.connector
import pandas as pd

def get_books(query):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bookscape_db"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

st.title("📚 BookScape Explorer")
st.sidebar.header("Filters")

option = st.sidebar.selectbox("Choose an option:", [
    "Top Rated Books", 
    "Books with > 500 Pages",
    "Books by Categories",
    "Check Availability of eBooks vs Physical Books",
    "Find the Publisher with the Most Books Published",
    "Identify the Publisher with the Highest Average Rating",
    "Get the Top 5 Most Expensive Books by Retail Price",
    "Find Books Published After 2010 with at Least 500 Pages",
    "List Books with Discounts Greater than 20%",
    "Find the Average Page Count for eBooks vs Physical Books",
    "Find the Top 3 Authors with the Most Books",
    "List Publishers with More than 10 Books",
    "Find the Average Page Count for Each Category",
    "Retrieve Books with More than 3 Authors",
    "Books with Ratings Count Greater Than the Average",
    "Books with the Same Author Published in the Same Year",
    "Books with a Specific Keyword in the Title",
    "Year with the Highest Average Book Price",
    "Count Authors Who Published 3 Consecutive Years",
    "Authors Published in Same Year but Different Publishers",
    "Average Retail Price of eBooks vs Physical Books",
    "Books with Ratings More than Two Standard Deviations from Average",
    "Publisher with the Highest Average Rating (More than 10 Books)"
])

if option == "Top Rated Books":
    query = "SELECT book_title, averageRating, ratingsCount FROM books ORDER BY averageRating DESC LIMIT 5"
    books = get_books(query)
    st.write(pd.DataFrame(books))

elif option == "Books with > 500 Pages":
    query = "SELECT book_title, pageCount FROM books WHERE pageCount > 500"
    books = get_books(query)
    st.write(pd.DataFrame(books))

elif option == "Books by Categories":
    category = st.sidebar.text_input("Enter a category:")
    if category:
        query = f"SELECT book_title, categories FROM books WHERE categories LIKE '%{category}%'"
        books = get_books(query)
        st.write(pd.DataFrame(books))

elif option == "Check Availability of eBooks vs Physical Books":
    query = """
    SELECT 
        SUM(CASE WHEN isEbook THEN 1 ELSE 0 END) AS ebook_count, 
        SUM(CASE WHEN NOT isEbook THEN 1 ELSE 0 END) AS physical_count 
    FROM books
    """
    availability = get_books(query)
    st.write(pd.DataFrame(availability))

elif option == "Find the Publisher with the Most Books Published":
    query = """
    SELECT 
        publisher, COUNT(*) AS book_count 
    FROM books 
    GROUP BY publisher 
    ORDER BY book_count DESC 
    LIMIT 1
    """
    publisher = get_books(query)
    st.write(pd.DataFrame(publisher))

elif option == "Identify the Publisher with the Highest Average Rating":
    query = """
    SELECT 
        publisher, AVG(averageRating) AS avg_rating 
    FROM books 
    GROUP BY publisher 
    ORDER BY avg_rating DESC 
    LIMIT 1
    """
    publisher = get_books(query)
    st.write(pd.DataFrame(publisher))

elif option == "Get the Top 5 Most Expensive Books by Retail Price":
    query = "SELECT book_title, amount_retailPrice FROM books ORDER BY amount_retailPrice DESC LIMIT 5"
    books = get_books(query)
    st.write(pd.DataFrame(books))

elif option == "Find Books Published After 2010 with at Least 500 Pages":
    query = "SELECT book_title, year, pageCount FROM books WHERE year > '2010' AND pageCount >= 500"
    books = get_books(query)
    st.write(pd.DataFrame(books))

elif option == "List Books with Discounts Greater than 20%":
    query = "SELECT book_title, amount_listPrice, amount_retailPrice FROM books WHERE (amount_listPrice - amount_retailPrice) / amount_listPrice > 0.2"
    books = get_books(query)
    st.write(pd.DataFrame(books))

elif option == "Find the Average Page Count for eBooks vs Physical Books":
    query = """
    SELECT 
        isEbook, AVG(pageCount) AS avg_pageCount 
    FROM books 
    GROUP BY isEbook
    """
    avg_pages = get_books(query)
    st.write(pd.DataFrame(avg_pages))

elif option == "Find the Top 3 Authors with the Most Books":
    query = """
    SELECT 
        book_authors, COUNT(*) AS book_count 
    FROM books 
    GROUP BY book_authors 
    ORDER BY book_count DESC 
    LIMIT 3
    """
    authors = get_books(query)
    st.write(pd.DataFrame(authors))

elif option == "List Publishers with More than 10 Books":
    query = """
    SELECT 
        publisher, COUNT(*) AS book_count 
    FROM books 
    GROUP BY publisher 
    HAVING book_count > 10
    """
    publishers = get_books(query)
    st.write(pd.DataFrame(publishers))

elif option == "Find the Average Page Count for Each Category":
    query = """
    SELECT 
        categories, AVG(pageCount) AS avg_pageCount 
    FROM books 
    GROUP BY categories
    """
    avg_category_pages = get_books(query)
    st.write(pd.DataFrame(avg_category_pages))

elif option == "Retrieve Books with More than 3 Authors":
    query = "SELECT book_title, book_authors FROM books WHERE LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) > 2"
    books = get_books(query)
    st.write(pd.DataFrame(books))

elif option == "Books with Ratings Count Greater Than the Average":
    query = """
    SELECT book_title, ratingsCount 
    FROM books 
    WHERE ratingsCount > (SELECT AVG(ratingsCount) FROM books)
    """
    books = get_books(query)
    st.write(pd.DataFrame(books))

elif option == "Books with the Same Author Published in the Same Year":
    query = """
    SELECT book_authors, year, COUNT(*) AS book_count 
    FROM books 
    GROUP BY book_authors, year 
    HAVING book_count > 1
    """
    books = get_books(query)
    st.write(pd.DataFrame(books))

elif option == "Books with a Specific Keyword in the Title":
    keyword = st.sidebar.text_input("Enter a keyword:")
    if keyword:
        query = f"SELECT book_title FROM books WHERE book_title LIKE '%{keyword}%'"
        books = get_books(query)
        st.write(pd.DataFrame(books))

elif option == "Year with the Highest Average Book Price":
    query = """
    SELECT year, AVG(amount_retailPrice) AS avg_price 
    FROM books 
    GROUP BY year 
    ORDER BY avg_price DESC 
    LIMIT 1
    """
    year_avg_price = get_books(query)
    st.write(pd.DataFrame(year_avg_price))

elif option == "Count Authors Who Published 3 Consecutive Years":
    query = """
    SELECT book_authors, COUNT(DISTINCT year) AS years_count 
    FROM books 
    GROUP BY book_authors 
    HAVING years_count >= 3
    """
    authors = get_books(query)
    st.write(pd.DataFrame(authors))

elif option == "Authors Published in Same Year but Different Publishers":
    query = """
    SELECT book_authors, year, COUNT(DISTINCT publisher) AS publishers_count 
    FROM books 
    GROUP BY book_authors, year 
    HAVING publishers_count > 1
    """
    authors = get_books(query)
    st.write(pd.DataFrame(authors))

elif option == "Average Retail Price of eBooks vs Physical Books":
    query = """
    SELECT 
        AVG(CASE WHEN isEbook THEN amount_retailPrice END) AS avg_ebook_price, 
        AVG(CASE WHEN NOT isEbook THEN amount_retailPrice END) AS avg_physical_price 
    FROM books
    """
    avg_prices = get_books(query)
    st.write(pd.DataFrame(avg_prices))

elif option == "Books with Ratings More than Two Standard Deviations from Average":
    query = """
    SELECT book_title, averageRating, ratingsCount 
    FROM books 
    WHERE averageRating > (SELECT AVG(averageRating) + 2 * STDDEV(averageRating) FROM books) 
    OR averageRating < (SELECT AVG(averageRating) - 2 * STDDEV(averageRating) FROM books)
    """
    outliers = get_books(query)
    st.write(pd.DataFrame(outliers))

elif option == "Publisher with the Highest Average Rating (More than 10 Books)":
    query = """
    SELECT 
        publisher, AVG(averageRating) AS avg_rating, COUNT(*) AS book_count 
    FROM books 
    GROUP BY publisher 
    HAVING book_count > 10 
    ORDER BY avg_rating DESC 
    LIMIT 1
    """
    publisher_rating = get_books(query)
    st.write(pd.DataFrame(publisher_rating))