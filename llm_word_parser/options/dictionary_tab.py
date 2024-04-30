from aqt.qt import *

from llm_word_parser.dictionary.repository import dictionary_repository


class DictionaryTab(QWidget):

    def __init__(self, parent: QWidget):
        super(DictionaryTab, self).__init__(parent)
        self.repository = dictionary_repository

        layout = QVBoxLayout(self)
        self.dictionary_list = QListWidget(self)
        layout.addWidget(self.dictionary_list)

        self.add_path_button = QPushButton("Add Scan Path")
        self.add_path_button.clicked.connect(self.add_scan_path)
        layout.addWidget(self.add_path_button)

        self.rescan_button = QPushButton("Rescan Dictionaries")
        self.rescan_button.clicked.connect(self.rescan_dictionaries)
        layout.addWidget(self.rescan_button)

        self.refresh_list_button = QPushButton("Refresh List")
        self.refresh_list_button.clicked.connect(self.refresh_dictionary_list)
        layout.addWidget(self.refresh_list_button)

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

    def refresh_dictionary_list(self) -> None:
        self.dictionary_list.clear()
        dictionaries = self.repository.all_dictionaries()
        for dictionary in dictionaries:
            item = QListWidgetItem(f"{dictionary.name} - {'Active' if dictionary.active else 'Inactive'}")
            item.setCheckState(Qt.CheckState.Checked if dictionary.active else Qt.CheckState.Unchecked)
            self.dictionary_list.addItem(item)
