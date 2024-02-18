import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTextEdit, QDialog, QSizePolicy, QTableWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt, QPropertyAnimation, QRect
from PySide6.QtGui import QColor, QFont, QIcon


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
            return [("No books available.", "", "", "")]
        else:
            book_list = []
            for book in books:
                book_info = book.strip().split(",")
                if len(book_info) == 4:
                    title, author, release_year, num_pages = book_info
                    book_list.append((title, author, release_year, num_pages))
            if not book_list:
                return [("No books available.", "", "", "")]
            else:
                return book_list

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
        self.setGeometry(100, 100, 600, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.buttons_layout = QVBoxLayout()
        self.layout.addLayout(self.buttons_layout)

        self.list_button = QPushButton(QIcon("icons/list_icon.ico"), " List Books")
        self.apply_button_animation(self.list_button)
        self.list_button.setStyleSheet("QPushButton { background-color: #313233; color: white; border-radius: 15px; }"
                                       "QPushButton:hover { background-color: #2980b9; }")
        self.list_button.setFont(QFont("Arial", 12))
        self.list_button.setMinimumHeight(40)
        self.list_button.setMinimumWidth(120)
        self.list_button.clicked.connect(self.list_books)
        self.buttons_layout.addWidget(self.list_button)

        self.add_button = QPushButton(QIcon("icons/add_book_icon.ico"), " Add Book")
        self.apply_button_animation(self.add_button)
        self.add_button.setStyleSheet("QPushButton { background-color: #313233; color: white; border-radius: 15px; }"
                                      "QPushButton:hover { background-color: #27ae60; }")
        self.add_button.setFont(QFont("Arial", 12))
        self.add_button.setMinimumHeight(40)
        self.add_button.setMinimumWidth(120)
        self.add_button.clicked.connect(self.add_book_dialog)
        self.buttons_layout.addWidget(self.add_button)

        self.remove_button = QPushButton(QIcon("icons/book_remove_icon.ico"), " Remove Book")
        self.apply_button_animation(self.remove_button)
        self.remove_button.setStyleSheet("QPushButton { background-color: #313233; color: white; border-radius: 15px; }"
                                         "QPushButton:hover { background-color: #c0392b; }")
        self.remove_button.setFont(QFont("Arial", 12))
        self.remove_button.setMinimumHeight(40)
        self.remove_button.setMinimumWidth(120)
        self.remove_button.clicked.connect(self.remove_book_dialog)
        self.buttons_layout.addWidget(self.remove_button)

        self.quit_button = QPushButton(QIcon("icons/exit_icon.ico"), " Quit")
        self.apply_button_animation(self.quit_button)
        self.quit_button.setStyleSheet("QPushButton { background-color: #ed6a5e; color: white; border-radius: 15px; }"
                                       "QPushButton:hover { background-color: #f39c12; }")
        self.quit_button.setFont(QFont("Arial", 12))
        self.quit_button.setMinimumHeight(40)
        self.quit_button.setMinimumWidth(120)
        self.quit_button.clicked.connect(self.close_application)
        self.buttons_layout.addWidget(self.quit_button)

        self.table_layout = QVBoxLayout()
        self.layout.addLayout(self.table_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Author", "Release Year", "Number of Pages"])
        self.table_layout.addWidget(self.table)

        self.library = Library()

    def list_books(self):
        books_info = self.library.list_books()
        self.table.setRowCount(len(books_info))
        for row, book in enumerate(books_info):
            for col, data in enumerate(book):
                item = QTableWidgetItem(data)
                self.table.setItem(row, col, item)

    def add_book_dialog(self):
        dialog = AddBookDialog(self)
        if dialog.exec():
            QMessageBox.information(self, "Success", "Book added successfully.")
            self.list_books()

    def remove_book_dialog(self):
        dialog = RemoveBookDialog(self)
        if dialog.exec():
            QMessageBox.information(self, "Success", "Book removed successfully.")
            self.list_books()

    def close_application(self):
        QApplication.instance().quit()

    def apply_button_animation(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(200)
        start_rect = QRect(button.x(), button.y(), button.width(), button.height())
        hover_rect = QRect(button.x(), button.y(), button.width() * 1.1, button.height() * 1.1)
        animation.setStartValue(start_rect)
        animation.setEndValue(hover_rect)
        button.mouseEnterEvent = lambda event: animation.start()
        leave_animation = QPropertyAnimation(button, b"geometry")
        leave_animation.setDuration(200)
        leave_animation.setStartValue(hover_rect)
        leave_animation.setEndValue(start_rect)
        button.mouseLeaveEvent = lambda event: leave_animation.start()


class AddBookDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Add Book")
        self.setWindowIcon(QIcon("icons/add_book_icon.ico"))  # İkon ekleniyor
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

        self.add_button = QPushButton(QIcon("icons/add_book_icon.ico"), "Add")
        self.add_button.setStyleSheet("QPushButton { background-color: #313233; color: white; border-radius: 15px; }"
                                      "QPushButton:hover { background-color: #27ae60; }")
        self.add_button.setFont(QFont("Arial", 12))
        self.add_button.setMinimumHeight(40)
        self.add_button.setMinimumWidth(120)
        self.add_button.clicked.connect(self.add_book)
        self.layout.addWidget(self.add_button)

        self.library = parent.library

    def add_book(self):
        title = self.title_edit.text()
        author = self.author_edit.text()
        release_year = self.release_year_edit.text()
        pages = self.pages_edit.text()

        message = self.library.add_book(title, author, release_year, pages)
        if message.startswith("Book added"):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)


class RemoveBookDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Remove Book")
        self.setWindowIcon(QIcon("icons/book_remove_icon.ico"))
        self.setGeometry(200, 200, 300, 100)

        self.layout = QVBoxLayout(self)

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Enter book title")
        self.layout.addWidget(self.title_edit)

        self.remove_button = QPushButton(QIcon("icons/book_remove_icon.ico"), "Remove")
        self.remove_button.setStyleSheet("QPushButton { background-color: #313233; color: white; border-radius: 15px; }"
                                         "QPushButton:hover { background-color: #c0392b; }")
        self.remove_button.setFont(QFont("Arial", 12))
        self.remove_button.setMinimumHeight(40)
        self.remove_button.setMinimumWidth(120)
        self.remove_button.clicked.connect(self.remove_book)
        self.layout.addWidget(self.remove_button)

        self.library = parent.library

    def remove_book(self):
        title = self.title_edit.text()
        message = self.library.remove_book(title)
        if message.startswith("Book removed"):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
