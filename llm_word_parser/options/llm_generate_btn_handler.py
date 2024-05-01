from aqt import mw
from aqt.editor import Editor
import json

from aqt.utils import showInfo

from llm_word_parser import DocumentRepository
from llm_word_parser.dictionary.repository import DictionaryRepository
from llm_word_parser.llm.Llama import Llama
from llm_word_parser.options import GenerateDialog
from llm_word_parser.util import get_field_contents


def __get_dictionary_contents(word: str, dictionary_repository: DictionaryRepository) -> dict[str, str]:
    dictionaries = dictionary_repository.get_active_dictionaries()
    res = {}
    for dictionary in dictionaries:
        definition = dictionary.query(word)
        if definition:
            res[dictionary.name] = definition
    return res


def __get_dictionary_contents_in_str(dictionary_contents: dict[str, str], separator: str) -> str:
    return separator.join([f"{name}:\n{definition}\n" for name, definition in dictionary_contents.items()])


def __build_llm_prompt(word: str, context: str, dictionary_contents: dict[str, str]) -> str:
    separator = "--------------------------------------------------------"
    return f"""
    I'm learning a foreign language, below is the definition of the word "{word}" from my dictionaries, different dictionaries will be shown separately, each containing two parts: the dictionary name and the dictionary definition. Each dictionary will be separated by {separator}.
    
    You need to generate a JSON based on these definitions, the JSON should have following properties:
    - Word: the word you are learning
    - IPA: the International Phonetic Alphabet of the word
    - Type: the type of the word, e.g. noun, verb, etc.
    - Meaning: the meaning of the word
    - Sentence: a sentence that uses the word
    
    Notice that:
    1. You should only fill the values of these properties verbatim from dictionary definitions I'll give you, don't make them up yourself.
    2. One word may have multiple definition, choose the one which is the same as the definition of the word {word} in this sentence: {context}
    3. Only generate the JSON, don't add extra explanations or comments. In other words, your answer should start with {{ and ends with }}.
    
    Here are the definitions:
    
    {__get_dictionary_contents_in_str(dictionary_contents, separator)}
"""


def on_llm_generate_btn_clicked(editor: Editor, dict_repo: DictionaryRepository, doc_repo: DocumentRepository) -> None:
    if not editor.note:
        showInfo("The editor's note is not found.")
        return
    word = get_field_contents("Word", editor.note)
    if not word:
        showInfo("Cannot get the current word from the \"Word\" field.")
        return
    dialog = GenerateDialog(editor, word, doc_repo)
    if not dialog.exec():
        return
    if not editor.note:
        raise Exception("The editor's note is not found.")
    if not mw:
        raise Exception("Anki is not running.")
    if not dialog.context:
        showInfo("No context is available.")
        return
    dictionary_contents = __get_dictionary_contents(dialog.word, dict_repo)
    llm_prompt = __build_llm_prompt(dialog.word, dialog.context, dictionary_contents)
    print(f"prompt {llm_prompt}")
    llm_response = Llama().answer(llm_prompt)
    print(f"llm response: {llm_response}")
    answer_in_json = json.loads(llm_response)
    for fieldName, fieldValue in answer_in_json.items():
        editor.note[fieldName] = fieldValue
    mw.col.update_note(editor.note)
