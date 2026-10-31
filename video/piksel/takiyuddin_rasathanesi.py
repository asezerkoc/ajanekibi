"""Aynı Gökyüzü, İki Gözlemevi: Takiyüddin'in İstanbul Rasathanesi (1577-1580). Piksel Tarih (@pikseltarihim),
sahneler 410-449. Grafikerin tarifi (teslimler/gece/ara/takiyuddin-rasathanesi/5-grafik.md); metin ve kartlar
4-kalite-metin.md'den. Yön dili: sağ = İstanbul / rasathane, sol = Hven / Avrupa.
Kullanım: python3 -I video/piksel/takiyuddin_rasathanesi.py [sahne numaraları]

Yeni figürler (bu dosyada; ciz.py'ye eklenmedi, yalnızca piksel()/hex2()/ImageDraw ve mevcut figürlerle):
  teras, rasathane, ceyrek_daire, armilla, top_, kuyruklu_yildiz, uraniborg, osmanli_camii, ulugbey_rasathanesi,
  dokumhane, masa_saati, minyatur_kitap, bos_sedir. Hepsi zemine oturur (duz_zemin / zemin_y); gökteki tek nesneler
  kuyruklu yıldız, ay ve yıldızlardır (gökyüzü katmanına çizilir).
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import ImageDraw  # noqa: E402

from ciz import KOYU, _ac, _esik, agac, duman, duz_zemin, figur, gunes, hex2, orta_asya_sehri, piksel, sehir, taslar, temas_golgesi, yeni, zemin_y  # noqa: E402
from sahneler import duz, gokyuzu, kaydet, on, orta, sprite, uzak  # noqa: E402
from timur_figur import anadolu_kalesi, atli, gemi, gur_i_emir, kisi, oturan, sedir  # noqa: E402
from timur import ic_mekan, kandil, mumluk, su_ve_kiyi, kalabalik  # noqa: E402
from kalender import taht, rahle, kitaplar  # noqa: E402

KARE = 24      # sprite kare sayısı (SKILL.md)
PAY = 135      # orta/ön plan yan payı (SKILL.md)
SIN = lambda f, k=1: math.sin(f * 2 * math.pi * k)  # noqa: E731


def _u(v, s):
    return max(1, int(round(v * s)))


# ==========================================================================
# YENİ FİGÜRLER
# ==========================================================================
TAS = "#c8b89a"          # Tophane kesme taşı
KURSUN = "#8a96a0"       # kurşun kubbe
PIRINC = "#d8a840"       # alet pirinci


def teras(img, x0, x1, zemin, h, tas="#a89878"):
    """Yeni figür: yamaç üstündeki düz set (teras). Kesme taş istinat duvarı düz zemine oturur; üstü dümdüz bir
    platformdur ve yapılar onun üstüne kurulur. Dönen değer: platformun y'si (yeni zemin)."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "teras", tolerans=3)
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0 + 4)
    ust = y - h
    d.rectangle([x0, ust, x1, y - 1], fill=hex2(tas))
    koyu = hex2(_ac(tas, -0.28))
    for k, yy in enumerate(range(ust + 4, y - 1, 4)):                 # taş sıraları (şaşırtmalı derz)
        d.line([x0, yy, x1, yy], fill=koyu)
        for xx in range(x0 + (k % 2) * 5, x1, 10):
            d.line([xx, yy - 3, xx, yy], fill=koyu)
    d.rectangle([x0 - 1, ust - 2, x1 + 1, ust], fill=hex2(_ac(tas, 0.25)))   # platformun ışıklı üst kenarı
    return ust


def rasathane(img, x, zemin, s=1.0, yikik=0.0, isik=False, tas=TAS, kubbe=KURSUN):
    """Yeni figür: İstanbul Rasathanesi (mimarisi bilinmiyor; kaynaklarla çelişmeyen sade Osmanlı taş yapısı).
    Solda iki katlı taş blok ve kurşun kubbe, sağda düz damlı gözlem kulesi (dam korkuluklu). Yalnızca düz zemine
    kurulur. yikik 0-1: kubbe düşer, duvar ve kule tepesi kırılır, dibinde moloz yığılır (moloz da zemine oturur).
    isik=True: pencerelerde kandil ışığı. Dönen değer: (kule_tepe_x, kule_tepe_y, moloz noktaları)."""
    k = yeni(img.width, img.height)
    d = ImageDraw.Draw(k)
    y = duz_zemin(zemin, x - int(24 * s), x + int(22 * s), "rasathane", tolerans=max(3, int(s)))
    taskoyu, tasacik = hex2(_ac(tas, -0.25)), hex2(_ac(tas, 0.2))
    pen = hex2("#f8c860") if isik else hex2("#2a2420")
    # ana blok
    bx0, bx1, by = x - int(22 * s), x + int(6 * s), y - int(20 * s)
    d.rectangle([bx0, by, bx1, y - 1], fill=hex2(tas))
    for yy in range(by + _u(3, s), y - 1, _u(3, s)):
        d.line([bx0, yy, bx1, yy], fill=taskoyu)
    d.rectangle([bx0 - _u(1, s), by - _u(1, s), bx1 + _u(1, s), by], fill=tasacik)          # saçak
    for kat, py in ((0, y - int(9 * s)), (1, y - int(17 * s))):
        for px in (bx0 + int(4 * s), bx0 + int(11 * s), bx0 + int(18 * s)):
            if kat == 0 and px == bx0 + int(11 * s):
                continue
            d.rectangle([px - _u(1.2, s), py, px + _u(1.2, s), py + int(4 * s)], fill=pen)
            d.chord([px - _u(1.2, s), py - _u(1.2, s), px + _u(1.2, s), py + _u(1.2, s)], 180, 360, fill=pen)
    kx = bx0 + int(11 * s)                                                                    # kemerli kapı
    d.rectangle([kx - _u(2, s), y - int(6 * s), kx + _u(2, s), y - 1], fill=hex2("#3a2a1e"))
    d.chord([kx - _u(2, s), y - int(8 * s), kx + _u(2, s), y - int(4 * s)], 180, 360, fill=hex2("#3a2a1e"))
    # kubbe (kasnak + kurşun kubbe + alem)
    cx = bx0 + int(11 * s)
    d.rectangle([cx - int(7 * s), by - int(3 * s), cx + int(7 * s), by], fill=hex2(tas), outline=taskoyu)
    d.chord([cx - int(7 * s), by - int(10 * s), cx + int(7 * s), by - int(3 * s) + int(3 * s)], 180, 360, fill=hex2(kubbe))
    for r in (-4, 0, 4):                                                                      # kubbe dilimleri
        d.line([cx + int(r * s), by - int(3 * s), cx + int(r * 0.6 * s), by - int(9 * s)], fill=hex2(_ac(kubbe, -0.18)))
    d.line([cx, by - int(10 * s), cx, by - int(12.5 * s)], fill=hex2("#e0b040"), width=_u(0.5, s))
    # gözlem kulesi
    tx0, tx1, ty = x + int(6 * s), x + int(20 * s), y - int(32 * s)
    d.rectangle([tx0, ty, tx1, y - 1], fill=hex2(_ac(tas, -0.05)))
    for yy in range(ty + _u(3, s), y - 1, _u(3, s)):
        d.line([tx0, yy, tx1, yy], fill=taskoyu)
    for kx_ in range(tx0, tx1 + 1, _u(3, s)):                                                  # dam korkuluğu
        d.rectangle([kx_, ty - _u(2, s), min(tx1, kx_ + _u(1.5, s)), ty], fill=hex2(tas))
    d.rectangle([tx0 - _u(1, s), ty, tx1 + _u(1, s), ty + _u(1, s)], fill=tasacik)
    for py in (y - int(14 * s), y - int(24 * s)):
        mx = (tx0 + tx1) // 2
        d.rectangle([mx - _u(1.2, s), py, mx + _u(1.2, s), py + int(4 * s)], fill=pen)
        d.chord([mx - _u(1.2, s), py - _u(1.2, s), mx + _u(1.2, s), py + _u(1.2, s)], 180, 360, fill=pen)
    tepe = ((tx0 + tx1) // 2, ty - _u(2, s))
    molozlar = []
    if yikik > 0:
        rnd = random.Random(int(x * 7 + y))
        px = k.load()
        # kırık üst profil: kubbe ve korkuluk gider, duvar dişli kırılır
        kesim_ana = by + int(yikik * 14 * s)
        kesim_kule = ty + int(yikik * 26 * s)
        sol, sag = bx0 - _u(2, s), tx1 + _u(2, s)
        dis = 0
        for xx in range(sol, sag + 1):
            if rnd.random() < 0.35:
                dis = rnd.randint(0, max(1, int(4 * s)))
            kes = (kesim_kule if xx >= tx0 else kesim_ana) + dis
            for yy in range(0, min(kes, img.height)):
                if 0 <= xx < img.width:
                    px[xx, yy] = (0, 0, 0, 0)
        tepe = ((tx0 + tx1) // 2, kesim_kule)
        # duvarda gedikler (koyu delikler)
        for _ in range(int(3 + 5 * yikik)):
            gx = rnd.randint(bx0 + int(2 * s), tx1 - int(2 * s))
            gy = rnd.randint(min(y - int(4 * s), kesim_ana + int(2 * s)), y - int(4 * s))
            gr = _u(rnd.uniform(1.2, 2.4), s)
            d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=hex2("#2a2420"))
        # moloz yığınları: zemine oturur, üçgen tümsek + taş blokları
        for mx, mw in ((bx0 - int(2 * s), 10), (x + int(2 * s), 12), (tx1 + int(3 * s), 9)):
            mw = int(mw * s * (0.5 + yikik))
            mh = int(mw * 0.45)
            d.polygon([(mx - mw // 2, y - 1), (mx, y - 1 - mh), (mx + mw // 2, y - 1)], fill=hex2(_ac(tas, -0.15)))
            for _ in range(int(6 * (0.5 + yikik))):
                ox = rnd.randint(-mw // 3, mw // 3)
                oy = y - 2 - rnd.randint(0, max(1, mh - abs(ox) - 1))
                b = _u(rnd.uniform(0.8, 1.6), s)
                d.rectangle([mx + ox - b, oy - b, mx + ox + b, min(oy + b, y - 1)], fill=hex2(rnd.choice([tas, _ac(tas, -0.3), _ac(tas, 0.15)])))
            molozlar.append((mx, y - mh // 2))
    img.alpha_composite(k)
    temas_golgesi(img, x - int(2 * s), y, 46 * s)
    return tepe[0], tepe[1], molozlar


def ceyrek_daire(img, x, zemin, s=1.0, yon=1, maden=PIRINC, tas=TAS, aci=0.6):
    """Yeni figür: duvar çeyrek dairesi (libne). Taş ayak (duvar) zemine oturur; pirinç çeyrek yay duvarın yüzüne
    tutturulmuştur (yayın merkezi duvarın tepesinde, alt ucu duvar dibine yakın). aci 0-1: nişangâh cetvelinin açısı."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(3 * s), x + int(3 * s), "çeyrek daire", tolerans=max(3, int(s)))
    temas_golgesi(img, x + int(8 * s) * yon, y, 26 * s)
    # taş ayak
    d.rectangle([x - int(2.5 * s), y - int(27 * s), x + int(2.5 * s), y - 1], fill=hex2(tas))
    for yy in range(y - int(27 * s) + _u(3, s), y - 1, _u(3, s)):
        d.line([x - int(2.5 * s), yy, x + int(2.5 * s), yy], fill=hex2(_ac(tas, -0.25)))
    d.rectangle([x - int(3.2 * s), y - int(2 * s), x + int(3.2 * s), y - 1], fill=hex2(_ac(tas, -0.15)))   # kaide
    # yay: merkez duvarın tepesi, yarıçap 22s, yon tarafına dönük çeyrek
    cx, cy, r = x, y - int(26 * s), int(22 * s)
    m, mk = hex2(maden), hex2(_ac(maden, -0.35))
    kutu = [cx - r, cy - r, cx + r, cy + r]
    bas, son = (0, 90) if yon > 0 else (90, 180)
    d.arc(kutu, bas, son, fill=m, width=_u(1.6, s))
    for a in range(bas, son + 1, 6):                                                      # derece çizgileri
        rad = math.radians(a)
        d.line([cx + math.cos(rad) * (r - _u(1.6, s)), cy + math.sin(rad) * (r - _u(1.6, s)),
                cx + math.cos(rad) * (r - _u(3, s)), cy + math.sin(rad) * (r - _u(3, s))], fill=mk)
    d.line([cx, cy, cx + r * yon, cy], fill=m, width=_u(1, s))                             # yatay kol
    d.line([cx, cy, cx, cy + r], fill=m, width=_u(1, s))                                   # dikey kol (duvar boyunca)
    rad = math.radians(bas + (son - bas) * (aci if yon > 0 else 1 - aci))
    d.line([cx, cy, cx + math.cos(rad) * r, cy + math.sin(rad) * r], fill=hex2("#5a3a1a"), width=_u(0.8, s))  # nişangâh
    d.ellipse([cx - _u(1.2, s), cy - _u(1.2, s), cx + _u(1.2, s), cy + _u(1.2, s)], fill=m)
    # yayın alt ucunu yere bağlayan ayak (yay havada durmaz)
    ax = cx + int(r * 0.98) * yon
    d.line([ax, cy + int(r * 0.2), ax, y - 1], fill=hex2("#5a3a1e"), width=_u(1, s))


def armilla(img, x, zemin, s=1.0, faz=0.0, maden=PIRINC):
    """Yeni figür: halkalı küre (zatü'l-halak). Üç ayaklı kaide zemine basar, ortadaki sütun küreyi taşır; meridyen ve
    ufuk halkaları sabit, iç halka faz ile yavaşça döner."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 12 * s)
    temas_golgesi(img, x, y, 14 * s)
    ah = hex2("#5a3a1e")
    for dx in (-6, 0, 6):                                                                     # ayaklar
        d.line([x, y - int(7 * s), x + int(dx * s), y - 1], fill=ah, width=_u(0.9, s))
    d.line([x, y - int(7 * s), x, y - int(12 * s)], fill=ah, width=_u(1.2, s))               # sütun
    cy, r = y - int(21 * s), int(9 * s)
    m, mk = hex2(maden), hex2(_ac(maden, -0.3))
    d.ellipse([x - r, cy - r, x + r, cy + r], outline=m, width=_u(1.1, s))                    # meridyen
    d.ellipse([x - r - _u(1, s), cy - _u(2, s), x + r + _u(1, s), cy + _u(2, s)], outline=m, width=_u(0.9, s))  # ufuk
    gen = max(1, int(abs(math.cos(faz * 2 * math.pi)) * r))                                  # dönen halka
    d.ellipse([x - gen, cy - r + _u(1, s), x + gen, cy + r - _u(1, s)], outline=mk, width=_u(0.8, s))
    eg = int(r * 0.45)                                                                        # ekliptik (eğik)
    d.line([x - r, cy + eg, x + r, cy - eg], fill=mk, width=_u(0.7, s))
    d.ellipse([x - _u(1.3, s), cy - _u(1.3, s), x + _u(1.3, s), cy + _u(1.3, s)], fill=hex2("#e8d8a0"))
    d.line([x, cy + r, x, y - int(12 * s)], fill=m, width=_u(1, s))                           # küreyi sütuna bağlar


def top_(img, x, zemin, s=1.0, yon=1, ates=0.0, egim=0.18):
    """Yeni figür: tunç top, iki tekerlekli ahşap kundak. Tekerlekler ve kundağın kuyruğu zemine basar; namlu
    egim kadar yukarı bakar. ates 0-1: namlu ağzında alev (ates>0.6) ve ağızdan çıkan duman (dumanı sahne çizer)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 18 * s)
    temas_golgesi(img, x, y, 20 * s)
    ah, ahk = hex2("#6a4428"), hex2("#4a2e1a")
    tx = x - int(1 * s) * yon                                                                 # teker merkezi
    tr = int(3.4 * s)
    # kundak: kuyruğu yerde, öne doğru yükselir
    d.polygon([(x - int(10 * s) * yon, y - 1), (x - int(9 * s) * yon, y - int(2 * s)), (tx + int(3 * s) * yon, y - int(5.5 * s)),
               (tx + int(3 * s) * yon, y - int(3.5 * s))], fill=ah)
    # namlu
    nx0, ny0 = tx - int(5 * s) * yon, y - int(5 * s)
    boy = 15 * s
    nx1, ny1 = nx0 + int(boy * math.cos(egim)) * yon, ny0 - int(boy * math.sin(egim))
    d.line([nx0, ny0, nx1, ny1], fill=hex2("#9a7a3a"), width=_u(2.6, s))
    d.line([nx0, ny0 - _u(1, s), nx1, ny1 - _u(1, s)], fill=hex2("#c8a050"), width=_u(0.7, s))
    d.ellipse([nx0 - _u(1.6, s), ny0 - _u(1.6, s), nx0 + _u(1.6, s), ny0 + _u(1.6, s)], fill=hex2("#8a6a2a"))   # dip topuzu
    d.ellipse([nx1 - _u(1.5, s), ny1 - _u(1.5, s), nx1 + _u(1.5, s), ny1 + _u(1.5, s)], fill=hex2("#8a6a2a"))   # ağız
    # tekerlek (ön planda): altı zemine değer
    d.ellipse([tx - tr, y - 2 * tr, tx + tr, y - 1], outline=ahk, width=_u(1, s))
    for a in range(0, 180, 45):
        rad = math.radians(a)
        d.line([tx - math.cos(rad) * tr, y - tr - math.sin(rad) * tr, tx + math.cos(rad) * tr, y - tr + math.sin(rad) * tr], fill=ah)
    d.ellipse([tx - _u(0.8, s), y - tr - _u(0.8, s), tx + _u(0.8, s), y - tr + _u(0.8, s)], fill=ahk)
    if ates > 0.6:
        for r_, renk in ((3.2, "#f8a030"), (2.0, "#ffd060"), (1.0, "#fff8d0")):
            rr = r_ * s * (ates - 0.4)
            d.ellipse([nx1 + int(2 * s) * yon - rr, ny1 - rr, nx1 + int(2 * s) * yon + rr, ny1 + rr], fill=hex2(renk))
    return nx1 + int(2 * s) * yon, ny1


def kuyruklu_yildiz(img, x, y, boy, aci=-2.5, renk="#e8f4ff", kuyruk="#a8d0f0", tohum=1):
    """Yeni figür (gökyüzü): 1577 kuyruklu yıldızı. Parlak çekirdek ve hale; kuyruk aci yönünde (radyan) uzar,
    genişler ve titreşimle söner. Gökyüzü katmanına çizilir (gökteki bir cisim olduğu için zemine bağlanmaz)."""
    rnd = random.Random(tohum)
    dx, dy = math.cos(aci), math.sin(aci)
    nx, ny = -dy, dx
    for i in range(int(boy)):
        t = i / boy
        gen = 1.2 + t * boy * 0.16
        for j in range(-int(gen) - 1, int(gen) + 2):
            yog = (1 - t) * (1 - abs(j) / (gen + 1.5))
            px_, py_ = x + dx * i + nx * j, y + dy * i + ny * j
            if yog > 0 and yog * 1.25 > _esik(int(px_) % img.width, int(py_) % img.height):
                renk_ = renk if (abs(j) < 1.2 and t < 0.35) else kuyruk
                piksel(img, int(px_) % img.width, int(py_), hex2(renk_, int(110 + 145 * yog)))
        if rnd.random() < 0.25 and t > 0.15:                                                  # kuyruk lifleri
            j = rnd.uniform(-gen, gen)
            piksel(img, int(x + dx * i + nx * j) % img.width, int(y + dy * i + ny * j), hex2(kuyruk, 160))
    gunes(img, x, y, 2, ["#ffffff", renk])


def uraniborg(img, x, zemin, s=1.0, yikik=0.0, isik=False):
    """Yeni figür: Hven'deki Uraniborg (Tycho Brahe). Kırmızı tuğla simetrik köşk, ortada bakır kubbe ve fener,
    iki yanda kubbeli yuvarlak gözlem kuleleri. Düz zemine kurulur. yikik 0-1: kubbeler düşer, duvarlar kırılır,
    dibinde tuğla molozu."""
    k = yeni(img.width, img.height)
    d = ImageDraw.Draw(k)
    y = duz_zemin(zemin, x - int(24 * s), x + int(24 * s), "Uraniborg", tolerans=max(3, int(s)))
    tug, tugk, tas = hex2("#a8503a"), hex2("#7a3426"), hex2("#e8dcc0")
    bakir, bakirk = hex2("#5aa08a"), hex2("#3a7a6a")
    pen = hex2("#f8c860") if isik else hex2("#2a2024")
    # orta köşk
    d.rectangle([x - int(12 * s), y - int(22 * s), x + int(12 * s), y - 1], fill=tug)
    for yy in range(y - int(22 * s) + _u(3, s), y - 1, _u(3, s)):
        d.line([x - int(12 * s), yy, x + int(12 * s), yy], fill=tugk)
    d.rectangle([x - int(13 * s), y - int(23 * s), x + int(13 * s), y - int(22 * s)], fill=tas)
    d.polygon([(x - int(13 * s), y - int(23 * s)), (x, y - int(29 * s)), (x + int(13 * s), y - int(23 * s))], fill=tugk)  # alınlık
    d.chord([x - int(6 * s), y - int(36 * s), x + int(6 * s), y - int(24 * s)], 180, 360, fill=bakir)         # kubbe
    d.rectangle([x - _u(1.5, s), y - int(38 * s), x + _u(1.5, s), y - int(35 * s)], fill=bakirk)               # fener
    d.line([x, y - int(38 * s), x, y - int(41 * s)], fill=hex2("#e0b040"))
    for px in (-8, -3, 3, 8):
        for py in (-18, -10):
            d.rectangle([x + int(px * s) - _u(1, s), y + int(py * s), x + int(px * s) + _u(1, s), y + int((py + 4) * s)], fill=pen)
    d.rectangle([x - _u(2, s), y - int(6 * s), x + _u(2, s), y - 1], fill=hex2("#3a2218"))                   # kapı
    # yan kuleler
    for yon in (-1, 1):
        kx = x + int(17 * s) * yon
        d.rectangle([kx - int(5 * s), y - int(18 * s), kx + int(5 * s), y - 1], fill=tug)
        for yy in range(y - int(18 * s) + _u(3, s), y - 1, _u(3, s)):
            d.line([kx - int(5 * s), yy, kx + int(5 * s), yy], fill=tugk)
        d.rectangle([kx - int(5.5 * s), y - int(19 * s), kx + int(5.5 * s), y - int(18 * s)], fill=tas)
        d.chord([kx - int(5 * s), y - int(26 * s), kx + int(5 * s), y - int(12 * s)], 180, 360, fill=bakir)
        d.line([kx, y - int(26 * s), kx, y - int(28 * s)], fill=hex2("#e0b040"))
        d.rectangle([kx - _u(1, s), y - int(13 * s), kx + _u(1, s), y - int(9 * s)], fill=pen)
    if yikik > 0:
        rnd = random.Random(int(x * 5 + y))
        px = k.load()
        kes0 = y - int(30 * s) + int(yikik * 20 * s)
        dis = 0
        for xx in range(x - int(26 * s), x + int(26 * s)):
            if rnd.random() < 0.35:
                dis = rnd.randint(0, max(1, int(5 * s)))
            kes = kes0 + dis + (int(4 * s) if abs(xx - x) > 12 * s else 0)
            for yy in range(0, min(kes, img.height)):
                if 0 <= xx < img.width:
                    px[xx, yy] = (0, 0, 0, 0)
        for mx in (x - int(20 * s), x + int(2 * s), x + int(21 * s)):
            mw = int(10 * s * (0.5 + yikik))
            d.polygon([(mx - mw // 2, y - 1), (mx, y - 1 - mw // 3), (mx + mw // 2, y - 1)], fill=tugk)
            for _ in range(5):
                ox = rnd.randint(-mw // 3, mw // 3)
                b = _u(1, s)
                d.rectangle([mx + ox - b, y - 2 - b * 2, mx + ox + b, y - 2], fill=rnd.choice([tug, tas]))
    img.alpha_composite(k)
    temas_golgesi(img, x, y, 50 * s)


def osmanli_camii(img, x, zemin, s=1.0, tas="#d8cdb8", kubbe=KURSUN):
    """Yeni figür: Kılıç Ali Paşa Camii (Mimar Sinan): kare gövde, yan yarım kubbeler, merkezî kurşun kubbe,
    sağda tek kalem minare (şerefeli, külahlı). Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(22 * s), x + int(26 * s), "cami", tolerans=max(3, int(s)))
    temas_golgesi(img, x + int(2 * s), y, 50 * s)
    t, tk = hex2(tas), hex2(_ac(tas, -0.22))
    kb, kbk = hex2(kubbe), hex2(_ac(kubbe, -0.2))
    d.rectangle([x - int(20 * s), y - int(12 * s), x + int(20 * s), y - 1], fill=t)              # gövde
    for yy in range(y - int(12 * s) + _u(3, s), y - 1, _u(3, s)):
        d.line([x - int(20 * s), yy, x + int(20 * s), yy], fill=tk)
    for px in (-15, -9, 9, 15):                                                                 # pencereler
        d.rectangle([x + int(px * s) - _u(1, s), y - int(9 * s), x + int(px * s) + _u(1, s), y - int(5 * s)], fill=hex2("#2a3040"))
        d.chord([x + int(px * s) - _u(1, s), y - int(10 * s), x + int(px * s) + _u(1, s), y - int(8 * s)], 180, 360, fill=hex2("#2a3040"))
    d.rectangle([x - _u(2.4, s), y - int(8 * s), x + _u(2.4, s), y - 1], fill=hex2("#3a2a20"))   # taç kapı
    d.chord([x - _u(2.4, s), y - int(10 * s), x + _u(2.4, s), y - int(6 * s)], 180, 360, fill=hex2("#3a2a20"))
    for yon in (-1, 1):                                                                         # yarım kubbeler
        cx = x + int(12 * s) * yon
        d.rectangle([cx - int(6 * s), y - int(14 * s), cx + int(6 * s), y - int(12 * s)], fill=t)
        d.chord([cx - int(6 * s), y - int(19 * s), cx + int(6 * s), y - int(10 * s)], 180, 360, fill=kb)
    d.rectangle([x - int(10 * s), y - int(18 * s), x + int(10 * s), y - int(12 * s)], fill=t, outline=tk)   # kasnak
    for px in range(-8, 9, 4):
        d.rectangle([x + int(px * s) - _u(0.5, s), y - int(17 * s), x + int(px * s) + _u(0.5, s), y - int(14 * s)], fill=hex2("#2a3040"))
    d.chord([x - int(10 * s), y - int(29 * s), x + int(10 * s), y - int(8 * s)], 180, 360, fill=kb)        # ana kubbe
    for r in (-6, -2, 2, 6):
        d.line([x + int(r * s), y - int(18 * s), x + int(r * 0.4 * s), y - int(28 * s)], fill=kbk)
    d.line([x, y - int(29 * s), x, y - int(32 * s)], fill=hex2("#e0b040"), width=_u(0.5, s))
    mx = x + int(24 * s)                                                                         # minare
    d.rectangle([mx - _u(1.8, s), y - int(40 * s), mx + _u(1.8, s), y - 1], fill=t)
    d.line([mx + _u(1.8, s), y - int(40 * s), mx + _u(1.8, s), y - 1], fill=tk)
    d.rectangle([mx - _u(3, s), y - int(31 * s), mx + _u(3, s), y - int(30 * s)], fill=hex2(_ac(tas, -0.1)))  # şerefe
    d.polygon([(mx - _u(2, s), y - int(40 * s)), (mx, y - int(48 * s)), (mx + _u(2, s), y - int(40 * s))], fill=kb)
    d.rectangle([mx - _u(2.6, s), y - int(3 * s), mx + _u(2.6, s), y - 1], fill=tk)            # kaide


def ulugbey_rasathanesi(img, x, zemin, s=1.0, tugla="#c8a878", mavi="#2a7ab8"):
    """Yeni figür: Semerkant'taki Uluğ Bey gözlemevi: üç katlı silindir gövde (önden), mavi çini kuşaklar, kemerli
    nişler; ortada dev meridyen yayının yuvası (koyu dikey yarık). Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(20 * s), x + int(20 * s), "Uluğ Bey gözlemevi", tolerans=max(3, int(s)))
    temas_golgesi(img, x, y, 44 * s)
    h = int(30 * s)
    for xx in range(x - int(20 * s), x + int(20 * s) + 1):                                     # silindir gölgelemesi
        t = (xx - x) / (20 * s)
        renk = _ac(tugla, -0.35 * t * t) if t > -0.4 else _ac(tugla, 0.08)
        d.line([xx, y - h, xx, y - 1], fill=hex2(renk))
    for kat in (1, 2):
        ky = y - int(kat * 10 * s)
        d.rectangle([x - int(20 * s), ky - _u(1.4, s), x + int(20 * s), ky], fill=hex2(mavi))
        for xx in range(x - int(20 * s), x + int(20 * s), 3):
            piksel(img, xx, ky - _u(0.7, s), hex2("#f4ecd8"))
    for kat in range(3):
        for px in (-15, -9, 9, 15):
            ky = y - int(kat * 10 * s) - int(3 * s)
            d.rectangle([x + int(px * s) - _u(1.4, s), ky - int(4 * s), x + int(px * s) + _u(1.4, s), ky], fill=hex2("#3a2a20"))
            d.chord([x + int(px * s) - _u(1.4, s), ky - int(5.5 * s), x + int(px * s) + _u(1.4, s), ky - int(2.5 * s)], 180, 360,
                    fill=hex2("#3a2a20"))
    d.rectangle([x - int(3 * s), y - h, x + int(3 * s), y - 1], fill=hex2("#2a1e18"))         # meridyen yuvası
    d.arc([x - int(3 * s), y - h - int(1 * s), x + int(3 * s) + int(30 * s), y + int(30 * s)], 180, 230, fill=hex2(PIRINC), width=_u(0.8, s))
    d.rectangle([x - int(21 * s), y - h - _u(1.4, s), x + int(21 * s), y - h], fill=hex2(mavi))   # üst kuşak


def dokumhane(img, x, zemin, s=1.0, tugla="#9a5a40"):
    """Yeni figür: Tophane-i Âmire top döküm ocağı: alçak kâgir yapı, kurşun kubbeler, iki ocak bacası. Düz zemine
    kurulur. Dönen değer: baca ağızları [(x, y)] (duman buradan yukarı çıkar)."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(24 * s), x + int(24 * s), "döküm ocağı", tolerans=max(3, int(s)))
    temas_golgesi(img, x, y, 52 * s)
    t, tk = hex2(tugla), hex2(_ac(tugla, -0.3))
    d.rectangle([x - int(24 * s), y - int(12 * s), x + int(24 * s), y - 1], fill=t)
    for yy in range(y - int(12 * s) + _u(2, s), y - 1, _u(2, s)):
        d.line([x - int(24 * s), yy, x + int(24 * s), yy], fill=tk)
    for kx in (-14, 0, 14):
        d.chord([x + int((kx - 6) * s), y - int(19 * s), x + int((kx + 6) * s), y - int(6 * s)], 180, 360, fill=hex2(KURSUN))
        d.line([x + int(kx * s), y - int(19 * s), x + int(kx * s), y - int(21 * s)], fill=hex2("#e0b040"))
    bacalar = []
    for bx in (-20, 20):
        d.rectangle([x + int(bx * s) - _u(1.8, s), y - int(26 * s), x + int(bx * s) + _u(1.8, s), y - int(12 * s)], fill=tk)
        d.rectangle([x + int(bx * s) - _u(2.3, s), y - int(27 * s), x + int(bx * s) + _u(2.3, s), y - int(26 * s)], fill=t)
        bacalar.append((x + int(bx * s), y - int(27 * s)))
    for px in (-8, 8):                                                                           # ocak ağızları
        d.rectangle([x + int(px * s) - _u(2.2, s), y - int(6 * s), x + int(px * s) + _u(2.2, s), y - 1], fill=hex2("#e86a20"))
        d.rectangle([x + int(px * s) - _u(1.2, s), y - int(4 * s), x + int(px * s) + _u(1.2, s), y - 1], fill=hex2("#ffd060"))
    return bacalar


def masa_saati(img, x, zemin, s=1.0, f=0.0):
    """Yeni figür: Takiyüddin'in mekanik masa saati, ahşap ayaklı sehpanın üstünde. Sehpanın ayakları zemine basar;
    saat gövdesi sehpaya oturur, kadranda akrep f ile döner, üstte çan."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 8 * s)
    temas_golgesi(img, x, y, 10 * s)
    ah = hex2("#6a4428")
    ust = y - int(7 * s)
    for dx in (-3, 3):
        d.line([x + int(dx * s), ust, x + int(dx * 1.2 * s), y - 1], fill=ah, width=_u(0.8, s))
    d.rectangle([x - int(4.5 * s), ust - _u(1, s), x + int(4.5 * s), ust], fill=hex2("#8a5a34"))
    g0 = ust - _u(1, s)
    d.rectangle([x - int(2.6 * s), g0 - int(7 * s), x + int(2.6 * s), g0], fill=hex2("#c8a040"), outline=hex2("#7a5a22"))
    cy, r = g0 - int(4 * s), int(2 * s)
    d.ellipse([x - r, cy - r, x + r, cy + r], fill=hex2("#f4ecd8"), outline=hex2("#7a5a22"))
    a = f * 2 * math.pi
    d.line([x, cy, x + math.sin(a) * (r - 1), cy - math.cos(a) * (r - 1)], fill=hex2("#2a1a10"))
    d.chord([x - int(1.6 * s), g0 - int(9.5 * s), x + int(1.6 * s), g0 - int(6.5 * s)], 180, 360, fill=hex2("#e0b040"))  # çan


def minyatur_kitap(img, x, zemin, s=1.0):
    """Yeni figür: Şehinşâhnâme'nin açık sayfası, rahlenin üstünde. Rahlenin çapraz ayakları zemine basar; sol
    sayfada altın çerçeveli rasathane minyatürü (küçük sarıklı gökbilimciler, yay ve küre), sağ sayfada yazı satırları."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 20 * s)
    temas_golgesi(img, x, y, 22 * s)
    ah = hex2("#5a3a1e")
    d.line([x - int(8 * s), y - 1, x + int(6 * s), y - int(9 * s)], fill=ah, width=_u(1.2, s))   # rahle ayakları
    d.line([x + int(8 * s), y - 1, x - int(6 * s), y - int(9 * s)], fill=ah, width=_u(1.2, s))
    by = y - int(9 * s)
    # sayfalar (hafif açık V)
    sol = [(x - int(15 * s), by - int(12 * s)), (x, by - int(10 * s)), (x, by), (x - int(15 * s), by - int(2 * s))]
    sag = [(x, by - int(10 * s)), (x + int(15 * s), by - int(12 * s)), (x + int(15 * s), by - int(2 * s)), (x, by)]
    d.polygon([(p[0], p[1] + _u(1, s)) for p in sol + sag[1:3]], fill=hex2("#6a2a1e"))          # cilt
    d.polygon(sol, fill=hex2("#f0e4c4"))
    d.polygon(sag, fill=hex2("#ece0c0"))
    d.line([x, by - int(10 * s), x, by], fill=hex2("#b8a888"))
    # minyatür (sol sayfa)
    fx0, fx1 = x - int(13.5 * s), x - int(1.5 * s)
    fy0, fy1 = by - int(10.5 * s), by - int(3 * s)
    d.rectangle([fx0, fy0, fx1, fy1], fill=hex2("#3a6a9a"), outline=hex2("#e0b040"))
    d.rectangle([fx0 + 1, fy0 + int(4.5 * s), fx1 - 1, fy1 - 1], fill=hex2("#c87a4a"))         # oda zemini
    d.arc([fx0 + int(1 * s), fy0 + int(1 * s), fx0 + int(7 * s), fy0 + int(7 * s)], 270, 360, fill=hex2("#ffd060"))  # yay
    d.ellipse([fx1 - int(4 * s), fy0 + int(1 * s), fx1 - int(1 * s), fy0 + int(4 * s)], outline=hex2("#ffd060"))      # küre
    rnd = random.Random(7)
    for kx in range(fx0 + int(2 * s), fx1 - int(1 * s), max(2, int(2.2 * s))):                  # sarıklı küçük figürler
        gy = fy1 - 2
        d.rectangle([kx - 1, gy - int(2.5 * s), kx + 1, gy], fill=hex2(rnd.choice(["#2a6a3a", "#8a1e22", "#2a4a8a", "#e0b040"])))
        piksel(img, kx, gy - int(2.5 * s) - 1, hex2("#d6a07a"))
        piksel(img, kx, gy - int(2.5 * s) - 2, hex2("#f8f4ea"))
    for k_ in range(6):                                                                          # yazı satırları (sağ)
        yy = by - int((10.5 - k_ * 1.5) * s)
        d.line([x + int(2 * s), yy + int(k_ * 0.1 * s), x + int(13 * s), yy - int(0.6 * s) + int(k_ * 0.1 * s)],
               fill=hex2("#3a2a1a" if k_ % 3 else "#8a1e22"))


def bos_sedir(img, x, zemin, s=1.0, renk="#7a4a2a", ortu="#2a6a3a", minder="#c8a040"):
    """Yeni figür: boş makam (sadrazamın boş koltuğu): ayakları zemine basan sedir, üstünde dokunulmamış minder ve
    yaslanma yastığı."""
    d = ImageDraw.Draw(img)
    ust = sedir(img, x, zemin, s, renk=renk, ortu=ortu)
    d.rectangle([x - int(6 * s), ust - int(1.8 * s), x + int(6 * s), ust], fill=hex2(minder), outline=hex2(_ac(minder, -0.35)))
    d.rounded_rectangle([x - int(9 * s), ust - int(6 * s), x - int(6 * s), ust], radius=_u(1, s), fill=hex2(_ac(minder, -0.15)),
                        outline=hex2(_ac(minder, -0.4)))
    return ust


def ortulu_tabut(img, x, zemin, s=1.0, ortu="#2a5a3a"):
    """Yeni figür: veba sahnesi için yeşil örtülü ahşap tabut: iki alçak sehpanın üstünde; sehpaların ayakları
    zemine basar, örtünün kenarları sehpaların yanından sarkar."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 26 * s)
    temas_golgesi(img, x, y, 28 * s)
    ah = hex2("#5a3a1e")
    for sx_ in (-9, 9):
        d.rectangle([x + int(sx_ * s) - int(3 * s), y - int(4 * s), x + int(sx_ * s) + int(3 * s), y - int(3.2 * s)], fill=ah)
        for ax in (-2, 2):
            d.line([x + int((sx_ + ax) * s), y - int(3.2 * s), x + int((sx_ + ax * 1.2) * s), y - 1], fill=ah, width=_u(0.6, s))
    g0 = y - int(4 * s)
    d.polygon([(x - int(13 * s), g0), (x - int(12 * s), g0 - int(5 * s)), (x + int(12 * s), g0 - int(6 * s)),
               (x + int(13 * s), g0)], fill=hex2(ortu))
    d.line([x - int(12 * s), g0 - int(5 * s), x + int(12 * s), g0 - int(6 * s)], fill=hex2(_ac(ortu, 0.25)))
    for kx in (-6, 0, 6):                                                                         # örtü kıvrımları
        d.line([x + int(kx * s), g0 - int(5.4 * s), x + int(kx * s), g0], fill=hex2(_ac(ortu, -0.25)))


# ==========================================================================
# ÖLÇEK VE KADRAJ YARDIMCILARI (Cem Sultan dosyasının kalıbı: video/piksel/cem_sultan.py)
# Yeni çizim fonksiyonu DEĞİL: figürü boş yüzeye çizip alfa kanalından ölçer.
# ==========================================================================
def _bb(img):
    return img.getchannel("A").getbbox()


_ONBELLEK = {}


def olcek(ad, yakin, cizim, oran=0.32):
    """Figür kutusu kadraj yüksekliğinin >= oran'ı olan en küçük s (0.1 adım). Görünen ızgara yüksekliği = 960/yakin."""
    anahtar = (ad, yakin, oran)
    if anahtar in _ONBELLEK:
        return _ONBELLEK[anahtar]
    hedef = oran * 960 / yakin
    s = 2.0
    while s <= 9.0:
        t = yeni(560, 420)
        cizim(t, round(s, 1), duz(417, 560))
        bb = _bb(t)
        if bb and bb[1] <= 1:
            break
        if bb and bb[3] - bb[1] >= hedef:
            _ONBELLEK[anahtar] = round(s, 1)
            return _ONBELLEK[anahtar]
        s += 0.1
    raise RuntimeError(f"olcek({ad}, yakin={yakin}): %{int(oran * 100)} boya ulaşılamadı")


def s_kisi(yakin, oran=0.32):
    return olcek("kisi", yakin, lambda t, s, z: figur(t, kisi, 280, z, s, **TAKI, yon=1), oran)


def s_oturan(yakin, oran=0.30):
    return olcek("oturan", yakin, lambda t, s, z: figur(t, oturan, 280, z, s, **TAKI, yon=-1, minder="#c8a040"), oran)


def s_atli(yakin):
    """İnsan/at oranı: atlı 2.9 ↔ kisi 2.6 (SKILL.md)."""
    return round(s_kisi(yakin, 0.24) * 2.9 / 2.6, 1)


def _kz(yakin, taban=634, h=300):
    """Kandil zinciri: sprite'ın üst kenarından (tavan) kadrajın üst kenarının biraz altına."""
    ust_gorunen = (taban - 12) * (1 - 1 / yakin)
    return max(40, int(ust_gorunen - (taban - h)) + 10)


def _kadraj(no, kare, w, h, yakin, esik):
    """Görünür aralık yerel x = w/2 ± 270/yakin. Opak piksellerin en az `esik` oranı içeride olmalı; figür sprite'ın
    üstüne değmemeli (kesik baş = hata)."""
    yarim = 270 / yakin
    a, b = max(int(w / 2 - yarim), 0), min(int(w / 2 + yarim), w)
    for i in (0, 12):
        t = yeni(w, h)
        kare(t, duz(h - 1, w), i)
        alfa = t.getchannel("A")
        toplam = sum(alfa.histogram()[1:])
        bb = alfa.getbbox()
        ust_satir = sum(alfa.crop((0, 0, w, 2)).histogram()[1:])
        if not toplam or (bb[1] <= 1 and ust_satir > 12):
            raise RuntimeError(f"Sahne {no}: sprite yüksekliği (h={h}) yetmiyor ya da kare boş")
        ici = sum(alfa.crop((a, 0, b, h)).histogram()[1:])
        if ici / toplam < esik:
            raise RuntimeError(f"Sahne {no}: figürlerin %{int(100 * ici / toplam)}'i görünür aralıkta (x {a}-{b})")


def _spr(no, w, h, kare, yakin, esik=0.75):
    _kadraj(no, kare, w, h, yakin, esik)
    sprite(no, "karakter", w, h, KARE, kare)      # taban_denetimi varsayılan açık


def _gorunur(no, xler, sx0, sx1, yakin, pay=12):
    """Orta plandaki önemli figürlerin ızgara x'i, sprite'ın başlangıç ve bitiş sx değerlerinde görünür aralıkta."""
    for sx in (sx0, sx1):
        a, b = sx - 270 / yakin + pay, sx + 270 / yakin - pay
        for x in xler:
            if not a <= x <= b:
                raise RuntimeError(f"Sahne {no}: orta plan figürü x={x} görünür aralık [{int(a)}, {int(b)}] dışında")


# ==========================================================================
# KİŞİLER (renk kimlikleri bütün sahnelerde aynı)
# ==========================================================================
TAKI = dict(govde="#2a5a6a", bas="sarik", bas_renk="#f4f0e6", sakal="#3a2a1a")          # Takiyüddin
TAKI_YASLI = dict(TAKI, sakal="#e0dcd4")
TYCHO = dict(govde="#2a2a36", bas="sapka", bas_renk="#1a1a22", sakal="#c8903a", kemer="#c8a040")
FREDERIK = dict(govde="#8a1e22", bas="tac", bas_renk="#e0b040", sakal="#a87a4a")
MURAD = dict(govde="#8a1e22", bas="sarik", bas_renk="#f8f4ea", sakal="#a8522a")         # III. Murad
ULUGBEY = dict(govde="#3a5a8a", bas="sorguc", bas_renk="#2a1a14", sakal="#2a1a12")
KILIC_ALI = dict(govde="#7a1e22", bas="sarik", bas_renk="#f4f0e6", sakal="#9a9088")
SEYHULISLAM = dict(govde="#2a4a3a", bas="sarik", bas_renk="#fbf8f0", sakal="#ece8e0")
SOKOLLU = dict(govde="#2a6a3a", bas="sarik", bas_renk="#f8f4ea", sakal="#d8d0c8")
SINAN = dict(govde="#6a5a44", bas="sarik", bas_renk="#f0ebe0", sakal="#e0dcd4")
LEVEND = dict(govde="#a8281e", bas="kalpak", bas_renk="#4a3222", sakal="#6a4a30")       # donanma topçusu
KATIP = dict(govde="#5a4a6a", bas="sarik", bas_renk="#ece6d8", sakal="#4a3a2a")
NAKKAS = dict(govde="#6a3a2a", bas="sarik", bas_renk="#ece6d8", sakal="#2a1a12")
MUNECCIM = dict(govde="#4a3a6a", bas="sarik", bas_renk="#f4f0e6", sakal="#2a1a12")      # sonraki müneccimbaşı

# ==========================================================================
# KATMAN YARDIMCILARI
# ==========================================================================
GECE = ["#070a1c", "#0e1430", "#162046", "#1e2c5a", "#28386a", "#324478"]
GECE_BULUT = ("#4a5a80", "#34446a", "#243458")


def _gok(no, renkler, bulutlar=(), bulut_renk=("#fff8ec", "#f4dcc8", "#d8a8a0"), gunes_=None, yildiz=0,
         y0=300, y1=600, ay=None, kuyruk=None):
    """Gökyüzü + görünür bölgeye (y0-y1) yıldızlar + ay + kuyruklu yıldız. ciz.yildizlar yalnızca y<300'e serper;
    yakın çekimde görünen gök y≈380-600 arasıdır, yıldızlar oraya da serpilir."""
    img = gokyuzu(no, renkler, gunes_, bulutlar, bulut_renk, 0)
    if yildiz:
        rnd = random.Random(no * 13)
        for _ in range(yildiz):
            x, y = rnd.randrange(img.width), rnd.randrange(y0, y1)
            a = rnd.choice((110, 170, 255))
            piksel(img, x, y, hex2("#fff8e0", a))
            if a == 255 and rnd.random() < 0.35:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    piksel(img, x + dx, y + dy, hex2("#fff8e0", 80))
    if ay:
        gunes(img, ay[0], ay[1], ay[2], ["#f4f0e0", "#b8c4dc"])
    if kuyruk:
        kuyruklu_yildiz(img, *kuyruk, tohum=no)
    kaydet(img, f"sahne{no}-gokyuzu.png")


def _uzak_deniz(no, dag, tepe, deniz, dag_y, tepe_y, ova_y, gemiler=(), kenar=None):
    """Uzak plan: karşı kıyı tepeleri ve önünde düz deniz (ova rengi su). gemiler: [(x, s, yelken)] su çizgisine oturur."""
    img = uzak(no, dag, tepe, deniz, dag_y=dag_y, tepe_y=tepe_y, ova_y=ova_y, kenar=kenar)
    for x, s, yelken in gemiler:
        figur(img, gemi, x, ova_y + int(6 * s), s, 1, 0.0, govde="#3a2a22", yelken=yelken, hac=False)
    kaydet(img, f"sahne{no}-uzak.png")


def _toz(t, x, y, f, boy, tohum, genislik=1.4, renk="#b8aa94"):
    """Yıkıntıdan yükselen toz: yerden (y) başlar, yukarı çıkar (ciz.duman)."""
    duman(t, x, y, boy, tohum, faz=f, renk=renk, ruzgar=0.25, genislik=genislik)


def _cimen(t, z, f, renkler, tohum, x0=0, x1=None, boy=6):
    """Sprite'ın zemin satırında rüzgârla salınan çimen (dibi zemine basar)."""
    from ciz import cimen_tutamlari
    cimen_tutamlari(t, z, renkler, tohum, 0.45, boy, x0, x1, ruzgar=0.6 * SIN(f))


# Ortak paletler
KIS = ["#24243e", "#3e3a58", "#5a506e", "#7a6680", "#987a88", "#b08e8e"]          # Ocak 1580: kış alacakaranlığı
KIS_DAG, KIS_TEPE = ["#4e4a66", "#44405c"], ["#5a5470", "#4e4a64"]
KIS_DENIZ = ["#44506e", "#3c4864", "#34405a"]
KIS_ORTA = ["#5a5a4a", "#4e4e40", "#424236", "#36362e", "#2c2c26"]
GUN_IST = ["#4a7ab8", "#6a92c4", "#8aaad0", "#a8c0dc", "#c4d4e4", "#d8e2ea"]       # İstanbul gündüz
ALTIN_SAAT = ["#4a3a6a", "#8a5a7a", "#c8786a", "#e89a6a", "#f4bc7a", "#f8d494"]
GECE_DAG, GECE_TEPE = ["#1a2240", "#161d38"], ["#1e2846", "#19223e"]
GECE_DENIZ = ["#1a2a4a", "#162440", "#121e38"]
GECE_ORTA = ["#2a3440", "#242d38", "#1e2630", "#182028", "#121a20"]


def _gece_ortasi(no, ust=(540, 552), ekle=None, renkler=GECE_ORTA, kenar="#5a6a84"):
    orta(no, ust, renkler, kenar, ekle=ekle)
    on(no, [renkler[-1], renkler[-2], renkler[-3]], kenar, boy=120)


# --------------------------------------------------------------------------
# 410 (kapak + kart 1-2): yıkım anı (anlatıya göre). Sağ geride terastaki rasathane, solda topçu ve top.
# --------------------------------------------------------------------------
def _rasathane_orta(cx, s, yikik=0.0, teras_h=10, isik=False, zemin_y_=588, genis=(62, 58)):
    """Orta plana teras + rasathane çizen ekle fonksiyonu (cx: ızgara x'i)."""
    def ekle(img, z):
        ust = figur(img, teras, PAY + cx - genis[0], PAY + cx + genis[1], duz(zemin_y_), teras_h)
        figur(img, rasathane, PAY + cx, duz(ust), s, yikik=yikik, isik=isik)
    return ekle


def sahne410():
    """Kanca: Ocak 1580, kış alacakaranlığı. Tophane sırtında terastaki rasathane kısmen yıkık, dibinden toz kalkar;
    solda donanmanın topçusu ve namlusu binaya dönük tunç top ateşler (anlatıya göre)."""
    _gok(410, KIS)
    uzak(410, KIS_DAG, KIS_TEPE, KIS_DENIZ, dag_y=(436, 470), tepe_y=478, ova_y=494)
    yk = 2.6
    K = s_kisi(yk, 0.30)
    _gorunur(410, [272, 356], 270, 270, yk)
    orta(410, (540, 552), KIS_ORTA, "#8a8a70", ekle=_rasathane_orta(314, 1.9, yikik=0.35))
    on(410, [KIS_ORTA[-1], KIS_ORTA[-2], KIS_ORTA[-3]], "#8a8a70", boy=120)
    st = round(0.72 * K, 1)

    def kare(t, z, i):
        f = i / KARE
        for j, mx in enumerate((248, 288)):                          # moloz noktalarından toz (ızgara 318 ve 358)
            _toz(t, mx, 246, (f + j * 0.45) % 1, 54, 410 + j, genislik=2.0)
        figur(t, kisi, 132, z, K, **LEVEND, yon=1, kol=0.45 + 0.05 * SIN(f))      # topçu binayı gösterir
        ates = max(0.0, 1 - f / 0.12) if f < 0.12 else 0.0
        mx, my = figur(t, top_, 196, z, st, 1, ates=ates)
        duman(t, mx + 4, my, 44, 7, faz=f, renk="#d8d0c8", ruzgar=0.45, genislik=1.2)   # namlu dumanı yukarı çıkar

    _spr(410, 400, 300, kare, yk, esik=0.7)


# --------------------------------------------------------------------------
# 411 (kart 3-4): Tophane'nin yukarısı, alacakaranlık; bina sağlam (üç yıl önce kurulan yapı), pencerelerde kandil.
# --------------------------------------------------------------------------
def sahne411():
    """'Tophane'nin yukarısı, İstanbul': alacakaranlıkta terasın üstünde sağlam rasathane, pencerelerde kandil ışığı;
    arkada Boğaz ve karşı kıyının tepeleri. İnsan yok; terasın dibinde çimen rüzgârda salınır."""
    _gok(411, ["#1e1e3e", "#3a3058", "#6a4a6e", "#a0607a", "#c8807e", "#e0a088"], yildiz=40, y0=380, y1=470)
    uzak(411, ["#4a3e60", "#403656"], ["#54466a", "#4a3e60"], ["#3a4870", "#344066", "#2e385c"],
         dag_y=(470, 500), tepe_y=506, ova_y=516)
    orta(411, (548, 556), ["#4a5040", "#40463a", "#363c32", "#2e322a", "#262a22"], "#7a8a68")
    on(411, ["#262a22", "#2e322a", "#363c32"], "#7a8a68", boy=120)
    yk = 2.2
    s = 3.4

    def kare(t, z, i):
        f = i / KARE
        ust = figur(t, teras, 96, 314, z, 16)
        figur(t, rasathane, 205, duz(ust, t.width), s, isik=True)
        _cimen(t, z, f, ["#5a6a48", "#4a5a3c", "#6a7a54"], 411, 60, 340, boy=7)

    _spr(411, 400, 300, kare, yk, esik=0.85)


# --------------------------------------------------------------------------
# 412 (kart 5-6): gece, terasta Takiyüddin halkalı kürenin başında; sağ geride ışıklı rasathane.
# --------------------------------------------------------------------------
def sahne412():
    """'Kuran: Takiyüddin': gece; Takiyüddin halkalı kürenin (armilla) yanında ona döner, iç halka yavaşça döner;
    sağ geride terastaki rasathanenin pencereleri yanar."""
    _gok(412, GECE, yildiz=160, y0=360, y1=560)
    uzak(412, GECE_DAG, GECE_TEPE, GECE_DENIZ, dag_y=(470, 500), tepe_y=506, ova_y=516)
    yk = 2.6
    K = s_kisi(yk)
    _gorunur(412, [301, 359], 270, 270, yk)
    _gece_ortasi(412, (540, 552), ekle=_rasathane_orta(330, 1.3, isik=True, teras_h=8, genis=(40, 38)))

    def kare(t, z, i):
        f = i / KARE
        figur(t, armilla, 150, z, 3.6, faz=f * 0.5)
        figur(t, kisi, 215, z, K, **TAKI, yon=-1, kol=0.2 + 0.04 * SIN(f))

    _spr(412, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 413 (kart 7): soru. Gece; sağda terastaki rasathane, solda karanlıkta ona dönük tek bir top.
# --------------------------------------------------------------------------
def sahne413():
    """'Padişahın kendi gözlemevi hedef oldu': gece, terasın üstünde ışıklı rasathane; sol önde namlusu binaya dönük
    tunç top (topçu yok: tehdit, olay değil)."""
    _gok(413, ["#0a0818", "#160e2a", "#24163a", "#36204a", "#4a2a52", "#5e3456"], yildiz=120, y0=330, y1=560)
    uzak(413, ["#24183a", "#1e1432"], ["#2a1c40", "#241838"], ["#1e2444", "#1a203c", "#161c34"],
         dag_y=(486, 510), tepe_y=514, ova_y=524)
    orta(413, (556, 562), ["#2e2a36", "#28242e", "#221e28", "#1c1822", "#16121c"], "#5a4a6a")
    on(413, ["#16121c", "#1c1822", "#221e28"], "#5a4a6a", boy=100)
    yk = 2.2

    def kare(t, z, i):
        f = i / KARE
        ust = figur(t, teras, 150, 318, z, 14)
        figur(t, rasathane, 238, duz(ust, t.width), 2.9, isik=(i % 12) != 5)    # kandil titrer
        figur(t, top_, 108, z, 3.6, 1, egim=0.24)
        _cimen(t, z, f, ["#3a3446", "#2e2a3a", "#4a4256"], 413, 70, 150, boy=6)

    _spr(413, 400, 300, kare, yk, esik=0.85)


# --------------------------------------------------------------------------
# 414 (kart 8-9): Hven adası, 1576. Kral II. Frederik adayı Tycho'ya verir; arkada yükselen Uraniborg.
# --------------------------------------------------------------------------
KUZEY = ["#5a7aa8", "#7a96bc", "#9ab0cc", "#b8c8da", "#d0dae4", "#e0e6ea"]
KUZEY_DENIZ = ["#4a6a8a", "#42627e", "#3a5a74"]
HVEN_ORTA = ["#5a8a4a", "#4e7e42", "#44723a", "#3a6632", "#305a2a"]


def sahne414():
    """Hven, 1576: deniz ortasında yeşil ada; Kral II. Frederik (taçlı) belgeyi Tycho'ya uzatır, Tycho krala döner;
    arkada düz zeminde Uraniborg."""
    _gok(414, KUZEY)
    uzak(414, ["#7a8aa4", "#6e7e98"], ["#8a9aa8", "#7e8e9c"], KUZEY_DENIZ, dag_y=(476, 500), tepe_y=504, ova_y=512)
    yk = 2.8
    K = s_kisi(yk)
    _gorunur(414, [270], 270, 270, yk)
    orta(414, (536, 548), HVEN_ORTA, "#9ac078",
         ekle=lambda img, z: figur(img, uraniborg, PAY + 270, duz(588), 1.4))
    on(414, [HVEN_ORTA[-1], HVEN_ORTA[-2], HVEN_ORTA[-3]], "#9ac078", boy=120)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 148, z, K, **FREDERIK, yon=1, silah="mektup", kol=0.42 + 0.03 * SIN(f), pelerin="#2a2a6a")
        figur(t, kisi, 246, z, K, **TYCHO, yon=-1, kol=0.05 + 0.03 * SIN(f), pelerin="#6a2a2a")
        _cimen(t, z, f, ["#6a9a52", "#5a8a46", "#7aaa5e"], 414, 90, 310, boy=6)

    _spr(414, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 415 (kart 10): Uraniborg büyük plan, altın saat; çimen salınır.
# --------------------------------------------------------------------------
def sahne415():
    """'Tycho oraya Uraniborg'u kuruyor': altın saatte Hven'de Uraniborg; kırmızı tuğla, bakır kubbeler."""
    _gok(415, ["#5a5a8a", "#8a7a9a", "#c0909a", "#e0a890", "#f0c49a", "#f6d8a8"])
    uzak(415, ["#8a7a9a", "#7e6e90"], ["#9a8a9a", "#8e7e90"], ["#6a7a9a", "#5e6e90", "#526288"],
         dag_y=(486, 506), tepe_y=510, ova_y=518)
    orta(415, (550, 556), HVEN_ORTA, "#b8d088")
    on(415, [HVEN_ORTA[-1], HVEN_ORTA[-2], HVEN_ORTA[-3]], "#b8d088", boy=120)
    yk = 2.2

    def kare(t, z, i):
        f = i / KARE
        figur(t, uraniborg, 200, z, 3.0)
        _cimen(t, z, f, ["#6a9a52", "#5a8a46", "#8aba66"], 415, 60, 340, boy=8)

    _spr(415, 400, 300, kare, yk, esik=0.85)


# --------------------------------------------------------------------------
# 416 (kart 11): iki gözlemci, iki dev alet, teleskop yok. Solda Tycho ve çeyrek daire, sağda Takiyüddin ve armilla.
# --------------------------------------------------------------------------
def sahne416():
    """'Tycho da Takiyüddin de çıplak gözle, dev aletlerle bakıyor': aynı gece göğü altında solda Tycho duvar çeyrek
    dairesinin yayında, sağda Takiyüddin halkalı kürenin yanında. Teleskop hiçbir yerde yok."""
    _gok(416, GECE, yildiz=200, y0=340, y1=580)
    uzak(416, GECE_DAG, GECE_TEPE, GECE_DENIZ, dag_y=(480, 506), tepe_y=510, ova_y=520)
    _gece_ortasi(416, (548, 556))
    yk = 2.4
    K = s_kisi(yk, 0.30)

    def kare(t, z, i):
        f = i / KARE
        figur(t, ceyrek_daire, 160, z, 3.4, -1, aci=0.55 + 0.05 * SIN(f))
        figur(t, kisi, 118, z, K, **TYCHO, yon=1, kol=0.3, pelerin="#6a2a2a")
        figur(t, armilla, 276, z, 3.6, faz=f * 0.5)
        figur(t, kisi, 220, z, K, **TAKI, yon=1, kol=0.3)

    _spr(416, 400, 300, kare, yk, esik=0.8)


# --------------------------------------------------------------------------
# 417 (kart 12-13) ve 448 (kart 49-50): aynı gökyüzü, iki gözlemevi (solda Uraniborg, sağda İstanbul Rasathanesi).
# --------------------------------------------------------------------------
def _iki_gozlemevi(no, yikik):
    _gok(no, GECE, yildiz=240, y0=320, y1=590)
    uzak(no, GECE_DAG, GECE_TEPE, GECE_DENIZ, dag_y=(500, 526), tepe_y=530, ova_y=540)
    _gece_ortasi(no, (566, 572))
    yk = 2.0

    def kare(t, z, i):
        f = i / KARE
        figur(t, uraniborg, 126, z, 2.2, yikik=yikik[0], isik=not yikik[0])
        ust = figur(t, teras, 224, 332, z, 10)
        figur(t, rasathane, 280, duz(ust, t.width), 2.2, yikik=yikik[1], isik=not yikik[1])
        _cimen(t, z, f, ["#3a4a5a", "#2e3e4e", "#4a5a6a"], no, 60, 340, boy=7 if yikik[0] else 5)

    _spr(no, 400, 300, kare, yk, esik=0.9)


def sahne417():
    """'Aynı gökyüzü, iki gözlemevi': tek yıldızlı gece göğü altında yan yana Uraniborg (Hven) ve İstanbul
    Rasathanesi; ikisinin de pencereleri yanar."""
    _iki_gozlemevi(417, (0.0, 0.0))


# --------------------------------------------------------------------------
# 418 (kart 14-15): Şam, 1559: Takiyüddin rahlede saat kitabını yazar; yanında mekanik masa saati.
# --------------------------------------------------------------------------
def sahne418():
    """Şam, 1559: taş oda, kandil; Takiyüddin minderde oturup rahlede yazar, yanında sehpada mekanik masa saati."""
    ic_mekan(418, duvar=("#4a3a2a", "#5a4632", "#6a543a"), kemer="#3a2a1a", cini="#2a7a8a",
             zemin_renk=("#6a5a44", "#5a4c3a", "#4a3e30"), isik="#f8c060", hali=True)
    yk = 3.0
    s = s_oturan(yk)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, zincir=_kz(yk))
        mumluk(t, 112, z, f, 2)
        figur(t, oturan, 168, z, s, **TAKI, yon=1, el="kalem", minder="#8a2a2a")
        rahle(t, 222, z[0], 3.6)
        figur(t, masa_saati, 272, z, 4.4, f=f)

    _spr(418, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 419 (kart 16): Şam gecesi: Takiyüddin yıldızları gösterir, yanında masa saati; arkada Şam'ın kubbeleri.
# --------------------------------------------------------------------------
def sahne419():
    """'Saati gökyüzüne bağlamak': Şam'da gece avlu; Takiyüddin eliyle yıldızları gösterir, yanında sehpada
    mekanik saat; arkada düz ovada şehrin kubbeleri ve damları."""
    _gok(419, GECE, yildiz=200, y0=360, y1=560)
    uzak(419, GECE_DAG, GECE_TEPE, ["#2a2a3a", "#242432", "#1e1e2a"], dag_y=(480, 506), tepe_y=510, ova_y=520)
    yk = 2.6
    K = s_kisi(yk)
    _gorunur(419, [190, 350], 270, 270, yk, pay=0)
    _gece_ortasi(419, (540, 552), renkler=["#3a3430", "#322c28", "#2a2622", "#22201c", "#1c1a16"], kenar="#6a5e50",
                 ekle=lambda img, z: figur(img, orta_asya_sehri, PAY + 170, PAY + 370, duz(588), 1.3, tohum=419,
                                           kerpic="#7a6a5a", golge="#5a4c40", kubbe="#4a6a7a"))

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 168, z, K, **TAKI, yon=1, kol=0.75 + 0.05 * SIN(f))
        figur(t, masa_saati, 236, z, 5.0, f=f)

    _spr(419, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 420 (kart 17): İstanbul, 1571: Takiyüddin elinde beratıyla sağa yürür; arkada cami ve şehir.
# --------------------------------------------------------------------------
def sahne420():
    """İstanbul, 1571: gündüz; müneccimbaşı Takiyüddin elinde belgeyle yürür; arkada düz zeminde kurşun kubbeli cami."""
    _gok(420, GUN_IST, [(120, 330, 22)], ("#ffffff", "#e8eef4", "#c8d4e0"))
    uzak(420, ["#7a8ab0", "#6e7ea4"], ["#8a9aa8", "#7e8e9c"], ["#4a7aa8", "#42709c", "#3a6690"],
         dag_y=(476, 500), tepe_y=504, ova_y=512)
    yk = 2.8
    K = s_kisi(yk)
    _gorunur(420, [300], 255, 285, yk)
    orta(420, (536, 548), ["#7a8a5a", "#6e7e50", "#627246", "#56663e", "#4a5a36"], "#b0c088",
         ekle=lambda img, z: figur(img, osmanli_camii, PAY + 290, duz(588), 1.4))
    on(420, ["#4a5a36", "#56663e", "#627246"], "#b0c088", boy=120)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 190, z, K, **TAKI, yon=1, adim=f, silah="mektup")

    _spr(420, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 421 (kart 18): Semerkant: Uluğ Bey elinde yıldız cetveli; arkada gözlemevi ve mavi kubbe.
# --------------------------------------------------------------------------
def sahne421():
    """Semerkant (Uluğ Bey'in zamanı, geçmiş): altın saat; Uluğ Bey elinde cetvel; arkada silindir gözlemevi ve
    Gür-i Emir'in mavi kubbesi, ikisi de düz ovada."""
    _gok(421, ALTIN_SAAT)
    uzak(421, ["#8a6a7a", "#7e5e70"], ["#a07a70", "#946e66"], ["#c8a070", "#b89464", "#a88458"],
         dag_y=(476, 500), tepe_y=504, ova_y=512)
    yk = 2.8
    K = s_kisi(yk)
    _gorunur(421, [215, 320], 270, 270, yk)

    def ekle(img, z):
        figur(img, gur_i_emir, PAY + 215, duz(584), 0.9, mavi="#2a7ab8", tugla="#b89868")
        figur(img, ulugbey_rasathanesi, PAY + 322, duz(590), 1.5)

    orta(421, (536, 548), ["#c8a060", "#b89054", "#a88048", "#98703e", "#886036"], "#e8c888", ekle=ekle)
    on(421, ["#886036", "#98703e", "#a88048"], "#e8c888", boy=120)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 168, z, K, **ULUGBEY, yon=1, silah="mektup", kol=0.35 + 0.03 * SIN(f), pelerin="#2a3a5a")

    _spr(421, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 422 (kart 19): Semerkant gecesi: Uluğ Bey gözlemevi büyük plan.
# --------------------------------------------------------------------------
def sahne422():
    """'Uluğ Bey bu cetvel için orada bir gözlemevi kurmuştu': gece; üç katlı silindir gözlemevi, ortasında dev
    meridyen yayının yuvası; yıldızlar."""
    _gok(422, GECE, yildiz=220, y0=330, y1=580)
    uzak(422, GECE_DAG, GECE_TEPE, ["#2a2632", "#24202c", "#1e1a26"], dag_y=(486, 510), tepe_y=514, ova_y=524)
    _gece_ortasi(422, (552, 560), renkler=["#3a3430", "#322c28", "#2a2622", "#22201c", "#1c1a16"], kenar="#6a5e50")
    yk = 2.2

    def kare(t, z, i):
        f = i / KARE
        figur(t, ulugbey_rasathanesi, 200, z, 3.3, tugla="#a8906a", mavi="#2a6aa8")
        _cimen(t, z, f, ["#4a4436", "#3a362c", "#5a5444"], 422, 60, 340, boy=6)

    _spr(422, 400, 300, kare, yk, esik=0.85)


# --------------------------------------------------------------------------
# 423 (kart 20): saray: III. Murad sedirde; Takiyüddin diz çöküp kitabını sunar; yerde kitaplar.
# --------------------------------------------------------------------------
def _saray(no, pencere=None):
    ic_mekan(no, duvar=("#2a3a3a", "#344a46", "#405a54"), kemer="#1a2a28", cini="#2a8a9a",
             pencere=pencere, zemin_renk=("#6a4a3a", "#5a3e30", "#4a3428"), isik="#f8c060", hali=True)


def sahne423():
    """'Padişah Üçüncü Murad kitabı ve resmi seven bir hükümdar. Onay veriyor.': saray odası; III. Murad sedirde
    oturur, Takiyüddin önünde diz çöküp kitabını sunar; yanda yığılı kitaplar."""
    _saray(423)
    yk = 2.8
    K = s_kisi(yk)
    so = s_oturan(yk, 0.26)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, zincir=_kz(yk))
        ust = figur(t, sedir, 258, z, round(0.75 * so, 1), renk="#7a4a2a", ortu="#8a1e22")
        figur(t, oturan, 258, duz(ust, t.width), so, **MURAD, yon=-1, minder="#c8a040")
        figur(t, kisi, 158, z, K, **TAKI, yon=1, diz=True, silah="mektup", kol=0.35 + 0.03 * SIN(f))
        kitaplar(t, 112, z[0], 4.0)
        mumluk(t, 312, z, f, 3)

    _spr(423, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 424 (kart 21): Tophane'nin yukarısı, 1577: çeyrek daire kurulur; Takiyüddin yön verir, işçi kazar.
# --------------------------------------------------------------------------
def sahne424():
    """1577: gündüz, Tophane sırtı; taş ayaklı çeyrek daire yerine oturtulur; Takiyüddin eliyle gösterir, işçi kazma
    sallar; sağ geride terastaki rasathane."""
    _gok(424, GUN_IST, [(400, 330, 22)], ("#ffffff", "#e8eef4", "#c8d4e0"))
    uzak(424, ["#7a8ab0", "#6e7ea4"], ["#8a9aa8", "#7e8e9c"], ["#4a7aa8", "#42709c", "#3a6690"],
         dag_y=(476, 500), tepe_y=504, ova_y=512)
    yk = 2.6
    K = s_kisi(yk)
    _gorunur(424, [300, 352], 270, 270, yk)
    orta(424, (536, 548), ["#8a8a5a", "#7e7e50", "#727246", "#66663e", "#5a5a36"], "#c0c088",
         ekle=_rasathane_orta(328, 1.3, teras_h=8, genis=(40, 38)))
    on(424, ["#5a5a36", "#66663e", "#727246"], "#c0c088", boy=120)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 122, z, K, **TAKI, yon=1, kol=0.45)
        figur(t, ceyrek_daire, 196, z, 3.0, 1, aci=0.4)
        figur(t, taslar, 255, z, 2.6)
        figur(t, kisi, 288, z, K, govde="#6a4a2a", bas="bork", bas_renk="#4a3222", sakal=None, yon=-1,
              silah="kazma", kol=0.5 + 0.4 * SIN(f))

    _spr(424, 400, 300, kare, yk, esik=0.72)


# --------------------------------------------------------------------------
# 425-427: Kasım 1577 kuyruklu yıldızı. Ufuk alçak tutulur ki yıldız yazının altında, figürlerin yanında görünsün.
# --------------------------------------------------------------------------
ALCAK_UZAK = dict(dag_y=(548, 570), tepe_y=574, ova_y=584)


def sahne425():
    """Kasım 1577, İstanbul gecesi: terastaki rasathanenin üstünde, gökte uzun kuyruklu yıldız belirir. İnsan yok."""
    _gok(425, GECE, yildiz=260, y0=320, y1=590, kuyruk=(252, 528, 62, -2.6))
    uzak(425, GECE_DAG, GECE_TEPE, GECE_DENIZ, **ALCAK_UZAK)
    _gece_ortasi(425, (598, 604))
    yk = 2.0

    def kare(t, z, i):
        f = i / KARE
        ust = figur(t, teras, 214, 334, z, 12)
        figur(t, rasathane, 272, duz(ust, t.width), 2.4, isik=True)
        _cimen(t, z, f, ["#3a4a5a", "#2e3e4e", "#4a5a6a"], 425, 60, 340, boy=5)

    _spr(425, 400, 300, kare, yk, esik=0.9)


def sahne426():
    """Hven, 13 Kasım 1577 gecesi: Tycho çeyrek dairenin yanında elini kuyruklu yıldıza kaldırır; gökte alçakta Ay,
    daha yukarıda kuyruklu yıldız (ölçümün sonucu: yıldız Ay'ın ötesinde)."""
    _gok(426, GECE, yildiz=240, y0=320, y1=590, ay=(178, 552, 7), kuyruk=(352, 516, 56, -2.6))
    uzak(426, ["#1c2440", "#182038"], ["#202a46", "#1b243e"], ["#1a2c48", "#16263e", "#122036"], **ALCAK_UZAK)
    _gece_ortasi(426, (598, 604), renkler=["#24382e", "#1e3028", "#182822", "#12201c", "#0e1a16"], kenar="#4a6a5a")
    yk = 2.2
    K = s_kisi(yk, 0.30)

    def kare(t, z, i):
        f = i / KARE
        figur(t, ceyrek_daire, 232, z, 3.6, 1, aci=0.62 + 0.04 * SIN(f))
        figur(t, kisi, 166, z, K, **TYCHO, yon=1, kol=0.62 + 0.05 * SIN(f), pelerin="#6a2a2a")

    _spr(426, 400, 300, kare, yk, esik=0.85)


def sahne427():
    """İstanbul, aynı günlerin gecesi: Takiyüddin halkalı kürenin yanında kuyruklu yıldıza bakar, elini kaldırır."""
    _gok(427, GECE, yildiz=240, y0=320, y1=590, kuyruk=(206, 528, 50, -2.6))
    uzak(427, GECE_DAG, GECE_TEPE, GECE_DENIZ, **ALCAK_UZAK)
    _gece_ortasi(427, (598, 604))
    yk = 2.2
    K = s_kisi(yk, 0.30)

    def kare(t, z, i):
        f = i / KARE
        figur(t, armilla, 286, z, 3.6, faz=f * 0.5)
        figur(t, kisi, 212, z, K, **TAKI, yon=-1, kol=0.62 + 0.05 * SIN(f))

    _spr(427, 400, 300, kare, yk, esik=0.85)


# --------------------------------------------------------------------------
# 428 (kart 26): kaynaklar ayrışıyor: kâtip iki kitap arasında yazar.
# --------------------------------------------------------------------------
def sahne428():
    """'Kaynaklar ayrışıyor': gece, kâtip odası; vakanüvis rahlede yazar, iki yanında ayrı kitap yığınları."""
    ic_mekan(428, duvar=("#2a2a34", "#343440", "#40404e"), kemer="#1a1a22", cini="#5a3a6a",
             pencere=("#0a1228", "#cfd8e8"), zemin_renk=("#4a4440", "#3e3834", "#322e2c"), isik="#e8b060",
             hali=False)
    yk = 3.0
    s = s_oturan(yk)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, zincir=_kz(yk))
        kitaplar(t, 118, z[0], 4.2)
        figur(t, oturan, 178, z, s, **KATIP, yon=1, el="kalem", minder="#5a2a4a")
        rahle(t, 232, z[0], 3.6)
        kitaplar(t, 284, z[0], 4.2)

    _spr(428, 400, 300, kare, yk)


def sahne429():
    """'Takiyüddin yıldızı Osmanlı'nın zaferine yoruyor' (anlatıya göre): gece, saray odası; Takiyüddin eliyle
    gökyüzünü gösterir, III. Murad sedirde dinler; pencerelerde yıldızlar."""
    _saray(429, pencere=("#0a1228", "#cfd8e8"))
    yk = 2.8
    K = s_kisi(yk)
    so = s_oturan(yk, 0.26)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 210, 0, f, zincir=_kz(yk))
        ust = figur(t, sedir, 262, z, round(0.75 * so, 1), renk="#7a4a2a", ortu="#8a1e22")
        figur(t, oturan, 262, duz(ust, t.width), so, **MURAD, yon=-1, minder="#c8a040")
        figur(t, kisi, 160, z, K, **TAKI, yon=1, kol=0.85 + 0.08 * SIN(f))

    _spr(429, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 430 (kart 28): Ağustos 1578, Çıldır: ordu doğuya (sağa) yürür.
# --------------------------------------------------------------------------
def sahne430():
    """Ağustos 1578, Çıldır yolunda: yaz öğleden sonrası, yüksek yayla; kızıl kaftanlı atlı ve börklü yaya asker sağa
    (doğuya) yürür, toynakların dibinden toz kalkar."""
    _gok(430, ["#6a8ab8", "#8aa2c4", "#a8b8cc", "#c8c8c8", "#dcd0b8", "#e8d8b0"])
    uzak(430, ["#8a8aa0", "#7a7a94"], ["#9a9488", "#8e887c"], ["#b8a070", "#a89464", "#98885a"],
         dag_y=(450, 494), tepe_y=500, ova_y=512)
    orta(430, (536, 548), ["#b89a60", "#a88c56", "#987e4c", "#887044", "#78623a"], "#e0c888")
    on(430, ["#78623a", "#887044", "#987e4c"], "#e0c888", boy=120)
    yk = 2.6
    K = s_kisi(yk, 0.30)
    sa = s_atli(yk)

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 12, t.width)
        figur(t, kisi, 120, arka, round(0.85 * K, 1), govde="#3a5a8a", bas="bork", bas_renk="#f4f0e6", sakal="#3a2a1a",
              yon=1, adim=(f + 0.3) % 1, silah="kalkan")
        figur(t, atli, 205, z, sa, 1, faz=f, at_renk="#6b3f24", yele="#2b1a12", govde="#8a1e22", bas="sarik",
              bas_renk="#f4f0e6", sakal="#2a1a12", silah="kilic", adim=0.45)    # mızrak/sancak yok: yazı bandına girmesin
        figur(t, kisi, 286, z, K, govde="#3a5a8a", bas="bork", bas_renk="#f4f0e6", sakal="#3a2a1a", yon=1,
              adim=(f + 0.6) % 1)
        _toz(t, 168, 299, f, 22, 430, genislik=1.2, renk="#c8b48a")

    _spr(430, 400, 300, kare, yk, esik=0.7)


# --------------------------------------------------------------------------
# 431 (kart 29): veba: yaslılar örtülü tabutun yanında; biri tepedeki rasathaneyi gösterir.
# --------------------------------------------------------------------------
def sahne431():
    """'Sonra İstanbul'a veba geliyor. Parmaklar rasathaneyi gösteriyor.': soğuk akşam; yeşil örtülü tabutun başında
    iki yaslı; biri eliyle sağ gerideki terastaki rasathaneyi gösterir."""
    _gok(431, ["#1a1e30", "#2a2e44", "#3e3e56", "#54506a", "#6a6070", "#7e7076"])
    uzak(431, ["#3a3a54", "#32324a"], ["#42405a", "#3a3850"], ["#2e3a54", "#2a344c", "#242e44"],
         dag_y=(476, 500), tepe_y=504, ova_y=514)
    yk = 2.6
    K = s_kisi(yk, 0.30)
    _gorunur(431, [306, 358], 270, 270, yk)
    orta(431, (540, 552), ["#3e4038", "#363830", "#2e302a", "#262822", "#1e201c"], "#6a6a5a",
         ekle=_rasathane_orta(332, 1.3, teras_h=8, genis=(40, 38)))
    on(431, ["#1e201c", "#262822", "#2e302a"], "#6a6a5a", boy=120)

    def kare(t, z, i):
        f = i / KARE
        figur(t, ortulu_tabut, 160, z, 3.6)
        figur(t, kisi, 112, z, K, govde="#2a2a32", bas="ortu", bas_renk="#3a3440", sakal=None, yon=1, kadin=True,
              kol=0.02 * (1 + SIN(f)))
        figur(t, kisi, 230, z, K, govde="#3a3a2a", bas="sarik", bas_renk="#d8d4c8", sakal="#5a4a3a", yon=1,
              kol=0.72 + 0.04 * SIN(f))

    _spr(431, 400, 300, kare, yk, esik=0.75)


# --------------------------------------------------------------------------
# 432 (kart 30): Şeyhülislam karşı çıkar.
# --------------------------------------------------------------------------
def sahne432():
    """'Şeyhülislam Kadızâde Ahmed Efendi karşı çıkıyor' (anlatıya göre): koyu yeşil çinili oda; ak sakallı
    şeyhülislam ayakta elini kaldırır; yerde kitaplar, mum."""
    ic_mekan(432, duvar=("#24302a", "#2e3c34", "#3a4a40"), kemer="#16201a", cini="#3a7a5a",
             zemin_renk=("#4a4a3e", "#3e3e34", "#32322a"), isik="#e8c070", hali=True)
    yk = 3.0
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 270, 0, f, zincir=_kz(yk))
        mumluk(t, 122, z, f, 2)
        figur(t, kisi, 200, z, K, **SEYHULISLAM, yon=-1, kol=0.62 + 0.06 * SIN(f), pelerin="#e8e2d4")
        kitaplar(t, 268, z[0], 4.2)

    _spr(432, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 433 (kart 31): Ocak 1580: Kaptan-ı Derya Kılıç Ali Paşa kıyıda; arkada donanmanın kadırgaları.
# --------------------------------------------------------------------------
H_DENIZ = 300
SU_Y = H_DENIZ - 16


def _gemi_denetimi(s, su, w, h):
    """Gövde su çizgisine ulaşmalı (havada gemi olmaz)."""
    for f in (0.0, 0.25, 0.5, 0.75):
        g = yeni(w, h)
        figur(g, gemi, w // 2, su, s, 1, f)
        if _bb(g)[3] < su:
            raise RuntimeError(f"Gemi suya ulaşmıyor: alt={_bb(g)[3]}, su_y={su}")


def sahne433():
    """Ocak 1580, kış alacakaranlığı: Kaptan-ı Derya Kılıç Ali Paşa kıyıdaki taş rıhtımda, elinde kılıç; arkasında
    koyda donanmanın iki kadırgası su çizgisine oturur."""
    _gok(433, KIS)
    uzak(433, KIS_DAG, KIS_TEPE, KIS_DENIZ, dag_y=(470, 498), tepe_y=504, ova_y=514)

    def ekle(img, z):
        su_ve_kiyi(img, 560, renkler=("#3c4864", "#34405a", "#2c3850", "#243046"))
        for x, s_ in ((PAY + 220, 1.9), (PAY + 330, 1.6)):
            figur(img, gemi, x, 572, s_, -1, 0.0, govde="#3a2a22", yelken="#e8dcc0", hac=False)
        img_d = ImageDraw.Draw(img)
        img_d.rectangle([0, 600, img.width, img.height], fill=hex2("#5a5448"))           # rıhtım (düz taş)
        for xx in range(0, img.width, 14):
            img_d.line([xx, 600, xx, 610], fill=hex2("#46403a"))
        img_d.line([0, 600, img.width, 600], fill=hex2("#8a8270"))

    orta(433, (536, 548), KIS_ORTA, "#8a8a70", ekle=ekle)
    on(433, ["#3a362e", "#46403a", "#504a40"], "#8a8270", boy=100)
    yk = 2.8
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 200, z, K, **KILIC_ALI, yon=1, silah="kilic", kol=0.3 + 0.03 * SIN(f), pelerin="#1e2a4a")

    _spr(433, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 434 (kart 32): İnebahtı, 1571: kızıl dumanlar arasından kadırgalar kaçar.
# --------------------------------------------------------------------------
def sahne434():
    """İnebahtı, 1571: kızıl gün batımı; ufukta savaş dumanları yükselir; Kılıç Ali'nin kadırgası öne, sağa
    (kurtuluşa) yol alır."""
    _gok(434, ["#2a1a2e", "#5a2a3a", "#9a3a3a", "#c85a3a", "#e0824a", "#eca060"])
    img = uzak(434, ["#4a2a3a", "#40243a"], ["#5a3040", "#4e2a38"], ["#5a3a4a", "#4e3242", "#422a3a"],
               dag_y=(486, 508), tepe_y=512, ova_y=520)
    for x, b in ((120, 70), (210, 50), (430, 64)):                     # ufuktaki yanan gemilerden yükselen duman
        figur(img, gemi, x, 528, 0.8, 1, 0.0, govde="#2a1a1a", yelken="#3a2a2a", hac=False)
        duman(img, x, 516, b, x, faz=0.3, renk="#3a2a2e", ruzgar=0.3, genislik=1.6)
    kaydet(img, "sahne434-uzak.png")
    orta(434, (552, 556), ["#4a3048", "#422a40", "#3a2438", "#321e30", "#2a1a28"], "#a06a6a",
         ekle=lambda img, z: su_ve_kiyi(img, 552, renkler=("#5a3a4a", "#4e3242", "#422a3a", "#36222e")))
    on(434, ["#2a1a28", "#321e30", "#3a2438"], "#a06a6a", boy=40)
    yk = 2.4
    sg = 3.6
    _gemi_denetimi(sg, SU_Y, 400, H_DENIZ)

    def kare(t, z, i):
        f = i / KARE
        figur(t, gemi, 200, SU_Y, sg, 1, f, govde="#3a2a22", yelken="#c8b898", hac=False)
        su_ve_kiyi(t, SU_Y, renkler=("#5a3a4a", "#4e3242", "#422a3a", "#36222e"))

    _spr(434, 400, H_DENIZ, kare, yk, esik=0.4)


# --------------------------------------------------------------------------
# 435 (kart 33): Kılıç Ali Paşa yıkımı yönetir; top ateşler, rasathane daha çok yıkılmış, toz kalkar.
# --------------------------------------------------------------------------
def sahne435():
    """'Şimdi bir gözlemevini yıkıyor' (anlatıya göre): Kılıç Ali Paşa kılıcıyla binayı gösterir, önündeki top ateşler;
    sağ gerideki rasathane büyük ölçüde yıkık, molozdan toz kalkar."""
    _gok(435, KIS)
    uzak(435, KIS_DAG, KIS_TEPE, KIS_DENIZ, dag_y=(436, 470), tepe_y=478, ova_y=494)
    yk = 2.6
    K = s_kisi(yk, 0.30)
    _gorunur(435, [272, 356], 270, 270, yk)
    orta(435, (540, 552), KIS_ORTA, "#8a8a70", ekle=_rasathane_orta(314, 1.9, yikik=0.65))
    on(435, [KIS_ORTA[-1], KIS_ORTA[-2], KIS_ORTA[-3]], "#8a8a70", boy=120)
    st = round(0.72 * K, 1)

    def kare(t, z, i):
        f = i / KARE
        for j, mx in enumerate((198, 248, 288)):
            _toz(t, mx, 246, (f + j * 0.33) % 1, 60, 435 + j, genislik=2.2)
        figur(t, kisi, 130, z, K, **KILIC_ALI, yon=1, silah="kilic", kol=0.55 + 0.05 * SIN(f), pelerin="#1e2a4a")
        ates = max(0.0, 1 - (f - 0.5) / 0.12) if 0.5 <= f < 0.62 else 0.0
        mx, my = figur(t, top_, 200, z, st, 1, ates=ates)
        duman(t, mx + 4, my, 44, 9, faz=(f + 0.5) % 1, renk="#d8d0c8", ruzgar=0.45, genislik=1.2)

    _spr(435, 400, 300, kare, yk, esik=0.7)


# --------------------------------------------------------------------------
# 436 (kart 34): Tophane-i Âmire: top döküm ocağı, bacalardan duman; önde yeni dökülmüş namlular.
# --------------------------------------------------------------------------
def sahne436():
    """'Semtin adı zaten top döküm ocağından geliyor: Tophane.': akşam; kurşun kubbeli döküm ocağı, ocak ağızları
    kızıl, iki bacadan duman yukarı çıkar. İnsan yok."""
    _gok(436, ["#2a2440", "#4a3a5a", "#7a4a5a", "#a85a50", "#c87a58", "#d8986a"])
    uzak(436, ["#4a3a5a", "#403250"], ["#54406a", "#4a3860"], ["#3a4a6a", "#344264", "#2e3a5a"],
         dag_y=(486, 510), tepe_y=514, ova_y=524)
    orta(436, (556, 562), ["#5a4a3e", "#4e4036", "#42362e", "#382e26", "#2e261e"], "#9a7a5a")
    on(436, ["#2e261e", "#382e26", "#42362e"], "#9a7a5a", boy=100)
    yk = 2.2

    def kare(t, z, i):
        f = i / KARE
        bacalar = figur(t, dokumhane, 200, z, 2.9)
        for j, (bx, by) in enumerate(bacalar):
            duman(t, bx, by, 60, 436 + j, faz=(f + j * 0.5) % 1, renk="#8a8088", ruzgar=0.3, genislik=1.3)

    _spr(436, 400, 300, kare, yk, esik=0.8)


# --------------------------------------------------------------------------
# 437 (kart 35): Mimar Sinan elinde planla; arkada Kılıç Ali Paşa Camii (bugün ayakta).
# --------------------------------------------------------------------------
def sahne437():
    """Tophane: altın saat; Mimar Sinan elinde planla durur; arkada düz zeminde Kılıç Ali Paşa Camii, tek minareli."""
    _gok(437, ALTIN_SAAT)
    uzak(437, ["#8a6a8a", "#7e5e7e"], ["#9a7a8a", "#8e6e7e"], ["#5a7a9a", "#527090", "#4a6686"],
         dag_y=(476, 500), tepe_y=504, ova_y=514)
    yk = 2.8
    K = s_kisi(yk)
    _gorunur(437, [262, 330], 270, 270, yk)
    orta(437, (540, 552), ["#a89a70", "#9a8c64", "#8c7e58", "#7e704e", "#706244"], "#e0d0a0",
         ekle=lambda img, z: figur(img, osmanli_camii, PAY + 284, duz(588), 1.35))
    on(437, ["#706244", "#7e704e", "#8c7e58"], "#e0d0a0", boy=120)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 170, z, K, **SINAN, yon=1, silah="mektup", kol=0.3 + 0.03 * SIN(f))

    _spr(437, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 438 (kart 36): yer bilinmiyor: boş sırt, dağınık taşlar, rüzgârda çimen.
# --------------------------------------------------------------------------
def sahne438():
    """'Rasathanenin kesin yeri bile bilinmiyor': soluk akşam, boş tepe; otların arasında dağınık taşlar. Bina yok."""
    _gok(438, ["#3a4060", "#5a5a78", "#7a7088", "#9a8890", "#b8a098", "#c8b0a0"])
    uzak(438, ["#5a5a78", "#50506e"], ["#62627a", "#585870"], ["#4a5a7a", "#42526e", "#3a4a64"],
         dag_y=(486, 510), tepe_y=514, ova_y=524)
    orta(438, (556, 562), ["#5a6a48", "#4e5e40", "#445438", "#3a4a30", "#304028"], "#9aaa78")
    on(438, ["#304028", "#3a4a30", "#445438"], "#9aaa78", boy=120)
    yk = 2.4

    def kare(t, z, i):
        f = i / KARE
        for x, s_ in ((140, 2.2), (215, 1.6), (262, 2.6)):
            figur(t, taslar, x, z, s_)
        _cimen(t, z, f, ["#7a8a5a", "#6a7a4e", "#8a9a66"], 438, 70, 330, boy=12)

    _spr(438, 400, 300, kare, yk, esik=0.85)


# --------------------------------------------------------------------------
# 439 (kart 37-38): 11 Ekim 1579: Sokollu divanda; dilekçeli bir derviş önünde diz çöker (suikastın öncesi).
# --------------------------------------------------------------------------
def _divan(no):
    ic_mekan(no, duvar=("#3a2a2a", "#4a3634", "#5a4440"), kemer="#2a1a1a", cini="#8a2a2a",
             pencere=("#2a3a5a", "#f4d8a0"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"), isik="#f8c060", hali=True)


def sahne439():
    """11 Ekim 1579: divan odası, akşam; sadrazam Sokollu Mehmed Paşa sedirde oturur; önünde elinde dilekçeyle diz
    çökmüş bir derviş. Ölüm anı gösterilmez."""
    _divan(439)
    yk = 2.8
    K = s_kisi(yk)
    so = s_oturan(yk, 0.26)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 205, 0, f, zincir=_kz(yk))
        ust = figur(t, sedir, 262, z, round(0.75 * so, 1), renk="#7a4a2a", ortu="#2a6a3a")
        figur(t, oturan, 262, duz(ust, t.width), so, **SOKOLLU, yon=-1, minder="#c8a040")
        figur(t, kisi, 160, z, K, govde="#5a4a32", bas="bork", bas_renk="#7a6448", sakal="#3a2a1a", yon=1, diz=True,
              silah="mektup", kol=0.3 + 0.03 * SIN(f))
        mumluk(t, 112, z, f, 3)

    _spr(439, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 440 (kart 39): rasathane yıkılıyor (büyük plan): kule kırık, kubbe yok, molozdan toz kalkar.
# --------------------------------------------------------------------------
def sahne440():
    """'Üç ay sonra rasathane yıkılıyor': Ocak 1580, gri gün; terastaki rasathane büyük plan, kubbesi düşmüş, kule
    kırık; molozdan toz yükselir. İnsan yok."""
    _gok(440, KIS)
    uzak(440, KIS_DAG, KIS_TEPE, KIS_DENIZ, dag_y=(486, 510), tepe_y=514, ova_y=524)
    orta(440, (556, 562), KIS_ORTA, "#8a8a70")
    on(440, [KIS_ORTA[-1], KIS_ORTA[-2], KIS_ORTA[-3]], "#8a8a70", boy=100)
    yk = 2.2

    def kare(t, z, i):
        f = i / KARE
        ust = figur(t, teras, 92, 318, z, 16)
        _, _, molozlar = figur(t, rasathane, 205, duz(ust, t.width), 3.4, yikik=0.7)
        for j, (mx, my) in enumerate(molozlar):
            _toz(t, mx, ust, (f + j * 0.33) % 1, 70, 440 + j, genislik=2.4)

    _spr(440, 400, 300, kare, yk, esik=0.8)


# --------------------------------------------------------------------------
# 441 (kart 40): boş koltuk: divanda boş sedir, kandil.
# --------------------------------------------------------------------------
def sahne441():
    """'Bağ mı, tesadüf mü? Belgesi yok.': aynı divan odası, gece; sadrazamın sediri boş, minder dokunulmamış."""
    _divan(441)
    yk = 2.8

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 205, 0, f, zincir=_kz(yk))
        figur(t, bos_sedir, 225, z, 4.6, ortu="#2a6a3a")
        mumluk(t, 128, z, f, 1)

    _spr(441, 400, 300, kare, yk, esik=0.7)


# --------------------------------------------------------------------------
# 442 (kart 41): yaşlı Takiyüddin gece odasında yalnız; yanında masa saati.
# --------------------------------------------------------------------------
def sahne442():
    """'Takiyüddin beş yıl daha yaşıyor. 1585'te İstanbul'da ölüyor.': gece, sade oda; ak sakallı Takiyüddin
    minderde yalnız oturur; yanında mekanik saati, tek mum."""
    ic_mekan(442, duvar=("#1e1e28", "#282834", "#34323e"), kemer="#12121a", cini="#2a3a5a",
             pencere=("#0a1228", "#cfd8e8"), zemin_renk=("#3e3a40", "#34303a", "#2a2630"), isik="#d8a860", hali=True)
    yk = 3.2
    s = s_oturan(yk, 0.30)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 128, z, f, 1)
        figur(t, oturan, 198, z, s, **TAKI_YASLI, yon=1, minder="#4a3a5a")
        figur(t, masa_saati, 262, z, 3.8, f=f)

    _spr(442, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 443 (kart 42): makam sürer: yeni müneccimbaşı damda halkalı küreyle gökyüzüne bakar.
# --------------------------------------------------------------------------
def sahne443():
    """'Osmanlı'da gökyüzüne bakmak bitmiyor': yıldızlı gece; sonraki müneccimbaşı halkalı kürenin başında eliyle
    gökyüzünü gösterir."""
    _gok(443, GECE, yildiz=240, y0=330, y1=580)
    uzak(443, GECE_DAG, GECE_TEPE, GECE_DENIZ, dag_y=(480, 506), tepe_y=510, ova_y=520)
    _gece_ortasi(443, (548, 556))
    yk = 2.6
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, armilla, 250, z, 3.4, faz=f * 0.5)
        figur(t, kisi, 180, z, K, **MUNECCIM, yon=1, kol=0.7 + 0.05 * SIN(f))

    _spr(443, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 444-445 (kart 43-46): Şehinşâhnâme minyatürü: nakkaş çizer; sonra sayfa yakın plan.
# --------------------------------------------------------------------------
def _nakkashane(no):
    ic_mekan(no, duvar=("#3a3028", "#4a3c32", "#5a4a3c"), kemer="#2a2018", cini="#2a6a8a",
             pencere=("#5a7aa0", "#f4e8c8"), zemin_renk=("#6a5a48", "#5a4c3c", "#4a3e32"), isik="#f8d080", hali=True)


def sahne444():
    """1581 dolayı, nakkaşhane: nakkaş minderde oturup rahledeki Şehinşâhnâme sayfasına rasathane minyatürünü çizer."""
    _nakkashane(444)
    yk = 2.8
    s = s_oturan(yk)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, zincir=_kz(yk))
        figur(t, oturan, 150, z, s, **NAKKAS, yon=1, el="kalem", minder="#8a2a2a")
        figur(t, minyatur_kitap, 248, z, 4.6)

    _spr(444, 400, 300, kare, yk)


def sahne445():
    """'Aletleri bugün en iyi orada görüyoruz': rahledeki açık sayfa yakın plan; minyatürde sarıklı gökbilimciler,
    yay ve küre; yanda mum titrer."""
    _nakkashane(445)
    yk = 2.8

    def kare(t, z, i):
        f = i / KARE
        figur(t, minyatur_kitap, 205, z, 6.2)
        mumluk(t, 112, z, f, 2)

    _spr(445, 400, 300, kare, yk, esik=0.8)


# --------------------------------------------------------------------------
# 446 (kart 47): 1597: Tycho'nun gemisi Hven'den ayrılır; arkada Uraniborg.
# --------------------------------------------------------------------------
def sahne446():
    """1597: soğuk gri gün; Tycho'yu götüren gemi sola (Avrupa'ya) yol alır; arkada adada Uraniborg."""
    _gok(446, ["#5a6478", "#727c8e", "#8a92a0", "#a2a8b2", "#b8bcc2", "#c8cacc"])
    img = uzak(446, ["#6a7488", "#5e687c"], ["#56744a", "#4c6a42"], ["#4a5e74", "#42566a", "#3a4e60"],
               dag_y=(492, 512), tepe_y=520, ova_y=530)
    kaydet(img, "sahne446-uzak.png")
    orta(446, (548, 552), ["#4a5e74", "#42566a", "#3a4e60", "#324656", "#2a3e4c"], "#8aa0b4",
         ekle=lambda img, z: (su_ve_kiyi(img, 552, renkler=("#4a5e74", "#42566a", "#3a4e60", "#324656")),
                              figur(img, uraniborg, PAY + 300, duz(552), 1.0)))
    on(446, ["#2a3e4c", "#324656", "#3a4e60"], "#8aa0b4", boy=40)
    yk = 2.4
    sg = 3.4
    _gemi_denetimi(sg, SU_Y, 400, H_DENIZ)

    def kare(t, z, i):
        f = i / KARE
        figur(t, gemi, 200, SU_Y, sg, -1, f, govde="#3a2a22", yelken="#e8e4d8", hac=False)
        su_ve_kiyi(t, SU_Y, renkler=("#4a5e74", "#42566a", "#3a4e60", "#324656"))

    _spr(446, 400, H_DENIZ, kare, yk, esik=0.4)


# --------------------------------------------------------------------------
# 447 (kart 48): Uraniborg bakımsız, yıkık; otlar sarmış.
# --------------------------------------------------------------------------
def sahne447():
    """'Uraniborg bakımsız kalıyor, zamanla yıkılıyor': kapalı gri gün; kubbeleri düşmüş, duvarları kırık Uraniborg,
    dibinde tuğla molozu, uzun otlar rüzgârda."""
    _gok(447, ["#4a5466", "#5e687a", "#727a8a", "#868c98", "#9aa0a8", "#aab0b4"])
    uzak(447, ["#5a6476", "#4e586a"], ["#5a6a5a", "#4e5e4e"], ["#4a5a6a", "#42525e", "#3a4a54"],
         dag_y=(486, 510), tepe_y=514, ova_y=524)
    orta(447, (556, 562), ["#4a6a40", "#406036", "#36562e", "#2e4c28", "#264222"], "#8aa070")
    on(447, ["#264222", "#2e4c28", "#36562e"], "#8aa070", boy=120)
    yk = 2.2

    def kare(t, z, i):
        f = i / KARE
        figur(t, uraniborg, 200, z, 3.0, yikik=0.65)
        _cimen(t, z, f, ["#6a8a52", "#5a7a46", "#7a9a5e"], 447, 60, 340, boy=12)

    _spr(447, 400, 300, kare, yk, esik=0.85)


def sahne448():
    """'Aynı gökyüzü, iki gözlemevi. İkisi de yok.': aynı yıldızlı gök altında iki yıkıntı yan yana; uzun otlar."""
    _iki_gozlemevi(448, (0.75, 0.85))


# --------------------------------------------------------------------------
# 449 (kart 51): soru: gece, Tophane sırtında terasın üstünde moloz; gökte kuyruklu yıldız.
# --------------------------------------------------------------------------
def sahne449():
    """Son soru: gece, Tophane sırtı; boş terasın üstünde moloz yığınları; gökte 1577'nin kuyruklu yıldızı
    (dört olası sebebin ilki gökte asılı kalır)."""
    _gok(449, GECE, yildiz=260, y0=320, y1=590, kuyruk=(150, 534, 56, -2.6))
    uzak(449, GECE_DAG, GECE_TEPE, GECE_DENIZ, **ALCAK_UZAK)
    _gece_ortasi(449, (598, 604))
    yk = 2.0

    def kare(t, z, i):
        f = i / KARE
        ust = figur(t, teras, 170, 330, z, 12)
        figur(t, rasathane, 254, duz(ust, t.width), 2.4, yikik=0.95)
        _cimen(t, z, f, ["#3a4a5a", "#2e3e4e", "#4a5a6a"], 449, 60, 340, boy=8)

    _spr(449, 400, 300, kare, yk, esik=0.85)


SAHNELER = {n: globals()[f"sahne{n}"] for n in range(410, 450)}

if __name__ == "__main__":
    for n in ([int(a) for a in sys.argv[1:]] or sorted(SAHNELER)):
        SAHNELER[n]()
        print(f"sahne {n} tamam")
