from typing import List

from anki.hooks import addHook
from aqt import mw
from aqt.editor import Editor
from aqt.qt import *

from llm_word_parser.dictionary.repository import DictionaryRepository
from llm_word_parser.document.repository import DocumentRepository
from llm_word_parser.options.dictionary_tab import DictionaryTab
from llm_word_parser.options.document_tab import DocumentTab
from llm_word_parser.options.generate_dialog import GenerateDialog
from llm_word_parser.options.llm_generate_btn_handler import on_llm_generate_btn_clicked


def add_generate_contents_btn(buttons: List[str], editor: Editor, dict_repo: DictionaryRepository, doc_repo: DocumentRepository) -> List[str]:
    """Add a custom button to the editor's button box."""
    ai_icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'res', 'ai.png')
    editor._links['ai-generate-contents'] = lambda editor: on_llm_generate_btn_clicked(editor, dict_repo, doc_repo)
    return buttons + [editor._addButton(ai_icon_path,
                                        "ai-generate-contents",
                                        "Fill contents with LLM")]


def add_toolbar_btn(dict_repo: DictionaryRepository, doc_repo: DocumentRepository) -> None:
    addHook("setupEditorButtons", lambda buttons, editor: add_generate_contents_btn(buttons, editor, dict_repo, doc_repo))


def add_menu_item(dictionary_repository: DictionaryRepository, document_repository: DocumentRepository) -> None:
    if mw is None:
        raise Exception("Anki is not running")
    action = QAction("LLM-Word-Parser", mw)
    action.triggered.connect(lambda: open_main_dialog(dictionary_repository, document_repository))
    mw.form.menuTools.addAction(action)


class MainDialog(QDialog):
    def __init__(self, parent: QWidget, dictionary_repository: DictionaryRepository, document_repository: DocumentRepository):
        super(MainDialog, self).__init__(parent)
        self.setWindowTitle("LLM-Word-Parser")
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.tab_document = DocumentTab(self, document_repository)
        self.tab_dictionary = DictionaryTab(self, dictionary_repository)

        self.tabs.addTab(self.tab_document, "Document")
        self.tabs.addTab(self.tab_dictionary, "Dictionary")

        layout.addWidget(self.tabs)
        self.setLayout(layout)


def open_main_dialog(dictionary_repository: DictionaryRepository, document_repository: DocumentRepository) -> None:
    if mw is None:
        raise Exception("Anki is not running")
    dialog = MainDialog(mw, dictionary_repository, document_repository)
    dialog.exec()
