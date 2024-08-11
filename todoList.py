import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import mysql.connector

# Database Connection
db = mysql.connector.connect(
    host='localhost',
    user='[YOUR_USERNAME]',
    password='[YOUR_PASSWORD]',
    database='todoList'
)

def add_task(tasksName, description):
    cursor = db.cursor()
    sql = "INSERT INTO tasks (tasksName, description) VALUES (%s, %s)"
    val = (tasksName, description)
    cursor.execute(sql, val)
    db.commit()

def get_tasks():
    cursor = db.cursor()
    sql = "SELECT * FROM tasks"
    cursor.execute(sql)
    return cursor.fetchall()

def mark_completed(taskID):
    cursor = db.cursor()
    sql = "UPDATE tasks SET isCompleted = 1 WHERE id = %s"
    val = (taskID,)
    cursor.execute(sql, val)
    db.commit()

def update_task(taskID, tasksName, description):
    cursor = db.cursor()
    sql = "UPDATE tasks SET tasksName = %s, description = %s WHERE id = %s"
    val = (tasksName, description, taskID)
    cursor.execute(sql, val)
    db.commit()

def delete_task(taskID):
    cursor = db.cursor()
    sql = "DELETE FROM tasks WHERE id = %s"
    val = (taskID,)
    cursor.execute(sql, val)
    db.commit()

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self):
        # Frame for adding tasks
        add_frame = tk.Frame(self.root)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Task Name:").grid(row=0, column=0, padx=5)
        self.task_name_entry = tk.Entry(add_frame, width=30)
        self.task_name_entry.grid(row=0, column=1, padx=5)

        tk.Label(add_frame, text="Description:").grid(row=1, column=0, padx=5)
        self.description_entry = tk.Entry(add_frame, width=30)
        self.description_entry.grid(row=1, column=1, padx=5)

        tk.Button(add_frame, text="Add Task", command=self.add_task_gui).grid(row=2, column=0, columnspan=2, pady=5)

        # Treeview for displaying tasks
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Description", "Completed"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Task Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Completed", text="Completed")
        self.tree.pack(pady=10)

        # Buttons for operations
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Mark as Completed", command=self.mark_completed_gui).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Task", command=self.update_task_gui).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Task", command=self.delete_task_gui).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_tasks).grid(row=0, column=3, padx=5)

    def add_task_gui(self):
        tasksName = self.task_name_entry.get()
        description = self.description_entry.get()
        if tasksName:
            add_task(tasksName, description)
            messagebox.showinfo("Success", "Task added successfully!")
            self.task_name_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.refresh_tasks()
        else:
            messagebox.showwarning("Input Error", "Task name cannot be empty.")

    def refresh_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        tasks = get_tasks()
        for task in tasks:
            self.tree.insert('', tk.END, values=(task[0], task[1], task[2], "Yes" if task[3] else "No"))

    def get_selected_task_id(self):
        selected_item = self.tree.selection()
        if selected_item:
            task = self.tree.item(selected_item)
            return task['values'][0]
        else:
            messagebox.showwarning("Selection Error", "No task selected.")
            return None

    def mark_completed_gui(self):
        taskID = self.get_selected_task_id()
        if taskID:
            mark_completed(taskID)
            messagebox.showinfo("Success", "Task marked as completed!")
            self.refresh_tasks()

    def update_task_gui(self):
        taskID = self.get_selected_task_id()
        if taskID:
            new_name = simpledialog.askstring("Update Task", "Enter new task name:")
            new_description = simpledialog.askstring("Update Task", "Enter new description:")
            if new_name:
                update_task(taskID, new_name, new_description)
                messagebox.showinfo("Success", "Task updated successfully!")
                self.refresh_tasks()
            else:
                messagebox.showwarning("Input Error", "Task name cannot be empty.")

    def delete_task_gui(self):
        taskID = self.get_selected_task_id()
        if taskID:
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?")
            if confirm:
                delete_task(taskID)
                messagebox.showinfo("Success", "Task deleted successfully!")
                self.refresh_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
