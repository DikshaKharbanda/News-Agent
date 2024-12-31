import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_articles_from_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Modify selectors based on the website structure
        articles = []
        for article_section in soup.find_all('article', limit=5):  # Find top 5 articles
            title_tag = article_section.find('h2') or article_section.find('h3') or article_section.find('h1')
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            link = title_tag.find('a')
            article_url = urljoin(url, link['href']) if link and link.get('href') else url

            # Find description
            description_tag = article_section.find('p')
            description = description_tag.get_text(strip=True) if description_tag else "No description available."

            # Find image
            img_tag = article_section.find('img')
            image_url = urljoin(url, img_tag['src']) if img_tag and img_tag.get('src') else None

            articles.append({
                "title": title,
                "url": article_url,
                "description": description,
                "image_url": image_url
            })

        return articles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return []

def send_email(articles, sender_email, recipient_email, smtp_server, smtp_port, login, password):
    try:
        # Create email content
        subject = "Today's Top Generative AI News"

        body = """
        <html>
        <head><style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; }
        .email-container { width: 80%; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px;  }
        .email-container h1 {
        color: black;
        border-bottom: 1px solid #ececec;
        }
        .email-container p {
        color: black;
        
        line-height: 1.6;
        }
        .email-header h1 {
            color: #333;
        }
        .article {
            padding: 15px 0;
            border-bottom: 1px solid #ececec;
            margin-bottom: 20px;
        }
        .article:last-child {
            border-bottom: none;
        }
        .article h2 {
            color: blue;
            font-size: 18px;
        }
        .article h2 a {
            text-decoration: none;
            color: blue;
        }
        .article h2 a:hover {
            text-decoration: underline;
            color:red;
        }
        .article p {
            color: black;
            font-size: 14px;
            line-height: 1.6;
        }
        .article img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin-top: 10px;
        }
        .footer {
            text-align: left;
            padding-top: 20px;
            color: black;
            font-size: 12px;
            margin-top: 40px;
        }
        .footer table {
            width: 100%;
        }
        .footer img {
            width: 120px;
            height: 120px;
            margin-bottom: 40px;
        }
        .footer td {
            padding: 2px;
            gap:2px;
        }
        .footer a {
            color: blue;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
            color:red;
        }
        .footer p new{
        font-size: 20px;
        }
        .footer a:hover {
            text-decoration: underline;
            color:red;
        }
        .disclaimer {
            font-size: 10px;
            color: black;
            line-height: 1.6;
                
        }
        .footer p{
            font-size: 10px;
            color: black;
        }
        @media (min-width: 1024px) {
    .footer {
        margin: 0; /* Remove extra margin */
        max-width: 1300px; /* Restrict width for left alignment */
        gap:5px;
        
    }

    .footer table {
        margin: 0 auto; /* Center the table if needed */
        gap:5px;
    }

    .footer img {
        width: 150px; /* Adjust image size for laptops */
        height: 150px;
        
    }

    .footer td {
        padding: 25px;
    }

    .footer a {
        font-size: 14px; /* Increase link font size */
    }

    .disclaimer {
        font-size: 12px; /* Adjust text size for clarity on larger screens */
    }
}
        </style></head>
        <body>
        <div class="email-container">
        <h1>Generative AI Daily News</h1>
        <p>Stay updated with the latest in generative AI technology</p>
        """
        for article in articles:
            body += f"""
            <div class="article">
                <h2><a href="{article['url']}">{article['title']}</a></h2>
                <p>{article['description']}</p>
            """
            if article['image_url']:
                body += f"<img src='{article['image_url']}' alt='{article['title']}'>"
            body += "</div>"

        body += """ <div class="footer">
            <p class = "new">Regards,</p>
            <table>
                    <tr>
                        <td style="padding-right: 15px;">
                            <img src="https://drive.google.com/uc?export=view&id=1ciMZhUymSZeswzqmvhgph4Jd-FVVFPwc" alt="Company Logo">
                        </td>

                    
                    <td>
                        <b>Diksha Kharbanda</b>
                        <p>Ernst & Young LLP</p>
                        <p>Plot number 67, Sector 44, Gurugram, Haryana, 122003, India</p>
                        <p>Cell: +918572820094 | dkharbanda.diksha@gmail.com</p>
                        <p>Website: <a href="http://www.ey.com" target="_blank">www.ey.com</a></p>
                        <br>
                        </td>
                </tr>
            </table>
                        <p class="disclaimer">The information contained in this communication is intended solely for the use of the individual or entity to whom it is addressed and others authorized to receive it. It may contain confidential or legally privileged information. If you are not the intended recipient you are hereby notified that any disclosure, copying, distribution or taking any action in reliance on the contents of this information is strictly prohibited and may be unlawful. If you have received this communication in error, please notify us immediately by responding to this email and then delete it from your system. The firm is neither liable for the proper and complete transmission of the information contained in this communication nor for any delay in its receipt.</p>
        </div>
    </div></body></html>"""

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(login, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")

# Example usage
if __name__ == "__main__":
    website_url = "https://www.artificialintelligence-news.com/"
    sender_email = "dkharbanda.diksha@gmail.com"
    recipient_email = "kharbanda.dikshak@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_login = "dkharbanda.diksha@gmail.com"
    email_password = "fprr vmtu puwb vmuv"  # Use App Password if 2FA is enabled

    articles = fetch_articles_from_website(website_url)
    if articles:
        print("Articles fetched successfully. Sending email...")
        send_email(articles, sender_email, recipient_email, smtp_server, smtp_port, email_login, email_password)
    else:
        print("No articles found to send via email.")