import csv
from datetime import datetime, date, time, timedelta
from util import get_deadline, START_TIME
from Package import Package
from Truck import Truck
from HashTable import HashTable
from Log import Log

# Initializes HashTable object with size=40 to store package data.
#
# Time Complexity: O(n)
# Space Complexity: O(n^2)
package_data = HashTable(40)
# Initializes HashTable object with size=27 to store address data.
#
# Time Complexity: O(n)
# Space Complexity: O(n^2)
address_data = HashTable(27)
# Initializes HashTable object with size=42 to store status logs for all packages.
#
# Time Complexity: O(n)
# Space Complexity: O(n^2)
package_log = HashTable(42)
# Initializes empty list for distance_data.
#
# Time Complexity: O(1)
# Space Complexity: O(n)
distance_data = []
# Initializes empty list for packages that must be delivered on the same truck.
#
# Time Complexity: O(1)
# Space Complexity: O(n)
group_queue = []
# Initializes empty list for delayed packages.
#
# Time Complexity: O(1)
# Space Complexity: O(n)
delay_queue = []
# Initializes empty list for packages with a deadline.
#
# Time Complexity: O(1)
# Space Complexity: O(n)
priority_queue = []
# Initializes empty list for packages all other packages.
#
# Time Complexity: O(1)
# Space Complexity: O(n)
standard_queue = []
# Initializes a list of log times for retrieving logs from the package_log hash table.
#
# Time Complexity: O(1)
# Space Complexity: O(n)
log_times = []
# Initializes a new truck object with name "truck 1" and time=START_TIME
#
# Time Complexity: O(n)
# Space Complexity: O(n^2)
truck_1 = Truck("truck 1",START_TIME)
# Initializes a new truck object with name "truck 2" and time=START_TIME
#
# Time Complexity: O(n)
# Space Complexity: O(n^2)
truck_2 = Truck("truck 2",START_TIME)

# Loads package data from CSV file into package_data hash table.
#
# Time Complexity: O(n^2)
# Space Complexity: O(1)
def load_package_data(filename, hash):
    # Opens the file.
    with open(filename) as packages:
        packageData = csv.reader(packages, delimiter=',')
        # Copies each line into temporary variable (O(n)).
        for package in packageData:
            id = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zip = package[4]
            # Converts deadline to datetime object.
            deadline = get_deadline(package[5])
            weight = package[6]
            notes = package[7]
            status = "at hub"
            # Updates status for delayed package.
            if(notes == "Delayed on flight---will not arrive to depot until 9:05 am"):
                status = "delayed"
            # Creates new Package object from variables.
            p = Package(id, address, city, state, zip, deadline, weight, notes, status)
            # Inserts package into hash table (O(n)).
            hash.insert(id, p)
            # Adds package to corresponding list.
            add_to_queue(p)

# Loads distance data from CSV into distance_data matrix.
#
# Time Complexity: O(n)
# Space Complexity: O(n^2)
def load_distance_data(file, distance_list):
    # Opens the file.
    with open(file) as distances:
        reader = csv.reader(distances, delimiter=',')
        # Loops through each row in file (O(n))
        for row in reader:
            # Creates a new list containing each item in row, then appends to list.
            distance_data.append(list(float(i) for i in row))

# Adds a package to a list depending on the package's attributes.
#
# Time Complexity: O(1)
# Space Complexity: O(1)
def add_to_queue(p):
    # Adds package to group_queue if it must be delivered with other packages.
    if(p.in_group()):
        group_queue.append(p)
    elif(p.is_delayed()):
        delay_queue.append(p)
    # Adds package to priority_queue if it has a deadline.
    elif(p.has_deadline()):
        priority_queue.append(p)
    # Otherwise adds package to standard_queue.
    else:
        standard_queue.append(p)

# Checks for undelivered packages in package_data hash table.
#
# Time Complexity: O(1)
# Space Complexity: O(1)
def has_undelivered_packages():
    return len(group_queue) > 0 or len(priority_queue) > 0 or len(standard_queue) > 0

# Adds a new status log to the package_log hash table, using log time as the key.
#
# Time Complexity: O(n)
# Space Complexity: O(1)
def update_package_log(log_time):
    # Creates an empty string to hold the report.
    report = ""
    # Adds all packages in the package_data hash table to the report (O(n)).
    for i in range(len(package_data.table)):
        report += str(package_data.search(i+1)) + "\n"
    # Inserts the report into the package_log hash table, using the time as the key (O(n)).
    package_log.insert(log_time, report)
    # Add the log time to log_times list O(1).
    log_times.append(log_time)

# Finds a datetime object in a sequential list of times that either matches or
# is the next highest match under a time input, using a binary search.
# Since package_log and a truck's status_log are hash tables that use a datetime
# object as a key, this function finds the key to the most recent log without
# going over the time input.
#
# Time complexity: O(log n)
# Space Complexity: O(1)
def get_log_time(list, input):
    if(not list):
        return None
    # Returns earliest time if input matches or is below earliest time.
    if(input <= list[0]):
        return list[0]
    left = 0
    right = len(list) - 1
    # Continues unless the right index is greater or equal to the left (O(n)).
    while(left <= right):
        # Divides the list in half at midpoint (O(log n)).
        mid = (left + right) // 2
        # Returns mid if it matches the input.
        if(list[mid] == input):
            return list[mid]
        else:
            # Moves left if mid is lower than input.
            if(list[mid] < input):
                left = mid + 1
            # Otherwise moves right.
            else:
                right = mid - 1
    # Returns the next highest time below input.
    return list[right]

# Returns the hash table entry for a for a truck's log at the given time.
#
# Time Complexity: O(log n)
# Space Complexity: O(1)
def get_truck_log(truck, time):
    # Gets the nearest time in truck's log_times list (O(log n)).
    log_time = get_log_time(truck.log_times,time)
    # Returns the log from the truck's log hash table (O(n)).
    return truck.status_log.search(log_time)

# Prints a status report that includes the status of all packages and trucks at
# the specified time.
#
# Time Complexity: O(n)
# Space Complexity: O(1)
def get_log(time):
    # Adds a title to the report.
    report = "\nStatus Report: " + str(time) + "\n\n"
    # START of package table.
    report += "Packages in the System:\n\n"
    # Creates format for package table header.
    p_header = "{:2} {:20} {:10} {:20} {:5} {:7} {:8} {:10} {:10} {}\n"
    # Adds header for package table to report.
    report += p_header.format("ID","Address","Deadline","City","Zip","Mass(k)","Status","Truck","Updated","Notes")
    # Adds a separator.
    report += "-"*157 + "\n"
    # Gets the nearest time in log_times list (O(log n)).
    log_time = get_log_time(log_times,time)
    # Retrieves the log in the package_log hash table (O(n)).
    report += package_log.search(log_time)
    # END of package table
    # START of truck table.
    report += "\nTrucks on the Road:\n\n"
    # Creates format for truck table header.
    t_header = "{:9} {:20.20} {:>18} {:>18} {}\n"
    # Adds header for truck table to report.
    report += t_header.format("Truck","Location","Delivered","Mileage","Time")
    # Adds a separator.
    report += "-"*157 + "\n"
    # Gets log entry from truck_1's status log (O(n)).
    truck_1_log = get_truck_log(truck_1, time)
    # Creates a variable to store total_delivered and adds truck_1's total.
    total_delivered = truck_1_log.delivered
    # Creates a variable to store total_mileage and adds truck_1's total.
    total_mileage = truck_1_log.mileage
    # Adds truck_1's log to report.
    report += str(truck_1_log) + "\n"
    # Gets log entry from truck_2's status log (O(n)).
    truck_2_log = get_truck_log(truck_2, time)
    # Adds truck_2's total delivered to total_delivered.
    total_delivered += truck_2_log.delivered
    # Adds truck_2's total mileage to total_mileage.
    total_mileage += truck_2_log.mileage
    # Adds truck_2's log to report.
    report += str(truck_2_log) + "\n"
    # Adds a separator.
    report += "-"*157 + "\n"
    # Adds a row for the totals between the trucks.
    report += "{:9} {:20.20} {:>18} {:>18.1f} {}\n".format("Total","",total_delivered,total_mileage,"")
    # Returns the report.
    return report
