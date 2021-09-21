import smtplib
from flask import current_app

from email.message import EmailMessage



class EmailSend:
    def sendEmailWithHtml(self, subject, reciever_email, html):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = current_app.config["EMAIL_USERNAME"]
        msg["To"] = reciever_email
        msg.add_alternative(html, subtype="html")
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                try:
                    smtp.login(current_app.config["EMAIL_USERNAME"], current_app.config["EMAIL_PASSWORD"])
                    try:
                        smtp.send_message(msg)
                        return {"code": 200, "message": "SMTP Email sent Successfully : "}, 200
                    except Exception as e:
                        smtp.quit()
                        return {"code": 421, "message": "SMTP Failed to send Email : " + str(e)}, 421
                except Exception as e:
                    smtp.quit()
                    return {"code": 421, "message": "SMTP Email Account Login Failed : " + str(e)}, 421

        except Exception as e:
            print("SMTP Server connection Failed : " + str(e))
            return {"code": 421, "message": "SMTP Server connection Failed : " + str(e)}, 421