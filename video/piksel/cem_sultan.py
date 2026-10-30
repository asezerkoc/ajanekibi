"""Cem Sultan'ın Zehirli Tıraşı: Piksel Tarih (@pikseltarihim), sahneler 90-105. Grafikerin tarifi
(teslimler/2026-10-30-1652-piksel-tarihim-pikseltarihim-icin-reels.md); kod tarafı sahneleri 72-87'den 90-105'e aldı (Kalender ile
çakışmasın) ve imza uyumsuzluklarını düzeltti. Kullanım: python3 -I video/piksel/cem_sultan.py [sahne numaraları]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ciz import agac, figur, hex2, piksel, sehir, yeni
from sahneler import gokyuzu, uzak, orta, on, sprite, duz
from timur_figur import kisi, bayezid, oturan, atli, otag, gemi, koy_evleri
from timur import (ic_mekan, mumluk, mangal, kandil, ates, su_ve_kiyi,
                   kalabalik)
from kayip_mezar import muhafiz

KARE = 24      # sprite kare sayısı (SKILL.md)
PAY = 135      # orta/ön plan yan payı (SKILL.md)
SIN = lambda f, k=1: math.sin(f * 2 * math.pi * k)


# --------------------------------------------------------------------------
# Ölçüm yardımcıları (yalnızca ciz.yeni + ciz.figur + PIL alfa kanalı).
# Yeni çizim fonksiyonu değildir: figürü boş bir yüzeye çizip piksellerini ölçer.
# Amaç: elle yazılmış koordinat yerine figürün kendi pikselinden türetmek.
# --------------------------------------------------------------------------
def _opak(img):
    """Opak piksel kümesi {(x, y)}."""
    px = img.getchannel("A").load()
    w, h = img.size
    return {(x, y) for y in range(h) for x in range(w) if px[x, y] > 0}


# --------------------------------------------------------------------------
# Tıraş sahnesi (72 ve 87 ortak kare çizimi)
# Cem minderde oturur (sola bakar), berber ayakta (sağa bakar).
# Ustura berberin elinin ucundan türetilir: kol oynayınca ustura da oynar.
# Parıltı NÖTR beyazdır (zehir olgu gibi gösterilmez).
# --------------------------------------------------------------------------
CEM_X, BERBER_X = 235, 203          # sprite yerel x (ayar noktası: yalnızca BERBER_X)
CEM = dict(govde="#7a1e22", bas="sarik", bas_renk="#e8e0d0", sakal="#2a1a12",
           minder="#8a2a2a")
BERBER = dict(govde="#7a6a4a", bas="sapka", bas_renk="#3a2a1a", sakal=None,
              kemer="#c8b890")


def _el_ucu(w, h, z, x, s, yon, kol):
    """Elin ucu: aynı poz kol=0 ve kol=kol ile çizilir; farkın yöne en uzak noktası el ucudur."""
    a = yeni(w, h)
    figur(a, kisi, x, z, s, yon=yon, kol=0.0, **BERBER)
    b = yeni(w, h)
    figur(b, kisi, x, z, s, yon=yon, kol=kol, **BERBER)
    fark = _opak(b) - _opak(a)
    if not fark:
        raise RuntimeError("Ustura: kol farkı bulunamadı, el ucu hesaplanamadı")
    return max(fark, key=lambda p: (yon * p[0], -p[1]))


def _yuz_denetimi(w, h, z, el, yon):
    """Bıçak ucu Cem'in yüzüne değmeli (-4..+8 px boşluk) ve yüz yüksekliğinde olmalı."""
    c = yeni(w, h)
    figur(c, oturan, CEM_X, z, 2.6, yon=-yon, **CEM)
    k = _opak(c)
    ust = min(y for _, y in k)
    alt = max(y for _, y in k)
    yuz = [x for x, y in k if y <= ust + 0.45 * (alt - ust)]
    uc_x = el[0] + yon * 9
    kenar = min(yuz) if yon == 1 else max(yuz)
    bosluk = (kenar - uc_x) * yon
    if not (-4 <= bosluk <= 8) or not (ust <= el[1] <= ust + 0.55 * (alt - ust)):
        raise RuntimeError(
            f"Ustura yüze hizalı değil: boşluk={bosluk}, el_y={el[1]}, "
            f"yüz_y=({ust}..{alt}). BERBER_X ayarını değiştir.")


def _ustura(t, el, yon, i, nabiz):
    ex, ey = el
    for k in range(-2, 3):                               # sap: elin içinde
        piksel(t, ex + yon * k, ey, hex2("#3a2414"))
    for k in range(3, 10):                               # bıçak: Cem'e doğru
        yy = ey - (k - 3) // 4
        piksel(t, ex + yon * k, yy, hex2("#dfe6ee"))
        piksel(t, ex + yon * k, yy - 1, hex2("#f4f8ff"))       # üst kenar ışığı
    if i % (KARE // nabiz) < 3:                          # nötr beyaz parıltı
        piksel(t, ex + yon * 10, ey - 3, hex2("#ffffff"))
        piksel(t, ex + yon * 9, ey - 3, hex2("#cfd8e4"))


def _tiras_kare(t, z, i, nabiz=2):
    f = i / KARE
    w, h = t.size
    mumluk(t, 125, z, f, 3)
    mangal(t, 305, z, f)
    figur(t, oturan, CEM_X, z, 2.6, yon=-1, **CEM)
    kol = 0.55 + 0.10 * SIN(f, 2)
    figur(t, kisi, BERBER_X, z, 2.6, yon=1, kol=kol, **BERBER)
    el = _el_ucu(w, h, z, BERBER_X, 2.6, 1, kol)
    _yuz_denetimi(w, h, z, el, 1)
    _ustura(t, el, 1, i, nabiz)


def sahne90():
    """Kanca: Napoli, 1495. Berber minderdeki Cem'i tıraş ediyor; ustura parlar (rivayet)."""
    ic_mekan(90, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a",
             pencere=("#2a3a5a", "#f4e0b0"),
             zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"), isik="#f8c060", hali=True)
    sprite(90, "karakter", 440, 170, KARE, lambda t, z, i: _tiras_kare(t, z, i, 2))


def sahne91():
    """Taht savaşı sonrası: yenilen Cem'in küçük kafilesi Bayezid'in otağından uzaklaşır."""
    gokyuzu(91, ["#4a4a7a", "#8a5a8a", "#d0708a", "#ee9a7c", "#f6c48a", "#f8dca4"],
            (150, 400, 30, ["#fff0c0", "#ffd890"]), [(380, 330, 26), (110, 300, 24)],
            ("#fff4e0", "#f4d0c0", "#d098a0"))
    uzak(91, ["#7a5a7a", "#6a4a6a"], ["#8a6a78", "#7a5a6a"],
         ["#8a6a5a", "#7a5a4a", "#6a4a3e"], dag_y=(350, 430))

    def ekle(img, z):
        # zemin: duz(588) / duz(590); otağ ve Bayezid düz çizgiye oturur
        kalabalik(img, duz(588), PAY + 170, PAY + 235, 16, 73, ("#2a5a3a", "#3a6a44"),
                  s=1.3, yon=1)
        figur(img, otag, PAY + 250, duz(588), 2.3, "#2a6a3a", "#e0b040", faz=0.0)
        figur(img, bayezid, PAY + 330, duz(590), 2.1, yon=1)

    orta(91, (528, 560), ["#8a7a4a", "#7a6a40", "#6a5a38", "#5a4c30", "#4a3e2a"],
         "#c8a860", ekle=ekle)
    on(91, ["#3a2e1e", "#4a3c26", "#5a4a30"], "#b89858")

    def kare(t, z, i):                   # z: son satıra basan zemin (632)
        f = i / KARE
        atlar = ((330, "#7a1e22", "sarik", "#e8e0d0"),       # Cem önde
                 (235, "#4a3a5a", "kalpak", "#3a2a1a"),
                 (150, "#4a3a5a", "kalpak", "#3a2a1a"))
        for j, (x, govde, bas, bas_renk) in enumerate(atlar):
            figur(t, atli, x, z, 2.9, 1, faz=(f + j * 0.37) % 1,
                  at_renk="#6b3f24", yele="#2b1a12", govde=govde, bas=bas,
                  bas_renk=bas_renk, sakal="#2a1a12", adim=0.45)

    sprite(91, "karakter", 520, 160, KARE, kare)


# --------------------------------------------------------------------------
# Sahne 74 (Rodos): TEK ölçü sistemi
#   KIYI_Y: deniz başlangıcı, surlu yapı ve şövalyelerin tabanı (orta plan, ızgara y)
#   SU_SPR: sprite içinde gemi su çizgisi; sprite h=170 -> alt 14 satır su (SU_SPR..169)
#   Kumsal yok: düz liman kıyısı. Kara şeridi KIYI_Y'nin üstünde (y 552-558 .. 580).
# --------------------------------------------------------------------------
KIYI_Y = 580
SU_SPR = 156
KALE_X0, KALE_X1 = 120, 235          # ızgara x (orta planda PAY + ...)
GEMI_X = 330                         # gemi sprite yerel x; ızgara x = sx - 270 + 330
SX_BAS, SX_SON = 330, 270            # sprite kayması (TSX x: [330, 270])


def _gemi_denetimi():
    """Gemi gövdesi su çizgisine ulaşmalı; gemi hareketin sonunda bile yapıdan uzak kalmalı."""
    for f in (0.0, 0.25, 0.5, 0.75):
        g = yeni(540, 170)
        figur(g, gemi, GEMI_X, SU_SPR, 2.0, -1, f)
        sol, ust, sag, alt = g.getchannel("A").getbbox()
        if alt < SU_SPR:
            raise RuntimeError(f"Gemi suya ulaşmıyor: alt={alt}, su_y={SU_SPR}")
        if SX_SON - 270 + sol < KALE_X1 + 20:
            raise RuntimeError(f"Gemi kıyıdaki yapıya karışıyor: sol={SX_SON - 270 + sol}")


def sahne92():
    """Rodos: kırmızı yelkenli kadırga taş surlu limana gelir; kıyıda şövalyeler."""
    gokyuzu(92, ["#5a8ac8", "#78a8d8", "#98c0e0", "#b8d4e8", "#d8e4e8"],
            (400, 330, 26, ["#fffbe8", "#fff0c0"]), [(130, 320, 26), (330, 290, 30)],
            ("#ffffff", "#e8eef4", "#c0cce0"))
    uzak(92, ["#7a9ab0", "#6a8aa0"], ["#8aa890", "#7a9880"],
         ["#6a9ab8", "#5a8aa8", "#4a7a98"], dag_y=(350, 430), tepe_y=450, ova_y=490)

    def ekle(img, z):
        su_ve_kiyi(img, KIYI_Y)                                  # KIYI_Y'den aşağısı deniz
        figur(img, sehir, PAY + KALE_X0, PAY + KALE_X1, duz(KIYI_Y), 1.3,
              duvar="#c0b8a8", golge="#8a8478", cati="#a8452e", tohum=74)
        for x in (PAY + 165, PAY + 205):                          # tabanları KIYI_Y
            figur(img, kisi, x, duz(KIYI_Y), 1.9, govde="#a8281e", bas="migfer",
                  bas_renk="#9aa2ac", sakal=None, yon=1, silah="mizrak")

    orta(92, (KIYI_Y - 28, KIYI_Y - 24),
         ["#6a8a7a", "#5a7a6a", "#4a6a5a", "#3e5a4e", "#324a40"], "#a8c0a0", ekle=ekle)
    on(92, ["#3e5a4e", "#4a6a5a", "#5a7a6a"], "#a8c0a0", boy=120)   # kıyı kamışı

    _gemi_denetimi()

    def kare(t, z, i):
        f = i / KARE
        figur(t, gemi, GEMI_X, SU_SPR, 2.0, -1, f)    # gövde su çizgisine oturur, alt kısmı batık
        su_ve_kiyi(t, SU_SPR)                          # alt 14 satır su: son satır opak

    sprite(92, "karakter", 540, 170, KARE, kare)


def sahne93():
    """Elden ele: Rodos, Fransa, Roma görevlileri arasında yürüyen Cem."""
    ic_mekan(93, duvar=("#2e2a2e", "#3a3238", "#4a3e44"), kemer="#1a1418", cini="#5a3a6a",
             zemin_renk=("#4a4440", "#3e3834", "#322e2c"), isik="#f8c060", hali=False)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 150, 0, f)
        kandil(t, 390, 0, f)
        figur(t, kisi, 170, z, 2.6, govde="#a8281e", bas="migfer", bas_renk="#9aa2ac",
              sakal=None, yon=1, adim=(f + 0.2) % 1, silah="mizrak")        # Rodos
        figur(t, kisi, 245, z, 2.6, govde="#7a1e22", bas="sarik", bas_renk="#e8e0d0",
              sakal="#2a1a12", yon=1, adim=f)                               # Cem
        figur(t, kisi, 320, z, 2.6, govde="#2a4a9a", bas="migfer", bas_renk="#aab2bc",
              sakal=None, yon=1, adim=(f + 0.55) % 1, silah="mizrak")       # Fransa
        figur(t, kisi, 395, z, 2.6, govde="#d8b040", bas="sapka", bas_renk="#a8281e",
              sakal=None, yon=1, adim=(f + 0.8) % 1, silah="mizrak")        # Roma

    sprite(93, "karakter", 540, 170, KARE, kare)


def sahne94():
    """Umut: akşam penceresine bakan Cem; tek mum."""
    ic_mekan(94, duvar=("#2a2630", "#342e3a", "#403848"), kemer="#1a1620", cini="#3a4a6a",
             pencere=("#3a5a8a", "#f4e0b0"),
             zemin_renk=("#4a4048", "#3e363e", "#322c34"), isik="#e8a860", hali=False)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 60, z, f, 1)
        figur(t, kisi, 150, z, 2.8, govde="#7a1e22", bas="sarik", bas_renk="#e8e0d0",
              sakal="#2a1a12", yon=1, kol=0.05 + 0.03 * SIN(f))

    sprite(94, "karakter", 300, 170, KARE, kare)


def sahne95():
    """Hediye yollar: İstanbul surları önünde Bayezid; mızraklı elçi Roma'ya (sola) gider."""
    gokyuzu(95, ["#6a9ad0", "#88b0dc", "#a8c8e4", "#c4d8e8", "#e0e4dc"],
            (110, 330, 26, ["#fffbe8", "#fff0c0"]), [(380, 300, 28), (150, 340, 22)],
            ("#ffffff", "#e8eef4", "#c0cce0"))
    uzak(95, ["#8aa0b0", "#7a90a0"], ["#9ab098", "#8aa088"],
         ["#a0a878", "#90985e", "#80884e"], dag_y=(350, 430))

    def ekle(img, z):
        figur(img, sehir, PAY + 20, PAY + 300, duz(588), 1.6, tohum=77)
        figur(img, bayezid, PAY + 260, duz(590), 2.4, yon=-1, kol=0.6)

    orta(95, (528, 560), ["#8a9a58", "#7a8a4e", "#6a7a44", "#5a6a3a", "#4a5a30"],
         "#c0cc88", ekle=ekle)
    on(95, ["#4a5a30", "#5a6a3a", "#6a7a44"], "#c0cc88")

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 175, z, 2.9, -1, faz=f, govde="#2a6a3a", bas="sarik",
              bas_renk="#f4f0e6", sakal="#2a1a12", silah="mizrak", bayrak="#e8d8a0",
              adim=0.7)                                                      # elçi (önde, solda)
        figur(t, atli, 285, z, 2.9, -1, faz=(f + 0.37) % 1, govde="#3a4a3a",
              bas="kalpak", bas_renk="#3a2a1a", sakal="#2a1a12", adim=0.7)   # eşlikçi

    sprite(95, "karakter", 420, 170, KARE, kare)


# Roma odası: sahne 78 ve 83 aynı paleti kullanır
def _roma_odasi(no):
    ic_mekan(no, duvar=("#4a3a30", "#5a4638", "#6a5440"), kemer="#3a2a20", cini="#8a2a2a",
             pencere=("#6a9ad0", "#fff4d8"),
             zemin_renk=("#6a5a4a", "#5a4c3e", "#4a3e32"), isik="#f8c060", hali=True)


def sahne96():
    """Roma, 31 Mayıs 1492: Burchard yazar; diz çökmüş elçi Kutsal Mızrak'ı uzatır."""
    _roma_odasi(96)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 100, z, f, 3)
        mumluk(t, 320, z, f, 1)
        figur(t, kisi, 170, z, 2.7, govde="#1a1a22", bas="sapka", bas_renk="#2a1a22",
              sakal=None, yon=1, silah="mektup", kol=0.30 + 0.08 * SIN(f))   # Burchard
        figur(t, kisi, 270, z, 2.7, govde="#2a6a3a", bas="sarik", bas_renk="#f4f0e6",
              sakal="#2a1a12", yon=-1, diz=True, silah="mizrak", kol=0.6)    # elçi: mızrak elde, koordinatsız

    sprite(96, "karakter", 400, 170, KARE, kare)


def sahne97():
    """Hediye mi, pazarlık mı? Solda Cem ve muhafızlar, sağda mızrağı tutan Papa."""
    ic_mekan(97, duvar=("#3a2a30", "#4a3640", "#5a4450"), kemer="#2a1a20", cini="#8a6a2a",
             zemin_renk=("#5a4a4a", "#4a3c3c", "#3e3030"), isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        ust = duz(z[0] - 12, 520)             # arka sıra daha yüksek zeminde
        for x in (140, 210):
            figur(t, muhafiz, x, ust, 2.3, faz=f, mizrak=True, mesale=False, deel="#2a2a3a")
        figur(t, kisi, 175, ust, 2.3, govde="#7a1e22", bas="sarik", bas_renk="#e8e0d0",
              sakal="#2a1a12", yon=1)                                         # Cem
        mumluk(t, 280, z, f, 3)
        figur(t, kisi, 360, z, 2.9, govde="#f2eee4", bas="tac", bas_renk="#e0b040",
              sakal="#d8d0c8", yon=-1, silah="mizrak", kol=0.15 + 0.05 * SIN(f),
              pelerin="#8a1e22")                                              # Papa

    sprite(97, "karakter", 520, 170, KARE, kare)


def sahne98():
    """Ocak 1495: Cem papalık görevlilerinden Fransız süvarilerine doğru yürür."""
    gokyuzu(98, ["#6a7a9a", "#8a96b0", "#a8b0c0", "#c4c8d0", "#d8d8d8"], None,
            [(120, 320, 28), (400, 300, 30)], ("#e8ecf0", "#c8ccd8", "#a0a8b8"))
    uzak(98, ["#8a94a8", "#7a849a"], ["#98a0b0", "#8a92a4"],
         ["#7a8068", "#6a7058", "#5a604a"], dag_y=(350, 430))

    def ekle(img, z):
        # Roma surları: nötr surlu şehir, düz zemine (duz(588))
        figur(img, sehir, PAY + 40, PAY + 300, duz(588), 1.6,
              duvar="#b8a890", golge="#8a7a68", cati="#8a5a46", tohum=80)

    orta(98, (528, 560), ["#7a8068", "#6a7058", "#5a604a", "#4c523e", "#3e4432"],
         "#a8b090", ekle=ekle)
    on(98, ["#4c523e", "#5a604a", "#6a7058"], "#a8b090")

    def kare(t, z, i):
        f = i / KARE
        for x in (125, 160):
            figur(t, kisi, x, z, 2.7, govde="#d8b040", bas="sapka", bas_renk="#a8281e",
                  sakal=None, yon=1, silah="mizrak")                          # papalık
        figur(t, kisi, 215, z, 2.7, govde="#7a1e22", bas="sarik", bas_renk="#e8e0d0",
              sakal="#2a1a12", yon=1, adim=f)                                 # Cem yürür
        figur(t, atli, 365, z, 2.9, -1, dur=True, govde="#2a4a9a", bas="migfer",
              bas_renk="#aab2bc", zirh="#9aa2ac", bayrak="#2a4a9a")           # arkadaki süvari
        figur(t, atli, 300, z, 2.9, -1, dur=True, govde="#2a4a9a", bas="tac",
              bas_renk="#e0b040", sakal="#5a3a22", zirh="#9aa2ac", bayrak="#2a4a9a")  # Fransa Kralı

    sprite(98, "karakter", 500, 170, KARE, kare)


def sahne99():
    """Napoli, Şubat 1495 gecesi: surlu yapı ve meşaleli nöbetçiler. Ölüm gösterilmez."""
    gokyuzu(99, ["#0a0e24", "#141a3a", "#1e2a50", "#2a3a62", "#3a4a74"],
            (400, 360, 22, ["#f4f0e0", "#c8d0e0"]), [(140, 330, 26)],
            ("#6a7a9a", "#4a5a7a", "#2a3a5a"), yildiz=90)
    uzak(99, ["#1a2240", "#141c38"], ["#202a48", "#1a2240"],
         ["#1a2438", "#141c2e", "#101828"], dag_y=(360, 440))

    def ekle(img, z):
        figur(img, sehir, PAY + 90, PAY + 450, duz(588), 1.9,
              duvar="#4a4e5a", golge="#2a2e3a", cati="#3a3040", tohum=81)

    orta(99, (530, 560), ["#1e2a24", "#18241e", "#141e18", "#101a14", "#0c140e"],
         "#3a4a44", ekle=ekle)
    on(99, ["#0c140e", "#141e18", "#18241e"], "#3a4a44")

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((90, 210)):
            figur(t, muhafiz, x, z, 2.6, faz=(f + j * 0.37) % 1, mizrak=True,
                  mesale=True, deel="#2a2a3a")

    sprite(99, "karakter", 300, 170, KARE, kare)


def sahne100():
    """Guicciardini yazar: çalışma odası, mumlar; olaydan yaklaşık kırk yıl sonra."""
    ic_mekan(100, duvar=("#2e2a30", "#3a343c", "#48404a"), kemer="#1e1a20", cini="#6a2a2a",
             pencere=("#2a3a5a", "#f4d8a0"),
             zemin_renk=("#5a4a42", "#4a3c36", "#3e3230"), isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 110, z, f, 3)
        mumluk(t, 310, z, f, 2)
        figur(t, kisi, 210, z, 2.8, govde="#6a2a2a", bas="sapka", bas_renk="#2a1a1a",
              sakal=None, yon=1, silah="mektup", kol=0.35 + 0.10 * SIN(f, 2))

    sprite(100, "karakter", 420, 170, KARE, kare)


def sahne101():
    """Burchard'ın sessizliği: Roma odasında günlüğüne yazan Burchard (Napoli'de değil)."""
    _roma_odasi(101)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 80, z, f, 3)
        mumluk(t, 270, z, f, 2)
        figur(t, kisi, 170, z, 2.7, govde="#1a1a22", bas="sapka", bas_renk="#2a1a22",
              sakal=None, yon=1, silah="mektup", kol=0.30 + 0.08 * SIN(f))

    sprite(101, "karakter", 340, 170, KARE, kare)


def sahne102():
    """'Hastalık der': nötr Napoli penceresi, akşam ışığı; odada kimse yok, hastalık çizilmez."""
    ic_mekan(102, duvar=("#2a2a30", "#34343c", "#403e48"), kemer="#1a1a20", cini="#2a4a6a",
             pencere=("#3a5a8a", "#f4d8a0"),
             zemin_renk=("#4a4440", "#3e3834", "#322e2c"), isik="#e8b060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 150, 0, f)
        mumluk(t, 80, z, f, 3)
        mumluk(t, 220, z, f, 1)

    sprite(102, "karakter", 300, 170, KARE, kare)


def sahne103():
    """Belge yok: iki kaynak yan yana; ortada gri silüet halinde tıraş rivayeti (ustura çizilmez)."""
    ic_mekan(103, duvar=("#2e3036", "#383a42", "#444650"), kemer="#1e2026", cini="#4a5a6a",
             zemin_renk=("#4a4a4e", "#3e3e42", "#323236"), isik="#d8d0b0", hali=False)

    def kare(t, z, i):
        f = i / KARE
        ust = duz(z[0] - 12, 440)
        figur(t, oturan, 225, ust, 2.0, govde="#6a6a72", bas="sarik", bas_renk="#9a9aa2",
              sakal="#4a4a52", yon=-1)                                    # gri silüet: rivayet
        figur(t, kisi, 180, ust, 2.0, govde="#5a5a62", bas="sapka", bas_renk="#4a4a52",
              sakal=None, yon=1, kol=0.5)
        figur(t, kisi, 105, z, 2.8, govde="#1a1a22", bas="sapka", bas_renk="#2a1a22",
              sakal=None, yon=1, silah="mektup", kol=0.2 + 0.05 * SIN(f))   # Burchard
        figur(t, kisi, 335, z, 2.8, govde="#6a2a2a", bas="sapka", bas_renk="#2a1a1a",
              sakal=None, yon=-1, silah="mektup", kol=0.2 + 0.05 * SIN(f))  # Guicciardini

    sprite(103, "karakter", 440, 170, KARE, kare)


def sahne104():
    """Halk anlatısı: alacakaranlık köyde ateş başında dinleyiciler, ayakta anlatıcı."""
    gokyuzu(104, ["#2a2a5a", "#5a3a6a", "#a05a78", "#d88a7a", "#f0b088", "#f4c898"],
            (420, 410, 26, ["#fff0c0", "#ffd890"]), [(130, 330, 24), (330, 300, 26)],
            ("#f4e0d0", "#d8a8b0", "#a07890"), yildiz=50)
    uzak(104, ["#5a4a6a", "#4a3c5a"], ["#6a5a6a", "#5a4a5a"],
         ["#6a5a4e", "#5a4a40", "#4a3c32"], dag_y=(350, 430))

    def ekle(img, z):
        figur(img, koy_evleri, PAY + 60, PAY + 330, duz(588), 1.5, tohum=86)
        figur(img, agac, PAY + 360, duz(590), 2.0, tohum=86)

    orta(104, (528, 560), ["#6a6a3e", "#5a5a36", "#4a4a2e", "#3e3e28", "#323220"],
         "#b8a860", ekle=ekle)
    on(104, ["#323220", "#3e3e28", "#4a4a2e"], "#b8a860")

    def kare(t, z, i):
        f = i / KARE
        ates(t, 190, z, f, 1.0)
        for x, yon, renk in ((100, 1, "#3a5a8a"), (140, 1, "#6a3a2a"),
                             (240, -1, "#3a6a4a"), (285, -1, "#7a5a2a")):
            figur(t, oturan, x, z, 2.2, govde=renk, bas="bork", bas_renk="#5a3a22",
                  sakal=None, yon=yon)
        figur(t, kisi, 322, z, 2.5, govde="#6a4a2a", bas="bork", bas_renk="#5a3a22",
              sakal="#d8d0c8", yon=-1, kol=0.55 + 0.25 * SIN(f))           # anlatıcı

    sprite(104, "karakter", 380, 150, KARE, kare)


def sahne105():
    """Soru: tıraş odası bu kez gece penceresiyle; ustura yavaş parlar (kapanış)."""
    ic_mekan(105, duvar=("#2a2020", "#382a28", "#463430"), kemer="#1a1210", cini="#1e4a7a",
             pencere=("#0e1630", "#f4f8ff"),
             zemin_renk=("#4a3c32", "#3e322a", "#322822"), isik="#f8c060", hali=True)
    sprite(105, "karakter", 440, 170, KARE, lambda t, z, i: _tiras_kare(t, z, i, 1))


SAHNELER = {90: sahne90, 91: sahne91, 92: sahne92, 93: sahne93, 94: sahne94,
            95: sahne95, 96: sahne96, 97: sahne97, 98: sahne98, 99: sahne99,
            100: sahne100, 101: sahne101, 102: sahne102, 103: sahne103, 104: sahne104,
            105: sahne105}

if __name__ == "__main__":
    import sys
    for n in ([int(a) for a in sys.argv[1:]] or sorted(SAHNELER)):
        SAHNELER[n]()
