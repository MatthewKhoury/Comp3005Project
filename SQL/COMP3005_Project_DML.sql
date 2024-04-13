-- Populate Members Table
INSERT INTO Members (name, email, date_of_birth, password, goal_statement)
VALUES 
('John Doe', 'test@email.com', '2001-05-12', 'abcde1', 'I want to get fit!'),
('Mary Jane', 'temporary@outlook.com', '1994-02-27', '12345', 'Trying to bulk up!'),
('Tom Jeremy', 'another@gmail.com', '2000-11-15', 'Password', 'Wanting to lose weight.'),
('Jimmy Johnson', 'jimmymail@email.com', '1972-08-02', 'GymPass', 'Keep in shape.');

-- Populate Health_Metrics Table
INSERT INTO Health_Metrics (member_id, last_updated, height, weight, avg_blood_pressure)
VALUES
(1, CURRENT_DATE, 72, 175, '140/80'),
(2, '2023-11-19', 59, 125, '110/70'),
(3, '2024-01-16', 67, 210, '160/80'),
(4, '2017-03-09', 63, 155, '110/70');

-- Populate Routines Table
INSERT INTO Routines (member_id, time_limit, exercise_list, num_reps)
VALUES
(1, '003000', 'Pullups, Pushups, Squats', 20),
(1, '001500', 'Planks, Lunges, Deadlifts, Burpees', 10),
(2, '004500', 'Deadlifts, Pushups, Lunges, Squats', 15),
(2, '010000', 'Burpees, Planks, Lunges', 10),
(2, '003000', 'Squats, Lunges, Situps, Jumping-Jacks', 20),
(3, '002000', 'Deadlifts, Pushups, Dumbbell-press', 15),
(4, '003000', 'Pushups, Pullups, Situps', 25),
(4, '001000', 'Kettlebell-lifts, Bicep-curls, Deadlifts', 10);

-- Populate Fitness_Goals Table
INSERT INTO Fitness_Goals (member_id, start_date, desired_weight, goal_time)
VALUES
(1, CURRENT_DATE, 160, '2024-06-01'),
(2, '2024-03-15', 130, '2024-05-01'),
(3, '2024-01-20', 180, '2024-09-15'),
(4, '2023-05-11', 150, '2024-05-30');

-- Populate Fitness_Achievements Table
INSERT INTO Fitness_Achievements (member_id, date_achieved, goal_description)
VALUES
(1, CURRENT_DATE, 'You joined the gym, congrats!'),
(2, '2023-11-19', 'You joined the gym, congrats!'),
(2, '2024-01-23', 'You achieved your first goal, well done!'),
(3, '2024-01-16', 'You joined the gym, congrats!'),
(4, '2017-03-09', 'You joined the gym, congrats!'),
(4, '2019-06-21', 'You achieved your first goal, well done!'),
(4, '2022-02-04', 'You achieved another goal, great job!'),
(4, '2023-05-09', 'You achieved your goal, nice work!');

-- Populate Trainers Table
INSERT INTO Trainers (name, email, date_of_birth, password, specialization)
VALUES
('Dorothy', 'dorothytrainer@email.com', '1992-04-29', 'Apples21', 'Cardio'),
('James', 'jameswork@gmail.com', '1999-02-05', '12345', 'Arms'),
('Amir', 'amirtrainer@outlook.com', '1985-09-10', 'Password123', 'Legs');

-- Populate Trainer_Schedules Table
INSERT INTO Trainer_Schedules (trainer_id, start_time, end_time)
VALUES
(1, '2024-04-10 12:00:00', '2024-06-09 00:00:00'),
(2, '2024-03-07 14:30:00', '2024-04-10 00:00:00'),
(3, '2023-05-21 12:00:00', '2024-09-11 00:00:00');

-- Populate Admin_Staff Table
INSERT INTO Admin_Staff (email, password)
VALUES
('admin1@outlook.com', 'password123'),
('admin2@gmail.com', 'Orange97'),
('admin3@email.com', '12354');

-- Populate Equipment Table
INSERT INTO Equipment (name, last_checkup, description, issues, admin_id)
VALUES
('Treadmill #1', '2024-02-12', 'Treadmill with 12 speeds, inclined', 'No issues', 1),
('Treadmill #2', '2024-03-23', 'Treadmill with 12 speeds, no incline', 'Issue with display', 1),
('Treadmill #3', '2024-03-10', 'Treadmill with 5 speeds, no incline', 'No issues', 1),
('Leg Press #1', '2024-03-10', 'Leg Press with 150 lbs max', 'Frayed wire', 2),
('Leg Press #2', '2024-03-23', 'Leg Press with 100 lbs max', 'No issues', 2),
('Exercise Bike #1', '2024-04-02', 'Exercise Bike with adjustable resistance', 'No issues', 3),
('Exercise Bike #2', '2024-03-23', 'Exercise Bike with adjustable resistance', 'Broken pedal', 3);

-- Populate Room_Bookings Table
INSERT INTO Room_Bookings (admin_id, start_date, end_date, capacity)
VALUES
(1, '2024-02-10', '2024-05-01', 20),
(1, '2024-04-01', '2024-04-20', 30),
(2, '2024-03-15', '2024-05-15', 10),
(2, '2024-04-05', '2024-06-05', 25),
(2, '2024-02-25', '2024-04-25', 20);

-- Populate Classes Table
INSERT INTO Classes (name, room_id, trainer_id, participants, schedule, duration)
VALUES
('Yoga', 1, 1, '{1, 2, 3}', '2024-05-09', '010000'),
('Lifting', 1, 2, '{1, 2, 4}', '2024-04-01', '003000'),
('Running', 2, 3, '{3, 4}', '2024-06-21', '013000');

-- Populate Bookings Table
INSERT INTO Bookings (member_id, class_id, session_id)
VALUES
(1, 1, NULL),
(2, 1, NULL),
(3, 1, NULL),
(1, 2, NULL),
(2, 2, NULL),
(4, 2, NULL),
(3, 3, NULL),
(4, 3, NULL);

-- Populate Bills Table
INSERT INTO Bills (amount_due, due_date, member_id, admin_id)
VALUES
(54.99, CURRENT_DATE + interval '14 days', 1, 1),  -- New membership fee
(24.99, '2024-05-23', 1, 2),
(24.99, '2024-05-23', 2, 2), -- Yoga class fees
(24.99, '2024-05-23', 3, 2),
(19.99, '2024-04-15', 1, 2),
(19.99, '2024-04-15', 2, 2), -- Lifting class fees
(19.99, '2024-04-15', 4, 2),
(29.99, '2024-07-05', 3, 3), -- Running class fees
(29.99, '2024-07-05', 4, 3);