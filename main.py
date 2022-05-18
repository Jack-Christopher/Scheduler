import os
import datetime
import tkinter as tk
import database as db
from time import sleep
from tkinter import simpledialog
from tkcalendar import Calendar, DateEntry


class Schedule(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Scheduler - Managment of my tasks')
        self.geometry('500x600+500+20')
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

        # init view
        self.view_tasks()
        
    
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
        new_name.iconphoto(False, tk.PhotoImage(file='scheduler.png'))
                 
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
        new_course = tk.Toplevel(self)
        new_course.title("Add course")
        new_course.geometry('300x50+600+200')
        new_course.iconphoto(False, tk.PhotoImage(file='scheduler.png'))
                 
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

    def select_date(self, new_task, selected):
        top = tk.Toplevel(new_task)
        # get current date
        date = datetime.datetime.now() 
        cal = Calendar(top, font="Arial 14", selectmode='day', cursor="hand2", year=date.year, month=date.month, day=date.day, date_pattern="dd-mm-yyyy")
        cal.pack(fill="both", expand=True)
        
        def get_values():
            selected['date'] = cal.get_date()
            # print("SD: ", selected['date'])
            top.destroy()
        tk.Button(top, text="Choose", command=lambda: get_values()).pack(pady=10)
        top.mainloop()


    def select_course(self, new_task, selected):
        courses = db.select(self.cur, "courses", ["rowid", "name"], None, None)
        course_list = []
        for c in courses:
            course_list.append(str(c[0]) + "-. " + c[1])
        # list box to select the course
        course_selection = tk.Toplevel(new_task)
        course_selection.title("Select course")
        course_selection.geometry('300x200+600+200')
        course_selection.iconphoto(False, tk.PhotoImage(file='scheduler.png'))

        course_listbox = tk.Listbox(course_selection, selectmode=tk.SINGLE)
        for course in course_list:
            course_listbox.insert(tk.END, course)
        course_listbox.pack(fill=tk.BOTH, expand=True)

        def get_values():
            selected['course'] = course_listbox.get(tk.ACTIVE)
            course_selection.destroy()
            # print("SC: ", selected['course'])

        tk.Button(course_selection, text="OK", command=lambda: get_values()).pack()
        course_selection.mainloop()

        
    def add_task(self):
        # New window to introduce the new task name, task priority due date and task course
        new_task = tk.Toplevel(self)
        new_task.title("Add task")
        new_task.geometry('300x190+600+200')
        new_task.iconphoto(False, tk.PhotoImage(file='scheduler.png'))

        # add entry for task name with label
        new_task_name_label = tk.Label(new_task, text="Task name:").pack(side=tk.TOP)
        new_task_name_entry = tk.Entry(new_task)
        new_task_name_entry.pack(fill=tk.X)
        # add number selector between 1-10 for task priority with label
        new_task_priority_label = tk.Label(new_task, text="Task priority:").pack(side=tk.TOP)
        new_task_priority_entry = tk.Spinbox(new_task, from_=1, to=10)
        new_task_priority_entry.pack(fill=tk.X)
        # add date picker for task due date
        selected = {'date': "", 'course': ""}
        date_button = tk.Button(new_task, text="Select Due Date", command=lambda: self.select_date(new_task, selected) ).pack(fill=tk.X)
        course_button = tk.Button(new_task, text="Select Course", command=lambda: self.select_course(new_task, selected) ).pack(fill=tk.X)

        def add_task_helper(task_name, task_priority, task_due_date, task_course):
            course_id = int(task_course.split("-. ")[0])

            db.insert(self.con, self.cur, "tasks", ["name", "priority", "due_date", "course_id"], (task_name, task_priority, task_due_date, course_id))
            new_task.destroy()
            # print("Data: ", task_name, task_priority, task_due_date, task_course)
            self.view_tasks()

        # add button to add task
        new_task_button = tk.Button(new_task, text="Add", command=lambda: add_task_helper(new_task_name_entry.get(), new_task_priority_entry.get(), selected['date'], selected['course']))
        new_task_button.pack(side=tk.BOTTOM, pady=10)
        
        new_task.mainloop()        


    def delete_task(self, task_id):
        db.delete(self.con, self.cur, "tasks", "rowid=?", (task_id, ))
        self.view_tasks()


    def view_tasks(self):
        # if there's already a frame, destroy it
        if self.scrollable_frame is not None:
            self.scrollable_frame.destroy()
        self.scrollable_frame = tk.Frame(self)
        self.scrollable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        courses = db.select(self.cur, "courses", ["rowid", "name"], None, None)

        if len(courses) != 0:
            for course in courses:
                # put the course name in a scrollable frame
                course_frame = tk.Frame(self.scrollable_frame)
                course_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                course_label = tk.Label(course_frame, text=course[1], font=("Helvetica", 13, "bold"))
                course_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                
                # put the tasks below the course name
                tasks = db.select(self.cur, "tasks", ["name", "due_date", "priority", "rowid"], "course_id=?", (course[0], ))
                if len(tasks) != 0:
                    for task in tasks:
                        # table of tasks
                        task_frame = tk.Frame(self.scrollable_frame)
                        task_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                        priority_label = tk.Label(task_frame, text="  {}{}".format('\u2666'*task[2], " "*(10-task[2])), font=("Courier", 10), justify=tk.LEFT)
                        task_label = tk.Label(task_frame, text="  {}".format(task[0]), font=("Courier", 10), justify=tk.LEFT, width=24, wraplength=200)
                        date_label = tk.Label(task_frame, text="  {}".format(task[1]), font=("Courier", 10), justify=tk.LEFT, width=12, wraplength=100)

                        priority_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                        task_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                        date_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                        # delete  option
                        delete_button = tk.Button(task_frame, text="Delete", command=lambda id=task[3]: self.delete_task(id))
                        delete_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)

                else:
                    tk.Label(self.scrollable_frame, text="No tasks", fg="gray", font=("Courier", 10)).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                
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