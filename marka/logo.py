"""SKONSTART tarih sayfası logosu (64-bit piksel sanatı).

Rozet 120x120 ızgarada çizilir ve en yakın komşu yöntemiyle 9 kat büyütülür (1080x1080).
Gün batımında, tepede tuğ tutan bir atlı. Atlı ve tepe zemine oturur, hiçbir şey havada durmaz.

Kullanım: python3 -I marka/logo.py   (çıktılar marka/ altına yazılır)
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

N = 120
OLCEK = 9
KLASOR = Path(__file__).parent
FONT = KLASOR.parent / "video" / "public" / "fonts" / "Jersey10-latin-ext.woff2"
FONT_LAT = KLASOR.parent / "video" / "public" / "fonts" / "Jersey10-latin.woff2"

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

KOYU = (43, 26, 18)
KAHVE = (74, 42, 26)
ALTIN = (240, 190, 80)
ACIK_ALTIN = (255, 228, 150)
GOK = [(46, 38, 92), (112, 60, 120), (206, 92, 92), (244, 150, 80), (252, 206, 118)]
DAG = (126, 74, 112)
DAG2 = (92, 54, 96)


def karis(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gok_rengi(y, x):
    """Dikey gradyan; bantlar arası geçiş Bayer dither ile (kenar yumuşatma yok)."""
    t = y / 92 * (len(GOK) - 1)
    i = min(int(t), len(GOK) - 2)
    f = t - i
    # 3 ara ton, aralarında dither
    adim = f * 3
    k = int(adim)
    kalan = adim - k
    if kalan * 16 > BAYER[y % 4][x % 4]:
        k += 1
    return karis(GOK[i], GOK[i + 1], min(k, 3) / 3)


def tepe_y(x):
    return 93 + int(((x - 60) / 60) ** 2 * 10)


def rozet(yazi: bool = False) -> Image.Image:
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    px = img.load()
    c = (N - 1) / 2

    # gökyüzü
    for y in range(N):
        for x in range(N):
            px[x, y] = (*gok_rengi(min(y, 92), x), 255)

    # güneş ve dither halesi (atlının arkasında, biraz solda)
    gx, gy, gr = 50, 70, 17
    for y in range(N):
        for x in range(N):
            d = math.hypot(x - gx, y - gy)
            if d <= gr:
                px[x, y] = (255, 236, 170, 255) if d < gr - 2 or (x + y) % 2 else (*ALTIN, 255)
            elif d <= gr + 6:
                t = 1 - (d - gr) / 6
                if t * 16 > BAYER[y % 4][x % 4] + 4:
                    px[x, y] = (*karis(px[x, y][:3], (255, 214, 130), 0.55), 255)

    # kuşlar
    for bx, by in ((84, 36), (91, 31), (96, 40)):
        for dx, dy in ((-2, -1), (-1, 0), (1, 0), (2, -1)):
            px[bx + dx, by + dy] = (*KAHVE, 255)

    # uzak dağlar: iki sıra, alt kenarları tepenin altına girer
    for x in range(N):
        y1 = 76 + int(6 * math.sin(x * 0.11) + 3 * math.sin(x * 0.31 + 1))
        y2 = 83 + int(4 * math.sin(x * 0.17 + 2) + 2 * math.sin(x * 0.43))
        for y in range(y1, 100):
            px[x, y] = (*DAG, 255)
        if 0 <= y1 < N:
            px[x, y1] = (*karis(DAG, ALTIN, 0.35), 255)  # sırtta gün ışığı
        for y in range(y2, 100):
            px[x, y] = (*DAG2, 255)

    # tepe
    d = ImageDraw.Draw(img)
    for x in range(N):
        ty = tepe_y(x)
        for y in range(ty, N):
            px[x, y] = (*KOYU, 255)
        px[x, ty] = (*KAHVE, 255)
    # tepe üstünde çimen tutamları
    for x in range(4, N - 4, 5):
        ty = tepe_y(x)
        px[x, ty - 1] = (*KOYU, 255)
        px[x + 1, ty - 2] = (*KOYU, 255)

    # atlı silüeti ayrı katmanda: sonra kenar ışığı verilir
    sil = Image.new("1", (N, N), 0)
    s = ImageDraw.Draw(sil)
    ax = 62
    G = tepe_y(ax)  # toynakların bastığı satır
    k = 1.35

    def p(dx, dy):
        return (ax + round(dx * k), G + round(dy * k))

    # bacaklar (arkalar yerde, bir ön bacak kalkık)
    for a, b in (((-9, -9), (-10, 0)), ((-6, -9), (-6, 0)), ((6, -9), (7, 0))):
        s.line([p(*a), p(*b)], fill=1, width=2)
    s.line([p(9, -9), p(12, -5)], fill=1, width=2)
    s.line([p(12, -5), p(11, -2)], fill=1, width=2)
    s.ellipse([p(-12, -17), p(12, -8)], fill=1)  # gövde
    s.polygon([p(6, -15), p(11, -23), p(15, -22), p(13, -11)], fill=1)  # boyun
    s.polygon([p(11, -24), p(15, -25), p(21, -18), p(19, -16), p(14, -19)], fill=1)  # baş
    s.line([p(13, -25), p(14, -28)], fill=1, width=1)  # kulak
    s.line([p(7, -15), p(11, -23)], fill=1, width=2)  # yele
    s.polygon([p(-11, -15), p(-16, -12), p(-19, -5), p(-17, -4), p(-15, -9), p(-11, -11)], fill=1)  # kuyruk
    # binici
    s.line([p(-1, -15), p(2, -10)], fill=1, width=2)  # bacak, üzengide
    s.polygon([p(-4, -26), p(0, -26), p(1, -16), p(-4, -16)], fill=1)  # gövde
    s.ellipse([p(-4, -31), p(0, -27)], fill=1)  # baş
    s.polygon([p(-5, -29), p(1, -29), p(-2, -35)], fill=1)  # sivri börk
    s.line([p(-1, -23), p(4, -26)], fill=1, width=2)  # tuğu tutan kol
    # tuğ: direk, mızrak ucu, rüzgârda savrulan at kılı
    s.line([p(4, -12), p(4, -52)], fill=1, width=1)
    s.polygon([p(3, -52), p(5, -52), p(4, -57)], fill=1)
    s.ellipse([p(2.5, -51), p(5.5, -48)], fill=1)
    for ux, uy in ((-1, -38), (-3, -39), (-5, -40), (-7, -42), (1, -37), (-4, -37)):
        s.line([p(4, -48), p((4 + ux) / 2 - 1, -45), p(ux, uy)], fill=1, width=1)  # rüzgârda at kılı

    sp = sil.load()
    for y in range(N):
        for x in range(N):
            if sp[x, y]:
                isik = y > 0 and not sp[x, y - 1] and x < 70
                px[x, y] = (*(ALTIN if isik and y < G - 1 else KOYU), 255)

    # yuvarlak çerçeve: koyu halka, içte altın çizgi, dışı şeffaf
    for y in range(N):
        for x in range(N):
            r = math.hypot(x - c, y - c)
            if r > 59.5:
                px[x, y] = (0, 0, 0, 0)
            elif r > 55.5:
                px[x, y] = (*KOYU, 255)
            elif r > 54.3:
                px[x, y] = (*ALTIN, 255)
    return img


def buyut(img: Image.Image, olcek: int = OLCEK) -> Image.Image:
    return img.resize((img.width * olcek, img.height * olcek), Image.NEAREST)


def yazili(rozet_img: Image.Image) -> Image.Image:
    """Kare gönderi/kapak için rozet + yazı (1080x1080, 120x120 ızgara)."""
    buyuk = Image.new("RGBA", (N * OLCEK, N * OLCEK), (*KOYU, 255))
    buyuk.alpha_composite(buyut(rozet_img, 6), (180, 30))
    d = ImageDraw.Draw(buyuk)
    for metin, boy, y, renk in (("SKONSTART", 150, 790, ACIK_ALTIN), ("TARİH", 96, 935, ALTIN)):
        # latin dosyasında İ yok, latin-ext dosyasında ASCII yok: harf harf seçilir
        fl, fe = ImageFont.truetype(str(FONT_LAT), boy), ImageFont.truetype(str(FONT), boy)
        harfler = [(h, fl if h.isascii() else fe) for h in metin]
        w = sum(d.textlength(h, font=f) for h, f in harfler) + 8 * (len(harfler) - 1)
        x = (buyuk.width - w) / 2
        for h, f in harfler:
            for ox, oy in ((-6, 0), (6, 0), (0, -6), (0, 6), (0, 9)):
                d.text((x + ox, y + oy), h, font=f, fill=(*KAHVE, 255))
            d.text((x, y), h, font=f, fill=(*renk, 255))
            x += d.textlength(h, font=f) + 8
    return buyuk


if __name__ == "__main__":
    r = rozet()
    buyut(r).save(KLASOR / "logo-profil.png")
    yazili(r).save(KLASOR / "logo-yazili.png")
    print("marka/logo-profil.png ve marka/logo-yazili.png yazıldı")
