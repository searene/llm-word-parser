from aqt import mw

from aqt.qt import QAction, QDialog, QTabWidget, QVBoxLayout

from llm_word_parser.options.dictionary import DictionaryTab
from llm_word_parser.options.document import DocumentTab


def add_menu_item():
    pass
    action = QAction("LLM-Word-Parser", mw)
    action.triggered.connect(open_main_dialog)
    mw.form.menuTools.addAction(action)


class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setWindowTitle("LLM-Word-Parser")
        self.layout = QVBoxLayout(self)

        # self.tabs = QTabWidget()
        # self.tab_document = DocumentTab(self)
        # self.tab_dictionary = DictionaryTab(self)
        #
        # self.tabs.addTab(self.tab_document, "Document")
        # self.tabs.addTab(self.tab_dictionary, "Dictionary")
        #
        # self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


def open_main_dialog():
    dialog = MainDialog(mw)
    dialog.exec_()


add_menu_item()
