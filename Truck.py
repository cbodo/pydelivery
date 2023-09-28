import data
from datetime import datetime, date, time, timedelta
from util import HUB, START_TIME, DELAY_TIME
from HashTable import HashTable
from Log import Log
from address import get_address_index,get_street

class Truck(object):
    # Initializes a Truck class object with passed name and time fields and
    # an optional field averate_rate that defaults to 18 MPH.  Truck objects
    # can also store a list of package objects, the total mileage driven, the
    # total number of deliveries completed, and the number of delivery runs
    # completed.
    #
    # Time Complexity: O(n)
    # Space Complexity: O(n^2)
    def __init__(self, name, time, rate=18):
        self.name = name
        self.time = time
        self.rate = rate
        self.packages = []
        self.mileage = 0
        self.eta = time
        self.delivered = 0
        self.run = 0
        self.status_log = HashTable(44)
        self.log_times = []

    # Overrides the standard string function of Truck class for cleaner print.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def __str__(self):
        format = "{:9} {:>18} {:>18.1f} {:>18}"
        time_string = self.time.strftime("%I:%M %p")
        return format.format(self.name.capitalize(),self.delivered,self.mileage,time_string)

    # Updates the truck's current time by adding the duration between two stops.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def update_time(self, distance):
        if(distance == 0):
            return
        # Adds delivery duration to truck's current time (O(1)).
        self.time = self.time + self.duration(distance,self.rate)

    # Gets the distance between two addresses.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def distance(self, address_1, address_2):
        return data.distance_data[get_address_index(address_1)][get_address_index(address_2)]

    # Calculates duration based on distance and rate.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def duration(self, distance, rate):
        # Divides distance by rate (O(1)).
        dur = distance/rate
        # Returns result as a timedelta object (O(1)).
        return timedelta(hours=dur)

    # Gets the next closest package that can be loaded.
    #
    # Time Complexity: O(n)
    # Space Complexity: O(1)
    def min_distance(self, address, list):
        # Initializes an empty object p to store package result (O(1)).
        closest = None
        # Initializes min with number larger than all distances  number to compare.
        min = 10000
        # Loops through list to find minimum distance, skipping hub (i=0) (O(n)).
        for p in list:
            # Gets the distance between the input address and the current package address.
            d = self.distance(address,p.address)
            # Checks if distance is less than current min and if package is loadable.
            if(d < min):
                # Saves distance in min and package in closest.
                min = d
                closest = p
        # Returns package
        return closest

    # Creates a new log in the truck's status_log hash table.  Creates a new log
    # in the package_log hash table.
    #
    # Time Complexity: O(n)
    # Space Complexity: O(1)
    def update_log(self, location):
        # Initializes a new log object with the truck's data.
        log = Log(self.name,location,self.delivered,self.mileage,self.time)
        # Inserts log into the hash table using the truck's time as the key (O(n)).
        self.status_log.insert(self.time,log)
        # Adds the log time to the log_times list.
        self.log_times.append(self.time)
        # Updates package_log hash table (O(n)).
        data.update_package_log(self.time)


    # Adds a package to a truck's package list and updates the truck's running
    # eta, then updates the package information in the package_data hash table.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def load_package(self, package, distance=0):
        self.packages.append(package)
        self.eta = self.eta + self.duration(distance,self.rate)
        package.update_status(self.name,"in transit",self.time)

    # Loads a list of packages onto a truck.
    #
    # Time Complexity: O(n^2)
    # Space Complexity: O(n)
    def load_packages(self, list):
        # Initializes a queue and copies passed list into it (O(n)).
        queue = []
        for p in list:
            queue.append(p)
        # Creates a variable to store the first package to load.
        first = None
        # Creates a variable to store the distance for the first package.
        dist = 0
        # Checks if truck has any packages.
        if(len(self.packages) > 0):
            # Gets package nearest to previous package (O(n)).
            first = self.min_distance(self.packages[-1].address,queue)
            # Get distance between the two addresses.
            dist = self.distance(self.packages[-1].address,first.address)
        else:
            # Gets package nearest to hub (O(n)).
            first = self.min_distance(HUB,queue)
            # Gets distance between the two addresses.
            dist = self.distance(HUB,first.address)
        # Copies first into current.
        current = first
        # Adds first to truck's package list.
        self.load_package(first,dist)
        # Removes first from the queue.
        queue.remove(first)
        # Removes from passed list.
        list.remove(first)
        # Loops through queue (O(n))
        while(len(queue) > 0):
            # Finds package nearest to current (O(n))
            next = self.min_distance(current.address,queue)
            # Gets distance between the two addresses (O(1)).
            dist = self.distance(current.address,next.address)
            # Gets duration for eta check (O(1)).
            dur = self.duration(dist,self.rate)
            # Checks truck is not empty and package can be loaded at current time (O(1)).
            if(len(self.packages) < 16 and next.is_loadable(self.name,self.time,self.eta,dur)):
                # Adds next to truck's package list O(1).
                self.load_package(next,dist)
                # Removes from list O(1).
                list.remove(next)
            # Copies next into current.
            current = next
            # Removes next from the queue.
            queue.remove(next)

    # Loads truck with packages in package_data hash table..
    #
    # Time Complexity: O(n^2)
    # Space Complexity: O(n)
    def load(self):
        # Loads all delayed packages if they have arrived at hub (O(n^2)).
        if(self.time > DELAY_TIME and len(data.delay_queue) > 0):
            self.load_packages(data.delay_queue)
        # Loads all grouped packages (O(n^2)).
        if(len(data.group_queue) > 0):
            self.load_packages(data.group_queue)
        # Loads all priority packages (O(n^2)).
        if(len(data.priority_queue) > 0):
            self.load_packages(data.priority_queue)
        # Loads all standard packages (O(n^2)).
        if(len(data.standard_queue) > 0):
            self.load_packages(data.standard_queue)
        # Updates status log O(n).
        self.update_log("In Transit")

    # Delivers the current package.
    #
    # Time Complexity: O(n)
    # Space Complexity: O(1)
    def deliver_package(self, package, distance):
        # Increments the truck's total delivered counter (O(1)).
        self.delivered += 1
        # Increments the truck's total mileage counter (O(1)).
        self.mileage += distance
        # Updates the truck's current time (O(1)).
        self.update_time(distance)
        # Updates the package status to "delivered" and time of status change (O(1)).
        package.update_status(self.name,"delivered",self.time)
        # Updates truck's status_log and package_log (O(n)).
        self.update_log("Delivering: " + package.address)
        # Removes package from truck.
        self.packages.remove(package)

    # Greedy Algorithm--Utilizes a greedy algorithm to deliver packages by finding
    # the next nearest address at time of delivery.
    #
    # Time Complexity: O(n^2)
    # Space Complexity: O(1)
    def deliver(self):
        # Returns None if truck is empty.
        if(len(self.packages) == 0):
            return None
        # Incremenets truck's run counter.
        self.run += 1
        # Copies current time into time_left for report.
        time_left = self.time
        # Copies total number of packages on truck for report.
        total_packages = len(self.packages)
        # Gets package nearest to hub (O(n)).
        first = self.min_distance(HUB,self.packages)
        # Gets distance between the two addresses.
        dist = self.distance(HUB,first.address)
        # Creates variable to track total distance and adds dist.
        total_distance = dist
        # Copies first into current.
        current = first
        # Delivers the first package (O(n)).
        self.deliver_package(first,dist)
        # Creates package report string and adds first package.
        package_report = "  " + str(first) + "\n"
        # Continues until truck is empty (O(n))
        while(len(self.packages) > 0):
            # Gets package nearest to current (O(n)).
            next = self.min_distance(current.address,self.packages)
            # Gets distance between the two addresses.
            dist = self.distance(current.address,next.address)
            # Checks if package can be delivered at current time (O(1)).
            if(next.is_deliverable(self.time)):
                # Delivers the next package (O(n))
                self.deliver_package(next,dist)
                # Adds dist to total_distance.
                total_distance += dist
            # Copies next into current.
            current = next
            # dds package string to delivery report.
            package_report += "  " + str(next) + "\n"
        # Gets distance between last delivery and hub.
        dist = self.distance(current.address,HUB)
        # Adds dist to total_distance.
        total_distance += dist
        # Adds dist to truck's total mileage counter.
        self.mileage += dist
        # Increments truck's time.
        self.update_time(dist)
        # Creates format for hub return string.
        format = "  {:>2} {:18.18} {:10} {:20} {:5} {:7} {:10} {:8} {:%-I:%M %p} {}\n"
        # Adds hub return to package_report.
        package_report += format.format("","Returned to hub","","","","","","",self.time,"")
        # Updates package_log and truck's status_log hash tables (O(n)).
        self.update_log("At hub")
        # Returns report
        return self.delivery_report(package_report,total_packages,total_distance,time_left)

    # Returns a string report of packages delivered by truck.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def delivery_report(self,packages,delivered,mileage,time_left):
        # Adds a separator.
        report = "="*159 + "\n"
        # Creates string for a delivery report.
        report += "{}, Run #{} - Delivery Report:\n\n".format(self.name.capitalize(),self.run)
        # Creates format for truck's status.
        format = "  Packages delivered: {}\n  Distance traveled: {:.1f} miles\n  Left hub at: {:%-I:%M %p}\n  Returned to hub at: {:%-I:%M %p}\n\n"
        # Adds trucks status to report.
        report += format.format(delivered,mileage,time_left,self.time)
        # Creates format for package header.
        format = "  {:>2} {:20.20} {:10} {:20} {:5} {:7} {:10} {:8} {:10} {}\n"
        # Adds header for package table to report.
        report += format.format("ID","Address","Deadline","City","Zip","Mass(k)","Status","Truck","Updated at","Notes")
        # Adds a separator.
        report += "  " + "-"*157 + "\n"
        # Adds package report to report.
        report += packages
        # Returns report.
        return report
