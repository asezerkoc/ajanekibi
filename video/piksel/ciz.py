"""SKONSTART piksel sanatı çizim aracı (64-bit oyun tarzı: ince piksel, bol detay).

Ekran ızgarası 540x960'tır ve en sonda en yakın komşu yöntemiyle 2 kat büyütülür
(1080x1920). Kenar yumuşatma yoktur: pikseller keskin kalır. Katmanlar farklı genişlikte
olabilir (orta ve ön plan 810 genişliktedir); fonksiyonlar tuvalin ve zemin listesinin
kendi genişliğini kullanır.

Fizik kuralı: zemine basan her nesne, zemin listesindeki çizgiye oturtulur ve ayaklarının
altına bir temas gölgesi çizilir. Yapılar yalnızca düz zemine kurulur (duz_zemin); değilse
FizikHatasi verilir. Havada duran nesne olmaz.
"""
from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw

W, H = 540, 960
OLCEK = 2

BANT = 20  # arazinin renk bantlarının yüksekliği (piksel)

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

KOYU = "#2b1a12"


def hex2(h: str, a: int = 255) -> tuple[int, int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def _ac(h: str, t: float) -> str:
    """t > 0 açar, t < 0 koyulaştırır."""
    r, g, b, _ = hex2(h)
    if t >= 0:
        return "#%02x%02x%02x" % tuple(int(c + (255 - c) * t) for c in (r, g, b))
    return "#%02x%02x%02x" % tuple(int(c * (1 + t)) for c in (r, g, b))


def yeni(w: int = W, h: int = H) -> Image.Image:
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def buyut(img: Image.Image) -> Image.Image:
    return img.resize((img.width * OLCEK, img.height * OLCEK), Image.NEAREST)


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


def _esik(x, y):
    return (BAYER[y % 4][x % 4] + 0.5) / 16


# ---------------------------------------------------------------- gökyüzü


def gradyan(img, renkler: list[str], y0: int = 0, y1: int | None = None):
    """Renk basamakları arasında Bayer titreşimli (dither) dikey geçiş."""
    y1 = img.height if y1 is None else y1
    ramp = [hex2(r) for r in renkler]
    n = len(ramp) - 1
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1) * n
        i = min(int(t), n - 1)
        f = t - i
        for x in range(img.width):
            img.putpixel((x, y), ramp[i + 1] if f > _esik(x, y) else ramp[i])


def gunes(img, cx, cy, r, renkler: list[str]):
    """Işıyan güneş/ay: dolu çekirdek, dışa doğru titreşimle sönen hale."""
    cekirdek, hale = hex2(renkler[0]), hex2(renkler[1])
    for y in range(int(cy - r * 3), int(cy + r * 3)):
        for x in range(int(cx - r * 3), int(cx + r * 3)):
            d = math.hypot(x - cx, y - cy)
            if d <= r:
                piksel(img, x, y, cekirdek)
            elif d <= r * 2.6 and 0 <= y < img.height:
                if (d - r) / (r * 1.6) < _esik(x % img.width, y) * 1.1:
                    piksel(img, x % img.width, y, hale)


def bulut(img, cx, cy, boy, renkler: list[str], tohum: int, sar: bool = True):
    """Düz gölgeli piksel bulut: üstte ışık, altta gölge bandı. sar=True: kenardan taşan kısım
    öbür kenardan girer (yatayda dikişsiz tekrar eden gökyüzü için)."""
    rnd = random.Random(tohum)
    isik, govde, golge = (hex2(r) for r in renkler)
    toplar = [(cx + rnd.randint(-boy, boy), cy + rnd.randint(-boy // 4, boy // 6), rnd.randint(boy // 3, boy // 2 + 2))
              for _ in range(7)]
    toplar.append((cx, cy, boy // 2 + 3))
    maske = set()
    for bx, by, r in toplar:
        for y in range(by - r, by + r + 1):
            for x in range(bx - r, bx + r + 1):
                if (x - bx) ** 2 + ((y - by) * 1.4) ** 2 <= r * r:
                    maske.add((x, y))
    alt = max(y for _, y in maske)
    for (x, y) in maske:
        if (x, y - 2) not in maske:
            renk = isik
        elif y > alt - boy // 4 or (x, y + 3) not in maske:
            renk = golge
        else:
            renk = govde
        piksel(img, x % img.width if sar else x, y, renk)


def yildizlar(img, adet, ymax, renk, tohum):
    rnd = random.Random(tohum)
    for _ in range(adet):
        x, y = rnd.randrange(img.width), rnd.randrange(ymax)
        a = rnd.choice((120, 180, 255))
        piksel(img, x, y, hex2(renk, a))
        if a == 255 and rnd.random() < 0.3:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                piksel(img, x + dx, y + dy, hex2(renk, 90))


# ---------------------------------------------------------------- arazi


def sirt(taban, genlik, tohum, dalga=2.0, puruz=0.0, w: int = W, dongulu: bool = False) -> list[int]:
    """Bir tepe ya da dağ sırtının her x için y değeri (zemin çizgisi).
    dongulu=True: tam sayı frekanslarla, sol ve sağ kenarı birbirine dikişsiz uyan sırt."""
    rnd = random.Random(tohum)
    f1, f2, f3 = rnd.random() * 6.28, rnd.random() * 6.28, rnd.random() * 6.28
    if dongulu:
        k1 = max(1, round(dalga / 2))
        k2 = k1 * 2 + 1
        kp = max(1, round(w / 7 / (2 * math.pi)) * 1)
        return [
            int(taban - genlik * (0.6 * math.sin(2 * math.pi * k1 * x / w + f1) + 0.4 * math.sin(2 * math.pi * k2 * x / w + f2))
                - puruz * math.sin(2 * math.pi * kp * 7 * x / w + f3) * (0.5 + 0.5 * math.sin(2 * math.pi * 3 * x / w)))
            for x in range(w)
        ]
    return [
        int(taban - genlik * (0.6 * math.sin(x / w * math.pi * dalga + f1) + 0.4 * math.sin(x / w * math.pi * dalga * 2.3 + f2))
            - puruz * math.sin(x / 7 + f3) * (0.5 + 0.5 * math.sin(x / 23)))
        for x in range(w)
    ]


def duzle(zemin: list[int], x0: int, x1: int, y: int, yumusak: int = 30) -> list[int]:
    """Zemin çizgisinde x0-x1 arasını y'de dümdüz yapar, kenarlarda yumuşakça eski çizgiye bağlar.
    Yapıların ve figürlerin duracağı düz şeritleri hazırlamak için."""
    z = list(zemin)
    for x in range(len(z)):
        if x0 <= x <= x1:
            z[x] = y
        elif x0 - yumusak <= x < x0:
            t = (x0 - x) / yumusak
            z[x] = int(y + (zemin[x] - y) * t * t * (3 - 2 * t))
        elif x1 < x <= x1 + yumusak:
            t = (x - x1) / yumusak
            z[x] = int(y + (zemin[x] - y) * t * t * (3 - 2 * t))
    return z


def arazi(img, zemin: list[int], renkler: list[str], kenar: str | None = None, doku_tohum: int | None = None,
          y_bit: int | None = None, perspektif: bool = False):
    """Zemin çizgisinin altını doldurur: derinleştikçe koyulaşan bantlar, üstte ışıklı kenar.
    perspektif=True: bantlar izleyiciye yaklaştıkça genişler (yakın çayır)."""
    ramp = [hex2(r) for r in renkler]
    son = img.height if y_bit is None else y_bit
    for x in range(len(zemin)):
        for y in range(max(0, zemin[x]), son):
            d = y - zemin[x]
            v = math.sqrt(2 * d / BANT) if perspektif else d / BANT
            i = min(len(ramp) - 1, int(v))
            f = v - int(v)
            if i < len(ramp) - 1 and f > 0.6 and _esik(x, y) < (f - 0.6) * 2.5:
                i += 1
            img.putpixel((x, y), ramp[i])
        if kenar and 0 <= zemin[x] < img.height:
            img.putpixel((x, zemin[x]), hex2(kenar))
    if doku_tohum is not None:
        rnd = random.Random(doku_tohum)
        for _ in range(len(zemin) * 3):
            x = rnd.randrange(len(zemin))
            if zemin[x] + 3 >= son:
                continue
            y = rnd.randrange(zemin[x] + 3, son)
            renk = ramp[max(0, min(len(ramp) - 1, (y - zemin[x]) // BANT - 1))]
            piksel(img, x, y, renk)
            piksel(img, x + 1, y, renk)


def zemin_y(zemin: list[int], x: float, genislik: float = 0) -> int:
    """Nesnenin tabanı: ayak izi boyunca zeminin en alçak noktası (nesne asla havada kalmaz)."""
    n = len(zemin)
    x0, x1 = int(max(0, x - genislik / 2)), int(min(n - 1, x + genislik / 2))
    return max(zemin[x0:x1 + 1]) if x1 >= x0 else zemin[int(min(n - 1, max(0, x)))]


class FizikHatasi(ValueError):
    pass


def duz_zemin(zemin: list[int], x0: int, x1: int, ad: str, tolerans: int = 4) -> int:
    """Fizik denetimi: yapılar ancak düz zemine kurulur. Ayak izi boyunca zemin toleranstan
    fazla iniş çıkış yapıyorsa (sarp sırt, tepe yamacı) çizmeyi reddeder; yoksa tabanı verir."""
    parca = zemin[max(0, x0):min(len(zemin), x1 + 1)]
    if not parca:
        raise FizikHatasi(f"{ad}: tuvalin dışında (x {x0}-{x1})")
    fark = max(parca) - min(parca)
    if fark > tolerans:
        raise FizikHatasi(f"{ad}: zemin düz değil (x {x0}-{x1} arasında {fark} piksel iniş çıkış), "
                          f"havada ya da yamaca gömülü görünür; daha düz bir yer seç")
    return max(parca)


def temel(img, zemin: list[int], x0: int, x1: int, y: int, renk: str):
    """Yapının altını zemine bağlayan toprak dolgu: taban ile zemin arasında boşluk kalmaz."""
    d = ImageDraw.Draw(img)
    for x in range(max(0, x0 - 3), min(len(zemin), x1 + 4)):
        if zemin[x] < y + 1:
            d.line([x, zemin[x], x, y + 1], fill=hex2(renk))


def temas_golgesi(img, x, y, genislik, renk="#1a2410", alfa=120):
    """Ayakların bastığı satırda (y-1) koyu, bir üstünde açık titreşimli gölge şeridi."""
    for dx in range(-int(genislik / 2), int(genislik / 2) + 1):
        if abs(dx) < genislik / 2 - 1 or (x + dx + y) % 2 == 0:
            piksel(img, x + dx, y - 1, hex2(renk, alfa))
            if abs(dx) < genislik / 3 and (x + dx) % 2 == 0:
                piksel(img, x + dx, y - 2, hex2(renk, alfa // 2))


def cimen_tutamlari(img, zemin, renkler: list[str], tohum, yogunluk=0.5, boy=4, x0=0, x1=None, ruzgar=0.0):
    rnd = random.Random(tohum)
    ramp = [hex2(r) for r in renkler]
    for x in range(x0, len(zemin) if x1 is None else x1):
        if rnd.random() < yogunluk:
            h = rnd.randint(1, boy)
            renk = rnd.choice(ramp)
            egim = rnd.choice((-1, 0, 0, 1))
            for i in range(h):
                ex = (egim if i > h // 2 else 0) + int(ruzgar * i * i / max(1, h))
                piksel(img, x + ex, zemin[x] - i, renk)


def cicekler(img, zemin, renkler, tohum, adet=20, derinlik=30, x0=0, x1=None):
    rnd = random.Random(tohum)
    for _ in range(adet):
        x = rnd.randrange(x0, len(zemin) if x1 is None else x1)
        y = zemin[x] + rnd.randint(2, derinlik)
        r = hex2(rnd.choice(renkler))
        piksel(img, x, y, r)
        if rnd.random() < 0.5:
            piksel(img, x + 1, y, r)


def cayir_dokusu(img, zemin, renkler: list[str], tohum, yogunluk=0.035, isik: str | None = None):
    """Çayıra perspektifli çimen dokusu: uzakta (üstte) küçük ve seyrek, yakında (altta) uzun
    ve belirgin çimen vuruşları; her vuruşun tepesi ışık alır."""
    rnd = random.Random(tohum)
    ramp = [hex2(r) for r in renkler]
    for x in range(len(zemin)):
        for y in range(max(0, zemin[x]) + 4, img.height):
            yakin = (y - zemin[x]) / max(1, img.height - zemin[x])
            if rnd.random() < yogunluk * (0.4 + yakin):
                boy = 1 + int(yakin * 7 * rnd.random() + rnd.random() * 2)
                renk = rnd.choice(ramp)
                egim = rnd.choice((-1, 0, 0, 1))
                for i in range(boy):
                    ex = egim if i > boy // 2 else 0
                    piksel(img, x + ex, y - i, hex2(isik) if isik and i == boy - 1 and boy > 2 else renk)


def patika(img, zemin, x0, x1, derinlik, renk, tohum):
    """Zemin üzerinde hafif çiğnenmiş toprak yol (titreşimli şerit)."""
    rnd = random.Random(tohum)
    for x in range(x0, x1):
        cy = zemin[x] + derinlik + int(math.sin(x / 40 + tohum) * 4)
        for dy in range(-2, 3):
            if rnd.random() < 0.6 - abs(dy) * 0.15:
                piksel(img, x, cy + dy, hex2(renk, 160))


# ---------------------------------------------------------------- yapılar


def yurt(img, x, zemin, s=1.0, keçe="#efe4cc", golge="#c9b996", kapi="#c8552c", isik=False, isik_gucu=1.0):
    """Moğol yurdu (ger): silindir keçe duvar, alçak kubbe çatı, turuncu kapı, tepe halkası.
    Yalnızca düz zemine kurulur. Dönen değer: baca noktası (duman buradan çıkar)."""
    d = ImageDraw.Draw(img)
    gen = int(26 * s)
    duvar_h, cati_h = int(10 * s), int(8 * s)
    x0, x1 = x - gen // 2, x + gen // 2
    y = duz_zemin(zemin, x0, x1, "yurt", tolerans=max(3, int(2 * s)))
    temas_golgesi(img, x, y, gen + 6)
    d.rectangle([x0, y - duvar_h, x1, y - 1], fill=hex2(keçe), outline=hex2(KOYU))
    d.rectangle([x1 - gen // 4, y - duvar_h + 1, x1 - 1, y - 2], fill=hex2(golge))
    # duvar kafesi (khana) ipuçları ve ip bantları
    for kx in range(x0 + 3, x1 - 1, max(3, int(3 * s))):
        piksel(img, kx, y - duvar_h // 2, hex2(_ac(golge, -0.1), 140))
    for by in (y - duvar_h + 2, y - 3):
        d.line([x0 + 1, by, x1 - 1, by], fill=hex2("#8a5a3a"))
    d.chord([x0 - 1, y - duvar_h - cati_h, x1 + 1, y - duvar_h + cati_h], 180, 360, fill=hex2(keçe), outline=hex2(KOYU))
    for cx in range(x + gen // 5, x1 + 1):
        t = (cx - x) / (gen / 2 + 1)
        tepe = y - duvar_h - int(cati_h * math.sqrt(max(0, 1 - t * t)))
        d.line([cx, tepe + 2, cx, y - duvar_h - 1], fill=hex2(golge))
    for i in range(1, 6):
        ux = x0 + i * gen // 6
        d.line([x, y - duvar_h - cati_h + 2, ux, y - duvar_h - 1], fill=hex2(_ac(golge, -0.08)))
    d.line([x0, y - duvar_h, x1, y - duvar_h], fill=hex2(KOYU))
    d.rectangle([x - max(1, int(2 * s)), y - duvar_h - cati_h, x + max(1, int(2 * s)), y - duvar_h - cati_h + 1], fill=hex2("#8a5a3a"))
    kw, kh = max(3, int(5 * s)), max(5, int(8 * s))
    d.rectangle([x - kw // 2 - 1, y - kh - 1, x + kw // 2 + 1, y - 1], fill=hex2(kapi), outline=hex2(KOYU))
    ic = _ac("#ffc76a", -0.15 * (1 - isik_gucu)) if isik else "#5a2a18"
    d.rectangle([x - kw // 2 + 1, y - kh + 1, x + kw // 2 - 1, y - 2], fill=hex2(ic))
    return (x, y - duvar_h - cati_h)


def kapi_isigi(img, x, y, s, guc=1.0):
    """Açık kapıdan yere düşen sıcak ışık (zeminde, kapının önünde)."""
    kw = max(3, int(5 * s))
    for i in range(0, int(7 * s)):
        for dx in range(-kw // 2 - i // 2, kw // 2 + i // 2 + 1):
            if (dx + i) % 2 == 0:
                piksel(img, x + dx, y + i, hex2("#ffd88a", max(0, int((110 - i * 110 / (7 * s)) * guc))))


def duman(img, x, y, boy, tohum, faz=0.0, renk="#d9d2c4", ruzgar=0.35, genislik=1.0):
    """Bacadan ya da çatıdan yukarı çıkan duman. Puflar faz ile yukarı süzülür; faz 0→1
    bir tam döngüdür ve döngü dikişsiz tekrar eder. Duman hep kaynağından başlar."""
    aralik = 6
    n = boy // aralik + 2
    for k in range(n):
        yy = (k + faz) * aralik
        if yy > boy:
            continue
        cx = x + yy * ruzgar + math.sin(yy / 11 + tohum) * (1.5 + yy / 20)
        r = (1.2 + yy / 9) * genislik
        a = int(210 * (1 - yy / boy) ** 1.2)
        for py in range(int(-r), int(r) + 1):
            for px_ in range(int(-r), int(r) + 1):
                if px_ * px_ + py * py <= r * r:
                    gx, gy = int(cx + px_), int(y - yy + py)
                    if gy <= y and (a > 120 or _esik(gx, gy) < a / 140):
                        piksel(img, gx, gy, hex2(renk if py > -r / 3 else _ac(renk, 0.2), min(255, a)))


def sehir(img, x0, x1, zemin, s=1.0, duvar="#a88a6a", golge="#7a6048", toprak=None, cati="#7a4a34", tohum=1):
    """Surlu şehir: mazgallı duvar, kuleler, kapı ve duvarın üstünden görünen damlar.
    Yalnızca düz ovaya kurulur. Dönen değer: duman çıkabilecek çatı noktaları [(x, y)]."""
    d = ImageDraw.Draw(img)
    rnd = random.Random(tohum)
    y = duz_zemin(zemin, x0 - int(6 * s), x1 + int(6 * s), "şehir", tolerans=max(3, int(3 * s)))
    if toprak:
        temel(img, zemin, x0, x1, y, toprak)

    def u(v):
        return max(1, int(v * s))

    # duvarın arkasındaki evler ve damları
    damlar = []
    for hx in range(x0 + u(6), x1 - u(6), u(9)):
        hh = u(rnd.randint(18, 28))
        hw = u(rnd.randint(6, 8))
        d.rectangle([hx, y - hh, hx + hw, y - u(10)], fill=hex2(_ac(duvar, -0.08)))
        d.polygon([(hx - u(1), y - hh), (hx + hw // 2, y - hh - u(5)), (hx + hw + u(1), y - hh)], fill=hex2(cati))
        d.line([hx + hw // 2, y - hh - u(5), hx + hw + u(1), y - hh], fill=hex2(_ac(cati, -0.25)))
        piksel(img, hx + hw // 2, y - hh + u(3), hex2("#3a2a1e"))
        damlar.append((hx + hw // 2, y - hh - u(5)))
    # sur duvarı
    d.rectangle([x0, y - u(14), x1, y - 1], fill=hex2(duvar))
    for by in range(y - u(12), y - 1, u(4)):
        off = (by // u(4)) % 2 * u(3)
        for bx in range(x0 + off, x1, u(6)):
            piksel(img, bx, by, hex2(golge, 160))
        d.line([x0, by, x1, by], fill=hex2(_ac(duvar, -0.05)))
    for mx in range(x0, x1, u(4)):
        d.rectangle([mx, y - u(16), mx + u(1), y - u(14)], fill=hex2(duvar))
    for kx in range(x0, x1 + 1, max(1, (x1 - x0) // 3)):
        d.rectangle([kx - u(4), y - u(26), kx + u(4), y - 1], fill=hex2(golge))
        d.rectangle([kx + u(1), y - u(26), kx + u(4), y - 1], fill=hex2(_ac(golge, -0.15)))
        d.polygon([(kx - u(5), y - u(26)), (kx, y - u(33)), (kx + u(5), y - u(26))], fill=hex2(cati))
        d.rectangle([kx - u(1), y - u(21), kx, y - u(18)], fill=hex2("#3a2a1e"))
    gx = (x0 + x1) // 2
    d.rectangle([gx - u(3), y - u(9), gx + u(3), y - 1], fill=hex2("#3a2a1e"))
    d.chord([gx - u(3), y - u(12), gx + u(3), y - u(6)], 180, 360, fill=hex2("#3a2a1e"))
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0 + 8, alfa=90)
    return damlar


def orta_asya_sehri(img, x0, x1, zemin, s=1.0, tohum=1, kerpic="#c8a878", golge="#9a7a58", kubbe="#4a9a9a"):
    """Orta Asya / İpek Yolu şehri: kerpiç sur, yuvarlak burçlar (düz, mazgallı tepe), kemerli kapı;
    surun üstünden kubbeli yapılar ve düz damlı evler görünür. Avrupa şatosu gibi sivri kule yok.
    Yalnızca düz ovaya kurulur. Dönen değer: duman çıkabilecek dam noktaları [(x, y)]."""
    d = ImageDraw.Draw(img)
    rnd = random.Random(tohum)
    y = duz_zemin(zemin, x0 - int(4 * s), x1 + int(4 * s), "şehir", tolerans=max(3, int(3 * s)))

    def u(v):
        return max(1, int(v * s))

    damlar = []
    # surun arkasında düz damlı kerpiç evler
    for hx in range(x0 + u(4), x1 - u(8), u(7)):
        hh = u(rnd.randint(17, 24))
        hw = u(rnd.randint(6, 9))
        renk = _ac(kerpic, rnd.uniform(-0.12, 0.05))
        d.rectangle([hx, y - hh, hx + hw, y - u(10)], fill=hex2(renk))
        d.line([hx, y - hh, hx + hw, y - hh], fill=hex2(_ac(renk, 0.2)))  # düz dam kenarı
        d.rectangle([hx + hw // 3, y - hh + u(3), hx + hw // 3 + u(1), y - hh + u(5)], fill=hex2("#3a2a1e"))
        damlar.append((hx + hw // 2, y - hh))
    # kubbeli büyük yapılar (cami/medrese kubbesi) ve ince bir minare
    for kx, kr in ((x0 + (x1 - x0) * 0.35, 9), (x0 + (x1 - x0) * 0.68, 7)):
        kx = int(kx)
        govde_ust = y - u(24)
        d.rectangle([kx - u(kr), govde_ust, kx + u(kr), y - u(10)], fill=hex2(_ac(kerpic, -0.05)))
        d.chord([kx - u(kr), govde_ust - u(kr), kx + u(kr), govde_ust + u(kr)], 180, 360, fill=hex2(kubbe))
        d.chord([kx, govde_ust - u(kr) + 1, kx + u(kr), govde_ust + u(kr)], 270, 360, fill=hex2(_ac(kubbe, -0.25)))
        d.line([kx, govde_ust - u(kr), kx, govde_ust - u(kr) - u(3)], fill=hex2("#e0b040"))
        for i in range(-u(kr) + u(2), u(kr) - u(1), u(4)):  # kemerli pencereler
            d.rectangle([kx + i, govde_ust + u(4), kx + i + u(1), govde_ust + u(8)], fill=hex2("#3a2a1e"))
    mx = int(x0 + (x1 - x0) * 0.52)
    d.rectangle([mx - u(2), y - u(44), mx + u(2), y - u(10)], fill=hex2(_ac(kerpic, 0.06)))
    d.rectangle([mx - u(3), y - u(38), mx + u(3), y - u(36)], fill=hex2(golge))
    d.chord([mx - u(2), y - u(47), mx + u(2), y - u(41)], 180, 360, fill=hex2(kubbe))
    # kerpiç sur: hafif eğimli duvar, yatay kerpiç sıraları
    d.polygon([(x0, y - 1), (x0 + u(1), y - u(14)), (x1 - u(1), y - u(14)), (x1, y - 1)], fill=hex2(kerpic))
    for by in range(y - u(12), y - 1, u(3)):
        d.line([x0 + 1, by, x1 - 1, by], fill=hex2(_ac(kerpic, -0.07)))
    for mx_ in range(x0 + u(1), x1 - u(1), u(4)):  # düz mazgallar
        d.rectangle([mx_, y - u(16), mx_ + u(2), y - u(14)], fill=hex2(kerpic))
    # yuvarlak burçlar: duvardan biraz yüksek, tepesi düz ve mazgallı
    for bx in [x0, x0 + (x1 - x0) // 3, x0 + 2 * (x1 - x0) // 3, x1]:
        d.rectangle([bx - u(5), y - u(18), bx + u(5), y - 1], fill=hex2(_ac(kerpic, -0.04)))  # tabanı düz, zemine oturur
        d.chord([bx - u(5), y - u(21), bx + u(5), y - u(15)], 180, 360, fill=hex2(_ac(kerpic, -0.04)))
        d.rectangle([bx + u(1), y - u(18), bx + u(5), y - 1], fill=hex2(golge))
        d.line([bx - u(5), y - 1, bx + u(5), y - 1], fill=hex2(_ac(golge, -0.2)))  # taban satırı
        for m in range(-u(5), u(5), u(3)):
            d.rectangle([bx + m, y - u(22), bx + m + u(1), y - u(20)], fill=hex2(_ac(kerpic, -0.04)))
    gx = (x0 + x1) // 2
    d.rectangle([gx - u(5), y - u(17), gx + u(5), y - 1], fill=hex2(_ac(kerpic, 0.05)))  # kapı kulesi
    d.chord([gx - u(3), y - u(12), gx + u(3), y - u(4)], 180, 360, fill=hex2("#3a2a1e"))
    d.rectangle([gx - u(3), y - u(8), gx + u(3), y - 1], fill=hex2("#3a2a1e"))
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0 + 10, alfa=90)
    return damlar


def piksel_ok(img, x0, x1, y, kavis=10, kalinlik=4, renk="#fff3d4", kontur="#3a2414"):
    """Sağdan sola giden piksel ok: basamaklı yay gövde ve net '<' ucu, koyu konturlu."""
    d = ImageDraw.Draw(img)
    noktalar = []
    for x in range(x1, x0 - 1, -1):
        u = (x1 - x) / max(1, x1 - x0)
        noktalar.append((x, int(round(y - kavis * math.sin(math.pi * u) - 4 * u))))
    uc_x, uc_y = noktalar[-1]
    bas = kalinlik * 4
    for kat, (renk_, ek) in enumerate(((kontur, 2), (renk, 0))):
        for x, yy in noktalar[:-bas // 2]:
            d.rectangle([x, yy - kalinlik // 2 - ek, x, yy + kalinlik // 2 + ek], fill=hex2(renk_))
        d.polygon([(uc_x - ek * 2, uc_y), (uc_x + bas + ek, uc_y - bas + 1 - ek * 2), (uc_x + bas + ek, uc_y + bas - 1 + ek * 2)],
                  fill=hex2(renk_))
    return (uc_x, uc_y)


def tug(img, x, zemin, s=1.0, faz=0.0, flamalar=("#c8552c", "#3a6aa8", "#e0b040")):
    """Dokuz tuğ geleneğinden esinli beyaz at kılı sancak: direk zemine dikili, dibinde toprak ve
    taş tümseği. faz 0→1: flamalar ve kıl püskülleri rüzgârda dalgalanır (direk hiç kıpırdamaz)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 4)
    temas_golgesi(img, x, y, 22 * s)
    # tümsek
    d.chord([x - int(10 * s), y - int(5 * s), x + int(10 * s), y + int(5 * s)], 180, 360, fill=hex2("#7a5a3a"))
    for i, (dx, r) in enumerate(((-6, 2.2), (5, 2.0), (-1, 2.6), (8, 1.5), (-8, 1.4))):
        cx, cy = x + int(dx * s), y - int(r * s)
        d.ellipse([cx - int(r * s), cy - int(r * s * 0.8), cx + int(r * s), y - 1], fill=hex2(("#8a8478", "#9e978a", "#b2ab9c")[i % 3]))
    tepe = y - int(58 * s)
    d.line([x, y - 2, x, tepe], fill=hex2("#5a3a22"), width=max(1, int(1.6 * s)))
    d.line([x + 1, y - 2, x + 1, tepe], fill=hex2("#7a5232"))
    d.polygon([(x - int(2 * s), tepe), (x, tepe - int(6 * s)), (x + int(2 * s), tepe)], fill=hex2("#e0b040"))
    d.rectangle([x - int(5 * s), tepe + 1, x + int(5 * s), tepe + int(2 * s)], fill=hex2("#7a5232"))
    # at kılı püskül: tepeden sarkar, rüzgârla salınır
    for i in range(int(18 * s)):
        w = 3 + i // 4
        sal = int(math.sin(faz * 2 * math.pi + i / 6) * i / 10)
        for dx in range(-w, w + 1):
            if (dx + i) % 3:
                piksel(img, x + dx + sal, tepe + int(2 * s) + i, hex2("#f4f0e6" if dx < w - 1 else "#c8c0b0"))
    # flamalar: direğin ortasında, rüzgâr yönünde dalgalanır
    for j, renk in enumerate(flamalar):
        fy = tepe + int((26 + j * 8) * s)
        boy = int((22 - j * 3) * s)
        for i in range(boy):
            dalga = math.sin(faz * 2 * math.pi - i / (4 * s) + j) * (i / boy) * 3 * s
            kal = max(1, int((4 - i * 3 / boy) * s))
            for k in range(kal):
                piksel(img, x + 2 + i, int(fy + dalga + k), hex2(renk if k > 0 else _ac(renk, 0.25)))


# ---------------------------------------------------------------- canlılar


def _lerp_nokta(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(2))


def at(img, x, zemin, s=1.0, yon=1, renk="#6b3f24", yele="#2b1a12", binici=None, eyer=False, faz=0.0,
       dur=False, bas=0.0, kulak=0.0, kuyruk=0.0, yuk=None, binici_kadin=False, adim=0.55):
    """Moğol atı (kısa bacaklı, gür yeleli). faz: 0-1 adım döngüsü; dur=True ayakta duran at.
    bas: 0 baş yukarıda, 1 otluyor (ağzı çimende). kulak, kuyruk: -1..1 kıpırdama.
    yuk: yük atı için heybe rengi. Toynaklar zemine basar; binici varsa eyerde oturur."""
    d = ImageDraw.Draw(img)
    gen = int(22 * s)
    y = zemin_y(zemin, x, gen * 0.8)
    bacak = max(3, int(7 * s))
    govde_y = y - bacak
    g = hex2(renk)
    k = hex2(yele)
    acik = hex2(_ac(renk, 0.22))
    koyu_g = hex2(_ac(renk, -0.25))
    temas_golgesi(img, x, y, gen)

    def p(dx, dy):  # at koordinatı (burun yönü +x) -> tuval
        return (x + int(round(dx * s)) * yon, govde_y + int(round(dy * s)))

    # bacaklar: uzaktaki çift koyu, yakındaki çift açık; ön ve arka çift zıt fazda (dörtlü yürüyüş)
    for bx, uzak in ((-7, True), (6, True), (-5, False), (8, False)):
        aci = 0 if dur else math.sin((faz + (0.5 if bx < 0 else 0) + (0.25 if uzak else 0)) * 2 * math.pi) * adim
        ux, uy = p(bx, -1)
        ax = ux + int(math.sin(aci) * bacak) * yon
        kalk = 0 if dur else max(0, math.cos((faz + (0.5 if bx < 0 else 0) + (0.25 if uzak else 0)) * 2 * math.pi))
        ay = y - 1 - int(kalk * min(3, bacak * 0.25))
        diz = (ux + (ax - ux) // 2 + int(kalk * 1.5 * s) * yon, uy + (ay - uy) // 2)
        d.line([ux, uy, *diz], fill=koyu_g if uzak else g, width=max(1, int(1.8 * s)))
        d.line([*diz, ax, ay], fill=koyu_g if uzak else g, width=max(1, int(1.4 * s)))
        d.rectangle([min(ax, ax + yon * max(1, int(s))), ay - max(0, int(s * 0.6)), max(ax, ax + yon * max(1, int(s))), ay], fill=k)
    # gövde: yuvarlak göğüs ve sağrı, aradaki karın
    d.ellipse([*p(-11, -8), *p(-2, 1)] if yon > 0 else [*p(-2, -8), *p(-11, 1)], fill=g)
    d.ellipse([*p(1, -8), *p(10, 1)] if yon > 0 else [*p(10, -8), *p(1, 1)], fill=g)
    d.rectangle([min(p(-7, -8)[0], p(6, -8)[0]), p(0, -8)[1], max(p(-7, 0)[0], p(6, 0)[0]), p(0, 0)[1]], fill=g)
    d.line([p(-9, -7), p(5, -7)], fill=acik)
    d.line([p(-6, 0), p(5, 0)], fill=koyu_g)  # karın gölgesi
    # boyun ve baş: yukarı poz ile otlama pozu arasında
    boyun_y = [(5, -7), (10, -15), (13, -14), (11, -3)]
    boyun_a = [(5, -7), (9, -8), (15, 1), (11, 2)]
    bas_y = [(10, -16), (13, -17), (18, -11), (17, -9), (13, -11)]
    bas_a = [(13, 0), (16, -1), (19, 5), (17, 6.5), (14, 3)]
    boyun = [p(*_lerp_nokta(a, b, bas)) for a, b in zip(boyun_y, boyun_a)]
    kafa = [p(*_lerp_nokta(a, b, bas)) for a, b in zip(bas_y, bas_a)]
    d.polygon(boyun, fill=g)
    d.polygon(kafa, fill=g)
    kb = _lerp_nokta((10, -16), (13, 0), bas)
    d.line([p(*kb), p(kb[0] + 1 + kulak, kb[1] - 2.2)], fill=g, width=max(1, int(s)))  # kulak
    yele_uc = _lerp_nokta((10, -16), (13, 0), bas)
    d.line([p(6, -8), p(*yele_uc)], fill=k, width=max(1, int(1.6 * s)))  # yele
    piksel(img, *p(*_lerp_nokta((13, -14), (15.5, 1.5), bas)), k)  # göz
    piksel(img, *p(*_lerp_nokta((17, -10), (18.5, 5.5), bas)), koyu_g)  # burun
    # kuyruk: sağrıdan sarkar; yürürken geriye savrulur, dururken kıpırdar
    kx, ky = p(-11, -6)
    savrulma = 0 if dur else 0.6
    for i in range(int(9 * s)):
        sal = int(kuyruk * i * 0.35)
        tx = kx - int(i * (0.3 + savrulma * 0.5)) * yon + sal * yon
        ty = ky + int(i * (1 - savrulma * 0.4))
        piksel(img, tx, ty, k)
        piksel(img, tx - yon, ty, k)
    sirt_y = govde_y - int(8 * s)
    if yuk:
        d.rectangle([*p(-6, -11), *p(4, -5)] if yon > 0 else [*p(4, -11), *p(-6, -5)], fill=hex2(yuk), outline=hex2(KOYU))
        d.line([p(-6, -8), p(4, -8)], fill=hex2(_ac(yuk, -0.3)))
    if eyer or binici:
        d.rectangle([x - int(3 * s), sirt_y - 1, x + int(4 * s), sirt_y + int(2 * s)], fill=hex2("#7a2e1e"), outline=hex2(KOYU))
        d.rectangle([x - int(3 * s), sirt_y - int(1.5 * s), x - int(2 * s), sirt_y], fill=hex2("#7a2e1e"))  # eyer kaşı
        d.line([x, sirt_y + int(2 * s), x, govde_y - int(1 * s)], fill=hex2("#3a2a1e"))  # üzengi kayışı
        d.rectangle([x - max(1, int(s * 0.7)), govde_y - int(1 * s), x + max(1, int(s * 0.7)), govde_y - int(0.5 * s)], fill=hex2("#9a8a6a"))
    if binici:
        _binici(img, x, sirt_y, s, yon, binici, binici_kadin, faz if not dur else 0.0)


def _binici(img, x, y, s, yon, deel, kadin=False, faz=0.0):
    d = ImageDraw.Draw(img)
    gv = hex2(deel)
    sek = int(round(math.sin(faz * 4 * math.pi) * 0.5 * s))  # adımla hafif sekme
    y = y - max(0, sek)
    d.rectangle([x - int(2 * s), y - int(9 * s), x + int(2 * s), y], fill=gv)
    d.line([x - int(1 * s) * yon, y - int(1 * s), x + int(1 * s) * yon, y + int(4 * s)], fill=gv, width=max(1, int(2 * s)))  # bacak
    d.line([x + int(4 * s) * yon, y + int(4 * s), x + int(5 * s) * yon, y + int(4 * s)], fill=hex2(KOYU))  # çizme
    d.line([x + int(1 * s) * yon, y - int(7 * s), x + int(5 * s) * yon, y - int(4 * s)], fill=gv, width=max(1, int(1.5 * s)))  # kol
    d.line([x - int(2 * s), y - int(5 * s), x + int(2 * s), y - int(5 * s)], fill=hex2("#e0b040"))  # kuşak
    d.ellipse([x - int(2 * s), y - int(13 * s), x + int(2 * s), y - int(9 * s)], fill=hex2("#d6a07a"))
    if kadin:
        d.rectangle([x - int(3 * s), y - int(15 * s), x + int(3 * s), y - int(12 * s)], fill=hex2("#9a2e3e"))
        d.line([x - int(3 * s) * yon, y - int(12 * s), x - int(4 * s) * yon, y - int(6 * s)], fill=hex2(KOYU), width=max(1, int(s)))  # örgü
    else:
        d.polygon([(x - int(3 * s), y - int(12 * s)), (x, y - int(16 * s)), (x + int(3 * s), y - int(12 * s))], fill=hex2("#5a3a22"))
        d.line([x - int(3 * s), y - int(12 * s), x + int(3 * s), y - int(12 * s)], fill=hex2("#8a6a3a"))


def insan(img, x, zemin, s=1.0, deel="#3a5a8a", bebek=False, kadin=False, adim=None, yon=1, ruzgar=0.0):
    """Ayakta ya da yürüyen insan. adim: None ayakta, 0-1 yürüyüş döngüsü (bir ayak hep yerde).
    ruzgar: pelerin ve saçın rüzgârla savrulması."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    temas_golgesi(img, x, y, 8 * s)
    gv = hex2(deel)
    koyu = hex2(_ac(deel, -0.3))
    kalca = y - int(5 * s)
    if adim is None:
        ayaklar = [(x - int(1.2 * s), y - 1), (x + int(1.2 * s), y - 1)]
    else:
        a = math.sin(adim * 2 * math.pi) * 2.2 * s
        kalk = abs(math.cos(adim * 2 * math.pi))
        ayaklar = [(x + int(a) * yon, y - 1 - (int(kalk * s * 0.8) if a > 0 else 0)),
                   (x - int(a) * yon, y - 1 - (int(kalk * s * 0.8) if a < 0 else 0))]
    for i, (ax, ay) in enumerate(ayaklar):
        d.line([x, kalca, ax, ay], fill=koyu if i == 0 else hex2("#4a3a2a"), width=max(1, int(1.4 * s)))
        d.line([ax, ay, ax + max(1, int(s)) * yon, ay], fill=hex2(KOYU))
    # deel (dize kadar), rüzgârla arkaya savrulan etek
    sav = int(ruzgar * 2 * s) * -yon
    d.polygon([(x - int(3 * s) + min(0, sav), y - int(4 * s)), (x - int(2 * s), y - int(11 * s)), (x + int(2 * s), y - int(11 * s)),
               (x + int(3 * s) + max(0, sav), y - int(4 * s))], fill=gv)
    d.line([x - int(2.5 * s), y - int(7 * s), x + int(2.5 * s), y - int(7 * s)], fill=hex2("#e0b040"))
    # kollar: yürürken bacaklara zıt salınır
    kol = 0 if adim is None else math.sin(adim * 2 * math.pi) * 1.5 * s
    d.line([x, y - int(10 * s), x - int(kol) * yon, y - int(6 * s)], fill=koyu, width=max(1, int(s)))
    # baş: gövdeye oranlı (yakın planda da yetişkin oranı), yüzde göz, yanakta kızarıklık
    bas_y = y - int(13.6 * s)
    r = max(2, int(1.7 * s))
    d.ellipse([x - r, bas_y - r, x + r, bas_y + r], fill=hex2("#d6a07a"))
    if s >= 3:
        d.rectangle([x + int(0.6 * s) * yon, bas_y - int(0.3 * s), x + int(0.6 * s) * yon + max(1, int(0.3 * s)), bas_y], fill=hex2(KOYU))
        piksel(img, x + int(0.4 * s) * yon, bas_y + int(0.7 * s), hex2("#c87a6a"))
    else:
        piksel(img, x + int(1 * s) * yon, bas_y, hex2(KOYU))
    if kadin:
        d.chord([x - r - 1, bas_y - r - 1, x + r + 1, bas_y + r], 180, 360, fill=hex2(KOYU))  # saç
        d.rectangle([x - r - 1, bas_y - r - max(1, int(1.2 * s)), x + r + 1, bas_y - r], fill=hex2("#9a2e3e"))  # başlık
        d.rectangle([x - r - 1, bas_y - r - max(1, int(1.2 * s)), x + r + 1, bas_y - r - max(1, int(1.2 * s)) + max(1, int(0.3 * s))],
                    fill=hex2("#e0b040"))
        for i in range(int(5 * s)):  # rüzgârda savrulan saç örgüsü
            piksel(img, x - r * yon - int(i * ruzgar * 0.6) * yon, bas_y + i, hex2(KOYU))
            if s >= 3:
                piksel(img, x - r * yon - int(i * ruzgar * 0.6) * yon - yon, bas_y + i, hex2(KOYU))
    else:
        d.polygon([(x - r - 1, bas_y - r + 1), (x, bas_y - r - int(2.6 * s)), (x + r + 1, bas_y - r + 1)], fill=hex2("#5a3a22"))
        d.line([x - r - 1, bas_y - r + 1, x + r + 1, bas_y - r + 1], fill=hex2("#8a6a3a"))
    if bebek:  # kundaklı bebek kucakta: kundak, açık yüz
        bx = x + int(1.6 * s) * yon
        by = y - int(9 * s)
        d.ellipse([bx - int(2 * s), by - int(1.6 * s), bx + int(2 * s), by + int(1.6 * s)], fill=hex2("#efe4cc"), outline=hex2(KOYU))
        d.line([bx - int(1.6 * s), by, bx + int(1.6 * s), by], fill=hex2("#c8a878"))
        fx = bx + int(1.1 * s) * yon
        d.ellipse([fx - int(0.8 * s), by - int(1.1 * s), fx + int(0.8 * s), by + int(0.3 * s)], fill=hex2("#e0b090"))
        d.line([x - int(1 * s) * yon, y - int(10 * s), bx, by + int(1 * s)], fill=hex2(_ac(deel, -0.3)), width=max(1, int(s)))  # kucaklayan kol


def okuz(img, x, zemin, s=1.0, yon=1, renk="#5a4030", faz=0.0):
    """Kağnı öküzü: iri gövde, kısa bacak, boynuz, başı önde ve alçakta. Toynaklar zemine basar."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 20 * s)
    bacak = max(3, int(6 * s))
    gy = y - bacak
    g = hex2(renk)
    koyu = hex2(_ac(renk, -0.3))
    temas_golgesi(img, x, y, 24 * s)

    def p(dx, dy):
        return (x + int(round(dx * s)) * yon, gy + int(round(dy * s)))

    for bx, uzak in ((-8, True), (7, True), (-6, False), (9, False)):
        aci = math.sin((faz + (0.5 if bx < 0 else 0) + (0.25 if uzak else 0)) * 2 * math.pi) * 0.35
        ux, uy = p(bx, 0)
        ax = ux + int(math.sin(aci) * bacak) * yon
        d.line([ux, uy, ax, y - 1], fill=koyu if uzak else g, width=max(1, int(2 * s)))
        piksel(img, ax, y - 1, hex2(KOYU))
    d.rounded_rectangle([min(p(-11, -10)[0], p(10, -10)[0]), p(0, -10)[1], max(p(-11, 1)[0], p(10, 1)[0]), p(0, 1)[1]],
                        radius=int(4 * s), fill=g)
    d.polygon([p(4, -10), p(9, -12), p(11, -3)], fill=hex2(_ac(renk, -0.1)))  # hörgüç/omuz
    d.polygon([p(9, -9), p(14, -7), p(15, -2), p(11, -1)], fill=g)  # baş
    d.line([p(12, -8), p(15, -12)], fill=hex2("#e8dcc0"), width=max(1, int(s)))  # boynuz
    d.line([p(11, -8), p(10, -12)], fill=hex2("#d8ccb0"), width=max(1, int(s)))
    piksel(img, *p(13, -6), hex2(KOYU))
    d.line([p(-11, -9), p(-13, -3)], fill=koyu, width=max(1, int(s)))  # kuyruk
    return p(14, -8)  # boyunduruk noktası


def kagni(img, x, zemin, s=1.0, yon=1, faz=0.0, yuk="#d8c8a8"):
    """İki büyük tekerlekli Moğol kağnısı; üstünde katlanmış yurt keçesi ve direkler.
    faz 0→1 tekerlekler döner. Tekerlek altları zemine basar."""
    d = ImageDraw.Draw(img)
    r = int(7 * s)
    y = zemin_y(zemin, x, 26 * s)
    temas_golgesi(img, x, y, 30 * s)
    cx1, cx2 = x - int(7 * s), x + int(7 * s)
    gov_y = y - r - int(2 * s)
    d.rectangle([x - int(13 * s), gov_y - int(2 * s), x + int(13 * s), gov_y + int(1 * s)], fill=hex2("#6a4a2a"), outline=hex2(KOYU))
    # yük: katlanmış keçe, çatı direkleri
    d.rounded_rectangle([x - int(11 * s), gov_y - int(11 * s), x + int(10 * s), gov_y - int(2 * s)], radius=int(2 * s), fill=hex2(yuk), outline=hex2(KOYU))
    d.line([x - int(11 * s), gov_y - int(7 * s), x + int(10 * s), gov_y - int(7 * s)], fill=hex2("#8a5a3a"))
    for i in range(4):
        d.line([x - int(8 * s) + i * int(5 * s), gov_y - int(11 * s), x - int(12 * s) + i * int(5 * s), gov_y - int(15 * s)], fill=hex2("#8a5a3a"))
    # ok (çeki oku) öne uzanır
    ok_uc = (x + int(24 * s) * yon, gov_y - int(1 * s))
    d.line([x + int(13 * s) * yon, gov_y, *ok_uc], fill=hex2("#6a4a2a"), width=max(1, int(s)))
    for cx in (cx1, cx2):
        cy = y - 1 - r
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=hex2("#4a3020"), width=max(1, int(1.4 * s)))
        for k in range(4):
            a = (faz * yon * -1 + k / 8) * 2 * math.pi
            d.line([cx + math.cos(a) * r, cy + math.sin(a) * r, cx - math.cos(a) * r, cy - math.sin(a) * r], fill=hex2("#6a4a2a"))
        d.ellipse([cx - int(1.5 * s), cy - int(1.5 * s), cx + int(1.5 * s), cy + int(1.5 * s)], fill=hex2("#3a2a1e"))
    return ok_uc


def agac(img, x, zemin, s=1.0, yaprak=("#2f5a2a", "#477a34", "#6a9a44"), govde="#4a3022", tohum=1, sallanma=0.0):
    """Yaşlı ağaç: kalın gövde, zemine yayılan kökler, katmanlı taç. Gövde tabanı zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 8 * s)
    temas_golgesi(img, x, y, 30 * s)
    gv = hex2(govde)
    gk = hex2(_ac(govde, -0.3))
    # kökler zemin çizgisine yayılır
    for dx in (-9, -5, 5, 10):
        d.line([x + int(dx * 0.3 * s), y - int(3 * s), x + int(dx * s), y - 1], fill=gv, width=max(1, int(1.5 * s)))
    d.polygon([(x - int(4 * s), y - 1), (x - int(2 * s), y - int(26 * s)), (x + int(2 * s), y - int(28 * s)), (x + int(5 * s), y - 1)], fill=gv)
    d.line([x + int(2 * s), y - int(2 * s), x + int(1 * s), y - int(24 * s)], fill=gk, width=max(1, int(s)))
    d.line([x, y - int(18 * s), x - int(10 * s), y - int(30 * s)], fill=gv, width=max(1, int(2.2 * s)))
    d.line([x + 1, y - int(20 * s), x + int(11 * s), y - int(32 * s)], fill=gv, width=max(1, int(2 * s)))
    rnd = random.Random(tohum)
    for i, renk in enumerate(yaprak):
        for _ in range(12):
            cx = x + rnd.randint(-int(17 * s), int(17 * s)) + i + int(sallanma * s)
            cy = y - int(36 * s) + rnd.randint(-int(9 * s), int(7 * s)) - i * 2
            r = int(rnd.randint(5, 9) * s) - i
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hex2(renk))
        for _ in range(40):  # yaprak benekleri
            px_ = x + rnd.randint(-int(22 * s), int(22 * s))
            py_ = y - int(36 * s) + rnd.randint(-int(14 * s), int(10 * s))
            if img.getpixel((max(0, min(img.width - 1, px_)), max(0, min(img.height - 1, py_))))[3] > 0:
                piksel(img, px_, py_, hex2(_ac(renk, 0.15)))


def taslar(img, x, zemin, s=1.0, cicek=False):
    """Ovoo: üst üste konmuş taş yığını; alttaki büyük taşlar zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 18 * s)
    temas_golgesi(img, x, y, 24 * s)
    sira = [(0, 9, 5, 0), (-7, 6, 4, 0), (7, 6, 4, 0), (-3, 5, 3, 1), (4, 5, 3, 1), (0, 4, 3, 2), (1, 2, 2, 3)]
    for i, (dx, w, h, katman) in enumerate(sira):
        alt = y - 1 if katman == 0 else y - int((katman * 7 - 1) * s)
        cy = alt - int(h * s)
        cx = x + int(dx * s)
        renk = ("#8a8478", "#9e978a", "#b2ab9c")[i % 3]
        d.ellipse([cx - int(w * s), cy - int(h * s), cx + int(w * s), alt], fill=hex2(renk), outline=hex2("#4a4440"))
        d.line([cx - int(w * s) + 2, cy - int(h * s) + 1, cx, cy - int(h * s) + 1], fill=hex2("#d8d2c4"))
        piksel(img, cx + int(w * s * 0.4), cy, hex2("#6a6458"))


def cicek(img, x, zemin, s=1.0, faz=0.0, renk="#f4d24a", orta="#c8552c"):
    """Tek kır çiçeği: kalın sap, dolu yapraklar ve dolu taç yaprakları (taşlarla aynı dolu piksel dili).
    Sap dibi zemine sabit; üst kısmı rüzgârda salınır."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 2)
    temas_golgesi(img, x, y, 10 * s, alfa=90)
    boy = int(13 * s)
    sal = math.sin(faz * 2 * math.pi) * 2.5 * s
    kal = max(2, int(0.7 * s))
    yol = [(x + sal * (i / boy) ** 2, y - 1 - i) for i in range(boy)]
    for px_, py_ in yol:
        d.rectangle([int(px_) - kal // 2, py_, int(px_) + (kal - 1) // 2, py_], fill=hex2("#4a8a32"))
        piksel(img, int(px_) + (kal - 1) // 2, py_, hex2("#6aaa44"))
    for yon, yuk, uz in ((-1, 0.25, 5.5), (1, 0.45, 4.5)):  # dolu yapraklar
        tx, ty = yol[int(boy * yuk)]
        uc = (tx + yon * uz * s + sal * 0.3, ty - 2.5 * s)
        d.polygon([(tx, ty), (tx + yon * uz * s * 0.5, ty - 2.2 * s), uc, (tx + yon * uz * s * 0.55, ty - 0.4 * s)], fill=hex2("#5a9a3a"))
        d.line([(tx, ty), uc], fill=hex2("#3f7a2a"))
    cx, cy = yol[-1]
    r = 2.3 * s
    for k in range(6):  # dolu taç yaprakları
        a = k / 6 * 2 * math.pi + faz * 0.6
        px_, py_ = cx + math.cos(a) * r, cy + math.sin(a) * r * 0.85
        d.ellipse([px_ - 1.5 * s, py_ - 1.2 * s, px_ + 1.5 * s, py_ + 1.2 * s], fill=hex2(renk))
        d.ellipse([px_ - 0.8 * s, py_ - 0.9 * s, px_ + 0.4 * s, py_ + 0.1 * s], fill=hex2(_ac(renk, 0.35)))
    d.ellipse([cx - 1.3 * s, cy - 1.3 * s, cx + 1.3 * s, cy + 1.3 * s], fill=hex2(orta))
    piksel(img, cx - 0.4 * s, cy - 0.4 * s, hex2(_ac(orta, 0.4)))


# ---------------------------------------------------------------- figür işleme


def figur(img, ciz_fn, *args, kontur="#24160e", f_isik=0.18, f_golge=0.22, **kwargs):
    """Figürü ayrı bir katmanda çizer, sonra 64-bit oyun figürü gibi işler: dışına 1 piksel
    koyu kontur, üst kenarlarına ışık, alt kenarlarına gölge. Sonra sahneye bindirir.
    Çizim fonksiyonunun döndürdüğü değeri (ör. yurdun baca noktası) geri verir."""
    katman = yeni(img.width, img.height)
    sonuc = ciz_fn(katman, *args, **kwargs)
    px = katman.load()
    kw, kh = katman.size

    def dolu(x, y):
        return 0 <= x < kw and 0 <= y < kh and px[x, y][3] > 200

    kutu = katman.getbbox()
    if kutu:
        x0, y0, x1, y1 = kutu
        isle = {}
        for y in range(max(0, y0 - 1), min(kh, y1 + 1)):
            for x in range(max(0, x0 - 1), min(kw, x1 + 1)):
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


def sprite_sayfasi(kare_w, kare_h, adet, ciz_kare) -> Image.Image:
    """Yatay şerit sprite sayfası. ciz_kare(tuval, zemin, i) her kareyi çizer; zemin, karenin
    en alt satırına basan düz bir çizgidir (ayaklar son satıra değer)."""
    sayfa = yeni(kare_w * adet, kare_h)
    for i in range(adet):
        kare = yeni(kare_w, kare_h)
        ciz_kare(kare, [kare_h] * kare_w, i)
        sayfa.alpha_composite(kare, (i * kare_w, 0))
    return sayfa


def taban_denetimi(sayfa: Image.Image, kare_w: int, ad: str, bosluk: int = 0):
    """Fizik denetimi (sprite): her karede en alttaki opak piksel, karenin son satırında olmalı.
    Değilse figür zeminin üstünde havada durur."""
    for i in range(sayfa.width // kare_w):
        kare = sayfa.crop((i * kare_w, 0, (i + 1) * kare_w, sayfa.height))
        kutu = kare.split()[3].point(lambda a: 255 if a > 200 else 0).getbbox()
        if not kutu:
            raise FizikHatasi(f"{ad}: {i + 1}. kare boş")
        if kutu[3] < sayfa.height - bosluk:
            raise FizikHatasi(f"{ad}: {i + 1}. karede figürün tabanı son satırdan {sayfa.height - kutu[3]} piksel yukarıda (havada)")
