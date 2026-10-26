"""SKONSTART piksel sanatı çizim aracı (64-bit oyun tarzı: ince piksel, bol detay).

Her şey bir tuvale (540x960) piksel piksel çizilir ve en sonda en yakın komşu
yöntemiyle 2 kat büyütülür (1080x1920). Kenar yumuşatma yoktur: pikseller keskin kalır.

Fizik kuralı: zemine basan her nesne, çizildiği tepenin zemin çizgisine (zemin listesi)
oturtulur ve altına bir temas gölgesi çizilir. Havada duran nesne olmaz.
"""
from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw

W, H = 540, 960
OLCEK = 2

BANT = 20  # arazinin renk bantlarının yüksekliği (piksel)

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def hex2(h: str, a: int = 255) -> tuple[int, int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def yeni() -> Image.Image:
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def buyut(img: Image.Image) -> Image.Image:
    return img.resize((W * OLCEK, H * OLCEK), Image.NEAREST)


def piksel(img, x, y, renk):
    """Tek piksel; yarı saydam renk alttakiyle karışır (gölge, ışık, duman)."""
    x, y = int(x), int(y)
    if not (0 <= x < img.width and 0 <= y < img.height):
        return
    a = renk[3] if len(renk) == 4 else 255
    if a < 255:
        r0, g0, b0, a0 = img.getpixel((x, y))
        t = a / 255
        oa = a + a0 * (1 - t)
        if oa == 0:
            return
        renk = tuple(int((c * a + c0 * a0 * (1 - t)) / oa) for c, c0 in zip(renk[:3], (r0, g0, b0))) + (int(oa),)
    img.putpixel((x, y), renk)


# ---------------------------------------------------------------- gökyüzü


def gradyan(img, renkler: list[str], y0: int = 0, y1: int = H):
    """Renk basamakları arasında Bayer titreşimli (dither) dikey geçiş: 32-bit oyunların gökyüzü."""
    ramp = [hex2(r) for r in renkler]
    n = len(ramp) - 1
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1) * n
        i = min(int(t), n - 1)
        f = t - i
        for x in range(img.width):
            esik = (BAYER[y % 4][x % 4] + 0.5) / 16
            img.putpixel((x, y), ramp[i + 1] if f > esik else ramp[i])


def gunes(img, cx, cy, r, renkler: list[str]):
    """İç içe halkalarla ışıyan güneş (dışa doğru titreşimle sönen hale)."""
    cekirdek, hale = hex2(renkler[0]), hex2(renkler[1])
    for y in range(int(cy - r * 3), int(cy + r * 3)):
        for x in range(int(cx - r * 3), int(cx + r * 3)):
            d = math.hypot(x - cx, y - cy)
            if d <= r:
                piksel(img, x, y, cekirdek)
            elif d <= r * 2.6 and 0 <= x < W and 0 <= y < H:
                t = (d - r) / (r * 1.6)
                if t < (BAYER[y % 4][x % 4] + 0.5) / 16 * 1.1:
                    piksel(img, x, y, hale)


def bulut(img, cx, cy, boy, renkler: list[str], tohum: int):
    """Düz gölgeli piksel bulut: üstte ışık, altta gölge bandı."""
    rnd = random.Random(tohum)
    isik, govde, golge = (hex2(r) for r in renkler)
    toplar = [(cx + rnd.randint(-boy, boy), cy + rnd.randint(-boy // 4, boy // 6), rnd.randint(boy // 3, boy // 2 + 2))
              for _ in range(7)]
    toplar.append((cx, cy, boy // 2 + 3))
    maske = {}
    for bx, by, r in toplar:
        for y in range(by - r, by + r + 1):
            for x in range(bx - r, bx + r + 1):
                if (x - bx) ** 2 + ((y - by) * 1.4) ** 2 <= r * r:
                    maske[(x, y)] = True
    alt = max(y for _, y in maske)
    for (x, y) in maske:
        if (x, y - 2) not in maske:
            renk = isik
        elif y > alt - boy // 4 or (x, y + 3) not in maske:
            renk = golge
        else:
            renk = govde
        piksel(img, x, y, renk)


def yildizlar(img, adet, ymax, renk, tohum):
    rnd = random.Random(tohum)
    for _ in range(adet):
        x, y = rnd.randrange(W), rnd.randrange(ymax)
        piksel(img, x, y, hex2(renk, rnd.choice((150, 200, 255))))


# ---------------------------------------------------------------- arazi


def sirt(taban, genlik, tohum, dalga=2.0, puruz=0.0) -> list[int]:
    """Bir tepe ya da dağ sırtının her x için y değeri (zemin çizgisi)."""
    rnd = random.Random(tohum)
    f1, f2, f3 = rnd.random() * 6.28, rnd.random() * 6.28, rnd.random() * 6.28
    return [
        int(taban - genlik * (0.6 * math.sin(x / W * math.pi * dalga + f1) + 0.4 * math.sin(x / W * math.pi * dalga * 2.3 + f2))
            - puruz * math.sin(x / 7 + f3) * (0.5 + 0.5 * math.sin(x / 23)))
        for x in range(W)
    ]


def arazi(img, zemin: list[int], renkler: list[str], kenar: str | None = None, doku_tohum: int | None = None):
    """Zemin çizgisinin altını doldurur: derinleştikçe koyulaşan bantlar, üstte ışıklı kenar."""
    ramp = [hex2(r) for r in renkler]
    rnd = random.Random(doku_tohum or 0)
    for x in range(W):
        for y in range(zemin[x], H):
            d = y - zemin[x]
            i = min(len(ramp) - 1, d // BANT)
            f = (d % BANT) / BANT
            if i < len(ramp) - 1 and f > 0.6 and (BAYER[y % 4][x % 4] + 0.5) / 16 < (f - 0.6) * 2.5:
                i += 1
            img.putpixel((x, y), ramp[i])
        if kenar:
            img.putpixel((x, zemin[x]), hex2(kenar))
    if doku_tohum is not None:
        # Çimen benekleri: zeminle aynı tonlardan küçük lekeler
        for _ in range(W * 2):
            x = rnd.randrange(W)
            y = rnd.randrange(zemin[x] + 3, H)
            renk = ramp[max(0, min(len(ramp) - 1, (y - zemin[x]) // BANT - 1))]
            piksel(img, x, y, renk)
            piksel(img, x + 1, y, renk)


def zemin_y(zemin: list[int], x: float, genislik: float = 0) -> int:
    """Nesnenin tabanı: ayak izi boyunca zeminin en alçak noktası (nesne asla havada kalmaz)."""
    x0, x1 = int(max(0, x - genislik / 2)), int(min(W - 1, x + genislik / 2))
    return max(zemin[x0:x1 + 1]) if x1 >= x0 else zemin[int(min(W - 1, max(0, x)))]


def temas_golgesi(img, x, y, genislik, renk="#1a2410", alfa=110):
    for dx in range(-int(genislik / 2), int(genislik / 2) + 1):
        if abs(dx) < genislik / 2 - 1 or (x + dx + y) % 2 == 0:
            piksel(img, x + dx, y, hex2(renk, alfa))
            if abs(dx) < genislik / 3:
                piksel(img, x + dx, y + 1, hex2(renk, alfa // 2))


def cimen_tutamlari(img, zemin, renkler: list[str], tohum, yogunluk=0.5, boy=4):
    rnd = random.Random(tohum)
    ramp = [hex2(r) for r in renkler]
    for x in range(W):
        if rnd.random() < yogunluk:
            h = rnd.randint(1, boy)
            renk = rnd.choice(ramp)
            egim = rnd.choice((-1, 0, 0, 1))
            for i in range(h):
                piksel(img, x + (egim if i > h // 2 else 0), zemin[x] - i, renk)


def cicekler(img, zemin, renkler, tohum, adet=20):
    rnd = random.Random(tohum)
    for _ in range(adet):
        x = rnd.randrange(W)
        y = zemin[x] + rnd.randint(2, 30)
        piksel(img, x, y, hex2(rnd.choice(renkler)))


# ---------------------------------------------------------------- figürler

KOYU = "#2b1a12"


def yurt(img, x, zemin, s=1.0, keçe="#efe4cc", golge="#c9b996", kapi="#c8552c", isik=False, duman=True):
    """Moğol yurdu (ger): silindir keçe duvar, alçak kubbe çatı, turuncu kapı, tepe halkası."""
    d = ImageDraw.Draw(img)
    gen = int(26 * s)
    y = zemin_y(zemin, x, gen)
    duvar_h, cati_h = int(10 * s), int(8 * s)
    x0, x1 = x - gen // 2, x + gen // 2
    temas_golgesi(img, x, y, gen + 4)
    # duvar
    d.rectangle([x0, y - duvar_h, x1, y - 1], fill=hex2(keçe), outline=hex2(KOYU))
    d.rectangle([x1 - gen // 4, y - duvar_h + 1, x1 - 1, y - 2], fill=hex2(golge))
    # ip bantları
    for by in (y - duvar_h + 2, y - 3):
        d.line([x0 + 1, by, x1 - 1, by], fill=hex2("#8a5a3a"))
    # çatı (alçak kubbe)
    d.chord([x0 - 1, y - duvar_h - cati_h, x1 + 1, y - duvar_h + cati_h], 180, 360, fill=hex2(keçe), outline=hex2(KOYU))
    # çatının sağ yarısı gölgede: kubbe eğrisini izleyen dikey şeritler
    for cx in range(x + gen // 5, x1 + 1):
        t = (cx - x) / (gen / 2 + 1)
        tepe = y - duvar_h - int(cati_h * math.sqrt(max(0, 1 - t * t)))
        d.line([cx, tepe + 2, cx, y - duvar_h - 1], fill=hex2(golge))
    # çatı direkleri (uni): tepe halkasından saçağa ışınlar
    for i in range(1, 6):
        ux = x0 + i * gen // 6
        d.line([x, y - duvar_h - cati_h + 2, ux, y - duvar_h - 1], fill=hex2(_ac(golge, -0.08)))
    d.line([x0, y - duvar_h, x1, y - duvar_h], fill=hex2(KOYU))
    # tepe halkası (toono)
    d.rectangle([x - max(1, int(2 * s)), y - duvar_h - cati_h, x + max(1, int(2 * s)), y - duvar_h - cati_h + 1], fill=hex2("#8a5a3a"))
    # kapı
    kw, kh = max(3, int(5 * s)), max(5, int(8 * s))
    d.rectangle([x - kw // 2 - 1, y - kh - 1, x + kw // 2 + 1, y - 1], fill=hex2(kapi), outline=hex2(KOYU))
    d.rectangle([x - kw // 2 + 1, y - kh + 1, x + kw // 2 - 1, y - 2], fill=hex2("#ffc76a" if isik else "#5a2a18"))
    if isik:
        for i in range(1, int(10 * s)):
            for dx in range(-kw // 2 - i // 2, kw // 2 + i // 2 + 1):
                if (dx + i) % 2 == 0:
                    piksel(img, x + dx, y + i, hex2("#ffd88a", max(0, 120 - i * 12)))
    return (x, y - duvar_h - cati_h)  # baca: duman buradan çıkar


def duman(img, x, y, boy, tohum, renk="#d9d2c4", ruzgar=0.4):
    """Tepe halkasından yukarı çıkan, rüzgârla eğilen ve seyrelen duman."""
    rnd = random.Random(tohum)
    for i in range(boy):
        cx = x + int(i * ruzgar + math.sin(i / 4 + tohum) * 1.5)
        r = 1 + i // 8
        a = max(0, 200 - i * 200 // boy)
        for dx in range(-r, r + 1):
            if rnd.random() < 0.8:
                piksel(img, cx + dx, y - i, hex2(renk, a))


def at(img, x, zemin, s=1.0, yon=1, renk="#6b3f24", yele="#2b1a12", binici=None, eyer=False, faz=0.0, dur=False):
    """Moğol atı (kısa bacaklı, gür yeleli). faz: 0-1 dörtnal döngüsü; dur=True ayakta duran at.
    Toynaklar zemine basar; binici varsa eyerde oturur."""
    d = ImageDraw.Draw(img)
    gen = int(22 * s)
    y = zemin_y(zemin, x, gen * 0.8)
    bacak = max(3, int(7 * s))
    govde_y = y - bacak
    g = hex2(renk)
    k = hex2(yele)
    acik = hex2(_ac(renk, 0.25))
    temas_golgesi(img, x, y, gen)

    def p(dx, dy):  # at koordinatı (burun yönü +x) -> tuval
        return (x + int(round(dx * s)) * yon, govde_y + int(round(dy * s)))

    koyu_g = hex2(_ac(renk, -0.25))
    # bacaklar: uzaktaki çift koyu, yakındaki çift açık; dörtnal fazı ön ve arka çiftte zıt
    for i, (bx, uzak) in enumerate(((-7, True), (6, True), (-5, False), (8, False))):
        aci = 0 if dur else math.sin((faz + (0.5 if bx < 0 else 0) + (0.1 if uzak else 0)) * 2 * math.pi) * 0.55
        ux, uy = p(bx, -1)
        ax = ux + int(math.sin(aci) * bacak) * yon
        ay = y - 1 if dur or math.cos(aci * 3) > 0 else y - 2
        d.line([ux, uy, ax, ay], fill=koyu_g if uzak else g, width=max(1, int(1.6 * s)))
        piksel(img, ax, ay, k)
        piksel(img, ax + yon, ay, k)
    # gövde: yuvarlak göğüs ve sağrı, aradaki karın
    d.ellipse([*p(-11, -8), *p(-2, 1)] if yon > 0 else [*p(-2, -8), *p(-11, 1)], fill=g)
    d.ellipse([*p(1, -8), *p(10, 1)] if yon > 0 else [*p(10, -8), *p(1, 1)], fill=g)
    d.rectangle([min(p(-7, -8)[0], p(6, -8)[0]), p(0, -8)[1], max(p(-7, 0)[0], p(6, 0)[0]), p(0, 0)[1]], fill=g)
    d.line([p(-9, -7), p(5, -7)], fill=acik)
    # boyun öne ve yukarı eğik, baş uzun ve aşağı bakar
    d.polygon([p(5, -7), p(10, -15), p(13, -14), p(11, -3)], fill=g)
    d.polygon([p(10, -16), p(13, -17), p(18, -11), p(17, -9), p(13, -11)], fill=g)
    d.line([p(10, -16), p(11, -18)], fill=g)  # kulak
    d.line([p(6, -8), p(10, -16)], fill=k, width=max(1, int(1.5 * s)))  # yele
    piksel(img, *p(13, -14), k)  # göz
    piksel(img, *p(17, -10), koyu_g)  # burun
    # kuyruk: sağrıdan aşağı sarkar, koşarken geriye savrulur
    kx, ky = p(-11, -6)
    savrulma = 0 if dur else 0.8
    for i in range(int(9 * s)):
        tx = kx - int(i * (0.3 + savrulma * 0.5)) * yon
        piksel(img, tx, ky + int(i * (1 - savrulma * 0.4)), k)
        piksel(img, tx - yon, ky + int(i * (1 - savrulma * 0.4)), k)
    sirt_y = govde_y - int(8 * s)
    if eyer or binici:
        d.rectangle([x - int(3 * s), sirt_y - 1, x + int(4 * s), sirt_y + int(2 * s)], fill=hex2("#7a2e1e"), outline=hex2(KOYU))
        d.line([x, sirt_y + int(2 * s), x, govde_y], fill=hex2("#3a2a1e"))  # üzengi kayışı
    if binici:
        _binici(img, x, sirt_y, s, yon, binici)


def _binici(img, x, y, s, yon, deel):
    d = ImageDraw.Draw(img)
    gv = hex2(deel)
    d.rectangle([x - int(2 * s), y - int(9 * s), x + int(2 * s), y], fill=gv)  # gövde (deel)
    d.line([x - int(2 * s), y - int(4 * s), x - int(2 * s), y + int(3 * s)], fill=gv, width=max(1, int(2 * s)))  # bacak
    d.line([x + int(1 * s) * yon, y - int(7 * s), x + int(5 * s) * yon, y - int(4 * s)], fill=gv, width=max(1, int(1.5 * s)))  # kol (dizgin)
    d.line([x - int(2 * s), y - int(5 * s), x + int(2 * s), y - int(5 * s)], fill=hex2("#e0b040"))  # kuşak
    d.ellipse([x - int(2 * s), y - int(13 * s), x + int(2 * s), y - int(9 * s)], fill=hex2("#d6a07a"))  # yüz
    d.polygon([(x - int(3 * s), y - int(12 * s)), (x, y - int(16 * s)), (x + int(3 * s), y - int(12 * s))], fill=hex2("#5a3a22"))  # börk


def insan(img, x, zemin, s=1.0, deel="#3a5a8a", bebek=False, kadin=False):
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    temas_golgesi(img, x, y, 7 * s)
    gv = hex2(deel)
    d.polygon([(x - int(3 * s), y - 1), (x - int(2 * s), y - int(11 * s)), (x + int(2 * s), y - int(11 * s)), (x + int(3 * s), y - 1)], fill=gv)
    d.line([x - int(3 * s), y - int(6 * s), x + int(3 * s), y - int(6 * s)], fill=hex2("#e0b040"))
    d.ellipse([x - int(2 * s), y - int(15 * s), x + int(2 * s), y - int(11 * s)], fill=hex2("#d6a07a"))
    if kadin:
        d.rectangle([x - int(3 * s), y - int(17 * s), x + int(3 * s), y - int(15 * s)], fill=hex2("#9a2e3e"))
    else:
        d.polygon([(x - int(3 * s), y - int(14 * s)), (x, y - int(18 * s)), (x + int(3 * s), y - int(14 * s))], fill=hex2("#5a3a22"))
    if bebek:
        d.ellipse([x + int(1 * s), y - int(10 * s), x + int(5 * s), y - int(7 * s)], fill=hex2("#efe4cc"), outline=hex2(KOYU))


def agac(img, x, zemin, s=1.0, yaprak=("#2f5a2a", "#477a34", "#6a9a44"), tohum=1):
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    temas_golgesi(img, x, y, 16 * s)
    d.polygon([(x - int(3 * s), y), (x - int(1 * s), y - int(26 * s)), (x + int(2 * s), y - int(26 * s)), (x + int(4 * s), y)], fill=hex2("#4a3022"))
    d.line([x, y - int(18 * s), x - int(8 * s), y - int(28 * s)], fill=hex2("#4a3022"), width=max(1, int(2 * s)))
    d.line([x + 1, y - int(20 * s), x + int(9 * s), y - int(30 * s)], fill=hex2("#4a3022"), width=max(1, int(2 * s)))
    rnd = random.Random(tohum)
    for i, renk in enumerate(yaprak):
        for _ in range(9):
            cx = x + rnd.randint(-int(14 * s), int(14 * s)) + i
            cy = y - int(34 * s) + rnd.randint(-int(8 * s), int(6 * s)) - i * 2
            r = int(rnd.randint(5, 8) * s) - i
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hex2(renk))


def tug(img, x, zemin, s=1.0):
    """Beyaz at kılından tuğ (sancak): direk zemine dikili."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 4)
    temas_golgesi(img, x, y, 6 * s)
    tepe = y - int(46 * s)
    d.line([x, y, x, tepe], fill=hex2("#5a3a22"), width=max(1, int(2 * s)))
    d.polygon([(x - int(2 * s), tepe), (x, tepe - int(5 * s)), (x + int(2 * s), tepe)], fill=hex2("#e0b040"))
    for i in range(int(14 * s)):
        w = 2 + i // 3
        for dx in range(-w, w + 1):
            if (dx + i) % 3:
                piksel(img, x + dx, tepe + 2 + i, hex2("#f4f0e6" if dx < w - 1 else "#c8c0b0"))


def sehir(img, x0, x1, zemin, s=1.0, duvar="#a88a6a", golge="#7a6048"):
    """Uzak surlu şehir: mazgallı duvar, kuleler, kapı. Tabanı zemine oturur."""
    d = ImageDraw.Draw(img)
    y = max(zemin[max(0, x0):min(W, x1)])

    def u(v):
        return max(1, int(v * s))

    d.rectangle([x0, y - u(14), x1, y], fill=hex2(duvar))
    for mx in range(x0, x1, u(4)):
        d.rectangle([mx, y - u(16), mx + u(1), y - u(14)], fill=hex2(duvar))
    for kx in range(x0, x1 + 1, (x1 - x0) // 3):
        d.rectangle([kx - u(4), y - u(24), kx + u(4), y], fill=hex2(golge))
        d.polygon([(kx - u(5), y - u(24)), (kx, y - u(31)), (kx + u(5), y - u(24))], fill=hex2("#6a3a2a"))
        d.rectangle([kx - u(1), y - u(20), kx + u(1) - 1, y - u(17)], fill=hex2("#3a2a1e"))  # mazgal penceresi
    gx = (x0 + x1) // 2
    d.rectangle([gx - u(3), y - u(8), gx + u(3), y], fill=hex2("#3a2a1e"))
    d.line([x0, y, x1, y], fill=hex2(golge))


def taslar(img, x, zemin, s=1.0, cicek=True):
    """Ovoo: üst üste konmuş taş yığını (alttaki büyük taşlar zemine oturur), yanında tek çiçek."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 18 * s)
    temas_golgesi(img, x, y, 22 * s)
    sira = [(0, 9, 5), (-6, 6, 4), (6, 6, 4), (-3, 4, 3), (3, 4, 3), (0, 3, 3)]
    taban = y
    for i, (dx, w, h) in enumerate(sira):
        katman = 0 if i < 3 else (1 if i < 5 else 2)
        cy = taban - int((katman * 6 + h) * s)
        cx = x + int(dx * s) if katman else x + int(dx * s)
        renk = ("#8a8478", "#9e978a", "#b2ab9c")[i % 3]
        d.ellipse([cx - int(w * s), cy - int(h * s), cx + int(w * s), cy + int(h * s)], fill=hex2(renk), outline=hex2("#4a4440"))
        d.line([cx - int(w * s) + 2, cy - int(h * s) + 1, cx, cy - int(h * s) + 1], fill=hex2("#d8d2c4"))
    if cicek:
        cx = x + int(14 * s)
        cy = zemin_y(zemin, cx, 2)
        d.line([cx, cy, cx, cy - int(7 * s)], fill=hex2("#3f6b2a"))
        piksel(img, cx - 1, cy - int(4 * s), hex2("#5a8f36"))
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            piksel(img, cx + dx, cy - int(8 * s) + dy, hex2("#f4d24a"))
        piksel(img, cx, cy - int(8 * s), hex2("#c8552c"))


def figur(img, ciz_fn, *args, kontur="#24160e", f_isik=0.18, f_golge=0.22, **kwargs):
    """Figürü ayrı bir katmanda çizer, sonra 64-bit oyun figürü gibi işler: dışına 1 piksel
    koyu kontur, üst kenarlarına ışık, alt kenarlarına gölge. Sonra sahneye bindirir.
    Çizim fonksiyonunun döndürdüğü değeri (ör. yurdun baca noktası) geri verir."""
    katman = yeni()
    sonuc = ciz_fn(katman, *args, **kwargs)
    px = katman.load()
    dolu = lambda x, y: 0 <= x < W and 0 <= y < H and px[x, y][3] > 200
    kutu = katman.getbbox()
    if kutu:
        x0, y0, x1, y1 = kutu
        isle = {}
        for y in range(max(0, y0 - 1), min(H, y1 + 1)):
            for x in range(max(0, x0 - 1), min(W, x1 + 1)):
                if dolu(x, y):
                    r, g, b, a = px[x, y]
                    if not dolu(x, y - 1) or not dolu(x - 1, y - 1) and dolu(x - 1, y):
                        isle[(x, y)] = tuple(int(c + (255 - c) * f_isik) for c in (r, g, b)) + (a,)
                    elif not dolu(x, y + 1) or not dolu(x + 2, y):
                        isle[(x, y)] = tuple(int(c * (1 - f_golge)) for c in (r, g, b)) + (a,)
                elif px[x, y][3] < 60 and any(dolu(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    isle[(x, y)] = hex2(kontur)
        for (x, y), renk in isle.items():
            px[x, y] = renk
    img.alpha_composite(katman)
    return sonuc


def _ac(h: str, t: float) -> str:
    """t > 0 açar, t < 0 koyulaştırır."""
    r, g, b, _ = hex2(h)
    if t >= 0:
        return "#%02x%02x%02x" % tuple(int(c + (255 - c) * t) for c in (r, g, b))
    return "#%02x%02x%02x" % tuple(int(c * (1 + t)) for c in (r, g, b))
