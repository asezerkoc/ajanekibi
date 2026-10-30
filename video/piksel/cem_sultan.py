"""Cem Sultan'ın Zehirli Tıraşı: Piksel Tarih (@pikseltarihim), sahneler 90-121 (104 kullanılmıyor). Grafikerin revize tarifi
(teslimler/2026-10-30-1652-piksel-tarihim-pikseltarihim-icin-reels.md); kod tarafı imza uyumsuzluklarını düzeltir.
Yön dili: sağ = eve doğru, sol = sürgün. Kullanım: python3 -I video/piksel/cem_sultan.py [sahne numaraları]"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ciz import agac, figur, hex2, piksel, sehir, taslar, yeni
from sahneler import gokyuzu, uzak, orta, on, sprite, duz
from timur_figur import kisi, bayezid, oturan, atli, otag, gemi, koy_evleri
from timur import ic_mekan, mumluk, kandil, su_ve_kiyi, kalabalik, tabut
from kayip_mezar import muhafiz

KARE = 24      # sprite kare sayısı (SKILL.md)
PAY = 135      # orta/ön plan yan payı (SKILL.md)
SIN = lambda f, k=1: math.sin(f * 2 * math.pi * k)

CEM_K = dict(govde="#7a1e22", bas="sarik", bas_renk="#e8e0d0", sakal="#2a1a12")    # Cem, olgun
CEM_GENC = dict(govde="#7a1e22", bas="sarik", bas_renk="#e8e0d0", sakal=None)      # Cem, 21-22 yaş


# --------------------------------------------------------------------------
# Ölçüm yardımcıları. Yeni çizim fonksiyonu DEĞİL: figürü boş yüzeye çizip alfa
# kanalından ölçer (ciz.yeni + ciz.figur + PIL).
# --------------------------------------------------------------------------
def _opak(img):
    w = img.size[0]
    return {(i % w, i // w) for i, v in enumerate(img.getchannel("A").getdata()) if v > 0}


def _bb(img):
    return img.getchannel("A").getbbox()


_ONBELLEK = {}


def olcek(ad, yakin, cizim, oran=0.32):
    """Figür kutusu kadraj yüksekliğinin >= oran'ı olan en küçük s (0.1 adım).
    Kadrajda görünen ızgara yüksekliği = 960 / yakin."""
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
            break                                    # tuvale sığmıyor
        if bb and bb[3] - bb[1] >= hedef:
            _ONBELLEK[anahtar] = round(s, 1)
            return _ONBELLEK[anahtar]
        s += 0.1
    raise RuntimeError(f"olcek({ad}, yakin={yakin}): %{int(oran * 100)} boya ulaşılamadı; "
                       "yakin değerini düşür ya da sprite h'sini büyüt")


def s_kisi(yakin, oran=0.32):
    return olcek("kisi", yakin, lambda t, s, z: figur(
        t, kisi, 280, z, s, govde="#7a1e22", bas="sarik", bas_renk="#e8e0d0",
        sakal="#2a1a12", yon=1), oran)


def s_oturan(yakin, oran=0.30):
    return olcek("oturan", yakin, lambda t, s, z: figur(
        t, oturan, 280, z, s, govde="#2a6a3a", bas="sarik", bas_renk="#f4f0e6",
        sakal="#2a1a12", yon=-1, minder="#c8a040"), oran)


def s_atli(yakin):
    """İnsan/at oranı: atlı 2.9 ↔ kisi 2.6 (SKILL.md)."""
    return round(s_kisi(yakin) * 2.9 / 2.6, 1)


def s_muhafiz(yakin, oran=0.32):
    return olcek("muhafiz", yakin, lambda t, s, z: figur(
        t, muhafiz, 280, z, s, faz=0.0, mizrak=True, mesale=True, deel="#2a2a3a"), oran)


def s_gemi(yakin, oran=0.30):
    return olcek("gemi", yakin, lambda t, s, z: figur(t, gemi, 280, 400, s, 1, 0.0), oran)


def _gemi_yarim(s):
    t = yeni(560, 420)
    figur(t, gemi, 280, 400, s, 1, 0.0)
    a, _, b, _ = _bb(t)
    return max(280 - a, b - 280)


def _gemi_denetimi(s, su, w, h):
    """Gövde su çizgisine ulaşmalı (havada gemi olmaz)."""
    for f in (0.0, 0.25, 0.5, 0.75):
        g = yeni(w, h)
        figur(g, gemi, w // 2, su, s, 1, f)
        if _bb(g)[3] < su:
            raise RuntimeError(f"Gemi suya ulaşmıyor: alt={_bb(g)[3]}, su_y={su}")


def _kz(yakin, taban=634, h=300):
    """Kandil zinciri: sprite'ın üst kenarından (tavan) kadrajın üst kenarının biraz altına.
    Kadrajın üst satırı = (taban-12)·(1 - 1/yakin); varsayılan odakY = taban-12."""
    ust_gorunen = (taban - 12) * (1 - 1 / yakin)
    return max(40, int(ust_gorunen - (taban - h)) + 10)


def _kadraj(no, kare, w, h, yakin, esik):
    """Görünür aralık yerel x = w/2 ± 270/yakin. Opak piksellerin en az `esik` oranı içeride
    olmalı; figür sprite'ın üstüne değmemeli (kesik baş = hata)."""
    yarim = 270 / yakin
    a, b = max(int(w / 2 - yarim), 0), min(int(w / 2 + yarim), w)
    for i in (0, 12):
        t = yeni(w, h)
        kare(t, duz(h - 1, w), i)
        alfa = t.getchannel("A")
        toplam = sum(alfa.histogram()[1:])
        bb = alfa.getbbox()
        # üst iki satırdaki opak piksel: kandil zinciri (tavandan sarkar, 1 px) sayılmaz; daha fazlası kesik baş demektir
        ust_satir = sum(alfa.crop((0, 0, w, 2)).histogram()[1:])
        if not toplam or (bb[1] <= 1 and ust_satir > 12):
            raise RuntimeError(f"Sahne {no}: sprite yüksekliği (h={h}) yetmiyor ya da kare boş")
        ici = sum(alfa.crop((a, 0, b, h)).histogram()[1:])
        if ici / toplam < esik:
            raise RuntimeError(f"Sahne {no}: figürlerin %{int(100 * ici / toplam)}'i görünür "
                               f"aralıkta (x {a}-{b}); konumları merkeze çek")


def _spr(no, w, h, kare, yakin, esik=0.75):
    _kadraj(no, kare, w, h, yakin, esik)
    sprite(no, "karakter", w, h, KARE, kare)      # taban_denetimi varsayılan açık


def _gorunur(no, xler, sx0, sx1, yakin, pay=12):
    """Orta plandaki (hareketsiz) önemli figürlerin ızgara x'i, sprite'ın başlangıç ve bitiş
    sx değerlerinin ikisinde de görünür aralıkta (sx ± 270/yakin) kalmalı."""
    for sx in (sx0, sx1):
        a, b = sx - 270 / yakin + pay, sx + 270 / yakin - pay
        for x in xler:
            if not a <= x <= b:
                raise RuntimeError(f"Sahne {no}: orta plan figürü x={x} görünür aralık "
                                   f"[{int(a)}, {int(b)}] dışında (sx={sx}); x ya da sx'i kaydır")


# --------------------------------------------------------------------------
# Tıraş sahnesi (90 ve 105 ortak kare çizimi)
# Cem minderde oturur (sola bakar), berber ayakta (sağa bakar).
# Ustura berberin el ucundan türetilir. Parıltı NÖTR beyazdır (zehir olgu gibi gösterilmez).
# --------------------------------------------------------------------------
TW, TH, CEM_X = 400, 300, 255
CEM = dict(govde="#7a1e22", bas="sarik", bas_renk="#e8e0d0", sakal="#2a1a12", minder="#8a2a2a")
BERBER = dict(govde="#7a6a4a", bas="sapka", bas_renk="#3a2a1a", sakal=None, kemer="#c8b890")
_TIRAS = {}


def _cem_yuz(z, s):
    c = yeni(TW, TH)
    figur(c, oturan, CEM_X, z, s, yon=-1, **CEM)
    k = _opak(c)
    ust = min(y for _, y in k)
    alt = max(y for _, y in k)
    return min(x for x, y in k if y <= ust + 0.45 * (alt - ust)), ust, alt


def _berber_el(z, s, bx, kol):
    """El ucu: aynı poz kol=0 ve kol ile çizilir; farkın sağa en uzak noktası el ucudur."""
    a = yeni(TW, TH)
    figur(a, kisi, bx, z, s, yon=1, kol=0.0, **BERBER)
    b = yeni(TW, TH)
    figur(b, kisi, bx, z, s, yon=1, kol=kol, **BERBER)
    fark = _opak(b) - _opak(a)
    return max(fark, key=lambda p: (p[0], -p[1])) if fark else None


def _tiras_ayar(yakin):
    """Ölçek ve berber konumu ölçülerek bulunur (elle BERBER_X yok)."""
    if yakin in _TIRAS:
        return _TIRAS[yakin]
    s = s_kisi(yakin)
    z = duz(TH - 1, TW)
    boy = max(8, round(2.7 * s))                      # bıçak uzunluğu
    kenar, ust, alt = _cem_yuz(z, s)
    for d in range(int(8 * s), int(45 * s)):
        bx = CEM_X - d
        tamam = True
        for kol in (0.45, 0.55, 0.65):                # kol aralığının uçları ve ortası
            el = _berber_el(z, s, bx, kol)
            if el is None or not (-4 <= kenar - (el[0] + boy + 1) <= 8
                                  and ust <= el[1] <= ust + 0.55 * (alt - ust)):
                tamam = False
                break
        if tamam:
            _TIRAS[yakin] = (s, bx, boy, kenar, ust, alt)
            return _TIRAS[yakin]
    raise RuntimeError("Ustura yüze hizalanamadı: kol aralığını daralt ya da CEM_X'i değiştir")


def _ustura(t, el, i, nabiz, boy):
    ex, ey = el
    for k in range(-3, 2):                                # sap: elin içinde
        for dy in (0, 1):
            piksel(t, ex + k, ey + dy, hex2("#3a2414"))
    for k in range(2, boy + 2):                           # bıçak: Cem'e doğru, 2 piksel kalın
        yy = ey - (k - 2) // 5
        piksel(t, ex + k, yy - 1, hex2("#f4f8ff"))              # üst kenar ışığı
        piksel(t, ex + k, yy, hex2("#dfe6ee"))
        piksel(t, ex + k, yy + 1, hex2("#aeb8c6"))              # alt kenar gölgesi
    if i % (KARE // nabiz) < 3:                           # nötr beyaz parıltı
        piksel(t, ex + boy + 2, ey - 4, hex2("#ffffff"))
        piksel(t, ex + boy + 1, ey - 4, hex2("#cfd8e4"))
        piksel(t, ex + boy + 2, ey - 5, hex2("#cfd8e4"))


def _tiras_kare(t, z, i, yakin, nabiz):
    s, bx, boy, kenar, ust, alt = _tiras_ayar(yakin)
    f = i / KARE
    kandil(t, 205, 0, f, zincir=_kz(yakin))               # zincir tavana kadar
    mumluk(t, 112, z, f, 3)
    figur(t, oturan, CEM_X, z, s, yon=-1, **CEM)
    kol = 0.55 + 0.10 * SIN(f, 2)
    figur(t, kisi, bx, z, s, yon=1, kol=kol, **BERBER)
    el = _berber_el(z, s, bx, kol)
    if el is None or not (-4 <= kenar - (el[0] + boy + 1) <= 8
                          and ust <= el[1] <= ust + 0.55 * (alt - ust)):
        raise RuntimeError(f"Kare {i}: ustura yüze hizalı değil")
    _ustura(t, el, i, nabiz, boy)


def sahne90():
    """Kanca: Napoli, 1495. Berber minderdeki Cem'i tıraş ediyor; ustura parlar (rivayet)."""
    ic_mekan(90, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a",
             pencere=("#2a3a5a", "#f4e0b0"),
             zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"), isik="#f8c060", hali=True)
    _spr(90, TW, TH, lambda t, z, i: _tiras_kare(t, z, i, 2.9, 2), 2.9)


# --------------------------------------------------------------------------
# 106: Cem rıhtımda yalnız (alacakaranlık), sağa (eve doğru) bakar.
# --------------------------------------------------------------------------
def sahne106():
    """'Fatih'in oğlu Cem': taş rıhtımda yalnız Cem, arkasında deniz ve uzak kıyı."""
    gokyuzu(106, ["#2a2a5a", "#5a3a6a", "#a05a78", "#d88a7a", "#f0b088", "#f4c898"],
            (400, 410, 26, ["#fff0c0", "#ffd890"]), [(130, 330, 24), (360, 300, 26)],
            ("#f4e0d0", "#d8a8b0", "#a07890"))
    uzak(106, ["#5a4a7a", "#4a3c6a"], ["#6a5a7a", "#5a4a6a"],
         ["#4a5a8a", "#3e4e7e", "#324270"], dag_y=(392, 440), tepe_y=462, ova_y=476)
    orta(106, (554, 558), ["#6a6a78", "#5c5c6a", "#4e4e5c", "#42424e", "#38384a"], "#a0a0b4")
    on(106, ["#2a3a38", "#344a44", "#3e5a50"], "#6a8a78", boy=90)
    yk = 3.2
    s = s_kisi(yk, 0.34)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 150, z, s, **CEM_K, yon=1, kol=0.03 * (1 + SIN(f)), pelerin="#4a1018")

    _spr(106, 300, 260, kare, yk)


# --------------------------------------------------------------------------
# 107: ekran 4 (yavaş, sessiz). Geniş deniz, ufukta çok küçük tek gemi sağa (eve doğru) süzülür.
# --------------------------------------------------------------------------
KIYI2 = 508                  # orta planda su başlangıcı (ufuk)
H107 = 150
SU107 = H107 - 14            # sprite alt 14 satır su


def sahne107():
    """'Evi, denizin öbür yanında.': alacakaranlıkta geniş deniz, ufukta küçük gemi."""
    gokyuzu(107, ["#1a1a44", "#3a2a5a", "#6a3a6a", "#a05a78", "#d88a7a", "#f0b088"],
            (410, 420, 24, ["#fff0c0", "#ffd890"]), [(150, 330, 24)],
            ("#f4e0d0", "#d8a8b0", "#a07890"))
    uzak(107, ["#4a4a6a", "#3e3e5e"], ["#5a4a6a", "#4e4260"],
         ["#3a4a7a", "#324270", "#2a3a66"], dag_y=(392, 440), tepe_y=462, ova_y=476)
    orta(107, (528, 532), ["#2a3a66", "#243462", "#1e2e5a", "#182850", "#142248"], "#6a8ab0",
         ekle=lambda img, z: su_ve_kiyi(img, KIYI2))
    on(107, ["#142238", "#1a2c44", "#22364e"], "#4a6a88", boy=40)
    s = 1.3                                              # uzak: ölçek bilerek küçük
    _gemi_denetimi(s, SU107, 360, H107)

    def kare(t, z, i):
        f = i / KARE
        figur(t, gemi, 180, SU107, s, 1, f, govde="#3a2a22", yelken="#a8381e")
        su_ve_kiyi(t, SU107)                    # alt 14 satır su: son satır opak

    _spr(107, 360, H107, kare, 2.2, esik=0.3)   # tam genişlikte su bandı sayımı büyütür


# --------------------------------------------------------------------------
# 111: ekran 5. Genç Cem (sakalsız), alacakaranlık odada yalnız.
# --------------------------------------------------------------------------
def sahne111():
    """'Babası ölünce Cem yirmi bir, yirmi iki yaşındadır.': yalnız genç Cem, tek mum."""
    ic_mekan(111, duvar=("#242a34", "#2e3642", "#3a4452"), kemer="#161a22", cini="#3a4a6a",
             pencere=("#3a3a6a", "#e8b890"),
             zemin_renk=("#4a4440", "#3e3834", "#322e2c"), isik="#e8b060", hali=False)
    yk = 3.2
    s = s_kisi(yk, 0.34)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 125, z, f, 1)
        kandil(t, 275, 0, f, zincir=_kz(yk))
        figur(t, kisi, 200, z, s, **CEM_GENC, yon=1, kol=0.03 * (1 + SIN(f)))

    _spr(111, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 91: Yenişehir. Cem atıyla SOLA çekilir (sürgün). Sağ geride Bayezid'in otağı ve askerleri.
# --------------------------------------------------------------------------
def sahne91():
    """Haziran 1481, Yenişehir: Cem atıyla sola çekilir; sağ geride Bayezid'in otağı ve Bayezid."""
    gokyuzu(91, ["#2a2a58", "#5a3a6a", "#a05078", "#d07a78", "#e8a080", "#f0bc90"],
            (410, 410, 30, ["#fff0c0", "#ffd890"]), [(130, 330, 26), (300, 300, 24)],
            ("#f4d8c8", "#d8a0a8", "#a87890"))
    uzak(91, ["#6a4a6a", "#5a3e5a"], ["#7a5a6a", "#6a4a5a"],
         ["#7a5a4a", "#6a4a3e", "#5a3e34"], dag_y=(372, 436))
    yk = 2.8
    K = s_kisi(yk)
    _gorunur(91, [285, 305, 335], 280, 255, yk)

    def ekle(img, z):
        kalabalik(img, duz(588), PAY + 285, PAY + 335, 22, 91, ("#2a5a3a", "#3a6a44"),
                  s=round(0.8 * K, 1), yon=-1)
        figur(img, otag, PAY + 305, duz(588), round(0.9 * K, 1), "#2a6a3a", "#e0b040", faz=0.0)
        figur(img, bayezid, PAY + 335, duz(590), round(0.8 * K, 1), yon=-1)

    orta(91, (528, 560), ["#7a6a4a", "#6a5a40", "#5a4c38", "#4c4030", "#3e3426"],
         "#b89858", ekle=ekle)
    on(91, ["#3a2e1e", "#4a3c26", "#5a4a30"], "#b89858")
    sa = s_atli(yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 175, z, sa, -1, faz=f, at_renk="#6b3f24", yele="#2b1a12",
              **CEM_K, adim=0.45)

    _spr(91, 420, 300, kare, yk)


# --------------------------------------------------------------------------
# 112: Kahire. Cem sağa, kapıya yürür; kapıda iki Memlük nöbetçi (orta planda, hareketsiz).
# --------------------------------------------------------------------------
def sahne112():
    """Kahire: sıcak gün batımı, Memlük surları; Cem kapıya yürür, kapıda iki nöbetçi."""
    gokyuzu(112, ["#5a3a5a", "#a0506a", "#d8785a", "#f0a060", "#f4c078", "#f6d890"],
            (150, 410, 28, ["#fff0c0", "#ffd890"]), [(390, 330, 26)],
            ("#f8e0c0", "#e8b898", "#c09078"))
    uzak(112, ["#a07858", "#906a4e"], ["#b08a60", "#a07c54"],
         ["#c8a070", "#b89464", "#a88458"], dag_y=(372, 440), tepe_y=460, ova_y=482)
    yk = 2.8
    K = s_kisi(yk)
    _gorunur(112, [330, 346], 265, 290, yk)

    def ekle(img, z):
        figur(img, sehir, PAY + 245, PAY + 465, duz(588), round(0.6 * K, 1),
              duvar="#d0b078", golge="#a08050", cati="#b07a48", tohum=112)   # Kahire (yaklaşık)
        for x in (330, 346):
            figur(img, muhafiz, PAY + x, duz(590), round(0.8 * K, 1), faz=0.0, mizrak=True,
                  mesale=False, deel="#8a6a2a")

    orta(112, (528, 560), ["#c8a060", "#b89054", "#a88048", "#98703e", "#886036"], "#e8c888",
         ekle=ekle)
    on(112, ["#886036", "#98703e", "#a88048"], "#e8c888")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 160, z, K, **CEM_K, yon=1, adim=f)

    _spr(112, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 113 / 114: Anadolu'ya dönüş (sağa) ve ikinci yenilgi (sola)
# --------------------------------------------------------------------------
def sahne113():
    """'Anadolu'ya döner, bir kez daha dener.': soluk sabah, boş bozkır; Cem atıyla sağa."""
    gokyuzu(113, ["#6a7a9c", "#8a90b0", "#b8a0b0", "#e0b0a8", "#f0c8a0", "#f6dcb0"],
            (150, 430, 26, ["#fff8e0", "#fff0c0"]), [(380, 330, 26)],
            ("#f8e8d8", "#e0c0b8", "#b898a0"))
    uzak(113, ["#8a8aa0", "#7a7a94"], ["#8a8a98", "#7a7a88"],
         ["#8a9068", "#7a8460", "#6a7858"], dag_y=(372, 436))
    orta(113, (528, 560), ["#8a9060", "#7c8456", "#6e764c", "#606842", "#525a38"], "#b8c088")
    on(113, ["#525a38", "#606842", "#6e764c"], "#b8c088")
    yk = 2.8
    sa = s_atli(yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 210, z, sa, 1, faz=f, at_renk="#6b3f24", yele="#2b1a12",
              **CEM_K, adim=0.45)

    _spr(113, 420, 300, kare, yk)


def sahne114():
    """'Yine yenilir.': gri alacakaranlık; Cem atıyla sola çekilir, sağ geride Bayezid'in askerleri."""
    gokyuzu(114, ["#2a2a46", "#4a3a56", "#6a4a60", "#8a5a62", "#a87470", "#c09080"],
            (410, 440, 22, ["#f0d8b0", "#d8b890"]), [(130, 330, 24), (330, 300, 26)],
            ("#d8c8c8", "#b098a8", "#8a7090"))
    uzak(114, ["#4a4a68", "#3e3e5c"], ["#52485e", "#463e54"],
         ["#4a4a4a", "#40403e", "#363632"], dag_y=(372, 436))
    yk = 2.8
    K = s_kisi(yk)
    _gorunur(114, [296, 330], 285, 250, yk)

    def ekle(img, z):
        kalabalik(img, duz(588), PAY + 296, PAY + 330, 18, 114, ("#2a5a3a", "#3a6a44"),
                  s=round(0.8 * K, 1), yon=-1)

    orta(114, (528, 560), ["#5a5a44", "#4e4e3c", "#424234", "#36362c", "#2c2c24"], "#8a8a68",
         ekle=ekle)
    on(114, ["#2c2c24", "#36362c", "#424234"], "#8a8a68")
    sa = s_atli(yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 210, z, sa, -1, faz=f, at_renk="#5a3320", yele="#2b1a12",
              **CEM_K, adim=0.4)

    _spr(114, 420, 300, kare, yk)


# --------------------------------------------------------------------------
# 92 Rodos: gemiye biniş. TEK ölçü sistemi
#   KIYI_Y: orta planda deniz başlangıcı; üstündeki dar kıyı şeridinde Cem, şövalyeler, yapı
#   SU92 = h-14: sprite içinde gemi su çizgisi (alt 14 satır su); gemi kıyının ÖNÜNDE (daha yakın)
# Cem ve şövalyeler orta planda hareketsiz; konumları ölçülen gemi genişliğinden bulunur.
# --------------------------------------------------------------------------
KIYI_Y = 576
H92 = 300
SU92 = H92 - 14
GL92 = 140                   # gemi yerel x (sprite genişliği 420, merkez 210)
SX92 = (262, 272)


def sahne92():
    """Rodos: büyük direkli kadırga limanda; kıyıda Cem gemiye dönük, arkasında şövalyeler."""
    gokyuzu(92, ["#4a4a7a", "#7a6a8a", "#a8808a", "#d0a090", "#e8c0a0"],
            (130, 400, 24, ["#fffbe8", "#fff0c0"]), [(130, 330, 26), (380, 300, 28)],
            ("#e8dcd8", "#c8b0b8", "#a08ca0"))
    uzak(92, ["#6a6a8a", "#5a5a7a"], ["#7a7a8a", "#6a6a7a"],
         ["#5a7a9a", "#4a6a8a", "#3e5a7a"], dag_y=(372, 436), tepe_y=450, ova_y=490)
    yk = 2.2
    K = s_kisi(yk, 0.35)
    sg = s_gemi(yk)
    _gemi_denetimi(sg, SU92, 420, H92)
    yar = _gemi_yarim(sg)
    gemi_son = SX92[1] - 210 + GL92                 # sprite sonunda gemi merkezi (ızgara x)
    cem_x = round(gemi_son + yar + 14)              # gemi kıçının hemen sağı
    sag = SX92[0] + 270 / yk - 8
    sov = [x for x in (cem_x + 28, cem_x + 44) if x <= sag]   # yalnız görünür olanlar çizilir
    _gorunur(92, [cem_x], SX92[0], SX92[1], yk)

    def ekle(img, z):
        su_ve_kiyi(img, KIYI_Y)                                    # KIYI_Y'den aşağısı deniz
        figur(img, sehir, PAY + cem_x - 30, PAY + cem_x + 130, duz(KIYI_Y - 14),
              round(0.55 * K, 1), duvar="#c0b8a8", golge="#8a8478", cati="#a8452e", tohum=92)
        for x in sov:                                              # şövalyeler: bir sıra arkada
            figur(img, kisi, PAY + x, duz(KIYI_Y - 8), round(0.8 * K, 1),
                  govde="#a8281e", bas="migfer", bas_renk="#9aa2ac", sakal=None, yon=-1,
                  silah="mizrak")
        figur(img, kisi, PAY + cem_x, duz(KIYI_Y), K, **CEM_K, yon=-1)   # Cem gemiye dönük

    orta(92, (548, 552), ["#6a8a7a", "#5a7a6a", "#4a6a5a", "#3e5a4e", "#324a40"], "#a8c0a0",
         ekle=ekle)
    on(92, ["#3e5a4e", "#4a6a5a", "#5a7a6a"], "#a8c0a0", boy=100)

    def kare(t, z, i):
        f = i / KARE
        figur(t, gemi, GL92, SU92, sg, 1, f)          # gövde su çizgisine oturur
        su_ve_kiyi(t, SU92)

    _spr(92, 420, H92, kare, yk, esik=0.4)


# --------------------------------------------------------------------------
# 115: "Gemi Fransa'ya gider." Büyük direkli kadırga sola yol alır. İnsan yok.
# --------------------------------------------------------------------------
H115 = 300
SU115 = H115 - 14


def sahne115():
    """Gemi Fransa'ya gider: gün batımında büyük kadırga sola (batıya) yol alır."""
    gokyuzu(115, ["#2a2a56", "#5a3a64", "#9a5a72", "#d07a72", "#e8a07a", "#f0be8c"],
            (140, 430, 26, ["#fff0c0", "#ffd890"]), [(390, 330, 26)],
            ("#f4d8c8", "#d8a0a8", "#a87890"))
    uzak(115, ["#5a4a6a", "#4e4260"], ["#6a4e66", "#5a445c"],
         ["#4a5a86", "#3e4e7a", "#324270"], dag_y=(392, 440), tepe_y=462, ova_y=476)
    orta(115, (528, 532), ["#34406e", "#2c3866", "#26325e", "#202c54", "#1a264a"], "#7a96b8",
         ekle=lambda img, z: su_ve_kiyi(img, KIYI2))
    on(115, ["#18263c", "#1e3048", "#263a54"], "#5a7a98", boy=40)
    yk = 2.4
    sg = s_gemi(yk)
    _gemi_denetimi(sg, SU115, 420, H115)

    def kare(t, z, i):
        f = i / KARE
        figur(t, gemi, 210, SU115, sg, -1, f, govde="#3a2a22", yelken="#9a2e1e")
        su_ve_kiyi(t, SU115)

    _spr(115, 420, H115, kare, yk, esik=0.4)


# --------------------------------------------------------------------------
# 116: Bourganeuf'te kule yapımı (genel görünüm: işçiler, taş yığınları)
# --------------------------------------------------------------------------
def sahne116():
    """'Bourganeuf'te onun için bir kule yapılır.': bulutlu Fransa kırı; işçiler, taş yığınları."""
    gokyuzu(116, ["#4a5a70", "#6a7a8a", "#8a96a0", "#a8b0b0", "#c0c4bc"], None,
            [(130, 330, 26), (400, 300, 28)], ("#e8ecec", "#c8d0d4", "#a0acb8"))
    uzak(116, ["#6a7a8a", "#5c6c7c"], ["#6a8068", "#5c7258"],
         ["#5a7a58", "#4e6e4e", "#446244"], dag_y=(372, 440), tepe_y=458, ova_y=480)
    yk = 2.8
    K = s_kisi(yk)

    def ekle(img, z):
        figur(img, sehir, PAY + 60, PAY + 230, duz(588), round(0.5 * K, 1),
              duvar="#a8a090", golge="#78726a", cati="#6a4a3e", tohum=116)
        for x in (300, 345):
            figur(img, taslar, PAY + x, duz(592), round(0.7 * K, 1))

    orta(116, (528, 560), ["#5a7050", "#506648", "#465c40", "#3c5238", "#324830"], "#8aa070",
         ekle=ekle)
    on(116, ["#324830", "#3c5238", "#465c40"], "#8aa070")
    renk = ("#5a3a22", "#3a4a6a", "#6a4a2a")

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((125, 200, 275)):
            ph = (f + j * 0.33) % 1
            figur(t, kisi, x, z, K, govde=renk[j], bas="bork", bas_renk="#4a3222", sakal=None,
                  yon=1, silah="kurek" if j == 1 else "kazma", kol=0.5 + 0.4 * SIN(ph))

    _spr(116, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 117: bugün Zizim Kulesi. İnsan yok. Kule orta planda (düz zemin), iki ağaç sprite'ta sallanır.
# --------------------------------------------------------------------------
def sahne117():
    """'Bugün de ayakta: Zizim Kulesi.': soğuk altın saatte yalnız taş kule, rüzgârda ağaçlar."""
    gokyuzu(117, ["#2a3050", "#5a4a6a", "#a0607a", "#d88a7a", "#f0b088", "#f4c898"],
            (140, 420, 24, ["#fff0c0", "#ffd890"]), [(390, 330, 26)],
            ("#f4e0d0", "#d8a8b0", "#a07890"))
    uzak(117, ["#5a4a7a", "#4a3c6a"], ["#5a5a72", "#4e4e66"],
         ["#4a5a5a", "#3e4e50", "#344446"], dag_y=(372, 440), tepe_y=460, ova_y=480)
    yk = 2.8
    K = s_kisi(yk)

    def ekle(img, z):
        figur(img, sehir, PAY + 228, PAY + 312, duz(588), round(0.9 * K, 1),
              duvar="#9a9488", golge="#6a665e", cati="#6a4a3e", tohum=117)   # kule (yaklaşık)

    orta(117, (528, 560), ["#3e5a40", "#364e38", "#2e4430", "#283a2a", "#223224"], "#6a8a60",
         ekle=ekle)
    on(117, ["#223224", "#283a2a", "#2e4430"], "#6a8a60")

    def kare(t, z, i):
        f = i / KARE
        for x, ph in ((150, 0.0), (250, 0.5)):
            figur(t, agac, x, z, round(0.75 * K, 1), yaprak=("#2a4a30", "#3a6038", "#52784a"),
                  govde="#3a2618", tohum=3, sallanma=0.25 * SIN(f + ph))

    _spr(117, 400, 300, kare, yk, esik=0.7)


def sahne93():
    """Elden ele: Rodos, Fransa, Roma görevlileri arasında sola yürüyen Cem (ön sırada, en büyük)."""
    ic_mekan(93, duvar=("#2e2a2e", "#3a3238", "#4a3e44"), kemer="#1a1418", cini="#5a3a6a",
             zemin_renk=("#4a4440", "#3e3834", "#322e2c"), isik="#f8c060", hali=False)
    yk = 2.8
    s = s_kisi(yk)
    sa = round(0.92 * s, 1)
    ara = round(11.5 * s)

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 12, 400)
        for x in (130, 270):
            kandil(t, x, 0, f, zincir=_kz(yk))
        xs = [200 + round((1.5 - j) * ara) for j in range(4)]       # sola yürür: j=0 en sağda
        figur(t, kisi, xs[0], arka, sa, govde="#a8281e", bas="migfer", bas_renk="#9aa2ac",
              sakal=None, yon=-1, adim=(f + 0.2) % 1, silah="mizrak")        # Rodos
        figur(t, kisi, xs[2], arka, sa, govde="#2a4a9a", bas="migfer", bas_renk="#aab2bc",
              sakal=None, yon=-1, adim=(f + 0.55) % 1, silah="mizrak")       # Fransa
        figur(t, kisi, xs[3], arka, sa, govde="#d8b040", bas="sapka", bas_renk="#a8281e",
              sakal=None, yon=-1, adim=(f + 0.8) % 1, silah="mizrak")        # Roma
        figur(t, kisi, xs[1], z, s, **CEM_K, yon=-1, adim=f)                 # Cem önde

    _spr(93, 400, 300, kare, yk, esik=0.7)


def sahne94():
    """'Kimse onu eve göndermez.': gece, kule odası; kafesli pencereye bakan yalnız Cem."""
    ic_mekan(94, duvar=("#22222c", "#2c2c38", "#383646"), kemer="#14141c", cini="#2a3a5a",
             pencere=("#0a1228", "#cfd8e8"),
             zemin_renk=("#3e3a40", "#34303a", "#2a2630"), isik="#d8a860", hali=False)
    yk = 3.2
    s = s_kisi(yk, 0.34)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 125, z, f, 1)
        kandil(t, 270, 0, f, zincir=_kz(yk))
        figur(t, kisi, 205, z, s, **CEM_K, yon=-1, kol=0.04 + 0.02 * SIN(f), pelerin="#4a1018")

    _spr(94, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 118: "Siz olsanız dayanabilir miydiniz?" Cem minderde yalnız, tek mum, gece.
# --------------------------------------------------------------------------
def sahne118():
    """Siz olsanız dayanabilir miydiniz?: gece, taş oda; Cem minderde yalnız oturur."""
    ic_mekan(118, duvar=("#1e1e28", "#282834", "#34323e"), kemer="#12121a", cini="#2a3a5a",
             pencere=("#0a1228", "#cfd8e8"),
             zemin_renk=("#3e3a40", "#34303a", "#2a2630"), isik="#d8a860", hali=True)
    yk = 3.2
    s = s_oturan(yk, 0.32)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 125, z, f, 1)
        figur(t, oturan, 205, z, s, yon=-1, **CEM)

    _spr(118, 400, 300, kare, yk)


def sahne108():
    """'Kardeşi tahtta': saray odasında minderde (taht yerine) oturan Bayezid; yalnız figür."""
    ic_mekan(108, duvar=("#2a3a2e", "#344a38", "#425a46"), kemer="#1a2a1e", cini="#c8a040",
             pencere=("#3a4a6a", "#f4d8a0"),
             zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"), isik="#f8c060", hali=True)
    yk = 3.2
    s = s_oturan(yk)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 125, z, f, 3)
        kandil(t, 275, 0, f, zincir=_kz(yk))
        figur(t, oturan, 205, z, s, govde="#2a6a3a", bas="sarik", bas_renk="#f4f0e6",
              sakal="#2a1a12", yon=-1, minder="#c8a040")

    _spr(108, 400, 300, kare, yk)


# --------------------------------------------------------------------------
# 119: "Roma'ya bir hediye gelir." Elçi (silahsız, yorgun at) Roma surlarına sola yürür.
# --------------------------------------------------------------------------
def sahne119():
    """Roma'ya bir hediye gelir: soğuk sabah, sol geride surlu şehir; elçi atıyla şehre yürür."""
    gokyuzu(119, ["#6a7a9a", "#8a8aa8", "#a8a0b0", "#c4b8b8", "#dcd0c4"], None,
            [(380, 320, 28), (150, 350, 24)], ("#eeeaf0", "#d0cad8", "#a8a4b8"))
    uzak(119, ["#8a90a8", "#7a8098"], ["#98a0a8", "#8a929c"],
         ["#98a088", "#889078", "#788068"], dag_y=(372, 436))
    yk = 2.8
    K = s_kisi(yk)
    _gorunur(119, [240, 300], 330, 250, yk, pay=0)   # sur geniş (110-300); görünür kalan bölümü denetlenir

    def ekle(img, z):
        figur(img, sehir, PAY + 110, PAY + 300, duz(588), round(0.6 * K, 1),
              duvar="#b8a890", golge="#8a7a68", cati="#8a5a46", tohum=119)

    orta(119, (528, 560), ["#7a8668", "#6c785e", "#5e6a52", "#505c46", "#424e3a"], "#a0aa88",
         ekle=ekle)
    on(119, ["#424e3a", "#505c46", "#5e6a52"], "#a0aa88")
    sa = s_atli(yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 210, z, sa, -1, faz=f, govde="#2a6a3a", bas="sarik", bas_renk="#f4f0e6",
              sakal="#2a1a12", adim=0.45)

    _spr(119, 420, 300, kare, yk)


def sahne95():
    """Gönderen Bayezid: İstanbul surları önünde Bayezid; mızraklı elçi önünden Roma'ya (sola) gider."""
    gokyuzu(95, ["#6a7a9a", "#8a8aa8", "#a8a0b0", "#c4b8b8", "#dcd0c4"], None,
            [(380, 320, 28), (150, 350, 24)], ("#eeeaf0", "#d0cad8", "#a8a4b8"))
    uzak(95, ["#8a90a8", "#7a8098"], ["#98a0a8", "#8a929c"],
         ["#98a088", "#889078", "#788068"], dag_y=(372, 436))
    yk = 2.8
    K = s_kisi(yk)
    _gorunur(95, [285], 335, 255, yk)

    def ekle(img, z):
        figur(img, sehir, PAY + 150, PAY + 440, duz(588), round(0.55 * K, 1), tohum=95)
        figur(img, bayezid, PAY + 285, duz(590), round(0.85 * K, 1), yon=-1, kol=0.6)

    orta(95, (528, 560), ["#7a8668", "#6c785e", "#5e6a52", "#505c46", "#424e3a"], "#a0aa88",
         ekle=ekle)
    on(95, ["#424e3a", "#505c46", "#5e6a52"], "#a0aa88")
    sa = s_atli(yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 210, z, sa, -1, faz=f, govde="#2a6a3a", bas="sarik", bas_renk="#f4f0e6",
              sakal="#2a1a12", silah="mizrak", bayrak="#e8d8a0", adim=0.7)

    _spr(95, 420, 300, kare, yk)


def _roma(no, gece=False):
    pen = ("#2a3a5a", "#f4d8a0") if gece else ("#6a9ad0", "#fff4d8")
    ic_mekan(no, duvar=("#4a3a30", "#5a4638", "#6a5440"), kemer="#3a2a20", cini="#8a2a2a",
             pencere=pen, zemin_renk=("#6a5a4a", "#5a4c3e", "#4a3e32"), isik="#f8c060",
             hali=True)


def sahne96():
    """Roma, 31 Mayıs 1492: ayakta Burchard günlüğüne yazar; yalnız figür."""
    _roma(96)
    yk = 3.2
    s = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 125, z, f, 3)
        kandil(t, 275, 0, f, zincir=_kz(yk))
        figur(t, kisi, 200, z, s, govde="#1a1a22", bas="sapka", bas_renk="#2a1a22",
              sakal=None, yon=1, silah="mektup", kol=0.30 + 0.08 * SIN(f))   # Burchard

    _spr(96, 400, 300, kare, yk)


def sahne109():
    """Roma: diz çökmüş elçi, inanılan Kutsal Mızrak'ı uzatır; Burchard ayakta izler."""
    _roma(109)
    yk = 2.8
    s = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 115, z, f, 3)
        kandil(t, 285, 0, f, zincir=_kz(yk))
        figur(t, kisi, 150, z, s, govde="#1a1a22", bas="sapka", bas_renk="#2a1a22",
              sakal=None, yon=1, silah="mektup", kol=0.30)                    # Burchard
        figur(t, kisi, 240, z, s, govde="#2a6a3a", bas="sarik", bas_renk="#f4f0e6",
              sakal="#2a1a12", yon=-1, diz=True, silah="mizrak",
              kol=0.55 + 0.05 * SIN(f))                                       # elçi: mızrak elde

    _spr(109, 400, 300, kare, yk)


def sahne97():
    """Cem'e değil, Papa'ya: solda arkada Cem ve muhafızlar, sağ önde mızrağı tutan Papa."""
    ic_mekan(97, duvar=("#3a2a30", "#4a3640", "#5a4450"), kemer="#2a1a20", cini="#8a6a2a",
             zemin_renk=("#5a4a4a", "#4a3c3c", "#3e3030"), isik="#f8c060", hali=True)
    yk = 2.8
    s = s_kisi(yk)
    sb = round(0.75 * s, 1)

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 12, 400)
        kandil(t, 215, 0, f, zincir=_kz(yk))
        for x in (118, 178):
            figur(t, muhafiz, x, arka, sb, faz=f, mizrak=True, mesale=False, deel="#2a2a3a")
        figur(t, kisi, 148, arka, sb, **CEM_K, yon=1)                         # Cem (arkada)
        mumluk(t, 215, z, f, 3)
        figur(t, kisi, 262, z, s, govde="#f2eee4", bas="tac", bas_renk="#e0b040",
              sakal="#d8d0c8", yon=-1, silah="mizrak", kol=0.15 + 0.05 * SIN(f),
              pelerin="#8a1e22")                                              # Papa (önde)

    _spr(97, 400, 300, kare, yk, esik=0.7)


# --------------------------------------------------------------------------
# 120: "Hediye mi, pazarlık mı?" Elçi ile Papa karşı karşıya; mumluk ortada. Niyet gösterilmez.
# --------------------------------------------------------------------------
def sahne120():
    """Hediye mi, pazarlık mı?: Roma odası, gece; Osmanlı elçisi ve Papa karşı karşıya, ortada mum."""
    _roma(120, gece=True)
    yk = 2.8
    s = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, zincir=_kz(yk))
        figur(t, kisi, 145, z, s, govde="#2a6a3a", bas="sarik", bas_renk="#f4f0e6",
              sakal="#2a1a12", yon=1, kol=0.25 + 0.05 * SIN(f))               # elçi
        mumluk(t, 200, z, f, 3)
        figur(t, kisi, 255, z, s, govde="#f2eee4", bas="tac", bas_renk="#e0b040",
              sakal="#d8d0c8", yon=-1, kol=0.10, pelerin="#8a1e22")           # Papa

    _spr(120, 400, 300, kare, yk)


def sahne98():
    """Ocak 1495: Cem sola, Fransa Kralı'na doğru yürür; sağ arkada papalık görevlisi (soğuk gri gün)."""
    gokyuzu(98, ["#6a7a9a", "#8a96b0", "#a8b0c0", "#c4c8d0", "#d8d8d8"], None,
            [(120, 320, 28), (400, 300, 30)], ("#e8ecf0", "#c8ccd8", "#a0a8b8"))
    uzak(98, ["#8a94a8", "#7a849a"], ["#98a0b0", "#8a92a4"],
         ["#7a8068", "#6a7058", "#5a604a"], dag_y=(372, 436))
    yk = 2.8
    K = s_kisi(yk)

    def ekle(img, z):
        figur(img, sehir, PAY + 120, PAY + 420, duz(588), round(0.55 * K, 1),
              duvar="#b8a890", golge="#8a7a68", cati="#8a5a46", tohum=98)

    orta(98, (528, 560), ["#7a8068", "#6a7058", "#5a604a", "#4c523e", "#3e4432"], "#a8b090",
         ekle=ekle)
    on(98, ["#4c523e", "#5a604a", "#6a7058"], "#a8b090")
    sa = s_atli(yk)

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 12, 420)
        figur(t, atli, 135, arka, round(0.8 * sa, 1), 1, dur=True, govde="#2a4a9a", bas="tac",
              bas_renk="#e0b040", sakal="#5a3a22", zirh="#9aa2ac", bayrak="#2a4a9a")  # Fransa Kralı
        figur(t, kisi, 290, arka, round(0.9 * K, 1), govde="#d8b040", bas="sapka",
              bas_renk="#a8281e", sakal=None, yon=-1, silah="mizrak")         # papalık görevli
        figur(t, kisi, 215, z, K, **CEM_K, yon=-1, adim=f)                    # Cem yürür (önde)

    _spr(98, 420, 300, kare, yk, esik=0.65)


# --------------------------------------------------------------------------
# 121: "Yabancı ordu, yabancı şehir: Napoli." Mavi giysili askerlerin arasında Cem önde yürür.
# --------------------------------------------------------------------------
def sahne121():
    """Napoli: gri-mor sabah, sol geride surlu şehir; yabancı askerlerin arasında Cem sola yürür."""
    gokyuzu(121, ["#4a5070", "#6a6a88", "#8a8098", "#a89aa0", "#c4b0a8"], None,
            [(130, 330, 26), (400, 300, 28)], ("#e0dce0", "#c0b8c8", "#98909c"))
    uzak(121, ["#6a6a88", "#5e5e7c"], ["#76728a", "#686480"],
         ["#6a7068", "#5c6258", "#4e5448"], dag_y=(372, 436))
    yk = 2.8
    K = s_kisi(yk)

    def ekle(img, z):
        figur(img, sehir, PAY + 60, PAY + 260, duz(588), round(0.6 * K, 1),
              duvar="#b0a090", golge="#806e60", cati="#8a5a46", tohum=121)

    orta(121, (528, 560), ["#6a7260", "#5e6656", "#525a4a", "#464e40", "#3a4236"], "#9aa088",
         ekle=ekle)
    on(121, ["#3a4236", "#464e40", "#525a4a"], "#9aa088")
    sa = round(0.9 * K, 1)

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 12, 420)
        for j, x in enumerate((140, 265, 290)):
            figur(t, kisi, x, arka, sa, govde="#2a4a9a", bas="migfer", bas_renk="#aab2bc",
                  sakal=None, yon=-1, adim=(f + j * 0.37) % 1, silah="mizrak")
        figur(t, kisi, 205, z, K, **CEM_K, yon=-1, adim=f)                    # Cem önde

    _spr(121, 420, 300, kare, yk, esik=0.7)


def sahne99():
    """Napoli gecesi: surlu yapı, kapıda meşaleli nöbetçiler. Ölüm gösterilmez."""
    gokyuzu(99, ["#0a0e24", "#141a3a", "#1e2a50", "#2a3a62", "#3a4a74"],
            (400, 360, 22, ["#f4f0e0", "#c8d0e0"]), [(140, 330, 26)],
            ("#6a7a9a", "#4a5a7a", "#2a3a5a"), yildiz=90)
    uzak(99, ["#1a2240", "#141c38"], ["#202a48", "#1a2240"],
         ["#1a2438", "#141c2e", "#101828"], dag_y=(372, 440))
    yk = 2.8
    K = s_kisi(yk)

    def ekle(img, z):
        figur(img, sehir, PAY + 110, PAY + 430, duz(588), round(0.55 * K, 1),
              duvar="#4a4e5a", golge="#2a2e3a", cati="#3a3040", tohum=99)

    orta(99, (530, 560), ["#1e2a24", "#18241e", "#141e18", "#101a14", "#0c140e"], "#3a4a44",
         ekle=ekle)
    on(99, ["#0c140e", "#141e18", "#18241e"], "#3a4a44")
    sm = s_muhafiz(yk)

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((150, 255)):
            figur(t, muhafiz, x, z, sm, faz=(f + j * 0.37) % 1, mizrak=True, mesale=True,
                  deel="#2a2a3a")

    _spr(99, 400, 300, kare, yk)


def sahne110():
    """Bursa, alacakaranlık: yerde kapalı tabut, iki yaslı; arkada dağ ve evler."""
    gokyuzu(110, ["#1a1e44", "#3a3060", "#704a72", "#a8647a", "#d08a7c", "#e8a888"],
            (420, 420, 22, ["#fff0c0", "#ffd890"]), [(130, 330, 24), (330, 300, 26)],
            ("#e8d0d0", "#c0a0b0", "#907890"), yildiz=40)
    uzak(110, ["#4a4a6e", "#3e3e60"], ["#524a68", "#464060"],
         ["#3a4054", "#323848", "#2a303c"], dag_y=(372, 430))
    yk = 2.8
    K = s_kisi(yk)

    def ekle(img, z):
        figur(img, koy_evleri, PAY + 80, PAY + 400, duz(588), round(0.5 * K, 1), tohum=110,
              kerpic="#8a7a68")

    orta(110, (528, 560), ["#3e4a3a", "#364232", "#2e3a2c", "#263224", "#1e2a1c"], "#6a7a5a",
         ekle=ekle)
    on(110, ["#1e2a1c", "#263224", "#2e3a2c"], "#6a7a5a")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 125, z, K, govde="#1a1a22", bas="bork", bas_renk="#2a1a14", sakal=None,
              yon=1, kol=0.02 * (1 + SIN(f)))
        figur(t, kisi, 285, z, K, govde="#1a1a22", bas="bork", bas_renk="#2a1a14",
              sakal="#d8d0c8", yon=-1, kol=0.02 * (1 + SIN(f)))
        figur(t, tabut, 205, z, round(0.9 * K, 1), acik=False)           # kapalı tabut yere oturur

    _spr(110, 420, 300, kare, yk, esik=0.7)


def _yazar_odasi(no, duvar, pencere, cini):
    ic_mekan(no, duvar=duvar, kemer="#1e1a20", cini=cini, pencere=pencere,
             zemin_renk=("#5a4a42", "#4a3c36", "#3e3230"), isik="#f8c060", hali=True)


def sahne100():
    """Guicciardini yazar: Floransa tarzı çalışma odası, mumlar; olaydan yaklaşık kırk yıl sonra."""
    _yazar_odasi(100, ("#2e2a30", "#3a343c", "#48404a"), ("#2a3a5a", "#f4d8a0"), "#6a2a2a")
    yk = 3.2
    s = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 125, z, f, 3)
        kandil(t, 275, 0, f, zincir=_kz(yk))
        figur(t, kisi, 200, z, s, govde="#6a2a2a", bas="sapka", bas_renk="#2a1a1a",
              sakal=None, yon=1, silah="mektup", kol=0.35 + 0.10 * SIN(f, 2))

    _spr(100, 400, 300, kare, yk)


def sahne101():
    """Burchard susar: Roma odası, gece; Burchard hareketsiz (yazmıyor), yalnız mumlar kımıldar."""
    _roma(101, gece=True)
    yk = 3.2
    s = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 125, z, f, 2)
        kandil(t, 275, 0, f, zincir=_kz(yk))
        figur(t, kisi, 200, z, s, govde="#1a1a22", bas="sapka", bas_renk="#2a1a22",
              sakal=None, yon=-1, silah="mektup", kol=0.30)

    _spr(101, 400, 300, kare, yk)


def sahne102():
    """'Hastalık der': akşam penceresi olan boş oda; hasta, hekim ve testi yok, hastalık çizilmez."""
    ic_mekan(102, duvar=("#2a2a30", "#34343c", "#403e48"), kemer="#1a1a20", cini="#2a4a6a",
             pencere=("#3a5a8a", "#f4d8a0"),
             zemin_renk=("#4a4440", "#3e3834", "#322e2c"), isik="#e8b060", hali=True)
    yk = 2.8

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, zincir=_kz(yk))
        mumluk(t, 145, z, f, 3)
        mumluk(t, 255, z, f, 1)

    _spr(102, 400, 300, kare, yk, esik=0.6)


def sahne103():
    """Belge yok: iki kaynak yan yana; ortada arkada gri silüet halinde tıraş rivayeti (ustura yok)."""
    ic_mekan(103, duvar=("#2e3036", "#383a42", "#444650"), kemer="#1e2026", cini="#4a5a6a",
             zemin_renk=("#4a4a4e", "#3e3e42", "#323236"), isik="#d8d0b0", hali=False)
    yk = 2.8
    s = s_kisi(yk)
    sg = round(0.7 * s, 1)

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 14, 400)
        figur(t, oturan, 214, arka, sg, govde="#6a6a72", bas="sarik", bas_renk="#9a9aa2",
              sakal="#4a4a52", yon=-1)                                    # gri silüet: rivayet
        figur(t, kisi, 176, arka, sg, govde="#5a5a62", bas="sapka", bas_renk="#4a4a52",
              sakal=None, yon=1, kol=0.5)                                 # (ustura çizilmez)
        figur(t, kisi, 130, z, s, govde="#1a1a22", bas="sapka", bas_renk="#2a1a22",
              sakal=None, yon=1, silah="mektup", kol=0.2 + 0.05 * SIN(f))   # Burchard
        figur(t, kisi, 270, z, s, govde="#6a2a2a", bas="sapka", bas_renk="#2a1a1a",
              sakal=None, yon=-1, silah="mektup", kol=0.2 + 0.05 * SIN(f))  # Guicciardini

    _spr(103, 400, 300, kare, yk, esik=0.7)


def sahne105():
    """Soru: tıraş odası bu kez gece penceresiyle; ustura yavaş parlar (kapanış)."""
    ic_mekan(105, duvar=("#2a2020", "#382a28", "#463430"), kemer="#1a1210", cini="#1e4a7a",
             pencere=("#0e1630", "#f4f8ff"),
             zemin_renk=("#4a3c32", "#3e322a", "#322822"), isik="#f8c060", hali=True)
    _spr(105, TW, TH, lambda t, z, i: _tiras_kare(t, z, i, 2.9, 1), 2.9)


SAHNELER = {90: sahne90, 91: sahne91, 92: sahne92, 93: sahne93, 94: sahne94, 95: sahne95,
            96: sahne96, 97: sahne97, 98: sahne98, 99: sahne99, 100: sahne100,
            101: sahne101, 102: sahne102, 103: sahne103, 105: sahne105,
            106: sahne106, 107: sahne107, 108: sahne108, 109: sahne109, 110: sahne110,
            111: sahne111, 112: sahne112, 113: sahne113, 114: sahne114, 115: sahne115,
            116: sahne116, 117: sahne117, 118: sahne118, 119: sahne119, 120: sahne120,
            121: sahne121}

if __name__ == "__main__":
    import sys
    for n in ([int(a) for a in sys.argv[1:]] or sorted(SAHNELER)):
        SAHNELER[n]()
