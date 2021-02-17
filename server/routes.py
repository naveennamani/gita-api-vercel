from typing import Union

from fastapi import APIRouter

from server.model import APIError
from server.model import GitaVerse
from server.model import Language
from server.utils import chapter_wise_verse_counts
from server.utils import get_ch_verse_no
from server.utils import get_odia_verse
from server.utils import get_telugu_verse

router = APIRouter()


@router.get("/{language}/verse/{chapter_no}/{verse_no}",
            response_model = Union[GitaVerse, APIError])
def get_verse(language: Language, chapter_no: int, verse_no: int):
    if chapter_no > 18 or chapter_no <= 0:
        return {
            "error": "Invalid chapter no",
            "message": "Please ensure chapter no to be <= 18"
        }
    if not 0 < verse_no <= chapter_wise_verse_counts[chapter_no - 1]:
        return {
            "error": "Invalid verse no",
            "message": f"The chapter {chapter_no} has only {chapter_wise_verse_counts[chapter_no - 1]}"
                       f" verses"
        }
    return serve_verse(language, chapter_no, verse_no)


@router.get("/{language}/verse/{verse_no_serial}", response_model = Union[GitaVerse, APIError])
def get_verse_serial(language: Language, verse_no_serial: int):
    if not 0 < verse_no_serial <= 701:
        return {
            "error": "Invalid verse no",
            "message": "The BG has only 700 verses"
        }
    return serve_verse(language, *get_ch_verse_no(verse_no_serial))


def serve_verse(language: Language, chapter_no: int, verse_no: int):
    if language == Language.telugu:
        return get_telugu_verse(chapter_no, verse_no)
    elif language == Language.odia:
        return get_odia_verse(chapter_no, verse_no)
    else:
        return {
            "error": "Language not implemented",
            "message": f"Language {language} not implemented yet"
        }
