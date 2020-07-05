#RUN FORREST RUN 
import smtplib, ssl, email, imapclient, os, time, csv, gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd 
from matplotlib import pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from report_functions import (get_journal_df, create_all_data_plots, rank_columns_correlation_plot, rank_columns_mean_plot, \
                         rank_columns_std_plot, create_all_group_plots)

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

user = "user1"
with open('C:/Users/alexa/Desktop/Important/config_' + user + ".csv", newline='') as f:
    config_data = [config_data_list[0] for config_data_list in csv.reader(f)]
    creds_path, attatchment_path, bot_mail, sheet = config_data

groups={"Development":["Discipline", "Productivity", "Creativity", "Insight", "Motivation"], \
        "Health":["Sleep", "Training&Strech", "Diet", "Physique"], \
        "Happiness":["Harmony", "Social", "ER", "Experience"]}

show = False
send_mail = True

#-----------------------------------------------------------------------------------------------------------
#Call functions 
df = get_journal_df(creds_path, scope, sheet)
create_all_data_plots(df, attatchment_path, show=show)
rank_columns_correlation_plot(df, attatchment_path, show=show)
rank_columns_mean_plot(df, attatchment_path, show=show)
rank_columns_std_plot(df, attatchment_path, show=show)
create_all_group_plots(df, attatchment_path, groups, show=show)

#-----------------------------------------------------------------------------------------------------------
#Email details
password = open("C:/Users/alexa/Desktop/Important/bot_pass.txt").read()
sender_email = bot_mail
receiver_email = open("C:/Users/alexa/Desktop/Important/receiver.txt").read()
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Good morning"
message["Bcc"] = receiver_email

#Add attatchments to Email, based on the attachments folder
directory = r"{}".format(attatchment_path)
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):  #Loopa över bilder
        file = attatchment_path + filename
        with open(file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part) #Encode
        part.add_header(  #Detta är vad attatchmentet kommer heta i Emailet. Viktigt för att kunna öppnas
            "Content-Disposition",
            f"attachment; filename= {filename}")
        message.attach(part)

body = "Här är den dagliga statistikrapporten från journalen \n Lycka till idag!"
message.attach(MIMEText(body, "plain"))

#Send email
port = 465
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(bot_mail, password)
    if send_mail:
        server.sendmail(bot_mail, receiver_email, message.as_string())
        print("Sent.")
    else: print("Done.")