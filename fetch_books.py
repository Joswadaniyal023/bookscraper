import requests
import mysql.connector

BASE_URL = "https://www.googleapis.com/books/v1/volumes"

def fetch_books(api_key, search_query, max_results=100):
    books = []
    start_index = 0
    
    while len(books) < max_results:
        params = {
            "q": search_query,
            "startIndex": start_index,
            "maxResults": 40,
            "key": api_key
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if "items" not in data:
            break
        
        for item in data["items"]:
            volume_info = item.get("volumeInfo", {})
            sale_info = item.get("saleInfo", {})
            book_info = {
                "book_id": item.get("id", ""),
                "search_key": search_query,
                "book_title": volume_info.get("title", ""),
                "book_subtitle": volume_info.get("subtitle", ""),
                "book_authors": ", ".join(volume_info.get("authors", [])),
                "book_description": volume_info.get("description", ""),
                "industryIdentifiers": ", ".join([identifier.get("identifier", "") for identifier in volume_info.get("industryIdentifiers", [])]),
                "text_readingModes": volume_info.get("readingModes", {}).get("text", False),
                "image_readingModes": volume_info.get("readingModes", {}).get("image", False),
                "pageCount": volume_info.get("pageCount", 0),
                "categories": ", ".join(volume_info.get("categories", [])),
                "language": volume_info.get("language", ""),
                "imageLinks": volume_info.get("imageLinks", {}).get("thumbnail", ""),
                "ratingsCount": volume_info.get("ratingsCount", 0),
                "averageRating": volume_info.get("averageRating", None),
                "country": sale_info.get("country", ""),
                "saleability": sale_info.get("saleability", ""),
                "isEbook": sale_info.get("isEbook", False),
                "amount_listPrice": sale_info.get("listPrice", {}).get("amount", None),
                "currencyCode_listPrice": sale_info.get("listPrice", {}).get("currencyCode", ""),
                "amount_retailPrice": sale_info.get("retailPrice", {}).get("amount", None),
                "currencyCode_retailPrice": sale_info.get("retailPrice", {}).get("currencyCode", ""),
                "buyLink": sale_info.get("buyLink", ""),
                "year": volume_info.get("publishedDate", "")[:4],
                "publisher": volume_info.get("publisher", "")  # New publisher field added
            }
            books.append(book_info)
        
        start_index += 40
    
    return books

def insert_into_database(books):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bookscape_db"
    )
    cursor = conn.cursor()
    
    for book in books:
        cursor.execute("""
            INSERT IGNORE INTO books (
                book_id, search_key, book_title, book_subtitle, book_authors,
                book_description, industryIdentifiers, text_readingModes, image_readingModes,
                pageCount, categories, language, imageLinks, ratingsCount, averageRating,
                country, saleability, isEbook, amount_listPrice, currencyCode_listPrice,
                amount_retailPrice, currencyCode_retailPrice, buyLink, year, publisher  -- Add publisher to the INSERT statement
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  -- Add publisher placeholder
        """, (
            book["book_id"], book["search_key"], book["book_title"], book["book_subtitle"], book["book_authors"],
            book["book_description"], book["industryIdentifiers"], book["text_readingModes"], book["image_readingModes"],
            book["pageCount"], book["categories"], book["language"], book["imageLinks"], book["ratingsCount"], book["averageRating"],
            book["country"], book["saleability"], book["isEbook"], book["amount_listPrice"], book["currencyCode_listPrice"],
            book["amount_retailPrice"], book["currencyCode_retailPrice"], book["buyLink"], book["year"],
            book["publisher"]  
        ))
    
    conn.commit()
    conn.close()


API_KEY = "AIzaSyAZ7i85WBoTEc1pHMhPZmid8DJsMR7TINU"
books_data = fetch_books(API_KEY, search_query="fiction",max_results=1000)
insert_into_database(books_data)