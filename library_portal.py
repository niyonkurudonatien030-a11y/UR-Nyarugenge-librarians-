# library_portal.py
"""UR-CST Library Portal - main program.
Users: 1. Student 2. Librarian 3. Guest
Imports the data modules books_data, students_data and librarians_data.
Rules: loan = 14 days, reminder 2 days before the due date,
fine = RWF 500 for each late day, lost book cost goes to student debts.
"""
from datetime import date, timedelta
import books_data as bd
import students_data as sd
import librarians_data as ld

LOAN_DAYS = 14 # two weeks
REMINDER_DAYS = 2 # send a message two days before the due date
FINE_PER_DAY = 500 # RWF for each late day
MAX_BOOKS = 3 # books one student may hold at the same time

# ---------------------------------------------------------------- display
def line(char="=", width=70):
 """Print a separator line."""
 print(char * width)

def title(text):
 """Print a centred title between two lines."""
 line()
 print(text.center(70))
 line()

def date_text(the_date):
 """Return a date as text, e.g. 05-Dec-2026."""
 return the_date.strftime("%d-%b-%Y")

def ask_number(prompt, low, high):
 """Keep asking until the user types a whole number from low to high."""
 while True:
  text = input(prompt).strip()
  if text.isdigit() and low <= int(text) <= high:
   return int(text)
  print("Invalid choice. Enter a number from", low, "to", high)

def show_book(book):
 """Print all details of one book."""
 print(" Code :", book["code"])
 print(" Title :", book["title"])
 print(" Author :", book["author"])
 print(" Publisher :", book["publisher"])
 print(" Pub. year :", book["year"])
 print(" Edition No :", book["edition"])
 print(" ISBN :", book["isbn"])
 print(" Affiliation :", book["affiliation"])

def show_book_table(books):
 """Print a list of books as a table."""
 if len(books) == 0:
  print("No books to show.")
  return
 line("-")
 print(f"{'No':<4}{'Code':<9}{'Title':<34}{'Author':<20}{'Year':<6}")
 line("-")
 for number, book in enumerate(books, 1):
  print(f"{number:<4}{book['code']:<9}{book['title'][:32]:<34}"
        f"{book['author'][:18]:<20}{book['year']:<6}")
 line("-")

# ---------------------------------------------------------- data helpers
def visible_books():
 """Return the available books that are not hidden from students."""
 shown = []
 for book in bd.available_books:
  if not book["hidden"]:
   shown.append(book)
 return shown

def find_book(code, books):
 """Return the book with this code in the list, or None."""
 for book in books:
  if book["code"].lower() == code.lower().strip():
   return book
 return None

def search_books(keyword):
 """Search visible books by title, author, year, area or keyword."""
 keyword = keyword.lower().strip()
 found = []
 for book in visible_books():
  text = (book["title"] + " " + book["author"] + " " +
          str(book["year"]) + " " + book["affiliation"] + " " +
          book["code"] + " " + book["keywords"]).lower()
  if keyword in text:
   found.append(book)
 return found

def sort_books(books, field, descending=False):
 """Return a sorted copy of the books (bubble sort on one field)."""
 result = books[:]
 for i in range(len(result)):
  for j in range(len(result) - 1 - i):
   first = result[j][field]
   second = result[j + 1][field]
   if isinstance(first, str):
    first, second = first.lower(), second.lower()
   if (first > second and not descending) or \
      (first < second and descending):
    result[j], result[j + 1] = result[j + 1], result[j]
 return result

def student_loans(reg_no):
 """Return the loans (borrowed books) of one student."""
 loans = []
 for loan in bd.borrowed_books:
  if loan["reg_no"] == reg_no:
   loans.append(loan)
 return loans

def days_late(due_date):
 """Return the number of late days (0 if the book is not late)."""
 late = (date.today() - due_date).days
 return late if late > 0 else 0

def fine_for(loan):
 """Fine of a loan: RWF 500 added for each late day."""
 return days_late(loan["due_date"]) * FINE_PER_DAY

def add_debt(reg_no, amount):
 """Add an amount (RWF) to the student's debts in the school system."""
 sd.debts[reg_no] = sd.debts.get(reg_no, 0) + amount

def new_loan(book, reg_no):
 """Move a book from available to borrowed and return the loan."""
 today = date.today()
 loan = {"book": book, "reg_no": reg_no, "borrow_date": today,
 "due_date": today + timedelta(days=LOAN_DAYS), "renewals": 0,
 "reminded": False, "overdue_notified": False}
 bd.available_books.remove(book)
 bd.borrowed_books.append(loan)
 return loan

def close_loan(loan):
 """Take a returned book: add any fine, move book back to available."""
 fine = fine_for(loan)
 if fine > 0:
  add_debt(loan["reg_no"], fine)
 bd.borrowed_books.remove(loan)
 bd.available_books.append(loan["book"])
 return fine

def show_loans(loans):
 """Print loans with due dates, days left and fines."""
 if len(loans) == 0:
  print("No borrowed books.")
  return
 line("-")
 print(f"{'No':<4}{'Title':<30}{'Borrowed':<13}{'Due date':<13}"
       f"{'Status'}")
 line("-")
 for number, loan in enumerate(loans, 1):
  left = (loan["due_date"] - date.today()).days
  if left >= 0:
   status = str(left) + " day(s) left"
  else:
   status = "LATE " + str(-left) + " day(s), fine RWF " + \
            str(fine_for(loan))
  print(f"{number:<4}{loan['book']['title'][:28]:<30}"
        f"{date_text(loan['borrow_date']):<13}"
        f"{date_text(loan['due_date']):<13}{status}")
 line("-")

# ---------------------------------------------------- automatic messages
def send_message(reg_no, text):
 """Send (simulate) an SMS to the student and keep it in the log."""
 student = sd.students[reg_no]
 sd.messages.append({"reg_no": reg_no, "phone": student["phone"],
 "date": date.today(), "text": text})

def send_reminders():
 """Automatic job: remind students two days before the due date and
 warn students whose books are late. Returns the number sent."""
 sent = 0
 for loan in bd.borrowed_books:
  left = (loan["due_date"] - date.today()).days
  reg_no = loan["reg_no"]
  name = sd.students[reg_no]["name"]
  book_title = loan["book"]["title"]
  if 0 <= left <= REMINDER_DAYS and not loan["reminded"]:
   send_message(reg_no, "Dear " + name + ", '" + book_title +
            "' is due on " + date_text(loan["due_date"]) +
            ". Return it or renew it to avoid a fine of RWF " +
            str(FINE_PER_DAY) + " per day.")
   loan["reminded"] = True
   sent += 1
  elif left < 0 and not loan["overdue_notified"]:
   send_message(reg_no, "Dear " + name + ", '" + book_title +
            "' is LATE. Current fine: RWF " +
            str(fine_for(loan)) + ". Please return it now.")
   loan["overdue_notified"] = True
   sent += 1
 return sent

def show_messages(reg_no):
 """Show the messages and the debts of one student."""
 count = 0
 for message in sd.messages:
  if message["reg_no"] == reg_no:
   print(" -", date_text(message["date"]), "|", message["text"])
   count += 1
 print("Messages received:", count)
 print("Debts in school system: RWF", sd.debts.get(reg_no, 0))

# ------------------------------------------------------ shared book forms
def ask_book_details():
 """Ask for the details of a book and return the book record."""
 print("Enter the book details:")
 book_title = input(" Title: ").strip()
 author = input(" Author: ").strip()
 publisher = input(" Publisher: ").strip()
 year = ask_number(" Publication year: ", 1500, 2100)
 edition = ask_number(" Edition No: ", 1, 100)
 isbn = input(" ISBN: ").strip()
 print(" Affiliation:")
 for number, name in enumerate(bd.AFFILIATIONS, 1):
  print(" ", number, name)
 pick = ask_number(" Choose affiliation: ", 1, len(bd.AFFILIATIONS))
 cost = ask_number(" Cost (RWF): ", 0, 10000000)
 book = bd.make_book("", book_title, author, publisher, year, edition,
                     isbn, bd.AFFILIATIONS[pick - 1], cost, "")
 return book

def donate_book():
 """Donate a book: it waits for the librarian's approval."""
 book = ask_book_details()
 bd.donated_books.append(book)
 print("Thank you! Your donation will be checked by a librarian.")

def sort_menu(books):
 """Show books using the sorting option chosen by the user."""
 print("Sort by: 1 Affiliation 2 A-Z 3 Z-A 4 Oldest first "
       "5 Newest first 6 Code 7 Author")
 choice = ask_number("Choose sorting: ", 1, 7)
 if choice == 1:
  show_book_table(sort_books(books, "affiliation"))
 elif choice == 2:
  show_book_table(sort_books(books, "title"))
 elif choice == 3:
  show_book_table(sort_books(books, "title", True))
 elif choice == 4:
  show_book_table(sort_books(books, "year"))
 elif choice == 5:
  show_book_table(sort_books(books, "year", True))
 elif choice == 6:
  show_book_table(sort_books(books, "code"))
 else:
  show_book_table(sort_books(books, "author"))

# ---------------------------------------------------------------- student
def student_borrow(reg_no):
 """Student borrows an available book."""
 if len(student_loans(reg_no)) >= MAX_BOOKS:
  print("You already hold", MAX_BOOKS, "books. Return one first.")
  return
 code = input("Enter the code of the book to borrow: ")
 book = find_book(code, visible_books())
 if book is None:
  print("This book is not available.")
  return
 loan = new_loan(book, reg_no)
 print("Borrowed:", book["title"])
 print("Return it before", date_text(loan["due_date"]),
       "(" + str(LOAN_DAYS), "days).")

def student_return(reg_no):
 """Student returns a borrowed book."""
 loans = student_loans(reg_no)
 show_loans(loans)
 if len(loans) == 0:
  return
 pick = ask_number("Number of the book to return (0 = cancel): ",
                   0, len(loans))
 if pick == 0:
  return
 fine = close_loan(loans[pick - 1])
 print("Book returned. Thank you!")
 if fine > 0:
  print("Late fine added to your debts: RWF", fine)

def student_renew(reg_no):
 """Renew = return the book and borrow it again for 14 days."""
 loans = student_loans(reg_no)
 show_loans(loans)
 if len(loans) == 0:
  return
 pick = ask_number("Number of the book to renew (0 = cancel): ",
                   0, len(loans))
 if pick == 0:
  return
  