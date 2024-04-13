# -*- coding: utf-8 -*-
"""
Getter class which retrieves necessary information from the
gym database.

@author: Matthew Khoury
"""
from member import *

def fetch_all_trainers():
    """Fetch all trainer IDs from the database."""
    conn = connect()
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("SELECT trainer_id, name FROM Trainers ORDER BY name")
                trainers = cur.fetchall()
                return trainers
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
        return []
    finally:
        if conn:
            conn.close()
            
            
def fetch_all_classes():
    conn = connect()
    try:
        if conn:
            with conn.cursor() as cur:
                cur.execute("SELECT class_id, name FROM Classes ORDER BY name")
                classes = cur.fetchall()
                return classes
    except psycopg2.DatabaseError as error:
        print(f"An error occurred: {error}")
        return []
    finally:
        if conn:
            conn.close()