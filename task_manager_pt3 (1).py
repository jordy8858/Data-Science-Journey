'''
Create a task manager that allows users to register, add tasks, and view tasks.
this progream will work with the Two text files user.txt to store the username and password of the users
and it will work with task.txt to store the details of the tasks added by the users
tasks.txt will have the following format:
username, title, description, assigned date, due date, yes or no value for task completed
user.txt will have the following format:
username, password make sure there is a comma and space between the username and password in the user.txt file
the user is going to have to confirm the password before the username and password are added to the user.txt file
make sure only one user name and password is added per line in the user.txt file
make a login prompt that will ask the user to enter their username and password and check if the username and password are correct by reading the user.txt file
if the username and password are correct, the user will be presented with a menu of options to choose from
if the user name and passowrd are inncorrect, make sure the user is prompted to enter the username and password again until they enter the correct username and password
once the user is logged in, they will be able to choose from the following options:
r - register a user
a - add task
va - view all tasks 
vm - view my tasks
e - exit
if the user selects r they will be asked to enter a new username and password and confirm the password before the username and password are added to the user.txt file
if the user selects a they will be asked to enter:
- the username of the person whom the task is assigned to,
- the title of the task,
- the description of the task
- the due date of the task
- the current date will be added automatically to the task.txt file when the task is added
- if the task has ben completed or not. - this should be defaulted to "no" when it is added since the task is not completed when it is added
if the user selects va they will see a list of all the tasks that have been added to the task.txt file in the following format:
Task: task title
Assigned to: username
description: task description
Date assigned: date assigned
Due date: due date
Task complete? yes or no
if the user selects vm they will see a list of all the tasks that have been assigned to them in the following format:
Task: task title
description: task description
date assigned: date assigned
Due date: due date
Task complete? yes or no
no reason to put username here since they are viewint their own tasks.
had to look up about the datetime module to get the current date when a task is added and to format the date in a way that is easy to read and understand
'''

# ===== Importing external modules ===========

import datetime #importing the datetime module to get the current date when a task is added

# ===== Functions =====

def reg_user(users): #added users as a parameter to the reg_user function so that we can check if the new username is already in the users dictionary
    
    while True:
         new_username = input('Enter a new username: ').strip() #strip is used to remove whitespace
         if not new_username:
              print('Username cannot be empty. Please try again.') #print an error message if the username is empty
              continue
         if new_username in users: #check if the new username is already in the users dictionary
                print('Username already exists. Please choose a different username.') #print an error message if the username already exists
                continue
         break # break loop to get back to password input if the username is valid
    while True: # use a while loop to keep asking the user to enter a new password and confirm until they match
        new_password = input('Enter a new password: ')
        confirm_password = input('Confirm the new password: ') #confirmation of the new password

        if new_password == confirm_password:
            break #break out of the while loop if the passwords match
        else:
            print('Passwords do not match try again. ')
    if new_username in users: #check if the new username is already in the users dictionary
                print('Username already exists. Please choose a different username.') #print an error message if the username already exists
    else:
        with open('user.txt', 'a') as user_file: #open the user.txt file in append mode to add the new username and password
            user_file.write(f'\n{new_username}, {new_password}') #write the new username and password to the user.txt file
        users[new_username] = new_password #add the new username and password to the users dictionary
        print('User registered successfully!')

def add_task():
        username_assigned = input('Enter the username of the person who the task is assigned to: ')
        title = input('Enter the title of the Task: ')
        description = input('Enter the description of the task: ')
        due_date = input('Enter the due date of the task (MM/DD/YYYY): ') #sorry I am from the US so I am used to writing the date in this
        assigned_date = datetime.datetime.now().strftime('%m/%d/%Y') #get the current date and format it in the same way as the due date
        task_completed = 'No' #default value for task completed is "No" since the task is not completed when it is added
        with open('tasks.txt', 'a') as task_file: #open the task.txt file in append mode to add the new task
            task_file.write(f'\n{username_assigned}, {title}, {description}, {assigned_date}, {due_date}, {task_completed}') #adding the new task to the task.txt file
            print('Task added successfully!')

def view_all():
        print('\n--- All tasks ---') #print a header for the list of all tasks and center it to make it look nicer
        with open('tasks.txt', 'r') as task_file: #open the task.txt file in read mode to read the tasks
            for line in task_file: #making sure each line is read
                if line.strip(): #check if the line is not empty
                    parts = line.strip().split(', ') #split the line where there is a comma and space to get the different parts of the task
                    if len(parts) == 6: #check if there are 6 parts in the line to avoid errors
                        username_assigned, title, description, assigned_date, due_date, task_completed = parts #assign the different parts of the task to variables
                        print(f'Task:               {title}')
                        print(f'Assigned to:        {username_assigned}')
                        print(f'Description:        {description}')
                        print(f'Date assigned:      {assigned_date}')
                        print(f'Due date:           {due_date}')
                        print(f'Task complete?      {task_completed}\n') 
                        print('--------------------') #
                    else:
                        print('Error: Task format is incorrect. Skipping this task.') #print an error message if the task format is incorrect
        print('--- End of tasks ---') #print a footer for the list of all tasks and center it to make 

def view_mine():
        print(f'\n--- Tasks assigned to {current_user} ---') #print a header for the list of tasks assigned to the current user and center it
        found_tasks = False #variable to keep track of whether any tasks assigned to the current user were found
        with open('tasks.txt', 'r') as task_file: #the rest of this code block should be very similar to the va code black
            all_lines = [line.strip() for line in task_file if line.strip()] #read all the lines in the task.txt file and strip them of whitespace and check if they are not empty

        found_tasks = [] #empty list to store the tasks assigned to the current user
        display_number = 1 #variable to keep track of the number of tasks assigned to the user
        
        for i, line in enumerate(all_lines): #loop through all the lines in the task.txt file and check if they are assigned to the current user
            parts = line.split(', ')
            if len(parts) == 6 and parts[0] == current_user: #check if there are 6 parts in the line 
                    username_assigned, title, description, assigned_date, due_date, task_completed = parts #unpack the parts of the task into variables
                    found_tasks.append((display_number, i, parts)) #add the task to the user_tasks list as a tuple with the display number, the line number in the task.txt file, and the parts of the task
                    
                    print(f'\n======Task #{display_number}======:') #print the task number to make it easier for the user to read and understand
                    print(f'Task:               {title}')
                    print(f'Description:        {description}')
                    print(f'Date assigned:      {assigned_date}')
                    print(f'Due date:           {due_date}')
                    print(f'Task complete?      {task_completed}\n')
                    print('--------------------')
                    display_number += 1 #the display number goes up by 1 for each task


        if not found_tasks: #check if no tasks assigned to the current user were found
            print(f'No tasks assigned to {current_user}.') #print a message if no tasks assigned to the current user were found
            print(f'--- End of tasks assigned to {current_user} ---') #footer
            return
#====== Task selection for marking as complete or editing ======
        while True: #use a while loop to keep asking the user to select a task until they enter -1 to return to the main menu
            choice = input('Enter the task number you want to select, or enter -1 to return to the main menu: ')
            if choice == '-1': 
                break #break out of the while loop to return to the main menu
        
            if not choice.isdigit():
                print("inavlid option. Please enter a valid task number or -1 to return to the main menu.")
                continue
            choice = int(choice)

            selected_task = None 
            for task in found_tasks: #loop through the found_tasks list to find the task that matches the user's choice
                if task[0] == choice: #check if the display number of the task matches the user's choice
                    selected_task = task #set the selected_task variable to the task that matches the user's choice
                    break
                    
            if not selected_task:
                print(f"Task number {choice} is not an option. Please enter a valid task number or -1 to return to the main menu.")
                continue

            display_number, line_number, parts = selected_task #unpack the selected task into variables
            username_assigned, title, description, assigned_date, due_date, task_completed = parts
            is_completed = task_completed.lower() == 'yes' #check if the task is completed

            print(f'You have selected Task #{display_number}:') #display the details of the selected task to the user
            print(f'Title:              {title}')
            print(f'Description:        {description}')
            print(f'Date assigned:      {assigned_date}')
            print(f'Due date:           {due_date}')
            print(f'Task complete?      {task_completed}\n')
        
            print('What would you like to do with this task?')
            print('c - Mark the task as complete')
            print('e - Edit the task')
            print('b - Go back to the task list')
            action = input('Enter your choice: ').lower()
            if action == 'c':
                if is_completed:
                    print('This task is already marked as complete.')  #more and more and more defensive programming to make sure the user doesn't mess up the task.txt file
                else:
                    parts[5] = 'Yes' #the task completed part is at index 5
                    all_lines[line_number] = ', '.join(parts) 
                    with open('tasks.txt', 'w') as task_file: 
                        for line in all_lines:
                            task_file.write(line + '\n') #write the updated tasks back to the task.txt file
                    print(f'Task #{display_number} has been marked as complete.')
           
            elif action == 'e':
                if is_completed:
                    print('This task is already marked as complete and cannot be edited.')
                else:
                    new_title = input('Enter the new title of the task (leave blank to keep current title): ')
                    new_description = input('Enter the new description of the task (leave blank to keep current description): ')
                    new_due_date = input('Enter the new due date of the task (MM/DD/YYYY) (leave blank to keep current due date): ')
                    
                    if new_title:
                        parts[1] = new_title #the title part is at index 1
                    if new_description:
                        parts[2] = new_description #the description part is at index 2
                    if new_due_date:
                        parts[4] = new_due_date #the due date part is at index 4
                    
                    all_lines[line_number] = ', '.join(parts) #update the line in the all_lines list with the edited task information
                    with open('tasks.txt', 'w') as task_file: 
                        for line in all_lines:
                            task_file.write(line + '\n')
                    print(f'Task #{display_number} has been updated.')
                    break
           
            elif action == 'b':
                continue

            else:
                print('Invalid option. Please enter c, e, or b.')
        print(f'--- End of tasks assigned to {current_user} ---') #footer
#The View_mine fuction was the hardest part of the project and I had to go back to old material several times to get by. A lot of errors to get here. 
#are fuctions supposed to be this long? I don't know but it works and I am happy with it. is there any way that i could have made it shorter or more efficient?
#mostly talking to myself here i have been working on this all day to get this done.


def view_completed(): 
        print('\n--- Completed tasks ---') #print a header for the list of completed tasks and center it
        found_tasks = False #variable to keep track of whether any completed tasks were found
        with open('tasks.txt', 'r') as task_file: 
            for line in task_file: 
                if line.strip(): 
                    parts = line.strip().split(', ') 
                    if len(parts) == 6: 
                        username_assigned, title, description, assigned_date, due_date, task_completed = parts 
                        if task_completed.lower() == 'yes': #check if the task is completed
                            found_tasks = True #set found_tasks to True since we found a completed task
                            print(f'Task:               {title}')
                            print(f'Assigned to:        {username_assigned}')
                            print(f'Description:        {description}') 
                            print(f'Date assigned:      {assigned_date}')
                            print(f'Due date:           {due_date}')
                            print(f'Task complete?      {task_completed}\n')
                            print('--------------------')
        if not found_tasks: #check if no completed tasks were found
            print('No completed tasks found.') #print a message if no completed tasks were found
        print('--- End of completed tasks ---') #footer

def delete_task():    
        task_to_delete = input('Enter the title of the task you want to delete: ') #ask the user to enter the title of the task they want to delete
        tasks = [] #empty list to store the tasks that are not deleted
        task_deleted = False #variable to keep track of whether a task was deleted or not
        with open('tasks.txt', 'r') as task_file: 
            for line in task_file: 
                if line.strip(): 
                    parts = line.strip().split(', ') 
                    if len(parts) == 6: 
                        username_assigned, title, description, assigned_date, due_date, task_completed = parts 
                        if title == task_to_delete: #check if the title of the task matches the title of the task to delete
                            task_deleted = True #set task_deleted to True since we found the task to delete
                            print(f'Task "{title}" has been deleted.') #print a message that the task has been deleted
                        else:
                            tasks.append(line.strip()) #add the task to the tasks list if it is not deleted
        if not task_deleted: #check if no task was deleted
            print(f'Task "{task_to_delete}" not found. No tasks were deleted.') #print a message if no task was deleted
        else:
            with open('tasks.txt', 'w') as task_file: #open the tasks.txt file in write mode to overwrite it with the tasks that are not deleted
                for task in tasks:
                    task_file.write(task + '\n') #write the tasks that are not deleted back to the tasks.txt file


users = {} #empty dictionary to store the username and password from the user.txt file
with open('user.txt', 'r') as user_file:
    for line in user_file:
        username, password = line.strip().split(', ') #split the line where there is a comma and space to get the username and password
        users[username] = password #add the username and password to the users dictionary

logged_in = False #variable to keep track of whether the user is logged in or not
current_user = None #variable to indicate failed login attempt

#===== New Functions =====

def generate_reports():
    with open('tasks.txt', 'r') as task_file:
        all_tasks = [line.strip() for line in task_file if line.strip()] #need to see all the tasks to create the overviews
#task overview
#count 
    total_tasks = len(all_tasks)
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0
    current_date = datetime.datetime.now()

    for lines in all_tasks:
        parts = lines.split(', ')
        if len(parts) == 6: #check if there are 6 parts in the line to avoid errors
            due_date_str = parts[4] #the due date part is at index 4
            task_completed = parts[5].lower() #the task completed part is at index 5

            if task_completed == 'yes':
                completed_tasks += 1
            else:
                uncompleted_tasks += 1

                #overdue
                try:
                    due_date = datetime.datetime.strptime(due_date_str, '%m/%d/%Y') #convert the due date string to a datetime object
                    if due_date < current_date: #check if the due date is before the current date
                        overdue_tasks += 1
                except:
                    pass

#percentage
    if total_tasks > 0:
        percentage_incomplete = (uncompleted_tasks / total_tasks) * 100 #calculate the percentage of incomplete tasks
        percentage_overdue = (overdue_tasks / total_tasks) * 100 #calculate the percentage of overdue tasks
    else:
        percentage_incomplete = 0
        percentage_overdue = 0

#task_overview.txt
    with open('task_overview.txt', 'w') as f:
        f.write("=== Task Overview ===\n")
        f.write(f"Total tasks:              {total_tasks}\n")
        f.write(f"Completed tasks:          {completed_tasks}\n")
        f.write(f"Uncompleted tasks:        {uncompleted_tasks}\n")
        f.write(f"Overdue tasks:            {overdue_tasks}\n")
        f.write(f"Percentage incomplete:    {percentage_incomplete:.2f}%\n") #need % sign almost forgot it
        f.write(f"Percentage overdue:       {percentage_overdue:.2f}%\n")
    print('Task overview report generated successfully!')


#user overview
    user_overview = {}
    with open('user.txt', 'r') as user_file:
        for line in user_file:
            if line.strip():
                username = line.strip().split(', ')[0] #get the username from the user.txt file
                user_overview[username] = {
                    'total_tasks': 0,
                    'completed_tasks': 0,
                        'uncompleted_tasks': 0,
                        'overdue_tasks': 0
                    }
        #overdue
        today = datetime.datetime.now()
        for lines in all_tasks:
            parts = lines.split(', ')
            if len(parts) == 6:
                username_assigned = parts[0] #the username assigned part is at index 0
                due_date_str = parts[4] #the due date part is at index 4
                task_completed = parts[5].lower() #the task completed part is at index 5

                if username_assigned in user_overview:
                    user_overview[username_assigned]['total_tasks'] += 1
                    if task_completed == 'yes':
                        user_overview[username_assigned]['completed_tasks'] += 1
                    else:
                        user_overview[username_assigned]['uncompleted_tasks'] += 1

                        try:
                            due_date = datetime.datetime.strptime(due_date_str, '%m/%d/%Y')
                            if due_date < today:
                                user_overview[username_assigned]['overdue_tasks'] += 1
                        except:
                            pass #quite the slope 

        with open('user_overview.txt', 'w') as f:
            f.write("=== User Overview ===\n")
            for username, overview in user_overview.items(): #loop through the user_overview dictionary to write the overview for each user to the user_overview.txt file
                total_tasks = overview['total_tasks']
                completed_tasks = overview['completed_tasks']
                uncompleted_tasks = overview['uncompleted_tasks']
                overdue_tasks = overview['overdue_tasks'] 

                if total_tasks > 0: #calculate the percentages for each user, need to check if total_tasks is greater than 0 to avoid division by zero error
                    percentage_completed = (completed_tasks / total_tasks) * 100
                    percentage_uncompleted = (uncompleted_tasks / total_tasks) * 100
                    percentage_overdue = (overdue_tasks / total_tasks) * 100
                else:
                    percentage_completed = 0
                    percentage_uncompleted = 0
                    percentage_overdue = 0

                f.write(f"User: {username}\n")
                f.write(f"Total tasks assigned:     {total_tasks}\n")
                f.write(f"Completed tasks:          {completed_tasks}\n")
                f.write(f"Uncompleted tasks:        {uncompleted_tasks}\n")
                f.write(f"Overdue tasks:            {overdue_tasks}\n")
                f.write(f"Percentage completed:     {percentage_completed:.2f}%\n")
                f.write(f"Percentage uncompleted:   {percentage_uncompleted:.2f}%\n")
                f.write(f"Percentage overdue:       {percentage_overdue:.2f}%\n")
                f.write('--------------------\n')
    print('User overview report generated successfully!')

#this one was almost as bad as the view_mine function to write. I had to go back and forth between the task overview and user overview sections to make sure I was calculating the statistics correctly and writing them to the correct files. I also had to look up how to format the percentages in the output files to make them look nice.

def display_statistics():
    try:
        with open('task_overview.txt', 'r') as task_overview_file:
            task_overview = task_overview_file.read()
            print(task_overview)
    except FileNotFoundError:
        print('Task overview report not found. Please generate the reports first.')

    try:
        with open('user_overview.txt', 'r') as user_overview_file:
            user_overview = user_overview_file.read()
            print(user_overview)
    except FileNotFoundError:
        print('User overview report not found. Please generate the reports first.')

#====login====
while not logged_in: #use a while loop to keep asking the user to enter their username and password until they enter the correct username and password
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    if username in users and users[username] == password: #check if the username is in the users dictionary and if the password matches the password in the users dictionary
        print('Login Successful!')
        logged_in = True #set logged_in to True to exit the while loop
        current_user = username # set current_user to the username that was successfully logged in
    else:
        print('Invalid username or password. Please try again.') #print an error message if the username or password is incorrect


# ===== Main Menu =====
while True: #changed the while loop to make the admin menu and the user menu
    if  current_user == 'admin': 
        admin_menu = input(
        'Select one of the following options:' 
        '\nr - Register a user'
        '\na - Add a task'
        '\nva - View all tasks'
        '\nvm - View my tasks'
        '\nvc - View completed tasks'
        '\ndel - Delete a task'
        '\nds - Display statistics'
        '\ngr - Generate reports'
        '\ne - Exit'
        '\nEnter your choice: '
        ).lower()
    else:
        user_menu = input(
        'Select one of the following options:' 
        '\na - Add a task'
        '\nva - View all tasks'
        '\nvm - View my tasks'
        '\ne - Exit'
        '\nEnter your choice: '
        ).lower()   

    if current_user == 'admin': #added this if statement so that the menu variable would be set to the correct menu based on the user.
        menu = admin_menu
    else:
        menu = user_menu

# ===== Main Program Loop =====
    if menu == 'r':
        reg_user(users)

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm': 
        view_mine()
    
    elif menu == 'vc' and current_user == 'admin': #added this option to the admin menu to view completed tasks
        view_completed()

    elif menu == 'del' and current_user == 'admin': #added this option to the admin menu to delete a task
        delete_task()
    
    elif menu == 'ds' and current_user == 'admin': #added this option to the admin menu to display statistics
        display_statistics()
    
    elif menu == 'gr' and current_user == 'admin': #added this option to the admin menu to generate reports
        generate_reports()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()


#very proud of this project. I hope it works as well as it has been during testing.