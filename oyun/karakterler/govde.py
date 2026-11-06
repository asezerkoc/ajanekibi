"""Ortak gövde parçaları: baş ve yüz, kollar, bacaklar, çizmeler, kaftan. Standart yetişkin koordinatları
(128x176 ızgara, ayak tabanı 167. satır, gövde ekseni x=64). Sol taraf için yazılır, sağ taraf aynalanır."""
from __future__ import annotations

from motor import CX, ZEMIN, C, E, L, P, R, kivrim, palet

TEN_ACIK = "#e2b48c"
TEN = "#d39e78"
TEN_ESMER = "#b88060"


def ay(x):
    return 2 * CX - x


def ayna(pts):
    return [(ay(x), y) for x, y in pts]


# ---------------------------------------------------------------- baş


def bas(t, ten=TEN, sac="#2a1a14", goz="#2a1a14", z=60, yas="genc", kulak=True, kadin=False, cocuk=False,
        kas=True, agiz="duz"):
    """Baş, kulaklar, boyun ve yüz ayrıntıları. yas: genc, orta, yasli."""
    t.parca(z, ten, [E(56, 25, 72, 47)], golge="kure")
    t.parca(z - 2, ten, [R(60, 44, 68, 54)], golge="silindir", isik=-0.15)  # boyun
    if kulak:
        t.parca(z - 1, ten, [E(54, 33, 58, 41)], golge="kure", isik=-0.05)
        t.parca(z - 1, ten, [E(70, 33, 74, 41)], golge="kure", isik=-0.1)
    p = palet(ten)
    sp = palet(sac)
    # gözler
    for gx, yon in ((59, 1), (67, -1)):
        t.px(gx, 36, "#f2ece0")
        t.px(gx + 1, 36, "#f2ece0")
        t.px(gx + (1 if yon == 1 else 0), 36, goz)
        t.cizgi(gx - 1, 35, gx + 2, 35, "#2a1612")
        if kadin:
            t.px(gx - 1 if yon == 1 else gx + 2, 34, "#2a1612")
    if kas:
        if yas == "yasli":
            kr = palet("#d8d0c4")[2]
        else:
            kr = sp[1]
        t.cizgi(58, 33, 61, 32, kr)
        t.cizgi(66, 32, 69, 33, kr)
    # burun
    t.px(64, 37, p[2])
    t.px(65, 38, p[1])
    t.px(65, 39, p[1])
    t.px(63, 40, p[0])
    t.px(65, 40, p[0])
    t.px(64, 39, p[3])
    # ağız
    dudak = palet("#b05a50")
    if agiz == "duz":
        t.cizgi(62, 43, 66, 43, dudak[1])
        t.px(63, 44, p[1])
        t.px(64, 44, p[1])
    elif agiz == "gulus":
        t.cizgi(62, 43, 66, 43, dudak[1])
        t.px(61, 42, dudak[1])
        t.px(67, 42, dudak[1])
    elif agiz == "sert":
        t.cizgi(62, 43, 66, 43, dudak[0])
    if kadin or cocuk:
        t.px(58, 39, palet("#e08070")[3])
        t.px(69, 39, palet("#e08070")[3])
    if yas == "yasli":
        t.cizgi(57, 38, 58, 40, p[1])
        t.cizgi(70, 38, 69, 40, p[1])
        t.px(61, 31, p[2])
        t.px(66, 31, p[2])
    elif yas == "orta":
        t.px(60, 39, p[1])
        t.px(68, 39, p[1])


def sac_yanlar(t, renk, z=59, uzun=False):
    """Başlığın altından görünen saç/favori."""
    alt = 46 if uzun else 38
    t.parca(z, renk, [P((55, 28), (58, 28), (58, alt - 4), (56, alt))], golge="duz", doku=kivrim(2, 0.1))
    t.parca(z, renk, [P((73, 28), (70, 28), (70, alt - 4), (72, alt))], golge="duz", doku=kivrim(2, 0.1), isik=-0.1)


def biyik(t, renk, z=64, tur="pala"):
    if tur == "pala":  # yeniçeri: gür, uçları aşağı kıvrık
        t.parca(z, renk, [P((59, 41), (64, 40), (69, 41), (73, 46), (71, 47), (67, 43), (64, 43), (61, 43), (57, 47), (55, 46))],
                golge="duz", doku=kivrim(2, 0.08))
    elif tur == "burma":  # uçları yukarı burulmuş
        t.parca(z, renk, [P((59, 41), (64, 40), (69, 41), (73, 39), (74, 37), (72, 42), (64, 43), (56, 42), (54, 37), (55, 39))],
                golge="duz")
    elif tur == "sarkik":  # voyvoda: uzun, aşağı sarkan
        t.parca(z, renk, [P((59, 41), (64, 40), (69, 41), (72, 50), (70, 52), (67, 43), (61, 43), (58, 52), (56, 50))],
                golge="duz", doku=kivrim(2, 0.1))
    else:  # ince
        t.parca(z, renk, [P((60, 41), (64, 40), (68, 41), (69, 43), (64, 42), (59, 43))], golge="duz")


def sakal(t, renk, z=63, tur="dolgun"):
    if tur == "dolgun":
        t.parca(z, renk, [P((56, 36), (58, 43), (61, 46), (67, 46), (70, 43), (72, 36), (72, 44), (69, 52), (64, 55), (59, 52), (56, 44))],
                golge="kure", doku=kivrim(2, 0.12))
    elif tur == "sivri":
        t.parca(z, renk, [P((56, 37), (58, 43), (61, 46), (67, 46), (70, 43), (72, 37), (71, 47), (66, 56), (64, 60), (62, 56), (57, 47))],
                golge="kure", doku=kivrim(2, 0.12))
    elif tur == "uzun":
        t.parca(z, renk, [P((56, 36), (58, 43), (61, 46), (67, 46), (70, 43), (72, 36), (72, 48), (68, 62), (64, 68), (60, 62), (56, 48))],
                golge="silindir", doku=kivrim(2, 0.14))
    elif tur == "kisa":
        t.parca(z, renk, [P((57, 40), (60, 46), (68, 46), (71, 40), (70, 47), (64, 51), (58, 47))], golge="kure", doku=kivrim(2, 0.08))


# ---------------------------------------------------------------- kollar


POZ = {
    # omuz, dirsek, bilek, el merkezi (sol taraf)
    "yan": ((47, 57), (43, 83), (41, 103), (40, 108)),
    "bel": ((47, 57), (34, 74), (44, 87), (47, 88)),
    "gogus": ((47, 57), (43, 82), (55, 90), (58, 90)),
    "direk": ((47, 57), (37, 80), (32, 94), (31, 97)),
    "kilic": ((47, 57), (44, 80), (50, 92), (52, 94)),
    "kaldir": ((47, 57), (38, 40), (36, 24), (36, 20)),
    "one": ((47, 57), (40, 78), (44, 98), (46, 101)),
    "sepet": ((47, 57), (38, 80), (34, 98), (34, 101)),
    "kabza": ((47, 57), (44, 82), (57, 93), (60, 94)),
    "omuz": ((47, 57), (40, 78), (50, 66), (54, 62)),
}


def kol(t, renk, poz="yan", sag=False, ten=TEN, z=50, eldiven=None, yen=None, kalin=10, el=True, doku=None):
    """Kol: üst kol, ön kol, isteğe bağlı yen (manşet) ve el. sag=True: sağ taraf (aynalı)."""
    o, d, b, e = POZ[poz]
    if sag:
        o, d, b, e = (ay(o[0]), o[1]), (ay(d[0]), d[1]), (ay(b[0]), b[1]), (ay(e[0]), e[1])
    isik = -0.12 if sag else 0.0
    t.parca(z, renk, [L(o, d, w=kalin)], golge="silindir", isik=isik, doku=doku or kivrim(4, 0.06))
    t.parca(z + 0.5, renk, [L(d, b, w=kalin - 1)], golge="silindir", isik=isik, doku=doku or kivrim(4, 0.06))
    if yen:
        t.parca(z + 0.7, yen, [L(((b[0] * 3 + d[0]) / 4, (b[1] * 3 + d[1]) / 4), b, w=kalin)], golge="silindir", isik=isik)
    if el:
        t.parca(z + 1, eldiven or ten, [C(e[0], e[1], 4.5)], golge="kure", isik=isik)
    return e


# ---------------------------------------------------------------- bacaklar ve ayakkabılar


def cizme(t, renk="#6a2a1e", z=20, kisa=False, uc=True):
    ust = 158 if kisa else 146
    sol = [(51, ust), (62, ust), (62, 167), (47 if uc else 50, 167), (49, 162)]
    t.parca(z, renk, [P(*sol)], golge="silindir")
    t.parca(z, renk, [P(*ayna(sol))], golge="silindir", isik=-0.1)


def bacak(t, renk, z=22, ust=90, alt=158, doku=None, ac=0):
    t.parca(z, renk, [L((58 - ac, ust), (56 - ac, alt), w=12)], golge="silindir", doku=doku)
    t.parca(z, renk, [L((70 + ac, ust), (72 + ac, alt), w=12)], golge="silindir", isik=-0.1, doku=doku)
    t.parca(z - 1, renk, [P((50 - ac, ust - 2), (78 + ac, ust - 2), (76, ust + 10), (52, ust + 10))], golge="silindir", doku=doku)


def gomlek_govde(t, renk, z=40, alt=94, genis=0, doku=None, desen=None, isik=0.0):
    g = genis
    t.parca(z, renk, [P((44 - g, 58), (48 - g, 52), (56, 50), (72, 50), (80 + g, 52), (84 + g, 58), (80 + g, alt), (48 - g, alt))], golge="silindir",
            doku=doku or kivrim(6, 0.08), desen=desen, isik=isik)


def kaftan(t, renk, z=40, boy=160, etek=26, ic=None, ic_genis=5, desen=None, doku=None, kontrast=1.0, isik=0.0):
    """Uzun, eteği genişleyen kaftan; ic: önden görünen iç entari şeridi."""
    t.parca(z, renk, [P((43, 58), (47, 52), (56, 50), (72, 50), (81, 52), (85, 58), (CX + etek, boy), (CX - etek, boy))], golge="silindir",
            doku=doku or kivrim(7, 0.12), desen=desen, kontrast=kontrast, isik=isik)
    if ic:
        t.parca(z + 1, ic, [P((CX - 3, 58), (CX + 3, 58), (CX + ic_genis, boy), (CX - ic_genis, boy))], golge="silindir",
                doku=kivrim(3, 0.06))


def kusak(t, renk, z=48, y=84, kalin=7, genis=0, desen=None, sarkan=False):
    t.parca(z, renk, [P((47 - genis, y), (81 + genis, y), (81 + genis, y + kalin), (47 - genis, y + kalin))], golge="yatay",
            doku=kivrim(3, 0.1, egim=1), desen=desen)
    if sarkan:
        t.parca(z + 0.2, renk, [P((72, y + kalin - 1), (77, y + kalin - 1), (78, y + 18), (73, y + 19))], golge="silindir",
                doku=kivrim(3, 0.1))


def kurk_yaka(t, renk, z=55, boy=160, etek=26):
    from motor import kurk
    t.parca(z, renk, [P((46, 51), (58, 51), (64, 60), (70, 51), (82, 51), (78, 58), (68, 66), (64, 70), (60, 66), (50, 58))],
            golge="kure", doku=kurk(3))
    t.parca(z - 0.5, renk, [L((60, 66), (CX - etek * 0.38, boy - 1), w=5)], golge="silindir", doku=kurk(4))
    t.parca(z - 0.5, renk, [L((68, 66), (CX + etek * 0.38, boy - 1), w=5)], golge="silindir", doku=kurk(5), isik=-0.1)
    t.parca(z - 0.6, renk, [P((CX - etek - 1, boy - 5), (CX + etek + 1, boy - 5), (CX + etek + 1, boy), (CX - etek - 1, boy))],
            golge="yatay", doku=kurk(6))


def salvar(t, renk, z=22, ust=100, alt=156, doku=None):
    """Bol şalvar: üstte geniş, çizme ağzında büzülür."""
    t.parca(z, renk, [P((49, ust), (64, ust), (63, alt - 6), (61, alt), (51, alt), (48, alt - 8), (46, ust + 20))], golge="silindir",
            doku=doku or kivrim(4, 0.12, egim=0.3))
    t.parca(z, renk, [P(*ayna([(49, ust), (64, ust), (63, alt - 6), (61, alt), (51, alt), (48, alt - 8), (46, ust + 20)]))],
            golge="silindir", isik=-0.1, doku=doku or kivrim(4, 0.12, egim=-0.3))
