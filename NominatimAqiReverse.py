"""
Haoran Li
80921159  haoral19
project 3 NominatimAqiReverse file
11/17/2020
"""

import json
import urllib.parse
import urllib.request
import urllib.error

_BASE_SEARCH_URL = "https://nominatim.openstreetmap.org/reverse"


def _build_search_reverse_url(latitude: float, longitude: float) -> str:
    """
    This function takes a latitude and a longitude and return a nominatim reverse url in the correct format that
    contains the given latitude and the given longitude.
    """
    query_parameters = [
        ("format", "json"), ("lat", latitude), ("lon", longitude),
    ]
    encoded_parameters = urllib.parse.urlencode(query_parameters)
    return f"{_BASE_SEARCH_URL}?{encoded_parameters}"


def _download_data(url: str) -> dict:
    """
    This function takes in url, request to connect, download the response, transfer the response into uniform code and
    return the response data.
    """
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    try:
        json_text = response.read().decode(encoding="utf-8")
        return json.loads(json_text)
    finally:
        response.close()


class WebGeocodingReverse:
    """
    This class is the Web class for GeocoingReverse
    """
    def __init__(self, latitude: float, longitude: float) -> None:
        """
        Set the given latitude and given longitude to self latitude and self longitude. Build up an url, and set it
        to self url.
        """
        self._latitude = latitude
        self._longitude = longitude
        self._path = _build_search_reverse_url(self._latitude, self._longitude)

    def find_description(self) -> str or tuple:
        """
        This is the shared interface between WebGeocoingReverse and FileGeocodinReverse.
        It downs data from the self url path, and find out the display_name part in the data, and
        return the description string. If the url's response is not 200, returns NOT 200, the status code and the url.
        If the url is not connected, returns NETWORK, None, and the url. If the url data is not formatted correctly,
        returns FORMAT, 200, and the url.
        """
        try:
            data = _download_data(self._path)
            return data["display_name"]
        except urllib.error.HTTPError as e:
            return "NOT 200", e.code, self._path
        except urllib.error.URLError:
            return "NETWORK", None, self._path
        except:
            return "FORMAT", 200, self._path


class FileGeocodingReverse:
    """
    This class is the File class for GeocoingReverse
    """
    def __init__(self, path: str) -> None:
        """
        Set the given path the self path
        """
        self._path = path

    def find_description(self) -> str or tuple:
        """
        This is the shared interface between WebGeocoingReverse and FileGeocodinReverse. It opens the json location
        file from the self path, find out the display_name part in the data, and return the
        description string. If the file does not exist, return MISSING, None and the path of the
        file. If the file has a different format then json, return FORMAT, None and the path of the file. Close the file
        if the file is opened in the end.
        """
        file = None
        try:
            file = open(self._path)
            data = json.load(file)
            return data["display_name"]
        except FileNotFoundError:
            return "MISSING", None, self._path
        except:
            return "FORMAT", None, self._path

        finally:
            if file is not None:
                file.close()

    def find_lat_and_lon(self) -> tuple:
        """
        This function finds out the latitude and the longitude from the json location file that belongs to self path,
        and return the latitude and the longitude in float format.
        """
        file = open(self._path)
        data = json.load(file)
        lat = float(data["lat"])
        lon = float(data["lon"])
        return lat, lon

