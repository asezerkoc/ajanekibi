"""Defterde Bin Yazıyor: Abdülmecid'in İrlanda Büyük Kıtlığı yardımı, belge ile efsane (1847). Piksel Tarih (@pikseltarihim),
sahneler 490-524. Grafikerin tarifi: teslimler/gece/ara/irlanda-kitligi/5-grafik.md; kartlar 4-kalite-metin.md.
Kalıp: video/piksel/cem_sultan.py ve celebi_mehmed_paris.py (ölçek, kadraj, yazı bandı denetimleri), orhun_yazitlari.py
(19. yy Avrupalı figürü, başörtülü kadın), kalender.py (taht).
Yön dili: sağ = İrlanda'ya / yardıma doğru, sol = geriye, belgeye.
Sahne ayarları (yakin, kamera, sprite w/h/x/taban, kartlar) TEK KAYNAKTAN, video/src/sahneler/IrlandaKitligi.tsx'ten okunur.
Yeni figürler (bu dosyada; ciz.piksel/hex2 + PIL, her biri zemine ya da su çizgisine oturur): beyefendi (19. yy erkek:
setre/redingot, fes, silindir şapka, kasket; padişah için sorguçlu fes), hanim (uzun etekli kadın: taç, şal), yelkenli
(1840'lar iki direkli tüccar brikı), kulube (İrlanda taş kulübesi, saz dam), patates (çürüyen fide), kursu (yüksek kâtip
kürsüsü, açık defter), masa, sandalye, raf, vitrin, baski_makinesi (demir el baskı makinesi), kese, kale_kapisi
(iki kuleli kasaba kapısı), arma_kalkani (hilal-yıldızlı kalkan), sancak (eski armalı bayrak), beyaz_kule, cami,
tugla_evler, kahvehane, otel_cephesi (plaket), dizustu, fener_el.
Kullanım: python3 -I video/piksel/irlanda_kitligi.py [sahne numaraları]"""
import math
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw  # noqa: E402

from ciz import _ac, agac, duz_zemin, figur, gradyan, hex2, piksel, temas_golgesi, temel, yeni, zemin_y  # noqa: E402
from sahneler import GW, H, W, duz, gokyuzu, kaydet, sprite, uzak  # noqa: E402
from ciz import sirt, arazi, _esik  # noqa: E402
from timur_figur import kisi, oturan  # noqa: E402
from kalender import taht  # noqa: E402

KARE = 24
PAY = 135
SIN = lambda f, k=1: math.sin(f * 2 * math.pi * k)  # noqa: E731
TEN = "#e8b890"
KOYU = "#24160e"
PUB = Path(__file__).parents[1] / "public"
TSX = Path(__file__).parents[1] / "src" / "sahneler" / "IrlandaKitligi.tsx"


def _u(v, s):
    return max(1, int(round(v * s)))


def _bb(img):
    return img.getchannel("A").getbbox()


# ==========================================================================
# SAHNE AYARLARI: IrlandaKitligi.tsx'ten (tek kaynak)
# ==========================================================================
def _tsx_bolumler():
    metin = TSX.read_text()
    govde = metin[metin.index("bolumler:"):metin.index("kapanis:")]
    sonuc = {}
    for b in re.split(r"\n    \{", govde)[1:]:
        no = int(re.search(r"no: (\d+)", b).group(1))
        yk = float(re.search(r"yakin: ([\d.]+)", b).group(1))
        kam = float(re.search(r"kamera: ([\d.]+)", b).group(1))
        sp = re.search(r"sprite: \{ w: (\d+), h: (\d+), fps: (\d+), x: (\[[\d, ]+\]|\d+), taban: (\d+)", b)
        x = eval(sp.group(4))
        yy = re.search(r"yaziY: (\d+)", b)
        ust = int(yy.group(1)) if yy else 300
        alt = 0
        for m in re.finditer(r"satirlar: \[([^\]]*)\], sure: [\d.]+(?:, boy: (\d+))?", b):
            sat = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
            boy = int(m.group(2) or 92)
            sig = min(boy, math.floor(950 / (max(len(s) for s in sat) * 0.46)))
            alt = max(alt, (ust + len(sat) * sig * 1.12 + 8) / 2)          # ekran px → ızgara
        sonuc.setdefault(no, []).append(dict(yk=yk, kam=kam, w=int(sp.group(1)), h=int(sp.group(2)),
                                             sx=x if isinstance(x, list) else [x], taban=int(sp.group(5)),
                                             ust=ust / 2, alt=alt))
    return sonuc


B = _tsx_bolumler()


def P(no):
    """Sahnenin ilk Bolum ayarı (çizim ölçüsü bunu kullanır; denetimler bütün Bolum'ları dolaşır)."""
    return B[no][0]


# ==========================================================================
# DENETİMLER (cem_sultan/celebi/hezarfen kalıbı, sıkılaştırılmış)
# ==========================================================================
def _gorunur_yerel(b, z, kam, sx):
    """Sprite yerel x'inde görünür aralık: odak sx, yakınlaşma z, kamera kaydırması kam (ekran px, sprite ·0.65)."""
    w = b["w"]
    kay = kam * 0.65 / 2
    return w / 2 - sx / z - kay, w / 2 + (540 - sx) / z - kay


def _kadraj(no, kare, esik=0.8, pay=6, serbest_alt=0):
    """Her Bolum için 24 karenin hepsinde: tam opak piksellerin (alfa>200) sol ve sağ uçları, sahne başında (yakin, -kamera)
    ve sonunda (yakin·1.06, +kamera) görünür aralığın `pay` px içinde kalır (kenarda kesilen nesne yok). Figür sprite'ın
    üstüne değmez (kesik baş). Opak piksellerin en az `esik` oranı görünür aralıkta. serbest_alt: sprite'ın en alt satırlarında
    bilerek tam genişlikte çizilen su/döşeme bandı kenar denetimi dışındadır."""
    for b in B[no]:
        w, h = b["w"], b["h"]
        for i in range(KARE):
            t = yeni(w, h)
            kare(t, duz(h - 1, w), i)
            alfa = t.getchannel("A")
            tam = alfa.point(lambda v: 255 if v > 200 else 0)
            ust = tam.crop((0, 0, w, h - serbest_alt)).getbbox()
            if not ust:
                continue
            if ust[1] <= 1:
                n = sum(tam.crop((0, 0, w, 2)).histogram()[1:])
                if n > 12:
                    raise RuntimeError(f"Sahne {no}: kare {i} sprite'ın üst kenarına değiyor (h={h})")
            for sx in b["sx"]:
                for z, kam in ((b["yk"], -b["kam"]), (b["yk"], b["kam"]), (b["yk"] * 1.06, -b["kam"]), (b["yk"] * 1.06, b["kam"])):
                    a, c = _gorunur_yerel(b, z, kam, sx)
                    if ust[0] < a + pay or ust[2] > c - pay:
                        raise RuntimeError(f"Sahne {no}, kare {i}, sx {sx}: opak nesne x {ust[0]}-{ust[2]}, görünür "
                                           f"{a:.0f}-{c:.0f} (pay {pay}): kenarda kesiliyor")
            if i % 6 == 0:
                toplam = sum(alfa.histogram()[1:])
                for sx in b["sx"]:
                    a, c = _gorunur_yerel(b, b["yk"], 0, sx)
                    ici = sum(alfa.crop((max(0, int(a)), 0, min(w, int(c)), h)).histogram()[1:])
                    if ici / toplam < esik:
                        raise RuntimeError(f"Sahne {no}: figürlerin %{int(100 * ici / toplam)}'i görünür aralıkta")


def _bant(no, orta_denetle=True, pay=4):
    """Yazı bandı denetimi (celebi kalıbı): sprite'ın ve (dış mekânda) orta planın görünür sütunlarında, ekran yazısının
    dünya y bandında 2 pikselden fazla opak satır olmamalı. İç mekânda orta plan bir duvardır; denetim sprite'a uygulanır,
    duvar süsleri ayrıca bandın altına konur."""
    spr = Image.open(PUB / f"sahne{no}-karakter.png").convert("RGBA").getchannel("A")
    ort = Image.open(PUB / f"sahne{no}-orta.png").convert("RGBA").getchannel("A")
    for b in B[no]:
        w, h, taban = b["w"], b["h"], b["taban"]
        o = taban - 12
        for z in (b["yk"], b["yk"] * 1.06):
            y0, y1 = int(o - (o - b["ust"]) / z), int(o - (o - b["alt"]) / z) + pay
            for sx in b["sx"]:
                a, c = _gorunur_yerel(b, z, 0, sx)
                for i in range(0, KARE, 3):
                    for y in range(max(y0, taban - h), y1 + 1):
                        ly = y - (taban - h)
                        n = sum(spr.crop((i * w + max(0, int(a)), ly, i * w + min(w, int(c)), ly + 1)).histogram()[1:])
                        if n > 2:
                            raise RuntimeError(f"Sahne {no}: sprite (kare {i}) yazı bandına giriyor: dünya y {y} "
                                               f"(bant {y0}-{y1}, yakin {z:.2f})")
                if orta_denetle:
                    gx0 = PAY + sx - sx / z - 8
                    gx1 = PAY + sx + (540 - sx) / z + 8
                    for y in range(y0, y1 + 1):
                        n = sum(ort.crop((int(gx0), y, int(gx1), y + 1)).histogram()[1:])
                        if n > 2:
                            raise RuntimeError(f"Sahne {no}: orta plandaki yapı yazı bandına giriyor: y {y} (bant {y0}-{y1})")


def _orta_gorunur(no, xler, pay=8):
    """Orta plandaki önemli nesnelerin (gemi, kule, kapı) ızgara x aralıkları (x0, x1; orta plan koordinatı) her Bolum'un
    başında ve sonunda (kamera ve %6 yakınlaşma dahil) görünür aralıkta kalmalı."""
    for b in B[no]:
        for sx in b["sx"]:
            for z, kam in ((b["yk"], -b["kam"]), (b["yk"] * 1.06, b["kam"]), (b["yk"] * 1.06, -b["kam"]), (b["yk"], b["kam"])):
                kay = kam * 0.65 / 2
                a = PAY + sx - sx / z - kay + pay
                c = PAY + sx + (540 - sx) / z - kay - pay
                for x0, x1 in xler:
                    if x0 < a or x1 > c:
                        raise RuntimeError(f"Sahne {no}: orta plan nesnesi x {x0}-{x1} görünür aralık {a:.0f}-{c:.0f} dışında")


def _bitir(no, kare, esik=0.8, pay=6, serbest_alt=0, orta_denetle=True):
    _kadraj(no, kare, esik, pay, serbest_alt)
    b = P(no)
    sprite(no, "karakter", b["w"], b["h"], KARE, kare)
    _bant(no, orta_denetle)


_ONBELLEK = {}


def olcek(ad, yakin, cizim, oran):
    """Figür kutusu kadraj yüksekliğinin >= oran'ı olan en küçük s (0.1 adım); kadrajda görünen ızgara yüksekliği 960/yakin."""
    anahtar = (ad, yakin, oran)
    if anahtar in _ONBELLEK:
        return _ONBELLEK[anahtar]
    hedef = oran * 960 / yakin
    s = 1.0
    while s <= 14.0:
        t = yeni(600, 560)
        cizim(t, round(s, 1), duz(557, 600))
        bb = _bb(t)
        if bb and bb[3] - bb[1] >= hedef:
            _ONBELLEK[anahtar] = round(s, 1)
            return _ONBELLEK[anahtar]
        s += 0.1
    raise RuntimeError(f"olcek({ad}): ulaşılamadı")


def K(no, oran=0.30):
    """Sahnenin insan ölçeği: başlıksız ayakta insan kadraj yüksekliğinin `oran`'ı (brif: en az %30)."""
    return olcek("kisi", P(no)["yk"], lambda t, s, z: figur(t, beyefendi, 300, z, s), oran)


def _kz(no):
    """Kandil zinciri: sprite'ın üst kenarından (tavan) kadrajın üst kenarının biraz altına."""
    b = P(no)
    ust_gorunen = (b["taban"] - 12) * (1 - 1 / b["yk"])
    return max(40, int(ust_gorunen - (b["taban"] - b["h"])) + 10)


# ==========================================================================
# YENİ FİGÜRLER: İNSANLAR
# ==========================================================================
def _bas_geo(zemin, x, s):
    y = zemin_y(zemin, x, 6 * s)
    return y, y - int(13.6 * s), max(2, int(1.7 * s)), y - int(11 * s)


def _fes(d, img, x, by, r, s, yon, renk="#b8201e", sorguc=False):
    alt = by - int(0.5 * r)
    tepe = by - r - int(1.9 * s)
    d.polygon([(x - r - 1, alt), (x - r + 1, tepe), (x + r - 1, tepe), (x + r + 1, alt)], fill=hex2(renk))
    d.line([x - r + 1, tepe, x + r - 1, tepe], fill=hex2(_ac(renk, 0.3)))
    d.line([x - r, alt, x + r, alt], fill=hex2(_ac(renk, -0.3)))
    px_ = x - (r - 1) * yon                                    # püskül: tepeden ense tarafına sarkar
    d.line([x, tepe, px_, tepe + 1, px_, alt - 1], fill=hex2("#1a1a2a"), width=_u(0.4, s))
    if sorguc:                                                 # padişah: elmas iğne ve beyaz sorguç tüyü
        gx = x + int(0.5 * r) * yon
        gy = (alt + tepe) // 2 + 1
        d.ellipse([gx - _u(0.45, s), gy - _u(0.45, s), gx + _u(0.45, s), gy + _u(0.45, s)], fill=hex2("#f0f4ff"),
                  outline=hex2("#e0b040"))
        for i in range(_u(2.4, s)):
            piksel(img, gx + (i * i // 10) * yon, gy - 1 - i, hex2("#f8f6f0"))
            piksel(img, gx + (i * i // 10) * yon + 1, gy - 1 - i, hex2("#d8d4cc"))


def _silindir(d, x, by, r, s, renk="#16161c"):
    k = hex2(renk)
    d.rectangle([x - r - _u(0.8, s), by - r + _u(0.2, s), x + r + _u(0.8, s), by - r + _u(0.6, s)], fill=k)
    d.rectangle([x - r + 1, by - r - int(3.2 * s), x + r - 1, by - r + _u(0.2, s)], fill=k)
    d.line([x - r + 1, by - r - int(1.2 * s), x + r - 1, by - r - int(1.2 * s)], fill=hex2("#3a3a46"))


def _kasket(d, x, by, r, s, yon, renk):
    d.chord([x - r - 1, by - r - _u(1.2, s), x + r + 1, by + _u(0.1, s)], 180, 360, fill=hex2(renk))
    d.line([x, by - r + _u(0.1, s), x + (r + _u(1.6, s)) * yon, by - r + _u(0.4, s)], fill=hex2(_ac(renk, -0.3)), width=_u(0.5, s))


def _sac(d, x, by, r, s, yon, renk, favori=False):
    d.chord([x - r - 1, by - r - 1, x + r + 1, by + r // 3], 180, 360, fill=hex2(renk))
    ax = x - r * yon
    d.rectangle([min(ax, ax + (r // 3) * yon), by - r // 2, max(ax, ax + (r // 3) * yon), by + r // 3], fill=hex2(renk))
    if favori:                                                 # 1840'lar: yanak boyunca favori
        fx = x - int(0.2 * r) * yon
        d.rectangle([min(fx, fx - _u(0.5, s) * yon), by + 1, max(fx, fx - _u(0.5, s) * yon), by + r - 1], fill=hex2(renk))


def beyefendi(img, x, zemin, s=1.0, govde="#2a2a34", bas=None, bas_renk="#b8201e", sac="#3a2a1e", sakal=None,
              favori=False, biyik=None, yon=1, adim=None, kol=0.0, silah=None, yaka="#f0ece4", kravat=None,
              nisan=False, sorguc=False, zincir=False, yelek=None):
    """Yeni figür: 19-20. yüzyıl erkeği. timur_figur.kisi gövdesi (kemersiz, diz hizasında biten setre/redingot) +
    beyaz yaka, düğme dizisi, saç (ve favori/bıyık), başlık: 'fes' (sorguc=True: padişahın elmas iğneli sorguçlu fesi),
    'silindir' (silindir şapka), 'kasket'. nisan: göğüste altın nişan; zincir: belediye başkanı zinciri; kravat: modern
    kravat rengi. Ayakları kisi gibi zemine basar; göz satırı hiçbir başlıkla örtülmez."""
    kisi(img, x, zemin, s, govde=govde, bas=None, sakal=sakal, yon=yon, adim=adim, kol=kol, silah=silah, kemer=None)
    d = ImageDraw.Draw(img)
    y, by, r, ust = _bas_geo(zemin, x, s)
    if yelek:
        d.polygon([(x - int(0.9 * s), ust), (x + int(0.9 * s), ust), (x + int(0.7 * s), ust + int(4 * s)),
                   (x - int(0.7 * s), ust + int(4 * s))], fill=hex2(yelek))
    d.polygon([(x - int(1.1 * s), ust), (x + int(1.1 * s), ust), (x, ust + int(1.6 * s))], fill=hex2(yaka))   # yaka
    if kravat:
        d.polygon([(x - _u(0.35, s), ust + int(0.5 * s)), (x + _u(0.35, s), ust + int(0.5 * s)),
                   (x + _u(0.4, s), ust + int(3.6 * s)), (x, ust + int(4.2 * s)), (x - _u(0.4, s), ust + int(3.6 * s))],
                  fill=hex2(kravat))
    else:
        for k in range(2, 7, 2):                                        # düğme dizisi
            piksel(img, x + int(0.6 * s) * yon, ust + int(k * s * 0.9), hex2(_ac(govde, 0.45)))
    if nisan:
        nx = x - int(1.0 * s) * yon
        ny = ust + int(2.2 * s)
        d.ellipse([nx - _u(0.6, s), ny - _u(0.6, s), nx + _u(0.6, s), ny + _u(0.6, s)], fill=hex2("#e0b040"),
                  outline=hex2("#8a5a10"))
        piksel(img, nx, ny, hex2("#c8302a"))
    if zincir:
        for k in range(-10, 11):
            a = k / 10
            piksel(img, x + int(a * 1.8 * s), ust + int((1 - a * a) * 2.6 * s) + 1, hex2("#e8c040"))
        d.ellipse([x - _u(0.6, s), ust + int(2.4 * s), x + _u(0.6, s), ust + int(3.6 * s)], fill=hex2("#e8c040"))
    if bas != "fes" or True:
        _sac(d, x, by, r, s, yon, sac, favori)
    if biyik:
        d.rectangle([x + int(0.1 * s) * yon - (_u(0.9, s) if yon < 0 else 0), by + int(0.55 * s),
                     x + int(0.1 * s) * yon + (_u(0.9, s) if yon > 0 else 0), by + int(0.55 * s) + _u(0.3, s)], fill=hex2(biyik))
    if bas == "fes":
        _fes(d, img, x, by, r, s, yon, bas_renk, sorguc)
    elif bas == "silindir":
        _silindir(d, x, by, r, s, bas_renk)
    elif bas == "kasket":
        _kasket(d, x, by, r, s, yon, bas_renk)


def hanim(img, x, zemin, s=1.0, elbise="#2a3a6a", sac="#3a2418", bas=None, bas_renk="#e0b040", yon=1, kol=0.0,
          silah=None, kusak=None, etek=1.0, adim=None):
    """Yeni figür: uzun etekli kadın (19. yy ve bugün). Çan biçimli etek zemine değer (ayak ucu görünür), dar korsaj,
    ortadan ayrılmış saç ve ensede topuz; bas: 'tac' (küçük taç), 'sal' (başı ve omuzları örten yün şal; göz açık).
    kusak: omuzdan çapraz şerit (kraliçe). etek: etek genişliği çarpanı (modern elbise için <1)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 7 * s)
    temas_golgesi(img, x, y, 9 * s * etek)
    bel = y - int(8.5 * s)
    ust = y - int(11 * s)
    g = hex2(elbise)
    gen = 3.6 * s * etek
    sal = 0 if adim is None else int(SIN(adim) * 0.6 * s)
    for k, ax in ((0, -1), (1, 1)):                                        # ayak uçları
        fx = x + int((ax * 1.1 * s + (sal if k else -sal)))
        d.line([fx, y - 1, fx + _u(0.9, s) * yon, y - 1], fill=hex2(KOYU))
    d.polygon([(x - int(1.4 * s), bel), (x + int(1.4 * s), bel), (x + int(gen) + sal, y - 2), (x - int(gen) + sal, y - 2)], fill=g)
    for k in (-1, 1):                                                       # etek kıvrımları
        d.line([x + int(k * 0.6 * s), bel + int(1 * s), x + int(k * gen * 0.55), y - 3], fill=hex2(_ac(elbise, -0.18)))
    d.polygon([(x - int(1.6 * s), ust), (x + int(1.6 * s), ust), (x + int(1.3 * s), bel), (x - int(1.3 * s), bel)],
              fill=hex2(_ac(elbise, 0.08)))
    d.line([x - int(1.4 * s), bel, x + int(1.4 * s), bel], fill=hex2(_ac(elbise, -0.3)))
    if kusak:
        d.line([x - int(1.4 * s) * yon, ust, x + int(1.2 * s) * yon, bel - 1], fill=hex2(kusak), width=_u(0.6, s))
    omuz = (x + int(0.6 * s) * yon, ust + int(1 * s))
    if kol > 0:
        el = (x + int(3.4 * s) * yon, ust - int(3 * s * kol) + int(1.5 * s))
    else:
        el = (x + int(2.2 * s) * yon, ust + int(4.6 * s))
    d.line([*omuz, *el], fill=hex2(_ac(elbise, -0.2)), width=_u(0.9, s))
    piksel(img, el[0], el[1], hex2(TEN))
    if silah == "mektup":
        ex, ey = el
        d.rectangle([ex - int(1.5 * s), ey - int(2 * s), ex + int(1.5 * s), ey + int(1 * s)], fill=hex2("#f0e0b0"), outline=hex2("#8a6a3a"))
        piksel(img, ex, ey, hex2("#c8302a"))
    elif silah == "bohca":
        ex, ey = el
        d.ellipse([ex - int(1.8 * s), ey - int(1 * s), ex + int(1.6 * s), ey + int(2.6 * s)], fill=hex2("#8a7a5a"))
        d.line([ex - int(1 * s), ey, ex + int(1 * s), ey + int(2 * s)], fill=hex2("#5a4a32"))
    by = y - int(13.4 * s)
    r = max(2, int(1.7 * s))
    d.rectangle([x - _u(0.5, s), ust - int(0.8 * s), x + _u(0.5, s), ust], fill=hex2(TEN))           # boyun
    d.ellipse([x - r, by - r, x + r, by + r], fill=hex2(TEN))
    if s >= 3:
        d.rectangle([x + int(0.6 * s) * yon, by - int(0.3 * s), x + int(0.6 * s) * yon + _u(0.3, s), by], fill=hex2(KOYU))
    else:
        piksel(img, x + int(1 * s) * yon, by, hex2(KOYU))
    if bas == "sal":
        k = hex2(bas_renk)
        d.chord([x - r - 1, by - r - 1, x + r + 1, by], 180, 360, fill=k)
        arka = x - r * yon
        d.rectangle([min(arka, arka - int(0.9 * s) * yon), by - int(0.8 * s), max(arka, arka - int(0.9 * s) * yon),
                     by + r + int(1.5 * s)], fill=k)
        d.polygon([(x - int(2 * s), ust - 1), (x + int(2 * s), ust - 1), (x + int(2.4 * s), ust + int(3 * s)),
                   (x - int(2.4 * s), ust + int(3 * s))], fill=k)                                        # omuz örtüsü
        return
    d.chord([x - r - 1, by - r - 1, x + r + 1, by + r // 2], 180, 360, fill=hex2(sac))
    d.line([x, by - r, x, by - r // 2], fill=hex2(_ac(sac, 0.25)))                                      # ortadan ayrık
    tx = x - (r + _u(0.6, s)) * yon                                                                      # topuz
    d.ellipse([tx - _u(0.9, s), by - _u(0.6, s), tx + _u(0.9, s), by + _u(1.2, s)], fill=hex2(sac))
    if bas == "tac":
        tr = int(r * 0.75)
        d.rectangle([x - tr, by - r - _u(1.2, s), x + tr, by - r + _u(0.2, s)], fill=hex2(bas_renk))
        for dx in (-tr, 0, tr):
            d.polygon([(x + dx - _u(0.5, s), by - r - _u(1.2, s)), (x + dx, by - r - _u(2.2, s)),
                       (x + dx + _u(0.5, s), by - r - _u(1.2, s))], fill=hex2(bas_renk))
        piksel(img, x, by - r - _u(0.6, s), hex2("#c8302a"))


# ==========================================================================
# YENİ FİGÜRLER: GEMİLER, KIR, KASABA
# ==========================================================================
def yelkenli(img, x, su_y, s=1.0, yon=1, faz=0.0, govde="#1e1a1a", serit="#d8d0b8", yelken="#e8e0cc", acik=0.0,
             bayrak=None):
    """Yeni figür: 1840'ların iki direkli tüccar yelkenlisi (brik). Kara gövde, açık renk boya şeridi, baş bodoslama
    çubuğu, iki direk, seren ve armalar. acik 0: yelkenler serenlere sarılı (limanda), 1: açık. Gövde su çizgisine
    oturur (alt kısmı suya batık), dalgayla hafifçe iner kalkar. Boyut: s=1'de gövde boyu 36, direk 32 px (insan s=1 ≈ 15 px
    olduğundan gemi insanın yaklaşık 18 katı uzun; yanındaki figürlerle bu oranda çizilir)."""
    d = ImageDraw.Draw(img)
    y = su_y + int(round(SIN(faz) * 0.5 * s))
    L = 18 * s
    on_ = x + L * yon
    arka = x - L * yon
    gv = hex2(govde)
    ust = y - int(5 * s)
    pts = [(arka, ust - int(1.2 * s)), (on_ - 2 * s * yon, ust - int(0.6 * s)), (on_ + 1 * s * yon, ust - int(1.4 * s)),
           (on_ - 3 * s * yon, y + int(2 * s)), (arka + 2 * s * yon, y + int(2 * s)), (arka - 0.5 * s * yon, ust)]
    d.polygon(pts, fill=gv)
    d.line([arka, ust + int(1.2 * s), on_ - 2 * s * yon, ust + int(1.6 * s)], fill=hex2(serit), width=_u(0.8, s))
    for k in range(int(-L + 4 * s), int(L - 5 * s), max(3, int(3 * s))):              # şeritte lomboz izleri
        piksel(img, x + k * yon, ust + int(1.4 * s), hex2(_ac(govde, 0.1)))
    d.line([arka, ust - int(1.2 * s), on_ - 2 * s * yon, ust - int(0.6 * s)], fill=hex2(_ac(govde, 0.35)))   # küpeşte
    bc = (on_ + 1 * s * yon, ust - int(1.4 * s))
    bu = (on_ + 8 * s * yon, ust - int(5 * s))
    d.line([*bc, *bu], fill=hex2("#4a3220"), width=_u(0.7, s))                        # baş bodoslama
    ip = hex2("#3a2a1e")
    direkler = []
    for dk, boy in ((8, 31), (-7, 29)):
        mx = x + int(dk * s) * yon
        tep = ust - int(boy * s)
        d.line([mx, ust, mx, tep], fill=hex2("#4a3220"), width=_u(0.9, s))
        direkler.append((mx, tep))
        for j, (yy, gen) in enumerate(((0.30, 7.5), (0.55, 6.2), (0.78, 4.8))):        # serenler ve yelkenler
            sy = ust - int(boy * s * (1 - yy))
            g2 = gen * s
            d.line([mx - g2, sy, mx + g2, sy], fill=hex2("#4a3220"), width=_u(0.5, s))
            if acik > 0:
                yh = int(boy * s * 0.22 * acik)
                sis = SIN(faz) * 0.6 * s * yon
                d.polygon([(mx - g2, sy), (mx + g2, sy), (mx + g2 * 0.95 + sis, sy + yh), (mx - g2 * 0.95 + sis, sy + yh)],
                          fill=hex2(yelken if j % 2 == 0 else _ac(yelken, -0.06)))
                d.line([mx - g2 * 0.95 + sis, sy + yh, mx + g2 * 0.95 + sis, sy + yh], fill=hex2(_ac(yelken, -0.25)))
            else:
                d.line([mx - g2 + 1, sy + _u(0.6, s), mx + g2 - 1, sy + _u(0.6, s)], fill=hex2(yelken), width=_u(0.8, s))
    d.line([*direkler[0], *bu], fill=ip)                                                # armalar (halatlar)
    d.line([*direkler[0], *direkler[1]], fill=ip)
    d.line([*direkler[1], arka, ust - int(1.2 * s)], fill=ip)
    for mx, tep in direkler:
        for k in (-1, 1):
            d.line([mx, tep + int(4 * s), mx + int(3.5 * s) * k, ust - int(1 * s)], fill=hex2("#5a4632"))
    if bayrak:
        mx, tep = direkler[1]
        dal = SIN(faz) * 0.8 * s
        d.polygon([(mx, tep), (mx - 5 * s * yon, tep + int(1 * s) + dal), (mx - 5 * s * yon, tep + int(2.8 * s) + dal),
                   (mx, tep + int(3 * s))], fill=hex2(bayrak))
    return y + int(2 * s)


def su_cizgisi(t, x0, x1, y, f, renk="#e8f4fc", alfa=170):
    """Gövdenin suya girdiği satırda köpük: gövde suya oturuyor okunur."""
    for x in range(int(x0), int(x1)):
        if (x * 7 + int(f * 24)) % 5 < 3:
            piksel(t, x, y, hex2(renk, alfa))


def kulube(img, x, zemin, s=1.0, duvar="#d8d2c4", dam="#8a7448", cokmus=False, duman_=None):
    """Yeni figür: İrlanda taş kulübesi. Kireç badanalı alçak taş duvar, yuvarlatılmış saz dam, ahşap kapı, küçük pencere.
    cokmus=True: dam çökmüş (yalnız iki kalkan duvarı ve birkaç mertek), kapı boşluğu karanlık: terk edilmiş ev.
    Düz zemine kurulur. Dönen değer: baca noktası."""
    d = ImageDraw.Draw(img)
    g = int(12 * s)
    y = duz_zemin(zemin, x - g, x + g, "kulube", tolerans=max(3, int(s)))
    temel(img, zemin, x - g, x + g, y, _ac(duvar, -0.4))
    temas_golgesi(img, x, y, 2 * g + 4)
    h = int(7 * s)
    d.rectangle([x - g, y - h, x + g, y - 1], fill=hex2(duvar))
    rnd = random.Random(int(x * 3 + s * 10))
    for _ in range(int(14 * s)):                                                     # taş dokusu
        px_, py_ = rnd.randint(x - g + 1, x + g - 2), rnd.randint(y - h + 1, y - 2)
        d.line([px_, py_, px_ + _u(1.2, s), py_], fill=hex2(_ac(duvar, -0.12)))
    kx = x - int(4 * s)
    d.rectangle([kx - int(1.6 * s), y - int(5.2 * s), kx + int(1.6 * s), y - 1], fill=hex2("#1a1410" if cokmus else "#5a3a22"))
    d.rectangle([x + int(4 * s), y - int(5 * s), x + int(6.5 * s), y - int(3 * s)], fill=hex2("#2a2420"))
    bx = x + int(7 * s)
    if not cokmus:
        d.chord([x - g - int(1.5 * s), y - h - int(7 * s), x + g + int(1.5 * s), y - h + int(4 * s)], 180, 360, fill=hex2(dam))
        for k in range(-g, g, max(2, int(2 * s))):                                  # saz çizgileri
            d.line([x + k, y - h - int(1 * s), x + k + int(0.6 * s), y - h - int(4 * s)], fill=hex2(_ac(dam, -0.15)))
        d.line([x - g - int(1.5 * s), y - h - int(1.4 * s), x + g + int(1.5 * s), y - h - int(1.4 * s)], fill=hex2(_ac(dam, -0.3)))
        d.rectangle([bx - _u(1, s), y - h - int(7.5 * s), bx + _u(1, s), y - h - int(3 * s)], fill=hex2(_ac(duvar, -0.25)))
        return (bx, y - h - int(7.5 * s))
    for k in (-1, 1):                                                                # yalnız kalkan duvarları kalmış
        ex = x + k * g
        d.polygon([(ex, y - h), (ex - k * int(4 * s), y - h), (ex - k * int(1.5 * s), y - h - int(5 * s))], fill=hex2(duvar))
    for k in (-0.5, 0.1, 0.6):                                                       # kırık mertekler
        mx = x + int(k * g)
        d.line([mx, y - h, mx + int(2 * s), y - h - int(3 * s)], fill=hex2("#3a2a1a"), width=_u(0.5, s))
    return None


def patates(img, x, zemin, s=1.0, curuk=1.0, faz=0.0, tohum=1):
    """Yeni figür: patates fidesi; curuk 0 yeşil, 1 kararmış ve çökmüş (yanıklık). Sap dibi zemine sabit."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 4 * s)
    rnd = random.Random(tohum)
    yap = _ac("#4a7a3a", -0.55 * curuk) if curuk < 0.6 else "#3a2e22"
    sarki = 1.0 - 0.55 * curuk
    for j in range(5):
        a = -0.9 + j * 0.45 + rnd.uniform(-0.15, 0.15)
        L = (3.2 + rnd.uniform(-0.5, 0.5)) * s
        uc = (x + math.sin(a) * L + SIN(faz + j * 0.2) * 0.2 * s, y - 1 - math.cos(a) * L * sarki)
        d.line([x, y - 1, *uc], fill=hex2(yap), width=_u(0.5, s))
        d.ellipse([uc[0] - _u(0.7, s), uc[1] - _u(0.5, s), uc[0] + _u(0.7, s), uc[1] + _u(0.5, s)],
                  fill=hex2(_ac(yap, rnd.uniform(-0.1, 0.12))))
        if curuk > 0.5 and rnd.random() < 0.6:
            piksel(img, uc[0], uc[1], hex2("#1a1612"))


# ==========================================================================
# YENİ FİGÜRLER: EŞYA
# ==========================================================================
def defter_sayfa(d, img, x0, y0, x1, y1, renk="#f2ead4", satir="#9a8a70", cilt="#5a2e1e", kalin=1):
    """Açık defter (önden): iki sayfa, ortada cilt sırtı, sayfalarda yalnızca satır çizgileri (rakam/yazı yok)."""
    d.rectangle([x0 - kalin - 1, y0 - 1, x1 + kalin + 1, y1 + kalin + 1], fill=hex2(cilt))
    d.rectangle([x0, y0, x1, y1], fill=hex2(renk))
    orta_ = (x0 + x1) // 2
    d.line([orta_, y0, orta_, y1], fill=hex2(_ac(renk, -0.3)))
    adim = max(2, (y1 - y0) // 9)
    rnd = random.Random(x0 * 7 + y0)
    for yy in range(y0 + adim, y1 - 1, adim):
        for a, b in ((x0 + 2, orta_ - 2), (orta_ + 2, x1 - 2)):
            uz = int((b - a) * rnd.uniform(0.55, 1.0))
            d.line([a, yy, a + uz, yy], fill=hex2(satir))
    d.line([x0 + (orta_ - x0) * 2 // 3, y0 + 1, x0 + (orta_ - x0) * 2 // 3, y1 - 1], fill=hex2("#c8a0a0"))   # sütun çizgisi
    d.line([orta_ + (x1 - orta_) * 2 // 3, y0 + 1, orta_ + (x1 - orta_) * 2 // 3, y1 - 1], fill=hex2("#c8a0a0"))


def kursu(img, x, zemin, s=1.0, renk="#5a3820", defter=True, cilt="#5a2e1e", mum=None):
    """Yeni figür: yüksek kâtip kürsüsü (ayakta yazılır). Dört ayak zemine basar, eğik üst tabla izleyiciye dönük;
    tablada açık defter (satır çizgili). Dönen değer: tabla arka kenarının y'si (mürekkep hokkası buraya)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 14 * s)
    temas_golgesi(img, x, y, 15 * s)
    w2 = int(7 * s)
    on_y = y - int(8 * s)
    arka_y = y - int(10.5 * s)
    k = hex2(_ac(renk, -0.35))
    for ax in (-w2 + int(0.5 * s), w2 - int(1.5 * s)):
        d.rectangle([x + ax, on_y, x + ax + _u(1, s), y - 1], fill=k)
    d.rectangle([x - w2 + int(0.5 * s), y - int(2 * s), x + w2 - int(0.5 * s), y - int(1.4 * s)], fill=k)      # alt kuşak
    d.rectangle([x - w2, on_y - int(1.2 * s), x + w2, on_y + int(1 * s)], fill=hex2(_ac(renk, -0.12)))     # ön kasa
    d.polygon([(x - w2, on_y - int(1.2 * s)), (x + w2, on_y - int(1.2 * s)), (x + w2 - int(0.6 * s), arka_y),
               (x - w2 + int(0.6 * s), arka_y)], fill=hex2(renk))
    d.line([x - w2, on_y - int(1.2 * s), x + w2, on_y - int(1.2 * s)], fill=hex2(_ac(renk, 0.3)))
    if defter:
        defter_sayfa(d, img, x - int(5.5 * s), arka_y + int(0.3 * s), x + int(5.5 * s), on_y - int(1.4 * s), cilt=cilt,
                     kalin=_u(0.3, s))
    hx = x + w2 - int(1.4 * s)
    d.rectangle([hx - _u(0.6, s), arka_y - _u(0.9, s), hx + _u(0.6, s), arka_y], fill=hex2("#1a1a22"))          # hokka
    d.line([hx, arka_y - _u(0.9, s), hx + int(1.4 * s), arka_y - int(3 * s)], fill=hex2("#f4f0e6"), width=_u(0.3, s))  # tüy kalem
    return arka_y


def masa(img, x, zemin, s=1.0, renk="#5a3820", ortu=None, gen=8.0, yuk=6.5):
    """Yeni figür: masa (önden). Ayaklar zemine basar; ortu verilirse örtü ön yüzü yere kadar örter. Üst yüz y'sini döndürür."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 2 * gen * s)
    temas_golgesi(img, x, y, 2 * gen * s + 2)
    w2 = int(gen * s)
    ust = y - int(yuk * s)
    if ortu:
        d.rectangle([x - w2, ust, x + w2, y - 1], fill=hex2(ortu))
        for k in range(-w2 + int(2 * s), w2, max(3, int(3 * s))):
            d.line([x + k, ust + int(1.5 * s), x + k, y - 2], fill=hex2(_ac(ortu, -0.08)))
        d.line([x - w2, ust + int(1 * s), x + w2, ust + int(1 * s)], fill=hex2(_ac(ortu, -0.2)))
    else:
        k = hex2(_ac(renk, -0.35))
        for ax in (-w2 + int(0.6 * s), w2 - int(1.6 * s)):
            d.rectangle([x + ax, ust, x + ax + _u(1, s), y - 1], fill=k)
        d.rectangle([x - w2 + int(0.6 * s), ust + int(0.8 * s), x + w2 - int(0.6 * s), ust + int(2 * s)], fill=hex2(_ac(renk, -0.15)))
    d.rectangle([x - w2 - _u(0.4, s), ust - _u(0.8, s), x + w2 + _u(0.4, s), ust], fill=hex2(renk if not ortu else _ac(ortu, 0.1)))
    return ust - _u(0.8, s)


def sandalye(img, x, zemin, s=1.0, renk="#4a2c18", minder="#7a1e22"):
    """Yeni figür: arkalıklı sandalye (önden; oturanın arkasında kalır). Ayaklar zemine basar."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    temas_golgesi(img, x, y, 6 * s)
    w2 = int(2.8 * s)
    k = hex2(renk)
    for ax in (-w2, w2 - _u(0.7, s)):
        d.rectangle([x + ax, y - int(14 * s), x + ax + _u(0.7, s), y - 1], fill=k)
    d.rectangle([x - w2, y - int(14 * s), x + w2, y - int(12.5 * s)], fill=hex2(_ac(renk, 0.15)))
    d.rectangle([x - w2 + _u(0.7, s), y - int(12.5 * s), x + w2 - _u(0.7, s), y - int(8 * s)], fill=hex2(minder))
    d.rectangle([x - w2, y - int(6 * s), x + w2, y - int(5.2 * s)], fill=k)


def oturan_masada(img, x, zemin, s, cizen, **kw):
    """Masada oturan: figür, ayakları masanın arkasında (görünmez) kalacak biçimde 4.5·s alçaltılarak çizilir; masa
    sonra önüne çizilir. Kaşık figür (beyefendi/hanim) parametreleri kw ile."""
    alt = [v + int(4.5 * s) for v in zemin]
    cizen(img, x, alt, s, **kw)


def kese(img, x, zemin, s=1.0, renk="#8a1e22", serit="#e0b040"):
    """Yeni figür: ağzı büzülü para kesesi; tabanı yere (masaya) oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 3 * s)
    d.ellipse([x - int(1.8 * s), y - int(3 * s), x + int(1.8 * s), y - 1], fill=hex2(renk))
    d.polygon([(x - int(0.8 * s), y - int(2.8 * s)), (x + int(0.8 * s), y - int(2.8 * s)), (x + int(1.2 * s), y - int(4 * s)),
               (x - int(1.2 * s), y - int(4 * s))], fill=hex2(_ac(renk, 0.1)))
    d.line([x - int(0.9 * s), y - int(2.9 * s), x + int(0.9 * s), y - int(2.9 * s)], fill=hex2(serit), width=_u(0.3, s))


def kitaplar_yigini(img, x, zemin, s=1.0, adet=4, tohum=1):
    """Yeni figür: yatık kitap yığını (masa üstüne ya da yere oturur)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 5 * s)
    rnd = random.Random(tohum)
    for j in range(adet):
        rk = rnd.choice(("#8a2a2a", "#2a4a7a", "#3a5a3a", "#6a4a2a", "#5a3a5a"))
        w = rnd.uniform(3.6, 4.8) * s
        ox = rnd.uniform(-0.6, 0.6) * s
        yy = y - 1 - int(j * 1.1 * s)
        d.rectangle([x - w / 2 + ox, yy - int(1.1 * s) + 1, x + w / 2 + ox, yy], fill=hex2(rk), outline=hex2("#2a1a10"))
        d.line([x - w / 2 + ox + 1, yy - int(0.5 * s), x + w / 2 + ox - 1, yy - int(0.5 * s)], fill=hex2("#e8dcc0"))


def mum(t, x, y, f, s=1.0, k=0):
    """Pirinç şamdanda tek mum (y = oturduğu yüzey). Alev dikişsiz titrer, çevresine sıcak ışık düşer."""
    d = ImageDraw.Draw(t)
    d.rectangle([x - _u(1.3, s), y - _u(0.5, s), x + _u(1.3, s), y - 1], fill=hex2("#c8a040"), outline=hex2("#5a3a10"))
    d.rectangle([x - _u(0.3, s), y - int(1.5 * s), x + _u(0.3, s), y - _u(0.5, s)], fill=hex2("#a88030"))
    d.rectangle([x - _u(0.45, s), y - int(4 * s), x + _u(0.45, s), y - int(1.5 * s)], fill=hex2("#f4ecd8"))
    alev = 1.3 + 0.35 * SIN(f, 3) + 0.15 * SIN(f + k * 0.3, 5)
    ay = y - int(4 * s)
    d.polygon([(x - _u(0.5, s), ay), (x, ay - int(alev * 1.6 * s)), (x + _u(0.5, s), ay)], fill=hex2("#f8c040"))
    piksel(t, x, ay - 1, hex2("#fff4c0"))
    rnd = random.Random(x * 13 + y)
    for r in range(int(2 * s), int(8 * s), 2):
        for a in range(0, 360, 12):
            px_, py_ = x + math.cos(math.radians(a)) * r * 1.2, ay + math.sin(math.radians(a)) * r
            if py_ < y - 1 and rnd.random() < 0.4 * (1 - r / (8 * s)):
                piksel(t, px_, py_, hex2("#ffd479", 50))


def samdan(t, x, z, f, s=1.0, adet=3, sonuk=0.0):
    """Ayaklı şamdan (ölçekli): ayak zemine basar; adet mum. sonuk 0-1: mumlar kısalır, alev küçülür (1861 sahnesi)."""
    d = ImageDraw.Draw(t)
    y = z[0]
    temas_golgesi(t, x, y, 5 * s)
    d.rectangle([x - int(2 * s), y - _u(1, s), x + int(2 * s), y - 1], fill=hex2("#8a6a2a"))
    d.line([x, y - _u(1, s), x, y - int(10 * s)], fill=hex2("#c8a040"), width=_u(0.6, s))
    d.line([x - int(2.6 * s), y - int(10 * s), x + int(2.6 * s), y - int(10 * s)], fill=hex2("#c8a040"), width=_u(0.5, s))
    for k in range(adet):
        mx = x + int((k - (adet - 1) / 2) * 2.6 * s)
        boy = int((3 - 1.8 * sonuk) * s)
        d.rectangle([mx - _u(0.4, s), y - int(10 * s) - boy, mx + _u(0.4, s), y - int(10 * s)], fill=hex2("#f0e8d0"))
        alev = (1.2 - 0.5 * sonuk) + 0.3 * SIN(f + k * 0.37, 3)
        ay = y - int(10 * s) - boy
        d.polygon([(mx - _u(0.45, s), ay), (mx, ay - int(alev * 1.5 * s)), (mx + _u(0.45, s), ay)], fill=hex2("#f8c040"))
        piksel(t, mx, ay - 1, hex2("#fff4c0"))
    rnd = random.Random(x)
    for r in range(int(2 * s), int(9 * s), 2):
        for a in range(0, 360, 10):
            px_, py_ = x + math.cos(math.radians(a)) * r * 1.3, y - int(12 * s) + math.sin(math.radians(a)) * r
            if py_ < y - 1 and rnd.random() < 0.35 * (1 - r / (9 * s)) * (1 - 0.5 * sonuk):
                piksel(t, px_, py_, hex2("#ffd479", 55))


def kandil(t, x, ust, f, zincir=36, s=1.0):
    """Tavandan zincirle sarkan pirinç avize-kandil (dikişsiz salınım): zincir tavana kadar."""
    d = ImageDraw.Draw(t)
    sal = SIN(f) * 1.2
    for k in range(0, zincir, 3):
        piksel(t, x + sal * k / zincir, ust + k, hex2("#8a7a4a"))
    ky, kx = ust + zincir, x + sal
    d.polygon([(kx - 7 * s, ky), (kx + 7 * s, ky), (kx + 4 * s, ky + 7 * s), (kx - 4 * s, ky + 7 * s)], fill=hex2("#c8a040"),
              outline=hex2("#5a3a10"))
    for dx in (-5, 0, 5):
        alev = 1.5 + 0.5 * SIN(f + dx * 0.05, 3)
        d.polygon([(kx + dx * s - 1, ky), (kx + dx * s, ky - alev * 2.5), (kx + dx * s + 1, ky)], fill=hex2("#f8c040"))
    rnd = random.Random(int(x))
    for r in range(5, 24, 3):
        for a in range(0, 360, 12):
            px_, py_ = kx + math.cos(math.radians(a)) * r * 1.3, ky + math.sin(math.radians(a)) * r
            if rnd.random() < 0.4 * (1 - r / 24):
                piksel(t, px_, py_, hex2("#f8e8a0", 55))


def raf(img, x, zemin, s=1.0, dolu=True, tohum=1, renk="#5a3a22", kat=4, gen=9):
    """Yeni figür: ahşap kitap rafı (celebi.kitap_rafi kalıbı, ölçülü). Gövde zemine oturur; dolu=False raflar boş
    (yalnız toz). Dönen değer: üst y."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 2 * gen * s)
    temas_golgesi(img, x, y, 2 * gen * s + 1)
    hy = int(7.4 * s)
    ust = y - kat * hy - int(1.5 * s)
    d.rectangle([x - int(gen * s), ust, x + int(gen * s), y - 1], fill=hex2(_ac(renk, -0.45)))
    for k in (-1, 1):
        d.rectangle([x + k * int(gen * s) - _u(0.6, s), ust, x + k * int(gen * s) + _u(0.6, s), y - 1], fill=hex2(renk))
    d.rectangle([x - int((gen + 1) * s), ust - int(1.2 * s), x + int((gen + 1) * s), ust], fill=hex2(_ac(renk, 0.15)))
    rnd = random.Random(tohum)
    for j in range(kat):
        sy = y - int(1.2 * s) - j * hy
        d.rectangle([x - int(gen * s), sy, x + int(gen * s), sy + _u(0.8, s)], fill=hex2(renk))
        if dolu:
            bx = x - int((gen - 1) * s)
            while bx < x + int((gen - 1.5) * s):
                bw = max(1, int(rnd.uniform(0.9, 1.8) * s))
                bh = int(rnd.uniform(4.2, 6.2) * s)
                rk = rnd.choice(("#8a2a2a", "#2a4a7a", "#3a6a3a", "#a8803a", "#5a3a5a", "#7a5a3a"))
                d.rectangle([bx, sy - bh, min(bx + bw, x + int((gen - 1) * s)), sy - 1], fill=hex2(rk))
                piksel(img, bx, sy - bh + 1, hex2(_ac(rk, 0.4)))
                bx += bw + 1
        else:
            for _ in range(int(4 * s)):
                piksel(img, x - int((gen - 1) * s) + rnd.randint(0, int((2 * gen - 2) * s)), sy - 1, hex2("#8a7a6a"))
    return ust


def vitrin(img, x, zemin, s=1.0, ahsap="#4a2e1a"):
    """Yeni figür: ayaklı camlı vitrin (kütüphane); içinde eğik altlıkta mühürlü mektup. Ayaklar zemine basar."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 14 * s)
    temas_golgesi(img, x, y, 15 * s)
    w2 = int(7 * s)
    k = hex2(ahsap)
    for ax in (-w2 + int(0.5 * s), w2 - int(1.5 * s)):
        d.rectangle([x + ax, y - int(6 * s), x + ax + _u(1, s), y - 1], fill=k)
    d.rectangle([x - w2, y - int(7.5 * s), x + w2, y - int(6 * s)], fill=k)
    d.rectangle([x - w2, y - int(11.5 * s), x + w2, y - int(7.5 * s)], fill=hex2("#b8d0d8"))              # cam
    d.rectangle([x - int(5 * s), y - int(10.8 * s), x + int(5 * s), y - int(7.8 * s)], fill=hex2("#e8dcc0"))  # mektup
    for yy in range(int(10 * s), int(8.2 * s), -max(1, int(0.6 * s))):
        d.line([x - int(4 * s), y - yy, x + int(3.5 * s), y - yy], fill=hex2("#8a7a60"))
    d.ellipse([x + int(2.6 * s), y - int(9.4 * s), x + int(4.2 * s), y - int(7.9 * s)], fill=hex2("#a8281e"))  # mühür
    for k2 in range(0, int(4 * s), 2):                                                                  # cam parıltısı
        piksel(img, x - w2 + int(1 * s) + k2, y - int(11 * s) + k2 // 2, hex2("#ffffff", 150))
    d.rectangle([x - w2, y - int(11.5 * s), x + w2, y - int(7.5 * s)], outline=k)
    d.line([x - w2 - _u(0.4, s), y - int(11.6 * s), x + w2 + _u(0.4, s), y - int(11.6 * s)], fill=hex2(_ac(ahsap, 0.25)), width=_u(0.6, s))


def baski_makinesi(img, x, zemin, s=1.0, faz=0.0):
    """Yeni figür: 1840'ların demir el baskı makinesi (Washington tipi). Dökme demir kemerli çerçeve iki ayakla zemine
    basar; ortada vida ve pres plakası faz ile iner kalkar; önde kızak üstünde harf kasası ve kâğıt (frisket).
    Dönen değer: kolun bağlandığı nokta."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 26 * s)
    temas_golgesi(img, x, y, 28 * s)
    dem, ac = hex2("#2a2c30"), hex2("#4a4e56")
    for k in (-1, 1):
        d.rectangle([x + k * int(6 * s) - _u(1.2, s), y - int(22 * s), x + k * int(6 * s) + _u(1.2, s), y - 1], fill=dem)
        d.rectangle([x + k * int(6 * s) - int(2.4 * s), y - _u(1.2, s), x + k * int(6 * s) + int(2.4 * s), y - 1], fill=dem)
    d.chord([x - int(7.2 * s), y - int(26 * s), x + int(7.2 * s), y - int(19 * s)], 180, 360, fill=dem)
    d.rectangle([x - int(7.2 * s), y - int(22.6 * s), x + int(7.2 * s), y - int(21 * s)], fill=dem)
    d.line([x - int(5 * s), y - int(24.5 * s), x + int(5 * s), y - int(24.5 * s)], fill=ac)
    ty = y - int(11 * s)
    d.rectangle([x - int(13 * s), ty, x + int(13 * s), ty + _u(1.4, s)], fill=hex2("#5a3a22"))          # kızak
    for ux in (-12, 12):
        d.rectangle([x + int(ux * s) - _u(0.5, s), ty + 1, x + int(ux * s) + _u(0.5, s), y - 1], fill=hex2("#3a2614"))
    d.rectangle([x - int(4.5 * s), ty - _u(1, s), x + int(4.5 * s), ty - 1], fill=hex2("#1a1a1e"))         # harf kasası
    d.rectangle([x + int(5 * s), ty - _u(0.6, s), x + int(12 * s), ty - 1], fill=hex2("#f0e8d4"))
    bas = (1 - math.cos(faz * 2 * math.pi)) / 2
    py = y - int(18 * s) + int(bas * 5 * s)
    d.rectangle([x - _u(0.7, s), y - int(21 * s), x + _u(0.7, s), py], fill=hex2("#8a8a94"))
    d.rectangle([x - int(5 * s), py, x + int(5 * s), py + _u(1.4, s)], fill=ac)
    return (x + int(1 * s), y - int(17 * s) + int(bas * 2 * s))


def dizustu(img, x, y, s=1.0):
    """Yeni figür: masa üstünde açık dizüstü bilgisayar (2010); ekran soluk mavi ışır, yazı yok."""
    d = ImageDraw.Draw(img)
    d.rectangle([x - int(3 * s), y - _u(0.5, s), x + int(3 * s), y - 1], fill=hex2("#6a6e74"))
    d.polygon([(x - int(2.8 * s), y - _u(0.5, s)), (x + int(2.8 * s), y - _u(0.5, s)), (x + int(2.4 * s), y - int(4.4 * s)),
               (x - int(2.4 * s), y - int(4.4 * s))], fill=hex2("#3a3e44"))
    d.rectangle([x - int(2 * s), y - int(4 * s), x + int(2 * s), y - int(1 * s)], fill=hex2("#a8c8e8"))
    for k in range(3):
        d.line([x - int(1.6 * s), y - int((3.4 - k * 0.8) * s), x + int((0.4 + k * 0.3) * s), y - int((3.4 - k * 0.8) * s)],
               fill=hex2("#d8e8f8"))


def kagit(img, x, y, s=1.0, muhur=False, renk="#f0e6d0"):
    """Masa üstünde düz duran kâğıt (önden hafif eğik); satır çizgileri; muhur: kırmızı balmumu."""
    d = ImageDraw.Draw(img)
    d.polygon([(x - int(3 * s), y - 1), (x + int(3 * s), y - 1), (x + int(2.4 * s), y - _u(1.2, s)), (x - int(2.4 * s), y - _u(1.2, s))],
              fill=hex2(renk), outline=hex2(_ac(renk, -0.3)))
    if muhur:
        piksel(img, x + int(1.6 * s), y - _u(0.7, s), hex2("#b8281e"))


def kale_kapisi(img, x, zemin, s=1.0, tas="#8a8478", arma=None, soluk=False):
    """Yeni figür: iki yuvarlak kuleli kasaba kapısı (barbakan). Kuleler ve kemerli geçit düz zemine oturur, mazgallı
    tepe. arma: ('hilal'|'aslan', renk) kapı kemerinin üstünde asılı kalkan. Dönen değer: en üst y."""
    d = ImageDraw.Draw(img)
    g = int(11 * s)
    y = duz_zemin(zemin, x - g, x + g, "kale_kapisi", tolerans=max(3, int(s)))
    temel(img, zemin, x - g, x + g, y, _ac(tas, -0.4))
    temas_golgesi(img, x, y, 2 * g + 2)
    h = int(26 * s)
    for k in (-1, 1):
        cx = x + k * int(7 * s)
        d.rectangle([cx - int(4 * s), y - h, cx + int(4 * s), y - 1], fill=hex2(tas))
        d.line([cx + int(2.5 * s) * k, y - h, cx + int(2.5 * s) * k, y - 1], fill=hex2(_ac(tas, -0.2)))
        for yy in range(y - h + int(6 * s), y - int(2 * s), int(6 * s)):
            d.rectangle([cx - _u(0.5, s), yy, cx + _u(0.5, s), yy + int(1.6 * s)], fill=hex2("#1e1a18"))   # mazgal deliği
        for mx in range(cx - int(4 * s), cx + int(4 * s), int(2 * s)):
            d.rectangle([mx, y - h - int(1.2 * s), mx + int(1 * s), y - h], fill=hex2(tas))
    d.rectangle([x - int(3 * s), y - int(22 * s), x + int(3 * s), y - 1], fill=hex2(_ac(tas, -0.06)))
    d.chord([x - int(2.6 * s), y - int(10 * s), x + int(2.6 * s), y - int(4.6 * s)], 180, 360, fill=hex2("#1e1a18"))
    d.rectangle([x - int(2.6 * s), y - int(7.4 * s), x + int(2.6 * s), y - 1], fill=hex2("#1e1a18"))
    for yy in range(y - int(22 * s), y - int(10 * s), max(2, int(1.6 * s))):
        d.line([x - int(3 * s), yy, x + int(3 * s), yy], fill=hex2(_ac(tas, -0.12)))
    if arma:
        arma_kalkani(img, x, y - int(12 * s), s * 0.55, arma[0], arma[1])
    return y - h - int(1.2 * s)


def arma_kalkani(img, x, alt_y, s=1.0, desen="hilal", zemin_renk="#2a4a8a"):
    """Yeni figür: kalkan biçimli arma (bir yüzeye asılı ya da tutulu; alt ucu alt_y'de). desen 'hilal': altın hilal ve
    üstünde yıldız; 'aslan': kırmızı üstünde üç altın aslan izi (eski İngiliz kraliyet arması, yazısız)."""
    d = ImageDraw.Draw(img)
    w2 = int(5 * s)
    ust = alt_y - int(11 * s)
    d.polygon([(x - w2, ust), (x + w2, ust), (x + w2, ust + int(6 * s)), (x, alt_y), (x - w2, ust + int(6 * s))],
              fill=hex2(zemin_renk), outline=hex2("#e0b040"))
    if desen == "hilal":
        cy = ust + int(6.4 * s)
        r = int(3.2 * s)
        d.ellipse([x - r, cy - r, x + r, cy + r], fill=hex2("#f0c850"))
        d.ellipse([x - r + int(0.4 * s), cy - r - int(1.4 * s), x + r - int(0.4 * s), cy + r - int(1.6 * s)], fill=hex2(zemin_renk))
        yx, yy = x, ust + int(2.6 * s)
        rr = max(1, int(1.4 * s))
        noktalar = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            rk = rr if k % 2 == 0 else rr * 0.45
            noktalar.append((yx + math.cos(a) * rk, yy + math.sin(a) * rk))
        d.polygon(noktalar, fill=hex2("#f0c850"))
    else:
        for j in range(3):
            ay = ust + int((2 + j * 2.8) * s)
            d.rectangle([x - int(2.6 * s), ay, x + int(2.2 * s), ay + _u(1, s)], fill=hex2("#f0c850"))
            d.rectangle([x + int(1.6 * s), ay - _u(0.8, s), x + int(2.6 * s), ay], fill=hex2("#f0c850"))
            d.line([x - int(2.6 * s), ay, x - int(3.4 * s), ay - _u(1, s)], fill=hex2("#f0c850"))


def sancak(img, x, zemin, s=1.0, f=0.0, renk="#b8201e", desen="aslan"):
    """Yeni figür: eski armalı sancak. Direk zemine dikili (dibinde taş tümsek), bayrak rüzgârda dalgalanır; üstünde
    yazısız arma deseni."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 3 * s)
    temas_golgesi(img, x, y, 4 * s)
    d.chord([x - int(2 * s), y - int(1.6 * s), x + int(2 * s), y + int(1.6 * s)], 180, 360, fill=hex2("#6a6258"))
    tep = y - int(24 * s)
    d.line([x, y - 1, x, tep], fill=hex2("#5a3a22"), width=_u(0.7, s))
    d.ellipse([x - _u(0.7, s), tep - _u(1.2, s), x + _u(0.7, s), tep], fill=hex2("#e0b040"))
    for i in range(int(9 * s)):
        dal = SIN(f - i / (9 * s) * 0.8) * 0.6 * s * (i / (9 * s))
        d.line([x + 1 + i, tep + int(1 * s) + dal, x + 1 + i, tep + int(7 * s) + dal], fill=hex2(renk))
    if desen == "aslan":
        for j in range(3):
            ay = tep + int((2 + j * 1.6) * s) + int(SIN(f - 0.4) * 0.3 * s)
            d.line([x + int(2.5 * s), ay, x + int(5.5 * s), ay], fill=hex2("#f0c850"))
            piksel(img, x + int(5.8 * s), ay - 1, hex2("#f0c850"))


def beyaz_kule(img, x, zemin, s=1.0, tas="#e0dccc"):
    """Yeni figür: Selanik'in Beyaz Kulesi (silindir gövde, üstte dar kule ve mazgallar). Düz zemine oturur."""
    d = ImageDraw.Draw(img)
    g = int(7 * s)
    y = duz_zemin(zemin, x - g, x + g, "beyaz_kule", tolerans=max(3, int(s)))
    temel(img, zemin, x - g, x + g, y, _ac(tas, -0.4))
    temas_golgesi(img, x, y, 2 * g + 2)
    h = int(20 * s)
    d.rectangle([x - g, y - h, x + g, y - 1], fill=hex2(tas))
    d.rectangle([x + int(3 * s), y - h, x + g, y - 1], fill=hex2(_ac(tas, -0.15)))
    for mx in range(x - g, x + g, int(2 * s)):
        d.rectangle([mx, y - h - int(1.2 * s), mx + int(1 * s), y - h], fill=hex2(tas))
    d.rectangle([x - int(3.5 * s), y - h - int(6 * s), x + int(3.5 * s), y - h], fill=hex2(_ac(tas, -0.05)))
    for mx in range(x - int(3.5 * s), x + int(3.5 * s), int(2 * s)):
        d.rectangle([mx, y - h - int(7 * s), mx + int(1 * s), y - h - int(6 * s)], fill=hex2(tas))
    for yy in (y - int(6 * s), y - int(12 * s), y - int(17 * s)):
        for k in (-3, 0, 3):
            d.rectangle([x + int(k * s) - _u(0.4, s), yy, x + int(k * s) + _u(0.4, s), yy + int(1.6 * s)], fill=hex2("#3a3630"))
    return y - h - int(7 * s)


def cami(img, x, zemin, s=1.0, tas="#d8ccb4", kursun="#7a8490"):
    """Yeni figür (hezarfen.kubbeli_cami kalıbı, sade): kubbeli cami ve tek minare; düz zemine oturur."""
    d = ImageDraw.Draw(img)
    g = int(8 * s)
    y = duz_zemin(zemin, x - g, x + g + int(3 * s), "cami", tolerans=max(3, int(s)))
    temel(img, zemin, x - g, x + g + int(3 * s), y, _ac(tas, -0.4))
    hy = y - int(7 * s)
    d.rectangle([x - g, hy, x + g, y - 1], fill=hex2(tas))
    for k in (-4, 0, 4):
        d.chord([x + int(k * s) - _u(1, s), hy + int(2 * s), x + int(k * s) + _u(1, s), hy + int(5 * s)], 180, 360, fill=hex2("#3a3430"))
        d.rectangle([x + int(k * s) - _u(1, s), hy + int(3.5 * s), x + int(k * s) + _u(1, s), hy + int(5 * s)], fill=hex2("#3a3430"))
    d.chord([x - int(5 * s), hy - int(6 * s), x + int(5 * s), hy + int(1 * s)], 180, 360, fill=hex2(kursun))
    d.line([x, hy - int(3.5 * s), x, hy - int(5 * s)], fill=hex2("#e0b040"))
    mx = x + g + int(1.5 * s)
    mh = int(20 * s)
    d.rectangle([mx - _u(0.8, s), y - mh, mx + _u(0.8, s), y - 1], fill=hex2(_ac(tas, 0.06)))
    d.rectangle([mx - _u(1.4, s), y - int(15 * s), mx + _u(1.4, s), y - int(14.4 * s)], fill=hex2(_ac(tas, -0.15)))
    d.polygon([(mx - _u(0.9, s), y - mh), (mx, y - mh - int(4 * s)), (mx + _u(0.9, s), y - mh)], fill=hex2(kursun))
    return y - mh - int(4 * s)


def tugla_evler(img, x0, x1, zemin, s=1.0, tohum=1, tugla=("#8a3a2a", "#7a3426", "#9a4a34"), isik=False):
    """Yeni figür: bitişik nizam 3-4 katlı tuğla evler (Londra, Dublin, New York): beyaz pencere söveleri, düz korniş,
    bacalar. Düz zemine kurulur. Dönen değer: en üst y."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "tugla_evler", tolerans=max(3, int(s)))
    temel(img, zemin, x0, x1, y, "#3a2a22")
    rnd = random.Random(tohum)
    kh = max(4, int(round(6 * s)))
    en_ust = y
    x = x0
    while x1 - x >= int(8 * s):
        gw = min(int(rnd.randint(14, 20) * s), x1 - x)
        kat = rnd.choice((3, 4, 4))
        ust = y - kat * kh - int(2 * s)
        tg = rnd.choice(tugla)
        d.rectangle([x, ust, x + gw - 1, y - 1], fill=hex2(tg))
        d.line([x, ust, x, y - 1], fill=hex2(_ac(tg, -0.35)))
        d.rectangle([x, ust - _u(1, s), x + gw - 1, ust], fill=hex2(_ac(tg, 0.25)))
        bx = x + int(gw * 0.25)
        d.rectangle([bx, ust - int(3 * s), bx + int(2 * s), ust - _u(1, s)], fill=hex2(_ac(tg, -0.2)))
        en_ust = min(en_ust, ust - int(3 * s))
        n = max(2, gw // max(3, int(5 * s)))
        for k in range(kat):
            fy = y - k * kh
            for j in range(n):
                wx = x + int((j + 0.5) * gw / n)
                if k == 0 and j == 0:
                    d.rectangle([wx - int(1.2 * s), fy - int(5 * s), wx + int(1.2 * s), fy - 1], fill=hex2("#2a1e18"))
                    continue
                a, b = fy - kh + max(1, int(1.4 * s)), fy - max(1, int(1.2 * s))
                d.rectangle([wx - int(1 * s), a, wx + int(1 * s), b], fill=hex2("#f8d880" if isik and rnd.random() < 0.4 else "#2a3440"))
                d.line([wx - int(1.2 * s), a - 1, wx + int(1.2 * s), a - 1], fill=hex2("#e8e0d0"))
        x += gw
    return en_ust


def ambar(img, x0, x1, zemin, s=1.0, tas="#6a645c", cati="#3a3a40"):
    """Yeni figür: rıhtım ambarı (taş, kırma çatılı, büyük kapılı tahıl deposu). Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "ambar", tolerans=max(3, int(s)))
    temel(img, zemin, x0, x1, y, "#2a2622")
    h = int(16 * s)
    d.rectangle([x0, y - h, x1, y - 1], fill=hex2(tas))
    d.polygon([(x0 - _u(1, s), y - h), (x1 + _u(1, s), y - h), ((x0 + x1) // 2, y - h - int(6 * s))], fill=hex2(cati))
    for kx in range(x0 + int(4 * s), x1 - int(3 * s), int(9 * s)):
        d.rectangle([kx - int(2 * s), y - int(7 * s), kx + int(2 * s), y - 1], fill=hex2("#3a2a1a"))
        d.rectangle([kx - _u(1, s), y - int(13 * s), kx + _u(1, s), y - int(10 * s)], fill=hex2("#2a2a30"))
    return y - h - int(6 * s)


def eski_ev_sirasi(img, x0, x1, zemin, s=1.0, tohum=1, sivalar=("#c8c0b0", "#b8b0a0", "#d8d0c0", "#a8a090"), cati="#4a4a52",
                   isik=False):
    """Yeni figür: İrlanda kasabası iki-üç katlı sıvalı evleri (düz cephe, arduvaz dam, baca). Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "eski_ev_sirasi", tolerans=max(3, int(s)))
    temel(img, zemin, x0, x1, y, "#3a3430")
    rnd = random.Random(tohum)
    kh = max(4, int(round(6 * s)))
    en_ust = y
    x = x0
    while x1 - x >= int(8 * s):
        gw = min(int(rnd.randint(12, 18) * s), x1 - x)
        kat = rnd.choice((2, 3, 3))
        ust = y - kat * kh
        sv = rnd.choice(sivalar)
        d.rectangle([x, ust, x + gw - 1, y - 1], fill=hex2(sv))
        d.line([x, ust, x, y - 1], fill=hex2(_ac(sv, -0.3)))
        d.polygon([(x - 1, ust), (x + gw, ust), (x + gw - int(2 * s), ust - int(4 * s)), (x + int(2 * s), ust - int(4 * s))], fill=hex2(cati))
        bx = x + int(gw * 0.7)
        d.rectangle([bx, ust - int(6 * s), bx + int(1.6 * s), ust - int(3 * s)], fill=hex2(_ac(sv, -0.25)))
        en_ust = min(en_ust, ust - int(6 * s))
        n = max(2, gw // max(3, int(5 * s)))
        for k in range(kat):
            fy = y - k * kh
            for j in range(n):
                wx = x + int((j + 0.5) * gw / n)
                if k == 0 and j == n // 2:
                    d.rectangle([wx - int(1.2 * s), fy - int(5 * s), wx + int(1.2 * s), fy - 1], fill=hex2("#3a2a20"))
                    continue
                a, b = fy - kh + max(1, int(1.4 * s)), fy - max(1, int(1.2 * s))
                d.rectangle([wx - int(1 * s), a, wx + int(1 * s), b], fill=hex2("#f8d880" if isik and rnd.random() < 0.5 else "#2a3440"))
        x += gw
    return en_ust


def cuval(img, x, zemin, s=1.0, renk="#c8b080"):
    """Yeni figür: ağzı bağlı tahıl çuvalı; tabanı zemine (ya da alttaki çuvala) oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 4 * s)
    d.rounded_rectangle([x - int(2.2 * s), y - int(4.6 * s), x + int(2.2 * s), y - 1], radius=max(1, int(1 * s)), fill=hex2(renk))
    d.polygon([(x - int(0.9 * s), y - int(4.6 * s)), (x + int(0.9 * s), y - int(4.6 * s)), (x + int(1.2 * s), y - int(5.8 * s)),
               (x - int(1.2 * s), y - int(5.8 * s))], fill=hex2(_ac(renk, -0.1)))
    d.line([x - int(1 * s), y - int(4.7 * s), x + int(1 * s), y - int(4.7 * s)], fill=hex2("#5a4a2a"))
    d.line([x - int(1.6 * s), y - int(2.4 * s), x + int(1.6 * s), y - int(2.4 * s)], fill=hex2(_ac(renk, -0.15)))
    return y - int(4.6 * s)


def cuval_yigini(img, x, zemin, s=1.0, sira=(3, 2, 1), renk="#c8b080"):
    """Üst üste dizili çuvallar: her sıra alttakinin üstüne oturur."""
    yy = zemin_y(zemin, x, 4 * s * sira[0])
    for k, n in enumerate(sira):
        for j in range(n):
            cx = x + int((j - (n - 1) / 2) * 4.4 * s)
            cuval(img, cx, duz(yy, img.width), s, _ac(renk, (j + k) % 2 * -0.06))
        yy -= int(4.2 * s)


def babalar(d, x, y, s=1.0):
    """Rıhtım babası (halat bağlama demiri): rıhtım yüzüne oturur."""
    d.rectangle([x - int(1.2 * s), y - int(2.4 * s), x + int(1.2 * s), y - 1], fill=hex2("#2a2a2e"))
    d.rectangle([x - int(1.7 * s), y - int(3.2 * s), x + int(1.7 * s), y - int(2.4 * s)], fill=hex2("#3a3a40"))


def fener_el(t, ex, ey, f, s=1.0):
    """Elde tutulan fener: tutamaktan sarkar, camında alev titrer, çevreye ışık."""
    d = ImageDraw.Draw(t)
    d.line([ex, ey, ex, ey + int(1 * s)], fill=hex2("#3a3a3a"))
    fy = ey + int(1 * s)
    d.rectangle([ex - int(1 * s), fy, ex + int(1 * s), fy + int(2.6 * s)], fill=hex2("#f8d070"), outline=hex2("#2a2a2a"))
    piksel(t, ex, fy + int(1.3 * s) + int(SIN(f, 3) * 0.6), hex2("#fff8e0"))
    rnd = random.Random(int(ex))
    for r in range(int(2 * s), int(9 * s), 2):
        for a in range(0, 360, 10):
            px_, py_ = ex + math.cos(math.radians(a)) * r * 1.2, fy + int(1.3 * s) + math.sin(math.radians(a)) * r
            if rnd.random() < 0.35 * (1 - r / (9 * s)):
                piksel(t, px_, py_, hex2("#ffd479", 50))
