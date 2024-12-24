import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_articles_from_website(url):
    # Send a GET request to the website
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Step 1: Search for all possible headline tags (h1, h2, h3, etc.)
        headline_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        articles = []

        # Step 2: Collect titles, URLs, and brief descriptions
        for tag in headline_tags:
            title = tag.get_text(strip=True)
            # Find the closest <a> tag for the link
            link = tag.find_parent('a') or tag.find_next('a')
            if link and link.get('href'):
                article_url = urljoin(url, link['href'])  # Ensure complete URL
                
                # Step 3: Try to find a brief description or snippet related to the article
                description = None
                # Attempt to find the first <p> tag or any other tag nearby that might contain a description
                description_tag = tag.find_next(['p', 'span', 'div'])
                if description_tag:
                    description = description_tag.get_text(strip=True)

                articles.append({
                    "title": title,
                    "url": article_url,
                    "description": description if description else "No description available."
                })

        # Step 4: Output the top articles with their brief details (limit to top 5)
        if articles:
            print(f"Top Articles from {url}:")
            for i, article in enumerate(articles[:5], start=1):
                print(f"{i}. {article['title']}")
                print(f"   URL: {article['url']}")
                print(f"   Brief: {article['description']}")
                print()
        else:
            print("No articles found on the page.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")

# Example usage
fetch_articles_from_website("https://generative-ai-newsroom.com/")