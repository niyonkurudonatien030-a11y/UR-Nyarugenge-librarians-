# books_data.py
"""Data module: book records of the UR-CST Library Portal.
Holds the available, borrowed, lost and donated books and the e-books.
All details below are imaginary sample data used for demonstration.
"""
from datetime import date, timedelta

AFFILIATIONS = ["Math", "Physics", "Engineering", "Chemistry", "Geography",
 "Fiction", "Architecture", "Arts", "Other"]

def make_book(code, title, author, publisher, year, edition, isbn,
 affiliation, cost, keywords=""):
 """Return one book record (a dictionary)."""
 return {
 "code": code, "title": title, "author": author,
 "publisher": publisher, "year": year, "edition": edition,
 "isbn": isbn, "affiliation": affiliation, "cost": cost,
 "keywords": keywords, "hidden": False,
 }

available_books = [
 make_book("MTH-101", "Engineering Mathematics Basics", "Alice Uwase",
 "Kigali Academic Press", 2015, 3, "978-9-0001-0101-1",
 "Math", 18000, "algebra calculus"),
 make_book("MTH-102", "Calculus for Beginners", "Jean Bosco Habimana",
 "Huye University Press", 2019, 2, "978-9-0001-0102-8",
 "Math", 16000, "calculus limits"),
 make_book("PHY-101", "Physics for Engineers", "Grace Mukamana",
 "Kigali Academic Press", 2012, 5, "978-9-0001-0201-4",
 "Physics", 22000, "mechanics"),
 make_book("PHY-102", "Waves and Optics Explained", "Patrick Nkurunziza",
 "Lakeside Publishers", 2020, 1, "978-9-0001-0202-1",
 "Physics", 20000, "waves light"),
 make_book("ENG-101", "Introduction to IoT Systems", "Eric Niyonzima",
 "Tech Rwanda Books", 2022, 1, "978-9-0001-0301-7",
 "Engineering", 30000, "iot sensors internet of things"),
 make_book("ENG-102", "Thermodynamics Made Simple", "Sandrine Ingabire",
 "Lakeside Publishers", 2017, 4, "978-9-0001-0302-4",
 "Engineering", 25000, "thermo heat energy"),
 make_book("ENG-103", "Basic Electrical Circuits", "Olivier Mugabo",
 "Tech Rwanda Books", 2010, 6, "978-9-0001-0303-1",
 "Engineering", 21000, "circuits electricity"),
 make_book("CHM-101", "General Chemistry Notes", "Diane Uwimana",
 "Huye University Press", 2016, 2, "978-9-0001-0401-0",
 "Chemistry", 17000, "atoms reactions"),
 make_book("GEO-101", "Geography of the Great Lakes Region",
 "Claude Ndayisaba", "Lakeside Publishers", 2018, 1,
 "978-9-0001-0501-7", "Geography", 19000, "maps lakes"),
 make_book("FIC-101", "The Last Bus to Kigali", "Aline Kamanzi",
 "Imvano Stories", 2021, 1, "978-9-0001-0601-4",
 "Fiction", 9000, "novel story"),
 make_book("ARC-101", "Principles of Building Design", "Samuel Rutayisire",
 "Kigali Academic Press", 2014, 2, "978-9-0001-0701-1",
 "Architecture", 28000, "design buildings"),
 make_book("ART-101", "History of African Art", "Chantal Uwera",
 "Imvano Stories", 2013, 1, "978-9-0001-0801-8",
 "Arts", 15000, "painting culture"),
]

# Each loan: book, reg_no, borrow_date, due_date, renewals and message flags
borrowed_books = [
 {"book": make_book("ENG-104", "Python Programming for Engineers",
 "Mark Kalisa", "Tech Rwanda Books", 2023, 1,
 "978-9-0001-0304-8", "Engineering", 26000,
 "python coding"),
 "reg_no": "222001001", "borrow_date": date.today() - timedelta(days=12),
 "due_date": date.today() + timedelta(days=2), "renewals": 0,
 "reminded": False, "overdue_notified": False},
 {"book": make_book("MTH-103", "Linear Algebra Essentials",
 "Josiane Mukarugwiro", "Huye University Press", 2018,
 2, "978-9-0001-0103-5", "Math", 17000, "matrices"),
 "reg_no": "222001002", "borrow_date": date.today() - timedelta(days=17),
 "due_date": date.today() - timedelta(days=3), "renewals": 0,
 "reminded": True, "overdue_notified": False},
]

lost_books = [] # each: book, reg_no, date_reported
donated_books = [] # donated books waiting for the librarian's approval

e_books = [
 {"title": "Introduction to Python (free e-book)", "author": "UR-CST Staff",
 "text": "Python is a high-level, interpreted programming language."},
 {"title": "Basics of Electronics (free e-book)", "author": "UR-CST Staff",
 "text": "Electronics studies the control of electric current."},
 {"title": "Study Skills for University (free e-book)",
 "author": "UR-CST Staff",
 "text": "Plan your week and revise a little every day."},
]
