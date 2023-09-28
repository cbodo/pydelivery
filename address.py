def get_address_index(street):
    match street:
        case "4001 S 700 E":
        	return 0
        case "1060 Dalton Ave S":
        	return 1
        case "1330 2100 S":
        	return 2
        case "1488 4800 S":
        	return 3
        case "177 W Price Ave":
        	return 4
        case "195 W Oakland Ave":
        	return 5
        case "2010 W 500 S":
        	return 6
        case "2300 Parkway Blvd":
        	return 7
        case "233 Canyon Rd":
        	return 8
        case "2530 S 500 E":
        	return 9
        case "2600 Taylorsville Blvd":
        	return 10
        case "2835 Main St":
        	return 11
        case "300 State St":
        	return 12
        case "3060 Lester St":
        	return 13
        case "3148 S 1100 W":
        	return 14
        case "3365 S 900 W":
        	return 15
        case "3575 W Valley Central Station Bus Loop":
        	return 16
        case "3595 Main St":
        	return 17
        case "380 W 2880 S":
        	return 18
        case "410 S State St":
        	return 19
        case "4300 S 1300 E":
        	return 20
        case "4580 S 2300 E":
        	return 21
        case "5025 State St":
        	return 22
        case "5100 S 2700 W":
        	return 23
        case "5383 S 900 E #104":
        	return 24
        case "600 E 900 S":
        	return 25
        case "6351 S 900 E":
        	return 26
        case _:
            return 0

def get_street(index):
    match index:
        case 0:
        	return "4001 S 700 E"
        case 1:
        	return "1060 Dalton Ave S"
        case 2:
        	return "1330 2100 S"
        case 3:
        	return "1488 4800 S"
        case 4:
        	return "177 W Price Ave"
        case 5:
        	return "195 W Oakland Ave"
        case 6:
        	return "2010 W 500 S"
        case 7:
        	return "2300 Parkway Blvd"
        case 8:
        	return "233 Canyon Rd"
        case 9:
        	return "2530 S 500 E"
        case 10:
        	return "2600 Taylorsville Blvd"
        case 11:
        	return "2835 Main St"
        case 12:
        	return "300 State St"
        case 13:
        	return "3060 Lester St"
        case 14:
        	return "3148 S 1100 W"
        case 15:
        	return "3365 S 900 W"
        case 16:
        	return "3575 W Valley Central Station Bus Loop"
        case 17:
        	return "3595 Main St"
        case 18:
        	return "380 W 2880 S"
        case 19:
        	return "410 S State St"
        case 20:
        	return "4300 S 1300 E"
        case 21:
        	return "4580 S 2300 E"
        case 22:
        	return "5025 State St"
        case 23:
        	return "5100 S 2700 W"
        case 24:
        	return "5383 S 900 E #104"
        case 25:
        	return "600 E 900 S"
        case 26:
        	return "6351 S 900 E"
        case _:
            return "4001 S 700 E"
