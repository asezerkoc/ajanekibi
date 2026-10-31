"""Paris'teki Elçi: Yirmisekiz Çelebi Mehmed Efendi'nin Paris sefareti (1720-21). Piksel Tarih (@pikseltarihim), sahneler 290-321.
Grafikerin tarifi: teslimler/gece/ara/celebi-mehmed-paris/5-grafik.md. Kalıp: video/piksel/cem_sultan.py (ölçek ve kadraj
yardımcıları oradan alınır), kalender.py (taht, rahle, kitaplar).
Yön dili: sağ = Paris'e / Batı'ya doğru giden yol, sol = eve dönüş ve geride kalan.
Kullanım: python3 -I video/piksel/celebi_mehmed_paris.py [sahne numaraları]"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import ImageDraw  # noqa: E402

from ciz import _ac, agac, cicek, duman, duz_zemin, figur, hex2, piksel, sehir, temas_golgesi, temel, yeni, zemin_y  # noqa: E402
from sahneler import GW, H, duz, gokyuzu, kaydet, on, orta, uzak  # noqa: E402
from timur_figur import atli, gemi, kisi, otag, oturan  # noqa: E402
from timur import agac_kavak, ates, ic_mekan, kalabalik, kandil, mumluk, su_ve_kiyi  # noqa: E402
from kayip_mezar import muhafiz  # noqa: E402
from kalender import kitaplar, rahle, taht  # noqa: E402
from cem_sultan import _kz, _spr, s_kisi, s_oturan  # noqa: E402

KARE = 24      # sprite kare sayısı (SKILL.md)
PAY = 135      # orta/ön plan yan payı (SKILL.md)
SIN = lambda f, k=1: math.sin(f * 2 * math.pi * k)  # noqa: E731

# Dış mekân sprite'ı (brif: h 170-230) ve iç mekân sprite'ı (brif: h 300)
DW, DH, DT = 400, 220, 632
IW, IH, IT = 400, 300, 634

# Kişiler (renk dili bütün videoda aynı kalır)
ELCI = dict(govde="#1f4f7a", bas="sarik", bas_renk="#f2ece0", sakal="#2a1a12")          # Çelebi Mehmed: mavi kaftan, orta yaşlı
ELCI_K = dict(ELCI, pelerin="#8a1e22")                                                   # ayakta: kırmızı kürk/pelerin
SAID = dict(govde="#6a3a6a", bas="sarik", bas_renk="#f2ece0", sakal=None)                # oğul Said, 1720: genç, sakalsız
SAID_1742 = dict(govde="#6a3a6a", bas="sarik", bas_renk="#f2ece0", sakal="#3a2414")      # 1742: sakallı, babasının pelerini
PADISAH = dict(govde="#7a1e22", bas="sarik", bas_renk="#f8f4ea", sakal="#2a1a12", pelerin="#c8a040")
SADRAZAM = dict(govde="#2a6a3a", bas="sarik", bas_renk="#f2ece0", sakal="#3a2a1a")
FRANSIZ = dict(govde="#2a3a8a", bas="sapka", bas_renk="#1a1a22", sakal=None)
NAIP = dict(govde="#5a1a3a", bas="sapka", bas_renk="#1a1a1a", sakal=None)
MUTEFERRIKA = dict(govde="#5a4a3a", bas="sarik", bas_renk="#ece6d8", sakal="#4a3a2a")
SEYHULISLAM = dict(govde="#e4e0d4", bas="sarik", bas_renk="#f8f6f0", sakal="#d8d0c8")
YENICERI = dict(govde="#3a4a7a", bas="bork", bas_renk="#ece6d8", sakal="#2a1a12")


# --------------------------------------------------------------------------
# Yazı bandı denetimi (bu serinin ek fizik/kadraj denetimi). Remotion kamerası sahneyi (sx, odakY = taban-12)
# çevresinde yakin..1.06·yakin büyütür; ekran yazısı ekran ızgarasında y 150'den yazının alt kenarına kadar durur.
# Bu bant dünya y'sine çevrilir; sprite'ta ve orta planda bu satırlarda görünür sütunlarda opak piksel varsa
# (1-2 piksellik kandil zinciri hariç) figür/yapı yazıya giriyor demektir: betik durur.
# Yazı alt kenarları ve yakin değerleri CelebiMehmed.tsx'ten okunur (kartlar orada; tek kaynak).
# --------------------------------------------------------------------------
TSX = Path(__file__).parents[1] / "src" / "sahneler" / "CelebiMehmed.tsx"


def _tsx_bantlari():
    import re
    if not TSX.exists():
        return {}
    metin = TSX.read_text()
    govde = metin[metin.index("bolumler:"):metin.index("kapanis:")]
    sonuc = {}
    for b in re.split(r"\n    \{", govde)[1:]:
        no = int(re.search(r"no: (\d+)", b).group(1))
        yk = float(re.search(r"yakin: ([\d.]+)", b).group(1))
        yy = re.search(r"yaziY: (\d+)", b)
        ust = int(yy.group(1)) if yy else 300
        alt = 0
        for m in re.finditer(r"satirlar: \[([^\]]*)\], sure: [\d.]+(?:, boy: (\d+))?", b):
            sat = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
            boy = int(m.group(2) or 92)
            sig = min(boy, math.floor(950 / (max(len(x) for x in sat) * 0.46)))
            alt = max(alt, (ust + len(sat) * sig * 1.12 + 8) / 2)          # ekran px → ızgara
        sonuc.setdefault(no, []).append((yk, alt, ust / 2))
    return sonuc


def _bant_denetimi(no, w, h, taban, pay=4):
    from PIL import Image
    bantlar = _tsx_bantlari().get(no, [])
    pub = Path(__file__).parents[1] / "public"
    spr = Image.open(pub / f"sahne{no}-karakter.png").convert("RGBA").getchannel("A")
    ort = Image.open(pub / f"sahne{no}-orta.png").convert("RGBA").getchannel("A")
    o = taban - 12
    for yk, alt, ust in bantlar:
        for z in (yk, yk * 1.06):
            y0, y1 = int(o - (o - ust) / z), int(o - (o - alt) / z) + pay
            yar = 270 / z
            for i in range(0, KARE, 3):
                for y in range(max(y0, taban - h), y1 + 1):
                    ly = y - (taban - h)
                    satir = spr.crop((i * w + int(w / 2 - yar), ly, i * w + int(w / 2 + yar), ly + 1))
                    n = sum(satir.histogram()[1:])
                    if n > 2:
                        raise RuntimeError(f"Sahne {no}: sprite (kare {i}) yazı bandına giriyor: dünya y {y} "
                                           f"(bant {y0}-{y1}, yakin {z:.2f}); figürü küçült ya da alçalt")
            for y in range(y0, y1 + 1):
                n = sum(ort.crop((PAY + int(270 - yar - 30), y, PAY + int(270 + yar + 30), y + 1)).histogram()[1:])
                if n > 2:
                    raise RuntimeError(f"Sahne {no}: orta plandaki yapı yazı bandına giriyor: y {y} (bant {y0}-{y1})")


def _spr2(no, w, h, kare, yakin, esik=0.75, taban=None):
    """cem_sultan._spr (kadraj + taban denetimi) + yazı bandı denetimi."""
    _spr(no, w, h, kare, yakin, esik)
    _bant_denetimi(no, w, h, taban or (DT if h == DH else IT))


def _bant_alt(no, taban=DT, pay=8):
    """Sahnenin bütün kartları ve yakınlaşma için yazı bandının en alt dünya y'si (+pay): duman ve yapılar bunun altında kalır."""
    o = taban - 12
    return max((int(o - (o - alt) / (yk * 1.06)) + pay for yk, alt, _ in _tsx_bantlari().get(no, [])), default=0)


def _bos_on(no):
    """Ön plan boş (sokak, liman, iç mekân): çimen tutamı yok."""
    kaydet(yeni(GW, H), f"sahne{no}-on.png")


def _yildiz_ekle(no, adet, y0, y1):
    """Gece sahnesi: gokyuzu() yıldızları y 300'ün üstüne koyar (kamera yakınken görünmez); görünür gök şeridine
    (y0-y1) seyrek yıldız ekler. Dosyayı yeniden işler; yatayda dikişsiz (x 0-539)."""
    from PIL import Image
    yol = Path(__file__).parents[1] / "public" / f"sahne{no}-gokyuzu.png"
    img = Image.open(yol).convert("RGBA")
    rnd = random.Random(no)
    for _ in range(adet):
        x, y = rnd.randrange(540), rnd.randrange(y0, y1)
        piksel(img, x, y, hex2(rnd.choice(("#fff8e0", "#d8e0f8", "#a8b4d8"))))
        if rnd.random() < 0.15:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                piksel(img, (x + dx) % 540, y + dy, hex2("#8890b8", 150))
    img.save(yol)


def _yerel(gx, sx, w):
    """Izgara x'i → sprite yerel x'i (SKILL.md: yerel = izgara − (sx − w/2))."""
    return gx - (sx - w // 2)


# ==========================================================================
# YENİ FİGÜRLER (ciz.py'ye eklenmedi; yalnızca bu seride). Hepsi (img, x, zemin, s, ...) alır,
# tabanını zemin çizgisine oturtur; yapılar duz_zemin ile yalnızca düz zemine kurulur.
# ==========================================================================
def paris_evleri(img, x0, x1, zemin, s=1.0, tohum=1, pencerede=False,
                 sivalar=("#d8c8a8", "#c8b494", "#e0d4bc", "#b8a488"), cati="#4a4e5e"):
    """Yeni figür: 1720'ler Paris sokağı. Bitişik nizam 3-4 katlı taş evler, mansart (kırık) arduvaz çatı, çatı
    pencereleri, kat silmeleri, zemin katta kapılar. pencerede=True: bazı pencerelerde sokağa bakan başlar (kalabalık).
    Düz zemine kurulur. Dönen değer: baca noktaları [(x, y)]."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "paris_evleri")
    temel(img, zemin, x0, x1, y, "#5a5048")
    rnd = random.Random(tohum)
    kh = max(4, int(round(7 * s)))
    bacalar = []
    x = x0
    while x1 - x >= int(10 * s):
        gw = min(int(rnd.randint(16, 23) * s), x1 - x)
        kat = rnd.choice((3, 3, 4))
        ust = y - kat * kh
        siva = rnd.choice(sivalar)
        d.rectangle([x, ust, x + gw - 1, y - 1], fill=hex2(siva))
        d.line([x, ust, x, y - 1], fill=hex2(_ac(siva, -0.3)))                       # bitişik ev sınırı
        for k in range(1, kat):
            d.line([x, y - k * kh, x + gw - 1, y - k * kh], fill=hex2(_ac(siva, -0.18)))  # kat silmesi
        ch = max(3, int(5 * s))
        d.polygon([(x, ust), (x + gw - 1, ust), (x + gw - 1 - int(2 * s), ust - ch), (x + int(2 * s), ust - ch)],
                  fill=hex2(cati))
        d.line([x + int(2 * s), ust - ch, x + gw - 1 - int(2 * s), ust - ch], fill=hex2(_ac(cati, 0.3)))
        for cx in range(x + int(5 * s), x + gw - int(3 * s), max(3, int(7 * s))):    # çatı pencereleri
            d.rectangle([cx - int(1 * s), ust - ch + int(1.6 * s), cx + int(1 * s), ust - 1], fill=hex2("#2a2a34"))
            d.line([cx - int(1 * s), ust - ch + int(1.4 * s), cx + int(1 * s), ust - ch + int(1.4 * s)],
                   fill=hex2(_ac(cati, 0.4)))
        bx = x + int(gw * 0.7)                                                          # baca: çatıdan yükselir
        d.rectangle([bx, ust - ch - int(2.5 * s), bx + max(1, int(1.6 * s)), ust - ch], fill=hex2("#6a5a52"))
        bacalar.append((bx + 1, ust - ch - int(2.5 * s)))
        n = max(2, gw // max(3, int(6 * s)))
        for k in range(kat):                                                            # pencereler
            fy = y - k * kh
            for j in range(n):
                wx = x + int((j + 0.5) * gw / n)
                if k == 0 and j == n // 2:                                              # zemin katta kapı
                    d.rectangle([wx - int(1.4 * s), fy - int(5.4 * s), wx + int(1.4 * s), fy - 1], fill=hex2("#3a2418"))
                    d.line([wx - int(1.4 * s), fy - int(5.4 * s), wx + int(1.4 * s), fy - int(5.4 * s)],
                           fill=hex2(_ac(siva, 0.3)))
                    continue
                a, b = fy - kh + max(1, int(1.6 * s)), fy - max(1, int(1.4 * s))
                d.rectangle([wx - int(1.1 * s), a, wx + int(1.1 * s), b], fill=hex2("#2a3440"))
                d.line([wx - int(1.3 * s), a - 1, wx + int(1.3 * s), a - 1], fill=hex2(_ac(siva, 0.35)))
                if pencerede and k >= 1 and rnd.random() < 0.45:                       # pencereden bakan baş
                    r = max(1, int(0.8 * s))
                    hy = b - r
                    d.ellipse([wx - r, hy - r, wx + r, hy + r], fill=hex2(rnd.choice(("#d6a07a", "#c89070", "#e0b090"))))
                    d.rectangle([wx - r, hy - r - max(1, int(0.6 * s)), wx + r, hy - r], fill=hex2(
                        rnd.choice(("#1a1a22", "#5a3a22", "#e8e0d0"))))
        x += gw
    return bacalar


def saray_cephesi(img, x0, x1, zemin, s=1.0, tas="#d8ccb0", cati="#4a5060", kubbe=True, pencere="#3a4a5a"):
    """Yeni figür: 18. yüzyıl Fransız sarayı cephesi (Tuileries, Versailles, Paris Rasathanesi için). İki katlı uzun
    kanat, kemerli pencere dizisi, pilastrlar, mansart çatı; ortada daha yüksek merkez köşkü (kubbe=True: kare kubbe ve
    fener), iki uçta köşe köşkleri. Düz zemine kurulur. Dönen değer: en üst y."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "saray_cephesi")
    temel(img, zemin, x0, x1, y, "#6a604e")
    golge = _ac(tas, -0.22)
    h = int(16 * s)
    ust = y - h
    d.rectangle([x0, ust, x1, y - 1], fill=hex2(tas))
    d.rectangle([x0, y - max(1, int(1.6 * s)), x1, y - 1], fill=hex2(golge))           # kaide
    d.line([x0, ust, x1, ust], fill=hex2(_ac(tas, 0.3)))                                # korniş
    d.line([x0, ust + int(8 * s), x1, ust + int(8 * s)], fill=hex2(golge))              # kat silmesi
    d.polygon([(x0, ust), (x1, ust), (x1 - int(3 * s), ust - int(5 * s)), (x0 + int(3 * s), ust - int(5 * s))],
              fill=hex2(cati))
    bay = max(4, int(5 * s))
    for bx in range(x0 + int(3 * s), x1 - int(2 * s), bay):
        d.line([bx - bay // 2, ust + 1, bx - bay // 2, y - 2], fill=hex2(_ac(tas, 0.18)))  # pilastr
        for a in (ust + int(2.4 * s), ust + int(10 * s)):
            pw = max(1, int(1.1 * s))
            d.rectangle([bx - pw, a + pw, bx + pw, a + int(4.6 * s)], fill=hex2(pencere))
            d.chord([bx - pw, a, bx + pw, a + 2 * pw], 180, 360, fill=hex2(pencere))
        if bx % (3 * bay) < bay:                                                         # çatı penceresi
            d.rectangle([bx - int(0.8 * s), ust - int(3.2 * s), bx + int(0.8 * s), ust - 1], fill=hex2(_ac(tas, 0.1)))
    for ux in (x0, x1 - int(8 * s)):                                                     # köşe köşkleri
        d.rectangle([ux, ust - int(3 * s), ux + int(8 * s), y - 1], outline=hex2(golge), fill=None)
        d.polygon([(ux, ust - int(3 * s)), (ux + int(8 * s), ust - int(3 * s)), (ux + int(6.5 * s), ust - int(8 * s)),
                   (ux + int(1.5 * s), ust - int(8 * s))], fill=hex2(cati))
        d.rectangle([ux + 1, ust - int(3 * s), ux + int(8 * s) - 1, ust - 1], fill=hex2(tas))
    cx, pw = (x0 + x1) // 2, int(9 * s)
    tepe = ust - int(8 * s)
    d.rectangle([cx - pw, ust - int(6 * s), cx + pw, y - 1], fill=hex2(_ac(tas, 0.08)))   # merkez köşkü
    for k in (-1, 1):
        d.line([cx + k * (pw - int(1.5 * s)), ust - int(6 * s), cx + k * (pw - int(1.5 * s)), y - 2], fill=hex2(golge))
    d.chord([cx - int(2.4 * s), y - int(8 * s), cx + int(2.4 * s), y - int(3 * s)], 180, 360, fill=hex2("#3a2a20"))
    d.rectangle([cx - int(2.4 * s), y - int(5.5 * s), cx + int(2.4 * s), y - 1], fill=hex2("#3a2a20"))  # büyük kapı
    for a in (ust - int(3 * s), ust + int(5 * s)):
        d.rectangle([cx - int(1.2 * s), a, cx + int(1.2 * s), a + int(4 * s)], fill=hex2(pencere))
    if kubbe:
        d.polygon([(cx - pw, ust - int(6 * s)), (cx + pw, ust - int(6 * s)), (cx + pw - int(3 * s), ust - int(13 * s)),
                   (cx - pw + int(3 * s), ust - int(13 * s))], fill=hex2(cati))
        d.line([cx - pw + int(3 * s), ust - int(13 * s), cx + pw - int(3 * s), ust - int(13 * s)], fill=hex2(_ac(cati, 0.35)))
        d.rectangle([cx - int(1.4 * s), ust - int(16 * s), cx + int(1.4 * s), ust - int(13 * s)], fill=hex2(_ac(tas, 0.1)))
        tepe = ust - int(16 * s)
    else:
        d.polygon([(cx - pw, ust - int(6 * s)), (cx + pw, ust - int(6 * s)), (cx, ust - int(10 * s))], fill=hex2(_ac(tas, 0.1)))
        tepe = ust - int(10 * s)
    return tepe


def havuz(img, x, zemin, s=1.0, faz=0.0, fiskiye=True, tas="#c8c0b0", su="#4a7aa8"):
    """Yeni figür: taş kenarlı oval süs havuzu (yukarıdan hafif bakış). Ön duvarın alt kenarı zemine oturur; ortadaki
    vazodan fışkıran su iki yana kavis çizerek havuza düşer (su sütunu hep kaynağına bağlı). faz 0→1 dikişsiz döngü."""
    d = ImageDraw.Draw(img)
    rx, ry, hd = int(16 * s), max(2, int(3.4 * s)), max(2, int(2.6 * s))
    y = zemin_y(zemin, x, 2 * rx)
    temas_golgesi(img, x, y, 2 * rx + 2)
    cy = y - 1 - hd - ry
    d.ellipse([x - rx, cy + hd - ry, x + rx, cy + hd + ry], fill=hex2(_ac(tas, -0.25)))  # ön duvar (alt elips)
    d.rectangle([x - rx, cy, x + rx, cy + hd], fill=hex2(_ac(tas, -0.12)))
    d.ellipse([x - rx, cy - ry, x + rx, cy + ry], fill=hex2(tas))                        # taş kenar
    d.ellipse([x - rx + int(1.4 * s), cy - ry + int(0.8 * s), x + rx - int(1.4 * s), cy + ry - int(0.8 * s)], fill=hex2(su))
    rnd = random.Random(7)
    for _ in range(int(14 * s)):                                                         # su yüzünde parıltı
        px_ = x + rnd.randint(-rx + int(3 * s), rx - int(3 * s))
        py_ = cy + rnd.randint(-ry + 2, ry - 2)
        if ((px_ - x) / rx) ** 2 + ((py_ - cy) / ry) ** 2 < 0.6 and (rnd.random() + faz) % 1 < 0.5:
            piksel(img, px_, py_, hex2("#b8d8f0"))
    if not fiskiye:
        return cy
    vy = cy - int(3 * s)
    d.rectangle([x - max(1, int(0.7 * s)), vy, x + max(1, int(0.7 * s)), cy], fill=hex2(_ac(tas, -0.1)))  # vazo ayağı
    d.chord([x - int(2.4 * s), vy - int(1.2 * s), x + int(2.4 * s), vy + int(1.2 * s)], 0, 180, fill=hex2(tas))
    boy = int(11 * s * (0.93 + 0.07 * SIN(faz)))
    top = vy - boy
    jw = max(1, int(0.6 * s))
    d.rectangle([x - jw, top, x + jw, vy], fill=hex2("#d8ecf8"))                          # su sütunu
    for k in (-1, 1):                                                                     # iki yana düşen su
        for i in range(0, 41):
            t = i / 40
            px_ = x + k * t * 7 * s
            py_ = top + t * t * (cy - top)
            piksel(img, px_, py_, hex2("#cfe6f6"))
            if s > 2.5:
                piksel(img, px_ + k, py_, hex2("#a8cce8"))
        for j in range(3):                                                                # damlalar kavis boyunca kayar
            t = (faz + j / 3) % 1
            piksel(img, x + k * t * 7 * s, top + t * t * (cy - top) - 1, hex2("#ffffff"))
    for k in (-1, 1):                                                                     # düştüğü yerde köpük
        fx = x + k * int(7 * s)
        for dx in range(-int(1.2 * s), int(1.2 * s) + 1):
            piksel(img, fx + dx, cy - (1 if (dx + int(faz * 6)) % 2 else 0), hex2("#e8f4fc"))
    return cy


def teleskop(img, x, zemin, s=1.0, yon=1, aci=0.55):
    """Yeni figür: üç ayaklı sehpa üstünde pirinç dürbün (rasathane). Üç ayak zemine basar; tüp sehpanın tepesine
    bağlı, gökyüzüne (aci radyan) eğik."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 12 * s)
    temas_golgesi(img, x, y, 12 * s)
    ax, ay = x, y - int(13 * s)
    lw = max(1, int(0.7 * s))
    for dx in (-5, 5, 1.5 * yon):
        d.line([ax, ay, x + int(dx * s), y - 1], fill=hex2("#5a3a1e"), width=lw)
    ca, sa = math.cos(aci), math.sin(aci)
    bx, by = ax - ca * 5 * s * yon, ay + sa * 5 * s
    fx, fy = ax + ca * 15 * s * yon, ay - sa * 15 * s
    d.line([bx, by, fx, fy], fill=hex2("#c8a040"), width=max(2, int(2.2 * s)))
    for t in (0.25, 0.55, 0.85):
        cx_, cy_ = bx + (fx - bx) * t, by + (fy - by) * t
        d.line([cx_ - sa * 1.3 * s * yon, cy_ - ca * 1.3 * s, cx_ + sa * 1.3 * s * yon, cy_ + ca * 1.3 * s],
               fill=hex2("#6a4a1a"), width=max(1, int(0.5 * s)))
    d.line([fx - sa * 1.6 * s * yon, fy - ca * 1.6 * s, fx + sa * 1.6 * s * yon, fy + ca * 1.6 * s],
           fill=hex2("#e8c860"), width=max(1, int(0.8 * s)))                              # objektif halkası
    d.ellipse([ax - int(1 * s), ay - int(1 * s), ax + int(1 * s), ay + int(1 * s)], fill=hex2("#3a2a1a"))


def kadran(img, x, zemin, s=1.0):
    """Yeni figür: ayaklı pirinç çeyrek daire (gözlem aleti). Kaide zemine basar, yay direğin tepesine bağlı."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 8 * s)
    temas_golgesi(img, x, y, 8 * s)
    d.rectangle([x - int(4 * s), y - max(2, int(1.4 * s)), x + int(4 * s), y - 1], fill=hex2("#5a3a1e"))
    d.rectangle([x - max(1, int(0.7 * s)), y - int(12 * s), x + max(1, int(0.7 * s)), y - 1], fill=hex2("#6a4a2a"))
    cx, cy, r = x, y - int(12 * s), int(9 * s)
    lw = max(1, int(0.8 * s))
    d.arc([cx - r, cy - r, cx + r, cy + r], 180, 270, fill=hex2("#c8a040"), width=lw)
    for a in (180, 202, 225, 248, 270):
        d.line([cx, cy, cx + math.cos(math.radians(a)) * r, cy + math.sin(math.radians(a)) * r],
               fill=hex2("#a88030"), width=max(1, lw - 1))


def baski_tezgahi(img, x, zemin, s=1.0, faz=0.0, kagit=True):
    """Yeni figür: ahşap el baskı tezgâhı (18. yüzyıl). İki dikme kızaklarla zemine basar; üst başlık, vida kirişi,
    vida ve pres plakası; iki yana taşan tabla uç ayaklarıyla yere iner, üstünde harf kalıbı ve kâğıt. faz 0→1:
    plaka iner kalkar (dikişsiz). Kol çizilmez: baskıcının eline göre sahnede çizilir (bkz. _baski_kolu).
    Dönen değer: vidanın kol bağlantı noktası (x, y)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 24 * s)
    temas_golgesi(img, x, y, 26 * s)
    ag = "#6a4a2a"
    koyu, acik = _ac(ag, -0.3), _ac(ag, 0.2)
    bw = max(2, int(1.8 * s))
    for k in (-1, 1):                                                                    # kızaklar ve dikmeler
        d.rectangle([x + k * int(7 * s) - int(2.5 * s), y - max(2, int(1.4 * s)), x + k * int(7 * s) + int(2.5 * s), y - 1],
                    fill=hex2(koyu))
        d.rectangle([x + k * int(7 * s) - bw // 2, y - int(30 * s), x + k * int(7 * s) + bw // 2, y - 2], fill=hex2(ag))
    d.rectangle([x - int(9 * s), y - int(31.5 * s), x + int(9 * s), y - int(29 * s)], fill=hex2(koyu))   # başlık
    d.rectangle([x - int(7.5 * s), y - int(23 * s), x + int(7.5 * s), y - int(21 * s)], fill=hex2(ag))   # vida kirişi
    ty = y - int(12 * s)
    d.rectangle([x - int(12 * s), ty, x + int(12 * s), ty + max(2, int(1.4 * s))], fill=hex2(acik))        # tabla
    for ux in (-11.4, 11.4):
        d.rectangle([x + int(ux * s) - max(1, int(0.5 * s)), ty + 1, x + int(ux * s) + max(1, int(0.5 * s)), y - 1],
                    fill=hex2(koyu))
    d.rectangle([x - int(4 * s), ty - max(1, int(1 * s)), x + int(4 * s), ty - 1], fill=hex2("#2a2a2e"))    # harf kalıbı
    for k in range(-3, 4):
        piksel(img, x + int(k * s), ty - 1, hex2("#8a8a90"))
    bas = (1 - math.cos(faz * 2 * math.pi)) / 2
    py = y - int(19 * s) + int(bas * 5.5 * s)
    py = min(py, ty - max(1, int(1 * s)) - max(2, int(1.2 * s)) - 1)
    d.rectangle([x - max(1, int(0.6 * s)), y - int(21 * s), x + max(1, int(0.6 * s)), py], fill=hex2("#8a8a96"))  # vida
    d.rectangle([x - int(5 * s), py, x + int(5 * s), py + max(2, int(1.2 * s))], fill=hex2(koyu))            # plaka
    if kagit:
        d.rectangle([x + int(5 * s), ty - max(1, int(0.6 * s)), x + int(11 * s), ty - 1], fill=hex2("#f0e8d4"))
        d.line([x + int(6 * s), ty - 1, x + int(10 * s), ty - 1], fill=hex2("#2a2a2e"))
    return x, y - int(20 * s)


def _baski_kolu(t, vida, el):
    """Baskı kolu: vidadan baskıcının eline uzanan demir çubuk (iki ucu da bağlı)."""
    d = ImageDraw.Draw(t)
    d.line([*vida, *el], fill=hex2("#3a3a40"), width=2)
    d.line([vida[0], vida[1] - 1, el[0], el[1] - 1], fill=hex2("#7a7a84"))


def _el(x, z, s, yon, kol):
    """kisi() figürünün el ucu (timur_figur.kisi ile aynı formül; ayakta, diz=False)."""
    y = zemin_y(z, x, 6 * s)
    ust = y - int(11 * s)
    if kol > 0:
        return x + int(3.5 * s) * yon, ust - int(4 * s * kol) + int(1 * s)
    return x + int(2.5 * s) * yon, ust + int(5 * s)


def kitap_rafi(img, x, zemin, s=1.0, dolu=True, tohum=1):
    """Yeni figür: ayaklı ahşap raf dolabı. Gövde zemine oturur; dolu=True raflar kitaplı, dolu=False raflar boş
    (yalnız toz ve tek bir yatık defter)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 18 * s)
    temas_golgesi(img, x, y, 19 * s)
    ag = "#5a3a22"
    d.rectangle([x - int(9 * s), y - int(30 * s), x + int(9 * s), y - 1], fill=hex2(_ac(ag, -0.45)))
    for k in (-1, 1):
        d.rectangle([x + k * int(9 * s) - max(1, int(0.6 * s)), y - int(30 * s), x + k * int(9 * s) + max(1, int(0.6 * s)), y - 1],
                    fill=hex2(ag))
    d.rectangle([x - int(10 * s), y - int(31.5 * s), x + int(10 * s), y - int(30 * s)], fill=hex2(_ac(ag, 0.15)))
    rnd = random.Random(tohum)
    for sy in (y - int(1.2 * s), y - int(8.6 * s), y - int(16 * s), y - int(23.2 * s)):
        d.rectangle([x - int(9 * s), sy, x + int(9 * s), sy + max(1, int(0.8 * s))], fill=hex2(ag))
        if dolu:
            bx = x - int(8 * s)
            while bx < x + int(7.5 * s):
                bw = max(1, int(rnd.uniform(0.9, 1.8) * s))
                bh = int(rnd.uniform(4.2, 6.2) * s)
                renk = rnd.choice(("#8a2a2a", "#2a4a7a", "#3a6a3a", "#a8803a", "#5a3a5a", "#7a5a3a"))
                d.rectangle([bx, sy - bh, min(bx + bw, x + int(8 * s)), sy - 1], fill=hex2(renk))
                piksel(img, bx, sy - bh + 1, hex2(_ac(renk, 0.4)))
                bx += bw + 1
        else:
            for k in range(int(4 * s)):
                piksel(img, x - int(8 * s) + rnd.randint(0, int(16 * s)), sy - 1, hex2("#8a7a6a"))
    if not dolu:                                                                         # tek yatık defter
        sy = y - int(8.6 * s)
        d.rectangle([x - int(3 * s), sy - int(1.2 * s), x + int(3 * s), sy - 1], fill=hex2("#6a3a2a"))


def kavuk_yerde(img, x, zemin, s=1.0, renk="#f2ece0"):
    """Yeni figür: yere düşüp yan yatmış kavuk. Yuvarlak gövde zemine değer, kırmızı tepesi yana bakar."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 10 * s)
    temas_golgesi(img, x, y, 11 * s)
    # kırmızı külah (kavuğun tepesi) sağa bakar: tabanı yere değer
    d.polygon([(x + int(2.5 * s), y - int(5.2 * s)), (x + int(6.5 * s), y - int(4.2 * s)), (x + int(6.5 * s), y - 1),
               (x + int(2.5 * s), y - 1)], fill=hex2("#a82a22"))
    d.line([x + int(6.5 * s), y - int(4.2 * s), x + int(6.5 * s), y - 1], fill=hex2("#7a1a16"))
    # sarık gövdesi: yan yatmış yuvarlak sargı, eğik sarım bantları
    d.ellipse([x - int(5 * s), y - int(7 * s), x + int(3.5 * s), y - 1], fill=hex2(renk))
    for k in range(-4, 4, 2):
        d.line([x + int(k * s), y - int(6.6 * s), x + int((k + 2.2) * s), y - int(1.4 * s)], fill=hex2(_ac(renk, -0.2)))
    d.arc([x - int(5 * s), y - int(7 * s), x + int(3.5 * s), y - 1], 20, 160, fill=hex2(_ac(renk, -0.3)))


def kosk(img, x, zemin, s=1.0, iskele=False):
    """Yeni figür: Lale Devri sahil köşkü (Sâdâbâd için temsili). Taş zemin kat ve kemerli açıklıklar, ahşap üst kat,
    geniş saçaklı basık kırma çatı. iskele=True: yapım hâlinde; direkler zemine dikili, yatay kalaslar bağlı, çatının
    sağ yarısı henüz kaplanmamış (yalnız mertekler). Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(27 * s), x + int(27 * s), "kosk")
    temel(img, zemin, x - int(27 * s), x + int(27 * s), y, "#6a604e")
    tas, ahsap, cati = "#d8d0c0", "#c8a878", "#8a5a4a"
    d.rectangle([x - int(20 * s), y - int(11 * s), x + int(20 * s), y - 1], fill=hex2(tas))
    for k in range(-2, 3):
        kx = x + int(k * 8 * s)
        d.rectangle([kx - int(2.4 * s), y - int(6.5 * s), kx + int(2.4 * s), y - 1], fill=hex2("#3a3a42"))
        d.chord([kx - int(2.4 * s), y - int(8.5 * s), kx + int(2.4 * s), y - int(4.5 * s)], 180, 360, fill=hex2("#3a3a42"))
    d.rectangle([x - int(22 * s), y - int(21 * s), x + int(22 * s), y - int(11 * s)], fill=hex2(ahsap))
    d.line([x - int(22 * s), y - int(11 * s), x + int(22 * s), y - int(11 * s)], fill=hex2(_ac(ahsap, -0.35)), width=max(1, int(0.6 * s)))
    for wx in range(x - int(19 * s), x + int(20 * s), max(3, int(4.2 * s))):
        d.rectangle([wx, y - int(19 * s), wx + max(1, int(2 * s)), y - int(13.5 * s)], fill=hex2("#3a4a5a"))
    yarim = x if iskele else x + int(27 * s)
    d.polygon([(x - int(27 * s), y - int(21 * s)), (yarim, y - int(21 * s)), (min(yarim, x + int(15 * s)), y - int(27 * s)),
               (x - int(15 * s), y - int(27 * s))], fill=hex2(cati))
    d.line([x - int(27 * s), y - int(21 * s), yarim, y - int(21 * s)], fill=hex2(_ac(cati, -0.3)))
    if iskele:
        for mx in range(x, x + int(27 * s), max(2, int(3 * s))):                        # kaplanmamış mertekler
            d.line([mx, y - int(21 * s), mx - int((mx - x) * 0.45), y - int(27 * s)], fill=hex2("#7a5a32"))
        d.line([x, y - int(27 * s), x + int(15 * s), y - int(27 * s)], fill=hex2("#7a5a32"))
        for px_ in (x + int(6 * s), x + int(16 * s), x + int(25 * s)):                     # iskele direkleri
            d.line([px_, y - 1, px_, y - int(29 * s)], fill=hex2("#8a6a3a"), width=max(1, int(0.8 * s)))
        for ly in (y - int(11 * s), y - int(21 * s)):
            d.line([x + int(4 * s), ly, x + int(26 * s), ly], fill=hex2("#8a6a3a"), width=max(1, int(0.6 * s)))
        d.line([x + int(6 * s), y - 2, x + int(16 * s), y - int(11 * s)], fill=hex2("#7a5a32"))


def masa(img, x, zemin, s=1.0, ortu="#2a3a8a"):
    """Yeni figür: örtülü küçük masa; dört ayak zemine basar. Dönen değer: tabla üst y (kitaplar buna oturur)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 16 * s)
    temas_golgesi(img, x, y, 17 * s)
    top = y - int(8 * s)
    for k in (-7, -3, 3, 7):
        d.rectangle([x + int(k * s) - max(1, int(0.5 * s)), top, x + int(k * s) + max(1, int(0.5 * s)), y - 1], fill=hex2("#4a2e1a"))
    d.rectangle([x - int(8 * s), top - max(1, int(1 * s)), x + int(8 * s), top + int(3 * s)], fill=hex2(ortu))
    d.line([x - int(8 * s), top + int(3 * s), x + int(8 * s), top + int(3 * s)], fill=hex2("#e0b040"))
    return top - max(1, int(1 * s))


def sahne_tahtasi(img, x, zemin, s=1.0, f=0.0):
    """Yeni figür: tiyatro sahnesi (alçak ahşap platform). Ön yüz zemine oturur; üst yüzün ön kenarında titreyen
    sahne mumları (kaplarının içinde). Dönen değer: oyuncuların bastığı üst yüz y'si."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 60 * s)
    temas_golgesi(img, x, y, 62 * s)
    on_ust = y - int(5 * s)
    derin = int(4 * s)
    d.rectangle([x - int(30 * s), on_ust - derin, x + int(30 * s), on_ust], fill=hex2("#8a6a42"))   # üst yüz (tahtalar)
    for k in range(on_ust - derin + 2, on_ust, 3):
        d.line([x - int(30 * s), k, x + int(30 * s), k], fill=hex2("#7a5a36"))
    d.rectangle([x - int(30 * s), on_ust, x + int(30 * s), y - 1], fill=hex2("#4a2e1a"))             # ön yüz
    for px_ in range(x - int(30 * s), x + int(30 * s), max(3, int(5 * s))):
        d.line([px_, on_ust + 1, px_, y - 2], fill=hex2("#3a2214"))
    d.line([x - int(30 * s), on_ust, x + int(30 * s), on_ust], fill=hex2("#b08a5a"))
    for j, mx in enumerate(range(x - int(27 * s), x + int(28 * s), max(4, int(6 * s)))):           # sahne mumları
        d.rectangle([mx - 1, on_ust - 2, mx + 1, on_ust], fill=hex2("#5a4a3a"))
        alev = 2 + int(1.5 + 1.2 * math.sin((f + j * 0.37) * 2 * math.pi))
        for k in range(alev):
            piksel(img, mx, on_ust - 3 - k, hex2("#ffd060" if k < alev - 1 else "#fff4c0"))
    return on_ust - derin // 2


def cit(img, x0, x1, zemin, s=1.0, renk="#6a4a2a"):
    """Yeni figür: ahşap karantina çiti. Kazıklar zemine çakılı (dibinde temas gölgesi), üstte iki yatay kalas."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "cit", tolerans=6)
    pw = max(1, int(0.7 * s))
    for px_ in range(x0, x1 + 1, max(4, int(9 * s))):
        temas_golgesi(img, px_, y, 3 * s)
        d.rectangle([px_ - pw, y - int(9 * s), px_ + pw, y - 1], fill=hex2(renk))
        d.polygon([(px_ - pw, y - int(9 * s)), (px_ + pw, y - int(9 * s)), (px_, y - int(10.5 * s))], fill=hex2(renk))
    for ry in (y - int(7.5 * s), y - int(3.8 * s)):
        d.rectangle([x0, ry, x1, ry + max(1, int(0.9 * s))], fill=hex2(_ac(renk, 0.15)))


def _duman_noktalari(no, noktalar, sx, w, h, taban, en=None, boy=30):
    """Orta plandaki çatı noktalarını sprite yerel koordinatına çevirir (orta ve sprite aynı paralaksta: 0.65).
    Her nokta için duman boyu, duman yazı bandına girmeyecek biçimde kısaltılır: (x, y, boy)."""
    alt = _bant_alt(no, taban)
    sonuc = []
    for x, y in noktalar:
        lx, ly = x - PAY - (sx - w // 2), y - (taban - h)
        b = min(boy, y - alt - 10)
        if 4 <= lx <= w - 4 and 0 < ly < h and b >= 8:
            sonuc.append((lx, ly, b))
    return sonuc[:en] if en else sonuc


# ==========================================================================
# 290 · KAPAK + kart 1 · Toulon limanı, 1720 sonu: rıhtımda elçi ve oğlu; geride demirli gemi
# ==========================================================================
SU290 = 590      # orta planda gemi su çizgisi
RIHTIM = 600     # orta planda taş rıhtımın üst kenarı (sprite tabanı 632 bunun içinde)


def _liman_orta(no, renkler, kenar, gemi_x, sg, yelken, govde="#3a2a22", ekle=None):
    def _ekle(img, z):
        su_ve_kiyi(img, 556, renkler=renkler)
        figur(img, gemi, PAY + gemi_x, SU290, sg, 1, 0.0, govde=govde, yelken=yelken, hac=False)
        d = ImageDraw.Draw(img)
        d.rectangle([0, RIHTIM, GW, H], fill=hex2("#6a6460"))                     # taş rıhtım
        d.rectangle([0, RIHTIM, GW, RIHTIM + 2], fill=hex2(kenar))
        for yy in range(RIHTIM + 10, H, 14):
            d.line([0, yy, GW, yy], fill=hex2("#5a5450"))
            for xx in range((yy // 14) % 2 * 18, GW, 36):
                d.line([xx, yy, xx, yy + 14], fill=hex2("#5a5450"))
        for bx in (PAY + 120, PAY + 300, PAY + 450):                              # babalar: rıhtıma oturur
            d.rectangle([bx - 3, RIHTIM - 7, bx + 3, RIHTIM + 1], fill=hex2("#3a3634"))
            d.rectangle([bx - 4, RIHTIM - 9, bx + 4, RIHTIM - 7], fill=hex2("#4a4644"))
        if ekle:
            ekle(img, z)
    orta(no, (552, 556), [renkler[0]] * 5, renkler[0], ekle=_ekle)


def sahne290():
    """Toulon limanı, 1720'nin sonu, alacakaranlık: taş rıhtımda elçi ve oğlu Said denize (sola) bakar; geride demirli gemi."""
    gokyuzu(290, ["#2a2a5a", "#4a3a6a", "#7a4a72", "#b0647a", "#d88a7c", "#eaa888"], None,
            [(110, 404, 20), (430, 408, 18)], ("#f4d8d0", "#d8a8b0", "#a07890"))
    uzak(290, ["#4a4068", "#40385e"], ["#5a4a6a", "#4e4060"], ["#3e4a78", "#36426e", "#2e3a64"],
         dag_y=(398, 446), tepe_y=470, ova_y=500)
    yk = 2.8
    K = s_kisi(yk, 0.30)
    _liman_orta(290, ("#3e4a78", "#36426e", "#2e3a64", "#28325a"), "#a8a4b4", 215, 2.0, "#e8dcc8")
    _bos_on(290)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 262, z, round(0.92 * K, 1), **SAID, yon=-1, kol=0.02 * (1 + SIN(f + 0.3)))
        figur(t, kisi, 194, z, K, **ELCI_K, yon=-1, kol=0.03 * (1 + SIN(f)))

    _spr2(290, DW, DH, kare, yk)


# ==========================================================================
# 291 · kart 2 · Veba: kapatılmış yol, karantina çitinde nöbetçi; geride Toulon'un damlarından duman
# ==========================================================================
def sahne291():
    """'Dışarıda veba var.': kurşuni alacakaranlık; çitle kapatılmış yolda tek nöbetçi, geride şehirden duman yükselir."""
    gokyuzu(291, ["#2a2a3e", "#3e3a4e", "#5a4a5a", "#7a5a62", "#986e6e", "#aa8478"], None,
            [(120, 406, 20), (420, 402, 22)], ("#b8a8a8", "#988890", "#786a78"))
    uzak(291, ["#4a4652", "#3e3a48"], ["#56505a", "#4a4450"], ["#5a5650", "#4e4a46", "#423e3c"],
         dag_y=(392, 440), tepe_y=462, ova_y=488)
    yk = 2.8
    K = s_kisi(yk)
    sx = 270
    catilar = []

    def ekle(img, z):
        catilar.extend(figur(img, sehir, PAY + 160, PAY + 390, duz(590), 2.0, duvar="#8a8278",
                             golge="#5e584e", cati="#6a3a30", tohum=291))

    orta(291, (532, 560), ["#5a564a", "#4e4a40", "#424036", "#38362e", "#2e2c26"], "#8a8676", ekle=ekle)
    on(291, ["#2e2c26", "#38362e", "#424036"], "#7a7666", boy=90)
    dumanlar = _duman_noktalari(291, catilar[2::6], sx, DW, DH, DT, en=4)

    def kare(t, z, i):
        f = i / KARE
        for j, (x, y, b) in enumerate(dumanlar):
            duman(t, x, y, b, 291 + j, faz=(f + j * 0.29) % 1, renk="#6a6468", ruzgar=0.25, genislik=1.4)
        figur(t, cit, 120, 300, z, round(0.55 * K, 1))
        figur(t, muhafiz, 238, z, round(K - 0.2, 1), faz=f, mizrak=False, mesale=True, deel="#3a3a4a")

    _spr2(291, DW, DH, kare, yk, esik=0.6)


# ==========================================================================
# 292 · kart 3 ve 25 · Elçi yazar: bak, öğren, anlat (sıcak oda, rahle, mum)
# ==========================================================================
def _yazan_elci(no, yk, duvar, pencere, cini, zemin_renk, govde=ELCI, kandil_x=268, hali=True, mum=3):
    ic_mekan(no, duvar=duvar, kemer=_ac(duvar[0], -0.4), cini=cini, pencere=pencere,
             zemin_renk=zemin_renk, isik="#f8c060", hali=hali)
    s = s_oturan(yk, 0.30)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, kandil_x, 0, f, zincir=_kz(yk))
        mumluk(t, 128, z, f, mum)
        kitaplar(t, 152, z[0], round(0.45 * s, 1))
        figur(t, oturan, 210, z, s, yon=1, el="kalem", minder="#8a2a2a", **govde)
        rahle(t, 210 + int(4.2 * s), z[0], round(0.95 * s, 1))

    _spr2(no, IW, IH, kare, yk)


def sahne292():
    """'Görevi üç kelimeye sığıyor: bak, öğren, anlat.': gece, sıcak oda; elçi minderde rahlesine yazar."""
    _yazan_elci(292, 3.0, ("#3a2a22", "#4a3628", "#5a4230"), ("#1a2a4a", "#f4e0b0"), "#2a6a9a",
                ("#5a4a3a", "#4a3c2e", "#3e3226"))


# ==========================================================================
# 293 · kart 4 · İstanbul sarayı: III. Ahmed ve Damat İbrahim karşı karşıya; arkada taht
# ==========================================================================
SARAY_IC = dict(duvar=("#2a3a2e", "#344a38", "#425a46"), kemer="#1a2a1e", cini="#c8a040",
                pencere=("#3a4a6a", "#f4d8a0"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"), isik="#f8c060", hali=True)


def sahne293():
    """'Onu gönderenler bir sadrazam ve bir padişah.': saray odası; padişah (sağda) ve sadrazam karşı karşıya, ortada arkada taht."""
    ic_mekan(293, **SARAY_IC)
    yk = 2.8
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 12, IW)
        kandil(t, 140, 0, f, zincir=_kz(yk))
        kandil(t, 262, 0, (f + 0.4) % 1, zincir=_kz(yk))
        figur(t, taht, 200, arka, round(0.52 * K, 1), renk="#c8a040", ortu="#8a1e22")
        figur(t, kisi, 152, z, K, **SADRAZAM, yon=1, kol=0.05 + 0.04 * (1 + SIN(f)))
        figur(t, kisi, 250, z, K, **PADISAH, yon=-1, kol=0.02 * (1 + SIN(f + 0.5)))

    _spr2(293, IW, IH, kare, yk)


# ==========================================================================
# 294 · kart 5 · Pasarofça 1718: barış çadırları; Osmanlı ve Habsburg-Venedik murahhasları
# ==========================================================================
def sahne294():
    """Pasarofça, 1718 yazı: düz ovada iki müzakere çadırı; Osmanlı murahhası (sağda) antlaşmayı uzatır, karşısında Habsburg ve Venedik elçileri."""
    gokyuzu(294, ["#6a8ab8", "#88a4c8", "#a8bcd0", "#c8d4d4", "#e0e0cc"], None,
            [(100, 402, 22), (400, 406, 20)], ("#ffffff", "#e8ecf0", "#c0c8d8"))
    uzak(294, ["#7a8aa0", "#6c7c94"], ["#7a9a78", "#6c8c6a"], ["#8aa868", "#7c9a5c", "#6e8c52"],
         dag_y=(390, 440), tepe_y=460, ova_y=484)
    yk = 2.8
    K = s_kisi(yk)

    def ekle(img, z):
        figur(img, otag, PAY + 320, duz(586), 1.6, "#2a6a3a", "#e0b040", faz=0.0)
        figur(img, otag, PAY + 220, duz(586), 1.6, "#e8e0d0", "#c8302a", faz=0.3)

    orta(294, (528, 560), ["#7a9a58", "#6c8c4e", "#5e7e46", "#50703e", "#426236"], "#b0c888", ekle=ekle)
    on(294, ["#426236", "#50703e", "#5e7e46"], "#b0c888")

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 10, DW)
        figur(t, kisi, 132, arka, round(0.9 * K, 1), govde="#8a2a2a", bas="sapka", bas_renk="#1a1a22", sakal=None, yon=1)   # Venedik
        figur(t, kisi, 178, z, K, govde="#e8e0c8", bas="sapka", bas_renk="#2a2a2a", sakal="#5a3a22", yon=1,
              kol=0.12 + 0.04 * SIN(f), kemer="#2a2a2a")                                                                # Habsburg
        figur(t, kisi, 248, z, K, **SADRAZAM, yon=-1, silah="mektup", kol=0.38 + 0.06 * SIN(f))                        # Osmanlı

    _spr2(294, DW, DH, kare, yk)


# ==========================================================================
# 295 · kart 6-7 · Sadrazam minderde, önünde kâğıtlar; elçi ayakta talimat dinler
# ==========================================================================
def sahne295():
    """'Derdi artık asker değil, bilgi.' / 'gör ve yaz': divanhane; Damat İbrahim Paşa minderde kâğıtlarıyla, elçi karşısında ayakta."""
    ic_mekan(295, duvar=("#2e3a2a", "#3a4a34", "#4a5a40"), kemer="#1a2614", cini="#c8a040",
             pencere=("#4a6a8a", "#f4e8c0"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"), isik="#f8c060", hali=True)
    yk = 2.8
    K = s_kisi(yk)
    so = s_oturan(yk, 0.28)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 205, 0, f, zincir=_kz(yk))
        mumluk(t, 126, z, f, 3)
        figur(t, oturan, 150, z, so, yon=1, el="kalem", minder="#c8a040", **SADRAZAM)
        rahle(t, 150 + int(4.2 * so), z[0], round(0.95 * so, 1))
        kitaplar(t, 202, z[0], round(0.5 * so, 1))
        figur(t, kisi, 255, z, K, **ELCI_K, yon=-1, kol=0.04 + 0.03 * (1 + SIN(f)))

    _spr2(295, IW, IH, kare, yk)


# ==========================================================================
# 296 · kart 8 · Fransız elçisi Bonnac, Boğaz'a bakan pencereli odada mektubunu okur
# ==========================================================================
def sahne296():
    """'Fransız elçisi Bonnac da bu yolculuğu istiyor.': öğle ışığı, Boğaz'a bakan kemerli pencereler; Bonnac elinde mektup."""
    ic_mekan(296, duvar=("#4a4a5a", "#5a5a6a", "#6a6a7a"), kemer="#2a2a3a", cini="#2a4a8a",
             pencere=("#5a8ac0", "#8ab8e0"), zemin_renk=("#6a5a4a", "#5a4c3e", "#4a3e32"), isik="#f8e0a0", hali=True)
    yk = 3.0
    s = s_kisi(yk, 0.32)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 268, 0, f, zincir=_kz(yk))
        mumluk(t, 135, z, f, 2)
        figur(t, kisi, 205, z, s, **FRANSIZ, yon=1, silah="mektup", kol=0.32 + 0.06 * SIN(f), pelerin="#1a2a6a")

    _spr2(296, IW, IH, kare, yk)


# ==========================================================================
# 297 · kart 9-10 · İstanbul rıhtımı, 1720: elçi ve Said gemiye yürür; arkada yeniçeriler
# ==========================================================================
def sahne297():
    """'Elçi, Yirmisekiz Çelebi Mehmed Efendi.' / 'Yanında oğlu Said.': gri sabah, İstanbul rıhtımı; baba ve oğul sola, gemiye yürür; rıhtımda iki yeniçeri."""
    gokyuzu(297, ["#5a6478", "#6e7688", "#888c98", "#a2a2a8", "#b8b4b0"], None,
            [(120, 404, 22), (390, 400, 24)], ("#d8d8dc", "#b8b8c0", "#9898a4"))
    uzak(297, ["#6a7080", "#5e6474"], ["#707684", "#646a78"], ["#5a6a80", "#4e5e76", "#44546c"],
         dag_y=(398, 446), tepe_y=470, ova_y=500)
    yk = 2.8
    K = s_kisi(yk)

    def yeniceriler(img, z):
        for x in (326, 342):
            figur(img, kisi, PAY + x, duz(RIHTIM + 6), round(0.8 * K, 1), **YENICERI, yon=-1)

    _liman_orta(297, ("#4e5e76", "#44546c", "#3a4a62", "#324058"), "#b8b8c0", 230, 2.0, "#e8e4d8", ekle=yeniceriler)
    _bos_on(297)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 212, z, round(0.92 * K, 1), **SAID, yon=-1, adim=(f + 0.5) % 1)
        figur(t, kisi, 172, z, K, **ELCI_K, yon=-1, adim=f)

    _spr2(297, DW, DH, kare, yk)


# ==========================================================================
# 298 · kart 11 · Marsilya: sur ve damlardan veba dumanı; boş yol çitle kapalı
# ==========================================================================
def sahne298():
    """'Marsilya'da salgın başlamış.': kül rengi gök; deniz kıyısında Marsilya surları, damlardan duman; önde boş yol ve çit."""
    gokyuzu(298, ["#3a3a44", "#4e4c54", "#646068", "#7a7478", "#8e8682"], None,
            [(140, 404, 24), (410, 400, 22)], ("#a8a0a0", "#8a8288", "#6a6470"))
    uzak(298, ["#55525a", "#4a4850"], ["#5e5a5e", "#525054"], ["#4a5464", "#40495a", "#363e50"],
         dag_y=(392, 440), tepe_y=462, ova_y=486)
    yk = 2.8
    K = s_kisi(yk)
    sx = 270
    catilar = []

    def ekle(img, z):
        catilar.extend(figur(img, sehir, PAY + 150, PAY + 400, duz(590), 2.0, duvar="#9a9084",
                             golge="#6a6258", cati="#7a4034", tohum=298))

    orta(298, (534, 560), ["#6a645a", "#5c564e", "#4e4a42", "#423e38", "#36332e"], "#8a8478", ekle=ekle)
    on(298, ["#36332e", "#423e38", "#4e4a42"], "#7a7468", boy=80)
    dumanlar = _duman_noktalari(298, catilar[1::5], sx, DW, DH, DT, en=5)

    def kare(t, z, i):
        f = i / KARE
        for j, (x, y, b) in enumerate(dumanlar):
            duman(t, x, y, b, 298 + j, faz=(f + j * 0.23) % 1, renk="#5e5a60", ruzgar=0.3, genislik=1.4)
        figur(t, cit, 108, 292, z, round(0.6 * K, 1), renk="#5a4028")

    _spr2(298, DW, DH, kare, yk, esik=0.5)


# ==========================================================================
# 299 · kart 12 · Toulon karantinası (lazaret): soğuk taş oda, parmaklıklı pencere; elçi bekler ve yazar
# ==========================================================================
def sahne299():
    """'Heyet Toulon'da tutulur. Karantina.': gece, soğuk taş oda; elçi minderde tek mumun ışığında yazar."""
    _yazan_elci(299, 3.0, ("#22262e", "#2c323c", "#383e4a"), ("#0e1630", "#c8d0e0"), "#3a4a5a",
                ("#45444a", "#3a393e", "#2f2e34"), kandil_x=262, hali=False, mum=1)


# ==========================================================================
# 300 · kart 13 · Paris, Mart 1721: sokakta ve pencerelerde kalabalık; elçi ve Said atlı ilerler
# ==========================================================================
def _paris_orta(no, tohum, kalabalik_renk, sivalar=("#d8c8a8", "#c8b494", "#e0d4bc", "#b8a488"), cati="#4a4e5e",
                tas=("#8a8478", "#7c766a", "#6e685e", "#605a52", "#524e46"), kenar="#b0a898", k_kalabalik=3.4, ev_y=562):
    """Paris: taş evler sokağın sonunda (uzak, küçük ölçek), kaldırımda kalabalık (orta), atlılar önde (sprite)."""
    def ekle(img, z):
        figur(img, paris_evleri, PAY - 10, PAY + 560, duz(ev_y), 1.5, tohum=tohum, pencerede=True,
              sivalar=sivalar, cati=cati)
        kalabalik(img, duz(594), PAY + 40, PAY + 500, 13, tohum, kalabalik_renk, s=k_kalabalik, yon=1, bas="sapka")
    orta(no, (ev_y - 4, ev_y), list(tas), kenar, ekle=ekle)
    _bos_on(no)


PARIS_KALABALIK = ("#2a3a6a", "#6a2a2a", "#3a5a3a", "#5a4a3a", "#7a6a8a", "#2a2a2a")


def sahne300():
    """'Mart 1721. Paris.': bahar sabahı, taş evli Paris sokağı; pencerelerde ve kaldırımda kalabalık; elçi ve Said atlarıyla sağa ilerler."""
    gokyuzu(300, ["#7aa0c8", "#98b4d0", "#b8c8d8", "#d4d8d8", "#e8e0d0"], None,
            [(110, 402, 22), (420, 406, 20)], ("#ffffff", "#e8ecf0", "#c8d0dc"))
    uzak(300, ["#8a9ab0", "#7c8ca4"], ["#9aa8b0", "#8c9aa4"], ["#a8a898", "#9a9a8a", "#8c8c7c"],
         dag_y=(398, 446), tepe_y=466, ova_y=492)
    yk = 2.6
    _paris_orta(300, 300, PARIS_KALABALIK)
    sa = 3.8                                   # atlı: başı yazı bandının altında kalan en büyük ölçek (bant denetimi)

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 8, DW)
        figur(t, atli, 161, arka, round(0.9 * sa, 1), 1, faz=(f + 0.5) % 1, at_renk="#8a6a4a", yele="#3a2a1a",
              adim=0.4, **SAID)
        figur(t, atli, 223, z, sa, 1, faz=f, at_renk="#e8e0d0", yele="#a8a090", adim=0.4,
              **{k: v for k, v in ELCI.items()})

    _spr2(300, DW, DH, kare, yk, esik=0.7)


# ==========================================================================
# 301 · kart 14 · Elçi atının üstünde defterine yazar; arkada Parisli kalabalık
# ==========================================================================
def sahne301():
    """'Bunu yazan, elçinin kendisi.': duran atının üstünde elçi defterini tutar; arkada pencerelerde ve sokakta kalabalık."""
    gokyuzu(301, ["#7aa0c8", "#98b4d0", "#b8c8d8", "#d4d8d8", "#e8e0d0"], None,
            [(150, 404, 22)], ("#ffffff", "#e8ecf0", "#c8d0dc"))
    uzak(301, ["#8a9ab0", "#7c8ca4"], ["#9aa8b0", "#8c9aa4"], ["#a8a898", "#9a9a8a", "#8c8c7c"],
         dag_y=(398, 446), tepe_y=466, ova_y=492)
    yk = 3.0
    _paris_orta(301, 301, PARIS_KALABALIK, sivalar=("#e0d0b0", "#d0bc9c", "#c8b8a0"), ev_y=570)
    sa = 3.6

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 205, z, sa, 1, dur=True, faz=0.0, at_renk="#e8e0d0", yele="#a8a090", silah="mektup",
              kol=0.35 + 0.05 * SIN(f), **ELCI)

    _spr2(301, DW, DH, kare, yk)


# ==========================================================================
# 302 · kart 15 · Molière'in sahnesi (1670): kaftanlı, sarıklı oyuncu ve Fransız oyuncu; sahne mumları
# ==========================================================================
def _tiyatro(no, duvar, cini):
    ic_mekan(no, duvar=duvar, kemer=_ac(duvar[0], -0.4), cini=cini, pencere=None,
             zemin_renk=("#4a3a32", "#3e3029", "#322620"), isik="#f8c060", hali=False)


def sahne302():
    """'Molière elli yıl önce sahneye koymuştu.': tiyatro; ahşap sahnede 'Türk' kılığında oyuncu ile Fransız oyuncu, ön kenarda mumlar."""
    _tiyatro(302, ("#3a1a1e", "#4a2228", "#5a2a30"), "#c8a040")
    yk = 2.8
    K = s_kisi(yk, 0.30)

    def kare(t, z, i):
        f = i / KARE
        ust = figur(t, sahne_tahtasi, 200, z, round(0.55 * K, 1), f=f)
        zt = duz(ust, IW)
        figur(t, kisi, 160, zt, K, govde="#c8a040", bas="sarik", bas_renk="#f4f0e6", sakal="#2a1a12", yon=1,
              kol=0.55 + 0.35 * SIN(f), pelerin="#2a6a3a")                          # 'Türk' kılığında oyuncu
        figur(t, kisi, 240, zt, K, govde="#6a2a5a", bas="sapka", bas_renk="#1a1a22", sakal=None, yon=-1,
              kol=0.15 + 0.1 * SIN(f + 0.5))                                         # Fransız oyuncu

    _spr2(302, IW, IH, kare, yk)


# ==========================================================================
# 303 · kart 16-17 · Tuileries sarayı: alacakaranlıkta uzun cephe; elçi ve Said saraya yürür
# ==========================================================================
def sahne303():
    """'Saray Paris'te, Tuileries'de.' / '1871'de yanacak.': kızıl alacakaranlık; Tuileries cephesi, önünde heyet saraya (sağa) yürür."""
    gokyuzu(303, ["#2a2a54", "#4a3a64", "#7a4a6a", "#b0606e", "#d8826e", "#eaa47c"], None,
            [(120, 404, 20), (420, 402, 22)], ("#f0c8b8", "#d09898", "#a07080"))
    uzak(303, ["#4a3e62", "#40365a"], ["#584866", "#4c3e5c"], ["#6a5a62", "#5e4e58", "#52444e"],
         dag_y=(398, 446), tepe_y=466, ova_y=492)
    yk = 2.8
    K = s_kisi(yk)

    def ekle(img, z):
        figur(img, saray_cephesi, PAY + 60, PAY + 480, duz(584), 2.0, tas="#d8c4a8", cati="#3e4256",
              kubbe=True, pencere="#f0c070")
        for x in (PAY + 40, PAY + 500):
            figur(img, agac_kavak, x, duz(586), round(0.5 * K, 1))

    orta(303, (556, 560), ["#9a8a78", "#8a7a6a", "#7a6a5c", "#6a5a4e", "#5a4c42"], "#c8b49c", ekle=ekle)
    on(303, ["#3a3a2a", "#44442e", "#4e4e34"], "#8a8a5a", boy=70)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 162, z, round(0.92 * K, 1), **SAID, yon=1, adim=(f + 0.5) % 1)
        figur(t, kisi, 205, z, K, **ELCI_K, yon=1, adim=f)
        figur(t, kisi, 258, duz(z[0] - 10, DW), round(0.85 * K, 1), **FRANSIZ, yon=1, adim=(f + 0.25) % 1)

    _spr2(303, DW, DH, kare, yk, esik=0.7)


# ==========================================================================
# 304 · kart 18 · Tuileries taht salonu: tahtta 11 yaşındaki XV. Louis; elçi karşısında
# 305 · kart 19-20 · geniş plan: tahtın yanında naip Philippe d'Orléans, karşıda elçi ve Said
# ==========================================================================
SALON = dict(duvar=("#3a4a6a", "#4a5a7a", "#5a6a88"), kemer="#2a344a", cini="#e0b040",
             pencere=("#8ab0d8", "#c8dcf0"), zemin_renk=("#6a5a4a", "#5a4c3e", "#4a3e32"), isik="#f8d080", hali=True)
KRAL = dict(govde="#2a3a9a", bas="tac", bas_renk="#e0b040", sakal=None)


def _kral_tahtta(t, x, z, K):
    ust = figur(t, taht, x, z, round(0.62 * K, 1), renk="#e0b040", ortu="#2a3a9a")
    figur(t, oturan, x, duz(ust, t.width), round(0.62 * K, 1), yon=-1, minder="#8a1e22", **KRAL)


def sahne304():
    """'Elçi salona girer.' / 'On bir yaşında.': Tuileries salonu, mavi ve altın; sağda tahtta çocuk kral, solda elçi."""
    ic_mekan(304, **SALON)
    yk = 3.0
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, zincir=_kz(yk))
        _kral_tahtta(t, 238, z, K)
        figur(t, kisi, 150, z, K, **ELCI_K, yon=1, kol=0.05 + 0.04 * (1 + SIN(f)))

    _spr2(304, IW, IH, kare, yk)


def sahne305():
    """'Ülkeyi onun adına naip yönetiyor.' / 'bir çocuğun karşısında duruyor': geniş plan; ortada tahtta kral, solunda naip, sağda elçi."""
    ic_mekan(305, **SALON)
    yk = 2.6
    K = s_kisi(yk, 0.30)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 150, 0, f, zincir=_kz(yk))
        kandil(t, 250, 0, (f + 0.5) % 1, zincir=_kz(yk))
        _kral_tahtta(t, 180, z, K)
        figur(t, kisi, 124, z, K, **NAIP, yon=1, kol=0.03 * (1 + SIN(f)))
        figur(t, kisi, 252, z, K, **ELCI_K, yon=-1, kol=0.03 * (1 + SIN(f + 0.5)))

    _spr2(305, IW, IH, kare, yk)


# ==========================================================================
# 306 · kart 21 · Palais-Royal operası: sahnede iki şarkıcı; önde elçi seyreder
# ==========================================================================
def sahne306():
    """'Palais-Royal'de opera seyreder.': opera salonu; sağda sahnede iki şarkıcı, solda önde elçi izler."""
    _tiyatro(306, ("#2a1a2e", "#3a2240", "#4a2a50"), "#e0b040")
    yk = 2.8
    K = s_kisi(yk, 0.30)

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 14, IW)
        ust = figur(t, sahne_tahtasi, 238, arka, round(0.42 * K, 1), f=f)
        zt = duz(ust, IW)
        figur(t, kisi, 220, zt, round(0.85 * K, 1), govde="#e8d8f0", bas="tac", bas_renk="#e0b040", sakal=None,
              yon=1, kol=0.45 + 0.25 * SIN(f), kadin=True, pelerin="#8a2a6a")       # şarkıcı
        figur(t, kisi, 262, zt, round(0.85 * K, 1), govde="#2a5a8a", bas="migfer", bas_renk="#c8c8d0", sakal=None,
              yon=-1, kol=0.35 + 0.25 * SIN(f + 0.5), pelerin="#c8a040")            # kahraman kılığında şarkıcı
        figur(t, kisi, 140, z, K, **ELCI_K, yon=1)

    _spr2(306, IW, IH, kare, yk, esik=0.7)


# ==========================================================================
# 307 · kart 22 · Paris Rasathanesi, gece: dürbün ve çeyrek daire; astronom gösterir, elçi bakar
# ==========================================================================
def sahne307():
    """'Gökyüzünü ölçen aletleri görür.': yıldızlı gece; arkada rasathane binası, önde dürbün ve çeyrek daire; astronom ve elçi."""
    gokyuzu(307, ["#0a0e24", "#121a38", "#1c284c", "#283860", "#344670"], None,
            [(430, 404, 18)], ("#5a6a8a", "#44547a", "#2e3e62"), yildiz=120)
    uzak(307, ["#1a2240", "#151c38"], ["#1e2846", "#18203e"], ["#1c2638", "#161e30", "#121a28"],
         dag_y=(440, 470), tepe_y=478, ova_y=494)
    _yildiz_ekle(307, 70, 384, 446)
    yk = 2.8
    K = s_kisi(yk)

    def ekle(img, z):
        figur(img, saray_cephesi, PAY + 150, PAY + 400, duz(584), round(0.4 * K, 1), tas="#8a8a9a", cati="#2a2e40",
              kubbe=False, pencere="#e8c070")

    orta(307, (556, 560), ["#2a3038", "#242a32", "#1e242c", "#1a1e26", "#161a20"], "#5a6070", ekle=ekle)
    on(307, ["#121820", "#161e28", "#1a2430"], "#3a4a5a", boy=60)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kadran, 142, z, round(0.55 * K, 1))
        figur(t, teleskop, 200, z, round(0.6 * K, 1), yon=1, aci=0.5)
        figur(t, kisi, 170, z, round(0.95 * K, 1), govde="#2a2a3a", bas="sapka", bas_renk="#1a1a1a", sakal=None,
              yon=1, kol=0.55 + 0.08 * SIN(f))                                          # astronom dürbünü gösterir
        figur(t, kisi, 256, z, K, **ELCI_K, yon=-1, kol=0.03 * (1 + SIN(f)))

    _spr2(307, DW, DH, kare, yk, esik=0.7)


# ==========================================================================
# 308 · kart 23-24 · Versailles bahçeleri: fıskiyeli havuz, budanmış ağaçlar; elçi defterine not alır
# ==========================================================================
def sahne308():
    """'Versailles'a da gider; gezgin olarak.' / 'Bahçeler, havuzlar, çeşmeler.': parlak öğle; uzakta saray, önde fıskiyeli havuz; elçi not alır."""
    gokyuzu(308, ["#5a8ac8", "#78a2d4", "#98b8dc", "#b8cce0", "#d4dce0"], None,
            [(100, 402, 22), (420, 404, 24)], ("#ffffff", "#eef2f8", "#c8d4e4"))
    uzak(308, ["#7a90b0", "#6c82a4"], ["#7a9a80", "#6c8c72"], ["#7aa060", "#6c9254", "#5e844a"],
         dag_y=(400, 448), tepe_y=468, ova_y=490)
    yk = 2.8
    K = s_kisi(yk)

    def ekle(img, z):
        figur(img, saray_cephesi, PAY + 120, PAY + 420, duz(574), round(0.3 * K, 1), tas="#e0d4bc", cati="#4a5068",
              kubbe=False, pencere="#4a5a6a")
        for x in (150, 186, 354, 390):
            figur(img, agac_kavak, PAY + x, duz(590), 1.4)

    orta(308, (566, 570), ["#c8b890", "#bcac84", "#b0a078", "#a4946c", "#988860"], "#e8dcb8", ekle=ekle)
    on(308, ["#4a6a3a", "#567a42", "#62884a"], "#a8c888", boy=70)

    def kare(t, z, i):
        f = i / KARE
        figur(t, havuz, 158, z, round(0.48 * K, 1), faz=f)
        figur(t, kisi, 262, z, K, **ELCI_K, yon=-1, silah="mektup", kol=0.30 + 0.06 * SIN(f, 2))

    _spr2(308, DW, DH, kare, yk, esik=0.7)


# ==========================================================================
# 309 · kart 26 · Kâğıthane, 1722: Sâdâbâd köşkü yapım hâlinde; işçiler
# ==========================================================================
def sahne309():
    """'Kâğıthane'de Sâdâbâd Kasrı ve bahçesi yükseliyor.': bahar sabahı; dere kıyısında iskeleli köşk, önde taş ve kalas taşıyan işçiler."""
    gokyuzu(309, ["#6a90c0", "#88a8cc", "#a8c0d4", "#c8d4d4", "#e4e0c8"], None,
            [(120, 404, 22), (410, 400, 20)], ("#ffffff", "#eef2f4", "#c8d4dc"))
    uzak(309, ["#7a90a8", "#6c829c"], ["#78986c", "#6a8a60"], ["#78a058", "#6a924e", "#5e8446"],
         dag_y=(396, 446), tepe_y=466, ova_y=488)
    yk = 2.8
    K = s_kisi(yk)

    def ekle(img, z):
        d = ImageDraw.Draw(img)
        d.rectangle([0, 560, GW, 572], fill=hex2("#5a8ab0"))                         # Kâğıthane deresi
        for k in range(0, GW, 9):
            piksel(img, k, 563 + (k // 9) % 3 * 3, hex2("#a8cce0"))
        figur(img, kosk, PAY + 270, duz(586), round(0.4 * K, 1), iskele=True)

    orta(309, (548, 552), ["#7aa058", "#6c924e", "#5e8446", "#50763e", "#426836"], "#b0d080", ekle=ekle)
    on(309, ["#426836", "#50763e", "#5e8446"], "#b0d080")

    def kare(t, z, i):
        f = i / KARE
        renk = ("#5a3a22", "#6a5a2a", "#6a4a2a")
        for j, x in enumerate((140, 205, 268)):
            ph = (f + j * 0.33) % 1
            figur(t, kisi, x, z, K, govde=renk[j], bas="bork" if j != 1 else "sarik", bas_renk="#ece6d8" if j == 1 else "#5a3a22",
                  sakal="#2a1a12" if j == 1 else None, yon=1 if j < 2 else -1,
                  silah="kurek" if j == 0 else ("mektup" if j == 1 else "kazma"),
                  kol=(0.5 + 0.4 * SIN(ph)) if j != 1 else 0.3)

    _spr2(309, DW, DH, kare, yk)


# ==========================================================================
# 310 · kart 27-28 · Kâğıthane mesiresi: havuz, laleler, mesire çadırları; elçi kıyıda
# ==========================================================================
def sahne310():
    """'Paris bahçelerinin izi mi?' / 'mesire geleneği zaten köklü': ikindi; ağaçlar arasında mesire çadırları, önde havuz ve laleler, elçi kıyıda."""
    gokyuzu(310, ["#7a90c0", "#98a8c8", "#c0b8c0", "#e0c8b0", "#f0d8b0"], None,
            [(110, 404, 22), (420, 402, 20)], ("#fff8ec", "#f4dcc8", "#d8b0a8"))
    uzak(310, ["#8a8aa8", "#7c7c9c"], ["#8aa080", "#7c9272"], ["#88a860", "#7a9a54", "#6c8c4a"],
         dag_y=(396, 446), tepe_y=466, ova_y=488)
    yk = 2.8
    K = s_kisi(yk)

    def ekle(img, z):
        figur(img, agac, PAY + 170, duz(584), 1.2, tohum=31)
        figur(img, otag, PAY + 222, duz(586), 1.5, "#c8302a", "#e0b040", faz=0.1)
        figur(img, otag, PAY + 318, duz(586), 1.5, "#2a6a9a", "#f0e8d0", faz=0.6)
        figur(img, agac, PAY + 372, duz(584), 1.2, tohum=32)

    orta(310, (530, 560), ["#7aa058", "#6c924e", "#5e8446", "#50763e", "#426836"], "#b8d888", ekle=ekle)
    on(310, ["#426836", "#50763e", "#5e8446"], "#b8d888")

    def kare(t, z, i):
        f = i / KARE
        figur(t, havuz, 165, z, round(0.48 * K, 1), faz=f)
        for j, x in enumerate((122, 136, 206, 220)):
            figur(t, cicek, x, z, round(0.32 * K, 1), faz=(f + j * 0.3) % 1, renk="#d8302a", orta="#f4d24a")
        figur(t, kisi, 262, z, K, **ELCI_K, yon=-1, kol=0.03 * (1 + SIN(f)))

    _spr2(310, DW, DH, kare, yk, esik=0.7)


# ==========================================================================
# 311 · kart 29 · 1727: ferman ve fetva. Şeyhülislam fetvayı tutar, kâtip fermanı yazar
# ==========================================================================
def sahne311():
    """'Padişahın yazılı onayı, şeyhülislamın fetvası': saray kalemi; ayakta şeyhülislam elinde fetva, minderde kâtip fermanı yazar."""
    ic_mekan(311, duvar=("#3a2e22", "#4a3a2a", "#5a4632"), kemer="#22180e", cini="#2a6a5a",
             pencere=("#2a3a5a", "#f4e0b0"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"), isik="#f8c060", hali=True)
    yk = 2.8
    K = s_kisi(yk)
    so = s_oturan(yk, 0.28)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 205, 0, f, zincir=_kz(yk))
        mumluk(t, 276, z, f, 3)
        figur(t, kisi, 150, z, K, **SEYHULISLAM, yon=1, silah="mektup", kol=0.35 + 0.05 * SIN(f))
        figur(t, oturan, 240, z, so, yon=-1, el="kalem", minder="#8a2a2a", govde="#3a5a8a", bas="sarik",
              bas_renk="#ece6d8", sakal="#2a1a12")
        rahle(t, 240 - int(4.2 * so), z[0], round(0.95 * so, 1))

    _spr2(311, IW, IH, kare, yk)


# ==========================================================================
# 312 · kart 30 · Osmanlı'da matbaa zaten var: üç ayrı baskı tezgâhı ve baskıcıları
# 313 · kart 31 · Müteferrika kendi tezgâhında
# 314 · kart 32-33 · Said belgeyle gelir, Müteferrika ilk basılan sayfayı tutar; yanda kitap yığını
# ==========================================================================
ATOLYE = dict(duvar=("#3a3026", "#4a3e30", "#5a4a3a"), kemer="#241c14", cini="#6a4a2a",
              pencere=("#c8b890", "#fff4d8"), zemin_renk=("#5a5046", "#4c443a", "#40382f"), isik="#f8d890", hali=False)


def _baski_ve_baskici(t, px, z, sp, bx, sk, f, kisi_kw):
    """Tezgâh + baskıcı: baskıcı tezgâhın sağında, sola bakar; kol (vida→el) her karede elin konumuna bağlanır."""
    bas = (1 - math.cos(f * 2 * math.pi)) / 2
    kol = 0.15 + 0.45 * bas
    vida = figur(t, baski_tezgahi, px, z, sp, faz=f)
    figur(t, kisi, bx, z, sk, yon=-1, kol=kol, **kisi_kw)
    _baski_kolu(t, vida, _el(bx, z, sk, -1, kol))


def sahne312():
    """'Yahudi, Ermeni, Rum matbaaları yüz yıllardır çalışıyor.': aydınlık atölye; arkada üç ayrı baskı tezgâhı, önde basılı sayfalarıyla üç baskıcı."""
    ic_mekan(312, **ATOLYE)
    yk = 2.6
    K = s_kisi(yk, 0.30)
    sp = round(0.42 * K, 1)
    baskicilar = (dict(govde="#3a3a4a", bas="kalpak", bas_renk="#2a2a2a", sakal="#2a1a12", kemer=None),
                  dict(govde="#6a2a2a", bas="takke", bas_renk="#e0d8c0", sakal="#3a2a1a", kemer=None),
                  dict(govde="#2a4a6a", bas="kalpak", bas_renk="#5a3a22", sakal="#2a1a12", kemer=None))

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 14, IW)
        kandil(t, 200, 0, f, zincir=_kz(yk))
        for j, x in enumerate((134, 200, 266)):                                     # üç ayrı tezgâh (arkada)
            figur(t, baski_tezgahi, x, arka, sp, faz=(f + j * 0.33) % 1)
        for j, (x, yon) in enumerate(((140, 1), (204, -1), (262, -1))):               # baskıcılar basılı sayfa tutar
            figur(t, kisi, x, z, K, yon=yon, silah="mektup", kol=0.30 + 0.05 * SIN(f + j * 0.3), **baskicilar[j])

    _spr2(312, IW, IH, kare, yk, esik=0.7)


def sahne313():
    """'Türkçe basan bir matbaa. Kurucusu İbrahim Müteferrika.': atölye; Müteferrika tezgâhın kolunu çeker, yanda basılmış sayfalar."""
    ic_mekan(313, **ATOLYE)
    yk = 2.8
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 280, 0, f, zincir=_kz(yk))
        _baski_ve_baskici(t, 175, z, round(0.66 * K, 1), 175 + int(15 * 0.66 * K), K, f, MUTEFERRIKA)

    _spr2(313, IW, IH, kare, yk, esik=0.7)


def sahne314():
    """'İzin sürecinde bir ad daha geçer: Said.' / 'Vankulu Lügati': atölye; solda Said elinde belge, sağda Müteferrika ilk sayfayı tutar, arkada tezgâh."""
    ic_mekan(314, **ATOLYE)
    yk = 2.8
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 12, IW)
        kandil(t, 140, 0, f, zincir=_kz(yk))
        figur(t, baski_tezgahi, 250, arka, round(0.5 * K, 1), faz=0.0)
        top = figur(t, masa, 205, z, round(0.55 * K, 1), ortu="#6a2a2a")
        kitaplar(t, 205, top, round(0.42 * K, 1))
        figur(t, kisi, 150, z, K, **SAID_1742, yon=1, silah="mektup", kol=0.30 + 0.04 * SIN(f))
        figur(t, kisi, 258, z, K, **MUTEFERRIKA, yon=-1, silah="mektup", kol=0.22 + 0.04 * SIN(f + 0.5))

    _spr2(314, IW, IH, kare, yk)


# ==========================================================================
# 315 · kart 34 · Belge yok; elçi görevini yapmıştır: boş raf, tek mum; elçi pencere önünde (orta yaşlı)
# ==========================================================================
def sahne315():
    """'Bunu kanıtlayan bir belge yok.' / 'Baktı, öğrendi, anlattı.': akşam; boş raf, tek mum, elçi pencereye dönük durur."""
    ic_mekan(315, duvar=("#2a2a34", "#343440", "#40404c"), kemer="#16161e", cini="#3a4a6a",
             pencere=("#4a4a7a", "#f0c890"), zemin_renk=("#4a4440", "#3e3834", "#322e2c"), isik="#e8b060", hali=False)
    yk = 2.8
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 205, 0, f, zincir=_kz(yk))
        figur(t, kitap_rafi, 148, z, round(0.6 * K, 1), dolu=False)
        mumluk(t, 178, z, f, 1)
        figur(t, kisi, 255, z, K, **ELCI_K, yon=1, kol=0.02 * (1 + SIN(f)))

    _spr2(315, IW, IH, kare, yk)


# ==========================================================================
# 316 · kart 35 · Eylül 1730, Patrona Halil: gece sokakta meşaleli kalabalık, yanan ateş
# ==========================================================================
def sahne316():
    """'Ama. Eylül 1730. Patrona Halil ayaklanır.': gece, İstanbul; meşaleli kalabalık sağa yürür, yerde ateş, damlardan duman."""
    gokyuzu(316, ["#0e0a1a", "#1a1226", "#2a1a2e", "#4a2230", "#6a2a2a"], None,
            [(130, 404, 20)], ("#6a3a3a", "#4a2a30", "#2a1a24"), yildiz=40)
    uzak(316, ["#1e1626", "#181220"], ["#24182a", "#1e1424"], ["#2a1a22", "#22161c", "#1a1016"],
         dag_y=(400, 448), tepe_y=468, ova_y=490)
    yk = 2.8
    K = s_kisi(yk)
    sx = 270
    catilar = []

    def ekle(img, z):
        catilar.extend(figur(img, sehir, PAY + 140, PAY + 400, duz(590), 2.0, duvar="#3a2e30",
                             golge="#241c20", cati="#4a2a24", tohum=316))
        kalabalik(img, duz(592), PAY + 150, PAY + 420, 16, 316, ("#2a2026", "#3a2a2a", "#2a2a3a"),
                  s=round(0.7 * K, 1), yon=1)

    orta(316, (556, 560), ["#2a2022", "#241a1c", "#1e1618", "#181214", "#120e10"], "#6a3a2a", ekle=ekle)
    _bos_on(316)
    dumanlar = _duman_noktalari(316, catilar[3::7], sx, DW, DH, DT, en=3)

    def kare(t, z, i):
        f = i / KARE
        for j, (x, y, b) in enumerate(dumanlar):
            duman(t, x, y, b, 316 + j, faz=(f + j * 0.3) % 1, renk="#3a2a2a", ruzgar=0.3)
        ates(t, 138, z, f, round(0.5 * K, 1))
        renk = ("#5a2a22", "#3a3a4a", "#6a4a2a")
        bas = (("kalpak", "#3a2a1a"), ("sarik", "#c8c0b0"), ("kalpak", "#5a3a22"))
        for j, x in enumerate((168, 208, 248)):
            figur(t, kisi, x, z, K, govde=renk[j], bas=bas[j][0], bas_renk=bas[j][1],
                  sakal="#2a1a12", yon=1, adim=(f + j * 0.37) % 1, silah="mesale", kol=0.0)

    _spr2(316, DW, DH, kare, yk, esik=0.7)


# ==========================================================================
# 317 · kart 36-37 · Boş taht ve devrilmiş kavuk (ölüm gösterilmez)
# ==========================================================================
def sahne317():
    """'Sadrazam öldürülür.' / 'Üçüncü Ahmed tahttan indirilir.': karanlık saray odası; boş taht, yerde devrilmiş kavuk, sallanan kandil."""
    ic_mekan(317, duvar=("#1a2420", "#22302a", "#2c3a32"), kemer="#0e1612", cini="#8a6a2a",
             pencere=("#0e1428", "#b0b8d0"), zemin_renk=("#3e3830", "#342e28", "#2a2620"), isik="#c89040", hali=True)
    yk = 2.8
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 268, 0, f, zincir=_kz(yk))
        mumluk(t, 128, z, f, 1)
        figur(t, taht, 188, z, round(0.62 * K, 1), renk="#c8a040", ortu="#8a1e22")
        figur(t, kavuk_yerde, 250, z, round(0.85 * K, 1))

    _spr2(317, IW, IH, kare, yk, esik=0.6)


# ==========================================================================
# 318 · kart 38-39 · Lale Devri kapanır: solan laleler; elçi uzaklaşır (sola, geride kalan)
# ==========================================================================
def sahne318():
    """'Lale Devri ... kapanır.' / 'Peki elçi? ... Kaynaklar ayrışıyor.': mor alacakaranlık; önde solgun laleler, patikada elçi sola uzaklaşır."""
    gokyuzu(318, ["#1e1e40", "#3a2e58", "#6a4268", "#9a5a6e", "#c07a70", "#d89a7c"], None,
            [(120, 404, 20), (420, 402, 22)], ("#e8c0b8", "#c098a0", "#906c84"))
    uzak(318, ["#3e3a5e", "#363254"], ["#4a4058", "#40384e"], ["#4a4a48", "#40403e", "#363634"],
         dag_y=(396, 446), tepe_y=466, ova_y=488)
    yk = 2.8
    K = s_kisi(yk)

    def ekle(img, z):
        figur(img, agac, PAY + 170, duz(584), 1.15, yaprak=("#2a3a2a", "#344a32", "#40583a"),
              govde="#2a1c14", tohum=40)
        figur(img, agac, PAY + 372, duz(584), 1.1, yaprak=("#2a3a2a", "#344a32", "#40583a"),
              govde="#2a1c14", tohum=41)
        for j, x in enumerate(range(PAY + 150, PAY + 400, 13)):                         # solgun laleler: önde, yere dikili
            figur(img, cicek, x, duz(684 + (j % 3) * 6), round(0.34 * K, 1), faz=0.15 + 0.1 * (j % 4),
                  renk=("#8a3a3a", "#7a3a4a", "#9a5a4a")[j % 3], orta="#6a5a3a")

    orta(318, (532, 560), ["#3e4a36", "#36402e", "#2e3828", "#283022", "#20281c"], "#6a7a5a", ekle=ekle)
    on(318, ["#20281c", "#283022", "#2e3828"], "#6a7a5a", boy=60)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 205, z, K, **ELCI_K, yon=-1, adim=f)

    _spr2(318, DW, DH, kare, yk)


# ==========================================================================
# 319 · kart 40-41 · Kitapçı dükkânı: 1757 Fransızca çeviri ve 1866 İstanbul baskısı, iki masa iki yığın
# ==========================================================================
def sahne319():
    """'Kitap 1757'de Fransızcaya çevrilir.' / '1866'yı bekler.': kitapçı dükkânı; dolu raflar, iki masada iki kitap yığını, kitapçı bir kitap tutar."""
    ic_mekan(319, duvar=("#3a3226", "#4a4030", "#5a4e3a"), kemer="#221c12", cini="#2a4a6a",
             pencere=("#8aa0c0", "#fff4d8"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"), isik="#f8d080", hali=False)
    yk = 2.8
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 12, IW)
        kandil(t, 200, 0, f, zincir=_kz(yk))
        figur(t, kitap_rafi, 140, arka, round(0.5 * K, 1), dolu=True, tohum=3)
        figur(t, kitap_rafi, 258, arka, round(0.5 * K, 1), dolu=True, tohum=4)
        for x, ortu, s_ in ((206, "#2a3a8a", 0.72), (258, "#8a1e22", 0.62)):              # Fransa 1757 (mavi), İstanbul 1866 (kırmızı)
            top = figur(t, masa, x, z, round(0.42 * K, 1), ortu=ortu)
            kitaplar(t, x, top, round(s_ * K, 1))
        figur(t, kisi, 148, z, K, govde="#5a4a3a", bas="sapka", bas_renk="#1a1a1a", sakal=None, yon=1,
              silah="mektup", kol=0.28 + 0.04 * SIN(f))

    _spr2(319, IW, IH, kare, yk)


# ==========================================================================
# 320 · kart 42-43 · 1742: Said, bu kez elçi olarak, aynı Paris sokağında yalnız atlı
# ==========================================================================
def sahne320():
    """'1742. Paris'e bir Osmanlı elçisi daha gelir. Adı Said.': altın ikindi, aynı Paris sokağı; Said tek başına atıyla sağa ilerler."""
    gokyuzu(320, ["#6a7ab0", "#9a98b8", "#c8b0b0", "#e8c8a8", "#f4dcb0"], None,
            [(110, 402, 22), (420, 406, 20)], ("#fff4e4", "#f0d4c0", "#d0a8a0"))
    uzak(320, ["#8a8aa8", "#7c7c9c"], ["#9a98a8", "#8c8a9c"], ["#b0a490", "#a29682", "#948874"],
         dag_y=(398, 446), tepe_y=466, ova_y=492)
    yk = 2.6
    _paris_orta(320, 300, PARIS_KALABALIK, sivalar=("#e8d0a8", "#d8bc94", "#f0dcb8", "#c8ac88"))
    sa = 3.9

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 205, z, sa, 1, faz=f, at_renk="#8a6a4a", yele="#3a2a1a", adim=0.4, **SAID_1742)

    _spr2(320, DW, DH, kare, yk)


# ==========================================================================
# 321 · kart 44-45 + kapanış · Said, babası gibi, gece defterini açar
# ==========================================================================
def sahne321():
    """'Bakar, öğrenir, anlatır.' / 'Sen ne dersin?': gece; Said minderde rahlesine yazar (292'deki babasının aynası)."""
    _yazan_elci(321, 3.0, ("#2a2230", "#362c3c", "#44384a"), ("#0e1430", "#f4f8ff"), "#6a2a4a",
                ("#4a3c38", "#3e322e", "#322824"), govde=SAID_1742)


SAHNELER = {n: globals()[f"sahne{n}"] for n in range(290, 322)}

if __name__ == "__main__":
    for n in ([int(a) for a in sys.argv[1:]] or sorted(SAHNELER)):
        SAHNELER[n]()
        print(f"sahne {n} çizildi")
