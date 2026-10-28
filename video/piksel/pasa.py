"""Paşa ve darağacı sahnesi (sahne 71): 64-bit piksel sanatı, skills/piksel-sahne şablonuyla yazıldı.

Sahne 71 — Alacakaranlık, kale önü meydan: ortada darağacı, üç asılmış adam iplerde hafifçe salınır; sağ önde
Paşa (büyük ölçek) onlara bakıp kahkaha atar: başı geriye düşer, ağzı açılır, eli darağacını gösterir, karnı
sarsılır. İki yanında mızraklı muhafız; gökte dönen kargalar. Kan yok; asılanlar silüet gibi koyu.

Yeni figürler: daragaci (kütüphanede yoktu), pasa_kahkaha (kisi üstüne geriye atılmış baş + açık ağız).
Kullanım: python3 -I video/piksel/pasa.py [--onizleme klasör]
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import ImageDraw  # noqa: E402

from ciz import KOYU, _ac, figur, hex2, piksel, temas_golgesi, zemin_y  # noqa: E402
from sahneler import GW, KARE, PAY, duz, gokyuzu, on, onizleme, orta, sprite, uzak  # noqa: E402
from timur_figur import TEN, _u, anadolu_kalesi, kisi  # noqa: E402


# ---------------------------------------------------------------- yeni figürler


def daragaci(img, x, zemin, s=1.0, adamlar=(), f=0.0, ip=4.0):
    """Darağacı: iki kalın direk zemine dikili, üstte kiriş, kirişten sarkan iplerde asılmış adamlar.
    adamlar: (yerel_x_orani -1..1, govde_rengi, yon) listesi. Asılanların ayakları yerden kesilir (ipte sallanır);
    salınım f ile. Direkler düz zemine basar, dipleri toprakla desteklidir."""
    d = ImageDraw.Draw(img)
    yarim = int(14 * s)
    y = zemin_y(zemin, x, yarim * 2)
    ust = y - int(36 * s)
    kalin = _u(1.8, s)
    ahsap, koyu = hex2("#5a3a1e"), hex2("#3a2410")
    for dx in (-yarim, yarim):  # direkler (düz zemine basar)
        d.rectangle([x + dx - kalin, ust, x + dx + kalin, y - 1], fill=ahsap)
        d.line([x + dx - kalin, ust, x + dx - kalin, y - 1], fill=koyu)
        d.polygon([(x + dx - int(4 * s), y - 1), (x + dx, y - int(2.5 * s)), (x + dx + int(4 * s), y - 1)], fill=hex2("#4a3620"))  # toprak destek
        temas_golgesi(img, x + dx, y, 8 * s)
    d.rectangle([x - yarim - int(3 * s), ust - kalin, x + yarim + int(3 * s), ust + kalin], fill=ahsap)  # kiriş
    d.line([x - yarim - int(3 * s), ust - kalin, x + yarim + int(3 * s), ust - kalin], fill=hex2("#7a5a34"))
    for dx in (-yarim, yarim):  # köşe payandaları: direkten kirişin iç tarafına
        ic = -1 if dx < 0 else 1
        d.line([x + dx, ust + int(8 * s), x + dx - ic * int(6 * s), ust + kalin], fill=koyu, width=_u(1, s))
    for k, (oran, govde, yon) in enumerate(adamlar):
        ax = x + int(oran * (yarim - int(2 * s)))
        sal = math.sin(f * 2 * math.pi + k * 1.9) * 1.2 * s  # ipte hafif salınım
        asili(img, ax, ust + kalin, s * 0.85, govde, yon, sal, ip)
    return ust


def asili(img, x, kiris_y, s=1.0, govde="#3a3a3a", yon=1, sal=0.0, ip=4.0):
    """İpte asılı adam: ip kirişten boyna iner, baş yana düşmüş, kollar iki yanda sarkık, bacaklar bitişik ve
    gevşek, ayaklar yerden kesik (zemine basmaz, gölgesi yok). sal: salınım (piksel)."""
    d = ImageDraw.Draw(img)
    gv, koyu = hex2(govde), hex2(_ac(govde, -0.3))
    ip_alt = kiris_y + int(ip * s)
    bx = x + sal
    d.line([x, kiris_y, bx, ip_alt], fill=hex2("#c8b890"), width=_u(0.7, s))
    r = max(2, int(1.7 * s))
    bas_y = ip_alt + r  # ilmik boyunda: baş ipin ucunda, yana düşmüş
    hx = bx + int(0.9 * s) * yon
    d.ellipse([hx - r, bas_y - r, hx + r, bas_y + r], fill=hex2(_ac(TEN, -0.3)))
    d.ellipse([bx - r - 1, ip_alt - 1, bx + r + 1, ip_alt + 2], outline=hex2("#c8b890"))  # ilmik
    piksel(img, hx + yon * (r - 1), bas_y, hex2(KOYU))
    boyun = bas_y + r
    ust, alt = boyun, boyun + int(7 * s)
    d.polygon([(bx - int(2 * s), ust), (bx + int(2 * s), ust), (bx + int(2.4 * s), alt), (bx - int(2.4 * s), alt)], fill=gv)
    for dx in (-1, 1):  # kollar sarkık
        d.line([bx + dx * int(2 * s), ust + int(1 * s), bx + dx * int(2.6 * s), alt + int(2 * s)], fill=koyu, width=_u(1, s))
        piksel(img, bx + dx * int(2.6 * s), alt + int(2 * s) + 1, hex2(_ac(TEN, -0.3)))
    for dx in (-0.7, 0.7):  # bacaklar bitişik, gevşek
        d.line([bx + int(dx * s), alt, bx + int(dx * s) + int(0.4 * s) * yon, alt + int(6 * s)], fill=hex2("#2a2420"), width=_u(1.3, s))
        d.line([bx + int(dx * s) + int(0.4 * s) * yon, alt + int(6 * s), bx + int(dx * s) + int(1.2 * s) * yon, alt + int(6 * s) + 1], fill=hex2(KOYU))
    return alt + int(6 * s)


def pasa_kahkaha(img, x, zemin, s=1.0, yon=-1, f=0.0, kaftan="#8a1e22", kurk="#e8e0d0", sakal="#2a1a12"):
    """Kahkaha atan Paşa: kisi gövdesi üstüne geriye düşmüş baş, kapalı gözler, açık ağız; kol darağacını gösterir,
    gövde kahkahayla sarsılır (f ile kol ve baş titrer). Ayakları zemine basar."""
    d = ImageDraw.Draw(img)
    sars = math.sin(f * 2 * math.pi * 3)  # saniyede ~3 sarsıntı
    kol = 0.55 + 0.12 * sars
    kisi(img, x, zemin, s, kaftan, None, "#c8302a", None, yon=yon, kol=kol, kemer="#e0b040")
    y = zemin_y(zemin, x, 6 * s)
    # eski küçük başın üstünü kaftan yakasıyla kapat, geriye atılmış büyük baş çiz
    bas_y0 = y - int(13.6 * s)
    r0 = max(2, int(1.7 * s))
    d.rectangle([x - r0 - 1, bas_y0 - r0 - int(4 * s), x + r0 + 1, bas_y0 + r0 + 1], fill=hex2(kaftan))
    d.polygon([(x - int(2.6 * s), bas_y0 + r0 + 1), (x, bas_y0 + r0 - int(1.5 * s)), (x + int(2.6 * s), bas_y0 + r0 + 1)], fill=hex2(kurk))  # kürk yaka
    bx = x - int(1.2 * s) * yon  # baş geriye (bakış yönünün tersine) düşer
    by = bas_y0 - int(0.8 * s) + int(0.4 * s * sars)
    r = max(3, int(2.0 * s))
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=hex2(TEN))
    # sarık: büyük beyaz kavuk, geriye yatık
    d.ellipse([bx - r - _u(1.8, s), by - r - _u(3.6, s), bx + r + _u(1.8, s), by - r + _u(0.3, s)], fill=hex2("#f4f0e6"))
    d.line([bx - r, by - r - _u(1.4, s), bx + r, by - r - _u(2.4, s)], fill=hex2("#d8d0c0"))
    d.rectangle([bx - _u(0.7, s), by - r - _u(4.8, s), bx + _u(0.7, s), by - r - _u(3.4, s)], fill=hex2("#c8302a"))
    # kapalı (kısılmış) göz: yukarı kavisli çizgi; açık ağız: koyu oval, içinde dişler
    gx = bx + int(0.9 * s) * yon
    d.arc([gx - _u(1, s), by - _u(0.6, s), gx + _u(1, s), by + _u(0.6, s)], 200, 340, fill=hex2(KOYU), width=_u(0.5, s))
    ag_w, ag_h = _u(1.4, s), _u(1.2, s) + int(0.3 * s * (1 + sars))
    ax, ay = bx + int(0.6 * s) * yon, by + int(1.4 * s)
    d.ellipse([ax - ag_w, ay - ag_h, ax + ag_w, ay + ag_h], fill=hex2("#3a0e10"))
    d.line([ax - ag_w + 1, ay - ag_h + 1, ax + ag_w - 1, ay - ag_h + 1], fill=hex2("#f4f0e6"))
    # sakal ağzın altında, geriye atılmış başla birlikte öne çıkar
    d.polygon([(bx - r + _u(0.4, s), ay + _u(0.6, s)), (bx + r, ay + _u(0.6, s)), (bx + int(0.8 * s) * yon, ay + r + _u(2.5, s))], fill=hex2(sakal))
    return (bx, by)


# ---------------------------------------------------------------- sahne


def sahne71():
    """Alacakaranlık meydan: darağacında üç adam, sağ önde kahkaha atan Paşa, iki muhafız, dönen kargalar, arkada kale."""
    gk = gokyuzu(71, ["#2a1a30", "#5a2a3a", "#9a3a2e", "#c8602a", "#e89a48", "#f0c070"], (140, 330, 22, ["#ffd890", "#f08040"]),
            [(400, 300, 34), (120, 350, 26)], ("#e8a888", "#b86a60", "#6a3a48"), yildiz=20)
    uz = uzak(71, ["#3a2a3a", "#302232"], ["#4a3a3a", "#3e3030"], ["#5a4a3a", "#4e4030", "#423628"], dag_y=(330, 420))

    def kale(img, z):
        figur(img, anadolu_kalesi, PAY + 40, PAY + 420, duz(588), 1.6, tas="#6a5a4e", golge="#443a32")

    ort = orta(71, (526, 560), ["#6a5a3a", "#5a4c32", "#4a3e2a", "#3e3424", "#322a1e"], "#9a8a5a", ekle=kale)
    onp = on(71, ["#322a1e", "#4a3e2a", "#5a4a2a"], "#c8a860", boy=180)

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        y = z[0]
        # darağacı sahnenin ortasında, biraz geride (daha küçük ölçek, aynı zemin satırında ama paşadan uzak)
        kiris = figur(t, daragaci, 150, duz(y - 10, len(z)), 2.3, adamlar=((-0.7, "#3a3a3a", 1), (0.0, "#4a3a2a", -1), (0.7, "#2a2a3a", 1)), f=f)
        # kargalar kirişin üstünde daire çizer
        for j in range(5):
            a = f * 2 * math.pi + j * 1.25
            cx, cy = 150 + math.cos(a) * (40 + j * 6), kiris - 30 - math.sin(a * 0.5) * 10 - j * 4
            kanat = 2 if (i + j) % 6 < 3 else -1
            d.line([cx - 4, cy - kanat, cx, cy, cx + 4, cy - kanat], fill=hex2("#120806"), width=2)
        # muhafızlar: paşanın iki yanında, mızraklı, darağacına dönük
        figur(t, kisi, 262, z, 3.0, "#3a4a6a", "migfer", "#8a8a90", "#2a1a12", yon=-1, silah="mizrak")
        figur(t, kisi, 352, z, 3.0, "#3a4a6a", "migfer", "#8a8a90", "#2a1a12", yon=-1, silah="mizrak")
        # Paşa: en önde ve en büyük, sola (darağacına) bakar, eli darağacını gösterir, kahkaha
        figur(t, pasa_kahkaha, 308, z, 3.3, yon=-1, f=f)
        # kahkaha sarsıntısı: paşanın ayak dibinde toz değil, kaftan kenarında titreyen ışık pikselleri (meşale yansıması)
        rnd = random.Random(i // 3)
        for _ in range(4):
            piksel(t, 296 + rnd.randint(0, 24), y - rnd.randint(6, 30), hex2("#ffd890", 90))

    sp = sprite(71, "karakter", 420, 150, KARE, kare)
    onizleme(71, gk, uz, ort, onp, [(sp, 420, 270, 632, "zemin")])
    return sp


if __name__ == "__main__":
    sahne71()
    print("sahne 71 tamam")
