# -*- coding: utf-8 -*-
"""
Admin GUI class which implements all GUIs necessary for an admin
to interface with the gym database.

@author: Matthew Khoury
@author: Evan Baldwin
"""

import tkinter as tk
from tkinter import messagebox
from admin import *
from datetime import date

current_admin_id = None

def show_main_admin_window():
    global current_admin_id
    print(current_admin_id)

    if current_admin_id is None:
        messagebox.showerror("Error", "Failed to fetch admin information.")
        return

    for widget in main_window.winfo_children():
        widget.destroy()
    # Display admin dashboard options
    tk.Label(main_window, text="Admin Dashboard").pack()

    tk.Button(main_window, text="Add Room Booking", command=add_room_booking_gui).pack(pady=10)
    tk.Button(main_window, text="Update Equipment", command=update_equipment_gui).pack(pady=10)
    tk.Button(main_window, text="Update Class Schedule", command=update_class_schedule_gui).pack(pady=10)
    tk.Button(main_window, text="Process Payment", command=process_payment_gui).pack(pady=10)

def login_admin_gui():
    def on_login():
        email = email_entry.get()
        password = password_entry.get()
        global current_admin_id
        current_admin_id = admin_login(email, password)
        if current_admin_id:
            messagebox.showinfo("Login", "Login successful.")
            login_window.destroy()
            show_main_admin_window()
        else:
            messagebox.showerror("Login", "Login failed. Please check your credentials.")

    login_window = tk.Toplevel(main_window)
    login_window.title("Admin Login")

    tk.Label(login_window, text="Email:").grid(row=0)
    tk.Label(login_window, text="Password:").grid(row=1)

    email_entry = tk.Entry(login_window)
    password_entry = tk.Entry(login_window, show="*")

    email_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    login_button=tk.Button(login_window, text="Login", command=on_login)
    login_button.grid(row=2, columnspan=2)
    

def add_room_booking_gui():
    def on_booking():
        try:
            start_date = entry_start.get()
            end_date = entry_end.get()
            capacity = entry_cap.get()
            admin_id = current_admin_id
            add_room_booking(admin_id, start_date, end_date, capacity)
            messagebox.showinfo("Success", "Room booked successfully.")
            add_window.destroy()
        except:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    add_window = tk.Toplevel(main_window)
    add_window.title("Add Room Booking")
    tk.Label(add_window, text="Start Date:").grid(row=0)
    tk.Label(add_window, text="End Date:").grid(row=1)
    tk.Label(add_window, text="Capacity:").grid(row=2)
    
    entry_start = tk.Entry(add_window)
    entry_end = tk.Entry(add_window)
    entry_cap = tk.Entry(add_window)
    
    entry_start.grid(row=0, column=1)
    entry_end.grid(row=1, column=1)
    entry_cap.grid(row=2, column=1)
    
    tk.Button(add_window, text="Add Booking", command=on_booking).grid(row=3, columnspan=2)


def update_equipment_gui():
    def on_entry():
        def on_update():
            try:
                equipment_id = int(equipment_id_entry.get())
                last_checkup = last_checkup_entry.get()
                description = description_entry.get()
                issues = issues_entry.get()
                admin_id = current_admin_id
                update_equipment(equipment_id, last_checkup, description, issues, admin_id)
                messagebox.showinfo("Success", "Equipment updated successfully.")
                update_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        equipment_id_to_update = id_entry.get()
        if equipment_id_to_update:
            select_window.destroy()
            update_window = tk.Toplevel(main_window)
            update_window.title("Update Equipment")

            tk.Label(update_window, text="Last Checkup (YYYY-MM-DD):").grid(row=0, column=0)
            tk.Label(update_window, text="Description:").grid(row=1, column=0)
            tk.Label(update_window, text="Issues (optional):").grid(row=2, column=0)
            tk.Label(update_window, text="Equipment ID:").grid(row=3, column=0)

            equipment_id_entry = tk.Entry(update_window)
            equipment_id_entry.insert(0, str(equipment_id_to_update))
            equipment_id_entry.grid(row=3, column=1)
            equipment_id_entry.config(state='readonly')

            last_checkup_entry = tk.Entry(update_window)
            last_checkup_entry.grid(row=0, column=1)

            description_entry = tk.Entry(update_window)
            description_entry.grid(row=1, column=1)

            issues_entry = tk.Entry(update_window)
            issues_entry.grid(row=2, column=1)

            tk.Button(update_window, text="Update", command=on_update).grid(row=4, columnspan=2)
            
    equipment_list = get_all_equipment()
    if not equipment_list:
        messagebox.showerror("Error", "Failed to fetch equipment list.")
        return

    select_window = tk.Toplevel(main_window)
    select_window.title("Select Equipment to Update")

    tk.Label(select_window, text="ID - Description").pack()
    for equipment in equipment_list:
        tk.Label(select_window, text=f"{equipment[0]} - {equipment[1]}").pack()
        
    tk.Label (select_window, text="Enter the ID of the equipment to update:").pack()
    id_entry = tk.Entry(select_window)
    id_entry.pack()
    
    tk.Button(select_window, text="Select", command=on_entry).pack()
    

def update_class_schedule_gui():
    def on_entry():
        def on_update():
            try:
                class_id = int(class_id_entry.get())
                schedule = schedule_entry.get()
                duration = duration_entry.get()
                update_class_schedule(class_id, schedule, duration)
                messagebox.showinfo("Success", "Class updated successfully.")
                update_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        class_id_to_update = id_entry.get()
        if class_id_to_update:
            select_window.destroy()
            update_window = tk.Toplevel(main_window)
            update_window.title("Update Class")

            tk.Label(update_window, text="New Schedule (YYYY-MM-DD):").grid(row=0, column=0)
            tk.Label(update_window, text="New Duration (hhmmss):").grid(row=1, column=0)
            tk.Label(update_window, text="Class ID:").grid(row=2, column=0)

            class_id_entry = tk.Entry(update_window)
            class_id_entry.insert(0, str(class_id_to_update))
            class_id_entry.grid(row=2, column=1)
            class_id_entry.config(state='readonly')

            schedule_entry = tk.Entry(update_window)
            schedule_entry.grid(row=0, column=1)

            duration_entry = tk.Entry(update_window)
            duration_entry.grid(row=1, column=1)

            tk.Button(update_window, text="Update", command=on_update).grid(row=3, columnspan=2)
            
    class_list = get_all_classes()
    if not class_list:
        messagebox.showerror("Error", "Failed to fetch class list.")
        return

    select_window = tk.Toplevel(main_window)
    select_window.title("Select Class to Update")

    tk.Label(select_window, text="Class ID - Name - Schedule - Duration").pack()
    for classes in class_list:
        tk.Label(select_window, text=f"{classes[0]} - {classes[1]} - {classes[2]} - {classes[3]}").pack()
        
    tk.Label (select_window, text="Enter the ID of the class to update:").pack()
    id_entry = tk.Entry(select_window)
    id_entry.pack()
    
    tk.Button(select_window, text="Select", command=on_entry).pack()

def process_payment_gui():
    def on_entry():
        def on_update():
            try:
                bill_id = id_entry.get()
                process_payment(bill_id)
                messagebox.showinfo("Success", "Bill successfully processed.")
                select_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                
        bill_list = get_bills(member_entry.get())
        if not bill_list:
            messagebox.showerror("Error", "Failed to fetch bill list.")
            return
    
        select_window = tk.Toplevel(main_window)
        select_window.title("Select Bill to Process")
    
        tk.Label(select_window, text="Bill ID - Amount Due - Due Date - Member ID").pack()
        for bills in bill_list:
            tk.Label(select_window, text=f"{bills[0]} - {bills[1]} - {bills[2]} - {bills[3]}").pack()
            
        tk.Label (select_window, text="Enter the ID of the bill to process").pack()
        id_entry = tk.Entry(select_window)
        id_entry.pack()
        
        tk.Button(select_window, text="Select", command=on_update).pack()
    
    bill_window = tk.Toplevel(main_window)
    bill_window.title("Bill Member")

    tk.Label(bill_window, text="Enter Member ID:").grid(row=0)

    member_entry = tk.Entry(bill_window)

    member_entry.grid(row=0, column=1)

    enter_button=tk.Button(bill_window, text="Select", command=on_entry)
    enter_button.grid(row=1, columnspan=2)

main_window = tk.Tk()
main_window.title("Admin Management System")

log_button = tk.Button(main_window, text="Login Admin", command=login_admin_gui)
log_button.pack(pady=10)

main_window.mainloop()
