from abc import ABC, abstractmethod


class Person(ABC):

    def __init__(self, name, id_code):
        self._name = name
        self._id_code = id_code

    @property
    def name(self):
        return self._name

    @property
    def id_code(self):
        return self._id_code

    @abstractmethod
    def get_role(self):
        pass

    def __str__(self):
        return f"{self.get_role()}: {self.name} (ID: {self.id_code})"


class Member(Person):

    def __init__(self, name, id_code):
        super().__init__(name, id_code)

    def get_role(self):
        return "Member"


class Librarian(Person):

    def __init__(self, name, id_code, employee_id):
        super().__init__(name, id_code)
        self.employee_id = employee_id

    def get_role(self):
        return "Librarian"

    def __str__(self):
        return f"{super().__str__()} [EmpID: {self.employee_id}]"


class Book:

    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self._title = title
        self.author = author
        self._is_available = True

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value

    @property
    def is_available(self):
        return self._is_available

    @is_available.setter
    def is_available(self, status):
        self._is_available = status

    def __str__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - [{status}]"


class Loan:

    def __init__(self, member, book):
        self.member = member
        self.book = book

    def __str__(self):
        return f"Loan: {self.member.name} borrowed {self.book.title}"


class Library:

    def __init__(self, name):
        self.name = name
        self.books = {}
        self.members = {}
        self.loans = []

    def add_book(self, book):
        self.books[book.isbn] = book

    def register_member(self, member):
        self.members[member.id_code] = member

    def issue_loan(self, member_id, isbn):
        if member_id in self.members and isbn in self.books:
            book = self.books[isbn]
            if book.is_available:
                book.is_available = False
                loan = Loan(self.members[member_id], book)
                self.loans.append(loan)
                return True
        return False

    def display_info(self):
        print(f"=== Library: {self.name} ===")
        for book in self.books.values():
            print(book)


library = Library("Central Library")
lib_member = Member("Alice", "M001")
librarian = Librarian("Bob", "L001", "EMP99")

book1 = Book("1111", "Python Basics", "John Doe")
book2 = Book("2222", "Advanced OOP", "Jane Smith")

library.register_member(lib_member)
library.add_book(book1)
library.add_book(book2)

people = [lib_member, librarian]
for person in people:
    print(person)

print("\n--- Before Loan ---")
library.display_info()

library.issue_loan("M001", "1111")

print("\n--- After Loan ---")
library.display_info()
