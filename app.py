from util import validate_time, clear, print_with_spacing
from data import package_data, load_package_data, distance_data, load_distance_data, truck_1, truck_2, get_log, has_undelivered_packages
# Starts the command-line program.
#
# Time Complexity: O(n^4)
# Space Complexity: O(n^2)
def run_app():
    # Loads package data from CSV into package_data hash table (O(n^2)).
    load_package_data('package.csv', package_data)
    # Loads distance data into distance_data matrix (O(n^2)).
    load_distance_data('distance.csv', distance_data)
    # Creates a new log entry for both trucks arriving at hub (O(n)).
    truck_1.update_log("At hub")
    truck_2.update_log("At hub")
    # Creates variable to store user response (O(1)).
    done = False
    # Continues program until done is true (O(n)).
    while(not done):
        clear()
        # Prints menu options to console (O(1)).
        print("\nWelcome to the PyDelivery System")
        print_with_spacing("\nMenu:")
        print("1. Deliver Packages")
        print("2. View Status Report")
        print("3. Locate Package")
        print("4. Exit")
        print()
        # Gets user menu choice input (O(1)).
        option = input("Chose an option (1,2,3 or 4): ")
        if(option == "1"):
            # Runs algorithm to deliver packages (O(n^3)).
            run_delivery_algorithm()
        elif(option == "2"):
            # Runs method to search for status reports (O(n^2)).
            status_report()
        elif(option == "3"):
            # Runs method to find a package function (O(n^2)).
            package_lookup()
        elif(option == "4"):
            # Exits program (O(1)).
            done = True
        # Alerts user if input is invalid (O(1)).
        else:
            print("Please enter a valid option.")

# Delivers all packages in the package_data hash table by first loading the
# trucks, then delivering each package.  The deliver method returns a report for
# each delivery that is printed to the console.
#
# Time Complexity: O(n^3)
# Space Complexity: O(n)
def run_delivery_algorithm():
    clear()
    # Continues until all packages have been delivered (O(n)).
    while(has_undelivered_packages()):
        # Orders trucks depending on which arrives at hub first.
        # Truck 1 arrives at hub first.
        if(truck_1.time <= truck_2.time):
            # Loads truck 1 with packages (O(n^2)).
            truck_1.load()
            # Delivers truck 1's packages (O(n^2)).
            report = truck_1.deliver()
            # Prints report.
            if(report):
                print(report)
            # Loads truck 2 with packages (O(n^2)).
            truck_2.load()
            # Delivers truck 2's packages (O(n^2)).
            report = truck_2.deliver()
            # Prints report.
            if(report):
                print(report)
        # Truck 2 arrives at hub first.
        else:
            # Loads truck 2 with packages (O(n^2)).
            truck_2.load()
            # Delivers truck 2's packages (O(n^2)).
            report = truck_2.deliver()
            # Prints report.
            if(report):
                print(report)
            # Loads truck 1 with packages (O(n^2)).
            truck_1.load()
            # Delivers truck 1's packages (O(n^2)).
            report = truck_1.deliver()
            # Prints returned report.
            if(report):
                print(report)
    print("Total Packages Delivered: {}".format(truck_1.delivered+truck_2.delivered))
    print("Total Miles Traveled: {:.1f}".format(truck_1.mileage+truck_2.mileage))
    # Creates a new log entry for both trucks returning to hub (O(n)).
    truck_1.update_log("At hub")
    truck_2.update_log("At hub")
    input("\n\nAll packages have been delivered. Press enter to return to menu...")

# Executes algorithm to print status reports at specified times.
#
# Time Complexity: O(n^2)
# Space Complexity: O(1)
def status_report():
    print()
    print("Find a Status Report")
    print("-"*20+"\n")
    # Stores boolean value to continue loop (O(1)).
    done = ""
    # Continues until done (O(n^2))
    while(done != "q"):
        try:
            # Prompts user for time input then converts to datetime object.
            time_input = input("Enter a time (use 24-hr format--e.g., \'825\', \'1515\') or enter 'q' to return to the menu: ")
            # Returns to menu if 'q' is entered.
            if(time_input.lower() == "q"):
                done = "q"
            else:
                # Validates time input.
                time_obj = validate_time(time_input)
                if(time_obj):
                    # Retrieves the status log (O(n)).
                    report = get_log(time_obj)
                    if(report):
                        print(report)
        # Throws exception for invalid input.
        except ValueError:
            print()
            print("Please enter a valid time.")

# Finds a package in the package_data hash table that matches a user-entered id.
#
# Time Complexity: O(n^2)
# Space Complexity: O(1)
def package_lookup():
    # Stores boolean value to continue loop (O(1)).
    done = ""
    # Continues until done (O(n)).
    while(done != "q"):
        try:
            # Prompts user for package id number.
            id_input = input("Enter ID of package to find or enter \'q\' to return to the menu: ")
            # Returns to menu if 'q' is entered.
            if(id_input.lower() == "q"):
                done = "q"
            else:
                # Saves input as int
                id_input = int(id_input)
                # Checks if input id is in hash table.
                if(id_input < 0 or id_input > len(package_data.table)):
                    print_with_spacing("Package with ID={} not found in system.".format(id_input))
                else:
                    # Retrieves the matching package from package_data hash table (O(n)).
                    package = package_data.search(id_input)
                    # Validates package.
                    if(package):
                        # Prints package in a table with column headers.
                        print()
                        format = "{:>2} {:18.18} {:10} {:20} {:5} {:7} {:10} {:8} {:10} {}"
                        print(format.format("ID","Address","Deadline","City","Zip","Mass(k)","Status","Truck","Updated","Notes"))
                        print('-'*157)
                        print(package)
                        print()
        # Throws exception for invalid input.
        except ValueError:
            print_with_spacing("Please enter a valid ID.")
