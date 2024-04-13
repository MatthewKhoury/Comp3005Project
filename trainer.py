# -*- coding: utf-8 -*-
"""
Trainer class which implements all functions necessary to operate 
as a trainer and interface with the database.

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
        return conn
    except psycopg2.DatabaseError as error:
        return None

def add_trainer_availability(trainer_id, start_time, end_time):
    """Allows a trainer to add availability to their schedule."""
    conn = connect()
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO Trainer_Schedules (trainer_id, start_time, end_time)
                VALUES (%s, %s, %s)
                """, (trainer_id, start_time, end_time))
                conn.commit()
                return "Availability added successfully."
    except:
        return "Failed to add availability."
    finally:
        if conn:
            conn.close()

def update_trainer_availability(schedule_id, start_time, end_time):
    """Allows a trainer to update their existing schedule."""
    conn = connect()
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE Trainer_Schedules
                SET start_time = %s, end_time = %s
                WHERE schedule_id = %s
                """, (start_time, end_time, schedule_id))
                conn.commit()
                return "Availability updated successfully."
    except:
        return "Failed to update availability."
    finally:
        if conn:
            conn.close()

def delete_trainer_availability(schedule_id):
    conn = connect()
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                DELETE FROM Trainer_Schedules
                WHERE schedule_id = %s
                """, (schedule_id,))
                conn.commit()
                
                
                
                return "Availability deleted successfully."
    except:
        return "Failed to delete availability."
    finally:
        if conn:
            conn.close()

def search_member_profiles(member_name):
    conn = connect()
    profiles = {}
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT member_id, name, email, date_of_birth, goal_statement
                FROM Members
                WHERE name ILIKE %s
                """, ('%' + member_name + '%',))
                result = cur.fetchone()
                if result:
                    profiles = {
                        "Member Id": result[0],
                        "Member Name": result[1],
                        "Member Email": result[2],
                        "Date of Birth": result[3],
                        "Goal Statement": result[4],
                    }
    except:
        print()
    finally:
        if conn:
            conn.close()
    return profiles
def login_trainer(email, password):
    """Attempt to log in as a trainer with the given email and password."""
    conn = connect()
    trainer_id = None
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT trainer_id FROM Trainers
                WHERE email = %s AND password = %s
                """, (email, password))
                result = cur.fetchone()
                if result:
                    trainer_id = result[0]
                    return trainer_id
                else:
                    return "Invalid email or password."
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
    return trainer_id
def get_trainer_info(trainer_id):
    """Fetch trainer information by their ID."""
    conn = connect()  # Assuming you have a 'connect' function to connect to your database
    try:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT name, email, date_of_birth, specialization
            FROM Trainers
            WHERE trainer_id = %s
            """, (trainer_id,))
            trainer_info = cur.fetchone()
            return trainer_info
    except Exception as error:
        print(f"An error occurred: {error}")
        return None
    finally:
        if conn:
            conn.close()
def register_trainer(name, email, date_of_birth, password, specialization):
    """Register a new trainer with the given details."""
    conn = connect()
    trainer_id=None
    try:
        if conn:
            with conn.cursor() as cur:
                # Check if email already exists
                cur.execute("""
                SELECT email FROM Trainers WHERE email = %s
                """, (email,))
                if cur.fetchone():
                    return "A trainer with this email already exists."

                # Insert new trainer
                cur.execute("""
                INSERT INTO Trainers (name, email, date_of_birth, password, specialization)
                VALUES (%s, %s, %s, %s, %s) RETURNING trainer_id
                """, (name, email, date_of_birth, password, specialization))
                trainer_id = cur.fetchone()[0]
                conn.commit()
                return trainer_id
                #return f"Trainer registered successfully with ID: {trainer_id}"
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
