import sqlite3
from datetime import datetime
from pydantic import BaseModel, ValidationError
from scraping import fetch_articles_from_website

class Article(BaseModel):
    headline: str
    description: str
    url: str
    date: str

def create_database():
    # Connect to SQLite database (creates file if not exists)
    conn = sqlite3.connect("articles.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            headline TEXT NOT NULL,
            description TEXT,
            url TEXT,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def store_articles_in_db(articles):
    # Connect to SQLite database
    conn = sqlite3.connect("articles.db")
    cursor = conn.cursor()

    # Insert articles into the database
    for article in articles:
        try:
            # Validate the article using Pydantic
            validated_article = Article(
                headline=article["title"],
                description=article["description"],
                url=article["url"],
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            # Insert validated article into the database
            cursor.execute('''
                INSERT INTO articles (headline, description, url, date)
                VALUES (?, ?, ?, ?)
            ''', (validated_article.headline, validated_article.description, validated_article.url, validated_article.date))
        except ValidationError as e:
            print(f"Error validating article: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Ensure database and table are created
    create_database()

    # URL of the website to scrape articles from
    website_url = "https://www.artificialintelligence-news.com/"

    # Fetch articles using scraping.py
    articles = fetch_articles_from_website(website_url)

    if articles:
        print("Articles fetched successfully. Storing in the database...")
        store_articles_in_db(articles)
        print("Articles stored successfully.")
    else:
        print("No articles found to store in the database.")

