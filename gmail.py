import markdown
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, recipient_email, subject, markdown_file):
    # Read the content from the .md file
    with open(markdown_file, 'r', encoding='utf-8') as file:
        md_content = file.read()
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content)
    
    # Add custom CSS to style the email content
    html_content_with_style = f"""
    <html>
    <head>
        <style>
            /* General Styles */
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                width: 80%;
                margin: auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
            }}
            .email-container h1 {{
                color: black;
                border-bottom: 1px solid #ececec;
            }}
            .email-container p {{
                color: black;
                line-height: 1.6;
            }}
            .header h1 {{
                color: #333;
            }}
            .headline {{
                font-size: 20px;
                font-weight: bold;
                color: black;
                margin-bottom: 10px;
            }}
            .description {{
                font-size: 14px;
                color: black;
                line-height: 1.6;
            }}
            .footer {{
                text-align: left;
                padding-top: 20px;
                color: black;
                font-size: 12px;
                margin-top: 40px;
            }}
            .footer img {{
                width: 120px;
                height: 120px;
                margin-bottom: 40px;
            }}
            .footer a {{
                color: blue;
                text-decoration: none;
            }}
            .footer a:hover {{
                text-decoration: underline;
                color: red;
            }}
            .disclaimer {{
                font-size: 10px;
                color: black;
                line-height: 1.6;
            }}
            @media (min-width: 1024px) {{
                .footer {{
                    margin: 0;
                    max-width: 1300px;
                }}
                .footer img {{
                    width: 150px;
                    height: 150px;
                }}
                .footer a {{
                    font-size: 14px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <h1>{subject}</h1>
            <p class="headline">Headline</p>
            <p class="description">{html_content}</p>
            <div class="footer">
                <p>© 2025 Your Company Name. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Create an email message
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email

    # Add both plain text and styled HTML content
    message.attach(MIMEText(md_content, "plain"))
    message.attach(MIMEText(html_content_with_style, "html"))

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
send_email(
    sender_email="dkharbanda.diksha@gmail.com",
    sender_password="fprr vmtu puwb vmuv",
    recipient_email="kharbanda.dikshak@gmail.com",
    subject="Daily Generative AI News",
    markdown_file="news-summaries.md"
)