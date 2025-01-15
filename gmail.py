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
            .content {{
                margin-top: 20px;
            }}
            .footer {{
                text-align: left;
                padding-top: 20px;
                color: black;
                font-size: 12px;
                margin-top: 40px;
            }}
            .footer table {{
                width: 100%;
            }}
            .footer img {{
                width: 120px;
                height: 120px;
                margin-bottom: 20px;
            }}
            .footer td {{
                padding: 5px;
            }}
            .footer a {{
                color: blue;
                text-decoration: underline; /* Ensures links are underlined */
            }}
            .footer a:hover {{
                text-decoration: underline;
            }}
            .footer p {{
                font-size: 10px;
                color: black;
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
                .footer p {{
                    font-size: 12px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <h1>{subject}</h1>
            <div class="content">
                {html_content}
            </div>
            <div class="footer">
                <table>
                    <tr>
                        <td style="padding-right: 15px;">
                            <img src="https://drive.google.com/uc?export=view&id=1ciMZhUymSZeswzqmvhgph4Jd-FVVFPwc" alt="EY Logo">
                        </td>
                        <td>
                            <b>Diksha Kharbanda | Intern</b>
                            <p>Ernst & Young LLP</p>
                            <p>Plot number 67, Sector 44, Gurugram, Haryana, 122003, India</p>
                            <p>Cell: +918572820094 | Email: 
                                <a href="mailto:dkharbanda.diksha@gmail.com" style="text-decoration: underline;">
                                    dkharbanda.diksha@gmail.com
                                </a>
                            </p>
                            <p>Website: 
                                <a href="http://www.ey.com" target="_blank" style="text-decoration: underline;">
                                    www.ey.com
                                </a>
                            </p>
                        </td>
                    </tr>
                </table>
                <p class="disclaimer">The information contained in this communication is intended solely for the use of the individual or entity to whom it is addressed and may contain confidential or privileged material. If you are not the intended recipient, please notify the sender immediately and delete this communication. Any unauthorized use, disclosure, or distribution of the information contained in this communication is prohibited.</p>
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
    sender_password="fprr vmtu puwb vmuv",  # Replace with your actual email password
    recipient_email="kharbanda.dikshak@gmail.com",
    subject="Today's Top Generative AI News",
    markdown_file="news-summaries.md"
)

