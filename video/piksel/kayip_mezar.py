""""Kayıp Mezar" kısa videosunun sahneleri (11-17): olay örgüsünü izleyen görseller.

11 ordugâh gecesi, Han'ın yurdu ve nöbetçiler · 12 kalabalık cenaze alayı · 13 aynı alay kızıl gökte
14 kutsal dağın eteğinde mezar höyüğü ve yas tutanlar · 15 mezarın üstünden sürülen at sürüsü
16 Büyük Yasak: orman, sınır taşları, muhafızlar · 17 yıldızlı gece, ormanlık dağ (uydu kodda geçer)

Dosyalar video/public/sahne11-...png gibi; sprite'lar fizik denetiminden geçer (sahneler.sprite).
Kullanım: python3 -I video/piksel/kayip_mezar.py [sahne numaraları]
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import ImageDraw  # noqa: E402

from ciz import (H, W, _ac, _esik, at, figur, hex2, insan, kagni, okuz, piksel, temas_golgesi, yeni, yurt,  # noqa: E402
                 zemin_y)
from sahneler import GW, KARE, PAY, duz, gokyuzu, kaydet, on, orta, sprite, uzak  # noqa: E402


# ---------------------------------------------------------------- yeni figürler


def cam(img, x, zemin, s=1.0, renk="#1e3a2a", isik="#2e5a3e"):
    """Çam: kat kat üçgen dallar, gövdesi zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 4 * s)
    d.rectangle([x - max(1, int(1.2 * s)), y - int(6 * s), x + max(1, int(1.2 * s)), y - 1], fill=hex2("#3a2418"))
    for k in range(4):
        taban = y - int((5 + k * 7) * s)
        gen = (12 - k * 2.4) * s
        d.polygon([(x - gen, taban), (x, taban - 11 * s), (x + gen, taban)], fill=hex2(renk))
        d.line([(x - gen * 0.2, taban - 9 * s), (x - gen * 0.85, taban - 1)], fill=hex2(isik))


def muhafiz(img, x, zemin, s=1.0, faz=0.0, mizrak=True, mesale=True, deel="#3a2a2a"):
    """Ayakta duran nöbetçi: uzun mızrak, elinde titreyen meşale. Ayakları zemine basar."""
    d = ImageDraw.Draw(img)
    insan(img, x, zemin, s, deel)
    y = zemin_y(zemin, x, 6 * s)
    if mizrak:
        mx = x + int(3 * s)
        d.line([(mx, y - 1), (mx, y - int(30 * s))], fill=hex2("#5a3a22"), width=max(1, int(0.8 * s)))
        d.polygon([(mx - 1.5 * s, y - 30 * s), (mx, y - 35 * s), (mx + 1.5 * s, y - 30 * s)], fill=hex2("#c8ccd0"))
        for i in range(4):  # mızrak püskülü
            piksel(img, mx - 1 + i % 2, y - int(29 * s) + i, hex2("#9a1a14"))
    if mesale:
        tx = x - int(3 * s)
        d.line([(tx, y - int(9 * s)), (tx - int(1 * s), y - int(18 * s))], fill=hex2("#4a2a16"), width=max(1, int(0.9 * s)))
        alev_y = y - int(19 * s)
        titre = math.sin(faz * 2 * math.pi * 3) * 0.8 * s
        for r, renk in ((3.2, "#e8601c"), (2.2, "#f8a030"), (1.2, "#fff0a0")):
            d.polygon([(tx - r * s * 0.45 - 1 + titre * 0.3, alev_y), (tx + titre, alev_y - r * s * 1.6),
                       (tx + r * s * 0.45 + 1 + titre * 0.3, alev_y)], fill=hex2(renk))
        for i in range(10):  # ışık halesi
            a = i / 10 * 2 * math.pi
            piksel(img, tx + math.cos(a) * 6 * s, alev_y - 2 * s + math.sin(a) * 6 * s, hex2("#f8a030", 70))


def cenaze_arabasi(img, x, zemin, s=1.0, faz=0.0, yon=-1):
    """Cenaze arabası: büyük tekerlekli kağnının üstünde beyaz keçe örtülü yurt, köşelerde beyaz sancaklar."""
    d = ImageDraw.Draw(img)
    kagni(img, x, zemin, s, yon=yon, faz=faz, yuk="#efe8dc")
    y = zemin_y(zemin, x, 26 * s)
    gov_y = y - int(7 * s) - int(2 * s)
    tavan = gov_y - int(11 * s)
    d.chord([x - 12 * s, tavan - 9 * s, x + 11 * s, tavan + 6 * s], 180, 360, fill=hex2("#f4f0e6"), outline=hex2("#2a1a12"))
    d.line([(x - 12 * s, tavan), (x + 11 * s, tavan)], fill=hex2("#8a5a3a"))
    for i in range(1, 5):
        d.line([(x - 1 * s, tavan - 8 * s), (x - 12 * s + i * 4.6 * s, tavan)], fill=hex2("#d8d0c0"))
    for sx in (-12, 11):  # beyaz yas sancakları
        px_ = x + sx * s
        d.line([(px_, gov_y), (px_, tavan - 18 * s)], fill=hex2("#3a2418"), width=max(1, int(0.8 * s)))
        for i in range(int(9 * s)):
            dal = math.sin(faz * 2 * math.pi + i / (2 * s)) * 1.4 * s * i / (9 * s)
            for k in range(int(4 * s)):
                piksel(img, px_ + i * -yon * -1 * (-1 if yon < 0 else 1), tavan - 17 * s + k + dal, hex2("#f4f0e6"))


def hoyuk(img, x, zemin, s=1.0):
    """Taze mezar höyüğü: koyu toprak tümsek, üstünde birkaç taş. Tabanı zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 30 * s)
    temas_golgesi(img, x, y, 40 * s)
    d.chord([x - 20 * s, y - 12 * s, x + 20 * s, y + 12 * s], 180, 360, fill=hex2("#4a3020"))
    d.chord([x - 16 * s, y - 10 * s, x + 6 * s, y + 6 * s], 180, 360, fill=hex2("#5e3e28"))
    rnd = random.Random(int(x))
    for _ in range(int(14 * s)):
        tx, ty = x + rnd.uniform(-14, 14) * s, y - rnd.uniform(1, 8) * s
        if (tx - x) ** 2 / (20 * s) ** 2 + (y - ty) ** 2 / (12 * s) ** 2 < 0.8:
            piksel(img, tx, ty, hex2(rnd.choice(("#8a7a6a", "#6a5040", "#3a2418"))))


def at_suru(img, zemin, i, s, adet, x0, aralik, renkler, tohum):
    """Binicisiz dörtnala koşan atlar: sıra sıra, farklı fazlarda; toynakların arkasından toz kalkar."""
    rnd = random.Random(tohum)
    f = i / KARE
    for j in range(adet):
        x = x0 + j * aralik + rnd.randint(-6, 6)
        faz = (f + rnd.random()) % 1
        for k in range(4):  # toz: yerden kalkar, arkaya savrulur
            tx = x + (14 + k * 6) * s * 0.5
            ty = zemin[0] - 2 - k * 2
            r = 2 + k
            for py in range(-r, r + 1):
                for px_ in range(-r, r + 1):
                    if px_ * px_ + py * py <= r * r and _esik(int(tx + px_), int(ty + py)) < 0.55 - k * 0.1:
                        piksel(img, tx + px_ + f * 6, ty + py, hex2("#c8a878", 140 - k * 25))
        figur(img, at, x, zemin, s, -1, rnd.choice(renkler), "#140a06", faz=faz, adim=0.75, kontur="#120806")


# ---------------------------------------------------------------- sahneler

GECE_GOK = ["#0a0c22", "#141a3a", "#2a2448", "#4a2a48", "#7a3440", "#a8483a"]


def sahne11():
    gokyuzu(11, GECE_GOK, (110, 250, 12, ["#f4ecd0", "#c8c0a8"]), [(420, 300, 38), (160, 330, 30)],
            ("#4a3a5a", "#3a2e4a", "#2a2238"), yildiz=120)
    uzak(11, ["#2a2440", "#221e36"], ["#2e2a3a", "#262230"], ["#3a3428", "#322c22", "#2a2620"])

    def kamp(img, z):
        zemin = duz(588)
        rnd = random.Random(11)
        for x in list(range(30, 360, 46)) + list(range(470, 800, 46)):
            figur(img, yurt, x + rnd.randint(-6, 6), zemin, rnd.uniform(1.1, 1.5), keçe="#8a8070", golge="#5a5448",
                  kapi="#3a1a10", isik=rnd.random() < 0.5, kontur="#0a0806")
        for x in range(60, 780, 120):  # kamp ateşleri
            for k, renk in enumerate(("#e8601c", "#f8a030", "#fff0a0")):
                piksel(img, x + 14, 586 - k, hex2(renk))
                piksel(img, x + 15, 586 - k, hex2(renk))

    orta(11, (520, 560), ["#3a3a26", "#323220", "#2a2a1c", "#222216", "#1a1a12"], "#5a5a3a", ekle=kamp)
    on(11, ["#1a1a12", "#26261a", "#3a2e2a"], "#6a5a7a")

    def kare(t, z, i):
        f = i / KARE
        figur(t, yurt, 130, z, 3.2, keçe="#d8cfc0", golge="#9a9080", kapi="#8a1a10", isik=True, isik_gucu=0.7 + 0.3 * math.sin(f * 6.28 * 2))
        from ciz import tug
        figur(t, tug, 218, z, 1.7, faz=f)
        for x in (40, 236):
            figur(t, muhafiz, x, z, 2.6, faz=(f + x / 100) % 1, deel="#4a2a2a")

    sprite(11, "karakter", 270, 170, KARE, kare)


def _alay(no, gok, gunes_, bulut_renk, ova, orta_renk, kenar, on_renk, on_isik, yildiz=0):
    gokyuzu(no, gok, gunes_, [(150, 300, 42), (420, 320, 36)], bulut_renk, yildiz=yildiz)
    uzak(no, ["#6a6070", "#5a5060"], ["#7a7058", "#6a604c"], ova)

    def ikinci_sira(img, z):  # arka planda ikinci, uzun bir yas kalabalığı sırası
        zemin = duz(586)
        rnd = random.Random(no)
        for x in range(20, 800, 9):
            if rnd.random() < 0.85:
                insan(img, x + rnd.randint(-2, 2), zemin, rnd.uniform(0.9, 1.15), rnd.choice(("#2a2420", "#3a3030", "#d8d0c0", "#4a3a2a")), yon=-1)
        for x in range(60, 800, 140):
            ImageDraw.Draw(img).line([(x, 586), (x, 556)], fill=hex2("#2a1a12"))
            for k in range(6):
                ImageDraw.Draw(img).line([(x, 557 + k), (x - 9, 559 + k)], fill=hex2("#efe8dc"))

    orta(no, (520, 560), orta_renk, kenar, ekle=ikinci_sira)
    on(no, on_renk, on_isik)

    def kare(t, z, i):
        f = i / KARE
        rnd = random.Random(7)
        # önde yürüyenler (sola gider)
        for j, x in enumerate(range(18, 150, 22)):
            figur(t, insan, x, z, 2.4, rnd.choice(("#2a2420", "#d8d0c0", "#3a2a2a", "#4a3a2a")), adim=(f + j * 0.37) % 1, yon=-1,
                  kadin=j % 3 == 1)
        figur(t, okuz, 182, z, 2.1, -1, "#4a3628", faz=f)
        figur(t, okuz, 214, z, 2.0, -1, "#5a4232", faz=(f + 0.5) % 1)
        figur(t, cenaze_arabasi, 286, z, 2.6, faz=f, yon=-1)
        for j, x in enumerate(range(338, 440, 20)):  # arkadan gelen yaslılar
            figur(t, insan, x, z, 2.4, rnd.choice(("#2a2420", "#d8d0c0", "#3a2a2a")), adim=(f + j * 0.29) % 1, yon=-1, kadin=j % 2 == 0)
        for j, x in enumerate((462, 512)):  # atlı muhafızlar
            figur(t, at, x, z, 2.1, -1, ("#3a2418", "#d8d0c0")[j], binici="#2a2420", faz=(f + j * 0.4) % 1, adim=0.4)

    sprite(no, "karakter", 540, 150, KARE, kare)


def sahne12():
    _alay(12, ["#5a6a88", "#7a88a0", "#9aa4b0", "#b8b8b0", "#c8c0a8"], None, ("#d8dce0", "#b8bcc4", "#8a909a"),
          ["#8a9070", "#7a8264", "#6a7458"], ["#6a7a4a", "#5a6a40", "#4a5a36", "#3a4a2e", "#2e3a26"], "#8a9a6a",
          ["#2e3a26", "#4a5a36", "#6a6a4a"], "#c8c8a0")


def sahne13():
    _alay(13, ["#1a0a10", "#3a1218", "#6a1a18", "#9a2a1a", "#c8481e", "#e87a30"], (380, 520, 40, ["#ffb060", "#e8601c"]),
          ("#4a1a18", "#3a1212", "#2a0e0e"), ["#5a3a2a", "#4a3022", "#3a261c"], ["#4a3a22", "#3e301c", "#322618", "#261e12", "#1a140c"],
          "#8a5a3a", ["#1a140c", "#2a2016", "#4a2a1a"], "#c86a3a", yildiz=30)


def _dag_ormani(img, z, yogunluk, tohum, renk="#1e3a2a"):
    rnd = random.Random(tohum)
    for x in range(-10, GW + 10, yogunluk):
        figur(img, cam, x + rnd.randint(-4, 4), z, rnd.uniform(1.6, 2.6), renk=renk, isik=_ac(renk, 0.25), kontur="#0a120c")


def sahne14():
    gokyuzu(14, ["#3a4a6a", "#5a6a88", "#8a8aa0", "#b8a0a0", "#d8b098"], None, [(130, 300, 40), (430, 330, 32)],
            ("#e8d8d8", "#c0b0b8", "#8a8098"))
    uzak(14, ["#3a4a40", "#2e4036"], ["#2a4030", "#223826"], ["#4a5a3a", "#40502e", "#364628"], dag_y=(250, 420), tepe_y=450)

    def orman(img, z):
        _dag_ormani(img, z, 14, 14)

    orta(14, (520, 556), ["#4a6a3a", "#3e5e32", "#34522a", "#2a4624", "#223a1e"], "#7a9a5a", ekle=orman)
    on(14, ["#223a1e", "#34522a", "#4a4a3a"], "#a8b888")

    def kare(t, z, i):
        f = i / KARE
        figur(t, hoyuk, 200, z, 3.0)
        rnd = random.Random(4)
        for j, x in enumerate((40, 70, 100, 300, 330, 360)):  # yas tutanlar: başları eğik, ayakta
            figur(t, insan, x, z, 2.5, rnd.choice(("#2a2420", "#d8d0c0", "#3a2a2a")), yon=1 if x < 200 else -1, kadin=j % 2 == 1)
        for x in (130, 270):
            figur(t, muhafiz, x, z, 2.5, faz=(f + x / 90) % 1, mizrak=False)

    sprite(14, "karakter", 400, 150, KARE, kare)


def sahne15():
    gokyuzu(15, ["#4a3a4a", "#7a5a5a", "#a87a5a", "#d8a060", "#f0c070"], (440, 520, 30, ["#ffe0a0", "#f8a050"]),
            [(120, 290, 42), (400, 330, 32)], ("#f0c8a0", "#c89878", "#8a6058"))
    uzak(15, ["#4a4a48", "#3e3e3e"], ["#3a5034", "#30462c"], ["#6a6a40", "#5e5e38", "#525230"], dag_y=(300, 420))

    def orman(img, z):
        _dag_ormani(img, z, 26, 15, renk="#24402e")

    orta(15, (520, 556), ["#7a7a3a", "#6a6a32", "#5a5a2c", "#4a4a24", "#3a3a1e"], "#a8a860", ekle=orman)
    on(15, ["#3a3a1e", "#5a5a2c", "#7a6a3a"], "#d8c888")

    def kare(t, z, i):
        at_suru(t, z, i, 2.2, 7, 30, 52, ("#3a2418", "#5a3a24", "#8a6a4a", "#2a1810", "#c8a070", "#6b3f24"), 15)
        for j, x in enumerate((440, 495)):
            figur(t, at, x, z, 2.2, -1, ("#2a1810", "#4a2e1e")[j], binici="#3a2a2a", faz=((i / KARE) + j * 0.3) % 1, adim=0.75)

    sprite(15, "karakter", 540, 140, KARE, kare)


def sahne16():
    gokyuzu(16, ["#06081a", "#0e1430", "#1a2248", "#2a2a54", "#3a3058"], (420, 300, 14, ["#f4ecd0", "#a8a8c0"]),
            [(140, 320, 34)], ("#3a3a5a", "#2a2a48", "#1e1e38"), yildiz=140)
    uzak(16, ["#141e2a", "#101822"], ["#14261c", "#102016"], ["#1e2a1e", "#1a241a", "#161e16"], dag_y=(260, 420))

    def orman(img, z):
        _dag_ormani(img, z, 11, 16, renk="#122a1c")

    orta(16, (520, 556), ["#1e2e1c", "#1a2818", "#162214", "#121c10", "#0e160c"], "#3a5a3a", ekle=orman)
    on(16, ["#0e160c", "#1a2818", "#2a2a3a"], "#5a6a8a")

    def kare(t, z, i):
        f = i / KARE
        from ciz import taslar
        for x in (120, 240):  # sınır taşları
            figur(t, taslar, x, z, 1.5)
        for x in (60, 180, 300):
            figur(t, muhafiz, x, z, 2.7, faz=(f + x / 70) % 1, deel="#2a2430")

    sprite(16, "karakter", 360, 170, KARE, kare)


def sahne17():
    gokyuzu(17, ["#04050f", "#080c1e", "#10162e", "#1a1e3a", "#262440"], None, [], yildiz=260)
    uzak(17, ["#101826", "#0c1420"], ["#0e1c16", "#0a1612"], ["#141e16", "#101a12", "#0c140e"], dag_y=(240, 420))

    def orman(img, z):
        _dag_ormani(img, z, 10, 17, renk="#0e2016")

    orta(17, (520, 556), ["#141e12", "#101a0e", "#0c140a", "#0a1008", "#060c06"], "#2a3a2a", ekle=orman)
    on(17, ["#060c06", "#101a0e", "#1a1a2a"], "#3a4a6a")
    # uydu: kodda gökyüzünde süzülür
    u = yeni(40, 16)
    d = ImageDraw.Draw(u)
    d.rectangle([16, 5, 23, 10], fill=hex2("#c8ccd0"), outline=hex2("#5a5e66"))
    for x0 in (2, 25):
        d.rectangle([x0, 6, x0 + 12, 9], fill=hex2("#2a4a8a"), outline=hex2("#8aa0d0"))
        for k in range(x0 + 3, x0 + 12, 3):
            d.line([(k, 6), (k, 9)], fill=hex2("#5a7ab8"))
    d.line([(19, 5), (19, 1)], fill=hex2("#c8ccd0"))
    piksel(u, 19, 0, hex2("#ff4040"))
    kaydet(u, "uydu.png")


if __name__ == "__main__":
    secim = [int(a) for a in sys.argv[1:] if a.isdigit()] or range(11, 18)
    for n in secim:
        globals()[f"sahne{n}"]()
        print(f"sahne {n} tamam")
