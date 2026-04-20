"""
InSync - Student Health & Emergency Record System
==================================================
Requirements covered:
  - Data structures   : list of dicts, nested dicts, list of contacts
  - Conditional       : if/elif/else throughout (login, validation, search)
  - Iterative         : for loops for display, search, file reading
  - Functions         : every action is its own clearly-named function
  - File handling     : save/load records to students.json using 'json' module
  - Standard libraries: tkinter, json, os, datetime
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json                        # standard library — save/load student data
import os                          # standard library — check if file exists
from datetime import datetime      # standard library — timestamp each record


DATA_FILE  = "students.json"
STAFF_PASS = "admin123"

students = []     # main list — holds all student dictionaries
next_id  = 1      # auto-incrementing ID counter

#  FILE HANDLING — save & load

def save_to_file():
    """
    FILE HANDLING (write):
    Saves the current students list to a JSON file so data
    is not lost when the program closes.
    """
    data = {
        "next_id" : next_id,
        "students": students
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_from_file():
    """
    FILE HANDLING (read):
    Loads student records from the JSON file when the program starts.
    If the file does not exist yet, we start with an empty list.
    """
    global students, next_id

    if os.path.exists(DATA_FILE):           # CONDITIONAL: only read if file exists
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        students = data.get("students", [])
        next_id  = data.get("next_id",  1)
    else:
        students = []                       # no file yet — start fresh
        next_id  = 1


#  DATA STRUCTURE HELPERS

def make_student(name, age, grade, health,
                 contact_name, contact_number,
                 address, relationship):
    """
    FUNCTION + DATA STRUCTURE:
    Builds and returns one student dictionary.
    """
    global next_id

    student = {
        "id"        : next_id,
        "name"      : name,
        "age"       : age,
        "grade"     : grade,
        "health"    : health,
        "registered": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "contacts"  : [
            {
                "name"        : contact_name,
                "number"      : contact_number,
                "address"     : address,
                "relationship": relationship
            }
        ]
    }

    next_id += 1
    return student


def find_by_id(student_id):
    """
    FUNCTION + ITERATIVE + CONDITIONAL:
    Loops through students and returns the one with a matching ID.
    Returns None if not found.
    """
    for student in students:                   # ITERATIVE
        if student["id"] == student_id:        # CONDITIONAL
            return student
    return None


def search_by_name(query):
    """
    FUNCTION + ITERATIVE + CONDITIONAL:
    Returns a list of students whose name contains the search query.
    """
    query = query.strip().lower()

    if not query:                              # CONDITIONAL: empty search
        return []

    results = []
    for student in students:                   # ITERATIVE: check every student
        if query in student["name"].lower():   # CONDITIONAL: partial match
            results.append(student)

    return results


def delete_student(student_id):
    """
    FUNCTION + ITERATIVE + CONDITIONAL:
    Removes the student with the given ID from the list, then saves.
    """
    global students
    original_count = len(students)

    students = [s for s in students if s["id"] != student_id]  # ITERATIVE

    if len(students) < original_count:         # CONDITIONAL
        save_to_file()
        return True
    return False


def validate_fields(fields_dict):
    """
    FUNCTION + ITERATIVE + CONDITIONAL:
    Checks that every field has a non-empty value.
    Returns (True, "") on success or (False, field_name) on failure.
    """
    for label, value in fields_dict.items():   # ITERATIVE
        if not value.strip():                  # CONDITIONAL
            return False, label
    return True, ""


#  MAIN WINDOW SETUP

root = tk.Tk()
root.title("InSync — Student Health & Emergency System")
root.geometry("750x560")
root.resizable(False, False)


#  REUSABLE UI HELPERS

def clear_window():
    """FUNCTION: destroy all widgets so we can redraw the screen."""
    for widget in root.winfo_children():
        widget.destroy()


def make_center_frame():
    """FUNCTION: return a frame centered in the window."""
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    return frame


def make_entry(parent, label_text, variable, hide=False):
    """FUNCTION: add a label + entry pair to a parent widget."""
    tk.Label(parent, text=label_text).pack(pady=(5, 0))
    tk.Entry(parent, textvariable=variable,
             show="*" if hide else "",
             justify="center").pack(pady=4)


def make_button(parent, text, command, width=22):
    """FUNCTION: add a button to a parent widget."""
    tk.Button(parent, text=text, command=command,
              width=width).pack(pady=5)


def make_table(parent, columns, col_width=130):
    """
    FUNCTION + ITERATIVE:
    Build a Treeview table with a scrollbar.
    """
    frame = tk.Frame(parent)
    frame.pack(expand=True, fill="both", pady=8, padx=10)

    scrollbar = ttk.Scrollbar(frame, orient="vertical")
    tree = ttk.Treeview(frame, columns=columns,
                        show="headings",
                        yscrollcommand=scrollbar.set)
    scrollbar.config(command=tree.yview)

    for col in columns:                    # ITERATIVE: configure every column
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=col_width)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return tree


def make_page_title(text):
    """FUNCTION: render a page heading at the top of the window."""
    tk.Label(root, text=text, font=("Segoe UI", 14, "bold")).pack(pady=(18, 4))


#  STUDENT FORM

def student_form():
    clear_window()
    frame = make_center_frame()

    tk.Label(frame, text="Student Registration",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

    name_var   = tk.StringVar()
    age_var    = tk.StringVar()
    grade_var  = tk.StringVar()
    health_var = tk.StringVar()
    cname_var  = tk.StringVar()
    cnum_var   = tk.StringVar()
    addr_var   = tk.StringVar()
    rel_var    = tk.StringVar()

    make_entry(frame, "Student Name",     name_var)
    make_entry(frame, "Age",              age_var)
    make_entry(frame, "Grade / Section",  grade_var)
    make_entry(frame, "Health Condition", health_var)

    tk.Label(frame, text="── Emergency Contact ──").pack(pady=(8, 0))

    make_entry(frame, "Contact Name",   cname_var)
    make_entry(frame, "Contact Number", cnum_var)
    make_entry(frame, "Address",        addr_var)
    make_entry(frame, "Relationship",   rel_var)

    def submit():
        # FUNCTION (inner) + ITERATIVE + CONDITIONAL
        fields = {
            "Student Name"    : name_var.get(),
            "Age"             : age_var.get(),
            "Grade / Section" : grade_var.get(),
            "Health Condition": health_var.get(),
            "Contact Name"    : cname_var.get(),
            "Contact Number"  : cnum_var.get(),
            "Address"         : addr_var.get(),
            "Relationship"    : rel_var.get()
        }
        ok, missing = validate_fields(fields)

        if not ok:                             # CONDITIONAL: missing field
            messagebox.showwarning("Incomplete", f"Please fill in: {missing}")
            return

        if not age_var.get().strip().isdigit():   # CONDITIONAL: age must be a number
            messagebox.showwarning("Invalid Age", "Age must be a number (e.g. 16).")
            return

        new_student = make_student(
            name           = name_var.get().strip(),
            age            = age_var.get().strip(),
            grade          = grade_var.get().strip(),
            health         = health_var.get().strip(),
            contact_name   = cname_var.get().strip(),
            contact_number = cnum_var.get().strip(),
            address        = addr_var.get().strip(),
            relationship   = rel_var.get().strip()
        )

        students.append(new_student)
        save_to_file()                         # FILE HANDLING: save immediately

        messagebox.showinfo("Registered",
                            f"Saved successfully!\nYour Student ID: {new_student['id']}")
        main_menu()

    make_button(frame, "Submit", submit)
    make_button(frame, "Back",   main_menu)


#  STAFF LOGIN

def staff_login():
    clear_window()
    frame = make_center_frame()

    tk.Label(frame, text="Staff Login",
             font=("Segoe UI", 14, "bold")).pack(pady=15)

    password_var = tk.StringVar()
    make_entry(frame, "Enter Password", password_var, hide=True)

    def login():
        entered = password_var.get()

        if not entered:                        # CONDITIONAL: empty
            messagebox.showwarning("Empty", "Please enter a password.")
        elif entered == STAFF_PASS:            # CONDITIONAL: correct
            messagebox.showinfo("Welcome", "Access granted. Welcome, Staff!")
            staff_menu()
        else:                                  # CONDITIONAL: wrong
            messagebox.showerror("Denied", "Incorrect password.")

    make_button(frame, "Login", login)
    make_button(frame, "Back",  main_menu)


#  STAFF MENU

def staff_menu():
    clear_window()
    frame = make_center_frame()

    tk.Label(frame, text="Staff Panel",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

    tk.Label(frame, text=f"Total Records on File: {len(students)}").pack(pady=(0, 10))

    make_button(frame, "View Health Records",     view_health)
    make_button(frame, "View Emergency Contacts", view_contacts)
    make_button(frame, "Search Student",          search_student)
    make_button(frame, "Delete a Record",         delete_record)
    make_button(frame, "Logout",                  main_menu)


#  VIEW HEALTH RECORDS

def view_health():
    clear_window()
    make_page_title("Health Records")

    if not students:                           # CONDITIONAL
        tk.Label(root, text="No records found.").pack(pady=20)
    else:
        columns = ("ID", "Name", "Age", "Grade", "Health Condition", "Registered")
        tree = make_table(root, columns, col_width=112)

        for s in students:                     # ITERATIVE: one row per student
            tree.insert("", "end", values=(
                s["id"],
                s["name"],
                s.get("age",        "—"),
                s.get("grade",      "—"),
                s["health"],
                s.get("registered", "—")
            ))

    make_button(root, "Back", staff_menu)


#  VIEW EMERGENCY CONTACTS

def view_contacts():
    clear_window()
    make_page_title("Emergency Contacts")

    if not students:                           # CONDITIONAL
        tk.Label(root, text="No records found.").pack(pady=20)
    else:
        columns = ("Stu. ID", "Student", "Contact Name",
                   "Number", "Relationship", "Address")
        tree = make_table(root, columns, col_width=108)

        for s in students:                     # ITERATIVE: outer loop — students
            for contact in s["contacts"]:      # ITERATIVE: inner loop — contacts
                tree.insert("", "end", values=(
                    s["id"],
                    s["name"],
                    contact["name"],
                    contact["number"],
                    contact["relationship"],
                    contact["address"]
                ))

    make_button(root, "Back", staff_menu)


#  SEARCH STUDENT

def search_student():
    clear_window()
    make_page_title("Search Student")

    search_frame = tk.Frame(root)
    search_frame.pack(pady=6)

    search_var = tk.StringVar()
    tk.Label(search_frame, text="Enter Name:").pack(side="left", padx=6)
    tk.Entry(search_frame, textvariable=search_var, width=24).pack(side="left", padx=6)

    result_frame = tk.Frame(root)
    result_frame.pack(expand=True, fill="both")

    def perform_search():
        for widget in result_frame.winfo_children():  # ITERATIVE: clear old results
            widget.destroy()

        results = search_by_name(search_var.get())

        if not results:                        # CONDITIONAL
            tk.Label(result_frame, text="No matching students found.").pack(pady=10)
            return

        columns = ("ID", "Name", "Age", "Grade", "Health", "Contact", "Number")
        tree = make_table(result_frame, columns, col_width=100)

        for s in results:                      # ITERATIVE: one row per result
            first = s["contacts"][0]
            tree.insert("", "end", values=(
                s["id"],
                s["name"],
                s.get("age",   "—"),
                s.get("grade", "—"),
                s["health"],
                first["name"],
                first["number"]
            ))

    tk.Button(search_frame, text="Search",
              command=perform_search).pack(side="left", padx=6)

    make_button(root, "Back", staff_menu)


#  DELETE A RECORD

def delete_record():
    clear_window()
    make_page_title("Delete a Record")

    frame = make_center_frame()

    tk.Label(frame, text="Enter Student ID to delete:").pack(pady=(10, 4))

    id_var      = tk.StringVar()
    preview_var = tk.StringVar(value="")

    tk.Entry(frame, textvariable=id_var, justify="center").pack(pady=6)
    tk.Label(frame, textvariable=preview_var).pack()

    def preview():
        """FUNCTION + CONDITIONAL: look up ID and preview the student name."""
        raw = id_var.get().strip()

        if not raw.isdigit():                  # CONDITIONAL
            preview_var.set("Please enter a valid numeric ID.")
            return

        found = find_by_id(int(raw))

        if found:                              # CONDITIONAL
            preview_var.set(
                f"Found: {found['name']}  |  "
                f"Grade: {found.get('grade', '?')}  |  "
                f"ID: {found['id']}"
            )
        else:
            preview_var.set("No student found with that ID.")

    def confirm_delete():
        """FUNCTION + CONDITIONAL: confirm then delete."""
        raw = id_var.get().strip()

        if not raw.isdigit():                  # CONDITIONAL
            messagebox.showwarning("Invalid", "Enter a numeric ID.")
            return

        sid   = int(raw)
        found = find_by_id(sid)

        if not found:                          # CONDITIONAL
            messagebox.showerror("Not Found", "No student with that ID.")
            return

        confirmed = messagebox.askyesno(
            "Confirm Delete",
            f"Delete record for '{found['name']}'?\nThis cannot be undone."
        )

        if confirmed:                          # CONDITIONAL
            success = delete_student(sid)
            if success:                        # CONDITIONAL
                messagebox.showinfo("Deleted", "Record removed successfully.")
                staff_menu()
            else:
                messagebox.showerror("Error", "Could not delete record.")

    make_button(frame, "Preview",        preview)
    make_button(frame, "Confirm Delete", confirm_delete)
    make_button(frame, "Back",           staff_menu)

#  MAIN MENU

def main_menu():
    clear_window()
    frame = make_center_frame()

    tk.Label(frame, text="InSync",
             font=("Segoe UI", 28, "bold")).pack(pady=(20, 0))

    tk.Label(frame, text="Student Health & Emergency Record System").pack(pady=(0, 24))

    make_button(frame, "Student — Register Info", student_form)
    make_button(frame, "Staff — View Records",    staff_login)

    tk.Label(frame, text=f"{len(students)} record(s) currently on file").pack(pady=(16, 0))


#  STARTUP

load_from_file()       # FILE HANDLING: read existing records on startup
main_menu()
root.mainloop()