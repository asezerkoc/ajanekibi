"""Kalması Uygun Değil: Hezarfen Ahmed Çelebi'nin uçuşu (tek kaynak Evliya Çelebi). Piksel Tarih (@pikseltarihim),
sahneler 370-407. Grafikerin tarifi: teslimler/gece/ara/hezarfen/5-grafik.md; metin ve 47 kart 4-kalite-metin.md'den.
Yön dili: sağ = doğu / Üsküdar (lodos güneybatıdan eser, rüzgâr soldan sağa), sol = batı / sürgün (Cezayir).
Kullanım: python3 -I video/piksel/hezarfen.py [sahne numaraları]

Yeni figürler (bu dosyada; ciz.py'ye eklenmedi, yalnızca piksel()/hex2()/ImageDraw ve mevcut figürlerle yazıldı):
  kanat / kanatli      kartal kanatlı adam: kanatlar omuzlardan çıkar; kapalıyken bedenin iki yanında sarkar, açıkken
                       yana uzanır. Ayakları zemine basar (havada=True yalnızca Boğaz süzülüşünde: temas gölgesi silinir).
  galata_kulesi        silindir taş gövde, çıkmalı şerefe, konik külah; düz zemine kurulur, şerefe y'sini döndürür.
  tas_minber           Okmeydanı'nın taş minberi: merdivenli taş kürsü; düz zemine kurulur, üst sahanlık y'sini döndürür.
  kubbeli_cami         kubbeli taş cami (tek minare); düz zemine kurulur. siluet: uzak plandaki kıyı silüeti.
  kese, fici           kese (altın/akçe), barut fıçısı: zemine oturur.
  fisek                Lagari'nin fişeği: ahşap sehpa ayakları zemine basar, gövdenin üstünde oturak (kol sayısı
                       vurgulanmaz: yalnızca gövde ve yanlarda iki kol görünür).
  yuzen                denizde yüzen adam: baş ve kollar su çizgisinin üstünde, gövde suyun altında.
  terazi               kefeli terazi: taban zemine basar, kefeler zincirle kola asılı.
  ucak, hangar, ruzgar_tulumu   bugünkü küçük pervaneli uçak (tekerlekler pistte), hangar, kısa direkli rüzgâr tulumu.
  perde, koltuk_sirasi sinema perdesi (iki ayak zemine basar) ve koltuk sırası.
  rampa, manken, beton_set      2009 deneyi: çelik rampa, oturan manken, beton bariyer (hepsi zemine oturur).
  fener                direğe asılı şenlik feneri (direk zemine dikili).
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import ImageDraw  # noqa: E402

from ciz import _ac, _esik, agac, duman, duz_zemin, figur, gunes, hex2, piksel, sehir, sirt, taslar, temas_golgesi, yeni, zemin_y  # noqa: E402
from ciz import arazi, orta_asya_sehri  # noqa: E402
from sahneler import duz, gokyuzu, kaydet, on, orta, sprite, uzak  # noqa: E402
from timur_figur import atli, gemi, kisi, oturan, sedir  # noqa: E402
from timur import ic_mekan, kandil, mumluk, su_ve_kiyi  # noqa: E402
from kalender import kitaplar, rahle  # noqa: E402

KARE = 24      # sprite kare sayısı (SKILL.md)
PAY = 135      # orta/ön plan yan payı (SKILL.md)
W, H = 540, 960
SIN = lambda f, k=1: math.sin(f * 2 * math.pi * k)  # noqa: E731
COS = lambda f, k=1: math.cos(f * 2 * math.pi * k)  # noqa: E731

# Kişiler (renk kimlikleri bütün sahnelerde aynı)
HEZARFEN = dict(govde="#3a5a6a", bas="sarik", bas_renk="#ece4d0", sakal="#3a2416")        # mavi-gri cübbe, beyaz sarık
MURAD = dict(govde="#8a1e22", bas="sarik", bas_renk="#f4f0e6", sakal="#2a1a12")           # IV. Murad: genç, kara sakal
LAGARI = dict(govde="#6a4a22", bas="bork", bas_renk="#8a2a1a", sakal="#2a1a12")           # fişekçi: kahverengi, kızıl börk
EVLIYA = dict(govde="#2a4a3a", bas="sarik", bas_renk="#f4f0e6", sakal="#e8e4dc")          # yaşlı Evliya: ak sakal
FIRNAS = dict(govde="#e0d4b8", bas="sarik", bas_renk="#f4f0e6", sakal="#d8d0c8")          # İbn Firnas: yaşlı, açık cübbe
CEVHERI = dict(govde="#5a4a6a", bas="sarik", bas_renk="#e8e0d0", sakal="#2a1a12")


def _u(v, s):
    return max(1, int(round(v * s)))


# ==========================================================================
# Ölçüm yardımcıları (Cem Sultan dosyasından, onaylı kalıp). Yeni çizim fonksiyonu değil: figürü boş yüzeye
# çizip alfa kanalından ölçer.
# ==========================================================================
def _bb(img):
    return img.getchannel("A").getbbox()


_ONBELLEK = {}


def olcek(ad, yakin, cizim, oran=0.32):
    """Figür kutusu kadraj yüksekliğinin >= oran'ı olan en küçük s (0.1 adım). Kadrajda görünen ızgara
    yüksekliği = 960 / yakin."""
    anahtar = (ad, yakin, oran)
    if anahtar in _ONBELLEK:
        return _ONBELLEK[anahtar]
    hedef = oran * 960 / yakin
    s = 1.0
    while s <= 12.0:
        t = yeni(700, 460)
        cizim(t, round(s, 1), duz(457, 700))
        bb = _bb(t)
        if bb and bb[1] <= 1:
            break
        if bb and bb[3] - bb[1] >= hedef:
            _ONBELLEK[anahtar] = round(s, 1)
            return _ONBELLEK[anahtar]
        s += 0.1
    raise RuntimeError(f"olcek({ad}, yakin={yakin}): %{int(oran * 100)} boya ulaşılamadı")


def s_kisi(yakin, oran=0.32):
    return olcek("kisi", yakin, lambda t, s, z: figur(t, kisi, 350, z, s, **HEZARFEN, yon=1), oran)


def s_oturan(yakin, oran=0.30):
    return olcek("oturan", yakin, lambda t, s, z: figur(t, oturan, 350, z, s, **MURAD, yon=-1, minder="#c8a040"), oran)


def _kz(yakin, taban=634, h=300):
    """Kandil zinciri: sprite'ın üst kenarından (tavan) kadrajın üst kenarının biraz altına."""
    ust_gorunen = (taban - 12) * (1 - 1 / yakin)
    return max(40, int(ust_gorunen - (taban - h)) + 10)


def yazi_alti(yakin, taban, satir=3, odak=None, yaziY=None):
    """Kartın alt kenarının dünya y'si. Ekranda yazı ızgara y (yaziY or 300)/2'den başlar, satır başına ~52 ızgara.
    Yakınlaşmanın odağı odakY (verilmezse taban-12)."""
    ekran = (yaziY or 300) / 2 + satir * 52 + 5
    o = odak if odak is not None else taban - 12
    return o + (ekran - o) / yakin


def _kadraj(no, kare, w, h, yakin, esik, taban, yazi_satir=3, serbest=0, odak=None, yaziY=None, sxler=(270,),
            kenar_pay=12, kenar_haric_alt=0, kenar_serbest=False):
    """Görünür aralık: yakınlaşmanın odağı sprite'ın ızgara x'i (sx) olduğundan görünen yerel x aralığı
    [w/2 - sx/yakin, w/2 + (540 - sx)/yakin]'dir (sx 270'te w/2 ± 270/yakin). Kayan sprite'ta baş ve son sx'in ikisi de
    denetlenir. Opak piksellerin en az `esik` oranı içeride olmalı; figür sprite'ın üstüne değmemeli (kesik baş).
    Yazı denetimi: görünür aralıkta, kartın alt kenarından yukarıda kalan opak piksel sayısı `serbest`'i aşmamalı.
    Kenar denetimi (görsel KK revizyonu): 24 karenin hiçbirinde, görünür aralığın sol ve sağ kenarından `kenar_pay` px
    (8 px pay + kamera paralaksı) içeride opak figür pikseli olmamalı: kanat uçları, mum, fener kadraj kenarında kesilmez.
    kenar_haric_alt: sprite'ın alt satırlarındaki tam genişlikte su bandı denetim dışıdır."""
    sinir = yazi_alti(yakin, taban, yazi_satir, odak, yaziY) - (taban - h)       # sprite yerel y
    if not kenar_serbest:
        for i in range(KARE):
            t = yeni(w, h)
            kare(t, duz(h, w), i)
            alfa = t.getchannel("A").point(lambda v: 255 if v > 200 else 0)
            for sx in sxler:
                a, b = int(w / 2 - sx / yakin), int(w / 2 + (540 - sx) / yakin)
                for x0, x1, yan in ((max(0, a - 400), a + kenar_pay, "sol"), (b - kenar_pay, min(w, b + 400), "sağ")):
                    x0, x1 = max(0, x0), min(w, x1)
                    if x1 > x0 and alfa.crop((x0, 0, x1, h - kenar_haric_alt)).getbbox():
                        raise RuntimeError(f"Sahne {no}, kare {i}, sx {sx}: {yan} kenarda kesilen opak piksel "
                                           f"(yerel x {x0}-{x1}, görünür {a}-{b})")
    for i in (0, 4, 8, 12, 16, 20):
        t = yeni(w, h)
        kare(t, duz(h, w), i)
        alfa = t.getchannel("A")
        toplam = sum(alfa.histogram()[1:])
        bb = alfa.getbbox()
        ust_satir = sum(alfa.crop((0, 0, w, 2)).histogram()[1:])
        if not toplam or (bb[1] <= 1 and ust_satir > serbest + 12):
            raise RuntimeError(f"Sahne {no}: sprite yüksekliği (h={h}) yetmiyor ya da kare boş")
        for sx in sxler:
            a, b = max(int(w / 2 - sx / yakin), 0), min(int(w / 2 + (540 - sx) / yakin), w)
            ici = sum(alfa.crop((a, 0, b, h)).histogram()[1:])
            if ici / toplam < esik:
                raise RuntimeError(f"Sahne {no}, kare {i}, sx {sx}: figürlerin %{int(100 * ici / toplam)}'i görünür aralıkta "
                                   f"(yerel x {a}-{b})")
            if sinir > 0:
                yukari = sum(alfa.crop((a, 0, b, int(sinir))).point(lambda v: 255 if v > 200 else 0).histogram()[1:])
                if yukari > serbest:
                    raise RuntimeError(f"Sahne {no}, kare {i}: {yukari} opak piksel yazı bandında (yerel y < {int(sinir)})")


def _gorunur(no, xler, sx0, sx1, yakin, pay=10):
    """Orta plandaki (hareketsiz) önemli figürlerin ızgara x'i sprite'ın baş ve son sx'inde görünür aralıkta kalmalı."""
    for sx in (sx0, sx1):
        a, b = sx - sx / yakin + pay, sx + (540 - sx) / yakin - pay
        for x in xler:
            if not a <= x <= b:
                raise RuntimeError(f"Sahne {no}: orta plan figürü x={x} görünür aralık [{int(a)}, {int(b)}] dışında (sx={sx})")


# ==========================================================================
# YENİ FİGÜRLER
# ==========================================================================
TUY = dict(koyu="#2e1c10", ana="#5e3c22", orta="#7a5230", ortu="#9a7040", isik="#d0a868", uc="#24160e")


def kanat(img, kx, ky, yon, aci, L, s, renk=None):
    """Yeni figür parçası: kartal kanadı. Kök (kx, ky) omuzdadır; aci derece (+ yukarı, - aşağı), L boy (px).
    Ön kenarda açık örtü tüyleri, arkada tarak kenarlı ikinci sıra tüyler, uçta ayrık koyu birincil tüyler."""
    r = dict(TUY, **(renk or {}))
    d = ImageDraw.Draw(img)
    a = math.radians(aci)
    dx, dy = yon * math.cos(a), -math.sin(a)
    nx, ny = -dy * yon, dx * yon                       # arka kenar yönü (açık kanatta aşağı)

    def P(u, v):
        return (kx + dx * u + nx * v, ky + dy * u + ny * v)

    n = max(10, int(L / 2))
    on_ = [P(L * k / n, -0.6 * s * math.sin(math.pi * k / n)) for k in range(n + 1)]
    derin = lambda u: s * (2.6 + 1.6 * u / L) + 0.45 * s * abs(math.sin(math.pi * u / (1.25 * s)))  # noqa: E731
    arka = [P(L * k / n * 0.86, derin(L * k / n * 0.86)) for k in range(n, -1, -1)]
    d.polygon(on_ + arka, fill=hex2(r["ana"]))
    # birincil tüyler (uçta, ayrık parmaklar): yelpaze gibi ön kenar yönünden arka kenar yönüne
    for j in range(5):
        u0 = L * (0.70 + 0.075 * j)
        b = math.radians(68 - j * 13)
        ux, uy = dx * math.cos(b) + nx * math.sin(b), dy * math.cos(b) + ny * math.sin(b)
        boy = s * (3.6 + 0.5 * j) * (0.55 + 0.45 * min(1.0, max(0.0, (aci + 78) / 84)))
        x0, y0 = P(u0, 0.4 * s)
        x1, y1 = x0 + ux * boy, y0 + uy * boy
        d.line([x0, y0, x1, y1], fill=hex2(r["uc"]), width=_u(0.9, s))
        d.line([x0, y0, (x0 + x1) / 2, (y0 + y1) / 2], fill=hex2(r["koyu"]), width=_u(1.2, s))
    # ikinci sıra tüylerin ayrım çizgileri
    u = 0.12 * L
    while u < 0.68 * L:
        d.line([*P(u, 1.5 * s), *P(u - 0.35 * s, derin(u) - 0.3 * s)], fill=hex2(r["koyu"]))
        u += 1.25 * s
    # örtü tüyleri bandı ve ışıklı ön kenar
    ortu = [P(L * k / n * 0.8, -0.6 * s * math.sin(math.pi * k / n * 0.8)) for k in range(n + 1)]
    ortu += [P(L * k / n * 0.8, 1.3 * s) for k in range(n, -1, -1)]
    d.polygon(ortu, fill=hex2(r["ortu"]))
    for k in range(1, n):
        if k % 2:
            piksel(img, *P(L * k / n * 0.78, 1.0 * s), hex2(r["orta"]))
    d.line(on_[: int(n * 0.9)], fill=hex2(r["isik"]), width=_u(0.5, s))


def kanatli(img, x, zemin, s=1.0, yon=1, acik=0.0, cirp=0.0, havada=False, diz=False, adim=None, kol=0.0,
            govde=HEZARFEN["govde"], bas=HEZARFEN["bas"], bas_renk=HEZARFEN["bas_renk"], sakal=HEZARFEN["sakal"],
            sol_dus=0.0):
    """Yeni figür: sırtında kartal kanatları olan adam (kisi + iki kanat). acik 0: kanatlar kapalı, bedenin iki yanında
    sarkar; 1: yana tam açık. cirp: -1..1 kanat ucu salınımı (rüzgâr). Ayaklar zemine basar; havada=True yalnızca
    süzülme sahnesi için (ayak altındaki temas gölgesi silinir). sol_dus: kırık/sarkık sol kanat (İbn Firnas inişi)."""
    k = yeni(img.width, img.height)
    y = zemin_y(zemin, x, 6 * s)
    yy = y + (int(3.6 * s) if diz else 0)
    oy = yy - int(10 * s)                                   # omuz hizası
    aci = -74 + 80 * acik + 10 * cirp
    L = s * (7.6 + 4.9 * acik)
    ky = oy - int(2.4 * s * (1 - acik))                      # kapalı kanadın dirseği omuzun üstünde: kanat sırtta okunur
    kanat(k, x + int((1.4 + 0.4 * acik) * s), ky, 1, aci, L, s)
    kanat(k, x - int((1.4 + 0.4 * acik) * s), ky, -1, aci - 30 * sol_dus, L * (1 - 0.15 * sol_dus), s)
    kisi(k, x, zemin, s, govde, bas, bas_renk, sakal, yon, adim, kol=kol, diz=diz, kemer="#c8a040")
    if acik > 0.3:                                          # kollar kanadın ön kenarını tutar
        d = ImageDraw.Draw(k)
        a = math.radians(aci)
        for yn in (-1, 1):
            kx = x + yn * int(1.6 * s)
            ux, uy = kx + yn * math.cos(a) * L * 0.42, oy - math.sin(a) * L * 0.42
            d.line([x + yn * int(1.4 * s), oy + int(0.8 * s), ux, uy], fill=hex2(_ac(govde, -0.3)), width=_u(1, s))
            piksel(k, ux, uy, hex2("#e8b890"))
    if havada:                                              # temas gölgesi (yarı saydam) silinir: ayak altında gölge yok
        px = k.load()
        for j in range(max(0, y - int(2 * s)), min(k.height, y + 2)):
            for i in range(max(0, x - int(8 * s)), min(k.width, x + int(8 * s))):
                if 0 < px[i, j][3] < 255:
                    px[i, j] = (0, 0, 0, 0)
    img.alpha_composite(k)


def galata_kulesi(img, x, zemin, s=1.0, tas="#b8ac98", kursun="#6e7884", pencere="#2a2420", isik=False):
    """Yeni figür: Galata Kulesi. Silindir taş gövde (soldan ışık, sağ kenar gölgede), taş sıraları, dar kemerli
    pencereler, çıkmalı seyir şerefesi ve konik kurşun külah. Toplam boy 42·s. Yalnızca düz zemine kurulur.
    Dönen değer: (şerefe zemininin y'si, şerefenin sol x'i, sağ x'i)."""
    d = ImageDraw.Draw(img)
    r = int(5 * s)
    y = duz_zemin(zemin, x - r - _u(0.6, s), x + r + _u(0.6, s), "Galata Kulesi", tolerans=max(3, int(s)))
    temas_golgesi(img, x, y, 2 * r + 6)
    ust = y - int(30 * s)                                   # gövdenin bittiği yer (şerefe tabanı)
    for i in range(-r, r + 1):                              # silindir gölgelemesi
        t = (i + r) / (2 * r)
        renk = _ac(tas, 0.18 - 0.5 * t) if t > 0.15 else _ac(tas, 0.05)
        d.line([x + i, ust, x + i, y - 1], fill=hex2(renk))
    d.rectangle([x - r - _u(0.6, s), y - int(2 * s), x + r + _u(0.6, s), y - 1], fill=hex2(_ac(tas, -0.12)))  # kaide
    for yy in range(ust + _u(2.4, s), y - int(2 * s), _u(2.4, s)):                 # taş sıraları
        d.line([x - r + 1, yy, x + r - 1, yy], fill=hex2(_ac(tas, -0.22)))
    pen = hex2("#f8c860") if isik else hex2(pencere)
    for kat, h in enumerate((7, 13, 19, 25)):
        for px_ in ((-2.2, 1.6) if kat % 2 else (-0.4,)):
            cx, cy = x + int(px_ * s), y - int(h * s)
            d.rectangle([cx - _u(0.5, s), cy, cx + _u(0.5, s), cy + int(2 * s)], fill=pen)
            d.chord([cx - _u(0.5, s), cy - _u(0.5, s), cx + _u(0.5, s), cy + _u(0.5, s)], 180, 360, fill=pen)
    # şerefe: dışa taşan konsollu balkon, korkuluk, arkada kemerli seyir odası
    sr = r + int(1.6 * s)
    serefe = ust
    d.polygon([(x - r, ust + int(1.4 * s)), (x - sr, ust), (x + sr, ust), (x + r, ust + int(1.4 * s))], fill=hex2(_ac(tas, -0.2)))
    d.rectangle([x - sr, ust - _u(0.6, s), x + sr, ust], fill=hex2(_ac(tas, 0.15)))
    oda_ust = ust - int(4 * s)
    d.rectangle([x - r, oda_ust, x + r, ust - 1], fill=hex2(_ac(tas, -0.05)))
    for ax in range(-r + _u(1.4, s), r - _u(0.8, s), _u(2.4, s)):
        d.rectangle([x + ax, oda_ust + _u(1.2, s), x + ax + _u(1, s), ust - _u(0.8, s)], fill=pen)
    for kx in range(x - sr, x + sr + 1, max(2, _u(0.9, s))):                         # korkuluk babaları
        d.line([kx, ust - _u(1.4, s), kx, ust - 1], fill=hex2(_ac(tas, -0.3)))
    d.line([x - sr, ust - _u(1.4, s), x + sr, ust - _u(1.4, s)], fill=hex2(_ac(tas, -0.3)))
    # konik külah: saçak taşar, kurşun dilimler, tepede alem
    sac = r + int(1.2 * s)
    tepe = oda_ust - int(8 * s)
    d.polygon([(x - sac, oda_ust), (x, tepe), (x + sac, oda_ust)], fill=hex2(kursun))
    d.polygon([(x, tepe), (x + sac, oda_ust), (x + sac // 3, oda_ust)], fill=hex2(_ac(kursun, -0.22)))
    for dl in (-0.55, 0.0, 0.55):
        d.line([x + int(dl * sac), oda_ust, x, tepe + 1], fill=hex2(_ac(kursun, -0.12)))
    d.line([x - sac, oda_ust, x + sac, oda_ust], fill=hex2(_ac(kursun, 0.2)))
    d.line([x, tepe, x, tepe - _u(1.6, s)], fill=hex2("#e0b040"))
    return serefe, x - sr, x + sr


def tas_minber(img, x, zemin, s=1.0, yon=-1, tas="#c8bca4"):
    """Yeni figür: Okmeydanı'ndaki açık hava taş minberi. Kesme taş kürsü (üst sahanlık 9·s yükseklikte, korkuluklu),
    yon tarafına inen taş merdiven, merdiven altında kemerli göz. Yalnızca düz zemine kurulur.
    Dönen değer: (sahanlık y'si, sahanlık sol x, sağ x)."""
    d = ImageDraw.Draw(img)
    gen = int(3.2 * s)
    mer = int(10 * s)
    xa, xb = (x - gen, x + gen + mer) if yon > 0 else (x - gen - mer, x + gen)
    y = duz_zemin(zemin, xa, xb, "taş minber", tolerans=max(3, int(s)))
    temas_golgesi(img, (xa + xb) // 2, y, xb - xa + 4)
    h = int(9 * s)
    ust = y - h
    koyu, acik_ = hex2(_ac(tas, -0.25)), hex2(_ac(tas, 0.2))
    d.rectangle([x - gen, ust, x + gen, y - 1], fill=hex2(tas))                    # kürsü gövdesi
    basamak = 8
    for b in range(basamak):                                                       # merdiven: aşağı doğru genişler
        by = ust + int((b + 1) * h / basamak)
        bx = x + yon * (gen + int((b + 1) * mer / basamak))
        x0, x1 = sorted((x + yon * gen, bx))
        d.rectangle([x0, by - int(h / basamak), x1, y - 1], fill=hex2(_ac(tas, -0.06)))
        d.line([x0, by - int(h / basamak), x1, by - int(h / basamak)], fill=acik_)
    gx = x + yon * (gen + int(mer * 0.55))                                          # merdiven altı kemerli göz
    d.rectangle([gx - _u(1.4, s), y - int(3 * s), gx + _u(1.4, s), y - 1], fill=hex2("#3a3028"))
    d.chord([gx - _u(1.4, s), y - int(4.4 * s), gx + _u(1.4, s), y - int(1.6 * s)], 180, 360, fill=hex2("#3a3028"))
    for yy in range(ust + _u(2.2, s), y - 1, _u(2.2, s)):                           # taş sıraları
        d.line([x - gen + 1, yy, x + gen - 1, yy], fill=koyu)
    d.rectangle([x - gen - 1, ust - _u(0.6, s), x + gen + 1, ust], fill=acik_)      # sahanlık kenarı
    korkuluk = x - gen if yon > 0 else x + gen                                     # merdivenin karşı yanında korkuluk
    d.rectangle([min(korkuluk, korkuluk - yon * _u(0.8, s)), ust - int(2.4 * s),
                 max(korkuluk, korkuluk - yon * _u(0.8, s)), ust], fill=hex2(tas), outline=koyu)
    return ust, x - gen, x + gen


def kubbeli_cami(img, x, zemin, s=1.0, tas="#d8ccb4", kursun="#7a8490", minare=1, isik=False):
    """Yeni figür: kubbeli Osmanlı camisi: kesme taş harim, kasnak üstünde kurşun kubbe ve alem, yarım kubbeler;
    minare (0 yok, 1 sağda, -1 solda): ince gövde, şerefe, kurşun külah. Yalnızca düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    g = int(9 * s)
    y = duz_zemin(zemin, x - g, x + g, "cami", tolerans=max(3, int(s)))
    temas_golgesi(img, x, y, 2 * g + 4, alfa=90)
    hy = y - int(7 * s)
    d.rectangle([x - g, hy, x + g, y - 1], fill=hex2(tas))
    d.line([x - g, hy, x + g, hy], fill=hex2(_ac(tas, 0.2)))
    pen = hex2("#f8c860") if isik else hex2("#4a3a30")
    for px_ in range(x - g + _u(2, s), x + g - _u(1, s), _u(3, s)):
        d.rectangle([px_, y - int(5 * s), px_ + _u(0.8, s), y - int(3 * s)], fill=pen)
    for yn in (-1, 1):                                                              # yarım kubbeler
        cx = x + yn * int(5 * s)
        d.chord([cx - int(3 * s), hy - int(3 * s), cx + int(3 * s), hy + int(3 * s)], 180, 360, fill=hex2(kursun))
    d.rectangle([x - int(4.4 * s), hy - int(2.4 * s), x + int(4.4 * s), hy], fill=hex2(_ac(tas, -0.06)))  # kasnak
    d.chord([x - int(5 * s), hy - int(8 * s), x + int(5 * s), hy - int(0.4 * s)], 180, 360, fill=hex2(kursun))
    d.chord([x + int(1 * s), hy - int(7.6 * s), x + int(5 * s), hy - int(0.6 * s)], 270, 360, fill=hex2(_ac(kursun, -0.2)))
    d.line([x, hy - int(4.2 * s), x, hy - int(6 * s)], fill=hex2("#e0b040"))
    if minare:
        mx = x + minare * (g + int(1.4 * s))
        mh = int(19 * s)
        d.rectangle([mx - _u(0.8, s), y - mh, mx + _u(0.8, s), y - 1], fill=hex2(_ac(tas, 0.06)))
        d.rectangle([mx - _u(1.4, s), y - int(14 * s), mx + _u(1.4, s), y - int(13.4 * s)], fill=hex2(_ac(tas, -0.15)))
        d.polygon([(mx - _u(0.9, s), y - mh), (mx, y - mh - int(4 * s)), (mx + _u(0.9, s), y - mh)], fill=hex2(kursun))
        d.rectangle([mx - _u(1.2, s), y - int(2 * s), mx + _u(1.2, s), y - 1], fill=hex2(_ac(tas, -0.1)))


def siluet(img, y, tohum, renk, x0=0, x1=W, yogun=1.0, minare_boy=14, cami=2):
    """Uzak plan kıyı silüeti (tek renk, kenarlardan dikişsiz sarar): kıyı çizgisi y'ye oturan evler, selviler,
    kubbeler ve kısa minareler."""
    d = ImageDraw.Draw(img)
    rnd = random.Random(tohum)
    k = hex2(renk)
    ak = hex2(_ac(renk, 0.12))

    def dik(xa, ya, xb, yb, c=k):
        for xx in range(int(xa), int(xb) + 1):
            d.line([xx % W, ya, xx % W, yb], fill=c)

    x = x0
    while x < x1:                                                    # evler ve damlar
        w = rnd.randint(5, 10)
        h = rnd.randint(4, 9)
        dik(x, y - h, x + w, y)
        for j in range(w // 2 + 1):                                  # kırma dam
            dik(x + j, y - h - min(j, w - j) // 2, x + j, y - h)
            dik(x + w - j, y - h - min(j, w - j) // 2, x + w - j, y - h)
        x += w + rnd.randint(0, 3) - int(2 * (1 - yogun))
    for _ in range(int(9 * yogun)):                                  # selviler
        sx = rnd.randint(x0, x1)
        sh = rnd.randint(9, 15)
        for j in range(sh):
            yar = max(0, int(1.6 * math.sin(math.pi * (j + 1) / (sh + 1))))
            dik(sx - yar, y - j - 1, sx + yar, y - j - 1, hex2(_ac(renk, -0.12)))
    for c in range(cami):                                            # kubbeli camiler ve minareler
        cx = x0 + int((c + 0.5) * (x1 - x0) / max(1, cami)) + rnd.randint(-20, 20)
        r = rnd.randint(6, 9)
        dik(cx - r - 3, y - 7, cx + r + 3, y)
        for j in range(-r, r + 1):
            hh = int(math.sqrt(max(0, r * r - j * j)) * 0.85)
            dik(cx + j, y - 7 - hh, cx + j, y - 7)
        for yn in (-1, 1):
            mx = cx + yn * (r + 6)
            dik(mx - 1, y - minare_boy, mx, y)
            dik(mx - 2, y - minare_boy + 4, mx + 1, y - minare_boy + 4)
            for j in range(4):
                dik(mx - (1 if j < 2 else 0), y - minare_boy - j, mx - (1 if j < 2 else 0), y - minare_boy - j)
        for j in range(0, r, 3):
            piksel(img, (cx - r + j) % W, y - 7 - int(r * 0.5), ak)


def kese(img, x, zemin, s=1.0, renk="#8a2a2a", sikke="#f0c040", sac=True):
    """Yeni figür: büzgülü kadife kese; ağzı iple bağlı, yanına birkaç sikke dökülmüş. Zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 4 * s)
    temas_golgesi(img, x, y, 6 * s)
    d.ellipse([x - int(3 * s), y - int(3.8 * s), x + int(3 * s), y - 1], fill=hex2(renk))           # şişkin gövde
    d.polygon([(x - int(1 * s), y - int(3.4 * s)), (x + int(1 * s), y - int(3.4 * s)), (x + int(0.8 * s), y - int(4.4 * s)),
               (x - int(0.8 * s), y - int(4.4 * s))], fill=hex2(renk))                                # büzgülü boyun
    d.polygon([(x - int(0.8 * s), y - int(4.4 * s)), (x - int(2 * s), y - int(5.6 * s)), (x - int(0.6 * s), y - int(5.2 * s)),
               (x, y - int(5.8 * s)), (x + int(0.6 * s), y - int(5.2 * s)), (x + int(2 * s), y - int(5.6 * s)),
               (x + int(0.8 * s), y - int(4.4 * s))], fill=hex2(_ac(renk, 0.12)))                     # kabarık ağız
    d.line([x - int(1.1 * s), y - int(4.3 * s), x + int(1.1 * s), y - int(4.3 * s)], fill=hex2("#e0b040"), width=_u(0.5, s))
    d.line([x + int(1.1 * s), y - int(4.3 * s), x + int(1.8 * s), y - int(3 * s)], fill=hex2("#e0b040"))    # sarkan ip
    d.chord([x - int(2.4 * s), y - int(3.4 * s), x - int(0.2 * s), y - int(1 * s)], 90, 270, fill=hex2(_ac(renk, 0.2)))
    if sac:
        for dx in (3.4, 4.6):
            cx = x + int(dx * s)
            d.ellipse([cx - _u(0.7, s), y - _u(0.9, s), cx + _u(0.7, s), y - 1], fill=hex2(sikke), outline=hex2(_ac(sikke, -0.35)))
        piksel(img, x + int(3.4 * s), y - _u(0.9, s), hex2("#fff8d0"))


def fici(img, x, zemin, s=1.0, renk="#7a5232"):
    """Yeni figür: barut fıçısı: şişkin tahta gövde, demir çemberler, kapağında kara barut lekesi. Zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 4 * s)
    temas_golgesi(img, x, y, 5 * s)
    d.ellipse([x - int(2.6 * s), y - int(6.4 * s), x + int(2.6 * s), y - 1], fill=hex2(renk))
    d.rectangle([x - int(2.2 * s), y - int(6 * s), x + int(2.2 * s), y - 1], fill=hex2(renk))
    for yy in (y - int(1.4 * s), y - int(4.8 * s)):
        d.line([x - int(2.4 * s), yy, x + int(2.4 * s), yy], fill=hex2("#3a3a3e"), width=_u(0.5, s))
    for dx in (-1.2, 0, 1.2):
        d.line([x + int(dx * s), y - int(5.8 * s), x + int(dx * s), y - int(1 * s)], fill=hex2(_ac(renk, -0.2)))
    d.ellipse([x - int(2.2 * s), y - int(6.8 * s), x + int(2.2 * s), y - int(5.6 * s)], fill=hex2(_ac(renk, 0.2)))
    d.ellipse([x - int(0.8 * s), y - int(6.5 * s), x + int(0.6 * s), y - int(6 * s)], fill=hex2("#2a2420"))


def fisek(img, x, zemin, s=1.0, govde="#a8301e", serit="#e0b040", alev=0.0, kalin=1.0):
    """Yeni figür: Lagari'nin fişeği. Ahşap sehpanın dört ayağı zemine basar; sehpadaki kalın gövde, iki yanında daha
    kısa iki kol (kolların sayısı vurgulanmaz), üstte ahşap oturak. alev 0-1: gövdenin dibinden kıvılcım ve alev.
    Dönen değer: oturağın y'si."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(6 * s), x + int(6 * s), "fişek sehpası", tolerans=max(3, int(s)))
    temas_golgesi(img, x, y, 13 * s)
    ah = hex2("#6a4428")
    halka = y - int(7 * s)
    for ax in (-6, -2.5, 2.5, 6):                                       # sehpa ayakları
        d.line([x + int(ax * s), y - 1, x + int(ax * 0.45 * s), halka], fill=ah, width=_u(0.8, s))
    d.line([x - int(5 * s), y - int(2.5 * s), x + int(5 * s), y - int(2.5 * s)], fill=ah, width=_u(0.5, s))
    d.rectangle([x - int(3.6 * s), halka - _u(0.8, s), x + int(3.6 * s), halka], fill=hex2("#8a5a34"))
    k = kalin
    for yn in (-1, 1):                                                   # yan kollar (kısa, arkada)
        cx = x + yn * int(2.3 * s * k)
        d.rectangle([cx - int(1 * s * k), y - int(18 * s), cx + int(1 * s * k), halka], fill=hex2(_ac(govde, -0.25)))
        d.polygon([(cx - int(1 * s * k), y - int(18 * s)), (cx, y - int(20 * s)), (cx + int(1 * s * k), y - int(18 * s))],
                  fill=hex2(_ac(serit, -0.2)))
        d.line([cx - int(1 * s * k), y - int(12 * s), cx + int(1 * s * k), y - int(12 * s)], fill=hex2(serit))
    ust = y - int(22 * s)
    gx = int(1.6 * s * k)
    d.rectangle([x - gx, ust, x + gx, halka + int(1.4 * s)], fill=hex2(govde))   # ana gövde
    d.line([x - gx, ust, x - gx, halka + int(1.4 * s)], fill=hex2(_ac(govde, 0.25)))
    for yy in (ust + int(3 * s), ust + int(8 * s), ust + int(13 * s)):
        d.rectangle([x - gx, yy, x + gx, yy + _u(0.6, s)], fill=hex2(serit))
    d.rectangle([x - int(3 * s * k), ust - _u(0.9, s), x + int(3 * s * k), ust], fill=hex2("#8a5a34"), outline=hex2("#3a2414"))  # oturak
    fit = halka + int(1.4 * s)
    d.line([x, fit, x + int(0.6 * s), fit + int(1.6 * s)], fill=hex2("#3a2a1a"))        # fitil
    if alev > 0:
        for j in range(int(10 * alev)):
            ax = x + int((j % 5 - 2) * 0.7 * s)
            boy = int((2 + (j * 7) % 4) * s * alev)
            d.polygon([(ax - _u(0.6, s), fit), (ax, fit + boy), (ax + _u(0.6, s), fit)],
                      fill=hex2(("#fff0a0", "#f8a030", "#e8601c")[j % 3]))
    return ust - _u(0.9, s)


def yuzen(img, x, su_y, s=1.0, yon=-1, f=0.0, govde=LAGARI["govde"], sac="#2a1a12"):
    """Yeni figür: denizde yüzen adam (kulaç). Baş, omuzlar ve sırasıyla suya giren kollar su çizgisinin üstünde;
    gövdenin geri kalanı suyun altındadır (su_y'den aşağısı çizilmez). Arkasında V biçimli iz, çevresinde köpük."""
    d = ImageDraw.Draw(img)
    r = max(2, int(1.7 * s))
    k = yeni(img.width, img.height)
    dk = ImageDraw.Draw(k)
    dk.ellipse([x - int(3.4 * s), su_y - int(1.6 * s), x + int(3.4 * s), su_y + int(1.6 * s)], fill=hex2(govde))   # omuzlar
    bx, by = x + yon * int(0.8 * s), su_y - int(2.2 * s) + int(SIN(f, 2) * 0.3 * s)
    dk.ellipse([bx - r, by - r, bx + r, by + r], fill=hex2("#e8b890"))
    dk.chord([bx - r, by - r - 1, bx + r, by + r - _u(0.6, s)], 180, 360, fill=hex2(sac))          # ıslak saç
    piksel(k, bx + yon * int(1 * s), by, hex2("#2b1a12"))
    for j, faz in enumerate((f, (f + 0.5) % 1)):                                                # iki kol sırayla
        a = faz * 2 * math.pi
        if math.sin(a) > 0:
            omuz = (x - yon * int(1.6 * s) * (1 if j else -1), su_y - int(0.8 * s))
            el = (x + yon * int(4.6 * s * math.cos(a)), su_y - int(4 * s * math.sin(a)))
            dk.line([*omuz, *el], fill=hex2(_ac(govde, -0.15)), width=_u(1, s))
            dk.ellipse([el[0] - _u(0.6, s), el[1] - _u(0.6, s), el[0] + _u(0.6, s), el[1] + _u(0.6, s)], fill=hex2("#e8b890"))
    px = k.load()
    for yy in range(su_y, k.height):                                                             # su çizgisinin altı silinir
        for xx in range(max(0, x - int(8 * s)), min(k.width, x + int(8 * s))):
            px[xx, yy] = (0, 0, 0, 0)
    img.alpha_composite(k)
    for j in range(1, int(12 * s)):                                                             # arkada V izi
        for sg in (-1, 1):
            if (j + int(f * 8)) % 3:
                piksel(img, x - yon * (int(3 * s) + j), su_y + sg * (j // 4) + 1, hex2("#c8dcec", 150))
    for kk in range(-int(4 * s), int(4 * s) + 1):                                               # köpük
        if (kk + int(f * 6)) % 3 == 0:
            piksel(img, x + kk, su_y, hex2("#e8f2f8", 200))


def terazi(img, x, zemin, s=1.0, egim=0.0, sol="kitap", sag="tuy"):
    """Yeni figür: kefeli pirinç terazi. Taban zemine basar, direğin tepesindeki kol egim kadar yatar; kefeler kol
    uçlarına zincirle asılıdır. sol/sag: kefedeki nesne ('kitap' ya da 'tuy': kartal tüyü)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    temas_golgesi(img, x, y, 8 * s)
    pr = hex2("#c8a040")
    pk = hex2("#7a5a1a")
    d.polygon([(x - int(4 * s), y - 1), (x - int(2 * s), y - int(2 * s)), (x + int(2 * s), y - int(2 * s)), (x + int(4 * s), y - 1)], fill=pk)
    tepe = y - int(16 * s)
    d.line([x, y - int(2 * s), x, tepe], fill=pr, width=_u(0.8, s))
    d.ellipse([x - _u(0.8, s), tepe - _u(0.8, s), x + _u(0.8, s), tepe + _u(0.8, s)], fill=hex2("#e0b850"))
    kol = 9 * s
    uclar = []
    for yn in (-1, 1):
        ux, uy = x + yn * kol, tepe + yn * kol * egim
        d.line([x, tepe, ux, uy], fill=pr, width=_u(0.6, s))
        uclar.append((ux, uy))
    for (ux, uy), nesne in zip(uclar, (sol, sag)):
        ky = uy + 8 * s
        for dx in (-2.4, 0, 2.4):
            d.line([ux, uy, ux + dx * s, ky], fill=hex2("#a88a40"))
        d.chord([ux - 3 * s, ky - 1.4 * s, ux + 3 * s, ky + 1.2 * s], 0, 180, fill=pr, outline=pk)
        if nesne == "kitap":
            d.rectangle([ux - 1.8 * s, ky - 1.4 * s, ux + 1.8 * s, ky - 0.2 * s], fill=hex2("#6a2a2a"), outline=hex2("#2a1a10"))
            d.line([ux - 1.6 * s, ky - 0.8 * s, ux + 1.6 * s, ky - 0.8 * s], fill=hex2("#e8dcc0"))
        elif nesne == "tuy":
            for j in range(int(4 * s)):
                tx = ux - 1.8 * s + j
                ty = ky - 0.6 * s - math.sin(math.pi * j / (4 * s)) * 1.2 * s
                piksel(img, tx, ty, hex2("#5e3c22"))
                piksel(img, tx, ty - 1, hex2("#9a7040"))
            piksel(img, ux + 2.2 * s, ky - 0.6 * s, hex2("#e8e0d0"))


def ucak(img, x, zemin, s=1.0, yon=1, f=0.0, govde="#f0f0ec", serit="#c8302a"):
    """Yeni figür: bugünkü küçük tek motorlu eğitim uçağı (üstten kanatlı). Ana ve burun tekerlekleri piste basar,
    pervane f ile döner (bulanık disk)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 14 * s)
    temas_golgesi(img, x, y, 24 * s, alfa=90)

    def X(v):
        return x + int(v * s) * yon

    gy = y - int(4.2 * s)                                                     # gövde alt hattı
    d.polygon([(X(-14), gy - int(3.6 * s)), (X(-14), gy - int(2.4 * s)), (X(-2), gy), (X(9), gy), (X(11), gy - int(1.4 * s)),
               (X(11), gy - int(3.4 * s)), (X(4), gy - int(5.6 * s)), (X(-3), gy - int(5.4 * s))], fill=hex2(govde))
    d.line([X(-13), gy - int(2.4 * s), X(10), gy - int(1.2 * s)], fill=hex2(serit), width=_u(0.6, s))
    d.polygon([(X(-14), gy - int(3.6 * s)), (X(-15), gy - int(9 * s)), (X(-11.5), gy - int(9 * s)), (X(-9), gy - int(3.8 * s))],
              fill=hex2(govde))                                               # dikey kuyruk
    d.line([X(-14.5), gy - int(8.4 * s), X(-11.5), gy - int(8.4 * s)], fill=hex2(serit), width=_u(0.6, s))
    d.polygon([(X(-16), gy - int(3.2 * s)), (X(-10), gy - int(3.4 * s)), (X(-10), gy - int(2.8 * s)), (X(-16), gy - int(2.6 * s))],
              fill=hex2(_ac(govde, -0.12)))                                   # yatay kuyruk
    d.rectangle([min(X(-3), X(6)), gy - int(6.4 * s), max(X(-3), X(6)), gy - int(5.6 * s)], fill=hex2(_ac(govde, -0.06)))  # kanat (kesit)
    d.line([X(1), gy - int(1.6 * s), X(-1.5), gy - int(5.6 * s)], fill=hex2("#8a8a90"), width=_u(0.3, s))     # kanat dikmesi
    d.polygon([(X(1), gy - int(5.4 * s)), (X(5), gy - int(5.4 * s)), (X(8), gy - int(3.4 * s)), (X(1), gy - int(3.4 * s))],
              fill=hex2("#3a5a7a"))                                           # kabin camı
    d.line([X(3.2), gy - int(5.4 * s), X(3.2), gy - int(3.4 * s)], fill=hex2(govde))
    for tx, ty in ((-1, 0), (8.5, 0)):                                         # tekerlek bacakları ve tekerlekler
        d.line([X(tx), gy - 1, X(tx), y - int(1.2 * s)], fill=hex2("#5a5a60"), width=_u(0.4, s))
        d.ellipse([X(tx) - _u(1.2, s), y - int(2.4 * s), X(tx) + _u(1.2, s), y - 1], fill=hex2("#2a2a2e"))
        piksel(img, X(tx), y - int(1.2 * s), hex2("#9a9aa0"))
    px_ = X(11.6)
    d.rectangle([min(px_, X(12.4)), gy - int(2.8 * s), max(px_, X(12.4)), gy - int(1.8 * s)], fill=hex2("#3a3a40"))
    for j in range(-int(3.4 * s), int(3.4 * s) + 1):                         # pervane diski
        if (j + int(f * 24)) % 3 == 0:
            piksel(img, X(12.6), gy - int(2.3 * s) + j, hex2("#c8c8d0", 170))
    a = f * 2 * math.pi * 3
    d.line([X(12.6), gy - int(2.3 * s) - int(3.2 * s * math.cos(a)), X(12.6), gy - int(2.3 * s) + int(3.2 * s * math.cos(a))],
           fill=hex2("#2a2a2e"))


def hangar(img, x0, x1, zemin, s=1.0, renk="#9aa4ac"):
    """Yeni figür: yarım silindir çatılı hangar, büyük sürgülü kapı. Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "hangar", tolerans=max(3, int(s)))
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0 + 4, alfa=90)
    h = int(10 * s)
    d.rectangle([x0, y - h, x1, y - 1], fill=hex2(renk))
    d.chord([x0, y - h - int(6 * s), x1, y - h + int(6 * s)], 180, 360, fill=hex2(_ac(renk, -0.1)))
    for k in range(x0 + 3, x1, 4):
        d.line([k, y - h, k, y - 2], fill=hex2(_ac(renk, -0.15)))
    kx = (x0 + x1) // 2
    d.rectangle([kx - int(6 * s), y - int(8 * s), kx + int(6 * s), y - 1], fill=hex2("#3a3e44"))
    d.line([kx, y - int(8 * s), kx, y - 1], fill=hex2("#5a5e64"))


def ruzgar_tulumu(img, x, zemin, s=1.0, f=0.0, yon=1):
    """Yeni figür: kısa direkli rüzgâr tulumu: direk zemine dikili, turuncu-beyaz çizgili tulum rüzgârla dalgalanır."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 2 * s)
    temas_golgesi(img, x, y, 3 * s)
    tepe = y - int(12 * s)
    d.line([x, y - 1, x, tepe], fill=hex2("#d8d8dc"), width=_u(0.5, s))
    for j in range(5):
        u0, u1 = j * 1.6 * s, (j + 1) * 1.6 * s
        dal = SIN(f + j * 0.15) * 0.4 * s
        r0, r1 = 1.4 * s * (1 - j * 0.12), 1.4 * s * (1 - (j + 1) * 0.12)
        d.polygon([(x + yon * u0, tepe - r0 + dal), (x + yon * u1, tepe - r1 + dal * 1.4), (x + yon * u1, tepe + r1 + dal * 1.4),
                   (x + yon * u0, tepe + r0 + dal)], fill=hex2("#f07020" if j % 2 == 0 else "#f4f0ec"))


def perde(img, x, zemin, s=1.0, f=0.0):
    """Yeni figür: sinema perdesi: siyah çerçeveli beyaz perde, iki ayağı zemine basar; perdede projeksiyon görüntüsü
    (gece mavisi gökte kule ve kanatlı adam silüeti), ışık f ile hafifçe titrer."""
    d = ImageDraw.Draw(img)
    g = int(16 * s)
    y = duz_zemin(zemin, x - g, x + g, "perde", tolerans=max(3, int(s)))
    temas_golgesi(img, x, y, 2 * g + 4, alfa=90)
    alt, ust = y - int(4 * s), y - int(22 * s)
    for ax in (-g + 2, g - 2):
        d.line([x + ax, y - 1, x + ax, alt], fill=hex2("#2a2a2e"), width=_u(0.8, s))
    d.rectangle([x - g, ust, x + g, alt], fill=hex2("#1a1a1e"))
    p = 0.06 * SIN(f, 3)
    d.rectangle([x - g + 2, ust + 2, x + g - 2, alt - 2], fill=hex2(_ac("#3a5a8a", p)))
    for j in range(ust + 2, alt - 2):                                     # alt yarı daha açık (ufuk)
        if j > (ust + alt) / 2:
            d.line([x - g + 2, j, x + g - 2, j], fill=hex2(_ac("#6a7aa0", p + (j - (ust + alt) / 2) / (alt - ust))))
    ky = alt - 3                                                          # perdede Galata Kulesi silüeti
    kx = x - int(7 * s)
    kr = max(2, int(1.6 * s))
    sil = hex2("#14141c")
    d.rectangle([kx - kr, ky - int(9 * s), kx + kr, ky], fill=sil)
    d.rectangle([kx - kr - 1, ky - int(9.6 * s), kx + kr + 1, ky - int(9 * s)], fill=sil)
    d.polygon([(kx - kr - 1, ky - int(9.6 * s)), (kx, ky - int(12.4 * s)), (kx + kr + 1, ky - int(9.6 * s))], fill=sil)
    d.rectangle([x - g + 2, ky - int(1.5 * s), x + g - 2, alt - 2], fill=hex2("#22263a"))   # perdede kıyı ve deniz
    ux, uy = x + int(5 * s), ust + int(8 * s) + int(SIN(f) * 1)          # perdede süzülen kanatlı adam silüeti
    for yn in (-1, 1):
        d.polygon([(ux, uy), (ux + yn * int(6 * s), uy - int(1.2 * s)), (ux + yn * int(5 * s), uy + int(0.8 * s)),
                   (ux + yn * int(2 * s), uy + int(1 * s))], fill=sil)
    d.rectangle([ux - 1, uy - int(1.8 * s), ux + 1, uy + int(2.6 * s)], fill=sil)
    d.ellipse([ux - 2, uy - int(2.6 * s), ux + 2, uy - int(1.6 * s)], fill=sil)


def koltuk_sirasi(img, x0, x1, zemin, s=1.0, bas=(), renk="#6a1e22"):
    """Yeni figür: sinema koltuk sırası (arkalıklar) zemine oturur; bas: koltukta oturan izleyicilerin baş x'leri."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, (x0 + x1) // 2, x1 - x0)
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0, alfa=90)
    for bx in bas:                                                       # oturan izleyici: omuz ve baş arkalığın üstünde
        d.rectangle([bx - int(2.4 * s), y - int(8 * s), bx + int(2.4 * s), y - int(5 * s)], fill=hex2("#1e1e24"))
        d.ellipse([bx - int(1.7 * s), y - int(11 * s), bx + int(1.7 * s), y - int(7.6 * s)], fill=hex2("#2a2228"))
    gen = int(6 * s)
    for kx in range(x0, x1 - gen + 1, gen + _u(1.4, s)):
        d.rounded_rectangle([kx, y - int(6.6 * s), kx + gen, y - 1], radius=_u(1.2, s), fill=hex2(renk))
        d.line([kx + 1, y - int(6.2 * s), kx + gen - 1, y - int(6.2 * s)], fill=hex2(_ac(renk, 0.25)))


def rampa(img, x, zemin, s=1.0):
    """Yeni figür: 2009 deneyinin çelik fırlatma rampası: kafes kule ve eğik ray, ayakları zemine cıvatalı beton
    kaideye basar. Dönen değer: rayın üst ucu (x, y)."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(5 * s), x + int(5 * s), "rampa", tolerans=max(3, int(s)))
    temas_golgesi(img, x, y, 12 * s)
    d.rectangle([x - int(5 * s), y - int(1.4 * s), x + int(5 * s), y - 1], fill=hex2("#9a968c"))
    ust = y - int(20 * s)
    ce = hex2("#8a8e94")
    for ax in (-2, 2):
        d.line([x + int(ax * s), y - int(1.4 * s), x + int(ax * s), ust], fill=ce, width=_u(0.5, s))
    yy = y - int(1.4 * s)
    while yy > ust + 2:                                                   # kafes çaprazları
        d.line([x - int(2 * s), yy, x + int(2 * s), yy - int(2.4 * s)], fill=hex2("#6a6e74"))
        d.line([x - int(2 * s), yy - int(2.4 * s), x + int(2 * s), yy - int(2.4 * s)], fill=ce)
        yy -= int(2.4 * s)
    return x, ust


def manken(img, x, zemin, s=1.0, yon=1, yatik=False):
    """Yeni figür: çarpışma testi mankeni (sarı-siyah işaretli). yatik=False: oturur; True: yere düşmüş, sırtüstü yatar.
    Her iki durumda gövde zemine (ya da oturağa) değer."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 8 * s)
    sari, kara = hex2("#e8c830"), hex2("#1a1a1e")
    if yatik:
        temas_golgesi(img, x, y, 12 * s)
        d.rectangle([x - int(4 * s), y - int(2.2 * s), x + int(2 * s), y - 1], fill=sari)
        d.line([x + int(2 * s), y - int(1 * s), x + int(6 * s), y - int(1 * s)], fill=sari, width=_u(1, s))
        d.ellipse([x - int(6.6 * s), y - int(2.6 * s), x - int(4 * s), y - 1], fill=sari)
        d.line([x - int(2 * s), y - int(2.2 * s), x, y - 1], fill=kara)
        return
    temas_golgesi(img, x, y, 6 * s)
    d.line([x, y - int(3 * s), x + yon * int(3 * s), y - int(3 * s)], fill=sari, width=_u(1.2, s))       # uyluk
    d.line([x + yon * int(3 * s), y - int(3 * s), x + yon * int(3.2 * s), y - 1], fill=sari, width=_u(1, s))
    d.rectangle([x - _u(1.4, s), y - int(9 * s), x + _u(1.4, s), y - int(3 * s)], fill=sari)
    d.line([x - _u(1.4, s), y - int(6 * s), x + _u(1.4, s), y - int(6 * s)], fill=kara)
    d.ellipse([x - int(1.5 * s), y - int(12 * s), x + int(1.5 * s), y - int(9 * s)], fill=sari)
    d.line([x - 1, y - int(10.5 * s), x + 1, y - int(10.5 * s)], fill=kara)


def beton_set(img, x0, x1, zemin, s=1.0):
    """Yeni figür: beton bariyer (New Jersey tipi) sırası: geniş taban zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, (x0 + x1) // 2, x1 - x0)
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0, alfa=90)
    g = int(7 * s)
    for kx in range(x0, x1 - g + 1, g + 1):
        d.polygon([(kx, y - 1), (kx + 1, y - int(2 * s)), (kx + int(1.6 * s), y - int(5 * s)), (kx + g - int(1.6 * s), y - int(5 * s)),
                   (kx + g - 1, y - int(2 * s)), (kx + g, y - 1)], fill=hex2("#b8b4a8"))
        d.line([kx + int(1.6 * s), y - int(5 * s), kx + g - int(1.6 * s), y - int(5 * s)], fill=hex2("#d8d4c8"))
        d.line([kx + 2, y - int(2.2 * s), kx + g - 2, y - int(2.2 * s)], fill=hex2("#8a867c"))


def fener(img, x, zemin, s=1.0, f=0.0, renk="#f8c860"):
    """Yeni figür: şenlik feneri: ahşap direk zemine dikili, kol ucunda asılı kâğıt fener titrer ve çevresine ışık düşer."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 2 * s)
    temas_golgesi(img, x, y, 4 * s)
    tepe = y - int(13 * s)
    d.line([x, y - 1, x, tepe], fill=hex2("#5a3a22"), width=_u(0.6, s))
    d.line([x, tepe, x + int(3 * s), tepe], fill=hex2("#5a3a22"), width=_u(0.4, s))
    fx, fy = x + int(3 * s), tepe + int(1 * s)
    d.line([fx, tepe, fx, fy], fill=hex2("#3a2414"))
    parla = 0.08 * SIN(f, 3)
    d.ellipse([fx - int(1.4 * s), fy, fx + int(1.4 * s), fy + int(3 * s)], fill=hex2(_ac(renk, parla)), outline=hex2("#8a3a1a"))
    for r in range(int(2 * s), int(6 * s), 2):
        for a in range(0, 360, 15):
            px_, py_ = fx + math.cos(math.radians(a)) * r, fy + 1.5 * s + math.sin(math.radians(a)) * r
            if _esik(int(px_), int(py_)) < 0.4 * (1 - r / (6 * s)):
                piksel(img, px_, py_, hex2(renk, 70))


def kosk(img, x, zemin, s=1.0, isik=False, tas="#c8bca4", ahsap="#8a5a3a", kursun="#6e7884"):
    """Yeni figür: sahil köşkü (Sinan Paşa Köşkü'nün temsili; mimari ayrıntısı bilinmiyor, sade Osmanlı köşkü): taş
    kaide düz zemine oturur, üstünde pencereli ahşap kat, geniş saçak ve kurşun kubbe. isik=True: pencerelerde ışık."""
    d = ImageDraw.Draw(img)
    g = int(12 * s)
    y = duz_zemin(zemin, x - g, x + g, "köşk", tolerans=max(3, int(s)))
    temas_golgesi(img, x, y, 2 * g + 4, alfa=90)
    ky = y - int(5 * s)
    d.rectangle([x - g, ky, x + g, y - 1], fill=hex2(tas))
    for yy in range(ky + _u(1.6, s), y - 1, _u(1.6, s)):
        d.line([x - g + 1, yy, x + g - 1, yy], fill=hex2(_ac(tas, -0.2)))
    uy = ky - int(8 * s)
    d.rectangle([x - g + _u(1, s), uy, x + g - _u(1, s), ky - 1], fill=hex2(ahsap))
    pen = hex2("#f8c860") if isik else hex2("#2a2a34")
    for px_ in range(x - g + _u(2.5, s), x + g - _u(2, s), _u(3.2, s)):
        d.rectangle([px_, uy + _u(1.6, s), px_ + _u(1.6, s), ky - _u(1.6, s)], fill=pen)
        d.line([px_ + _u(0.8, s), uy + _u(1.6, s), px_ + _u(0.8, s), ky - _u(1.6, s)], fill=hex2(_ac(ahsap, -0.3)))
    sac = g + int(2.5 * s)
    d.polygon([(x - sac, uy + _u(0.6, s)), (x - g + _u(2, s), uy - int(2.4 * s)), (x + g - _u(2, s), uy - int(2.4 * s)),
               (x + sac, uy + _u(0.6, s))], fill=hex2(kursun))
    d.line([x - sac, uy + _u(0.6, s), x + sac, uy + _u(0.6, s)], fill=hex2(_ac(kursun, -0.3)))
    d.chord([x - int(5 * s), uy - int(8 * s), x + int(5 * s), uy - int(1 * s)], 180, 360, fill=hex2(kursun))
    d.line([x, uy - int(4.6 * s), x, uy - int(6.4 * s)], fill=hex2("#e0b040"))
    if isik:
        for px_ in range(x - g + _u(2.5, s), x + g - _u(2, s), _u(3.2, s)):
            for k in range(6):
                piksel(img, px_ + k % 3, y + 1 + k // 3, hex2("#f8c860", 60))


# ==========================================================================
# KATMAN YARDIMCILARI (kütüphane katmanlarıyla aynı boyut ve dosya adları)
# ==========================================================================
GW = 810
SABAH = ["#5a76a4", "#7894bc", "#a4b0c4", "#d4bca8", "#eec8a0", "#f6dab0"]       # lodos sabahı (ılık, puslu)
GUN = ["#4a78b4", "#6894c4", "#88acd0", "#a8c2da", "#c4d6e2", "#dce6ea"]
AKSAM = ["#2a2a58", "#5a3a6a", "#a05a78", "#d88a7a", "#f0b088", "#f4c898"]
KIZIL_GOK = ["#2a1a3a", "#5a2a4a", "#9a3a4a", "#d0604a", "#ec8c4e", "#f4b070"]
GECE = ["#05081a", "#0a1028", "#121a3c", "#1a264e", "#24345e"]
DENIZ_SABAH = ("#5a7ea4", "#4a7098", "#3e628a", "#34567c")
DENIZ_GUN = ("#3e74a8", "#33669a", "#2a5a8c", "#224e7e")
DENIZ_AKSAM = ("#6a5a88", "#544c7a", "#44406c", "#38365e")
DENIZ_GECE = ("#1a2848", "#16223e", "#121c34", "#0e162a")
TAS_SICAK = ["#c8b89c", "#bcac90", "#b0a084", "#a49478", "#98886c"]
TAS_GECE = ["#4e4a54", "#46424c", "#3e3a44", "#36323c", "#2e2a34"]


def _gok(no, renkler, gunes_=None, bulutlar=(), bulut_renk=("#fff8ec", "#f4dcc8", "#d8a8a0"), yildiz=0):
    """Kütüphanenin gokyuzu katmanı; yıldızlar (yakın çekimde görünen 380-530 bandına da) eklenir."""
    img = gokyuzu(no, renkler, gunes_, bulutlar, bulut_renk, 0)
    if yildiz:
        rnd = random.Random(no)
        for _ in range(yildiz):
            x, y = rnd.randrange(W), rnd.randrange(380, 540)
            piksel(img, x, y, hex2("#fff8e0", rnd.choice((120, 180, 255))))
        kaydet(img, f"sahne{no}-gokyuzu.png")
    return img


def _uzak_deniz(no, kiyi, su, tepe, sil, su_renk, tohum, cami=2, minare=12, kule=None, isik=False, gemi_x=None):
    """Uzak plan (yeni katman yardımcısı): karşı kıyı tepeleri, kıyıya oturan şehir silüeti ve deniz. Yatayda dikişsiz.
    kule: Galata Kulesi silüetinin x'i (karşı kıyıda, kıyı çizgisine oturur). gemi_x: ufukta demirli küçük gemi."""
    img = yeni()
    hat = sirt(kiyi, 4, tohum, 3, 0.6, w=W, dongulu=True)
    arazi(img, hat, list(tepe))
    siluet(img, su, tohum, sil, 0, W, cami=cami, minare_boy=minare)
    d = ImageDraw.Draw(img)
    if kule is not None:                                             # karşı kıyıda küçük Galata Kulesi
        r = 3
        d.rectangle([kule - r, su - 13, kule + r, su - 1], fill=hex2(_ac(sil, -0.12)))
        d.rectangle([kule - r - 1, su - 15, kule + r + 1, su - 13], fill=hex2(_ac(sil, -0.12)))
        d.polygon([(kule - r - 1, su - 15), (kule, su - 20), (kule + r + 1, su - 15)], fill=hex2(_ac(sil, -0.2)))
    if isik:                                                         # gece: kıyıda yanan pencereler
        rnd = random.Random(tohum + 9)
        for _ in range(70):
            x, y = rnd.randrange(W), su - rnd.randint(2, 8)
            if img.getpixel((x, y))[3] > 0:
                piksel(img, x, y, hex2("#f8c860"))
    for y in range(su, H):                                           # deniz: titreşimli bantlar
        v = (y - su) / 9
        i = min(len(su_renk) - 1, int(v))
        f = v - int(v)
        for x in range(W):
            j = i + 1 if (i < len(su_renk) - 1 and f > 0.5 and _esik(x, y) < (f - 0.5) * 2) else i
            img.putpixel((x, y), hex2(su_renk[j]))
    rnd = random.Random(tohum + 3)
    for _ in range(260):                                             # dalga parıltıları (dikişsiz)
        x, y = rnd.randrange(W), rnd.randrange(su + 1, su + 90)
        for k in range(rnd.randint(2, 4 + (y - su) // 12)):
            piksel(img, (x + k) % W, y, hex2(_ac(su_renk[0], 0.35), 170))
    if gemi_x is not None:                                           # ufukta demirli küçük gemi (su çizgisine oturur)
        gy = su + 8
        d.polygon([(gemi_x - 9, gy - 3), (gemi_x + 9, gy - 3), (gemi_x + 7, gy), (gemi_x - 7, gy)], fill=hex2(_ac(sil, -0.25)))
        d.line([gemi_x, gy - 3, gemi_x, gy - 16], fill=hex2(_ac(sil, -0.3)))
        d.polygon([(gemi_x - 5, gy - 15), (gemi_x + 5, gy - 15), (gemi_x + 6, gy - 5), (gemi_x - 4, gy - 5)], fill=hex2(_ac(sil, 0.25)))
    kaydet(img, f"sahne{no}-uzak.png")
    return img


def _orta_duz(no, ust, renkler, tur="tas", korkuluk=0, ekle=None, kenar=None):
    """Orta plan (yeni katman yardımcısı, 810 geniş): dümdüz yapay zemin (taş döşeme, kaldırım, toprak dam, pist).
    Üst kenar = zeminin uzak kenarı; korkuluk>0 ise uzak kenarda o boyda alçak taş korkuluk (zemine oturur).
    ekle(img, z): zemin üstüne figür ve yapılar (z = düz zemin çizgisi)."""
    img = yeni(GW, H)
    d = ImageDraw.Draw(img)
    renk_y = lambda y: renkler[min(len(renkler) - 1, int((y - ust) / 22))]  # noqa: E731
    for y in range(ust, H):
        d.line([0, y, GW, y], fill=hex2(renk_y(y)))
    rnd = random.Random(no)
    if tur in ("tas", "kaldirim"):
        y, ara, k = ust + 3, 3.0, 0
        while y < H:
            d.line([0, y, GW, y], fill=hex2(_ac(renk_y(y), -0.16)))
            adim = int(ara * (4.2 if tur == "tas" else 1.8))
            ofs = (k % 2) * adim // 2
            for x in range(ofs, GW, max(3, adim)):
                d.line([x + int((x - GW / 2) * (y - ust) / 900), y - int(ara) + 1, x + int((x - GW / 2) * (y - ust) / 900), y - 1],
                       fill=hex2(_ac(renk_y(y), -0.12)))
            ara = ara * 1.16 + 0.35
            y += int(ara)
            k += 1
    elif tur == "dam":                                               # toprak dam: titreşimli doku, kuru ot
        for _ in range(2600):
            x, y = rnd.randrange(GW), rnd.randrange(ust + 1, H)
            piksel(img, x, y, hex2(_ac(renk_y(y), rnd.choice((-0.12, 0.08)))))
    elif tur == "pist":                                              # çayır üstünde asfalt pist (orta bölümde)
        for y in range(ust, H):
            pass
        a0 = ust + 26
        d.rectangle([0, a0, GW, a0 + 70], fill=hex2("#4a4c50"))
        d.line([0, a0, GW, a0], fill=hex2("#e8e8e0"))
        d.line([0, a0 + 70, GW, a0 + 70], fill=hex2("#e8e8e0"))
        for x in range(0, GW, 40):
            d.rectangle([x, a0 + 34, x + 20, a0 + 36], fill=hex2("#f0f0e8"))
    d.line([0, ust, GW, ust], fill=hex2(kenar or _ac(renkler[0], 0.22)))
    if korkuluk:                                                     # alçak taş korkuluk: uzak kenarın üstüne oturur
        k = hex2(_ac(renkler[0], -0.08))
        d.rectangle([0, ust - korkuluk, GW, ust - korkuluk + 1], fill=hex2(_ac(renkler[0], 0.12)))
        for x in range(0, GW, 6):
            d.rectangle([x, ust - korkuluk + 2, x + 2, ust - 1], fill=k)
    if ekle:
        ekle(img, duz(ust + 4))
    kaydet(img, f"sahne{no}-orta.png")
    return img


def _on_bos(no):
    kaydet(yeni(GW, H), f"sahne{no}-on.png")


# Sahne ayarları: TSX Bolum değerleriyle aynı (yk: yakin, w/h: sprite kare boyu, x: sprite ızgara x'i ya da [baş, son],
# taban: sprite tabanı, fps). Python denetimleri bu değerlerle yapılır; Hezarfen.tsx aynı sayıları kullanır.
class _P(dict):
    __getattr__ = dict.get


P = {n: _P(v) for n, v in {
    370: dict(yk=2.8, w=380, h=230, x=270, taban=632, fps=10),
    371: dict(yk=2.8, w=380, h=230, x=270, taban=632, fps=10),
    372: dict(yk=3.0, w=400, h=300, x=270, taban=634, fps=10),
    373: dict(yk=2.6, w=420, h=230, x=[245, 295], taban=632, fps=14),
    374: dict(yk=3.2, w=400, h=300, x=270, taban=634, fps=10),
    375: dict(yk=2.8, w=380, h=230, x=270, taban=632, fps=10),
    376: dict(yk=2.8, w=380, h=230, x=270, taban=632, fps=8),
    377: dict(yk=2.8, w=400, h=230, x=[240, 290], taban=632, fps=14),
    378: dict(yk=2.8, w=380, h=230, x=270, taban=632, fps=8),
    379: dict(yk=2.6, w=400, h=230, x=270, taban=632, fps=10),
    380: dict(yk=2.8, w=380, h=230, x=270, taban=632, fps=8),
    381: dict(yk=2.6, w=420, h=230, x=[250, 300], taban=650, fps=10, odak=600, yaziY=230),
    382: dict(yk=2.8, w=380, h=230, x=270, taban=632, fps=10),
    383: dict(yk=2.8, w=400, h=300, x=270, taban=634, fps=8),
    384: dict(yk=2.8, w=400, h=300, x=270, taban=634, fps=8),
    385: dict(yk=2.6, w=420, h=230, x=[300, 230], taban=632, fps=10),
    386: dict(yk=2.8, w=400, h=230, x=270, taban=632, fps=6),
    387: dict(yk=2.6, w=400, h=230, x=270, taban=632, fps=8),
    388: dict(yk=3.2, w=400, h=300, x=270, taban=634, fps=10),
    389: dict(yk=3.0, w=400, h=300, x=270, taban=634, fps=10),
    390: dict(yk=2.8, w=400, h=300, x=270, taban=634, fps=8),
    391: dict(yk=2.6, w=400, h=230, x=270, taban=632, fps=10),
    392: dict(yk=2.8, w=400, h=230, x=270, taban=632, fps=10),
    393: dict(yk=2.8, w=380, h=230, x=270, taban=632, fps=10),
    394: dict(yk=2.6, w=400, h=230, x=270, taban=632, fps=10),
    395: dict(yk=2.6, w=400, h=230, x=270, taban=632, fps=8),
    396: dict(yk=2.8, w=400, h=230, x=[300, 240], taban=632, fps=8),
    397: dict(yk=2.8, w=400, h=300, x=270, taban=634, fps=8),
    398: dict(yk=2.6, w=420, h=230, x=270, taban=632, fps=12),
    399: dict(yk=2.6, w=420, h=230, x=270, taban=632, fps=8),
    400: dict(yk=2.8, w=400, h=300, x=270, taban=634, fps=10),
    401: dict(yk=2.8, w=400, h=300, x=270, taban=634, fps=10),
    402: dict(yk=3.0, w=400, h=300, x=270, taban=634, fps=8),
    403: dict(yk=2.6, w=420, h=230, x=[220, 310], taban=632, fps=16),
    404: dict(yk=2.8, w=400, h=300, x=270, taban=634, fps=8),
    405: dict(yk=2.6, w=400, h=230, x=270, taban=632, fps=8),
    406: dict(yk=2.8, w=380, h=230, x=270, taban=632, fps=10),
}.items()}


def _sx(p):
    return p.x if not isinstance(p.x, list) else p.x


_DENETIM = [False]     # yazı bandı denetiminde tavandan sarkan kandil sayılmaz (bilinçli istisna: zincir tavana kadar)


def _kandil(t, x, f, no):
    if not _DENETIM[0]:
        p = P[no]
        kandil(t, x, 0, f, zincir=_kz(p.yk, p.taban, p.h))


def _cek(no, kare, esik=0.75, satir=3, serbest=0, kenar_haric_alt=0, kenar_serbest=False):
    """Sprite'ı P[no] ayarlarıyla denetleyip yazar: görünür aralık (sahne sonundaki %6 yakınlaşma dahil) ve yazı bandı."""
    p = P[no]
    _DENETIM[0] = True
    try:
        kam = 14 if isinstance(p.x, list) else 8                        # TSX kamera genliği (paralaks payı)
        _kadraj(no, kare, p.w, p.h, p.yk * 1.06, esik, p.taban, satir, serbest, odak=p.odak, yaziY=p.yaziY,
                sxler=tuple(p.x) if isinstance(p.x, list) else (p.x,), kenar_pay=8 + int(kam * 0.65 / 2 + 1),
                kenar_haric_alt=kenar_haric_alt, kenar_serbest=kenar_serbest)
    finally:
        _DENETIM[0] = False
    sprite(no, "karakter", p.w, p.h, KARE, kare)


def _yerel(no, izgara_x, sx=None):
    """Izgara x'ini sprite yerel x'ine çevirir (sx verilmezse sahnenin ilk sx'i)."""
    p = P[no]
    if sx is None:
        sx = p.x[0] if isinstance(p.x, list) else p.x
    return izgara_x - (sx - p.w / 2)


def _uzak_kara(no, kiyi, taban, tepe, sil, ova, tohum, cami=1, minare=10, kule=None, yogun=1.0, damlar=None):
    """Uzak plan (yeni katman yardımcısı): tepeler, ufuk çizgisine oturan şehir silüeti ve dümdüz ova. Dikişsiz."""
    img = yeni()
    hat = sirt(kiyi, 5, tohum, 3, 0.6, w=W, dongulu=True)
    arazi(img, hat, list(tepe))
    if sil:
        siluet(img, taban, tohum, sil, 0, W, yogun=yogun, cami=cami, minare_boy=minare)
    if kule is not None:
        d = ImageDraw.Draw(img)
        r = 3
        d.rectangle([kule - r, taban - 13, kule + r, taban - 1], fill=hex2(_ac(sil, -0.12)))
        d.rectangle([kule - r - 1, taban - 15, kule + r + 1, taban - 13], fill=hex2(_ac(sil, -0.12)))
        d.polygon([(kule - r - 1, taban - 15), (kule, taban - 20), (kule + r + 1, taban - 15)], fill=hex2(_ac(sil, -0.2)))
    arazi(img, [taban] * W, list(ova), None, doku_tohum=no + 3)
    if damlar:                                                       # aşağıda kalan şehrin düz damları (yukarıdan bakış)
        d = ImageDraw.Draw(img)
        rnd = random.Random(no + 11)
        y, sira = taban + 2, 0
        while y < 640:
            bh = 3 + sira                                            # yakına doğru büyüyen sıra yüksekliği (perspektif)
            x = rnd.randint(-10, 0)
            while x < W + 10:
                w = rnd.randint(6, 10) + sira * 2
                renk = _ac(damlar, rnd.uniform(-0.12, 0.08))
                x0 = x % W
                d.rectangle([x0, y + 1, min(W - 1, x0 + w), y + bh], fill=hex2(_ac(renk, -0.28)))       # cephe (gölgede)
                d.rectangle([x0, y - 1, min(W - 1, x0 + w), y + 1], fill=hex2(_ac(renk, 0.15)))         # dam yüzü (ışıkta)
                if rnd.random() < 0.5 and w > 7:
                    d.rectangle([x0 + 2, y + bh // 2 + 1, x0 + 3, y + bh - 1], fill=hex2("#2a1a14"))     # kapı/pencere
                x += w + rnd.randint(2, 4)
            y += bh + 3
            sira += 1
    kaydet(img, f"sahne{no}-uzak.png")
    return img


def _su_bandi(t, y0, orta_ust, sprite_ust, renkler):
    """Sprite'ın alt satırlarına orta plandaki denizle AYNI renkte su bandı (dikiş görünmez): her satırın rengi o satırın
    dünya y'sinden hesaplanır (su_ve_kiyi: 30 satırlık bantlar). Sprite tabanı bu suya oturur."""
    d = ImageDraw.Draw(t)
    for y in range(y0, t.height):
        dy = sprite_ust + y - orta_ust
        d.line([0, y, t.width, y], fill=hex2(renkler[min(len(renkler) - 1, max(0, dy) // 30)]))


def _orta_deniz(no, ust, renkler):
    """Orta plan deniz (kütüphanenin su_ve_kiyi'si, kumsalsız)."""
    img = yeni(GW, H)
    su_ve_kiyi(img, ust, renkler)
    kaydet(img, f"sahne{no}-orta.png")
    return img


def ev(img, x, zemin, s=1.0, duvar="#c8a878", cati="#a8452e", isik=False):
    """Yeni figür: İstanbul ahşap evi: düz zemine oturan iki katlı gövde, çıkma (cumba), kırma kiremit dam."""
    d = ImageDraw.Draw(img)
    g = int(6 * s)
    y = duz_zemin(zemin, x - g, x + g, "ev", tolerans=max(3, int(s)))
    temas_golgesi(img, x, y, 2 * g + 2, alfa=90)
    h = int(9 * s)
    d.rectangle([x - g, y - h, x + g, y - 1], fill=hex2(duvar))
    d.rectangle([x - g - _u(1, s), y - h, x + g + _u(1, s), y - int(5 * s)], fill=hex2(_ac(duvar, -0.06)))   # çıkma kat
    d.line([x - g - _u(1, s), y - int(5 * s), x + g + _u(1, s), y - int(5 * s)], fill=hex2(_ac(duvar, -0.3)))
    pen = hex2("#f8c860") if isik else hex2("#3a2a22")
    for px_ in (x - int(3.5 * s), x + int(1.5 * s)):
        d.rectangle([px_, y - int(8 * s), px_ + _u(1.6, s), y - int(6 * s)], fill=pen)
    d.rectangle([x - _u(1, s), y - int(3.6 * s), x + _u(1, s), y - 1], fill=hex2("#4a2a1a"))
    d.polygon([(x - g - _u(2, s), y - h), (x - int(2 * s), y - h - int(4 * s)), (x + int(2 * s), y - h - int(4 * s)),
               (x + g + _u(2, s), y - h)], fill=hex2(cati))
    d.line([x - g - _u(2, s), y - h, x + g + _u(2, s), y - h], fill=hex2(_ac(cati, -0.3)))
    return (x + int(3 * s), y - h - int(3 * s))                     # baca noktası


def _toz(t, x, y, f, s=1.0, adet=6, renk="#d8c8a8"):
    """Zeminden kalkan toz: puflar ayak hizasından doğar, yükselip yana açılır ve söner (yarı saydam)."""
    for k in range(adet):
        ph = (f + k / adet) % 1
        yon = -1 if k % 2 else 1
        px_ = x + yon * (1.5 + ph * 6) * s
        py_ = y - 1 - ph * 4 * s
        r = (0.6 + ph * 1.4) * s
        alfa = int(150 * (1 - ph))
        for yy in range(int(py_ - r), int(py_ + r) + 1):
            for xx in range(int(px_ - r), int(px_ + r) + 1):
                if (xx - px_) ** 2 + (yy - py_) ** 2 <= r * r and yy < y and _esik(xx, yy) < 0.6:
                    piksel(t, xx, yy, hex2(renk, alfa))


def _hilal(img, x, y, r, renk="#f4ecd0"):
    k = yeni(img.width, img.height)
    d = ImageDraw.Draw(k)
    d.ellipse([x - r, y - r, x + r, y + r], fill=hex2(renk))
    d.ellipse([x - r + int(r * 0.6), y - r - 1, x + r + int(r * 0.6), y + r - 1], fill=(0, 0, 0, 0))
    img.alpha_composite(k)


def _kanat_sehpasi(t, x, z, s):
    """Yeni figür: kanat sehpası: iki ayağı zemine basan ahşap askı; tepedeki kola bir çift kartal kanadı asılı."""
    d = ImageDraw.Draw(t)
    y = z[0]
    temas_golgesi(t, x, y, 12 * s)
    ust = y - int(15 * s)
    ah = hex2("#6a4428")
    for ax in (-5, 5):
        d.line([x + int(ax * s), y - 1, x + int(ax * 0.3 * s), ust], fill=ah, width=_u(0.7, s))
    d.line([x - int(4 * s), y - int(5 * s), x + int(4 * s), y - int(5 * s)], fill=ah, width=_u(0.5, s))
    d.rectangle([x - int(5 * s), ust - _u(0.8, s), x + int(5 * s), ust], fill=hex2("#8a5a34"))
    kanat(t, x - int(4 * s), ust, -1, -38, 8.0 * s, s)          # askıda yarı açık duran kanatlar
    kanat(t, x + int(4 * s), ust, 1, -38, 8.0 * s, s)


# ==========================================================================
# SAHNELER
# ==========================================================================
def _kule_tepesi(no, gok, deniz, tepe, sil, ust=600, cami=2):
    _gok(no, gok)
    _uzak_deniz(no, 520, 536, tepe, sil, deniz, no, cami=cami)
    _orta_duz(no, ust, TAS_SICAK, "tas", korkuluk=8)
    _on_bos(no)


def sahne370():
    """Kanca ve kapak: Galata Kulesi'nin şerefesinde kartal kanatlı Hezarfen; aşağıda Boğaz, karşıda Üsküdar (lodos sabahı)."""
    _kule_tepesi(370, SABAH, DENIZ_SABAH, ("#8a8aa4", "#7c7e98", "#70728c"), "#646884")
    p = P[370]
    s = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kanatli, p.w // 2, z, s, yon=1, acik=0.10 + 0.06 * (1 + SIN(f)), cirp=0.25 * SIN(f, 2))

    _cek(370, kare)


def sahne371():
    """'Aşağıda Boğaz. Karşıda Üsküdar.': şerefede sola çekilmiş Hezarfen sağa, Üsküdar'a bakar; kanatlar yarı açık."""
    _kule_tepesi(371, SABAH, DENIZ_SABAH, ("#8890a8", "#7a829c", "#6e7690"), "#5e6680", ust=606, cami=3)
    p = P[371]
    s = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kanatli, p.w // 2 - 34, z, s, yon=1, acik=0.40 + 0.08 * SIN(f), cirp=0.3 * SIN(f, 2))

    _cek(371, kare)


def _kosk_ic(no, pencere=("#5a8ab8", "#6e9cc8"), duvar=("#3a2e26", "#4a3a2e", "#5a4836"), cini="#2a6a8a", hali=True):
    """Köşk odası (iç mekân): kemerli duvar, çini kuşak, denize bakan pencereler, kilim."""
    ic_mekan(no, duvar=duvar, kemer="#2a1e16", cini=cini, pencere=pencere,
             zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"), isik="#f8c060", hali=hali)


def sahne372():
    """'Bu adam uçarsa padişah ona bir kese altın verecek.': köşk odasında minderde IV. Murad, önünde kese."""
    _kosk_ic(372)
    p = P[372]
    s = s_oturan(p.yk)

    def kare(t, z, i):
        f = i / KARE
        _kandil(t, 196, f, 372)
        mumluk(t, 292, z, f, 3)
        figur(t, oturan, 228, z, s, yon=-1, minder="#c8a040", **MURAD)
        figur(t, kese, 158, z, round(0.6 * s, 1))

    _cek(372, kare)


def sahne373():
    """'İstanbul, Dördüncü Murad'ın gençlik yılları.': genç IV. Murad atıyla Haliç kıyısında; karşıda kubbeler, minareler."""
    _gok(373, GUN)
    _uzak_deniz(373, 518, 536, ("#9aa2b4", "#8e96a8", "#828a9c"), "#727a92", DENIZ_GUN, 373, cami=3, minare=15)
    _orta_duz(373, 592, ["#b8aa8c", "#ac9e80", "#a09274", "#948668", "#887a5c"], "kaldirim")
    _on_bos(373)
    p = P[373]
    sa = 3.9            # atlı (at + binici) kadrajın ~%33'ü; sarık yazı bandının altında kalır (insan/at oranı at s=2.9 ↔ kisi 2.6)

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, p.w // 2, z, sa, 1, faz=f, at_renk="#ece6da", yele="#c8c0b0", adim=0.45, **MURAD)

    _cek(373, kare)


def sahne374():
    """'Adamın adı Ahmed Çelebi. Lakabı Hezarfen.': loş oda; Hezarfen ayakta, yanında sehpaya asılı kartal kanatları."""
    ic_mekan(374, duvar=("#2a2a30", "#363640", "#44424e"), kemer="#1a1a20", cini="#4a5a6a",
             pencere=("#2a3a5a", "#3a4a6a"), zemin_renk=("#4a4440", "#3e3834", "#322e2c"), isik="#e8b060", hali=False)
    p = P[374]
    s = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        _kandil(t, 200, f, 374)
        mumluk(t, 128, z, f, 2)
        _kanat_sehpasi(t, 242, z, round(0.85 * s, 1))
        figur(t, kisi, 170, z, s, yon=1, kol=0.03 * (1 + SIN(f)), **HEZARFEN)

    _cek(374, kare)


def sahne375():
    """Kurtuba, 9. yüzyıl, akşam: İbn Firnas sert iniş sonrası diz üstü; sol kanadı yere sarkmış, toz kalkar."""
    _gok(375, AKSAM)
    uzak(375, ["#7a5a6a", "#6a4e5e"], ["#8a6a5a", "#7a5e50"], ["#a07a58", "#906c4e", "#806044"], dag_y=(470, 500),
         tepe_y=510, ova_y=528)
    p = P[375]
    K = s_kisi(p.yk)
    _gorunur(375, [300], 270, 270, p.yk * 1.06)

    def ekle(img, z):
        figur(img, orta_asya_sehri, PAY + 200, PAY + 350, duz(588), 1.5, tohum=375, kerpic="#d8b888", golge="#a88a60",
              kubbe="#5a9a8a")                                    # Kurtuba (yaklaşık): kerpiç sur, kubbeler

    orta(375, (560, 566), ["#b08a5a", "#a07c50", "#906e46", "#80603c", "#705432"], "#d8b07a", ekle=ekle)
    on(375, ["#705432", "#80603c", "#906e46"], "#d8b07a", boy=110)

    def kare(t, z, i):
        f = i / KARE
        _toz(t, p.w // 2 - 22, p.h, f, K * 0.8, 6)
        _toz(t, p.w // 2 + 30, p.h, (f + 0.5) % 1, K * 0.7, 5)
        figur(t, kanatli, p.w // 2, z, K, yon=-1, acik=0.35, cirp=0.05 * SIN(f), diz=True, sol_dus=1.0, **FIRNAS)

    _cek(375, kare)


def sahne376():
    """Nişabur, 11. yüzyıl başı, kızıl akşam: sözlükçü Cevherî cami damında, kollarını açmış; yanında kubbe."""
    _gok(376, KIZIL_GOK)
    _uzak_kara(376, 530, 544, ("#6a3a4a", "#5e3442", "#522e3a"), "#4a2a36", ("#7a5a4a", "#6a4e40", "#5e4438"), 376,
               cami=1, minare=9, yogun=1.0, damlar="#9a7458")
    _orta_duz(376, 600, ["#a8805a", "#9c7650", "#906c48", "#846240", "#785838"], "dam", korkuluk=7)
    _on_bos(376)
    p = P[376]
    s = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        kx, ky, r = 122, z[0], int(4.4 * s)                      # damın üstündeki kubbe: kasnak dama oturur
        d.rectangle([kx - r - 3, ky - int(2.6 * s), kx + r + 3, ky - 1], fill=hex2("#b88a5e"))
        d.chord([kx - r, ky - int(2.6 * s) - r, kx + r, ky - int(2.6 * s) + r], 180, 360, fill=hex2("#3a8a9a"))
        d.line([kx, ky - int(2.6 * s) - r, kx, ky - int(2.6 * s) - r - _u(1.4, s)], fill=hex2("#e0b040"))
        temas_golgesi(t, kx, ky, 2 * r + 8)
        figur(t, kisi, 222, z, s, yon=1, kol=0.80 + 0.15 * SIN(f), pelerin="#3a2a4a", **CEVHERI)

    _cek(376, kare)


def sahne377():
    """Okmeydanı, gündüz: Hezarfen kanatları sırtında sağa yürür; geride açık alanda taş minber."""
    _gok(377, GUN)
    uzak(377, ["#7a8aa8", "#6e7e9c"], ["#7a9a72", "#6e8e68"], ["#8aa86a", "#7e9c60", "#729056"], dag_y=(470, 500),
         tepe_y=512, ova_y=530)
    p = P[377]
    s = s_kisi(p.yk)
    _gorunur(377, [300], p.x[0], p.x[1], p.yk * 1.06)

    def ekle(img, z):
        figur(img, agac, PAY + 120, duz(584), round(0.32 * s, 1), tohum=3)
        figur(img, tas_minber, PAY + 300, duz(588), round(0.85 * s, 1), yon=-1)

    orta(377, (560, 566), ["#8aa860", "#7e9c58", "#729050", "#668448", "#5a7840"], "#b8d088", ekle=ekle)
    on(377, ["#5a7840", "#668448", "#729050"], "#b8d088", boy=120)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kanatli, p.w // 2 - 20, z, s, yon=1, acik=0.0, adim=f)

    _cek(377, kare)


def sahne378():
    """Minberin üst sahanlığı: Hezarfen kanatlarını açıp kapar (talim); uzakta Haliç ve küçük Galata Kulesi."""
    _gok(378, GUN)
    _uzak_kara(378, 536, 548, ("#7a90a0", "#6e8496", "#62788a"), "#6a7a90", ("#8aa86a", "#7e9c60", "#729056"), 378,
               cami=1, minare=9, kule=300)
    _orta_duz(378, 604, ["#d0c4ac", "#c4b8a0", "#b8ac94", "#aca088", "#a0947c"], "tas", korkuluk=6)
    _on_bos(378)
    p = P[378]
    s = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kanatli, p.w // 2, z, s, yon=1, acik=0.55 - 0.42 * COS(f), cirp=0.2 * SIN(f, 2))

    _cek(378, kare)


def _galata_genis(no, gok, deniz, tepe, sil, zemin_renk, kenar, isik=False, gece=False, adam=True, yildiz=0, bugun=False):
    _gok(no, gok, yildiz=yildiz)
    _uzak_deniz(no, 520, 534, tepe, sil, deniz, no, cami=2, isik=isik)
    p = P[no]

    def ekle(img, z):
        if bugun:                                                     # bugün: surların yerinde çok katlı yapılar
            from timur_figur import koy_evleri
            figur(img, koy_evleri, PAY + 100, PAY + 440, duz(588), 1.6, tohum=no, kerpic="#c8a890")
        else:
            figur(img, sehir, PAY + 110, PAY + 430, duz(586), 0.9, duvar=_ac(zemin_renk[0], 0.1), golge=_ac(zemin_renk[0], -0.2),
                  cati="#8a3a2a" if not gece else "#3a2a30", tohum=no)

    _orta_duz(no, 562, list(zemin_renk), "kaldirim", ekle=ekle, kenar=kenar)
    _on_bos(no)
    sk = 2.8

    def kare(t, z, i):
        f = i / KARE
        cx = p.w // 2
        for ex, dx in ((cx - 46, 2.3), (cx + 50, 2.2)):
            baca = figur(t, ev, ex, z, dx, duvar="#c8a878" if not gece else "#5a4a44", cati="#a8452e" if not gece else "#4a2a2a",
                         isik=isik)
            if not bugun:                                              # ocak dumanı lodosla sağa yatar
                duman(t, baca[0], baca[1], 30, no + ex, faz=f, renk="#d8d2c8" if not gece else "#6a6670", ruzgar=0.9, genislik=0.7)
        serefe, a, b = figur(t, galata_kulesi, cx, z, sk, isik=isik)
        if adam:                                                       # şerefede kanatlı adam (uzaktan, küçük)
            figur(t, kanatli, b - 3, duz(serefe, t.width), 0.62, yon=1, acik=0.9, cirp=0.3 * SIN(f, 2))
        if bugun:
            d = ImageDraw.Draw(t)
            for lx in (cx - 74, cx + 76):                            # bugünkü sokak lambaları (direk zemine dikili)
                d.line([lx, z[0] - 1, lx, z[0] - 26], fill=hex2("#2a2a30"), width=2)
                d.line([lx, z[0] - 26, lx + 5, z[0] - 26], fill=hex2("#2a2a30"))
                d.rectangle([lx + 4, z[0] - 26, lx + 7, z[0] - 23], fill=hex2("#ffe8a0"))
                temas_golgesi(t, lx, z[0], 5)

    _cek(no, kare)


def sahne379():
    """'Sonra kule... altmış yedi metre. Lodos esiyor.': Galata Kulesi geniş çekim; şerefede küçük kanatlı adam, bacalardan
    çıkan duman lodosla sağa yatar."""
    _galata_genis(379, SABAH, DENIZ_SABAH, ("#8a8aa4", "#7c7e98", "#70728c"), "#646884",
                  ["#a89a7a", "#9c8e70", "#908266", "#84765c", "#786a52"], "#d0c098")


def sahne380():
    """Sarayburnu, Sinan Paşa Köşkü'nün taşlığı: minderde oturan IV. Murad sola, Haliç'in karşısındaki Galata'ya bakar."""
    _gok(380, SABAH)
    _uzak_deniz(380, 520, 536, ("#8a8aa4", "#7c7e98", "#70728c"), "#646884", DENIZ_SABAH, 380, cami=1, kule=222)
    _orta_duz(380, 598, TAS_SICAK, "tas", korkuluk=8)
    _on_bos(380)
    p = P[380]
    s = s_oturan(p.yk)
    _gorunur(380, [222], 270, 270, p.yk * 1.06)

    def kare(t, z, i):
        f = i / KARE
        figur(t, oturan, p.w // 2 + 20, z, s, yon=-1, minder="#c8a040", **MURAD)

    _cek(380, kare)


def sahne381():
    """'Adam atlıyor... Boğaz'ın üstünde süzülüyor.': kanatları açık Hezarfen lodosla sağa, Üsküdar'a süzülür.
    Bu sahnede figürün havada olması doğrudur (süzülme); altında deniz, gölge yok."""
    _gok(381, SABAH)
    _uzak_deniz(381, 520, 534, ("#8a8aa4", "#7c7e98", "#70728c"), "#646884", DENIZ_SABAH, 381, cami=3)
    _orta_deniz(381, 552, ("#3e628a", "#34567c", "#2c4c70", "#264466"))
    _on_bos(381)
    p = P[381]
    s = s_kisi(p.yk, 0.28)            # açık kanatlar kadraja sığsın diye (gövde ölçeği diğer sahnelere yakın)
    su = p.h - 14

    def kare(t, z, i):
        f = i / KARE
        _su_bandi(t, su, 552, p.taban - p.h, ("#3e628a", "#34567c", "#2c4c70", "#264466"))   # orta plandaki denizle aynı
        ayak = su - 36 + int(round(3 * SIN(f)))
        figur(t, kanatli, p.w // 2, duz(ayak, t.width), s, yon=1, acik=0.85, cirp=0.25 * SIN(f), havada=True)

    _cek(381, kare, esik=0.5)


def sahne382():
    """Üsküdar, Doğancılar Meydanı: Hezarfen'in ayakları yere değer; kanatlar iner, ayak dibinden toz kalkar."""
    _gok(382, SABAH)
    _uzak_kara(382, 528, 546, ("#8a90a4", "#7e8498", "#72788c"), "#6a7088", ("#a0a088", "#949480", "#888876"), 382,
               cami=1, minare=10)
    p = P[382]
    s = s_kisi(p.yk)

    def ekle(img, z):
        for x, dx in ((186, 3.0), (222, 3.2), (352, 3.0)):
            figur(img, ev, PAY + x, duz(588), dx)
        figur(img, kubbeli_cami, PAY + 312, duz(588), 2.0, minare=1)

    _orta_duz(382, 572, ["#c0b090", "#b4a484", "#a89878", "#9c8c6c", "#908060"], "kaldirim", ekle=ekle)
    _on_bos(382)

    def kare(t, z, i):
        f = i / KARE
        _toz(t, p.w // 2 - 10, p.h, f, s * 0.8, 6)
        _toz(t, p.w // 2 + 12, p.h, (f + 0.33) % 1, s * 0.7, 5)
        figur(t, kanatli, p.w // 2, z, s, yon=1, acik=0.62 + 0.28 * COS(f), cirp=0.1 * SIN(f, 2), adim=0.22)

    _cek(382, kare)


def sahne383():
    """'Padişah ödülünü veriyor: bir kese altın.': köşk odası; minderde IV. Murad, karşısında diz çökmüş Hezarfen, arada kese."""
    _kosk_ic(383)
    p = P[383]
    so, sk = s_oturan(p.yk), s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        _kandil(t, 200, f, 383)
        figur(t, oturan, 150, z, so, yon=1, minder="#c8a040", **MURAD)
        figur(t, kese, 204, z, round(0.6 * so, 1))
        figur(t, kisi, 252, z, sk, yon=-1, diz=True, kol=0.10 + 0.04 * SIN(f), **HEZARFEN)

    _cek(383, kare)


def sahne384():
    """'Ve aynı nefeste hükmünü söylüyor': aynı oda kızıl akşamda; IV. Murad ayağa kalkmış, eliyle gösterir; Hezarfen diz üstü."""
    _kosk_ic(384, pencere=("#a8484a", "#b85a54"), duvar=("#2e2020", "#3c2a28", "#4a3430"), cini="#6a2a2a")
    p = P[384]
    sk = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        _kandil(t, 206, f, 384)
        figur(t, kisi, 156, z, sk, yon=1, kol=0.70 + 0.05 * SIN(f), pelerin="#4a1018", **MURAD)
        figur(t, kese, 224, z, round(0.55 * sk, 1))
        figur(t, kisi, 262, z, sk, yon=-1, diz=True, **HEZARFEN)

    _cek(384, kare)


def sahne385():
    """'Cezayir... Hezarfen oraya gönderiliyor.': alacakaranlıkta kadırga batıya (sola), sürgüne yol alır."""
    _gok(385, AKSAM)
    _uzak_deniz(385, 528, 540, ("#5a4a6a", "#4e4260", "#443a56"), "#3e3654", DENIZ_AKSAM, 385, cami=0)
    _orta_deniz(385, 556, ("#3e3660", "#363058", "#2e2a50", "#282448"))
    _on_bos(385)
    p = P[385]
    sg = 3.4
    su = p.h - 14

    def kare(t, z, i):
        f = i / KARE
        figur(t, gemi, p.w // 2, su, sg, -1, f, govde="#3a2a22", yelken="#e8dcc0", hac=False)
        _su_bandi(t, su, 556, p.taban - p.h, ("#3e3660", "#363058", "#2e2a50", "#282448"))

    _cek(385, kare, esik=0.4)


def _cezayir_evleri(t, x0, x1, z, s, f, tohum):
    """Cezayir'in beyaz, düz damlı kübik evleri (yeni figür; düz zemine oturur); bazı pencerelerde titreyen kandil ışığı."""
    d = ImageDraw.Draw(t)
    rnd = random.Random(tohum)
    x = x0
    while x < x1:
        w = int(rnd.uniform(9, 15) * s)
        h = int(rnd.uniform(8, 16) * s)
        y = duz_zemin(z, x, x + w, "Cezayir evi", tolerans=3)
        renk = _ac("#d8d8e4", rnd.uniform(-0.45, -0.3))
        d.rectangle([x, y - h, x + w, y - 1], fill=hex2(renk))
        d.line([x, y - h, x + w, y - h], fill=hex2(_ac(renk, 0.25)))
        d.rectangle([x + w // 2 - _u(1, s), y - int(3.4 * s), x + w // 2 + _u(1, s), y - 1], fill=hex2("#1a1a2a"))
        yan = (k for k in range(3))
        for k in yan:
            if rnd.random() < 0.55:
                wx, wy = x + int((1.5 + k * 3.6) * s), y - h + int(2.4 * s)
                if wx + _u(1.4, s) < x + w:
                    yanik = rnd.random() < 0.6
                    titre = 0.15 * SIN(f + rnd.random(), 1)
                    d.rectangle([wx, wy, wx + _u(1.4, s), wy + _u(1.8, s)],
                                fill=hex2(_ac("#f0b850", titre) if yanik else "#1e1e2e"))
        temas_golgesi(t, x + w // 2, y, w, alfa=80)
        x += w + int(rnd.uniform(0, 2) * s)


def sahne386():
    """'Hakkında bilinen son söz üç kelime: Orada merhum oldu.': Cezayir'de gece; beyaz evler, hilal. İnsan yok, mezar yok."""
    img = _gok(386, GECE, yildiz=110)
    _hilal(img, 196, 524, 9)
    kaydet(img, "sahne386-gokyuzu.png")
    _uzak_kara(386, 540, 556, ("#1e2440", "#1a2038", "#161c30"), None, ("#1e2230", "#1a1e2a", "#161a24"), 386)
    _orta_duz(386, 566, ["#2a2a36", "#24242e", "#1e1e28", "#1a1a22", "#16161c"], "dam")
    _on_bos(386)
    p = P[386]

    def kare(t, z, i):
        f = i / KARE
        _cezayir_evleri(t, 104, 300, z, 3.4, f, 386)
        figur(t, kubbeli_cami, 214, z, 2.6, tas="#9a9aa8", kursun="#5a6070", minare=1, isik=True)

    _cek(386, kare)


def sahne387():
    """'Kalması uygun değildi. Kalmadı.': gece Galata Kulesi; şerefe boş, pencerelerde ışık."""
    _galata_genis(387, GECE, DENIZ_GECE, ("#1e2440", "#1a2038", "#161c30"), "#141a2e",
                  ["#3a3644", "#34303e", "#2e2a38", "#282432", "#221e2c"], "#5a5468", isik=True, gece=True, adam=False,
                  yildiz=90)


def _kahire_odasi(no, pencere=("#1a2a4a", "#3a4a70")):
    ic_mekan(no, duvar=("#3a2c22", "#4a382a", "#5a4632"), kemer="#2a1c14", cini="#3a7a5a", pencere=pencere,
             zemin_renk=("#5a4838", "#4a3c2e", "#3e3226"), isik="#f8c060", hali=True)


def sahne388():
    """'Tek bir adam: Evliya Çelebi.': Kahire'de yaşlı Evliya ayakta, elinde defter; mum ve kandil."""
    _kahire_odasi(388)
    p = P[388]
    s = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        _kandil(t, 270, f, 388)
        mumluk(t, 128, z, f, 3)
        figur(t, kisi, 200, z, s, yon=1, silah="mektup", kol=0.30 + 0.05 * SIN(f), **EVLIYA)

    _cek(388, kare)


def sahne389():
    """'Kahire'de, yaşlı bir adam.': Evliya minderde oturur, rahlede yazar; yanında kitap yığını."""
    _kahire_odasi(389)
    p = P[389]
    s = s_oturan(p.yk)

    def kare(t, z, i):
        f = i / KARE
        _kandil(t, 200, f, 389)
        mumluk(t, 290, z, f, 3)
        kitaplar(t, 116, z[0], round(0.9 * s, 1))
        figur(t, oturan, 180, z, s, yon=1, minder="#8a2a2a", **EVLIYA)
        rahle(t, 180 + int(5.4 * s), z[0], round(0.9 * s, 1))

    _cek(389, kare)


def sahne390():
    """'Başka hiçbir Osmanlı kroniği...': loş kütüphane; sedirde kitap yığınları, kapalı sandık, rulo mektuplar. İnsan yok."""
    _kahire_odasi(390, pencere=None)
    p = P[390]
    s = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        _kandil(t, 200, f, 390)
        ust = figur(t, sedir, 150, z, round(0.5 * s, 1), renk="#6a4a2a", ortu="#5a2a2a")
        for kx in (124, 140, 156, 172):
            kitaplar(t, kx, ust, round(0.55 * s, 1))
        y = z[0]                                                     # kapalı sandık: zemine oturur
        temas_golgesi(t, 262, y, int(9 * s))
        d.rectangle([262 - int(4.4 * s), y - int(5 * s), 262 + int(4.4 * s), y - 1], fill=hex2("#5a3a22"), outline=hex2("#2a1a10"))
        d.rectangle([262 - int(4.4 * s), y - int(5.6 * s), 262 + int(4.4 * s), y - int(4.6 * s)], fill=hex2("#6a4a2a"))
        for bx in (-3, 3):
            d.line([262 + int(bx * s), y - int(5.6 * s), 262 + int(bx * s), y - 1], fill=hex2("#c8a040"))
        for k, rx in enumerate((206, 224)):                           # rulo mektuplar: yere yatık
            d.ellipse([rx - int(1.8 * s), y - int(1.6 * s) - 1, rx + int(1.8 * s), y - 1], fill=hex2("#e8dcc0"))
            d.ellipse([rx + int(1.2 * s), y - int(1.6 * s) - 1, rx + int(2 * s), y - 1], fill=hex2("#c8b890"))
            piksel(t, rx, y - int(0.8 * s), hex2("#c8302a"))

    _cek(390, kare)


def _sarayburnu_gece(no, kosk_x=None):
    _gok(no, GECE, yildiz=110)
    _uzak_deniz(no, 524, 538, ("#1e2440", "#1a2038", "#161c30"), "#141a2e", DENIZ_GECE, no, cami=2, isik=True)

    def ekle(img, z):
        if kosk_x is not None:
            figur(img, kosk, PAY + kosk_x, duz(592), 2.6, isik=True, tas="#6a6474", ahsap="#4a3a34", kursun="#3a4250")

    _orta_duz(no, 586 if kosk_x is not None else 598, TAS_GECE, "tas", korkuluk=0 if kosk_x is not None else 8, ekle=ekle)
    _on_bos(no)


def sahne391():
    """'Lagari Hasan Çelebi. Fişekçi.': gece Sarayburnu'nda Lagari fişeğinin yanında; şenlik feneri."""
    _sarayburnu_gece(391)
    p = P[391]
    s = s_kisi(p.yk)
    sf = 5.0

    def kare(t, z, i):
        f = i / KARE
        figur(t, fisek, 236, z, sf)
        figur(t, kisi, 160, z, s, yon=1, kol=0.25 + 0.05 * SIN(f), **LAGARI)

    _cek(391, kare)


def sahne392():
    """'Kaya Sultan'ın doğduğu gece. Sarayburnu'nda şenlik.': ışıklı köşk, fenerler; fişekçi meşaleyle küçük fişekleri
    ateşler: fişekler sehpadan yükselir (kıvılcım kuyruğu sehpaya iner) ve alçakta patlar, kıvılcımlar yerçekimiyle düşer."""
    _sarayburnu_gece(392, kosk_x=205)
    p = P[392]
    s = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        y = z[0]
        figur(t, fener, 112, z, round(0.55 * s, 1), f=f)
        figur(t, fener, 286, z, round(0.55 * s, 1), f=(f + 0.4) % 1)
        rx = 238                                                         # fişek sehpası (zemine basar)
        d.line([rx - 9, y - 1, rx - 2, y - 18], fill=hex2("#6a4428"), width=2)
        d.line([rx + 9, y - 1, rx + 2, y - 18], fill=hex2("#6a4428"), width=2)
        d.rectangle([rx - 6, y - 20, rx + 6, y - 18], fill=hex2("#8a5a34"))
        temas_golgesi(t, rx, y, 20)
        for k in range(3):
            ph = (f + k / 3) % 1
            hx, cy = (196, 236, 276)[k], y - (70, 80, 66)[k]
            if ph < 0.35:                                                # yükselen fişek
                q = ph / 0.35
                fx, fy = rx + (hx - rx) * q, y - 20 - (y - 20 - cy) * q
                d.line([rx, y - 20, fx, fy], fill=hex2("#f8d070", 110))
                d.rectangle([fx - 1, fy - 4, fx + 1, fy], fill=hex2("#e8601c"))
                piksel(t, fx, fy - 5, hex2("#fff0a0"))
            else:                                                        # patlama: kıvılcımlar açılır, düşer ve söner
                q = (ph - 0.35) / 0.65
                renk = ("#ffd479", "#ffa486", "#b8e8ff")[k]
                for a in range(0, 360, 20):
                    for r0 in (1.0, 0.6):
                        r = (4 + q * 24) * r0
                        px_ = hx + math.cos(math.radians(a + k * 10)) * r
                        py_ = cy + math.sin(math.radians(a + k * 10)) * r + q * q * 16
                        if py_ < y - 2:
                            al = int(255 * (1 - q * 0.8))
                            d.rectangle([px_, py_, px_ + 1, py_ + 1], fill=hex2(renk, al))
        figur(t, kisi, 176, z, round(0.95 * s, 1), yon=1, silah="mesale", kol=0.0, **LAGARI)

    _cek(392, kare)


def sahne393():
    """'Yedi kollu bir fişek. İçinde altmış dört kilo kadar barut macunu.': fişek yakın plan; yanında barut fıçıları."""
    _sarayburnu_gece(393)
    p = P[393]
    s = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, fener, 290, z, round(0.6 * s, 1), f=f)
        for fx, fs in ((112, 0.8), (140, 0.85), (125, 0.0)):
            if fs:
                figur(t, fici, fx, z, round(fs * s, 1))
        figur(t, fisek, 210, z, 4.9)

    _cek(393, kare)


def _lagari_fisekte(t, x, z, f, sf, so, kalk=0, alev=0.0, kol=True):
    """Lagari fişeğin oturağında bağdaş kurmuş (oturak fişeğin üstünde: figür ona basar); bir kolu padişaha kalkık."""
    zz = duz(z[0] - kalk, t.width)
    oturak = figur(t, fisek, x, zz, sf, alev=alev, kalin=1.6)
    figur(t, oturan, x, duz(oturak, t.width), so, yon=-1, **LAGARI)
    if kol:
        d = ImageDraw.Draw(t)
        oy = oturak - int(9 * so)
        el = (x - int(4 * so), oy - int(3 * so) - int(1.2 * so * (1 + SIN(f))))
        d.line([x - int(1 * so), oy + int(1 * so), *el], fill=hex2(_ac(LAGARI["govde"], -0.3)), width=_u(1, so))
        piksel(t, el[0], el[1], hex2("#e8b890"))


def sahne394():
    """'Lagari fişeğe biniyor ve padişaha sesleniyor': Lagari fişeğin tepesinde, kolunu soldaki ışıklı köşke kaldırır."""
    _sarayburnu_gece(394, kosk_x=200)
    p = P[394]
    _gorunur(394, [200], 270, 270, p.yk * 1.06, pay=0)

    def kare(t, z, i):
        f = i / KARE
        figur(t, fener, 122, z, 3.0, f=f)
        _lagari_fisekte(t, 236, z, f, 3.2, 3.2)

    _cek(394, kare)


def sahne395():
    """'Fişek ateşleniyor. Göğe yükseliyor.': fitil yanar, dipten alev ve duman; fişek Lagari ile yükselip kadrajdan çıkar,
    sehpada yalnız duman kalır. (Yükselen fişeğin yazı bandından geçmesi bilinçli: 1 sn'lik hareket.)"""
    _sarayburnu_gece(395, kosk_x=200)
    p = P[395]

    def kare(t, z, i):
        f = i / KARE
        x = 236
        figur(t, fener, 122, z, 3.0, f=f)
        if f < 0.4:
            _lagari_fisekte(t, x, z, f, 3.2, 3.2, alev=0.3 + f * 1.6, kol=False)
        else:
            figur(t, fisek_sehpa, x, z, 3.2, kalin=1.6)
            if f < 0.8:
                kalk = int(((f - 0.4) / 0.4) ** 1.6 * 330)
                k = yeni(t.width, t.height + 400)
                _lagari_fisekte(k, x, duz(z[0] + 400, t.width), f, 3.2, 3.2, kalk=kalk, alev=1.0, kol=False)
                t.alpha_composite(k.crop((0, 400, t.width, t.height + 400)))
        for j in range(3):                                               # duman: sehpanın dibinden yükselir
            duman(t, x - 10 + j * 10, z[0] - 4, 60, 395 + j, faz=(f + j * 0.3) % 1, renk="#8a8694", ruzgar=0.3, genislik=1.2)

    _cek(395, kare, esik=0.5, serbest=6000)


def fisek_sehpa(img, x, zemin, s=1.0, kalin=1.0):
    """Fişek kalktıktan sonra boş kalan ahşap sehpa (fisek'in ayakları ve halkası; zemine basar)."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(6 * s), x + int(6 * s), "fişek sehpası", tolerans=max(3, int(s)))
    temas_golgesi(img, x, y, 13 * s)
    ah = hex2("#6a4428")
    halka = y - int(7 * s)
    for ax in (-6, -2.5, 2.5, 6):
        d.line([x + int(ax * s), y - 1, x + int(ax * 0.45 * s), halka], fill=ah, width=_u(0.8, s))
    d.line([x - int(5 * s), y - int(2.5 * s), x + int(5 * s), y - int(2.5 * s)], fill=ah, width=_u(0.5, s))
    d.rectangle([x - int(3.6 * s * max(1.0, kalin * 0.8)), halka - _u(0.8, s), x + int(3.6 * s * max(1.0, kalin * 0.8)), halka],
                fill=hex2("#5a3a22"))
    for k in range(int(6 * s)):                                          # isli kenar
        piksel(img, x - int(3 * s) + k, halka - _u(0.8, s), hex2("#2a2420"))


def sahne396():
    """'Lagari denize iniyor. Yüzerek padişahın önüne geliyor.': gece denizi; sağda düşüşün köpüklü halkası, Lagari sola,
    ışıklı kıyıya yüzer."""
    _gok(396, GECE, yildiz=110)
    _uzak_deniz(396, 524, 538, ("#1e2440", "#1a2038", "#161c30"), "#141a2e", DENIZ_GECE, 396, cami=1, isik=True)
    _orta_deniz(396, 552, ("#16223e", "#121c34", "#0e182c", "#0c1426"))
    _on_bos(396)
    p = P[396]
    s = s_kisi(p.yk) * 1.3
    su = p.h - 30

    def kare(t, z, i):
        f = i / KARE
        _su_bandi(t, su, 552, p.taban - p.h, ("#16223e", "#121c34", "#0e182c", "#0c1426"))
        hx = 256                                                         # düştüğü yer: genişleyen köpük halkası
        for k in range(2):
            r = 6 + ((f + k * 0.5) % 1) * 40
            for a in range(0, 360, 6):
                px_ = hx + math.cos(math.radians(a)) * r
                py_ = su + 1 + math.sin(math.radians(a)) * r * 0.18
                if py_ >= su:
                    piksel(t, px_, py_, hex2("#c8dcec", int(200 * (1 - ((f + k * 0.5) % 1)))))
        yuzen(t, 168, su, round(s, 1), -1, f)

    _cek(396, kare, esik=0.4)


def sahne397():
    """'Ona da bir kese akçe. Ve sipahilik. Sürgün yok.': gece köşk odası; ıslak Lagari diz üstü, IV. Murad minderde, arada kese."""
    _kosk_ic(397, pencere=("#14203a", "#e8e0b0"))
    p = P[397]
    so, sk = s_oturan(p.yk), s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        _kandil(t, 200, f, 397)
        mumluk(t, 320, z, f, 3)
        figur(t, oturan, 150, z, so, yon=1, minder="#c8a040", **MURAD)
        figur(t, kese, 204, z, round(0.6 * so, 1), renk="#3a4a6a", sikke="#d8d8e0")
        figur(t, kisi, 254, z, sk, yon=-1, diz=True, govde="#4a3418", bas=None, bas_renk="#2a1a12", sakal="#2a1a12")
        if i % 6 < 3:                                                    # ıslak: elbiseden damla
            piksel(t, 258, z[0] - int(2 * sk) + (i % 6), hex2("#a8c8e8"))

    _cek(397, kare)


def sahne398():
    """'İki uçan adam. Biri sipahi oluyor. Öteki Cezayir'e yollanıyor.': solda kalkanlı sipahi Lagari (sola bakar),
    sağda kanatları sırtında Hezarfen sağa, uzaktaki gemiye bakar."""
    _gok(398, AKSAM)
    _uzak_deniz(398, 520, 534, ("#5a4a6a", "#4e4260", "#443a56"), "#3e3654", DENIZ_AKSAM, 398, cami=1, gemi_x=352)
    _orta_duz(398, 598, ["#8a7a7a", "#7e6e70", "#726466", "#665a5c", "#5a5052"], "tas", korkuluk=7)
    _on_bos(398)
    p = P[398]
    s = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 160, z, s, yon=-1, silah="kalkan", kol=0.02 * (1 + SIN(f)), govde="#a8281e", bas="sarik",
              bas_renk="#f4f0e6", sakal="#2a1a12", pelerin="#e0b040")
        figur(t, kanatli, 252, z, s, yon=1, acik=0.0, cirp=0.1 * SIN(f))

    _cek(398, kare)


def sahne399():
    """'İki bin dokuzda Discovery ekibi fişeği yeniden yapıyor. Fişek parçalanıyor.': çöl deney alanı, gündüz. Fitil yanar,
    fişek sehpadan az kalkar ve alçakta parçalanır; parçalar yere düşer, manken sehpanın dibinde kalır (havalanmaz).
    Sağda beton bariyer arkasında kameralı iki kişilik ekip."""
    _gok(399, GUN)
    uzak(399, ["#c0a080", "#b09474"], ["#c8a884", "#b89a78"], ["#d8c098", "#ccb48c", "#c0a880"], dag_y=(480, 506),
         tepe_y=516, ova_y=532)
    _orta_duz(399, 572, ["#dcc8a0", "#d0bc94", "#c4b088", "#b8a47c", "#ac9870"], "dam")
    _on_bos(399)
    p = P[399]
    s = s_kisi(p.yk) * 0.9
    sf = 3.0
    rnd = random.Random(399)
    parcalar = [(rnd.uniform(-1, 1), rnd.uniform(0.4, 1.0), rnd.choice(("#a8301e", "#e0b040", "#6a4428"))) for _ in range(14)]

    def kare(t, z, i):
        f = i / KARE
        x = 168
        y = z[0]
        arka = duz(y - 10, t.width)
        for j, kx in enumerate((262, 294)):                             # ekip: bariyerin arkasında (bir sıra geride)
            figur(t, kisi, kx, arka, round(0.85 * s, 1), yon=-1, silah="kamera" if j == 0 else None, kol=0.2 if j else 0.0,
                  govde="#2a3a5a" if j else "#5a5a52", bas="kasket", bas_renk="#2a2a30", sakal=None, kemer=None)
        figur(t, beton_set, 238, 312, z, 3.0)
        if f < 0.3:                                                      # ateşleme: sehpada fişek ve oturan manken
            ot = figur(t, fisek, x, z, sf, alev=0.3 + f * 2.2)
            figur(t, manken, x, duz(ot, t.width), 3.4, yon=1)
        elif f < 0.5:                                                    # alçakta kalkış ve parçalanma
            q = (f - 0.3) / 0.2
            figur(t, fisek_sehpa, x, z, sf)
            figur(t, manken, x - 22, z, 3.4, yatik=True)
            cy = y - int(16 * sf) - int(q * 14)
            for k, (yx, hz_, renk) in enumerate(parcalar):
                px_ = x + yx * q * 60
                py_ = cy - hz_ * 30 * q + 90 * q * q
                if py_ < y - 1:
                    ImageDraw.Draw(t).rectangle([px_ - 2, py_ - 1, px_ + 2, py_ + 1], fill=hex2(renk))
            for a in range(0, 360, 20):
                r = 4 + q * 26
                piksel(t, x + math.cos(math.radians(a)) * r, cy + math.sin(math.radians(a)) * r, hex2("#ffd479", int(240 * (1 - q))))
        else:                                                            # parçalar yerde, duman yükselir
            figur(t, fisek_sehpa, x, z, sf)
            figur(t, manken, x - 22, z, 3.4, yatik=True)
            d = ImageDraw.Draw(t)
            for k, (yx, hz_, renk) in enumerate(parcalar):
                px_ = x + yx * 60
                d.rectangle([px_ - 2, y - 3, px_ + 2, y - 1], fill=hex2(renk))
        for j in range(2):
            duman(t, x - 6 + j * 12, y - 6, 60, 399 + j, faz=(f + j * 0.5) % 1, renk="#bab4aa", ruzgar=0.4, genislik=1.1)

    _cek(399, kare)


def _tartisma_odasi(no):
    ic_mekan(no, duvar=("#2e2a26", "#3a3530", "#48423a"), kemer="#1e1a16", cini="#5a4a3a",
             pencere=("#2a3a5a", "#3a4a6a"), zemin_renk=("#4e443a", "#433a32", "#38302a"), isik="#f8c060", hali=False)


SOL_HOCA = dict(govde="#3a3a48", bas="kalpak", bas_renk="#5a5a60", sakal="#8a8a8e")     # "rivayet" diyen
SAG_HOCA = dict(govde="#6a4a2a", bas="kalpak", bas_renk="#2a1a12", sakal="#2a1a12")     # "erken havacılık" diyen


def _tartisma(no, konusan):
    _tartisma_odasi(no)
    p = P[no]
    s = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        _kandil(t, 200, f, no)
        ust = figur(t, sedir, 200, z, round(0.22 * s, 1), renk="#5a3a22", ortu="#4a2a2a")
        kitaplar(t, 190, ust, round(0.5 * s, 1))
        kitaplar(t, 212, ust, round(0.45 * s, 1))
        mumluk(t, 118 if konusan == "sol" else 284, z, f, 3)          # konuşanın yanında mum: ışık konuşandadır
        figur(t, kisi, 140, z, s, yon=1, silah="mektup", kol=(0.78 + 0.12 * SIN(f, 2)) if konusan == "sol" else 0.0,
              **SOL_HOCA)
        figur(t, kisi, 262, z, s, yon=-1, silah="mektup", kol=(0.78 + 0.12 * SIN(f, 2)) if konusan == "sag" else 0.0,
              **SAG_HOCA)

    _cek(no, kare)


def sahne400():
    """'Rivayet diyenler...': iki taraf karşı karşıya; soldaki konuşur, elindeki kitabı kaldırır."""
    _tartisma(400, "sol")


def sahne401():
    """'Erken havacılık diyenler...': aynı oda; bu kez sağdaki konuşur."""
    _tartisma(401, "sag")


def sahne402():
    """'Kaynaklar ayrışıyor. Biz karar vermiyoruz.': terazinin kefelerinde bir kitap ve bir kartal tüyü; kol hafifçe salınır."""
    _tartisma_odasi(402)
    p = P[402]
    s = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        _kandil(t, 200, f, 402)
        mumluk(t, 300, z, f, 3)
        mumluk(t, 100, z, (f + 0.5) % 1, 3)
        figur(t, terazi, 200, z, round(0.95 * s, 1), egim=0.03 * SIN(f))

    _cek(402, kare)


def sahne403():
    """'Bugün Çatalca'da onun adını taşıyan bir havaalanı var.': çimenlik pistte küçük eğitim uçağı sağa ilerler, pervane döner;
    geride hangar ve rüzgâr tulumu."""
    _gok(403, GUN, bulutlar=[(130, 300, 24)])
    uzak(403, ["#8a9ab0", "#7e8ea6"], ["#7a9a72", "#6e8e68"], ["#8aa86a", "#7e9c60", "#729056"], dag_y=(480, 508),
         tepe_y=516, ova_y=530)
    p = P[403]

    def ekle(img, z):
        figur(img, hangar, PAY + 120, PAY + 230, duz(574), 2.2)
        figur(img, ruzgar_tulumu, PAY + 282, duz(576), 2.6, f=0.2)

    _orta_duz(403, 562, ["#7e9c58", "#729050", "#668448", "#5a7840", "#4e6c38"], "pist", ekle=ekle)
    _on_bos(403)
    su = 5.6

    def kare(t, z, i):
        f = i / KARE
        figur(t, ucak, p.w // 2, z, su, 1, f=f)

    _cek(403, kare)


def sahne404():
    """'Bir sinema filmi var: İstanbul Kanatlarımın Altında.': karanlık salon; perdede kule ve süzülen adam, önde koltuklar."""
    ic_mekan(404, duvar=("#14121a", "#1c1a24", "#24222e"), kemer="#0e0c12", cini="#2a1e2e", pencere=None,
             zemin_renk=("#2a2228", "#241e22", "#1e181c"), isik="#f8c060", hali=False)
    p = P[404]
    s = s_kisi(p.yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, perde, 200, duz(z[0] - 16, t.width), round(0.62 * s, 1), f=f)
        figur(t, koltuk_sirasi, 96, 306, z, round(0.6 * s, 1), bas=(146, 236))

    _cek(404, kare)


def sahne405():
    """'Padişah demişti... Neredeyse dört yüz yıl kaldı.': bugün, gün batımında Galata Kulesi; sokak lambaları yanar."""
    _galata_genis(405, AKSAM, DENIZ_AKSAM, ("#5a4a6a", "#4e4260", "#443a56"), "#3e3654",
                  ["#8a7a72", "#7e6e68", "#72625e", "#665854", "#5a4e4a"], "#c8a890", isik=True, adam=False, bugun=True)


def sahne406():
    """'Siz olsanız ona altın mı verirdiniz, sürgün mü?': Üsküdar kıyısında gün batımı; Hezarfen kanatları sırtında sola,
    karşıdaki Galata'ya bakar; yanında kese, uzakta sürgün gemisi."""
    _gok(406, AKSAM)
    _uzak_deniz(406, 520, 536, ("#5a4a6a", "#4e4260", "#443a56"), "#3e3654", DENIZ_AKSAM, 406, cami=2, kule=200, gemi_x=340)
    _orta_duz(406, 600, ["#9a8a7a", "#8e7e70", "#827266", "#76665c", "#6a5a52"], "tas", korkuluk=7)
    _on_bos(406)
    p = P[406]
    s = s_kisi(p.yk)
    _gorunur(406, [200], 270, 270, p.yk * 1.06)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kanatli, p.w // 2 + 16, z, s, yon=-1, acik=0.05 + 0.04 * (1 + SIN(f)), cirp=0.2 * SIN(f, 2))
        figur(t, kese, p.w // 2 - 50, z, round(0.6 * s, 1))

    _cek(406, kare)


SAHNELER = {n: globals()[f"sahne{n}"] for n in range(370, 407)}

if __name__ == "__main__":
    for n in ([int(a) for a in sys.argv[1:]] or sorted(SAHNELER)):
        SAHNELER[n]()
        print(f"sahne{n} tamam")
