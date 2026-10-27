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


def hava(no, tur="yagmur", yogunluk=260, renk="#b8c8e0", egim=0.25, simsek=()):
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
        if i in simsek:  # şimşek: gökte zikzak çizgi ve bütün kareye soluk beyaz parlama
            d = ImageDraw.Draw(t)
            rs = random.Random(i)
            px_, py_ = rs.randint(120, 420), 120
            yol = [(px_, py_)]
            while py_ < 380:
                px_ += rs.randint(-14, 14)
                py_ += rs.randint(14, 26)
                yol.append((px_, py_))
            d.line(yol, fill=hex2("#ffffff"), width=3)
            d.line(yol, fill=hex2("#c8d8ff"), width=1)
            for yy in range(0, H, 2):
                d.line([0, yy, W, yy], fill=hex2("#e8f0ff", 28))

    sayfa = sprite_sayfasi(W, H, KARE, kare)
    kaydet(sayfa, f"sahne{no}-hava.png")


def yatan_at(img, x, zemin, s=1.0, yon=1, renk="#5a3a24", nefes=0.0):
    """Hasta ya da ölü at: yan yatmış gövde zemine değer, boyun ve baş yerde uzanır, dört bacak
    dizden kırık yana uzanır; nefes 0-1 karnı hafifçe kabartır (hasta at)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 34 * s)
    temas_golgesi(img, x, y, 40 * s)
    g = hex2(renk)
    k = hex2(_ac(renk, -0.3))
    a = hex2(_ac(renk, 0.2))
    kab = int(nefes * 0.8 * s)
    d.ellipse([x - int(12 * s), y - int(10 * s) - kab, x + int(9 * s), y - 1], fill=g)  # gövde
    d.line([x - int(9 * s), y - int(9 * s) - kab, x + int(6 * s), y - int(9 * s) - kab], fill=a)
    # boyun ve baş: gövdenin önünden yere doğru uzanır
    bx = x + int(8 * s) * yon
    d.polygon([(bx, y - int(8 * s)), (bx + int(8 * s) * yon, y - int(5 * s)), (bx + int(8 * s) * yon, y - 1), (bx, y - 2)], fill=g)
    hx = bx + int(8 * s) * yon
    d.polygon([(hx, y - int(5.5 * s)), (hx + int(7 * s) * yon, y - int(3 * s)), (hx + int(7 * s) * yon, y - 1), (hx, y - 1)], fill=g)
    d.line([hx + int(1 * s) * yon, y - int(5.5 * s), hx - int(1 * s) * yon, y - int(8 * s)], fill=g, width=max(1, int(s)))  # kulak
    d.line([hx + int(2.5 * s) * yon, y - int(3.6 * s), hx + int(3.5 * s) * yon, y - int(3.6 * s)], fill=hex2("#120806"))  # kapalı göz
    piksel(img, hx + int(6.5 * s) * yon, y - int(2 * s), k)  # burun
    d.line([bx - int(1 * s) * yon, y - int(9 * s), hx, y - int(5.5 * s)], fill=hex2("#1a0e08"), width=max(1, int(1.2 * s)))  # yele
    # bacaklar: karından öne doğru, dizden kırık
    for i, ax in enumerate((-8, -4, 1, 5)):
        ux, uy = x + int(ax * s), y - int(3 * s)
        dx_, dy_ = ux + int(5 * s) * yon, y - int(2 * s) - (i % 2) * int(2 * s)
        ex_, ey_ = dx_ + int(6 * s) * yon, y - 1 - (i % 2) * int(1 * s)
        d.line([ux, uy, dx_, dy_], fill=k if i % 2 else g, width=max(1, int(1.6 * s)))
        d.line([dx_, dy_, ex_, ey_], fill=k if i % 2 else g, width=max(1, int(1.2 * s)))
        d.rectangle([ex_ - max(1, int(s * 0.6)), ey_ - max(1, int(s * 0.6)), ex_ + max(1, int(s * 0.6)), ey_], fill=hex2("#1a0e08"))
    for i in range(int(10 * s)):  # kuyruk yere serilir
        piksel(img, x - int(12 * s) * yon - i * yon, y - int(4 * s) + i * 0.35, hex2("#1a0e08"))
        piksel(img, x - int(12 * s) * yon - i * yon, y - int(3 * s) + i * 0.35, hex2("#1a0e08"))


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
    d.line([x - ux * 16, y - uy * 16, x, y], fill=hex2(renk), width=2)
    d.line([x, y, x + ux * 3, y + uy * 3], fill=hex2("#d8dce0"), width=2)
    for k in (14, 15, 16):
        piksel(t, x - ux * k, y - uy * k - 2, hex2("#f4f0e6"))
        piksel(t, x - ux * k, y - uy * k + 2, hex2("#f4f0e6"))


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
    """Keş, Hoca Ilgar köyü, 8 Nisan 1336 şafağı: arkada kerpiç evler, önde yurt; baba Taragay, yerde sallanan beşikte bebek Timur, anne Tekina Hatun, otlayan at."""
    gokyuzu(21, ["#2a3a6a", "#5a5a8a", "#a87a8a", "#e8a07a", "#f8c890", "#fce0a8"], (420, 470, 20, ["#fff2c0", "#ffd890"]),
            [(110, 300, 40), (420, 340, 30)], ("#fff0e0", "#f0c0a8", "#c08a8a"))
    uzak(21, ["#6a6a9a", "#5a5a8a"], ["#7a8a7a", "#6a7a6a"], ["#9aa86a", "#8a9a5e", "#7a8c54"], dag_y=(300, 420), kenar="#f4e8f0")

    def koy(img, z):
        zemin = duz(588)
        koy_evleri(img, 20, 330, zemin, 2.4, tohum=21)
        koy_evleri(img, 500, 800, zemin, 2.4, tohum=22)
        figur(img, agac_kavak, 380, zemin, 1.6)
        figur(img, agac_kavak, 455, zemin, 1.4)

    orta(21, (520, 560), ["#8aa84a", "#7a9a40", "#6a8a38", "#5a7a30", "#4a6a2a"], "#c8d870", ekle=koy)
    on(21, ["#4a6a2a", "#6a8a38", "#8a7a3a"], "#e8e070")

    def kare(t, z, i):
        f = i / KARE
        baca = figur(t, yurt, 70, z, 3.4, isik=True)
        duman(t, baca[0], baca[1], 100, 21, faz=f, ruzgar=0.3, genislik=1.2)
        figur(t, kisi, 150, z, 2.6, "#3a4a7a", "bork", "#5a3a22", "#3a2418", yon=1, silah="sopa")  # Taragay
        figur(t, insan, 205, z, 2.5, "#9a2e3e", kadin=True, yon=-1)  # Tekina Hatun
        figur(t, besik, 178, z, 2.4, math.sin(f * 2 * math.pi) * 0.12)  # yerdeki beşikte bebek Timur
        figur(t, at, 262, z, 3.0, -1, "#c8a070", "#5a3a22", dur=True, bas=0.6 + 0.4 * math.sin(f * 2 * math.pi),
              kuyruk=math.sin(f * 4 * math.pi))

    sprite(21, "karakter", 300, 180, KARE, kare)


def besik(img, x, zemin, s=1.0, sallanma=0.0):
    """Ahşap beşik: kavisli iki kızak zemine değer, sallanırken hep bir noktası yerde kalır; içinde kundaklı bebek."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 14 * s)
    temas_golgesi(img, x, y, 14 * s)
    dx = int(sallanma * 6 * s)
    d.arc([x - int(8 * s) + dx, y - int(6 * s), x + int(8 * s) + dx, y + int(2 * s) - 1], 20, 160, fill=hex2("#5a3a22"), width=max(1, int(1.2 * s)))
    ky = y - int(3 * s)
    d.rectangle([x - int(6 * s) + dx, ky - int(5 * s), x + int(6 * s) + dx, ky], fill=hex2("#8a5a32"), outline=hex2("#3a2410"))
    d.ellipse([x - int(4 * s) + dx, ky - int(7 * s), x + int(4 * s) + dx, ky - int(3 * s)], fill=hex2("#efe4cc"), outline=hex2("#3a2410"))
    d.ellipse([x + int(1 * s) + dx, ky - int(7 * s), x + int(4 * s) + dx, ky - int(4.4 * s)], fill=hex2("#e0b090"))
    d.line([x - int(6 * s) + dx, ky - int(5 * s), x - int(6 * s) + dx, ky - int(9 * s)], fill=hex2("#5a3a22"), width=max(1, int(s)))
    d.line([x + int(6 * s) + dx, ky - int(5 * s), x + int(6 * s) + dx, ky - int(9 * s)], fill=hex2("#5a3a22"), width=max(1, int(s)))
    d.line([x - int(6 * s) + dx, ky - int(9 * s), x + int(6 * s) + dx, ky - int(9 * s)], fill=hex2("#c8302a"), width=max(1, int(0.8 * s)))


def agac_kavak(img, x, zemin, s=1.0):
    """İnce uzun kavak: dar sütun biçimli taç, gövde zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 4 * s)
    temas_golgesi(img, x, y, 10 * s)
    d.rectangle([x - max(1, int(s)), y - int(10 * s), x + max(1, int(s)), y - 1], fill=hex2("#5a4030"))
    for dx in range(-int(5 * s), int(5 * s) + 1, 2):  # dipte çimen tutamları gövdeyi zemine bağlar
        for k in range(1 + (dx * 7) % 3):
            piksel(img, x + dx, y - 1 - k, hex2("#3a6a2a"))
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
    """1360: Tuğluk Timur'un Moğolları Keş surlarının önünde. Amca Hacı Barlas dörtnala kaçar, Timur yürüyüp istilacının karşısına çıkar."""
    gokyuzu(23, ["#4a4a6a", "#6a6a80", "#9a9090", "#c8a888", "#d8b890"], None, [(100, 290, 44), (380, 320, 38)],
            ("#c8c0c0", "#a09898", "#787078"))
    uzak(23, ["#6a6a7a", "#5a5a6a"], ["#8a8060", "#7a7054"], ["#a89868", "#988a5e", "#887c54"])

    def sehir(img, z):
        zemin = duz(588)
        orta_asya_sehri(img, 230, 600, zemin, 3.2, tohum=23)

    orta(23, (526, 560), ["#9a8a5a", "#8a7a50", "#7a6a48", "#6a5a40", "#5a4a38"], "#c8b880", ekle=sehir)
    on(23, ["#5a4a38", "#7a6a48", "#6a5a3a"], "#d8c890")

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((340, 405, 470)):  # Moğol atlıları durmuş, sola bakar
            figur(t, atli, x, z, 2.9, -1, (f + j * 0.3) % 1, ("#3a2418", "#5a3a24", "#2a1810")[j], "#140a06", "#4a3a3a", "kalpak", "#3a2a1a",
                  "#2a1a12", silah="mizrak", bayrak="#c8302a" if j == 0 else None, dur=True)
        figur(t, tug, 480, z, 1.6, faz=f, flamalar=("#2a2a2a", "#c8302a", "#e0b040"))
        figur(t, atli, 80, z, 2.9, -1, f, "#8a6a4a", "#2a1810", "#2a4a3a", "kalpak", "#4a3020", "#5a5a5a", adim=0.85)  # Hacı Barlas kaçar
        figur(t, timur, 255, z, 2.8, 1, adim=f)  # genç Timur istilacıya yürür

    sprite(23, "karakter", 520, 160, KARE, kare)


def sahne24():
    """Düğün gecesi (y. 1362): Timur ile Olcay Türkan, yanlarında Emir Hüseyin; ateş, ışıklı yurtlar, misafirler."""
    gokyuzu(24, ["#0a0c22", "#1a1a3a", "#2e2448", "#4a2e4a", "#6a3a40"], (440, 240, 12, ["#f4ecd0", "#c8c0a8"]),
            [(140, 330, 30)], ("#4a3a5a", "#3a2e4a", "#2a2238"), yildiz=120)
    uzak(24, ["#2a2440", "#221e36"], ["#2e2a3a", "#262230"], ["#3a3428", "#322c22", "#2a2620"])

    def kamp(img, z):
        zemin = duz(588)
        ordugah(img, zemin, 20, 800, 24, 2.0, mesale=True)

    orta(24, (520, 560), ["#5a5a36", "#4e4e2e", "#424228", "#363622", "#2a2a1c"], "#8a8a5a", ekle=kamp)
    on(24, ["#1a1a12", "#26261a", "#3a2e2a"], "#6a5a7a")

    def kare(t, z, i):
        f = i / KARE
        figur(t, yurt, 60, z, 3.0, keçe="#e8dcc0", golge="#a89878", kapi="#c8302a", isik=True, isik_gucu=0.8 + 0.2 * math.sin(f * 12))
        ates(t, 245, z, f, 1.9)
        rnd = random.Random(24)
        for j, x in enumerate((140, 175)):  # misafirler: çalgılı, alkışlayan
            figur(t, kisi, x, z, 2.4, rnd.choice(("#5a3a3a", "#3a4a5a")), "kalpak", "#3a2a1a", "#2a1a12", yon=1, kol=0.3 + 0.3 * math.sin(f * 12.56 + j))
        figur(t, timur, 300, z, 2.6, -1)
        figur(t, kisi, 325, z, 2.5, "#c8304a", "ortu", "#8a1a2a", kadin=True, yon=-1, kemer="#e0b040")  # Olcay Türkan
        figur(t, kisi, 352, z, 2.7, "#2a7ac8", "kalpak", "#4a3020", "#2a1a12", yon=-1, pelerin="#e0b040")  # Emir Hüseyin
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
    """Sistan, 1363-64: çölde pusu. Karşıdaki kayalık setin üstündeki okçular atar; iki ok Timur'un sağ dizine ve koluna saplanır, diz çöker."""
    gokyuzu(25, ["#c8a070", "#d8b080", "#e8c890", "#f0d8a0", "#f4e0b0"], (90, 300, 26, ["#fff8e0", "#ffe8b0"]),
            [(420, 360, 26)], ("#fff4e0", "#f0dcc0", "#d8b898"))
    uzak(25, ["#b8906a", "#a8805e"], ["#c8a070", "#b89062"], ["#d8b480", "#c8a472", "#b89464"], dag_y=(340, 420))
    orta(25, (528, 562), ["#d8b07a", "#c8a06e", "#b89062", "#a88056", "#98704c"], "#f0d098",
         ekle=lambda img, z: [figur(img, taslar, x, duz(588), 1.2) for x in (60, 700)])
    on(25, ["#98704c", "#b89062", "#a88056"], "#f0d8a0")

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        y = z[0]
        set_y = y - 34  # kayalık setin düz üstü
        d.polygon([(290, y - 1), (304, set_y + 8), (316, set_y), (430, set_y - 2), (444, set_y + 10), (452, y - 1)], fill=hex2("#a87a52"))
        d.polygon([(380, set_y), (430, set_y - 2), (444, set_y + 10), (452, y - 1), (400, y - 1)], fill=hex2("#8a6040"))
        d.line([318, set_y, 430, set_y], fill=hex2("#d8a878"), width=2)
        rnd = random.Random(25)
        for _ in range(40):
            piksel(t, rnd.randint(312, 432), rnd.randint(set_y + 3, y - 2), hex2("#8a6040"))
        temas_golgesi(t, 370, y, 150)
        figur(t, at, 110, z, 2.9, 1, "#6b3f24", "#2b1a12", eyer=True, dur=True, bas=0.2, kulak=math.sin(f * 20))
        vuruldu = f >= 0.5
        if vuruldu:
            figur(t, timur, 190, z, 2.6, 1, diz=True)
            for (ax, ay, bx_, by_) in ((195, y - 5, 211, y - 14), (197, y - 22, 213, y - 30)):  # dize ve kola saplı oklar
                d.line([ax, ay, bx_, by_], fill=hex2("#3a2418"), width=2)
                for k in range(3):
                    piksel(t, bx_ - k, by_ - 2, hex2("#f4f0e6"))
                    piksel(t, bx_ + 1 - k, by_ + 1, hex2("#f4f0e6"))
            for k in range(3):
                piksel(t, 194, y - 5 + k, hex2("#a01818"))
                piksel(t, 196, y - 21 + k, hex2("#a01818"))
        else:
            figur(t, timur, 190, z, 2.6, 1, adim=f * 2 % 1, silah="kilic")
        ust = duz(set_y, 440)
        for j, x in enumerate((340, 375, 410)):  # okçular setin üstünde
            figur(t, kisi, x, ust, 2.4, "#4a5a3a", "kalpak", "#3a2a1a", "#2a1a12", yon=-1, silah="yay", kol=0.4 if f < 0.5 else 0.0)
            if f < 0.5:
                ok_ucusu(t, x - 8, set_y - 26, 200 + j * 3, y - (8 if j % 2 else 24), ((f * 2) - j * 0.12) % 1)
            # vurulduktan sonra okçular ateşi keser, yaylar iner

    sprite(25, "karakter", 440, 160, KARE, kare)

def sahne26():
    """1365 Çamur Savaşı: sağanak ve şimşek; iki at çamura saplanıp çırpınır, keçe örtülü Moğollar sağdan gelir, Timur topallayarak çekilir."""
    gokyuzu(26, ["#1a1e26", "#262a34", "#363a44", "#4a4c52", "#5a5a5a"], None, [(120, 290, 48), (400, 300, 44), (270, 350, 30)],
            ("#4a4e58", "#3a3e48", "#2a2e38"))
    uzak(26, ["#3a3e48", "#32363e"], ["#3e4238", "#363a30"], ["#4a4638", "#423e30", "#3a362a"])
    orta(26, (528, 562), ["#5a4a36", "#4e402e", "#423628", "#382e22", "#2e261c"], "#7a6a52",
         ekle=lambda img, z: None)
    on(26, ["#2e261c", "#423628", "#3a3a3a"], "#7a8a9a")
    hava(26, "yagmur", 320, "#a8b8d0", 0.3, simsek=(4, 5, 16))

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        for j, x in enumerate((140, 205)):  # çamura saplanmış atlar: şahlanmaya çalışır, bacakları balçıkta
            gom = duz(z[0] + 12, len(z))  # at balçığa 12 piksel gömülü: toynaklar çamurun içinde
            figur(t, at, x, gom, 2.9, 1, ("#6b3f24", "#8a6a4a")[j], "#140a06", eyer=True, dur=False, faz=(f * 2 + j * 0.5) % 1, adim=1.1,
                  bas=0.15 + 0.15 * math.sin(f * 12.56 + j))
            d.rectangle([x - 40, z[0] - 6, x + 40, z[0] - 1], fill=hex2("#3e3020"))
            d.ellipse([x - 44, z[0] - 10, x + 44, z[0] + 2], fill=hex2("#3e3020"))
            d.ellipse([x - 30, z[0] - 9, x + 22, z[0] - 4], fill=hex2("#6a7a8a"))  # su birikintisi çamurun üstünde
            for k in range(8):  # çamur sıçrar
                u = (f * 2 + k / 8) % 1
                piksel(t, x - 20 + k * 6, z[0] - 14 - math.sin(u * math.pi) * 14, hex2("#5a4a32"))
                piksel(t, x - 19 + k * 6, z[0] - 14 - math.sin(u * math.pi) * 14, hex2("#5a4a32"))
        figur(t, timur, 262, z, 2.8, -1, adim=f, silah="kilic")  # Timur topallayarak çekilir
        for j, x in enumerate((325, 382, 440)):  # keçe örtülü Moğollar
            figur(t, atli, x, z, 2.8, -1, (f * 2 + j * 0.3) % 1, ("#2a1810", "#3a2418", "#2a1810")[j], "#140a06", "#8a8070", "kalpak",
                  "#5a5248", "#2a1a12", silah="mizrak", adim=0.6)
            d.rectangle([x - 26, z[0] - 3, x + 26, z[0] - 1], fill=hex2("#3e3020"))

    sprite(26, "karakter", 520, 170, KARE, kare)


def sahne27():
    """Semerkant, 1365: kapının önünde halk milisi Serbedarlar; surun dibinde salgından yere düşmüş Moğol atları, çekilen ordu."""
    gokyuzu(27, ["#5a6a8a", "#7a88a0", "#a8a8a8", "#c8b8a0", "#d8c098"], None, [(130, 300, 40), (420, 330, 34)],
            ("#e8e0d8", "#c8c0b8", "#9a9090"))
    uzak(27, ["#7a8098", "#6a7088"], ["#8a9070", "#7a8064"], ["#a8a070", "#989062", "#888256"])

    def sehir(img, z):
        zemin = duz(588)
        orta_asya_sehri(img, 200, 640, zemin, 3.5, tohum=27)
        rnd = random.Random(270)
        for x in range(500, 680, 30):  # uzakta sağa çekilen Moğol atlıları
            figur(img, atli, x + rnd.randint(-4, 4), duz(592), 1.6, 1, rnd.random(), "#3a2418", "#140a06", "#5a5248", "kalpak", "#3a3428",
                  silah="mizrak", kontur="#1a1008")

    orta(27, (526, 560), ["#8a8a52", "#7a7a48", "#6a6a40", "#5a5a38", "#4a4a30"], "#b8b878", ekle=sehir)
    on(27, ["#4a4a30", "#6a6a40", "#6a5a3a"], "#d8d890")

    def kare(t, z, i):
        f = i / KARE
        rnd = random.Random(27)
        for j, x in enumerate((110, 138, 180, 204, 245)):  # Serbedarlar kapı önünde
            figur(t, kisi, x, z, 2.6, rnd.choice(("#6a4a3a", "#4a4a5a", "#7a6a4a")), "takke", rnd.choice(("#3a5a3a", "#7a2a2a")), "#2a1a12",
                  yon=(1, 1, -1, 1, -1)[j], silah=("mizrak", "sopa", "yay", "mizrak", "sopa")[j], kemer=None, kol=(0, 0.6, 0.3, 0, 0.8)[j])
        figur(t, yatan_at, 60, z, 2.4, 1, "#5a3a24", nefes=0.5 + 0.5 * math.sin(f * 2 * math.pi))
        figur(t, yatan_at, 312, z, 2.4, 1, "#8a6a4a")
        figur(t, atli, 470, z, 2.8, 1, f, "#3a2418", "#140a06", "#5a5248", "kalpak", "#3a3428", "#2a1a12", silah="mizrak", adim=0.5)
        rnd = random.Random(int(f * 3))
        for k in range(10):  # leşlerin üstünde sinekler
            piksel(t, 360 + rnd.randint(-40, 40), z[0] - 30 - rnd.randint(0, 14), hex2("#1a1008"))

    sprite(27, "karakter", 520, 160, KARE, kare)


def sahne28():
    """Belh, 1370 gecesi: kuşatılmış şehrin kapısından Emir Hüseyin, iki muhafız arasında, meşaleler altında çıkar."""
    gokyuzu(28, ["#1a0e1e", "#3a1626", "#6a2228", "#a8422a", "#d8702e"], (100, 250, 12, ["#f4dcc0", "#c8a890"]),
            [(380, 320, 34)], ("#4a2a2a", "#3a1e22", "#2a1218"), yildiz=90)
    uzak(28, ["#2a1a22", "#22141c"], ["#2a1e1a", "#221814"], ["#3a2a1e", "#32241a", "#2a1e16"])

    def sehir(img, z):
        zemin = duz(588)
        orta_asya_sehri(img, 300, 700, zemin, 2.7, tohum=28, kerpic="#a8806a", golge="#7a5a48", kubbe="#2a6a7a")
        ordugah(img, zemin, 10, 250, 28, 1.7, mesale=True)

    orta(28, (526, 560), ["#5a4430", "#4e3a2a", "#423224", "#382a1e", "#2e2218"], "#9a7050", ekle=sehir)
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
        figur(t, oturan, 200, duz(y - 12, 400), 2.6, "#2a4a8a", "tac", "#e0b040", "#3a2418", minder="#9a2a2a")  # kukla han Soyurgatmış
        figur(t, timur, 250, z, 2.7, -1, kol=1.0)
        # kukla ipleri: Timur'un kaldırdığı çubuktan hanın başına ve kollarına iner (simge)
        cubuk_y = y - 52 + int(math.sin(f * 2 * math.pi) * 1.5)
        d.line([206, cubuk_y, 248, cubuk_y - 4], fill=hex2("#6a4a2a"), width=2)
        for hx, hy in ((196, y - 40), (204, y - 40), (192, y - 28), (208, y - 28)):
            d.line([hx + 6, cubuk_y - 1, hx, hy], fill=hex2("#e8e0d0"), width=1)
        figur(t, kisi, 150, z, 2.5, "#e8d8f0", "tac", "#e0b040", kadin=True, yon=1)  # Saray Mülk Hatun
        for j, x in enumerate((300, 335, 365, 100, 66)):
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
    """Kafesli tahtırevan: önde ve arkada aynı yöne yürüyen iki at; uzun sırıklar iki atın eyerine oturur, aralarında
    ahşap parmaklıklı, perdeli bir oda taşınır (demir kafes efsanesinin muhtemel gerçeği)."""
    ax1, ax2 = x - int(22 * s) * yon, x + int(22 * s) * yon
    at(img, ax1, zemin, s, yon, "#4a3020", "#1a0e08", eyer=True, faz=faz, adim=0.4)
    at(img, ax2, zemin, s, yon, "#6a4a30", "#1a0e08", eyer=True, faz=(faz + 0.5) % 1, adim=0.4)
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 10 * s)
    sy = y - int(15 * s) - 1  # eyer hizası
    d.line([ax1 - int(3 * s), sy, ax2 + int(3 * s), sy], fill=hex2("#5a3a22"), width=max(2, int(1.2 * s)))
    for ex in (ax1, ax2):  # sırık eyere kayışla bağlı
        d.line([ex, sy, ex, sy + int(2 * s)], fill=hex2("#2a1a10"), width=max(1, int(0.8 * s)))
    alt = sy - 1
    d.rectangle([x - int(9 * s), alt - int(15 * s), x + int(9 * s), alt], fill=hex2("#3a2416"))
    kisi(img, x, duz(alt, img.width), s * 0.8, "#2a6a3a", "sarik", "#f4f0e6", "#2a1a14", yon=yon)
    for k in range(-9, 10, 3):  # ahşap parmaklıklar
        d.line([x + int(k * s), alt - int(15 * s), x + int(k * s), alt], fill=hex2("#8a5a32"), width=max(1, int(0.7 * s)))
    d.rectangle([x - int(9 * s), alt - int(15 * s), x - int(5 * s), alt - int(4 * s)], fill=hex2("#9a2a2a"))  # toplanmış perde
    d.rectangle([x - int(11 * s), alt - int(18 * s), x + int(11 * s), alt - int(15 * s)], fill=hex2("#7a1e22"))
    d.polygon([(x - int(11 * s), alt - int(18 * s)), (x, alt - int(23 * s)), (x + int(11 * s), alt - int(18 * s))], fill=hex2("#9a2a2a"))


def sahne30():
    """Teslim olan şehir yaşadı, direnen şehir kule oldu: solda kapısı açık, pazarı kurulu, çocukların koştuğu aydınlık şehir;
    kamera sağa kayınca aynı ovada isyan etmiş, dumanı tüten şehrin önünde kafatası kuleleri ve kargalar."""
    # gün ışığı: sıcak pastel gök, altın güneş; direnen şehrin karanlığını yalnızca dumanı verir
    gokyuzu(30, ["#6aa0d8", "#9ac0e0", "#e0d0a8", "#f4d090", "#f0b070"], (110, 470, 18, ["#fff8d0", "#ffe090"]),
            [(140, 300, 30)], ("#fff8ec", "#f4dcc8", "#d8a8a0"))
    uzak(30, ["#9aa0b8", "#8a90a8"], ["#b8b070", "#a8a062"], ["#c8b870", "#b8aa62", "#a89c56"])

    def sehirler(img, z):
        zemin = duz(588)
        orta_asya_sehri(img, 10, 330, zemin, 2.6, tohum=30, kubbe="#2a8ac8")
        orta_asya_sehri(img, 520, 800, zemin, 2.6, tohum=31, kerpic="#8a6a52", golge="#5a4434", kubbe="#3a4a5a")
        for k, x in enumerate((600, 700)):
            duman(img, x, 545, 70, 30 + k, faz=0.3 * k, renk="#3a3434", ruzgar=0.4, genislik=1.2)

    orta(30, (526, 560), ["#9aa058", "#8a9050", "#7a8048", "#6a7040", "#5a6038"], "#c8d080", ekle=sehirler)
    on(30, ["#5a6038", "#7a8048", "#7a6a3a"], "#d8e090")

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        y = z[0]
        # teslim olan şehrin açık kapısı: figürlerle aynı zeminde kemerli kapı, kanatları açık
        d.rectangle([8, y - 56, 44, y - 1], fill=hex2("#c8a878"), outline=hex2("#6a4a2a"))
        d.chord([14, y - 50, 38, y - 26], 180, 360, fill=hex2("#3a2a1a"))
        d.rectangle([14, y - 38, 38, y - 1], fill=hex2("#3a2a1a"))
        d.rectangle([8, y - 56, 44, y - 52], fill=hex2("#2a8ac8"))
        d.polygon([(14, y - 40), (4, y - 36), (4, y - 1), (14, y - 1)], fill=hex2("#6a4a2a"))  # açık kanat
        d.polygon([(38, y - 40), (48, y - 36), (48, y - 1), (38, y - 1)], fill=hex2("#6a4a2a"))
        for x, renk in ((70, "#c8302a"), (126, "#2a7ac8")):  # pazar tezgâhları: direkler zemine dikili
            for px_ in (x - 18, x + 18):
                d.line([px_, y - 1, px_, y - 26], fill=hex2("#5a3a22"), width=2)
            d.polygon([(x - 22, y - 26), (x + 22, y - 26), (x + 18, y - 32), (x - 18, y - 32)], fill=hex2(renk))
            d.rectangle([x - 16, y - 12, x + 16, y - 9], fill=hex2("#7a4a2a"))
            for ax in (x - 14, x + 14):
                d.line([ax, y - 9, ax, y - 1], fill=hex2("#5a3a22"))
            for m in range(4):
                d.ellipse([x - 14 + m * 8, y - 16, x - 9 + m * 8, y - 11], fill=hex2(("#e0b040", "#c8302a", "#6aa040", "#f0e0c0")[m]))
        for j, x in enumerate((98, 158)):  # satıcı ve alıcı
            figur(t, kisi, x, z, 2.5, ("#6a4a8a", "#3a6a4a")[j], "takke", ("#2a5a3a", "#7a2a2a")[j], "#3a2a1a", yon=-1 if j else 1, kol=0.3)
        for j in range(2):  # koşan çocuklar (yetişkinin yaklaşık %70'i, okunur boyda)
            cx = 60 + ((f + j * 0.5) % 1) * 110
            figur(t, kisi, cx, z, 1.9, ("#c8a040", "#c8302a")[j], "takke" if j else None, "#2a5a3a", None, yon=1, adim=(f * 2 + j * 0.5) % 1,
                  kemer=None, uzun=False)
        for k, x in enumerate((390, 450)):  # isyan eden şehirden yükselen duman
            duman(t, x, y - 2, 150, 300 + k, faz=(f + k * 0.4) % 1, renk="#3a3434", ruzgar=0.3, genislik=1.4)
        for x, s in ((360, 2.6), (420, 3.0), (480, 2.6)):  # direnen şehrin önünde kafatası kuleleri
            figur(t, kafa_kulesi, x, z, s)
        for j in range(4):
            a = (f + j / 4) * 2 * math.pi
            cx, cy = 420 + math.cos(a) * 60, 30 + math.sin(a) * 12
            kanat = 2 if (i + j) % 6 < 3 else -1
            d.line([cx - 4, cy - kanat, cx, cy, cx + 4, cy - kanat], fill=hex2("#120806"), width=2)

    sprite(30, "karakter", 520, 170, KARE, kare)


def sahne31():
    """Toktamış'a karşı (1391-1395): bozkırda iki ordu çarpışır; Timur'un atlıları soldan, Altın Orda sağdan."""
    gokyuzu(31, ["#5a6a8a", "#8a90a0", "#b8a890", "#d8b888", "#e8c890"], (450, 470, 18, ["#fff2c0", "#ffd890"]),
            [(120, 300, 44), (330, 330, 30)], ("#e8d8c8", "#c8b0a0", "#987a78"))
    uzak(31, ["#7a7a90", "#6a6a80"], ["#9a9070", "#8a8064"], ["#b8a870", "#a89a62", "#988c56"])

    def ordular(img, z):
        zemin = duz(588)
        rnd = random.Random(31)
        for x in range(10, 380, 18):
            figur(img, atli, x + rnd.randint(-3, 3), zemin, 1.0, 1, rnd.random(), "#3a2418", "#140a06", "#1e4a7a", "kalpak", "#3a2a1a",
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
                  "#7a1e22" if j == 2 else ("#1e4a7a", "#1e6a7a", "#1e4a7a", "#1e6a7a")[j], "sorguc" if j == 2 else "kalpak", "#2a1a14", "#a8522a" if j == 2 else "#2a1a12",
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
        dam = orta_asya_sehri(img, 200, 760, zemin, 2.7, tohum=32, kerpic="#a8805a", golge="#7a5a40", kubbe="#2a6a9a")
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
        orta_asya_sehri(img, 380, 790, zemin, 2.4, tohum=33, kerpic="#c87a5a", golge="#9a5a40", kubbe="#f0e8d8")
        for x in (60, 140, 220, 300):
            figur(img, agac_kavak, x, zemin, 1.3)

    orta(33, (526, 560), ["#a8a05a", "#989050", "#888048", "#787040", "#686038"], "#d8d088", ekle=sehir)
    on(33, ["#686038", "#888048", "#7a6a3a"], "#e8e098")

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((70, 125, 180)):
            figur(t, atli, x, z, 2.1, 1, (f * 2 + j * 0.3) % 1, ("#3a2418", "#6b3f24", "#2a1810")[j], "#140a06",
                  "#7a1e22" if j == 1 else "#1e4a7a", "sorguc" if j == 1 else "kalpak", "#2a1a14", "#a8522a" if j == 1 else None,
                  silah="kilic" if j == 1 else "yay", kol=0.6, adim=0.8)
        # savaş filleri: omuz yüksekliği atın 1,7 katı (ölçek kuralı), atlılara doğru hücum; ayaklarında toz
        for j, x in enumerate((300, 400, 490)):
            figur(t, fil, x, z, 2.7, -1, (f * 1.5 + j * 0.4) % 1, ("#8a8a90", "#7a7a80", "#82828a")[j], adim=0.6)
            for k in range(6):
                u = (f * 1.5 + k / 6 + j * 0.2) % 1
                piksel(t, x + 30 + u * 40, z[0] - 3 - math.sin(u * math.pi) * 14 - k % 3 * 2, hex2("#c8b080", int(190 * (1 - u))))
        for j in range(3):
            ok_ucusu(t, 120 + j * 30, z[0] - 50, 330 + j * 40, z[0] - 80, (f * 1.5 + j * 0.33) % 1)

    sprite(33, "karakter", 520, 200, KARE, kare)


def sahne34():
    """Mektup: Timur'un ulağı ordugâhtan batıya, Bayezid'e dörtnala yola çıkar."""
    gokyuzu(34, ["#4a6aa8", "#6a8ac0", "#a8b8c8", "#e0c8a0", "#f0c890"], (110, 470, 16, ["#fff2c0", "#ffd890"]),
            [(140, 300, 36), (420, 320, 30)])
    uzak(34, ["#8a90a8", "#7a8098"], ["#9aa078", "#8a906a"], ["#b0a870", "#a09862", "#908a56"])

    def kamp(img, z):
        zemin = duz(588)
        figur(img, otag, 650, zemin, 2.0, "#7a1e22", "#e0b040", acik=True)
        ordugah(img, zemin, 430, 600, 34, 1.8)
        figur(img, tug, 740, zemin, 1.0)

    orta(34, (526, 560), ["#9aa058", "#8a9050", "#7a8048", "#6a7040", "#5a6038"], "#c8d080", ekle=kamp)
    on(34, ["#5a6038", "#7a8048", "#7a6a3a"], "#d8e090")

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 150, z, 2.3, -1, f, "#2a1810", "#140a06", "#5a3a3a", "kalpak", "#3a2a1a", "#2a1a12", silah="mektup", kol=0.0,
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
    """Sivas, Ağustos 1400: kavurucu sarı gök. Lağımcılar surun dibinde tünel ağzını kazar, içerideki destek kirişleri yanar,
    duman yukarı çıkar; mancınık surları döver, Timur izler."""
    gokyuzu(36, ["#c86a2a", "#e08a3a", "#f0b050", "#f8d070", "#fce090"], (420, 300, 24, ["#fff8d0", "#ffe080"]), [(120, 300, 30)],
            ("#fff0d0", "#f0c890", "#d8a070"))
    uzak(36, ["#b08a6a", "#a07a5e"], ["#c0a070", "#b09062"], ["#c8a868", "#b8985c", "#a88a52"])
    orta(36, (526, 560), ["#b8a058", "#a89050", "#988048", "#887040", "#786038"], "#e0c878",
         ekle=lambda img, z: figur(img, mancinik, 250, duz(588), 1.5, 1, 0.6))
    on(36, ["#786038", "#988048", "#8a6a3a"], "#f0d888")

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        anadolu_kalesi(t, 262, 384, z, 1.6, kapi=False)  # Sivas suru: düz ovaya oturur
        y = z[0]
        d.chord([262, y - 22, 302, y + 18], 180, 360, fill=hex2("#140c08"))  # sur dibinde lağım ağzı
        for k in range(5):  # tünelde yanan destek kirişleri
            d.line([266 + k * 7, y - 2, 270 + k * 7, y - 16], fill=hex2("#6a3a1a"), width=2)
        ates(t, 282, z, f, 0.9)
        duman(t, 282, y - 12, 140, 36, faz=f, renk="#4a4040", ruzgar=0.25, genislik=1.6)
        for j, x in enumerate((218, 243)):  # lağımcılar ağzın başında kazar
            figur(t, kisi, x, z, 2.4, "#5a4a3a", "bork", "#5a3a22", None, yon=1, silah="kazma",
                  kol=abs(math.sin((f + j * 0.4) * 2 * math.pi)), diz=j == 1)
        rnd = random.Random(i // 2)
        for k in range(16):  # kazıdan kalkan toz
            piksel(t, 250 + rnd.randint(-20, 20), y - rnd.randint(2, 18), hex2("#d8b888", 150))
        figur(t, timur, 168, z, 2.8, 1, silah="kilic", kol=0.8)

    sprite(36, "karakter", 520, 200, KARE, kare)


def sahne37():
    """Sivas sonrası: 'kan dökülmeyecek' sözü. Açılmış derin çukurda savunucular; kürekçiler üstlerine toprak atar, toz kalkar;
    mızraklı muhafızlar bekler. Arkada düz ovada Sivas suru."""
    gokyuzu(37, ["#2a1420", "#4a1c24", "#7a2a22", "#a83a1e", "#d06030"], (440, 520, 22, ["#ffa060", "#c8401c"]),
            [(150, 320, 36)], ("#3a1616", "#2a1010", "#1a0a0a"), yildiz=40)
    uzak(37, ["#2a1418", "#221014"], ["#3a2418", "#301e14"], ["#4a3020", "#40281a", "#362216"])

    def kale(img, z):
        anadolu_kalesi(img, 470, 800, duz(588), 2.2, tas="#6a5a52", golge="#4a3e38")

    orta(37, (526, 560), ["#6a4630", "#5a3c28", "#4e3220", "#42291a", "#362016"], "#9a6a3e", ekle=kale)
    on(37, ["#22160e", "#362216", "#3a1a12"], "#a85a3a")

    ALT = 44  # sprite zeminin altına 44 satır iner: çukurun içi görünsün, kafalar çukur ağzının altında kalsın

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        y = z[0] - ALT  # gerçek zemin çizgisi
        zemin = duz(y, len(z))
        d.polygon([(164, y), (172, z[0] - 1), (352, z[0] - 1), (360, y)], fill=hex2("#2a1a10"))  # çukur: zemine kazılmış
        for k in range(y + 2, z[0] - 1, 5):  # kazı duvarındaki toprak katmanları (iki yan şev)
            d.line([164 + (k - y) * 8 // (z[0] - y), k, 164 + (k - y) * 8 // (z[0] - y) + 10, k], fill=hex2("#4a2e1a"))
            d.line([360 - (k - y) * 8 // (z[0] - y) - 10, k, 360 - (k - y) * 8 // (z[0] - y), k], fill=hex2("#4a2e1a"))
        d.line([164, y, 172, z[0] - 1], fill=hex2("#6a4a2a"), width=2)
        d.line([360, y, 350, z[0] - 1], fill=hex2("#6a4a2a"), width=2)
        d.line([160, y - 1, 364, y - 1], fill=hex2("#7a5a32"))  # çukur ağzı: aydınlık kenar
        dip = duz(z[0], len(z))
        rnd = random.Random(37)
        for j, x in enumerate(range(182, 346, 18)):  # çukurdaki savunucular: büyük ve okunur, omuzları zemin hizasında
            kisi(t, x + rnd.randint(-2, 2), dip, rnd.uniform(2.6, 3.0), rnd.choice(("#4a3a2a", "#3a3a4a", "#5a2a2a", "#4a4a3a", "#6a4a3a")),
                 rnd.choice(("bork", "kalpak", "migfer", None)), rnd.choice(("#3a2a1a", "#5a3a22", "#7a7a80")), rnd.choice((None, "#2a1a12")),
                 yon=rnd.choice((1, -1)), kemer=None, kol=rnd.choice((0.0, 0.0, 0.6, 1.0)), diz=j % 4 == 1)
        dolu = int(f * 10)  # toprak çukuru dolduruyor
        d.rectangle([172, z[0] - 1 - dolu, 352, z[0] - 1], fill=hex2("#3a2416"))
        for kx in (150, 374):  # kenarlarda kazılmış toprağın yığınları (büyük, iki kademeli)
            d.chord([kx - 34, y - 22, kx + 34, y + 22], 180, 360, fill=hex2("#5a3a22"))
            d.chord([kx - 20, y - 28, kx + 20, y + 28], 180, 360, fill=hex2("#6a4a2e"))
            for m in range(6):
                piksel(t, kx - 18 + m * 7, y - 20 + m % 2 * 4, hex2("#8a6a3a"))
        for j, x in enumerate((150, 368)):
            figur(t, kisi, x, zemin, 2.5, "#5a4a3a", "kalpak", "#3a2a1a", "#2a1a12", yon=1 if x < 200 else -1, silah="kurek",
                  kol=abs(math.sin((f * 2 + j * 0.5) * math.pi)) * 0.7)
            u = (f * 2 + j * 0.5) % 1  # kürekten uçan toprak
            yon_ = 1 if x < 200 else -1
            for k in range(9):  # kürekten savrulan toprak öbekleri: yay çizip çukura düşer
                ox = x + yon_ * (14 + u * 70 + k * 4)
                oy = y - 26 - math.sin(u * math.pi) * 26 + k % 3 * 3
                ImageDraw.Draw(t).ellipse([ox - 3, oy - 3, ox + 3, oy + 2], fill=hex2("#7a5a32"), outline=hex2("#3a2416"))
        for k in range(60):  # çukurdan kalkan toz: yoğun, aydınlık
            piksel(t, 260 + rnd.randint(-90, 90), y - rnd.randint(2, 48) - (i % 6), hex2("#b89a6a", rnd.randint(90, 170)))
        for x in (134, 386):  # mızraklı muhafızlar iki yanda, kadrajın içinde
            figur(t, kisi, x, zemin, 2.5, "#3a2a2a", "migfer", "#7a7a80", "#2a1a12", yon=1 if x < 200 else -1, silah="mizrak")

    sprite(37, "karakter", 520, 170 + ALT, KARE, kare)


def sahne38():
    """Ankara, Temmuz 1402: Timur'un işçileri Çubuk Çayı'na kütük ve taş bent kurar; bentin arkasında su birikir, önünde dere
    yatağı çatlayarak kurur; Osmanlı askerleri boş kaplarla yatağa eğilir."""
    gokyuzu(38, ["#6a8ab8", "#9ab0c8", "#d8d0b0", "#f0d8a0", "#f8e0a8"], (300, 300, 13, ["#fffae0", "#fff0b0"]), [(430, 340, 22)])
    uzak(38, ["#a89a88", "#988a78"], ["#b8a070", "#a89062"], ["#c8a870", "#b89862", "#a88a56"])
    orta(38, (526, 560), ["#b8a058", "#a89050", "#988048", "#887040", "#786038"], "#e0c878")
    on(38, ["#786038", "#988048", "#8a6a3a"], "#f0d888")

    ALT_38 = 16

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        ALT = ALT_38  # sprite gerçek zeminin 8 satır altına iner: kuru yatak zeminden alçak görünsün
        y = z[0] - ALT
        zem = duz(y, len(z))
        # bentin arkasında yükselen göl: bent seviyesine kadar dolu, yüzeyde yansıma ve dalga pırıltısı
        d.rectangle([10, y - 20, 196, y - 1], fill=hex2("#2a5a8a"))
        d.rectangle([10, y - 20, 196, y - 17], fill=hex2("#4a8ab8"))
        for k in range(12, 196, 9):
            piksel(t, k + (i % 9), y - 18, hex2("#b8e0f0"))
            piksel(t, k + (i * 2 % 9), y - 10 - (k // 9) % 3 * 3, hex2("#3a6a9a"))
        for k, (bx, bs) in enumerate(((204, 1.7), (226, 1.9), (248, 1.7))):  # bent: büyük taş yığınları
            figur(t, taslar, bx, zem, bs)
        for k in range(6):  # üstüne yatırılmış kütükler
            d.line([194, y - 10 - k * 4, 260, y - 12 - k * 4], fill=hex2("#6a4428"), width=3)
            piksel(t, 194, y - 10 - k * 4, hex2("#c8a070"))
        # bentin önü: zeminden alçak, kurumuş ve çatlamış dere yatağı (kenarları kıyı şevi)
        d.polygon([(258, y - 1), (268, z[0] - 1), (514, z[0] - 1), (520, y - 1)], fill=hex2("#a8865a"))
        d.rectangle([268, y + 1, 514, z[0] - 1], fill=hex2("#b8966a"))
        rnd2 = random.Random(38)
        for k in range(272, 512, 11):  # çatlak dokusu: kırık çokgen çizgiler
            d.line([k, y + 1, k + 3, y + 4, k + 1, y + 7], fill=hex2("#5a3a1a"))
            d.line([k + 3, y + 4, k + 9, y + 4 + rnd2.randint(-1, 1)], fill=hex2("#5a3a1a"))
        for k in range(270, 512, 23):
            d.ellipse([k, y + 2, k + 3, y + 4], fill=hex2("#8a7050"))  # kuru çakıl
        yatak = duz(z[0], len(z))
        figur(t, kisi, 228, duz(y - 30, 520), 2.5, "#2a6a7a", "kalpak", "#3a2a1a", "#2a1a12", yon=-1, silah="sopa",
              kol=0.4 + 0.3 * math.sin(f * 6.28))  # bentin üstünde Timur'un işçisi
        for j, x in enumerate((290, 322, 384)):  # susuz askerler yatağa çökmüş, boş testiyle kuru toprağa eğilir
            figur(t, oturan, x, yatak, 2.7, ("#c8302a", "#2a6a3a", "#2a6a3a")[j], "sarik", "#f4f0e6", "#2a1a12", yon=-1, el="testi")
        figur(t, kisi, 352, yatak, 2.7, "#c8302a", "sarik", "#f4f0e6", "#2a1a12", yon=-1, silah="testi", kol=1.0)  # biri boş testiyi kaldırır
        for j, x in enumerate((283, 315, 377)):  # diz çökenlerin önünde ters çevrilmiş boş testi, tek damla düşmez
            d.ellipse([x - 3, y + 2, x + 3, y + 6], fill=hex2("#c8a040"), outline=hex2("#7a5a22"))
        rnd = random.Random(i)
        for k in range(14):  # sıcak hava titreşimi
            piksel(t, rnd.randrange(200, 500), y - 30 - rnd.randrange(0, 50), hex2("#fff8e0", 80))

    sprite(38, "karakter", 520, 150 + ALT_38, KARE, kare)


def sahne39():
    """Ankara Savaşı: Sırp zırhlı süvarisi Timurlu saflarına üç kez hücum eder; geride filler, toz ve oklar."""
    gokyuzu(39, ["#8a7a6a", "#a8907a", "#c8a880", "#d8b888", "#e0c090"], (100, 470, 22, ["#fff0c0", "#f8d090"]),
            [(380, 300, 44), (180, 330, 36)], ("#e8d0b8", "#c8a890", "#987868"))
    uzak(39, ["#9a8a7a", "#8a7a6a"], ["#a89070", "#988062"], ["#b89a68", "#a88a5c", "#987c52"])

    def arka(img, z):
        zemin = duz(588)
        rnd = random.Random(39)
        _ = (zemin, rnd)

    orta(39, (526, 560), ["#a88a58", "#987a50", "#886a48", "#785a40", "#684a38"], "#d8b880", ekle=arka)
    on(39, ["#684a38", "#886a48", "#7a5a3a"], "#e8c890")

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((100, 160, 220)):  # Sırp şövalyeleri sağa hücum
            figur(t, atli, x, z, 2.3, 1, (f * 2 + j * 0.3) % 1, ("#d8d8d8", "#3a2418", "#8a8a8a")[j], "#2a2a2a", "#5a5a6a", "sovalye", "#a8acb0",
                  silah="mizrak", zirh="#a8acb0", cul=("#c8302a", "#f0f0f0", "#c8302a")[j], bayrak="#f0f0f0", adim=0.85)
        for j, x in enumerate((300, 360, 420)):  # Timurlu atlılar ve saf değiştiren Tatarlar (turkuaz sancak) karşılar
            figur(t, atli, x, z, 2.1, -1, (f * 2 + j * 0.37) % 1, ("#3a2418", "#6b3f24", "#2a1810")[j], "#140a06", ("#1e4a7a", "#1e6a7a", "#1e6a7a")[j], "kalpak", "#3a2a1a",
                  "#2a1a12", silah="mizrak" if j == 2 else "kilic", bayrak="#2ab8b8" if j == 2 else None,
                  kol=0.4 + 0.5 * math.sin(f * 12.56 + j), adim=0.8)
        rnd = random.Random(i // 2)
        for k in range(40):  # toz bulutu
            x, y = 250 + rnd.randint(-60, 60), z[0] - rnd.randint(2, 30)
            piksel(t, x, y, hex2("#d8b888", 120))

    sprite(39, "karakter", 520, 170, KARE, kare)


def sahne40():
    """Bayezid dağlarda kuşatılır: atı yorulmuş, yaya kalmış; Timur'un atlıları ve mızraklı askerleri çevresini sarar, esir düşer."""
    gokyuzu(40, ["#2a2a4a", "#4a3a5a", "#7a4a5a", "#a8604a", "#c8784a"], (420, 520, 20, ["#ffc080", "#f08040"]),
            [(140, 300, 36)], ("#8a5a5a", "#6a4248", "#4a2a3a"), yildiz=30)
    uzak(40, ["#3a3048", "#30283e"], ["#4a3a3a", "#403232"], ["#5a4632", "#503e2c", "#463626"], dag_y=(180, 430), kenar="#8a7a9a")

    def dag(img, z):
        for x in range(0, 810, 30):
            figur(img, cam, x, duz(588), random.Random(x).uniform(1.4, 2.2), renk="#2a3a2a", isik="#3a4a3a", kontur="#101810")

    orta(40, (526, 560), ["#5a4a32", "#4e402c", "#423626", "#382e20", "#2e261a"], "#8a6a4a", ekle=dag)
    on(40, ["#2e261a", "#423626", "#3a2a2a"], "#a87a5a")

    def kare(t, z, i):
        f = i / KARE
        for j, (x, yon) in enumerate(((150, 1), (205, 1), (330, -1), (385, -1))):
            figur(t, atli, x, z, 2.6, yon, (f + j * 0.25) % 1, ("#3a2418", "#6b3f24", "#2a1810", "#5a3a24")[j], "#140a06", ("#1e4a7a", "#1e6a7a", "#1e4a7a", "#1e6a7a")[j], "kalpak",
                  "#3a2a1a", "#2a1a12", silah="mizrak", dur=True)
        figur(t, bayezid, 268, z, 2.8, 1, kol=0.5 + 0.2 * math.sin(f * 6.28), silah="kilic")
        for x in (115, 425):
            figur(t, kisi, x, z, 2.5, "#3a2a2a", "migfer", "#7a7a80", "#2a1a12", yon=1 if x < 268 else -1, silah="mizrak", kol=0.6)

    sprite(40, "karakter", 520, 170, KARE, kare)


def sahne41():
    """Ziyafet: Timur'un otağı önünde halıya serili alçak sofra; Timur ortada oturur, rivayete göre Bayezid'in eşi Despina
    testiden onun kâsesine şarap döker; esir Bayezid karşıda oturur."""
    gokyuzu(41, ["#0a0c22", "#1a1a3a", "#2e2448", "#4a2e4a", "#6a3a40"], (100, 240, 12, ["#f4ecd0", "#c8c0a8"]),
            [(400, 320, 30)], ("#4a3a5a", "#3a2e4a", "#2a2238"), yildiz=120)
    uzak(41, ["#2a2440", "#221e36"], ["#2e2a3a", "#262230"], ["#3a3428", "#322c22", "#2a2620"])

    def kamp(img, z):
        ordugah(img, duz(588), 20, 210, 41, 1.8, mesale=True)
        ordugah(img, duz(588), 610, 800, 42, 1.8, mesale=True)

    orta(41, (520, 560), ["#4a4a2e", "#404028", "#363622", "#2c2c1c", "#222216"], "#7a7a4a", ekle=kamp)
    on(41, ["#1a1a12", "#26261a", "#3a2e2a"], "#6a5a7a")

    def kare(t, z, i):
        f = i / KARE
        figur(t, otag, 160, z, 1.9, "#7a1e22", "#e0b040", faz=f, acik=True)
        d = ImageDraw.Draw(t)
        y = z[0]
        d.rectangle([150, y - 6, 410, y - 1], fill=hex2("#8a2a2a"))  # geniş desenli halı
        d.line([150, y - 6, 410, y - 6], fill=hex2("#e0b040"))
        for k in range(156, 410, 10):
            d.polygon([(k, y - 3), (k + 3, y - 5), (k + 6, y - 3), (k + 3, y - 1)], fill=hex2("#2a4a7a"))
        hali = duz(y - 6, 520)
        d.rectangle([272, y - 12, 312, y - 9], fill=hex2("#6a4428"))  # alçak sofra
        for ax in (275, 309):
            d.rectangle([ax - 1, y - 9, ax + 1, y - 5], fill=hex2("#4a2a16"))
        for k, renk in enumerate(("#c8a040", "#e8e0d0", "#8a3a1a")):
            d.ellipse([276 + k * 11, y - 16, 283 + k * 11, y - 12], fill=hex2(renk))
        figur(t, oturan, 250, hali, 3.4, "#7a1e22", "sorguc", "#2a1a14", "#d8d0c8", yon=1, el="kase", minder="#c8a040")
        figur(t, oturan, 340, hali, 3.2, "#2a6a3a", "sarik", "#f4f0e6", "#2a1a14", yon=-1, minder="#5a5a6a")
        figur(t, kisi, 226, hali, 3.0, "#3a3a7a", "ortu", "#c8a040", kadin=True, yon=-1, silah="testi", kol=0.3)
        for k in range(6):  # testiden kâseye akan şarap
            u = (f * 3 + k / 6) % 1
            piksel(t, 238 + u * 6, y - 40 + u * 16, hex2("#8a1020"))
            piksel(t, 239 + u * 6, y - 40 + u * 16, hex2("#8a1020"))

    sprite(41, "karakter", 520, 220, KARE, kare)


def sahne42():
    """İzmir, Aralık 1402: Rodos Şövalyeleri'nin liman kalesi. Mancınık kaleyi döver, işçiler liman ağzına taş döker, taş dolu
    sandal batırılır ve set yükselir; kırmızı yelkenli şövalye gemileri dönüp kaçar."""
    gokyuzu(42, ["#4a5a7a", "#6a7a90", "#9aa0a8", "#c8c0b0", "#d8c8a8"], None, [(120, 290, 44), (420, 320, 36)],
            ("#d8d8d8", "#b0b0b8", "#808090"))
    uzak(42, ["#6a7a90", "#5a6a80"], ["#7a8a7a", "#6a7a6a"], ["#4a6a8a", "#42607e", "#3a5672"])

    def liman(img, z):
        su_ve_kiyi(img, 596, kiyi_x=470)
        anadolu_kalesi(img, 300, 470, duz(588), 2.6, tas="#b0a898", golge="#807868")

    orta(42, (526, 560), ["#8a9a6a", "#7a8a5e", "#6a7a52", "#5a6a48", "#4a5a3e"], "#b8c890", ekle=liman)
    on(42, ["#2a4a6a", "#3a5a7a", "#4a5a6a"], "#a8c8e0")

    def kare(t, z, i):
        f = i / KARE
        su = z[0] - 8
        d = ImageDraw.Draw(t)
        d.rectangle([280, su, 520, z[0] - 1], fill=hex2("#2a5a8a"))  # liman suyu (sprite tabanında)
        for k in range(280, 520, 7):
            piksel(t, k + (i % 7), su, hex2("#8ab8d8"))
        for k, bx in enumerate(range(292, 344, 11)):  # liman ağzını dolduran uzun taş set
            figur(t, taslar, bx, z, 1.1 + 0.1 * (k % 2))
        d.polygon([(340, su + 2), (366, su + 2), (362, su + 6), (344, su + 6)], fill=hex2("#5a3a22"))  # batırılan taş dolu sandal
        gemi(t, 400, su + 2, 2.0, 1, f)  # kaçan şövalye gemisi
        figur(t, mancinik, 152, z, 2.0, 1, f, tas_x=390)
        figur(t, timur, 208, z, 2.6, 1, silah="kilic", kol=0.6)
        for j, x in enumerate((240, 262)):
            figur(t, kisi, x, z, 2.4, "#5a4a3a", "bork", "#5a3a22", None, yon=1, silah="kurek", kol=abs(math.sin((f + j * 0.5) * 6.28)) * 0.6)
            u = (f * 2 + j * 0.5) % 1  # sete atılan taşlar
            d.ellipse([x + 10 + u * 50, z[0] - 26 - math.sin(u * math.pi) * 18, x + 14 + u * 50, z[0] - 22 - math.sin(u * math.pi) * 18],
                      fill=hex2("#8a8478"))

    sprite(42, "karakter", 520, 200, KARE, kare)


def sahne43():
    """Kafes efsanesi ve gerçeği: iki at arasında kafesli tahtırevan; Bayezid Akşehir'e götürülür (8 Mart 1403)."""
    gokyuzu(43, ["#5a6070", "#7a7c88", "#9a9aa0", "#b8b4b0", "#c8c0b8"], None, [(130, 290, 44), (400, 320, 40)],
            ("#c8c8cc", "#a8a8b0", "#808088"))
    uzak(43, ["#6a6e7a", "#5e626e"], ["#7a7a6a", "#6e6e5e"], ["#8a8670", "#7e7a64", "#726e58"])

    def kasaba(img, z):
        zemin = duz(588)
        koy_evleri(img, 420, 800, zemin, 2.2, tohum=43, kerpic="#b8a890")
        for x in (60, 160, 260):
            figur(img, cam, x, zemin, 1.6, renk="#3a4a3a", isik="#4a5a4a", kontur="#141a14")

    orta(43, (526, 560), ["#7a7a58", "#6e6e4e", "#626246", "#56563e", "#4a4a36"], "#a8a880", ekle=kasaba)
    on(43, ["#4a4a36", "#626246", "#5a5a4a"], "#c8c8a8")

    def kare(t, z, i):
        f = i / KARE
        figur(t, tahtirevan, 250, z, 2.4, 1, f)
        for x, ff in ((140, 0.0), (400, 0.5)):
            figur(t, atli, x, z, 2.1, 1, (f + ff) % 1, "#3a2418", "#140a06", "#5a3a3a", "kalpak", "#3a2a1a", "#2a1a12", silah=None, adim=0.4)

    sprite(43, "karakter", 520, 170, KARE, kare)


# ================================================================ BÖLÜM 3 · Lanetli Mezar


def ic_mekan(no, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a", pencere=None, zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060", hali=False):
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
        if pencere:  # kemer içinde pencere: açık taş söve, cam, kayıtlar; içeri düşen ışık huzmesi duvarda okunur
            sove = hex2(_ac(duvar[2], 0.35))
            d.rectangle([x + 23, 340, x + 67, 444], fill=sove)
            d.chord([x + 23, 312, x + 67, 364], 180, 360, fill=sove)
            d.rectangle([x + 26, 340, x + 64, 440], fill=hex2(pencere[0]))
            d.chord([x + 26, 316, x + 64, 360], 180, 360, fill=hex2(pencere[0]))
            rnd = random.Random(x)
            for _ in range(90):  # pencerede kar: yoğun taneler, alt kenarda birikinti
                piksel(u, x + rnd.randint(27, 63), rnd.randint(322, 438), hex2(pencere[1]))
            d.chord([x + 24, 432, x + 66, 452], 180, 360, fill=hex2(pencere[1]))
            d.line([x + 45, 318, x + 45, 440], fill=hex2(kemer), width=2)
            d.line([x + 26, 390, x + 64, 390], fill=hex2(kemer), width=2)
            d.rectangle([x + 23, 444, x + 67, 447], fill=hex2(_ac(duvar[2], 0.5)))  # pencere denizliği
            for k in range(0, 40, 2):  # pencereden duvara düşen soluk ışık huzmesi (dither)
                for yy in range(448, 600, 3):
                    if _esik(x + 26 + k, yy) < 0.18 * (1 - (yy - 448) / 160):
                        piksel(u, x + 26 + k + (yy - 448) // 12, yy, hex2(pencere[1], 40))
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
    if hali:  # desenli kilim: baklava motifleri ve altın şeritler
        for y in range(604, H, 30):
            d.line([0, y, GW, y], fill=hex2("#e0b040"))
            for x in range(0, GW, 30):
                cx, cy = x + 15, y + 15
                d.polygon([(cx, cy - 8), (cx + 8, cy), (cx, cy + 8), (cx - 8, cy)], fill=hex2(_ac(zemin_renk[0], -0.3)))
                d.polygon([(cx, cy - 4), (cx + 4, cy), (cx, cy + 4), (cx - 4, cy)], fill=hex2("#2a4a7a"))
    else:
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
    """Açılmış mezar sandığı: yere oturur; içi karanlık, iskelet sandığın içinde yatar (sağ bacak dizden eğri: aksaklık,
    sağ kolda yara izi)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 30 * s)
    temas_golgesi(img, x, y, 34 * s)
    d.rectangle([x - int(16 * s), y - int(12 * s), x + int(16 * s), y - 1], fill=hex2("#2a1a12"), outline=hex2("#0a0604"))
    d.rectangle([x - int(15 * s), y - int(11 * s), x + int(15 * s), y - int(3 * s)], fill=hex2("#0e0806"))  # sandığın içi
    for k in range(3):  # sandığın ön yüzünde ahşap damarları
        d.line([x - int(15 * s), y - int(2.5 * s) + k, x + int(15 * s), y - int(2.5 * s) + k], fill=hex2(("#3a2418", "#2a1a12", "#1e120c")[k]))
    if acik:
        k = hex2("#e8e0c8")
        kg = hex2("#b8b098")  # kemik gölgesi
        ic = y - int(7 * s)  # iskeletin omurga hattı: sandığın dibinde, kutunun içinde yatar
        for r in range(1, 4):  # iskelet çevresinde hafif parlama (lamba ışığı kemiklerde)
            for a in range(0, 360, 10):
                px_, py_ = x - int(1 * s) + math.cos(math.radians(a)) * (12 + r * 1.4) * s, ic + math.sin(math.radians(a)) * (2.6 + r) * s
                if y - int(11 * s) < py_ < y - int(3 * s) and _esik(int(px_), int(py_)) < 0.5 * (1 - r / 4):
                    piksel(img, px_, py_, hex2("#fff0a0", 60))
        # kafatası: yuvarlak kubbe, göz çukuru, çene
        d.ellipse([x - int(14.5 * s), ic - int(3 * s), x - int(10 * s), ic + int(1.2 * s)], fill=k)
        d.rectangle([x - int(13 * s), ic + int(0.4 * s), x - int(10.5 * s), ic + int(2 * s)], fill=kg)  # çene
        d.ellipse([x - int(12.8 * s), ic - int(1.6 * s), x - int(11.4 * s), ic - int(0.2 * s)], fill=hex2("#2a2018"))  # göz çukuru
        piksel(img, x - int(11 * s), ic + int(0.2 * s), hex2("#2a2018"))  # burun boşluğu
        d.line([x - int(10 * s), ic, x + int(1 * s), ic], fill=k, width=max(1, int(s)))  # omurga
        for i in range(5):  # kaburga kafesi: omurgadan kıvrılan yaylar
            kx = x - int((9 - i * 1.6) * s)
            d.arc([kx - int(1.2 * s), ic - int(2.6 * s), kx + int(1.2 * s), ic + int(2.6 * s)], 250, 110, fill=k, width=max(1, int(0.6 * s)))
        d.ellipse([x - int(0.5 * s), ic - int(2 * s), x + int(3 * s), ic + int(2 * s)], outline=k, width=max(1, int(0.7 * s)))  # leğen
        # sol kol: omuzdan düz; sağ kol (önde, izleyiciye yakın): dirsekten kırık, yara izi
        d.line([x - int(9 * s), ic - int(1.5 * s), x - int(1 * s), ic - int(2.2 * s)], fill=kg, width=max(1, int(0.6 * s)))
        d.line([x - int(9 * s), ic + int(1.5 * s), x - int(6 * s), ic + int(2.8 * s), x - int(2 * s), ic + int(2.2 * s)], fill=k,
               width=max(1, int(0.7 * s)))
        d.ellipse([x - int(7 * s), ic + int(1.8 * s), x - int(5 * s), ic + int(3.6 * s)], fill=hex2("#6a2418"))  # dirsekteki yara: koyu kızıl iz
        piksel(img, x - int(6 * s), ic + int(2.6 * s), hex2("#a84a3a"))
        d.line([x + int(3 * s), ic - int(1 * s), x + int(13 * s), ic - int(1.4 * s)], fill=kg, width=max(1, int(0.8 * s)))  # sol bacak düz
        # sağ bacak (önde): dizden belirgin eğri, kısa kalmış (aksaklık)
        d.line([x + int(3 * s), ic + int(1 * s), x + int(7 * s), ic + int(3 * s), x + int(11 * s), ic + int(1.2 * s)], fill=k,
               width=max(1, int(0.9 * s)))
        d.ellipse([x + int(6.2 * s), ic + int(2.2 * s), x + int(7.8 * s), ic + int(3.8 * s)], fill=k)  # diz eklemi
        for ex_, ey_ in ((x + int(13 * s), ic - int(1.4 * s)), (x + int(11 * s), ic + int(1.2 * s))):
            d.line([ex_, ey_, ex_ + int(1.5 * s), ey_], fill=k, width=max(1, int(0.6 * s)))  # ayak kemikleri
    else:
        d.rectangle([x - int(17 * s), y - int(11 * s), x + int(17 * s), y - int(8 * s)], fill=hex2("#1e5a3a"), outline=hex2("#0a2a1a"))

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


def sahne44():
    """Akşehir, 8 Mart 1403: esir Bayezid, sade bir odada ahşap sedirde son nefesini verir; mum söner gibi titrer, kapıda muhafız."""
    ic_mekan(44, ("#1e1a26", "#2a2432", "#342c3c"), kemer="#141018", cini="#2a6a3a", pencere=("#3a3050", "#a8a0c8"),
             zemin_renk=("#4a3c30", "#3e3228", "#322820"))

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        y = z[0]
        # kapı: taş söveli kemerli kapı, aralık; eşiği zemine basar
        d.rectangle([82, y - 50, 112, y - 1], fill=hex2("#5a4a40"))
        d.chord([82, y - 62, 112, y - 38], 180, 360, fill=hex2("#5a4a40"))
        d.rectangle([86, y - 48, 108, y - 1], fill=hex2("#0e0a10"))
        d.chord([86, y - 58, 108, y - 38], 180, 360, fill=hex2("#0e0a10"))
        d.rectangle([98, y - 48, 108, y - 1], fill=hex2("#3a2a1a"))  # yarı açık ahşap kanat
        d.line([98, y - 48, 98, y - 1], fill=hex2("#6a4a2a"))
        figur(t, kisi, 128, z, 2.9, "#1e4a7a", "kalpak", "#3a2a1a", "#2a1a12", yon=1, silah="mizrak")  # kapıdaki muhafız
        figur(t, yatan, 222, z, 3.6, govde="#2a6a3a", bas="sarik", bas_renk="#f4f0e6", sakal="#2a1a14", nefes=0.3 + 0.3 * math.sin(f * 2 * math.pi))
        mumluk(t, 290, z, f, 1)  # yatağın yanında tek mum: söner gibi titrer
        if int(f * 24) % 24 in (7, 8, 15):
            d.rectangle([288, y - 40, 292, y - 30], fill=hex2("#1e1a26", 0))

    sprite(44, "karakter", 400, 140, KARE, kare)


def tabela(img, x, zemin, ad):
    """Köy girişinde ahşap tabela: iki direk zemine dikili, üstünde piksel yazılı levha."""
    from PIL import Image, ImageFont
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 30)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
    w = int(d.textlength(ad, font=font)) + 8
    for px_ in (x - w // 2 + 3, x + w // 2 - 3):
        d.line([px_, y - 1, px_, y - 24], fill=hex2("#4a2a16"), width=2)
    d.rectangle([x - w // 2, y - 38, x + w // 2, y - 22], fill=hex2("#a8784a"), outline=hex2("#3a2010"))
    yazi = Image.new("L", (w, 16))
    ImageDraw.Draw(yazi).text((4, 1), ad, font=font, fill=255)
    for yy in range(16):
        for xx in range(w):
            if yazi.getpixel((xx, yy)) > 60:  # eşik düşük: İ'nin noktası gibi ince ayrıntılar silinmesin
                piksel(img, x - w // 2 + xx, y - 38 + yy, hex2("#2a140a"))
    temas_golgesi(img, x, y, w)


def sahne51():
    """Semerkant dolayı: 'Bağdat', 'Dımaşk', 'Şiraz', 'Mısır' adlı köyler; sürgün ustalar deve kervanıyla gelir."""
    gokyuzu(51, ["#3a7ac8", "#5a98d8", "#8ab8e0", "#c8d8d8", "#f0e0b8"], (460, 300, 18, ["#fff8e0", "#fff0b0"]),
            [(120, 300, 38), (330, 335, 26)])
    uzak(51, ["#8a98b8", "#7a88a8"], ["#9aa878", "#8a986a"], ["#a8b070", "#98a062", "#889256"])

    def sehir(img, z):
        zemin = duz(588)
        orta_asya_sehri(img, 460, 800, zemin, 2.7, tohum=51, kubbe="#2a8ac8")
        koy_evleri(img, 10, 180, zemin, 2.2, tohum=51)
        koy_evleri(img, 230, 420, zemin, 2.2, tohum=52)
        for x in (200, 440):
            figur(img, agac_kavak, x, zemin, 1.5)
        for x, ad in ((322, "BAĞDAT"), (384, "DIMAŞK"), (444, "ŞİRAZ"), (502, "MISIR")):  # dördü de kamera kayarken görünen bantta
            tabela(img, x, zemin, ad)

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
        figur(img, bibi_hanim, 470, duz(588), 1.5, catlak=1.0)

    orta(52, (530, 560), ["#c8b078", "#b8a06a", "#a8905e", "#988052", "#887046"], "#e8d098", ekle=cami)
    on(52, ["#887046", "#a8905e", "#8a7a4a"], "#f0e0a8")

    def kare(t, z, i):
        f = i / KARE
        figur(t, tas_arabasi, 125, z, 2.0, 1, f)
        figur(t, fil, 220, z, 2.5, 1, f, kule=False, binici="#5a3a3a")
        d0 = ImageDraw.Draw(t)
        d0.line([164, z[0] - 26, 184, z[0] - 30], fill=hex2("#3a2418"), width=2)  # koşum: araba okundan filin göğüs kayışına
        d0.line([184, z[0] - 30, 196, z[0] - 34], fill=hex2("#3a2418"), width=2)
        # Timur at üstünde: kolu kapıyı gösterir (ağır gövdeli beyaz at, kızıl kaftan, sorguçlu külah)
        figur(t, atli, 290, z, 2.6, 1, 0.0, "#d8d0c4", "#8a8078", "#7a1e22", "sorguc", "#2a1a14", "#a8522a", kol=0.8, dur=True, cul="#3a2a5a")
        figur(t, kisi, 350, z, 2.4, "#5a4a3a", "takke", "#2a5a3a", "#3a2a1a", yon=-1, diz=True)  # mimar diz çökmüş, Timur'a dönük
        for j, x in enumerate((318, 334)):  # kazmalı işçiler taç kapının dibinde, Timur'un buyruğuyla kapıyı yıkar
            figur(t, kisi, x, z, 2.4, "#5a4a3a", "takke", "#2a5a3a", "#3a2a1a", yon=1, silah="kazma", kol=abs(math.sin((f * 2 + j * 0.5) * math.pi)) * 0.9)
        u = (f * 1.5) % 1  # taç kapıdan kopan tuğlalar düşer, yere değince toz kalkar
        for k in range(3):
            v = (u + k * 0.3) % 1
            bx, by = 286 + k * 12, 20 + v * (z[0] - 26)
            ImageDraw.Draw(t).rectangle([bx, by, bx + 5, by + 3], fill=hex2("#c88a5a"), outline=hex2("#5a3a22"))
            if v > 0.85:
                for m in range(5):
                    piksel(t, bx + 2 + (m - 2) * 3, z[0] - 2 - (v - 0.85) * 40 - m % 2 * 2, hex2("#d8c0a0", 160))

    sprite(52, "karakter", 480, 200, KARE, kare)


def sahne53():
    """Kânigil şöleni, Eylül 1404: ipek otağlar, at eti çevrilen ateş, müzisyenler; Kastilyalı elçiler gelir."""
    gokyuzu(53, ["#4a7ab8", "#6a98c8", "#a0b8d0", "#e0d8c0", "#f8e0a8"], (440, 470, 18, ["#fff2c0", "#ffd890"]),
            [(130, 300, 34), (330, 335, 24)])
    uzak(53, ["#8a98b8", "#7a88a8"], ["#8aa080", "#7a9070"], ["#9ab07a", "#8aa46c", "#7a985e"])

    def otaglar(img, z):
        zemin = duz(588)  # ipek otağlar düz çayırda, kadrajın görünen bandında (orta x = ızgara x + 135)
        for x, renk in ((300, "#2a6a9a"), (395, "#e0b040"), (490, "#7a2a8a"), (40, "#c8302a"), (660, "#2a8a5a"), (760, "#c8302a")):
            figur(img, otag, x, zemin, 2.0, renk, "#f4ecd8")

    orta(53, (520, 557), ["#7aa84a", "#6a9a3e", "#5a8a36", "#4a7a2e", "#3f6b2a"], "#a8d063", ekle=otaglar)
    on(53, ["#3f6b2a", "#5a8f36", "#8a7a3a"], "#d8e070")

    def kare(t, z, i):
        f = i / KARE
        figur(t, otag, 105, z, 1.9, "#c8302a", "#f4ecd8", faz=f, acik=True)  # ipek otağ düz çayıra kurulu
        d = ImageDraw.Draw(t)
        y = z[0]
        ates(t, 150, z, f, 1.3)
        d.line([132, y - 30, 168, y - 30], fill=hex2("#4a2a16"), width=2)  # şiş
        for yx in (134, 166):
            d.line([yx, y - 1, yx, y - 32], fill=hex2("#4a2a16"), width=2)  # çatal direkler zemine dikili
        d.ellipse([132, y - 40, 168, y - 22], fill=hex2("#8a3a1a"))  # çevrilen at eti: şişe geçirilmiş, ateşin üstünde
        d.ellipse([138, y - 36, 152, y - 28], fill=hex2("#a8502a"))
        # uzun sofra: yere serili desenli örtü (dastarhan), figürlerin önünde; üstünde kâseler ve ekmek
        d.rectangle([184, y - 11, 336, y - 1], fill=hex2("#e8dcc0"), outline=hex2("#8a6a3a"))
        for k in range(188, 336, 12):
            d.rectangle([k, y - 9, k + 5, y - 3], fill=hex2("#c8302a"))
        for k in range(11):
            d.ellipse([189 + k * 13, y - 15, 198 + k * 13, y - 10], fill=hex2(("#c8a040", "#e8e0d0", "#8a3a1a", "#6aa040")[k % 4]), outline=hex2("#5a3a1a"))
        for j, x in enumerate((200, 228)):
            figur(t, oturan, x, z, 2.7, ("#2a5a8a", "#7a2a5a")[j], "kalpak", "#3a2a1a", "#2a1a12", yon=1, el="kase", minder="#c8a040")
        figur(t, oturan, 262, z, 3.1, "#7a1e22", "sorguc", "#2a1a14", "#d8d0c8", yon=1, el="kase", minder="#9a2a2a")
        for j, x in enumerate((296, 324)):  # Kastilyalı elçiler (Clavijo) sofraya oturur
            figur(t, oturan, x, z, 2.8, ("#1a1a2a", "#3a1a1a")[j], "sapka", "#1a1a1a", "#3a2a1a", yon=-1, el="kase")
        figur(t, kisi, 176, z, 2.7, "#5a3a6a", "takke", "#2a5a3a", "#2a1a12", yon=1, silah="yay", kol=0.4 + 0.2 * math.sin(f * 25))  # müzisyen
        figur(t, kisi, 342, z, 2.7, "#3a5a4a", "takke", "#e8e0d0", None, yon=-1, kol=0.5)  # tepsili hizmetkâr: tepsi elinde
        d.rectangle([323, y - 34, 341, y - 32], fill=hex2("#e0b040"))  # tepsi
        for k in range(3):
            d.ellipse([324 + k * 6, y - 37, 328 + k * 6, y - 34], fill=hex2(("#c8302a", "#6aa040", "#e8e0d0")[k]))

    sprite(53, "karakter", 420, 190, KARE, kare)


def yasli_timur_yakin(img, x, zemin, f):
    """Yakın plan: minderde oturan yaşlı Timur, büyük ölçekte. Ağarmış sakal ve bıyık, ağır ve düşük göz kapakları, yavaş göz
    kırpışı; kürklü külahın altın şeridi alnın üstünde. Minder zemine oturur."""
    d = ImageDraw.Draw(img)
    s = 8.0
    y = zemin_y(zemin, x, 90)
    temas_golgesi(img, x, y, 100)
    d.rectangle([x - 46, y - 12, x + 46, y - 1], fill=hex2("#c8a040"), outline=hex2("#5a3a10"))  # minder
    y -= 12
    nefes = int(math.sin(f * 2 * math.pi) * 1.5)
    d.ellipse([x - 44, y - 26, x + 44, y], fill=hex2("#5a1418"))  # bağdaş
    d.polygon([(x - 34, y - 14), (x - 24, y - 92 - nefes), (x + 24, y - 92 - nefes), (x + 34, y - 14)], fill=hex2("#7a1e22"))  # kaftan
    d.line([x - 28, y - 58, x + 28, y - 58], fill=hex2("#e0b040"), width=4)  # altın kemer
    d.polygon([(x - 26, y - 92), (x - 40, y - 60), (x - 30, y - 30), (x - 20, y - 88)], fill=hex2("#3a2a5a"))  # pelerin
    for k in range(-20, 21, 8):  # kaftan kıvrımları
        d.line([x + k, y - 80, x + k * 1.3, y - 20], fill=hex2("#5a1418"))
    by = y - 112 - nefes  # baş merkezi
    d.ellipse([x - 17, by - 18, x + 17, by + 18], fill=hex2("#c8946a"))  # yüz
    d.ellipse([x - 14, by - 14, x - 4, by + 2], fill=hex2("#d6a07a"))  # yanak ışığı
    # göz: beyaz, iris; üstte ağır düşük kapak, altta torba
    for gx in (x - 2, x + 10):
        kirp = int(f * 24) % 24 < 2
        d.ellipse([gx - 5, by - 4, gx + 5, by + 3], fill=hex2("#efe8dc"))  # göz akı
        d.ellipse([gx - 2, by - 2, gx + 2, by + 2], fill=hex2("#2a1a10"))  # iris
        piksel(img, gx + 1, by - 1, hex2("#f8f4ec"))
        # ağır, düşük göz kapağı: gözün üst yarısına inen kıvrımlı deri; alt kenarı 1 px koyu kontur, üstü ışıklı
        kapak_alt = by + 2 if kirp else by - 1
        d.chord([gx - 6, by - 8, gx + 6, kapak_alt + 4], 180, 360, fill=hex2("#b8805a"))
        d.rectangle([gx - 6, by - 4, gx + 6, kapak_alt], fill=hex2("#b8805a"))
        d.line([gx - 6, kapak_alt, gx + 6, kapak_alt], fill=hex2("#3a2010"))
        d.line([gx - 4, by - 7, gx + 4, by - 7], fill=hex2("#d6a07a"))  # kapak üstü ışık
        d.arc([gx - 5, by - 1, gx + 5, by + 7], 0, 180, fill=hex2("#9a6a4a"))  # göz altı torbası
        d.line([gx - 6, by - 11, gx + 6, by - 10], fill=hex2("#e8e4dc"), width=2)  # ağarmış kaş
    d.polygon([(x + 4, by - 2), (x + 9, by + 8), (x + 3, by + 8)], fill=hex2("#a8704a"))  # burun
    d.polygon([(x - 16, by + 6), (x + 18, by + 6), (x + 12, by + 30), (x + 2, by + 40), (x - 10, by + 30)], fill=hex2("#e8e4dc"))  # sakal
    d.line([x - 2, by + 11, x + 16, by + 11], fill=hex2("#d0ccc4"), width=3)  # bıyık
    d.line([x + 2, by + 14, x + 10, by + 14], fill=hex2("#6a3020"), width=2)  # ağız
    d.chord([x - 20, by - 36, x + 20, by - 4], 180, 360, fill=hex2("#2a1a14"))  # kürklü külah
    d.rectangle([x - 20, by - 22, x + 20, by - 16], fill=hex2("#e0b040"))  # altın şerit alnın üstünde
    d.ellipse([x - 3, by - 24, x + 3, by - 18], fill=hex2("#c8302a"))
    for k in range(12):  # sorguç tüyü
        piksel(img, x - 4 - k // 3, by - 36 - k, hex2("#f4f0e6"))
        piksel(img, x - 3 - k // 3, by - 36 - k, hex2("#d8d0c0"))
    d.line([x + 22, y - 82, x + 36, y - 46], fill=hex2("#5a1418"), width=8)  # kol: omuzdan dize iner
    d.ellipse([x + 30, y - 50, x + 44, y - 36], fill=hex2("#c8946a"))  # el dizin üstünde, kolun ucunda
    d.line([x + 34, y - 44, x + 42, y - 40], fill=hex2("#a8704a"))  # parmak aralığı


def sahne54():
    """Yakın plan: otağın içinde yaşlı Timur; göz kapakları düşmüş, sakalı ağarmış."""
    ic_mekan(54, ("#2a0e0e", "#3a1414", "#4a1a1a"), kemer="#1a0808", cini="#c8a040", zemin_renk=("#9a2a2a", "#8a2424", "#7a1e1e"), hali=True)

    def kare(t, z, i):
        f = i / KARE
        figur(t, yasli_timur_yakin, 135, z, f)
        d = ImageDraw.Draw(t)  # buhurdan: ayaklı tunç kap zemine oturur, dumanı yukarı
        temas_golgesi(t, 200, z[0], 14)
        d.rectangle([194, z[0] - 4, 206, z[0] - 1], fill=hex2("#5a4a2a"))
        d.ellipse([190, z[0] - 16, 210, z[0] - 4], fill=hex2("#c8a040"), outline=hex2("#5a3a10"))
        d.ellipse([196, z[0] - 20, 204, z[0] - 14], fill=hex2("#e8601c"))
        for k in range(8):  # buhurdan dumanı
            u = (f + k / 8) % 1
            piksel(t, 200 + math.sin(u * 8) * 4, z[0] - 30 - u * 60, hex2("#d8d0c8", int(160 * (1 - u))))

    sprite(54, "karakter", 270, 200, KARE, kare)


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
             zemin_renk=("#4a2a2a", "#3e2424", "#321e1e"), hali=True)

    def kare(t, z, i):
        f = i / KARE
        figur(t, yatan, 190, z, 3.4, nefes=0.5 + 0.5 * math.sin(f * 2 * math.pi))
        for j, x in enumerate((104, 282)):
            figur(t, kisi, x, z, 2.8, ("#e8e0d0", "#3a4a5a")[j], "sarik", "#f4f0e6", "#d8d0c8", yon=1 if x < 190 else -1, diz=True)
        d = ImageDraw.Draw(t)
        d.chord([124, z[0] - 10, 150, z[0] + 4], 180, 360, fill=hex2("#c8c0b0"))  # buz dolu leğen
        for k in range(4):
            d.rectangle([128 + k * 5, z[0] - 9, 131 + k * 5, z[0] - 6], fill=hex2("#e0f0ff"))
        mumluk(t, 85, z, f, 3)  # ayaklı şamdan: üç mum, ateşli hastanın başucunda titreyen ışık
        mumluk(t, 296, z, f + 0.3, 2)
        mangal(t, 250, z, f)

    sprite(56, "karakter", 380, 140, KARE, kare)


def mumluk(t, x, z, f, adet=3):
    """Ayaklı şamdan: tunç ayak zemine basar, mumlar titrer ve çevresine sıcak ışık halkası düşer."""
    d = ImageDraw.Draw(t)
    y = z[0]
    temas_golgesi(t, x, y, 14)
    d.rectangle([x - 6, y - 3, x + 6, y - 1], fill=hex2("#6a5a2a"))
    d.line([x, y - 3, x, y - 22], fill=hex2("#c8a040"), width=2)
    d.line([x - 7, y - 22, x + 7, y - 22], fill=hex2("#c8a040"), width=2)
    for k in range(adet):
        mx = x + (k - (adet - 1) / 2) * 7
        d.rectangle([mx - 1, y - 30, mx + 1, y - 22], fill=hex2("#f0e8d0"))
        alev = 1.5 + math.sin(f * 30 + k * 2) * 0.8
        d.polygon([(mx - 2, y - 30), (mx, y - 30 - alev * 3), (mx + 2, y - 30)], fill=hex2("#f8c040"))
        piksel(t, mx, y - 31, hex2("#fff4c0"))
    for r in range(6, 26, 3):  # ışık halkası (dither)
        for a in range(0, 360, 12):
            px_, py_ = x + math.cos(math.radians(a)) * r * 1.4, y - 30 + math.sin(math.radians(a)) * r
            if py_ < y - 1 and _esik(int(px_), int(py_)) < 0.45 * (1 - r / 26):
                piksel(t, px_, py_, hex2("#f8d070", 70))


def mangal(t, x, z, f):
    """Kömür mangalı: üç ayak zemine basar, korlar kızarır, ince duman yukarı çıkar."""
    d = ImageDraw.Draw(t)
    y = z[0]
    temas_golgesi(t, x, y, 18)
    for dx in (-6, 0, 6):
        d.line([x + dx, y - 1, x + dx // 2, y - 7], fill=hex2("#4a3a2a"), width=2)
    d.ellipse([x - 9, y - 12, x + 9, y - 5], fill=hex2("#5a4a3a"), outline=hex2("#2a1a10"))
    for k in range(5):
        kor = 0.6 + 0.4 * math.sin(f * 20 + k)
        piksel(t, x - 5 + k * 2.5, y - 10, hex2(_ac("#e8601c", kor - 0.6)))
    for k in range(6):
        u = (f + k / 6) % 1
        piksel(t, x + math.sin(u * 9) * 2, y - 14 - u * 30, hex2("#c8c0b8", int(120 * (1 - u))))


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
        figur(t, kagni, 190, z, 2.4, 1, f, yuk="#1a1210")
        figur(t, okuz_, 270, z, 2.3, 1, f)
        ImageDraw.Draw(t).line([247, z[0] - 19, 252, z[0] - 20], fill=hex2("#3a2418"), width=2)  # boyunduruk bağı
        for j, x in enumerate((95, 130, 160)):
            figur(t, kisi, x, z, 2.4, ("#2a2420", "#d8d0c0", "#3a2a2a")[j], "kalpak", "#2a2a2a", "#2a1a12", yon=1, adim=(f + j * 0.3) % 1)
        figur(t, atli, 340, z, 2.6, 1, f, "#2a1810", "#140a06", "#2a2a2a", "kalpak", "#1a1a1a", silah="mizrak", bayrak="#f4f0e6", adim=0.4)

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
        gur_i_emir(img, 405, zemin, 2.0)
        koy_evleri(img, 10, 250, zemin, 2.1, tohum=58, kerpic="#c8b898")
        koy_evleri(img, 560, 800, zemin, 2.1, tohum=59, kerpic="#c8b898")

    orta(58, (526, 560), ["#c8ccd4", "#bcc0c8", "#b0b4bc", "#a4a8b0", "#989ca4"], "#f4f8ff", ekle=turbe)
    kar_ortusu(58)
    on(58, ["#989ca4", "#b0b4bc", "#8a8e98"], "#ffffff")
    hava(58, "kar", 160, "#ffffff")

    def kare(t, z, i):
        f = i / KARE
        rnd = random.Random(58)
        dd = ImageDraw.Draw(t)
        for j, x in enumerate((236, 258, 280, 302)):  # abanoz tabutu omuzlarında taşıyanlar
            figur(t, kisi, x, z, 2.5, ("#2a2a3a", "#3a2a2a", "#2a3a2a", "#3a3a3a")[j], "sarik", "#f4f0e6", "#3a2a1a", yon=1, adim=(i / KARE + j * 0.25) % 1)
        om = z[0] - int(11 * 2.5) - 2
        abanoz_tabut(dd, 226, 312, om)
        for j, x in enumerate(range(30, 520, 34)):
            if abs(x - 270) > 70:
                figur(t, kisi, x, z, 2.3, rnd.choice(("#2a2420", "#d8d0c0", "#3a2a2a")), rnd.choice(("sarik", "kalpak", "ortu")),
                      rnd.choice(("#f4f0e6", "#2a2a2a")), None, yon=1 if x < 270 else -1, kadin=j % 3 == 0)

    sprite(58, "karakter", 520, 150, KARE, kare)


def sahne59():
    """Koyu yeşil yeşim taşı: 1740'ta Nadir Şah'ın askerleri taşı götürmek ister, taş çatlar."""
    ic_mekan(59, ("#0e1a1a", "#162424", "#1e2e2e"), kemer="#081010", cini="#1e5a6a", zemin_renk=("#2a3030", "#222828", "#1a2020"),
             isik="#80e0a0", hali=True)

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        y = z[0]
        for kx, faz in ((200, 0.0), (300, 0.4)):  # tavandan sarkan kandiller: zincir sprite'ın üst kenarından iner
            kandil(t, kx, 0, f + faz, zincir=222)
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
        figur(t, kisi, 305, z, 2.7, "#2a3a6a", "tac", "#e0b040", "#2a1a12", yon=-1, pelerin="#c8a040")  # Nadir Şah

    sprite(59, "karakter", 400, 320, KARE, kare)


def kandil(t, x, ust, f, zincir=36):
    """Tavandan zincirle sarkan yağ kandili: pirinç gövde, titreyen alev, çevresine yeşil-sarı ışık halkası."""
    d = ImageDraw.Draw(t)
    sal = math.sin(f * 2 * math.pi) * 1.5
    for k in range(0, zincir, 3):
        piksel(t, x + sal * k / zincir, ust + k, hex2("#8a7a4a"))
    ky = ust + zincir
    kx = x + sal
    d.polygon([(kx - 7, ky), (kx + 7, ky), (kx + 4, ky + 8), (kx - 4, ky + 8)], fill=hex2("#c8a040"), outline=hex2("#5a3a10"))
    d.rectangle([kx - 2, ky + 8, kx + 2, ky + 11], fill=hex2("#8a6a2a"))
    alev = 1.5 + math.sin(f * 30) * 0.7
    d.polygon([(kx - 2, ky), (kx, ky - alev * 3), (kx + 2, ky)], fill=hex2("#f8c040"))
    for r in range(5, 24, 3):
        for a in range(0, 360, 12):
            px_, py_ = kx + math.cos(math.radians(a)) * r * 1.3, ky + math.sin(math.radians(a)) * r
            if _esik(int(px_), int(py_)) < 0.45 * (1 - r / 24):
                piksel(t, px_, py_, hex2("#e8e090", 60))


def sahne60():
    """Haziran 1941: Gerasimov'un ekibi lambalar altında mezarı açar; kameraman çeker; iskelette aksak sağ bacak."""
    ic_mekan(60, ("#141414", "#1e1c1a", "#282420"), kemer="#0e0c0a", cini="#1e4a6a", zemin_renk=("#3a342c", "#302a24", "#26221c"),
             isik="#fff0a0")

    def kare(t, z, i):
        f = i / KARE
        figur(t, tabut, 236, z, 4.2, True)
        dd = ImageDraw.Draw(t)
        temas_golgesi(t, 140, z[0], 18)  # Uluğ Bey'in ayrı duran kafatası: sandığın solunda, lamba ışığında açıkta
        dd.ellipse([132, z[0] - 13, 148, z[0] - 1], fill=hex2("#e8e0c8"), outline=hex2("#4a4030"))
        dd.ellipse([135, z[0] - 9, 139, z[0] - 5], fill=hex2("#2a2018"))
        dd.ellipse([141, z[0] - 9, 145, z[0] - 5], fill=hex2("#2a2018"))
        dd.line([136, z[0] - 3, 144, z[0] - 3], fill=hex2("#4a4030"))
        figur(t, lamba, 118, z, 2.2, f)
        figur(t, lamba, 342, z, 2.2, (f + 0.4) % 1)
        figur(t, kisi, 160, z, 2.7, "#5a5a4a", "kasket", "#3a3a32", "#5a4a3a", yon=1, diz=True)  # Gerasimov diz çökmüş, sandığa eğik
        figur(t, kisi, 316, z, 2.7, "#e8e4dc", None, None, None, yon=-1, kol=0.2, kemer=None)
        figur(t, kisi, 330, z, 2.7, "#3a3a2a", "kasket", "#4a4a3a", None, yon=-1, silah="kamera")  # Kayumov

    sprite(60, "karakter", 460, 170, KARE, kare)


def sahne61():
    """Çayhane: tahta sedirde oturan yaşlılar kameraman Kayumov'u uyarır: 'Mezarı açarsanız savaş çıkar.'"""
    gokyuzu(61, ["#e0a060", "#e8b878", "#f0c890", "#f4d8a8", "#f8e4c0"], (420, 420, 22, ["#fff4d0", "#ffe0a0"]), [(130, 330, 30)])
    uzak(61, ["#c8a080", "#b89070"], ["#c8b080", "#b8a070"], ["#d8c090", "#c8b082", "#b8a074"])

    def mahalle(img, z):
        zemin = duz(588)
        koy_evleri(img, 10, 800, zemin, 4.0, tohum=61, kerpic="#d8b888")  # kapılar insandan biraz alçak (ölçek kuralı)

    orta(61, (528, 560), ["#c8a878", "#b8986c", "#a88860", "#987854", "#886848"], "#e8d0a0", ekle=mahalle)
    on(61, ["#886848", "#a88860", "#8a7a4a"], "#f0e0b0")

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        y = z[0]
        for ax in (106, 166, 226, 276):  # sedirin dört ayağı zemine basar
            d.rectangle([ax - 2, y - 16, ax + 2, y - 1], fill=hex2("#5a3a22"))
        d.rectangle([100, y - 20, 282, y - 16], fill=hex2("#7a4a2a"), outline=hex2("#2a1408"))
        d.rectangle([102, y - 22, 280, y - 20], fill=hex2("#9a2a2a"))
        ust = duz(y - 22, 420)
        for j, x in enumerate((130, 188, 262)):  # yaşlılar kameramana dönük
            figur(t, oturan, x, ust, 2.8, ("#2a3a5a", "#5a3a2a", "#3a5a4a")[j], "takke", ("#1a1a1a", "#2a5a3a", "#7a2a2a")[j], "#e8e4dc",
                  yon=1, el="kase" if j != 1 else None)
        sx_ = 226  # semaver: tepsi, pirinç gövde, musluk, baca; buharı yukarı
        d.rectangle([sx_ - 10, y - 24, sx_ + 10, y - 22], fill=hex2("#8a6a2a"))
        d.rectangle([sx_ - 6, y - 38, sx_ + 6, y - 24], fill=hex2("#c8a040"), outline=hex2("#5a3a12"))
        d.ellipse([sx_ - 7, y - 40, sx_ + 7, y - 34], fill=hex2("#d8b050"))
        d.rectangle([sx_ - 2, y - 46, sx_ + 2, y - 40], fill=hex2("#8a6a2a"))
        d.line([sx_ + 6, y - 30, sx_ + 10, y - 30], fill=hex2("#5a3a12"), width=2)  # musluk
        for k in range(6):
            u = (f + k / 6) % 1
            piksel(t, sx_ + math.sin(u * 7) * 3, y - 48 - u * 26, hex2("#f0f0f0", int(180 * (1 - u))))
        figur(t, kisi, 302, z, 3.0, "#3a3a2a", "kasket", "#4a4a3a", None, yon=-1, silah="kamera")  # Kayumov yaşlılara dönük

    sprite(61, "karakter", 420, 160, KARE, kare)


def sahne62():
    """22 Haziran 1941 şafağı: Alman tankları sınırı geçer; ufukta patlamalar."""
    gokyuzu(62, ["#2a2a3a", "#4a3a4a", "#7a4a4a", "#b86a4a", "#e8a060"], (430, 510, 18, ["#ffd090", "#f08040"]),
            [(140, 300, 40), (400, 320, 36)], ("#8a5a5a", "#6a4248", "#4a2a3a"))
    uzak(62, ["#4a4050", "#40384a"], ["#5a5a40", "#505036"], ["#6a7a40", "#5e6e38", "#526230"])

    def koyler(img, z):
        zemin = duz(588)
        koy_evleri(img, 560, 800, zemin, 3.2, tohum=62, kerpic="#a89880")
        d = ImageDraw.Draw(img)
        for k, x in enumerate((300, 420, 520)):  # ufuktaki yanan köyler: alev zemine oturur, duman alevin tabanından yükselir
            for rr, renk in ((14, "#e8601c"), (9, "#f8a030"), (4, "#fff0a0")):
                d.ellipse([x - rr * 1.6, 588 - rr, x + rr * 1.6, 588], fill=hex2(renk))
            duman(img, x, 580, 120, 62 + k, faz=0.3 * k, renk="#3a3434", ruzgar=0.5, genislik=1.6)
        for x in range(340, 500, 22):  # ufukta ilerleyen piyade silüetleri (ölçek için)
            figur(img, kisi, x, zemin, 1.2, "#3a3a34", "migfer", "#3a3a34", None, yon=1, silah="mizrak", kemer=None)

    orta(62, (526, 560), ["#6a8a40", "#5e7e38", "#527230", "#46662a", "#3a5a24"], "#a0b870", ekle=koyler)
    on(62, ["#3a5a24", "#527230", "#5a5a3a"], "#c0c888")

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
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
        gur_i_emir(img, 405, duz(588), 1.6)

    orta(63, (526, 560), ["#c8ccd4", "#bcc0c8", "#b0b4bc", "#a4a8b0", "#989ca4"], "#f4f8ff", ekle=turbe)
    kar_ortusu(63)
    silik_sehir(63)  # efsane vurgusu: ufukta rüya gibi silik Stalingrad silüeti (yıkık bloklar, fabrika bacaları)
    on(63, ["#989ca4", "#b0b4bc", "#8a8e98"], "#ffffff")
    hava(63, "kar", 140, "#ffffff")

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        xs = (190, 215, 240, 265)
        for j, x in enumerate(xs):
            figur(t, kisi, x, z, 2.4, ("#2a2a3a", "#3a2a2a", "#2a3a2a", "#3a3a3a")[j], "takke", "#1a1a1a", "#3a2a1a", yon=1, adim=(f + j * 0.25) % 1)
        omuz = z[0] - int(11 * 2.4) - 2
        abanoz_tabut(d, 180, 275, omuz)
        figur(t, kisi, 330, z, 2.6, "#e8e4dc", "sarik", "#f4f0e6", "#e8e4dc", yon=-1, kol=0.6)  # imam dua eder
        rnd = random.Random(63)
        for j, x in enumerate((96, 118, 140, 162, 356, 378, 400, 422, 444, 466)):  # ağır ağır dua eden kalabalık: eller açık, bazıları diz çökmüş
            figur(t, kisi, x, z, 2.4, rnd.choice(("#3a3a4a", "#2a2a2a", "#4a3a3a", "#d8d0c0")), rnd.choice(("kasket", "takke", "ortu", "kalpak")),
                  rnd.choice(("#3a3a3a", "#1a1a1a", "#e8e0d0")), None if j % 3 else "#d8d0c8", yon=1 if x < 200 else -1,
                  kol=0.5 + 0.1 * math.sin(f * 2 * math.pi + j), diz=j % 4 == 2, kadin=j % 5 == 1)

    sprite(63, "karakter", 500, 160, KARE, kare)


def abanoz_tabut(d, x0, x1, omuz):
    """Omuzlarda taşınan abanoz tabut: hacimli gövde, açık renk kapak kenarı, altın şerit ve köşe bağları; üst yüzü
    perspektifle görünür."""
    d.rectangle([x0, omuz - 12, x1, omuz], fill=hex2("#1a1210"), outline=hex2("#000000"))  # gövde
    d.polygon([(x0 + 3, omuz - 12), (x1 - 3, omuz - 12), (x1 - 7, omuz - 17), (x0 + 7, omuz - 17)], fill=hex2("#2e2420"), outline=hex2("#000000"))  # kapak
    d.line([x0 + 7, omuz - 17, x1 - 7, omuz - 17], fill=hex2("#5a4a40"))
    d.line([x0 + 1, omuz - 12, x1 - 1, omuz - 12], fill=hex2("#3a2e28"))
    for kx in (x0 + 10, (x0 + x1) // 2, x1 - 10):  # altın bağlar
        d.rectangle([kx - 2, omuz - 16, kx + 2, omuz], fill=hex2("#e0b040"))
        d.rectangle([kx - 1, omuz - 15, kx + 1, omuz - 1], fill=hex2("#a88020"))
    d.line([x0 + 4, omuz - 6, x1 - 4, omuz - 6], fill=hex2("#e0b040"))  # altın şerit


def silik_sehir(no, y0=560, alfa=70):
    """Uzak planın ufuk hattına silik bir savaş şehri silüeti işler (uzak katmanı yeniden işlenir): yıkık bloklar,
    fabrika bacaları, kırık çatılar; düşük alfa ile rüya gibi."""
    from PIL import Image
    yol = Path(__file__).parents[1] / "public" / f"sahne{no}-uzak.png"
    img = Image.open(yol).convert("RGBA")
    kat = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(kat)
    rnd = random.Random(no * 7)
    x = 0
    while x < img.width:
        w = rnd.randint(14, 34)
        h = rnd.randint(14, 48)
        d.rectangle([x, y0 - h, x + w, y0 + 30], fill=(40, 44, 60, alfa))
        if rnd.random() < 0.5:  # yıkık üst kenar
            for k in range(0, w, 4):
                d.rectangle([x + k, y0 - h - rnd.randint(0, 6), x + k + 2, y0 - h], fill=(40, 44, 60, alfa))
        if rnd.random() < 0.35:  # fabrika bacası
            bx = x + rnd.randint(2, max(3, w - 4))
            d.rectangle([bx, y0 - h - rnd.randint(14, 30), bx + 3, y0 - h], fill=(40, 44, 60, alfa))
        for _ in range(rnd.randint(0, 3)):  # kırık pencereler
            px0, py0 = x + rnd.randint(2, max(3, w - 4)), y0 - rnd.randint(6, max(7, h - 4))
            d.rectangle([px0, py0, px0 + 1, py0 + 2], fill=(90, 80, 70, alfa))
        x += w + rnd.randint(2, 10)
    img.alpha_composite(kat)
    img.save(yol)


def sahne64():
    """Taşkent bugün: Marx heykelinin yerinde atlı Emir Timur; 'Güç adalettedir'."""
    gokyuzu(64, ["#2a2a5a", "#4a3a6a", "#8a5a6a", "#d8885a", "#f0b070"], (440, 470, 18, ["#ffe0a0", "#f8a050"]),
            [])
    uzak(64, ["#8a98b8", "#7a88a8"], ["#7a9a78", "#6a8a6a"], ["#8aa070", "#7a9062", "#6a8256"])

    def meydan(img, z):
        zemin = duz(588)
        for x in range(10, 800, 34):
            figur(img, agac_kavak, x, zemin, 1.3 + (x % 3) * 0.1)

    orta(64, (526, 560), ["#8a7a6a", "#7a6a5c", "#6a5a50", "#5a4c44", "#4a3e38"], "#b8a890", ekle=meydan)
    on(64, ["#3a602a", "#5a8038", "#6a6a3a"], "#c8d888")

    def kare(t, z, i):
        f = i / KARE
        # Marx heykelinin silik hatırası: aynı kaidenin solunda yarı saydam gri büst (sakallı baş, geniş omuz), nabız gibi solar
        d = ImageDraw.Draw(t)
        alfa = int(120 + 45 * math.sin(f * 2 * math.pi))
        hy = z[0]
        gri = (196, 200, 212, alfa)
        d.rectangle([152, hy - 30, 180, hy - 1], fill=gri)  # sütun kaide
        d.rectangle([148, hy - 34, 184, hy - 30], fill=gri)
        d.polygon([(150, hy - 34), (182, hy - 34), (186, hy - 56), (146, hy - 56)], fill=gri)  # büst: geniş omuzlar, ceket
        d.rectangle([163, hy - 60, 169, hy - 54], fill=gri)  # boyun
        d.ellipse([154, hy - 82, 178, hy - 58], fill=gri)  # baş
        d.polygon([(154, hy - 66), (178, hy - 66), (174, hy - 52), (166, hy - 46), (158, hy - 52)], fill=(214, 218, 228, alfa))  # gür sakal
        d.chord([150, hy - 90, 182, hy - 62], 180, 360, fill=(214, 218, 228, alfa))  # kabarık saç
        d.rectangle([158, hy - 72, 162, hy - 69], fill=(80, 84, 96, alfa))  # gözler
        d.rectangle([170, hy - 72, 174, hy - 69], fill=(80, 84, 96, alfa))
        figur(t, heykel, 250, z, 3.4, tunc="#4a6a5a")
        for j, x in enumerate((112, 312, 336)):
            figur(t, kisi, x, z, 2.4, ("#3a5a8a", "#8a3a3a", "#e8e0d0")[j], None if j else "kasket", "#3a3a3a", None,
                  yon=1 if x < 200 else -1, adim=(f + j * 0.3) % 1 if j == 2 else None, kemer=None)
        for k in range(4):  # güvercinler
            u = (f + k / 4) % 1
            piksel(t, 120 + u * 200, 30 + math.sin(u * 12 + k) * 6 + k * 8, hex2("#e8e8f0"))

    sprite(64, "karakter", 420, 200, KARE, kare)


def sahne45():
    """Kasım 1404, Semerkant dışı, altın saat: yaşlı Timur ağır adımlarla doğuya yürür, sağ bacağını sürür (zeminde sürtünme izi),
    uzak planda belirgin dağ sırtı; tuğ taşıyan bir asker arkasından gelir."""
    gokyuzu(45, ["#4a5a9a", "#8a7aa0", "#d89a70", "#f0b878", "#f8d090"], (430, 440, 20, ["#fff0c0", "#ffc070"]),
            [(150, 300, 30)], ("#f8e0c8", "#e0b0a0", "#a87a80"))
    uzak(45, ["#6a5a7a", "#5a4a6a"], ["#8a7a5a", "#7a6a4e"], ["#a89060", "#988256", "#88744c"], dag_y=(290, 430))
    orta(45, (526, 560), ["#b89a58", "#a88a50", "#987a48", "#886a40", "#785a38"], "#e0c478")
    on(45, ["#785a38", "#987a48", "#8a6a3a"], "#f0d888")

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        y = z[0]
        for k in range(112, 262, 3):  # sürüyen sağ ayağın toprakta bıraktığı iz: figürün arkasında (sağda), soluklaşarak
            d.line([k, y - 1, k + 2, y - 1], fill=hex2("#5a3a1e", int(210 - 150 * (k - 112) / 150)))
            if k % 9 == 0:
                piksel(t, k, y - 2, hex2("#8a6a3a", 120))
        figur(t, timur, 100, z, 3.6, -1, adim=f, yasli=True, kol=0.1)  # dağ sırtına, uzak Çin'e doğru yürür
        figur(t, kisi, 180, z, 2.9, "#3a3a5a", "kalpak", "#2a1a14", "#2a1a12", yon=-1, adim=(f + 0.5) % 1, silah="mizrak")
        figur(t, tug, 172, z, 1.6, faz=f)
        for k in range(5):  # sürünen ayağın kaldırdığı ince toz
            u = (f * 2 + k / 5) % 1
            piksel(t, 110 + u * 14, y - 2 - u * 6, hex2("#c8a878", int(150 * (1 - u))))

    sprite(45, "karakter", 300, 150, KARE, kare)


def sahne46():
    """Sığınma: Kara Yusuf ile Ahmed Celayir atlarından inmiş, Bayezid'in önünde diz çökmüş; Bayezid yeşil otağının önünde
    ayakta, sancağı yanında, onlara dönük; atlar arkada durur, yoldan gelen toz çöker."""
    gokyuzu(46, ["#3a5a9a", "#5a7ab0", "#8aa0c0", "#c8c0b0", "#e8d0a8"], None, [(130, 300, 40), (420, 320, 30)])
    uzak(46, ["#7a8aa0", "#6a7a90"], ["#7a9068", "#6a805c"], ["#8aa060", "#7a9054", "#6a804a"])

    def kamp(img, z):
        zemin = duz(588)
        for x, renk in ((80, "#2a6a3a"), (220, "#c8302a"), (640, "#2a6a3a")):
            figur(img, otag, x, zemin, 1.6, renk, "#f0e8d8")

    orta(46, (526, 560), ["#7a9a48", "#6a8a40", "#5a7a38", "#4a6a30", "#3a5a28"], "#a8c870", ekle=kamp)
    on(46, ["#3a5a28", "#5a7a38", "#6a6a3a"], "#c8d888")

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        y = z[0]
        figur(t, otag, 95, z, 3.0, "#2a6a3a", "#e0b040", faz=f, acik=True)  # Osmanlı otağı
        figur(t, kisi, 72, z, 2.6, "#c8302a", "sarik", "#f4f0e6", "#2a1a12", yon=1, silah="mizrak")  # yeniçeri
        # sancak: direk zemine dikili, kırmızı zemin üzerinde beyaz hilal; rüzgârda dalgalanır
        d.line([132, y - 1, 132, y - 58], fill=hex2("#5a3a22"), width=2)
        dalga = int(math.sin(f * 2 * math.pi) * 2)
        # dönem sancağı: hilalsiz, kırmızı-yeşil iki şeritli flama (anakronizm yok)
        d.polygon([(133, y - 58), (160 + dalga, y - 54), (158 + dalga, y - 48), (133, y - 50)], fill=hex2("#c8302a"))
        d.polygon([(133, y - 50), (158 + dalga, y - 48), (156 + dalga, y - 40), (133, y - 42)], fill=hex2("#2a6a3a"))
        for j, x in enumerate((262, 300)):  # yorgun atlar arkada, başları aşağıda; insan boyu at boyunun ~%70'i
            figur(t, at, x, z, 3.6, -1, ("#3a2418", "#6b3f24")[j], "#140a06", None, True, 0.0, True, 0.6)
        figur(t, bayezid, 158, z, 3.1, 1, kol=0.35)  # Bayezid ayakta, sığınanlara dönük, eli onlara uzanır
        for j, x in enumerate((204, 232)):  # Kara Yusuf (Karakoyunlu, siyah) ve Ahmed Celayir (mavi) diz çökmüş, atların önünde
            figur(t, kisi, x, z, 2.8, ("#1a1a22", "#2a4a8a")[j], ("kalpak", "sarik")[j], ("#2a2a2a", "#f0e8d8")[j], "#2a1a12", yon=-1,
                  diz=True, pelerin=("#3a3a4a", "#c8a040")[j])
        rnd = random.Random(i // 2)
        for k in range(12):  # yoldan gelen toz çöker
            piksel(t, 268 + rnd.randint(0, 80), y - rnd.randint(2, 18) - k % 3, hex2("#c8b890", rnd.randint(50, 140)))

    sprite(46, "karakter", 360, 170, KARE, kare)


if __name__ == "__main__":
    secim = [int(a) for a in sys.argv[1:] if a.isdigit()] or [n for n in range(21, 70) if f"sahne{n}" in globals()]
    if "parsomen" in sys.argv:
        parsomen()
    for n in secim:
        globals()[f"sahne{n}"]()
        print(f"sahne {n} tamam", flush=True)
