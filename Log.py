class Log(object):
    # Initializes a log object for truck status reports.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def __init__(self, name, location, delivered, mileage, time):
        self.name = name
        self.location = location
        self.delivered = delivered
        self.mileage = mileage
        self.time = time

    # Overrides standard string method.
    #
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def __str__(self):
        t = self.time.strftime("%I:%M %p")
        f = "{:9} {:60} {:>18} {:>18.1f} {}"
        return f.format(self.name,self.location,self.delivered,self.mileage,t)
