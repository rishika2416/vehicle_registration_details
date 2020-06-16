from flask import Flask, jsonify, request, Response
from bs4 import BeautifulSoup as Soup
import requests
import json
app = Flask(__name__)


@app.route("/getDetails", methods=["POST"])
def user_detail():
    API_ENDPOINT = 'https://www.regcheck.org.uk/api/reg.asmx/CheckIndia'
    rtoNo = request.form['rtoNo']
    userName = 'salona'
    data = {'RegistrationNumber':rtoNo,
            'username':userName}
    xml = requests.post(url = API_ENDPOINT, data = data)
    soup = Soup(xml.text,'xml')
    vehicleJson = json.loads(soup.find('vehicleJson').text);
    desc = vehicleJson.get('Description')
    year = vehicleJson.get('RegistrationYear')
    make = vehicleJson.get('CarMake').get('CurrentTextValue')
    model = vehicleJson.get('CarModel').get('CurrentTextValue')
    engine = vehicleJson.get('EngineNumber')
    fuel = vehicleJson.get('FuelType').get('CurrentTextValue')
    date = vehicleJson.get('RegistrationDate')
    location = vehicleJson.get('Location')
    print(model)
    htmlTemplate = """<html>
                          <head>
                            <meta charset="utf-8">
                            <title></title>
                          </head>
                          <body  style="font-family:Verdana;">
                            <form class="vehicle">
                              <b>Vehicle Description</b><br>
                              <textarea name="description" rows="3" cols="60">%s</textarea>
                              <hr style="height:2px">
                              <b>Registration Year</b><br>
                              <textarea name="year" rows="3" cols="60">%s</textarea>
                                <hr style="height:2px">
                              <b>Car Make</b><br>
                              <textarea name="make" rows="3" cols="60">%s</textarea>
                              <hr style="height:2px">
                              <b>Car Model</b><br>
                              <textarea name="model" rows="3" cols="60">%s</textarea>
                                <hr style="height:2px">
                              <b>Engine size</b><br>
                              <textarea name="size" rows="2" cols="60">%s</textarea>
                                <hr style="height:2px">
                              <b>Fuel Type</b><br>
                              <textarea name="fuel" rows="2" cols="60">%s</textarea>
                                <hr style="height:2px">
                              <b>Registration date</b><br>
                              <textarea name="date" rows="2" cols="60">%s</textarea>
                                <hr style="height:2px">
                              <b>Location</b><br>
                              <textarea name="location" rows="6" cols="60">%s</textarea>
                                <hr style="height:2px">
                            </form>
                         </body>
                     </html>"""

    htmlPage = htmlTemplate % (desc, year, make, model, engine, fuel, date, location)
    return Response(htmlPage,'text/html')
    return flask.render_template()
if __name__ == '__main__':
    app.run(debug=True,port=8080)
