#RUN FORREST RUN 
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint 
import pandas as pd 
from matplotlib import pyplot as plt
import numpy as np
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

#Get the number of datapoints by looking at Journal entries 
global iMax
iMax = len([len(item) for item in df["Journal"] if len(item) != 0])

#Turn numeric data in DF into floats (from str)
for column in df.columns:
    if column not in ['Day', 'Date', 'Journal']:
        df[column] = pd.to_numeric(df[column], errors='coerce')

#Analysis 
#std = df[0:iMax].std().sort_values()
#mean = df[0:iMax].mean().sort_values()
c = df[0:iMax].corr().abs()
s = c.unstack()
so = s.sort_values(kind="quicksort")
so = so.drop_duplicates()[:-1]

numDict = {}
for number in range(6):
    numDict[number] = 0
    largest = ["category", number]
    for column in remove_string_columns(df):
        a = df.loc[df[column] == number, column].count()
        if a > numDict[number] = a

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

def get_y(column1, column2):
    return (gaussian_filter1d(df[column1][:iMax], sigma=1.7), gaussian_filter1d(df[column2][:iMax], sigma=1.7))

def compare_plot(column1, column2):
    """In: two of: Average, Experience, Harmony, Social, Motivation, Physique, Creativity, ER, Diet, Discipline, Sleep, Productivity, Meditation, Training&Strech
    Out: Graph with both columns """
    
    #Init
    cmap = LinearSegmentedColormap.from_list('krg',["#31B247","#B6F6BE", "#f4f4f4","#F6BCB6", "#B23131"], N=256)
    fig, line = plt.subplots(figsize=(8.8,5), sharex=True, sharey=True)

    line.imshow([[0,0],[1,1]], cmap=cmap, interpolation='bicubic', extent=[0,iMax,0.7,5.3], aspect=iMax/14)

    x_values = df["Date"][:iMax]
    y_values1, y_values2 = get_y(column1, column2)
    #Lines
    line.plot_date(x_values, y_values1, linewidth="2", color="black", linestyle="-", marker=None, label=column1)
    line.plot_date(x_values, y_values2, linewidth="2", color="blue", linestyle="-", marker=None, label=column2)

    line.set_ylim(0.7, 5.3)
    xlabels =[]
    vecka = 21
    for i in range(iMax):
        if df["Day"][i] == "måndag":
            xlabels.append(df["Date"][i] + "\n Mån v: " + str(vecka))
            vecka += 1
    line.set_xticks([df["Date"][i] for i in range(iMax) if df["Day"][i] == "måndag"])
    line.set_xticks([df["Date"][i] for i in range(iMax) if df["Day"][i] != "måndag"], minor=True)
    line.set_xticklabels(xlabels, rotation=90)
    line.set_yticks([1,2,3,4,5])
    line.tick_params(axis='y', which='major', labelsize=10)
    line.grid(axis = "y", linestyle="-", color="darkgray")
    line.legend()
    line.set_title(column1 + " & " + column2) 
    fig.tight_layout()
    fig.savefig(attatchment_path+ "/plotcomp/"+str(column1)+ "_and_" + str(column2) +"_plot", facecolor="#f4f4f4", transparent=True, pad_inches=6, dpi=300)

def rank_columns_std_plot(df):
    fig, line = plt.subplots(figsize=(8.8,5), sharex=True, sharey=True)
    line.bar(remove_string_columns(df).columns, df[0:iMax].std(), label = "Standard Deviation")
    line.grid(axis = "y", linestyle="-", color="darkgray")
    line.legend()
    line.set_ylim(0, 2)
    line.tick_params(axis='x', labelrotation=90)
    line.set_facecolor("#F4F4F4")
    fig.set_facecolor("white")
    fig.show()

def rank_columns_mean_plot(df):
    fig, line = plt.subplots(figsize=(8.8,5), sharex=True, sharey=True)
    line.bar(remove_string_columns(df).columns, df[0:iMax].mean(), label = "Mean", color="green")
    line.grid(axis = "y", linestyle="-", color="darkgray")
    line.legend()
    line.set_ylim(0.7, 5.3)
    line.tick_params(axis='x', labelrotation=90)
    line.set_facecolor("#F4F4F4")
    fig.set_facecolor("white")
    fig.show()

def rank_column_correlation_plot(df):
    c = df[0:iMax].corr().abs()
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
    fig.show()

#rank_column_correlation_plot(df)
#rank_columns_std_plot(df)
#rank_columns_mean_plot(df)
#compare_plot("Creativity", "Harmony")
