from typing import List, Optional

from aqt.editor import Editor
from aqt.qt import *
from aqt.utils import showInfo

from llm_word_parser import DocumentRepository


class GenerateDialog(QDialog):
    def __init__(self, editor: Editor, word: str, doc_repo: DocumentRepository):
        super().__init__()
        self.editor = editor
        self.setWindowTitle("Generate Contents")
        self.word = word
        self.context: str | None = None
        self.setup_ui(doc_repo)

    def setup_ui(self, doc_repo: DocumentRepository) -> None:
        layout = QVBoxLayout(self)

        # Textarea
        self.dropdown = QComboBox(self)
        items = self.get_items(doc_repo)
        self.dropdown.addItems(items)
        self.dropdown.currentIndexChanged.connect(self.update_context)  # Connect the signal to the new method
        layout.addWidget(self.dropdown)

        # Initialize self.context to the first item in the dropdown
        if items:
            self.context = items[0]

        # Button Box
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_items(self, doc_repo: DocumentRepository) -> List[str]:
        default_doc = doc_repo.get_default_document()
        if not default_doc:
            showInfo("The default document hasn't been set.")
            return []
        return default_doc.get_contexts(self.word)

    def update_context(self, index: int) -> None:
        # Update the context variable when the selected item changes
        self.context = self.dropdown.itemText(index)