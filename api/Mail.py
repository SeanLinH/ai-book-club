import smtplib 
from email.mime.text import MIMEText  
import os





def register_welcome(mail):
  MAIL_KEY = os.environ.get("MAIL_KEY")
  print(MAIL_KEY)
  html="""
  <!doctype html>
  <html>
  <head>
    <meta charset='utf-8'>
    <title>感謝註冊智能讀書會 SageLink</title>
  </head>
  <body>
    <b>你已經成功註冊完 SageLink! </b>
  </body>
  </html>
  """

  mime=MIMEText(html, "html", "utf-8") #撰寫內文內容，以及指定格式為plain，語言為中文
  mime["Subject"]="註冊 SageLink 智能讀書會成功" #撰寫郵件標題
  mime["From"]="SageLink 智能讀書會" #撰寫你的暱稱或是信箱
  mime["To"]=mail #撰寫你要寄的人
  # mime["Cc"]="@gmail.com, @gmail.com" #副本收件人
  msg=mime.as_string() #將msg將text轉成str
  smtp=smtplib.SMTP("mail.sentipal.live", 587)  #googl的ping
  smtp.ehlo() #申請身分
  smtp.starttls() #加密文件，避免私密信息被截取
  smtp.login("support@sentipal.live", "bgad56j95m") 
  from_addr="support@sentipal.live"
  to_addr=[mail]
  status=smtp.sendmail(from_addr, to_addr, msg)
  if status=={}:
      print("郵件傳送成功!")
  else:
      print("郵件傳送失敗!")
  smtp.quit()