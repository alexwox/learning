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

creds_path = 'C:/Users/alexa/Desktop/Important/principles-347f1fb0ab19.json'
attatchment_path = "C:/Users/alexa/Desktop/Report/attatchments/"
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

#Get the number of datapoints by looking at Journal entries 
iMax = len([len(item) for item in df["Journal"] if len(item) != 0])

#Turn numeric data in DF into floats (from str)
for column in df.columns:
    if column not in ['Day', 'Date', 'Journal']:
        df[column] = pd.to_numeric(df[column], errors='coerce')


cmap = LinearSegmentedColormap.from_list('krg',["#31B247","#B6F6BE", "#f4f4f4","#F6BCB6", "#B23131"], N=256)
#cmap = LinearSegmentedColormap.from_list('krg',["#31B247", "#f4f4f4", "#FF0000"], N=256)

#Plot and save the graphs
aspect = iMax/14
for column in df.columns:
    if column not in ['Day', 'Date', 'Journal']:
        plt.figure(figsize=(6,3.4))
        if column == "Average":
            ysmoothed = gaussian_filter1d(df[column][:iMax], sigma=1.7)
            linestyle = "-"
            linecolor = "black"
        else:
            ysmoothed = gaussian_filter1d(df[column][:iMax], sigma=1.7)
            linestyle = "-"
            linecolor = "black"
        plt.rcParams["figure.figsize"] = (6,3.4)
        plt.plot(df["Date"][:iMax], ysmoothed, linewidth="3", color=linecolor, linestyle=linestyle)
        #plot1 = plt.plot_date(df["Date"][:iMax], df[column][:iMax], "k-")
        plt.plot(df["Date"][:iMax], df[column][:iMax], "kx", color="#494949" ,label=column)
        plt.xlim()
        plt.ylim()
        plt.plot()

        plt.imshow([[0,0],[1,1]], cmap=cmap, interpolation='bicubic', extent=[0,iMax,0.7,5.3], aspect=aspect)
        xlabels = [i for i in df["Date"]]
        #yaver = [np.average(df[column][:iMax]) for i in range(len(df[column][:iMax]))]
        plt.gca().set_facecolor("#f4f4f4")
        plt.xticks(df["Date"][:iMax], xlabels, rotation='vertical')
        plt.yticks([1,2,3,4,5])

        plt.tick_params(axis='y', which='major', labelsize=10)
        plt.minorticks_on()
        plt.grid(axis = "y", linestyle="-", color="darkgray")
        plt.legend()
        plt.title(column) 
        plt.tight_layout()
        #plt.set_size_inches(20, 11,dpi=100)
        plt.savefig(attatchment_path+str(column)+"_plot", facecolor="#f4f4f4", transparent=True, pad_inches=6, dpi=300)
        plt.show()
        plt.clf()

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
    #server.sendmail(bot_mail, receiver_email, message.as_string())

print("Sent.")