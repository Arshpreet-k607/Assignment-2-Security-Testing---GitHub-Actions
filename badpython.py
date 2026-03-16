import os
import pymysql  # type: ignore
from urllib.request import urlopen
import ssl
import smtplib
from email.message import EmailMessage

# flake8: noqa

# Read DB config from environment variables (avoid hard-coded credentials)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME', 'mydb')

if not DB_USER or not DB_PASSWORD:
    raise SystemExit(
        "Database credentials not set in environment variables "
        "(DB_USER/DB_PASSWORD).",
    )

db_config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'db': DB_NAME,
    'cursorclass': pymysql.cursors.DictCursor,
}


def get_user_input():
    user_input = input('Enter your name: ').strip()
    # Basic validation
    if not user_input:
        raise ValueError("Input cannot be empty.")
    if len(user_input) > 100:
        user_input = user_input[:100]
    return user_input


def send_email(to, subject, body):
    # Use Python's SMTP library instead of shelling out
    SMTP_HOST = os.environ.get('SMTP_HOST', 'localhost')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 25))
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    FROM_ADDRESS = os.environ.get('FROM_EMAIL', 'noreply@example.com')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = FROM_ADDRESS
    msg['To'] = to
    msg.set_content(body)

    try:
        if SMTP_USER and SMTP_PASSWORD:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.send_message(msg)
        print("Email sent.")
    except Exception as e:
        print("Error sending email:", e)


def get_data():
    url = 'https://insecure-api.com/get-data'  # prefer HTTPS
    try:
        context = ssl.create_default_context()
        with urlopen(url, timeout=10, context=context) as resp:
            if resp.status != 200:
                raise ValueError(f"HTTP error: {resp.status}")
            data = resp.read().decode()
            return data
    except Exception as e:
        print("Error fetching data:", e)
        return ""


def save_to_db(data):
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    try:
        with pymysql.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (data, 'Another Value'))
                connection.commit()
        print("Data saved to database.")
    except pymysql.MySQLError as e:
        print("Database error:", e)


if __name__ == '__main__':
    try:
        user_input = get_user_input()
        data = get_data()
        if data:
            save_to_db(data)
        send_email('admin@example.com', 'User Input', user_input)
    except Exception as e:
        print("Unexpected error:", e)
        # End of script
