from llm_word_parser.db import setup_database
from llm_word_parser.options import add_menu_item


def init_addon():
    setup_database()
    add_menu_item()


init_addon()
