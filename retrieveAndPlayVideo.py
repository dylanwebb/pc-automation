# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 21:39:02 2019

@author: dylan
"""

# import libraries
import imaplib
import base64
import os
import email
import subprocess

def getVideoFromEmail(email_user, email_password, basePath):
    # connect to inbox of email
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(email_user, email_password)
    mail.select('Inbox')

    # get latest email
    type, data = mail.search(None, 'ALL')
    latest_mail = data[0].split()[-1]
    type, data = mail.fetch(latest_mail, '(RFC822)' )
    raw_email = data[0][1]
    email_message = email.message_from_string(raw_email.decode('utf-8'))

    # download its attachments

    filePath = ""
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join(basePath, fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
    return filePath
        
vlcFilePath = "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"
basePath ='C:\\Users\\dylan\\Desktop'
# play video on loop
subprocess.Popen([vlcFilePath, getVideoFromEmail('','',basePath)])