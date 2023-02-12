# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

def reg_user():
    # - Request input of a new username
    new_username = input("New Username: ")
    # - Request input of a new password
    new_password = input("New Password: ")
    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")
    # - Check if the new username already exists and if so get user to try again.
    if new_username in username_password:
        print("Username already exists, please try again")
    # - Check if the new password and confirmed password are the same
    elif new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password           
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    # - Otherwise you present a relevant message.
    else:
        print("Passwords do not match, please try again")

def add_task():
    '''Allow a user to add a new task to task.txt file. Prompt a user for the following: 
         - A username of the person whom the task is assigned to,
         - A title of a task,
         - A description of the task and 
         - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
    else:
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")

def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
        '''
    
    for t in task_list:
        task_number = task_list.index(t) + 1 # generate task number from index position in task list
        if t['username'] == curr_user:
            disp_str = f"Task number:\t\t {task_number}\n"
            disp_str += f"Task: \t\t\t {t['title']}\n"
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \t {t['description']}\n"
            print(disp_str)
    # add functionality to edit user's tasks
    editing = True
    while editing: # while loop to edit assigned tasks until finished and select -1 to go back to main menu
        edit_task = int(input("Enter the Task number you wish to edit, or enter '-1' to go back to main menu: "))
        if edit_task == -1:
            editing = False
        else:
            if task_list[edit_task - 1]["completed"] == False: # if selected is not completed
                completed = input("Do you want to mark the task as complete?, enter y for yes or n for no: ") # input from user to confirm if task is complete
                completed = completed.lower() # validation
                if completed == "y": # if user confirms as completed
                    task_list[edit_task - 1]["completed"] = True # edit task list value for key 'completed' to True
                else:
                    edit_option = int(input("Do you wish to edit the task?, Enter the number from the list of options below:\n1 Assign task to new user\n2 Edit due date\n3 Exit\n")) # otherwise ask user which field they want to amend, User or Due date
                    if edit_option == 1: # if user selects change user
                        task_username = input("Enter username of person to be assigned to task: ") # ask user to confirm username of new person
                        while task_username not in username_password.keys(): # while loop check if username exists and ask user to re-input valid username
                            task_username = input("User does not exist. Please enter a valid username: ")
                        task_list[edit_task - 1]["username"] = task_username # update value for username in task list 
                    elif edit_option == 2: # if user selects change due date
                        while True:
                            try:
                                edit_due_date = input("New due date for task (YYYY-MM-DD): ") # ask user for new due date in required format
                                edit_date_time = datetime.strptime(edit_due_date, DATETIME_STRING_FORMAT)
                                break

                            except ValueError:
                                print("Invalid datetime format. Please use the format specified")
                        task_list[edit_task - 1]["due_date"] = edit_date_time # amend task list with new due date
                    else:
                        continue
            else: print("Task is already marked as complete.") # else task was already flagged as complete so cannot be amended, output to user
    # write edited task list to task.txt
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("You have left View my tasks.")

def generate_reports(): # add function to generate reports for tasks - task_overview.txt and users user_overview.txt
    num_tasks = len(task_list) # number of tasks = length of task list
    completed_tasks = 0 # initialise variable with initial value of zero
    uncompleted_tasks = 0 # initialise variable with initial value of zero
    overdue_tasks = 0 # initialise variable with initial value of zero
    for t in task_list: # for task in task list
        if t["completed"] == True: # if flagged as completed
            completed_tasks += 1 # add one to completed task count
        else:
            uncompleted_tasks += 1 # else add one to uncompleted task count
            if t["due_date"] < datetime.today(): # if due date was earlier (less than) than todays date
                overdue_tasks +=1 # add one to overdue task count
    percent_incomplete = (uncompleted_tasks/num_tasks) * 100 # percentage of total tasks completed
    percent_overdue = (overdue_tasks/num_tasks) * 100 # percentage of total tasks overdue
    with open ("task_overview.txt", "w") as task_report: # open task_overview.txt and write values calculated above
        task_report.write(f"Task Manager report - Task overview\n\nas at {date.today()}\n\nTotal number of tasks:\t\t\t\t{num_tasks}\nCompleted tasks:\t\t\t\t\t{completed_tasks}\nUncompleted tasks:\t\t\t\t\t{uncompleted_tasks}\nOverdue tasks yet to be completed:\t{overdue_tasks}\nPercentage of tasks incomplete:\t\t{percent_incomplete:.0f}%\nPercentage of tasks overdue:\t\t{percent_overdue:.0f}%")
    
    num_users = len(username_password.keys()) # number of users = number of usernames in username_password dict
    with open ("user_overview.txt", "w") as user_report: # open user_overview.txt and write high level numbers calculated above
        user_report.write(f"Task Manager report - User overview\n\nas at {date.today()}\n\nTotal users:\t\t\t\t\t\t{num_users}\nTotal number of tasks:\t\t\t\t{num_tasks}")
    for user in username_password.keys(): # for loop username in username_password
        user_tasks = 0 # initialise variables with initial value of zero
        user_complete = 0
        user_uncomplete = 0
        user_overdue = 0
        for t in task_list: # for loop task in task list
            if t["username"] == user: # if username = username in username_password
                user_tasks += 1 # add one to users task count
                if t["completed"]: # if task is flagged as completed
                    user_complete += 1 # add one to users completed task count
                else:
                    user_uncomplete += 1 # else add one to users uncomplete task count
                    if t["due_date"] < datetime.today(): # if due date is earlier (less than) todays date
                        user_overdue += 1 # add one to users overdue task count
            else: continue
        user_percent_assigned = (user_tasks/num_tasks) * 100 # percentage of total tasks assigned to user
        user_percent_complete = (user_complete/user_tasks) * 100 # percentage of users tasks complete
        user_percent_incomplete = (user_uncomplete/user_tasks) * 100 # percentage of users task incomplete
        user_percent_overdue = (user_overdue/user_tasks) * 100 # percentage of users tasks overdue
        with open ("user_overview.txt", "a") as user_report: # open user_overview.txt and append user data calculated above
            user_report.write(f"\n\nFor user: {user}\nNumber of tasks assigned: {user_tasks}\nPercentage of tasks assigned to this user:\t{user_percent_assigned:.0f}%\nPercentage of assigned tasks - completed:\t{user_percent_complete:.0f}%\nPercentage of assigned tasks - incomplete:\t{user_percent_incomplete:.0f}%\nPercentage of incomplete tasks - overdue:\t{user_percent_overdue:.0f}%")
    print("Reports generated") # once complete print Reports generated

def display_stats():
    num_users = len(username_password.keys())
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")
    print()
    with open ("task_overview.txt", "r") as task_file: # read data from task_overview.txt and print
        task_overview = task_file.read()
        task_overview = task_overview.replace("\t", "")
        print("-----------------------------------")
        print(task_overview)
        print("-----------------------------------")
    with open ("user_overview.txt", "r") as user_file: # read data from user_overview.txt and print
        user_overview = user_file.read()
        user_overview = user_overview.replace("\t","")
        print(user_overview)
    print("-----------------------------------")

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
ds - display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr':
        generate_reports()
                
    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        generate_reports()
        display_stats()
            

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")