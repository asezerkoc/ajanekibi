"""Cengiz Han portresi (64-bit piksel): kılıcını kaldırmış, sert bakışlı, belden yukarı.

Çıktı: video/public/cengiz-portre.png (540x960 ızgara, saydam). Gövde karenin alt kenarına kadar iner
(belden yukarı portre; kadrajın dışında devam eder, havada durmaz).

Kullanım: python3 -I video/piksel/cengiz.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import ImageDraw  # noqa: E402

from ciz import H, W, _ac, buyut, figur, hex2, piksel, yeni  # noqa: E402

TEN, TEN_G, TEN_I = "#c98c62", "#a06a46", "#e0aa80"
SAC = "#1e140e"
CELIK, CELIK_G, CELIK_I = "#9aa2ac", "#5e666e", "#dce2e8"
KURK, KURK_G, KURK_I = "#6a4a32", "#4a3222", "#8e6a4a"
DEEL, DEEL_G = "#8a2a24", "#5e1a16"
LAMEL, LAMEL_G, LAMEL_I = "#7a6a50", "#4e4232", "#a8946e"
ALTIN, ALTIN_G = "#e0b040", "#9a7420"


def portre(img, cx, cy, s):
    d = ImageDraw.Draw(img)

    def p(x, y):
        return (cx + x * s, cy + y * s)

    def poli(noktalar, renk):
        d.polygon([p(*n) for n in noktalar], fill=hex2(renk))

    def elips(x0, y0, x1, y1, renk):
        d.ellipse([*p(x0, y0), *p(x1, y1)], fill=hex2(renk))

    def cizgi(noktalar, renk, kal=1.0):
        d.line([p(*n) for n in noktalar], fill=hex2(renk), width=max(1, int(kal * s)), joint="curve")

    alt = (H - cy) / s + 2  # gövde karenin altına kadar

    # --- gövde: deel, pullu zırh, kürk yaka
    poli([(-54, 40), (54, 40), (64, alt), (-64, alt)], DEEL)
    poli([(-44, 46), (44, 46), (52, alt), (-52, alt)], LAMEL)
    for sira, y in enumerate(range(50, int(alt), 9)):  # lamel sıraları: kaydırmalı küçük plakalar
        kay = (sira % 2) * 4
        for x in range(-50 + kay, 46, 8):
            elips(x, y, x + 7, y + 8, LAMEL_I if (x // 8 + sira) % 3 == 0 else LAMEL)
            cizgi([(x, y + 8), (x + 7, y + 8)], LAMEL_G, 0.6)
            piksel(img, *p(x + 3.5, y + 3), hex2(_ac(LAMEL_I, 0.25)))
    poli([(-8, 46), (8, 46), (10, alt), (-10, alt)], DEEL_G)  # göğüs ortası kumaş şerit
    elips(-30, 100, 30, 112, ALTIN)  # kemer
    d.rectangle([*p(-6, 99), *p(6, 113)], fill=hex2(ALTIN_G))
    for x, yon in ((-46, -1), (46, 1)):  # omuzluklar
        elips(x - 16, 30, x + 16, 58, CELIK)
        elips(x - 13, 33, x + 8 * yon, 48, CELIK_I)
        cizgi([(x - 14, 50), (x + 14, 50)], CELIK_G, 1.2)
    poli([(-34, 26), (34, 26), (44, 46), (0, 56), (-44, 46)], KURK)  # kürk yaka
    for i in range(-38, 40, 5):
        cizgi([(i, 30 + abs(i) * 0.15), (i + 2, 50 - abs(i) * 0.1)], KURK_I if i % 10 == 0 else KURK_G, 0.6)

    # --- boyun ve baş
    poli([(-9, 14), (9, 14), (11, 30), (-11, 30)], TEN_G)
    elips(-17, -22, 17, 24, TEN)
    poli([(4, -18), (17, -6), (16, 12), (8, 22), (6, 6)], TEN_G)  # yüzün gölge yanı
    elips(-15, -18, -4, 6, TEN_I)  # ışık alan yanak

    # --- sert bakış: içe ve aşağı çatık kalın kaşlar, kısık gözler, alında çizgi
    for yon in (-1, 1):
        poli([(14 * yon, -11), (3 * yon, -5), (3 * yon, -2), (14 * yon, -7)], SAC)  # kaş
        poli([(12 * yon, -3), (4 * yon, -1), (5 * yon, 1), (12 * yon, 0)], "#f0e6d8")  # göz akı (kısık)
        elips(6 * yon - 1.6 if yon > 0 else -8.6, -2.2, 6 * yon + 1.6 if yon > 0 else -5.4, 1.2, SAC)  # göz bebeği
        cizgi([(12 * yon, -3), (4 * yon, -1.5)], SAC, 0.8)  # üst göz kapağı
        cizgi([(13 * yon, 3), (6 * yon, 4)], TEN_G, 0.6)  # göz altı
    cizgi([(-2, -9), (0, -4), (2, -9)], TEN_G, 0.6)  # kaş arası kırışık
    cizgi([(-7, -14), (7, -14)], TEN_G, 0.5)
    # burun
    poli([(-1, -3), (2, -3), (4, 9), (-3, 9)], TEN)
    cizgi([(2, -2), (4, 8)], TEN_G, 0.8)
    elips(-4, 7, 4, 11, TEN_G)
    # ağız: aşağı kıvrık, sıkılı
    cizgi([(-6, 15), (0, 14), (6, 15)], "#5a2018", 1.0)
    cizgi([(-6, 15), (-7, 17)], "#5a2018", 0.6)
    cizgi([(6, 15), (7, 17)], "#5a2018", 0.6)
    # bıyık: uzun, sarkık; sakal: ince, sivri, kır teller
    for yon in (-1, 1):
        cizgi([(1 * yon, 12), (7 * yon, 12), (12 * yon, 17), (14 * yon, 26), (13 * yon, 32)], SAC, 1.6)
    poli([(-6, 18), (6, 18), (3, 30), (0, 38), (-3, 30)], SAC)
    for x in (-2, 1):
        cizgi([(x, 21), (x * 0.5, 34)], "#6a6058", 0.5)

    # --- miğfer: kürk kenar, sivri çelik kubbe, altın tepe, kırmızı püskül, kürk kulaklıklar
    for yon in (-1, 1):
        poli([(15 * yon, -16), (25 * yon, -12), (24 * yon, 14), (17 * yon, 18), (15 * yon, 0)], KURK)
        for y in range(-12, 16, 4):
            cizgi([(17 * yon, y), (23 * yon, y + 2)], KURK_G, 0.5)
    poli([(-21, -18), (0, -52), (21, -18)], CELIK)
    poli([(0, -52), (21, -18), (8, -18)], CELIK_G)
    poli([(-4, -46), (0, -52), (-14, -22), (-17, -20)], CELIK_I)
    for i in range(1, 4):  # perçin
        piksel(img, *p(-14 + i * 7, -21), hex2(CELIK_I))
    elips(-27, -24, 27, -10, KURK)  # kürk kenar
    for x in range(-25, 26, 3):
        cizgi([(x, -22), (x + 1, -12)], KURK_I if x % 6 == 0 else KURK_G, 0.6)
    cizgi([(0, -52), (0, -60)], ALTIN, 1.4)  # tepe sivrisi
    elips(-2.5, -58, 2.5, -54, ALTIN)
    for i in range(14):  # kırmızı at kılı püskül, rüzgârda arkaya savrulur
        cizgi([(0, -60), (6 + i * 0.6, -66 + i * 0.4), (14 + i * 0.9, -58 + i * 1.3)], "#b8302a" if i % 3 else "#7a1a16", 0.7)

    # --- kılıçlı kol: sağ kol yukarı, kavisli kılıç başın yanında yükselir
    poli([(-46, 46), (-70, 34), (-80, -6), (-68, -12), (-56, 22), (-38, 30)], DEEL)
    for y in range(-4, 34, 7):  # kolluk lamelleri
        cizgi([(-76 + (y + 4) * 0.3, y), (-64 + (y + 4) * 0.3, y + 2)], LAMEL_G, 1.0)
    elips(-82, -22, -66, -6, TEN)  # yumruk
    cizgi([(-79, -16), (-69, -16)], TEN_G, 0.6)
    cizgi([(-78, -12), (-70, -12)], TEN_G, 0.6)
    d.rectangle([*p(-78, -6), *p(-70, 6)], fill=hex2("#4a2e1e"))  # kabza (yumruğun altında)
    elips(-77, 6, -71, 11, ALTIN)  # kabza topuzu
    poli([(-86, -24), (-62, -24), (-64, -20), (-84, -20)], ALTIN)  # balçak
    # kavisli namlu: yukarı ve hafif dışa kıvrılır
    namlu = []
    for i in range(0, 121):
        t = i / 120
        namlu.append((-74 - math.sin(t * 1.6) * 26 * t, -24 - t * 150))
    for i in range(len(namlu) - 1):
        (x0, y0), (x1, y1) = namlu[i], namlu[i + 1]
        gen = 4.2 * (1 - (i / 120) ** 3)
        poli([(x0 - gen, y0), (x0 + gen * 0.6, y0), (x1 + gen * 0.6, y1), (x1 - gen, y1)], CELIK)
        cizgi([(x0 + gen * 0.4, y0), (x1 + gen * 0.4, y1)], CELIK_I, 0.6)  # keskin kenar parıltısı
        cizgi([(x0 - gen * 0.5, y0), (x1 - gen * 0.5, y1)], CELIK_G, 0.4)  # oluk
    ux, uy = namlu[-1]
    for k in range(4):  # uçta piksel parıltı
        piksel(img, *p(ux + 3 + k, uy - 3 - k), hex2("#ffffff", 220 - k * 50))
        piksel(img, *p(ux + 3 - k, uy - 3 - k), hex2("#ffffff", 160 - k * 40))

    # --- diğer kol: dirsek dışarıda, eli kemerin üstünde
    poli([(42, 46), (58, 52), (62, 84), (36, 110), (26, 100), (46, 80)], DEEL)
    cizgi([(58, 56), (60, 82)], DEEL_G, 1.0)
    elips(18, 96, 36, 112, TEN)
    cizgi([(22, 102), (32, 102)], TEN_G, 0.6)


def main():
    img = yeni()
    figur(img, portre, 286, 470, 2.4, kontur="#1a0e08", f_isik=0.12, f_golge=0.2)
    hedef = Path(__file__).parents[1] / "public" / "cengiz-portre.png"
    img.save(hedef)
    print("yazıldı:", hedef)
    if "--onizleme" in sys.argv:
        buyut(img).save(sys.argv[sys.argv.index("--onizleme") + 1])


if __name__ == "__main__":
    main()
