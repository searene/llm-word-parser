from typing import List

from aqt.editor import Editor
from aqt.qt import *
from aqt.utils import showInfo

from llm_word_parser.dictionary.repository import dictionary_repository
from llm_word_parser.document.repository import document_repository
from llm_word_parser.util import get_field_contents


class GenerateDialog(QDialog):
    def __init__(self, editor: Editor):
        super().__init__()
        self.editor = editor
        self.setWindowTitle("Generate Contents")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Textarea
        self.dropdown = QComboBox(self)
        self.dropdown.addItems(self.get_items())
        layout.addWidget(self.dropdown)

        # Button Box
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_items(self) -> List[str]:
        if not self.editor.note:
            showInfo("No note is selected.")
            return []
        word = get_field_contents("Word", self.editor.note)
        if word is None:
            showInfo("The \"Word\" field doesn't exist.")
            return []
        default_doc = document_repository.get_default_document()
        if not default_doc:
            showInfo("The default document hasn't been set.")
            return []
        return default_doc.get_contexts(word)
