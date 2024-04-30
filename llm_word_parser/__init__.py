from llm_word_parser.db import setup_database
from llm_word_parser.options import add_menu_item, add_toolbar_btn


def init_addon() -> None:
    setup_database()
    add_menu_item()
    add_toolbar_btn()


init_addon()
