# -*- coding: utf-8 -*-
class Geojp(object):
    """Japan Airport group in area"""
    hokkado = ("CTS", "MBE", "AKJ", "RIS", "HKD", "OKD", "KUH", "OBO",
               "MMB", "AKJ", "OIR", "SHB", "WKJ")
    tohoku = ("ONJ", "FKS", "GAJ", "AXT", "AOJ", "MSJ", "HNA", "SDJ", "SYO")
    kanto = ("HND", "NRT", "OIM", "MYE", "IBR", "HAC")
    chubu = ("NGO", "NKM", "TOY", "NTQ", "KMQ", "MMJ", "KIJ", "FSZ", "FUJ")
    kinki = ("KIX", "ITM", "SHM", "TJH", "UKB")
    chugoku = ("IWK", "IWJ", "HIW", "UBJ", "HIJ", "IZO", "OKI",
               "OKJ", "TTJ", "UBJ", "YGJ")
    shikoku = ("MYJ", "KCZ", "TAK", "TKS")
    kyushu = ("TSJ", "IKI", "HSG", "KUM", "TNE", "KOJ", "KMJ",
              "AXJ", "NGS", "FUK", "KKJ", "OIT", "KMI")
    ryukyu = ("KJP", "HTR", "AGJ", "OGN", "ISG", "TRA", "MMY", "UEO", "OKA", "RNJ",
              "OKE", "ASJ", "KKX", "KTD", "MMD", "TKN", "UEO")
    dct = {'hokkado': 1, 'tohoku': 2, 'kanto': 3, 'chubu': 4, 'kinki': 5,
           'chugoku': 6, 'shikoku': 7, 'kyushu': 8, 'ryukyu': 9}

    def get_area_id(self, code):
        if code in self.hokkado:
            return 1
        elif code in self.tohoku:
            return 2
        elif code in self.kanto:
            return 3
        elif code in self.kinki:
            return 5
        elif code in self.chugoku:
            return 6
        elif code in self.shikoku:
            return 7
        elif code in self.chubu:
            return 4
        elif code in self.kyushu:
            return 8
        else:
            return 9

    def get_area(self, code):
        if code in self.hokkado:
            return 'hokkado', 1
        elif code in self.tohoku:
            return 'tohoku', 2
        elif code in self.kanto:
            return 'kanto', 3
        elif code in self.kinki:
            return 'kinki', 5
        elif code in self.chugoku:
            return 'chugoku', 6
        elif code in self.shikoku:
            return 'shikoku', 7
        elif code in self.chubu:
            return 'chubu', 4
        elif code in self.kyushu:
            return 'kyushu', 8
        else:
            return 'ryukyu', 9
