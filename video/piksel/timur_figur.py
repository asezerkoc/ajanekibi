"""Timur serisi için yeni figürler ve yapılar (64-bit piksel tarzı, ciz.py ile aynı dil).

Her figür (img, x, zemin, s, ...) alır ve tabanını zemin çizgisine oturtur (zemin_y); ayak, toynak,
tekerlek ya da yapı tabanı zemine basar, altına temas gölgesi düşer. Yapılar yalnızca düz zemine
kurulur (duz_zemin). Gemiler su çizgisine oturur.
"""
from __future__ import annotations

import math
import random

from PIL import ImageDraw

from ciz import KOYU, _ac, _esik, at, duz_zemin, hex2, piksel, temas_golgesi, zemin_y

TEN = "#d6a07a"


def _u(v, s):
    return max(1, int(round(v * s)))


# ---------------------------------------------------------------- insanlar


def _baslik(d, img, x, bas_y, r, s, yon, tur, renk):
    """Başlıklar: börk (sivri keçe), sarık, miğfer, kalpak (kürklü), taç, şapka (Avrupa), kasket, sorguç (Timur)."""
    k = hex2(renk)
    if tur == "bork":
        d.polygon([(x - r - 1, bas_y - r + 1), (x, bas_y - r - int(2.6 * s)), (x + r + 1, bas_y - r + 1)], fill=k)
        d.line([x - r - 1, bas_y - r + 1, x + r + 1, bas_y - r + 1], fill=hex2(_ac(renk, 0.3)))
    elif tur == "sarik":  # büyük beyaz kavuk: Osmanlı
        d.ellipse([x - r - _u(1.6, s), bas_y - r - _u(3.2, s), x + r + _u(1.6, s), bas_y - r + _u(1.2, s)], fill=k)
        d.line([x - r, bas_y - r - _u(1, s), x + r, bas_y - r - _u(2, s)], fill=hex2(_ac(renk, -0.15)))
        d.rectangle([x - _u(0.6, s), bas_y - r - _u(4.2, s), x + _u(0.6, s), bas_y - r - _u(3, s)], fill=hex2("#c8302a"))
    elif tur == "migfer":  # sivri, nazallı demir miğfer
        d.chord([x - r - 1, bas_y - r - 1, x + r + 1, bas_y + r], 180, 360, fill=k)
        d.polygon([(x - _u(1, s), bas_y - r), (x, bas_y - r - _u(2.4, s)), (x + _u(1, s), bas_y - r)], fill=k)
        d.line([x + _u(0.8, s) * yon, bas_y - r, x + _u(0.8, s) * yon, bas_y + _u(0.4, s)], fill=k)
    elif tur == "sovalye":  # kapalı kova miğfer
        d.rectangle([x - r - 1, bas_y - r - 1, x + r + 1, bas_y + r], fill=k)
        d.line([x - r, bas_y - _u(0.2, s), x + r, bas_y - _u(0.2, s)], fill=hex2("#1a1a1e"))
        d.line([x - r - 1, bas_y - r - 1, x + r + 1, bas_y - r - 1], fill=hex2(_ac(renk, 0.35)))
    elif tur == "kalpak":  # kürklü yuvarlak başlık
        d.chord([x - r - 1, bas_y - r - _u(2.2, s), x + r + 1, bas_y + _u(0.5, s)], 180, 360, fill=k)
        d.rectangle([x - r - 1, bas_y - r - _u(0.2, s), x + r + 1, bas_y - r + _u(0.8, s)], fill=hex2(_ac(renk, -0.25)))
    elif tur == "sorguc":  # Timur: koyu kürklü külah, altın şerit, beyaz sorguç tüyü
        d.chord([x - r - 1, bas_y - r - _u(2.6, s), x + r + 1, bas_y - _u(0.2, s)], 180, 360, fill=k)
        d.rectangle([x - r - 1, bas_y - r - _u(0.6, s), x + r + 1, bas_y - r + _u(0.1, s)], fill=hex2("#e0b040"))
        tx = x - _u(0.6, s) * yon
        tepe = bas_y - r - _u(2.2, s)
        for i in range(_u(3.2, s)):
            piksel(img, tx - (i * i // _u(4, s)) * yon, tepe - i, hex2("#f4f0e6"))
        piksel(img, x, bas_y - r - _u(1.6, s), hex2("#c8302a"))
    elif tur == "tac":
        d.rectangle([x - r, bas_y - r - _u(2, s), x + r, bas_y - r + _u(0.4, s)], fill=hex2("#e0b040"))
        for dx in (-r, 0, r):
            d.polygon([(x + dx - _u(0.7, s), bas_y - r - _u(2, s)), (x + dx, bas_y - r - _u(3.4, s)),
                       (x + dx + _u(0.7, s), bas_y - r - _u(2, s))], fill=hex2("#e0b040"))
        piksel(img, x, bas_y - r - _u(1, s), hex2("#c8302a"))
    elif tur == "sapka":  # Kastilyalı elçi: geniş kenarlı şapka
        d.rectangle([x - r - _u(1.8, s), bas_y - r, x + r + _u(1.8, s), bas_y - r + _u(0.6, s)], fill=k)
        d.rectangle([x - r + 1, bas_y - r - _u(2, s), x + r - 1, bas_y - r], fill=k)
    elif tur == "kasket":  # 1941 Sovyet ekibi
        d.chord([x - r - 1, bas_y - r - _u(1.4, s), x + r + 1, bas_y + _u(0.2, s)], 180, 360, fill=k)
        d.line([x, bas_y - r + _u(0.2, s), x + (r + _u(1.8, s)) * yon, bas_y - r + _u(0.4, s)], fill=hex2(_ac(renk, -0.3)), width=_u(0.6, s))
    elif tur == "takke":  # yaşlılar: işlemeli Özbek takkesi
        d.rectangle([x - r, bas_y - r - _u(1.2, s), x + r, bas_y - r + _u(0.4, s)], fill=k)
        d.line([x - r, bas_y - r - _u(0.4, s), x + r, bas_y - r - _u(0.4, s)], fill=hex2("#f4f0e6"))
    elif tur == "ortu":  # kadın: başörtüsü
        d.chord([x - r - 1, bas_y - r - 1, x + r + 1, bas_y + r + 1], 180, 360, fill=k)
        d.rectangle([x - r - 1, bas_y - _u(0.4, s), x - r + _u(0.4, s), bas_y + r + _u(2, s)], fill=k)
        d.rectangle([x + r - _u(0.4, s), bas_y - _u(0.4, s), x + r + 1, bas_y + r + _u(2, s)], fill=k)


def kisi(img, x, zemin, s=1.0, govde="#3a5a8a", bas="bork", bas_renk="#5a3a22", sakal=None, yon=1, adim=None,
         aksak=False, silah=None, kol=0.0, diz=False, kadin=False, ten=TEN, uzun=True, kemer="#e0b040", pelerin=None):
    """Genel insan figürü (ciz.insan'ın oranlarıyla). adim: None ayakta, 0-1 yürüyüş; aksak=True sağ bacak
    sürünür (Timur). silah: kilic, mizrak, kalkan, kurek, testi, mektup, kamera, mesale, yay, kazma, sopa.
    kol: 0 yanda, 1 yukarı kaldırılmış (silah savurma). diz=True: tek diz üstünde (dizi zemine değer)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    temas_golgesi(img, x, y, 8 * s)
    gv = hex2(govde)
    koyu = hex2(_ac(govde, -0.3))
    kalca = y - int(5 * s) - 0
    if diz:  # iki diz yerde (saygıyla diz çökme): uyluklar öne iner, baldırlar yerde arkaya uzanır
        kalca = y - int(3 * s)
        for k, renk in ((0, koyu), (1, hex2("#4a3a2a"))):
            diz_x = x + int((2 + k * 0.6) * s) * yon
            d.line([x, kalca, diz_x, y - 1], fill=renk, width=_u(1.4, s))
            d.line([diz_x, y - 1, x - int(3 * s) * yon, y - 1], fill=renk, width=_u(1.2, s))
        d.line([x - int(3 * s) * yon, y - 1, x - int(4 * s) * yon, y - 1], fill=hex2(KOYU))
    else:
        if adim is None:
            ayaklar = [(x - int(1.2 * s), y - 1), (x + int(1.2 * s), y - 1)]
        else:
            a = math.sin(adim * 2 * math.pi) * 2.2 * s
            kalk = abs(math.cos(adim * 2 * math.pi))
            ayaklar = [(x + int(a) * yon, y - 1 - (int(kalk * s * 0.8) if a > 0 else 0)),
                       (x - int(a) * yon, y - 1 - (int(kalk * s * 0.8) if a < 0 else 0))]
            if aksak:  # sağ bacak sürünür: neredeyse kalkmaz, adımı kısa
                ayaklar[1] = (x - int(a * 0.45) * yon, y - 1)
        for i, (ax, ay) in enumerate(ayaklar):
            d.line([x, kalca, ax, ay], fill=koyu if i == 0 else hex2("#4a3a2a"), width=_u(1.4, s))
            d.line([ax, ay, ax + _u(1, s) * yon, ay], fill=hex2(KOYU))
    # aksak yürüyüşte gövde topal bacağa doğru iner
    egil = int(abs(math.sin((adim or 0) * 2 * math.pi)) * 0.8 * s) if (aksak and adim is not None) else 0
    yy = y + egil + (int(2 * s) if diz else 0)
    ust = yy - int(11 * s)
    alt = yy - int(4 * s) if uzun else yy - int(6 * s)
    if diz:
        alt = kalca
    if pelerin:
        d.polygon([(x - int(2 * s), ust), (x - int(4.5 * s) * yon, alt + int(1 * s)), (x - int(1 * s) * yon, alt + int(1 * s))],
                  fill=hex2(pelerin))
    d.polygon([(x - int(3 * s), alt), (x - int(2 * s), ust), (x + int(2 * s), ust), (x + int(3 * s), alt)], fill=gv)
    if kemer:
        d.line([x - int(2.5 * s), ust + int(4 * s), x + int(2.5 * s), ust + int(4 * s)], fill=hex2(kemer))
    if kadin:
        d.line([x - int(1 * s), ust + int(1 * s), x + int(1 * s), ust + int(1 * s)], fill=hex2(_ac(govde, 0.25)))
    # kol ve el aleti
    omuz = (x + int(0.5 * s) * yon, ust + int(1 * s))
    if kol > 0:
        el = (x + int(3.5 * s) * yon, ust - int(4 * s * kol) + int(1 * s))
    else:
        sal = 0 if adim is None else math.sin(adim * 2 * math.pi) * 1.5 * s
        el = (x + int(2.5 * s) * yon - int(sal) * yon, ust + int(5 * s))
    d.line([*omuz, *el], fill=koyu, width=_u(1, s))
    piksel(img, el[0], el[1], hex2(ten))
    ex, ey = el
    if silah == "kilic":
        uc = (ex + int(7 * s * (0.4 if kol > 0 else 1)) * yon, ey - int(7 * s * (1 if kol > 0 else 0.15)))
        d.line([ex, ey, *uc], fill=hex2("#d8dce0"), width=_u(0.7, s))
        d.line([ex - _u(1, s), ey + _u(0.5, s), ex + _u(1, s), ey - _u(0.5, s)], fill=hex2("#e0b040"))
    elif silah == "mizrak":
        d.line([ex, ey + int(5 * s), ex, ey - int(16 * s)], fill=hex2("#5a3a22"), width=_u(0.7, s))
        d.polygon([(ex - _u(1.2, s), ey - int(16 * s)), (ex, ey - int(20 * s)), (ex + _u(1.2, s), ey - int(16 * s))], fill=hex2("#c8ccd0"))
    elif silah == "kalkan":
        d.ellipse([ex - int(2.6 * s), ey - int(3.2 * s), ex + int(2.6 * s), ey + int(3.2 * s)], fill=hex2("#8a3a22"), outline=hex2("#e0b040"))
        piksel(img, ex, ey, hex2("#e0b040"))
    elif silah == "kurek":
        d.line([ex, ey - int(3 * s), ex + int(1 * s) * yon, min(ey + int(6 * s), y - 4)], fill=hex2("#6a4a2a"), width=_u(0.7, s))
        alt_ = min(ey + int(8.5 * s), y - 2)
        d.rectangle([ex + int(0.2 * s) * yon - _u(1, s), alt_ - int(2.5 * s), ex + int(1.6 * s) * yon + _u(1, s), alt_], fill=hex2("#9a9aa0"))
    elif silah == "kazma":
        d.line([ex, ey, ex + int(2 * s) * yon, ey - int(6 * s)], fill=hex2("#6a4a2a"), width=_u(0.7, s))
        d.line([ex + int(0 * s) * yon, ey - int(6.5 * s), ex + int(4 * s) * yon, ey - int(5 * s)], fill=hex2("#9a9aa0"), width=_u(0.8, s))
    elif silah == "testi":
        d.ellipse([ex - int(1.6 * s), ey - int(1 * s), ex + int(1.6 * s), ey + int(3 * s)], fill=hex2("#c8a040"), outline=hex2("#7a5a22"))
        d.rectangle([ex - _u(0.6, s), ey - int(2 * s), ex + _u(0.6, s), ey - int(1 * s)], fill=hex2("#c8a040"))
    elif silah == "mektup":
        d.rectangle([ex - int(1.5 * s), ey - int(2 * s), ex + int(1.5 * s), ey + int(1 * s)], fill=hex2("#f0e0b0"), outline=hex2("#8a6a3a"))
        piksel(img, ex, ey, hex2("#c8302a"))
    elif silah == "mesale":  # elde tutulan meşale: sap elden öne-yukarı çıkar, alev sapın ucunda
        uc = (ex + int(2 * s) * yon, ey - int(7 * s))
        d.line([ex, ey + int(1.5 * s), *uc], fill=hex2("#5a3216"), width=_u(1, s))
        d.rectangle([uc[0] - _u(0.8, s), uc[1], uc[0] + _u(0.8, s), uc[1] + _u(1.2, s)], fill=hex2("#3a2010"))
        for r, renk in ((2.6, "#e8601c"), (1.6, "#f8a030"), (0.8, "#fff0a0")):
            d.polygon([(uc[0] - r * s * 0.5, uc[1]), (uc[0], uc[1] - r * s * 1.6), (uc[0] + r * s * 0.5, uc[1])], fill=hex2(renk))
    elif silah == "yay":
        d.arc([ex - int(2 * s), ey - int(6 * s), ex + int(2 * s), ey + int(6 * s)], 270 if yon > 0 else 90, 90 if yon > 0 else 270,
              fill=hex2("#6a3a1a"), width=_u(0.7, s))
    elif silah == "sopa":
        d.line([ex, ey + int(6 * s), ex - int(1 * s) * yon, ey - int(8 * s)], fill=hex2("#6a4a2a"), width=_u(0.7, s))
    elif silah == "kamera":  # 1941: tripodlu film kamerası
        cx = ex + int(3 * s) * yon
        d.line([cx, ey + int(1 * s), cx - int(2 * s), y - 1], fill=hex2("#3a3a3a"), width=_u(0.6, s))
        d.line([cx, ey + int(1 * s), cx + int(2 * s), y - 1], fill=hex2("#3a3a3a"), width=_u(0.6, s))
        d.line([cx, ey + int(1 * s), cx, y - 1], fill=hex2("#3a3a3a"), width=_u(0.6, s))
        d.rectangle([cx - int(2 * s), ey - int(2 * s), cx + int(2 * s), ey + int(1 * s)], fill=hex2("#2a2a2e"))
        d.ellipse([cx - int(2.6 * s), ey - int(4.6 * s), cx - int(0.6 * s), ey - int(2.6 * s)], outline=hex2("#5a5a5e"))
        d.ellipse([cx + int(0.6 * s), ey - int(4.6 * s), cx + int(2.6 * s), ey - int(2.6 * s)], outline=hex2("#5a5a5e"))
        a_, b_ = cx + int(2 * s) * yon, cx + int(3 * s) * yon
        d.rectangle([min(a_, b_), ey - int(1 * s), max(a_, b_), ey], fill=hex2("#6a6a70"))
    # baş
    bas_y = yy - int(13.6 * s)
    r = max(2, int(1.7 * s))
    d.ellipse([x - r, bas_y - r, x + r, bas_y + r], fill=hex2(ten))
    if s >= 3:
        d.rectangle([x + int(0.6 * s) * yon, bas_y - int(0.3 * s), x + int(0.6 * s) * yon + _u(0.3, s), bas_y], fill=hex2(KOYU))
    else:
        piksel(img, x + int(1 * s) * yon, bas_y, hex2(KOYU))
    if sakal:
        d.polygon([(x - r + _u(0.5, s), bas_y + _u(0.4, s)), (x + r, bas_y + _u(0.4, s)), (x + int(0.6 * s) * yon, bas_y + r + _u(2, s))],
                  fill=hex2(sakal))
    if bas:
        _baslik(d, img, x, bas_y, r, s, yon, bas, bas_renk)


def timur(img, x, zemin, s=1.0, yon=1, adim=None, silah=None, kol=0.0, yasli=False, diz=False):
    """Timur: koyu kırmızı kaftan, altın kemer, kürklü sorguçlu külah, kızıl sakal; sağ bacağı aksak."""
    kisi(img, x, zemin, s, "#7a1e22", "sorguc", "#2a1a14", "#d8d0c8" if yasli else "#a8522a", yon, adim, aksak=True,
         silah=silah, kol=kol, diz=diz, pelerin="#3a2a5a")


def bayezid(img, x, zemin, s=1.0, yon=1, adim=None, silah=None, kol=0.0, diz=False):
    """Yıldırım Bayezid: beyaz büyük kavuk, yeşil kaftan, kara sakal."""
    kisi(img, x, zemin, s, "#2a6a3a", "sarik", "#f4f0e6", "#2a1a14", yon, adim, silah=silah, kol=kol, diz=diz, pelerin="#c8a040")


def oturan(img, x, zemin, s=1.0, govde="#3a5a8a", bas="bork", bas_renk="#5a3a22", sakal=None, yon=1, ten=TEN, el=None, minder=None):
    """Bağdaş kurup oturan kişi: dizler zemine (ya da mindere) değer. el: 'testi', 'kase', 'kalem'."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 10 * s)
    temas_golgesi(img, x, y, 12 * s)
    if minder:
        d.rectangle([x - int(5 * s), y - int(1.6 * s), x + int(5 * s), y - 1], fill=hex2(minder), outline=hex2(_ac(minder, -0.35)))
        y -= int(1.6 * s)
    gv = hex2(govde)
    koyu = hex2(_ac(govde, -0.3))
    d.ellipse([x - int(5 * s), y - int(3 * s), x + int(5 * s), y - 1], fill=koyu)  # bağdaş bacaklar
    ust = y - int(9.5 * s)
    d.polygon([(x - int(3 * s), y - int(2 * s)), (x - int(2 * s), ust), (x + int(2 * s), ust), (x + int(3 * s), y - int(2 * s))], fill=gv)
    d.line([x - int(2.5 * s), ust + int(4 * s), x + int(2.5 * s), ust + int(4 * s)], fill=hex2("#e0b040"))
    el_ = (x + int(3 * s) * yon, y - int(4.5 * s))
    d.line([x + int(0.5 * s) * yon, ust + int(1 * s), *el_], fill=koyu, width=_u(1, s))
    if el == "kase":
        d.chord([el_[0] - int(1.6 * s), el_[1] - int(1.6 * s), el_[0] + int(1.6 * s), el_[1] + int(1.2 * s)], 0, 180, fill=hex2("#e8e0d0"))
    elif el == "testi":
        d.ellipse([el_[0] - int(1.4 * s), el_[1] - int(1 * s), el_[0] + int(1.4 * s), el_[1] + int(2.4 * s)], fill=hex2("#c8a040"))
    bas_y = ust - int(2.6 * s)
    r = max(2, int(1.7 * s))
    d.ellipse([x - r, bas_y - r, x + r, bas_y + r], fill=hex2(ten))
    piksel(img, x + int(1 * s) * yon, bas_y, hex2(KOYU))
    if sakal:
        d.polygon([(x - r + _u(0.5, s), bas_y + _u(0.4, s)), (x + r, bas_y + _u(0.4, s)), (x + int(0.6 * s) * yon, bas_y + r + _u(2, s))],
                  fill=hex2(sakal))
    if bas:
        _baslik(d, img, x, bas_y, r, s, yon, bas, bas_renk)


def sedir(img, x, zemin, s=1.0, renk="#7a4a2a", ortu="#8a2a2a"):
    """Alçak ahşap sedir (yatak): dört ayağı zemine basar. Üst yüzünün y'sini döndürür."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 24 * s)
    temas_golgesi(img, x, y, 26 * s)
    ust = y - int(5 * s)
    for ax in (-11, -4, 4, 11):
        d.rectangle([x + int(ax * s) - _u(0.6, s), ust, x + int(ax * s) + _u(0.6, s), y - 1], fill=hex2(_ac(renk, -0.25)))
    d.rectangle([x - int(12 * s), ust - int(1.6 * s), x + int(12 * s), ust], fill=hex2(renk), outline=hex2(KOYU))
    d.rectangle([x - int(12 * s), ust - int(2.6 * s), x + int(12 * s), ust - int(1.6 * s)], fill=hex2(ortu))
    return ust - int(2.6 * s)


def yatan(img, x, zemin, s=1.0, govde="#7a1e22", bas="sorguc", bas_renk="#2a1a14", sakal="#d8d0c8", yon=1, ortu="#e8e0d0",
          nefes=0.0):
    """Sedirde uzanan hasta: başı yastıkta, üstünde yorgan; nefes 0-1 göğsü hafifçe kaldırır."""
    d = ImageDraw.Draw(img)
    ust = sedir(img, x, zemin, s)
    bas_x = x - int(9 * s) * yon
    d.rectangle([bas_x - int(2.5 * s), ust - int(2 * s), bas_x + int(2.5 * s), ust], fill=hex2("#f0e8d8"))  # yastık
    kabar = int(nefes * 0.8 * s)
    d.rounded_rectangle([min(x - int(7 * s) * yon, x + int(11 * s) * yon), ust - int(3.6 * s) - kabar,
                         max(x - int(7 * s) * yon, x + int(11 * s) * yon), ust], radius=_u(1.5, s), fill=hex2(ortu))
    d.line([x - int(6 * s) * yon, ust - int(3.6 * s) - kabar, x + int(10 * s) * yon, ust - int(3.6 * s) - kabar], fill=hex2(_ac(ortu, 0.3)))
    r = max(2, int(1.7 * s))
    by = ust - int(3.4 * s)
    d.ellipse([bas_x - r, by - r, bas_x + r, by + r], fill=hex2(TEN))
    if sakal:
        d.polygon([(bas_x + _u(0.5, s) * yon, by + r - 1), (bas_x + int(3.6 * s) * yon, by + int(0.5 * s)), (bas_x + r * yon, by - _u(0.4, s))],
                  fill=hex2(sakal))
    piksel(img, bas_x, by - _u(0.5, s), hex2(KOYU))


# ---------------------------------------------------------------- hayvanlar ve atlılar


def atli(img, x, zemin, s=1.0, yon=1, faz=0.0, at_renk="#6b3f24", yele="#2b1a12", govde="#3a5a8a", bas="bork",
         bas_renk="#5a3a22", sakal=None, silah=None, kol=0.0, adim=0.55, dur=False, zirh=None, cul=None, bayrak=None):
    """Atlı savaşçı: at (ciz.at) ve eyerdeki binici. zirh: binicinin zırh rengi; cul: atın zırh örtüsü
    (Sırp şövalyesi); bayrak: mızrak ucundaki flama rengi."""
    at(img, x, zemin, s, yon, at_renk, yele, binici=None, eyer=True, faz=faz, dur=dur, adim=adim)
    d = ImageDraw.Draw(img)
    gen = int(22 * s)
    yz = zemin_y(zemin, x, gen * 0.8)
    govde_y = yz - max(3, int(7 * s))
    if cul:  # atın sırtından dizlerine inen örtü
        d.polygon([(x - int(11 * s), govde_y - int(7 * s)), (x + int(9 * s), govde_y - int(7 * s)), (x + int(10 * s), govde_y + int(2 * s)),
                   (x - int(12 * s), govde_y + int(2 * s))], fill=hex2(cul))
        for i in range(-11, 10, 3):
            piksel(img, x + int(i * s), govde_y + int(2 * s), hex2(_ac(cul, -0.3)))
    sy = govde_y - int(8 * s)
    sek = 0 if dur else int(round(math.sin(faz * 4 * math.pi) * 0.5 * s))
    sy -= max(0, sek)
    gv = hex2(zirh or govde)
    d.rectangle([x - int(2 * s), sy - int(9 * s), x + int(2 * s), sy], fill=gv)
    if zirh:
        for k in range(1, 4):
            d.line([x - int(2 * s), sy - int(k * 2.4 * s), x + int(2 * s), sy - int(k * 2.4 * s)], fill=hex2(_ac(zirh, -0.25)))
    d.line([x - int(1 * s) * yon, sy - int(1 * s), x + int(1 * s) * yon, sy + int(4 * s)], fill=hex2(govde), width=_u(2, s))
    d.line([x + int(1 * s) * yon, sy + int(4 * s), x + int(2.5 * s) * yon, sy + int(4 * s)], fill=hex2(KOYU))
    d.line([x - int(2 * s), sy - int(5 * s), x + int(2 * s), sy - int(5 * s)], fill=hex2("#e0b040"))
    omuz = (x + int(1 * s) * yon, sy - int(7 * s))
    if kol > 0:
        el = (x + int(4 * s) * yon, sy - int(7 * s) - int(5 * s * kol))
    else:
        el = (x + int(5 * s) * yon, sy - int(4 * s))
    d.line([*omuz, *el], fill=gv, width=_u(1.4, s))
    ex, ey = el
    if silah == "kilic":
        uc = (ex + int(6 * s) * yon, ey - int(6 * s * (1 if kol > 0 else 0.3)))
        d.line([ex, ey, *uc], fill=hex2("#d8dce0"), width=_u(0.7, s))
    elif silah == "mizrak":
        uc = (ex + int(14 * s) * yon, ey - int(3 * s))
        d.line([ex - int(6 * s) * yon, ey + int(1 * s), *uc], fill=hex2("#6a4a2a"), width=_u(0.7, s))
        d.polygon([(uc[0], uc[1] - _u(1, s)), (uc[0] + int(3 * s) * yon, uc[1]), (uc[0], uc[1] + _u(1, s))], fill=hex2("#c8ccd0"))
        if bayrak:
            for i in range(int(5 * s)):
                dal = math.sin(faz * 2 * math.pi + i / 2) * 0.8 * s
                for k in range(int(2 * s)):
                    piksel(img, uc[0] - int(1 * s) * yon - i * yon, uc[1] + k + dal + 1, hex2(bayrak))
    elif silah == "yay":
        d.arc([ex - int(2 * s), ey - int(6 * s), ex + int(2 * s), ey + int(6 * s)], 270 if yon > 0 else 90, 90 if yon > 0 else 270,
              fill=hex2("#6a3a1a"), width=_u(0.7, s))
    elif silah == "mektup":
        d.rectangle([ex - int(1.5 * s), ey - int(2 * s), ex + int(1.5 * s), ey + int(1 * s)], fill=hex2("#f0e0b0"), outline=hex2("#8a6a3a"))
    bas_y = sy - int(11 * s)
    r = max(2, int(1.7 * s))
    d.ellipse([x - r, bas_y - r, x + r, bas_y + r], fill=hex2(TEN))
    piksel(img, x + int(1 * s) * yon, bas_y, hex2(KOYU))
    if sakal:
        d.polygon([(x - r + _u(0.5, s), bas_y + _u(0.4, s)), (x + r, bas_y + _u(0.4, s)), (x + int(0.6 * s) * yon, bas_y + r + _u(2, s))],
                  fill=hex2(sakal))
    if bas:
        _baslik(d, img, x, bas_y, r, s, yon, bas, bas_renk)


def koyun(img, x, zemin, s=1.0, yon=1, faz=0.0, renk="#ece4d4", kos=False):
    """Kıvırcık yünlü koyun: kara baş ve bacaklar; koşarken bacaklar açılıp kapanır."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 8 * s)
    temas_golgesi(img, x, y, 10 * s)
    bacak = _u(3, s)
    gy = y - bacak
    for bx in (-3, -1.5, 2, 3.5):
        a = math.sin((faz + (0.5 if bx < 0 else 0)) * 2 * math.pi) * (1.4 if kos else 0.4) * s
        d.line([x + int(bx * s) * yon, gy, x + int(bx * s + a) * yon, y - 1], fill=hex2("#2a2420"), width=_u(0.8, s))
    d.ellipse([x - int(5 * s), gy - int(5 * s), x + int(5 * s), gy + int(1 * s)], fill=hex2(renk))
    for i in range(int(6 * s)):  # yün kıvrımları
        piksel(img, x - int(4 * s) + i * 1.6, gy - int(4.4 * s) + (i % 2), hex2(_ac(renk, 0.4)))
    hx = x + int(5 * s) * yon
    d.ellipse([hx - int(1.6 * s), gy - int(5 * s), hx + int(1.6 * s), gy - int(1.6 * s)], fill=hex2("#2a2420"))
    piksel(img, hx + int(1 * s) * yon, gy - int(4 * s), hex2("#c8c0b0"))


def fil(img, x, zemin, s=1.0, yon=1, faz=0.0, renk="#8a8a90", kule=True, binici="#c8a040", adim=0.35):
    """Savaş fili (Delhi): kalın sütun bacaklar zemine basar, sallanan hortum, fildişi, sırtında kule (hevdec)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 30 * s)
    temas_golgesi(img, x, y, 34 * s)
    g = hex2(renk)
    koyu = hex2(_ac(renk, -0.25))
    bacak = int(10 * s)
    gy = y - bacak

    def p(dx, dy):
        return (x + int(round(dx * s)) * yon, gy + int(round(dy * s)))

    for bx, uzak in ((-10, True), (8, True), (-7, False), (11, False)):
        a = math.sin((faz + (0.5 if bx < 0 else 0) + (0.25 if uzak else 0)) * 2 * math.pi) * adim
        ux, uy = p(bx, -2)
        ax = ux + int(math.sin(a) * bacak) * yon
        d.line([ux, uy, ax, y - 1], fill=koyu if uzak else g, width=_u(4, s))
        d.rectangle([ax - _u(2, s), y - _u(1, s), ax + _u(2, s), y - 1], fill=hex2("#d8d0c0"))  # tırnaklar
    d.ellipse([*p(-15, -18), *p(15, 2)] if yon > 0 else [*p(15, -18), *p(-15, 2)], fill=g)
    d.line([p(-12, -15), p(10, -16)], fill=hex2(_ac(renk, 0.2)))
    # baş, kulak, hortum
    d.ellipse([*p(9, -20), *p(21, -6)] if yon > 0 else [*p(21, -20), *p(9, -6)], fill=g)
    d.ellipse([*p(7, -19), *p(14, -7)] if yon > 0 else [*p(14, -19), *p(7, -7)], fill=koyu)  # kulak
    sal = math.sin(faz * 2 * math.pi) * 2.5
    onceki = p(19, -10)
    for i in range(1, 13):
        t = i / 12
        nx, ny = p(20 + t * 3 + sal * t * t, -10 + t * 16 - t * t * 3)
        d.line([*onceki, nx, ny], fill=g, width=_u(2.6 - t * 1.2, s))
        onceki = (nx, ny)
    d.line([p(18, -8), p(24, -9)], fill=hex2("#f4ecd8"), width=_u(1, s))  # fildişi
    piksel(img, *p(17, -15), hex2(KOYU))
    d.line([p(-15, -10), p(-17, -2)], fill=koyu, width=_u(0.8, s))  # kuyruk
    if kule:
        d.rectangle([*p(-8, -19), *p(6, -17)] if yon > 0 else [*p(6, -19), *p(-8, -17)], fill=hex2("#9a2a2a"))
        d.rectangle([min(p(-7, -28)[0], p(5, -28)[0]), p(0, -28)[1], max(p(-7, -19)[0], p(5, -19)[0]), p(0, -19)[1]],
                    fill=hex2("#c8a040"), outline=hex2(KOYU))
        d.chord([min(p(-8, -33)[0], p(6, -33)[0]), p(0, -33)[1], max(p(-8, -23)[0], p(6, -23)[0]), p(0, -23)[1]], 180, 360, fill=hex2("#9a2a2a"))
        hx, hy = p(-1, -28)
        d.rectangle([hx - _u(1.5, s), hy - _u(4, s), hx + _u(1.5, s), hy], fill=hex2(binici))
        d.ellipse([hx - _u(1.5, s), hy - _u(7, s), hx + _u(1.5, s), hy - _u(4, s)], fill=hex2("#b07a5a"))
        d.ellipse([hx - _u(1.8, s), hy - _u(8.2, s), hx + _u(1.8, s), hy - _u(6, s)], fill=hex2("#f4f0e6"))


def deve(img, x, zemin, s=1.0, yon=1, faz=0.0, renk="#b08a5a", yuk="#8a3a2a", adim=0.4):
    """Çift hörgüçlü (Baktriya) devesi: uzun bacaklar, kıvrık boyun, hörgüçler arasında yük."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 22 * s)
    temas_golgesi(img, x, y, 24 * s)
    g = hex2(renk)
    koyu = hex2(_ac(renk, -0.25))
    bacak = int(11 * s)
    gy = y - bacak

    def p(dx, dy):
        return (x + int(round(dx * s)) * yon, gy + int(round(dy * s)))

    for bx, uzak in ((-8, True), (6, True), (-6, False), (8, False)):
        a = math.sin((faz + (0.5 if bx < 0 else 0) + (0.25 if uzak else 0)) * 2 * math.pi) * adim
        ux, uy = p(bx, -1)
        ax = ux + int(math.sin(a) * bacak) * yon
        diz = (ux + (ax - ux) // 2, uy + (y - uy) // 2)
        d.line([ux, uy, *diz], fill=koyu if uzak else g, width=_u(1.6, s))
        d.line([*diz, ax, y - 1], fill=koyu if uzak else g, width=_u(1.2, s))
        piksel(img, ax, y - 1, hex2(KOYU))
    d.ellipse([*p(-11, -9), *p(10, 1)] if yon > 0 else [*p(10, -9), *p(-11, 1)], fill=g)
    for hx in (-5, 4):
        d.ellipse([*p(hx - 3.5, -15), *p(hx + 3.5, -5)] if yon > 0 else [*p(hx + 3.5, -15), *p(hx - 3.5, -5)], fill=g)
    if yuk:
        d.rectangle([min(p(-2, -12)[0], p(1, -12)[0]), p(0, -12)[1], max(p(-2, -2)[0], p(1, -2)[0]), p(0, -2)[1]], fill=hex2(yuk),
                    outline=hex2(KOYU))
    d.polygon([p(8, -6), p(12, -9), p(14, -18), p(17, -18), p(18, -16), p(15, -15), p(13, -6)], fill=g)
    piksel(img, *p(15, -17), hex2(KOYU))
    d.line([p(-11, -6), p(-12, 0)], fill=koyu)


def tank(img, x, zemin, s=1.0, yon=1, faz=0.0, renk="#5a5e58"):
    """1941 tankı: palet tekerlekleri döner, alt palet zemine basar; kule ve namlu."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 34 * s)
    temas_golgesi(img, x, y, 38 * s, alfa=150)
    g = hex2(renk)
    koyu = hex2(_ac(renk, -0.3))
    # palet
    d.rounded_rectangle([x - int(17 * s), y - int(7 * s), x + int(17 * s), y - 1], radius=int(3 * s), fill=hex2("#2a2a2a"))
    for i in range(6):
        cx = x - int(13 * s) + int(i * 5.2 * s)
        cy = y - int(3.6 * s)
        d.ellipse([cx - int(2.2 * s), cy - int(2.2 * s), cx + int(2.2 * s), cy + int(2.2 * s)], fill=hex2("#4a4a48"))
        a = -faz * 2 * math.pi * yon
        piksel(img, cx + math.cos(a) * 1.4 * s, cy + math.sin(a) * 1.4 * s, hex2("#8a8a88"))
    for i in range(int(34 * s)):  # palet dişleri kayar
        if (i + int(faz * 6) * -yon) % 3 == 0:
            piksel(img, x - int(17 * s) + i, y - int(7 * s), hex2("#5a5a58"))
    # gövde
    d.polygon([(x - int(18 * s), y - int(7 * s)), (x - int(15 * s), y - int(12 * s)), (x + int(14 * s), y - int(12 * s)),
               (x + int(18 * s), y - int(7 * s))], fill=g)
    d.line([x - int(15 * s), y - int(12 * s), x + int(14 * s), y - int(12 * s)], fill=hex2(_ac(renk, 0.25)))
    # kule ve namlu
    d.rounded_rectangle([x - int(7 * s), y - int(18 * s), x + int(6 * s), y - int(12 * s)], radius=_u(1.5, s), fill=g)
    d.line([x + int(6 * s) * yon, y - int(15.5 * s), x + int(20 * s) * yon, y - int(15.5 * s)], fill=koyu, width=_u(1.2, s))
    # beyaz konturlu siyah haç (Balkenkreuz)
    cx, cy = x - int(9 * s) * yon, y - int(9.5 * s)
    d.rectangle([cx - _u(2, s), cy - _u(0.6, s), cx + _u(2, s), cy + _u(0.6, s)], fill=hex2("#f0f0f0"))
    d.rectangle([cx - _u(0.6, s), cy - _u(2, s), cx + _u(0.6, s), cy + _u(2, s)], fill=hex2("#f0f0f0"))
    d.rectangle([cx - _u(1.4, s), cy - _u(0.2, s), cx + _u(1.4, s), cy + _u(0.2, s)], fill=hex2("#101010"))
    d.rectangle([cx - _u(0.2, s), cy - _u(1.4, s), cx + _u(0.2, s), cy + _u(1.4, s)], fill=hex2("#101010"))


def gemi(img, x, su_y, s=1.0, yon=1, faz=0.0, govde="#5a3a22", yelken="#b8281e", hac=True):
    """Kadırga: gövde su çizgisine oturur (alt kısmı suya batık), dalgayla hafifçe iner kalkar."""
    d = ImageDraw.Draw(img)
    y = su_y + int(math.sin(faz * 2 * math.pi) * 0.8 * s)
    d.polygon([(x - int(16 * s), y - int(6 * s)), (x + int(16 * s), y - int(6 * s)), (x + int(12 * s), y + int(2 * s)),
               (x - int(13 * s), y + int(2 * s))], fill=hex2(govde))
    d.line([x - int(16 * s), y - int(6 * s), x + int(16 * s), y - int(6 * s)], fill=hex2(_ac(govde, 0.3)))
    for i in range(-12, 13, 3):  # kürekler
        kx = x + int(i * s)
        a = math.sin(faz * 2 * math.pi + i * 0.1) * 1.4 * s
        d.line([kx, y - int(3 * s), kx - int(2 * s) + a, y + int(3 * s)], fill=hex2("#3a2418"))
    d.line([x, y - int(6 * s), x, y - int(30 * s)], fill=hex2("#4a2a16"), width=_u(1, s))
    sis = math.sin(faz * 2 * math.pi) * 1.2 * s
    d.polygon([(x - int(10 * s), y - int(27 * s)), (x + int(10 * s), y - int(27 * s)), (x + int(11 * s) + sis, y - int(10 * s)),
               (x - int(9 * s) + sis, y - int(10 * s))], fill=hex2(yelken))
    if hac:  # Rodos Şövalyeleri (Hospitalier): kırmızı yelken üstüne beyaz haç
        d.rectangle([x - _u(1, s) + int(sis * 0.5), y - int(23 * s), x + _u(1, s) + int(sis * 0.5), y - int(13 * s)], fill=hex2("#f4f0e6"))
        d.rectangle([x - int(5 * s) + int(sis * 0.5), y - int(19 * s), x + int(5 * s) + int(sis * 0.5), y - int(17 * s)], fill=hex2("#f4f0e6"))


def mancinik(img, x, zemin, s=1.0, yon=1, faz=0.0, tas_x=None):
    """Karşı ağırlıklı mancınık: ahşap çatı zemine basar, kol faz ile atış yapar (0-0.3 atış, sonra geri)."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(14 * s), x + int(14 * s), "mancınık", tolerans=max(4, int(2 * s)))
    temas_golgesi(img, x, y, 30 * s)
    ah = hex2("#6a4428")
    d.rectangle([x - int(14 * s), y - int(2 * s), x + int(14 * s), y - 1], fill=ah)
    d.line([x - int(9 * s), y - 2, x, y - int(20 * s)], fill=ah, width=_u(1.6, s))
    d.line([x + int(9 * s), y - 2, x, y - int(20 * s)], fill=ah, width=_u(1.6, s))
    for tx in (-10, 10):  # tekerlekler
        d.ellipse([x + int(tx * s) - _u(2.5, s), y - _u(5, s), x + int(tx * s) + _u(2.5, s), y - 1], outline=hex2("#3a2418"), width=_u(1, s))
    if faz < 0.3:
        aci = -0.9 + faz / 0.3 * 2.6
    else:
        aci = 1.7 - (faz - 0.3) / 0.7 * 2.6
    px_, py_ = x, y - int(20 * s)
    uzun, kisa = 22 * s, 7 * s
    ux, uy = px_ + math.cos(math.pi + aci) * uzun * yon * -1, py_ + math.sin(math.pi + aci) * uzun
    kx, ky = px_ - math.cos(math.pi + aci) * kisa * yon * -1, py_ - math.sin(math.pi + aci) * kisa
    d.line([ux, uy, kx, ky], fill=hex2("#7a5232"), width=_u(1.4, s))
    d.rectangle([kx - _u(3, s), ky, kx + _u(3, s), ky + _u(5, s)], fill=hex2("#5a5a5a"), outline=hex2(KOYU))  # ağırlık kasası
    d.ellipse([px_ - _u(1.2, s), py_ - _u(1.2, s), px_ + _u(1.2, s), py_ + _u(1.2, s)], fill=hex2("#3a2418"))
    if faz >= 0.3 and faz < 0.95 and tas_x is not None:  # fırlayan taş: parabol
        t = (faz - 0.3) / 0.65
        tx = x + (tas_x - x) * t
        ty = uy - math.sin(t * math.pi) * 60 * s / 3 + t * 20 * s
        d.ellipse([tx - _u(1.5, s), ty - _u(1.5, s), tx + _u(1.5, s), ty + _u(1.5, s)], fill=hex2("#8a8478"), outline=hex2(KOYU))


# ---------------------------------------------------------------- yapılar


def otag(img, x, zemin, s=1.0, renk="#c8302a", serit="#e0b040", faz=0.0, acik=False):
    """Büyük hükümdar otağı: dikdörtgen ipek çadır, sivri tepe, dalgalanan sancak; tabanı düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(20 * s), x + int(20 * s), "otağ", tolerans=max(3, int(2 * s)))
    temas_golgesi(img, x, y, 44 * s)
    g = hex2(renk)
    d.rectangle([x - int(18 * s), y - int(18 * s), x + int(18 * s), y - 1], fill=g)
    for i in range(-18, 19, 6):
        d.line([x + int(i * s), y - int(18 * s), x + int(i * s), y - 1], fill=hex2(_ac(renk, -0.2)))
    d.polygon([(x - int(20 * s), y - int(18 * s)), (x, y - int(32 * s)), (x + int(20 * s), y - int(18 * s))], fill=hex2(_ac(renk, 0.1)))
    d.line([x - int(20 * s), y - int(18 * s), x + int(20 * s), y - int(18 * s)], fill=hex2(serit), width=_u(1.4, s))
    for i in range(-18, 19, 3):  # saçak
        piksel(img, x + int(i * s), y - int(17 * s), hex2(serit))
        piksel(img, x + int(i * s), y - int(16 * s), hex2(serit))
    if acik:
        d.polygon([(x - int(6 * s), y - 1), (x - int(5 * s), y - int(14 * s)), (x + int(5 * s), y - int(14 * s)), (x + int(6 * s), y - 1)],
                  fill=hex2("#2a1410"))
        d.line([x - int(6 * s), y - 1, x - int(9 * s), y - int(14 * s)], fill=hex2(_ac(renk, 0.25)), width=_u(1, s))
        d.line([x + int(6 * s), y - 1, x + int(9 * s), y - int(14 * s)], fill=hex2(_ac(renk, 0.25)), width=_u(1, s))
    tepe = y - int(32 * s)
    d.line([x, tepe, x, tepe - int(10 * s)], fill=hex2("#5a3a22"), width=_u(0.8, s))
    for i in range(int(8 * s)):
        dal = math.sin(faz * 2 * math.pi - i / (2 * s)) * 1.2 * s * i / (8 * s)
        for k in range(int(3 * s)):
            piksel(img, x + 1 + i, tepe - int(10 * s) + k + dal, hex2(serit))


def koy_evleri(img, x0, x1, zemin, s=1.0, tohum=1, kerpic="#c8a878"):
    """Kerpiç köy evleri: düz damlı, küçük kapı ve pencere; damda kuruyan ot. Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    rnd = random.Random(tohum)
    x = x0
    while x < x1 - 14 * s:
        w = int(rnd.uniform(14, 22) * s)
        h = int(rnd.uniform(10, 15) * s)
        y = duz_zemin(zemin, x, x + w, "köy evi", tolerans=max(3, int(2 * s)))
        renk = _ac(kerpic, rnd.uniform(-0.12, 0.06))
        d.rectangle([x, y - h, x + w, y - 1], fill=hex2(renk))
        d.rectangle([x - 1, y - h - _u(1.4, s), x + w + 1, y - h], fill=hex2(_ac(renk, -0.2)))
        d.line([x - 1, y - h - _u(1.4, s), x + w + 1, y - h - _u(1.4, s)], fill=hex2(_ac(renk, 0.2)))
        d.rectangle([x + w // 3, y - int(7 * s), x + w // 3 + int(3 * s), y - 1], fill=hex2("#4a2a1a"))
        d.rectangle([x + 2 * w // 3, y - int(9 * s), x + 2 * w // 3 + int(2 * s), y - int(7 * s)], fill=hex2("#2a1a12"))
        temas_golgesi(img, x + w // 2, y, w + 4, alfa=80)
        x += w + int(rnd.uniform(3, 8) * s)


def anadolu_kalesi(img, x0, x1, zemin, s=1.0, tas="#9a948a", golge="#6a665e", kapi=True):
    """Taş sur: kesme taş örgü, dikdörtgen mazgallı kuleler, kemerli kapı. Düz zemine kurulur.
    Dönen değer: sur üstündeki (mazgal) y'si."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0 - int(6 * s), x1 + int(6 * s), "kale", tolerans=max(3, int(3 * s)))
    h = int(30 * s)
    d.rectangle([x0, y - h, x1, y - 1], fill=hex2(tas))
    rnd = random.Random(x0)
    for by in range(y - h + _u(3, s), y - 1, _u(3, s)):  # taş sıraları
        d.line([x0, by, x1, by], fill=hex2(_ac(tas, -0.12)))
        kay = rnd.randint(0, 5)
        for bx in range(x0 + kay, x1, _u(6, s)):
            piksel(img, bx, by - 1, hex2(_ac(tas, -0.18)))
    for mx in range(x0, x1, _u(5, s)):
        d.rectangle([mx, y - h - _u(3, s), mx + _u(2.6, s), y - h], fill=hex2(tas))
    for kx in [x0, x0 + (x1 - x0) // 3, x0 + 2 * (x1 - x0) // 3, x1]:
        kh = h + int(12 * s)
        d.rectangle([kx - int(7 * s), y - kh, kx + int(7 * s), y - 1], fill=hex2(_ac(tas, 0.04)))
        d.rectangle([kx + int(2 * s), y - kh, kx + int(7 * s), y - 1], fill=hex2(golge))
        for m in range(-7, 7, 4):
            d.rectangle([kx + int(m * s), y - kh - _u(3, s), kx + int((m + 2) * s), y - kh], fill=hex2(_ac(tas, 0.04)))
        d.rectangle([kx - _u(1, s), y - kh + int(8 * s), kx, y - kh + int(12 * s)], fill=hex2("#1a1612"))  # mazgal deliği
    if kapi:
        gx = (x0 + x1) // 2
        d.chord([gx - int(6 * s), y - int(22 * s), gx + int(6 * s), y - int(10 * s)], 180, 360, fill=hex2("#2a1e16"))
        d.rectangle([gx - int(6 * s), y - int(16 * s), gx + int(6 * s), y - 1], fill=hex2("#2a1e16"))
        for k in range(-5, 6, 2):
            d.line([gx + int(k * s), y - int(15 * s), gx + int(k * s), y - 1], fill=hex2("#4a3222"))
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0 + 16, alfa=100)
    return y - h


def kafa_kulesi(img, x, zemin, s=1.0, renk="#e8e0cc"):
    """Kafatası kulesi (İsfahan, Bağdat): koni biçimli harç ve kafataslarından kule, tabanı zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 14 * s)
    temas_golgesi(img, x, y, 18 * s)
    h = int(24 * s)
    d.polygon([(x - int(7 * s), y - 1), (x - int(3 * s), y - h), (x + int(3 * s), y - h), (x + int(7 * s), y - 1)], fill=hex2("#8a7a62"))
    rnd = random.Random(int(x * 7))
    for row in range(int(h / (2.4 * s))):
        ry = y - 1 - int(row * 2.4 * s) - _u(1, s)
        gen = 7 - 4 * row * 2.4 * s / h
        for cx in range(int(-gen * s) + 1, int(gen * s), _u(2.4, s)):
            kx = x + cx
            d.ellipse([kx - _u(1, s), ry - _u(1, s), kx + _u(1, s), ry + _u(1, s)], fill=hex2(_ac(renk, rnd.uniform(-0.15, 0.05))))
            piksel(img, kx - _u(0.4, s), ry, hex2("#2a1a12"))
            piksel(img, kx + _u(0.4, s), ry, hex2("#2a1a12"))


def gur_i_emir(img, x, zemin, s=1.0, mavi="#2a7ab8", tugla="#c8a878"):
    """Gür-i Emir türbesi: yüksek kasnak üstünde dilimli mavi kubbe, kemerli taç kapı (pištak), iki minare.
    Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(30 * s), x + int(30 * s), "Gür-i Emir", tolerans=max(3, int(3 * s)))
    temas_golgesi(img, x, y, 64 * s)
    d.rectangle([x - int(18 * s), y - int(26 * s), x + int(18 * s), y - 1], fill=hex2(tugla))  # gövde
    for by in range(y - int(26 * s), y, _u(4, s)):
        d.line([x - int(18 * s), by, x + int(18 * s), by], fill=hex2(_ac(tugla, -0.08)))
    # kasnak: mavi yazı kuşaklı silindir
    d.rectangle([x - int(12 * s), y - int(46 * s), x + int(12 * s), y - int(26 * s)], fill=hex2(_ac(tugla, 0.05)))
    d.rectangle([x - int(12 * s), y - int(42 * s), x + int(12 * s), y - int(36 * s)], fill=hex2(mavi))
    for i in range(-11, 12, 2):
        piksel(img, x + int(i * s), y - int(39 * s), hex2("#f4ecd8"))
    # dilimli kubbe: dikey koyu/açık dilimler, sağda gölge, solda ışık
    kub = [x - int(14 * s), y - int(70 * s), x + int(14 * s), y - int(42 * s)]
    cx_, cy_, rx, ry = x, (kub[1] + kub[3]) / 2, (kub[2] - kub[0]) / 2, (kub[3] - kub[1]) / 2
    for py_ in range(kub[1], kub[3] + 1):
        for px_ in range(kub[0], kub[2] + 1):
            u = (px_ - cx_) / rx
            if u * u + ((py_ - cy_) / ry) ** 2 <= 1:
                dilim = int((math.asin(max(-1, min(1, u))) + 1.6) * 5) % 2
                renk = _ac(mavi, -0.18) if dilim else mavi
                if u > 0.45:
                    renk = _ac(renk, -0.2)
                elif u < -0.5 and py_ < cy_:
                    renk = _ac(renk, 0.2)
                piksel(img, px_, py_, hex2(renk))
    # taç kapı
    d.rectangle([x - int(9 * s), y - int(34 * s), x + int(9 * s), y - 1], fill=hex2(_ac(tugla, 0.08)))
    d.rectangle([x - int(9 * s), y - int(34 * s), x + int(9 * s), y - int(31 * s)], fill=hex2(mavi))
    d.chord([x - int(5 * s), y - int(26 * s), x + int(5 * s), y - int(14 * s)], 180, 360, fill=hex2("#1a3a5a"))
    d.rectangle([x - int(5 * s), y - int(20 * s), x + int(5 * s), y - 1], fill=hex2("#1a3a5a"))
    # minareler
    for mx in (-26, 26):
        cx = x + int(mx * s)
        d.rectangle([cx - int(2.5 * s), y - int(48 * s), cx + int(2.5 * s), y - 1], fill=hex2(tugla))
        for k in range(4):
            d.line([cx - int(2.5 * s), y - int((10 + k * 10) * s), cx + int(2.5 * s), y - int((10 + k * 10) * s)], fill=hex2(mavi),
                   width=_u(1.4, s))
        d.rectangle([cx - int(3.5 * s), y - int(50 * s), cx + int(3.5 * s), y - int(48 * s)], fill=hex2(_ac(tugla, -0.1)))


def bibi_hanim(img, x, zemin, s=1.0, mavi="#2a8ac8", tugla="#c8a878", iskele=True, catlak=0.0):
    """Bibi Hanım Camii'nin dev taç kapısı ve kubbesi; iskele kurulu. catlak: 0-1 kubbede çatlak."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(36 * s), x + int(36 * s), "Bibi Hanım", tolerans=max(3, int(3 * s)))
    temas_golgesi(img, x, y, 76 * s)
    d.ellipse([x - int(20 * s) + int(18 * s), y - int(78 * s), x + int(20 * s) + int(18 * s), y - int(44 * s)], fill=hex2(mavi))  # kubbe arkada
    d.rectangle([x - int(2 * s) + int(18 * s), y - int(50 * s), x + int(38 * s), y - 1], fill=hex2(tugla))
    d.rectangle([x - int(22 * s), y - int(74 * s), x + int(10 * s), y - 1], fill=hex2(_ac(tugla, 0.06)))  # pištak
    d.rectangle([x - int(22 * s), y - int(74 * s), x + int(10 * s), y - int(70 * s)], fill=hex2(mavi))
    for k in range(4):
        d.line([x - int(22 * s), y - int((60 - k * 12) * s), x + int(10 * s), y - int((60 - k * 12) * s)], fill=hex2(_ac(mavi, 0.1)))
    d.chord([x - int(14 * s), y - int(60 * s), x + int(2 * s), y - int(30 * s)], 180, 360, fill=hex2("#1a3a5a"))
    d.rectangle([x - int(14 * s), y - int(45 * s), x + int(2 * s), y - 1], fill=hex2("#1a3a5a"))
    for mx in (-25, 13):  # köşe kuleleri
        cx = x + int(mx * s)
        d.rectangle([cx - int(3 * s), y - int(80 * s), cx + int(3 * s), y - 1], fill=hex2(tugla))
        for k in range(5):
            d.line([cx - int(3 * s), y - int((12 + k * 13) * s), cx + int(3 * s), y - int((12 + k * 13) * s)], fill=hex2(mavi), width=_u(1.2, s))
    if catlak > 0:
        cx, cy = x + int(18 * s), y - int(74 * s)
        for i in range(int(14 * s * catlak)):
            piksel(img, cx + int(math.sin(i * 0.9) * 2 * s), cy + i, hex2("#1a2a3a"))
    if iskele:
        ah = hex2("#8a6a3a")
        for ix in range(-26, 16, 6):
            d.line([x + int(ix * s), y - 1, x + int(ix * s), y - int(56 * s)], fill=ah)
        for iy in range(8, 57, 12):
            d.line([x - int(26 * s), y - int(iy * s), x + int(14 * s), y - int(iy * s)], fill=ah)


def heykel(img, x, zemin, s=1.0, tunc="#5a6a4a"):
    """Taşkent'teki atlı Emir Timur heykeli: granit kaide düz zemine oturur, üstünde tunç atlı."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(16 * s), x + int(16 * s), "heykel", tolerans=max(3, int(2 * s)))
    temas_golgesi(img, x, y, 36 * s)
    d.rectangle([x - int(16 * s), y - int(6 * s), x + int(16 * s), y - 1], fill=hex2("#5a5458"))
    d.rectangle([x - int(12 * s), y - int(26 * s), x + int(12 * s), y - int(6 * s)], fill=hex2("#7a7478"))
    d.line([x - int(12 * s), y - int(26 * s), x + int(12 * s), y - int(26 * s)], fill=hex2("#9a949a"))
    d.rectangle([x - int(8 * s), y - int(18 * s), x + int(8 * s), y - int(14 * s)], fill=hex2("#c8a040"))  # yazı levhası
    zem = [y - int(26 * s)] * img.width
    atli(img, x, zem, s * 0.9, 1, 0.0, tunc, _ac(tunc, -0.3), tunc, "sorguc", _ac(tunc, -0.2), None, None, dur=True)
    # ön ayakları kalkık at hissi için yükseltilmiş kol: elde kılıç değil, açık el (adalet)


def hendek(img, x0, x1, zemin, derin=14, renk="#2a1a10"):
    """Zemine kazılmış çukur: kenarları toprak yığını. Zemin listesini yerinde değiştirmez."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, (x0 + x1) / 2, x1 - x0)
    d.polygon([(x0, y), (x0 + 4, y + derin), (x1 - 4, y + derin), (x1, y)], fill=hex2(renk))
    d.polygon([(x0 + 2, y), (x0 + 5, y + derin - 2), (x0 + 10, y + derin - 2), (x0 + 6, y)], fill=hex2(_ac(renk, 0.15)))
    for kx, ky in ((x0 - 10, y), (x1 + 10, y)):
        d.chord([kx - 12, ky - 7, kx + 12, ky + 7], 180, 360, fill=hex2("#5a3a22"))
