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
from ciz import arazi, bulut  # noqa: E402
from sahneler import duz, gokyuzu, kaydet, on, orta, sprite, uzak  # noqa: E402
from timur_figur import _baslik, at, gemi, kisi, koy_evleri, oturan, sedir  # noqa: E402
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


def yazi_alti(yakin, taban, satir=3):
    """Kartın alt kenarının dünya y'si (odakY = taban-12). Ekranda yazı ızgara y 150'den başlar, satır başına ~52."""
    ekran = {1: 201, 2: 253, 3: 305}[satir]
    o = taban - 12
    return o + (ekran - o) / yakin


def _kadraj(no, kare, w, h, yakin, esik, taban, yazi_satir=3, serbest=0):
    """Görünür aralık yerel x = w/2 ± 270/yakin: opak piksellerin en az `esik` oranı içeride olmalı; figür sprite'ın
    üstüne değmemeli (kesik baş). Yazı denetimi: görünür aralıkta, kartın altından yukarıda kalan opak piksel sayısı
    `serbest`'i aşmamalı (kandil zinciri gibi bilinçli istisnalar için serbest verilir)."""
    yarim = 270 / yakin
    a, b = max(int(w / 2 - yarim), 0), min(int(w / 2 + yarim), w)
    sinir = yazi_alti(yakin, taban, yazi_satir) - (taban - h)       # sprite yerel y
    for i in (0, 6, 12, 18):
        t = yeni(w, h)
        kare(t, duz(h, w), i)
        alfa = t.getchannel("A")
        toplam = sum(alfa.histogram()[1:])
        bb = alfa.getbbox()
        ust_satir = sum(alfa.crop((0, 0, w, 2)).histogram()[1:])
        if not toplam or (bb[1] <= 1 and ust_satir > serbest + 12):
            raise RuntimeError(f"Sahne {no}: sprite yüksekliği (h={h}) yetmiyor ya da kare boş")
        ici = sum(alfa.crop((a, 0, b, h)).histogram()[1:])
        if ici / toplam < esik:
            raise RuntimeError(f"Sahne {no}: figürlerin %{int(100 * ici / toplam)}'i görünür aralıkta (x {a}-{b})")
        if sinir > 0:
            yukari = sum(alfa.crop((a, 0, b, int(sinir))).point(lambda v: 255 if v > 200 else 0).histogram()[1:])
            if yukari > serbest:
                raise RuntimeError(f"Sahne {no}, kare {i}: {yukari} opak piksel yazı bandında (yerel y < {int(sinir)})")


def _spr(no, w, h, kare, yakin, esik=0.75, taban=632, satir=3, serbest=0, ek="karakter"):
    _kadraj(no, kare, w, h, yakin, esik, taban, satir, serbest)
    sprite(no, ek, w, h, KARE, kare)      # taban_denetimi varsayılan açık


def _gorunur(no, xler, sx0, sx1, yakin, pay=10):
    """Orta plandaki (hareketsiz) önemli figürlerin ızgara x'i sprite'ın baş ve son sx'inde görünür aralıkta kalmalı."""
    for sx in (sx0, sx1):
        a, b = sx - 270 / yakin + pay, sx + 270 / yakin - pay
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
        boy = s * (3.6 + 0.5 * j)
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
    L = s * (9.5 + 3.0 * acik)
    kanat(k, x + int(1.6 * s), oy, 1, aci, L, s)
    kanat(k, x - int(1.6 * s), oy, -1, aci - 30 * sol_dus, L * (1 - 0.15 * sol_dus), s)
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
    d.ellipse([x - int(2.6 * s), y - int(4.2 * s), x + int(2.6 * s), y - 1], fill=hex2(renk))
    d.polygon([(x - int(1.2 * s), y - int(3.8 * s)), (x - int(1.6 * s), y - int(5.6 * s)), (x + int(1.6 * s), y - int(5.6 * s)),
               (x + int(1.2 * s), y - int(3.8 * s))], fill=hex2(_ac(renk, 0.1)))
    d.line([x - int(1.3 * s), y - int(4 * s), x + int(1.3 * s), y - int(4 * s)], fill=hex2("#e0b040"), width=_u(0.4, s))
    d.chord([x - int(2.2 * s), y - int(4 * s), x - int(0.4 * s), y - int(1.4 * s)], 90, 270, fill=hex2(_ac(renk, 0.18)))
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
    d.ellipse([x - int(2.6 * s), y - int(6.4 * s), x + int(2.6 * s), y + int(0.4 * s)], fill=hex2(renk))
    d.rectangle([x - int(2.2 * s), y - int(6 * s), x + int(2.2 * s), y - 1], fill=hex2(renk))
    for yy in (y - int(1.4 * s), y - int(4.8 * s)):
        d.line([x - int(2.4 * s), yy, x + int(2.4 * s), yy], fill=hex2("#3a3a3e"), width=_u(0.5, s))
    for dx in (-1.2, 0, 1.2):
        d.line([x + int(dx * s), y - int(5.8 * s), x + int(dx * s), y - int(1 * s)], fill=hex2(_ac(renk, -0.2)))
    d.ellipse([x - int(2.2 * s), y - int(6.8 * s), x + int(2.2 * s), y - int(5.6 * s)], fill=hex2(_ac(renk, 0.2)))
    d.ellipse([x - int(0.8 * s), y - int(6.5 * s), x + int(0.6 * s), y - int(6 * s)], fill=hex2("#2a2420"))


def fisek(img, x, zemin, s=1.0, govde="#a8301e", serit="#e0b040", alev=0.0):
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
    for yn in (-1, 1):                                                   # yan kollar (kısa, arkada)
        cx = x + yn * int(2.3 * s)
        d.rectangle([cx - int(1 * s), y - int(18 * s), cx + int(1 * s), halka], fill=hex2(_ac(govde, -0.25)))
        d.polygon([(cx - int(1 * s), y - int(18 * s)), (cx, y - int(20 * s)), (cx + int(1 * s), y - int(18 * s))],
                  fill=hex2(_ac(serit, -0.2)))
        d.line([cx - int(1 * s), y - int(12 * s), cx + int(1 * s), y - int(12 * s)], fill=hex2(serit))
    ust = y - int(22 * s)
    d.rectangle([x - int(1.6 * s), ust, x + int(1.6 * s), halka + int(1.4 * s)], fill=hex2(govde))   # ana gövde
    d.line([x - int(1.6 * s), ust, x - int(1.6 * s), halka + int(1.4 * s)], fill=hex2(_ac(govde, 0.25)))
    for yy in (ust + int(3 * s), ust + int(8 * s), ust + int(13 * s)):
        d.rectangle([x - int(1.6 * s), yy, x + int(1.6 * s), yy + _u(0.6, s)], fill=hex2(serit))
    d.rectangle([x - int(3 * s), ust - _u(0.9, s), x + int(3 * s), ust], fill=hex2("#8a5a34"), outline=hex2("#3a2414"))  # oturak
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
    """Yeni figür: denizde yüzen adam (kulaç). Baş ve bir kol su çizgisinin üstünde; gövde suyun altında kalır
    (su_y'den aşağısı çizilmez). Başın çevresinde dalga halkası."""
    d = ImageDraw.Draw(img)
    r = max(2, int(1.7 * s))
    bx, by = x, su_y - int(0.9 * s) + int(SIN(f, 2) * 0.3 * s)
    a = f * 2 * math.pi                                                  # kulaç: kol öne-yukarı çıkar, suya girer
    omuz = (x - yon * int(0.6 * s), su_y)
    el = (x + yon * int(4.2 * s * math.cos(a)), su_y - int(3.4 * s * max(0.0, math.sin(a))))
    if el[1] < su_y - 1:
        d.line([*omuz, *el], fill=hex2(govde), width=_u(1, s))
        piksel(img, el[0], el[1], hex2("#e8b890"))
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=hex2("#e8b890"))
    d.chord([bx - r, by - r - 1, bx + r, by + r - _u(0.4, s)], 180, 360, fill=hex2(sac))   # ıslak saç
    piksel(img, bx + yon * int(0.9 * s), by, hex2("#2b1a12"))
    for k in range(-int(4 * s), int(4 * s) + 1):                          # dalga halkası
        if abs(k) > r and (k + int(f * 6)) % 3:
            piksel(img, bx + k, su_y - 1, hex2("#d8eaf4"))


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
    ky = alt - 3                                                          # perdede kule silüeti
    kx = x - int(6 * s)
    d.rectangle([kx - 2, ky - int(9 * s), kx + 2, ky], fill=hex2("#14141c"))
    d.polygon([(kx - 3, ky - int(9 * s)), (kx, ky - int(12 * s)), (kx + 3, ky - int(9 * s))], fill=hex2("#14141c"))
    ux, uy = x + int(5 * s), ust + int(7 * s) + int(SIN(f) * 1)          # perdede süzülen kanatlı adam
    d.line([ux - int(5 * s), uy - 1, ux + int(5 * s), uy - 1], fill=hex2("#14141c"), width=2)
    d.line([ux, uy - 2, ux, uy + int(2 * s)], fill=hex2("#14141c"), width=2)


def koltuk_sirasi(img, x0, x1, zemin, s=1.0, bas=(), renk="#6a1e22"):
    """Yeni figür: sinema koltuk sırası (arkalıklar) zemine oturur; bas: koltukta oturan izleyicilerin baş x'leri."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, (x0 + x1) // 2, x1 - x0)
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0, alfa=90)
    for bx in bas:                                                       # oturan izleyici: omuz ve baş arkalığın üstünde
        d.rectangle([bx - int(2.4 * s), y - int(8 * s), bx + int(2.4 * s), y - int(5 * s)], fill=hex2("#1e1e24"))
        d.ellipse([bx - int(1.7 * s), y - int(11 * s), bx + int(1.7 * s), y - int(7.6 * s)], fill=hex2("#2a2228"))
    gen = int(6 * s)
    for kx in range(x0, x1 - gen + 1, gen + 1):
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
