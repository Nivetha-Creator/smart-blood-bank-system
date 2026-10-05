"""
Nearest Blood Bank Search Algorithm

Uses the Haversine formula to calculate the approximate
distance between a hospital and blood banks.

This helps identify nearby blood banks that may have
compatible inventory.
"""

from math import radians, sin, cos, sqrt, atan2


def calculate_distance(
    latitude1,
    longitude1,
    latitude2,
    longitude2
):
    """
    Calculate distance between two geographical points
    using the Haversine formula.

    Returns distance in kilometers.
    """

    earth_radius = 6371

    lat1 = radians(latitude1)
    lat2 = radians(latitude2)

    difference_latitude = radians(
        latitude2 - latitude1
    )

    difference_longitude = radians(
        longitude2 - longitude1
    )

    a = (
        sin(difference_latitude / 2) ** 2
        +
        cos(lat1)
        * cos(lat2)
        * sin(difference_longitude / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return earth_radius * c


def find_nearest_banks(
    hospital_latitude,
    hospital_longitude,
    blood_banks
):
    """
    Calculate distance to every blood bank
    and return them from nearest to farthest.
    """

    banks_with_distance = []

    for bank in blood_banks:

        distance = calculate_distance(
            hospital_latitude,
            hospital_longitude,
            bank["latitude"],
            bank["longitude"]
        )

        banks_with_distance.append({
            "id": bank["id"],
            "name": bank["name"],
            "location": bank["location"],
            "distance": round(distance, 2)
        })

    banks_with_distance.sort(
        key=lambda bank: bank["distance"]
    )

    return banks_with_distance


def get_nearest_bank(
    hospital_latitude,
    hospital_longitude,
    blood_banks
):
    """
    Return the nearest blood bank.
    """

    banks = find_nearest_banks(
        hospital_latitude,
        hospital_longitude,
        blood_banks
    )

    if not banks:
        return None

    return banks[0]