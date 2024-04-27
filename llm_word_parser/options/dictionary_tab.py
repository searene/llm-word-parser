from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidgetItem, QInputDialog
from aqt.qt import QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox

from llm_word_parser.db import db_path
from llm_word_parser.dictionary.repository import DictionaryRepository


class DictionaryTab(QWidget):
    def __init__(self, parent=None, repository: DictionaryRepository = None):
        super(DictionaryTab, self).__init__(parent)
        self.repository = repository or DictionaryRepository(db_path)

        self.layout = QVBoxLayout(self)
        self.dictionary_list = QListWidget()
        self.dictionary_list.itemClicked.connect(self.toggle_active_state)
        self.layout.addWidget(self.dictionary_list)

        self.add_path_button = QPushButton("Add Scan Path")
        self.add_path_button.clicked.connect(self.add_scan_path)
        self.layout.addWidget(self.add_path_button)

        self.rescan_button = QPushButton("Rescan Dictionaries")
        self.rescan_button.clicked.connect(self.rescan_dictionaries)
        self.layout.addWidget(self.rescan_button)

        self.refresh_list_button = QPushButton("Refresh List")
        self.refresh_list_button.clicked.connect(self.refresh_dictionary_list)
        self.layout.addWidget(self.refresh_list_button)

        self.refresh_dictionary_list()

    def add_scan_path(self):
        path, _ = QInputDialog.getText(self, "Add Scan Path", "Enter the directory path to scan for dictionaries:")
        if path:
            self.repository.add_scan_path(path)
            QMessageBox.information(self, "Success", "Scan path added successfully.")
            self.refresh_dictionary_list()

    def rescan_dictionaries(self):
        self.repository.scan()
        QMessageBox.information(self, "Rescan Complete", "Dictionaries have been rescanned.")
        self.refresh_dictionary_list()

    def refresh_dictionary_list(self):
        self.dictionary_list.clear()
        dictionaries = self.repository.all_dictionaries()
        for dictionary in dictionaries:
            item = QListWidgetItem(f"{dictionary.name} - {'Active' if dictionary.active else 'Inactive'}")
            item.setCheckState(Qt.CheckState.Checked if dictionary.active else Qt.CheckState.Unchecked)
            self.dictionary_list.addItem(item)

    def toggle_active_state(self, item: QListWidgetItem):
        # This toggles the state when an item is clicked.
        name = item.text().split(" - ")[0]
        new_state = not item.checkState()
        self.repository.set_active_state(name, new_state)
        item.setCheckState(Qt.CheckState.Checked if new_state else Qt.CheckState.Unchecked)
