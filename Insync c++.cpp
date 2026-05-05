/*
 * InSync - Student Health & Emergency Record System
 * ==================================================
 * Console-based C++ version
 * Features: list of structs, nested structs, conditionals,
 *           loops, functions, file handling (JSON-like CSV),
 *           yes/no navigation throughout
 */

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>
#include <ctime>
#include <limits>

using namespace std;

// ─────────────────────────────────────────────
//  DATA STRUCTURES
// ─────────────────────────────────────────────

struct EmergencyContact {
    string name;
    string number;
    string address;
    string relationship;
};

struct Student {
    int    id;
    string name;
    string age;
    string grade;
    string health;
    string registered;
    EmergencyContact contact;   // one contact per student (mirrors original)
};

// ─────────────────────────────────────────────
//  GLOBALS
// ─────────────────────────────────────────────

vector<Student> students;
int             nextId    = 1;
const string    DATA_FILE = "students_data.txt";
const string    STAFF_PASS = "admin123";

// ─────────────────────────────────────────────
//  UTILITY HELPERS
// ─────────────────────────────────────────────

// Clears the screen (cross-platform friendly fallback)
void clearScreen() {
    cout << "\n\n";
}

// Print a decorative banner line
void printLine(char c = '-', int len = 55) {
    cout << string(len, c) << "\n";
}

// Print a section header
void printHeader(const string& title) {
    clearScreen();
    printLine('=');
    cout << "  InSync | " << title << "\n";
    printLine('=');
}

// Get current datetime as string
string currentTime() {
    time_t now = time(nullptr);
    char buf[20];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M", localtime(&now));
    return string(buf);
}

// Convert string to lowercase
string toLower(const string& s) {
    string result = s;
    transform(result.begin(), result.end(), result.begin(), ::tolower);
    return result;
}

// Trim whitespace from both ends
string trim(const string& s) {
    size_t start = s.find_first_not_of(" \t\r\n");
    size_t end   = s.find_last_not_of(" \t\r\n");
    return (start == string::npos) ? "" : s.substr(start, end - start + 1);
}

// Escape pipe characters in stored strings (pipe is our delimiter)
string escape(const string& s) {
    string out;
    for (char c : s) {
        if (c == '|') out += "\\|";
        else          out += c;
    }
    return out;
}

// Unescape pipe characters when reading
string unescape(const string& s) {
    string out;
    for (size_t i = 0; i < s.size(); ++i) {
        if (s[i] == '\\' && i + 1 < s.size() && s[i+1] == '|') {
            out += '|';
            ++i;
        } else {
            out += s[i];
        }
    }
    return out;
}

// Ask a yes/no question; returns true for yes, false for no
bool askYesNo(const string& question) {
    string answer;
    while (true) {
        cout << question << " (yes/no): ";
        getline(cin, answer);
        answer = toLower(trim(answer));

        if (answer == "yes" || answer == "y") return true;
        if (answer == "no"  || answer == "n") return false;

        cout << "  Please type 'yes' or 'no'.\n";
    }
}

// Read a non-empty line from the user
string readLine(const string& prompt) {
    string value;
    while (true) {
        cout << prompt;
        getline(cin, value);
        value = trim(value);
        if (!value.empty()) return value;
        cout << "  This field cannot be empty. Please try again.\n";
    }
}

// Press Enter to continue
void pressEnter() {
    cout << "\nPress Enter to continue...";
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    // flush any leftover input
    if (cin.peek() != '\n' && !cin.eof()) {
        string dummy;
        getline(cin, dummy);
    }
}

// ─────────────────────────────────────────────
//  FILE HANDLING
// ─────────────────────────────────────────────

/*
 * FILE FORMAT (pipe-delimited, one student per line):
 * id|name|age|grade|health|registered|cname|cnumber|caddress|crelationship
 */

void saveToFile() {
    ofstream f(DATA_FILE);
    if (!f.is_open()) {
        cout << "  [Warning] Could not open file for saving.\n";
        return;
    }

    // First line: next ID
    f << nextId << "\n";

    for (const Student& s : students) {
        f << s.id                      << "|"
          << escape(s.name)            << "|"
          << escape(s.age)             << "|"
          << escape(s.grade)           << "|"
          << escape(s.health)          << "|"
          << escape(s.registered)      << "|"
          << escape(s.contact.name)    << "|"
          << escape(s.contact.number)  << "|"
          << escape(s.contact.address) << "|"
          << escape(s.contact.relationship) << "\n";
    }

    f.close();
}

void loadFromFile() {
    ifstream f(DATA_FILE);
    if (!f.is_open()) {
        // File doesn't exist yet — start fresh
        students.clear();
        nextId = 1;
        return;
    }

    string line;

    // First line is nextId
    if (getline(f, line)) {
        nextId = stoi(trim(line));
    }

    students.clear();

    while (getline(f, line)) {
        if (trim(line).empty()) continue;

        // Split by unescaped pipe
        vector<string> fields;
        string token;
        for (size_t i = 0; i < line.size(); ++i) {
            if (line[i] == '\\' && i + 1 < line.size() && line[i+1] == '|') {
                token += '|';
                ++i;
            } else if (line[i] == '|') {
                fields.push_back(unescape(token));
                token.clear();
            } else {
                token += line[i];
            }
        }
        fields.push_back(unescape(token));

        if (fields.size() < 10) continue;   // skip malformed lines

        Student s;
        s.id                      = stoi(fields[0]);
        s.name                    = fields[1];
        s.age                     = fields[2];
        s.grade                   = fields[3];
        s.health                  = fields[4];
        s.registered              = fields[5];
        s.contact.name            = fields[6];
        s.contact.number          = fields[7];
        s.contact.address         = fields[8];
        s.contact.relationship    = fields[9];

        students.push_back(s);
    }

    f.close();
}

// ─────────────────────────────────────────────
//  CORE FUNCTIONS
// ─────────────────────────────────────────────

// Build a new Student struct and append it to the list
void registerStudent() {
    printHeader("Student Registration");

    Student s;
    s.id         = nextId++;
    s.registered = currentTime();

    cout << "\n  Fill in the student details below.\n";
    printLine();

    s.name   = readLine("  Student Name     : ");
    s.age    = readLine("  Age              : ");
    s.grade  = readLine("  Grade / Section  : ");
    s.health = readLine("  Health Condition : ");

    cout << "\n  -- Emergency Contact --\n";

    s.contact.name         = readLine("  Contact Name     : ");
    s.contact.number       = readLine("  Contact Number   : ");
    s.contact.address      = readLine("  Address          : ");
    s.contact.relationship = readLine("  Relationship     : ");

    printLine();
    cout << "\n  Review your entry:\n";
    cout << "    Name    : " << s.name   << "\n";
    cout << "    Age     : " << s.age    << "\n";
    cout << "    Grade   : " << s.grade  << "\n";
    cout << "    Health  : " << s.health << "\n";
    cout << "    Contact : " << s.contact.name << " (" << s.contact.relationship << ")\n";
    cout << "    Number  : " << s.contact.number << "\n";
    printLine();

    if (askYesNo("\n  Save this record?")) {
        students.push_back(s);
        saveToFile();
        cout << "\n  Record saved! Student ID assigned: " << s.id << "\n";
    } else {
        --nextId;   // roll back the counter
        cout << "\n  Registration cancelled.\n";
    }

    pressEnter();
}

// Display all health records in a formatted table
void viewHealthRecords() {
    printHeader("Health Records");

    if (students.empty()) {
        cout << "\n  No records on file yet.\n";
        pressEnter();
        return;
    }

    // Column widths
    cout << "\n"
         << left
         << setw(6)  << "ID"
         << setw(22) << "Name"
         << setw(6)  << "Age"
         << setw(14) << "Grade"
         << setw(20) << "Health Condition"
         << "Registered\n";
    printLine('-', 75);

    for (const Student& s : students) {
        cout << left
             << setw(6)  << s.id
             << setw(22) << s.name.substr(0, 20)
             << setw(6)  << s.age
             << setw(14) << s.grade.substr(0, 12)
             << setw(20) << s.health.substr(0, 18)
             << s.registered << "\n";
    }

    printLine('-', 75);
    cout << "  Total: " << students.size() << " record(s)\n";
    pressEnter();
}

// Display all emergency contacts
void viewEmergencyContacts() {
    printHeader("Emergency Contacts");

    if (students.empty()) {
        cout << "\n  No records on file yet.\n";
        pressEnter();
        return;
    }

    cout << "\n"
         << left
         << setw(6)  << "ID"
         << setw(18) << "Student"
         << setw(18) << "Contact Name"
         << setw(14) << "Number"
         << setw(14) << "Relation"
         << "Address\n";
    printLine('-', 80);

    for (const Student& s : students) {
        cout << left
             << setw(6)  << s.id
             << setw(18) << s.name.substr(0, 16)
             << setw(18) << s.contact.name.substr(0, 16)
             << setw(14) << s.contact.number.substr(0, 12)
             << setw(14) << s.contact.relationship.substr(0, 12)
             << s.contact.address << "\n";
    }

    printLine('-', 80);
    cout << "  Total: " << students.size() << " record(s)\n";
    pressEnter();
}

// Search students by name (partial, case-insensitive)
void searchStudent() {
    printHeader("Search Student");

    cout << "\n  Enter the student name to search for.\n";
    string query = readLine("  Search: ");
    string lowerQuery = toLower(query);

    vector<Student*> results;
    for (Student& s : students) {
        if (toLower(s.name).find(lowerQuery) != string::npos) {
            results.push_back(&s);
        }
    }

    if (results.empty()) {
        cout << "\n  No students matched '" << query << "'.\n";
        pressEnter();
        return;
    }

    cout << "\n  Found " << results.size() << " result(s):\n";
    printLine();

    for (Student* s : results) {
        cout << "\n  ID       : " << s->id
             << "\n  Name     : " << s->name
             << "\n  Age      : " << s->age
             << "\n  Grade    : " << s->grade
             << "\n  Health   : " << s->health
             << "\n  Contact  : " << s->contact.name
                                  << " (" << s->contact.relationship << ")"
             << "\n  Number   : " << s->contact.number
             << "\n  Address  : " << s->contact.address
             << "\n  Saved on : " << s->registered << "\n";
        printLine();
    }

    // Ask if user wants to search again
    if (askYesNo("\n  Search for another student?")) {
        searchStudent();
    }
}

// Delete a student record by ID
void deleteRecord() {
    printHeader("Delete a Record");

    if (students.empty()) {
        cout << "\n  No records on file to delete.\n";
        pressEnter();
        return;
    }

    cout << "\n  Enter the Student ID you want to delete.\n";
    string input = readLine("  Student ID: ");

    // Validate numeric input
    bool isNum = !input.empty();
    for (char c : input) {
        if (!isdigit(c)) { isNum = false; break; }
    }

    if (!isNum) {
        cout << "\n  Invalid input. Please enter a numeric ID.\n";
        pressEnter();
        return;
    }

    int targetId = stoi(input);

    // Find the student
    Student* found = nullptr;
    for (Student& s : students) {
        if (s.id == targetId) {
            found = &s;
            break;
        }
    }

    if (!found) {
        cout << "\n  No student found with ID " << targetId << ".\n";

        if (askYesNo("\n  Try a different ID?")) {
            deleteRecord();
        }
        return;
    }

    // Preview
    cout << "\n  Found:\n";
    cout << "    ID    : " << found->id    << "\n";
    cout << "    Name  : " << found->name  << "\n";
    cout << "    Grade : " << found->grade << "\n";
    printLine();

    if (!askYesNo("\n  Are you sure you want to delete this record? This cannot be undone.")) {
        cout << "\n  Deletion cancelled.\n";
        pressEnter();
        return;
    }

    // Perform deletion
    students.erase(
        remove_if(students.begin(), students.end(),
                  [targetId](const Student& s){ return s.id == targetId; }),
        students.end()
    );

    saveToFile();
    cout << "\n  Record deleted successfully.\n";

    if (askYesNo("\n  Delete another record?")) {
        deleteRecord();
    }
}

// ─────────────────────────────────────────────
//  STAFF PANEL
// ─────────────────────────────────────────────

void staffPanel() {
    printHeader("Staff Panel");

    cout << "\n  Records currently on file: " << students.size() << "\n\n";

    // Yes/no driven menu
    if (askYesNo("  View health records?")) {
        viewHealthRecords();
    }

    if (askYesNo("  View emergency contacts?")) {
        viewEmergencyContacts();
    }

    if (askYesNo("  Search for a student?")) {
        searchStudent();
        pressEnter();
    }

    if (askYesNo("  Delete a record?")) {
        deleteRecord();
    }

    cout << "\n  Returning to the main menu...\n";
}

// Staff login with password
void staffLogin() {
    printHeader("Staff Login");

    cout << "\n";
    int attempts = 3;

    while (attempts > 0) {
        cout << "  Password: ";
        string pw;
        getline(cin, pw);
        pw = trim(pw);

        if (pw == STAFF_PASS) {
            cout << "\n  Access granted. Welcome, Staff!\n";
            pressEnter();
            staffPanel();
            return;
        }

        --attempts;
        if (attempts > 0) {
            cout << "  Incorrect password. " << attempts << " attempt(s) remaining.\n\n";

            if (!askYesNo("  Try again?")) {
                cout << "\n  Login cancelled.\n";
                pressEnter();
                return;
            }
        }
    }

    cout << "\n  Too many failed attempts. Access denied.\n";
    pressEnter();
}

// ─────────────────────────────────────────────
//  MAIN MENU
// ─────────────────────────────────────────────

void mainMenu() {
    while (true) {
        printHeader("Main Menu");

        cout << "\n"
             << "  Welcome to InSync\n"
             << "  Student Health & Emergency Record System\n\n"
             << "  Records on file: " << students.size() << "\n";
        printLine();

        // Yes/no driven navigation
        if (askYesNo("\n  Are you a student registering your information?")) {
            registerStudent();
            continue;
        }

        if (askYesNo("\n  Are you a staff member accessing records?")) {
            staffLogin();
            continue;
        }

        if (askYesNo("\n  Would you like to exit the system?")) {
            cout << "\n  Thank you for using InSync. Goodbye!\n\n";
            break;
        }

        cout << "\n  Please choose an option above.\n";
    }
}

// ─────────────────────────────────────────────
//  ENTRY POINT
// ─────────────────────────────────────────────

int main() {
    loadFromFile();   // FILE HANDLING: read existing records on startup
    mainMenu();
    return 0;
}