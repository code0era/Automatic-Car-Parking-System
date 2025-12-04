import sqlite3
import RPi.GPIO as GPIO
import time
from datetime import datetime

# GPIO pin configuration
RED_LED_PIN = 17
GREEN_LED_PIN = 27

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)

def setup_database():
    conn = sqlite3.connect('car_database.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_number TEXT UNIQUE NOT NULL,
            owner_name TEXT NOT NULL,
            is_blacklisted BOOLEAN NOT NULL,
            car_model TEXT,
            date_of_purchase TEXT
        )
    ''')

    conn.commit()
    conn.close()

def check_car(car_number):
    conn = sqlite3.connect('car_database.db')
    cursor = conn.cursor()
    
    # Query the database for car details
    cursor.execute('SELECT owner_name,car_model,date_of_purchase, is_blacklisted FROM cars WHERE car_number = ?', (car_number,))
    result = cursor.fetchone()
    
    if result:
        owner_name,car_model,date_of_purchase, is_blacklisted = result
        if is_blacklisted:
            # Turn on red light and print restriction message
            GPIO.output(RED_LED_PIN, GPIO.HIGH)
            GPIO.output(GREEN_LED_PIN, GPIO.LOW)
            print(' ')
            print(' ')
            print("Red Light - Defaulter's Car!")
            print(' ')
            print("Car information:")
            print(' ')
         # print("Car number {} belonging to {} is blacklisted.".format(car_number,owner_name))
            print("Car number: {} ".format(car_number))
            print("Car owner: {} ".format(owner_name))
            print("Blacklisted Status: {} ".format(is_blacklisted))
            print("Car model: {} ".format(car_model))
            print("Date of purchase: {} ".format(date_of_purchase))
            
            print("xxxxxxxxxxxxxxxxxxxxxx")
            print("Parking is restricted.")
            print("xxxxxxxxxxxxxxxxxxxxxx")
        else:
            # Turn on green light and print access message
            GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
            GPIO.output(RED_LED_PIN, GPIO.LOW)
            print(' ')
            print(' ')
            print("Green Light - Access Granted")
            print(' ')
            print("Car information:")
            print(' ')
           # print("Car number {} belonging to {} is allowed to park.".format(car_number,owner_name))
            print("Car number: {} ".format(car_number))
            print("Car owner: {} ".format(owner_name))
            print("Blacklisted Status: {} ".format(is_blacklisted))
            print("Car model: {} ".format(car_model))
            print("Date of purchase: {} ".format(date_of_purchase))
            print("xxxxxxxxxxxxxxxxxxxxxx")
            print("Parking is Allowed")
            print("xxxxxxxxxxxxxxxxxxxxxx")
    else:
        print("Car not found in the database.")
    
    conn.close()

def add_car():
    conn = sqlite3.connect('car_database.db')
    cursor = conn.cursor()
    
    # Collect car details from the user
    car_number = input("Enter the car number: ")
    owner_name = input("Enter the owner's name: ")
    is_blacklisted = input("Is the car blacklisted? (yes/no): ").strip().lower() == "yes"
    car_model = input("Enter the car model: ")
    date_of_purchase = input("Enter the date of purchase (YYYY-MM-DD): ")
    
    # Validate date format
    try:
        datetime.strptime(date_of_purchase, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Insert data into database
    try:
        cursor.execute('''
            INSERT INTO cars (car_number, owner_name, is_blacklisted, car_model, date_of_purchase)
            VALUES (?, ?, ?, ?, ?)
        ''', (car_number, owner_name, is_blacklisted, car_model, date_of_purchase))
        conn.commit()
        print("Car details added successfully.")
    except sqlite3.IntegrityError:
        print("Car number already exists in the database.")
    
    conn.close()

# Cleanup GPIO at the end
def cleanup():
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.cleanup()

# Main program
if __name__ == "__main__":
    setup_database()
    
    try:
        while True:
            print("\nSelect an option:")
            print("1. Check Car")
            print("2. Add Car Details")
            choice = input("Enter your choice (1 or 2): ")
            
            if choice == '1':
                car_number = input("Enter the car number: ")
                check_car(car_number)
            elif choice == '2':
                add_car()
            else:
                print("Invalid choice. Please select 1 or 2.")
                
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        cleanup()