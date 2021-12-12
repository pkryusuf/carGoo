

from wtforms import Form, BooleanField, StringField, PasswordField, validators,TextAreaField,DateField







class DriverSignUpForm(Form):
    ID = StringField("ID", [validators.Length(min=1, max=25)])
    first_name = StringField("first_name", [validators.Length(min=1, max=25)])
    last_name = StringField("last_name", [validators.Length(min=1, max=25)])
    birth_day = StringField("birth_day", [validators.Length(min=1, max=25)])
    driving_licence = StringField("driving_licence", [validators.Length(min=1, max=25)])
    phone_number = StringField("phone_number", [validators.Length(min=1, max=25)])
    address = StringField("address", [validators.Length(min=1, max=25)])
    password = PasswordField("password", [validators.Length(min=1, max=25)])
    vehicle_brand = StringField("vehicle_brand", [validators.Length(min=1, max=25)])
    vehicle_model = StringField("vehicle_model", [validators.Length(min=1, max=25)])
    vehicle_battery_health = StringField("vehicle_battery_health", [validators.Length(min=4, max=25)])


class LoginForm(Form):

    #TODO validation
    ID = StringField("Id", [validators.Length(min=1, max=25)])
    password =PasswordField("adress", [validators.Length(min=1, max=25)])


class CompanySignInForm(Form):

    companyName = StringField("companyName", [validators.Length(min=1, max=25)])
    branchId = StringField("BranchId", [validators.Length(min=1, max=25)])
    city = StringField("city", [validators.Length(min=1, max=25)])
    county = StringField("county", [validators.Length(min=1, max=25)])
    location = StringField("location", [validators.Length(min=1, max=25)])
    password = StringField("password", [validators.Length(min=1, max=25)])

class CargoInputForm(Form):
    origin = StringField("origin", [validators.Length(min=1, max=25)])
    destination = StringField("destination", [validators.Length(min=1, max=25)])
    volume =  StringField("city", [validators.Length(min=1, max=25)])
    category = StringField("category", [validators.Length(min=1, max=25)])

class DriverDestinationForm(Form):
    origin = StringField("origin", [validators.Length(min=1, max=25)])
    destination = StringField("destination", [validators.Length(min=1, max=25)])
    date = DateField("date")
    chargingStatus = StringField("destination", [validators.Length(min=1, max=25)])