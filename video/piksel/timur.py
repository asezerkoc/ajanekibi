"""Timur serisi (3 bölüm) sahneleri: 64-bit piksel sanatı, her sahne hikâyedeki olayı gösterir.

Bölüm 1 "Topal Kurt" (21-29) · Bölüm 2 "İki Yıldırım" (31-42) · Bölüm 3 "Lanetli Mezar" (51-63)

Dosyalar video/public/sahneNN-gokyuzu|uzak|orta|on|karakter|hava.png. Sprite'lar fizik denetiminden
geçer (taban_denetimi), yapılar düz zemine kurulur (duz_zemin). hava: yağmur/kar katmanı (24 kare).
Kullanım: python3 -I video/piksel/timur.py [sahne numaraları]
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import ImageDraw  # noqa: E402

from ciz import (H, W, _ac, _esik, at, figur, hex2, insan, orta_asya_sehri, piksel, sprite_sayfasi, taslar,  # noqa: E402
                 temas_golgesi, tug, yeni, yurt, zemin_y, duman)
from sahneler import GW, KARE, duz, gokyuzu, kaydet, on, orta, sprite, uzak  # noqa: E402
from timur_figur import (anadolu_kalesi, atli, bayezid, bibi_hanim, deve, fil, gemi, gur_i_emir, hendek,  # noqa: E402
                         heykel, kafa_kulesi, kisi, koy_evleri, koyun, mancinik, otag, oturan, sedir, tank, timur, yatan)
from kayip_mezar import cam  # noqa: E402


# ---------------------------------------------------------------- ortak yardımcılar


def hava(no, tur="yagmur", yogunluk=260, renk="#b8c8e0", egim=0.25):
    """Tam kare hava katmanı (24 karelik döngü): yağmur çizgileri ya da savrulan kar taneleri.
    Her tane bir döngüde tam sayı kez ekranı geçer, döngü dikişsiz."""
    rnd = random.Random(no)
    taneler = [(rnd.randrange(W), rnd.randrange(H), rnd.choice((1, 2)) if tur == "yagmur" else 1, rnd.random()) for _ in range(yogunluk)]

    def kare(t, z, i):
        f = i / KARE
        for x0, y0, hiz, faz in taneler:
            if tur == "yagmur":
                y = (y0 + f * H * hiz) % H
                x = (x0 - f * H * hiz * egim) % W
                for k in range(7):
                    piksel(t, x + k * egim, y - k, hex2(renk, 150 - k * 12))
            else:
                y = (y0 + f * H * hiz * 0.5) % H if hiz else y0
                y = (y0 + f * H) % H
                x = (x0 + math.sin((f + faz) * 2 * math.pi) * 6) % W
                piksel(t, x, y, hex2(renk, 230))
                if faz > 0.6:
                    piksel(t, x + 1, y, hex2(renk, 160))
                    piksel(t, x, y + 1, hex2(renk, 160))

    sayfa = sprite_sayfasi(W, H, KARE, kare)
    kaydet(sayfa, f"sahne{no}-hava.png")


def yatan_at(img, x, zemin, s=1.0, yon=1, renk="#5a3a24"):
    """Ölü at: yan yatmış gövde zemine değer, bacaklar kaskatı yana uzanır."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 26 * s)
    temas_golgesi(img, x, y, 30 * s)
    g = hex2(renk)
    d.ellipse([x - int(12 * s), y - int(8 * s), x + int(10 * s), y - 1], fill=g)
    d.polygon([(x + int(8 * s) * yon, y - int(6 * s)), (x + int(16 * s) * yon, y - int(4 * s)), (x + int(19 * s) * yon, y - 1),
               (x + int(9 * s) * yon, y - 1)], fill=g)
    for bx in (-8, -4, 3, 7):
        d.line([x + int(bx * s), y - int(5 * s), x + int((bx + 3) * s) * -yon + int(bx * s) * 0, y - int(1 * s)], fill=hex2(_ac(renk, -0.3)), width=max(1, int(1.4 * s)))
    d.line([x - int(12 * s) * yon, y - int(4 * s), x - int(17 * s) * yon, y - 1], fill=hex2("#1a0e08"), width=max(1, int(1.2 * s)))


def ok_ucusu(t, x0, y0, x1, y1, f, renk="#3a2418"):
    """Uçan ok: f 0-1 arasında (x0,y0)'dan (x1,y1)'e hafif yayla; yönüne bakar."""
    if not (0 <= f <= 1):
        return
    d = ImageDraw.Draw(t)
    x = x0 + (x1 - x0) * f
    y = y0 + (y1 - y0) * f - math.sin(f * math.pi) * 10
    dx, dy = (x1 - x0), (y1 - y0) - math.cos(f * math.pi) * 10 * math.pi
    n = math.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    d.line([x - ux * 9, y - uy * 9, x, y], fill=hex2(renk), width=1)
    piksel(t, x + ux, y + uy, hex2("#c8ccd0"))
    piksel(t, x - ux * 9, y - uy * 9 - 1, hex2("#f4f0e6"))
    piksel(t, x - ux * 8, y - uy * 8 + 1, hex2("#f4f0e6"))


def kalabalik(img, zemin, x0, x1, aralik, tohum, renkler, s=1.0, yon=1, bas="bork", adim=None):
    rnd = random.Random(tohum)
    for x in range(x0, x1, aralik):
        if rnd.random() < 0.85:
            kisi(img, x + rnd.randint(-2, 2), zemin, rnd.uniform(0.9, 1.1) * s, rnd.choice(renkler), bas,
                 rnd.choice(("#5a3a22", "#3a2a1a", "#7a5a3a")), yon=yon, adim=None if adim is None else (adim + rnd.random()) % 1,
                 kemer=None)


def ordugah(img, zemin, x0, x1, tohum, s=1.0, mesale=False):
    rnd = random.Random(tohum)
    for x in range(x0, x1, int(40 * s)):
        figur(img, yurt, x + rnd.randint(-5, 5), zemin, rnd.uniform(0.9, 1.2) * s, keçe="#c8bca8", golge="#9a8e7a",
              kapi="#6a2a1a", isik=mesale and rnd.random() < 0.6, kontur="#1a1008")


# ================================================================ BÖLÜM 1 · Topal Kurt


def sahne21():
    """Keş, Hoca Ilgar köyü, 8 Nisan 1336 şafağı: kerpiç evler, yurt; Taragay ve kucağında bebekle anne."""
    gokyuzu(21, ["#2a3a6a", "#5a5a8a", "#a87a8a", "#e8a07a", "#f8c890", "#fce0a8"], (420, 470, 20, ["#fff2c0", "#ffd890"]),
            [(110, 300, 40), (420, 340, 30)], ("#fff0e0", "#f0c0a8", "#c08a8a"))
    uzak(21, ["#6a6a9a", "#5a5a8a"], ["#7a8a7a", "#6a7a6a"], ["#9aa86a", "#8a9a5e", "#7a8c54"], dag_y=(300, 420), kenar="#f4e8f0")

    def koy(img, z):
        zemin = duz(588)
        koy_evleri(img, 20, 330, zemin, 1.6, tohum=21)
        koy_evleri(img, 500, 800, zemin, 1.6, tohum=22)
        figur(img, agac_kavak, 380, zemin, 1.6)
        figur(img, agac_kavak, 455, zemin, 1.4)

    orta(21, (520, 560), ["#8aa84a", "#7a9a40", "#6a8a38", "#5a7a30", "#4a6a2a"], "#c8d870", ekle=koy)
    on(21, ["#4a6a2a", "#6a8a38", "#8a7a3a"], "#e8e070")

    def kare(t, z, i):
        f = i / KARE
        baca = figur(t, yurt, 70, z, 3.4, isik=True)
        duman(t, baca[0], baca[1], 100, 21, faz=f, ruzgar=0.3, genislik=1.2)
        figur(t, kisi, 150, z, 2.6, "#3a4a7a", "bork", "#5a3a22", "#3a2418", yon=1, silah="sopa")  # Taragay
        figur(t, insan, 180, z, 2.5, "#9a2e3e", bebek=True, kadin=True, yon=-1)  # Tekina Hatun ve bebek
        figur(t, at, 255, z, 2.1, -1, "#c8a070", "#5a3a22", dur=True, bas=0.6 + 0.4 * math.sin(f * 2 * math.pi),
              kuyruk=math.sin(f * 4 * math.pi))

    sprite(21, "karakter", 300, 180, KARE, kare)


def agac_kavak(img, x, zemin, s=1.0):
    """İnce uzun kavak: dar sütun biçimli taç, gövde zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 4 * s)
    temas_golgesi(img, x, y, 10 * s)
    d.rectangle([x - max(1, int(s)), y - int(10 * s), x + max(1, int(s)), y - 1], fill=hex2("#5a4030"))
    d.ellipse([x - int(5 * s), y - int(46 * s), x + int(5 * s), y - int(8 * s)], fill=hex2("#4a7a34"))
    d.ellipse([x - int(4 * s), y - int(44 * s), x + int(1 * s), y - int(12 * s)], fill=hex2("#6a9a44"))


def sahne22():
    """Bozkırda yağma: genç Timur ve çetesi dörtnala, önlerinde kaçışan koyunlar (soldan sağa)."""
    gokyuzu(22, ["#4a7ab8", "#6a9ac8", "#9ab8d0", "#d8d0a8", "#f0d098"], (90, 470, 16, ["#fff2c0", "#ffe0a0"]),
            [(130, 300, 40), (400, 290, 34), (260, 345, 24)])
    uzak(22, ["#8a90a8", "#7a8098"], ["#a8a070", "#988f62"], ["#c8b070", "#b8a062", "#a89056"])
    orta(22, (530, 560), ["#b8a058", "#a89050", "#988048", "#887040", "#786038"], "#e0c878")
    on(22, ["#786038", "#988048", "#8a6a3a"], "#f0d888")

    def kare(t, z, i):
        f = i / KARE
        rnd = random.Random(22)
        for j in range(6):
            koyun_x = 290 + j * 22 + rnd.randint(-3, 3)
            figur(t, koyun, koyun_x, z, 2.2, 1, (f * 2 + rnd.random()) % 1, renk=rnd.choice(("#ece4d4", "#d8ccb4", "#c8b89a")), kos=True)
        for j, (x, renk, gv) in enumerate(((60, "#3a2418", "#5a4a3a"), (110, "#8a5a34", "#4a3a2a"), (210, "#2a1810", "#3a4a2a"))):
            figur(t, atli, x, z, 2.1, 1, (f + j * 0.33) % 1, renk, "#140a06", gv, "bork", "#3a2a1a", "#2a1a12",
                  silah="sopa" if j else "yay", adim=0.8)
        figur(t, atli, 160, z, 2.2, 1, (f + 0.5) % 1, "#6b3f24", "#140a06", "#7a1e22", "bork", "#5a3a22", None, silah="kilic", kol=0.6,
              adim=0.8)  # genç Timur

    sprite(22, "karakter", 420, 150, KARE, kare)


def sahne23():
    """1360: Tuğluk Timur'un Moğol ordusu Maveraünnehir'e iner; uzakta Keş, tuğlar ve sonsuz atlı kolu."""
    gokyuzu(23, ["#4a4a6a", "#6a6a80", "#9a9090", "#c8a888", "#d8b890"], None, [(100, 290, 44), (380, 320, 38)],
            ("#c8c0c0", "#a09898", "#787078"))
    uzak(23, ["#6a6a7a", "#5a5a6a"], ["#8a8060", "#7a7054"], ["#a89868", "#988a5e", "#887c54"])

    def sehir(img, z):
        zemin = duz(586)
        orta_asya_sehri(img, 480, 760, zemin, 1.4, tohum=23)
        rnd = random.Random(23)
        for x in range(20, 440, 26):  # uzak atlı kolu: ufukta toz içinde
            figur(img, atli, x + rnd.randint(-4, 4), zemin, 1.0, -1, 0.0, "#3a2418", "#140a06", "#4a3a3a", "bork", "#2a1a12", dur=True,
                  silah="mizrak", kontur="#1a1008")

    orta(23, (526, 560), ["#9a8a5a", "#8a7a50", "#7a6a48", "#6a5a40", "#5a4a38"], "#c8b880", ekle=sehir)
    on(23, ["#5a4a38", "#7a6a48", "#6a5a3a"], "#d8c890")

    def kare(t, z, i):
        f = i / KARE
        rnd = random.Random(5)
        for j, x in enumerate(range(30, 520, 54)):
            figur(t, atli, x + rnd.randint(-5, 5), z, 2.1, -1, (f + rnd.random()) % 1, rnd.choice(("#3a2418", "#5a3a24", "#2a1810", "#8a6a4a")),
                  "#140a06", rnd.choice(("#4a3a3a", "#3a3a4a", "#5a4a3a")), "kalpak", "#3a2a1a", "#2a1a12",
                  silah="mizrak" if j % 2 else None, bayrak="#c8302a" if j % 3 == 0 else None, adim=0.45)
        figur(t, tug, 300, z, 1.6, faz=f, flamalar=("#2a2a2a", "#c8302a", "#e0b040"))

    sprite(23, "karakter", 540, 160, KARE, kare)


def sahne24():
    """Düğün gecesi (y. 1362): Timur ile Olcay Türkan, yanlarında Emir Hüseyin; ateş, ışıklı yurtlar, misafirler."""
    gokyuzu(24, ["#0a0c22", "#1a1a3a", "#2e2448", "#4a2e4a", "#6a3a40"], (440, 240, 12, ["#f4ecd0", "#c8c0a8"]),
            [(140, 330, 30)], ("#4a3a5a", "#3a2e4a", "#2a2238"), yildiz=120)
    uzak(24, ["#2a2440", "#221e36"], ["#2e2a3a", "#262230"], ["#3a3428", "#322c22", "#2a2620"])

    def kamp(img, z):
        zemin = duz(588)
        ordugah(img, zemin, 20, 800, 24, 1.3, mesale=True)

    orta(24, (520, 560), ["#3a3a26", "#323220", "#2a2a1c", "#222216", "#1a1a12"], "#5a5a3a", ekle=kamp)
    on(24, ["#1a1a12", "#26261a", "#3a2e2a"], "#6a5a7a")

    def kare(t, z, i):
        f = i / KARE
        figur(t, yurt, 60, z, 3.0, keçe="#e8dcc0", golge="#a89878", kapi="#c8302a", isik=True, isik_gucu=0.8 + 0.2 * math.sin(f * 12))
        ates(t, 250, z, f, 1.4)
        rnd = random.Random(24)
        for j, x in enumerate((140, 175)):  # misafirler: çalgılı, alkışlayan
            figur(t, kisi, x, z, 2.4, rnd.choice(("#5a3a3a", "#3a4a5a")), "kalpak", "#3a2a1a", "#2a1a12", yon=1, kol=0.3 + 0.3 * math.sin(f * 12.56 + j))
        figur(t, timur, 300, z, 2.6, -1)
        figur(t, kisi, 325, z, 2.5, "#c8304a", "ortu", "#8a1a2a", kadin=True, yon=-1, kemer="#e0b040")  # Olcay Türkan
        figur(t, kisi, 365, z, 2.6, "#2a4a6a", "kalpak", "#4a3020", "#2a1a12", yon=-1)  # Emir Hüseyin
        for j, x in enumerate((395, 420)):
            figur(t, kisi, x, z, 2.4, ("#4a3a2a", "#6a2a3a")[j], "ortu" if j else "kalpak", ("#3a2a5a", "#3a2a1a")[j], kadin=bool(j), yon=-1,
                  kol=0.2 + 0.3 * math.sin(f * 12.56 + 2 + j))

    sprite(24, "karakter", 460, 170, KARE, kare)


def ates(t, x, z, f, s=1.0):
    """Kamp ateşi: zemine dizili taşlar, odunlar ve titreşen alev; kıvılcımlar yükselir."""
    d = ImageDraw.Draw(t)
    y = zemin_y(z, x, 14 * s)
    temas_golgesi(t, x, y, 18 * s)
    for dx in range(-7, 8, 3):
        d.ellipse([x + dx * s - 1.5 * s, y - 2.4 * s, x + dx * s + 1.5 * s, y - 1], fill=hex2("#6a6458"))
    d.line([x - 6 * s, y - 2 * s, x + 6 * s, y - 4 * s], fill=hex2("#4a2a16"), width=max(1, int(1.4 * s)))
    d.line([x - 6 * s, y - 4 * s, x + 6 * s, y - 2 * s], fill=hex2("#4a2a16"), width=max(1, int(1.4 * s)))
    for k, (r, renk) in enumerate(((6, "#e8601c"), (4.2, "#f8a030"), (2.4, "#fff0a0"))):
        for j in range(3):
            sal = math.sin(f * 2 * math.pi * 3 + j * 2 + k) * 1.2 * s
            cx = x + (j - 1) * r * 0.6 * s
            d.polygon([(cx - r * 0.5 * s, y - 3 * s), (cx + sal, y - 3 * s - r * (2.2 + 0.4 * math.sin(f * 6.28 * 2 + j)) * s),
                       (cx + r * 0.5 * s, y - 3 * s)], fill=hex2(renk))
    for j in range(5):
        u = (f * 2 + j / 5) % 1
        piksel(t, x + math.sin(j * 3 + u * 6) * 4 * s, y - 14 * s - u * 26 * s, hex2("#ffd070", int(255 * (1 - u))))
    for r in range(18, 34, 4):  # sıcak ışık halesi
        for a in range(0, 360, 12):
            px_, py_ = x + math.cos(math.radians(a)) * r * s, y - 8 * s + math.sin(math.radians(a)) * r * s * 0.6
            if py_ < y - 1 and _esik(int(px_), int(py_)) < 0.3:
                piksel(t, px_, py_, hex2("#f8a030", 40))


def sahne25():
    """Sistan, 1363-64: çölde pusu. Karşı tepedeki okçular atar; iki ok Timur'un sağ dizine ve eline saplanır, diz çöker."""
    gokyuzu(25, ["#c8a070", "#d8b080", "#e8c890", "#f0d8a0", "#f4e0b0"], (90, 300, 26, ["#fff8e0", "#ffe8b0"]),
            [(420, 360, 26)], ("#fff4e0", "#f0dcc0", "#d8b898"))
    uzak(25, ["#b8906a", "#a8805e"], ["#c8a070", "#b89062"], ["#d8b480", "#c8a472", "#b89464"], dag_y=(340, 420))
    orta(25, (528, 562), ["#d8b07a", "#c8a06e", "#b89062", "#a88056", "#98704c"], "#f0d098",
         ekle=lambda img, z: [figur(img, taslar, x, duz(588), 1.2) for x in (60, 700)])
    on(25, ["#98704c", "#b89062", "#a88056"], "#f0d8a0")

    def kare(t, z, i):
        f = i / KARE
        vuruldu = f >= 0.5
        figur(t, at, 70, z, 2.1, 1, "#6b3f24", "#2b1a12", eyer=True, dur=True, bas=0.2, kulak=math.sin(f * 20))
        if vuruldu:
            figur(t, timur, 150, z, 2.6, 1, diz=True)
            d = ImageDraw.Draw(t)
            yy = z[0]
            d.line([150 + 4, yy - 6, 150 + 14, yy - 12], fill=hex2("#3a2418"))  # dizdeki ok
            d.line([150 + 6, yy - 22, 150 + 15, yy - 27], fill=hex2("#3a2418"))  # eldeki ok
            for k in range(3):
                piksel(t, 150 + 4, yy - 5 + k, hex2("#a01818"))
                piksel(t, 150 + 6, yy - 21 + k, hex2("#a01818"))
        else:
            figur(t, timur, 150, z, 2.6, 1, adim=f * 2 % 1, silah="kilic")
        for j, x in enumerate((330, 365, 400)):  # okçular
            figur(t, kisi, x, z, 2.4, "#4a5a3a", "kalpak", "#3a2a1a", "#2a1a12", yon=-1, silah="yay", kol=0.4)
            ok_ucusu(t, x - 8, z[0] - 26, 160 + j * 3, z[0] - (8 if j % 2 else 24), ((f * 2) - j * 0.12) % 1 * 1.0 if f < 0.5 else -1)
            ok_ucusu(t, x - 8, z[0] - 26, 90 - j * 20, z[0] - 4, ((f - 0.5) * 2 - j * 0.15) if f >= 0.5 else -1)

    sprite(25, "karakter", 440, 160, KARE, kare)


def sahne26():
    """1365 Çamur Savaşı: sağanak, çamura saplanan atlar; keçe örtülü Moğollar sağdan saldırır."""
    gokyuzu(26, ["#1a1e26", "#262a34", "#363a44", "#4a4c52", "#5a5a5a"], None, [(120, 290, 48), (400, 300, 44), (270, 350, 30)],
            ("#4a4e58", "#3a3e48", "#2a2e38"))
    uzak(26, ["#3a3e48", "#32363e"], ["#3e4238", "#363a30"], ["#4a4638", "#423e30", "#3a362a"])
    orta(26, (528, 562), ["#5a4a36", "#4e402e", "#423628", "#382e22", "#2e261c"], "#7a6a52",
         ekle=lambda img, z: [ImageDraw.Draw(img).ellipse([x - 40, 590 + (x % 3) * 10, x + 40, 600 + (x % 3) * 10], fill=hex2("#6a7a8a", 120))
                              for x in range(60, 800, 130)])
    on(26, ["#2e261c", "#423628", "#3a3a3a"], "#7a8a9a")
    hava(26, "yagmur", 320, "#a8b8d0", 0.3)

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        for j, x in enumerate((40, 105, 165)):  # saplanan müttefik atlıları
            figur(t, atli, x, z, 2.1, 1, (f * 0.5 + j * 0.3) % 1, ("#6b3f24", "#3a2418", "#8a6a4a")[j], "#140a06",
                  ("#7a1e22", "#2a4a6a", "#4a3a2a")[j], ("sorguc", "kalpak", "bork")[j], "#2a1a14", "#a8522a" if j == 0 else None,
                  silah="kilic", kol=0.3 + 0.2 * math.sin(f * 12.56 + j), adim=0.15)
            d.ellipse([x - 26, z[0] - 7, x + 26, z[0] + 4], fill=hex2("#4a3a26"))  # çamur toynakları yutar
            for k in range(6):
                piksel(t, x - 20 + k * 8, z[0] - 7 - (k + i) % 2, hex2("#6a5a3e"))
        rnd = random.Random(26)
        for j, x in enumerate(range(270, 460, 48)):  # keçe örtülü Moğollar dörtnala
            figur(t, atli, x + rnd.randint(-4, 4), z, 2.1, -1, (f * 2 + rnd.random()) % 1, rnd.choice(("#2a1810", "#3a2418")), "#140a06",
                  "#5a5248", "kalpak", "#3a3428", "#2a1a12", silah="mizrak", adim=0.8)
            d.ellipse([x - 22, z[0] - 3, x + 22, z[0] + 4], fill=hex2("#4a3a26"))

    sprite(26, "karakter", 480, 160, KARE, kare)


def sahne27():
    """Semerkant, 1365: surlarda halk milisi Serbedarlar; dışarıda salgından ölen Moğol atları, çekilen ordu."""
    gokyuzu(27, ["#5a6a8a", "#7a88a0", "#a8a8a8", "#c8b8a0", "#d8c098"], None, [(130, 300, 40), (420, 330, 34)],
            ("#e8e0d8", "#c8c0b8", "#9a9090"))
    uzak(27, ["#7a8098", "#6a7088"], ["#8a9070", "#7a8064"], ["#a8a070", "#989062", "#888256"])

    def sehir(img, z):
        zemin = duz(588)
        orta_asya_sehri(img, 120, 700, zemin, 2.2, tohum=27)
        sur = 588 - int(16 * 2.2)
        zs = duz(sur)
        rnd = random.Random(27)
        for x in range(150, 680, 22):  # surda nöbetteki Serbedarlar (sur tepesine basar)
            figur(img, kisi, x + rnd.randint(-3, 3), zs, 1.3, rnd.choice(("#6a4a3a", "#4a4a5a", "#7a6a4a")), "takke",
                  rnd.choice(("#3a5a3a", "#7a2a2a")), "#2a1a12", silah=rnd.choice(("mizrak", "sopa", "yay")), kemer=None, kontur="#1a1008")

    orta(27, (526, 560), ["#8a8a52", "#7a7a48", "#6a6a40", "#5a5a38", "#4a4a30"], "#b8b878", ekle=sehir)
    on(27, ["#4a4a30", "#6a6a40", "#6a5a3a"], "#d8d890")

    def kare(t, z, i):
        f = i / KARE
        for x, yon in ((60, 1), (150, -1), (250, 1)):
            figur(t, yatan_at, x, z, 2.0, yon, ("#5a3a24", "#3a2418", "#8a6a4a")[x % 3])
        for j, x in enumerate((340, 395, 450)):  # çekilen Moğollar (sağa, uzaklaşır)
            figur(t, atli, x, z, 2.1, 1, (f + j * 0.3) % 1, ("#3a2418", "#2a1810", "#5a3a24")[j], "#140a06", "#5a5248", "kalpak",
                  "#3a3428", "#2a1a12", silah="mizrak", adim=0.5)
        rnd = random.Random(int(f * 3))
        for k in range(10):  # leşlerin üstünde sinekler
            piksel(t, 150 + rnd.randint(-120, 120), z[0] - 22 - rnd.randint(0, 14), hex2("#1a1008"))

    sprite(27, "karakter", 480, 140, KARE, kare)


def sahne28():
    """Belh, 1370 gecesi: kuşatılmış şehrin kapısından Emir Hüseyin, iki muhafız arasında, meşaleler altında çıkar."""
    gokyuzu(28, ["#06060f", "#140a18", "#2a0e1a", "#4a141a", "#7a2418"], (100, 250, 12, ["#f4dcc0", "#c8a890"]),
            [(380, 320, 34)], ("#4a2a2a", "#3a1e22", "#2a1218"), yildiz=90)
    uzak(28, ["#2a1a22", "#22141c"], ["#2a1e1a", "#221814"], ["#3a2a1e", "#32241a", "#2a1e16"])

    def sehir(img, z):
        zemin = duz(588)
        orta_asya_sehri(img, 380, 790, zemin, 2.0, tohum=28, kerpic="#7a5a48", golge="#5a4038", kubbe="#2a4a5a")
        ordugah(img, zemin, 10, 320, 28, 1.1, mesale=True)

    orta(28, (526, 560), ["#3a2a1e", "#32241a", "#2a1e16", "#221812", "#1a120e"], "#6a4a3a", ekle=sehir)
    on(28, ["#1a120e", "#2a1e16", "#3a1e1a"], "#8a4a3a")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 300, z, 2.6, "#5a2a2a", "migfer", "#8a8a90", "#2a1a12", yon=-1, adim=f, silah="mesale")
        figur(t, kisi, 270, z, 2.6, "#2a4a6a", "kalpak", "#4a3020", "#2a1a12", yon=-1, adim=(f + 0.5) % 1)  # Emir Hüseyin
        figur(t, kisi, 240, z, 2.6, "#5a2a2a", "migfer", "#8a8a90", "#2a1a12", yon=-1, adim=(f + 0.25) % 1, silah="mizrak")
        for x in (90, 140):
            figur(t, kisi, x, z, 2.5, "#3a2a2a", "migfer", "#7a7a80", "#2a1a12", yon=1, silah="mesale")

    sprite(28, "karakter", 400, 170, KARE, kare)


def sahne29():
    """Kurultay, 1370: tahtta kukla han Soyurgatmış; yanında Timur ve Cengiz soyundan Saray Mülk Hatun; emirler diz çöker."""
    gokyuzu(29, ["#3a6ab8", "#5a8ac8", "#8ab0d8", "#c8d8e0", "#f0e8c8"], (440, 300, 18, ["#fff8e0", "#fff0b0"]),
            [(120, 290, 36), (300, 330, 26)])
    uzak(29, ["#8a98b8", "#7a88a8"], ["#8aa080", "#7a9070"], ["#9ab07a", "#8aa46c", "#7a985e"])

    def otaglar(img, z):
        zemin = duz(588)
        for x, renk in ((60, "#2a5a9a"), (690, "#2a7a4a")):
            figur(img, otag, x, zemin, 1.6, renk, "#e0b040")
        kalabalik(img, zemin, 160, 640, 9, 29, ("#5a3a3a", "#3a4a5a", "#4a5a3a", "#7a6a4a"), 1.0, bas="kalpak")

    orta(29, (520, 557), ["#7aa84a", "#6a9a3e", "#5a8a36", "#4a7a2e", "#3f6b2a"], "#a8d063", ekle=otaglar)
    on(29, ["#3f6b2a", "#5a8f36", "#8a7a3a"], "#d8e070")

    def kare(t, z, i):
        f = i / KARE
        figur(t, otag, 200, z, 3.2, "#c8302a", "#e0b040", faz=f, acik=True)
        d = ImageDraw.Draw(t)
        y = z[0]
        d.rectangle([180, y - 10, 220, y - 1], fill=hex2("#7a4a2a"), outline=hex2("#2a1408"))  # taht kürsüsü zemine oturur
        d.rectangle([182, y - 12, 218, y - 10], fill=hex2("#c8a040"))
        figur(t, oturan, 200, duz(y - 12, 400), 2.6, "#e0b040", "tac", "#e0b040", "#3a2418", minder="#9a2a2a")  # Soyurgatmış
        figur(t, timur, 250, z, 2.7, -1)
        figur(t, kisi, 150, z, 2.5, "#e8d8f0", "tac", "#e0b040", kadin=True, yon=1)  # Saray Mülk Hatun
        for j, x in enumerate((300, 330, 360, 100, 70)):
            figur(t, kisi, x, z, 2.4, ("#3a4a5a", "#5a3a3a", "#4a5a3a", "#6a4a2a", "#2a3a5a")[j], "kalpak", "#3a2a1a", "#2a1a12",
                  yon=-1 if x > 200 else 1, diz=True)
        figur(t, tug, 385, z, 1.5, faz=f)

    sprite(29, "karakter", 400, 200, KARE, kare)


# ================================================================ BÖLÜM 2 · İki Yıldırım


def parsomen():
    """Mektup sahneleri için parşömen: kıvrık uçlar, lekeler, kırmızı balmumu mühür (430x380 ızgara)."""
    img = yeni(430, 380)
    d = ImageDraw.Draw(img)
    d.rectangle([20, 24, 410, 356], fill=hex2("#ecd9a8"))
    rnd = random.Random(7)
    for _ in range(900):
        x, y = rnd.randrange(22, 408), rnd.randrange(26, 354)
        piksel(img, x, y, hex2(rnd.choice(("#dcc48e", "#f4e4b8", "#d8bc84")), 200))
    for y0 in (14, 346):  # kıvrık üst ve alt rulolar
        d.rounded_rectangle([6, y0, 424, y0 + 22], radius=10, fill=hex2("#d8bc80"), outline=hex2("#7a5a2a"))
        d.line([12, y0 + 6, 418, y0 + 6], fill=hex2("#f4e2b4"))
    for x in (20, 410):
        d.line([x, 30, x, 350], fill=hex2("#b8985a"))
    d.ellipse([195, 300, 235, 340], fill=hex2("#9a1a14"), outline=hex2("#5a0a08"))
    d.ellipse([203, 308, 227, 332], outline=hex2("#c8302a"))
    kaydet(img, "parsomen.png")


def su_ve_kiyi(img, y0, renkler=("#2a5a8a", "#22507a", "#1a456a", "#143a5a"), kiyi_x=None, kum="#c8b080"):
    """Orta planda deniz: y0'dan aşağısı titreşimli su bantları ve dalga çizgileri; kiyi_x'e kadar kumsal."""
    d = ImageDraw.Draw(img)
    for y in range(y0, img.height):
        i = min(len(renkler) - 1, (y - y0) // 30)
        d.line([0, y, img.width, y], fill=hex2(renkler[i]))
    rnd = random.Random(y0)
    for _ in range(500):
        x, y = rnd.randrange(img.width), rnd.randrange(y0 + 2, img.height)
        for k in range(rnd.randint(3, 7)):
            piksel(img, x + k, y, hex2("#8ab8d8", 140))
    if kiyi_x:
        d.polygon([(0, y0 - 6), (kiyi_x, y0 - 6), (kiyi_x + 40, y0 + 30), (0, y0 + 30)], fill=hex2(kum))
        d.line([kiyi_x, y0 - 6, kiyi_x + 40, y0 + 30], fill=hex2("#f0f0e8"))


def tahtirevan(img, x, zemin, s=1.0, yon=1, faz=0.0):
    """Kafesli tahtırevan: önde ve arkada iki at, aralarındaki sırıklarda parmaklıklı bir oda taşınır."""
    at(img, x - int(24 * s) * yon, zemin, s, yon, "#4a3020", "#1a0e08", faz=faz, adim=0.4)
    at(img, x + int(22 * s) * yon, zemin, s, yon, "#6a4a30", "#1a0e08", faz=(faz + 0.5) % 1, adim=0.4)
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 10 * s)
    sy = y - int(17 * s) - int(math.sin(faz * 4 * math.pi) * 0.5 * s)
    d.line([x - int(30 * s), sy, x + int(30 * s), sy], fill=hex2("#5a3a22"), width=max(1, int(1.2 * s)))
    d.rectangle([x - int(9 * s), sy - int(16 * s), x + int(9 * s), sy + int(2 * s)], fill=hex2("#2a1a12"))
    kisi(img, x, duz(sy + int(2 * s), img.width), s * 0.85, "#2a6a3a", "sarik", "#f4f0e6", "#2a1a14", yon=yon)
    for k in range(-9, 10, 3):
        d.line([x + int(k * s), sy - int(16 * s), x + int(k * s), sy + int(2 * s)], fill=hex2("#8a8a90"), width=max(1, int(0.6 * s)))
    d.rectangle([x - int(10 * s), sy - int(19 * s), x + int(10 * s), sy - int(16 * s)], fill=hex2("#7a1e22"))


def sahne31():
    """Toktamış'a karşı (1391-1395): bozkırda iki ordu çarpışır; Timur'un atlıları soldan, Altın Orda sağdan."""
    gokyuzu(31, ["#5a6a8a", "#8a90a0", "#b8a890", "#d8b888", "#e8c890"], (450, 470, 18, ["#fff2c0", "#ffd890"]),
            [(120, 300, 44), (330, 330, 30)], ("#e8d8c8", "#c8b0a0", "#987a78"))
    uzak(31, ["#7a7a90", "#6a6a80"], ["#9a9070", "#8a8064"], ["#b8a870", "#a89a62", "#988c56"])

    def ordular(img, z):
        zemin = duz(588)
        rnd = random.Random(31)
        for x in range(10, 380, 18):
            figur(img, atli, x + rnd.randint(-3, 3), zemin, 1.0, 1, rnd.random(), "#3a2418", "#140a06", "#7a1e22", "kalpak", "#3a2a1a",
                  silah="mizrak", dur=True, kontur="#1a1008")
        for x in range(440, 800, 18):
            figur(img, atli, x + rnd.randint(-3, 3), zemin, 1.0, -1, rnd.random(), "#5a3a24", "#140a06", "#2a4a3a", "bork", "#e0b040",
                  silah="mizrak", dur=True, kontur="#1a1008")

    orta(31, (528, 560), ["#a89a5a", "#988a50", "#887a48", "#786a40", "#685a38"], "#d8c888", ekle=ordular)
    on(31, ["#685a38", "#887a48", "#7a6a3a"], "#e8d898")

    def kare(t, z, i):
        f = i / KARE
        rnd = random.Random(3)
        for j, x in enumerate((40, 95, 150, 205)):
            figur(t, atli, x, z, 2.1, 1, (f * 2 + j * 0.27) % 1, rnd.choice(("#3a2418", "#6b3f24", "#2a1810")), "#140a06",
                  "#7a1e22" if j == 2 else "#5a3a3a", "sorguc" if j == 2 else "kalpak", "#2a1a14", "#a8522a" if j == 2 else "#2a1a12",
                  silah="kilic", kol=0.5 + 0.5 * math.sin(f * 12.56 + j), adim=0.8)
        for j, x in enumerate((300, 355, 410, 465)):
            figur(t, atli, x, z, 2.1, -1, (f * 2 + j * 0.31) % 1, rnd.choice(("#5a3a24", "#8a6a4a", "#2a1810")), "#140a06", "#2a4a3a",
                  "bork", "#e0b040", "#2a1a12", silah="mizrak" if j % 2 else "kilic", kol=0.4 + 0.5 * math.sin(f * 12.56 + j + 1), adim=0.8)
        for j in range(4):
            ok_ucusu(t, 470 - j * 30, z[0] - 60, 120 - j * 20, z[0] - 30, (f * 1.5 + j * 0.25) % 1)
            ok_ucusu(t, 60 + j * 25, z[0] - 60, 400 + j * 20, z[0] - 30, (f * 1.5 + j * 0.25 + 0.5) % 1)

    sprite(31, "karakter", 520, 160, KARE, kare)


def sahne32():
    """İsfahan, 1387: isyan eden şehir yanıyor; kale önünde kafatası kuleleri, üstlerinde dönen kargalar."""
    gokyuzu(32, ["#1a0a10", "#3a1218", "#6a1a18", "#9a2a1a", "#c8481e", "#e87a30"], (400, 500, 30, ["#ffb060", "#e8601c"]),
            [(140, 300, 40), (420, 320, 34)], ("#4a1a18", "#3a1212", "#2a0e0e"), yildiz=20)
    uzak(32, ["#3a1a1a", "#301616"], ["#4a2a1e", "#40241a"], ["#5a3a26", "#503220", "#462a1c"])

    def sehir(img, z):
        zemin = duz(588)
        dam = orta_asya_sehri(img, 200, 760, zemin, 2.0, tohum=32, kerpic="#a8805a", golge="#7a5a40", kubbe="#2a6a9a")
        for k, (x, y) in enumerate(dam[::3]):
            duman(img, x, y, 70, 32 + k, faz=0.2 * k, renk="#3a2a2a", ruzgar=0.4, genislik=1.2)

    orta(32, (526, 560), ["#5a3a26", "#503220", "#462a1c", "#3a2418", "#2e1c12"], "#8a5a3a", ekle=sehir)
    on(32, ["#2e1c12", "#462a1c", "#3a1a12"], "#c86a3a")

    def kare(t, z, i):
        f = i / KARE
        for x, s in ((70, 2.4), (150, 2.8), (240, 2.5), (330, 2.9), (410, 2.3)):
            figur(t, kafa_kulesi, x, z, s)
        for j in range(6):  # kargalar daire çizer (havada uçan kuşlar)
            a = (f + j / 6) * 2 * math.pi
            cx, cy = 230 + math.cos(a) * 150, 40 + math.sin(a) * 20
            kanat = 2 if (i + j) % 6 < 3 else -1
            d = ImageDraw.Draw(t)
            d.line([cx - 4, cy - kanat, cx, cy, cx + 4, cy - kanat], fill=hex2("#120806"), width=2)
        figur(t, kisi, 480, z, 2.5, "#5a2a2a", "migfer", "#8a8a90", "#2a1a12", yon=-1, silah="mizrak")

    sprite(32, "karakter", 520, 170, KARE, kare)


def sahne33():
    """Delhi, Aralık 1398: Delhi sultanının savaş filleri hücum eder, Timur'un atlıları karşılar."""
    gokyuzu(33, ["#6a8ab8", "#8aa8c8", "#c8c8b0", "#e8d0a0", "#f0d898"], (90, 470, 18, ["#fff2c0", "#ffe0a0"]),
            [(140, 300, 40), (420, 330, 30)])
    uzak(33, ["#9a98a8", "#8a8898"], ["#a8a070", "#989062"], ["#c8b078", "#b8a06a", "#a8905e"])

    def sehir(img, z):
        zemin = duz(588)
        orta_asya_sehri(img, 380, 790, zemin, 1.8, tohum=33, kerpic="#c87a5a", golge="#9a5a40", kubbe="#f0e8d8")
        for x in (60, 140, 220, 300):
            figur(img, agac_kavak, x, zemin, 1.3)

    orta(33, (526, 560), ["#a8a05a", "#989050", "#888048", "#787040", "#686038"], "#d8d088", ekle=sehir)
    on(33, ["#686038", "#888048", "#7a6a3a"], "#e8e098")

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((60, 120, 180)):
            figur(t, atli, x, z, 2.1, 1, (f * 2 + j * 0.3) % 1, ("#3a2418", "#6b3f24", "#2a1810")[j], "#140a06",
                  "#7a1e22" if j == 1 else "#5a3a3a", "sorguc" if j == 1 else "kalpak", "#2a1a14", "#a8522a" if j == 1 else None,
                  silah="kilic" if j == 1 else "yay", kol=0.6, adim=0.8)
        for j, x in enumerate((310, 420)):
            figur(t, fil, x, z, 2.2, -1, (f + j * 0.5) % 1, ("#8a8a90", "#7a7a80")[j])
        for j in range(3):
            ok_ucusu(t, 120 + j * 30, z[0] - 50, 330 + j * 40, z[0] - 70, (f * 1.5 + j * 0.33) % 1)

    sprite(33, "karakter", 520, 200, KARE, kare)


def sahne34():
    """Mektup: Timur'un ulağı ordugâhtan batıya, Bayezid'e dörtnala yola çıkar."""
    gokyuzu(34, ["#4a6aa8", "#6a8ac0", "#a8b8c8", "#e0c8a0", "#f0c890"], (110, 470, 16, ["#fff2c0", "#ffd890"]),
            [(140, 300, 36), (420, 320, 30)])
    uzak(34, ["#8a90a8", "#7a8098"], ["#9aa078", "#8a906a"], ["#b0a870", "#a09862", "#908a56"])

    def kamp(img, z):
        zemin = duz(588)
        figur(img, otag, 650, zemin, 2.0, "#7a1e22", "#e0b040", acik=True)
        ordugah(img, zemin, 430, 600, 34, 1.2)
        figur(img, tug, 740, zemin, 1.0)

    orta(34, (526, 560), ["#9aa058", "#8a9050", "#7a8048", "#6a7040", "#5a6038"], "#c8d080", ekle=kamp)
    on(34, ["#5a6038", "#7a8048", "#7a6a3a"], "#d8e090")

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 150, z, 2.3, -1, f, "#2a1810", "#140a06", "#5a3a3a", "kalpak", "#3a2a1a", "#2a1a12", silah="mektup", kol=0.7,
              adim=0.85)

    sprite(34, "karakter", 260, 140, KARE, kare)


def sahne35():
    """Bayezid ordugâhında mektubu okur: yeşil Osmanlı otağı, yeniçeriler, sancak."""
    gokyuzu(35, ["#3a5a9a", "#5a7ab0", "#8aa0c0", "#c8c0b0", "#e8d0a8"], None, [(130, 300, 40), (420, 320, 30)])
    uzak(35, ["#7a8aa0", "#6a7a90"], ["#7a9068", "#6a805c"], ["#8aa060", "#7a9054", "#6a804a"])

    def kamp(img, z):
        zemin = duz(588)
        for x, renk in ((80, "#2a6a3a"), (220, "#c8302a"), (640, "#2a6a3a")):
            figur(img, otag, x, zemin, 1.6, renk, "#f0e8d8")
        kalabalik(img, zemin, 300, 600, 10, 35, ("#c8302a", "#2a5a8a", "#e8e0d0"), 1.0, bas="sarik")

    orta(35, (526, 560), ["#7a9a48", "#6a8a40", "#5a7a38", "#4a6a30", "#3a5a28"], "#a8c870", ekle=kamp)
    on(35, ["#3a5a28", "#5a7a38", "#6a6a3a"], "#c8d888")

    def kare(t, z, i):
        f = i / KARE
        figur(t, otag, 120, z, 3.0, "#2a6a3a", "#e0b040", faz=f, acik=True)
        figur(t, bayezid, 210, z, 2.8, -1, silah="mektup", kol=0.4)
        for x in (255, 290):
            figur(t, kisi, x, z, 2.5, "#c8302a", "sarik", "#f4f0e6", "#2a1a12", yon=-1, silah="mizrak")

    sprite(35, "karakter", 320, 190, KARE, kare)


def sahne36():
    """Sivas, Ağustos 1400: 18 gün kuşatma. Lağımcılar surun dibini kazar, destek kirişleri yakılır; mancınık atar."""
    gokyuzu(36, ["#5a6a8a", "#8a8a98", "#b8a090", "#d8a878", "#e8b880"], None, [(120, 300, 44), (420, 330, 30)],
            ("#d8c8c0", "#b0a098", "#807070"))
    uzak(36, ["#7a7a88", "#6a6a78"], ["#8a8468", "#7a765c"], ["#9a9068", "#8a845c", "#7a7852"])

    def kale(img, z):
        zemin = duz(588)
        anadolu_kalesi(img, 300, 790, zemin, 2.0)

    orta(36, (526, 560), ["#8a8a52", "#7a7a48", "#6a6a40", "#5a5a38", "#4a4a30"], "#b8b878", ekle=kale)
    on(36, ["#4a4a30", "#6a6a40", "#6a5a3a"], "#d8d890")

    def kare(t, z, i):
        f = i / KARE
        figur(t, mancinik, 70, z, 2.0, 1, f, tas_x=420)
        for j, x in enumerate((300, 340, 380)):  # lağımcılar kazar
            figur(t, kisi, x, z, 2.4, "#5a4a3a", "bork", "#5a3a22", None, yon=1, silah="kazma", kol=abs(math.sin((f + j * 0.3) * 2 * math.pi)))
        ates(t, 450, z, f, 1.2)  # lağımdaki destek kirişleri yanıyor
        duman(t, 450, z[0] - 20, 90, 36, faz=f, renk="#4a4040", ruzgar=0.3, genislik=1.4)
        figur(t, timur, 170, z, 2.6, 1, silah="kilic", kol=0.8)

    sprite(36, "karakter", 520, 200, KARE, kare)


def sahne37():
    """Sivas sonrası: 'kan dökülmeyecek' sözü. Savunucular açılan çukurlara diri diri gömülür; kürekçiler toprak atar."""
    gokyuzu(37, ["#140a12", "#2a1018", "#4a1418", "#7a2018", "#a83a1e"], (440, 520, 22, ["#ffa060", "#c8401c"]),
            [(150, 320, 36)], ("#3a1616", "#2a1010", "#1a0a0a"), yildiz=40)
    uzak(37, ["#2a1418", "#221014"], ["#3a2418", "#301e14"], ["#4a3020", "#40281a", "#362216"])

    def kale(img, z):
        zemin = duz(588)
        anadolu_kalesi(img, 420, 800, zemin, 1.6, tas="#6a5a52", golge="#4a3e38")

    orta(37, (526, 560), ["#4a3020", "#40281a", "#362216", "#2c1c12", "#22160e"], "#7a4a2e", ekle=kale)
    on(37, ["#22160e", "#362216", "#3a1a12"], "#a85a3a")

    def kare(t, z, i):
        f = i / KARE
        hendek(t, 150, 330, z, derin=12)
        d = ImageDraw.Draw(t)
        for j, x in enumerate(range(170, 320, 16)):  # çukurdaki tutsaklar: yalnızca omuz ve başları görünür
            by = z[0] + 3
            d.rectangle([x - 4, by - 8, x + 4, by], fill=hex2(("#4a3a2a", "#3a3a4a", "#5a2a2a")[j % 3]))
            d.ellipse([x - 3, by - 14, x + 3, by - 8], fill=hex2("#c8946e"))
        for j, x in enumerate((90, 365)):
            figur(t, kisi, x, z, 2.5, "#5a4a3a", "kalpak", "#3a2a1a", "#2a1a12", yon=1 if x < 200 else -1, silah="kurek",
                  kol=abs(math.sin((f + j * 0.5) * 2 * math.pi)) * 0.6)
            u = (f * 2 + j * 0.5) % 1  # küreklerden uçan toprak
            for k in range(6):
                piksel(t, x + (1 if x < 200 else -1) * (10 + u * 50 + k * 2), z[0] - 26 - math.sin(u * math.pi) * 22 + k, hex2("#5a3a22"))
        for x in (40, 420, 470):
            figur(t, kisi, x, z, 2.5, "#3a2a2a", "migfer", "#7a7a80", "#2a1a12", yon=1 if x < 200 else -1, silah="mizrak")

    sprite(37, "karakter", 520, 170, KARE, kare)


def sahne38():
    """Ankara, Temmuz 1402: Timur Çubuk Çayı'nı bentle keser; kuruyan dere yatağında susuz Osmanlı askerleri."""
    gokyuzu(38, ["#6a8ab8", "#9ab0c8", "#d8d0b0", "#f0d8a0", "#f8e0a8"], (270, 330, 26, ["#fffae0", "#fff0b0"]), [(430, 340, 22)])
    uzak(38, ["#a89a88", "#988a78"], ["#b8a070", "#a89062"], ["#c8a870", "#b89862", "#a88a56"])

    def bent(img, z):
        zemin = duz(588)
        dd = ImageDraw.Draw(img)
        dd.polygon([(500, 588), (560, 572), (800, 572), (800, 600), (500, 600)], fill=hex2("#3a6a9a"))  # bentin arkasında biriken su
        for x in range(480, 560, 8):
            figur(img, taslar, x, zemin, 0.9)
        for x in range(0, 480):  # kuruyan yatak: çatlak çamur şeridi
            yy = 600 + int(math.sin(x / 50) * 4)
            dd.line([x, yy - 4, x, yy + 4], fill=hex2("#a8865a"))
            if x % 9 == 0:
                dd.line([x, yy - 4, x + 4, yy + 4], fill=hex2("#6a4a2a"))

    orta(38, (526, 560), ["#b8a058", "#a89050", "#988048", "#887040", "#786038"], "#e0c878", ekle=bent)
    on(38, ["#786038", "#988048", "#8a6a3a"], "#f0d888")

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((60, 110, 170, 230)):
            figur(t, kisi, x, z, 2.5, ("#c8302a", "#2a5a8a", "#e8e0d0", "#c8302a")[j], "sarik", "#f4f0e6", "#2a1a12", yon=1,
                  diz=j % 2 == 0, adim=None if j % 2 == 0 else (f * 0.5 + j * 0.2) % 1, silah="testi" if j == 1 else None)
        figur(t, at, 300, z, 2.1, 1, "#8a6a4a", "#3a2418", dur=True, bas=0.9, kuyruk=math.sin(f * 6.28))
        rnd = random.Random(i)
        for k in range(14):  # sıcak hava titreşimi
            piksel(t, rnd.randrange(20, 360), z[0] - 30 - rnd.randrange(0, 50), hex2("#fff8e0", 80))

    sprite(38, "karakter", 380, 150, KARE, kare)


def sahne39():
    """Ankara Savaşı: Sırp zırhlı süvarisi Timurlu saflarına üç kez hücum eder; geride filler, toz ve oklar."""
    gokyuzu(39, ["#8a7a6a", "#a8907a", "#c8a880", "#d8b888", "#e0c090"], (100, 470, 22, ["#fff0c0", "#f8d090"]),
            [(380, 300, 44), (180, 330, 36)], ("#e8d0b8", "#c8a890", "#987868"))
    uzak(39, ["#9a8a7a", "#8a7a6a"], ["#a89070", "#988062"], ["#b89a68", "#a88a5c", "#987c52"])

    def arka(img, z):
        zemin = duz(588)
        rnd = random.Random(39)
        for x in range(430, 800, 50):
            figur(img, fil, x + rnd.randint(-5, 5), zemin, 0.9, -1, rnd.random(), kontur="#1a1008")
        for x in range(10, 400, 16):
            figur(img, kisi, x, zemin, 1.0, rnd.choice(("#c8302a", "#e8e0d0", "#2a5a8a")), "sarik", "#f4f0e6", silah="mizrak", kontur="#1a1008")

    orta(39, (526, 560), ["#a88a58", "#987a50", "#886a48", "#785a40", "#684a38"], "#d8b880", ekle=arka)
    on(39, ["#684a38", "#886a48", "#7a5a3a"], "#e8c890")

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((60, 125, 190)):  # Sırp şövalyeleri sağa hücum
            figur(t, atli, x, z, 2.3, 1, (f * 2 + j * 0.3) % 1, ("#d8d8d8", "#3a2418", "#8a8a8a")[j], "#2a2a2a", "#5a5a6a", "sovalye", "#a8acb0",
                  silah="mizrak", zirh="#a8acb0", cul=("#c8302a", "#f0f0f0", "#c8302a")[j], bayrak="#f0f0f0", adim=0.85)
        for j, x in enumerate((320, 380, 440)):  # Timurlu atlılar karşılar
            figur(t, atli, x, z, 2.1, -1, (f * 2 + j * 0.37) % 1, ("#3a2418", "#6b3f24", "#2a1810")[j], "#140a06", "#5a3a3a", "kalpak", "#3a2a1a",
                  "#2a1a12", silah="kilic", kol=0.4 + 0.5 * math.sin(f * 12.56 + j), adim=0.8)
        rnd = random.Random(i // 2)
        for k in range(40):  # toz bulutu
            x, y = 250 + rnd.randint(-60, 60), z[0] - rnd.randint(2, 30)
            piksel(t, x, y, hex2("#d8b888", 120))

    sprite(39, "karakter", 520, 170, KARE, kare)


def sahne40():
    """Bayezid dağlarda kuşatılır: birkaç yüz atlıyla kaçmıştı; çevresini Timur'un atlıları sarar, esir düşer."""
    gokyuzu(40, ["#2a2a4a", "#4a3a5a", "#7a4a5a", "#a8604a", "#c8784a"], (420, 520, 20, ["#ffc080", "#f08040"]),
            [(140, 300, 36)], ("#8a5a5a", "#6a4248", "#4a2a3a"), yildiz=30)
    uzak(40, ["#3a3048", "#30283e"], ["#4a3a3a", "#403232"], ["#5a4632", "#503e2c", "#463626"], dag_y=(240, 420))

    def dag(img, z):
        _ = z
        for x in range(0, 810, 30):
            figur(img, cam, x, duz(588), random.Random(x).uniform(1.4, 2.2), renk="#2a3a2a", isik="#3a4a3a", kontur="#101810")

    orta(40, (526, 560), ["#5a4a32", "#4e402c", "#423626", "#382e20", "#2e261a"], "#8a6a4a", ekle=dag)
    on(40, ["#2e261a", "#423626", "#3a2a2a"], "#a87a5a")

    def kare(t, z, i):
        f = i / KARE
        figur(t, bayezid, 260, z, 2.8, 1, kol=0.5 + 0.2 * math.sin(f * 6.28), silah="kilic")
        for j, (x, yon) in enumerate(((80, 1), (150, 1), (370, -1), (440, -1))):
            figur(t, atli, x, z, 2.1, yon, (f + j * 0.25) % 1, ("#3a2418", "#6b3f24", "#2a1810", "#5a3a24")[j], "#140a06", "#5a3a3a", "kalpak",
                  "#3a2a1a", "#2a1a12", silah="mizrak", dur=True, adim=0.2)
        figur(t, yatan_at, 205, z, 2.0, -1, "#d8d8d8")  # Bayezid'in düşen atı (doğrulanmadı: yalnızca 'atsız kaldı')

    sprite(40, "karakter", 520, 170, KARE, kare)


def sahne41():
    """Ziyafet: Timur'un otağı önünde esir Bayezid; rivayete göre Despina Hatun şarap sunar."""
    gokyuzu(41, ["#0a0c22", "#1a1a3a", "#2e2448", "#4a2e4a", "#6a3a40"], (100, 240, 12, ["#f4ecd0", "#c8c0a8"]),
            [(400, 320, 30)], ("#4a3a5a", "#3a2e4a", "#2a2238"), yildiz=120)
    uzak(41, ["#2a2440", "#221e36"], ["#2e2a3a", "#262230"], ["#3a3428", "#322c22", "#2a2620"])

    def kamp(img, z):
        zemin = duz(588)
        ordugah(img, zemin, 20, 800, 41, 1.2, mesale=True)

    orta(41, (520, 560), ["#3a3a26", "#323220", "#2a2a1c", "#222216", "#1a1a12"], "#5a5a3a", ekle=kamp)
    on(41, ["#1a1a12", "#26261a", "#3a2e2a"], "#6a5a7a")

    def kare(t, z, i):
        f = i / KARE
        figur(t, otag, 260, z, 3.4, "#7a1e22", "#e0b040", faz=f, acik=True)
        d = ImageDraw.Draw(t)
        d.rectangle([150, z[0] - 4, 370, z[0] - 1], fill=hex2("#8a2a2a"))  # yere serili halı
        for k in range(150, 370, 6):
            piksel(t, k, z[0] - 3, hex2("#e0b040"))
        figur(t, oturan, 200, duz(z[0] - 4, 520), 2.6, "#7a1e22", "sorguc", "#2a1a14", "#d8d0c8", yon=1, el="kase", minder="#c8a040")
        figur(t, oturan, 330, duz(z[0] - 4, 520), 2.6, "#2a6a3a", "sarik", "#f4f0e6", "#2a1a14", yon=-1)
        figur(t, kisi, 262, duz(z[0] - 4, 520), 2.5, "#3a3a7a", "ortu", "#c8a040", kadin=True, yon=1, silah="testi", adim=None)
        ates(t, 450, z, f, 1.0)
        for x in (110, 410):
            figur(t, kisi, x, z, 2.5, "#5a2a2a", "migfer", "#8a8a90", "#2a1a12", yon=1 if x < 200 else -1, silah="mesale")

    sprite(41, "karakter", 520, 200, KARE, kare)


def sahne42():
    """İzmir, Aralık 1402: Rodos Şövalyeleri'nin liman kalesi. Mancınıklar döver, liman ağzı taşla dolar, gemiler döner."""
    gokyuzu(42, ["#4a5a7a", "#6a7a90", "#9aa0a8", "#c8c0b0", "#d8c8a8"], None, [(120, 290, 44), (420, 320, 36)],
            ("#d8d8d8", "#b0b0b8", "#808090"))
    uzak(42, ["#6a7a90", "#5a6a80"], ["#7a8a7a", "#6a7a6a"], ["#4a6a8a", "#42607e", "#3a5672"])

    def liman(img, z):
        zemin = duz(588)
        su_ve_kiyi(img, 596, kiyi_x=560)
        anadolu_kalesi(img, 330, 540, zemin, 1.7, tas="#b0a898", golge="#807868")
        figur(img, taslar, 600, duz(600), 2.0)  # liman ağzına dökülen taşlar
        figur(img, taslar, 630, duz(604), 1.8)

    orta(42, (526, 560), ["#8a9a6a", "#7a8a5e", "#6a7a52", "#5a6a48", "#4a5a3e"], "#b8c890", ekle=liman)
    on(42, ["#2a4a6a", "#3a5a7a", "#4a5a6a"], "#a8c8e0")

    def kare(t, z, i):
        f = i / KARE
        su = z[0] - 8
        d = ImageDraw.Draw(t)
        d.rectangle([250, su, 520, z[0] - 1], fill=hex2("#2a5a8a"))  # deniz şeridi (sprite tabanında)
        for k in range(250, 520, 7):
            piksel(t, k + (i % 7), su, hex2("#8ab8d8"))
        for j, x in enumerate((330, 440)):
            gemi(t, x, su + 2, 2.2, -1, (f + j * 0.4) % 1)
        figur(t, mancinik, 70, z, 2.0, 1, f, tas_x=300)
        figur(t, timur, 160, z, 2.6, 1, silah="kilic", kol=0.6)
        for j, x in enumerate((200, 230)):
            figur(t, kisi, x, z, 2.4, "#5a4a3a", "bork", "#5a3a22", None, yon=1, silah="kurek", kol=abs(math.sin((f + j * 0.5) * 6.28)) * 0.6)

    sprite(42, "karakter", 520, 200, KARE, kare)


def sahne43():
    """Kafes efsanesi ve gerçeği: iki at arasında kafesli tahtırevan; Bayezid Akşehir'e götürülür (8 Mart 1403)."""
    gokyuzu(43, ["#5a6070", "#7a7c88", "#9a9aa0", "#b8b4b0", "#c8c0b8"], None, [(130, 290, 44), (400, 320, 40)],
            ("#c8c8cc", "#a8a8b0", "#808088"))
    uzak(43, ["#6a6e7a", "#5e626e"], ["#7a7a6a", "#6e6e5e"], ["#8a8670", "#7e7a64", "#726e58"])

    def kasaba(img, z):
        zemin = duz(588)
        koy_evleri(img, 420, 800, zemin, 1.5, tohum=43, kerpic="#b8a890")
        for x in (60, 160, 260):
            figur(img, cam, x, zemin, 1.6, renk="#3a4a3a", isik="#4a5a4a", kontur="#141a14")

    orta(43, (526, 560), ["#7a7a58", "#6e6e4e", "#626246", "#56563e", "#4a4a36"], "#a8a880", ekle=kasaba)
    on(43, ["#4a4a36", "#626246", "#5a5a4a"], "#c8c8a8")

    def kare(t, z, i):
        f = i / KARE
        figur(t, tahtirevan, 260, z, 2.1, 1, f)
        for x, ff in ((90, 0.0), (430, 0.5)):
            figur(t, atli, x, z, 2.1, 1, (f + ff) % 1, "#3a2418", "#140a06", "#5a3a3a", "kalpak", "#3a2a1a", "#2a1a12", silah="mizrak", adim=0.4)

    sprite(43, "karakter", 520, 170, KARE, kare)


# ================================================================ BÖLÜM 3 · Lanetli Mezar


def ic_mekan(no, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a", pencere=None, zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060"):
    """İç mekân katmanları: gokyuzu = duvar, uzak = dikişsiz kemer dizisi ve çini kuşak (pencere: kemer içinde
    gece/kar), orta = taş döşeme (düz zemin), on = boş."""
    g = yeni()
    from ciz import gradyan
    gradyan(g, list(duvar))
    kaydet(g, f"sahne{no}-gokyuzu.png")
    u = yeni()
    d = ImageDraw.Draw(u)
    d.rectangle([0, 200, W, 600], fill=hex2(duvar[1]))
    for x in range(0, W, 90):  # 6 kemer: 540'a tam bölünür, dikişsiz
        d.rectangle([x + 18, 330, x + 72, 600], fill=hex2(kemer))
        d.chord([x + 18, 300, x + 72, 360], 180, 360, fill=hex2(kemer))
        if pencere:
            d.rectangle([x + 26, 340, x + 64, 440], fill=hex2(pencere[0]))
            d.chord([x + 26, 316, x + 64, 360], 180, 360, fill=hex2(pencere[0]))
            rnd = random.Random(x)
            for _ in range(30):
                piksel(u, x + rnd.randint(27, 63), rnd.randint(322, 438), hex2(pencere[1]))
            d.line([x + 45, 318, x + 45, 440], fill=hex2(kemer), width=2)
            d.line([x + 26, 390, x + 64, 390], fill=hex2(kemer), width=2)
    d.rectangle([0, 250, W, 270], fill=hex2(cini))
    for x in range(0, W, 6):
        piksel(u, x, 260, hex2("#f4ecd8"))
        piksel(u, x + 3, 256, hex2(_ac(cini, 0.3)))
    d.rectangle([0, 586, W, 600], fill=hex2(_ac(duvar[1], -0.3)))
    kaydet(u, f"sahne{no}-uzak.png")
    o = yeni(GW, H)
    d = ImageDraw.Draw(o)
    for y in range(596, H):
        i = min(len(zemin_renk) - 1, (y - 596) // 60)
        d.line([0, y, GW, y], fill=hex2(zemin_renk[i]))
    for y in range(600, H, 24):  # taş döşeme derzleri (perspektif için aşağı indikçe seyrek)
        d.line([0, y, GW, y], fill=hex2(_ac(zemin_renk[0], -0.25)))
        kay = (y // 24) % 2 * 20
        for x in range(kay, GW, 40):
            d.line([x, y, x, y + 24], fill=hex2(_ac(zemin_renk[0], -0.25)))
    for r in range(60, 200, 20):  # sıcak ışık halkası
        for a in range(0, 360, 4):
            px_, py_ = 405 + math.cos(math.radians(a)) * r * 2, 640 + math.sin(math.radians(a)) * r * 0.4
            if _esik(int(px_), int(py_)) < 0.25 * (1 - r / 200):
                piksel(o, px_, py_, hex2(isik, 50))
    kaydet(o, f"sahne{no}-orta.png")
    kaydet(yeni(GW, H), f"sahne{no}-on.png")


def kar_ortusu(no, kenar="#f4f8ff"):
    """Kar: orta planın üst kenarına kar biriktirir (dosyayı yeniden işler)."""
    from PIL import Image
    yol = Path(__file__).parents[1] / "public" / f"sahne{no}-orta.png"
    img = Image.open(yol).convert("RGBA")
    px = img.load()
    for x in range(img.width):
        for y in range(img.height):
            if px[x, y][3] > 200:
                for k in range(4):
                    if y + k < img.height:
                        px[x, y + k] = hex2(kenar if k < 2 else "#d8e0ec")
                break
    img.save(yol)


def tas_arabasi(img, x, zemin, s=1.0, yon=1, faz=0.0):
    """Fil çekişli taş arabası: iki tekerlek zemine basar, üstünde kesme mermer blok."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 24 * s)
    temas_golgesi(img, x, y, 28 * s)
    r = int(6 * s)
    d.rectangle([x - int(12 * s), y - 2 * r - int(3 * s), x + int(12 * s), y - 2 * r], fill=hex2("#6a4a2a"), outline=hex2("#2a1408"))
    d.rectangle([x - int(9 * s), y - 2 * r - int(13 * s), x + int(9 * s), y - 2 * r - int(3 * s)], fill=hex2("#d8d4c8"), outline=hex2("#7a766c"))
    d.line([x - int(9 * s), y - 2 * r - int(8 * s), x + int(9 * s), y - 2 * r - int(8 * s)], fill=hex2("#b8b4a8"))
    for cx in (x - int(7 * s), x + int(7 * s)):
        d.ellipse([cx - r, y - 2 * r, cx + r, y - 1], outline=hex2("#3a2418"), width=max(1, int(1.2 * s)))
        a = -faz * 2 * math.pi * yon
        d.line([cx + math.cos(a) * r, y - r + math.sin(a) * r, cx - math.cos(a) * r, y - r - math.sin(a) * r], fill=hex2("#5a3a22"))
    d.line([x + int(12 * s) * yon, y - 2 * r - int(1 * s), x + int(22 * s) * yon, y - 2 * r - int(5 * s)], fill=hex2("#5a3a22"), width=max(1, int(s)))


def tabut(img, x, zemin, s=1.0, acik=True):
    """Açılmış mezar sandığı: yere oturur; içinde iskelet (sağ bacak kemiği eğri: aksaklık)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 30 * s)
    temas_golgesi(img, x, y, 34 * s)
    d.rectangle([x - int(16 * s), y - int(8 * s), x + int(16 * s), y - 1], fill=hex2("#2a1a12"), outline=hex2("#0a0604"))
    d.rectangle([x - int(15 * s), y - int(7 * s), x + int(15 * s), y - int(5 * s)], fill=hex2("#120a06"))
    if acik:
        k = hex2("#e8e0c8")
        d.ellipse([x - int(14 * s), y - int(9 * s), x - int(10 * s), y - int(5.5 * s)], fill=k)  # kafatası
        d.line([x - int(10 * s), y - int(7 * s), x + int(2 * s), y - int(7 * s)], fill=k, width=max(1, int(s)))  # omurga
        for i in range(4):
            d.line([x - int((8 - i * 2.4) * s), y - int(8.5 * s), x - int((8 - i * 2.4) * s), y - int(5.6 * s)], fill=k)  # kaburga
        d.line([x + int(2 * s), y - int(7.4 * s), x + int(13 * s), y - int(8 * s)], fill=k, width=max(1, int(0.8 * s)))  # sol bacak
        d.line([x + int(2 * s), y - int(6.4 * s), x + int(8 * s), y - int(6 * s), x + int(12 * s), y - int(6.8 * s)], fill=k,
               width=max(1, int(0.8 * s)))  # sağ bacak: dizden kırık
        piksel(img, x + int(8 * s), y - int(6 * s), hex2("#a87a5a"))
        d.rectangle([x - int(19 * s), y - int(5 * s), x - int(17 * s) + int(1 * s), y - 1], fill=hex2("#1e5a3a"))  # kenara konmuş yeşim taşı ucu
    else:
        d.rectangle([x - int(17 * s), y - int(10 * s), x + int(17 * s), y - int(7 * s)], fill=hex2("#1e5a3a"), outline=hex2("#0a2a1a"))


def lamba(img, x, zemin, s=1.0, faz=0.0):
    """Ayaklı kazı lambası: üç ayak zemine basar, ampul titrer ve çevresini aydınlatır."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 8 * s)
    temas_golgesi(img, x, y, 10 * s)
    for dx in (-4, 0, 4):
        d.line([x, y - int(18 * s), x + int(dx * s), y - 1], fill=hex2("#3a3a3a"))
    d.ellipse([x - int(2.2 * s), y - int(22 * s), x + int(2.2 * s), y - int(18 * s)], fill=hex2("#fff8c0"))
    g = 0.8 + 0.2 * math.sin(faz * 2 * math.pi * 3)
    for r in range(4, 22, 2):
        for a in range(0, 360, 10):
            px_, py_ = x + math.cos(math.radians(a)) * r * s, y - 20 * s + math.sin(math.radians(a)) * r * s
            if py_ < y - 1 and _esik(int(px_), int(py_)) < 0.4 * g * (1 - r / 22):
                piksel(img, px_, py_, hex2("#fff0a0", 70))


def sahne51():
    """Semerkant dolayı: 'Bağdat', 'Dımaşk', 'Şiraz', 'Mısır' adlı köyler; sürgün ustalar deve kervanıyla gelir."""
    gokyuzu(51, ["#3a7ac8", "#5a98d8", "#8ab8e0", "#c8d8d8", "#f0e0b8"], (460, 300, 18, ["#fff8e0", "#fff0b0"]),
            [(120, 300, 38), (330, 335, 26)])
    uzak(51, ["#8a98b8", "#7a88a8"], ["#9aa878", "#8a986a"], ["#a8b070", "#98a062", "#889256"])

    def sehir(img, z):
        zemin = duz(588)
        orta_asya_sehri(img, 460, 800, zemin, 2.0, tohum=51, kubbe="#2a8ac8")
        koy_evleri(img, 10, 180, zemin, 1.5, tohum=51)
        koy_evleri(img, 230, 420, zemin, 1.5, tohum=52)
        for x in (200, 440):
            figur(img, agac_kavak, x, zemin, 1.5)

    orta(51, (526, 560), ["#8aa84a", "#7a9a40", "#6a8a38", "#5a7a30", "#4a6a2a"], "#c8d870", ekle=sehir)
    on(51, ["#4a6a2a", "#6a8a38", "#8a7a3a"], "#e8e070")

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((60, 150, 240)):
            figur(t, deve, x, z, 2.2, 1, (f + j * 0.33) % 1, yuk=("#8a3a2a", "#2a5a8a", "#c8a040")[j])
        for j, x in enumerate((100, 195, 290, 330)):
            figur(t, kisi, x, z, 2.4, ("#5a4a3a", "#3a4a5a", "#6a3a3a", "#4a5a3a")[j], ("takke", "sarik", "kalpak", "takke")[j],
                  ("#2a5a3a", "#f0e8d8", "#3a2a1a", "#7a2a2a")[j], "#3a2a1a", yon=1, adim=(f + j * 0.27) % 1,
                  silah=("kazma", None, "kurek", None)[j])

    sprite(51, "karakter", 380, 180, KARE, kare)


def sahne52():
    """Bibi Hanım Camii şantiyesi: filler mermer blok çeker, iskelede ustalar; Timur kapıyı alçak bulur, kubbeden tuğla düşer."""
    gokyuzu(52, ["#4a8ac8", "#6aa0d8", "#9ac0e0", "#d0d8d0", "#f0e0b8"], (90, 300, 16, ["#fff8e0", "#fff0b0"]),
            [(380, 300, 34)])
    uzak(52, ["#8a98b8", "#7a88a8"], ["#a8a078", "#98906a"], ["#c8b078", "#b8a06a", "#a8905e"])

    def cami(img, z):
        figur(img, bibi_hanim, 470, duz(588), 2.1, catlak=1.0)

    orta(52, (530, 560), ["#c8b078", "#b8a06a", "#a8905e", "#988052", "#887046"], "#e8d098", ekle=cami)
    on(52, ["#887046", "#a8905e", "#8a7a4a"], "#f0e0a8")

    def kare(t, z, i):
        f = i / KARE
        figur(t, fil, 80, z, 2.0, 1, f, kule=False, binici="#5a3a3a")
        figur(t, tas_arabasi, 160, z, 2.0, 1, f)
        figur(t, timur, 270, z, 2.7, 1, silah="sopa", kol=0.7)
        for j, x in enumerate((340, 380)):
            figur(t, kisi, x, z, 2.4, "#5a4a3a", "takke", "#2a5a3a", "#3a2a1a", yon=-1, diz=True)
        u = (f * 1.5) % 1  # düşen tuğlalar
        for k in range(3):
            bx, by = 440 + k * 14, 10 + (u * 1.0 + k * 0.2) % 1 * (z[0] - 20)
            ImageDraw.Draw(t).rectangle([bx, by, bx + 5, by + 3], fill=hex2("#c88a5a"), outline=hex2("#5a3a22"))

    sprite(52, "karakter", 480, 200, KARE, kare)


def sahne53():
    """Kânigil şöleni, Eylül 1404: ipek otağlar, at eti çevrilen ateş, müzisyenler; Kastilyalı elçiler gelir."""
    gokyuzu(53, ["#4a7ab8", "#6a98c8", "#a0b8d0", "#e0d8c0", "#f8e0a8"], (440, 470, 18, ["#fff2c0", "#ffd890"]),
            [(130, 300, 34), (330, 335, 24)])
    uzak(53, ["#8a98b8", "#7a88a8"], ["#8aa080", "#7a9070"], ["#9ab07a", "#8aa46c", "#7a985e"])

    def otaglar(img, z):
        zemin = duz(588)
        for x, renk in ((40, "#c8302a"), (130, "#2a6a9a"), (220, "#e0b040"), (560, "#7a2a8a"), (650, "#2a8a5a"), (740, "#c8302a")):
            figur(img, otag, x, zemin, 1.5, renk, "#f4ecd8")

    orta(53, (520, 557), ["#7aa84a", "#6a9a3e", "#5a8a36", "#4a7a2e", "#3f6b2a"], "#a8d063", ekle=otaglar)
    on(53, ["#3f6b2a", "#5a8f36", "#8a7a3a"], "#d8e070")

    def kare(t, z, i):
        f = i / KARE
        ates(t, 120, z, f, 1.4)
        d = ImageDraw.Draw(t)
        d.line([92, z[0] - 26, 148, z[0] - 26], fill=hex2("#4a2a16"), width=2)  # şiş
        for yx in (94, 146):
            d.line([yx, z[0] - 1, yx, z[0] - 28], fill=hex2("#4a2a16"), width=2)  # çatal direkler zemine dikili
        d.ellipse([104, z[0] - 32, 136, z[0] - 20], fill=hex2("#8a3a1a"))
        for j, x in enumerate((180, 215)):
            figur(t, oturan, x, z, 2.4, ("#2a5a8a", "#7a2a5a")[j], "kalpak", "#3a2a1a", "#2a1a12", yon=1, el="kase", minder="#c8a040")
        figur(t, oturan, 255, z, 2.6, "#7a1e22", "sorguc", "#2a1a14", "#d8d0c8", yon=1, el="kase", minder="#9a2a2a")
        for j, x in enumerate((330, 365, 395)):  # Kastilyalı elçiler yaklaşır
            figur(t, kisi, x, z, 2.5, ("#1a1a2a", "#3a1a1a", "#1a1a2a")[j], "sapka", "#1a1a1a", "#3a2a1a", yon=-1, adim=(f + j * 0.33) % 1,
                  kemer=None, pelerin="#5a1a1a")
        figur(t, kisi, 40, z, 2.4, "#5a3a6a", "takke", "#2a5a3a", "#2a1a12", yon=1, silah="yay", kol=0.4 + 0.2 * math.sin(f * 25))

    sprite(53, "karakter", 420, 190, KARE, kare)


def sahne54():
    """Yakın plan: otağın içinde yaşlı Timur; göz kapakları düşmüş, sakalı ağarmış."""
    ic_mekan(54, ("#5a1a1a", "#7a2222", "#8a2a2a"), kemer="#4a1212", cini="#c8a040", zemin_renk=("#7a2a2a", "#6a2222", "#5a1c1c"))

    def kare(t, z, i):
        f = i / KARE
        figur(t, oturan, 130, z, 5.6, "#7a1e22", "sorguc", "#2a1a14", "#e0dcd4", yon=1, minder="#c8a040")
        d = ImageDraw.Draw(t)
        gy = z[0] - int(1.6 * 5.6) - int(9.5 * 5.6) - int(2.6 * 5.6)
        kapak = 1 if (i % 24) < 3 else 0  # ağır göz kırpışı; göz kapağı zaten yarı düşük
        d.line([130 + 3, gy - 2, 130 + 9, gy - 2 + kapak], fill=hex2("#a8704a"), width=2)
        for x in (40, 230):
            figur(t, kisi, x, z, 2.8, "#5a2a2a", "migfer", "#8a8a90", "#2a1a12", yon=1 if x < 130 else -1, silah="mizrak")
        for k in range(8):  # buhurdan dumanı
            u = (f + k / 8) % 1
            piksel(t, 200 + math.sin(u * 8) * 4, z[0] - 30 - u * 60, hex2("#d8d0c8", int(160 * (1 - u))))

    sprite(54, "karakter", 270, 160, KARE, kare)


def sahne55():
    """Kasım 1404 sonu: ordu karlar içinde doğuya, Çin'e yürür; develer, atlılar, tuğ; kar savrulur."""
    gokyuzu(55, ["#5a6478", "#7a8496", "#9aa2b0", "#b8bec8", "#d0d4dc"], None, [(130, 290, 44), (400, 320, 40)],
            ("#e0e4ec", "#c8ccd8", "#a0a4b4"))
    uzak(55, ["#c8d0dc", "#b8c0cc"], ["#d8dce4", "#c8ccd8"], ["#e8ecf0", "#dce0e8", "#d0d4dc"], kenar="#ffffff")
    orta(55, (526, 560), ["#e8ecf2", "#dce0e8", "#d0d4de", "#c4c8d4", "#b8bcc8"], "#ffffff")
    on(55, ["#b8bcc8", "#d0d4de", "#a8acb8"], "#ffffff")
    hava(55, "kar", 360, "#ffffff")

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((40, 140)):
            figur(t, deve, x, z, 2.2, 1, (f + j * 0.4) % 1, renk="#a07a4a", yuk="#5a3a2a")
        for j, x in enumerate((90, 200, 250, 320)):
            figur(t, atli, x, z, 2.1, 1, (f + j * 0.29) % 1, ("#3a2418", "#6b3f24", "#2a1810", "#5a3a24")[j], "#140a06",
                  "#7a1e22" if j == 1 else "#4a4a5a", "sorguc" if j == 1 else "kalpak", "#2a1a14", "#d8d0c8" if j == 1 else None,
                  silah="mizrak" if j != 1 else None, adim=0.45)
        figur(t, tug, 370, z, 1.6, faz=f)

    sprite(55, "karakter", 420, 170, KARE, kare)


def sahne56():
    """Otrar, Şubat 1405: ateşler içinde yatan Timur; hekimler buzla serinletmeye çalışır; pencerelerde kar."""
    ic_mekan(56, ("#1a1a2a", "#2a2634", "#342e3c"), kemer="#120e18", cini="#2a5a8a", pencere=("#1a2a4a", "#f4f8ff"),
             zemin_renk=("#3a3030", "#302828", "#262020"))

    def kare(t, z, i):
        f = i / KARE
        figur(t, yatan, 190, z, 3.0, nefes=0.5 + 0.5 * math.sin(f * 2 * math.pi))
        for j, x in enumerate((100, 290)):
            figur(t, kisi, x, z, 2.6, ("#e8e0d0", "#3a4a5a")[j], "sarik", "#f4f0e6", "#d8d0c8", yon=1 if x < 190 else -1, diz=True)
        d = ImageDraw.Draw(t)
        d.chord([118, z[0] - 10, 142, z[0] + 4], 180, 360, fill=hex2("#c8c0b0"))  # buz dolu leğen
        for k in range(4):
            d.rectangle([122 + k * 5, z[0] - 9, 125 + k * 5, z[0] - 6], fill=hex2("#e0f0ff"))
        mum_x = 340
        d.rectangle([mum_x - 2, z[0] - 14, mum_x + 2, z[0] - 1], fill=hex2("#f0e8d0"))
        alev = 2 + math.sin(f * 30) * 0.8
        d.polygon([(mum_x - 2, z[0] - 14), (mum_x, z[0] - 14 - alev * 3), (mum_x + 2, z[0] - 14)], fill=hex2("#f8c040"))

    sprite(56, "karakter", 380, 140, KARE, kare)


def sahne57():
    """Abanoz tabut misk ve gülsuyuyla, karla kapalı geçitlerden Semerkant'a döner."""
    gokyuzu(57, ["#3a4458", "#5a6478", "#7a8496", "#9aa2b0", "#b0b6c4"], None, [(140, 300, 40), (420, 320, 36)],
            ("#c8ccd8", "#a8acb8", "#8a8e9a"))
    uzak(57, ["#a8b0c0", "#98a0b0"], ["#c0c8d4", "#b0b8c4"], ["#d8dce4", "#ccd0d8", "#c0c4cc"], dag_y=(230, 420), kenar="#ffffff")

    def orman(img, z):
        for x in range(0, 810, 28):
            figur(img, cam, x, duz(588), random.Random(x).uniform(1.3, 2.0), renk="#2a3a3a", isik="#e8f0f8", kontur="#101818")

    orta(57, (526, 560), ["#dce0e8", "#d0d4de", "#c4c8d4", "#b8bcc8", "#acb0bc"], "#ffffff", ekle=orman)
    on(57, ["#acb0bc", "#c4c8d4", "#9a9eaa"], "#ffffff")
    hava(57, "kar", 300, "#ffffff")

    def kare(t, z, i):
        f = i / KARE
        from ciz import kagni
        figur(t, okuz_, 110, z, 2.1, 1, f)
        figur(t, kagni, 190, z, 2.4, 1, f, yuk="#1a1210")
        for j, x in enumerate((260, 300, 340)):
            figur(t, kisi, x, z, 2.4, ("#2a2420", "#d8d0c0", "#3a2a2a")[j], "kalpak", "#2a2a2a", "#2a1a12", yon=1, adim=(f + j * 0.3) % 1)
        figur(t, atli, 40, z, 2.1, 1, f, "#2a1810", "#140a06", "#2a2a2a", "kalpak", "#1a1a1a", silah="mizrak", bayrak="#f4f0e6", adim=0.4)

    sprite(57, "karakter", 400, 160, KARE, kare)


def okuz_(img, x, zemin, s=1.0, yon=1, faz=0.0):
    from ciz import okuz
    okuz(img, x, zemin, s, yon, "#4a3628", faz)


def sahne58():
    """Semerkant: Gür-i Emir'in mavi kubbesi. Timur, torunu için yaptırdığı türbeye gömülür."""
    gokyuzu(58, ["#5a6a88", "#7a88a0", "#a0a8b8", "#c8c8d0", "#d8d4d8"], None, [(130, 290, 36), (420, 320, 30)],
            ("#e8e8ec", "#c8c8d0", "#a0a0b0"))
    uzak(58, ["#8a98b0", "#7a88a0"], ["#a8b0b8", "#98a0a8"], ["#c8ccd4", "#bcc0c8", "#b0b4bc"])

    def turbe(img, z):
        zemin = duz(588)
        gur_i_emir(img, 405, zemin, 2.6)
        koy_evleri(img, 10, 250, zemin, 1.4, tohum=58, kerpic="#c8b898")
        koy_evleri(img, 560, 800, zemin, 1.4, tohum=59, kerpic="#c8b898")

    orta(58, (526, 560), ["#c8ccd4", "#bcc0c8", "#b0b4bc", "#a4a8b0", "#989ca4"], "#f4f8ff", ekle=turbe)
    kar_ortusu(58)
    on(58, ["#989ca4", "#b0b4bc", "#8a8e98"], "#ffffff")
    hava(58, "kar", 160, "#ffffff")

    def kare(t, z, i):
        f = i / KARE
        rnd = random.Random(58)
        for j, x in enumerate(range(30, 520, 34)):
            if abs(x - 270) > 50:
                figur(t, kisi, x, z, 2.3, rnd.choice(("#2a2420", "#d8d0c0", "#3a2a2a")), rnd.choice(("sarik", "kalpak", "ortu")),
                      rnd.choice(("#f4f0e6", "#2a2a2a")), None, yon=1 if x < 270 else -1, kadin=j % 3 == 0)

    sprite(58, "karakter", 520, 150, KARE, kare)


def sahne59():
    """Koyu yeşil yeşim taşı: 1740'ta Nadir Şah'ın askerleri taşı götürmek ister, taş çatlar."""
    ic_mekan(59, ("#0e1a1a", "#162424", "#1e2e2e"), kemer="#081010", cini="#1e5a6a", zemin_renk=("#2a3030", "#222828", "#1a2020"),
             isik="#80e0a0")

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        y = z[0]
        temas_golgesi(t, 200, y, 90)
        d.rectangle([150, y - 22, 250, y - 1], fill=hex2("#1e5a3a"), outline=hex2("#0a2a1a"))
        d.polygon([(150, y - 22), (160, y - 30), (260, y - 30), (250, y - 22)], fill=hex2("#2e7a4e"))
        d.polygon([(250, y - 22), (260, y - 30), (260, y - 9), (250, y - 1)], fill=hex2("#14422a"))
        for k in range(150, 250, 7):
            piksel(t, k + 3, y - 12, hex2("#4aa070"))
        catlak = min(1.0, f * 1.6)
        for k in range(int(22 * catlak)):  # çatlak yukarıdan aşağı ilerler
            piksel(t, 200 + int(math.sin(k * 0.8) * 3), y - 29 + k, hex2("#06140c"))
            piksel(t, 201 + int(math.sin(k * 0.8) * 3), y - 29 + k, hex2("#06140c"))
        for x, yon in ((110, 1), (290, -1)):
            figur(t, kisi, x, z, 2.6, "#7a2a2a", "kalpak", "#c8302a", "#2a1a12", yon=yon, kol=0.3, silah="sopa")
        figur(t, kisi, 340, z, 2.7, "#2a3a6a", "tac", "#e0b040", "#2a1a12", yon=-1, pelerin="#c8a040")  # Nadir Şah

    sprite(59, "karakter", 400, 170, KARE, kare)


def sahne60():
    """Haziran 1941: Gerasimov'un ekibi lambalar altında mezarı açar; kameraman çeker; iskelette aksak sağ bacak."""
    ic_mekan(60, ("#141414", "#1e1c1a", "#282420"), kemer="#0e0c0a", cini="#1e4a6a", zemin_renk=("#3a342c", "#302a24", "#26221c"),
             isik="#fff0a0")

    def kare(t, z, i):
        f = i / KARE
        figur(t, tabut, 220, z, 2.6, True)
        figur(t, lamba, 120, z, 2.0, f)
        figur(t, lamba, 330, z, 2.0, (f + 0.4) % 1)
        figur(t, kisi, 175, z, 2.6, "#5a5a4a", "kasket", "#3a3a32", "#5a4a3a", yon=1, diz=True)  # Gerasimov
        figur(t, kisi, 275, z, 2.6, "#e8e4dc", None, None, None, yon=-1, kol=0.2, kemer=None)
        figur(t, kisi, 380, z, 2.6, "#3a3a2a", "kasket", "#4a4a3a", None, yon=-1, silah="kamera")  # Kayumov

    sprite(60, "karakter", 460, 160, KARE, kare)


def sahne61():
    """Çayhane: tahta sedirde oturan yaşlılar kameraman Kayumov'u uyarır: 'Mezarı açarsanız savaş çıkar.'"""
    gokyuzu(61, ["#e0a060", "#e8b878", "#f0c890", "#f4d8a8", "#f8e4c0"], (420, 420, 22, ["#fff4d0", "#ffe0a0"]), [(130, 330, 30)])
    uzak(61, ["#c8a080", "#b89070"], ["#c8b080", "#b8a070"], ["#d8c090", "#c8b082", "#b8a074"])

    def mahalle(img, z):
        zemin = duz(588)
        koy_evleri(img, 10, 800, zemin, 1.8, tohum=61, kerpic="#d8b888")

    orta(61, (528, 560), ["#c8a878", "#b8986c", "#a88860", "#987854", "#886848"], "#e8d0a0", ekle=mahalle)
    on(61, ["#886848", "#a88860", "#8a7a4a"], "#f0e0b0")

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        y = z[0]
        for ax in (90, 170, 250, 330):  # sedirin dört ayağı zemine basar
            d.rectangle([ax - 2, y - 14, ax + 2, y - 1], fill=hex2("#5a3a22"))
        d.rectangle([84, y - 18, 336, y - 14], fill=hex2("#7a4a2a"), outline=hex2("#2a1408"))
        d.rectangle([86, y - 20, 334, y - 18], fill=hex2("#9a2a2a"))
        ust = duz(y - 20, 420)
        for j, x in enumerate((120, 180, 300)):
            figur(t, oturan, x, ust, 2.4, ("#2a3a5a", "#5a3a2a", "#3a5a4a")[j], "takke", ("#1a1a1a", "#2a5a3a", "#7a2a2a")[j], "#e8e4dc",
                  yon=1 if x < 240 else -1, el="kase" if j != 1 else None)
        d.rectangle([230, y - 30, 246, y - 20], fill=hex2("#c8a040"), outline=hex2("#5a3a12"))  # semaver
        d.rectangle([236, y - 34, 240, y - 30], fill=hex2("#c8a040"))
        for k in range(6):
            u = (f + k / 6) % 1
            piksel(t, 238 + math.sin(u * 7) * 3, y - 36 - u * 26, hex2("#f0f0f0", int(180 * (1 - u))))
        figur(t, kisi, 390, z, 2.6, "#3a3a2a", "kasket", "#4a4a3a", None, yon=-1, silah="kamera")

    sprite(61, "karakter", 420, 160, KARE, kare)


def sahne62():
    """22 Haziran 1941 şafağı: Alman tankları sınırı geçer; ufukta patlamalar."""
    gokyuzu(62, ["#2a2a3a", "#4a3a4a", "#7a4a4a", "#b86a4a", "#e8a060"], (430, 510, 18, ["#ffd090", "#f08040"]),
            [(140, 300, 40), (400, 320, 36)], ("#8a5a5a", "#6a4248", "#4a2a3a"))
    uzak(62, ["#4a4050", "#40384a"], ["#5a5a40", "#505036"], ["#6a7a40", "#5e6e38", "#526230"])

    def koyler(img, z):
        zemin = duz(588)
        koy_evleri(img, 500, 800, zemin, 1.4, tohum=62, kerpic="#a89880")
        for k, x in enumerate((560, 700)):
            duman(img, x, 570, 120, 62 + k, faz=0.3 * k, renk="#3a3434", ruzgar=0.5, genislik=1.6)

    orta(62, (526, 560), ["#6a8a40", "#5e7e38", "#527230", "#46662a", "#3a5a24"], "#a0b870", ekle=koyler)
    on(62, ["#3a5a24", "#527230", "#5a5a3a"], "#c0c888")

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((80, 230, 380)):
            figur(t, tank, x, z, 2.6, 1, (f * 2 + j * 0.3) % 1)
            for k in range(5):  # egzoz ve toz
                u = (f * 2 + k / 5 + j * 0.2) % 1
                piksel(t, x - 50 - u * 30, z[0] - 6 - u * 14, hex2("#8a7a6a", int(180 * (1 - u))))

    sprite(62, "karakter", 480, 120, KARE, kare)


def sahne63():
    """Kasım 1942: Timur İslami törenle yeniden gömülür; omuzlarda tabut, imam dua eder, Gür-i Emir karlar altında."""
    gokyuzu(63, ["#4a5468", "#6a7488", "#8a94a8", "#b0b8c4", "#c8ccd4"], None, [(140, 300, 36), (420, 330, 30)],
            ("#e0e4ec", "#c0c4d0", "#9aa0b0"))
    uzak(63, ["#8a98b0", "#7a88a0"], ["#a8b0b8", "#98a0a8"], ["#c8ccd4", "#bcc0c8", "#b0b4bc"])

    def turbe(img, z):
        gur_i_emir(img, 405, duz(588), 2.4)

    orta(63, (526, 560), ["#c8ccd4", "#bcc0c8", "#b0b4bc", "#a4a8b0", "#989ca4"], "#f4f8ff", ekle=turbe)
    kar_ortusu(63)
    on(63, ["#989ca4", "#b0b4bc", "#8a8e98"], "#ffffff")
    hava(63, "kar", 140, "#ffffff")

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        xs = (190, 215, 240, 265)
        for j, x in enumerate(xs):
            figur(t, kisi, x, z, 2.4, ("#2a2a3a", "#3a2a2a", "#2a3a2a", "#3a3a3a")[j], "takke", "#1a1a1a", "#3a2a1a", yon=1, adim=(f + j * 0.25) % 1)
        omuz = z[0] - int(11 * 2.4) - 2
        d.rectangle([180, omuz - 7, 275, omuz], fill=hex2("#2a6a3a"), outline=hex2("#0a2a12"))  # yeşil örtülü tabut
        for k in range(182, 274, 6):
            piksel(t, k, omuz - 4, hex2("#e0b040"))
        figur(t, kisi, 330, z, 2.6, "#e8e4dc", "sarik", "#f4f0e6", "#e8e4dc", yon=-1, kol=0.6)
        for x in (60, 100, 400, 440):
            figur(t, kisi, x, z, 2.3, "#3a3a4a", "kasket", "#3a3a3a", None, yon=1 if x < 200 else -1)

    sprite(63, "karakter", 500, 160, KARE, kare)


def sahne64():
    """Taşkent bugün: Marx heykelinin yerinde atlı Emir Timur; 'Güç adalettedir'."""
    gokyuzu(64, ["#3a7ac8", "#5a98d8", "#8ab8e0", "#c8d8e0", "#e8e8d8"], (440, 300, 18, ["#fff8e0", "#fff0b0"]),
            [(120, 300, 34), (300, 340, 24)])
    uzak(64, ["#8a98b8", "#7a88a8"], ["#7a9a78", "#6a8a6a"], ["#8aa070", "#7a9062", "#6a8256"])

    def meydan(img, z):
        zemin = duz(588)
        for x in range(10, 800, 34):
            figur(img, agac_kavak, x, zemin, 1.3 + (x % 3) * 0.1)

    orta(64, (526, 560), ["#7aa04a", "#6a9040", "#5a8038", "#4a7030", "#3a602a"], "#a8c870", ekle=meydan)
    on(64, ["#3a602a", "#5a8038", "#6a6a3a"], "#c8d888")

    def kare(t, z, i):
        f = i / KARE
        figur(t, heykel, 200, z, 3.4)
        for j, x in enumerate((60, 330, 380)):
            figur(t, kisi, x, z, 2.4, ("#3a5a8a", "#8a3a3a", "#e8e0d0")[j], None if j else "kasket", "#3a3a3a", None,
                  yon=1 if x < 200 else -1, adim=(f + j * 0.3) % 1 if j == 2 else None, kemer=None)
        for k in range(4):  # güvercinler
            u = (f + k / 4) % 1
            piksel(t, 120 + u * 200, 30 + math.sin(u * 12 + k) * 6 + k * 8, hex2("#e8e8f0"))

    sprite(64, "karakter", 420, 200, KARE, kare)


if __name__ == "__main__":
    secim = [int(a) for a in sys.argv[1:] if a.isdigit()] or [n for n in range(21, 70) if f"sahne{n}" in globals()]
    if "parsomen" in sys.argv:
        parsomen()
    for n in secim:
        globals()[f"sahne{n}"]()
        print(f"sahne {n} tamam", flush=True)
