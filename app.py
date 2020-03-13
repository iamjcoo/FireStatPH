
from flask import Flask, render_template, json, jsonify
import csv
import json
import re
import random

app = Flask(__name__)
counter=0;
data = 'BFP_FIreIncidents2012-2016.csv'
rlist=[]
lyear=[]
year=dict()
hey=dict()

labels = ['PSGC','REGION','PROVINCE_FIRE_DISTRICT','CONGRESSIONAL_DISTRICT','CITY_MUNICIPALITY','YEAR','INCIDENTS','INJURIES','DEATHS','ESTIMATED_DAMAGES']
with open(data, 'r') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=labels)
    for row in reader:
        rlist.append(row)
for x in rlist:
    if x['YEAR'] not in lyear:
        lyear.append(x['YEAR'])
    else:
        continue

@app.route("/")
def index():
    return render_template('dashboard.html')

@app.route("/quickstart")
def quickstart():
    return render_template('quickstart.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/cm/<int:ryear>/")
def cm(ryear):
    return render_template('cm.html', ryear=ryear)

@app.route("/heatmap/<int:ryear>/")
def hmap(ryear):
    for x in rlist:
        if x['YEAR'] == ryear:
            continue
    return render_template('top10.html', ryear=ryear)

@app.route("/hdata/<int:ryear>/")
def hdata(ryear):
    hdata=[]
    htemp=[]
    keys = ['name', 'firei', 'injuries', 'deaths', 'damages']
    for x in rlist:
        if int(x['YEAR']) == int(ryear):
            htemp=[]
            htemp.append(x['CITY_MUNICIPALITY'])
            htemp.append(x['INCIDENTS'])
            htemp.append(x['INJURIES'])
            htemp.append(x['DEATHS'])
            htemp.append(x['ESTIMATED_DAMAGES'])
            hdata.append(dict(zip(keys, htemp)))
    return jsonify(hdata)

@app.route("/cmby")
def cmby():
    years = dict()
    for x in rlist:
        if x['YEAR'] not in years:
            years[x['YEAR']]=int(x['INCIDENTS'])
        else:
            years[x['YEAR']]=int(years[x['YEAR']]) + int(x['INCIDENTS'])
    return render_template('cmby.html', years=years)

@app.route("/heatmap")
def heatmap():
    years = dict()
    for x in rlist:
        if x['YEAR'] not in years:
            years[x['YEAR']]=int(x['INCIDENTS'])
        else:
            years[x['YEAR']]=int(years[x['YEAR']]) + int(x['INCIDENTS'])
    return render_template('topten.html', years=years)

@app.route("/byyear")
def byyear():
    year.clear()
    for x in rlist:
        if x['YEAR'] not in year:
            year[x['YEAR']]=int(x['INCIDENTS'])
        else:
            year[x['YEAR']]=int(year[x['YEAR']]) + int(x['INCIDENTS'])
    return jsonify(year)

@app.route("/byisland/<int:year>")
def byisland(year):
    luzonreg = ['1', '2', '3', '4A', '4B', '5', 'CAR']
    visreg = ['6', '7', '8']
    minreg = ['9', '10', '11', '12', '13', 'ARMM', 'CARAGA']
    isl = dict()
    isl['Luzon']=0
    isl['Visayas']=0
    isl['Mindanao']=0
    isl['NCR']=0
    for x in rlist:
        if x['REGION'] in luzonreg and int(x['YEAR'])==year:
            isl['Luzon']=isl['Luzon']+int(x['INCIDENTS'])
        elif x['REGION'] in visreg and int(x['YEAR'])==year:
            isl['Visayas']=isl['Visayas']+int(x['INCIDENTS'])
        elif x['REGION'] in minreg and int(x['YEAR'])==year:
            isl['Mindanao']=isl['Mindanao']+int(x['INCIDENTS'])
        elif x['REGION'] == "NCR" and int(x['YEAR'])==year:
            isl['NCR']=isl['NCR']+int(x['INCIDENTS'])
        else:
            continue
    return jsonify(isl)

@app.route("/getJSONe/<int:ryear>/")
def getJSONe(ryear):
    inc=0
    inj=0
    data=[]
    cm=""
    deaths=""
    edamage=""
    with open('ph-MC.json', 'r') as f:
        data = json.load(f)
    for i in range(len(data['features'])):
        cm=re.sub("[\(\[].*?[\)\]]", "", data['features'][i]['properties']['name']).strip()
        if data['features'][i]['properties']['ENGTYPE_2'] == "City":
            if "city" not in cm.lower():
                cm = cm + " City"
            else:
                cm = cm
        else:
            print("")
        prov=""
        for x in rlist:
            if data['features'][i]['properties']['REGION']=="Metropolitan Manila":
                prov="NCR"
                prov2=x['REGION']
            elif x['PROVINCE_FIRE_DISTRICT'] == "COTABATO (NORTH COTABATO)":
                prov = data['features'][i]['properties']['PROVINCE']
                prov2 = "NORTH COTABATO"
            elif x['PROVINCE_FIRE_DISTRICT'] == "SAMAR (WESTERN SAMAR)":
                prov = data['features'][i]['properties']['PROVINCE']
                prov2 = "SAMAR"
            else:
                prov = data['features'][i]['properties']['PROVINCE']
                prov2 = x['PROVINCE_FIRE_DISTRICT']

            if int(x['YEAR'])==int(ryear) and re.sub("[\(\[].*?[\)\]]", "", x['CITY_MUNICIPALITY']).lower().strip()==re.sub("[\(\[].*?[\)\]]", "", cm).lower().strip() and prov.lower()==prov2.lower():
                inc=int(x['INCIDENTS'])
                inj=int(x['INJURIES'])
                deaths=int(x['DEATHS'])
                edamage=x['ESTIMATED_DAMAGES']
                break
            else:
                inc= "No Data"
        data['features'][i]['properties']['firei']=inc
        data['features'][i]['properties']['injuries']=inj
        data['features'][i]['properties']['deaths']=deaths
        data['features'][i]['properties']['edamage']=edamage
        if inc == "No Data":
            hey[cm] = prov
    return jsonify(data)

@app.route("/getIncC/<int:ryear>/<string:name>/")
def getIncC(ryear, name):
    for x in rlist:
        inc=dict()
        if int(x['YEAR']) == int(ryear) and x['CITY_MUNICIPALITY'].lower()==name.lower():
            inc[name]=int(x['INCIDENTS'])
            break
        else:
            inc[name]=int(0)

    return jsonify(inc)

@app.route("/injbyyear")
def injbyyear():
    year.clear()
    for x in rlist:
        if x['YEAR'] not in year:
            year[x['YEAR']]=int(x['INJURIES'])
        else:
            year[x['YEAR']]=int(year[x['YEAR']]) + int(x['INJURIES'])
    return jsonify(year)

@app.route("/deabyyear")
def deabyyear():
    year.clear()
    for x in rlist:
        if x['YEAR'] not in year:
            year[x['YEAR']]=int(x['DEATHS'])
        else:
            year[x['YEAR']]=int(year[x['YEAR']]) + int(x['DEATHS'])
    return jsonify(year)

@app.route("/gprate")
def gprate():
    fitemp=[]
    grrate=[]
    for x in lyear:
        cfi=0
        for y in rlist:
            if y['YEAR'] == x:
                cfi=cfi+int(y['INCIDENTS'])
        fitemp.append(cfi)
    for y in range(len(lyear)):
        cgrate=0
        cgrate = ((fitemp[y] - fitemp[y-1]) * 100.0 / fitemp[y-1])
        grrate.append(round(cgrate, 2))
    return jsonify(grrate)

@app.route("/gyear")
def gyear():
    return jsonify(lyear)

@app.route("/grate")
def grate():
    fitemp=[]
    grrate=[]
    for x in lyear:
        cfi=0
        for y in rlist:
            if y['YEAR'] == x:
                cfi=cfi+int(y['INCIDENTS'])
        fitemp.append(cfi)
    for y in range(len(lyear)):
        cgrate=0
        cgrate = ((fitemp[y] - fitemp[y-1]) * 100.0 / fitemp[y-1])
        grrate.append(cgrate)
    fgrate=sum(grrate[1:len(lyear)]) / len(grrate)
    return jsonify(round(fgrate, 2))

@app.route("/avinj")
def avinj():
    fitemp=[len(lyear)]
    for x in lyear:
        cfi=0
        for y in rlist:
            if y['YEAR'] == x:
                cfi=cfi+int(y['INJURIES'])
        fitemp.append(cfi)
    favinj=sum(fitemp) / len(fitemp)
    return jsonify(int(favinj))

@app.route("/avde")
def avde():
    fitemp=[len(lyear)]
    for x in lyear:
        cfi=0
        for y in rlist:
            if y['YEAR'] == x:
                cfi=cfi+int(y['DEATHS'])
        fitemp.append(cfi)
    fde=sum(fitemp) / len(fitemp)
    return jsonify(int(fde))

@app.route("/avdam")
def avdam():
    fitemp=[len(lyear)]
    for x in lyear:
        cfi=0
        for y in rlist:
            if y['YEAR'] == x:
                cfi=cfi+float(y['ESTIMATED_DAMAGES'])
        fitemp.append(cfi)
    fdam=sum(fitemp) / len(fitemp)
    return jsonify(round(fdam, 2))

@app.route("/fdetails")
def fdetails():
    keys = ['label', 'backgroundColor', 'data']
    dtemp=[]
    ddata=[]
    kdata=[]
    for x in lyear:
        cfi=0
        ci=0
        cd=0
        cad=0
        for y in rlist:
            if y['YEAR'] == x:
                cfi=cfi+int(y['INCIDENTS'])
                ci=ci+int(y['INJURIES'])
                cd=cd+int(y['DEATHS'])
                cad=cad+float(y['ESTIMATED_DAMAGES'])
        cyear=x
        kdata.clear()
        dtemp.clear()
        color=""
        dtemp.append(cfi)
        dtemp.append(ci)
        dtemp.append(cd)
        dtemp.append(cad)
        kdata.append(cyear)
        color = "rgba(" + str(random.randint(0, 255)) + ", " + str(random.randint(0, 255)) + ", " + str(random.randint(0, 255)) + ", 0.2)"
        kdata.append(color)
        kdata.append(dtemp)
        ddata.append(dict(zip(keys, kdata)))
    return jsonify(ddata)

if __name__ == '__main__':
    app.run(debug=False)
