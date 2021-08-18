"""
Haoran Li
80921159  haoral19
project 3 purpalAir file
11/17/2020
"""

import json
import math
import urllib.request
import urllib.error


def _round_to_int(aqi: float) -> int:
    """
    This function round the given float to integer and return the integer.
    """
    if aqi % 1 < 0.5:
        return int(aqi)
    else:
        return int(aqi + 0.5)


def calculate_aqi(concentration: float) -> int:
    """
    This function calculates the aqi of the given P.M 2.5 concentration, round the aqi into integer, and return the
    integer aqi.
    """
    if 0 <= concentration < 12.1:
        return _round_to_int(concentration * 50 / 12)
    elif 12.1 <= concentration < 35.5:
        return _round_to_int(51 + (concentration - 12.1) * 50 / 23.3)
    elif 35.5 <= concentration < 55.5:
        return _round_to_int(101 + (concentration - 35.5) * 50 / 19.9)
    elif 55.5 <= concentration < 150.5:
        return _round_to_int(151 + (concentration - 55.5) * 50 / 94.9)
    elif 150.5 <= concentration < 250.5:
        return _round_to_int(201 + (concentration - 150.5) * 50 / 99.9)
    elif 250.5 <= concentration < 350.5:
        return _round_to_int(301 + (concentration - 250.5) * 50 / 99.9)
    elif 350.5 <= concentration < 500.5:
        return _round_to_int(401 + (concentration - 350.5) * 50 / 149.9)
    else:
        return 501


def great_circle_distance(latitudes1: float, longitudes1: float, latitudes2: float, longitudes2: float) -> float:
    """
    This function takes in the latitude and longitude of two point in the earth, calculates the distance of two point
    using the great circle formula and then return the distance.
    """
    dlat = math.radians(latitudes1 - latitudes2)
    dlon = math.radians(longitudes1 - longitudes2)
    alat = math.radians((latitudes1 + latitudes2) / 2)
    R = 3958.8
    x = dlon * math.cos(alat)
    d = math.sqrt(math.pow(x, 2) + math.pow(dlat, 2)) * R
    return d


class FileJsonData:
    """
    This class is the file class for json data
    """
    def __init__(self, path: str) -> None:
        """
        set the given path into self path
        """
        self._path = path

    def get_data(self) -> dict or tuple:
        """
        A shared interface between filejsondata and webjsondata. The file one opens a file and reads the data part of
        the json file and return the data list. If the file does not exist, return MISSING, None and the path of the
        file. If the file has a different format then json, return FORMAT, None and the path of the file. Close the file
        if the file is opened in the end.
        """
        file = None
        try:
            file = open(self._path)
            data = json.load(file)["data"]
            return data
        except FileNotFoundError:
            return "MISSING", None, self._path
        except:
            return "FORMAT", None, self._path
        finally:
            if file is not None:
                file.close()


class WebJsonData:
    """
    This class is the Web class for json data
    """
    def __init__(self, url: str):
        """
        set the given url into self url
        """
        self._url = url

    def get_data(self) -> dict or str:
        """
        A shared interface between filejsondata and webjsondata. The Web one opens a url and reads the data part of
        the response and return the data list in uniform coding format. If the url' response is not 200, returns NOT 200,
        the status code and the url. If the url is not connected, returns NETWORK, None, and the url. If the url data
        is not formatted correctly, returns FORMAT, 200, and the url.
        """
        response = None
        try:
            request = urllib.request.Request(self._url)
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding="utf-8")
            return json.loads(json_text)["data"]
        except urllib.error.HTTPError as e:
            return "NOT 200", e.code, self._url
        except urllib.error.URLError:
            return "NETWORK", None, self._url
        except:
            return "FORMAT", 200, self._url
        finally:
            if response is not None:
                response.close()


def _location_checker(location_elements: list) -> bool:
    """
    This function checks if the elements in the location are interested. If not, return false.
    """
    if location_elements[1] is None or location_elements[4] is None or location_elements[25] is None or location_elements[27] is None or location_elements[28] is None:
        return False
    elif location_elements[4] > 3600 or location_elements[25] != 0:
        return False
    else:
        return True


def find(latitude: float, longitude: float, data_list: list, range: int) -> list:
    """
    This function takes a latitude, a longitude, a data list, and a range. Then it return all the locations
    that are interested and inside of the range to the center location in a list.
    """
    location_list = []
    for location in data_list:
        if _location_checker(location) and great_circle_distance(location[27], location[28], latitude, longitude) <= range:
            location_list.append(location)
    return location_list


def get_location_from_aqi(locations: list, threshold: int) -> list:
    """
    This function takes in a location list, and a threshold. Then it finds out all the location that have greater aqi
    than the threshold, add the location into a new list, and sort the list in descending aqi order, and return the
    new list.
    """
    location_list = []
    for location in locations:
        if calculate_aqi(location[1]) >= threshold:
            index = 0
            if len(location_list) == 0:
                location_list.append(location)
            else:
                for x in location_list:
                    if calculate_aqi(location[1]) <= calculate_aqi(x[1]):
                        index += 1
                location_list.insert(index, location)
    return location_list
