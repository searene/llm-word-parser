from typing import Optional

from anki.models import FieldDict
from anki.notes import Note


def get_field_by_name(target_field_name: str, note: Note) -> Optional[FieldDict]:
    """Get the field by name from the note."""
    note_type = note.note_type()
    if note_type is None:
        return None
    for fld in note_type['flds']:
        if fld['name'] == target_field_name:
            return fld
    return None


def get_field_contents(field_name: str, note: Note) -> Optional[str]:
    """Get the field contents by name from the note."""
    field = get_field_by_name(field_name, note)
    if field is None:
        return None
    return note.fields[field['ord']]