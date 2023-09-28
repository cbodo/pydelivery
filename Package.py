from datetime import datetime, date, time, timedelta
from util import DELAY_TIME, CORRECT_ADDRESS_TIME, CORRECT_ADDRESS, START_TIME, STOP_TIME
# Package class
class Package(object):
    # Initiales a Package class object with id, address, city, state, zip, deadline,
    # weight, notes, and status passed as parameters.  Also stores time_loaded
    # and time_delivered for each package.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def __init__(self, id, address, city, state, zip, deadline, weight, notes, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.truck = ""
        self.time = START_TIME

    # Overwrites default string method for printing Package class objects.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def __str__(self):
        # Gets format for printing packages (O(1)).
        format = "{:>2} {:18.18} {:10} {:20} {:5} {:7} {:10} {:8} {:10} {}"
        # Gets formatted time string for package deadline (O(1))
        deadline = self.deadline.strftime("%I:%M %p")
        # Gets formatted time string for package status_time (O(1))
        status_time = self.time.strftime("%I:%M %p")
        return format.format(self.id,self.address,deadline,self.city,self.zip,self.weight,self.status,self.truck.capitalize(),status_time,self.notes)

    # Updates a package's status and time when in transit/delivered.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def update_status(self, truck, status, time):
        self.truck = truck
        self.status = status
        self.time = time

    # Updates a package's address.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def update_address(self):
        self.address = CORRECT_ADDRESS["address"]
        self.city = CORRECT_ADDRESS["city"]
        self.state = CORRECT_ADDRESS["state"]
        self.zip = CORRECT_ADDRESS["zip"]
        self.notes = ""

    # Returns true if package is at the hub.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def at_hub(self):
        return self.status == "at hub"

    # Returns true if package must be delivered with other packages.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def in_group(self):
        return ("Must be delivered with" in self.notes or self.id in (13,15,19))

    # Returns true if package deadline is less than EOD.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def has_deadline(self):
        return self.deadline < STOP_TIME

    # Returns true if packages is delayed.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def is_delayed(self):
        return self.status == "delayed"

    # Checks if package can be loaded based on package's attributes.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def is_loadable(self, truck, current_time, eta, duration):
        # Returns false if a delayed package hasn't arrived at hub.
        if(self.status == "delayed"):
            if(current_time < DELAY_TIME):
                return False
            else:
                # Changes package status to "at hub" if package has arrived.
                self.status = "at hub"
                # Checks if package has a deadline.
                if(self.deadline.time() < time(17,0)):
                    # Checks if package will be late based on truck ETA (+10 mins).
                    if((duration + eta + timedelta(minutes=10)) > self.deadline):
                        return False
        # Returns false if package must be on truck 2, but the current truck is
        # not truck 2.
        if(self.notes == "Can only be on truck 2" and truck.lower() != "truck 2"):
            return False
        # Returns false if package has the wrong address and won't get the correct
        # address before the current eta for delivery.
        if(self.notes == "Wrong address listed"):
            if((duration + eta) < CORRECT_ADDRESS_TIME):
                return False
            # Updates address with correct information when it is received.
            if(current_time >= CORRECT_ADDRESS_TIME):
                self.update_address()
        # Returns false if package with deadline will be late based on truck ETA (+10 mins)
        if(self.deadline.time() < time(17,0)):
            if((duration + eta + timedelta(minutes=10)) > self.deadline):
                return False
        return True

    # Checks if a package can be delivered based on package's attributes.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def is_deliverable(self, time):
        # Returns false if package with wrong address cannot be updated.
        if(self.notes == "Wrong address listed"):
            if(time < CORRECT_ADDRESS_TIME):
                return False
            # Updates address with correct information when it is received.
            self.update_address()
        return True
