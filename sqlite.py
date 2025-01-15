from crewai import Agent
from tools import tool
from dotenv import load_dotenv
import sqlite3
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# SQLite database setup function
def create_database():
    conn = sqlite3.connect("news_articles.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            headline TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# SQLite data storage function
def store_data_in_db(headline, description, date):
    conn = sqlite3.connect("news_articles.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO articles (headline, description, date)
        VALUES (?, ?, ?)
    ''', (headline, description, date))
    conn.commit()
    conn.close()

# Create the database if it doesn't exist
create_database()

# Creating a senior researcher agent to fetch headlines
news_researcher = Agent(
    role="News Reporter",
    goal='Extracting News Headlines from different news article websites in {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "Driven by curiosity, you're at the forefront of "
        "innovation, eager to explore and share knowledge that could change "
        "the world."
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=True
)

# Creating a writer agent to narrate stories
news_writer = Agent(
    role='Writer',
    goal='Narrate compelling tech stories about {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplifying complex topics, you craft "
        "engaging narratives that captivate and educate, bringing new "
        "discoveries to light in an accessible manner."
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=False
)

# Creating a storer agent to save news articles in SQLite
news_storer = Agent(
    role="Data Storer",
    goal="Store fetched news data into an SQLite database with fields: headline, description, and date.",
    verbose=True,
    memory=False,
    backstory=(
        "As the gatekeeper of data, you ensure all valuable "
        "information is stored securely and can be retrieved efficiently."
    ),
    tools=[],
    llm=llm,
    allow_delegation=False,
    task_fn=lambda articles: [
        store_data_in_db(
            article.get("headline"),
            article.get("description"),
            article.get("date")
        )
        for article in articles
    ]
)

# Sample integration workflow
if __name__ == "__main__":
    # Step 1: Research news articles
    topic = "Generative AI"
    articles = news_researcher.run({"topic": topic})

    if articles:
        print("Articles fetched successfully by news_researcher.")
        
        # Step 2: Write narratives (optional, depending on workflow)
        narratives = news_writer.run({"topic": topic, "articles": articles})
        print("Narratives written successfully by news_writer.")

        # Step 3: Store the articles in the database
        news_storer.run(articles)
        print("Articles stored successfully by news_storer.")
    else:
        print("No articles fetched.")