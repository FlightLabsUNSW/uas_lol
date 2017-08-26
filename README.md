# uas_lol
CREATE UAS - Repository for Land O'Lakes competition


## Weather Usage

The weather script can be run as a standalone script (Will print responses to the command line) or it can be imported as a module. It uses the Open Weather Map API: https://openweathermap.org/current

Script usage is as follows:

python weather.py -[mode] -[input_type] <input-1> <input-2 (if applicable)>

`
inputs = {
    '': INPUT_NONE,
    '-n': INPUT_NAME,
    '-i': INPUT_ID,
    '-g': INPUT_GPS,
    '-z': INPUT_ZIP
}
modes = {
    '': MODE_NORMAL,
    '-n': MODE_NORMAL,
    '-x': MODE_CHECK,
    '-w': MODE_WIND
}
`

### Modes

MODE_NORMAL: Mode normal will simply print the JSON response to the screen
MODE_CHECK: This will check whether the predefined weather conditions are satisfied
MODE_WIND: Prints a tuple of wind data (speed, direction_in_degrees)

### Input Types

INPUT_NONE: This will just perfom a default call to the Sydney endpoint
INPUT_NAME: Supply the city's Name (-n Sydney)
INPUT_ID: Supply the city's ID (-i 6619279)
INPUT_GPS: Supply GPS Lat and Lon (-g -33.867779 151.208435)
INPUT_ZIP: Supply the city's zip and country code (-z 94040 us)
