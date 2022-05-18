import os
import tkinter as tk
import database as db
from time import sleep


class Schedule(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Scheduler - Managment of my tasks')
        self.geometry('450x600+500+20')
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
        self.courses_menu.add_command(label="Add a course", command=self.add_course)
        # self.courses_menu.add_command(label="Remove a course")

        # create the tasks_menu
        self.tasks_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.tasks_menu.add_command(label="View tasks", command=self.view_tasks)
        self.tasks_menu.add_separator()
        self.tasks_menu.add_command(label="Add a task", command=self.add_task)
        # self.tasks_menu.add_command(label="Remove a task")

        # create the settings_menu
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=lambda: self.destroy())

        # create the Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label='Welcome')
        self.help_menu.add_command(label='About...')

        # add the options to the menubar
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Courses", menu=self.courses_menu)
        self.menu_bar.add_cascade(label="Tasks", menu=self.tasks_menu)
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

    
    def rename_course_helper(self, course_id, new_name, window):
            db.update(self.con, self.cur, "courses", [("name", new_name)], "rowid=?", (course_id, ))
            window.destroy()
            self.view_courses()


    def rename_course(self, course_id):
        # New window to introduce the new name
        new_name = tk.Tk()
        new_name.title("Rename course")
        new_name.geometry('300x50+600+200')
                 
        # add entry
        new_name_entry = tk.Entry(new_name)
        new_name_entry.pack(fill=tk.X)
        # add button
        new_name_button = tk.Button(new_name, text="Rename", command=lambda: self.rename_course_helper(course_id, new_name_entry.get(), new_name))
        new_name_button.pack(fill=tk.X)
        new_name.mainloop()


    def add_course_helper(self, new_name, window):
        db.insert(self.con, self.cur, "courses", ["name"], (new_name, ))
        window.destroy()
        self.view_courses()

    def add_course(self):
        # New window to introduce the new course
        new_course = tk.Tk()
        new_course.title("Add course")
        new_course.geometry('300x50+600+200')
                 
        # add entry
        new_course_entry = tk.Entry(new_course)
        new_course_entry.pack(fill=tk.X)
        # add button
        new_course_button = tk.Button(new_course, text="Add", command=lambda: self.add_course_helper( new_course_entry.get(), new_course))
        new_course_button.pack(fill=tk.X)
        new_course.mainloop()

        db.insert(self.con, self.cur, "courses", ["name"], (course_name, ))

    
    def delete_course(self, course_id):
        db.delete(self.con, self.cur, "courses", "rowid=?", (course_id, ))
        self.view_courses()
        

    def view_courses(self):
        if self.scrollable_frame is not None:
            self.scrollable_frame.destroy()
        self.scrollable_frame = tk.Frame(self)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)
        
        courses = db.select(self.cur, "courses", ["rowid", "name"], None, None)

        for c in courses:
            course_frame = tk.Frame(self.scrollable_frame)
            # add padding to left
            course_label = tk.Label(course_frame, text=" "*3)
            course_label.pack(side=tk.LEFT)
            # add padding to right
            course_label = tk.Label(course_frame, text=" ")
            course_label.pack(side=tk.RIGHT)
            # add padding to top
            course_label = tk.Label(course_frame, text=" ")
            course_label.pack(side=tk.TOP)

            course_frame.pack(fill=tk.X)
            course_label = tk.Label(course_frame, text=c[1])
            course_label.pack(side=tk.LEFT)
            course_button = tk.Button(course_frame, text="Rename", command=lambda c=c[0]: self.rename_course(c))
            course_button.pack(side=tk.RIGHT)
            course_button = tk.Button(course_frame, text="Delete", command=lambda c=c[0]: self.delete_course(c))
            course_button.pack(side=tk.RIGHT)


    def view_tasks(self):
        # if there's already a frame, destroy it
        if self.scrollable_frame is not None:
            self.scrollable_frame.destroy()
        self.scrollable_frame = tk.Frame(self)
        self.scrollable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # self.scrollbar = tk.Scrollbar(self.scrollable_frame)
        # self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # self.listbox = tk.Listbox(self.scrollable_frame, yscrollcommand=self.scrollbar.set)
        # self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # self.scrollbar.config(command=self.listbox.yview)
        # self.listbox.bind('<Double-Button-1>', self.select_task)

        courses = db.select(self.cur, "courses", ["rowid", "name"], None, None)

        if len(courses) != 0:
            for course in courses:
                # put the course name in a scrollable frame
                course_frame = tk.Frame(self.scrollable_frame)
                course_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                course_label = tk.Label(course_frame, text=course[1], font=("Helvetica", 13, "bold"))
                course_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                
                # put the tasks below the course name
                tasks = db.select(self.cur, "tasks", ["name", "due_date", "priority"], "course_id=?", (course[0], ))
                if len(tasks) != 0:
                    for task in tasks:
                        # table of tasks
                        task_frame = tk.Frame(self.scrollable_frame)
                        task_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                        task_label = tk.Label(task_frame, text="{}{}  {}  {}".format('\u2666'*task[2], " "*3*(10-task[2]), task[0], task[1]), font=("Helvetica", 10))
                        task_label.pack(side=tk.TOP, fill=tk.X, expand=True)
                else:
                    tk.Label(self.scrollable_frame, text="No tasks", fg="gray", font=("Helvetica", 10)).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                
                # add a separator
                tk.Frame(self.scrollable_frame, height=2, bd=1, relief=tk.SUNKEN).pack(side=tk.TOP, fill=tk.X, pady=10)
        else:
            tk.Label(self.scrollable_frame, text="No courses", font=("Helvetica", 12)).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        

    def __del__(self):
        db.terminate(self.con)
    

if __name__ == "__main__":
    S = Schedule()
    S.mainloop()

    username = S.get_user()
    os.system("cls")
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