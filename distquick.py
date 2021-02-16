#!/usr/bin/env python3

import pyperclip
import plotly.express as px
import numpy as np

import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
root.withdraw()

##########################################################
#  TO DO
#
# - add sigma value to graph
##########################################################

def main():
    # get data from clipboard
    data = pyperclip.paste()

    #form data into a list of individual values
    data = data.split('\n')

    #removes non-numeric values in dataset
    data = [float(i) for i in data if checkNum(i)]

    #print(data)


    # prompt user for lsl
    lsl = float(simpledialog.askstring(title="Data Entry",
        prompt="What is the LSL of the data:"))

    # if nothing is entered, change lsl to 0.  Lets calculations run without exceptions
    if lsl == '':
        lsl = 0

    # prompt user for usl
    usl = float(simpledialog.askstring(title="Data Entry",
        prompt="What is the USL of the data:"))

    # if nothing is entered, change usl to 0.  Lets calculations run without exceptions
    if usl == '':
        usl = 0

    #print cp and cpk
    print("\ncp: {}".format(cp(data,lsl,usl)))
    print("cpk: {}".format(cpk(data,lsl,usl)))

    #make figure
    fig = px.histogram(data,
                            marginal = 'box')

    # if real lsl and usl vales are entered --> show them as lines on graph
    if (usl != 0) and (lsl != 0):
        fig.add_shape(type = 'line',
                xref = 'x', yref = 'paper',
                x0 = lsl, y0 = 0, x1 = lsl, y1 = 1,
                line = dict(
                    color = 'DarkOrange',
                    width = 3,
                    )
            )
        fig.add_shape(type = 'line',
                xref = 'x', yref = 'paper',
                x0 = usl, y0 = 0, x1 = usl, y1 = 1,
                line = dict(
                    color = 'DarkOrange',
                    width = 3,
                    )
            )

        fig.add_annotation(
            xref = 'paper', yref = 'paper',
            x = 1.06 , y = 0.6,
            text = "cp = {}".format(cp(data,lsl,usl)),
            showarrow = False,
            )

        fig.add_annotation(
            xref = 'paper', yref = 'paper',
            x = 1.06 , y = 0.5,
            text = "cp = {}".format(cpk(data,lsl,usl)),
            showarrow = False,
            )

    fig.show()


#calculate cp
def cp(data,lsl,usl):
    arr = np.array(data).astype(np.float)
    arr = arr.ravel()
    sigma = np.std(arr)
    cp = float(usl - lsl) / (6*sigma)
    cp = round(cp,3)
    return(cp)

#calculat cpk
def cpk(data,lsl,usl):
    arr = np.array(data).astype(np.float)
    sigma = np.std(arr)
    m = np.mean(arr)

    cpu = float(usl - m) / (3*sigma)
    cpl = float(m - lsl) / (3*sigma)
    cpk = np.min([cpu , cpl])
    cpk = round(cpk,3)
    return(cpk)


#Fuction that checks if passed item is a number. Returns True if item is a numeric value
def checkNum(item):
    try:
        float(item)
        return True
    except Exception:
        return False



if __name__== "__main__":
    main()
