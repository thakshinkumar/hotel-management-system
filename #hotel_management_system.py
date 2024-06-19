# hotel_management.py

import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('hotel_management.db')
cursor = conn.cursor()

# Create tables
def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY,
        room_number TEXT NOT NULL,
        room_type TEXT NOT NULL,
        price REAL NOT NULL,
        availability INTEGER NOT NULL DEFAULT 1
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        room_id INTEGER,
        check_in_date TEXT NOT NULL,
        check_out_date TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (room_id) REFERENCES rooms(id)
    )
    ''')

    conn.commit()

# CRUD operations
# Create
def add_customer(name, phone):
    cursor.execute('''
    INSERT INTO customers (name, phone) VALUES (?, ?)
    ''', (name, phone))
    conn.commit()

def add_room(room_number, room_type, price):
    cursor.execute('''
    INSERT INTO rooms (room_number, room_type, price) VALUES (?, ?, ?)
    ''', (room_number, room_type, price))
    conn.commit()

def add_booking(customer_id, room_id, check_in_date, check_out_date):
    cursor.execute('''
    INSERT INTO bookings (customer_id, room_id, check_in_date, check_out_date) VALUES (?, ?, ?, ?)
    ''', (customer_id, room_id, check_in_date, check_out_date))
    cursor.execute('''
    UPDATE rooms SET availability = 0 WHERE id = ?
    ''', (room_id,))
    conn.commit()

# Read
def get_customers():
    cursor.execute('SELECT * FROM customers')
    return cursor.fetchall()

def get_rooms():
    cursor.execute('SELECT * FROM rooms')
    return cursor.fetchall()

def get_bookings():
    cursor.execute('SELECT * FROM bookings')
    return cursor.fetchall()

# Update
def update_customer(customer_id, name, phone):
    cursor.execute('''
    UPDATE customers SET name = ?, phone = ? WHERE id = ?
    ''', (name, phone, customer_id))
    conn.commit()

def update_room(room_id, room_number, room_type, price, availability):
    cursor.execute('''
    UPDATE rooms SET room_number = ?, room_type = ?, price = ?, availability = ? WHERE id = ?
    ''', (room_number, room_type, price, availability, room_id))
    conn.commit()

def update_booking(booking_id, customer_id, room_id, check_in_date, check_out_date):
    cursor.execute('''
    UPDATE bookings SET customer_id = ?, room_id = ?, check_in_date = ?, check_out_date = ? WHERE id = ?
    ''', (customer_id, room_id, check_in_date, check_out_date, booking_id))
    conn.commit()

# Delete
def delete_customer(customer_id):
    cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
    conn.commit()

def delete_room(room_id):
    cursor.execute('DELETE FROM rooms WHERE id = ?', (room_id,))
    conn.commit()

def delete_booking(booking_id):
    cursor.execute('''
    DELETE FROM bookings WHERE id = ?
    ''', (booking_id,))
    cursor.execute('''
    UPDATE rooms SET availability = 1 WHERE id = (SELECT room_id FROM bookings WHERE id = ?)
    ''', (booking_id,))
    conn.commit()

# Create the tables
create_tables()

# Example usage
add_customer("John Doe", "1234567890")
add_room("101", "Single", 100.0)
add_booking(1, 1, "2024-06-20", "2024-06-25")

# Print data
print("Customers:", get_customers())
print("Rooms:", get_rooms())
print("Bookings:", get_bookings())

def main():
    while True:
        print("1. Add Customer")
        print("2. Add Room")
        print("3. Add Booking")
        print("4. Show Customers")
        print("5. Show Rooms")
        print("6. Show Bookings")
        print("7. Update Customer")
        print("8. Update Room")
        print("9. Update Booking")
        print("10. Delete Customer")
        print("11. Delete Room")
        print("12. Delete Booking")
        print("0. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            add_customer(name, phone)
        elif choice == 2:
            room_number = input("Enter room number: ")
            room_type = input("Enter room type: ")
            price = float(input("Enter price: "))
            add_room(room_number, room_type, price)
        elif choice == 3:
            customer_id = int(input("Enter customer ID: "))
            room_id = int(input("Enter room ID: "))
            check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
            check_out_date = input("Enter check-out date (YYYY-MM-DD): ")
            add_booking(customer_id, room_id, check_in_date, check_out_date)
        elif choice == 4:
            print("Customers:", get_customers())
        elif choice == 5:
            print("Rooms:", get_rooms())
        elif choice == 6:
            print("Bookings:", get_bookings())
        elif choice == 7:
            customer_id = int(input("Enter customer ID: "))
            name = input("Enter new name: ")
            phone = input("Enter new phone: ")
            update_customer(customer_id, name, phone)
        elif choice == 8:
            room_id = int(input("Enter room ID: "))
            room_number = input("Enter new room number: ")
            room_type = input("Enter new room type: ")
            price = float(input("Enter new price: "))
            availability = int(input("Enter availability (1 for available, 0 for not available): "))
            update_room(room_id, room_number, room_type, price, availability)
        elif choice == 9:
            booking_id = int(input("Enter booking ID: "))
            customer_id = int(input("Enter new customer ID: "))
            room_id = int(input("Enter new room ID: "))
            check_in_date = input("Enter new check-in date (YYYY-MM-DD): ")
            check_out_date = input("Enter new check-out date (YYYY-MM-DD): ")
            update_booking(booking_id, customer_id, room_id, check_in_date, check_out_date)
        elif choice == 10:
            customer_id = int(input("Enter customer ID: "))
            delete_customer(customer_id)
        elif choice == 11:
            room_id = int(input("Enter room ID: "))
            delete_room(room_id)
        elif choice == 12:
            booking_id = int(input("Enter booking ID: "))
            delete_booking(booking_id)
        elif choice == 0:
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()

