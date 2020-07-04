#RUN FORREST RUN 
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint 
import pandas as pd 
from matplotlib import pyplot as plt
import imapclient
import smtplib, ssl
import email
import numpy as np
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os 
from  matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker as ticker
import time
from scipy.ndimage.filters import gaussian_filter1d
from report_functions import (create_all_data_plots, rank_columns_correlation_plot, rank_columns_mean_plot, \
                         rank_columns_std_plot, create_all_group_plots)

creds_path = 'C:/Users/alexa/Desktop/Important/principles-347f1fb0ab19.json'
attatchment_path = "C:/Users/alexa/Desktop/Learning/Report/attatchments/"
bot_mail = "alwobot7@gmail.com"

#Load in Data from Google Sheets
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
gc = gspread.authorize(creds)
ws = gc.open('Journal (Start 12/5-20)').worksheets()
README = gc.open('Journal (Start 12/5-20)').get_worksheet(0)
j2020 = gc.open('Journal (Start 12/5-20)').get_worksheet(1)

#Set data from Sheet in DataFrame
df = pd.DataFrame(j2020.get_all_records())

#Turn numeric data in DF into floats (from str)
for column in df.columns:
    if column not in ['Day', 'Date', 'Journal']:
        df[column] = pd.to_numeric(df[column], errors='coerce')


groups={"Development":["Discipline", "Productivity", "Creativity", "Insight", "Motivation"], \
        "Health":["Sleep", "Training&Strech", "Diet", "Physique"], \
        "Happiness":["Harmony", "Social", "ER", "Experience"]}

show = False
send_mail = True

#Call functions 
create_all_data_plots(df, attatchment_path, show=show)
rank_columns_correlation_plot(df, attatchment_path, show=show)
rank_columns_mean_plot(df, attatchment_path, show=show)
rank_columns_std_plot(df, attatchment_path, show=show)
create_all_group_plots(df, attatchment_path, groups, show=show)

#--------------------------------------------------------------------------------------------------------------------------------------------
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
    if send_mail == True:
        server.sendmail(bot_mail, receiver_email, message.as_string())
        print("Sent.")
    else: print("Done.")