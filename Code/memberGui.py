# -*- coding: utf-8 -*-
"""
Member GUI class which implements all GUIs necessary to member
to interface with the gym database.

@author: Matthew Khoury
@author: Evan Baldwin
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from member import *
from getters import *

def login():
    member_name = entry_name.get()
    member_id = getMemberIdByName(member_name)
    if member_id:
        check_password(member_id, 1)
    else:
        response = messagebox.askyesno("Login Failed", f"Member '{member_name}' not found. Would you like to register?")
        if response:
            register_new_member()
#tk.Button(app, text="Register", command=register_member(name, email, dob, goal, metric))

def check_password(member_id, attempts):
    if attempts >= 4:
        messagebox.showinfo("Login failed", "Too many failed attempts, exiting..")
        app.destroy()
    password = simpledialog.askstring("Login", "Enter your password:")
    correct = validate_password(member_id, password)
    if correct:
        display_dashboard(member_id)
    else:
        messagebox.showinfo("Login", "Incorrect password: please try again.")
        check_password(member_id, attempts+1)
    
def register_new_member():
    name = simpledialog.askstring("Register", "Enter your full name:")
    
    email = simpledialog.askstring("Register", "Enter your email:")
    date_of_birth = simpledialog.askstring("Register", "Enter your date of birth (YYYY-MM-DD):")
    password = simpledialog.askstring("Register", "Enter your password (max 20 characters):")
    height = simpledialog.askstring("Register", "Enter your current height (inches):")
    weight = simpledialog.askstring("Register", "Enter your current weight (pounds):")
    avg_bp = simpledialog.askstring("Register", "Enter your expected average blood pressure:")
    
    if all([name, email, date_of_birth, password, height, weight, avg_bp]):  # Basic check to ensure all fields are filled
        member_id = registerMember(name, email, date_of_birth, password, height, weight, avg_bp)
        if member_id:
            messagebox.showinfo("Registration Successful", f"You have been registered. Your member ID is {member_id}.")
            display_dashboard(member_id)
        else:
            messagebox.showerror("Registration Failed", "An error occurred during registration.")
    else:
        messagebox.showerror("Registration Failed", "All fields are required to register.")

def view_routines(member_id, routineNum):
    routine_info = getRoutineInfo(member_id, routineNum)
    if routine_info:
        for widget in userDashboard.winfo_children():
            widget.destroy()
        idLabel=tk.Label(userDashboard, text=f"Routine Number: {routine_info['Routine Number']}")
        idLabel.pack()
        timeLable=tk.Label(userDashboard, text=f"Time Limit: {routine_info['Time Limit']}")
        timeLable.pack()
        exerciseLabel=tk.Label(userDashboard, text=f"Exercise List : {routine_info['Exercises']}")
        exerciseLabel.pack()
        repsLabel=tk.Label(userDashboard, text=f"Number of Reps: {routine_info['Num of Reps']}")
        repsLabel.pack()
        nextBut=tk.Button(userDashboard, text="Next Routine", command=lambda:view_routines(member_id, routineNum+1))
        nextBut.pack()
        if routineNum > 1:
            backBut=tk.Button(userDashboard, text="Previous Routine", command=lambda:view_routines(member_id, routineNum-1))
            backBut.pack()
        vwback=tk.Button(userDashboard, text="Back to Menu", command=lambda: display_dashboard(member_id))
        vwback.pack()
        
    else:
        messagebox.showerror("Routine Error", "This routine does not exist.")
    
def view_goals(member_id, goalNum):
    goal_info = getGoalInfo(member_id, goalNum)
    if goal_info:
        for widget in userDashboard.winfo_children():
            widget.destroy()
        idLabel=tk.Label(userDashboard, text=f"Goal Number: {goal_info['Goal Number']}")
        idLabel.pack()
        dateLable=tk.Label(userDashboard, text=f"Start Date: {goal_info['Start Date']}")
        dateLable.pack()
        weightLabel=tk.Label(userDashboard, text=f"Goal Weight: {goal_info['Weight']}")
        weightLabel.pack()
        timeLabel=tk.Label(userDashboard, text=f"Goal Time: {goal_info['Goal Time']}")
        timeLabel.pack()
        nextBut=tk.Button(userDashboard, text="Next Goal", command=lambda:view_goals(member_id, goalNum+1))
        nextBut.pack()
        if goalNum > 1:
            backBut=tk.Button(userDashboard, text="Previous Goal", command=lambda:view_goals(member_id, goalNum-1))
            backBut.pack()
        vwback=tk.Button(userDashboard, text="Back to Menu", command=lambda: display_dashboard(member_id))
        vwback.pack()
        
    else:
        messagebox.showerror("Goal Error", "Error with retrieving goals, goal does not exist.")
    
def view_achievements(member_id, achieveNum):
    achievement_info = getAchievementsInfo(member_id, achieveNum)
    if achievement_info:
        for widget in userDashboard.winfo_children():
            widget.destroy()
        idLabel=tk.Label(userDashboard, text=f"Achievement Number: {achievement_info['Achieve Num']}")
        idLabel.pack()
        dateLable=tk.Label(userDashboard, text=f"Date Achieved: {achievement_info['Date Achieved']}")
        dateLable.pack()
        descLabel=tk.Label(userDashboard, text=f"Description: {achievement_info['Description']}")
        descLabel.pack()
        nextBut=tk.Button(userDashboard, text="Next Achievement", command=lambda:view_achievements(member_id, achieveNum+1))
        nextBut.pack()
        if achieveNum > 1:
            backBut=tk.Button(userDashboard, text="Previous Achievement", command=lambda:view_achievements(member_id, achieveNum-1))
            backBut.pack()
        vwback=tk.Button(userDashboard, text="Back to Menu", command=lambda: display_dashboard(member_id))
        vwback.pack()
        
    else:
        messagebox.showerror("Achievement Error", "This acheivement does not exist.")
    
def view_health(member_id):
    health_info = getHealthInfo(member_id)
    if health_info:
        for widget in userDashboard.winfo_children():
            widget.destroy()
        idLabel=tk.Label(userDashboard, text=f"Member ID: {member_id}")
        idLabel.pack()
        dateLable=tk.Label(userDashboard, text=f"Last Updated: {health_info['Last Date']}")
        dateLable.pack()
        heightLabel=tk.Label(userDashboard, text=f"Height (inches): {health_info['Height']}")
        heightLabel.pack()
        weightLable=tk.Label(userDashboard, text=f"Weight (pounds): {health_info['Weight']}")
        weightLable.pack()
        avgbpLabel=tk.Label(userDashboard, text=f"Average Blood Pressure: {health_info['Avg BP']}")
        avgbpLabel.pack()
        vwback=tk.Button(userDashboard, text="Back to Menu", command=lambda: display_dashboard(member_id))
        vwback.pack()
        
    else:
        messagebox.showerror("Dashboard Error", "Unable to fetch dashboard information.")

def display_bills(member_id, billNum):
    bill_info = getBillInfo(member_id, billNum)
    if bill_info:
        for widget in userDashboard.winfo_children():
            widget.destroy()
        idLabel=tk.Label(userDashboard, text=f"Bill ID: {bill_info['Bill ID']}")
        idLabel.pack()
        dateLable=tk.Label(userDashboard, text=f"Amount Due: {bill_info['Amount Due']}")
        dateLable.pack()
        heightLabel=tk.Label(userDashboard, text=f"Due Date: {bill_info['Due Date']}")
        heightLabel.pack()
        nextBut=tk.Button(userDashboard, text="Next Bill", command=lambda:display_bills(member_id, billNum+1))
        nextBut.pack()
        if billNum > 1:
            backBut=tk.Button(userDashboard, text="Previous Bill", command=lambda:display_bills(member_id, billNum-1))
            backBut.pack()
        vwback=tk.Button(userDashboard, text="Back to Menu", command=lambda: display_dashboard(member_id))
        vwback.pack()
    else:
        messagebox.showerror("Bill Error", "This bill does not exist.")
    
def update_profile(member_id):
    current_info = getDashboard(member_id)
    email = simpledialog.askstring("Update Profile", "Update your email:", initialvalue=current_info["Email"])
    password = simpledialog.askstring("Update Profile", "Update your password:", initialvalue=current_info["Password"])
    if email != current_info["Email"] or password != current_info["Password"]:
        updateMemberProfile(member_id, email, password)
        messagebox.showinfo("Update Successful", "Your info has been updated")
        display_dashboard(member_id)  

def update_health(member_id):
    height = simpledialog.askstring("Update Health Stats", "Update your height (inches):")
    weight = simpledialog.askstring("Update Health Stats", "Update your weight (pounds):")
    avg_bp = simpledialog.askstring("Update Health Stats", "Update your average blood pressure:")
    
    updateMemberHealth(member_id, height, weight, avg_bp)
    messagebox.showinfo("Update Successful", "Your health stats has been updated")
    display_dashboard(member_id)  
    
def update_goals(member_id):
    desired_weight = simpledialog.askstring("Add New Goal", "New Desired Weight:")
    goal_time = simpledialog.askstring("Add New Goal", "Desired Goal Date (YYYY-MM-DD)")
    
    updateMemberGoals(member_id, desired_weight, goal_time)
    messagebox.showinfo("Update Successful", "Your new goal has been added")
    display_dashboard(member_id)
    
def display_dashboard(member_id):
    dashboard_info = getDashboard(member_id)
    if dashboard_info:
        for widget in userDashboard.winfo_children():
            widget.destroy()
        idLabel=tk.Label(userDashboard, text=f"Personal ID: {member_id}")
        idLabel.pack()
        nameLable=tk.Label(userDashboard, text=f"Name: {dashboard_info['Name']}")
        nameLable.pack()
        emailLabel=tk.Label(userDashboard, text=f"Email : {dashboard_info['Email']}")
        emailLabel.pack()
        bdayLabel=tk.Label(userDashboard, text=f"Date of Birth: {dashboard_info['Date of Birth']}")
        bdayLabel.pack()
        vwmore=tk.Button(userDashboard, text="View Detailed User Info", command=lambda: display_more(member_id))
        vwmore.pack()
        vwup=tk.Button(userDashboard, text="Update User Info", command=lambda: display_update(member_id))
        vwup.pack()
        bookingBut=tk.Button(userDashboard, text="Book Personal Training Session", command=lambda: book_session(member_id))
        bookingBut.pack()
        regBut=tk.Button(userDashboard, text="Register for Class", command=lambda: register_for_class_gui(member_id))
        regBut.pack()
        billbut=tk.Button(userDashboard, text="Check Current Bills", command=lambda: display_bills(member_id, 1))
        billbut.pack()
    else:
        messagebox.showerror("Dashboard Error", "Unable to fetch dashboard information.")

def display_more(member_id):
    for widget in userDashboard.winfo_children():
        widget.destroy()
    vwrout=tk.Button(userDashboard, text="View Exercise Routines", command=lambda: view_routines(member_id, 1))
    vwrout.pack()
    vwgoal=tk.Button(userDashboard, text="View Fitness Goals", command=lambda: view_goals(member_id, 1))
    vwgoal.pack()
    vwachv=tk.Button(userDashboard, text="View Fitness Achievements", command=lambda: view_achievements(member_id, 1))
    vwachv.pack()
    vwheal=tk.Button(userDashboard, text="View Full Health Metrics", command=lambda: view_health(member_id))
    vwheal.pack()
    vwback=tk.Button(userDashboard, text="Back to Menu", command=lambda: display_dashboard(member_id))
    vwback.pack()
    
def display_update(member_id):
    for widget in userDashboard.winfo_children():
        widget.destroy()
    upemail=tk.Button(userDashboard, text="Update Profile", command=lambda: update_profile(member_id))
    upemail.pack()
    upheal=tk.Button(userDashboard, text="Update Health Metrics", command=lambda:update_health(member_id))
    upheal.pack()
    upgoal=tk.Button(userDashboard, text="Add New Fitness Goal", command=lambda:update_goals(member_id))
    upgoal.pack()
    upback=tk.Button(userDashboard, text="Back to Menu", command=lambda: display_dashboard(member_id))
    upback.pack()

def book_session(member_id):
    trainers = fetch_all_trainers()
    if not trainers:
        messagebox.showerror("Error", "No trainers found.")
        return

    booking_window = tk.Toplevel(app)
    booking_window.title("Book a Session")

    tk.Label(booking_window, text="Choose a trainer:").pack()
    
    # Dropdown to select a trainer
    trainer_var = tk.StringVar(booking_window)
    trainer_var.set("Select a Trainer")
    trainer_dropdown = tk.OptionMenu(booking_window, trainer_var, *(f"{trainer[1]} (ID: {trainer[0]})" for trainer in trainers))
    trainer_dropdown.pack()

    # Entry to select a date
    tk.Label(booking_window, text="Enter the session date (YYYY-MM-DD):").pack()
    session_date_entry = tk.Entry(booking_window)
    session_date_entry.pack()

    def confirm_booking():  
        selected_trainer = trainer_var.get()
        if selected_trainer == "Select a Trainer":
            messagebox.showerror("Error", "You must select a trainer.")
            return
        # Extracting the ID from the trainer string
        trainer_id = int(selected_trainer.split("(ID: ")[1].rstrip(")"))
        
        session_date = session_date_entry.get()
        result = bookPersonalTrainingSession(member_id, trainer_id, session_date)
        if result == "Training session booked successfully.":
            messagebox.showinfo("Success", result)
            booking_window.destroy()
        else:
            messagebox.showerror("Error", result)
    
    # Button to confirm booking
    tk.Button(booking_window, text="Book Session", command=confirm_booking).pack()



def register_for_class_gui(member_id):
    classes = fetch_all_classes()
    if not classes:
        messagebox.showerror("Error", "No classes found.")
        return

    # Create a new Toplevel window for class registration
    class_window = tk.Toplevel(app)
    class_window.title("Register for a Class")

    tk.Label(class_window, text="Choose a class:").pack()
    
    # Dropdown to select a class
    class_var = tk.StringVar(class_window)
    class_var.set("Select a Class")
    class_dropdown = tk.OptionMenu(class_window, class_var, *(f"{class_[1]} (ID: {class_[0]})" for class_ in classes))
    class_dropdown.pack()

    def confirm_class_registration():
        selected_class = class_var.get()
        if selected_class == "Select a Class":
            messagebox.showerror("Error", "You must select a class.")
            return
        # Extracting the ID from the class string
        class_id = int(selected_class.split("(ID: ")[1].rstrip(")"))
        #print(result)
        result = registerForClass(member_id, class_id)
        if result == "Registered for class successfully.":
            messagebox.showinfo("Success", result)
            class_window.destroy()
        else:
            messagebox.showerror("Error", result)
    
    # Button to confirm registration
    tk.Button(class_window, text="Register for Class", command=confirm_class_registration).pack()

app = tk.Tk()
app.title("Health and Fitness Club Management System")

frame_login = tk.Frame(app)
frame_login.pack()

userDashboard = tk.Frame(app)
userDashboard.pack(pady=10)

Login=tk.Label(frame_login, text="Enter your name to login:")
Login.pack(side=tk.LEFT)
entry_name = tk.Entry(frame_login)
entry_name.pack(side=tk.LEFT)
tk.Button(frame_login, text="Login", command=login).pack(side=tk.LEFT)

#tk.Button(app, text="Book Personal Training Session", command=book_session).pack(fill=tk.X)

#tk.Button(app, text="Register for Class", command=register_class).pack(fill=tk.X)

app.mainloop()