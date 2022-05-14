import os
import tkinter as tk
import database as db
from time import sleep


class Schedule(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Scheduler - Managment of my tasks')
        self.geometry('450x600')
        self.iconphoto(False, tk.PhotoImage(file='scheduler.png'))

        # create menu bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        # create the file_menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)

        # create the courses_menu
        self.courses_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.courses_menu.add_command(label="View courses", command=self.view_courses)
        self.courses_menu.add_separator()
        self.courses_menu.add_command(label="Add a course")
        self.courses_menu.add_command(label="Remove a course")
        self.file_menu.add_cascade(label="Courses", menu=self.courses_menu)

        # create the tasks_menu
        self.tasks_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.tasks_menu.add_command(label="View tasks")
        self.tasks_menu.add_separator()
        self.tasks_menu.add_command(label="Add a task")
        self.tasks_menu.add_command(label="Remove a task")
        self.file_menu.add_cascade(label="Tasks", menu=self.tasks_menu)

        # create the settings_menu
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=lambda: self.destroy())

        # create the Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label='Welcome')
        self.help_menu.add_command(label='About...')

        # add the options to the menubar
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.scrollable_frame = None

        # start connection to database
        self.con, self.cur = db.start()
        
    
    def set_user(self, user_name):
        db.insert(self.con, self.cur, "settings", ["name", "value"], ("user", user_name))
        self.con.commit()
    
    def get_user(self):
        user_name = db.select(S.cur, "settings", ["value"], "name=?", ("user", ))
        if user_name == []:
            user_name = input("Enter you name: ")
            self.set_user(user_name)
        else:
            user_name = user_name[0][0]

        return user_name
    
    # def select_course(self):
    #     print("Select a course: ")
    #     courses = db.select(self.cur, "courses", ["rowid", "name"], None, None)
    #     for c in courses:
    #         print(" {}. {}".format(c[0], c[1]))
    #     choice = input("Enter a choice: ")
    #     return int(choice)
    
    
    def view_courses(self):
        # if there's already a frame, destroy it
        if self.scrollable_frame is not None:
            self.scrollable_frame.destroy()
        self.scrollable_frame = tk.Frame(self)
        self.scrollable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.scrollable_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self.scrollable_frame, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        courses = db.select(self.cur, "courses", ["rowid", "name"], None, None)

        if len(courses) != 0:
            for course in courses:
                # put the course name in a scrollable frame
                course_frame = tk.Frame(self.listbox)
                course_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                course_label = tk.Label(course_frame, text=course[1], font=("Helvetica", 15))
                course_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                
                # put the tasks below the course name
                tasks = db.select(self.cur, "tasks", ["name", "due_date", "priority"], "course_id=?", (course[0], ))
                if len(tasks) != 0:
                    for task in tasks:
                        # table of tasks
                        task_frame = tk.Frame(self.listbox)
                        task_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                        task_label = tk.Label(task_frame, text="{}{}  {}  {}".format('\u2666'*task[2], " "*3*(10-task[2]), task[0], task[1]), font=("Helvetica", 12))
                        task_label.pack(side=tk.TOP, fill=tk.X, expand=True)
                else:
                    tk.Label(self.listbox, text="No tasks", font=("Helvetica", 12)).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                
                # add a separator
                tk.Frame(self.listbox, height=2, bd=1, relief=tk.SUNKEN).pack(side=tk.TOP, fill=tk.X, pady=10)
        else:
            tk.Label(self.listbox, text="No courses", font=("Helvetica", 12)).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        

    def __del__(self):
        db.terminate(self.con)
    

if __name__ == "__main__":
    S = Schedule()
    S.mainloop()

    username = S.get_user()
    os.system("cls")
    # print("Welcome {}\n".format(username))
    # sleep(1)
    # menu_option = ""
    # while menu_option != "3":
    #     os.system("cls")
    #     menu_option = S.menu()
    #     os.system("cls")
    #     # Courses
    #     if menu_option == "1":
    #         choice = S.courses()
    #         os.system("cls")
    #         if choice == "1":
    #             course_name = input("Enter a course name: ")
    #             db.insert(S.con, S.cur, "courses", ["name"], (course_name,))
    #             S.con.commit()
    #         elif choice == "2":
    #             course_id = S.select_course()
    #             db.delete(S.con, S.cur, "courses", "rowid=?", (course_id,))
    #             S.con.commit()
    #     # Tasks
    #     elif menu_option == "2":
    #         choice = S.tasks()
    #         os.system("cls")
    #         if choice == "1":
    #             course_id = S.select_course()
    #             task_name = input("Enter a task name: ")
    #             due_date = input("Enter a due date: ")
    #             priority = input("Enter a priority: ")
    #             db.insert(S.con, S.cur, "tasks", ["name", "course_id", "due_date", "priority"], (task_name, course_id, due_date, priority))
    #             S.con.commit()
    #         elif choice == "2":
    #             course_name = input("Enter a course name: ")
    #             task_name = input("Enter a task name: ")
    #             db.delete(S.con, S.cur, "tasks", "name=? AND course_id=?", (task_name, course_name))
    #             S.con.commit()
    #         elif choice == "3":
    #             pass  

    # os.system("cls")