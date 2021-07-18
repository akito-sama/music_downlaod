#!/usr/bin/python

import datetime
import io
import itertools
import requests
import sys


class Extractor:
    @staticmethod
    def extract_thumbnail(dico, nbr_video):
        entiers = dico["entries"][nbr_video]
        thumbnail = entiers["thumbnail"]
        return thumbnail

    @staticmethod
    def extract_title(dico, nbr_video):
        entiers = dico["entries"][nbr_video]
        title = entiers["title"]
        return title

    @staticmethod
    def extract_channel(dico, nbr_video):
        entiers = dico["entries"][nbr_video]
        chaine = entiers["channel"]
        return chaine

    @staticmethod
    def extract_time(dico, nbr_video):
        duration = dico["entries"][nbr_video]["duration"]
        time = datetime.timedelta(seconds=duration)
        return str(time)

    @staticmethod
    def extract_audio_link(dico, nbr_video):
        for i in dico["entries"][nbr_video]["formats"]:
            if i["ext"] == "webm":
                return i["url"], i["filesize"]

    @staticmethod
    def download_music(url, filename, size, write=False, pourcent=50):
        rps = requests.get(url, stream=True)
        dl = 0
        done = 0
        with open(f"{filename}.webm", "wb") as f:
            for content in rps.iter_content(4096):
                dl += len(content)
                done = int(pourcent * dl / size)
                if write:
                    sys.stdout.write("\r[%s%s]" % ("■" * done, " " * (pourcent - done)))
                f.write(content)
                yield done
        sys.stdout.write("\n")

    @staticmethod
    def extract_first_of_music(url, file: io.BytesIO):
        rps = requests.get(url, stream=True)
        for content in itertools.islice(rps.iter_content(4096), 0, 100, 1):
            file.write(content)
        return file


class Infos:
    def __init__(self, infos, nbr_video):
        self.channel = Extractor.extract_channel(infos, nbr_video)
        self.download_url, self.size = Extractor.extract_audio_link(infos, nbr_video)
        self.title = Extractor.extract_title(infos, nbr_video)
        if len(self.title) > 60:
            self.title = f"{self.title[:60]} ..."
        self.duration = Extractor.extract_time(infos, nbr_video)
        self.thumbnail = Extractor.extract_thumbnail(infos, nbr_video)
        self.all_infos_list = (
            (self.title, "title :"),
            (self.channel, "channel :"),
            (self.duration, "duration :"),
        )


if __name__ == "__main__":
    url = "https://r3---sn-hxqpuxa-jhoz.googlevideo.com/videoplayback?expire=1626024983&ei=t9fqYLR7oZ2YsA_Sq62wCA&ip=196.113.9.84&id=o-ADuOfxIq1VVIq63bLGVRd_VxZm3mrRTO7bjq1RrYUjq3&itag=249&source=youtube&requiressl=yes&mh=o2&mm=31%2C29&mn=sn-hxqpuxa-jhoz%2Csn-h5qzen76&ms=au%2Crdu&mv=m&mvi=3&pl=18&initcwndbps=283750&vprv=1&mime=audio%2Fwebm&ns=iYV0cvhZYcqomzYklfe_GjsG&gir=yes&clen=1777279&dur=280.081&lmt=1570185070304121&mt=1626002950&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=WEB&txp=5531432&n=zVtL05dTmza-jq4o5_&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIgCfjWSontqd2eyLs8ZtCDmyX0sxy01UXNrwsoAy7Qv0ICIQDmzvtn9PH1zvxF-5s1iW6FDPVmvzUygwnSEpWKfD21ZQ%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAK7rrX3utPp7mdZfg-64irsyaDQSYOEPNRCBTb6j12EeAiEA_9TaWDH59EV9Ln2_t3cFAtZPrguChqlgZE3wVqQMIQQ%3D"
    for i in Extractor.download_music(
        url, "This Game | no game no life", 2065195, write=True
    ):
        pass
