import imaplib
import email
import os


def import_statements_from_email(user, password):
    M = imaplib.IMAP4_SSL("imap.gmail.com")

    M.login(user, password)

    M.select('"Home/Statements"')
    typ, data = M.search(None, "(UNSEEN)")

    for num in data[0].split():
        typ, data = M.fetch(num, "(RFC822)")
        raw_email = data[0][1]

        raw_email_string = raw_email.decode("utf-8")
        email_message = email.message_from_string(raw_email_string)

        for part in email_message.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition") is None:
                continue
            filename = part.get_filename()
            if bool(filename):
                filepath = os.path.join("./statements/", filename)
                if not os.path.isfile(filepath):
                    fp = open(filepath, "wb")
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                    subject = (
                        str(email_message)
                        .split("Subject: ", 1)[1]
                        .split("\nMIME", 1)[0]
                    )
                    print(f'Downloaded "{filename}" from email titled "{subject}".')

    M.logout()
