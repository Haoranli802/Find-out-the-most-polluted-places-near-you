"""
Haoran Li
80921159  haoral19
project 3 main file
11/17/2020
"""

from purpleAir import *
from NominatimAqi import *
from NominatimAqiReverse import *
import math


def read_first_line() -> tuple:
    """
    This function reads the first line of the input, determine if it is Nominatim or file format, and return the
    determination, and the path for file format, or the location for nominatim format in a tuple.
    """
    elements = input().split(" ")
    if elements[1] == "NOMINATIM":
        return 0, " ".join(elements[2:])
    else:
        return 1, elements[2]


def read_second_line() -> int:
    """
    This function reads the second line of the input, and return second element of the input which is the range in mile
    in integer form.
    """
    range_in_mile = input().split(" ")[1]
    return int(range_in_mile)


def read_third_line() -> int:
    """
    This function reads the second line of the input, and return second element of the input which is the threshold in
    integer form.
    """
    threshold = input().split(" ")[1]
    return int(threshold)


def read_fourth_line() -> int:
    """
    This function reads the second line of the input, and return second element of the input which is the maximum number
    in integer form.
    """
    max_number = input().split(" ")[1]
    return int(max_number)


def read_fifth_line() -> tuple:
    """
    This function reads the first line of the input, determine if it is PurpleAir or file format, and return the
    determination, and the path for file format, or None for PurpleAir format in a tuple.
    """
    aqi = input().split(" ")
    if aqi[1] == "PURPLEAIR":
        return 0, None
    else:
        return 1, aqi[2]


def read_sixth_line() -> tuple or list:
    """
     This function reads the first line of the input, determine if it is Nominatim reverse or file format, and return
     the determination, and the list of paths for file format, or None for Nominatim reverse format in a tuple.
    """
    nominatim = input().split(" ")
    if nominatim[1] == "NOMINATIM":
        return 0, None
    else:
        file_list = nominatim[2:]
        return 1, file_list


def lat_lon_transform(lat: float, lon: float) -> (str, str):
    """
    This function takes in the numerical form of the latitude and longitude, and transform them into North, South, West,
    East form, and return the new value for latitude and longitude.
    """
    new_lat = ""
    new_lon = ""
    if lat > 0:
        new_lat = f"{lat}/N"
    elif lat < 0:
        new_lat = f"{abs(lat)}/S"
    else:
        lat = "0"

    if lon > 0:
        new_lon = f"{lon}/E"
    elif lon < 0:
        new_lon = f"{abs(lon)}/W"
    else:
        new_lon = "0"
    return new_lat, new_lon


def read_from_first_line_error() ->None:
    """
    This function finish reading the rest of input when error occur after the first line of input, and return nothing
    """
    read_second_line()
    read_third_line()
    read_fourth_line()
    read_fifth_line()
    read_sixth_line()


def handling_error(error_type: str, e_code: int or None, error_path: str) -> None:
    """
    This function takes in an error type, an e code and an error path, determine the type of error, and print out the
    according error message.
    """
    print("FAILED")
    if type(e_code) == int:
        print(f"{e_code} {error_path}")
    else:
        print(error_path)
    print(error_type)


def run() -> None:
    """
    This is the main function of the project, it is long but unique.
    It first reads the first line of input, assign code

    and location into local variables, set end and error equal to false, and then create e code, error type, error path
    and the final print list.

    Then it starts a while loop, this loop will not end until either all the inputs are done or error occur in the
    middle of the inputs.

    Inside the while loop, it first create Geocoing object using the code and location, determine if error occur. If not
    , find out the latitude and longitude of the center location. If error occur, read all the rest of the inputs and
    end the loop.

    Then it reads from the second input to the fourth input, assign all the values into local variables.

    Then it reads the fifth input, and get the code and the path. Then create JsonData object based on the input,
    determine if they contains error. If not, get the location data list. If error occur, read all the rest of the
    input and end the loop.

    Then it will find out all the location with in the range of miles, find out the ones have higher aqi than the
    threshold, and sort the max number of them into a list.

    Then it reads the fifth input, and get the code and the path. Then create WebGeocoingReverse objects based on the
    input, determine if they contains error. If error occur, end the lopp. If no error occurs, get the description of
    the target locations, sort the information(latitude, longitude, aqi, description) into the final print list, and set
    end equal to True to get out of the loop.

    In the end, the function determine if any error occur during the previous steps, if not, prints out the final
    information list. If error occurs, prints the according error message instead.

    """
    code, location = read_first_line()
    end = False
    error = False
    e_code = 0
    error_type = ""
    error_path = ""
    print_list = []
    while not error and not end:
        if code == 0:
            location1 = WebGeocoding(location)
        else:
            location1 = FileGeocoding(location)
        if len(location1.find_lat_and_lon()) == 3: # if the description is a tuple of length 3, then error occur
            error_type, e_code, error_path = location1.find_lat_and_lon()
            error = True
            read_from_first_line_error()
            break
        lat, lon = location1.find_lat_and_lon()
        range_in_miles = read_second_line()
        threshold = read_third_line()
        max_number = read_fourth_line()
        code, path = read_fifth_line()
        if code == 0:
            data1 = WebJsonData("https://www.purpleair.com/data.json")
        else:
            data1 = FileJsonData(path)
        data_list = data1.get_data()
        if type(data_list) != list: # if the description is a tuple, then error occur
            error_type, e_code, error_path = data_list
            error = True
            read_sixth_line()
            break
        locations = find(lat, lon, data_list, range_in_miles)
        new_locations = get_location_from_aqi(locations, threshold)[:max_number]
        code, file_list = read_sixth_line()
        if code == 0:
            lat, lon = lat_lon_transform(lat, lon)
            print_list.append(f"CENTER {lat} {lon}")
            for target_location in new_locations:
                lat, lon = lat_lon_transform(target_location[27], target_location[28]) # I assume that if we aren't given location files, we print out the latitude and longitude of the target locations using purpleAir's data
                aqi = calculate_aqi(target_location[1])
                reverse = WebGeocodingReverse(float(target_location[27]), float(target_location[28]))
                description = reverse.find_description()
                if type(description) != str: # if the description is a tuple, then error occur
                    error_type, e_code, error_path = reverse.find_description()
                    error = True
                    break
                print_list.append(f"AQI {aqi}")
                print_list.append(f"{lat} {lon}")
                print_list.append(f"{description}")
        else:
            lat, lon = lat_lon_transform(lat, lon)
            print_list.append(f"CENTER {lat} {lon}")
            index = 0
            for x in file_list:
                aqi = calculate_aqi(new_locations[index][1])
                reverse = FileGeocodingReverse(x)
                description = reverse.find_description()
                if type(description) != str:
                    error_type, e_code, error_path = reverse.find_description()
                    error = True
                    break
                lat, lon = reverse.find_lat_and_lon() # I assume that if we are given location files, we print out the latitude and longitude of the given file instead of the ones in purpleAir
                lat, lon = lat_lon_transform(lat, lon)
                print_list.append(f"AQI {aqi}")
                print_list.append(f"{lat} {lon}")
                print_list.append(f"{description}")
                index += 1
        end = True

    if error:
        handling_error(error_type, e_code, error_path)
    else:
        for x in print_list:
            print(x)


if __name__ == "__main__":
    run()  # It might takes a while if you are running the web version. 
