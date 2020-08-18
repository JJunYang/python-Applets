import yagmail


def send_email(name, to, filepath):
    contents = '''Hello {name}, success send email with file {filepath}'''

    # from IMAP/SMTP service
    yag = yagmail.SMTP(user='', password='', host='')

    yag.send(to=to, subject='data', contents=contents)
