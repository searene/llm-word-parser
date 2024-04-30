import os

from aqt.qt import QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QMessageBox

from llm_word_parser.document import Document
from llm_word_parser.document.repository import document_repository


class DocumentTab(QWidget):
    def __init__(self, parent: QWidget):
        super(DocumentTab, self).__init__(parent)
        self.doc_repo = document_repository

        layout = QVBoxLayout(self)
        self.document_list = QListWidget(self)
        layout.addWidget(self.document_list)

        self.import_button = QPushButton("Import Document")
        self.import_button.clicked.connect(self.import_document)
        layout.addWidget(self.import_button)

        self.delete_button = QPushButton("Delete Document")
        self.delete_button.clicked.connect(self.delete_document)
        layout.addWidget(self.delete_button)

        self.set_default_button = QPushButton("Set as Default")
        self.set_default_button.clicked.connect(self.set_default_document)
        layout.addWidget(self.set_default_button)

        self.refresh_document_list()

    def import_document(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Document", "", "Text files (*.txt);;All files (*)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            filename = os.path.basename(file_path)
            try:
                document = Document(None, filename, content)
                doc_id = self.doc_repo.add(document)
                if self.doc_repo.count() == 1:
                    self.doc_repo.set_as_default(doc_id)
                QMessageBox.information(self, "Import Successful", "Document has been imported successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Import Failed", str(e))
            finally:
                self.refresh_document_list()

    def set_default_document(self):
        selected_item = self.document_list.currentItem()
        if selected_item:
            document_name = selected_item.text()
            try:
                document = self.doc_repo.find_by_name(document_name)
                if not document.id:
                    raise ValueError("Document ID is required.")
                self.doc_repo.set_as_default(document.id)
                QMessageBox.information(self, "Set Default", f"Default document set to '{document_name}' successfully.")
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))

    def refresh_document_list(self) -> None:
        self.document_list.clear()
        try:
            all_docs = self.doc_repo.all_documents()
            document_names = [self.get_doc_name(doc) for doc in all_docs]
            for name in document_names:
                self.document_list.addItem(name)
        except Exception as e:
            QMessageBox.warning(self, "Error", "Failed to refresh document list: " + str(e))

    def delete_document(self):
        selected_item = self.document_list.currentItem()
        if selected_item:
            document_name = selected_item.text()
            try:
                document = self.doc_repo.find_by_name(document_name)
                if not document.id:
                    raise ValueError("Document ID is required.")
                if self.doc_repo.is_default(document.id):
                    self.doc_repo.remove_default()
                self.doc_repo.remove(document.id)
                QMessageBox.information(self, "Deletion Successful", "Document has been deleted successfully.")
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))
            finally:
                self.refresh_document_list()

    def get_doc_name(self, doc: Document) -> str:
        if not doc.id:
            raise ValueError("Document ID is required.")
        if self.doc_repo.is_default(doc.id):
            return f"{doc.filename} (Default)"
        return doc.filename
