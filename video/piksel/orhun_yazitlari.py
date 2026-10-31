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

from ciz import (_ac, at, cicek, duman, figur, hex2, piksel, sehir, taslar, temas_golgesi, tug,  # noqa: E402
                 yeni, yurt, zemin_y)
from sahneler import gokyuzu, uzak, orta, on, sprite, duz  # noqa: E402
from timur_figur import kisi, oturan, atli, koyun, yatan  # noqa: E402
from timur import ic_mekan, mumluk, kandil, kalabalik, hava, kar_ortusu  # noqa: E402
from sahneler import GW  # noqa: E402
from kayip_mezar import hoyuk, cam  # noqa: E402

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
        tam = alfa.point(lambda v: 255 if v > 200 else 0).getbbox()      # tam opak pikseller (ışık halesi hariç)
        y2 = 270 / (yakin * 1.06)                                        # sahne sonu yakınlaşmasında görünen yarım
        if tam and (tam[0] < w / 2 - y2 + 2 or tam[2] > w / 2 + y2 - 2):
            raise RuntimeError(f"Sahne {no}: kare {i}, figürler x {tam[0]}-{tam[2]}, görünür aralık {a}-{b}: "
                               "kenarda kesilen figür var")
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


def _ust_sinir(no, kare, w, h, taban, yakin, yazi_alt, odak=None, bant_ust=230):
    """Yazı bandı denetimi: sprite'ta 3 px'ten geniş opak satırların hiçbiri, sahne başında da sonundaki
    yakınlaşmada da (yakin·1.06) ekran yazısının bandına (ekran y bant_ust .. yazi_alt+12) düşmemeli.
    Kandil zinciri 1 px olduğu için sayılmaz; kandilin kendisi bandın üstünde (kadrajın tepesinde) kalır."""
    oy = odak if odak is not None else taban - 12
    for i in (0, 6, 12, 18):
        t = yeni(w, h)
        kare(t, duz(h - 1, w), i)
        px = t.getchannel("A").load()
        for y in range(h):
            if sum(1 for x in range(w) if px[x, y] > 0) <= 3:
                continue
            for z in (yakin, yakin * 1.06):
                ekran = 2 * (oy + (taban - h + y - oy) * z)
                if bant_ust <= ekran <= yazi_alt + 12:
                    raise RuntimeError(f"Sahne {no}: kare {i}, sprite satırı {y} ekran y={int(ekran)} yazı bandında "
                                       f"({bant_ust}-{yazi_alt}); figürü küçült")


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
        kk = max(2, int(1.2 * s)) if kar else 0              # kar: önce beyaz kubbe, sonra kk px aşağıda kabuk
        if kar:
            d.chord([x - int(11 * s), y - int(9 * s), x + int(11 * s), y + int(3 * s)], 180, 360, fill=hex2("#eef2fa"))
        d.chord([x - int(11 * s), y - int(9 * s) + kk, x + int(11 * s), y + int(3 * s) + kk], 180, 360, fill=hex2(kab))
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
        # kemerli, ejder kabartmalı tepe (kar: önce beyaz kemer, sonra kk px aşağıda taş kemer)
        kk = max(2, int(1.2 * s)) if kar else 0
        if kar:
            for dx in range(yan_g, -1, -1):
                d.chord([sol + dx, ust - tep - round(kay * dx / max(1, yan_g)), sag + dx, ust + tep - round(kay * dx / max(1, yan_g))],
                        180, 360, fill=hex2("#f4f8ff"))
            d.chord([sol + yan_g, ust - tep + kk - kay, sag + yan_g, ust + tep + kk - kay], 180, 360, fill=yan)
        d.chord([sol, ust - tep + kk, sag, ust + tep + kk], 180, 360, fill=hex2(_ac(tas_renk, -0.08)))
        d.rectangle([sol, ust, sag, ust + kk], fill=hex2(_ac(tas_renk, -0.08)))
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
        if kar:                                             # tepede kar: önce beyaz, sonra 1-2 px aşağı kaymış taş
            d.polygon(kaba, fill=hex2("#f4f8ff"))
            k_ = max(2, int(1.2 * s))
            d.polygon([(px_, min(py_ + k_, gy)) for px_, py_ in kaba], fill=on_)
        else:
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


def _orta_kontrol(no, ekle, sx, taban, yakin, yazi_alt, odak=None):
    """Orta plana eklenen nesnelerin görünür bölümdeki en yüksek pikseli yazının altında kalmalı."""
    img = yeni(GW, 960)
    ekle(img, duz(588))
    a = int(PAY + sx - 270 / yakin)
    b = int(PAY + sx + 270 / yakin)
    bb = img.crop((a, 0, b, 960)).getchannel("A").getbbox()
    if bb:
        _orta_sinir(no, bb[1], taban, yakin, yazi_alt, odak)


# Ekran yazısının alt kenarı (ekran px, 1080x1920): kartların satır sayısı, en uzun satırı, boy ve yaziY'den
# TimurSeri.tsx Yazi bileşeninin formülüyle hesaplandı (sahne 130'a kapak yazısı dahil).
YAZI_ALT = {130: 613, 131: 644, 132: 546, 133: 589, 134: 600, 135: 546, 136: 576, 137: 559, 138: 529, 139: 545,
            140: 546, 141: 539, 142: 626, 143: 539, 144: 568, 145: 546, 146: 559, 147: 594, 148: 566, 149: 608,
            150: 559, 151: 546, 152: 576, 153: 566, 154: 556, 155: 566, 156: 599, 157: 576, 158: 545, 159: 546,
            160: 568, 161: 507}
DIS = dict(w=400, h=230, taban=632)       # dış mekân sprite'ı (taban 632)
IC = dict(w=400, h=300, taban=634)        # iç mekân sprite'ı (taban 634, kandil zinciri tavana)


def _hmax(no, yk, taban, geri=0, odak=None):
    """Zemini (taban - geri) olan bir figürün yazıya değmeden alabileceği en büyük boy (ızgara px), sahne sonu
    yakınlaşmasıyla (yakin·1.06) ve 20 px payla."""
    oy = odak if odak is not None else taban - 12
    ust = oy + ((YAZI_ALT[no] + 20) / 2 - oy) / (yk * 1.06)
    return (taban - geri) - ust


def _boy(no, yk, cizim, hedef, ic=False, geri=0):
    """Hedef oranı (kadraj yüksekliğinin) karşılayan en küçük ölçek; yazıya değecekse sığan en büyük ölçek."""
    taban = IC["taban"] if ic else DIS["taban"]
    hm = _hmax(no, yk, taban, geri)
    hh = hedef * 960 / yk
    if hh <= hm:
        s = olcek(("boy", no, id(cizim)), yk, cizim, hedef)
        t = yeni(600, 560)
        cizim(t, s, duz(557, 600))
        bb = _bb(t)
        if bb[3] - bb[1] <= hm:
            return s
    return _s_sigdir(cizim, hm)


def _K(no, yk, hedef=0.30, ic=False, tacli=False):
    """Ön sıradaki insanların ölçeği: başlıksız insan boyu kadrajın %30'u (başlıklılar biraz daha uzun);
    yazıya sığmıyorsa sığan en büyük ölçek."""
    if tacli:                                     # sahnede taçlı Bilge Kağan var: tacın ucu da yazının altında kalsın
        return _boy(no, yk, lambda t, s, z: figur(t, kisi, 280, z, s, **BILGE), hedef, ic)
    return _boy(no, yk, lambda t, s, z: figur(t, kisi, 280, z, s, govde="#2a2a34", bas=None, kemer=None), hedef, ic)


def _yazit_s(no, yk, hedef=0.38, geri=0, **kw):
    """Yazıt taşı ölçeği (ön sırada ya da geri px arkada)."""
    return _boy(no, yk, lambda t, s, z: tas(t, 280, z, s, **kw), hedef, geri=geri)


def _bitir(no, kare, yk, ic=False, esik=0.75):
    d = IC if ic else DIS
    _ust_sinir(no, kare, d["w"], d["h"], d["taban"], yk, YAZI_ALT[no])
    _spr(no, d["w"], d["h"], kare, yk, esik)


# ==========================================================================
# SAHNELER
# ==========================================================================
def sahne130():
    """Kart 1-2 (ve kapak): Moğolistan bozkırı, şafak. Kaplumbağa kaideli yazıt taşı yalnız; harfleri yavaşça
    ışıyıp söner (taş konuşuyor), çiçekler rüzgârda."""
    yk = 2.8
    ekle = lambda img, z: figur(img, taslar, PAY + 335, duz(588), 0.9)  # noqa: E731  uzakta ovoo
    _orta_kontrol(130, ekle, 270, 632, yk, YAZI_ALT[130])
    _dis(130, "safak", ekle=ekle)
    s = _yazit_s(130, yk, 0.38)
    K = _K(130, yk)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 185, z, s, isik=0.75, f=f, dalga=True, tohum=1)
        for x, ph in ((128, 0.0), (272, 0.4)):
            figur(t, cicek, x, z, round(0.32 * K, 1), (f + ph) % 1)

    _bitir(130, kare, yk)


def sahne131():
    """Kart 3: Kopenhag, 1893, gece. Çalışma odası: kitaplık, masada kâğıtlar ve taşın fotoğrafı, mum;
    Thomsen ayakta bir fotoğrafa bakar."""
    _oda(131, duvar=("#2a2420", "#3a3028", "#4a3c30"), cini="#5a3a22", pencere=("#14203a", "#22304c"))
    yk = 2.8
    K = _K(131, yk, ic=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 205, 0, f, zincir=_kz(yk))
        figur(t, kitaplik, 155, duz(z[0] - 8, t.width), round(0.92 * K, 1), tohum=131)
        u = figur(t, masa, 205, z, K, yuk="kagit")
        masa_mumu(t, 172, u, f, round(0.8 * K, 1))
        figur(t, avrupali, 266, z, K, **THOMSEN, sac=THOMSEN_SAC, yon=-1, silah="mektup", kol=0.30 + 0.04 * SIN(f))

    _bitir(131, kare, yk, ic=True, esik=0.7)


def sahne132():
    """Kart 4-5: Thomsen yakın plan; elli bir yaşında Danimarkalı dilbilimci, elinde fotoğraf. Tek şamdan, kandil."""
    _oda(132, duvar=("#2a2420", "#3a3028", "#4a3c30"), cini="#5a3a22", pencere=("#14203a", "#22304c"))
    yk = 3.2
    K = _K(132, yk, 0.33, ic=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 262, 0, f, zincir=_kz(yk))
        mumluk(t, 140, z, f, 3)
        figur(t, avrupali, 210, z, K, **THOMSEN, sac=THOMSEN_SAC, yon=-1, silah="mektup", kol=0.32 + 0.05 * SIN(f))

    _bitir(132, kare, yk, ic=True)


def sahne133():
    """Kart 6: Orhun Vadisi, 732. Yazıt taşı dikilmiş; iki işçi kaidenin dibine toprak atar, Bilge Kağan izler.
    Orta planda iki atlı bekler."""
    yk = 2.6
    K = _K(133, yk, tacli=True)
    sa = round(0.30 * K * 2.9 / 2.6, 1)

    def ekle(img, z):
        for x in (300, 324):
            figur(img, atli, PAY + x, duz(586), sa, -1, dur=True, govde="#5a3a22", bas="bork", bas_renk="#3a2a1a")

    _orta_kontrol(133, ekle, 270, 632, yk, YAZI_ALT[133])
    _dis(133, "gun", ekle=ekle)
    st = _yazit_s(133, yk, 0.40, geri=16)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 156, duz(z[0] - 16, t.width), st, tohum=2)
        for j, (x, yon) in enumerate(((124, 1), (198, -1))):
            ph = (f + j * 0.5) % 1
            figur(t, kisi, x, z, K, govde=("#6a5a3a", "#4a5a6a")[j], bas="bork", bas_renk="#5a3a22", yon=yon,
                  silah="kurek", kol=0.35 + 0.3 * SIN(ph), kemer=None)
        figur(t, kisi, 268, z, K, **BILGE, yon=-1, kol=0.12)

    _bitir(133, kare, yk, esik=0.7)


def sahne134():
    """Kart 7: Kül Tigin'in höyüğü, alacakaranlık. Eyerli, binicisiz atı başı önde bekler; koyunlar otlar (koyun yılı)."""
    yk = 2.8
    _dis(134, "aksam")
    K = _K(134, yk)
    sa = round(K * 2.9 / 2.6, 1)

    def kare(t, z, i):
        f = i / KARE
        figur(t, hoyuk, 160, z, round(0.34 * K, 1))
        figur(t, at, 222, z, round(0.6 * sa, 1), -1, "#5a3a24", "#1a120c", eyer=True, dur=True, bas=0.55 + 0.1 * SIN(f),
              kuyruk=0.5 * SIN(f, 2))
        for j, x in enumerate((138, 262)):
            figur(t, koyun, x, z, round(0.4 * K, 1), (1, -1)[j], (f + j * 0.37) % 1)

    _bitir(134, kare, yk, esik=0.7)


def sahne135():
    """Kart 8-9: taş ustası çekiçle kazır; yazıcı Yollıg Tigin bağdaş kurmuş, yazıyı kâğıda yazar. Gündüz."""
    yk = 2.8
    _dis(135, "gun")
    K = _K(135, yk)
    st = _yazit_s(135, yk, 0.40, geri=14)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 190, duz(z[0] - 14, t.width), st, tohum=3, isik=0.35 * (f > 0.5))
        figur(t, oturan, 147, z, round(0.95 * K, 1), **YOLLIG, yon=1, el="kalem")
        figur(t, kisi, 246, z, K, govde="#6a5a3a", bas="bork", bas_renk="#4a3222", yon=-1, silah="kazma",
              kol=0.45 + 0.35 * SIN(f, 2), kemer=None)

    _bitir(135, kare, yk, esik=0.7)


def sahne136():
    """Kart 10: Bilge Kağan'ın otağı, gece. Kağan sedirde yatar (nefes yavaşlar), başucunda bir hizmetkâr; şamdan ve kandil."""
    _oda(136, duvar=("#3a1614", "#4a1e1a", "#5a2620"), cini="#c8a040",
         zemin_renk=("#5a3a2a", "#4a3022", "#3e281c"), kemer="#2a100c", hali=True)
    yk = 2.8
    K = _K(136, yk, ic=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 228, 0, f, zincir=_kz(yk))
        mumluk(t, 128, z, f, 3)
        figur(t, yatan, 188, z, round(0.58 * K, 1), govde="#7a1e22", bas=None, sakal="#2a1a12", yon=1,
              ortu="#c8b890", nefes=0.5 + 0.5 * SIN(f))
        figur(t, kisi, 262, z, K, govde="#2a2a3a", bas="bork", bas_renk="#2a1a14", yon=-1, kol=0.02, kemer=None)

    _bitir(136, kare, yk, ic=True, esik=0.7)


def sahne137():
    """Kart 11: 735. Aynı vadide iki yazıt taşı yan yana: Kül Tigin'in ve Bilge Kağan'ın. Gündüz, rüzgârda çiçekler."""
    yk = 2.6
    _dis(137, "gun")
    s = _yazit_s(137, yk, 0.36)
    K = _K(137, yk)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 142, z, s, tohum=4)
        tas(t, 245, z, s, tohum=5, tas_renk="#c0b8a6")
        figur(t, cicek, 196, z, round(0.3 * K, 1), f)

    _bitir(137, kare, yk, esik=0.7)


def sahne138():
    """Kart 12: Tuul vadisi. Yaşlı danışman Tonyukuk, sağlığında diktirdiği iki kaba dikili taşın yanında, asasına dayanır."""
    yk = 2.8
    _dis(138, "safak", dag_y=(410, 456))
    K = _K(138, yk)
    st = _yazit_s(138, yk, 0.36, geri=10, kaplumbaga=False, tas_renk="#9a948a")

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 10, t.width)
        tas(t, 146, arka, st, kaplumbaga=False, tas_renk="#9a948a", tohum=6)
        tas(t, 190, arka, round(st * 0.9, 1), kaplumbaga=False, tas_renk="#8e887e", tohum=7)
        figur(t, kisi, 258, z, K, **TONYUKUK, yon=-1, silah="sopa", kol=0.05 + 0.03 * SIN(f), kemer="#8a7a5a")

    _bitir(138, kare, yk, esik=0.7)


def sahne139():
    """Kart 13: yüzyıllar. Kar fırtınası; kağanlık yıkılmış, taş yalnız. Tepesinde ve kaidesinde kar birikmiş,
    harfleri hâlâ soluk ışıkla kıpırdar."""
    yk = 2.8
    _dis(139, "kar")
    kar_ortusu(139)
    hava(139, "kar", 260, renk="#f4f8ff", egim=0.45)
    s = _yazit_s(139, yk, 0.38, kar=True)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 192, z, s, kar=True, isik=0.55, f=f, dalga=True, tohum=1)

    _bitir(139, kare, yk, esik=0.7)


def sahne140():
    """Kart 14: Poltava, 1709. Barut dumanlı gri ova; İsveçli subay Strahlenberg iki Rus askerinin arasında
    esir, sola yürür (tüfekler omuzda)."""
    yk = 2.8

    def ekle(img, z):
        for k, x in enumerate((205, 330)):
            duman(img, PAY + x, 586, 36, 140 + k, faz=0.0, renk="#b8b2a8", ruzgar=0.5, genislik=1.4)

    _orta_kontrol(140, ekle, 270, 632, yk, YAZI_ALT[140])
    _dis(140, "duman", ekle=ekle)
    K = _K(140, yk)

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((136, 252)):
            figur(t, avrupali, x, z, K, govde="#2a5a3a", sac="#3a2a1a", bas="sapka", bas_renk="#1a1a1e", yon=-1,
                  adim=(f + j * 0.5) % 1, silah="sopa")
        figur(t, avrupali, 193, z, K, govde="#2a4a8a", sac="#5a3a22", bas="sapka", bas_renk="#1a1a1e", yon=-1,
              adim=(f + 0.25) % 1)

    _bitir(140, kare, yk, esik=0.75)


def sahne141():
    """Kart 15-16: Sibirya, Yenisey boyu, kar. Çamlar; Strahlenberg (kürk kalpak) garip işaretli kaba bir taşın
    önünde durmuş, kâğıda kopyasını çıkarır."""
    yk = 2.8

    def ekle(img, z):
        for x, s_ in ((205, 1.3), (232, 1.1), (338, 1.4)):
            figur(img, cam, PAY + x, duz(588), s_, renk="#2a4a3e", isik="#e8f0f8")

    _orta_kontrol(141, ekle, 270, 632, yk, YAZI_ALT[141])
    _dis(141, "kar", ekle=ekle)
    kar_ortusu(141)
    hava(141, "kar", 160, renk="#f4f8ff", egim=0.2)
    K = _K(141, yk)
    st = _s_sigdir(lambda t, s, z_: tas(t, 300, z_, s, kaplumbaga=False, boy=0.75), 0.9 * 15.5 * K)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 150, z, st, kaplumbaga=False, boy=0.75, tas_renk="#8a8478", tohum=8, kar=True)
        figur(t, avrupali, 236, z, K, govde="#2a4a8a", sac="#5a3a22", bas="kalpak", bas_renk="#4a3a2a", yon=-1,
              silah="mektup", kol=0.30 + 0.06 * SIN(f, 2))

    _bitir(141, kare, yk, esik=0.7)


def sahne142():
    """Kart 17: akşam. Solda kaba Yenisey taşı, sağda kaplumbağalı Orhun taşı: aynı harfler, ikisinde birden ışır."""
    yk = 2.6
    _dis(142, "aksam")
    s = _yazit_s(142, yk, 0.36)
    sy = _yazit_s(142, yk, 0.27, kaplumbaga=False, boy=0.75)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 145, z, sy, kaplumbaga=False, boy=0.75, tas_renk="#8a8478", tohum=8, isik=0.8, f=f, dalga=True)
        tas(t, 240, z, s, tohum=1, isik=0.8, f=(f + 0.5) % 1, dalga=True)

    _bitir(142, kare, yk, esik=0.7)


def sahne143():
    """Kart 18: Orhun Vadisi, 1889. Gezgin Yadrintsev taşın önünde durur, eliyle gösterir; arkada çadırı ve
    uzakta ikinci taş."""
    yk = 2.6
    K = _K(143, yk)

    def ekle(img, z):
        figur(img, cadir, PAY + 262, duz(586), round(0.55 * K, 1))
        tas(img, PAY + 352, duz(584), round(0.26 * K, 1), tohum=9)

    _orta_kontrol(143, ekle, 270, 632, yk, YAZI_ALT[143])
    _dis(143, "gun", ekle=ekle)
    st = _yazit_s(143, yk, 0.40, geri=14)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 150, duz(z[0] - 14, t.width), st, tohum=1)
        figur(t, avrupali, 248, z, K, govde="#5a4a3a", sac="#3a2a1a", sakal="#3a2a1a", bas="kalpak",
              bas_renk="#3a2a1a", yon=-1, kol=0.40 + 0.04 * SIN(f))

    _bitir(143, kare, yk, esik=0.7)


def sahne144():
    """Kart 19: 1890, Fin-Ugor Cemiyeti'nin seferi. Fotoğrafçı tripodlu makinesini taşa çevirir; yanında
    biri kopya çıkarır."""
    yk = 2.8
    _dis(144, "gun")
    K = _K(144, yk)
    st = _yazit_s(144, yk, 0.40, geri=14)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 144, duz(z[0] - 14, t.width), st, tohum=2)
        figur(t, avrupali, 222, z, K, govde="#3a3a46", sac="#c8a878", sakal="#c8a878", bas="sapka",
              bas_renk="#3a3a2a", yon=-1, silah="kamera", kol=0.1)
        figur(t, avrupali, 267, z, K, govde="#4a4a3a", sac="#5a3a22", yon=-1, silah="mektup", kol=0.3 + 0.06 * SIN(f, 2))

    _bitir(144, kare, yk, esik=0.7)


def sahne145():
    """Kart 20: 1891, Rus seferi. Ortada ak sakallı Radloff, iki yanında Ruslar; hepsinin elinde kopya kâğıtları.
    Arkada (orta planda) taş."""
    yk = 2.8
    K = _K(145, yk)
    ekle = lambda img, z: tas(img, PAY + 300, duz(586), round(0.25 * K, 1), tohum=4)  # noqa: E731
    _orta_kontrol(145, ekle, 270, 632, yk, YAZI_ALT[145])
    _dis(145, "gun", ekle=ekle)

    def kare(t, z, i):
        f = i / KARE
        figur(t, avrupali, 136, z, K, govde="#4a5a4a", sac="#3a2a1a", bas="kalpak", bas_renk="#3a2a1a", yon=1,
              silah="mektup", kol=0.3)
        figur(t, avrupali, 262, z, K, govde="#5a5a4a", sac="#3a2a1a", sakal="#3a2a1a", bas="kalpak",
              bas_renk="#2a2a2a", yon=-1, silah="mektup", kol=0.3 + 0.05 * SIN(f))
        figur(t, avrupali, 200, z, K, govde="#3a3a46", sac="#e8e4dc", sakal="#e8e4dc", bas="kasket",
              bas_renk="#3a3a40", yon=1, silah="mektup", kol=0.36 + 0.05 * SIN(f, 2))

    _bitir(145, kare, yk, esik=0.75)


def sahne146():
    """Kart 21-22: Kül Tigin taşı yakın plan; ön yüzde Göktürk harfleri, yan yüzde Çince yazı soluk kızıl ışıkla
    belirir (Çin imparatoru Xuanzong'un sözleri)."""
    yk = 3.0
    _dis(146, "gun")
    s = _yazit_s(146, yk, 0.38, yuz="iki")

    def kare(t, z, i):
        f = i / KARE
        tas(t, 190, z, s, yuz="iki", cin_isik=0.8 + 0.2 * (SIN(f) > 0), tohum=1)

    _bitir(146, kare, yk, esik=0.7)


def sahne147():
    """Kart 23: Leiden, 1892, gündüz. Sinolog Schlegel masasında Çince yüzün kopyasını okur; arkada kitaplık."""
    _oda(147, duvar=("#3a3a32", "#4a4a40", "#5a5a4e"), cini="#2a4a6a", pencere=("#8ab0d8", "#d8e8f4"))
    yk = 2.8
    K = _K(147, yk, ic=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 150, 0, f, zincir=_kz(yk))
        figur(t, kitaplik, 155, duz(z[0] - 8, t.width), round(0.92 * K, 1), tohum=147, renk="#5a3a22")
        figur(t, masa, 202, z, K, yuk="kagit", renk="#7a5030")
        figur(t, avrupali, 266, z, K, govde="#3a3026", sac="#4a3a2a", yon=-1, silah="mektup", kol=0.3 + 0.05 * SIN(f))

    _bitir(147, kare, yk, ic=True, esik=0.7)


def sahne148():
    """Kart 24: gece, bozkır. Taşın Türkçe yüzü karanlık ve sessiz; yalnız Çince yan yüz soluk ışır."""
    yk = 2.8
    _dis(148, "gece", yildiz=150)
    s = _yazit_s(148, yk, 0.38, yuz="iki")

    def kare(t, z, i):
        tas(t, 190, z, s, yuz="iki", cin_isik=0.5, tas_renk="#a8a498", tohum=1)

    _bitir(148, kare, yk, esik=0.7)


def sahne149():
    """Kart 25-26: Kopenhag, gece. Helsingfors albümü Thomsen'in masasında açık; Thomsen önündeki
    bilinmeyen harflere bakar."""
    _oda(149, duvar=("#2a2420", "#3a3028", "#4a3c30"), cini="#5a3a22", pencere=("#14203a", "#22304c"))
    yk = 2.8
    K = _K(149, yk, ic=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 150, 0, f, zincir=_kz(yk))
        u = figur(t, masa, 188, z, K, yuk="album")
        masa_mumu(t, 228, u, f, round(0.8 * K, 1))
        figur(t, avrupali, 264, z, K, **THOMSEN, sac=THOMSEN_SAC, yon=-1, silah="mektup", kol=0.22 + 0.05 * SIN(f))

    _bitir(149, kare, yk, ic=True, esik=0.7)


def sahne150():
    """Kart 27: bozkırda taşın önünde üç grup: Rus subayı, Türkolog Radloff ve fotoğraf makineli Fin.
    Hepsi taşa bakar; hiçbiri çözümü yayımlamaz."""
    yk = 2.6
    K = _K(150, yk)
    ekle = lambda img, z: tas(img, PAY + 200, duz(586), round(0.27 * K, 1), tohum=1)  # noqa: E731
    _orta_kontrol(150, ekle, 270, 632, yk, YAZI_ALT[150])
    _dis(150, "aksam", ekle=ekle)

    def kare(t, z, i):
        f = i / KARE
        figur(t, avrupali, 172, z, K, govde="#3a3a46", sac="#c8a878", sakal="#c8a878", bas="sapka",
              bas_renk="#3a3a2a", yon=-1, silah="kamera", kol=0.1)              # Fin fotoğrafçı
        figur(t, avrupali, 224, z, K, govde="#4a5a4a", sac="#3a2a1a", bas="kalpak", bas_renk="#3a2a1a", yon=-1,
              silah="sopa")                                                       # Rus subayı
        figur(t, avrupali, 270, z, K, govde="#3a3a46", sac="#e8e4dc", sakal="#e8e4dc", bas="kasket",
              bas_renk="#3a3a40", yon=-1, silah="mektup", kol=0.3 + 0.04 * SIN(f))  # Radloff

    _bitir(150, kare, yk, esik=0.75)


def sahne151():
    """Kart 28-29: Danimarka Kraliyet Akademisi, 1893. Thomsen kürsüde konuşur, eli kalkar; solda dinleyiciler."""
    _oda(151, duvar=("#2e2a3a", "#3a3648", "#484458"), cini="#c8a040", pencere=("#1a2a4a", "#26365a"),
         zemin_renk=("#4a4040", "#3e3636", "#322c2c"))
    yk = 2.8
    K = _K(151, yk, ic=True)

    def kare(t, z, i):
        f = i / KARE
        for x, ph in ((140, 0.0), (262, 0.4)):
            kandil(t, x, 0, (f + ph) % 1, zincir=_kz(yk))
        arka = duz(z[0] - 12, t.width)
        for j, x in enumerate((132, 159, 186)):
            figur(t, avrupali, x, arka, round(0.82 * K, 1), govde=("#2a2a34", "#3a2a2a", "#2a3a3a")[j],
                  sac=("#3a2a1a", "#c8c0b0", "#5a4a3a")[j], sakal=(None, "#c8c0b0", None)[j], yon=1)
        figur(t, avrupali, 252, z, K, **THOMSEN, sac=THOMSEN_SAC, yon=-1, kol=0.25 + 0.25 * max(0, SIN(f)))
        figur(t, kursu, 226, z, K)

    _bitir(151, kare, yk, ic=True, esik=0.7)


def sahne152():
    """Kart 30: gün doğumu, bozkır. Taşın bütün harfleri altın renginde yanar: bu kez biri anlıyor."""
    yk = 2.8
    _dis(152, "safak")
    s = _yazit_s(152, yk, 0.38)
    K = _K(152, yk)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 192, z, s, isik=1.0, tohum=1)
        for x, ph in ((130, 0.2), (270, 0.7)):
            figur(t, cicek, x, z, round(0.32 * K, 1), (f + ph) % 1, renk="#f4d24a")

    _bitir(152, kare, yk, esik=0.7)


def sahne153():
    """Kart 31-32: üstte mavi gök, altta yağız (kara) yer; arada iki insan, bir erkek ve bir kadın, taşa bakar.
    Taşın ilk harfleri ışır (Tengri)."""
    yk = 2.6
    _dis(153, "mavi")
    K = _K(153, yk)
    st = _yazit_s(153, yk, 0.40, geri=14)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 140, duz(z[0] - 14, t.width), st, tohum=1, isik=0.7, f=f, dalga=True)
        figur(t, kisi, 226, z, K, **YOLLIG, yon=-1)
        figur(t, kisi, 264, z, round(0.94 * K, 1), govde="#8a2a2a", bas="ortu", bas_renk="#e8e0d0", kadin=True,
              yon=-1, kemer="#e0b040")

    _bitir(153, kare, yk, esik=0.7)


def sahne154():
    """Kart 33: Bilge Kağan halkına seslenir, eli kalkık; önde iki dinleyici, orta planda halk."""
    yk = 2.6
    K = _K(154, yk, tacli=True)

    def ekle(img, z):
        kalabalik(img, duz(588), PAY + 176, PAY + 290, 10, 154, ("#3a5a8a", "#6a4a2a", "#2a5a3a", "#7a2a22"),
                  s=round(0.42 * K, 1), yon=1)

    _orta_kontrol(154, ekle, 270, 632, yk, YAZI_ALT[154])
    _dis(154, "gun", ekle=ekle)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 132, z, K, govde="#4a5a6a", bas="bork", bas_renk="#5a3a22", yon=1, kemer=None)
        figur(t, kisi, 176, z, round(0.94 * K, 1), govde="#8a5a2a", bas="ortu", bas_renk="#3a5a8a", kadin=True, yon=1)
        figur(t, kisi, 262, z, K, **BILGE, yon=-1, kol=0.55 + 0.1 * SIN(f))

    _bitir(154, kare, yk, esik=0.75)


def sahne155():
    """Kart 34-35: akşam. Çin elçisi bir Türk'e ipek uzatır; arkada (orta planda) surlu Çin şehri."""
    yk = 2.6
    K = _K(155, yk)

    def ekle(img, z):
        figur(img, sehir, PAY + 250, PAY + 420, duz(588), round(0.36 * K, 1), duvar="#b89878", golge="#8a6a50",
              cati="#3a5a4a", tohum=155)

    _orta_kontrol(155, ekle, 270, 632, yk, YAZI_ALT[155])
    _dis(155, "aksam", ekle=ekle)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 140, z, K, **YOLLIG, yon=1, kol=0.15 + 0.1 * max(0, SIN(f)))
        figur(t, ipek_sunan, 238, z, K, f=f, govde="#a8281e", bas="takke", bas_renk="#1a1a1e", sakal="#2a1a12",
              yon=-1, kemer="#e0b040")

    _bitir(155, kare, yk, esik=0.75)


def sahne156():
    """Kart 36: taşın iki yüzü aynı kadrajda: ön yüzde Göktürk harfleri altın, yan yüzde Çince yazı kızıl."""
    yk = 3.0
    _dis(156, "aksam")
    s = _yazit_s(156, yk, 0.38, yuz="iki")

    def kare(t, z, i):
        f = i / KARE
        tas(t, 188, z, s, yuz="iki", isik=1.0, f=f, dalga=True, cin_isik=1.0, tohum=1)

    _bitir(156, kare, yk, esik=0.7)


def sahne157():
    """Kart 37-38: Bilge Kağan taşının yanında halkını uyarır gibi elini kaldırır; orta planda yurtlar ve dumanları."""
    yk = 2.6
    K = _K(157, yk, tacli=True)

    def ekle(img, z):
        for x, s_ in ((300, 0.42), (348, 0.36)):
            b = figur(img, yurt, PAY + x, duz(588), round(s_ * K, 1))
            duman(img, b[0], b[1], 14, 157 + x, faz=0.3)

    _orta_kontrol(157, ekle, 270, 632, yk, YAZI_ALT[157])
    _dis(157, "safak", ekle=ekle)
    st = _yazit_s(157, yk, 0.40, geri=14)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 140, duz(z[0] - 14, t.width), st, tohum=1, isik=0.5, f=f, dalga=True)
        figur(t, kisi, 240, z, K, **BILGE, yon=-1, kol=0.40 + 0.08 * SIN(f))

    _bitir(157, kare, yk, esik=0.7)


def sahne158():
    """Kart 39: Petersburg, 1894. Radloff'un masasında basılmaya başlayan okumaları (kitap yığını); Radloff ayakta."""
    _oda(158, duvar=("#2a3430", "#34403a", "#404c46"), cini="#6a2a2a", pencere=("#14203a", "#22304c"))
    yk = 2.8
    K = _K(158, yk, ic=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 150, 0, f, zincir=_kz(yk))
        u = figur(t, masa, 190, z, K, yuk="kitap")
        masa_mumu(t, 222, u, f, round(0.8 * K, 1))
        figur(t, avrupali, 266, z, K, govde="#3a3a46", sac="#e8e4dc", sakal="#e8e4dc", yon=-1, silah="mektup",
              kol=0.3 + 0.05 * SIN(f))

    _bitir(158, kare, yk, ic=True, esik=0.7)


def sahne159():
    """Kart 40: Tuul vadisi, alacakaranlık. Tonyukuk'un iki taşı yalnız; kimse bilmiyor. Koyunlar otlar."""
    yk = 2.8
    _dis(159, "aksam", dag_y=(410, 456))
    st = _yazit_s(159, yk, 0.36, kaplumbaga=False)
    K = _K(159, yk)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 150, z, st, kaplumbaga=False, tas_renk="#9a948a", tohum=6)
        tas(t, 198, z, round(st * 0.9, 1), kaplumbaga=False, tas_renk="#8e887e", tohum=7)
        figur(t, koyun, 262, z, round(0.55 * K, 1), -1, f)

    _bitir(159, kare, yk, esik=0.7)


def sahne160():
    """Kart 41: Kopenhag, şafak. Thomsen pencerenin önünde elinde kâğıtla durur; şafak ışığı odaya düşer."""
    _oda(160, duvar=("#3a2c24", "#4a3a2e", "#5a4838"), cini="#5a3a22", pencere=("#e8a878", "#fff0c8"))
    yk = 3.0
    K = _K(160, yk, 0.32, ic=True)

    def kare(t, z, i):
        f = i / KARE
        mumluk(t, 135, z, f, 1)
        figur(t, avrupali, 210, z, K, **THOMSEN, sac=THOMSEN_SAC, yon=-1, silah="mektup", kol=0.4 + 0.04 * SIN(f))

    _bitir(160, kare, yk, ic=True)


def sahne161():
    """Kart 42 (ve kapanış): gece, yıldızlı bozkır. Taşın harfleri yavaşça altın ışıkla akar."""
    yk = 2.8
    _dis(161, "gece", yildiz=170)
    s = _yazit_s(161, yk, 0.38)

    def kare(t, z, i):
        f = i / KARE
        tas(t, 192, z, s, isik=0.9, f=f, dalga=True, tas_renk="#aaa69a", tohum=1)

    _bitir(161, kare, yk, esik=0.7)


SAHNELER = {n: globals()[f"sahne{n}"] for n in range(130, 162)}

if __name__ == "__main__":
    for n in ([int(a) for a in sys.argv[1:]] or sorted(SAHNELER)):
        SAHNELER[n]()
        print("sahne", n, "tamam")
