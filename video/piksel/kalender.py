"""Timur'un Soyundan Kalender (Bâbür Kalender Mîrzâ) — sahneler 72-89. Grafikerin tarifi (teslimler/2026-10-29-...-grafiker.md),
kod tarafı imza uyumsuzluklarını düzeltti. Kullanım: python3 -I video/piksel/kalender.py [sahne numaraları]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import ImageDraw  # noqa: E402

from ciz import agac, cicek, cicekler, duman, figur, hex2, orta_asya_sehri, piksel, taslar, tug, yurt  # noqa: E402
from sahneler import GW, KARE, PAY, duz, gokyuzu, on, orta, sprite, uzak  # noqa: E402
from timur import abanoz_tabut, ic_mekan, kalabalik, kandil, mangal, mumluk  # noqa: E402
from timur_figur import anadolu_kalesi, atli, gur_i_emir, kisi, oturan, sedir, timur  # noqa: E402


def rahle(t, x, y, s=1.0, kagit=True):
    """Alçak yazı rahlesi: iki çapraz ayak zemine basar, üstünde eğik tahta ve kâğıt."""
    d = ImageDraw.Draw(t)
    k = hex2("#5a3a1e")
    d.line([x - int(3 * s), y - 1, x + int(2 * s), y - int(4.5 * s)], fill=k, width=max(1, int(0.8 * s)))
    d.line([x + int(3 * s), y - 1, x - int(2 * s), y - int(4.5 * s)], fill=k, width=max(1, int(0.8 * s)))
    d.polygon([(x - int(4 * s), y - int(4 * s)), (x + int(4 * s), y - int(5.5 * s)), (x + int(4 * s), y - int(4.5 * s)),
               (x - int(4 * s), y - int(3 * s))], fill=hex2("#7a5a34"), outline=hex2("#2a1a10"))
    if kagit:
        d.polygon([(x - int(3 * s), y - int(4.6 * s)), (x + int(3 * s), y - int(5.8 * s)), (x + int(3 * s), y - int(5.2 * s)),
                   (x - int(3 * s), y - int(4 * s))], fill=hex2("#f0e6d0"))
        d.line([x - int(2 * s), y - int(4.8 * s), x + int(2 * s), y - int(5.5 * s)], fill=hex2("#3a2414"))


def kitaplar(t, x, y, s=1.0):
    """Yere yığılmış üç kitap: en alttaki zemine basar."""
    d = ImageDraw.Draw(t)
    for k, renk in enumerate(("#8a2a2a", "#2a5a8a", "#c8a040")):
        yy = y - int(k * 1.6 * s)
        d.rectangle([x - int(3 * s), yy - int(1.6 * s), x + int(3 * s), yy - 1], fill=hex2(renk), outline=hex2("#2a1a10"))


# ---------------------------------------------------------------- 72
def sahne72():
    """Kanca: tahtta Kalender; solda kılıçlı muhafız, sağda yazan kâtip. İç mekân, kandil + mum."""
    ic_mekan(72, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a",
             pencere=("#1a2a4a", "#f8e0a0"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 270, 0, f, 64)
        mumluk(t, 160, z, f, 3)
        mumluk(t, 385, z, (f + 0.3) % 1, 3)
        ust = figur(t, sedir, 270, z, 3.6, renk="#c8a040", ortu="#8a1e22")     # taht: sedir (tabanı z)
        figur(t, oturan, 270, duz(ust, t.width), 3.0, govde="#6a7a5a", bas="sarik",
              bas_renk="#e8e0cc", sakal="#2a1a12", el="kalem", minder="#8a2a2a")
        figur(t, kisi, 205, z, 3.0, govde="#7a1e22", bas="migfer", bas_renk="#9aa2ac",
              yon=1, silah="kilic", kol=0.15)                                   # kılıç tarafı (kadraj içi)
        rahle(t, 322, z[0], 2.8)
        figur(t, oturan, 340, z, 2.8, govde="#3a5a8a", bas="bork", bas_renk="#5a3a22",
              sakal="#2a1a12", yon=-1, el="kalem", minder="#6a3a2a")            # şiir tarafı: kâtip rahlede yazar

    sprite(72, "karakter", 540, 200, KARE, kare)


# ---------------------------------------------------------------- 73
def sahne73():
    """Herat: Timur (ata) ve tahtta oğlu Şahruh; arkada Herat silüeti ve türbe. Altın saat."""
    gokyuzu(73, ["#5a5a98", "#8a78a8", "#d09aa0", "#f0b890", "#f8d8a0", "#fce8b8"],
            None, [],
            ("#fff4e0", "#f4dcc8", "#d8a8a0"))
    uzak(73, ["#7a6a98", "#8a7aa0"], ["#9a82a0", "#a88aa0"], ["#c89a98", "#b88a90", "#a87a84"],
         dag_y=(400, 455), tepe_y=462)
    orta(73, (524, 558), ["#a8885a", "#987a50", "#887048", "#78603e", "#685036"], "#d8b878",
         ekle=lambda img, z: [
             figur(img, orta_asya_sehri, PAY + 10, PAY + 330, duz(588), 2.2, tohum=73),
             figur(img, gur_i_emir, PAY + 345, duz(588), 1.4)])
    on(73, ["#685036", "#887048", "#78603e"], "#d8b878")

    def kare(t, z, i):
        f = i / KARE
        figur(t, tug, 182, z, 1.5, f)                                              # flamalar dalgalanır
        figur(t, timur, 222, z, 3.0, 1, silah="kilic",
              kol=0.25 + 0.1 * math.sin(f * 2 * math.pi), yasli=True)
        ust = figur(t, sedir, 332, z, 3.0, renk="#8a6a3a", ortu="#2a6a3a")
        figur(t, oturan, 332, duz(ust, t.width), 2.7, govde="#2a6a3a", bas="sorguc",
              bas_renk="#e0b040", sakal="#2a1a12", yon=-1)

    sprite(73, "karakter", 540, 170, KARE, kare)


# ---------------------------------------------------------------- 74
def sahne74():
    """Baysungur'un akademisi: hattat, nakkaş, müzehhip; Baysungur ve çocuk Bâbür. İç mekân, kandil."""
    ic_mekan(74, duvar=("#4a3626", "#5a4430", "#6a5238"), kemer="#2a1a14", cini="#2a8a8a",
             pencere=("#b88a50", "#e8d0a0"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 215, 0, f, 56)
        kandil(t, 335, 0, (f + 0.4) % 1, 56)
        for x, govde, bas, bas_renk, minder in ((192, "#8a3a2a", "#2a1a12", None, "#8a2a2a"), (248, "#2a6a5a", None, None, "#6a4a2a"),
                                                (304, "#6a4a8a", "#2a1a12", None, "#2a4a6a")):
            rahle(t, x + 11, z[0], 2.6)                                            # her ustanın önünde rahle ve kâğıt
            figur(t, oturan, x, z, 2.8, govde=govde, bas="sarik" if x != 248 else "bork",
                  bas_renk="#e8e0cc" if x != 248 else "#5a3a22", sakal=bas, el="kalem", minder=minder)
        kitaplar(t, 176, z[0], 2.2)
        kitaplar(t, 318, z[0], 1.8)
        figur(t, kisi, 336, z, 3.0, govde="#2a3a6a", bas="sorguc", bas_renk="#e0b040",
              sakal="#2a1a12", yon=-1, kol=0.2 + 0.1 * math.sin(f * 2 * math.pi))   # Baysungur
        figur(t, kisi, 356, z, 2.1, govde="#8a7a5a", bas="bork", bas_renk="#5a3a22",
              yon=-1)                                                               # çocuk Bâbür (kadraj içi)

    sprite(74, "karakter", 540, 200, KARE, kare)


# ---------------------------------------------------------------- 75
def sahne75():
    """Baysungur'un cenazesi: omuzlarda abanoz tabut, önde çocuk Bâbür. Alacakaranlık."""
    gokyuzu(75, ["#3a3a6a", "#6a5a88", "#a87a8a", "#d8908a", "#e8b090", "#f0c8a0"],
            None, [],
            ("#f0d8d0", "#d8b0b0", "#a88090"))
    uzak(75, ["#5a5a88", "#6a6a90"], ["#7a6a88", "#8a7088"], ["#8a6a78", "#7a5a6a", "#6a4a5c"],
         dag_y=(400, 455), tepe_y=462)
    orta(75, (526, 560), ["#6a5a58", "#5a4a4c", "#4a3c40", "#3c3036", "#30262c"], "#9a8078",
         ekle=lambda img, z: [
             figur(img, orta_asya_sehri, PAY + 260, PAY + 560, duz(588), 2.0, tohum=75),
             kalabalik(img, duz(596), PAY + 20, PAY + 230, 26, 75, ("#2a2430", "#3a3038"),
                       s=1.1, yon=1)])
    on(75, ["#30262c", "#4a3c40", "#3c3036"], "#9a8078")

    def kare(t, z, i):
        f = i / KARE
        abanoz_tabut(ImageDraw.Draw(t), 178, 338, z[0] - 20)  # göğüs-omuz hizası: başlar tabutun üstünde görünür
        for j, x in enumerate((180, 225, 285, 325)):                               # taşıyıcılar
            figur(t, kisi, x, z, 2.6, govde="#24202c", bas="bork", bas_renk="#2a2420",
                  yon=1, adim=(f + (j % 2) * 0.5) % 1)
        figur(t, kisi, 362, z, 2.1, govde="#3a3a5a", bas="bork", bas_renk="#5a3a22",
              yon=1, adim=f)                                                        # çocuk Bâbür, önde ve kadraj içi

    sprite(75, "karakter", 540, 170, KARE, kare)


# ---------------------------------------------------------------- 76
def sahne76():
    """Herat sarayı avlusu: asalı derviş şehzade yürür, saray ehli bakar. Gündüz."""
    gokyuzu(76, ["#7aa0c8", "#a8c0d0", "#d8d0c0", "#f4dcb0", "#f8e4b8"],
            None, [],
            ("#fff8ec", "#f4e4d0", "#d8c4b0"))
    uzak(76, ["#8a9ab0", "#9aa8b8"], ["#a8b4a0", "#b4bc9c"], ["#c4c090", "#b4b080", "#a4a070"],
         dag_y=(400, 455), tepe_y=462)
    orta(76, (524, 558), ["#b8a870", "#a89860", "#988850", "#887842", "#786838"], "#e0d090",
         ekle=lambda img, z: [
             figur(img, orta_asya_sehri, PAY + 10, PAY + 520, duz(588), 2.4, tohum=76),
             kalabalik(img, duz(596), PAY + 60, PAY + 420, 38, 76,
                       ("#8a2a2a", "#2a5a8a", "#2a6a3a", "#8a6a2a"), s=1.7, yon=1),
             figur(img, agac, PAY + 590, duz(592), 1.6)])
    on(76, ["#786838", "#988850", "#887842"], "#e0d090")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 150, z, 3.0, govde="#8a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=1, adim=f, silah="sopa")                         # derviş şehzade, asalı

    sprite(76, "karakter", 300, 170, KARE, kare)


# ---------------------------------------------------------------- 77
def sahne77():
    """Kalender yazar, Câmî muamma risalesini uzatır. İç mekân, gece penceresi, kandil + mum."""
    ic_mekan(77, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a",
             pencere=("#1a2a4a", "#f4f8ff"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 270, 0, f, 60)
        mumluk(t, 270, z, f, 3)
        rahle(t, 205, z[0], 2.8)
        figur(t, oturan, 190, z, 3.0, govde="#6a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=1, el="kalem", minder="#8a2a2a")                 # Kalender rahlede yazar
        figur(t, kisi, 340, z, 3.0, govde="#2a4a6a", bas="sarik", bas_renk="#f4f0e6",
              sakal="#e8e4dc", yon=-1, silah="mektup",
              kol=0.35 + 0.2 * math.sin(f * 2 * math.pi))                           # Câmî

    sprite(77, "karakter", 540, 190, KARE, kare)


# ---------------------------------------------------------------- 78
def sahne78():
    """Kapıda sadaka (rivayet): Kalender yoksula altın verir. Öğleden sonra."""
    gokyuzu(78, ["#7aa0c8", "#a8c0d0", "#d8d0c0", "#f4dcb0", "#f8e4b8"],
            None, [],
            ("#fff8ec", "#f4e4d0", "#d8c4b0"))
    uzak(78, ["#8a9ab0", "#9aa8b8"], ["#a8b4a0", "#b4bc9c"], ["#c4c090", "#b4b080", "#a4a070"],
         dag_y=(400, 455), tepe_y=462)
    orta(78, (524, 558), ["#b8a870", "#a89860", "#988850", "#887842", "#786838"], "#e0d090",
         ekle=lambda img, z: [
             figur(img, orta_asya_sehri, PAY + 100, PAY + 440, duz(588), 2.2, tohum=78),
             kalabalik(img, duz(596), PAY + 20, PAY + 130, 28, 78, ("#6a5a4a", "#5a4a3a"),
                       s=1.5, yon=1)])
    on(78, ["#786838", "#988850", "#887842"], "#e0d090")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 175, z, 2.9, govde="#6a4a4a", bas="bork", bas_renk="#4a3a2a",
              kadin=True, yon=1)                                                    # yoksul kadın
        figur(t, kisi, 212, z, 2.9, govde="#6a5a4a", bas="kalpak", bas_renk="#4a3a2a",
              sakal="#3a2a1a", yon=1, kol=0.6)                                      # yoksul, eli açık
        figur(t, kisi, 262, z, 3.0, govde="#8a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=-1,
              kol=0.45)                                                             # Kalender, kolu yoksula uzanık
        d = ImageDraw.Draw(t)
        if 0.3 < f < 0.8:                                                           # altın kese elden ele (5x5 px, parlak)
            p = (f - 0.3) / 0.5
            xk = int(250 - 30 * p)
            yk = int(z[0] - 46 - 10 * math.sin(p * math.pi))
            d.rectangle([xk - 2, yk - 2, xk + 2, yk + 2], fill=hex2("#ffe070"), outline=hex2("#a07820"))
            piksel(t, xk, yk - 3, hex2("#fff8c0"))

    sprite(78, "karakter", 540, 170, KARE, kare)


# ---------------------------------------------------------------- 79
def sahne79():
    """Şahruh'un cenazesi; arkada birbirine düşen torunlar (karşılıklı atlı gruplar). Bulutlu gün."""
    gokyuzu(79, ["#8a9ab0", "#a8b0b8", "#c8c0b8", "#e0d0b8", "#ece0c4"],
            None, [],
            ("#f4f0ea", "#d8d4d0", "#a8a8b0"))
    uzak(79, ["#7a8498", "#8a92a4"], ["#98a09c", "#a4aaa0"], ["#b4b090", "#a4a080", "#949070"],
         dag_y=(400, 455), tepe_y=462)
    orta(79, (526, 560), ["#a09870", "#908862", "#807854", "#706a48", "#625c40"], "#c8c090",
         ekle=lambda img, z: [
             figur(img, orta_asya_sehri, PAY + 250, PAY + 520, duz(588), 2.0, tohum=79),
             kalabalik(img, duz(596), PAY + 220, PAY + 330, 22, 79, ("#2a2430", "#3a3038"),
                       s=1.4, yon=-1),
             figur(img, atli, PAY + 168, duz(586), 1.4, 1, dur=True, zirh="#9aa2ac",
                   silah="mizrak", bayrak="#8a1e22"),
             figur(img, atli, PAY + 196, duz(586), 1.4, 1, dur=True, zirh="#9aa2ac",
                   silah="mizrak", bayrak="#8a1e22"),
             figur(img, atli, PAY + 352, duz(586), 1.4, -1, dur=True, zirh="#9aa2ac",
                   silah="mizrak", bayrak="#2a5a8a"),
             figur(img, atli, PAY + 380, duz(586), 1.4, -1, dur=True, zirh="#9aa2ac",
                   silah="mizrak", bayrak="#2a5a8a")])
    on(79, ["#625c40", "#807854", "#706a48"], "#c8c090")

    def kare(t, z, i):
        f = i / KARE
        abanoz_tabut(ImageDraw.Draw(t), 200, 358, z[0] - 20)
        for j, x in enumerate((212, 252, 308, 346)):
            figur(t, kisi, x, z, 2.6, govde="#24202c", bas="sarik", bas_renk="#2a2420",
                  yon=-1, adim=(f + (j % 2) * 0.5) % 1)

    sprite(79, "karakter", 540, 170, KARE, kare)


# ---------------------------------------------------------------- 80
def sahne80():
    """Ordu Herat kapısına: atlı Kalender elinde kılıç, arkasında iki atlı; orta planda ordu ve tuğ."""
    gokyuzu(80, ["#6a9ad0", "#98b8dc", "#c8d8e0", "#f0e4c0", "#f8ecc8"],
            None, [],
            ("#ffffff", "#f0eef0", "#c8ccd8"))
    uzak(80, ["#7a9ab8", "#8aa6c0"], ["#98b098", "#a4bc98"], ["#c4c488", "#b4b478", "#a4a468"],
         dag_y=(400, 455), tepe_y=462)
    orta(80, (524, 558), ["#b8b070", "#a8a460", "#989450", "#888442", "#787438"], "#e0dc90",
         ekle=lambda img, z: [
             figur(img, orta_asya_sehri, PAY + 250, PAY + 530, duz(588), 2.4, tohum=80),
             kalabalik(img, duz(596), PAY + 20, PAY + 220, 14, 80,
                       ("#2a2420", "#3a3030", "#5a2a2a"), s=1.5, yon=1, bas="migfer"),
             kalabalik(img, duz(592), PAY + 30, PAY + 240, 12, 81,
                       ("#3a3030", "#4a3a2a"), s=1.3, yon=1, bas="migfer"),
             figur(img, tug, PAY + 70, duz(592), 1.8, 0.0)])
    on(80, ["#787438", "#988850", "#888442"], "#e0dc90")

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 178, z, 2.9, 1, faz=(f + 0.71) % 1, at_renk="#5a3a22", yele="#2b1a12",
              govde="#6a2a2a", bas="migfer", bas_renk="#9aa2ac", silah="mizrak", adim=0.45,
              zirh="#9aa2ac")
        figur(t, atli, 258, z, 2.9, 1, faz=(f + 0.37) % 1, at_renk="#6b3f24", yele="#2b1a12",
              govde="#7a1e22", bas="migfer", bas_renk="#9aa2ac", silah="mizrak", adim=0.45,
              zirh="#9aa2ac")
        figur(t, atli, 342, z, 2.9, 1, faz=f, at_renk="#3a2a22", yele="#1a1210",
              govde="#8a7a5a", bas="sarik", bas_renk="#e8e0cc", sakal="#2a1a12",
              silah="kilic", kol=0.6, adim=0.45)                                    # Kalender

    sprite(80, "karakter", 540, 160, KARE, kare)


# ---------------------------------------------------------------- 81
def sahne81():
    """Gazele giriş: kadehle ve kalemle şiir yazan hükümdar. İç mekân, mum + kandil."""
    ic_mekan(81, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a",
             pencere=("#1a2a4a", "#f4f8ff"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 220, 0, f, 60)
        mumluk(t, 135, z, f, 3)
        mumluk(t, 305, z, (f + 0.3) % 1, 2)
        el = "kase" if 0.55 <= f < 0.85 else "kalem"
        rahle(t, 238, z[0], 2.9, kagit=True)
        figur(t, oturan, 220, z, 3.1, govde="#6a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=1, el=el, minder="#8a2a2a")

    sprite(81, "karakter", 440, 200, KARE, kare)


# ---------------------------------------------------------------- 82
def sahne82():
    """Beyit 1: gece gökyüzü, dolunay; Kalender aya bakar, yanında taş yığını."""
    gokyuzu(82, ["#0a1228", "#16204a", "#26306a", "#3a407a", "#4a4a84"],
            (330, 380, 26, ["#fff8e0", "#f4e8b8"]), [],
            ("#8890b8", "#6a70a0", "#4a5088"), yildiz=70)                            # dolunay kadraj içinde (yakin 2.2'de görünür y ≥ 340)
    uzak(82, ["#1e2a52", "#26305a"], ["#2a3460", "#323c68"], ["#2a3254", "#242c4a", "#1e2640"],
         dag_y=(400, 455), tepe_y=462)
    orta(82, (526, 560), ["#3a4060", "#323852", "#2a3048", "#242a3e", "#1e2434"], "#6a7098",
         ekle=lambda img, z: [
             figur(img, taslar, PAY + 80, duz(588), 1.2),
             figur(img, taslar, PAY + 440, duz(588), 1.2)])
    on(82, ["#1e2434", "#2a3048", "#242a3e"], "#6a7098")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 150, z, 3.0, govde="#6a6a5a", bas="sarik", bas_renk="#d8d4c4",
              sakal="#2a1a12", yon=1)                                               # aya bakar (sağa)
        figur(t, taslar, 250, z, 2.8, cicek=False)

    sprite(82, "karakter", 380, 170, KARE, kare)


# ---------------------------------------------------------------- 83
def sahne83():
    """Beyit 2: gün batımı, büyük gül ve düşen yaprak."""
    gokyuzu(83, ["#4a2a5a", "#8a3a62", "#c85a5a", "#e88a58", "#f4b868", "#f8d890"],
            (300, 452, 26, ["#fff0c0", "#ffb868"]), [],
            ("#f8d0b8", "#e0a090", "#a86078"))
    uzak(83, ["#6a3a62", "#7a4268"], ["#8a4a68", "#9a5870"], ["#a8607a", "#985470", "#884a66"],
         dag_y=(400, 455), tepe_y=462)
    orta(83, (526, 560), ["#7a4a52", "#6a4048", "#5a363e", "#4a2c34", "#3c242a"], "#c08070")
    on(83, ["#3c242a", "#5a363e", "#4a2c34"], "#c08070")

    def kare(t, z, i):
        f = i / KARE
        figur(t, cicek, 70, z, 2.4, (f + 0.3) % 1, "#c8302a", "#f4d24a")
        figur(t, cicek, 150, z, 4.2, f, "#c8302a", "#f4d24a")
        figur(t, cicek, 230, z, 2.8, (f + 0.6) % 1, "#c8302a", "#f4d24a")
        ytop = z[0] - 50                                                            # yaprak aşağı düşer
        xk = int(165 + 6 * math.sin(f * 2 * math.pi))
        yk = int(ytop + f * (z[0] - ytop))
        piksel(t, xk, yk, hex2("#c8302a"))
        piksel(t, xk + 1, yk, hex2("#e85a4a"))

    sprite(83, "karakter", 300, 170, KARE, kare)


# ---------------------------------------------------------------- 84
def sahne84():
    """Beyit 3: Nevruz, bahar bahçesi; ağaç altında kadehli Kalender, dilberler, gül."""
    gokyuzu(84, ["#78b0e0", "#a0c8e8", "#c8def0", "#e8eed8", "#f8f0d0"],
            None, [],
            ("#ffffff", "#eef0f8", "#c8d0e0"))
    uzak(84, ["#7a9ab8", "#8aa8c0"], ["#90b090", "#a0bc98"], ["#a8c878", "#98b868", "#88a858"],
         dag_y=(400, 455), tepe_y=462)
    orta(84, (524, 558), ["#8aa868", "#7a985c", "#6a8850", "#5c7846", "#4e683c"], "#b8d088",
         ekle=lambda img, z: [
             cicekler(img, z, ["#f4d24a", "#e86a8a", "#ffffff", "#8a6ae0"], 84, adet=60,
                      derinlik=26),
             figur(img, agac, PAY + 185, duz(590), 1.7,
                   yaprak=("#d8789a", "#f0a0b8", "#f8d0d8"), govde="#4a3022", tohum=84),
             figur(img, agac, PAY + 350, duz(590), 1.5,
                   yaprak=("#d8789a", "#f0a0b8", "#f8d0d8"), govde="#4a3022", tohum=85)])
    on(84, ["#406a2a", "#5a8838", "#4c7830"], "#b8e078")

    def kare(t, z, i):
        f = i / KARE
        figur(t, agac, 312, z, 2.6, yaprak=("#d8789a", "#f0a0b8", "#f8d0d8"),
              govde="#4a3022", tohum=84, sallanma=math.sin(f * 2 * math.pi))        # ağaç Kalender'in yanında, gövdesi zeminde görünür
        figur(t, kisi, 185, z, 2.8, govde="#c8508a", bas="ortu", bas_renk="#f0d0e0",
              kadin=True, yon=1)
        figur(t, kisi, 218, z, 2.8, govde="#8a5ac8", bas="ortu", bas_renk="#e8d0f0",
              kadin=True, yon=1)
        figur(t, oturan, 262, z, 2.9, govde="#6a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=-1, el="kase", minder="#8a2a2a")
        for gx, gs, gf in ((352, 3.0, f), (372, 2.4, (f + 0.4) % 1), (388, 2.7, (f + 0.7) % 1)):   # gül çalısı
            figur(t, cicek, gx, z, gs, gf, "#c8302a", "#f4d24a")
        for j in range(6):                                                          # düşen yapraklar
            y = 20 + ((f + j / 6) % 1) * (z[0] - 20)
            x = 330 + j * 12 + 5 * math.sin((f + j / 6) * 2 * math.pi)
            piksel(t, int(x), int(y), hex2("#f8c0d0"))

    sprite(84, "karakter", 540, 170, KARE, kare)


# ---------------------------------------------------------------- 85
def sahne85():
    """Beyit 4: kadeh; oturan Kalender kadeh tutar, saki testiyle doldurur. İç mekân."""
    ic_mekan(85, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a",
             pencere=("#1a2a4a", "#f4f8ff"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 225, 0, f, 56)
        mumluk(t, 225, z, f, 3)
        figur(t, oturan, 170, z, 3.0, govde="#6a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=1, el="kase", minder="#8a2a2a")
        figur(t, kisi, 280, z, 3.0, govde="#7a4a8a", bas="bork", bas_renk="#5a3a22",
              yon=-1, silah="testi", kol=0.35 + 0.3 * math.sin(f * 2 * math.pi))      # saki

    sprite(85, "karakter", 440, 190, KARE, kare)


# ---------------------------------------------------------------- 86
def sahne86():
    """Beyit 5: gece, ince ay, mangaldan yükselen gönül dumanı, halk."""
    gokyuzu(86, ["#0a1228", "#16204a", "#26306a", "#3a407a", "#4a4a84"],
            (340, 385, 12, ["#f4ecd0", "#c8c0a0"]), [],
            ("#8890b8", "#6a70a0", "#4a5088"), yildiz=90)
    uzak(86, ["#1e2a52", "#26305a"], ["#2a3460", "#323c68"], ["#2a3254", "#242c4a", "#1e2640"],
         dag_y=(400, 455), tepe_y=462)
    orta(86, (526, 560), ["#3a4060", "#323852", "#2a3048", "#242a3e", "#1e2434"], "#6a7098",
         ekle=lambda img, z: [
             kalabalik(img, duz(596), PAY + 30, PAY + 260, 30, 86,
                       ("#2a2a40", "#3a3050", "#2a3a48"), s=1.6, yon=1)])
    on(86, ["#1e2434", "#2a3048", "#242a3e"], "#6a7098")

    def kare(t, z, i):
        f = i / KARE
        mangal(t, 200, z, f)
        duman(t, 200, z[0] - 13, 110, 86, faz=f, renk="#d9d2c4", ruzgar=0.2)         # mangalın ağzından
        figur(t, oturan, 135, z, 2.9, govde="#6a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=1, minder="#8a2a2a")
        figur(t, oturan, 265, z, 2.9, govde="#4a5a7a", bas="sarik", bas_renk="#d8d4c4",
              sakal="#e8e4dc", yon=-1, minder="#4a3a2a")

    sprite(86, "karakter", 400, 170, KARE, kare)


# ---------------------------------------------------------------- 87
def sahne87():
    """Beyit 6: Mecnun çölde yürür; ufukta Leyla'nın ışıklı çadırı (yurt). Akşam çölü."""
    def ekle(img, z):
        baca = figur(img, yurt, PAY + 470, duz(588), 2.2, keçe="#d8c8a8", golge="#b0986e",
                     isik=True)
        duman(img, baca[0], baca[1], 80, 87, faz=0.0)
        figur(img, taslar, PAY + 70, duz(588), 1.2)

    gokyuzu(87, ["#3a2a5a", "#7a3a6a", "#c05a5a", "#e88a58", "#f4b868", "#f8d890"],
            (300, 452, 26, ["#fff0c0", "#ffb868"]), [],
            ("#f8d0b8", "#e0a090", "#a86078"))
    uzak(87, ["#8a5a62", "#9a6a68"], ["#aa7a6a", "#ba8a70"], ["#c89a78", "#b88a6c", "#a87a60"],
         dag_y=(400, 455), tepe_y=462)
    orta(87, (526, 560), ["#d0a870", "#c09862", "#b08856", "#a0784a", "#90683e"], "#f0c888",
         ekle=ekle)
    on(87, ["#90683e", "#b08856", "#a0784a"], "#f0c888")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 150, z, 3.0, govde="#7a6a52", bas="sarik", bas_renk="#a89878",
              sakal="#3a2a1a", yon=1, adim=f)                                       # Mecnun
        figur(t, taslar, 330, z, 1.8)

    sprite(87, "karakter", 440, 170, KARE, kare)


# ---------------------------------------------------------------- 88
def sahne88():
    """Çözümleme: kılıçlı siluet (öbür yüz) ve yazan, kadeh kaldıran Kalender. İç mekân."""
    ic_mekan(88, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a",
             pencere=("#1a2a4a", "#f4f8ff"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 260, 0, f, 60)
        mumluk(t, 260, z, f, 3)
        figur(t, kisi, 195, z, 3.0, govde="#1a1620", bas="sarik", bas_renk="#1a1620",
              sakal="#1a1620", yon=1, silah="kilic", kol=0.5, ten="#1e1824")        # gölge siluet
        el = "kalem" if f < 0.5 else "kase"
        rahle(t, 310, z[0], 2.8)
        figur(t, oturan, 330, z, 3.0, govde="#6a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=-1, el=el, minder="#8a2a2a")

    sprite(88, "karakter", 540, 200, KARE, kare)


# ---------------------------------------------------------------- 89
def sahne89():
    """Kapanış: alacakaranlık, uzaklaşan derviş silüeti, silik Herat ve mavi türbe."""
    gokyuzu(89, ["#1a1a3a", "#3a2a5a", "#7a3a6a", "#c05a62", "#e88a60", "#f4b878"],
            (300, 452, 26, ["#fff0c0", "#ffb868"]), [],
            ("#f0d0d0", "#d8a8b0", "#a07088"), yildiz=50)
    uzak(89, ["#3a2a52", "#4a3258"], ["#5a3a5e", "#6a4264"], ["#6a4668", "#5a3a5a", "#4a304c"],
         dag_y=(400, 455), tepe_y=462)
    orta(89, (526, 560), ["#4a3050", "#402848", "#382240", "#301c38", "#281630"], "#7a5068",
         ekle=lambda img, z: [
             figur(img, orta_asya_sehri, PAY + 300, PAY + 560, duz(588), 2.0, tohum=89,
                   kerpic="#6a4a60", golge="#4a3248", kubbe="#5a5a8a"),
             figur(img, gur_i_emir, PAY + 120, duz(588), 1.6, mavi="#3a4a7a", tugla="#6a4a60")])
    on(89, ["#281630", "#402848", "#382240"], "#7a5068")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 150, z, 3.0, govde="#140e1c", bas="sarik", bas_renk="#140e1c",
              sakal="#140e1c", yon=-1, adim=f, silah="sopa", ten="#140e1c")

    sprite(89, "karakter", 300, 150, KARE, kare)


SAHNELER = {72: sahne72, 73: sahne73, 74: sahne74, 75: sahne75, 76: sahne76, 77: sahne77,
            78: sahne78, 79: sahne79, 80: sahne80, 81: sahne81, 82: sahne82, 83: sahne83,
            84: sahne84, 85: sahne85, 86: sahne86, 87: sahne87, 88: sahne88, 89: sahne89}

if __name__ == "__main__":
    secim = [int(a) for a in sys.argv[1:] if a.isdigit()] or sorted(SAHNELER)
    for n in secim:
        SAHNELER[n]()
        print(f"sahne {n} tamam")
