"""Taş Konuşuyor: Orhun yazıtları ve Vilhelm Thomsen (1893). Piksel Tarih (@pikseltarihim), sahneler 130-161.
Grafikerin tarifi (teslimler/gece/ara/orhun-yazitlari/5-grafik.md); kartlar 4-kalite-metin.md "Nihai ekran kartları".
Yön dili: bozkır sahnelerinde taş solda/ortada, Avrupa sahneleri iç mekân (mum ve kandil ışığı).
Yeni figürler (bu dosyada, ciz.piksel/hex2 + PIL ile): yazit (kaplumbağa kaideli yazıt taşı), masa (kâğıtlı
çalışma masası), masa_mumu, kursu (konuşma kürsüsü), cadir (gezgin çadırı), sac (açık başa saç), ipek_top.
Kullanım: python3 -I video/piksel/orhun_yazitlari.py [sahne numaraları]"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import ImageDraw  # noqa: E402

from ciz import (_ac, agac, cicek, duman, figur, hex2, piksel, sehir, taslar, temas_golgesi, tug,  # noqa: E402
                 yeni, yurt, zemin_y)
from sahneler import gokyuzu, uzak, orta, on, sprite, duz  # noqa: E402
from timur_figur import kisi, oturan, atli, koyun, deve, yatan, otag  # noqa: E402
from timur import ic_mekan, mumluk, kandil, kalabalik, hava, kar_ortusu  # noqa: E402
from kayip_mezar import hoyuk  # noqa: E402

KARE = 24      # sprite kare sayısı (SKILL.md)
PAY = 135      # orta/ön plan yan payı (SKILL.md)
SIN = lambda f, k=1: math.sin(f * 2 * math.pi * k)  # noqa: E731
TEN = "#e8b890"

# Kişiler (renk kimlikleri bütün videoda aynı)
BILGE = dict(govde="#7a1e22", bas="tac", bas_renk="#e0b040", sakal="#2a1a12", kemer="#e0b040")       # Bilge Kağan
YOLLIG = dict(govde="#3a5a8a", bas="bork", bas_renk="#5a3a22", sakal=None)                          # yazıcı Yollıg Tigin
TONYUKUK = dict(govde="#4a4a6a", bas="bork", bas_renk="#e8e0cc", sakal="#e8e4dc")                   # yaşlı danışman
THOMSEN = dict(govde="#2a2a34", bas=None, bas_renk="#000000", sakal="#8a7a6a", kemer=None)           # 51 yaş, kır sakal
THOMSEN_SAC = "#7a6a5a"


# --------------------------------------------------------------------------
# Ölçüm yardımcıları (cem_sultan.py kalıbı). Yeni çizim fonksiyonu DEĞİL: figürü boş yüzeye
# çizip alfa kanalından ölçer.
# --------------------------------------------------------------------------
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
    s = 1.0
    while s <= 12.0:
        t = yeni(560, 520)
        cizim(t, round(s, 1), duz(517, 560))
        bb = _bb(t)
        if bb and bb[1] <= 1:
            break
        if bb and bb[3] - bb[1] >= hedef:
            _ONBELLEK[anahtar] = round(s, 1)
            return _ONBELLEK[anahtar]
        s += 0.1
    raise RuntimeError(f"olcek({ad}, yakin={yakin}): %{int(oran * 100)} boya ulaşılamadı")


def s_kisi(yakin, oran=0.30):
    return olcek("kisi", yakin, lambda t, s, z: figur(t, kisi, 280, z, s, **BILGE), oran)


def s_oturan(yakin, oran=0.26):
    return olcek("oturan", yakin, lambda t, s, z: figur(t, oturan, 280, z, s, **YOLLIG), oran)


def s_yazit(yakin, oran=0.36, **kw):
    return olcek(("yazit", tuple(sorted(kw.items()))), yakin, lambda t, s, z: tas(t, 280, z, s, **kw), oran)


def _kz(yakin, taban=634, h=300):
    """Kandil zinciri: sprite'ın üst kenarından (tavan) kadrajın üst kenarının biraz altına."""
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
    """Orta plandaki önemli figürler sprite'ın başlangıç ve bitiş sx'inde görünür aralıkta kalmalı."""
    for sx in (sx0, sx1):
        a, b = sx - 270 / yakin + pay, sx + 270 / yakin - pay
        for x in xler:
            if not a <= x <= b:
                raise RuntimeError(f"Sahne {no}: orta plan figürü x={x} görünür aralık "
                                   f"[{int(a)}, {int(b)}] dışında (sx={sx})")


def _ust_sinir(no, kare, w, h, taban, yakin, yazi_alt, odak=None):
    """Yazı bandı denetimi: sprite'taki en yüksek opak piksel, sahne sonundaki yakınlaşmada (yakin·1.06)
    bile ekran yazısının alt kenarının (yazi_alt, ekran px) altında kalmalı. Kandil zinciri (tavandan
    sarkan 1 px çizgi) sayılmaz: yalnız 3 px'ten geniş satırlar ölçülür."""
    oy = odak if odak is not None else taban - 12
    z = yakin * 1.06
    for i in (0, 6, 12, 18):
        t = yeni(w, h)
        kare(t, duz(h - 1, w), i)
        a = t.getchannel("A")
        px = a.load()
        for y in range(h):
            if sum(1 for x in range(w) if px[x, y] > 0) > 3:
                ust = taban - h + y
                break
        else:
            continue
        ekran = 2 * (oy + (ust - oy) * z)
        if ekran < yazi_alt + 12:
            raise RuntimeError(f"Sahne {no}: figür tepesi ekran y={int(ekran)}, yazının alt kenarı {yazi_alt}; "
                               "figürü küçült ya da yakin'i düşür")


def _orta_sinir(no, ust_y, taban, yakin, yazi_alt, odak=None):
    """Orta plandaki en yüksek nesnenin tepesi (ızgara y) yazının altında kalmalı."""
    oy = odak if odak is not None else taban - 12
    ekran = 2 * (oy + (ust_y - oy) * yakin * 1.06)
    if ekran < yazi_alt + 12:
        raise RuntimeError(f"Sahne {no}: orta plan nesnesi ekran y={int(ekran)} yazıya giriyor ({yazi_alt})")


def _olc_ust(cizim, w=560, h=520):
    """Bir orta plan çiziminin en yüksek opak satırı (ızgara y)."""
    t = yeni(w, h)
    cizim(t)
    return _bb(t)[1]


# --------------------------------------------------------------------------
# YENİ FİGÜR: yazıt taşı. Kaplumbağa kaide (iki ön ayak ve kabuğun alt kenarı zemine basar), üstünde
# mermer gövde (ön yüz + perspektifte yan yüz), ejder kabartmalı kemerli tepe. Ön yüzde dikey sütunlar
# hâlinde Göktürk harfleri (yukarıdan aşağı), yuz="cince" ya da "iki" ise yan yüzde/ön yüzde kare Çince
# işaretler. Ölçek: s=1'de toplam boy ≈ 37 piksel (insan kisi s=1 ≈ 15,5 px: taş ≈ 2,4 insan boyu).
# kaplumbaga=False: Tonyukuk ve Yenisey taşları gibi kaidesiz, kaba yontulmuş dikili taş (toprak dolguya
# gömülü). Harf konumlarını döndürür; tas() bunları isik (0-1) ile altın rengine yakar.
# --------------------------------------------------------------------------
RUNLER = [  # 3x5 piksel Göktürk harfi benzeri işaretler (tasarım; okunur metin değil)
    ["010", "010", "111", "010", "010"], ["100", "110", "101", "100", "100"], ["001", "011", "101", "001", "001"],
    ["111", "001", "011", "001", "111"], ["010", "101", "101", "010", "010"], ["100", "100", "111", "001", "001"],
    ["101", "101", "010", "010", "010"], ["010", "010", "010", "101", "101"], ["110", "001", "010", "100", "011"],
    ["011", "100", "110", "100", "011"], ["101", "010", "101", "010", "101"], ["111", "100", "100", "100", "100"],
]
CINCE = [  # 4x4 kare Çince işaret benzeri
    ["1111", "0100", "1111", "0101"], ["0100", "1111", "0110", "1001"], ["1111", "1001", "1111", "1001"],
    ["0010", "1111", "0100", "1111"], ["1010", "1111", "1010", "1011"], ["1111", "0010", "0110", "1010"],
]


def _yazit_govde(img, x, zemin, s=1.0, yuz="runik", kaplumbaga=True, tas_renk="#b8b2a2", kar=False, tohum=1,
                 boy=1.0, glifler=None):
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, (24 if kaplumbaga else 14) * s)
    koyu = hex2(_ac(tas_renk, -0.45))
    yan = hex2(_ac(tas_renk, -0.22))
    on_ = hex2(tas_renk)
    k = hex2("#2a241e")
    if kaplumbaga:
        temas_golgesi(img, x, y, 24 * s)
        kab = "#6e6c60"
        # ayaklar: kalın, kısa; tabanları zemine basar
        for ax in (-8, 6):
            d.rectangle([x + int(ax * s), y - int(3 * s), x + int((ax + 3) * s), y - 1], fill=hex2(_ac(kab, -0.2)))
        # kabuk: alt kenarı düz (zemine bir piksel kala), üstü kubbe
        d.chord([x - int(11 * s), y - int(9 * s), x + int(11 * s), y + int(3 * s)], 180, 360, fill=hex2(kab))
        d.rectangle([x - int(11 * s), y - int(3 * s), x + int(11 * s), y - int(1 * s)], fill=hex2(_ac(kab, -0.15)))
        # kabuk deseni (altıgen izler)
        for kx in range(-8, 9, 4):
            for ky in (-6, -4):
                piksel(img, x + int(kx * s), y + int(ky * s), hex2(_ac(kab, -0.35)))
                piksel(img, x + int((kx + 1) * s), y + int(ky * s), hex2(_ac(kab, -0.35)))
        # baş (sağa bakar): kabuğun önünden uzanır, çenesi zemine yakın
        d.ellipse([x + int(10 * s), y - int(5.5 * s), x + int(14.5 * s), y - int(1.5 * s)], fill=hex2(_ac(kab, 0.1)))
        piksel(img, x + int(13 * s), y - int(4 * s), hex2("#1a1612"))
        gy = y - int(8.5 * s)                       # gövdenin oturduğu kabuk sırtı
    else:
        temas_golgesi(img, x, y, 14 * s)
        d.chord([x - int(7 * s), y - int(2.5 * s), x + int(7 * s), y + int(2.5 * s)], 180, 360, fill=hex2("#5a4a38"))
        gy = y - int(1 * s)
    gen = int((10 if kaplumbaga else 7) * s)          # ön yüz genişliği
    yan_g = int((6 if yuz == "iki" else 3) * s) if kaplumbaga else int(2 * s)
    yuk = int((25 if kaplumbaga else 22) * s * boy)
    sol = x - gen // 2 - yan_g // 2
    sag = sol + gen
    ust = gy - yuk
    # gövde: ön yüz ve sağda perspektif yan yüz (yukarı doğru hafif daralır)
    if kaplumbaga:
        tep = int(6 * s)
        kay = int(1 * s)                                   # yan yüz: ön yüzün sağa-yukarı kaydırılmış kopyası
        for dx in range(yan_g, 0, -1):
            dy = -round(kay * dx / max(1, yan_g))
            d.rectangle([sol + dx, ust + dy, sag + dx, gy + dy - 1], fill=yan)
            d.chord([sol + dx, ust - tep + dy, sag + dx, ust + tep + dy], 180, 360, fill=yan)
        d.rectangle([sol, ust, sag, gy], fill=on_)
        # kemerli, ejder kabartmalı tepe
        d.chord([sol, ust - tep, sag, ust + tep], 180, 360, fill=hex2(_ac(tas_renk, -0.08)))
        for a in range(200, 341, 20):                          # ejder kıvrımları
            cx_, cy_ = (sol + sag) / 2, ust
            for r in ((gen / 2) * 0.55, (gen / 2) * 0.85):
                piksel(img, cx_ + math.cos(math.radians(a)) * r, cy_ + math.sin(math.radians(a)) * r * (tep / (gen / 2)), koyu)
        d.rectangle([sol + int(3.5 * s), ust - int(3 * s), sag - int(3.5 * s), ust - int(1 * s)], fill=hex2(_ac(tas_renk, -0.3)))
        d.line([sol, ust, sag, ust], fill=koyu)
    else:
        rnd = random.Random(tohum)
        kaba = [(sol, gy), (sol - 1, ust + int(4 * s)), (sol + int(1.5 * s), ust + rnd.randint(0, 3)),
                (sol + gen // 2, ust - int(1.5 * s)), (sag - int(1 * s), ust + rnd.randint(1, 4)), (sag, ust + int(5 * s)), (sag, gy)]
        d.polygon(kaba, fill=on_)
        d.polygon([(sag, ust + int(5 * s)), (sag + yan_g, ust + int(6 * s)), (sag + yan_g, gy - 1), (sag, gy)], fill=yan)
        for _ in range(int(12 * s)):                            # aşınma lekeleri
            piksel(img, rnd.randint(sol + 2, sag - 2), rnd.randint(ust + int(5 * s), gy - 2), hex2(_ac(tas_renk, -0.12)))
    # yazı alanı: ön yüzde dikey sütunlar
    pay = max(2, int(1.2 * s))
    sutun = 5 if yuz != "cince" else 6
    gl = [] if glifler is None else glifler
    rnd = random.Random(tohum * 7 + 3)
    bas_y = ust + (int(1 * s) if kaplumbaga else int(6 * s))
    alt_y = gy - pay
    desen = CINCE if yuz == "cince" else RUNLER
    gw = len(desen[0][0])
    gh = len(desen[0])
    xs = list(range(sol + pay, sag - pay - gw + 1, sutun))
    for sx_ in xs:
        yy = bas_y + pay
        while yy + gh <= alt_y:
            g = rnd.choice(desen)
            for j, sat in enumerate(g):
                for i_, c in enumerate(sat):
                    if c == "1":
                        piksel(img, sx_ + i_, yy + j, hex2("#4a443a"))
                        gl.append((sx_ + i_, yy + j))
            yy += gh + 2
    if yuz == "iki" and kaplumbaga:                         # yan yüzde Çince: kare işaretler, soluk
        for sx_ in range(sag + 2, sag + yan_g - 4, 5):
            yy = bas_y + int(2 * s)
            while yy + 4 <= gy - int(2 * s):
                g = rnd.choice(CINCE)
                for j, sat in enumerate(g):
                    for i_, c in enumerate(sat):
                        if c == "1":
                            piksel(img, sx_ + i_, yy + j, hex2("#3e3a32"))
                yy += 6
    if kar:                                                 # tepede ve kabukta biriken kar
        d.chord([sol, ust - int(6 * s) if kaplumbaga else ust - int(2 * s), sag + yan_g,
                 ust - int(3 * s) if kaplumbaga else ust + int(2 * s)], 180, 360, fill=hex2("#f4f8ff"))
        if kaplumbaga:
            d.chord([x - int(10 * s), y - int(9 * s), x + int(10 * s), y - int(5 * s)], 180, 360, fill=hex2("#e8eef8"))
    return gl


def tas(t, x, z, s=1.0, isik=0.0, f=0.0, dalga=False, **kw):
    """Yazıt taşı figürü (konturlu) + harflerin ışıması. isik 0-1: harfler oyuk koyu renkten altına döner;
    dalga=True: ışık sütunlar boyunca yukarıdan aşağı akar (taş konuşuyor), f ile döngü."""
    gl = []
    figur(t, _yazit_govde, x, z, s, glifler=gl, **kw)
    if isik <= 0 or not gl:
        return
    y0 = min(p[1] for p in gl)
    y1 = max(p[1] for p in gl)
    for (px_, py_) in gl:
        g = isik
        if dalga:
            faz = ((py_ - y0) / max(1, y1 - y0) - f) % 1.0
            g = isik * max(0.25, 1 - faz * 2.2) if faz < 0.6 else isik * 0.25
        if g > 0.5:
            piksel(t, px_, py_, hex2("#ffe08a"))
            if g > 0.8:
                for dx, dy in ((1, 0), (-1, 0), (0, -1), (0, 1)):
                    piksel(t, px_ + dx, py_ + dy, hex2("#ffd479", 60))
        elif g > 0.2:
            piksel(t, px_, py_, hex2("#c8a050"))
