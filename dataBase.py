import pymongo
from driver import Driver


class DB:
    def __init__(self):
        self.myclient = pymongo.MongoClient(
            "mongodb://bizme:bizmefutures@bizmedb-shard-00-00.8bo6c.mongodb.net:27017,bizmedb-shard-00-01.8bo6c.mongodb.net:27017,bizmedb-shard-00-02.8bo6c.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-jtwmp1-shard-0&authSource=admin&retryWrites=true&w=majority")
        self.partnerdb = self.myclient["partnerdb"]
        self.partnerscol = self.partnerdb["partners"]
        self.driverdb = self.myclient["driversDB"]
        self.driversscol = self.driverdb["drivers"]

    def create_partner(self, partnerBranchName, partnerLocation, partnerProvince, partnerDistrict, partnerPassword,
                       partnerID):
        mydict = {"partnerID": partnerID, "partnerBranchName": partnerBranchName, "partnerLocation": partnerLocation,
                  "partnerProvince": partnerProvince, "partnerDistrict": partnerDistrict,
                  "partnerPassword": partnerPassword}

        _ = self.partnerscol.insert_one(mydict)

    def create_driver(self, driver):
        mydict = {"driverId": driver.ID, "driving_licence": driver.driving_licence, "first_name": driver.first_name,
                  "last_name": driver.last_name, "birth_day": driver.birth_day,
                  "phone_number": driver.phone_number, "address": driver.address, "vehicle_brand": driver.vehicle_brand,
                  "vehicle_model": driver.vehicle_model, "vehicle_battery_health": driver.vehicle_battery_health,
                  "password": driver.password,"green_coin":0,"star_point":5}
        _ = self.driversscol.insert_one(mydict)

    def find_partner(self):
        print(self.partnerscol.find_one())

    def confirm_partner_login(self, ID, password):
        user = self.partnerscol.find({"partnerID": ID, "partnerPassword": password})

        if len(list(user)) != 0:
            return True
        else:
            return False


    def confirm_driver_login(self, ID, password):
        user = self.driversscol.find({"driverId": ID, "password": password})

        if len(list(user)) != 0:
            return True
        else:
            return False


if __name__ == "__main__":
    # DB().create_partner("123","brancj","ddddddd","ccccccc","xxxx","0000")
    #print(DB().confirm_partner_login("0000", "xxxx"))
    print(DB().confirm_driver_login("0000d", "asdasdasdasd"))

