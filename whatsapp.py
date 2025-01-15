import pywhatkit
import markdown
import html2text
from datetime import datetime, timedelta

def read_markdown_as_text(markdown_file):
    """
    Reads a Markdown file and converts its content to plain text.
    """
    with open(markdown_file, 'r', encoding='utf-8') as file:
        md_content = file.read()
    
    # Convert Markdown to HTML and then to plain text
    html_content = markdown.markdown(md_content)
    plain_text = html2text.html2text(html_content).strip()
    return plain_text

def send_whatsapp_message(phone_number, message):
    """
    Sends a WhatsApp message using pywhatkit.
    """
    now = datetime.now()
    # Schedule for 1 minute later (minimum allowed time by pywhatkit)
    send_time = now + timedelta(minutes=1)  # send in 1 minute
    
    try:
        pywhatkit.sendwhatmsg(
            phone_number, 
            message, 
            send_time.hour,  # hour
            send_time.minute,  # minute
            wait_time=15  # Optional, wait for the message to be sent
        )
        print("Message scheduled successfully!")
    except Exception as e:
        print(f"Failed to send message: {e}")

# Example Usage
if __name__ == "__main__":
    # Replace these with your actual values
    recipient_phone_number = "+919876543210"  # Replace with the recipient's WhatsApp number
    markdown_file_path = "news-summaries.md"  # Path to your Markdown file

    # Read the message from the Markdown file
    message = read_markdown_as_text(markdown_file_path)

    # Send the message
    send_whatsapp_message(recipient_phone_number, message)
