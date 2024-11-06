# Import required libraries for email handling, web scraping, and environment variables
import os
from dotenv import load_dotenv
import imaplib
import email
from bs4 import BeautifulSoup
import requests
load_dotenv()

# Get email credentials from environment variables for security
username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def connect_to_mail():
    """Establish a secure connection to Gmail's IMAP server"""
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    return mail

def extract_links_from_html(html_content):
    """Parse HTML content and extract all unsubscribe links"""
    soup = BeautifulSoup(html_content, "html.parser")
    # Find all 'a' tags with href attributes containing 'unsubscribe'
    links = [link["href"] for link in soup.find_all("a", href=True) if "unsubscribe" in link["href"].lower()]
    return links

def click_link(link):
    """Simulate clicking on an unsubscribe link by sending a GET request"""
    try:
        response = requests.get(link)
        if response.status_code == 200:
            print("Successfully visited",link)
        else:
            print("Failed to visit",link, "error code", response.status_code)
    except Exception as e:
        print("Error visiting",link,str(e))

def search_for_email():
    """Search inbox for emails containing 'unsubscribe' and extract links"""
    mail = connect_to_mail()
    # Search for emails containing 'unsubscribe' in the body
    _, search_data = mail.search(None, '(BODY "unsubscribe")')
    data = search_data[0].split()
    
    links = []
    for num in data:
        # Fetch each email's content
        _, data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        
        if msg.is_multipart():
            # Handle multipart emails (emails with both HTML and text content)
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    try:
                        # Try different encodings to handle various email formats
                        html_content = part.get_payload(decode=True).decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            html_content = part.get_payload(decode=True).decode('latin-1')
                        except UnicodeDecodeError:
                            html_content = part.get_payload(decode=True).decode('cp1252', errors='ignore')
                    links.extend(extract_links_from_html(html_content))
        else:
            # Handle single part emails
            content_type = msg.get_content_type()
            content = msg.get_payload(decode=True).decode()
            if content_type == "text/html":
                links.extend(extract_links_from_html(content))
    mail.logout()
    return links

def save_links(links):
    """Save extracted unsubscribe links to a text file"""
    with open("links.txt", "w") as f:
        for link in links:
            f.write("\n".join(links))

# Main execution flow
links = search_for_email()  # First, search for and collect all unsubscribe links
for link in links:         # Then visit each link to trigger unsubscribe
    click_link(link)

save_links(links)          # Finally, save all links to a file for reference