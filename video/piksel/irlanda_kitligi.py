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
        for i in range(_u(1.5, s)):
            piksel(img, gx - (i * i // 30) * yon, gy - 1 - i, hex2("#f8f6f0"))
            piksel(img, gx - (i * i // 30) * yon + 1, gy - 1 - i, hex2("#d8d4cc"))


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
              nisan=False, sorguc=False, zincir=False, yelek=None, gazete=False):
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
        bx0 = x + int(0.15 * s) * yon
        d.line([bx0 - _u(0.5, s), by + int(0.6 * s), bx0 + _u(0.9, s), by + int(0.6 * s)], fill=hex2(biyik))
    if gazete:                                                          # iki eliyle açık tuttuğu gazete (sütun çizgili)
        gx0, gx1 = x - int(2.8 * s), x + int(2.8 * s)
        gy0, gy1 = ust + int(1.4 * s), ust + int(6 * s)
        d.rectangle([gx0, gy0, gx1, gy1], fill=hex2("#e8e2d0"), outline=hex2("#8a8270"))
        d.line([x, gy0, x, gy1], fill=hex2("#b0a890"))
        for cx in (gx0 + _u(0.6, s), x + _u(0.6, s)):
            d.rectangle([cx, gy0 + _u(0.6, s), cx + int(2 * s), gy0 + _u(1.2, s)], fill=hex2("#3a3630"))
            for yy in range(gy0 + int(1.8 * s), gy1 - 1, max(2, int(0.7 * s))):
                d.line([cx, yy, cx + int(2 * s), yy], fill=hex2("#9a9480"))
        for k in (gx0, gx1):
            piksel(img, k, gy0 + int(2 * s), hex2(TEN))
    if bas == "fes":
        _fes(d, img, x, by, r, s, yon, bas_renk, sorguc)
    elif bas == "silindir":
        _silindir(d, x, by, r, s, bas_renk)
    elif bas == "kasket":
        _kasket(d, x, by, r, s, yon, bas_renk)


def hanim(img, x, zemin, s=1.0, elbise="#2a3a6a", sac="#3a2418", bas=None, bas_renk="#e0b040", yon=1, kol=0.0,
          silah=None, kusak=None, etek=1.0, adim=None, topuz=True):
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
    if topuz:
        d.ellipse([tx - _u(0.9, s), by - _u(0.6, s), tx + _u(0.9, s), by + _u(1.2, s)], fill=hex2(sac))
    else:                                                                                                # bugün: kısa saç
        d.rectangle([min(x - r * yon, x - r * yon - _u(0.5, s) * yon), by - r // 2, max(x - r * yon, x - r * yon - _u(0.5, s) * yon),
                     by + r // 2], fill=hex2(sac))
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


def kursu(img, x, zemin, s=1.0, renk="#5a3820", defter=True, cilt="#5a2e1e", mum=None, egim=2.5):
    """Yeni figür: yüksek kâtip kürsüsü (ayakta yazılır). Dört ayak zemine basar, eğik üst tabla izleyiciye dönük;
    tablada açık defter (satır çizgili). Dönen değer: tabla arka kenarının y'si (mürekkep hokkası buraya)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 14 * s)
    temas_golgesi(img, x, y, 15 * s)
    w2 = int(7 * s)
    on_y = y - int(8 * s)
    arka_y = y - int((8 + egim) * s)
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


# ==========================================================================
# KATMAN YARDIMCILARI
# ==========================================================================
def _bos(no, kat):
    kaydet(yeni(GW if kat in ("orta", "on") else W, H), f"sahne{no}-{kat}.png")


FL = 596          # iç mekânda duvar ile döşemenin birleştiği satır (orta plan); sprite tabanı 634 bunun 38 px önünde


def oda(no, duvar="#4a5a4a", desen="cizgi", lambri="#5a3a22", pencere=("#8a9aa8", "#c8d4dc"), pencere_x=(), zemin="tahta",
        zemin_renk="#6a4a2e", hali=None, tablo=(), perde=None, kemerli=False, isik="#f8d890", ocak=None, raflar=()):
    """İç mekân (Batı tarzı oda, 19. yy - bugün): duvar ve döşeme tek parça hâlinde ORTA planda (810 geniş) durur; böylece
    duvar paralaksla kaymaz, döşemeyle birlikte hareket eder. Gökyüzü ve uzak katmanları duvarın düz rengi.
    desen: 'cizgi' (çizgili duvar kâğıdı), 'damask' (çiçekli), 'tugla', 'sade', 'lambri' (ahşap kaplama).
    pencere_x: orta plan x'lerinde dikdörtgen (kemerli=True: kemerli) pencereler; tablo: (x, renk) çerçeveli resimler;
    perde: pencere perdeleri rengi; ocak: şömine x'i; zemin: 'tahta', 'parke', 'tas', 'mermer'; hali: halı rengi."""
    g = yeni()
    gradyan(g, [_ac(duvar, -0.25), _ac(duvar, -0.15)])
    kaydet(g, f"sahne{no}-gokyuzu.png")
    kaydet(g, f"sahne{no}-uzak.png")
    o = yeni(GW, H)
    d = ImageDraw.Draw(o)
    gradyan(o, [_ac(duvar, -0.22), _ac(duvar, -0.05), duvar], 0, FL)
    rnd = random.Random(no)
    if desen == "cizgi":
        for x in range(0, GW, 12):
            d.line([x, 0, x, FL], fill=hex2(_ac(duvar, 0.07)), width=3)
    elif desen == "damask":
        for y in range(10, FL, 22):
            for x in range((y // 22) % 2 * 11, GW, 22):
                d.polygon([(x, y - 4), (x + 3, y), (x, y + 4), (x - 3, y)], fill=hex2(_ac(duvar, 0.12)))
                piksel(o, x, y, hex2(_ac(duvar, 0.3)))
    elif desen == "tugla":
        for y in range(0, FL, 6):
            d.line([0, y, GW, y], fill=hex2(_ac(duvar, -0.18)))
            for x in range((y // 6) % 2 * 7, GW, 14):
                d.line([x, y, x, y + 6], fill=hex2(_ac(duvar, -0.18)))
    elif desen == "lambri":
        for x in range(0, GW, 18):
            d.line([x, 0, x, FL], fill=hex2(_ac(duvar, -0.15)))
            d.line([x + 1, 0, x + 1, FL], fill=hex2(_ac(duvar, 0.08)))
    d.rectangle([0, 0, GW, 6], fill=hex2(_ac(duvar, -0.3)))
    if lambri:                                                          # alt ahşap kaplama ve süpürgelik
        d.rectangle([0, FL - 34, GW, FL], fill=hex2(lambri))
        d.line([0, FL - 34, GW, FL - 34], fill=hex2(_ac(lambri, 0.35)), width=2)
        for x in range(8, GW, 36):
            d.rectangle([x, FL - 28, x + 26, FL - 6], outline=hex2(_ac(lambri, -0.25)))
    for px_ in pencere_x:
        x0, x1, y0, y1 = px_ - 22, px_ + 22, 500, FL - 40
        if perde:
            d.rectangle([x0 - 10, y0 - 14, x1 + 10, y1 + 4], fill=hex2(perde))
        d.rectangle([x0 - 3, y0 - 3, x1 + 3, y1 + 4], fill=hex2(_ac(duvar, 0.35)))
        if kemerli:
            d.chord([x0 - 3, y0 - 25, x1 + 3, y0 + 19], 180, 360, fill=hex2(_ac(duvar, 0.35)))
            d.chord([x0, y0 - 22, x1, y0 + 22], 180, 360, fill=hex2(pencere[0]))
        gradyan_kutu(o, x0, y0, x1, y1, pencere)
        d.line([px_, y0 - (22 if kemerli else 0), px_, y1], fill=hex2(_ac(duvar, 0.2)), width=2)
        for yy in range(y0 + 14, y1, 14):
            d.line([x0, yy, x1, yy], fill=hex2(_ac(duvar, 0.2)))
        d.rectangle([x0 - 5, y1 + 2, x1 + 5, y1 + 5], fill=hex2(_ac(duvar, 0.45)))
        if perde:
            for k in (-1, 1):
                ex = px_ + k * 26
                d.polygon([(ex, y0 - 14), (ex + k * 10, y0 - 14), (ex + k * 12, y1 + 4), (ex + k * 4, y1 + 4)], fill=hex2(perde))
                d.line([ex + k * 7, y0 - 10, ex + k * 8, y1], fill=hex2(_ac(perde, -0.2)))
        for k in range(0, 30, 2):                                       # pencereden düşen ışık
            for yy in range(y1 + 6, FL + 70, 3):
                if _esik(px_ - 15 + k, yy) < 0.16 * (1 - (yy - y1) / 160):
                    piksel(o, px_ - 15 + k + (yy - y1) // 10, yy, hex2(pencere[1], 50))
    for tx, tr in tablo:                                                # çerçeveli resim (yazısız)
        d.rectangle([tx - 15, 508, tx + 15, 540], fill=hex2("#c8a040"))
        d.rectangle([tx - 12, 511, tx + 12, 537], fill=hex2(tr))
        d.rectangle([tx - 12, 528, tx + 12, 537], fill=hex2(_ac(tr, -0.2)))
        d.ellipse([tx - 4, 515, tx + 4, 527], fill=hex2(_ac(tr, 0.3)))
    if ocak is not None:                                                # şömine: döşemeye oturur
        d.rectangle([ocak - 26, FL - 40, ocak + 26, FL], fill=hex2("#d8d0c0"))
        d.rectangle([ocak - 30, FL - 44, ocak + 30, FL - 40], fill=hex2("#e8e0d0"))
        d.rectangle([ocak - 15, FL - 28, ocak + 15, FL], fill=hex2("#1e1410"))
        for k in range(-10, 11, 3):
            piksel(o, ocak + k, FL - 3 - abs(k) // 4, hex2("#e8701c"))
    # döşeme
    zr = zemin_renk
    for y in range(FL, H):
        d.line([0, y, GW, y], fill=hex2(_ac(zr, -0.18 * min(1, (y - FL) / 200))))
    if zemin in ("tahta", "parke"):
        y, ara = FL, 3.0
        while y < H:
            d.line([0, y, GW, y], fill=hex2(_ac(zr, -0.3)))
            if zemin == "parke":
                for x in range(int((y // 3) % 2 * 10), GW, 20):
                    d.line([x, y, x, y + int(ara)], fill=hex2(_ac(zr, -0.25)))
            ara = ara * 1.15 + 0.3
            y += int(ara)
    elif zemin in ("tas", "mermer"):
        y, ara, k = FL, 4.0, 0
        while y < H:
            d.line([0, y, GW, y], fill=hex2(_ac(zr, -0.2)))
            for x in range(k % 2 * int(ara * 2), GW, int(ara * 4)):
                d.line([x, y, x, y + int(ara)], fill=hex2(_ac(zr, -0.2)))
            ara = ara * 1.2 + 0.4
            y += int(ara)
            k += 1
    if hali:
        d.rectangle([PAY + 150, FL + 14, PAY + 390, H], fill=hex2(hali))
        d.rectangle([PAY + 156, FL + 18, PAY + 384, H], outline=hex2("#e0b040"))
        for y in range(FL + 30, H, 26):
            for x in range(PAY + 170, PAY + 380, 26):
                d.polygon([(x, y - 5), (x + 5, y), (x, y + 5), (x - 5, y)], fill=hex2(_ac(hali, -0.25)))
    for r in range(40, 200, 16):                                        # sıcak ışık halkası
        for a in range(0, 360, 4):
            px_, py_ = PAY + 270 + math.cos(math.radians(a)) * r * 1.6, FL + 40 + math.sin(math.radians(a)) * r * 0.35
            if py_ > FL and _esik(int(px_), int(py_)) < 0.22 * (1 - r / 200):
                piksel(o, px_, py_, hex2(isik, 45))
    kaydet(o, f"sahne{no}-orta.png")
    _bos(no, "on")


def gradyan_kutu(img, x0, y0, x1, y1, renkler):
    k = yeni(x1 - x0 + 1, y1 - y0 + 1)
    gradyan(k, list(renkler))
    img.paste(k, (x0, y0), k)


def gok(no, renkler, gunes_=None, bulutlar=(), bulut_renk=("#fff8ec", "#e8e0d8", "#c8c0c0"), yildiz=0, sis=None):
    img = gokyuzu(no, renkler, gunes_, bulutlar, bulut_renk, 0)
    if yildiz:
        rnd = random.Random(no)
        for _ in range(yildiz):
            x, y = rnd.randrange(W), rnd.randrange(380, 540)
            piksel(img, x, y, hex2("#fff8e0", rnd.choice((110, 170, 240))))
    kaydet(img, f"sahne{no}-gokyuzu.png")
    return img


def uzak_tepe(no, tepe=("#5a7a5a", "#4e6e50"), ufuk=548, ekle=None, su=None):
    """Uzak plan: yumuşak yeşil İrlanda tepeleri (dikişsiz) ve ufuk çizgisi; ekle(img, zemin) ufka oturan yapılar;
    su: (y, renkler) ufuktan aşağısı su (karşı kıyı)."""
    img = yeni()
    hat = sirt(ufuk - 14, 10, no, 3, 0.6, w=W, dongulu=True)
    arazi(img, hat, list(tepe))
    d = ImageDraw.Draw(img)
    d.rectangle([0, ufuk, W, H], fill=hex2(tepe[-1]))
    if ekle:
        ekle(img, duz(ufuk, W))
    if su:
        sy, renkler = su
        for y in range(sy, H):
            d.line([0, y, W, y], fill=hex2(renkler[min(len(renkler) - 1, (y - sy) // 10)]))
    kaydet(img, f"sahne{no}-uzak.png")
    return img


def zemin_orta(no, ust, renkler, tur="cayir", ekle=None, kenar=None, su=None):
    """Orta plan (810 geniş): düz zemin. tur: 'cayir' (çimen dokulu), 'tarla' (sürülmüş sırtlar), 'kaldirim' (arnavut
    kaldırımı), 'toprak' (yol). su: (y0, y1, renkler) ust'ün üstünde, y0-y1 arasında nehir/deniz şeridi (orta planın
    gerisinde karşı kıyı uzak plandadır). ekle(img, z): zemine oturan yapılar ve figürler (z = düz zemin)."""
    img = yeni(GW, H)
    d = ImageDraw.Draw(img)
    rnd = random.Random(no)
    if su:
        y0, y1, sr = su
        for y in range(y0, y1):
            d.line([0, y, GW, y], fill=hex2(sr[min(len(sr) - 1, (y - y0) // 10)]))
        for _ in range(240):
            x, y = rnd.randrange(GW), rnd.randrange(y0 + 1, y1)
            for k in range(rnd.randint(2, 6)):
                piksel(img, x + k, y, hex2(_ac(sr[0], 0.3), 150))
    rk = lambda y: renkler[min(len(renkler) - 1, int((y - ust) / 24))]  # noqa: E731
    for y in range(ust, H):
        d.line([0, y, GW, y], fill=hex2(rk(y)))
    if tur == "kaldirim":
        y, ara, k = ust + 2, 2.5, 0
        while y < H:
            d.line([0, y, GW, y], fill=hex2(_ac(rk(y), -0.18)))
            adim = max(3, int(ara * 2.2))
            for x in range((k % 2) * adim // 2, GW, adim):
                d.line([x, y - int(ara) + 1, x, y - 1], fill=hex2(_ac(rk(y), -0.14)))
            ara = ara * 1.14 + 0.3
            y += int(ara)
            k += 1
    elif tur == "tarla":
        y, ara = ust + 3, 3.0
        while y < H:
            d.line([0, y, GW, y], fill=hex2(_ac(rk(y), -0.22)), width=max(1, int(ara / 3)))
            d.line([0, y - int(ara / 2), GW, y - int(ara / 2)], fill=hex2(_ac(rk(y), 0.08)))
            ara = ara * 1.16 + 0.4
            y += int(ara)
    elif tur in ("cayir", "toprak"):
        for _ in range(3000):
            x, y = rnd.randrange(GW), rnd.randrange(ust + 1, H)
            dy = (y - ust) / 300
            if tur == "cayir":
                d.line([x, y, x + rnd.choice((-1, 0, 1)), y - 1 - int(dy * 4)], fill=hex2(_ac(rk(y), rnd.choice((-0.12, 0.1)))))
            else:
                piksel(img, x, y, hex2(_ac(rk(y), rnd.choice((-0.1, 0.08)))))
    d.line([0, ust, GW, ust], fill=hex2(kenar or _ac(renkler[0], 0.2)))
    if ekle:
        ekle(img, duz(ust + 30))
    kaydet(img, f"sahne{no}-orta.png")
    return img


def on_cimen(no, renkler, isik, boy=90):
    from sahneler import on
    on(no, renkler, isik, boy)


RIHTIM = 600      # liman sahnelerinde orta plandaki taş rıhtımın üst kenarı


def liman_orta(no, su_renk, tas="#6a6460", kenar="#a8a4a0", ust_su=548, ekle_arka=None, ekle_on=None):
    """Orta plan liman: ust_su'dan rıhtıma kadar nehir/deniz, RIHTIM'den aşağısı düz taş rıhtım (derzli), rıhtım
    kenarında babalar. ekle_arka(img): suyun üstündeki kıyı şeridine (karşı kıyı) oturan nesneler; ekle_on(img, z):
    rıhtıma oturan nesneler."""
    img = yeni(GW, H)
    d = ImageDraw.Draw(img)
    for y in range(ust_su, RIHTIM):
        d.line([0, y, GW, y], fill=hex2(su_renk[min(len(su_renk) - 1, (y - ust_su) // 12)]))
    rnd = random.Random(no)
    for _ in range(320):
        x, y = rnd.randrange(GW), rnd.randrange(ust_su + 2, RIHTIM - 2)
        for k in range(rnd.randint(2, 3 + (y - ust_su) // 10)):
            piksel(img, x + k, y, hex2(_ac(su_renk[0], 0.3), 140))
    if ekle_arka:
        ekle_arka(img)
    d.rectangle([0, RIHTIM, GW, H], fill=hex2(tas))
    d.rectangle([0, RIHTIM, GW, RIHTIM + 2], fill=hex2(kenar))
    d.rectangle([0, RIHTIM + 3, GW, RIHTIM + 9], fill=hex2(_ac(tas, -0.25)))      # rıhtım duvarının yüzü
    y, ara, k = RIHTIM + 10, 3.0, 0
    while y < H:
        d.line([0, y, GW, y], fill=hex2(_ac(tas, -0.12)))
        adim = int(ara * 5)
        for x in range((k % 2) * adim // 2, GW, adim):
            d.line([x, y, x, y + int(ara)], fill=hex2(_ac(tas, -0.12)))
        ara = ara * 1.2 + 0.4
        y += int(ara)
        k += 1
    for bx in range(PAY + 40, PAY + 520, 120):
        babalar(d, bx, RIHTIM + 2, 2.0)
    if ekle_on:
        ekle_on(img, duz(RIHTIM + 30))
    kaydet(img, f"sahne{no}-orta.png")
    return img


def kasaba_uzak(no, gok_alt, tepe, ev_renk, ufuk=546, kilise=True, su=None, isik=False):
    """Uzak plan: yeşil tepeler ve ufuk çizgisine (karşı kıyıya) oturan kasaba silüeti: damlar, bacalar, sivri kilise
    kulesi. Yatayda dikişsiz."""
    def ekle(img, z):
        d = ImageDraw.Draw(img)
        rnd = random.Random(no + 5)
        x = 0
        while x < W:
            w = rnd.randint(7, 13)
            h = rnd.randint(6, 12)
            rk = rnd.choice(ev_renk)
            d.rectangle([x, ufuk - h, min(W - 1, x + w), ufuk], fill=hex2(rk))
            d.polygon([(x, ufuk - h), (min(W - 1, x + w), ufuk - h), (min(W - 1, x + w - 2), ufuk - h - 3), (x + 2, ufuk - h - 3)],
                      fill=hex2(_ac(rk, -0.35)))
            if rnd.random() < 0.5:
                d.rectangle([x + 3, ufuk - h - 5, x + 4, ufuk - h - 3], fill=hex2(_ac(rk, -0.3)))
            if isik and rnd.random() < 0.6:
                piksel(img, x + 3, ufuk - h // 2, hex2("#f8c860"))
            x += w + rnd.randint(1, 3)
        if kilise:
            for kx in (120, 390):
                kr = _ac(ev_renk[0], -0.2)
                d.rectangle([kx - 4, ufuk - 26, kx + 4, ufuk], fill=hex2(kr))
                d.polygon([(kx - 4, ufuk - 26), (kx + 4, ufuk - 26), (kx, ufuk - 40)], fill=hex2(_ac(kr, -0.2)))
    return uzak_tepe(no, tepe, ufuk, ekle, su)


# ==========================================================================
# KİŞİLER (renk kimlikleri bütün videoda aynı)
# ==========================================================================
PADISAH = dict(govde="#1e2a4a", bas="fes", bas_renk="#b8201e", sac="#2a1a12", biyik="#2a1a12", nisan=True, sorguc=True)
KATIP_OS = dict(govde="#2a2a30", bas="fes", bas_renk="#a01e1c", sac="#3a2a1a", sakal="#3a2a1a")
NAZIR = dict(govde="#3a2a3a", bas="fes", bas_renk="#a8201e", sac="#4a4a4a", sakal="#8a8a88", nisan=True)
WELLESLEY = dict(govde="#1a1a24", sac="#6a4a2a", favori=True, yelek="#8a7a5a")
LONDRA_1 = dict(govde="#2a2a2a", sac="#8a8a88", favori=True, yelek="#5a2a2a")
LONDRA_2 = dict(govde="#3a3428", sac="#3a2418", favori=True)
KATIP_LON = dict(govde="#3a3a40", sac="#5a3a20")
VICTORIA = dict(elbise="#2a3a7a", sac="#2a1a12", bas="tac", bas_renk="#e8c040", kusak="#4a7ad0")
SU_GECE = ("#1e2a40", "#1a2638", "#162232", "#121e2c")


def gemi_suda(t, x, su_y, s, f, su_renk, dunya_ust, yon=1, alt=None, **kw):
    """Yelkenli + gövdenin suya batık kısmını örten, orta plandaki suyla AYNI renkte yerel su yaması (dikiş görünmez),
    su çizgisinde köpük. su_renk(dunya_y) → renk."""
    figur(t, yelkenli, x, su_y, s, yon, f, **kw)
    d = ImageDraw.Draw(t)
    x0, x1 = int(x - 20 * s), int(x + 20 * s)
    for y in range(su_y + 1, min(t.height if alt is None else alt, su_y + int(2 * s) + 3)):
        d.line([x0, y, x1, y], fill=hex2(su_renk(dunya_ust + y)))
    su_cizgisi(t, x - 17 * s, x + 17 * s, su_y + 1, f)


def nehir_rengi(y0, renkler, adim=12):
    return lambda y: renkler[min(len(renkler) - 1, max(0, y - y0) // adim)]


def nehir_orta(no, y0, renkler, adim=12, ekle=None):
    """Orta plan tamamen su (nehir/deniz): y0'dan aşağısı, nehir_rengi ile aynı bantlar; parıltılar yarı saydam."""
    img = yeni(GW, H)
    d = ImageDraw.Draw(img)
    rf = nehir_rengi(y0, renkler, adim)
    for y in range(y0, H):
        d.line([0, y, GW, y], fill=hex2(rf(y)))
    rnd = random.Random(no)
    for _ in range(360):
        x, y = rnd.randrange(GW), rnd.randrange(y0 + 2, H)
        for k in range(rnd.randint(2, 3 + (y - y0) // 12)):
            piksel(img, x + k, y, hex2(_ac(renkler[0], 0.35), 120))
    if ekle:
        ekle(img)
    kaydet(img, f"sahne{no}-orta.png")


# ==========================================================================
# SAHNELER
# ==========================================================================
def sahne490():
    """Kapak + kart 1: İstanbul, saray odası (1847). Genç padişah (fes, sorguç, lacivert setre, nişan, hafif bıyık)
    masadaki bağış kesesini gösterir; karşısında fesli kâtip kâğıdı almak için elini uzatır. Avize-kandil."""
    no = 490
    oda(no, duvar="#2e4a42", desen="damask", lambri="#c8bca0", pencere=("#9ab8d0", "#e8f0f4"), pencere_x=(PAY + 210, PAY + 330),
        kemerli=True, perde="#7a1e22", zemin="mermer", zemin_renk="#b8ae9a", hali="#8a2a2a")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, _kz(no))
        figur(t, beyefendi, 140, z, k, **KATIP_OS, yon=1, kol=0.22 + 0.04 * SIN(f))
        u = figur(t, masa, 192, z, k, renk="#5a3418", gen=3.6, yuk=6.4)
        figur(t, kese, 182, duz(u, t.width), round(k * 0.55, 1))
        kagit(t, 200, u, k * 0.45, muhur=True)
        figur(t, beyefendi, 252, z, k, **PADISAH, yon=-1, kol=0.12 + 0.05 * (1 + SIN(f)))

    _bitir(no, kare, orta_denetle=False)


def sahne491():
    """Kart 2, 31, 52 (efsane): gece, sisli nehir; üç yelkenli soluk, hayal gibi (soğuk gri-mavi), yelkenleri yarı açık.
    Karşı kıyıda soluk kasaba ışıkları. Hilal-yıldız yok (yalnızca 514'te kalkan üstünde)."""
    no = 491
    gok(no, ["#0a0e22", "#121a34", "#1c2846", "#283654", "#36445e"], yildiz=60)
    kasaba_uzak(no, None, ("#1e2a36", "#1a2430"), ("#2a3442", "#26303c", "#303a48"), ufuk=546, isik=True)
    nehir_orta(no, 552, SU_GECE)
    _bos(no, "on")
    b = P(no)
    ust = b["taban"] - b["h"]
    rf = nehir_rengi(552, SU_GECE)
    soluk = dict(govde="#5a6a80", serit="#9aa8bc", yelken="#b4c0d0")

    def kare(t, z, i):
        f = i / KARE
        h = t.height
        gemi_suda(t, 152, h - 30, 1.5, (f + 0.5) % 1, rf, ust, acik=0.6, **soluk)
        gemi_suda(t, 238, h - 18, 2.0, (f + 0.25) % 1, rf, ust, yon=-1, acik=0.6, **soluk)
        gemi_suda(t, 178, h - 7, 2.7, f, rf, ust, acik=0.7, **soluk)
        rnd = random.Random(7)
        for _ in range(260):                                        # sis: yarı saydam, yana süzülür
            x = (rnd.randrange(t.width) + int(f * 24)) % t.width
            y = rnd.randrange(h - 70, h)
            piksel(t, x, y, hex2("#a8b4c8", 70))

    _bitir(no, kare, esik=0.7)


def sahne492():
    """Kart 3 ve 51 (motif): kâtip kürsüsünde açık defter yakın plan; satır çizgileri, rakam yok. Hokka, tüy kalem, mum."""
    no = 492
    oda(no, duvar="#3a2c22", desen="lambri", lambri=None, zemin="tahta", zemin_renk="#4a3424", isik="#f8c060")
    s = 7.0

    def kare(t, z, i):
        f = i / KARE
        u = figur(t, kursu, 200, z, s, egim=5.5)
        mum(t, 160, u, f, 2.4)

    _bitir(no, kare, orta_denetle=False)


def sahne493():
    """Kart 4-5: İstanbul, 1847 baharı. Saray bahçesinin taş korkuluklu terasında erguvanlar çiçekte; padişah sağa yürür,
    arkasında kâtip. Korkuluğun ötesinde Boğaz, karşı kıyıda puslu tepeler ve ince minareli silüet (uzak plan)."""
    no = 493
    gok(no, ["#6a8ac0", "#86a2cc", "#a6bcd8", "#c6d4e0", "#e2e2dc"], None, [(110, 420, 18), (420, 410, 16)])

    def karsi(img, z):
        d = ImageDraw.Draw(img)
        rnd = random.Random(4)
        renk = hex2("#7a8aa0")
        for x in range(0, W, 9):
            hh = rnd.randint(3, 7)
            d.rectangle([x, 520 - hh, x + 7, 520], fill=renk)
        for x in (60, 230, 400):
            d.chord([x - 9, 508, x + 9, 526], 180, 360, fill=renk)
            d.rectangle([x + 13, 500, x + 14, 520], fill=renk)
            piksel(img, x + 13, 499, renk)
    uzak_tepe(no, ("#8a9aac", "#7e8ea2"), 520, karsi, su=(521, ("#5a86b0", "#4e7ca8", "#4672a0")))

    def ekle(img, z):
        d = ImageDraw.Draw(img)
        y = z[0] - 30
        d.rectangle([0, y - 10, GW, y], fill=hex2("#d8d0bc"))                         # taş korkuluk (terasın kenarı)
        d.rectangle([0, y - 12, GW, y - 10], fill=hex2("#ece6d6"))
        for x in range(4, GW, 9):
            d.rectangle([x, y - 8, x + 3, y - 2], fill=hex2("#b0a690"))
        rnd = random.Random(493)
        for x in range(0, GW, 7):                                                     # korkuluk dibinde çiçekli erguvan çalıları
            for _ in range(3):
                cx, cy = x + rnd.randint(-3, 3), y + 2 - rnd.randint(0, 8)
                r = rnd.randint(3, 5)
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hex2(rnd.choice(("#a83a7a", "#c8508e", "#e07aa8", "#b8467e"))))
            piksel(img, x, y + 4, hex2("#4a3022"))
        for x in range(0, GW, 5):
            d.line([x, y + 3, x, y + 6], fill=hex2("#5a6a3a"))
    zemin_orta(no, 560, ["#c8bca4", "#bcb098", "#b0a48c", "#a49880"], "kaldirim", ekle)
    _bos(no, "on")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        figur(t, beyefendi, 160, z, round(k * 0.96, 1), **KATIP_OS, yon=1, adim=(f + 0.5) % 1)
        figur(t, beyefendi, 222, z, k, **PADISAH, yon=1, adim=f)

    _bitir(no, kare)


def lamba_tavan(t, x, ust, f, zincir=36):
    """Bugünün tavan lambası: tavandan inen ince çubuk, konik metal şapka, altında sıcak ışık (titremez, hafif salınmaz)."""
    d = ImageDraw.Draw(t)
    for k in range(0, zincir, 2):
        piksel(t, x, ust + k, hex2("#4a4a50"))
    ky = ust + zincir
    d.polygon([(x - 3, ky), (x + 3, ky), (x + 9, ky + 7), (x - 9, ky + 7)], fill=hex2("#2a3a3a"), outline=hex2("#141c1c"))
    d.line([x - 7, ky + 7, x + 7, ky + 7], fill=hex2("#fff4d0"), width=2)
    rnd = random.Random(int(x))
    for r in range(4, 22, 3):
        for a in range(0, 180, 10):
            px_, py_ = x + math.cos(math.radians(a)) * r * 1.3, ky + 8 + math.sin(math.radians(a)) * r
            if rnd.random() < 0.35 * (1 - r / 22):
                piksel(t, px_, py_, hex2("#fff0c0", 50))


def oturan_fesli(img, x, zemin, s, govde, fes="#a01e1c", sakal=None, yon=1, minder=None, gazete=False, sac="#3a2a1a"):
    """Yeni figür: bağdaş kurup oturan fesli Osmanlı (timur_figur.oturan + fes; gazete=True elinde açık gazete)."""
    oturan(img, x, zemin, s, govde=govde, bas=None, sakal=sakal, yon=yon, minder=minder)
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 10 * s) - (int(1.6 * s) if minder else 0)
    ust = y - int(9.5 * s)
    by = ust - int(2.6 * s)
    r = max(2, int(1.7 * s))
    _sac(d, x, by, r, s, yon, sac)
    _fes(d, img, x, by, r, s, yon, fes)
    if gazete:
        gx = x + int(2.2 * s) * yon
        gx0, gx1 = min(gx, gx + int(5 * s) * yon), max(gx, gx + int(5 * s) * yon)
        d.rectangle([gx0, y - int(8 * s), gx1, y - int(3.4 * s)], fill=hex2("#e8e2d0"), outline=hex2("#8a8270"))
        for yy in range(y - int(7 * s), y - int(4 * s), max(2, int(0.7 * s))):
            d.line([gx0 + 2, yy, gx1 - 2, yy], fill=hex2("#9a9480"))
        d.rectangle([gx0 + 2, y - int(7.6 * s), gx1 - 2, y - int(7.1 * s)], fill=hex2("#3a3630"))


def peyke(img, x, zemin, s=1.0, renk="#6a4a2a", ortu="#8a3a22"):
    """Yeni figür: kahvehane peykesi (alçak, geniş ahşap oturak, üstü kilimli). Ayaklar zemine basar; üst y'yi döndürür."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 16 * s)
    temas_golgesi(img, x, y, 17 * s)
    ust = y - int(3.4 * s)
    for ax in (-7.5, 7.5):
        d.rectangle([x + int(ax * s) - _u(0.6, s), ust, x + int(ax * s) + _u(0.6, s), y - 1], fill=hex2(_ac(renk, -0.3)))
    d.rectangle([x - int(8.5 * s), ust - _u(1, s), x + int(8.5 * s), ust + _u(0.6, s)], fill=hex2(renk))
    d.rectangle([x - int(8 * s), ust - _u(1.6, s), x + int(8 * s), ust - _u(1, s)], fill=hex2(ortu))
    return ust - _u(1.6, s)


def kahvehane(img, x0, x1, zemin, s=1.0, ahsap="#8a6a44"):
    """Yeni figür: ahşap kahvehane cephesi: geniş açık önler (içi loş), sundurma saçağı, yazısız tabela. Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "kahvehane", tolerans=max(3, int(s)))
    temel(img, zemin, x0, x1, y, "#4a3a2a")
    h = int(16 * s)
    d.rectangle([x0, y - h, x1, y - 1], fill=hex2(ahsap))
    for x in range(x0, x1, max(3, int(2 * s))):
        d.line([x, y - h, x, y - 1], fill=hex2(_ac(ahsap, -0.12)))
    for kx in range(x0 + int(4 * s), x1 - int(8 * s), int(12 * s)):
        d.rectangle([kx, y - int(10 * s), kx + int(8 * s), y - int(2 * s)], fill=hex2("#2a1e16"))
        d.line([kx, y - int(6 * s), kx + int(8 * s), y - int(6 * s)], fill=hex2(_ac(ahsap, -0.3)))
        piksel(img, kx + int(2 * s), y - int(4 * s), hex2("#f8c060"))
    d.polygon([(x0 - int(2 * s), y - int(11 * s)), (x1 + int(2 * s), y - int(11 * s)), (x1, y - int(13.5 * s)), (x0, y - int(13.5 * s))],
              fill=hex2("#6a3a2a"))
    d.polygon([(x0 - int(1 * s), y - h), (x1 + int(1 * s), y - h), (x1 - int(3 * s), y - h - int(4 * s)), (x0 + int(3 * s), y - h - int(4 * s))],
              fill=hex2("#9a4a32"))
    cx = (x0 + x1) // 2
    d.rectangle([cx - int(6 * s), y - int(15.6 * s), cx + int(6 * s), y - int(14 * s)], fill=hex2("#2a4a3a"), outline=hex2("#c8a040"))
    return y - h - int(4 * s)


def otel_cephesi(img, x0, x1, zemin, s=1.0, siva="#d8d0c0", plaket_x=None):
    """Yeni figür: 18. yy (Georgian) üç katlı sıvalı otel cephesi: düz pencere dizileri, merkezde sütunlu kapı. plaket_x:
    zemin kat duvarında yazısız bronz plaket (yalnız çizgiler). Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "otel", tolerans=max(3, int(s)))
    temel(img, zemin, x0, x1, y, "#4a4440")
    kh = int(8 * s)
    h = 3 * kh + int(2 * s)
    d.rectangle([x0, y - h, x1, y - 1], fill=hex2(siva))
    d.rectangle([x0, y - h - _u(1.2, s), x1, y - h], fill=hex2(_ac(siva, 0.2)))
    d.rectangle([x0, y - int(1.6 * s), x1, y - 1], fill=hex2(_ac(siva, -0.3)))
    cx = (x0 + x1) // 2
    for k in range(3):
        fy = y - k * kh
        for wx in range(x0 + int(5 * s), x1 - int(3 * s), int(9 * s)):
            if k == 0 and (abs(wx - cx) < int(6 * s) or (plaket_x is not None and abs(wx - plaket_x) < int(7 * s))):
                continue
            d.rectangle([wx - int(1.6 * s), fy - kh + int(2 * s), wx + int(1.6 * s), fy - int(1.4 * s)], fill=hex2("#2e3a48"))
            d.line([wx, fy - kh + int(2 * s), wx, fy - int(1.4 * s)], fill=hex2("#d8d8d0"))
            d.line([wx - int(1.6 * s), fy - kh + int(4 * s), wx + int(1.6 * s), fy - kh + int(4 * s)], fill=hex2("#d8d8d0"))
    d.rectangle([cx - int(2 * s), y - int(6.5 * s), cx + int(2 * s), y - 1], fill=hex2("#2a3a2a"))
    d.chord([cx - int(2 * s), y - int(8.5 * s), cx + int(2 * s), y - int(4.5 * s)], 180, 360, fill=hex2("#e8e0c8"))
    for k in (-1, 1):
        d.rectangle([cx + k * int(3 * s) - _u(0.5, s), y - int(7 * s), cx + k * int(3 * s) + _u(0.5, s), y - 1], fill=hex2("#f0ece0"))
    if plaket_x is not None:
        px_ = plaket_x
        d.rectangle([px_ - int(3 * s), y - int(6.5 * s), px_ + int(3 * s), y - int(2.5 * s)], fill=hex2("#a87a2a"), outline=hex2("#5a3a10"))
        for yy in range(y - int(5.6 * s), y - int(3 * s), max(2, int(0.8 * s))):
            d.line([px_ - int(2.2 * s), yy, px_ + int(2.2 * s), yy], fill=hex2("#e8c060"))
    return y - h - _u(1.2, s)


def _el(x, z, s, yon, kol):
    """kisi() figürünün el ucu (timur_figur.kisi ile aynı formül; ayakta)."""
    y = zemin_y(z, x, 6 * s)
    ust = y - int(11 * s)
    if kol > 0:
        return x + int(3.5 * s) * yon, ust - int(4 * s * kol) + int(1 * s)
    return x + int(2.5 * s) * yon, ust + int(5 * s)


def bohca_el(t, x, z, s, yon, adim=None):
    """Yürüyenin elinde sallanan bohça (eli kisi formülüyle bulunur; bohça elden sarkar)."""
    y = zemin_y(z, x, 6 * s)
    ust = y - int(11 * s)
    sal = 0 if adim is None else math.sin(adim * 2 * math.pi) * 1.5 * s
    ex, ey = x + int(2.5 * s) * yon - int(sal) * yon, ust + int(5 * s)
    d = ImageDraw.Draw(t)
    d.ellipse([ex - int(1.8 * s), ey, ex + int(1.8 * s), ey + int(3.2 * s)], fill=hex2("#8a7a5a"), outline=hex2(KOYU))
    d.line([ex - int(1 * s), ey + int(0.6 * s), ex + int(1 * s), ey + int(2.6 * s)], fill=hex2("#5a4a32"))


# --------------------------------------------------------------------------
def sahne494():
    """Kart 6: İstanbul, kahvehane önü. Peykede bağdaş kurmuş fesli adam gazete okur; yanında ayakta biri dinler.
    Arkada ahşap kahvehane cephesi (düz kaldırıma oturur)."""
    no = 494
    gok(no, ["#7aa0d0", "#94b4dc", "#b2c8e4", "#d0dcea", "#ece8dc"], None, [(120, 418, 16), (400, 412, 18)])
    uzak_tepe(no, ("#9aa6b4", "#8e9aaa"), 540)

    def ekle(img, z):
        figur(img, kahvehane, PAY + 150, PAY + 400, z, 3.6)
    zemin_orta(no, 560, ["#b8ac94", "#aca088", "#a0947c", "#948870"], "kaldirim", ekle)
    _bos(no, "on")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        u = figur(t, peyke, 168, z, round(k * 0.62, 1))
        figur(t, oturan_fesli, 172, duz(u, t.width), round(k * 0.95, 1), govde="#4a3a2a", sakal="#3a2a1a", yon=1, gazete=True)
        figur(t, beyefendi, 250, z, k, govde="#2a3a4a", bas="fes", bas_renk="#a8201e", sac="#2a1a12", biyik="#2a1a12", yon=-1,
              kol=0.05 + 0.05 * (1 + SIN(f)))

    _bitir(no, kare)


GOK_IRL = ["#5a6470", "#6e7680", "#848a92", "#9ca0a4", "#b0b2b0"]
TEPE_IRL = ("#4a5a46", "#42523e")


def sahne495():
    """Kart 7: İrlanda, 1845 sonbaharı. Kurşuni gök; tarlada kararmış, çökmüş patates fideleri; köylü kürekle kazar,
    yanında şallı kadın boş sepetle bakar; geride saz damlı taş kulübe (düz zemine oturur)."""
    no = 495
    gok(no, GOK_IRL, None, [(100, 420, 22), (380, 416, 24)], ("#c8c8c8", "#a8aaac", "#8a8c90"))
    uzak_tepe(no, TEPE_IRL, 540)

    def ekle(img, z):
        figur(img, kulube, PAY + 330, z, 3.4)
        rnd = random.Random(5)
        for row, y in enumerate(range(574, 600, 6)):
            for x in range(4, GW, 9):
                patates(img, x + rnd.randint(-2, 2), duz(y, GW), 1.0 + row * 0.25, 1.0, tohum=x + y)
    _orta_gorunur(no, [(PAY + 330 - 45, PAY + 330 + 45)])
    zemin_orta(no, 562, ["#5a4a36", "#524230", "#4a3c2a", "#423424"], "tarla", ekle)
    _bos(no, "on")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        for x in range(124, 280, 13):
            patates(t, x, z, round(k * 0.6, 1), 1.0, faz=f, tohum=x)
        figur(t, beyefendi, 168, z, k, govde="#5a4a32", sac="#3a2a1a", sakal="#4a3420", yon=1, silah="kurek",
              kol=0.25 + 0.2 * SIN(f))
        figur(t, hanim, 246, z, k, elbise="#4a3a3a", bas="sal", bas_renk="#6a5a4a", yon=-1, silah="bohca")

    _bitir(no, kare)


def sahne496():
    """Kart 8-9: göç yolu. Bohçalı aile (baba, şallı anne, çocuk) sola, limana yürür; geride damı çökmüş boş kulübe."""
    no = 496
    gok(no, GOK_IRL, None, [(140, 420, 22), (420, 418, 22)], ("#c8c8c8", "#a8aaac", "#8a8c90"))
    uzak_tepe(no, TEPE_IRL, 540)

    def ekle(img, z):
        figur(img, kulube, PAY + 300, z, 3.4, cokmus=True)
    _orta_gorunur(no, [(PAY + 300 - 45, PAY + 300 + 45)])
    zemin_orta(no, 562, ["#6a6046", "#625840", "#5a503a", "#524834"], "toprak", ekle)
    on_cimen(no, ["#3e4a32", "#465238", "#4e5a3e"], "#7a8a5a", boy=70)
    k = K(no, 0.30)

    def kare(t, z, i):
        f = i / KARE
        a1, a2, a3 = f, (f + 0.37) % 1, (f + 0.71) % 1
        figur(t, beyefendi, 160, z, k, govde="#4a4234", sac="#2a2018", sakal="#3a2a1a", yon=-1, adim=a1)
        bohca_el(t, 160, z, k, -1, a1)
        figur(t, hanim, 205, z, round(k * 0.95, 1), elbise="#3a3a4a", bas="sal", bas_renk="#7a6a52", yon=-1, adim=a2)
        figur(t, beyefendi, 244, z, round(k * 0.62, 1), govde="#6a5a40", sac="#8a5a2a", yon=-1, adim=a3)

    _bitir(no, kare)


def sahne497():
    """Kart 10 ve 12: Londra, Ocak 1847. Yardım derneğinin odası: yeşil çizgili duvar kâğıdı, sisli pencere; masa başında
    oturan başkan, ayakta konuşan üye, kâğıtlı kâtip."""
    no = 497
    oda(no, duvar="#3a5a4a", desen="cizgi", lambri="#4a2e1a", pencere=("#8a9098", "#c0c4c8"), pencere_x=(PAY + 222, PAY + 318),
        tablo=(), zemin="tahta", zemin_renk="#5a3a24", hali="#5a2a2a")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, _kz(no))
        oturan_masada(t, 200, z, k, beyefendi, **LONDRA_1, yon=1)
        u = figur(t, masa, 200, z, k, ortu="#2a4a2a", gen=4.0, yuk=6.2)
        for j, x in enumerate((186, 204)):
            kagit(t, x, u, k * 0.4)
        figur(t, beyefendi, 142, z, k, **LONDRA_2, yon=1, kol=0.25 + 0.12 * (1 + SIN(f)))
        figur(t, beyefendi, 258, z, k, **KATIP_LON, yon=-1, silah="mektup", kol=0.3)

    _bitir(no, kare, orta_denetle=False)


def sahne498():
    """Kart 11: Kraliçe Victoria (27 yaşında; küçük taç, mavi kuşak) bağış kâğıdını uzatır; karşısında eğilen sekreter.
    Kızıl damask duvarlı saray odası, altın çerçeveli tablolar, perdeler."""
    no = 498
    oda(no, duvar="#6a1e22", desen="damask", lambri="#e8dcc0", pencere=("#a8b8c8", "#e8eef4"), pencere_x=(PAY + 270,),
        perde="#c8a040", tablo=((PAY + 215, "#4a5a3a"), (PAY + 325, "#3a4a6a")), zemin="parke", zemin_renk="#7a5232")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, _kz(no))
        figur(t, beyefendi, 150, z, k, **LONDRA_1, yon=1, kol=0.15 + 0.05 * SIN(f))
        figur(t, hanim, 226, z, k, **VICTORIA, yon=-1, silah="mektup", kol=0.3 + 0.04 * SIN(f))

    _bitir(no, kare, orta_denetle=False)


def sahne499():
    """Kart 13 ve 27: İstanbul, 1847 baharı. Kemerli pencereli divan salonu; fesli, nişanlı nazır bağış kesesini uzatır,
    İngiliz elçisi Wellesley (koyu redingot, favori) eliyle konuşur (rivayet kartında 'araya girer')."""
    no = 499
    oda(no, duvar="#c8b890", desen="sade", lambri="#6a4a2a", pencere=("#8ab0d0", "#e0ecf4"), pencere_x=(PAY + 220, PAY + 320),
        kemerli=True, zemin="tahta", zemin_renk="#6a4a30", hali="#2a4a6a")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, _kz(no))
        figur(t, beyefendi, 150, z, k, **NAZIR, yon=1, kol=0.3)
        ex, ey = _el(150, z, k, 1, 0.3)
        figur(t, kese, ex + 3, duz(ey + int(3.4 * k * 0.5), t.width), round(k * 0.5, 1))
        figur(t, beyefendi, 248, z, k, **WELLESLEY, yon=-1, kol=0.15 + 0.15 * (1 + SIN(f)))

    _bitir(no, kare, orta_denetle=False)


def sahne500():
    """Kart 14: Londra, derneğin yazıhanesi. Kâtip yüksek kürsüde açık deftere yazar; arkada raf dolusu defter."""
    no = 500
    oda(no, duvar="#8a7a5a", desen="sade", lambri="#4a3020", pencere=("#9aa0a8", "#d0d4d8"), pencere_x=(PAY + 300,),
        zemin="tahta", zemin_renk="#5a3e26")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 210, 0, f, _kz(no))
        figur(t, kursu, 172, z, round(k * 0.95, 1), egim=3.0)
        figur(t, beyefendi, 240, z, k, **KATIP_LON, yon=-1, kol=0.12 + 0.04 * SIN(f, 2))

    _bitir(no, kare, orta_denetle=False)


def sahne501():
    """Kart 15: Osmanlı kâtibi minderde bağdaş kurmuş, rahledeki deftere kayıt düşer; çini kuşaklı oda, şamdan."""
    no = 501
    from timur import ic_mekan
    ic_mekan(no, duvar=("#2a3a3a", "#344640", "#40524a"), kemer="#1a2620", cini="#2a6a9a", pencere=("#5a7a9a", "#a8c0d4"),
             zemin_renk=("#6a5a42", "#5a4c38", "#4e4230"), hali=True)
    k = K(no)
    so = round(k * 1.05, 1)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 214, 0, f, _kz(no))
        samdan(t, 142, z, f, round(k * 0.55, 1), 1)
        figur(t, taht_yok, 0, z, 1) if False else None
        from kalender import rahle
        rahle(t, 192, z[0], round(so * 0.9, 1))
        figur(t, oturan_fesli, 240, z, so, govde="#2a2a30", sakal="#3a2a1a", yon=-1, minder="#8a2a22")

    _bitir(no, kare, orta_denetle=False)


def taht_yok(*a, **k):
    pass


def _stand(d, img, x, y, s, renk="#5a3820"):
    """Masa üstünde eğik kitap altlığı: ayağı masaya oturur; ön yüz izleyiciye dönük."""
    d.polygon([(x - int(5 * s), y - int(1 * s)), (x + int(5 * s), y - int(1 * s)), (x + int(4.4 * s), y - int(8 * s)),
               (x - int(4.4 * s), y - int(8 * s))], fill=hex2(renk))
    d.rectangle([x - int(5.4 * s), y - int(1.2 * s), x + int(5.4 * s), y - 1], fill=hex2(_ac(renk, -0.25)))
    return y - int(8 * s), y - int(1.4 * s)


def sahne502():
    """Kart 16: iki defter yan yana (yakın plan): solda kahverengi deri ciltli İngiliz defteri eğik altlıkta, sağda
    kırmızı ciltli Osmanlı defteri rahlede; aralarında mum. Sayfalarda yalnız satır çizgileri."""
    no = 502
    oda(no, duvar="#2e3a34", desen="lambri", lambri=None, zemin="tahta", zemin_renk="#3e2c1e")
    s = 5.4

    def kare(t, z, i):
        f = i / KARE
        u = figur(t, masa, 200, z, s, renk="#4a2c18", gen=12.0, yuk=6.0)
        d = ImageDraw.Draw(t)
        a, b = _stand(d, t, 160, u, s * 0.85)
        defter_sayfa(d, t, 160 - int(3.8 * s * 0.85), a + 2, 160 + int(3.8 * s * 0.85), b - 3, cilt="#5a3a22", kalin=2)
        a, b = _stand(d, t, 240, u, s * 0.85, renk="#6a4426")
        defter_sayfa(d, t, 240 - int(3.8 * s * 0.85), a + 2, 240 + int(3.8 * s * 0.85), b - 3, renk="#f4ecd4",
                     satir="#8a6a5a", cilt="#8a1e1e", kalin=2)
        d.rectangle([236, b - 3, 244, b - 1], fill=hex2("#e0b040"))
        mum(t, 200, u, f, 2.2)

    _bitir(no, kare, orta_denetle=False)


def sahne503():
    """Kart 17-18: Dublin, 1847. Sarımsı duvarlı toplantı salonu, uzun pencereler, portreler. Masada oturan soylu
    teşekkür mektubunu imzalar; iki beyefendi ayakta izler."""
    no = 503
    oda(no, duvar="#c8b878", desen="cizgi", lambri="#5a3a22", pencere=("#9aa8b4", "#dce4ea"), pencere_x=(PAY + 210, PAY + 330),
        perde="#2a4a3a", tablo=((PAY + 270, "#5a4a3a"),), zemin="parke", zemin_renk="#6a4a2e")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        oturan_masada(t, 200, z, k, beyefendi, govde="#2a2a3a", sac="#9a9a98", favori=True, yon=1, kol=0.32 + 0.04 * SIN(f, 2))
        u = figur(t, masa, 200, z, k, ortu="#3a2a4a", gen=4.4, yuk=6.2)
        d = ImageDraw.Draw(t)
        d.rectangle([194, u - int(0.8 * k), 214, u - 1], fill=hex2("#f0e6d0"), outline=hex2("#8a7a5a"))
        piksel(t, 210, u - 2, hex2("#b8281e"))
        figur(t, beyefendi, 140, z, k, govde="#3a3428", sac="#5a3a20", favori=True, yelek="#8a6a3a", yon=1, kol=0.05)
        figur(t, beyefendi, 260, z, k, govde="#1e2a3a", sac="#2a1a12", favori=True, yon=-1)

    _bitir(no, kare, orta_denetle=False)


def sahne504():
    """Kart 19: bugün, kütüphane. Kitap rafı, camlı vitrinde mühürlü mektup; bugünün bir okuru eğilip bakar.
    Tavan lambası (dönem dışı aletten kaçınılır: yalnız sade lamba)."""
    no = 504
    oda(no, duvar="#e0dcd2", desen="sade", lambri="#8a6a4a", zemin="parke", zemin_renk="#a8845a", isik="#fff0c8")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        lamba_tavan(t, 205, 0, f, _kz(no))
        figur(t, raf, 146, z, round(k * 0.55, 1), tohum=504, kat=4, gen=8)
        figur(t, vitrin, 207, z, round(k * 0.62, 1))
        figur(t, hanim, 262, z, k, elbise="#3a5a6a", sac="#5a3a22", yon=-1, etek=0.75, topuz=False, kol=0.08)

    _bitir(no, kare, orta_denetle=False)


SU_IRL = ("#5a7080", "#52687a", "#4a6072", "#42586a")
GOK_DROG = ["#7a90a8", "#90a2b6", "#a8b6c4", "#c0cad0", "#d4d8d4"]


def _drogheda(no, gok_r=GOK_DROG, su=SU_IRL, isik=False, tas="#6e6862"):
    """Drogheda limanı (505-507 ortak): karşı kıyıda kasaba (uzak), Boyne nehri (orta, 548-600), önde taş rıhtım.
    Karşı kıyının taş seddi suyun üst kenarındadır; kasaba suya değil sete oturur."""
    gok(no, gok_r, None, [(100, 420, 20), (390, 414, 22)], ("#f0f0ec", "#d0d4d8", "#a8b0b8"))
    kasaba_uzak(no, None, ("#4e6250", "#46584a"), ("#a8a098", "#988e86", "#b0a8a0", "#8a827c"), ufuk=544, isik=isik)

    def arka(img):
        d = ImageDraw.Draw(img)
        d.rectangle([0, 544, GW, 550], fill=hex2("#5a5650"))                   # karşı kıyı seddi (kara)
        d.line([0, 544, GW, 544], fill=hex2("#8a8680"))
    liman_orta(no, su, tas=tas, ust_su=550, ekle_arka=arka)
    _bos(no, "on")


def sahne505():
    """Kart 20: Drogheda, Mayıs 1847: Boyne nehri kıyısında liman (nehir ağzı değil). Önde taş rıhtım, çuvallar;
    rıhtımda tüccar nehre bakar, hamal bekler; karşı kıyıda kasaba ve kilise kuleleri."""
    no = 505
    _drogheda(no)
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        figur(t, cuval_yigini, 150, z, round(k * 0.42, 1), (2, 1))
        figur(t, beyefendi, 205, z, k, govde="#2a2a2a", bas="silindir", sac="#5a3a20", favori=True, yon=1, kol=0.03 * (1 + SIN(f)))
        figur(t, beyefendi, 258, z, k, govde="#5a4a3a", bas="kasket", bas_renk="#3a3a3a", sac="#3a2a1a", yon=-1)

    _bitir(no, kare)


def sahne506():
    """Kart 21: üç yabancı yelkenli rıhtıma yanaşır. Gemiler insanın kat kat üstünde (insan s=1 ≈ 15 px, gemi s=2.8:
    direk ≈ 100 px); gövdeler rıhtım kenarının ardında suya oturur; rıhtımda halat bekleyen üç küçük hamal."""
    no = 506
    _drogheda(no)
    b = P(no)
    ust = b["taban"] - b["h"]
    rf = nehir_rengi(550, SU_IRL)
    kenar = RIHTIM - ust                                     # rıhtım kenarının sprite satırı

    def kare(t, z, i):
        f = i / KARE
        gemi_suda(t, 134, kenar - 18, 1.6, (f + 0.5) % 1, rf, ust, alt=kenar, acik=0.0, govde="#2a2420", serit="#c8b890")
        gemi_suda(t, 250, kenar - 11, 2.1, (f + 0.25) % 1, rf, ust, yon=-1, alt=kenar, acik=0.5, govde="#1e1e24", serit="#d8d0b8")
        gemi_suda(t, 180, kenar - 5, 2.7, f, rf, ust, alt=kenar, acik=0.0, govde="#241c18", serit="#e0d8c0", bayrak="#3a5a8a")
        for j, x in enumerate((150, 196, 236)):
            figur(t, beyefendi, x, z, 0.9, govde=("#5a4a3a", "#4a4a4a", "#6a5a40")[j], bas="kasket", bas_renk="#3a3a3a",
                  yon=-1 if x > 190 else 1, kol=0.2 + 0.15 * SIN(f + j * 0.3))
        d = ImageDraw.Draw(t)
        d.line([150, z[0] - 10, 170, kenar - 8], fill=hex2("#6a5a3a"))      # yanaşan gemiden rıhtıma halat

    _bitir(no, kare, esik=0.7)


def sahne507():
    """Kart 22-23: rıhtımda ambarların önü: buğday ve mısır çuvalları üst üste; defterli tüccar çuvalları sayar,
    yanındaki tüccar kasabanın gazetesini açmış okur."""
    no = 507
    gok(no, GOK_DROG, None, [(110, 420, 20), (400, 414, 22)], ("#f0f0ec", "#d0d4d8", "#a8b0b8"))
    uzak_tepe(no, ("#5e6e60", "#566658"), 540)

    def ekle(img, z):
        figur(img, ambar, PAY + 160, PAY + 260, z, 3.4)
        figur(img, ambar, PAY + 270, PAY + 380, z, 3.2, tas="#7a7066")
    zemin_orta(no, 560, ["#7a746c", "#6e6860", "#625c54", "#58524a"], "kaldirim", ekle)
    _bos(no, "on")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        figur(t, cuval_yigini, 148, z, round(k * 0.42, 1), (3, 2, 1), renk="#c8b080")
        figur(t, beyefendi, 205, z, k, govde="#2a2a2a", bas="silindir", sac="#6a4a2a", favori=True, yon=-1, silah="mektup",
              kol=0.28 + 0.04 * SIN(f))
        figur(t, beyefendi, 258, z, k, govde="#3a3a2a", bas="silindir", sac="#8a8a88", favori=True, yelek="#6a2a2a", yon=-1,
              gazete=True)

    _bitir(no, kare)


def sahne508():
    """Kart 24: Selanik limanı (o yıllarda Osmanlı limanı). Rıhtımda Beyaz Kule, karşıda minareli şehir; rıhtıma
    yanaşmış yelkenli (gövdesi rıhtım kenarının ardında suda)."""
    no = 508
    gok(no, ["#5a8ac8", "#78a2d4", "#98b8dc", "#bcd0e2", "#e0e4e0"], None, [(120, 418, 18), (430, 412, 16)])

    def karsi(img, z):
        d = ImageDraw.Draw(img)
        rnd = random.Random(8)
        renk = hex2("#c8bca8")
        for x in range(0, W, 8):
            hh = rnd.randint(4, 9)
            d.rectangle([x, 540 - hh, x + 6, 540], fill=renk)
            d.line([x, 540 - hh, x + 6, 540 - hh], fill=hex2("#a8442e"))
        for x in (40, 200, 330, 470):
            d.chord([x - 8, 526, x + 8, 542], 180, 360, fill=hex2("#9aa0a8"))
            d.rectangle([x + 11, 516, x + 12, 540], fill=hex2("#e0d8c8"))
            piksel(img, x + 11, 515, hex2("#9aa0a8"))
    uzak_tepe(no, ("#8a9a7a", "#7e8e70"), 540, karsi)
    su = ("#3a7ab0", "#3472a8", "#2e6aa0", "#286298")

    def on_ekle(img, z):
        figur(img, beyaz_kule, PAY + 205, z, 3.0)
    liman_orta(no, su, tas="#c8bca4", kenar="#e8e0d0", ust_su=548, ekle_on=on_ekle)
    _orta_gorunur(no, [(PAY + 205 - 24, PAY + 205 + 24)])
    _bos(no, "on")
    b = P(no)
    ust = b["taban"] - b["h"]
    rf = nehir_rengi(548, su)
    kenar = RIHTIM - ust

    def kare(t, z, i):
        f = i / KARE
        gemi_suda(t, 248, kenar - 5, 2.4, f, rf, ust, yon=-1, alt=kenar, acik=0.0, govde="#2a2420", serit="#e0d8c0")

    _bitir(no, kare, esik=0.7)


def sahne509():
    """Kart 25: New York, 21 Temmuz 1849. Tuğla evli sokak; kasketli gazeteci çocuk gazeteyi havaya kaldırır,
    silindir şapkalı beyefendi gazetesini okur."""
    no = 509
    gok(no, ["#5a8ac0", "#76a0cc", "#96b6d8", "#b8cce0", "#dce0e0"], None, [(100, 418, 16), (420, 412, 18)])
    uzak_tepe(no, ("#9aa0a8", "#8e949c"), 540)

    def ekle(img, z):
        figur(img, tugla_evler, PAY + 140, PAY + 410, z, 2.6, tohum=509)
    zemin_orta(no, 560, ["#8a8278", "#7e766c", "#726a60", "#665e56"], "kaldirim", ekle)
    _bos(no, "on")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        figur(t, beyefendi, 158, z, round(k * 0.66, 1), govde="#5a4a3a", bas="kasket", bas_renk="#4a4a4a", sac="#8a5a2a",
              yon=1, silah="mektup", kol=0.7 + 0.25 * SIN(f, 2))
        figur(t, beyefendi, 238, z, k, govde="#1e2230", bas="silindir", sac="#3a2a1a", favori=True, yon=-1, gazete=True)

    _bitir(no, kare)


def sahne510():
    """Kart 26: basımhane. Demir el baskı makinesi; baskıcı kolu çeker (pres plakası iner kalkar), yanında basılı
    kâğıt yığını. Tuğla duvar, küçük pencere."""
    no = 510
    oda(no, duvar="#7a4a3a", desen="tugla", lambri=None, pencere=("#9ab0c0", "#d8e4ea"), pencere_x=(PAY + 320,),
        zemin="tahta", zemin_renk="#4a3624")
    k = K(no)
    sm = round(k * 0.62, 1)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 214, 0, f, _kz(no))
        faz = (1 - math.cos(f * 2 * math.pi)) / 2
        bag = figur(t, baski_makinesi, 172, z, sm, f)
        kol = 0.1 + 0.35 * faz
        figur(t, beyefendi, 252, z, k, govde="#4a4a52", sac="#3a2a1a", yelek="#7a6a4a", yon=-1, kol=kol)
        el = _el(252, z, k, -1, kol)
        d = ImageDraw.Draw(t)
        d.line([*bag, *el], fill=hex2("#3a3a40"), width=2)

    _bitir(no, kare, orta_denetle=False)


def sahne511():
    """Kart 28: gece. Aynı kâtip kürsüsünde açık defter; üstünde katlanmış gazete; tek mum. Motif: defterde bin,
    hikâye yolda."""
    no = 511
    oda(no, duvar="#1e2638", desen="lambri", lambri=None, pencere=("#0e1428", "#4a5a7a"), pencere_x=(PAY + 330,),
        zemin="tahta", zemin_renk="#2a2420", isik="#f8c060")
    s = 7.0

    def kare(t, z, i):
        f = i / KARE
        u = figur(t, kursu, 200, z, s, egim=5.5)
        mum(t, 160, u, f, 2.4)
        d = ImageDraw.Draw(t)
        y = zemin_y(z, 200, 14 * s) - int(8 * s) - int(1.4 * s)
        g0, g1 = 196, 238
        d.polygon([(g0, y - 2), (g1, y - 4), (g1 + 2, y - 24), (g0 + 3, y - 22)], fill=hex2("#ddd6c2"), outline=hex2("#6a6250"))
        for yy in range(y - 19, y - 5, 3):
            d.line([g0 + 6, yy, g1 - 4, yy - 1], fill=hex2("#8a8470"))
        d.line([g0 + 6, y - 21, g1 - 4, y - 22], fill=hex2("#2a2620"), width=2)

    _bitir(no, kare, orta_denetle=False)


def sahne512():
    """Kart 29: Londra, 1851. Mavi-gri duvarlı çalışma odası, şömine; yazar masa başında biyografiyi yazar, masada
    kitap yığını ve mum; yanda dolu raf."""
    no = 512
    oda(no, duvar="#4a5a7a", desen="cizgi", lambri="#3a2416", ocak=PAY + 330, zemin="tahta", zemin_renk="#5a3a24",
        hali="#3a2a4a", tablo=((PAY + 230, "#6a5a3a"),))
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 206, 0, f, _kz(no))
        figur(t, raf, 140, z, round(k * 0.55, 1), tohum=512, kat=4, gen=7)
        oturan_masada(t, 222, z, k, beyefendi, govde="#2a2a34", sac="#7a7a78", favori=True, yon=-1, kol=0.3 + 0.03 * SIN(f, 2))
        u = figur(t, masa, 222, z, k, renk="#4a2c18", gen=4.2, yuk=6.0)
        figur(t, kitaplar_yigini, 206, duz(u, t.width), round(k * 0.55, 1), 3, 512)
        mum(t, 240, u, f, 1.6)

    _bitir(no, kare, orta_denetle=False)


def sahne513():
    """Kart 30 ve 50: Drogheda, yıllar sonra (1930'lar). Sıvalı evli kasaba sokağı; kasketli üç adam konuşur
    (biri eliyle anlatır)."""
    no = 513
    gok(no, ["#6a7a8e", "#808ea0", "#98a4b2", "#b0b8c0", "#c8ccca"], None, [(110, 420, 20), (400, 416, 20)],
        ("#e8e8e4", "#c8ccd0", "#a0a6ae"))
    uzak_tepe(no, ("#5a6a5c", "#526254"), 540)

    def ekle(img, z):
        figur(img, eski_ev_sirasi, PAY + 140, PAY + 410, z, 2.6, tohum=513)
    zemin_orta(no, 560, ["#7a7670", "#6e6a64", "#625e58", "#56524e"], "kaldirim", ekle)
    _bos(no, "on")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        figur(t, beyefendi, 148, z, k, govde="#4a4234", bas="kasket", bas_renk="#5a5248", sac="#3a2a1a", yon=1)
        figur(t, beyefendi, 205, z, k, govde="#2e3440", bas="kasket", bas_renk="#3a3a40", sac="#6a4a2a", yon=-1,
              kol=0.2 + 0.2 * (1 + SIN(f)))
        figur(t, beyefendi, 260, z, round(k * 0.97, 1), govde="#5a3a2a", bas="kasket", bas_renk="#4a3a2a", sac="#2a1a12",
              biyik="#2a1a12", yon=-1)

    _bitir(no, kare)


def sahne514():
    """Kart 32 (efsane): kasaba kapısı (iki kuleli barbakan), kemerin üstünde hilal ve yıldızlı kalkan. Bütün sahne
    soluk mavi sis içinde, hayal gibi (491 ile aynı gece paleti)."""
    no = 514
    gok(no, ["#141c34", "#1e2a46", "#2a3a56", "#3a4a66", "#4a5a74"], yildiz=40)
    kasaba_uzak(no, None, ("#26324a", "#222c42"), ("#34405a", "#303a52", "#3a465e"), ufuk=546, isik=True)
    zemin_orta(no, 560, ["#3a465a", "#364256", "#323e50", "#2e3a4c"], "kaldirim")
    _bos(no, "on")
    s = 4.4

    def kare(t, z, i):
        f = i / KARE
        figur(t, kale_kapisi, 200, z, s, tas="#8a96aa", arma=("hilal", "#2a4a8a"))
        rnd = random.Random(14)
        for _ in range(240):
            x = (rnd.randrange(t.width) + int(f * 24)) % t.width
            y = rnd.randrange(t.height - 60, t.height)
            piksel(t, x, y, hex2("#a8b4c8", 70))

    _bitir(no, kare, esik=0.7)


def sahne515():
    """Kart 33: 1844. Tarihçi D'Alton (kır saçlı, favorili) çalışma odasında; masada açık kitabı ve belediye
    başkanının mührü; elinde notları."""
    no = 515
    oda(no, duvar="#5a4630", desen="lambri", lambri=None, pencere=("#8a98a4", "#d0d8dc"), pencere_x=(PAY + 320,),
        zemin="tahta", zemin_renk="#4a3222")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, _kz(no))
        figur(t, raf, 140, z, round(k * 0.55, 1), tohum=515, kat=4, gen=7)
        u = figur(t, masa, 202, z, k, renk="#5a3418", gen=3.8, yuk=6.2)
        d = ImageDraw.Draw(t)
        d.rectangle([188, u - 2, 206, u - 1], fill=hex2("#f0e6d0"), outline=hex2("#5a2e1e"))       # açık kitap
        d.line([197, u - 3, 197, u - 1], fill=hex2("#8a7a5a"))
        d.ellipse([210, u - 6, 218, u - 1], fill=hex2("#c8a040"), outline=hex2("#5a3a10"))       # mühür
        d.rectangle([213, u - 10, 215, u - 6], fill=hex2("#5a3a20"))
        figur(t, beyefendi, 258, z, k, govde="#2a2a2e", sac="#b8b8b4", favori=True, yon=-1, silah="mektup",
              kol=0.3 + 0.04 * SIN(f))

    _bitir(no, kare, orta_denetle=False)


def sahne516():
    """Kart 34: mühür yakın planı. Kürsüde belge; kırmızı balmumu mühürde altın hilal ve yıldız (belediye başkanının
    mührü, 1844 kaydı)."""
    no = 516
    oda(no, duvar="#3a2a22", desen="lambri", lambri=None, zemin="tahta", zemin_renk="#3e2c1e")
    s = 7.0

    def kare(t, z, i):
        f = i / KARE
        figur(t, kursu, 200, z, s, defter=False, egim=5.5)
        d = ImageDraw.Draw(t)
        y = zemin_y(z, 200, 14 * s)
        on_y, arka_y = y - int(8 * s), y - int(13.5 * s)
        d.polygon([(166, on_y - 10), (234, on_y - 10), (230, arka_y + 3), (170, arka_y + 3)], fill=hex2("#f0e6d0"))
        for yy in range(arka_y + 8, on_y - 26, 4):
            d.line([176, yy, 226, yy], fill=hex2("#9a8a70"))
        cx, cy, r = 200, on_y - 20, 13
        d.ellipse([cx - r - 2, cy - r - 1, cx + r + 2, cy + r + 1], fill=hex2("#7a1410"))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hex2("#a82018"))
        d.ellipse([cx - 9, cy - 6, cx + 9, cy + 10], fill=hex2("#f0c850"))
        d.ellipse([cx - 8, cy - 9, cx + 8, cy + 6], fill=hex2("#a82018"))
        noktalar = []
        for k2 in range(10):
            a = -math.pi / 2 + k2 * math.pi / 5
            rk = 4 if k2 % 2 == 0 else 1.8
            noktalar.append((cx + math.cos(a) * rk, cy - 5 + math.sin(a) * rk))
        d.polygon(noktalar, fill=hex2("#f0c850"))
        parl = int(6 + 4 * SIN(f))
        piksel(t, cx - parl, cy - r + 3, hex2("#ff8a70"))
        mum(t, 160, arka_y, f, 2.4)

    _bitir(no, kare, orta_denetle=False)


def sahne517():
    """Kart 35-36: 13. yüzyıl. Kral John (taç, kızıl-altın kaftan, mavi pelerin, sakal) taş kalenin önünde; yanında
    eski kraliyet aslanlı sancak, elinde hilal-yıldızlı nişan kalkanı."""
    no = 517
    gok(no, ["#6a8ab0", "#86a0c0", "#a4b8cc", "#c4d0d8", "#dcdcd4"], None, [(110, 420, 18), (410, 414, 20)])
    uzak_tepe(no, ("#5a7a52", "#52704a"), 540)

    def ekle(img, z):
        figur(img, kale_kapisi, PAY + 305, z, 2.5, tas="#8a8478")
    _orta_gorunur(no, [(PAY + 305 - 30, PAY + 305 + 30)])
    zemin_orta(no, 560, ["#6a8a4a", "#5e7e42", "#52723a", "#466632"], "cayir", ekle)
    on_cimen(no, ["#466632", "#52723a", "#5e7e42"], "#a8c870", boy=70)
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        figur(t, sancak, 146, z, round(k * 0.5, 1), f, "#b8201e", "aslan")
        figur(t, kisi, 232, z, k, govde="#8a1e22", bas="tac", bas_renk="#e0b040", sakal="#5a3a22", yon=-1, kol=0.2,
              pelerin="#2a3a8a")
        ex, ey = _el(232, z, k, -1, 0.2)
        figur(t, arma_kalkani, ex - 2, ey + int(4 * k * 0.55), k * 0.55, "hilal", "#2a4a8a")

    _bitir(no, kare)


def sahne518():
    """Kart 37: arşiv. Gri, penceresiz oda; boş raflar; arşivci elinde fenerle arar."""
    no = 518
    oda(no, duvar="#4a4a46", desen="sade", lambri=None, zemin="tas", zemin_renk="#4a4844", isik="#f8d890")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        figur(t, raf, 146, z, round(k * 0.55, 1), dolu=False, tohum=518, kat=4, gen=7)
        figur(t, raf, 256, z, round(k * 0.55, 1), dolu=False, tohum=519, kat=4, gen=7)
        figur(t, beyefendi, 200, z, k, govde="#3a3a42", sac="#5a4a3a", yon=1, kol=0.35)
        ex, ey = _el(200, z, k, 1, 0.35)
        fener_el(t, ex, ey, f, k * 0.5)

    _bitir(no, kare, orta_denetle=False)


def sahne519():
    """Kart 38-39: kasabanın tarihçisi (bugün) kitaplarla dolu odasında; elinde açık kitap. Masada kitap yığını."""
    no = 519
    oda(no, duvar="#7a7a5e", desen="sade", lambri="#5a4026", pencere=("#a8b8c4", "#e0e8ec"), pencere_x=(PAY + 300,),
        zemin="parke", zemin_renk="#7a5a3a", isik="#fff0c8")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        lamba_tavan(t, 205, 0, f, _kz(no))
        figur(t, raf, 140, z, round(k * 0.55, 1), tohum=520, kat=4, gen=7)
        u = figur(t, masa, 202, z, k, renk="#6a4a2a", gen=3.6, yuk=6.0)
        figur(t, kitaplar_yigini, 196, duz(u, t.width), round(k * 0.55, 1), 4, 519)
        figur(t, beyefendi, 258, z, k, govde="#5a3a2a", sac="#9a9a96", yon=-1, silah="mektup", kol=0.3 + 0.05 * SIN(f),
              kravat=None, yaka="#d8d0c0")

    _bitir(no, kare, orta_denetle=False)


def sahne520():
    """Kart 40-42: Drogheda, 2 Mayıs 1995. West Street'te otel cephesi; zemin kat duvarında bronz plaket. Önde
    belediye başkanı (altın zincir) ve Türk büyükelçisi yan yana."""
    no = 520
    gok(no, ["#6a90c0", "#84a4cc", "#a2bad8", "#c2d2e2", "#dfe4e4"], None, [(110, 418, 18), (420, 412, 18)])
    uzak_tepe(no, ("#7a8a7a", "#6e7e70"), 540)

    def ekle(img, z):
        figur(img, otel_cephesi, PAY + 150, PAY + 400, z, 2.8, plaket_x=PAY + 270)
    zemin_orta(no, 560, ["#8a8680", "#7e7a74", "#726e68", "#66625c"], "kaldirim", ekle)
    _bos(no, "on")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        figur(t, beyefendi, 160, z, k, govde="#24242a", sac="#6a6a68", yon=1, zincir=True, kravat="#7a1e22",
              kol=0.03 * (1 + SIN(f)))
        figur(t, beyefendi, 242, z, k, govde="#22283a", sac="#2a2018", biyik="#2a2018", yon=-1, kravat="#b8201e")

    _bitir(no, kare)


def sahne521():
    """Kart 43-44: Ankara, 23 Mart 2010. Resmî yemek: beyaz örtülü uzun masa, oturan iki konuk; ortada İrlanda
    Cumhurbaşkanı ayakta konuşur. Kristal avize."""
    no = 521
    oda(no, duvar="#e0d8c4", desen="damask", lambri="#c8b890", pencere=("#3a4a6a", "#8a9ab8"), pencere_x=(PAY + 215, PAY + 325),
        perde="#7a1e22", zemin="parke", zemin_renk="#8a6a42", hali="#7a1e22", isik="#fff0c8")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, _kz(no))
        oturan_masada(t, 146, z, k, beyefendi, govde="#22283a", sac="#5a5a58", yon=1, kravat="#2a3a6a")
        figur(t, hanim, 200, z, k, elbise="#2a6a4a", sac="#c8a878", yon=1, etek=0.7, topuz=False, kol=0.25 + 0.15 * (1 + SIN(f)))
        oturan_masada(t, 254, z, k, beyefendi, govde="#1e1e24", sac="#2a2018", biyik="#2a2018", yon=-1, kravat="#b8201e")
        u = figur(t, masa, 200, z, k, ortu="#f4f0e6", gen=11.0, yuk=6.0)
        for x in (146, 254):
            kagit(t, x, u, k * 0.35, renk="#ffffff")

    _bitir(no, kare, orta_denetle=False)


def sahne522():
    """Kart 45: ertesi gün, ofis (2010). Aydınlık pencere; masada dizüstü bilgisayar; basın görevlisi düzeltme
    metnini okur."""
    no = 522
    oda(no, duvar="#c8ccd0", desen="sade", lambri=None, pencere=("#b8d4ec", "#f4f8fc"), pencere_x=(PAY + 230,),
        zemin="parke", zemin_renk="#a88a64", isik="#fff8e0")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        lamba_tavan(t, 210, 0, f, _kz(no))
        u = figur(t, masa, 172, z, k, renk="#8a6a4a", gen=4.0, yuk=6.2)
        figur(t, dizustu, 168, u, k * 0.7) if False else dizustu(t, 168, u, k * 0.7)
        figur(t, beyefendi, 248, z, k, govde="#3a4a5a", sac="#4a3a2a", yon=-1, kravat="#5a2a3a", silah="mektup",
              kol=0.32 + 0.03 * SIN(f))

    _bitir(no, kare, orta_denetle=False)


def sahne523():
    """Kart 46-47: 1861. Boş taht; iki yanda mumları kısalmış şamdanlar; koyu kızıl perdeler. Ağırbaşlı, kimse yok."""
    no = 523
    oda(no, duvar="#3a1a1e", desen="damask", lambri="#2a1a14", pencere=("#141a2a", "#2a3448"), pencere_x=(PAY + 210, PAY + 330),
        perde="#4a1418", zemin="mermer", zemin_renk="#6a625a", hali="#4a1a1a", isik="#f8c060")
    k = K(no)

    def kare(t, z, i):
        f = i / KARE
        figur(t, samdan, 142, z, f, round(k * 0.6, 1), 3, 0.7) if False else samdan(t, 142, z, f, round(k * 0.6, 1), 3, 0.7)
        samdan(t, 258, z, (f + 0.4) % 1, round(k * 0.6, 1), 3, 0.7)
        figur(t, taht, 200, z, round(k * 0.62, 1), "#c8a040", "#5a1418")

    _bitir(no, kare, orta_denetle=False)


def sahne524():
    """Kart 48-49: belgeler masası (yakın plan): solda eğik altlıkta defter, ortada kese, sağda mühürlü teşekkür
    mektubu; mum."""
    no = 524
    oda(no, duvar="#3a2e24", desen="lambri", lambri=None, zemin="tahta", zemin_renk="#3e2c1e")
    s = 5.4

    def kare(t, z, i):
        f = i / KARE
        u = figur(t, masa, 200, z, s, renk="#4a2c18", gen=12.0, yuk=6.0)
        d = ImageDraw.Draw(t)
        a, b = _stand(d, t, 158, u, s * 0.85)
        defter_sayfa(d, t, 158 - int(3.8 * s * 0.85), a + 2, 158 + int(3.8 * s * 0.85), b - 3, cilt="#5a3a22", kalin=2)
        figur(t, kese, 200, duz(u, t.width), 2.8)
        a, b = _stand(d, t, 242, u, s * 0.85, renk="#6a4426")
        d.rectangle([242 - int(3.4 * s * 0.85), a + 2, 242 + int(3.4 * s * 0.85), b - 3], fill=hex2("#f0e6d0"), outline=hex2("#8a7a5a"))
        for yy in range(a + 6, b - 10, 3):
            d.line([242 - int(2.8 * s * 0.85), yy, 242 + int(2.6 * s * 0.85), yy], fill=hex2("#9a8a70"))
        d.ellipse([248, b - 12, 258, b - 3], fill=hex2("#a82018"), outline=hex2("#6a1010"))
        mum(t, 222, u, f, 1.8)

    _bitir(no, kare, orta_denetle=False)


SAHNELER = {n: globals()[f"sahne{n}"] for n in range(490, 525)}

if __name__ == "__main__":
    for n in ([int(a) for a in sys.argv[1:]] or sorted(SAHNELER)):
        SAHNELER[n]()
        print("sahne", n, "tamam")
