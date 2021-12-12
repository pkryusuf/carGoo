
class Cargo:
    def __init__(self,origin,destination,volume,type,ownerId,driverId=None):
        self.origin = origin
        self.destination = destination
        self.volume = volume
        self.type = type
        self.ownerId = ownerId
        self.driverId = driverId

