# -*- coding: utf-8 -*-
"""
Trainer GUI class which implements all GUIs necessary for a trainer
to interface with the gym database.

@author: Matthew Khoury
@author: Evan Baldwin
"""

import tkinter as tk
from tkinter import messagebox
from trainer import *

current_trainer_id = None

def show_main_trainer_window():
    global current_trainer_id
    trainer_info = get_trainer_info(current_trainer_id)
    if trainer_info is None:
        messagebox.showerror("Error", "Failed to fetch trainer information.")
        return
    
   # register_window
    #trainer_window = tk.Toplevel(main_window)
    #trainer_window.title("Trainer Dashboard")
    reg_but.destroy()
    log_but.destroy()

    tk.Label(main_window, text=f"Name: {trainer_info[0]}").pack()
    tk.Label(main_window, text=f"Email: {trainer_info[1]}").pack()
    tk.Label(main_window, text=f"Date of Birth: {trainer_info[2]}").pack()
    tk.Label(main_window, text=f"Specialization: {trainer_info[3]}").pack()

    tk.Button(main_window, text="Update Availability", command=update_availability_gui).pack(pady=10)
    tk.Button(main_window, text="Delete Availability", command=delete_availability_gui).pack(pady=10)
    tk.Button(main_window, text="Find Member", command=find_member_gui).pack(pady=10)

def find_member_gui():
    def on_search():
        member_name = entry_name.get()
        member_info = search_member_profiles(member_name)
        if member_info:
            for widget in main_window.winfo_children():
                widget.destroy()
            idLabel=tk.Label(main_window, text=f"Member's ID: {member_info['Member Id']}")
            idLabel.pack()
            nameLable=tk.Label(main_window, text=f"Member's Name: {member_info['Member Name']}")
            nameLable.pack()
            exerciseLabel=tk.Label(main_window, text=f"Member's Email: {member_info['Member Email']}")
            exerciseLabel.pack()
            dateLabel=tk.Label(main_window, text=f"Member's Date of Birth: {member_info['Date of Birth']}")
            dateLabel.pack()
            goalLabel=tk.Label(main_window, text=f"Member's Goal Statement: {member_info['Goal Statement']}")
            goalLabel.pack()
            vwback=tk.Button(main_window, text="Back to Menu", command=lambda: back_to_menu())
            vwback.pack()
        else:
            messagebox.showerror("Search Error", "This member does not exist.")
    
    def back_to_menu():
        for widget in main_window.winfo_children():
            widget.destroy()
        search_window.destroy()
        show_main_trainer_window()
        
    search_window = tk.Toplevel(main_window)
    search_window.title("Find Member")
    tk.Label(search_window, text="Name:").grid(row=0)
    entry_name = tk.Entry(search_window)
    entry_name.grid(row=0, column=1)
    tk.Button(search_window, text="Search", command=on_search).grid(row=1, columnspan=2)

def register_trainer_gui():
    def on_register():
        name = entry_name.get()
        email = eemail.get()
        dob = entry_dob.get()
        password = entry_password.get()
        specialization = entry_specialization.get()
     #   start_time = entry_start.get()  
     #   end_time = entry_end.get()  
        result = register_trainer(name, email, dob, password, specialization)
        
        
        if result:
            messagebox.showinfo("Registration", "Registration successful.")
            register_window.destroy()
            global current_trainer_id
            current_trainer_id = result
            show_main_trainer_window()
            #main_window.destroy()

        else:
            messagebox.showerror("Registration", "Registration failed. Please try again.")

    register_window = tk.Toplevel(main_window)
    register_window.title("Register Trainer")

    tk.Label(register_window, text="Name:").grid(row=0)
    tk.Label(register_window, text="Email:").grid(row=1)
    tk.Label(register_window, text="Date of Birth (YYYY-MM-DD):").grid(row=2)
    tk.Label(register_window, text="Password:").grid(row=3)
    tk.Label(register_window, text="Specialization:").grid(row=4)

    entry_name = tk.Entry(register_window)
    eemail = tk.Entry(register_window)
    entry_dob = tk.Entry(register_window)
    entry_password = tk.Entry(register_window)
    entry_specialization = tk.Entry(register_window)

    entry_name.grid(row=0, column=1)
    eemail.grid(row=1, column=1)
    entry_dob.grid(row=2, column=1)
    entry_password.grid(row=3, column=1)
    entry_specialization.grid(row=4, column=1)

    tk.Button(register_window, text="Register", command=on_register).grid(row=5, columnspan=2)

def login_trainer_gui():
    def on_login():
        email = entry_email.get()
        password = entry_password.get()
        trainer_id = login_trainer(email, password)
        if trainer_id is not None and not isinstance(trainer_id, str):
            messagebox.showinfo("Login", "Login successful.")
            login_window.destroy()
            global current_trainer_id
            current_trainer_id = trainer_id
            show_main_trainer_window()
            #main_window.destroy()

        else:
            messagebox.showerror("Login", "Login failed. Please check your credentials.")

    login_window = tk.Toplevel(main_window)
    login_window.title("Login Trainer")

    tk.Label(login_window, text="Email:").grid(row=0)
    tk.Label(login_window, text="Password:").grid(row=1)

    entry_email = tk.Entry(login_window)
    entry_password = tk.Entry(login_window)

    entry_email.grid(row=0, column=1)
    entry_password.grid(row=1, column=1)

    tk.Button(login_window, text="Login", command=on_login).grid(row=2, columnspan=2)

def update_availability_gui():
    def on_update():
        schedule_id = entry_schedule_id.get()
        start_time = entry_start_time.get()
        end_time = entry_end.get()
        result = update_trainer_availability(schedule_id, start_time, end_time)
        if result == "Availability updated successfully.":
            messagebox.showinfo("Update Availability", result)
            update_window.destroy()
        else:
            messagebox.showerror("Update Availability", result)

    update_window = tk.Toplevel(main_window)
    update_window.title("Update Availability")

    tk.Label(update_window, text="Schedule ID:").grid(row=0)
    tk.Label(update_window, text="Start Time (YYYY-MM-DD HH:MM):").grid(row=1)
    tk.Label(update_window, text="End Time (YYYY-MM-DD HH:MM):").grid(row=2)

    entry_schedule_id = tk.Entry(update_window)
    entry_start_time = tk.Entry(update_window)
    entry_end = tk.Entry(update_window)

    entry_schedule_id.grid(row=0, column=1)
    entry_start_time.grid(row=1, column=1)
    entry_end.grid(row=2, column=1)

    tk.Button(update_window, text="Update", command=on_update).grid(row=3, columnspan=2)

def delete_availability_gui():
    def on_delete():
        schedule_id = entry_schedule_id.get()
        result = delete_trainer_availability(schedule_id)
        if result == "Availability deleted successfully.":
            messagebox.showinfo("Delete Availability", result)
            delete_window.destroy()
        else:
            messagebox.showerror("Delete Availability", result)

    delete_window = tk.Toplevel(main_window)
    delete_window.title("Delete Availability")

    tk.Label(delete_window, text="Schedule ID:").grid(row=0)
    entry_schedule_id = tk.Entry(delete_window)
    entry_schedule_id.grid(row=0, column=1)

    tk.Button(delete_window, text="Delete", command=on_delete).grid(row=1, columnspan=2)

main_window = tk.Tk()
main_window.title("Health and Fitness Club Management System")

reg_but=tk.Button(main_window, text="Register Trainer", command=register_trainer_gui)
reg_but.pack(pady=10)
log_but=tk.Button(main_window, text="Login Trainer", command=login_trainer_gui)
log_but.pack(pady=10)
mem_but=tk.Button(main_window, text="Find Member by Name", command=find_member_gui)

main_window.mainloop()
