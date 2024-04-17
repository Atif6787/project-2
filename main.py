import argparse
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

def scrape_website():
    url = "https://www.livecharts.co.uk/currency-strength.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Check if the elements are found before accessing properties
    usd_block = soup.find('div', class_='usd currency-row')
    if usd_block:
        rating_div = usd_block.find('div', class_='rating')
        if rating_div:
            return rating_div.text.strip()
        else:
            return "Rating not found"
    else:
        return "USD block not found"

def send_email(email, subject, body):
    sender_email = "your_email@gmail.com"
    password = "your_password"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())

def main():
    parser = argparse.ArgumentParser(description="Currency Strength Meter Bot")
    parser.add_argument("--email", required=True, help="Email address for notifications")
    args = parser.parse_args()

    previous_blocks = None

    while True:
        current_blocks = scrape_website()

        if previous_blocks is not None and current_blocks != previous_blocks:
            subject = "USD Currency Strength Update"
            body = f"The stability of USD currency has been updated. Current stability: {current_blocks}"
            send_email(args.email, subject, body)

        previous_blocks = current_blocks
        time.sleep(60)

if __name__ == "__main__":
    main()
