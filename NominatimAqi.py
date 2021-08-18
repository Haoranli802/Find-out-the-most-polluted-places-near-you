"""
Haoran Li
80921159  haoral19
project 3 NominatimAqi file
11/17/2020
"""

import json
import urllib.parse
import urllib.request
import urllib.error

_BASE_SEARCH_URL = "https://nominatim.openstreetmap.org/"


def _build_search_url(search_query: str) -> str:
    """
    This function takes the search query, build up a url in the nominatim format based on the query and returns the url.
    """
    query_parameters = [
        ("addressdetails", 1), ("q", search_query),
        ("format", "json"), ("limit", 1),
    ]
    encoded_parameters = urllib.parse.urlencode(query_parameters)
    return f"{_BASE_SEARCH_URL}?{encoded_parameters}"


def _download_data(url: str) -> dict:
    """
    This function takes a url, request to connect, translate the response into uniform encoding format, and return the
    text. Close the connect in the end.
    """
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    try:
        json_text = response.read().decode(encoding="utf-8")
        return json.loads(json_text)
    finally:
        response.close()


class WebGeocoding:
    """
    This class is the Web class for Geocoing
    """
    def __init__(self, address: str) -> None:
        """
        Build up an url based on the given address, and set the url into self path
        """
        self._path = _build_search_url(address)

    def find_lat_and_lon(self) -> tuple:
        """
        A shared interface between WenGeocoing and FileGeocoding
        This function download data from the self path, find the latitude and longitude of the location json file and
        return them in a tuple. If the url's response is not 200, returns NOT 200, the status code and the url. If the
        url is not connected, returns NETWORK, None, and the url. If the url data is not formatted correctly, returns
        FORMAT, 200, and the url.
        """
        try:
            data = _download_data(self._path)
            latitude = float(data[0]["lat"])
            longitude = float(data[0]["lon"])
            return latitude, longitude
        except urllib.error.HTTPError as e:
            return "NOT 200", e.code, self._path
        except urllib.error.URLError:
            return "NETWORK", None, self._path
        except:
            return "FORMAT", 200, self._path


class FileGeocoding:
    """
    This class is the file class for Geocoing
    """
    def __init__(self, path: str) -> None:
        """
        Set the given path to self path
        """
        self._path = path

    def find_lat_and_lon(self) -> tuple:
        """
        A shared interface between WenGeocoing and FileGeocoding
        This function opens the json from the self path, find the latitude and longitude of the location in the file and
        return them in a tuple. If the file does not exist, return MISSING, None and the path of the
        file. If the file has a different format then json, return FORMAT, None and the path of the file. Close the file
        if the file is opened in the end.
        """
        file = None
        try:
            file = open(self._path)
            data = json.load(file)
            return float(data[0]["lat"]), float(data[0]["lon"])
        except FileNotFoundError:
            return "MISSING", None, self._path
        except:
            return "FORMAT", None, self._path
        finally:
            if file is not None:
                file.close()
