import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the API key and endpoint for Gemini API
ai_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyCw2B5ou8onk1BabogyppBYX_Ff2oalQ00"

# File paths for memory
short_term_memory_file = "short_term_memory.json"
long_term_memory_file = "long_term_memory.json"

# Initialize memory structures
short_term_memory = {}
long_term_memory = {}

# Load memory from file
def load_memory(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading memory from {file_path}: {e}")
        return {}

# Save memory to file
def save_memory(memory, file_path):
    try:
        with open(file_path, "w") as file:
            json.dump(memory, file, indent=4)
        print(f"Memory saved to {file_path}")
    except Exception as e:
        print(f"Error saving memory to {file_path}: {e}")

# AI Agent to manage decisions
class AIAgent:
    def __init__(self):  # Fixed constructor
        self.memory_check_log = []  # Correct initialization of memory_check_log

    def decide_memory_source(self, url):
        """
        Decide whether to fetch data from short-term memory, long-term memory, or fresh data.
        """
        if url in short_term_memory:
            self.memory_check_log.append(f"Using short-term memory for URL: {url}")
            return "short-term"
        elif url in long_term_memory:
            self.memory_check_log.append(f"Using long-term memory for URL: {url}")
            return "long-term"
        else:
            self.memory_check_log.append(f"Fetching fresh data for URL: {url}")
            return "fetch"

    def summarize_log(self):
        """
        Summarize AI agent decisions for debugging.
        """
        print("\n=== AI Agent Decision Log ===")
        for log in self.memory_check_log:
            print(log)

# Function to generate a concise description using Gemini API
def generate_ai_description(text):
    payload = {
        "prompt": {
            "text": f"Summarize the following into a concise paragraph: {text}"
        },
        "maxOutputTokens": 100  # Limit the output length for conciseness
    }
    headers = {
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(ai_url, headers=headers, json=payload)
        if response.status_code == 200:
            ai_response = response.json()
            if 'candidates' in ai_response and len(ai_response['candidates']) > 0:
                return ai_response['candidates'][0]['output'].strip()
        return text  # Fallback to original text if API fails
    except Exception as e:
        print(f"Error communicating with Gemini API: {e}")
        return text  # Fallback to original text if API request fails

# Function to fetch articles from a website
def fetch_articles_from_website(url, agent):
    decision = agent.decide_memory_source(url)

    if decision == "short-term":
        return short_term_memory[url]
    elif decision == "long-term":
        # Load into short-term memory for future use
        short_term_memory[url] = long_term_memory[url]
        save_memory(short_term_memory, short_term_memory_file)
        return long_term_memory[url]

    # Fetch fresh data from the website
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        potential_headlines = soup.find_all(['h1', 'h2', 'h3'], limit=10)
        for headline in potential_headlines:
            title = headline.get_text(strip=True)
            link = headline.find_parent('a') or headline.find('a')
            article_url = urljoin(url, link['href']) if link and link.get('href') else url
            description_tag = headline.find_next('p')
            description = description_tag.get_text(strip=True) if description_tag else "No description available."
            description = generate_ai_description(f"Title: {title}. Description: {description}")
            articles.append({
                "title": title,
                "url": article_url,
                "description": description
            })
            if len(articles) >= 5:
                break

        # Save to both short-term and long-term memory
        short_term_memory[url] = articles
        long_term_memory[url] = articles
        save_memory(short_term_memory, short_term_memory_file)
        save_memory(long_term_memory, long_term_memory_file)

        return articles
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return []

# Save output to JSON
def save_to_json(data, filename="output.json"):
    try:
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

# Main function to fetch and save articles
if __name__ == "__main__":
    # Load persistent memory on startup
    short_term_memory = load_memory(short_term_memory_file)
    long_term_memory = load_memory(long_term_memory_file)

    # Initialize AI agent
    agent = AIAgent()

    # Website URL for fetching articles
    website_url = "https://analyticsindiamag.com/news/generative-ai/"  # Example URL

    # Fetch articles using AI agent
    articles = fetch_articles_from_website(website_url, agent)

    # Save fetched articles to JSON
    save_to_json(articles)

    # Summarize agent's decisions
    agent.summarize_log()
