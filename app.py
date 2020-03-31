from flask import Flask, render_template, request
import csv
import os
import json
import pandas as pd 
import numpy as np
from datetime import datetime
import math
import uuid 
   
app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template("file_split.html")

@app.route("/merge", methods=['GET'])
def merge():
    return render_template("file_merge.html")

@app.route("/split_processing", methods=['GET', 'POST'])
def split_processing():
    if request.method == "POST":
        csv_file = request.files['file']
        df = pd.read_csv(csv_file)
        header_rows = int(request.form['header'])
        skip = int(request.form['skip'])
        if request.form['lines'] == '':
            pass
        else:
            size = int(request.form['lines'])
        files = request.form['files']

        if files:
            files = int(files)
            size = math.ceil(len(df)/files)
        list_of_dfs = [df.loc[i:i+size-1,:] for i in range(0, len(df),size)]
        folder = os.path.join(os.getcwd(), 'static')

        filenames = []

        if header_rows == 1:
            for i, df in enumerate(list_of_dfs):
                id = uuid.uuid1()
                filename = os.path.join('static', 'split_{}.csv'.format(id))
                filename_path = os.path.join(folder, "split_{}.csv".format(id))
                filenames.append(filename)
                df.to_csv(filename_path, header=True, index=None)
        else:
            header = df.iloc[0:header_rows-1]
            for i, df in enumerate(list_of_dfs):
                data = header.append(df, ignore_index=True)
                id = uuid.uuid1()
                filename = os.path.join('static', 'split_{}.csv'.format(id))
                filename_path = os.path.join(folder, "split_{}.csv".format(id))
                filenames.append(filename)
                data.to_csv(filename_path, header=True, index=None)
        print(filenames)
    return render_template("output.html", filenames=filenames)

@app.route("/merge_processing", methods=['GET', 'POST'])
def merge_processing():
    if request.method == "POST":
        csv_files = request.files
        print(csv_files)
        df_list = []
        folder = os.path.join(os.getcwd(), 'static')
        for file in csv_files.values():
            df_list.append(pd.read_csv(file))
        
        length = len(df_list[0].columns)

        for df in df_list:
            if len(df.columns) != length:
                return render_template("output.html", filenames=[], message="Formats Mismatched.")
            else:
                pass

        new_df = pd.concat(df_list)

        # data = header.append(df, ignore_index=True)
        filenames = []
        id = uuid.uuid1()
        filename = os.path.join('static', 'merged_{}.csv'.format(id))
        filename_path = os.path.join(folder, "merged_{}.csv".format(id))
        filenames.append(filename)
        new_df.to_csv(filename_path, header=True, index=None)

    return render_template("output.html", filenames=filenames)

if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug=True)