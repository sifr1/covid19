# https://raw.githubusercontent.com/BlankerL/DXY-COVID-19-Data/master/json/DXYArea.json
from flask import Flask, render_template,jsonify,Response
from flask_cors import CORS
import requests
import json
import math
import pandas as pd
from pandas.io.json import json_normalize   
import urllib3


app = Flask(__name__)
CORS(app)

# this file has countries coordinates.
with open('countries.json') as f:
    data = json.load(f)

# settings for debugging purpose.
# pd.set_option('display.max_rows', None)
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

 
def getdata():

    try:
        # raw data in github.
        r = requests.get('https://raw.githubusercontent.com/BlankerL/DXY-COVID-19-Data/master/json/DXYArea.json', verify=False)
        r.raise_for_status()
        cases_data = json.loads(r.text)
        # converting data to pandas dataframe
        df_all = json_normalize(cases_data,'results', errors='ignore')
        
        # select some columns.
        df_selected = df_all[['countryEnglishName','confirmedCount','curedCount','deadCount']]
        
        # grouping data by name, because there are more than one node for some countries like china.
        df_grouped = df_selected.groupby(['countryEnglishName'], as_index=False)[["confirmedCount", "curedCount", "deadCount"]].sum()

        # adding necessary data for WebGL globe.
        df_grouped.insert(4, 'lat', 0)
        df_grouped.insert(5, 'lng', 0)
        df_grouped.insert(6, 'name',"0")
        df_grouped.insert(6, 'size',0)
        df_grouped.insert(7, 'color', '&red&')

        for index, row in df_grouped.iterrows():
            for i in data:
                if i['name'] == str(row[0]):
                        df_grouped.at[index,'lat'] = i['latlng'][0]
                        df_grouped.at[index,'lng'] = i['latlng'][1]
                        df_grouped.at[index,'name'] = row[0]
                        df_grouped.at[index,'size'] = row[1]
    
        return df_grouped
    except r.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
    except r.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except r.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except r.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)     
   

    

@app.route('/')
def homepage():
    # data for the table in the right side.
    data_ = getdata()
    data_ = data_.nlargest(50, 'confirmedCount')
    data_ = data_.filter(['countryEnglishName', 'confirmedCount','curedCount','deadCount'])
    final = data_.rename(columns={"countryEnglishName": "Country", "confirmedCount": "Confirmed", "curedCount": "Cured", "deadCount": "Dead"})
    return render_template('covid.html',tables=[final.to_html(classes='datatable',index=False)],border=0, titles="Confirmed Cases")


@app.route('/get_csv_data')
def get_csv_data():
    # preparing data for WebGL globe.
    data_ = getdata()
    final_ = data_.to_csv(index=False)
    return Response(final_)

@app.route('/summary')
def summary():
    # data for the summary in the top left corner.
    data_ = getdata()
    total = data_[["confirmedCount", "curedCount", "deadCount"]].sum()
    return Response(total.to_json())

@app.route('/topten')
def topten():
    # data for the chart.
    data_ = getdata()
    data_ = data_.nlargest(10, 'confirmedCount')
    data_ = data_.filter(['countryEnglishName', 'confirmedCount'])
    data_ = data_.rename(columns={"countryEnglishName": "label", "confirmedCount": "y"})
    final = data_.to_json(orient='records')
    return Response(final)


if __name__ == "__main__":
      app.run(debug=True)