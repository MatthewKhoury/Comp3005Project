# -*- coding: utf-8 -*-
"""
Member class which implements all functions necessary to operate
as a member of the gym.

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
        print(error)
        return None

def getMemberIdByName(name):
    """Fetch the member_id for a given name from the database."""
    conn = connect()
    memberId = None
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("SELECT member_id FROM Members WHERE name = %s", (name,))
                result = cur.fetchone()
                if result:
                    memberId = result[0]
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
    return memberId

def registerForClass(memberId, classId):
    """Allow a member to register for a group fitness class."""
    conn = connect()
    try:
        if conn:
            with conn.cursor() as cur:
                # Check class capacity
                cur.execute("""
                SELECT COUNT(*) FROM Bookings WHERE class_id = %s
                """, (classId,))
                bookingsCount = cur.fetchone()[0]

                cur.execute("""
                SELECT room_bookings.capacity, room_bookings.room_id, classes.class_id, classes.room_id
                FROM classes
                INNER JOIN room_bookings ON classes.room_id=room_bookings.room_id
                WHERE classes.class_id = %s
                """, (classId,))
                capacity = cur.fetchone()[0]
                if bookingsCount >= capacity:
                    return "Class is full."
                
                # Register for the class
                cur.execute("""
                INSERT INTO Bookings (member_id, class_id)
                VALUES (%s, %s)
                """, (memberId, classId))
                
                # Pay for class
                cur.execute("""
                INSERT INTO Bills (amount_due, due_date, member_id)
                VALUES (%s, CURRENT_DATE + interval '14 days', %s)
                """, (24.99, memberId))
                conn.commit()
                return "Registered for class successfully."
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
        return "Failed to register for the class."
    finally:
        if conn:
            conn.close()

def bookPersonalTrainingSession(memberId, trainerId, sessionDate):
    """Book a personal training session using just the date."""
    conn = connect()
    try:
        if conn:
            with conn.cursor() as cur:
                # Check trainer availability for the date
                cur.execute("""
                SELECT * FROM Sessions
                WHERE trainer_id = %s AND schedule::date = %s
                """, (trainerId, sessionDate))
                if cur.fetchone():
                    return "Trainer is not available on the selected date."
                
                # Book session
                cur.execute("""
                INSERT INTO Sessions (member_id, trainer_id, schedule)
                VALUES (%s, %s, %s)
                """, (memberId, trainerId, sessionDate))
                
                # Pay for session
                cur.execute("""
                INSERT INTO Bills (amount_due, due_date, member_id)
                VALUES (%s, CURRENT_DATE + interval '14 days', %s)
                """, (34.99, memberId))
                conn.commit()
                return "Training session booked successfully."
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
        return "Failed to book the training session."
    finally:
        if conn:
            conn.close()

def registerMember(name, email, dateOfBirth, password, height, weight, avg_bp):
    """Register a new member and return the member_id."""
    conn = connect()
    memberId = None
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO Members (name, email, date_of_birth, password)
                VALUES (%s, %s, %s, %s) RETURNING member_id
                """, (name, email, dateOfBirth, password))
                memberId = cur.fetchone()[0]
                cur.execute("""
                INSERT INTO Health_Metrics (member_id, last_updated, height, weight, avg_blood_pressure)
                VALUES (%s, CURRENT_DATE, %s, %s, %s) 
                """, (memberId, height, weight, avg_bp))
                cur.execute("""
                INSERT INTO Routines (member_id, time_limit, exercise_list, num_reps)
                VALUES (%s, %s, %s, %s) 
                """, (memberId, '003000', 'Pushups, Squats, Situps', 10))
                cur.execute("""
                INSERT INTO Fitness_Achievements (member_id, date_achieved, goal_description)
                VALUES (%s, CURRENT_DATE, %s)
                """, (memberId, 'You started at the gym!'))
                # Pay for membership
                cur.execute("""
                INSERT INTO Bills (amount_due, due_date, member_id)
                VALUES (%s, CURRENT_DATE + interval '14 days', %s)
                """, (54.99, memberId))
                conn.commit()
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
    return memberId

def updateMemberProfile(memberId, email, password):
    """Update member profile information based on the given member_id."""
    conn = connect()
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE Members SET email = %s, password = %s WHERE member_id = %s", (email, password, memberId))
                conn.commit()
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
            
def updateMemberHealth(memberId, height, weight, avg_bp):
    """Update member health metrics based on the given member_id."""
    conn = connect()
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE Health_Metrics SET height = %s, weight = %s, avg_blood_pressure = %s WHERE member_id = %s", (height, weight, avg_bp, memberId))
                conn.commit()
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
    
def updateMemberGoals(memberId, desired_weight, goal_time):
    """Update member goals based on the given member_id."""
    conn = connect()
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Fitness_Goals (member_id, start_date, desired_weight, goal_time) VALUES (%s, CURRENT_DATE, %s, %s)", (memberId, desired_weight, goal_time))
                conn.commit()
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()

def getBillInfo(memberId, billNum):
    """Fetch and return member's current bills."""
    conn = connect()
    billInfo = {}
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT bill_id, amount_due, due_date
                FROM Bills WHERE member_id = %s
                """, (memberId,))
                result = cur.fetchall()
                try:
                    r = result[billNum-1]
                except IndexError:
                    r = False
                if r:
                    billInfo = {
                        "Bill ID": r[0],
                        "Amount Due": r[1],
                        "Due Date": r[2],
                    }
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
    return billInfo

def getDashboard(memberId):
    """Fetch and return member's dashboard information."""
    conn = connect()
    dashboardInfo = {}
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT name, email, date_of_birth, password
                FROM Members WHERE member_id = %s
                """, (memberId,))
                result = cur.fetchone()
                if result:
                    dashboardInfo = {
                        "Name": result[0],
                        "Email": result[1],
                        "Date of Birth": result[2],
                        "Password": result[3],
                    }
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
    return dashboardInfo

def getRoutineInfo(memberId, routNum):
    """Fetch and return member's routine information."""
    conn = connect()
    routineInfo = {}
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT routine_number, time_limit, exercise_list, num_reps
                FROM Routines WHERE member_id = %s
                """, (memberId,))
                result = cur.fetchall()
                try:
                    r = result[routNum-1]
                except IndexError:
                    r = False
                if r:
                    routineInfo = {
                        "Routine Number": r[0],
                        "Time Limit": r[1],
                        "Exercises": r[2],
                        "Num of Reps": r[3],
                    }
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
    return routineInfo

def getGoalInfo(memberId, goalNum):
    """Fetch and return member's fitness goals information."""
    conn = connect()
    goalInfo = {}
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT goal_number, start_date, desired_weight, goal_time
                FROM Fitness_Goals WHERE member_id = %s
                """, (memberId,))
                result = cur.fetchall()
                try:
                    r = result[goalNum-1]
                except IndexError:
                    r = False
                if r:
                    goalInfo = {
                        "Goal Number": r[0],
                        "Start Date": r[1],
                        "Weight": r[2],
                        "Goal Time": r[3],
                    }
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
    return goalInfo

def getAchievementsInfo(memberId, achieveNum):
    """Fetch and return member's fitness achievements information."""
    conn = connect()
    goalInfo = {}
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT achievement_num, date_achieved, goal_description
                FROM Fitness_Achievements WHERE member_id = %s
                """, (memberId,))
                result = cur.fetchall()
                try:
                    r = result[achieveNum-1]
                except IndexError:
                    r = False
                if r:
                    goalInfo = {
                        "Achieve Num": r[0],
                        "Date Achieved": r[1],
                        "Description": r[2],
                    }
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
    return goalInfo

def getHealthInfo(memberId):
    """Fetch and return member's health metrics information."""
    conn = connect()
    goalInfo = {}
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT last_updated, height, weight, avg_blood_pressure
                FROM Health_Metrics WHERE member_id = %s
                """, (memberId,))
                result = cur.fetchone()
                if result:
                    goalInfo = {
                        "Last Date": result[0],
                        "Height": result[1],
                        "Weight": result[2],
                        "Avg BP": result[3],
                    }
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
    return goalInfo

def validate_password(member_id, password):
    conn = connect()
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT password
                FROM Members WHERE member_id = %s
                """, (member_id,))
                result = cur.fetchone()
                if result[0] == password:
                    return True
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
    finally:
        if conn:
            conn.close()
    return False

def main():
    memberId = getMemberIdByName("John Doe")
    trainerId = 1  # Assuming you know the trainer's ID
    classId = 1    # Assuming you know the class ID

    # Book a personal training session
    sessionDate = "2028-05-10"  # YYYY-MM-DD format
    print(bookPersonalTrainingSession(memberId, trainerId, sessionDate))

    # Register for a group fitness class
    print(registerForClass(memberId, classId))

if __name__ == "__main__":
    main()