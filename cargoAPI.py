# this class is only for testing Google Maps api
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyA02vq5et0wTVE_Sr9IZUNUtQc2rJxJYlM')

# Geocoding an address
geocode_result = gmaps.geocode('istanbul taksim')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("istanbul,taksim",
                                     "izmir ,buca",

                                     mode="transit",
                                     departure_time=now)


def decode_polyline(polyline_str):
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string. In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them later
        for unit in ['latitude', 'longitude']:
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index += 1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']

        coordinates.append((lat / 100000.0, lng / 100000.0))

    return coordinates


print(geocode_result[0]["geometry"]["location"]["lat"])
print(geocode_result[0]["geometry"]["location"]["lng"])
print(directions_result)
