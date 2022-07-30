import imaplib
import email
import json
from flask import Flask, jsonify, request
from multiprocessing import connection
import smtplib

import requests

username= "austinjb32@yahoo.com"
password="nzowibezaixphxze"
host='imap.mail.yahoo.com'
to='austinjb32@gmail.com'



app= Flask(__name__)
print(app);


def get_inbox():
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("inbox")
    _, search_data = mail.search(None, 'ALL')
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        # print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            # print("{}: {}".format(header, email_message[header]))
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data['html_body'] = html_body.decode()
        my_message.append(email_data)
    return my_message


# if __name__ == "__main__":
#     my_inbox = get_inbox()
#     print(my_inbox)
# print(search_data)
# ///////////////////////////////////////////////////////////////////////////////////////



















# ///////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/returnjson', methods = ['GET'])
def ReturnJSON():
    if(request.method == 'GET'):
        my_inbox = get_inbox()
        data = my_inbox
        return jsonify(data)

@app.route('/compose',methods = ['POST'])
def login():
   if request.method == 'POST':
      to_address= request.form.get('to')
      subject=request.form.get('subject')
      body=request.form.get('body')
      connection=smtplib.SMTP("smtp.mail.yahoo.com")
      connection.starttls()
      connection.login(user=username,password=password)
      connection.sendmail(from_addr=username, to_addrs={to_address} ,msg=f"Subject:{subject} \n\n{body}")
      connection.close()
      return jsonify(response={"success": "Your data was a success."})
   
  
