import tkinter as tk                                        
from tkinter import Label, Menu, messagebox, simpledialog   
import json                                                 
import os                                                   
from datetime import datetime, date                         

TASKS_FILE = "tasks.json"     
tasks = []                    
dark_mode = False             

# ----------------------- TASK LOGIC -----------------------

def load_tasks():
    if os.path.exists(TASKS_FILE):                 
        with open(TASKS_FILE, "r") as f:           
            return json.load(f)                     
    return []

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)               

def update_task_list():
    task_listbox.delete(0, tk.END)                  
    for task in tasks:
        status = "✅" if task["done"] else "❌"
        task_listbox.insert(tk.END, f'{task["id"]}. [{status}] {task["title"]} | Due: {task["due"]} | Priority: {task["priority"]}')

def add_task():
    title = simpledialog.askstring("Task Title", "Enter task title:")
    if not title:
        return
    due = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):")
    priority = simpledialog.askstring("Priority", "Enter priority (low/medium/high):")   
    task = {                                                                            
        "id": len(tasks) + 1,                                                            
        "title": title,
        "due": due,
        "priority": priority,
        "done": False
    }
    tasks.append(task)
    update_task_list()

def delete_task():
    selected = task_listbox.curselection()                              
    if selected:
        index = selected[0]
        task = tasks.pop(index)
        update_task_list()
        messagebox.showinfo("Deleted", f"Deleted task: {task['title']}")
    else:
        messagebox.showwarning("No selection", "Please select a task to delete.")

def mark_done():                                        
    selected = task_listbox.curselection()
    if selected:
        index = selected[0]
        tasks[index]["done"] = True
        update_task_list()
        messagebox.showinfo("Marked Done", f'Marked "{tasks[index]["title"]}" as done!')
    else:
        messagebox.showwarning("No selection", "Please select a task to mark as done.")

def edit_task():                                       
    selected = task_listbox.curselection()
    if selected:
        index = selected[0]
        task = tasks[index]
        title = simpledialog.askstring("Edit Title", "Enter new title:", initialvalue=task["title"])
        due = simpledialog.askstring("Edit Due Date", "Enter new due date (YYYY-MM-DD):", initialvalue=task["due"])
        priority = simpledialog.askstring("Edit Priority", "Enter new priority (low/medium/high):", initialvalue=task["priority"])
        if title and due and priority:
            task["title"] = title
            task["due"] = due
            task["priority"] = priority
            update_task_list()
            messagebox.showinfo("Updated", "Task updated successfully.")
    else:
        messagebox.showwarning("No selection", "Please select a task to edit.")

def check_due_reminders():   
    today = date.today()
    due_today = []
    overdue = []

    for task in tasks:
        try:
            due_date = datetime.strptime(task["due"], "%Y-%m-%d").date()        
            if not task["done"]:
                if due_date == today:
                    due_today.append(task["title"])
                elif due_date < today:
                    overdue.append(task["title"])
        except:
            continue

    msg = ""
    if due_today:
        msg += "Tasks due *today*📅:\n" + "\n".join(f"• {t}" for t in due_today) + "\n\n"
    if overdue:
        msg += "*Overdue* tasks⚠️:\n" + "\n".join(f"• {t}" for t in overdue)

    if msg:
        messagebox.showinfo("Due Date Reminder 🔔", msg)

def save_and_exit():     
    save_tasks()
    root.destroy()

def toggle_theme():         
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():              
    bg = "#1C1818" if dark_mode else "#ffffff"
    fg = "#ffffff" if dark_mode else "#000000"
    btn_bg = "#161414" if dark_mode else "#fffafa"

    root.configure(bg=bg)
    task_listbox.configure(bg=bg, fg=fg, selectbackground="#322929" if dark_mode else "#cce6ff")

    for widget in btn_frame.winfo_children():
        widget.configure(bg=btn_bg, fg=fg)

    toggle_btn.configure(bg=btn_bg, fg=fg)


# ----------------------- MAIN APP WINDOW -----------------------

def launch_main_app():          
    global root, task_listbox, btn_frame, toggle_btn
    global tasks                                        #Declare GUI elements and task list as global to be accessed throughout.

    tasks = load_tasks()    

    root = tk.Tk()
    root.title("📝 To-Do List App")     #Create the main window and set the title.
    
    w = Label(root, text='Welcome to your To-Do List!')
    w.pack()    #Show a welcome label.

    menu = Menu(root)           #Set up basic menu bar(File and Help)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label='File', menu=filemenu)
    filemenu.add_command(label='New')
    filemenu.add_command(label='Open...')
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=root.quit)
    helpmenu = Menu(menu)
    menu.add_cascade(label='Help', menu=helpmenu)
    helpmenu.add_command(label='About')

    task_listbox = tk.Listbox(root, width=70, height=15)   #display area for the task
    task_listbox.pack(padx=10, pady=10)

    btn_frame = tk.Frame(root)      #Holds the task management buttons
    btn_frame.pack()

    #Create buttons for Add, Edit, Delete, Done, Save & Exit.
    tk.Button(btn_frame, text="Add Task ➕", width=15, command=add_task).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="Mark Done ✅", width=15, command=mark_done).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(btn_frame, text="Delete Task 🗑️", width=15, command=delete_task).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(btn_frame, text="Edit Task ✏️", width=15, command=edit_task).grid(row=0, column=3, padx=5, pady=5)
    tk.Button(btn_frame, text="Save & Exit 💾", width=15, command=save_and_exit).grid(row=0, column=4, padx=5, pady=5)

    #Button to switch themes.
    toggle_btn = tk.Button(root, text="Switch Theme 🌓", command=toggle_theme)
    toggle_btn.pack(pady=5)

    update_task_list()    #Initialize the task list, check for due tasks, apply current theme.
    check_due_reminders()
    apply_theme()

    root.mainloop()    #Start the Tkinter event loop.

# ----------------------- LOGIN WINDOW -----------------------

def login():                                #Handles login verification.
    username = user_entry.get()
    password = pass_entry.get()

    if username == "shreeja" and password == "welcome123":              #Hardcoded credentials.
        login_win.destroy()                                             #Close login window and launch main app on success.
        launch_main_app()
    else:                                                               #Show error if credentials are invalid.
        messagebox.showerror("Login Failed", "Invalid username or password.")

#------GUI Setup for Login---------

login_win = tk.Tk()      #Create the login window.
login_win.title("Login 🔐")
login_win.geometry("300x200")

tk.Label(login_win, text="Username:").pack(pady=5)    #Username and password entry fields.
user_entry = tk.Entry(login_win)
user_entry.pack()

tk.Label(login_win, text="Password:").pack(pady=5)
pass_entry = tk.Entry(login_win, show="*")
pass_entry.pack()

#Login button triggers the login logic.
tk.Button(login_win, text="Login", command=login).pack(pady=15)

login_win.mainloop()
#Starts login window’s event loop.


