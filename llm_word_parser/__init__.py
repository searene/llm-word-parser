from aqt import mw

from llm_word_parser.db import setup_database, get_db_path
from llm_word_parser.dictionary.repository import DictionaryRepository
from llm_word_parser.document.repository import DocumentRepository
from llm_word_parser.options import add_menu_item, add_toolbar_btn


def init_addon() -> None:
    dict_repo = DictionaryRepository(get_db_path())
    doc_repo = DocumentRepository(get_db_path())
    setup_database()
    add_menu_item(dict_repo, doc_repo)
    add_toolbar_btn(dict_repo, doc_repo)


if mw:
    init_addon()
