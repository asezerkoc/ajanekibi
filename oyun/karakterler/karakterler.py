"""Osmanlı Balkanları strateji oyunu: 30 karakterlik kadro (128-bit tarzı piksel sanatı).

Her karakter bir fonksiyondur: Tuval alır, parçalarını ekler. KADRO listesi kart bilgisini taşır.
Kullanım: python3 -I oyun/karakterler/karakterler.py [çıktı_klasörü]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from govde import (TEN, TEN_ACIK, TEN_ESMER, ayna, bacak, bas, biyik, cizme, gomlek_govde, kaftan,  # noqa: E402
                   kol, kurk_yaka, kusak, sac_yanlar, sakal, salvar)
from motor import (CX, C, E, L, P, R, Tuval, birlestir, kart, kivrim, kurk, palet,  # noqa: E402
                   yatay_cizgi, zincir)

ALTIN = "#d8a83a"
DEMIR = "#8a8e98"
CELIK = "#a8b0bc"
AHSAP = "#7a4a2a"
KEMIK = "#efe6d2"
BEYAZ = "#f2ece0"

# küçük desenler: (satırlar, renk, yatay adım, dikey adım)
CINTEMANI = ([".x.x.", "..x..", ".....", "x...x", ".x.x."], ALTIN, 8, 7)
NOKTA = (["x"], ALTIN, 4, 4)
CICEK = ([".x.", "xxx", ".x."], "#c83a30", 7, 7)
CICEK_BEYAZ = ([".x.", "x.x", ".x."], "#f0e0d0", 6, 6)
ISLEME = (["x.x", ".x."], "#c83a30", 4, 3)
CIZGI = (["xxxxxxxx"], ALTIN, 8, 4)
KORDON = (["xxxxxxxxxxxx", "............"], ALTIN, 12, 4)
LEKE = ([".xx.", "x..x", ".xx."], "#3a2414", 7, 6)


# ---------------------------------------------------------------- silahlar ve eşyalar


def tufek(t, x, ust=18, z=49):
    """Fitilli tüfek: dipçik yerde (zemine basar), namlu yukarıda."""
    t.parca(z, AHSAP, [P((x - 3, 128), (x + 2, 128), (x + 3, 166), (x - 4, 166))], golge="silindir")
    t.parca(z, AHSAP, [R(x - 1, 60, x + 1, 128)], golge="silindir")
    t.parca(z + 0.1, "#4a4a52", [R(x - 1, ust, x, 112)], golge="silindir")
    for y in (60, 84, 108):
        t.parca(z + 0.2, ALTIN, [R(x - 2, y, x + 2, y + 1)], golge="duz")
    t.parca(z + 0.2, "#3a3a40", [R(x + 1, 118, x + 4, 123)], golge="duz")


def sopa(t, x, ust, z=49, renk=AHSAP, kalin=3):
    t.parca(z, renk, [L((x, ust), (x, 166), w=kalin)], golge="silindir", doku=yatay_cizgi(11, 0.06))


def mizrak(t, x, ust=4, z=49, flama=None, flama2=None, uc=CELIK):
    sopa(t, x, ust + 12, z)
    t.parca(z + 0.3, uc, [P((x, ust), (x + 3, ust + 9), (x + 1, ust + 14), (x - 1, ust + 14), (x - 3, ust + 9))], golge="kure")
    if flama:
        t.parca(z - 0.2, flama, [P((x + 1, ust + 15), (x + 24, ust + 19), (x + 15, ust + 23), (x + 24, ust + 27), (x + 1, ust + 31))],
                golge="duz", doku=kivrim(5, 0.15, egim=0.5))
        if flama2:
            t.parca(z - 0.1, flama2, [P((x + 1, ust + 22), (x + 18, ust + 23), (x + 1, ust + 26))], golge="duz")


def yatagan(t, x, y, z=50):
    """Kuşağa sokulmuş yatağan: kulaklı kemik kabza yukarıda, kın aşağı."""
    t.parca(z, "#3a2a22", [L((x, y + 2), (x - 3, y + 24), (x - 1, y + 34), w=4)], golge="silindir")
    t.parca(z + 0.2, ALTIN, [L((x - 1, y + 29), (x - 1, y + 34), w=4)], golge="silindir")
    t.parca(z + 0.3, ALTIN, [R(x - 3, y, x + 3, y + 2)], golge="duz")
    t.parca(z + 0.4, KEMIK, [P((x - 2, y - 7), (x + 2, y - 7), (x + 1, y), (x - 1, y))], golge="silindir")
    t.parca(z + 0.4, KEMIK, [P((x - 4, y - 11), (x - 1, y - 7), (x + 1, y - 7), (x + 4, y - 11), (x + 2, y - 6), (x - 2, y - 6))],
            golge="duz")


def kilic(t, x, y, z=46, sag=False, kin="#3a1e1a"):
    """Bele asılı pala: kın kalçadan bacak boyunca dışa doğru iner."""
    yon = 1 if sag else -1
    t.parca(z, kin, [L((x, y), (x + 3 * yon, y + 28), (x + 9 * yon, y + 50), w=4)], golge="silindir")
    for k in (14, 34):
        t.parca(z + 0.1, ALTIN, [L((x + (1 + k / 12) * yon, y + k), (x + (2 + k / 11) * yon, y + k + 2), w=4)], golge="silindir")
    t.parca(z + 0.2, ALTIN, [L((x + 8 * yon, y + 46), (x + 9 * yon, y + 50), w=4)], golge="silindir")
    t.parca(z + 0.3, ALTIN, [R(x - 4, y - 1, x + 4, y + 1)], golge="duz")
    t.parca(z + 0.3, "#2a1a14", [L((x, y - 1), (x - 2 * yon, y - 9), w=3)], golge="silindir")
    t.parca(z + 0.4, ALTIN, [C(x - 2 * yon, y - 10, 1.5)], golge="kure")


def duz_kilic(t, x, ust, alt, z=72):
    """Avrupa düz kılıcı, ucu yerde; şövalye ellerini kabzasına dayar."""
    t.parca(z, CELIK, [P((x - 2, ust + 12), (x + 2, ust + 12), (x + 1, alt - 3), (x, alt), (x - 1, alt - 3))], golge="silindir")
    t.cizgi(x, ust + 13, x, alt - 6, palet(CELIK)[4], z=900)
    t.parca(z + 1, ALTIN, [R(x - 9, ust + 9, x + 9, ust + 11)], golge="yatay")
    t.parca(z + 1, "#4a2a1a", [R(x - 1, ust + 1, x + 1, ust + 9)], golge="silindir")
    t.parca(z + 2, ALTIN, [C(x, ust, 2.5)], golge="kure")


def topuz(t, x, y, z=72, renk=ALTIN, sap=26):
    t.parca(z, "#5a3a22", [L((x, y), (x, y + sap), w=3)], golge="silindir")
    t.parca(z + 1, renk, [C(x, y - 3, 5)], golge="kure", doku=kivrim(2, 0.15))
    t.parca(z + 2, renk, [P((x - 6, y - 3), (x, y - 10), (x + 6, y - 3), (x, y + 3))], golge="kure", isik=0.05)
    t.px(x - 2, y - 5, "#fff4c8")


def barut_kabi(t, x, y, z=47):
    t.parca(z, "#8a6a3a", [E(x - 5, y - 4, x + 5, y + 6)], golge="kure")
    t.parca(z + 0.1, ALTIN, [R(x - 1, y - 7, x + 1, y - 4)], golge="duz")
    t.parca(z + 0.1, ALTIN, [C(x, y + 1, 2)], golge="kure")


def kitap(t, x, y, z=52, renk="#5a2a1e"):
    t.parca(z, renk, [P((x - 9, y - 6), (x + 9, y - 6), (x + 9, y + 6), (x - 9, y + 6))], golge="duz")
    t.parca(z + 0.1, "#efe2c4", [R(x - 8, y + 4, x + 8, y + 6)], golge="yatay")
    t.parca(z + 0.2, ALTIN, [E(x - 3, y - 3, x + 3, y + 2)], golge="kure")


# ---------------------------------------------------------------- başlıklar


def yeniceri_borku(t, z=80, renk=KEMIK, kasiklik=ALTIN, sorguc=None, yatirma=True):
    """Ak börk (üsküf): uzun beyaz keçe külah, alında kaşıklık, arkadan sırta sarkan yatırma."""
    t.parca(z, renk, [P((55, 31), (73, 31), (72, 20), (70, 8), (66, 2), (60, 4), (57, 14), (56, 22))],
            golge="silindir", doku=kivrim(4, 0.07))
    t.parca(z + 1, kasiklik, [P((55, 26), (73, 26), (73, 31), (55, 31))], golge="yatay")
    t.parca(z + 2, kasiklik, [P((62, 9), (66, 9), (66, 27), (62, 27))], golge="silindir")
    t.parca(z + 3, "#c83a30", [E(62, 26, 66, 30)], golge="kure", isik=0.1)
    if yatirma:
        t.parca(10, renk, [P((70, 14), (80, 24), (87, 62), (79, 70), (74, 40))], golge="silindir", isik=-0.15, doku=kivrim(4, 0.08))
    if sorguc:  # çorbacı tüyü: börkün önünden yükselip arkaya dökülür
        t.parca(z + 4, sorguc, [P((62, 10), (58, -4), (54, -16), (60, -10), (60, -24), (66, -12), (72, -22), (70, -6), (80, -12),
                                  (90, -2), (96, 14), (86, 6), (80, 4), (74, 6), (68, 10))],
                golge="silindir", doku=kivrim(2, 0.14))


def kavuk(t, z=80, renk=BEYAZ, tur="yuvarlak", ic="#c83a30", sorguc=None, mucevher=None, iki_sorguc=False):
    """Sarık/kavuk. tur: yuvarlak (örfi), kallavi (uzun, çapraz altın şeritli), sultan (çok büyük)."""
    if tur == "yuvarlak":
        t.parca(z, renk, [E(49, 6, 79, 34)], golge="kure", doku=kivrim(4, 0.12, egim=-0.8))
        t.parca(z + 1, ic, [E(60, 3, 68, 11)], golge="kure")
    elif tur == "kallavi":
        t.parca(z - 1, ic, [P((57, 10), (71, 10), (70, -6), (58, -6))], golge="silindir")
        t.parca(z, renk, [P((50, 32), (78, 32), (80, 16), (75, 2), (53, 2), (48, 16))], golge="silindir", doku=kivrim(3, 0.1))
        t.parca(z + 1, ALTIN, [P((50, 27), (54, 31), (78, 9), (74, 4))], golge="duz")
    elif tur == "sultan":
        t.parca(z, renk, [E(43, 2, 85, 37)], golge="kure", doku=kivrim(4, 0.13, egim=-0.9))
        t.parca(z + 1, ic, [E(57, -6, 71, 8)], golge="kure")
    if sorguc:
        xs = (59, 69) if iki_sorguc else (64,)
        for x in xs:
            t.parca(z + 2, sorguc, [P((x - 1, 12), (x - 6, -12), (x - 2, -26), (x + 1, -12), (x + 4, -28), (x + 5, -12), (x + 1, 12))],
                    golge="silindir", doku=kivrim(2, 0.15))
    if mucevher:
        t.parca(z + 3, ALTIN, [E(59, 10, 69, 22)], golge="kure")
        t.parca(z + 4, mucevher, [E(61, 12, 67, 19)], golge="kure", isik=0.12)
        for x, y in ((59, 24), (64, 25), (69, 24)):
            t.parca(z + 3, "#f0ece4", [C(x, y, 1.2)], golge="kure", isik=0.2)


def kalpak(t, z=80, renk="#3a2a20", boy=14, ust=None, tepe="#a83a2a", doku_tohum=7):
    """Kürk kalpak: silindir gövde; ust verilirse tepesinde kumaş."""
    t.parca(z, renk, [P((53, 32), (75, 32), (76, 30 - boy), (52, 30 - boy))], golge="silindir", doku=kurk(doku_tohum, 0.35))
    if ust:
        t.parca(z + 1, tepe, [P((55, 30 - boy), (73, 30 - boy), (70, 26 - boy), (58, 26 - boy))], golge="yatay")


# ---------------------------------------------------------------- HALK


def koylu(t):
    """Rumeli köylüsü (reaya): koyun postu yelek, keten gömlek, dolaklı ayak, çapa."""
    bas(t, TEN_ESMER, sac="#3a2a1e", yas="orta")
    biyik(t, "#3a2a1e", tur="sarkik")
    sakal(t, "#3a2a1e", tur="kisa")
    kalpak(t, renk="#4a3a2a", boy=12)
    gomlek_govde(t, KEMIK, z=40, alt=118, doku=kivrim(5, 0.1))
    t.parca(40, KEMIK, [P((48, 100), (80, 100), (84, 122), (44, 122))], golge="silindir", doku=kivrim(5, 0.1),
            desen=(["x.x.", "...."], "#b83a2a", 4, 2))
    yelek = [(44, 58), (48, 52), (57, 51), (60, 104), (46, 104)]
    t.parca(44, "#8a6a42", [P(*yelek)], golge="silindir", doku=kurk(2, 0.3))
    t.parca(44, "#8a6a42", [P(*ayna(yelek))], golge="silindir", doku=kurk(3, 0.3), isik=-0.1)
    kusak(t, "#a83a2a", z=46, y=90, kalin=5)
    bacak(t, "#d8ccb0", z=22, ust=112, alt=160, doku=yatay_cizgi(3, 0.18))
    cizme(t, "#6a4a2e", z=24, kisa=True)
    kol(t, KEMIK, "yan", ten=TEN_ESMER, z=50)
    kol(t, KEMIK, "direk", sag=True, ten=TEN_ESMER, z=50)
    sopa(t, 97, 40, z=49)
    t.parca(49, DEMIR, [P((88, 156), (104, 156), (106, 167), (86, 167))], golge="yatay")  # çapa ağzı yerde


def koylu_kadin(t):
    """Balkan köylü kadını: işlemeli yemeni, kırmızı fistan, desenli önlük, ekmek sepeti."""
    bas(t, TEN_ACIK, sac="#4a2a1a", kadin=True, agiz="gulus")
    t.parca(30, "#e8dcc4", [P((52, 30), (56, 20), (64, 17), (72, 20), (76, 30), (80, 58), (48, 58))], golge="silindir",
            doku=kivrim(4, 0.08))  # yemeninin sırta inen kısmı
    t.parca(62, "#e8dcc4", [P((54, 34), (55, 24), (60, 19), (68, 19), (73, 24), (74, 34), (71, 28), (64, 26), (57, 28))], golge="kure")
    t.parca(63, "#b8302a", [P((55, 27), (58, 23), (70, 23), (73, 27), (72, 30), (56, 30))], golge="yatay", desen=(["x.", ".x"], ALTIN, 2, 2))
    kaftan(t, "#8a2a2a", z=40, boy=162, etek=30, doku=kivrim(6, 0.12))
    t.parca(42, KEMIK, [P((56, 52), (72, 52), (68, 62), (60, 62))], golge="silindir", desen=ISLEME)  # gömlek yakası
    t.parca(44, "#2a2a3a", [P((54, 92), (74, 92), (80, 158), (48, 158))], golge="silindir", doku=kivrim(5, 0.1), desen=CICEK)
    t.parca(45, "#2a2a3a", [P((48, 152), (80, 152), (80, 158), (48, 158))], golge="yatay", desen=(["x."], "#d8a83a", 2, 1))
    kusak(t, "#c8a050", z=48, y=86, kalin=6, desen=(["xx.."], "#b8302a", 4, 3))
    cizme(t, "#5a3a22", z=24, kisa=True)
    kol(t, KEMIK, "bel", ten=TEN_ACIK, z=50, yen="#b8302a")
    kol(t, KEMIK, "yan", sag=True, ten=TEN_ACIK, z=50, yen="#b8302a")
    # ekmek sepeti kalçada
    t.parca(53, "#b08a4a", [P((26, 92), (50, 92), (47, 108), (29, 108))], golge="silindir", doku=birlestir(yatay_cizgi(3, 0.2), kivrim(3, 0.1)))
    t.parca(52, "#c89a58", [E(29, 85, 41, 95)], golge="kure")
    t.parca(52, "#b07a3a", [E(37, 84, 48, 94)], golge="kure")
    t.parca(54, "#b08a4a", [L((26, 92), (38, 76), (50, 92), w=2)], golge="duz")


def cocuk(t):
    """Devşirme çağında köy çocuğu: işlemeli uzun gömlek, yalın ayak, elinde annesinin bağladığı bohça."""
    with t.olcek(0.66):
        with t.olcek(1.32, 64, 52):
            bas(t, TEN_ACIK, sac="#5a3a22", cocuk=True, agiz="duz")
            t.parca(62, "#5a3a22", [P((55, 33), (55, 25), (60, 21), (68, 21), (73, 25), (73, 33), (71, 28), (66, 27), (63, 30), (60, 27), (57, 29))],
                    golge="kure", doku=kivrim(2, 0.12))
        gomlek_govde(t, KEMIK, z=40, alt=132, genis=1, doku=kivrim(5, 0.1))
        t.parca(41, KEMIK, [P((47, 112), (81, 112), (84, 134), (44, 134))], golge="silindir", desen=ISLEME, doku=kivrim(5, 0.1))
        kusak(t, "#3a6a4a", z=46, y=94, kalin=5)
        bacak(t, TEN_ACIK, z=22, ust=128, alt=163)
        for x in (50, 72):
            t.parca(24, TEN_ACIK, [E(x, 160, x + 9, 167)], golge="kure")
        kol(t, KEMIK, "gogus", ten=TEN_ACIK, z=50)
        kol(t, KEMIK, "gogus", sag=True, ten=TEN_ACIK, z=50)
        t.parca(49, "#3a5a8a", [E(46, 80, 82, 108)], golge="kure", desen=([".x.", "x.x"], "#f0e0c0", 5, 4))  # bohça
        t.parca(52, "#3a5a8a", [P((58, 82), (54, 72), (62, 78), (64, 76), (66, 78), (74, 72), (70, 82), (64, 86))], golge="kure")  # düğüm


def tuccar(t):
    """Raguzalı tüccar: kürk kenarlı uzun cüppe, yumuşak başlık, altın zincir, hesap defteri."""
    bas(t, TEN_ACIK, sac="#6a4a2a", yas="orta", agiz="gulus")
    sakal(t, "#6a4a2a", tur="kisa")
    biyik(t, "#6a4a2a", tur="ince")
    sac_yanlar(t, "#6a4a2a", uzun=True)
    t.parca(80, "#1e1a22", [P((53, 31), (75, 31), (78, 22), (72, 14), (58, 13), (50, 20))], golge="kure", doku=kivrim(4, 0.1))
    t.parca(81, "#7a1a2a", [P((53, 31), (75, 31), (75, 27), (53, 27))], golge="yatay")
    kaftan(t, "#7a1a2a", z=40, boy=162, etek=28, ic="#2a2a3a")
    kurk_yaka(t, "#5a4030", boy=162, etek=28)
    t.parca(57, ALTIN, [L((52, 56), (58, 74), (64, 80), (70, 74), (76, 56), w=2)], golge="duz", desen=(["x."], "#8a6a20", 2, 1))
    t.parca(58, ALTIN, [C(64, 82, 3)], golge="kure")
    cizme(t, "#2a1a14", z=24, kisa=True)
    kol(t, "#7a1a2a", "gogus", ten=TEN_ACIK, z=50, yen="#5a4030", kalin=12)
    kol(t, "#7a1a2a", "yan", sag=True, ten=TEN_ACIK, z=50, yen="#5a4030", kalin=12)
    kitap(t, 58, 98, z=52, renk="#2a3a5a")
    t.parca(51, "#8a6a3a", [E(83, 112, 93, 124)], golge="kure", desen=(["x"], ALTIN, 3, 3))  # para kesesi
    t.parca(51.5, "#5a3a1a", [L((86, 110), (90, 110), w=2)], golge="duz")


def dervis(t):
    """Bektaşi dervişi: on iki dilimli elifî tâc, yamalı hırka, teber ve keşkül. Ocağın manevi babası."""
    bas(t, TEN_ESMER, sac="#d8d0c4", yas="yasli", agiz="gulus")
    biyik(t, "#d8d0c4", tur="ince")
    sakal(t, "#d8d0c4", tur="uzun")
    t.parca(80, BEYAZ, [P((54, 32), (74, 32), (73, 4), (70, -6), (58, -6), (55, 4))], golge="silindir", doku=kivrim(3, 0.18))
    t.parca(81, "#c8bfae", [P((54, 28), (74, 28), (74, 32), (54, 32))], golge="yatay")
    kaftan(t, "#6a6a42", z=40, boy=162, etek=28, ic="#8a7a5a",
           doku=birlestir(kivrim(7, 0.12), yatay_cizgi(13, 0.12)))
    for x0, y0, renk in ((44, 110, "#7a5a3a"), (70, 128, "#4a5a3a"), (54, 140, "#8a6a4a")):  # yamalar
        t.parca(42, renk, [R(x0, y0, x0 + 9, y0 + 8)], golge="duz", doku=kivrim(3, 0.1))
    kusak(t, "#c8bfae", z=48, y=86, kalin=5)
    t.parca(49, "#e8e0d0", [P((60, 70), (68, 70), (66, 78), (62, 78))], golge="kure")  # teslim taşı
    t.parca(48, "#a89a7a", [L((56, 52), (64, 70), (72, 52), w=1)], golge="duz", kontur=False)
    cizme(t, "#5a3a22", z=24, kisa=True)
    kol(t, "#6a6a42", "one", ten=TEN_ESMER, z=50, kalin=12)
    kol(t, "#6a6a42", "direk", sag=True, ten=TEN_ESMER, z=50, kalin=12)
    t.parca(53, "#4a2a1a", [E(36, 102, 54, 114)], golge="kure", doku=kivrim(3, 0.1))  # keşkül
    t.parca(54, ALTIN, [L((36, 104), (45, 92), (54, 104), w=1)], golge="duz")
    sopa(t, 97, 26, z=49)
    t.parca(49.5, CELIK, [P((97, 22), (110, 18), (114, 30), (106, 40), (97, 34))], golge="kure")  # teber ağzı


def hayduk(t):
    """Hayduk: dağlarda yaşayan asi; uzun saç, kürk kalpak, koyun postu yelek, silahlık, uzun saplı balta."""
    bas(t, TEN_ESMER, sac="#1e1612", yas="orta", agiz="sert")
    biyik(t, "#1e1612", tur="sarkik")
    sac_yanlar(t, "#1e1612", uzun=True)
    t.parca(30, "#1e1612", [P((52, 32), (76, 32), (78, 62), (50, 62))], golge="silindir", doku=kivrim(2, 0.12))  # omuza dökülen saç
    kalpak(t, renk="#2a2220", boy=16, ust=True, tepe="#8a2a22")
    gomlek_govde(t, "#e0d4bc", z=40, alt=112)
    yelek = [(44, 58), (48, 52), (57, 51), (59, 100), (45, 100)]
    t.parca(44, "#4a3a2a", [P(*yelek)], golge="silindir", doku=kurk(9, 0.3))
    t.parca(44, "#4a3a2a", [P(*ayna(yelek))], golge="silindir", doku=kurk(10, 0.3), isik=-0.1)
    t.parca(47, "#6a4a2a", [P((46, 84), (82, 84), (82, 100), (46, 100))], golge="yatay", doku=yatay_cizgi(4, 0.15))  # silahlık
    for x in (54, 68):  # kuşağa sokulmuş elma kabzalı tabancalar
        t.parca(48, "#5a3a22", [L((x, 82), (x + 2, 96), w=4)], golge="silindir")
        t.parca(48.5, CELIK, [E(x - 4, 74, x + 4, 82)], golge="kure", desen=(["x."], ALTIN, 2, 2))
    bacak(t, "#3a2a2a", z=22, ust=104, alt=158)
    t.parca(23, "#d8ccb0", [L((57, 134), (56, 158), w=13)], golge="silindir", doku=yatay_cizgi(3, 0.2))  # dolak
    t.parca(23, "#d8ccb0", [L((71, 134), (72, 158), w=13)], golge="silindir", doku=yatay_cizgi(3, 0.2), isik=-0.1)
    cizme(t, "#4a3020", z=24, kisa=True)
    kol(t, "#e0d4bc", "yan", ten=TEN_ESMER, z=50)
    kol(t, "#e0d4bc", "direk", sag=True, ten=TEN_ESMER, z=50)
    sopa(t, 97, 22, z=49, kalin=3)
    t.parca(49.5, CELIK, [P((97, 20), (106, 16), (110, 24), (106, 32), (97, 30))], golge="kure")


# ---------------------------------------------------------------- KAPIKULU


def acemi_oglan(t):
    """Acemi oğlan: Ocağa yetiştirilen genç; keçe külah, kısa dolama, elinde kürek (bahçe ve inşaat hizmeti)."""
    with t.olcek(0.9):
        bas(t, TEN, sac="#3a2a1e", agiz="duz")
        t.parca(80, "#a83a2a", [P((55, 31), (73, 31), (71, 18), (66, 8), (62, 8), (57, 18))], golge="silindir", doku=kivrim(4, 0.08))
        t.parca(81, "#7a2a20", [P((55, 28), (73, 28), (73, 31), (55, 31))], golge="yatay")
        kaftan(t, "#9a7a42", z=40, boy=130, etek=24, ic="#d8c8a0")
        kusak(t, "#5a6a3a", z=48, y=86, kalin=6)
        salvar(t, "#d8ccb0", z=22, ust=118, alt=156)
        cizme(t, "#b8902a", z=24, kisa=True)
        kol(t, "#9a7a42", "yan", ten=TEN, z=50)
        kol(t, "#9a7a42", "direk", sag=True, ten=TEN, z=50)
        sopa(t, 97, 44, z=49)
        t.parca(49.5, DEMIR, [P((91, 150), (103, 150), (103, 162), (97, 167), (91, 162))], golge="kure")  # kürek ağzı yerde


def yeniceri_neferi(t):
    """Yeniçeri neferi: ak börk, etekleri kuşağa sokulmuş mavi dolama, fitilli tüfek, yatağan."""
    bas(t, TEN, sac="#2a1a14", agiz="sert")
    biyik(t, "#2a1a14", tur="pala")
    yeniceri_borku(t)
    kaftan(t, "#2e4f8f", z=40, boy=126, etek=22, ic="#c8a060")
    for kenar in ([(42, 92), (54, 92), (49, 128), (38, 126)],):
        t.parca(39, "#b8302a", [P(*kenar)], golge="silindir", doku=kivrim(4, 0.1))
        t.parca(39, "#b8302a", [P(*ayna(kenar))], golge="silindir", isik=-0.1, doku=kivrim(4, 0.1))
    salvar(t, "#e8dcc4", z=22, ust=112, alt=156)
    cizme(t, "#a8282a", z=24)
    kusak(t, "#c8302a", z=48, y=84, desen=CIZGI)
    yatagan(t, 72, 88)
    barut_kabi(t, 50, 104)
    kol(t, "#2e4f8f", "yan", ten=TEN, z=50, yen="#c8a060")
    kol(t, "#2e4f8f", "direk", sag=True, ten=TEN, z=50, yen="#c8a060")
    tufek(t, 97)


def corbaci(t):
    """Yeniçeri çorbacısı: ortanın komutanı; tüylü börk, kırmızı dolama, altın düğmeler, topuz."""
    bas(t, TEN, sac="#2a1a14", yas="orta", agiz="sert")
    biyik(t, "#2a1a14", tur="burma")
    yeniceri_borku(t, sorguc="#e8dcc8", kasiklik="#e0b848")
    kaftan(t, "#a82a26", z=40, boy=160, etek=28, ic="#e0c890")
    for y in range(60, 84, 5):
        t.parca(46, ALTIN, [C(59, y, 1.5), C(69, y, 1.5)], golge="kure")
    t.parca(45, ALTIN, [L((59, 62), (59, 82), w=1), L((69, 62), (69, 82), w=1)], golge="duz", kontur=False)
    kusak(t, "#2e4f8f", z=48, y=86, desen=CIZGI)
    kilic(t, 50, 92, z=46)
    cizme(t, "#d8a830", z=24, kisa=True)
    kol(t, "#a82a26", "kilic", ten=TEN, z=50, yen="#e0c890")
    kol(t, "#a82a26", "gogus", sag=True, ten=TEN, z=50, yen="#e0c890")
    topuz(t, 70, 84, z=49, sap=22)


def yeniceri_agasi(t):
    """Yeniçeri ağası: Ocağın başı; sorguçlu büyük kavuk, samur kürklü çintemani kaftan, altın topuz."""
    bas(t, TEN, sac="#1e1612", yas="orta", agiz="sert")
    biyik(t, "#1e1612", tur="burma")
    sakal(t, "#1e1612", tur="dolgun")
    kavuk(t, tur="yuvarlak", ic="#2e4f8f", sorguc="#f4f0e8", mucevher="#2a8a5a")
    kaftan(t, "#5a1e4a", z=40, boy=162, etek=30, ic="#e0c890", desen=CINTEMANI)
    kurk_yaka(t, "#3a2a20", boy=162, etek=30)
    kusak(t, ALTIN, z=48, y=86, kalin=6)
    cizme(t, "#d8a830", z=24, kisa=True)
    kol(t, "#5a1e4a", "bel", ten=TEN, z=50, yen="#3a2a20", kalin=12)
    kol(t, "#5a1e4a", "direk", sag=True, ten=TEN, z=50, yen="#3a2a20", kalin=12)
    t.parca(49, "#6a3a1a", [L((97, 66), (97, 166), w=3)], golge="silindir")  # ağa asası, ucu yerde
    t.parca(49.5, ALTIN, [C(97, 62, 5)], golge="kure", doku=kivrim(2, 0.15))
    t.parca(49.6, "#c83a30", [C(97, 61, 2)], golge="kure", isik=0.1)


def topcu(t):
    """Topçu: sarıklı kırmızı külah, sıvalı kollar, deri önlük, top tokmağı."""
    bas(t, TEN_ESMER, sac="#1e1612", yas="orta")
    biyik(t, "#1e1612", tur="pala")
    sakal(t, "#1e1612", tur="kisa")
    t.parca(80, "#8a2a22", [P((56, 30), (72, 30), (70, 12), (66, 6), (62, 6), (58, 12))], golge="silindir")
    t.parca(81, "#e0d4bc", [E(52, 22, 76, 34)], golge="yatay", doku=kivrim(3, 0.15, egim=-1))
    gomlek_govde(t, "#3a5a3a", z=40, alt=120, genis=2)
    t.parca(44, "#6a4a2e", [P((50, 70), (78, 70), (80, 130), (48, 130))], golge="silindir", doku=kivrim(6, 0.08))  # deri önlük
    t.parca(45, "#6a4a2e", [L((52, 70), (56, 52), w=2), L((76, 70), (72, 52), w=2)], golge="duz")
    t.parca(46, "#1e1612", [E(58, 104, 64, 109), E(68, 116, 72, 119)], golge="duz", kontur=False)  # barut lekeleri
    kusak(t, "#c8a050", z=48, y=84, kalin=5)
    salvar(t, "#5a5a4a", z=22, ust=118, alt=156)
    cizme(t, "#3a2a20", z=24, kisa=True)
    kol(t, "#3a5a3a", "yan", ten=TEN_ESMER, z=50, el=True)
    t.parca(50.6, TEN_ESMER, [L((43, 86), (41, 103), w=8)], golge="silindir")  # sıvalı ön kol
    kol(t, "#3a5a3a", "direk", sag=True, ten=TEN_ESMER, z=50)
    t.parca(50.6, TEN_ESMER, [L((91, 80), (96, 94), w=8)], golge="silindir", isik=-0.1)
    sopa(t, 97, 18, z=49, kalin=3)
    t.parca(49.5, "#5a4030", [P((92, 6), (102, 6), (102, 22), (92, 22))], golge="silindir", doku=kurk(12, 0.3))  # tokmak başı


# ---------------------------------------------------------------- TAŞRA VE SARAY


def sipahi(t):
    """Tımarlı sipahi: çiçak miğfer, zincir zırh, renkli hasır kalkan, flamalı mızrak."""
    bas(t, TEN, sac="#2a1a14", yas="orta", agiz="sert")
    biyik(t, "#2a1a14", tur="pala")
    sakal(t, "#2a1a14", tur="kisa")
    t.parca(30, DEMIR, [P((52, 30), (76, 30), (82, 60), (46, 60))], golge="silindir", doku=zincir())  # zincir enselik
    t.parca(80, CELIK, [P((53, 32), (55, 20), (60, 12), (64, 2), (68, 12), (73, 20), (75, 32))], golge="kure", doku=kivrim(5, 0.1))
    t.parca(81, ALTIN, [P((53, 28), (75, 28), (75, 32), (53, 32))], golge="yatay", desen=(["x."], "#8a6a20", 2, 1))
    t.parca(82, CELIK, [R(63, 30, 65, 42)], golge="silindir")  # burunluk
    kaftan(t, "#a83a2a", z=38, boy=156, etek=28)
    t.parca(42, DEMIR, [P((43, 58), (47, 52), (56, 50), (72, 50), (81, 52), (85, 58), (84, 112), (44, 112))], golge="silindir",
            doku=zincir())
    t.parca(43, CELIK, [P((52, 62), (76, 62), (74, 84), (54, 84))], golge="kure", doku=yatay_cizgi(4, 0.15))  # göğüs plakaları
    kusak(t, "#2e4f8f", z=48, y=86, kalin=5)
    kilic(t, 76, 92, z=46, sag=True)
    cizme(t, "#d8a830", z=24)
    kol(t, DEMIR, "gogus", ten=TEN, z=50, doku=zincir())
    kol(t, DEMIR, "direk", sag=True, ten=TEN, z=50, doku=zincir())
    t.parca(55, "#c8a050", [C(42, 92, 17)], golge="kure", doku=birlestir(kivrim(3, 0.12), yatay_cizgi(3, 0.08)))  # hasır kalkan
    t.parca(56, "#a8302a", [C(42, 92, 12)], golge="kure", doku=kivrim(2, 0.1))
    t.parca(57, "#2e4f8f", [C(42, 92, 7)], golge="kure")
    t.parca(58, ALTIN, [C(42, 92, 3)], golge="kure")
    mizrak(t, 97, flama="#c8302a", flama2="#e0b848")


def deli(t):
    """Deli (akıncı öncüsü): pars postu, kartal kanatlı kürk kalpak, kargı ve gözü kara bakış."""
    bas(t, TEN_ESMER, sac="#1e1612", agiz="sert")
    biyik(t, "#1e1612", tur="burma")
    kalpak(t, renk="#3a2a20", boy=18, doku_tohum=13)
    # kartal kanadı: omuzlardan yukarı ve dışa açılan tüyler, uçları koyu
    kanat = [(54, 62), (44, 44), (30, 26), (20, 10), (28, 14), (24, 4), (34, 12), (34, 2), (42, 14), (46, 6), (50, 22), (56, 40), (58, 60)]
    t.parca(12, "#e8e0d0", [P(*kanat)], golge="silindir", doku=kivrim(4, 0.2, egim=1.0))
    t.parca(12, "#e8e0d0", [P(*ayna(kanat))], golge="silindir", doku=kivrim(4, 0.2, egim=-1.0), isik=-0.1)
    t.parca(13, "#3a2a22", [P((20, 10), (28, 14), (24, 4), (34, 12), (34, 2), (42, 14), (46, 6), (46, 12), (38, 18), (28, 18))],
            golge="duz")
    t.parca(13, "#3a2a22", [P(*ayna([(20, 10), (28, 14), (24, 4), (34, 12), (34, 2), (42, 14), (46, 6), (46, 12), (38, 18), (28, 18)]))],
            golge="duz", isik=-0.1)
    gomlek_govde(t, "#2e3a5a", z=40, alt=120)
    post = [(42, 60), (48, 50), (80, 50), (86, 60), (88, 118), (76, 128), (64, 116), (52, 128), (40, 118)]
    t.parca(44, "#d8a048", [P(*post)], golge="silindir", desen=LEKE, doku=kivrim(6, 0.08))  # pars postu
    t.parca(45, "#d8a048", [E(56, 48, 72, 62)], golge="kure", desen=LEKE)  # postun başı göğüste
    t.parca(46, "#1e1612", [C(61, 55, 1), C(67, 55, 1)], golge="duz", kontur=False)
    kusak(t, "#c8302a", z=48, y=90, kalin=5)
    salvar(t, "#a83a2a", z=22, ust=114, alt=156)
    cizme(t, "#d8a830", z=24)
    kol(t, "#2e3a5a", "bel", ten=TEN_ESMER, z=50)
    kol(t, "#2e3a5a", "direk", sag=True, ten=TEN_ESMER, z=50)
    mizrak(t, 97, ust=2, flama=None)
    t.parca(48.5, "#d8a048", [P((95, 18), (99, 18), (100, 28), (94, 28))], golge="silindir", desen=LEKE)


def kadi(t):
    """Kadı: şeriat ve kanunun yerel temsilcisi; büyük örfî kavuk, geniş yenli cüppe, kitap."""
    bas(t, TEN, sac="#c8c0b4", yas="yasli", agiz="duz")
    biyik(t, "#c8c0b4", tur="ince")
    sakal(t, "#c8c0b4", tur="uzun")
    kavuk(t, tur="yuvarlak", ic="#2a5a3a")
    kaftan(t, "#2a3a4a", z=40, boy=162, etek=30, ic="#e0d8c4")
    t.parca(45, "#3a5a4a", [L((58, 56), (56, 160), w=4), L((70, 56), (72, 160), w=4)], golge="silindir")
    kusak(t, "#e0d8c4", z=48, y=88, kalin=5)
    cizme(t, "#e0c890", z=24, kisa=True)
    kol(t, "#2a3a4a", "gogus", ten=TEN, z=50, kalin=14)
    kol(t, "#2a3a4a", "gogus", sag=True, ten=TEN, z=50, kalin=14)
    kitap(t, 64, 92, z=52, renk="#5a2a1e")


def beylerbeyi(t):
    """Rumeli beylerbeyi (paşa): kallavi kavuk, çintemani desenli kaftan, samur kürk, el kılıç kabzasında."""
    bas(t, TEN, sac="#1e1612", yas="orta", agiz="sert")
    biyik(t, "#1e1612", tur="pala")
    sakal(t, "#1e1612", tur="dolgun")
    kavuk(t, tur="kallavi", ic="#a82a26")
    kaftan(t, "#8a1e22", z=40, boy=162, etek=30, ic="#e0c890", desen=CINTEMANI)
    kurk_yaka(t, "#3a2a20", boy=162, etek=30)
    kusak(t, ALTIN, z=48, y=86, kalin=6)
    kilic(t, 52, 92, z=46)
    cizme(t, "#d8a830", z=24, kisa=True)
    kol(t, "#8a1e22", "kilic", ten=TEN, z=50, yen="#3a2a20", kalin=12)
    kol(t, "#8a1e22", "bel", sag=True, ten=TEN, z=50, yen="#3a2a20", kalin=12)


def padisah(t):
    """Padişah: çift sorguçlu büyük kavuk, altın sırma kaftan, samur kürk; Rumeli seferinin başında."""
    bas(t, TEN_ACIK, sac="#3a2418", yas="orta", agiz="duz")
    biyik(t, "#3a2418", tur="ince")
    sakal(t, "#3a2418", tur="sivri")
    kavuk(t, tur="sultan", ic="#a82a26", sorguc="#f4f0e8", mucevher="#2a8a5a", iki_sorguc=True)
    kaftan(t, "#d8b060", z=40, boy=162, etek=32, ic="#a82a26",
           desen=([".x.x.", "..x..", ".....", "x...x", ".x.x."], "#a82a26", 8, 7))
    kurk_yaka(t, "#2a1e18", boy=162, etek=32)
    kusak(t, "#a82a26", z=48, y=86, kalin=6, desen=NOKTA)
    t.parca(49, "#2a8a5a", [E(61, 85, 67, 92)], golge="kure", isik=0.1)
    kilic(t, 52, 92, z=46, kin="#2a1e18")
    cizme(t, "#d8a830", z=24, kisa=True)
    kol(t, "#d8b060", "kilic", ten=TEN_ACIK, z=50, yen="#2a1e18", kalin=12)
    kol(t, "#d8b060", "gogus", sag=True, ten=TEN_ACIK, z=50, yen="#2a1e18", kalin=12)
    t.parca(53, BEYAZ, [P((68, 88), (74, 90), (72, 102), (68, 100))], golge="duz", doku=kivrim(2, 0.1))  # mendil


def saray_hanimi(t):
    """Saray hanımı: tüllü hotoz, inci dizileri, gül desenli entari, kürk kenarlı kaftan, elinde gül."""
    bas(t, TEN_ACIK, sac="#3a2418", kadin=True, agiz="gulus")
    t.parca(30, "#f4e8f0", [P((54, 24), (74, 24), (86, 70), (80, 120), (48, 120), (42, 70))], golge="silindir",
            doku=kivrim(4, 0.12), isik=0.1)  # arkaya dökülen tül
    t.parca(58, "#3a2418", [P((55, 33), (56, 26), (64, 24), (72, 26), (73, 33), (72, 44), (70, 32), (58, 32), (56, 44))], golge="kure")
    t.parca(80, "#a83a5a", [P((56, 28), (72, 28), (74, 10), (68, 4), (60, 4), (54, 10))], golge="silindir", desen=NOKTA)  # hotoz
    t.parca(81, ALTIN, [P((54, 26), (74, 26), (74, 30), (54, 30))], golge="yatay", desen=(["x."], "#f4f0e8", 2, 1))
    t.parca(82, "#f4e8f0", [P((64, 4), (60, -10), (66, -16), (70, -6))], golge="silindir", isik=0.1)
    for i, (x, y) in enumerate(((58, 58), (61, 62), (64, 63), (67, 62), (70, 58))):
        t.parca(60, "#f4f0ec", [C(x, y, 1.3)], golge="kure", isik=0.2)  # inci dizisi
    kaftan(t, "#3a6a6a", z=40, boy=164, etek=32, ic="#e8b8c0", ic_genis=14, desen=CICEK_BEYAZ)
    t.parca(41.5, "#e8b8c0", [P((58, 56), (70, 56), (78, 164), (50, 164))], golge="silindir", desen=CICEK, doku=kivrim(5, 0.08))
    kurk_yaka(t, "#efe6dc", boy=164, etek=32)
    kusak(t, ALTIN, z=48, y=84, kalin=5, desen=(["x."], "#2a8a5a", 2, 1))
    kol(t, "#3a6a6a", "gogus", ten=TEN_ACIK, z=50, yen="#efe6dc", kalin=11)
    kol(t, "#3a6a6a", "yan", sag=True, ten=TEN_ACIK, z=50, yen="#efe6dc", kalin=11)
    t.parca(53, "#4a7a3a", [L((58, 92), (60, 80), w=1)], golge="duz")
    t.parca(54, "#c8304a", [C(60, 78, 3)], golge="kure", doku=kivrim(2, 0.15))


# ---------------------------------------------------------------- HAÇLI CEPHESİ


def voyvoda(t):
    """Voyvoda: kürk kalpakta mücevherli sorguç, uzun boyar kaftanı, kırmızı pelerin, gürz."""
    bas(t, TEN_ACIK, sac="#1e1612", yas="orta", agiz="sert")
    biyik(t, "#1e1612", tur="sarkik")
    sac_yanlar(t, "#1e1612", uzun=True)
    t.parca(30, "#1e1612", [P((52, 32), (76, 32), (77, 58), (51, 58))], golge="silindir", doku=kivrim(2, 0.12))
    kalpak(t, renk="#2a2220", boy=16, ust=True, tepe="#7a1a2a", doku_tohum=21)
    t.parca(82, ALTIN, [E(60, 18, 68, 26)], golge="kure")
    t.parca(83, "#c8302a", [E(62, 20, 66, 24)], golge="kure", isik=0.1)
    t.parca(81, "#f4f0e8", [P((65, 18), (70, -4), (74, -14), (72, 2), (68, 18))], golge="silindir", doku=kivrim(2, 0.15))
    t.parca(15, "#8a1a22", [P((44, 52), (84, 52), (96, 160), (32, 160))], golge="silindir", doku=kivrim(8, 0.14))  # pelerin
    kaftan(t, "#2a4a3a", z=40, boy=162, etek=26, ic="#c8a050", ic_genis=4)
    for y in range(60, 150, 7):
        t.parca(46, ALTIN, [C(64, y, 1.5)], golge="kure")
    t.parca(45, "#3a2a20", [P((44, 52), (84, 52), (80, 60), (48, 60))], golge="yatay", doku=kurk(22, 0.3))  # kürk omuz
    t.parca(45.5, ALTIN, [C(48, 58, 3), C(80, 58, 3)], golge="kure")
    t.parca(45.4, ALTIN, [L((48, 58), (80, 58), w=1)], golge="duz")
    kusak(t, "#8a1a22", z=48, y=88, kalin=5, desen=NOKTA)
    cizme(t, "#5a1a1a", z=24, kisa=True)
    kol(t, "#2a4a3a", "bel", ten=TEN_ACIK, z=50, yen=ALTIN)
    kol(t, "#2a4a3a", "gogus", sag=True, ten=TEN_ACIK, z=50, yen=ALTIN)
    topuz(t, 70, 84, z=51, renk=CELIK, sap=24)


def macar_suvarisi(t):
    """Macar süvarisi (huszár): tüylü keçe kalpak, kordonlu dolman, kanat biçimli kalkan, flamalı mızrak."""
    bas(t, TEN_ACIK, sac="#4a2a1a", agiz="sert")
    biyik(t, "#4a2a1a", tur="burma")
    t.parca(80, "#2a2a3a", [P((54, 32), (74, 32), (76, 8), (70, 4), (56, 6))], golge="silindir", doku=kivrim(4, 0.1))
    t.parca(81, "#c8302a", [P((54, 28), (74, 28), (74, 32), (54, 32))], golge="yatay")
    t.parca(82, "#2a2a2a", [P((72, 10), (80, -10), (82, -26), (76, -8), (70, 8))], golge="silindir", doku=kivrim(2, 0.2))  # turna tüyü
    t.parca(82.5, ALTIN, [C(72, 12, 2.5)], golge="kure")
    gomlek_govde(t, "#2a4a8a", z=40, alt=104, desen=KORDON)
    t.parca(41, "#2a4a8a", [P((46, 98), (82, 98), (84, 112), (44, 112))], golge="silindir")
    for y in range(58, 100, 6):
        t.parca(42, ALTIN, [C(64, y, 1.2)], golge="kure")
    kusak(t, "#c8302a", z=48, y=88, kalin=5, desen=NOKTA)
    bacak(t, "#c8302a", z=22, ust=104, alt=150)
    cizme(t, "#d8a830", z=24)
    kilic(t, 78, 96, z=46, sag=True)
    kol(t, "#2a4a8a", "gogus", ten=TEN_ACIK, z=50, yen=ALTIN, doku=kivrim(3, 0.1))
    kol(t, "#2a4a8a", "direk", sag=True, ten=TEN_ACIK, z=50, yen=ALTIN, doku=kivrim(3, 0.1))
    kalkan = [(26, 66), (54, 60), (56, 94), (46, 124), (36, 130), (30, 112), (28, 90), (18, 72)]
    t.parca(55, "#e8e0cc", [P(*kalkan)], golge="silindir", doku=kivrim(6, 0.06))
    t.parca(56, "#c8302a", [P((30, 72), (50, 68), (52, 92), (44, 116), (36, 120), (32, 92))], golge="silindir")
    t.parca(57, "#e8e0cc", [P((40, 80), (44, 80), (44, 88), (52, 88), (52, 92), (44, 92), (44, 108), (40, 108), (40, 92), (34, 92),
                              (34, 88), (40, 88))], golge="duz")
    mizrak(t, 97, ust=0, flama="#e8e0cc", flama2="#c8302a")


def sovalye(t):
    """Şövalye: tam plaka zırh, kırmızı tüylü kapalı miğfer, çift haçlı arma, ucu yerde düz kılıç."""
    t.parca(60, CELIK, [P((54, 46), (54, 26), (58, 20), (70, 20), (74, 26), (74, 46), (64, 50))], golge="kure",
            doku=kivrim(6, 0.06))  # miğfer
    t.parca(61, CELIK, [P((54, 30), (74, 30), (74, 44), (64, 50), (54, 44))], golge="kure", isik=0.05)  # vizör
    t.parca(62, "#1a1a22", [R(56, 34, 72, 35)], golge="duz", kontur=False)  # göz yarığı
    for y in (39, 42):
        for x in range(58, 71, 3):
            t.px(x, y, "#1a1a22")
    t.parca(59, "#c8302a", [P((62, 22), (58, 8), (62, -4), (72, -10), (82, -4), (78, 4), (70, 6), (66, 22))], golge="kure",
            doku=kivrim(3, 0.15))  # tüy
    t.parca(57, CELIK, [R(58, 46, 70, 54)], golge="silindir", doku=yatay_cizgi(3, 0.2))  # boğazlık
    t.parca(40, CELIK, [P((46, 54), (82, 54), (80, 100), (48, 100))], golge="kure", doku=kivrim(14, 0.05))  # göğüslük
    t.parca(42, "#a82a26", [P((48, 62), (80, 62), (82, 132), (46, 132))], golge="silindir", doku=kivrim(7, 0.1))  # arma cüppesi
    t.parca(43, BEYAZ, [R(62, 70, 66, 116), R(54, 80, 74, 84), R(56, 94, 72, 98)], golge="duz")  # çift haç
    t.parca(43.5, "#5a8a3a", [P((56, 112), (72, 112), (68, 124), (60, 124))], golge="kure")  # üç tepe
    t.parca(44, "#4a2a1a", [R(48, 100, 80, 104)], golge="yatay")
    for taraf in (False, True):
        isik = -0.1 if taraf else 0
        omuz = [(38, 54), (48, 50), (56, 54), (54, 66), (40, 68)]
        t.parca(55, CELIK, [P(*(ayna(omuz) if taraf else omuz))], golge="kure", isik=isik, doku=yatay_cizgi(4, 0.15))
    bacak(t, CELIK, z=22, ust=128, alt=158, doku=kivrim(8, 0.06))
    for x in (56, 72):
        t.parca(23, CELIK, [E(x - 6, 140, x + 6, 150)], golge="kure", isik=0.05)  # dizlik
    cizme(t, DEMIR, z=24, kisa=True)
    duz_kilic(t, 64, 86, 166, z=70)
    for sag in (False, True):
        kol(t, CELIK, "kabza", sag=sag, ten=TEN, z=73, eldiven=DEMIR, doku=yatay_cizgi(5, 0.1), kalin=11)


# ---------------------------------------------------------------- 30'luk kadroya eklenenler


def sadrazam(t):
    """Sadrazam: devletin mührünü taşıyan vezir; beyaz atlas kaftan, samur kürk, kallavi, elinde mühr-i hümayun."""
    bas(t, TEN, sac="#b8b0a4", yas="yasli", agiz="duz")
    biyik(t, "#b8b0a4", tur="ince")
    sakal(t, "#b8b0a4", tur="dolgun")
    kavuk(t, tur="kallavi", ic="#2a6a4a")
    kaftan(t, "#e8e0d0", z=40, boy=162, etek=30, ic="#2a6a4a", desen=(["x"], ALTIN, 6, 6))
    kurk_yaka(t, "#2a1e18", boy=162, etek=30)
    kusak(t, "#2a6a4a", z=48, y=86, kalin=6, desen=NOKTA)
    cizme(t, "#d8a830", z=24, kisa=True)
    kol(t, "#e8e0d0", "gogus", ten=TEN, z=50, yen="#2a1e18", kalin=13)
    kol(t, "#e8e0d0", "yan", sag=True, ten=TEN, z=50, yen="#2a1e18", kalin=13)
    t.parca(53, "#a82a26", [E(52, 80, 64, 92)], golge="kure", desen=(["x."], ALTIN, 2, 2))  # mühür kesesi
    t.parca(54, ALTIN, [C(58, 86, 3)], golge="kure", isik=0.1)
    t.parca(53.5, ALTIN, [L((54, 80), (62, 80), w=1)], golge="duz")


def sehzade(t):
    """Şehzade: sancağa çıkmış genç veliaht; sorguçlu kavuk, çintemani mavi kaftan, el kılıç kabzasında."""
    with t.olcek(0.95):
        bas(t, TEN_ACIK, sac="#3a2418", agiz="duz")
        biyik(t, "#3a2418", tur="ince")
        kavuk(t, tur="yuvarlak", ic="#2a4a8a", sorguc="#f4f0e8", mucevher="#c8302a")
        kaftan(t, "#2a4a8a", z=40, boy=162, etek=28, ic="#e0c890", desen=CINTEMANI)
        t.parca(45, ALTIN, [L((59, 56), (56, 160), w=3), L((69, 56), (72, 160), w=3)], golge="silindir")
        kusak(t, "#a82a26", z=48, y=86, kalin=6, desen=NOKTA)
        kilic(t, 52, 92, z=46)
        cizme(t, "#d8a830", z=24, kisa=True)
        kol(t, "#2a4a8a", "kilic", ten=TEN_ACIK, z=50, yen=ALTIN)
        kol(t, "#2a4a8a", "yan", sag=True, ten=TEN_ACIK, z=50, yen=ALTIN)


def akinci(t):
    """Akıncı: sınır boylarının hafif atlısı; kürk bantlı kızıl börk, kısa kaftan, yay, sadak ve pala."""
    bas(t, TEN_ESMER, sac="#2a1a14", agiz="sert")
    biyik(t, "#2a1a14", tur="pala")
    sakal(t, "#2a1a14", tur="kisa")
    t.parca(79, "#a8302a", [P((56, 24), (72, 24), (76, 6), (70, -2), (62, 0))], golge="silindir", doku=kivrim(4, 0.1))
    kalpak(t, renk="#4a3a2a", boy=7, doku_tohum=31)
    kaftan(t, "#8a5a2a", z=40, boy=128, etek=24, ic="#d8c8a0")
    salvar(t, "#3a4a6a", z=22, ust=114, alt=156)
    cizme(t, "#d8a830", z=24)
    kusak(t, "#a8302a", z=48, y=86, kalin=6)
    kilic(t, 52, 92, z=46)
    t.parca(47, "#6a3a1e", [P((80, 82), (89, 80), (95, 120), (86, 122))], golge="silindir", desen=(["x."], ALTIN, 2, 3))  # sadak
    for x in (83, 86, 89):
        t.parca(46.5, "#e8e0d0", [P((x - 2, 72), (x + 1, 72), (x + 1, 82), (x - 1, 82))], golge="duz")  # ok tüyleri
    kol(t, "#8a5a2a", "direk", ten=TEN_ESMER, z=50, yen="#d8c8a0")
    kol(t, "#8a5a2a", "yan", sag=True, ten=TEN_ESMER, z=50, yen="#d8c8a0")
    t.parca(49, "#5a3a1e", [L((30, 56), (24, 70), (26, 90), (31, 97), (26, 104), (24, 124), (30, 138), w=3)], golge="silindir")  # yay
    t.parca(49.2, ALTIN, [R(29, 94, 33, 100)], golge="duz")
    t.cizgi(30, 57, 30, 137, "#e8e0d0", z=900)


def avci(t):
    """Doğancı avcı: eldivenli elinde doğan, yeşil av kaftanı, av torbası ve boru."""
    bas(t, TEN, sac="#4a2a1a", yas="orta", agiz="gulus")
    biyik(t, "#4a2a1a", tur="pala")
    sakal(t, "#4a2a1a", tur="kisa")
    t.parca(80, "#4a5a2a", [P((52, 32), (76, 32), (74, 22), (68, 16), (58, 16), (54, 22))], golge="kure", doku=kivrim(3, 0.1))
    t.parca(81, "#6a4a2a", [R(53, 28, 75, 32)], golge="yatay")
    t.parca(81.5, "#c83a30", [P((72, 24), (82, 8), (84, 2), (78, 14), (74, 26))], golge="silindir")  # tüy
    kaftan(t, "#3a5a2a", z=40, boy=134, etek=24, ic="#c8b890")
    bacak(t, "#6a5a3a", z=22, ust=118, alt=156)
    cizme(t, "#5a3a22", z=24)
    kusak(t, "#6a4a2a", z=48, y=86, kalin=6)
    t.parca(47, "#8a6a3a", [E(70, 92, 90, 116)], golge="kure", doku=yatay_cizgi(4, 0.1))  # av torbası
    t.parca(47.5, "#e8dcc0", [L((52, 98), (44, 108), (48, 112), w=4)], golge="silindir")  # av borusu
    kol(t, "#3a5a2a", "kus", ten=TEN, z=50, eldiven="#8a6a3a", yen="#8a6a3a")
    kol(t, "#3a5a2a", "yan", sag=True, ten=TEN, z=50)
    # doğan: eldivenin üstüne konmuş
    t.parca(60, "#6a4a32", [P((24, 60), (36, 60), (36, 46), (32, 40), (26, 40), (22, 48))], golge="kure",
            desen=([".x.", "..."], "#3a2a1e", 3, 2))
    t.parca(60.5, "#e8dcc4", [E(28, 46, 35, 58)], golge="kure", desen=(["x.."], "#6a4a32", 3, 2))  # göğüs
    t.parca(61, "#4a3428", [C(31, 39, 4)], golge="kure")
    t.parca(59, "#5a3a28", [P((23, 58), (30, 58), (28, 70), (22, 68))], golge="silindir", doku=yatay_cizgi(2, 0.15))  # kuyruk
    t.px(33, 38, "#f0d040", z=1001)
    t.px(34, 40, "#e8b040", z=1001)
    t.px(35, 41, "#3a2a1e", z=1001)


def hain(t):
    """Hain: düşmana bilgi satan bey; bir elinde mühürlü mektup, öbüründe rüşvet kesesi, gözü yanda."""
    bas(t, TEN, sac="#1e1612", yas="orta", agiz="gulus")
    for gx in (59, 67):  # gözler yana kaçmış
        t.px(gx, 36, "#2a1a14", z=1001)
        t.px(gx + 1, 36, "#f2ece0", z=1001)
    biyik(t, "#1e1612", tur="burma")
    sakal(t, "#1e1612", tur="sivri")
    kavuk(t, tur="yuvarlak", renk="#d8d0c0", ic="#3a2a4a")
    kaftan(t, "#2a3a2a", z=40, boy=162, etek=28, ic="#5a3a5a", doku=kivrim(5, 0.14))
    kusak(t, "#5a3a5a", z=48, y=86, kalin=6)
    cizme(t, "#3a2a20", z=24, kisa=True)
    kol(t, "#2a3a2a", "gogus", ten=TEN, z=50, yen="#5a3a5a")
    kol(t, "#2a3a2a", "one", sag=True, ten=TEN, z=50, yen="#5a3a5a")
    t.parca(52, "#efe2c4", [P((50, 80), (64, 78), (66, 92), (52, 94))], golge="duz", doku=yatay_cizgi(3, 0.08))  # mektup
    t.parca(53, "#a82a26", [C(58, 87, 3)], golge="kure")  # düşman mührü
    t.px(58, 86, "#f0d0a0", z=1001)
    t.parca(51, "#c8a050", [E(76, 100, 90, 116)], golge="kure", desen=(["x"], "#fff0b0", 3, 3))  # altın kesesi
    t.parca(51.5, "#6a4a2a", [L((80, 100), (86, 100), w=2)], golge="duz")
    t.parca(52, ALTIN, [C(78, 120, 2), C(84, 124, 2)], golge="kure", isik=0.1)  # dökülen altınlar


def casus(t):
    """Düşman casusu: kukuletalı koyu pelerin, yüzü örtülü, elinde gizli harita, belde hançer."""
    bas(t, TEN_ACIK, sac="#2a1a14", agiz="duz")
    t.parca(12, "#2a2a34", [P((46, 50), (82, 50), (94, 162), (34, 162))], golge="silindir", doku=kivrim(8, 0.15))  # pelerin
    t.parca(62, "#2a2a34", [P((52, 50), (51, 30), (55, 20), (64, 15), (73, 20), (77, 30), (76, 50), (72, 44), (72, 32), (64, 28),
                              (56, 32), (56, 44))], golge="kure", doku=kivrim(4, 0.1))  # kukuleta
    t.parca(64, "#1e1e26", [P((55, 40), (73, 40), (72, 48), (64, 51), (56, 48))], golge="kure")  # yüz örtüsü
    gomlek_govde(t, "#3a3a44", z=40, alt=118)
    t.parca(44, "#2a2a34", [P((44, 56), (56, 50), (60, 140), (40, 146)), P((84, 56), (72, 50), (68, 140), (88, 146))],
            golge="silindir", doku=kivrim(6, 0.14))  # pelerinin önü
    bacak(t, "#2a2a30", z=22, ust=112, alt=158)
    cizme(t, "#1e1a1a", z=24)
    kusak(t, "#4a3a2a", z=46, y=88, kalin=4)
    kol(t, "#2a2a34", "gogus", ten=TEN_ACIK, z=50, eldiven="#3a2a22")
    kol(t, "#2a2a34", "yan", sag=True, ten=TEN_ACIK, z=50, eldiven="#3a2a22")
    t.parca(52, "#d8c8a0", [P((50, 84), (66, 82), (68, 96), (52, 98))], golge="duz", doku=kivrim(3, 0.1))  # harita
    t.cizgi(54, 88, 62, 92, "#a82a26", z=1001)
    t.cizgi(56, 94, 64, 86, "#5a4a3a", z=1001)
    t.parca(47, CELIK, [P((72, 92), (74, 92), (75, 112), (73, 116), (71, 112))], golge="silindir")  # hançer
    t.parca(47.5, "#3a2a22", [R(70, 86, 76, 92)], golge="duz")


def casit(t):
    """Çaşıt: düşman topraklarında köylü kılığında dolaşan Osmanlı gözcüsü; heybe, değnek, uyanık bakış."""
    bas(t, TEN_ESMER, sac="#3a2a1e", yas="orta", agiz="sert")
    biyik(t, "#3a2a1e", tur="pala")
    sakal(t, "#3a2a1e", tur="kisa")
    kalpak(t, renk="#5a4a3a", boy=10, doku_tohum=41)
    t.parca(12, "#7a6a4a", [P((60, 60), (88, 56), (92, 108), (68, 112))], golge="kure", doku=kivrim(4, 0.12))  # sırttaki heybe
    gomlek_govde(t, "#d8ccb0", z=40, alt=116)
    t.parca(44, "#6a4a32", [P((43, 58), (48, 52), (56, 50), (72, 50), (80, 52), (85, 58), (88, 128), (40, 128))], golge="silindir",
            doku=birlestir(kivrim(6, 0.12), yatay_cizgi(9, 0.08)))  # kepenek
    t.parca(45, "#d8ccb0", [P((58, 52), (70, 52), (68, 128), (60, 128))], golge="silindir")
    t.parca(46, "#5a3a22", [L((74, 52), (54, 100), w=3)], golge="silindir")  # heybe kayışı
    kusak(t, "#8a2a22", z=47, y=92, kalin=4)
    t.parca(47.5, CELIK, [P((60, 96), (62, 96), (62, 104), (61, 106), (60, 104))], golge="silindir")  # kuşakta saklı bıçak ucu
    bacak(t, "#a89a7a", z=22, ust=120, alt=160, doku=yatay_cizgi(3, 0.16))
    cizme(t, "#6a4a2e", z=24, kisa=True)
    kol(t, "#6a4a32", "yan", ten=TEN_ESMER, z=50)
    kol(t, "#6a4a32", "direk", sag=True, ten=TEN_ESMER, z=50)
    t.parca(49, "#8a6a42", [L((97, 54), (97, 166), w=3)], golge="silindir")
    t.parca(49.5, "#8a6a42", [L((97, 54), (92, 48), w=3)], golge="silindir")


def ermin(t, z, sekiller, golge="silindir"):
    t.parca(z, "#f0ece4", sekiller, golge=golge, desen=(["x...", "....", "..x.", "...."], "#1a1418", 4, 4))


def kral(t):
    """Macar kralı: kapalı kemerli taç, kakım kürklü kırmızı kral pelerini, asa ve küre."""
    bas(t, TEN_ACIK, sac="#6a4a2a", yas="orta", agiz="sert")
    sac_yanlar(t, "#6a4a2a", uzun=True)
    t.parca(30, "#6a4a2a", [P((52, 30), (76, 30), (78, 56), (50, 56))], golge="silindir", doku=kivrim(2, 0.12))
    biyik(t, "#6a4a2a", tur="ince")
    sakal(t, "#6a4a2a", tur="dolgun")
    t.parca(80, ALTIN, [P((54, 30), (74, 30), (74, 24), (54, 24))], golge="yatay")  # taç bandı
    t.parca(79, ALTIN, [L((55, 25), (58, 14), (64, 10), (70, 14), (73, 25), w=3)], golge="silindir")  # kemer
    t.parca(78.5, "#a82a26", [P((57, 24), (71, 24), (69, 15), (64, 12), (59, 15))], golge="kure")
    t.parca(81, ALTIN, [R(63, 2, 65, 10), R(61, 4, 67, 6)], golge="duz")  # eğik haç
    for x, r in ((58, "#2a8a5a"), (64, "#c8302a"), (70, "#2a4a8a")):
        t.parca(81, r, [C(x, 27, 1.6)], golge="kure", isik=0.15)
    t.parca(14, "#a82a26", [P((42, 52), (86, 52), (100, 164), (28, 164))], golge="silindir", doku=kivrim(9, 0.14))  # pelerin
    kaftan(t, "#2a3a7a", z=40, boy=162, etek=26, ic=ALTIN, ic_genis=4, desen=([".x.", "xxx", ".x."], ALTIN, 8, 8))
    ermin(t, 46, [P((42, 50), (86, 50), (84, 64), (64, 70), (44, 64))], golge="kure")  # kakım yaka
    kusak(t, ALTIN, z=48, y=88, kalin=4)
    cizme(t, "#3a2a20", z=24, kisa=True)
    kol(t, "#a82a26", "gogus", ten=TEN_ACIK, z=50, yen="#f0ece4")
    kol(t, "#a82a26", "direk", sag=True, ten=TEN_ACIK, z=50, yen="#f0ece4")
    t.parca(54, ALTIN, [C(58, 82, 6)], golge="kure")  # küre
    t.parca(54.5, ALTIN, [R(57, 72, 59, 78), R(55, 74, 61, 75)], golge="duz")
    t.parca(54.4, "#a82a26", [R(52, 81, 64, 82)], golge="duz", kontur=False)
    t.parca(49, ALTIN, [R(96, 50, 98, 112)], golge="silindir")  # asa
    t.parca(49.5, ALTIN, [P((97, 40), (102, 48), (97, 54), (92, 48))], golge="kure")
    t.parca(49.6, "#c8302a", [C(97, 47, 1.5)], golge="kure", isik=0.15)


def prens(t):
    """Prens: tüylü kadife bere, sırmalı kısa ceket, tek omuza atılmış kısa pelerin, ince kılıç."""
    with t.olcek(0.96):
        bas(t, TEN_ACIK, sac="#c8a050", agiz="duz")
        sac_yanlar(t, "#c8a050", uzun=True)
        t.parca(30, "#c8a050", [P((52, 30), (76, 30), (78, 52), (50, 52))], golge="silindir", doku=kivrim(2, 0.12))
        t.parca(80, "#2a1e2a", [E(48, 18, 80, 30)], golge="kure")  # bere
        t.parca(81, "#f4f0e8", [P((72, 22), (88, 12), (92, 6), (84, 18), (74, 26))], golge="silindir", doku=kivrim(2, 0.15))
        t.parca(81.5, ALTIN, [C(72, 24, 2)], golge="kure")
        t.parca(14, "#5a1e3a", [P((40, 52), (66, 52), (60, 120), (32, 116))], golge="silindir", doku=kivrim(6, 0.14))  # kısa pelerin
        gomlek_govde(t, "#2a5a3a", z=40, alt=106, desen=([".x", "x."], ALTIN, 6, 6))
        t.parca(41, "#2a5a3a", [P((46, 100), (82, 100), (86, 116), (42, 116))], golge="silindir", doku=kivrim(4, 0.12))  # etek
        t.parca(46, ALTIN, [L((52, 54), (64, 66), (76, 54), w=2)], golge="duz")  # altın zincir
        t.parca(46.5, ALTIN, [C(64, 68, 2.5)], golge="kure")
        kusak(t, "#3a2a20", z=48, y=96, kalin=4)
        bacak(t, "#a82a3a", z=22, ust=110, alt=154)
        cizme(t, "#2a1e1a", z=24)
        kilic(t, 76, 98, z=46, sag=True, kin="#2a1e1a")
        kol(t, "#2a5a3a", "bel", ten=TEN_ACIK, z=50, yen=ALTIN)
        kol(t, "#2a5a3a", "kilic", sag=True, ten=TEN_ACIK, z=50, yen=ALTIN)


def prenses(t):
    """Prenses: duvaklı uzun hennin, inci gerdanlık, sırmalı mavi gelinlik, elinde dua kitabı."""
    with t.olcek(0.95):
        bas(t, TEN_ACIK, sac="#a8783a", kadin=True, agiz="gulus")
        t.parca(10, "#f4f0f4", [P((76, -12), (90, 20), (94, 90), (82, 140), (74, 60), (68, 20))], golge="silindir",
                doku=kivrim(5, 0.14), isik=0.1)  # duvak
        t.parca(58, "#a8783a", [P((55, 34), (56, 27), (64, 25), (72, 27), (73, 34), (74, 50), (71, 34), (57, 34), (54, 50))],
                golge="kure", doku=kivrim(2, 0.1))
        t.parca(80, "#2a3a7a", [P((56, 30), (72, 30), (80, -14), (75, -16), (60, 18))], golge="silindir",
                desen=(["x"], ALTIN, 4, 5))  # hennin
        t.parca(81, ALTIN, [P((55, 26), (73, 26), (73, 31), (55, 31))], golge="yatay", desen=(["x."], "#f4f0ec", 2, 1))
        for x, y in ((58, 56), (61, 59), (64, 60), (67, 59), (70, 56)):
            t.parca(60, "#f4f0ec", [C(x, y, 1.3)], golge="kure", isik=0.2)
        kaftan(t, "#2a3a7a", z=40, boy=164, etek=34, ic=ALTIN, ic_genis=6, desen=(["x"], ALTIN, 5, 5))
        t.parca(41, "#2a3a7a", [P((CX - 34, 156), (CX + 34, 156), (CX + 38, 166), (CX - 38, 166))], golge="yatay")  # yere değen etek
        ermin(t, 44, [P((48, 52), (80, 52), (78, 58), (64, 64), (50, 58))], golge="kure")
        kusak(t, ALTIN, z=48, y=78, kalin=4, desen=(["x."], "#c8302a", 2, 1))
        kol(t, "#2a3a7a", "gogus", ten=TEN_ACIK, z=50, yen="#f0ece4")
        kol(t, "#2a3a7a", "gogus", sag=True, ten=TEN_ACIK, z=50, yen="#f0ece4")
        kitap(t, 64, 92, z=52, renk="#a82a26")


KADRO = [
    # HALK
    dict(ad="Rumeli Köylüsü", kod="koylu", ciz=koylu, sinif="Halk",
         aciklama="Toprağı işleyen reaya. Vergisi hazineyi, oğulları ocağı besler; zulüm görürse dağa çıkar."),
    dict(ad="Köylü Kadın", kod="koylu_kadin", ciz=koylu_kadin, sinif="Halk",
         aciklama="Köyün asıl yükünü taşıyan el. Hasat, ekmek, dokuma; köyün bereketi onun sepetinde."),
    dict(ad="Köy Çocuğu", kod="cocuk", ciz=cocuk, sinif="Halk",
         aciklama="Devşirme çağındaki çocuk. Bohçası annesinin elinden; yarın bir yeniçeri, belki bir vezir."),
    dict(ad="Raguzalı Tüccar", kod="tuccar", ciz=tuccar, sinif="Halk",
         aciklama="Adriyatik ile İstanbul arasında mal ve haber taşır. Defteri kılıçtan keskindir."),
    dict(ad="Bektaşi Dervişi", kod="dervis", ciz=dervis, sinif="Halk",
         aciklama="Ocağın manevi babası. Kışlada dua eder, yeniçeriye moral verir; sözü ağadan ağır basar."),
    dict(ad="Hayduk", kod="hayduk", ciz=hayduk, sinif="Halk",
         aciklama="Dağların kanun tanımaz adamı. Kervan basar, köylüyü korur; yanına çekilirse değerli bir müttefik."),
    dict(ad="Doğancı Avcı", kod="avci", ciz=avci, sinif="Halk",
         aciklama="Ormanı ve dağı en iyi bilen adam. Doğanıyla saraya av getirir, yolları ve geçitleri bilir."),
    # KAPIKULU
    dict(ad="Acemi Oğlan", kod="acemi_oglan", ciz=acemi_oglan, sinif="Kapıkulu",
         aciklama="Devşirmeyle gelip Türk ailelerinin yanında yetişen genç. Bahçede, inşaatta çalışır; sırası gelince ocağa geçer."),
    dict(ad="Yeniçeri Neferi", kod="yeniceri_neferi", ciz=yeniceri_neferi, sinif="Kapıkulu",
         aciklama="Ocağın belkemiği. Ak börkü, fitilli tüfeği ve yatağanıyla hem cephede hem kışlada söz sahibi."),
    dict(ad="Yeniçeri Çorbacısı", kod="corbaci", ciz=corbaci, sinif="Kapıkulu",
         aciklama="Bir ortanın komutanı. Askerin karnını doyurur, sesini dinler; isyan kazanı onun ortasında kaynar."),
    dict(ad="Yeniçeri Ağası", kod="yeniceri_agasi", ciz=yeniceri_agasi, sinif="Kapıkulu",
         aciklama="Ocağın başı. Padişaha en yakın asker; Ocak onu severse taht sağlam, sevmezse sallantıda."),
    dict(ad="Topçu", kod="topcu", ciz=topcu, sinif="Kapıkulu",
         aciklama="Kuşatmanın ustası. Barut lekeli önlüğü ve tokmağıyla surları dövecek topları hazırlar."),
    # TAŞRA VE SARAY
    dict(ad="Tımarlı Sipahi", kod="sipahi", ciz=sipahi, sinif="Taşra ve Saray",
         aciklama="Tımarının geliriyle atını, zırhını, askerini besleyen süvari. Ocağın en eski rakibi."),
    dict(ad="Deli", kod="deli", ciz=deli, sinif="Taşra ve Saray",
         aciklama="Pars postlu, kanatlı öncü süvari. Akınların en önünde; korkuyu düşmana o taşır."),
    dict(ad="Akıncı", kod="akinci", ciz=akinci, sinif="Taşra ve Saray",
         aciklama="Uç beylerinin hafif atlısı. Yayı ve palasıyla sınırın ötesine dalar, ganimetle döner."),
    dict(ad="Kadı", kod="kadi", ciz=kadi, sinif="Taşra ve Saray",
         aciklama="Kazanın hâkimi. Davaya bakar, vergiyi denetler; halkın şikâyeti önce onun kapısına gelir."),
    dict(ad="Rumeli Beylerbeyi", kod="beylerbeyi", ciz=beylerbeyi, sinif="Taşra ve Saray",
         aciklama="Balkanların en güçlü paşası. Sancak beylerini ve sipahileri sefere o çıkarır."),
    dict(ad="Sadrazam", kod="sadrazam", ciz=sadrazam, sinif="Taşra ve Saray",
         aciklama="Padişahın mutlak vekili. Mühr-i hümayun onda; divanı o toplar, seferde serdar o olur."),
    dict(ad="Padişah", kod="padisah", ciz=padisah, sinif="Taşra ve Saray",
         aciklama="Devletin başı. Cülus bahşişini dağıtan da, Ocağın öfkesine ilk hedef olan da odur."),
    dict(ad="Şehzade", kod="sehzade", ciz=sehzade, sinif="Taşra ve Saray",
         aciklama="Sancakta yetişen veliaht. Ocak onu tutarsa taht onundur; tutmazsa kardeşi."),
    dict(ad="Saray Hanımı", kod="saray_hanimi", ciz=saray_hanimi, sinif="Taşra ve Saray",
         aciklama="Sarayın görünmeyen gücü. Vakıf kurar, ittifak örer; bir fısıltısı sefer kararını değiştirebilir."),
    # HAÇLI CEPHESİ
    dict(ad="Voyvoda", kod="voyvoda", ciz=voyvoda, sinif="Karşı Cephe",
         aciklama="Tuna ötesi beyliklerin hükümdarı. Bir gün haraç öder, ertesi gün Haçlılarla yürür."),
    dict(ad="Macar Süvarisi", kod="macar_suvarisi", ciz=macar_suvarisi, sinif="Karşı Cephe",
         aciklama="Sınırın hızlı atlısı. Kanat biçimli kalkanı ve uzun mızrağıyla akıncıların ezelî rakibi."),
    dict(ad="Şövalye", kod="sovalye", ciz=sovalye, sinif="Karşı Cephe",
         aciklama="Tepeden tırnağa çelik. Haçlı ordusunun ağır vurucu gücü; yavaş ama durdurulması zor."),
    dict(ad="Kral", kod="kral", ciz=kral, sinif="Karşı Cephe",
         aciklama="Macar tacının sahibi. Haçlı ittifakının başı; soyluları birleştirebildiği kadar güçlü."),
    dict(ad="Prens", kod="prens", ciz=prens, sinif="Karşı Cephe",
         aciklama="Tahtın genç varisi. Şövalye romanlarıyla büyümüş; savaşı henüz bir turnuva sanıyor."),
    dict(ad="Prenses", kod="prenses", ciz=prenses, sinif="Karşı Cephe",
         aciklama="Bir evlilikle iki krallığı birleştirebilir. Barış masasında en değerli koz onun elinde."),
    # GÖLGELER
    dict(ad="Hain", kod="hain", ciz=hain, sinif="Gölgeler",
         aciklama="Divandaki kulak, düşmana açılan kapı. Altın kesesi dolu, sadakati satılık."),
    dict(ad="Casus", kod="casus", ciz=casus, sinif="Gölgeler",
         aciklama="Venedik ya da Viyana için çalışan gizli göz. Kalelerin planını çizer, ordunun yolunu satar."),
    dict(ad="Çaşıt", kod="casit", ciz=casit, sinif="Gölgeler",
         aciklama="Osmanlı'nın gözcüsü. Köylü kılığında düşman ülkesini gezer, ordunun gücünü ve yolunu haber verir."),
]

SINIF_RENK = {
    "Halk": dict(gok=("#2a3a3a", "#4a6a5a", "#a8a070", "#e8c890"), toprak="#5a4a32", vurgu="#7aa05a"),
    "Kapıkulu": dict(gok=("#1e2a44", "#3a4a6a", "#7a6a7a", "#d8a070"), toprak="#5a4a32", vurgu="#3a6ac8"),
    "Taşra ve Saray": dict(gok=("#2a1a2a", "#5a2a3a", "#a85a3a", "#e8b060"), toprak="#5a4430", vurgu="#d8a83a"),
    "Karşı Cephe": dict(gok=("#1a1a24", "#2a2a3a", "#5a4a5a", "#a87a6a"), toprak="#4a4038", vurgu="#c8302a"),
    "Gölgeler": dict(gok=("#0e0c16", "#1e1a30", "#3a2a4a", "#6a4a5a"), toprak="#3a3238", vurgu="#9a5ac8"),
}


def uret(cikti: Path):
    cikti.mkdir(parents=True, exist_ok=True)
    for k in KADRO:
        t = Tuval()
        k["ciz"](t)
        fig = t.ciz()
        fig.resize((fig.width * 4, fig.height * 4), 0).save(cikti / f"{k['kod']}_sprite.png")
        (cikti / "1x").mkdir(exist_ok=True)
        fig.save(cikti / "1x" / f"{k['kod']}.png")  # 3B voksel görüntüleyici bu ham boyutu okur
        r = SINIF_RENK[k["sinif"]]
        kart(fig, r["gok"], r["toprak"], r["vurgu"]).save(cikti / f"{k['kod']}.png")
    return cikti


if __name__ == "__main__":
    yol = uret(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "cikti")
    print("tamam:", yol)
