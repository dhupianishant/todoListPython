# To-Do List Application

A simple Tkinter-based To-Do List application that uses a MySQL database for data storage. This project allows users to add, view, update, mark as completed, and delete tasks through a graphical user interface (GUI).

## Features

- **Add Task:** Add a new task with a name and description.
- **View Tasks:** Display all tasks stored in the database.
- **Mark Task as Completed:** Mark a task as completed.
- **Update Task:** Update the name and description of a task.
- **Delete Task:** Remove a task from the database.

## Requirements

- **Python 3.12**
- **MySQL Server**
- **Tkinter:** Usually included with Python.
- **MySQL Connector for Python:** Install it using `pip install mysql-connector-python`.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/todoListApp.git
cd todoListApp
```

### 2. Set up the MySQL Database:
- Import the 'todoList.sql' file into your MySQL Server:
  ```bash
  mysql -u root -p < todoList.sql
  ```
- Replace 'root' with your MySQL username

### 3. Update the MySQL connection settings in `todo_app.py`:
```python
db = mysql.connector.connect(
    host='localhost',
    user='[YOUR_USERNAME]',
    password='[YOUR_PASSWORD]',
    database='todoList'
)
```

### 4. Run the application:
```bash
python todoList.py
```

## License

This project is open-source and available to all under the MIT License.
