import json
import logging
import smtplib
import warnings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configparser import ConfigParser
from datetime import datetime
from itertools import cycle

# Buffer of tasks to be assigned on a weekly rotating basis
warnings.warn(
    "Assign your tasks here. If tasks > 10, consider importing from a file instead.",
    Warning,
)
tasks_buffer = cycle([
    "Task# 1",
    "Task# 2",
    "Task# 3",
    "Task# 4",
])

# Set up .log file
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[logging.FileHandler("task_reminder.log"), logging.StreamHandler()],
)

# Configure logging and load configuration
logging.basicConfig(level=logging.INFO)
config = ConfigParser()
config.read("config.ini")

# Load email credentials and start date from configuration
try:
    sender_email = config["EMAIL"]["SENDER_EMAIL"]
    sender_passwd = config["EMAIL"]["SENDER_PASSWORD"]
    smtp_server = config["EMAIL"]["SMTP_SERVER"]
    smtp_port = int(config["EMAIL"]["SMTP_PORT"])
    templates = config["TEMPLATES"]
    start_date = datetime.strptime(config["DATE"]["START_DATE"], "%Y-%m-%d")
except KeyError as e:
    logging.error(f"Missing configuration key: {e}")
    raise


# Load user information from JSON file
# User : {email, initial position in task buffer} e.g {"John":[john@domain.com, 0]}
try:
    with open("users.json", "r") as file:
        user_info = json.load(file)
except json.JSONDecodeError as e:
    logging.error(f"Error decoding user information: {e}")
    raise


def week_calc(today: datetime, start: datetime) -> int:
    """Calculate the number of weeks since the start date."""
    delta_days = (today - start).days
    if delta_days < 0:
        raise ValueError("Start date should not be in the future relative to today.")
    delta_weeks = delta_days // 7
    return delta_weeks


def assign_task(user: str, info: dict, tasks: cycle, weeks: int) -> tuple[str, str]:
    """Assign a task to a user based on the current week."""
    for _ in range(weeks):
        next(tasks)
    task = next(tasks)
    return info[user][0], task


def format_email(user: str, task: str, today: datetime) -> str:
    """Format the email content using an HTML template."""

    # Uses the notification template on Monday and uses the reminder the other days
    if today.isoweekday() == 1:
        template = templates["NOTIFICATION"]
    else:
        template = templates["REMINDER"]

    with open(template, "r") as file:
        html_content = file.read()
        html_content = html_content.replace("{{name}}", user)
        html_content = html_content.replace("{{task}}", task)
    return html_content


def send_email(email: str, html_content: str) -> bool:
    """Send an email with the given HTML content."""
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = "Your Weekly Task Reminder"

    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_passwd)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        logging.error(e)
        return False


def main():

    today = datetime.today()
    weeks = week_calc(today, start_date)

    for user in user_info:
        email, task = assign_task(user, user_info, tasks_buffer, weeks)
        html_content = format_email(user, task, today)
        success = send_email(email, html_content)
        if success:
            logging.info(f"Email sent to {user} with task: {task}")
        else:
            logging.error(f"Failed to send email to {user}")


if __name__ == "__main__":
    main()
