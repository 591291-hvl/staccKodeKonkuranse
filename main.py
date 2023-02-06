from flask import Flask, render_template, request, jsonify
import json
import matplotlib.pyplot as plt
import base64
import pandas as pd


with open("data/consumption.json", "r") as json_file:
    my_dict = json.load(json_file)


def getDict():
    return my_dict


def setDict(newDict):
    global my_dict
    my_dict = newDict


spotPrisDF = pd.read_excel('data/spotpriser.xlsx')


def getSpotPrisDF():
    return spotPrisDF


def setSpotPrisDF(newDF):
    global spotPrisDF
    spotPrisDF = newDF


app = Flask(__name__)


# ===========================
# FUNCTIONS

def average(jsonList):
    return sum([d['consumption'] for d in jsonList])/len(jsonList)


def fastPris(pris, jsonList):
    pris = float(pris.replace(",", "."))
    return sum([d['consumption']*pris for d in jsonList])


def spotPris(dataframe, dictonary):
    dataframe = dataframe.assign(
        consumption=[d['consumption'] for d in dictonary])
    return (dataframe['NO1'] * dataframe['consumption']).sum()


def plot(n):
    plt.figure(figsize=(8, 6))
    plt.plot(range(len(my_dict)), [d['consumption'] for d in my_dict])
    plt.xlabel("Hours")
    plt.ylabel("kWh")

    plt.plot(range(len(my_dict)), [int(n)] *
             len(my_dict), 'r', label="Average")
    plt.legend()
    plt.savefig("plot.png")


def dualPlot(n, dictionary, dataframe, radio):
    plt.figure(figsize=(8, 6))
    plt.plot(range(len(dictionary)), [d['consumption']
             for d in dictionary], label="Forbruk")
    plt.xlabel("Hours")
    plt.ylabel("kWh")

    plt.plot(range(len(my_dict)), [int(n)] *
             len(my_dict), 'r', label="Average")

    plt.plot(range(dataframe[radio].size), dataframe[radio], label="Spotpris")
    plt.legend()
    plt.savefig("plot.png")


def removeTimeDF(dataframe):  # removes non date value
    dataframe['Dato/klokkeslett'] = dataframe['Dato/klokkeslett'].str[0:10]
    return dataframe


def spotPrisKorting(dataframe, dictonary):  # clips spotpris to fit usage
    dataframe = removeTimeDF(dataframe)
    indexes = dataframe[dataframe['Dato/klokkeslett']
                        == dictonary[0]['from'][0:10]].index.values
    newDataframe = dataframe.iloc[indexes[0]:indexes[0]+len(dictonary)]
    return newDataframe


# =====================
# ROUTINGS

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/createPlot', methods=['POST'])
def get_Img():
    print("plot")
    spotPrisDF = spotPrisKorting(getSpotPrisDF(), getDict())
    dualPlot(average(getDict()), getDict(), spotPrisDF, request.json['radio'])
    base = base64.encodebytes(open("plot.png", "rb").read())
    return base


@app.route('/sendFile', methods=['POST'])
def get_file():
    print("file")
    try:
        file = request.files['file']
    except:
        file = open("data/consumption.json", "r")

    setDict(json.load(file))
    return "TEST"


@app.route('/fastPris', methods=['POST'])
def get_fastPris():
    print("price")
    sumVal = round(fastPris(request.json['value'], getDict()), 2)
    averageVal = round(average(getDict()), 2)
    spotVal = round(spotPris(spotPrisKorting(
        getSpotPrisDF(), getDict()), getDict()), 2)
    return str(sumVal) + "_" + str(averageVal) + "_" + str(spotVal)


if __name__ == '__main__':
    app.debug = True
    app.run()  # go to http://127.0.0.1:5000/ to view the page.
