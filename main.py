import tkinter as tk
from tkinter import *
from tkinter import messagebox  # Import messagebox

root = Tk()
root.title("To-Do-List")
root.geometry("420x700+400+100")  # Increased window height to avoid overlap
root.resizable(False, False)

task_list = []

def addTask():
    task = task_entry.get()
    task_entry.delete(0, END)
    
    if task:
        with open("file/tasklist.txt", 'a', encoding='utf-8') as tf:  # Use utf-8 encoding
            tf.write(f"{task}\n")
        task_list.append(task)
        listbox.insert(END, task)

def deleteTask():
    global task_list
    task = str(listbox.get(ANCHOR))
    if task in task_list:
        task_list.remove(task)
        with open("file/tasklist.txt", 'w', encoding='utf-8') as tf:  # Use utf-8 encoding
            for task in task_list:
                tf.write(task + "\n")
        listbox.delete(ANCHOR)

def completeTask():
    try:
        selected_task = listbox.get(ANCHOR)
        # Mark task as completed
        updated_task = f"{selected_task} ✔"  # Adding a checkmark to denote completion
        task_list[task_list.index(selected_task)] = updated_task  # Update in task_list
        
        # Update the listbox and task file
        listbox.delete(ANCHOR)
        listbox.insert(ANCHOR, updated_task)
        
        with open("file/tasklist.txt", 'w', encoding='utf-8') as tf:  # Use utf-8 encoding
            for task in task_list:
                tf.write(task + "\n")
    except ValueError:
        messagebox.showwarning("Complete Error", "Please select a task to mark as complete.")

def openTaskFile():
    try:
        global task_list
        with open("file/tasklist.txt", "r", encoding='utf-8') as taskfile:  # Use utf-8 encoding
            tasks = taskfile.readlines()
        
        for task in tasks:
            if task.strip():  # Avoid empty lines
                task_list.append(task.strip())
                listbox.insert(END, task.strip())
    except FileNotFoundError:
        with open("file/tasklist.txt", 'w', encoding='utf-8') as taskfile:  # Use utf-8 encoding
            pass  # Create the file if it doesn't exist

def searchTasks():
    search_query = search_entry.get().lower()  # Get the search query and convert to lowercase
    listbox.delete(0, END)  # Clear the current listbox
    
    # Insert tasks that match the search query
    for task in task_list:
        if search_query in task.lower():  # Check if the search query is in the task
            listbox.insert(END, task)

# Key Bindings
def on_enter_key(event):
    addTask()

def on_delete_key(event):
    deleteTask()

# Soft Pastels Color Palette
BG_COLOR = "#FFFAF3"  # Soft Cream
TASK_LIST_BG = "#FFE5D9"  # Light Peach
TEXT_COLOR = "#5C5C5C"  # Medium Gray
BUTTON_BG = "#FF847C"  # Coral Pink
BUTTON_TEXT = "#FFFFFF"  # White
HIGHLIGHT_BG = "#D8A7B1"  # Soft Mauve

# UI Setup
root.configure(bg=BG_COLOR)

heading = Label(root, text="ALL TASK", font="arial 22 bold", fg=TEXT_COLOR, bg=BG_COLOR)
heading.place(x=130, y=20)

# Main Entry Frame
frame = Frame(root, width=400, height=50, bg=BG_COLOR)
frame.place(x=0, y=100)  # Lowered the main task entry

task_entry = Entry(frame, width=18, font="arial 20", bd=0, bg=TASK_LIST_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
task_entry.place(x=10, y=7)
task_entry.focus()

button = Button(frame, text="ADD", font="arial 20 bold", width=6, bg=BUTTON_BG, fg=BUTTON_TEXT, activebackground=HIGHLIGHT_BG, activeforeground=BUTTON_TEXT, bd=0, command=addTask)
button.place(x=300, y=0)

# Search Entry Frame
search_frame = Frame(root, width=400, height=50, bg=BG_COLOR)
search_frame.place(x=0, y=160)  # Lowered the search frame

search_entry = Entry(search_frame, width=18 , font="arial 20", bd=0, bg=TASK_LIST_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
search_entry.place(x=10, y=7)
search_entry.focus()

search_button = Button(search_frame, text="FIND", font="arial 20 bold", width=6, bg=BUTTON_BG, fg=BUTTON_TEXT, activebackground=HIGHLIGHT_BG, activeforeground=BUTTON_TEXT, bd=0, command=searchTasks)
search_button.place(x=300, y=0)

# Listbox Frame
frame1 = Frame(root, bd=3, width=700, height=200, bg=BG_COLOR)
frame1.pack(pady=(210, 0))  # Lowered the listbox frame

listbox = Listbox(frame1, font=('arial', 12), width=40, height=16, bg=TASK_LIST_BG, fg=TEXT_COLOR, selectbackground=HIGHLIGHT_BG, selectforeground=TEXT_COLOR, cursor="hand2", bd=0)
listbox.pack(side=LEFT, fill=BOTH, padx=2)
scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=BOTH)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

openTaskFile()

# Delete Button
delete_button = Button(root, text="DELETE", font="arial 20 bold", bg=BUTTON_BG, fg=BUTTON_TEXT, activebackground=HIGHLIGHT_BG, activeforeground=BUTTON_TEXT, bd=0, command=deleteTask)
delete_button.pack(side=BOTTOM, pady=20)

# Complete Button
complete_button = Button(root, text="COMPLETE", font="arial 20 bold", bg=BUTTON_BG, fg=BUTTON_TEXT, activebackground=HIGHLIGHT_BG, activeforeground=BUTTON_TEXT, bd=0, command=completeTask)
complete_button.pack(side=BOTTOM, pady=10)

# Drag-and-Drop Functions
def on_drag_start(event):
    global dragged_task, dragged_task_index
    dragged_task_index = listbox.nearest(event.y)  # Get the task index based on the mouse position
    if dragged_task_index != -1:
        dragged_task = listbox.get(dragged_task_index)  # Get the task text

def on_drag_motion(event):
    # Simulate drag by highlighting the current index (not necessary for actual dragging)
    listbox.select_clear(0, END)
    listbox.select_set(dragged_task_index)

def on_drop(event):
    global dragged_task, dragged_task_index
    if dragged_task:
        drop_index = listbox.nearest(event.y)
        if drop_index != -1 and drop_index != dragged_task_index:
            # Swap the dragged task with the task at the drop index
            task_list.remove(dragged_task)
            task_list.insert(drop_index, dragged_task)
            
            # Update listbox and file
            listbox.delete(0, END)
            for task in task_list:
                listbox.insert(END, task)
            
            with open("tasklist.txt", 'w', encoding='utf-8') as tf:  # Use utf-8 encoding
                for task in task_list:
                    tf.write(task + "\n")
        dragged_task = None  # Reset the dragged task

# Bind the mouse events for drag-and-drop
listbox.bind("<ButtonPress-1>", on_drag_start)
listbox.bind("<B1-Motion>", on_drag_motion)
listbox.bind("<ButtonRelease-1>", on_drop)

# Bind Keys
root.bind("<Return>", on_enter_key)  # Bind Enter key
root.bind("<Delete>", on_delete_key)  # Bind Delete key

root.mainloop()

