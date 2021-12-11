from flask import Flask, render_template, request
from forms import *
import dataBase
from driver import Driver
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import googlemaps

app = Flask(__name__)
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
            print(ID,"ID")
            if ID[0].isdigit():
                print("driver")
            else:
                print("partner")

            print("is logged in ", dataBase.confirm_partner_login(ID, password))






        except Exception as e:
            print("Exception", e)

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
                dataBase.create_driver(Driver(ID,driving_licence,first_name,
                                              last_name,birth_day,phone_number,
                                              address,vehicle_brand,vehicle_model,
                                              vehicle_battery_health,password))





        except Exception as e:
            print("Exception", e)

    return render_template("driversignup.html", form=form)


@app.route('/partnersignup', methods=["GET", "POST"])
def partnersignup():
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
            print(branchId,city)
            if not alreadySignIN:
                dataBase.create_partner(companyName,location,city,county,password,(companyName+"-"+branchId))
            else:
                print("old user")


        except Exception as e:
            print("Exception", e)

    return render_template("partnersignup.html", form=form)



@app.route("/")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': 37.4419,
             'lng': -122.1419,
             'infobox': "<b>Hello World</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
             'lat': 37.4300,
             'lng': -122.1400,
             'infobox': "<b>Hello World from other place</b>"
          }
        ]
    )
    return render_template('map.html', mymap=mymap, sndmap=sndmap)


if __name__ == '__main__':
    app.run()
