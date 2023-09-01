import smtplib
import datetime
from datetime import datetime, date


def send_summary_email(user, password, message):
    smtp_object = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_object.ehlo()
    smtp_object.starttls()

    smtp_object.login(user, password)

    from_address = user
    to_address = user
    subject = f"Interest Summary: {datetime.today()}"

    msg = "Subject: " + subject + "\n\n" + message
    smtp_object.sendmail(from_address, to_address, msg)

    smtp_object.quit()


if __name__ == "__main__":
    subject = f"Interest Summary: {datetime.today()}"
    message = "Test message"
    msg = "Subject: " + subject + "\n\n" + message
    print(msg)
