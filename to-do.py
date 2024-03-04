import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import *


def GetValue(event):
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    row_id = listBox.selection()[0]
    select = listBox.item(row_id, 'values')
    e1.insert(0, select[0])
    e2.insert(0, select[1])
    e3.insert(0, select[2])


def Add():
    task_id = e1.get()
    task_name = e2.get()
    due_date = e3.get()
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="root", database="task")
    mycursor = mysqldb.cursor()

    try:
        sql = "INSERT INTO tasks (id, task, due_date) VALUES (%s, %s, %s)"
        val = (task_id, task_name, due_date)
        mycursor.execute(sql, val)
        mysqldb.commit()
        last_id = mycursor.lastrowid
        messagebox.showinfo("Information", "Task Inserted Successfully")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e1.focus_set()
    except Exception as e:
        print(e)
        mysqldb.rollback()
    finally:
        mysqldb.close()


def Update():
    task_id = e1.get()
    task_name = e2.get()
    due_date = e3.get()
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="root", database="task")
    mycursor = mysqldb.cursor()

    try:
        sql = "UPDATE tasks SET task = %s, due_date = %s WHERE id = %s"
        val = (task_name, due_date, task_id)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Task Updated Successfully")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e1.focus_set()
    except Exception as e:
        print(e)
        mysqldb.rollback()
    finally:
        mysqldb.close()


def Delete():
    task_id = e1.get()
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="root", database="task")
    mycursor = mysqldb.cursor()

    try:
        sql = "DELETE FROM tasks WHERE id = %s"
        val = (task_id,)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Task Deleted Successfully")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e1.focus_set()
    except Exception as e:
        print(e)
        mysqldb.rollback()
    finally:
        mysqldb.close()


def Search():
    task_id = e1.get()
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="root", database="task")
    mycursor = mysqldb.cursor()

    try:
        sql = "SELECT id, task, due_date FROM tasks WHERE id = %s"
        val = (task_id,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()

        if result:
            e2.delete(0, END)
            e3.delete(0, END)
            e2.insert(0, result[1])
            e3.insert(0, result[2])
            messagebox.showinfo("Information", "Search Successful")
        else:
            messagebox.showinfo("Information", "Task not found")

    except Exception as e:
        print(e)
    finally:
        mysqldb.close()


def Show():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="root", database="task")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT id, task, due_date FROM tasks")
    records = mycursor.fetchall()

    for i, (id, task, due_date) in enumerate(records, start=1):
        listBox.insert("", "end", values=(id, task, due_date))

    mysqldb.close()


root = Tk()
root.geometry("800x500")
global e1
global e2
global e3

Label(root, text="To-Do List", fg="red", font=(None, 30)).place(x=300, y=5)
Label(root, text="Task ID").place(x=10, y=10)
Label(root, text="Task Name").place(x=10, y=40)
Label(root, text="Due Date").place(x=10, y=70)

e1 = Entry(root)
e1.place(x=140, y=10)

e2 = Entry(root)
e2.place(x=140, y=40)

e3 = Entry(root)
e3.place(x=140, y=70)

Button(root, text="Add", height=3, width=13, command=Add).place(x=30, y=100)
Button(root, text="Update", height=3, width=13, command=Update).place(x=140, y=100)
Button(root, text="Delete", height=3, width=13, command=Delete).place(x=250, y=100)
Button(root, text="Search", height=3, width=13, command=Search).place(x=360, y=100)

cols = ('id', 'task', 'due_date')
listBox = ttk.Treeview(root, columns=cols, show='headings')  # Like columns
for col in cols:
    listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)
    listBox.place(x=10, y=200)

Show()
listBox.bind('<Double-Button-1>', GetValue)  # DOUBLE CLICK ON BLUE LINE HIGHLIGHT FOR GETTING VALUE

root.mainloop()
