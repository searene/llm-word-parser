from aqt.qt import QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QMessageBox


class DictionaryTab(QWidget):
    def __init__(self, parent=None):
        super(DictionaryTab, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # List widget to display dictionaries
        self.dictionary_list = QListWidget()
        self.layout.addWidget(self.dictionary_list)

        # Buttons for dictionary management
        self.add_path_button = QPushButton("Add Scan Path")
        self.add_path_button.clicked.connect(self.add_scan_path)
        self.layout.addWidget(self.add_path_button)

        self.rescan_button = QPushButton("Rescan Dictionaries")
        self.rescan_button.clicked.connect(self.rescan_dictionaries)
        self.layout.addWidget(self.rescan_button)

        self.set_active_button = QPushButton("Toggle Active/Inactive")
        self.set_active_button.clicked.connect(self.toggle_dictionary_active)
        self.layout.addWidget(self.set_active_button)

        self.refresh_dictionary_list()

    def add_scan_path(self):
        directory_path = QFileDialog.getExistingDirectory(self, "Select Dictionary Folder")
        if directory_path:
            # Assume storing paths in a simple text file
            with open('dictionary_paths.txt', 'a') as file:
                file.write(directory_path + '\n')
            self.rescan_dictionaries()
            QMessageBox.information(self, "Path Added", "Scan path has been added successfully.")

    def rescan_dictionaries(self):
        try:
            with open('dictionary_paths.txt', 'r') as paths_file:
                paths = paths_file.readlines()
            dictionaries = []
            for path in paths:
                # Simulating dictionary scanning in the directory
                # In practice, you'd check for dictionary files here
                dictionaries.append(path.strip() + "/example_dict.mdict")
            with open('dictionaries.txt', 'w') as file:
                for dictionary in dictionaries:
                    file.write(dictionary + '\n')
            self.refresh_dictionary_list()
        except FileNotFoundError:
            QMessageBox.warning(self, "No Paths Found", "No scan paths found. Please add a scan path first.")

    def toggle_dictionary_active(self):
        selected_item = self.dictionary_list.currentItem()
        if selected_item:
            # Simple toggle implementation, assuming dictionaries are toggled in a file
            active_dictionaries = self.get_active_dictionaries()
            dictionary_path = selected_item.text()
            if dictionary_path in active_dictionaries:
                active_dictionaries.remove(dictionary_path)
            else:
                active_dictionaries.add(dictionary_path)
            with open('active_dictionaries.txt', 'w') as file:
                for dictionary in active_dictionaries:
                    file.write(dictionary + '\n')
            QMessageBox.information(self, "Toggle Active", "Dictionary active status toggled.")

    def refresh_dictionary_list(self):
        self.dictionary_list.clear()
        try:
            with open('dictionaries.txt', 'r') as file:
                dictionaries = file.readlines()
            for dictionary in dictionaries:
                self.dictionary_list.addItem(dictionary.strip())
        except FileNotFoundError:
            with open('dictionaries.txt', 'w') as file:  # Create the file if it does not exist
                pass

    def get_active_dictionaries(self):
        try:
            with open('active_dictionaries.txt', 'r') as file:
                return set(file.read().splitlines())
        except FileNotFoundError:
            return set()
