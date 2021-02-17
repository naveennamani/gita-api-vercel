####################################################################################################
# Utility methods for gita API
####################################################################################################
import bisect
import json

import requests
from bs4 import BeautifulSoup

chapter_wise_verse_counts = [47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 35, 27, 20, 24, 28, 78]


def get_ch_verse_no(verse_no):
    chapter_wise_cumulative_verse_counts = [47, 119, 162, 204, 233, 280, 310, 338, 372, 414, 469,
                                            489, 524, 551, 571, 595, 623, 701]
    chapter_no = bisect.bisect_left(chapter_wise_cumulative_verse_counts, verse_no)
    return chapter_no + 1, verse_no - chapter_wise_cumulative_verse_counts[
        chapter_no - 1] if chapter_no > 0 else verse_no


def get_holy_bhagavad_gita_org_verse(chapter_no, verse_no, lang1, lang2):
    resp = requests.get(
        f"https://www.holy-bhagavad-gita.org/chapter/{chapter_no}/verse/{verse_no}/{lang1}")
    bs = BeautifulSoup(resp.text, "html.parser")
    current_verses = bs.select(".verseSmall > .current")
    if len(current_verses) > 1:
        verse_no = list(map(lambda x: int(x.text), current_verses))
        next_verse = verse_no[-1]
    else:
        next_verse = verse_no + 1
    chapter_name = bs.select_one(".chapterTitle").text.strip()
    main_verse_lines = [
        z.strip()
        for z in bs.select_one("#originalVerse").get_text("\n").split("\n")
        if z.strip()
    ]
    odl = ['୦', '୧', '୨', '୩', '୪', '୫', '୬', '୭', '୮', '୯']
    odltt = {ord(str(x)): y for x, y in enumerate(odl)}
    if isinstance(verse_no, list):
        main_verses = [[]]
        verse_no_iter = iter(verse_no + [0])
        current_verse_no = next(verse_no_iter)
        for verse in main_verse_lines:
            main_verses[-1].append(verse)
            if str(current_verse_no) in verse or str(current_verse_no).translate(odltt) in verse:
                current_verse_no = next(verse_no_iter)
                main_verses.append([])
        main_verse = ["\n".join(verse) for verse in main_verses][:-1]
        assert len(main_verse) == len(verse_no), (main_verse, verse_no)
    else:
        main_verse = "\n".join(main_verse_lines)
    word_meanings = bs.select_one("#wordMeanings").text.strip()
    audio_link = "https://www.holy-bhagavad-gita.org" + \
                 bs.select_one("audio").get_attribute_list("src")[0]
    translation = bs.select_one("#translation").text.strip().split('\r\n')[1].strip()
    commentary = [x.text.strip() for x in bs.select("#commentary > p")]
    return {
        "chapter_no": chapter_no,
        "verse_no": verse_no,
        "language": lang2,
        "chapter_name": chapter_name,
        "verse": main_verse,
        "transliteration": "",
        "synonyms": word_meanings,
        "audio_link": audio_link,
        "translation": translation,
        "purport": commentary,
        "next_verse": next_verse,
    }


def get_telugu_verse(chaper_no, verse_no):
    # return get_holy_bhagavad_gita_org_verse(chaper_no, verse_no, "te", "telugu")
    with open(f"verses_telugu_json/{chaper_no}.json") as fh:
        return json.load(fh)[str(verse_no)]


def get_odia_verse(chapter_no, verse_no):
    return get_holy_bhagavad_gita_org_verse(chapter_no, verse_no, "or", "odia")
