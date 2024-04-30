import os
from typing import List

from anki.hooks import addHook
from aqt import mw
from aqt.editor import Editor

from aqt.qt import *
from aqt.utils import showInfo

from llm_word_parser.options.dictionary_tab import DictionaryTab
from llm_word_parser.options.document_tab import DocumentTab

from llm_word_parser.options.generate_dialog import GenerateDialog


def on_llm_generate_btn_clicked(editor: Editor) -> None:
    dialog = GenerateDialog(editor)
    if dialog.exec():
        showInfo("OK was pressed")
    else:
        showInfo("Cancel was pressed")


def add_generate_contents_btn(buttons: List[str], editor: Editor) -> List[str]:
    """Add a custom button to the editor's button box."""
    ai_icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'res', 'ai.png')
    editor._links['ai-generate-contents'] = on_llm_generate_btn_clicked
    return buttons + [editor._addButton(ai_icon_path,
                                  "ai-generate-contents",
                                  "Fill contents with LLM")]


def add_toolbar_btn() -> None:
    addHook("setupEditorButtons", add_generate_contents_btn)


def add_menu_item() -> None:
    if mw is None:
        raise Exception("Anki is not running")
    action = QAction("LLM-Word-Parser", mw)
    action.triggered.connect(open_main_dialog)
    mw.form.menuTools.addAction(action)


class MainDialog(QDialog):
    def __init__(self, parent: QWidget):
        super(MainDialog, self).__init__(parent)
        self.setWindowTitle("LLM-Word-Parser")
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.tab_document = DocumentTab(self)
        self.tab_dictionary = DictionaryTab(self)

        self.tabs.addTab(self.tab_document, "Document")
        self.tabs.addTab(self.tab_dictionary, "Dictionary")

        layout.addWidget(self.tabs)
        self.setLayout(layout)


def open_main_dialog():
    if mw is None:
        raise Exception("Anki is not running")
    dialog = MainDialog(mw)
    dialog.exec()
