# -*- coding: utf-8 -*-
"""
Admin class which implements all funcitons necessary to operate
as an admin and interface with the database.

@author: Matthew Khoury
@author: Evan Baldwin
"""

import psycopg2

dbName = "ProjectV2"
dbUser = "postgres"
dbPass = "admin"
dbHost = "localhost"
dbPort = "5432"

def connect():
    """Connect to the PostgreSQL database server"""
    try:
        conn = psycopg2.connect(dbname=dbName, user=dbUser, password=dbPass, host=dbHost, port=dbPort)
        print("test")
        return conn
    except psycopg2.DatabaseError as error:
        #print(error)
        print()
        return None
    
def admin_login(email, password):
    """Attempt to log in as a trainer with the given email and password."""
    conn = connect()
    trainer_id = None
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT admin_id  FROM Admin_Staff
                WHERE email = %s AND password = %s
                """, (email, password))
                result = cur.fetchone()
                if result:
                    admin_id = result[0]
                    return admin_id
                else:
                    return None
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
    return admin_id

def get_all_equipment():
    """Fetch all equipment from the database."""
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT equipment_id, description FROM Equipment")
            equipment_list = cur.fetchall()
            return equipment_list
    except psycopg2.DatabaseError as error:
        print(f"Database error: {error}")
        return []
    finally:
        if conn:
            conn.close()
            
def add_room_booking(admin_id, start_date, end_date, capacity):
    """Add a new room booking."""
    conn = connect()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO Room_Bookings (admin_id, start_date, end_date, capacity)
                VALUES (%s, %s, %s, %s)
                """, (admin_id, start_date, end_date, capacity))
                conn.commit()
                print("Room booking added successfully.")
        except psycopg2.DatabaseError as error:
            print(f"Error adding room booking: {error}")
        finally:
            conn.close()

def update_equipment(equipment_id, last_checkup, description, issues, admin_id):
    """Update equipment maintenance records."""
    conn = connect()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE Equipment
                SET last_checkup = %s, description = %s, issues = %s, admin_id = %s
                WHERE equipment_id = %s
                """, (last_checkup, description, issues, admin_id, equipment_id))
                conn.commit()
                print("Equipment updated successfully.")
        except psycopg2.DatabaseError as error:
            print(f"Error updating equipment: {error}")
        finally:
            conn.close()
            
def get_all_classes():
    """Fetch all equipment from the database."""
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT class_id, name, schedule, duration FROM Classes")
            class_list = cur.fetchall()
            return class_list
    except psycopg2.DatabaseError as error:
        print(f"Database error: {error}")
        return []
    finally:
        if conn:
            conn.close()

def update_class_schedule(class_id, schedule, duration):
    """Update the schedule for a fitness class."""
    conn = connect()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE Classes
                SET schedule = %s, duration = %s
                WHERE class_id = %s
                """, (schedule, duration, class_id))
                conn.commit()
                print("Class schedule updated successfully.")
        except psycopg2.DatabaseError as error:
            print(f"Error updating class schedule: {error}")
        finally:
            conn.close()

def get_bills(member_id):
    """Retrieve all bills associated with the member."""
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT bill_id, amount_due, due_date, member_id 
            FROM Bills WHERE member_id = %s
            """, (member_id))
            bill_list = cur.fetchall()
            return bill_list
    except psycopg2.DatabaseError as error:
        print(f"Database error: {error}")
        return []
    finally:
        if conn:
            conn.close()

def process_payment(bill_id):
    """Simulate processing a payment and updating the bill."""
    conn = connect()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                DELETE FROM Bills
                WHERE bill_id = %s
                """, (bill_id))
                conn.commit()
        except psycopg2.DatabaseError as error:
            print(f"Error processing payment: {error}")
        finally:
            conn.close()


#add_room_booking(admin_id=1, start_date='2024-05-01', end_date='2024-05-02', capacity=20)
#update_equipment(equipment_id=1, last_checkup='2024-04-12', description='Treadmill', issues='', admin_id=1)
#update_class_schedule(class_id=1, schedule='2024-05-03 08:00:00', duration='01:00:00')
#process_payment(bill_id=1, date='2024-05-01',amount_due=0) 