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
THOMSEN_SAC = "#5a4838"


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
                 boy=1.0, glifler=None, cin_glifler=None):
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
                            if cin_glifler is not None:
                                cin_glifler.append((sx_ + i_, yy + j))
                yy += 6
    if kar:                                                 # tepede ve kabukta biriken kar
        d.chord([sol, ust - int(6 * s) if kaplumbaga else ust - int(2 * s), sag + yan_g,
                 ust - int(3 * s) if kaplumbaga else ust + int(2 * s)], 180, 360, fill=hex2("#f4f8ff"))
        if kaplumbaga:
            d.chord([x - int(10 * s), y - int(9 * s), x + int(10 * s), y - int(5 * s)], 180, 360, fill=hex2("#e8eef8"))
    return gl


def tas(t, x, z, s=1.0, isik=0.0, f=0.0, dalga=False, cin_isik=0.0, **kw):
    """Yazıt taşı figürü (konturlu) + harflerin ışıması. isik 0-1: harfler oyuk koyu renkten altına döner;
    dalga=True: ışık sütunlar boyunca yukarıdan aşağı akar (taş konuşuyor), f ile döngü.
    cin_isik 0-1: yan yüzdeki Çince işaretler soluk kızıl ışır (yuz="iki")."""
    gl, cg = [], []
    figur(t, _yazit_govde, x, z, s, glifler=gl, cin_glifler=cg, **kw)
    if cin_isik > 0:
        for (px_, py_) in cg:
            piksel(t, px_, py_, hex2("#ffa486" if cin_isik > 0.6 else "#b87060"))
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


# --------------------------------------------------------------------------
# YENİ FİGÜRLER (küçük yardımcılar; ciz.piksel/hex2 + PIL, her biri zemine oturur)
# --------------------------------------------------------------------------
def avrupali(img, x, zemin, s=1.0, govde="#2a2a34", sac="#7a6a5a", sakal=None, yon=1, silah=None, kol=0.0,
             adim=None, bas=None, bas_renk="#1a1a1e", **_):
    """Yeni figür: 19. yüzyıl Avrupalı bilgini/subayı. timur_figur.kisi gövdesi (kemersiz), açık başta saç
    (ya da bas ile şapka/kalpak), beyaz yaka. Ayakları kisi gibi zemine basar."""
    kisi(img, x, zemin, s, govde=govde, bas=bas, bas_renk=bas_renk, sakal=sakal, yon=yon, silah=silah, kol=kol,
         adim=adim, kemer=None)
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    ust = y - int(11 * s)
    d.rectangle([x - int(0.9 * s), ust, x + int(0.9 * s), ust + max(1, int(0.5 * s))], fill=hex2("#f0ece4"))  # yaka
    if bas is None:
        by = y - int(13.6 * s)
        r = max(2, int(1.7 * s))
        d.chord([x - r - 1, by - r - 1, x + r + 1, by + r // 3], 180, 360, fill=hex2(sac))
        ax = x - r * yon                                   # ensede saç (yüzün karşı tarafı)
        d.rectangle([min(ax, ax + (r // 3) * yon), by - r // 2, max(ax, ax + (r // 3) * yon), by + r // 3], fill=hex2(sac))


def ipek_sunan(img, x, zemin, s=1.0, f=0.0, ipek="#d8b040", yon=1, **kw):
    """Yeni figür: ipek top uzatan elçi. kisi (kol 0.35) + elinden sarkan, rüzgârda kıpırdayan ipek kumaş."""
    kol = 0.35
    kisi(img, x, zemin, s, yon=yon, kol=kol, **kw)
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    ust = y - int(11 * s)
    ex = x + int(3.5 * s) * yon
    ey = ust - int(4 * s * kol) + int(1 * s)
    gen = int(2.4 * s)
    dal = 0.5 * s * SIN(f)
    x0, x1 = (ex, ex + gen) if yon > 0 else (ex - gen, ex)
    d.rectangle([x0, ey - int(0.6 * s), x1, ey + int(0.4 * s)], fill=hex2(_ac(ipek, -0.2)))       # top (rulo)
    d.polygon([(x0, ey), (x1, ey), (x1 + dal, ey + int(4 * s)), (x0 + dal, ey + int(4.4 * s))], fill=hex2(ipek))
    d.line([x0 + int(0.7 * s), ey + 1, x0 + int(0.7 * s) + dal, ey + int(4 * s)], fill=hex2(_ac(ipek, 0.35)))
    d.line([x0 + int(1.7 * s), ey + 1, x0 + int(1.7 * s) + dal, ey + int(4 * s)], fill=hex2("#c8302a"))


def masa(img, x, zemin, s=1.0, renk="#6a4426", yuk="kagit"):
    """Yeni figür: çalışma masası (yan görünüş). Dört ayak zemine basar; üstünde yuk: 'kagit' (kâğıt yığını ve
    dayalı taş fotoğrafı), 'album' (açık büyük albüm), 'kitap' (basılı kitap yığını). Masa üstünün y'sini döndürür."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 14 * s)
    temas_golgesi(img, x, y, 14 * s)
    w2 = int(6.5 * s)
    ust = y - int(7 * s)
    k = hex2(_ac(renk, -0.35))
    for ax in (-w2 + int(1.2 * s), w2 - int(2.4 * s)):                       # arka ayaklar (koyu, içeride)
        d.rectangle([x + ax + int(0.6 * s), ust, x + ax + int(1.4 * s), y - 1 - int(0.4 * s)], fill=hex2(_ac(renk, -0.5)))
    for ax in (-w2 + int(0.4 * s), w2 - int(1.6 * s)):                       # ön ayaklar
        d.rectangle([x + ax, ust, x + ax + int(1.2 * s), y - 1], fill=k)
    d.rectangle([x - w2 + int(0.4 * s), ust + int(1 * s), x + w2 - int(0.4 * s), ust + int(2.2 * s)], fill=hex2(_ac(renk, -0.15)))
    d.rectangle([x - w2, ust, x + w2, ust + int(1 * s)], fill=hex2(renk))
    d.line([x - w2, ust, x + w2, ust], fill=hex2(_ac(renk, 0.3)))
    if yuk == "kagit":
        for j in range(3):                                                   # kâğıt yığını
            d.rectangle([x - int(5 * s) + j, ust - int((j + 1) * 0.5 * s) - 1, x - int(1 * s) + j, ust - int(j * 0.5 * s) - 1],
                        fill=hex2(("#f0e8d4", "#e4dcc4", "#f8f2e4")[j]))
        fx0, fx1 = x + int(0.5 * s), x + int(4.5 * s)                       # dayalı fotoğraf: içinde taş silüeti
        d.polygon([(fx0, ust - 1), (fx0 + int(0.6 * s), ust - int(5 * s)), (fx1 + int(0.6 * s), ust - int(5 * s)), (fx1, ust - 1)],
                  fill=hex2("#d8d0bc"))
        d.rectangle([fx0 + int(1.4 * s), ust - int(4 * s), fx1 - int(0.8 * s), ust - int(1 * s)], fill=hex2("#6a665e"))
        d.rectangle([fx0 + int(2 * s), ust - int(3.6 * s), fx1 - int(1.4 * s), ust - int(1.6 * s)], fill=hex2("#b4ae9e"))
    elif yuk == "album":
        d.polygon([(x - int(5 * s), ust - int(1.2 * s)), (x, ust - 1), (x + int(5 * s), ust - int(1.2 * s)), (x + int(5 * s), ust - int(0.4 * s)),
                   (x, ust), (x - int(5 * s), ust - int(0.4 * s))], fill=hex2("#3a2a4a"))
        d.polygon([(x - int(4.6 * s), ust - int(1.6 * s)), (x, ust - int(0.6 * s)), (x, ust - 1), (x - int(4.6 * s), ust - int(1 * s))], fill=hex2("#f4ecd8"))
        d.polygon([(x + int(4.6 * s), ust - int(1.6 * s)), (x, ust - int(0.6 * s)), (x, ust - 1), (x + int(4.6 * s), ust - int(1 * s))], fill=hex2("#e8e0cc"))
        for kx in range(1, 4):                                               # sayfada harf satırları
            piksel(img, x - int(kx * 1.1 * s), ust - int(1.1 * s), hex2("#4a443a"))
            piksel(img, x + int(kx * 1.1 * s), ust - int(1.1 * s), hex2("#4a443a"))
    elif yuk == "kitap":
        for j, rk in enumerate(("#8a2a2a", "#2a4a7a", "#c8a040", "#3a5a3a")):
            yy = ust - 1 - int(j * 1.1 * s)
            d.rectangle([x - int(4.5 * s) + j, yy - int(1.1 * s) + 1, x + int(0.5 * s) + j, yy], fill=hex2(rk), outline=hex2("#2a1a10"))
    return ust


def masa_mumu(t, x, y, f, s=1.0):
    """Yeni figür: masa üstünde pirinç şamdanda tek mum (y = masa üstü). Alev titrer, çevresine sıcak ışık düşer."""
    d = ImageDraw.Draw(t)
    d.rectangle([x - int(1.2 * s), y - max(1, int(0.5 * s)), x + int(1.2 * s), y - 1], fill=hex2("#c8a040"), outline=hex2("#5a3a10"))
    d.rectangle([x - max(1, int(0.3 * s)), y - int(1.4 * s), x + max(1, int(0.3 * s)), y - int(0.5 * s)], fill=hex2("#a88030"))
    d.rectangle([x - max(1, int(0.45 * s)), y - int(4 * s), x + max(1, int(0.45 * s)), y - int(1.4 * s)], fill=hex2("#f4ecd8"))
    alev = 1.3 + 0.35 * SIN(f, 3) + 0.15 * SIN(f, 7)
    ay = y - int(4 * s)
    d.polygon([(x - max(1, int(0.5 * s)), ay), (x, ay - int(alev * 1.6 * s)), (x + max(1, int(0.5 * s)), ay)], fill=hex2("#f8c040"))
    piksel(t, x, ay - 1, hex2("#fff4c0"))
    for r in range(int(2 * s), int(9 * s), 2):
        for a in range(0, 360, 10):
            px_, py_ = x + math.cos(math.radians(a)) * r * 1.2, ay + math.sin(math.radians(a)) * r
            if (int(px_) + int(py_)) % 2 == 0 and py_ < y - 1 and random.Random(int(px_) * 31 + int(py_)).random() < 0.5 * (1 - r / (9 * s)):
                piksel(t, px_, py_, hex2("#ffd479", 55))


def kitaplik(img, x, zemin, s=1.0, renk="#4a2e1a", tohum=1):
    """Yeni figür: alçak kitaplık (insan boyundan kısa). Yan tahtaları zemine basar; raflarda renkli sırtlar."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 12 * s)
    temas_golgesi(img, x, y, 12 * s)
    w2 = int(6 * s)
    ust = y - int(12 * s)
    d.rectangle([x - w2, ust, x + w2, y - 1], fill=hex2(renk))
    rnd = random.Random(tohum)
    raf = int(3.6 * s)
    for k in range(3):
        r0 = ust + int(0.8 * s) + k * raf
        d.rectangle([x - w2 + int(0.8 * s), r0, x + w2 - int(0.8 * s), r0 + raf - int(0.8 * s)], fill=hex2(_ac(renk, -0.45)))
        bx = x - w2 + int(0.8 * s)
        while bx < x + w2 - int(1.6 * s):
            bw = max(1, int(rnd.uniform(0.6, 1.2) * s))
            bh = int(rnd.uniform(0.6, 0.85) * (raf - int(0.8 * s)))
            d.rectangle([bx, r0 + raf - int(0.8 * s) - bh, bx + bw - 1, r0 + raf - int(0.8 * s) - 1],
                        fill=hex2(rnd.choice(("#8a2a2a", "#2a4a7a", "#5a6a3a", "#c8a040", "#6a3a5a", "#d8d0bc"))))
            bx += bw + (1 if rnd.random() < 0.3 else 0)
    d.rectangle([x - w2 - int(0.4 * s), ust - int(0.8 * s), x + w2 + int(0.4 * s), ust], fill=hex2(_ac(renk, 0.15)))


def kursu(img, x, zemin, s=1.0, renk="#5a3420", yon=-1):
    """Yeni figür: konuşma kürsüsü. Ayaklı taban zemine basar, eğik üst tablada kâğıt; konuşmacının önünde durur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 7 * s)
    temas_golgesi(img, x, y, 8 * s)
    d.rectangle([x - int(3.5 * s), y - int(1 * s), x + int(3.5 * s), y - 1], fill=hex2(_ac(renk, -0.2)))
    d.rectangle([x - int(2.2 * s), y - int(9.5 * s), x + int(2.2 * s), y - int(1 * s)], fill=hex2(renk))
    d.line([x - int(1.2 * s), y - int(9 * s), x - int(1.2 * s), y - int(1.5 * s)], fill=hex2(_ac(renk, 0.25)))
    yuk_ = int(1.6 * s) * yon * -1
    d.polygon([(x - int(4 * s), y - int(9.5 * s) - (yuk_ if yuk_ > 0 else 0)), (x + int(4 * s), y - int(9.5 * s) + (yuk_ if yuk_ < 0 else 0)),
               (x + int(4 * s), y - int(8.5 * s) + (yuk_ if yuk_ < 0 else 0)), (x - int(4 * s), y - int(8.5 * s) - (yuk_ if yuk_ > 0 else 0))],
              fill=hex2(_ac(renk, 0.1)))
    d.line([x - int(3 * s), y - int(9.6 * s) - (yuk_ * 3 // 4 if yuk_ > 0 else 0), x + int(3 * s), y - int(9.6 * s) + (yuk_ * 3 // 4 if yuk_ < 0 else 0)],
           fill=hex2("#f4ecd8"), width=max(1, int(0.4 * s)))


def cadir(img, x, zemin, s=1.0, renk="#c8bc9a"):
    """Yeni figür: gezgin çadırı (A biçimi, 3/4 görünüş). Ön ve yan etekleri, direk ve kazıklı gergi ipleri
    zemine basar; ön yüzde koyu kapı aralığı."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x + int(4.5 * s), 32 * s)
    temas_golgesi(img, x + int(5 * s), y, 26 * s)
    sirt_on = (x, y - int(10 * s))
    sirt_arka = (x + int(9 * s), y - int(11 * s))
    ip = hex2("#5a4a38")
    d.line([*sirt_on, x - int(11 * s), y - 1], fill=ip)
    d.line([*sirt_arka, x + int(20 * s), y - 1], fill=ip)
    for kx in (x - int(11 * s), x + int(20 * s)):
        d.rectangle([kx - 1, y - max(2, int(0.8 * s)), kx + 1, y - 1], fill=hex2("#3a2a1a"))
    d.polygon([sirt_on, sirt_arka, (x + int(16 * s), y - 1), (x + int(7 * s), y - 1)], fill=hex2(_ac(renk, -0.22)))
    d.polygon([(x - int(7 * s), y - 1), sirt_on, (x + int(7 * s), y - 1)], fill=hex2(renk))
    d.polygon([(x - int(2.6 * s), y - 1), (x, y - int(6.5 * s)), (x + int(2.6 * s), y - 1)], fill=hex2("#3a2e22"))
    d.polygon([(x, y - int(6.5 * s)), (x + int(2.6 * s), y - 1), (x + int(4 * s), y - 1)], fill=hex2(_ac(renk, 0.12)))  # açık kanat
    d.line([sirt_on[0], sirt_on[1] - int(1.5 * s), *sirt_on], fill=hex2("#4a3420"), width=max(1, int(0.5 * s)))
    d.line([*sirt_on, *sirt_arka], fill=hex2(_ac(renk, 0.3)))


# --------------------------------------------------------------------------
# Sahne kurucular
# --------------------------------------------------------------------------
PALET = {
    "safak": dict(gok=["#2a3a6a", "#5a5a8a", "#a87a8a", "#e8a07a", "#f8c890", "#fce0a8"],
                  dag=["#7a6a98", "#6a5a88"], tepe=["#8a8a7a", "#7a7a6c"], ova=["#a8a86a", "#98985e", "#8a8c54"],
                  orta=["#8a9a54", "#7c8c4a", "#6e7e42", "#60703a", "#526232"], kenar="#d0c888",
                  on=["#526232", "#60703a", "#6e7e42"], isik="#d8d090"),
    "gun": dict(gok=["#3a6aa8", "#5a8ac0", "#7aa4d0", "#9abcdc", "#bcd4e4"],
                dag=["#7a8aa8", "#6a7a98"], tepe=["#7a9470", "#6a8462"], ova=["#9ab06a", "#8aa45e", "#7a9854"],
                orta=["#8aa456", "#7c964c", "#6e8842", "#607a3a", "#526c32"], kenar="#c8d890",
                on=["#526c32", "#607a3a", "#6e8842"], isik="#c8d890"),
    "aksam": dict(gok=["#2a2a58", "#5a3a6a", "#a05078", "#d07a78", "#e8a080", "#f0bc90"],
                  dag=["#6a4a6a", "#5a3e5a"], tepe=["#7a5a6a", "#6a4a5a"], ova=["#8a6a54", "#7a5c48", "#6a503e"],
                  orta=["#7a7044", "#6c623c", "#5e5434", "#50482c", "#423c24"], kenar="#c0a870",
                  on=["#423c24", "#50482c", "#5e5434"], isik="#c0a870"),
    "gece": dict(gok=["#0a0e24", "#141a3a", "#1e2a50", "#2a3a62", "#3a4a74"],
                 dag=["#28304e", "#222a46"], tepe=["#2a3450", "#242e4a"], ova=["#2a3446", "#242e3e", "#1e2836"],
                 orta=["#34443e", "#2e3c37", "#283430", "#222c29", "#1c2422"], kenar="#6a8a80",
                 on=["#1c2422", "#222c29", "#283430"], isik="#6a8a80"),
    "kar": dict(gok=["#4a5a74", "#6a7890", "#8a96a8", "#a8b2c0", "#c4ccd6"],
                dag=["#9aa4b4", "#8a94a6"], tepe=["#b0b8c4", "#a0a8b6"], ova=["#d0d6de", "#c4cad4", "#b8bec8"],
                orta=["#d8dee8", "#ccd2de", "#c0c6d4", "#b4bacb", "#a8aec2"], kenar="#f4f8ff",
                on=["#8a92a2", "#9aa2b2", "#aab2c0"], isik="#f4f8ff"),
    "mavi": dict(gok=["#12307a", "#1a3e8e", "#244ea2", "#2e5eb4", "#3a6ec4", "#4a7ed0"],
                 dag=["#3a4a7a", "#32426e"], tepe=["#3a3a4a", "#323240"], ova=["#3a2c22", "#32261e", "#2a201a"],
                 orta=["#4a3626", "#3e2e20", "#34261a", "#2a2016", "#221a12"], kenar="#7a6248",
                 on=["#221a12", "#2a2016", "#34261a"], isik="#7a6248"),
    "duman": dict(gok=["#4a4a50", "#5e5c5e", "#76726e", "#8e8880", "#a49c90"],
                  dag=["#6a6a6e", "#5e5e64"], tepe=["#7a7468", "#6c665c"], ova=["#8a7c62", "#7c7058", "#6e624e"],
                  orta=["#7a6e4c", "#6c6044", "#5e543c", "#504834", "#423c2c"], kenar="#a89c78",
                  on=["#423c2c", "#504834", "#5e543c"], isik="#a89c78"),
}


def _gok(no, renkler, yildiz=0):
    """Gökyüzü: dither gradyan + (gece) ufka kadar yıldız. sahneler.gokyuzu yıldızları y 300'e kadar koyar;
    yakin 2.6-3.2'de görünen gök y 380-470 arasıdır, bu yüzden yıldızlar ciz.yildizlar ile ufka kadar serpilir."""
    from ciz import gradyan, yildizlar
    from sahneler import kaydet
    g = yeni()
    gradyan(g, renkler)
    if yildiz:
        yildizlar(g, yildiz, 470, "#fff8e0", no)
    kaydet(g, f"sahne{no}-gokyuzu.png")


def _dis(no, palet, ekle=None, dag_y=(404, 452), tepe_y=464, ova_y=486, yildiz=0, orta_ust=(540, 560), on_boy=160):
    p = PALET[palet]
    _gok(no, p["gok"], yildiz)
    uzak(no, p["dag"], p["tepe"], p["ova"], dag_y=dag_y, tepe_y=tepe_y, ova_y=ova_y)
    orta(no, orta_ust, p["orta"], p["kenar"], ekle=ekle)
    on(no, p["on"], p["isik"], boy=on_boy)


def _oda(no, duvar, cini, pencere=None, zemin_renk=("#4a3a2e", "#3e3026", "#32261e"), kemer="#1e1814", hali=False):
    ic_mekan(no, duvar=duvar, kemer=kemer, cini=cini, pencere=pencere, zemin_renk=zemin_renk, isik="#f8c060", hali=hali)


def _sigar(taban, yakin, yazi_alt, odak=None, pay=20):
    """Yazının altına sığan en büyük figür oranı (kadraj yüksekliğine göre), sahne sonu yakınlaşmasıyla."""
    oy = odak if odak is not None else taban - 12
    z = yakin * 1.06
    zemin_ekran = 2 * (oy + (taban - oy) * z)
    return (zemin_ekran - yazi_alt - pay) / (1920 * 1.06)


def _s_sigdir(cizim, hmax, s0=0.8, s1=12.0):
    """Çizimin kutu yüksekliği hmax'ı (ızgara) aşmayan en büyük s (0.1 adım)."""
    s, iyi = s0, s0
    while s <= s1:
        t = yeni(600, 560)
        cizim(t, round(s, 1), duz(557, 600))
        bb = _bb(t)
        if bb[3] - bb[1] > hmax or bb[1] <= 1:
            break
        iyi = round(s, 1)
        s += 0.1
    return iyi


def _arka_yazit(taban, yakin, yazi_alt, geri=14, oran_ust=None, odak=None, **kw):
    """Arka sıradaki (zemini geri px yukarıda) yazıt taşının ölçeği: tepesi yazının altında kalır."""
    oy = odak if odak is not None else taban - 12
    z = yakin * 1.06
    ust_izgara = oy + ((yazi_alt + 20) / 2 - oy) / z
    hmax = (taban - geri) - ust_izgara
    if oran_ust:
        hmax = min(hmax, oran_ust * 960 / yakin)
    return _s_sigdir(lambda t, s, z_: tas(t, 300, z_, s, **kw), hmax)
