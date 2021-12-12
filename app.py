from functools import wraps

from flask import Flask, render_template, request, session, redirect, url_for
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


@app.route("/s")
def maptest():
    return render_template("maptest.html")


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







        except Exception as e:
            print("Exception", e)
    return render_template('cargoinput.html', form=form)


@app.route("/")
def index():
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

@app.route("/listcargos")
def listcargos():
    cargos = dataBase.get_cargos()
    return render_template("list_cargos.html",cargos=cargos)


if __name__ == '__main__':
    app.run()
