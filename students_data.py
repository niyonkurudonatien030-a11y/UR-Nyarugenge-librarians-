# students_data.py
"""Data module: registered students, their debts and the message log."""

def make_student(reg_no, name, email, phone, age, grade, department):
 """Return one student record (a dictionary)."""
 return {"reg_no": reg_no, "name": name, "email": email, "phone": phone,
 "age": age, "grade": grade, "department": department}

# Key = registration number, value = student details (imaginary samples)
students = {
 "222001001": make_student("222001001", "Divine Uwamahoro",
 "divine@example.com", "0788100001", 21,
 "Year 2", "ETE"),
 "222001002": make_student("222001002", "Eric Habineza",
 "eric@example.com", "0788100002", 22,
 "Year 2", "ETE"),
 "222001003": make_student("222001003", "Aline Mutesi",
 "aline@example.com", "0788100003", 20,
 "Year 1", "EEE"),
}

debts = {} # reg_no -> amount in RWF owed to the school system
messages = [] # every automatic message sent: reg_no, phone, date, text
