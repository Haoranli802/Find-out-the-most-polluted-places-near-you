# Find-out-the-most-polluted-places-near-you
This python project is based on uci ics ICS32A project #3(stop here and do not look at any part of the project if you are enrolled in this course). 
It aims to find out the most polluted places near a designated location based on the AQI(Air Quality Index) value.
It takes in six inputs, and the inputs has to be in their correct format. 

The first line of input will be in one of two formats:
CENTER NOMINATIM location, where location is any arbitrary, non-empty string describing the "center" point of our analysis. For example, if this line of input said
CENTER NOMINATIM Bren Hall, Irvine, CA, the center of our analysis is Bren Hall on the campus of UC Irvine. The word NOMINATIM indicates that we'll use Nominatim's
API to determine the precise location (i.e., the latitude and longitude) of our center point.
CENTER FILE path, where path is the path to a file on your hard drive containing the result of a previous call to Nominatim. The file needs to exist. The
expectation is the file will contain data in the same format that Nominatim would have given you, but will allow you to test your work without having to call the
API every time — important, because Nominatim imposes limitations on how often you can call into it, and because this could allow you to make large parts of the
program work without having hooked up the APIs at all.


The second line of input will be in the following format:
RANGE miles, where miles is a positive integer number of miles. For example, if this line of input said RANGE 30, then the range of our analysis is 30 miles from
the center location.


The third line of input will be in the following format:
THRESHOLD AQI, where AQI is a positive integer specifying the AQI threshold, which means we're interested in finding places that have AQI values at least as high as
that threshold. It is safe to assume that the AQI threshold is non-negative, though it could be zero.


The fourth line of input will be in the following format:
MAX number, where number is the maximum number of locations we want to find in our search, which you can assume would be a positive integer. For example, if this
line of input said MAX 5, then we're looking for up to five locations where the AQI value is at or above the AQI threshold.


The fifth line of input will be in one of two formats:
AQI PURPLEAIR, which means that we want to obtain our air quality information from PurpleAir's API.
AQI FILE path, where path is the path to a file on your hard drive containing the result of a previous call to PurpleAir's API with all of the sensor data in it.


The sixth line of input will be in one of two formats:
REVERSE NOMINATIM, which means that we want to use the Nominatim API to do reverse geocoding, i.e., to determine a description of where problematic air quality
sensors are located.
REVERSE FILES path1 path2 ..., which means that we want to use files stored on our hard drive containing the results of previous calls to Nominatim's reverse
geocoding API instead. Paths are separated by spaces — which means they can't contain spaces — and we expect there to be as many paths listed as the number we
passed to MAX (e.g., if we said MAX 5 previously, then we'd specify five files containing reverse geocoding data).
(source from https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/)

The output will be the following:
After reading all of the input, you'd first display the latitude and longitude of the center location, with latitudes and longitudes shown in the following format.

CENTER 33.64324045/N 117.84185686276017/W
Then, you'd use the information that's either stored in the specified files or downloaded from the specified APIs to find the sensors that are in the specified
range of the center location, then determine which of those sensors have the highest AQI values and, for any of them that are at or above the AQI threshold, display
information about the first n of them.
(source from https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/)


A complete example using only website connections:

CENTER NOMINATIM Bren Hall, Irvine, CA
RANGE 100
THRESHOLD 50
MAX 5
AQI PURPLEAIR
REVERSE NOMINATIM
CENTER 33.6432477/N 117.84186526398847/W
AQI 161
34.64158/N 117.82862/W
Challenger Middle School, 170th Street East, Lake Los Angeles, California, 93591, United States
AQI 158
32.567635/N 117.13274/W
1690, Seacoast Drive, Imperial Beach, San Diego County, California, 91932, United States
AQI 130
34.155277/N 118.56824/W
4648, Nomad Drive, Los Angeles, California, 91364, United States
AQI 129
34.28839/N 118.44374/W
100, Fermoore Street, San Fernando, California, 91340, United States
AQI 98
34.110126/N 118.21719/W
862, Tacuba Street, Los Angeles, California, 90065, United States

Another example using local json files for center and api(private information is blocked):
CENTER FILE /Users/******/Desktop/project3/nominatim1.json
RANGE 100
THRESHOLD 70
MAX 10
AQI FILE /Users/******/Desktop/project3/data.json
REVERSE NOMINATIM
CENTER 33.64324045/N 117.84185686276017/W
AQI 501
33.99/N 118.17824/W
4798, East 52nd Drive, Maywood, California, 90270, United States
AQI 187
33.88965/N 118.413376/W
204, 19th Street, Manhattan Beach, California, 90266, United States
AQI 173
34.137314/N 118.07097/W
501, Michigan Boulevard, Chapman Woods, El Monte, California, 91107, United States
AQI 171
34.0244/N 118.51302/W
Annenberg Beach House, Pacific Coast Highway, Santa Monica, California, 90402, United States
AQI 167
33.73609/N 117.44975/W
Laundry & Shower, Skyview Circle, Riverside County, California, United States
AQI 159
34.18076/N 118.50706/W
8, Metro Orange Line Bikeway, Los Angeles, California, 91406-5441, United States
AQI 159
34.045525/N 118.71656/W
24592, Mariposa Circle, California, 90265, United States
AQI 153
33.73571/N 118.33903/W
3466, Coolheights Drive, Rancho Palos Verdes, California, 90275, United States
AQI 148
34.18794/N 118.33993/W
2654, Pacific Avenue, Vega, Burbank, California, 91505, United States
AQI 134
33.987827/N 117.3369/W
306, Massachusetts Avenue, Canyon Crest Heights, Riverside, Riverside County, California, 92521, United States



Implementing instructions:
The python projects should be keep together in the same folder.
The project3.py file is the main executable file to start taking inputs and output outputs. 
The .json files should be keep together in the same folder as the python files, they are for file inputs. 
