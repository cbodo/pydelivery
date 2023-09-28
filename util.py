from datetime import datetime, date, time, timedelta
# Global variables
# Time Complexity: O(1)
# Space Complexity: O(1)
HUB = "4001 S 700 E"
START_TIME = datetime.combine(date.today(),time(8,0))
STOP_TIME = datetime.combine(date.today(),time(17,0))
DELAY_TIME = datetime.combine(date.today(),time(9,5))
CORRECT_ADDRESS_TIME = datetime.combine(date.today(),time(10,20))
CORRECT_ADDRESS = {
    'address': '410 S State St',
    'city': 'Salt Lake City',
    'state': 'UT',
    'zip': '84111',
}

# "Clears" console screen.
#
# Time Complexity: O(1)
# Space Complexity: O(1)
def clear():
    print("\n"*60)

# Prints string with empty line above and below it.
#
# Time Complexity: O(1)
# Space Complexity: O(1)
def print_with_spacing(string):
    print()
    print(string)
    print()

# Returns a datetime object to represent a package deadline.  This program
# assumes that EOD is 5:00 PM (17:00).
#
# Time Complexity: O(1)
# Space Complexity: O(1)
def get_deadline(deadline):
    # Returns datetime object for EOD deadline (O(1)).
    if(deadline == "EOD"):
        return datetime.combine(date.today(),time(17,0))
    date_string = date.today().strftime("%Y-%m-%d ")
    date_string += deadline.strip()
    return datetime.strptime(date_string,"%Y-%m-%d %I:%M %p")

# Validates time input.
#
# Time Complexity: O(1)
# Space Complexity: O(1)
def validate_time(string):
    if(len(string) == 3):
        string = "0"+string
    date_string = date.today().strftime("%Y-%m-%d ")
    date_string += string.strip()
    return datetime.strptime(date_string,"%Y-%m-%d %H%M")
