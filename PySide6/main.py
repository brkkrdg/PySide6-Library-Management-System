import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTextEdit, QDialog


class Library:
    def __init__(self):
        self.file = open("books.txt", "a+")
        self.file.seek(0)

    def __del__(self):
        self.file.close()

    def list_books(self):
        self.file.seek(0)
        books = self.file.readlines()
        if not books:
            return "No books available."
        else:
            return "\n".join(books)

    def add_book(self, title, author, release_year, num_pages):
        book_info = f"{title},{author},{release_year},{num_pages}\n"
        self.file.write(book_info)
        return "Book added successfully."

    def remove_book(self, title):
        self.file.seek(0)
        books = self.file.readlines()
        books = [book for book in books if not book.startswith(title)]
        self.file.truncate(0)
        self.file.writelines(books)
        return "Book removed successfully."


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)  # Add spacing between widgets
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Welcome to Library Management System")
        self.layout.addWidget(self.label)

        self.list_button = QPushButton("List Books")
        self.list_button.setStyleSheet("QPushButton { background-color: #2ecc71; color: white; border-radius: 5px; }"
                                       "QPushButton:hover { background-color: #27ae60; }")
        self.list_button.clicked.connect(self.list_books)
        self.layout.addWidget(self.list_button)

        self.add_button = QPushButton("Add Book")
        self.add_button.setStyleSheet("QPushButton { background-color: #3498db; color: white; border-radius: 5px; }"
                                      "QPushButton:hover { background-color: #2980b9; }")
        self.add_button.clicked.connect(self.add_book_dialog)
        self.layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Book")
        self.remove_button.setStyleSheet("QPushButton { background-color: #e74c3c; color: white; border-radius: 5px; }"
                                         "QPushButton:hover { background-color: #c0392b; }")
        self.remove_button.clicked.connect(self.remove_book_dialog)
        self.layout.addWidget(self.remove_button)

        self.quit_button = QPushButton("Quit")
        self.quit_button.setStyleSheet("QPushButton { background-color: #f39c12; color: white; border-radius: 5px; }"
                                       "QPushButton:hover { background-color: #d35400; }")
        self.quit_button.clicked.connect(self.close_application)
        self.layout.addWidget(self.quit_button)

        self.output_text = QTextEdit()
        self.layout.addWidget(self.output_text)

        self.library = Library()

    def list_books(self):
        books_info = self.library.list_books()
        self.output_text.setPlainText(books_info)

    def add_book_dialog(self):
        dialog = AddBookDialog(self)
        dialog.exec()

    def remove_book_dialog(self):
        dialog = RemoveBookDialog(self)
        dialog.exec()

    def close_application(self):
        QApplication.instance().quit()


class AddBookDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Add Book")
        self.setGeometry(200, 200, 300, 200)

        self.layout = QVBoxLayout(self)

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Enter book title")
        self.layout.addWidget(self.title_edit)

        self.author_edit = QLineEdit()
        self.author_edit.setPlaceholderText("Enter author")
        self.layout.addWidget(self.author_edit)

        self.release_year_edit = QLineEdit()
        self.release_year_edit.setPlaceholderText("Enter release year")
        self.layout.addWidget(self.release_year_edit)

        self.pages_edit = QLineEdit()
        self.pages_edit.setPlaceholderText("Enter number of pages")
        self.layout.addWidget(self.pages_edit)

        self.add_button = QPushButton("Add")
        self.add_button.setStyleSheet("QPushButton { background-color: #3498db; color: white; border-radius: 5px; }"
                                      "QPushButton:hover { background-color: #2980b9; }")
        self.add_button.clicked.connect(self.add_book)
        self.layout.addWidget(self.add_button)

        self.library = parent.library

    def add_book(self):
        title = self.title_edit.text()
        author = self.author_edit.text()
        release_year = self.release_year_edit.text()
        pages = self.pages_edit.text()

        message = self.library.add_book(title, author, release_year, pages)
        self.parent().output_text.setPlainText(message)
        self.close()


class RemoveBookDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Remove Book")
        self.setGeometry(200, 200, 300, 100)

        self.layout = QVBoxLayout(self)

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Enter book title")
        self.layout.addWidget(self.title_edit)

        self.remove_button = QPushButton("Remove")
        self.remove_button.setStyleSheet("QPushButton { background-color: #e74c3c; color: white; border-radius: 5px; }"
                                         "QPushButton:hover { background-color: #c0392b; }")
        self.remove_button.clicked.connect(self.remove_book)
        self.layout.addWidget(self.remove_button)

        self.library = parent.library

    def remove_book(self):
        title = self.title_edit.text()
        message = self.library.remove_book(title)
        self.parent().output_text.setPlainText(message)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
