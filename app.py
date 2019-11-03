from flask import Flask,request,render_template,flash,redirect,url_for
import base64
import pyqrcode
from pyqrcode import QRCode
import smtplib
import imghdr
import qrcode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders



app = Flask(__name__)
app.secret_key = 'my unobvious secret key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send',methods=['GET','POST'])
def send_ticket():
    res = " "
    if request.method=="POST":
        s = ""+request.form.get('Name',None)+" "+request.form.get('regno',None)
        print(s)
        res = str(base64.b64encode(s))
        print(res)
        name=""+request.form.get('Name',None)+".png"
        img = qrcode.make(res)
        img.save(name)
        reciever = ""+request.form.get('email',None)+" "

#Email details of the sender can be used from environment variables
        email_user = 'emailid'
        email_password = 'password'


        email_send = reciever

        subject = 'Your EVENT TICKET'

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        body = 'Add Body'
        msg.attach(MIMEText(body,'plain'))

        filename =  name
        attachment  =open(filename,'rb')

  # Encode the details of the ticket
        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= "+filename)

#Build the email to send
        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email_user,email_password)


        server.sendmail(email_user,email_send,text)
        server.quit()


    return render_template('index.html')


if __name__ == '__main__':
	sess.init_app(app)
	app.debug = True
	app.run(host = '0.0.0.0',port =5000)
