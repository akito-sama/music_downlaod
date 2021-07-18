#!/usr/bin/python
import json
import requests
import youtube_dl as yd
import sys


def _print(value):
    print("----------------------------------", value)


def reformat_url(name: str):
    dico_translator = {
        58: "%3A",
        47: "%2F",
        63: "%3F",
        35: "%23",
        91: "%5B",
        93: "%5D",
        64: "%40",
        33: "%21",
        36: "%24",
        38: "%26",
        39: "%27",
        40: "%28",
        41: "%29",
        42: "%2A",
        43: "%2B",
        44: "%2C",
        59: "%3B",
        61: "%3D",
        37: "%25",
        32: "+",
    }
    translated_name = name.translate(dico_translator)
    link = f"https://www.youtube.com/results?search_query={translated_name}"
    return link


def search_video(name: str, limite: int):
    formats = {"writethumbnail": True}
    youtube_link = reformat_url(name)
    print(youtube_link)
    with yd.YoutubeDL(formats) as youtube:
        return youtube.extract_info(f"ytsearch{limite}:{name}", download=False)


if __name__ == "__main__":
    print(search_video(" ".join(sys.argv[1:]), 6))
