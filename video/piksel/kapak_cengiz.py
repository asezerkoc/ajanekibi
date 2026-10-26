"""Reels kapağı arka planı ve karakteri (64-bit piksel): atının üstünde Cengiz Han, kızıl gün batımı,
sancaklar, karlı dağlar, nehir, yurt kampı, uzakta atlı ordu, kartal; elinde kanlı kılıç.

Çıktı: video/public/kapak-cengiz-arka.png (540x960 ızgara). Başlık ve logo Remotion'da eklenir
(KapakSavas, src/sahneler/Kapak.tsx).

Kullanım: python3 -I video/piksel/kapak_cengiz.py [--onizleme dosya]
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import ImageDraw  # noqa: E402

from ciz import (H, W, _ac, _esik, arazi, at, buyut, duman, figur, gradyan, gunes, hex2, piksel, sirt, yeni,  # noqa: E402
                 yurt)

UFUK = 580  # ova çizgisi (ızgara y)


def gokyuzu(img):
    gradyan(img, ["#2a0a0e", "#4a1214", "#7a1e16", "#b23a1a", "#e0661e", "#f8a040", "#ffc866"], 0, UFUK)
    rnd = random.Random(4)
    d = ImageDraw.Draw(img)
    # yatay, yanık kızıl bulut şeritleri: altları güneşten turuncu ışık alır
    for _ in range(26):
        y = rnd.randint(40, 520)
        x = rnd.randint(-80, W)
        uz = rnd.randint(90, 260)
        kal = rnd.randint(6, 16)
        koyu = _ac("#3a0e10", min(0.5, y / 900))
        for i in range(uz):
            yy = y + int(math.sin((x + i) / 37 + y) * 3)
            ust = kal * math.sin(math.pi * i / uz)
            for k in range(int(ust)):
                piksel(img, x + i, yy - k, hex2(koyu if k > 2 else _ac(koyu, 0.08)))
            for k in range(2):  # alt kenar ışığı
                if _esik(x + i, yy + k) < 0.75:
                    piksel(img, x + i, yy + k, hex2("#f08a30" if y > 250 else "#c84a22"))


def kartal(img, x, y, s, faz=0.3):
    d = ImageDraw.Draw(img)
    k = hex2("#1a0a08")
    kanat = math.sin(faz * math.pi) * 6 * s
    d.polygon([(x - 26 * s, y - kanat), (x - 10 * s, y - 3 * s), (x, y), (x + 10 * s, y - 3 * s), (x + 26 * s, y - kanat),
               (x + 14 * s, y + 1 * s), (x + 4 * s, y + 3 * s), (x, y + 8 * s), (x - 4 * s, y + 3 * s), (x - 14 * s, y + 1 * s)], fill=k)
    for i in range(4):  # kanat ucu tüyleri
        for yon in (-1, 1):
            d.line([(x + yon * (20 + i * 2) * s, y - kanat + i * s), (x + yon * (26 + i) * s, y - kanat + (i + 2) * s)], fill=k)
    d.polygon([(x - 2 * s, y + 7 * s), (x + 2 * s, y + 7 * s), (x, y + 12 * s)], fill=k)


def daglar(img):
    zemin = sirt(522, 30, 21, 7, 9)
    zemin = [z if x > 250 else z + int((250 - x) * 0.25) for x, z in enumerate(zemin)]
    for x, z in enumerate(zemin):
        for y in range(z, UFUK + 4):
            yuk = (y - z)
            if yuk < 14 + (x * 7 % 9) and z < 525:
                renk = "#f4ece4" if _esik(x, y) < 0.8 or yuk < 5 else "#c8b8c0"  # karlı doruk
            else:
                renk = "#6a4258" if (x + y) % 9 else "#5a3448"
                if x % 23 < 11 and yuk > 10:
                    renk = "#4e2c42"  # gölgeli yamaç
            piksel(img, x, y, hex2(renk))
        # günbatımı ışığı sırt kenarında
        piksel(img, x, z, hex2("#ffb070"))


def ova(img):
    z = [UFUK] * W
    arazi(img, z, ["#c86a30", "#a85428", "#8a4222", "#6e341c", "#56281a", "#3e1c14", "#2a120e"], "#f8a050", doku_tohum=3,
          perspektif=True)
    d = ImageDraw.Draw(img)
    # kıvrılan nehir: güneşi yansıtır
    for i in range(400):
        t = i / 400
        x = 560 - t * 330 + math.sin(t * 7) * 30
        y = UFUK + 4 + t * t * 120
        gen = 2 + t * 16
        d.line([(x - gen, y), (x + gen, y)], fill=hex2("#f8c070" if (i // 6) % 3 else "#ffe0a0"))
        d.line([(x - gen - 1, y + 1), (x - gen + 2, y + 1)], fill=hex2("#5a3020"))


def kamp(img):
    z = [UFUK + 22] * W
    for x, s in ((420, 1.0), (452, 1.25), (488, 0.95), (520, 1.15), (396, 0.8)):
        baca = figur(img, yurt, x, z, s, keçe="#e8c8a0", golge="#a87a5a", kapi="#8a2a1a", kontur="#2a120a")
        duman(img, baca[0], baca[1], 30, x, faz=0.4, renk="#a87060", ruzgar=0.4, genislik=0.6)


def sancak(img, x_dip, y_dip, x_tepe, y_tepe, boy, renk="#8a1a16", faz=0.0, sus=True):
    """Direğe bağlı, rüzgârda dalgalanan sancak; direk dibi zemine dikili."""
    d = ImageDraw.Draw(img)
    d.line([(x_dip, y_dip), (x_tepe, y_tepe)], fill=hex2("#2a1208"), width=max(1, int(boy / 40)))
    gen, yuk = boy, boy * 0.62
    ust, alt = [], []
    for i in range(int(gen) + 1):
        t = i / gen
        dal = math.sin(t * 5 + faz) * yuk * 0.07 * t
        ust.append((x_tepe + i, y_tepe + 4 + dal + t * yuk * 0.08))
        alt.append((x_tepe + i, y_tepe + 4 + yuk + dal - t * yuk * 0.1))
    d.polygon(ust + alt[::-1], fill=hex2(renk))
    for i in range(0, int(gen), 3):  # kumaş kıvrım gölgeleri
        t = i / gen
        if math.cos(t * 5 + faz) < -0.3:
            d.line([ust[i], alt[i]], fill=hex2(_ac(renk, -0.3)))
        elif math.cos(t * 5 + faz) > 0.6:
            d.line([ust[i], alt[i]], fill=hex2(_ac(renk, 0.15)))
    for i in range(0, int(gen) - 4, 9):  # saçak
        d.line([alt[i], (alt[i][0] + 1, alt[i][1] + yuk * 0.07)], fill=hex2("#d8a040"))
    if sus:  # altın düğüm süsü (sonsuzluk düğümü esinli)
        cx, cy = x_tepe + gen * 0.42, y_tepe + 4 + yuk * 0.5
        r = yuk * 0.24
        renk_s = hex2("#f0d8a0")
        for k in range(4):
            a = k * math.pi / 2
            ex, ey = cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55
            d.ellipse([ex - r * 0.45, ey - r * 0.45, ex + r * 0.45, ey + r * 0.45], outline=renk_s, width=max(1, int(r / 6)))
        d.ellipse([cx - r * 0.18, cy - r * 0.18, cx + r * 0.18, cy + r * 0.18], fill=renk_s)
    piksel(img, x_tepe, y_tepe - 2, hex2("#e0b040"))
    d.polygon([(x_tepe - 3, y_tepe), (x_tepe, y_tepe - 8), (x_tepe + 3, y_tepe)], fill=hex2("#e0b040"))


def ordu(img):
    z = [UFUK + 70] * W
    rnd = random.Random(9)
    for x in range(250, 545, 22):
        figur(img, at, x + rnd.randint(-4, 4), z, 1.0, -1, rnd.choice(("#3a2418", "#4a2e1e", "#2a1810")), "#120806",
              binici=rnd.choice(("#3a2020", "#2a2a30", "#4a2a1a")), faz=rnd.random(), kontur="#1a0a06")
    for x in range(262, 545, 66):  # ordunun sancakları
        sancak(img, x, UFUK + 70, x, UFUK + 6, 20, faz=x, sus=False)
    z2 = [UFUK + 40] * W
    for x in range(300, 545, 15):  # daha uzakta ikinci sıra (silüet)
        at(img, x, z2, 0.6, -1, "#3a1a12", "#1a0a08", binici="#2a1410", faz=rnd.random())


def han(img, cx, cy, s):
    """Cengiz Han: kürk börk, uzun saç, gür sakal, sert bakış, pullu zırh, kırmızı pelerin."""
    d = ImageDraw.Draw(img)

    def p(x, y):
        return (cx + x * s, cy + y * s)

    def poli(n, r):
        d.polygon([p(*q) for q in n], fill=hex2(r))

    def elips(x0, y0, x1, y1, r):
        d.ellipse([*p(x0, y0), *p(x1, y1)], fill=hex2(r))

    def cizgi(n, r, k=1.0):
        d.line([p(*q) for q in n], fill=hex2(r), width=max(1, int(k * s)), joint="curve")

    alt = (H - cy) / s + 2
    TEN, TEN_G, TEN_I = "#b87650", "#8a5232", "#d8966a"
    SAC = "#160c08"
    # pelerin: arkada sola savrulur
    poli([(-30, 30), (-150, 70), (-175, alt), (40, alt), (50, 40)], "#7a1414")
    for x in range(-160, 30, 9):
        cizgi([(x + 20, 60 + abs(x) * 0.1), (x, alt)], "#5a0e0e", 0.8)
    cizgi([(-150, 70), (-175, alt)], "#a82a1e", 1.2)
    # gövde ve zırh
    poli([(-62, 36), (62, 36), (74, alt), (-74, alt)], "#3a2418")
    for sira, y in enumerate(range(52, int(alt), 8)):
        kay = (sira % 2) * 4
        for x in range(-58 + kay, 58, 8):
            elips(x, y, x + 7, y + 8, "#5a4630" if (x // 8 + sira) % 4 else "#7a6040")
            cizgi([(x, y + 8), (x + 7, y + 8)], "#22160e", 0.6)
            piksel(img, *p(x + 3, y + 2.5), hex2("#b89060"))
    poli([(-16, 40), (16, 40), (20, alt), (-20, alt)], "#2a1810")  # göğüs plakası arkası
    for y in range(48, 110, 12):  # göğüs plakaları
        poli([(-14, y), (14, y), (12, y + 10), (-12, y + 10)], "#6a5236")
        cizgi([(-14, y), (14, y)], "#a8845a", 0.6)
    for x, y in ((-36, 70), (36, 70), (0, 62)):  # altın madalyonlar
        elips(x - 7, y - 7, x + 7, y + 7, "#c8962a")
        elips(x - 4, y - 4, x + 3, y + 3, "#f0c860")
        cizgi([(x - 6, y + 6), (x + 6, y + 6)], "#7a5414", 0.6)
    poli([(-50, 118), (50, 118), (52, 132), (-52, 132)], "#4a2a16")  # kemer
    elips(-9, 116, 9, 134, "#c8962a")
    for x, yon in ((-62, -1), (62, 1)):  # omuz plakaları
        for k in range(3):
            elips(x - 22 + k * 2 * yon, 34 + k * 9, x + 22 + k * 2 * yon, 56 + k * 9, "#5a4630" if k % 2 else "#6e563a")
            cizgi([(x - 20, 50 + k * 9), (x + 20, 50 + k * 9)], "#c8962a", 0.6)
    # kürk yaka
    poli([(-50, 22), (50, 22), (64, 44), (30, 56), (0, 50), (-30, 56), (-64, 44)], "#7a5a3a")
    for i in range(-60, 62, 3):
        cizgi([(i, 26 + abs(i) * 0.12), (i + 2, 48 - abs(i) * 0.05)], "#a88458" if i % 9 == 0 else "#5a3e26", 0.6)
    # uzun saç: omuzlara iner
    for yon in (-1, 1):
        poli([(16 * yon, -20), (28 * yon, -10), (34 * yon, 34), (22 * yon, 40), (16 * yon, 10)], SAC)
        for k in range(4):
            cizgi([(20 * yon + k * 2 * yon, -8), (24 * yon + k * 3 * yon, 36)], "#2e2016", 0.5)
    # boyun ve yüz
    poli([(-10, 14), (10, 14), (12, 30), (-12, 30)], TEN_G)
    elips(-17, -22, 17, 24, TEN)
    poli([(4, -18), (17, -6), (16, 12), (8, 22), (6, 6)], TEN_G)
    elips(-15, -16, -5, 4, TEN_I)
    # sert bakış
    for yon in (-1, 1):
        poli([(15 * yon, -10), (3 * yon, -4), (3 * yon, -1), (15 * yon, -6)], SAC)
        poli([(12 * yon, -2), (4 * yon, 0), (5 * yon, 2), (12 * yon, 1)], "#e8dccc")
        elips(7 * yon - 1.8, -1.6, 7 * yon + 1.8, 1.6, SAC)
        cizgi([(12 * yon, -2), (4 * yon, -0.5)], SAC, 0.8)
        cizgi([(13 * yon, 4), (6 * yon, 5)], TEN_G, 0.6)
        cizgi([(15 * yon, -14), (6 * yon, -13)], TEN_G, 0.4)  # alın çizgisi
    cizgi([(-2, -8), (0, -3), (2, -8)], TEN_G, 0.6)
    poli([(-1, -2), (2, -2), (4, 9), (-3, 9)], TEN)
    cizgi([(2, -1), (4, 8)], TEN_G, 0.8)
    elips(-4, 7, 4, 11, TEN_G)
    # gür bıyık ve sakal
    poli([(-12, 10), (12, 10), (16, 22), (14, 34), (6, 44), (0, 46), (-6, 44), (-14, 34), (-16, 22)], SAC)
    for x in range(-12, 13, 3):
        cizgi([(x, 14), (x * 0.6, 42)], "#3a2a20", 0.5)
    for x in (-8, 3, 9):
        cizgi([(x, 20), (x * 0.7, 38)], "#6a5a50", 0.4)  # kır teller
    poli([(-14, 10), (14, 10), (12, 14), (-12, 14)], "#2a1a12")  # bıyık
    cizgi([(-5, 16), (5, 16)], "#6a2018", 0.8)  # sıkılı dudak
    # kürk börk: kalın kürk kenar, deri kubbe, altın sivri, siyah tüy
    elips(-26, -40, 26, -18, "#4a3222")
    poli([(-18, -36), (-14, -52), (0, -58), (14, -52), (18, -36)], "#5a2a18")
    for k in range(-14, 15, 7):
        cizgi([(k * 0.4, -57), (k, -37)], "#c8962a", 0.6)
    elips(-29, -31, 29, -13, "#4a3628")
    for x in range(-27, 28, 2):
        cizgi([(x, -30 + abs(x) * 0.05 + (x % 3)), (x + 1, -14 - (x % 2))], "#8a7058" if x % 6 == 0 else ("#2e2018" if x % 4 else "#6a5444"), 0.6)
    cizgi([(0, -58), (0, -68)], "#e0b040", 1.4)
    elips(-3, -66, 3, -60, "#e0b040")
    for i in range(12):
        cizgi([(0, -68), (-4 - i * 0.8, -76 + i * 0.6), (-12 - i * 1.4, -70 + i * 1.6)], "#1a1210" if i % 3 else "#3a2e28", 0.7)
    # kılıçlı kol: aşağıda, kılıç çapraz iner
    poli([(-56, 50), (-84, 70), (-90, 120), (-64, 150), (-50, 140), (-66, 112), (-58, 78)], "#3a2418")
    for y in range(76, 140, 8):
        cizgi([(-86, y), (-62, y + 6)], "#7a6040", 0.8)
    elips(-74, 136, -50, 158, TEN)  # yumruk
    cizgi([(-71, 146), (-53, 146)], TEN_G, 0.6)
    poli([(-66, 128), (-50, 136), (-54, 142), (-70, 134)], "#c8962a")  # balçak
    cizgi([(-78, 154), (-86, 162)], "#4a2a16", 2.4)  # kabza ucu
    elips(-90, 160, -82, 168, "#e0b040")
    namlu = [(-52 + t * 150, 140 + t * 116 + math.sin(t * 2.4) * 8) for t in [i / 160 for i in range(161)]]  # uç kadrajda
    for i in range(len(namlu) - 1):
        (x0, y0), (x1, y1) = namlu[i], namlu[i + 1]
        g = 6.5 * (1 - (i / 160) ** 4)
        poli([(x0, y0 - g), (x0, y0 + g * 0.5), (x1, y1 + g * 0.5), (x1, y1 - g)], "#b8bec6")
        cizgi([(x0, y0 - g * 0.8), (x1, y1 - g * 0.8)], "#f4f6f8", 0.6)
        cizgi([(x0, y0 + g * 0.1), (x1, y1 + g * 0.1)], "#7a8088", 0.4)
    rnd = random.Random(11)
    for i in range(60, 160):  # kan: namlunun uç yarısında, aşağı damlar
        if rnd.random() < 0.95:
            x, y = namlu[i]
            g = 6.5 * (1 - (i / 160) ** 4)
            for _ in range(7):
                piksel(img, *p(x + rnd.uniform(-1, 1), y + rnd.uniform(-g, g * 0.5)), hex2(rnd.choice(("#8a0a0a", "#b01212", "#6a0606"))))
    for i in (96, 120, 142):  # damlalar
        x, y = namlu[i]
        for k in range(rnd.randint(5, 10)):
            elips(x - 0.8, y + 3 + k * 1.2, x + 0.8, y + 4.6 + k * 1.2, "#a00e0e")
    # diğer el: dizgin tutar
    elips(46, 128, 66, 146, TEN)
    cizgi([(56, 140), (150, 190)], "#3a1a0e", 0.9)


def at_basi(img, cx, cy, s):
    """Sağ altta Cengiz Han'ın atının başı: uzun yüzlü koyu doru, sola aşağı bakar; gem, yular ve kırmızı püsküller."""
    d = ImageDraw.Draw(img)

    def p(x, y):
        return (cx + x * s, cy + y * s)

    g, k = "#3a2016", "#140a06"
    d.polygon([p(44, 70), p(34, -10), p(16, -40), p(4, -44), p(-10, -36), p(-26, -6), p(-38, 14), p(-40, 26),
               p(-30, 32), p(-14, 26), p(-2, 38), p(10, 70)], fill=hex2(g))
    d.polygon([p(2, -42), p(-2, -62), p(10, -46)], fill=hex2(g))  # kulaklar: sivri, dik
    d.polygon([p(10, -44), p(16, -64), p(20, -42)], fill=hex2(_ac(g, -0.15)))
    for i in range(-44, 60, 3):  # yele boyun arkasında
        d.line([p(30 + i * 0.12, i), p(44 + i * 0.1, i + 10)], fill=hex2(k), width=max(1, int(s)))
    d.line([p(-6, -36), p(-30, 4)], fill=hex2(_ac(g, 0.2)), width=max(1, int(s)))  # burun sırtı ışığı
    d.ellipse([*p(-8, -24), *p(0, -17)], fill=hex2("#0a0604"))  # göz
    piksel(img, *p(-5, -22), hex2("#f0e0c0"))
    d.ellipse([*p(-36, 14), *p(-31, 19)], fill=hex2("#0a0604"))  # burun deliği
    d.line([p(-36, 26), p(-24, 28)], fill=hex2(k))  # ağız
    d.line([p(-30, 2), p(-6, 12)], fill=hex2("#5a2a14"), width=max(1, int(1.8 * s)))  # burun kayışı
    d.line([p(0, -38), p(-6, 14)], fill=hex2("#5a2a14"), width=max(1, int(1.8 * s)))  # yanak kayışı
    d.line([p(-6, -34), p(14, -40)], fill=hex2("#5a2a14"), width=max(1, int(1.6 * s)))  # alın kayışı
    d.line([p(-28, 22), p(30, 50)], fill=hex2("#3a1a0e"), width=max(1, int(s)))  # dizgin
    for x, y in ((-30, 2), (-6, 12), (0, -38)):
        d.ellipse([*p(x - 3, y - 3), *p(x + 3, y + 3)], fill=hex2("#c8962a"))
        for i in range(10):  # kırmızı püskül
            d.line([p(x, y + 3), p(x - 3 + i * 0.6, y + 15 + i % 3)], fill=hex2("#b01a14" if i % 2 else "#7a0e0a"))


def main():
    img = yeni()
    gokyuzu(img)
    gunes(img, 405, 470, 62, ["#ffd88a", "#ffb050"])
    kartal(img, 448, 404, 1.6)
    for x, y in ((360, 360), (382, 340), (500, 330)):
        kartal(img, x, y, 0.35, faz=0.6)
    daglar(img)
    ova(img)
    kamp(img)
    ordu(img)
    sancak(img, 10, 960, 30, 196, 230, faz=0.4)  # büyük sancak, direk kadrajın altına iner
    sancak(img, 4, 960, 6, 420, 60, renk="#6a1210", faz=1.2, sus=False)
    figur(img, han, 196, 452, 2.05, kontur="#120604", f_isik=0.1, f_golge=0.18)
    figur(img, at_basi, 452, 840, 2.4, kontur="#0a0402", f_isik=0.12, f_golge=0.2)
    # alt kenarda logo için koyulaşma (basamaklı)
    for i, y0 in enumerate((820, 870, 910)):
        for y in range(y0, H):
            for x in range(W):
                if (x + y) % 3 == 0:
                    piksel(img, x, y, hex2("#0a0402", 40 + i * 20))
    hedef = Path(__file__).parents[1] / "public" / "kapak-cengiz-arka.png"
    img.save(hedef)
    print("yazıldı:", hedef)
    if "--onizleme" in sys.argv:
        buyut(img).save(sys.argv[sys.argv.index("--onizleme") + 1])


if __name__ == "__main__":
    main()
