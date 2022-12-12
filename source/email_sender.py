"""
The original plan was to have the musical notation sent via the email
but somehow, the SMTP is blocked in the campus network and we never 
get it work
"""
import smtplib
import email.mime.multipart
import email.message
import os

from logger import log_info

_SUBJECT = "Your Music Notation"
_SENDER = "Music Notation"
_CONTENT = "Please see attached your music notation\n"

def create_email_object(to_address, appendage_path):
    msg=email.message.EmailMessage()
    msg['subject']=_SUBJECT
    msg['from']=_SENDER+'<noreply>'
    msg['to']=to_address
    msg['date'] = email.utils.formatdate(None,True,True)
    msg['Content-Type'] = 'text/html'
    msg.set_payload(_CONTENT,charset='utf8')

    subfile=email.mime.multipart.MIMEMultipart()
    subfile['Content-Type']='multipart/related'

    data=open(appendage_path,'rb')
    filetype=appendage_path.split('.')[-1]
    datafile=email.mime.multipart.MIMEBase(filetype,filetype)
    datafile.set_payload(data.read())
    data.close()

    email.encoders.encode_base64(datafile)
    basename=os.path.basename(appendage_path)
    datafile.add_header('Content-Disposition','attachment', filename = basename)
    subfile.attach(datafile)

    fullmessage=email.mime.multipart.MIMEMultipart()
    fullmessage['subject'] = msg['subject']
    fullmessage['from'] = msg['from']
    fullmessage['date'] = email.utils.formatdate(None,True,True)
    fullmessage['Content-Type']='multipart/mixed'
    fullmessage.attach(msg)
    fullmessage.attach(subfile)
    return fullmessage

def send_email_object_SMTP(from_address, password, to_address, email_object):
    mail_host='smtp.mail'+from_address.split('@')[-1]

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(from_address, password)
        print("Log-in")
        smtpObj.sendmail(from_address, to_address, email_object.as_string())
        smtpObj.close()
        log_info("Send an email to %s" % (to_address))
    except:
        log_info("Failed to send an email to %s"%(to_address))
        

if __name__ =='__main__':
    from_address = "qshan.yuezhao@yahoo.com"
    password = "yz2697hl2425"
    to_address = "lihaoyangjingzhou@outlook.com"
    appendage_path = "melody_0.svg"
    email_object = create_email_object(to_address, appendage_path)
    send_email_object_SMTP(from_address, password, to_address, email_object)
