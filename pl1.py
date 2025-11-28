import csv
from collections import defaultdict
from graphics import *

# ------------------- VALIDATION FUNCTIONS -------------------
def validate_airport_code():
    """Prompt user for airport code and validate it"""
    airport_codes = {
        'LHR': 'London Heathrow',
        'MAD': 'Madrid Adolfo Suárez-Barajas',
        'CDG': 'Charles De Gaulle International',
        'IST': 'Istanbul Airport International',
        'AMS': 'Amsterdam Schiphol',
        'LIS': 'Lisbon Portela',
        'FRA': 'Frankfurt Main',
        'FCO': 'Rome Fiumicino',
        'MUC': 'Munich International',
        'BCN': 'Barcelona International'
    }

    while True:
        code = input("Please enter the three-letter code for the departure city required: ").upper()
        if len(code) != 3:
            print("Wrong code length - please enter a three-letter city code")
            continue
        if code not in airport_codes:
            print("Unavailable city code - please enter a valid city code")
            continue
        return code, airport_codes[code]

def validate_year():
    """Prompt user for year and validate it"""
    while True:
        year_input = input("Please enter the year required in the format YYYY: ")
        if not year_input.isdigit():
            print("Wrong data type - please enter a four-digit year value")
            continue
        year = int(year_input)
        if year < 2000 or year > 2025:
            print("Out of range - please enter a value from 2000 to 2025")
            continue
        return year

# ------------------- TASK A -------------------
def task_a():
    """Main function for Task A - handles input validation and file selection"""
    airport_code, airport_name = validate_airport_code()
    year = validate_year()
    selected_data_file = f"{airport_code}{year}.csv"
    print("*" * 70)
    print(f"File {selected_data_file} selected - Planes departing {airport_name} {year}.")
    print("*" * 70)
    return selected_data_file

# ------------------- LOAD & ANALYZE -------------------
def load_data(filename):
    """Load data from CSV file into a list of dictionaries"""
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return []

def analyze_flight_data(data_list):
    """Analyze flight data and calculate all required metrics"""
    total_flights = len(data_list)
    runway1_flights = 0
    long_flights = 0
    ba_flights = 0
    rain_flights = 0
    delayed_flights = 0
    af_flights = 0
    rain_hours = set()
    destination_counts = defaultdict(int)

    airport_names = {
        'LHR': 'London Heathrow',
        'MAD': 'Madrid Adolfo Suárez-Barajas',
        'CDG': 'Charles De Gaulle International',
        'IST': 'Istanbul Airport International',
        'AMS': 'Amsterdam Schiphol',
        'LIS': 'Lisbon Portela',
        'FRA': 'Frankfurt Main',
        'FCO': 'Rome Fiumicino',
        'MUC': 'Munich International',
        'BCN': 'Barcelona International'
    }

    for flight in data_list:
        if flight['RunwayNum'] == '1':
            runway1_flights += 1
        if float(flight['Distance miles']) > 500:
            long_flights += 1
        if flight['FlightNum'].startswith('BA'):
            ba_flights += 1
        if flight['FlightNum'].startswith('AF'):
            af_flights += 1
        if 'rain' in flight['WeatherConditions'].lower():
            rain_flights += 1
            hour = int(flight['ScheduledDeparture'].split(':')[0])
            rain_hours.add(hour)
        if flight['ActualDeparture'] != flight['ScheduledDeparture']:
            delayed_flights += 1
        dest_code = flight['Destination']
        destination_counts[airport_names.get(dest_code, dest_code)] += 1

    avg_flights_per_hour = round(total_flights / 12, 2)
    af_percentage = round((af_flights / total_flights) * 100, 2) if total_flights > 0 else 0
    delayed_percentage = round((delayed_flights / total_flights) * 100, 2) if total_flights > 0 else 0

    max_count = max(destination_counts.values()) if destination_counts else 0
    common_destinations = [dest for dest, count in destination_counts.items() if count == max_count]

    return {
        'total_flights': total_flights,
        'runway1_flights': runway1_flights,
        'long_flights': long_flights,
        'ba_flights': ba_flights,
        'rain_flights': rain_flights,
        'avg_flights_per_hour': avg_flights_per_hour,
        'af_percentage': af_percentage,
        'delayed_percentage': delayed_percentage,
        'rain_hours_count': len(rain_hours),
        'common_destinations': common_destinations
    }

# ------------------- DISPLAY RESULTS -------------------
def display_results(filename, airport_name, year, results):
    """Display the analysis results in the required format"""
    print("*" * 70)
    print(f"File {filename} selected - Planes departing {airport_name} {year}.")
    print("*" * 70)
    print()
    print(f"The total number of flights from this airport was {results['total_flights']}")
    print(f"The total number of flights departing Runway one was {results['runway1_flights']}")
    print(f"The total number of departures of flights over 500 miles was {results['long_flights']}")
    print(f"There were {results['ba_flights']} British Airways flights from this airport")
    print(f"There were {results['rain_flights']} flights from this airport departing in rain")
    print(f"There was an average of {results['avg_flights_per_hour']} flights per hour from this airport")
    print(f"Air France planes made up {results['af_percentage']}% of all departures")
    print(f"{results['delayed_percentage']}% of all departures were delayed")
    print(f"There were {results['rain_hours_count']} hours in which rain fell")
    print(f"The most common destinations are {results['common_destinations']}")
    print("*" * 70)

# ------------------- SAVE RESULTS -------------------
def save_results_to_file(filename, airport_name, year, results):
    """Save analysis results to a text file"""
    try:
        with open("results.txt", "a") as file:
            file.write("*" * 70 + "\n")
            file.write(f"File {filename} selected - Planes departing {airport_name} {year}.\n")
            file.write("*" * 70 + "\n\n")
            file.write(f"The total number of flights from this airport was {results['total_flights']}\n")
            file.write(f"The total number of flights departing Runway one was {results['runway1_flights']}\n")
            file.write(f"The total number of departures of flights over 500 miles was {results['long_flights']}\n")
            file.write(f"There were {results['ba_flights']} British Airways flights from this airport\n")
            file.write(f"There were {results['rain_flights']} flights from this airport departing in rain\n")
            file.write(f"There was an average of {results['avg_flights_per_hour']} flights per hour from this airport\n")
            file.write(f"Air France planes made up {results['af_percentage']}% of all departures\n")
            file.write(f"{results['delayed_percentage']}% of all departures were delayed\n")
            file.write(f"There were {results['rain_hours_count']} hours in which rain fell\n")
            file.write(f"The most common destinations are {results['common_destinations']}\n")
            file.write("*" * 70 + "\n\n")
        print("Results successfully saved to results.txt")
    except Exception as e:
        print(f"Error saving results: {str(e)}")

# ------------------- TASK C -------------------
def task_c(selected_data_file, results):
    """Extract metadata and call save function"""
    airport_code = selected_data_file[:3]
    year = selected_data_file[3:7]
    airport_names = {
        'LHR': 'London Heathrow',
        'MAD': 'Madrid Adolfo Suárez-Barajas',
        'CDG': 'Charles De Gaulle International',
        'IST': 'Istanbul Airport International',
        'AMS': 'Amsterdam Schiphol',
        'LIS': 'Lisbon Portela',
        'FRA': 'Frankfurt Main',
        'FCO': 'Rome Fiumicino',
        'MUC': 'Munich International',
        'BCN': 'Barcelona International'
    }
    airport_name = airport_names.get(airport_code, airport_code)
    save_results_to_file(selected_data_file, airport_name, year, results)

# ------------------- TASK B -------------------
def task_b(selected_data_file):
    """Load, analyze, display, and save flight data"""
    airport_code = selected_data_file[:3]
    year = selected_data_file[3:7]
    airport_names = {
        'LHR': 'London Heathrow',
        'MAD': 'Madrid Adolfo Suárez-Barajas',
        'CDG': 'Charles De Gaulle International',
        'IST': 'Istanbul Airport International',
        'AMS': 'Amsterdam Schiphol',
        'LIS': 'Lisbon Portela',
        'FRA': 'Frankfurt Main',
        'FCO': 'Rome Fiumicino',
        'MUC': 'Munich International',
        'BCN': 'Barcelona International'
    }
    airport_name = airport_names.get(airport_code, airport_code)

    data_list = load_data(selected_data_file)
    if not data_list:
        return {}

    results = analyze_flight_data(data_list)
    display_results(selected_data_file, airport_name, year, results)
    task_c(selected_data_file, results)
    return results

# ------------------- TASK D -------------------
def task_d(selected_data_file, airline_code):
    """Create histogram for selected airline's departures by hour"""
    valid_airlines = ['BA', 'AF', 'AY', 'KL', 'SK', 'TP', 'TK', 'W6', 'U2', 'FR', 'A3', 'SN', 'EK', 'QR', 'IB', 'LH']
    if airline_code.upper() not in valid_airlines:
        print("Unavailable Airline code - please try again")
        return False

    data_list = load_data(selected_data_file)
    if not data_list:
        return False

    airport_code = selected_data_file[:3]
    year = selected_data_file[3:7]
    airport_names = {
        'LHR': 'London Heathrow',
        'MAD': 'Madrid Adolfo Suárez-Barajas',
        'CDG': 'Charles De Gaulle International',
        'IST': 'Istanbul Airport International',
        'AMS': 'Amsterdam Schiphol',
        'LIS': 'Lisbon Portela',
        'FRA': 'Frankfurt Main',
        'FCO': 'Rome Fiumicino',
        'MUC': 'Munich International',
        'BCN': 'Barcelona International'
    }
    airport_name = airport_names.get(airport_code, airport_code)

    hourly_counts = [0] * 12
    for flight in data_list:
        if flight['FlightNum'].startswith(airline_code.upper()):
            hour = int(flight['ScheduledDeparture'].split(':')[0])
            if 0 <= hour < 12:
                hourly_counts[hour] += 1

    max_flights = max(hourly_counts) if max(hourly_counts) > 0 else 1
    win = GraphWin(f"{airline_code} Departures Histogram", 900, 400)
    margin = 60
    graph_width = 900 - 2 * margin
    graph_height = 400 - 2 * margin
    bar_width = graph_width / 18
    gap = 15
    actual_bar_width = bar_width - gap

    title = Text(Point(450, 30), f"{airline_code} Departures from {airport_name} {year}")
    title.setSize(18)
    title.setStyle("bold")
    title.draw(win)

    Line(Point(margin, margin), Point(margin, 350)).draw(win)
    Line(Point(margin, 350), Point(850, 350)).draw(win)

    for hour in range(12):
        x1 = margin + hour * bar_width + gap / 2
        x2 = x1 + actual_bar_width
        y1 = 350
        bar_height = (hourly_counts[hour] / max_flights) * graph_height
        y2 = y1 - bar_height
        Rectangle(Point(x1, y1), Point(x2, y2)).draw(win).setFill("blue")
        Text(Point(x1 + bar_width/2, 370), f"{hour:02d}:00").draw(win)
        if hourly_counts[hour] > 0:
            Text(Point(x1 + bar_width/2, y2 - 15), str(hourly_counts[hour])).draw(win)

    Text(Point(margin - 25, margin + graph_height / 2), "Flights").draw(win)
    win.getMouse()
    win.close()
    return True

# ------------------- TASK E (Main Program Loop) -------------------
def task_e():
    """Main program loop allowing user to process multiple files"""
    while True:
        selected_file = task_a()
        results = task_b(selected_file)

        while True:
            airline_code = input("\nEnter a two-character Airline code to plot a histogram (or 'N' to skip): ").strip().upper()
            if airline_code == 'N':
                break
            if len(airline_code) != 2:
                print("Please enter a valid 2-character airline code")
                continue
            task_d(selected_file, airline_code)

        while True:
            choice = input("\nDo you want to select a new data file? (Y/N): ").strip().upper()
            if choice in ['Y', 'N']:
                break
            print("Please enter Y or N")
        if choice == 'N':
            break
        
        print("\nThank you. End of run.")

# ------------------- MAIN ENTRY POINT -------------------
if __name__ == "__main__":
    task_e()