from functools import wraps
import googlemaps
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for,flash
from flask_login import LoginManager
from cargo import Cargo
from forms import *
import dataBase
from driver import Driver
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import googlemaps
import cargoAPI

app = Flask(__name__)
app.secret_key = "supersecretkey"
dataBase = dataBase.DB()
app.config['GOOGLEMAPS_KEY'] = "AIzaSyA02vq5et0wTVE_Sr9IZUNUtQc2rJxJYlM"

GoogleMaps(app)


@app.route('/login', methods=["GET", "POST"])
def login():  # put application's code here
    form = LoginForm(request.form)

    if request.method == "POST":

        try:
            ID = form.ID.data
            password = form.password.data
            print(ID, "ID")
            if ID[0].isdigit():
                dataBase.confirm_driver_login(ID, password)
                session["type"] = "driver"
                session["ID"] = ID
                print("driver")
            else:
                print("partner")
                session["type"] = "partner"

            if dataBase.confirm_partner_login(ID, password):
                session["logged_in"] = True
                session["ID"] = ID
                return render_template("cargoinput.html")
            elif dataBase.confirm_driver_login(ID,password):
                print("ELİF")
                session["type"] = "driver"
                session["ID"] = ID
                session["logged_in"] = True
                return redirect(url_for("driver_first_page"))
            else:
                session["logged_in"] = False

            print(session["logged_in"], session["type"])



        except Exception as e:
            print("Exception", e)
    try:
        if session["type"] == "driver":
            return render_template()
    except Exception as e:
        return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@app.route('/driversignup', methods=["GET", "POST"])
def driver_sign_up():
    form = DriverSignUpForm(request.form)

    if request.method == "POST":
        # TODO encrypt password
        try:
            ID = form.ID.data
            driving_licence = form.driving_licence.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            birth_day = form.birth_day.data
            phone_number = form.phone_number.data
            address = form.address.data
            vehicle_brand = form.vehicle_brand.data
            vehicle_model = form.vehicle_model.data
            vehicle_battery_health = form.vehicle_battery_health.data
            password = form.password.data

            alreadySignIN = dataBase.confirm_driver_login(ID, password)

            if not alreadySignIN:
                dataBase.create_driver(Driver(ID, driving_licence, first_name,
                                              last_name, birth_day, phone_number,
                                              address, vehicle_brand, vehicle_model,
                                              vehicle_battery_health, password))
                session["logged_in"] = True
                session["type"] = "driver"
                session["ID"] = ID
                return redirect(url_for("driver_first_page"))







        except Exception as e:
            print("Exception", e)

    return render_template("driversignup.html", form=form)


@app.route('/partnersignup', methods=["GET", "POST"])
def partner_signup():
    form = CompanySignInForm(request.form)

    if request.method == "POST":
        # TODO encrypt password
        # TODO already signin alert

        try:
            companyName = form.companyName.data
            branchId = form.branchId.data
            city = form.city.data
            county = form.county.data
            location = form.location.data

            password = form.password.data

            alreadySignIN = dataBase.confirm_partner_login(branchId, password)

            if not alreadySignIN:
                dataBase.create_partner(companyName, location, city, county, password, (companyName + "-" + branchId))
            else:
                return redirect(url_for("/partnersignup"))


        except Exception as e:
            print("Exception", e)

    return render_template("partnersignup.html", form=form)


@app.route("/mapview")
def mapview():
    # creating a map in the view

    mymap = Map(
        identifier="view-side",
        lat=41.0370023,
        lng=28.9850917,
        markers=[(41.0370023, 28.9850917)]
    )
    markers = []
    x = cargoAPI.xx()
    for i in x:
        markers.append({
            'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
            'lat': i[0],
            'lng': i[1],
            'infobox': "<b>Hello World</b>"
        })
    print(x)
    sndmap = Map(
        identifier="sndmap",
        lat=41.0370023,
        lng=28.9850917,

        markers=markers
    )
    return render_template('map.html', mymap=mymap, sndmap=sndmap)


@app.route("/map", methods=["GET", "POST"])
def map():
    now = datetime.now()
    gmaps = googlemaps.Client(key='AIzaSyA02vq5et0wTVE_Sr9IZUNUtQc2rJxJYlM')
    geocode_result = gmaps.geocode('istanbul taksim')
    directions_result = gmaps.directions("istanbul,taksim",
                                         "Bursa ,merkez",

                                         mode="transit",
                                         departure_time=now)

    lat1 = geocode_result[0]["geometry"]["location"]["lat"]
    lng1= geocode_result[0]["geometry"]["location"]["lng"]

    geocode_result = gmaps.geocode('İzmit türkiye')
    lat2 = geocode_result[0]["geometry"]["location"]["lat"]
    lng2 = geocode_result[0]["geometry"]["location"]["lng"]

    geocode_result = gmaps.geocode('yalova türkiye')
    lat3 = geocode_result[0]["geometry"]["location"]["lat"]
    lng3 = geocode_result[0]["geometry"]["location"]["lng"]


    geocode_result = gmaps.geocode('bursa türkiye')
    lat4 = geocode_result[0]["geometry"]["location"]["lat"]
    lng4 = geocode_result[0]["geometry"]["location"]["lng"]




    directions_result = {"distance":162,"time":2.2,"coin":(162*0.10 +2)}
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=lat3,
        lng=lng3,
        zoom=8,
        markers=[
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': lat1,
                'lng': lng1,
                'infobox': "<b>Starting Point</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': lat2,
                'lng': lng2,
                'infobox': "<b>Cargo Accept Point</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': lat3,
                'lng': lng3,
                'infobox': "<b>Cargo Delivery Point</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': lat4,
                'lng': lng4,
                'infobox': "<b>Destination point</b>"
            }
        ]
    )
    if request.method == "POST":
        return redirect(url_for("takecargo"))
    print(geocode_result)
    return render_template('harita.html', mymap=mymap, sndmap=sndmap,result=directions_result)


@app.route("/cargoinput", methods=["GET", "POST"])
def cargo_input():
    if not session["logged_in"]:
        return redirect(url_for("login"))

    form = CargoInputForm(request.form)

    if request.method == "POST":

        try:
            origin = form.origin.data
            destination = form.destination.data
            volume = form.volume.data
            category = form.category.data

            dataBase.add_cargo(Cargo(origin, destination, volume, category, session["ID"]))
            return redirect(url_for("index"))







        except Exception as e:
            print("Exception", e)
    return render_template('cargoinput.html', form=form)


@app.route("/")
def index():
    flash("Mesajınız alındı", "success")
    return render_template("index.html")


@app.route("/driverfirstpage", methods=["GET", "POST"])
def driver_first_page():
    try:
        if not session["logged_in"]:
            return redirect(url_for("login"))
    except Exception as e:
        return redirect(url_for("login"))

    form = DriverDestinationForm(request.form)

    if request.method == "POST":

        try:
            origin = form.origin.data
            destination = form.destination.data
            date = form.date.data
            chargingStatus = form.chargingStatus.data

            # TODO kargo ekranı

            driverInfo = {"origin": origin, "destination": destination, "date": date, "chargingStatus": chargingStatus}

            print("ınfo", driverInfo)
            return redirect(url_for("listcargos"))
        except Exception as e:
            print("Exception", e)

    return render_template('driver_first_page.html', form=form)


@app.route("/profile")
def profile():
    try:
        if not session["logged_in"] or session["type"] != "driver":
            session["logged_in"] = False
            return redirect(url_for("login"))
    except Exception as e:
        return redirect(url_for("login"))
    print("sessionid", session["ID"])
    driver = dataBase.find_driver_with_id(session["ID"])
    if not driver:
        return redirect(url_for("login"))

    return render_template("profile.html", driver)

@app.route("/listcargos", methods=["GET", "POST"])
def listcargos():
    cargos = dataBase.get_cargos()
    if request.method == "POST":
        print("POST MAP")
        return redirect(url_for("map"))
    return render_template("list_cargos.html",cargos=cargos)

@app.route("/takecargo", methods=["GET", "POST"])
def takecargo():
    if request.method == "POST":
        return redirect(url_for("map_next"))
    return render_template("takingCargo.html")



@app.route("/mapnext", methods=["GET", "POST"])
def map_next():
    if request.method == "POST":
        pass
    now = datetime.now()
    gmaps = googlemaps.Client(key='AIzaSyA02vq5et0wTVE_Sr9IZUNUtQc2rJxJYlM')
    geocode_result = gmaps.geocode('istanbul taksim')
    directions_result = gmaps.directions("istanbul,taksim",
                                         "Bursa ,merkez",

                                         mode="transit",
                                         departure_time=now)

    lat1 = geocode_result[0]["geometry"]["location"]["lat"]
    lng1= geocode_result[0]["geometry"]["location"]["lng"]

    geocode_result = gmaps.geocode('İzmit türkiye')
    lat2 = geocode_result[0]["geometry"]["location"]["lat"]
    lng2 = geocode_result[0]["geometry"]["location"]["lng"]

    geocode_result = gmaps.geocode('yalova türkiye')
    lat3 = geocode_result[0]["geometry"]["location"]["lat"]
    lng3 = geocode_result[0]["geometry"]["location"]["lng"]


    geocode_result = gmaps.geocode('bursa türkiye')
    lat4 = geocode_result[0]["geometry"]["location"]["lat"]
    lng4 = geocode_result[0]["geometry"]["location"]["lng"]




    directions_result = {"distance":133,"time":1.2,"coin":(162*0.10 +2)}
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=lat3,
        lng=lng3,
        zoom=8,
        markers=[
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': lat1,
                'lng': lng1,
                'infobox': "<b>Starting Point</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': lat2,
                'lng': lng2,
                'infobox': "<b>Cargo Accept Point</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': lat3,
                'lng': lng3,
                'infobox': "<b>Cargo Delivery Point</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': lat4,
                'lng': lng4,
                'infobox': "<b>Destination point</b>"
            }
        ]
    )
    if request.method == "POST":
        return redirect(url_for("cargo_delivery"))
    print(geocode_result)
    return render_template('haritanext.html', mymap=mymap, sndmap=sndmap,result=directions_result)

@app.route("/cargodelivery", methods=["GET", "POST"])
def cargo_delivery():
    if request.method == "POST":
        return redirect(url_for("final_page"))
    return render_template("deliverCargo.html")

@app.route("/final", methods=["GET", "POST"])
def final_page():
    if request.method == "POST":
        return redirect(url_for("index"))
    return render_template("final.html")

if __name__ == '__main__':
    app.run()
