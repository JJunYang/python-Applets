import poplib
from email.parser import Parser
from email.header import decode_header


def connect_email():
    user = ''
    password = ''
    host = ''

    server = poplib.POP3(host)
    server.set_debuglevel(1)
    print(server.getwelcome().decode('utf-8'))

    server.user(user)
    server.pass_(password)
    return server


def get_email_content(server):
    email_num, email_size = server.stat()
    rsp, msglines, mgsiz = server.retr(email_num)
    msg_content = b'\r\n'.join(msglines).decode('gbk')
    msg = Parser().parsestr(msg_content)
    server.close()
    return msg


def parser_subject(msg):
    subject = msg['Subject']
    value, charset = decode_header(subject)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    charset = msg.get_charset()
    if not charset:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos+8:].strip()
    return charset


def parser_content(msg, indent=0):
    if msg.is_multipart():
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print(f"{'    'indent*4} part {n+1}")
            print(f"{'    'indent*4}{'-'*50}")
            parser_content(part, indent+1)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
                print(f"{'    'indent*4} content is :{content}")
        else:
            print(f"{'    'indent}*4 touch content is :{content_type}")


def main():
    server = connect_email()
    msg = get_email_content(server)
    print(msg)


main()
