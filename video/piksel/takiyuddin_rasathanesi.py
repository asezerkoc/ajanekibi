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
LEVEND = dict(govde="#a8281e", bas="kalpak", bas_renk="#4a3222", sakal="#3a2a1a")       # donanma topçusu
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
