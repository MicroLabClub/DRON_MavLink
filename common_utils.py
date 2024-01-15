
def get_battery_value(vehicle):
#    print("vehicle.battery.level: %s", vehicle.battery.level)
    return vehicle.battery.level if vehicle else None

def get_coordinates(vehicle):
    coordinates = []

    coordinates.append({"lat": vehicle.location.global_relative_frame.lat, "lng": vehicle.location.global_relative_frame.lon, "alt": vehicle.location.global_relative_frame.alt})

    return coordinates
