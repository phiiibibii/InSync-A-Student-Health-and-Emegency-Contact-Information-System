# InSync – Student Health & Emergency Record System

## 📌 Overview

**InSync** is a Python-based desktop application built using Tkinter that manages student health records and emergency contact information. The system is designed to improve student safety by providing quick, organized, and accessible data for school staff, especially during emergencies.

---

## 🎯 Objectives

This system was developed to address the following key issues:

### 1. Lack of Real-Time Monitoring of Students’ Health and Contact Information

Many schools rely on scattered or outdated records, making it difficult to access student information when needed.

**InSync addresses this by:**

* Centralizing all student data into one system
* Allowing instant access to health and contact information
* Providing a digital record that is always available and up-to-date

---

### 2. Limited Health Information Monitoring

Traditional systems often fail to properly track or display important health conditions of students, which may lead to inadequate preparation during emergencies.

**InSync improves this by:**

* Recording student health conditions systematically
* Displaying health records in an organized table format
* Making health information easily viewable by authorized staff

---

### 3. Difficulty in Emergency Response and Accountability

During emergencies, delays in retrieving student information can affect response time and accountability. Schools may struggle to identify students' needs or contact guardians quickly.

**InSync solves this by:**

* Providing quick search functionality for students
* Linking each student with emergency contact details
* Allowing staff to retrieve critical information instantly

---

## ⚙️ Features

* 👨‍🎓 **Student Registration**

  * Input personal and health details
  * Add emergency contact information

* 🔐 **Staff Login System**

  * Secure access using a password

* 📋 **Health Records Viewer**

  * Displays all student health data in a structured table

* 📞 **Emergency Contacts Viewer**

  * Shows linked contact details for each student

* 🔍 **Search Function**

  * Quickly find students by name

* ❌ **Delete Records**

  * Remove records with confirmation

* 💾 **File Handling**

  * Saves and loads data using a JSON file (`students.json`)

---

## 🧱 Technologies Used

* **Python**
* **Tkinter** – GUI development
* **JSON** – Data storage
* **OS Module** – File handling
* **Datetime Module** – Timestamping

---

## 📁 File Structure

* `main.py` – Main program file
* `students.json` – Stored student records

---

## 🚀 How to Run

1. Ensure Python is installed
2. Run the program:

   ```bash
   python main.py
   ```
3. Use the interface:

   * Select **Student** to register
   * Select **Staff** to view records

---

## ⚠️ Notes

* Default staff password: `admin123`
* Ensure `students.json` is in the same folder
* Data is automatically saved after each registration

---

## 🔮 Future Improvements

* Real-time data syncing across multiple devices
* Multiple emergency contacts per student
* Edit/update student records
* Stronger authentication system
* Cloud-based database integration

---

## 👩‍💻 Author

Developed as part of an academic project focusing on:

* Data Structures
* File Handling
* GUI Programming
* Real-world problem solving in school systems

---
