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

#Define all necessary functions
def get_iMax(df):
    return len([len(item) for item in df["Journal"] if len(item) != 0]) #Num datapoints by looking at journal column

def df_no_str_cols(df):
    df_clean = df.copy()
    try:
        del df_clean["Day"]
        del df_clean["Date"]
        del df_clean["Journal"]
        return df_clean
    except:
        return df_clean

def get_xlabels(df):
    xlabels =[]
    vecka = 21
    for i in range(get_iMax(df)):
        if df["Day"][i] == "måndag":
            xlabels.append(df["Date"][i] + "\n Mån v: " + str(vecka))
            vecka += 1
    return xlabels

def create_data_plot(df, column, attatchment_path, show=True):
    #Background cmap definined manually 
    cmap = LinearSegmentedColormap.from_list('krg',["#008702","#7fe393", "#f4f4f4","#F6BCB6", "#B23131"], N=256)
    #Plot and save the graphs
    iMax = get_iMax(df)
    aspect = iMax/14
    iMin = iMax - len(df[column].dropna())
    fig, line = plt.subplots(figsize=(8.8,5), sharex=True, sharey=True)
    line.imshow([[0,0],[1,1]], cmap=cmap, interpolation='bicubic', extent=[0,iMax,0.7,5.3], aspect=aspect)

    #x_values = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in df["Date"][:iMax]]
    x_values = df["Date"][:iMax]
    y_values1 = gaussian_filter1d(df[column][:iMax], sigma=1.7)
    y_values2 = gaussian_filter1d(df[column][:iMax], sigma=1)
    y_values3 = df[column][:iMax]

    linestyle = "-"
    linecolor = "black"

    line.plot_date(x_values, y_values2, linewidth="1", color="gray", linestyle=linestyle, marker=None)
    line.plot_date(x_values, y_values3, linewidth="0.5", color="lightgray", linestyle=linestyle, marker=None)
    line.plot_date(x_values, y_values1, linewidth="3", color=linecolor, linestyle=linestyle, marker=None)

    line.plot_date(x_values, df[column][:iMax], "kx", color="#494949" ,label=column)
    line.set_ylim(0.7, 5.3)
    
    xlabels = get_xlabels(df)
    line.set_xticks([df["Date"][i] for i in range(iMax) if df["Day"][i] == "måndag"])
    line.set_xticks([df["Date"][i] for i in range(iMax) if df["Day"][i] != "måndag"], minor=True)
    line.set_xticklabels(xlabels, rotation=90)
    line.set_yticks([1,2,3,4,5])
    line.tick_params(axis='y', which='major', labelsize=10)

    line.grid(axis = "y", linestyle="-", color="darkgray")    
    line.legend()
    line.set_title(column) 
    fig.tight_layout()
    plt.savefig(attatchment_path+str(column)+"_plot", facecolor="#f4f4f4", transparent=True, pad_inches=6, dpi=300)
    if show: 
        plt.show()
    else: 
        plt.clf()

def create_all_data_plots(df, attatchment_path, show=False):
    for column in df_no_str_cols(df):
        create_data_plot(df, column, attatchment_path, show)

def int_columns(df):
    for column in df.columns:
        if column not in ['Day', 'Date', 'Journal']:
            df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

def remove_string_columns(df):
    df_clean = df.copy()
    try:
        del df_clean["Day"]
        del df_clean["Date"]
        del df_clean["Journal"]
        return df_clean
    except:
        return df_clean

def rank_columns_std_plot(df, attatchment_path, show=False):
    fig, line = plt.subplots(figsize=(8.8,6), sharex=True, sharey=True)
    line.bar(remove_string_columns(df).columns, df[0:get_iMax(df)].std(), label = "Standard Deviation")
    line.grid(axis = "y", linestyle="-", color="darkgray")
    line.legend()
    line.set_ylim(0, 2)
    line.tick_params(axis='x', labelrotation=90)
    line.set_facecolor("#F4F4F4")
    fig.set_facecolor("white")
    fig.tight_layout()
    line.set_title("Standard deviations") 
    fig.savefig(attatchment_path+"z_std"+"_plot", facecolor="#f4f4f4", transparent=True, pad_inches=6, dpi=300)

    if show: 
        plt.show()
    else: 
        plt.clf()

def rank_columns_mean_plot(df, attatchment_path, show=False):
    fig, line = plt.subplots(figsize=(8.8,6), sharex=True, sharey=True)
    line.bar(remove_string_columns(df).columns, df[0:get_iMax(df)].mean(), label = "Mean", color="green")
    line.grid(axis = "y", linestyle="-", color="darkgray")
    line.legend()
    line.set_ylim(0.7, 5.3)
    line.tick_params(axis='x', labelrotation=90)
    line.set_facecolor("#F4F4F4")
    fig.set_facecolor("white")
    fig.tight_layout()
    line.set_title("Means") 
    fig.savefig(attatchment_path+"z_means"+"_plot", facecolor="#f4f4f4", transparent=True, pad_inches=6, dpi=300)
    
    if show: 
        plt.show()
    else: 
        plt.clf()

def rank_columns_correlation_plot(df, attatchment_path, show=False):
    c = df[0:get_iMax(df)].corr().abs()
    s = c.unstack()
    so = s.sort_values(kind="quicksort")
    so = so.drop_duplicates()[:-1]
    x = [so.index[i][0] + ", " + so.index[i][1] for i in range(len(so.index))]
    fig, line = plt.subplots(figsize=(50,10), sharex=True, sharey=True)
    line.bar(x, so, label = "Correlations", color="lightblue", edgecolor="black")
    for i, v in enumerate(so):
        line.text(i-0.3, v+0.03, "- "+  str(round(v,4)), fontweight="bold", color='black', rotation=90)
    line.grid(axis = "y", linestyle="-", color="darkgray")
    line.set_aspect("auto")
    line.legend(loc="upper left", markerscale="4")
    line.set_ylim(0, 1)
    line.tick_params(axis='x', labelrotation=90)
    line.set_facecolor("#F4F4F4")
    fig.set_facecolor("white")
    line.set_title("Correlations") 
    fig.tight_layout()
    fig.savefig(attatchment_path+"z_correlations"+"_plot", facecolor="#f4f4f4", transparent=True, pad_inches=6, dpi=300)

    if show: 
        plt.show()
    else: 
        plt.clf()

show = False
create_all_data_plots(df, attatchment_path, show=show)
rank_columns_correlation_plot(df, attatchment_path, show=show)
rank_columns_mean_plot(df, attatchment_path, show=show)
rank_columns_std_plot(df, attatchment_path, show=show)

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
    server.sendmail(bot_mail, receiver_email, message.as_string())

print("Sent.")