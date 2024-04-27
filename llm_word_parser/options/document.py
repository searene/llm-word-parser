from aqt.qt import QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QMessageBox

class DocumentTab(QWidget):
    def __init__(self, parent=None):
        super(DocumentTab, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # List widget to display documents
        self.document_list = QListWidget()
        self.layout.addWidget(self.document_list)

        # Buttons for document management
        self.import_button = QPushButton("Import Document")
        self.import_button.clicked.connect(self.import_document)
        self.layout.addWidget(self.import_button)

        self.delete_button = QPushButton("Delete Document")
        self.delete_button.clicked.connect(self.delete_document)
        self.layout.addWidget(self.delete_button)

        self.set_default_button = QPushButton("Set as Default")
        self.set_default_button.clicked.connect(self.set_default_document)
        self.layout.addWidget(self.set_default_button)

        self.refresh_document_list()

    def import_document(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Document", "", "Text files (*.txt);;All files (*)")
        if file_path:
            # Assuming we're using a simple list to store file paths
            with open('document_list.txt', 'a') as file:
                file.write(file_path + '\n')
            self.refresh_document_list()
            QMessageBox.information(self, "Import Successful", "Document has been imported successfully.")

    def delete_document(self):
        selected_item = self.document_list.currentItem()
        if selected_item:
            confirmation = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this document?')
            if confirmation == QMessageBox.Yes:
                # Assuming we're using a simple list to store file paths
                with open('document_list.txt', 'r') as file:
                    lines = file.readlines()
                with open('document_list.txt', 'w') as file:
                    for line in lines:
                        if line.strip("\n") != selected_item.text():
                            file.write(line)
                self.refresh_document_list()
                QMessageBox.information(self, "Deletion Successful", "Document has been deleted successfully.")

    def set_default_document(self):
        selected_item = self.document_list.currentItem()
        if selected_item:
            with open('default_document.txt', 'w') as file:
                file.write(selected_item.text())
            QMessageBox.information(self, "Set Default", "Default document set successfully.")

    def refresh_document_list(self):
        self.document_list.clear()
        try:
            with open('document_list.txt', 'r') as file:
                documents = file.readlines()
            for document in documents:
                self.document_list.addItem(document.strip())
        except FileNotFoundError:
            with open('document_list.txt', 'w') as file:  # Create the file if it does not exist
                pass
