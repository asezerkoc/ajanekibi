"""Haritayı Çizen Adam: Piri Reis'in haritaları ve idamı (1513-1554). Piksel Tarih (@pikseltarihim), sahneler 330-367.
Grafikerin tarifi: teslimler/gece/ara/piri-reis/5-grafik.md. Kalıp: video/piksel/cem_sultan.py (ölçek ve kadraj
yardımcıları oradan alınır), celebi_mehmed_paris.py (yazı bandı denetimi, masa ve kitap rafı kopyalandı),
takiyuddin_rasathanesi.py (cami silüeti, gemi denetimi kopyalandı), kalender.py (taht, rahle, kitaplar).
Yön dili: sağ = sefere, doğuya giden; sol = eve dönüş, geride kalan.
Kuşbakışı masa sahneleri (336, 337, 361, 363, 365, 367): zemin = masa düzlemi; parşömen, kaynak haritalar, hokka ve
kalem masanın üstünde yatar (gölgeleri masaya düşer); masa orta planda ve sprite'la aynı paralakstadır (kamera 0).
Kullanım: python3 -I video/piksel/piri_reis.py [sahne numaraları]"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw  # noqa: E402

from ciz import _ac, _esik, duman, duz_zemin, figur, gunes, hex2, piksel, temas_golgesi, temel, yeni, zemin_y  # noqa: E402
from ciz import W, H, sprite_sayfasi  # noqa: E402
from sahneler import GW, duz, gokyuzu, kaydet, on, orta, uzak  # noqa: E402
from timur_figur import anadolu_kalesi, atli, deve, gemi, kisi, koy_evleri, otag, oturan  # noqa: E402
from timur import ic_mekan, kandil, lamba, mumluk  # noqa: E402
from kalender import kitaplar, rahle, taht  # noqa: E402
from cem_sultan import _bb, _kz, _spr, s_kisi, s_oturan  # noqa: E402

KARE = 24      # sprite kare sayısı (SKILL.md)
PAY = 135      # orta/ön plan yan payı (SKILL.md)
SIN = lambda f, k=1: math.sin(f * 2 * math.pi * k)  # noqa: E731
COS = lambda f, k=1: math.cos(f * 2 * math.pi * k)  # noqa: E731

# Dış mekân sprite'ı (brif: h 170-230), iç mekân sprite'ı (brif: h 300), deniz sprite'ı (su sprite'ın içinde)
DW, DH, DT = 400, 220, 632
IW, IH, IT = 400, 300, 634
SW, SH, ST = 400, 300, 632
SU = SH - 18          # deniz sprite'ında su çizgisi (yerel); dünya y = 614


def _u(v, s):
    return max(1, int(round(v * s)))


# Kişiler (renk dili bütün videoda aynı kalır)
PIRI_GENC = dict(govde="#2a5a6a", bas="sarik", bas_renk="#f2ece0", sakal="#2a1a12")      # deniz yeşili kaftan
PIRI_1513 = dict(govde="#2a5a6a", bas="sarik", bas_renk="#f2ece0", sakal="#5a4632")
PIRI_KAPTAN = dict(PIRI_1513, pelerin="#1e3a5a")                                          # 1524: kaptan pelerini
PIRI_YASLI = dict(govde="#2a5a6a", bas="sarik", bas_renk="#f2ece0", sakal="#ece8e0", pelerin="#1e3a5a")
PIRI_YASLI_O = {k: v for k, v in PIRI_YASLI.items() if k != "pelerin"}                   # oturan/diz figürü için
KEMAL = dict(govde="#7a2a1e", bas="sarik", bas_renk="#f2ece0", sakal="#3a2a1a", pelerin="#4a1a14")
YAVUZ = dict(govde="#8a1e22", bas="sarik", bas_renk="#f8f4ea", sakal=None)
IBRAHIM = dict(govde="#2a6a3a", bas="sarik", bas_renk="#f8f4ea", sakal="#2a1a12", pelerin="#c8a040")
KANUNI = dict(govde="#3a2a6a", bas="sarik", bas_renk="#f8f4ea", sakal="#3a2a1a")
CAVUS = dict(govde="#8a2a2a", bas="bork", bas_renk="#ece6d8", sakal="#2a1a12")
KUBAD = dict(govde="#6a4a1a", bas="sarik", bas_renk="#f2ece0", sakal="#1a1a1a")
SEYDI = dict(govde="#2a3a6a", bas="sarik", bas_renk="#f2ece0", sakal="#2a1a12", pelerin="#6a1e22")
SEYDI_O = {k: v for k, v in SEYDI.items() if k != "pelerin"}
ESIR = dict(govde="#8a7a5a", bas="takke", bas_renk="#6a4a2a", sakal="#6a4a2a", kemer=None)  # İspanyol esir: başı açık
EDHEM = dict(govde="#2a2a34", bas="sapka", bas_renk="#3a3a40", sakal="#d8d0c8", kemer=None)
DEISSMANN = dict(govde="#4a4038", bas="takke", bas_renk="#e0dcd4", sakal="#e0dcd4", kemer=None)
KAHLE = dict(govde="#3a4a3a", bas="takke", bas_renk="#5a4a3a", sakal=None, kemer=None)
OHLMEYER = dict(govde="#4a5a7a", bas="kasket", bas_renk="#34405a", sakal=None, kemer="#c8c8d0")
HAPGOOD = dict(govde="#5a4a3a", bas="takke", bas_renk="#9a9a98", sakal=None, kemer=None)

YELKEN = "#e8dcc0"     # Osmanlı kadırgası
GOVDE = "#4a2e1e"


# --------------------------------------------------------------------------
# Yazı bandı denetimi (celebi_mehmed_paris.py'den; odakY desteği eklendi). Remotion kamerası sahneyi (sx, odakY;
# verilmezse taban-12) çevresinde yakin..1.06·yakin büyütür; ekran yazısı ekran ızgarasında yaziY/2'den (varsayılan
# 150) yazının alt kenarına kadar durur. Bu bant dünya y'sine çevrilir; sprite'ta ve orta planda bu satırlarda görünür
# sütunlarda opak piksel varsa (1-2 piksellik kandil zinciri hariç) figür/yapı yazıya giriyor demektir: betik durur.
# Kartlar, yakin, yaziY ve odakY PiriReis.tsx'ten okunur (tek kaynak).
# --------------------------------------------------------------------------
TSX = Path(__file__).parents[1] / "src" / "sahneler" / "PiriReis.tsx"


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
        od = re.search(r"odakY: (\d+)", b)
        ust = int(yy.group(1)) if yy else 300
        alt = 0
        for m in re.finditer(r"satirlar: \[([^\]]*)\], sure: [\d.]+(?:, boy: (\d+))?", b):
            sat = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
            boy = int(m.group(2) or 92)
            sig = min(boy, math.floor(950 / (max(len(x) for x in sat) * 0.46)))
            alt = max(alt, (ust + len(sat) * sig * 1.12 + 8) / 2)          # ekran px → ızgara
        sonuc.setdefault(no, []).append((yk, alt, ust / 2, int(od.group(1)) if od else None))
    return sonuc


def _bant_denetimi(no, w, h, taban, pay=4, orta_bant=True):
    bantlar = _tsx_bantlari().get(no, [])
    pub = Path(__file__).parents[1] / "public"
    spr = Image.open(pub / f"sahne{no}-karakter.png").convert("RGBA").getchannel("A")
    ort = Image.open(pub / f"sahne{no}-orta.png").convert("RGBA").getchannel("A")
    for yk, alt, ust, od in bantlar:
        o = od or taban - 12
        for z in (yk, yk * 1.06):
            y0, y1 = int(o - (o - ust) / z), int(o - (o - alt) / z) + pay
            yar = 270 / z
            for i in range(0, KARE, 3):
                for y in range(max(y0, taban - h), y1 + 1):
                    ly = y - (taban - h)
                    satir = spr.crop((i * w + int(w / 2 - yar), ly, i * w + int(w / 2 + yar), ly + 1))
                    if sum(satir.histogram()[1:]) > 2:
                        raise RuntimeError(f"Sahne {no}: sprite (kare {i}) yazı bandına giriyor: dünya y {y} "
                                           f"(bant {y0}-{y1}, yakin {z:.2f}); figürü küçült ya da alçalt")
            if not orta_bant:
                continue
            for y in range(y0, y1 + 1):
                n = sum(ort.crop((PAY + int(270 - yar - 30), y, PAY + int(270 + yar + 30), y + 1)).histogram()[1:])
                if n > 2:
                    raise RuntimeError(f"Sahne {no}: orta plandaki yapı yazı bandına giriyor: y {y} (bant {y0}-{y1})")


def _spr2(no, w, h, kare, yakin, esik=0.75, taban=None, orta_bant=True):
    """cem_sultan._spr (kadraj + taban denetimi) + yazı bandı denetimi."""
    _spr(no, w, h, kare, yakin, esik)
    _bant_denetimi(no, w, h, taban or {DH: DT, IH: IT}.get(h, IT), orta_bant=orta_bant)


def _bant_alt(no, taban=DT, pay=8):
    """Sahnenin bütün kartları ve yakınlaşma için yazı bandının en alt dünya y'si (+pay)."""
    return max((int((od or taban - 12) - ((od or taban - 12) - alt) / (yk * 1.06)) + pay
                for yk, alt, _, od in _tsx_bantlari().get(no, [])), default=0)


def _bos_on(no):
    """Ön plan boş (iç mekân, liman, güverte): çimen tutamı yok."""
    kaydet(yeni(GW, H), f"sahne{no}-on.png")


def _yildiz_ekle(no, adet, y0, y1, tohum=0):
    """Gece: görünür gök şeridine (y0-y1) seyrek yıldız ekler (gokyuzu() yıldızları y 300'ün üstüne koyar)."""
    yol = Path(__file__).parents[1] / "public" / f"sahne{no}-gokyuzu.png"
    img = Image.open(yol).convert("RGBA")
    rnd = random.Random(no + tohum)
    for _ in range(adet):
        x, y = rnd.randrange(540), rnd.randrange(y0, y1)
        piksel(img, x, y, hex2(rnd.choice(("#fff8e0", "#d8e0f8", "#a8b4d8"))))
    img.save(yol)


def _hava(no, yogunluk=300, renk="#b8c8e0", egim=0.3, parlama=(5, 6, 17)):
    """Yağmur katmanı (timur.hava kalıbı). Şimşek zikzağı çizilmez (yazı bandını keserdi); şimşek, bütün kareye
    düşen soluk beyaz bir parlamayla gösterilir."""
    rnd = random.Random(no)
    taneler = [(rnd.randrange(W), rnd.randrange(H), rnd.choice((1, 2))) for _ in range(yogunluk)]

    def kare(t, z, i):
        f = i / KARE
        for x0, y0, hiz in taneler:
            y = (y0 + f * H * hiz) % H
            x = (x0 - f * H * hiz * egim) % W
            for k in range(7):
                piksel(t, x + k * egim, y - k, hex2(renk, 150 - k * 12))
        if i in parlama:
            d = ImageDraw.Draw(t)
            for yy in range(0, H, 2):
                d.line([0, yy, W, yy], fill=hex2("#e8f0ff", 34 if i == parlama[0] else 20))

    kaydet(sprite_sayfasi(W, H, KARE, kare), f"sahne{no}-hava.png")


# ==========================================================================
# YENİ FİGÜRLER (ciz.py'ye eklenmedi; yalnızca bu seride)
# ==========================================================================
PARSOMEN = "#d8bc8c"     # ceylan derisi
MUREKKEP = "#4a2a1a"


def _harita_katmani(w, h, s, renk=PARSOMEN, notlar=True, tohum=1513):
    """Parşömen haritanın kuşbakışı resmi (yerel 0..w, 0..h; s = 1 için 120x160). Kalıp Piri Reis'in 1513 haritası:
    solda Güney Amerika kıyısı (aşağıda doğuya bükülür), sağda Afrika ve İberya kıyısı, ortada rüzgâr gülü ve ondan
    çıkan pusula hatları, Antiller adaları, küçük gemiler, kara üstünde kenar notları. Sağ kenar yırtık (parça).
    Döner: (resim, maske, noktalar). Bire bir kopya değil; ceylan derisi rengi ve kenar notları okunur."""
    rnd = random.Random(tohum)
    P = lambda u, v: (u * s, v * s)  # noqa: E731
    # parşömenin kenarı: solda düz ama hafif dalgalı, sağda yırtık
    sol = [(rnd.uniform(0, 1.5), v) for v in range(0, 161, 10)]
    sag = []
    for v in range(160, -1, -8):
        u = 120 - 6 * (v / 160) - rnd.uniform(0, 6) - (10 if 100 < v < 128 else 0)
        sag.append((u, v))
    kenar = [P(0, 0)] + [P(*p) for p in sag[::-1]][:1] + [P(*p) for p in sag[::-1]] + [P(1, 160)] + [P(*p) for p in sol[::-1]]
    maske = Image.new("L", (w, h), 0)
    ImageDraw.Draw(maske).polygon(kenar, fill=255)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, h], fill=hex2(renk))
    koyu, acik = _ac(renk, -0.12), _ac(renk, 0.08)
    for _ in range(int(w * h * 0.05)):                                    # deri dokusu: lekeler
        x, y = rnd.randrange(w), rnd.randrange(h)
        piksel(img, x, y, hex2(koyu if rnd.random() < 0.6 else acik))
    for _ in range(int(14 * s)):                                          # büyük soluk lekeler
        cx, cy, r = rnd.randrange(w), rnd.randrange(h), rnd.uniform(3, 9) * s
        for yy in range(int(cy - r), int(cy + r)):
            for xx in range(int(cx - r), int(cx + r)):
                if (xx - cx) ** 2 + (yy - cy) ** 2 < r * r and _esik(xx, yy) < 0.35:
                    piksel(img, xx, yy, hex2(_ac(renk, -0.08)))
    # Güney Amerika: kıyı çizgisi ve kara (kara kıyının solunda ve bükülen kıyının altında)
    gam = [(3, 14), (12, 20), (19, 30), (25, 42), (29, 55), (30, 68), (28, 80), (28, 92), (31, 104), (37, 115),
           (46, 124), (58, 131), (72, 136), (88, 139), (104, 140), (122, 139)]
    d.polygon([P(0, 14)] + [P(*p) for p in gam] + [P(122, 160), P(0, 160)], fill=hex2("#b8a070"))
    # Afrika ve İberya: sağda
    afr = [(92, 0), (96, 6), (90, 12), (86, 22), (83, 34), (86, 46), (94, 55), (104, 61), (114, 64), (124, 66)]
    d.polygon([P(*p) for p in afr] + [P(124, 0)], fill=hex2("#c4a878"))
    # pusula hatları (kara üstünde de geçer), rüzgâr gülü
    gx, gy = 60, 66
    for k in range(16):
        a = k * math.pi / 8
        renk_ = ("#a85a44", "#6a8a4a", "#5a4030")[k % 3]
        d.line([P(gx, gy), P(gx + math.cos(a) * 160, gy + math.sin(a) * 160)], fill=hex2(renk_, 110))
    for k in range(8):
        a = k * math.pi / 8 + math.pi / 16
        d.line([P(58, 10), P(58 + math.cos(a) * 90, 10 + math.sin(a) * 90)], fill=hex2("#6a8a4a", 70))
    # kara dokusu: dağlar (küçük ^) ve ağaç noktaları
    for _ in range(int(40 * s)):
        u, v = rnd.uniform(2, 26), rnd.uniform(24, 156)
        if v > 110:
            u = rnd.uniform(2, 110)
            if v < 128 + (u / 110) * 12:
                continue
        x, y = u * s, v * s
        if rnd.random() < 0.5:
            piksel(img, x, y, hex2("#7a5a32"))
            piksel(img, x - 1, y + 1, hex2("#7a5a32"))
            piksel(img, x + 1, y + 1, hex2("#7a5a32"))
        else:
            piksel(img, x, y, hex2("#5a7a3a"))
    for _ in range(int(16 * s)):
        u, v = rnd.uniform(96, 118), rnd.uniform(6, 56)
        piksel(img, u * s, v * s, hex2(rnd.choice(("#a8402a", "#5a7a3a", "#7a5a32"))))
    # kıyı çizgileri (1 px mürekkep)
    d.line([P(*p) for p in gam], fill=hex2(MUREKKEP), width=1)
    d.line([P(*p) for p in afr], fill=hex2(MUREKKEP), width=1)
    # Antiller: renkli adalar
    for (u, v, a, b, c) in ((38, 16, 9, 3, "#a8402a"), (50, 22, 6, 2, "#3a6a9a"), (58, 14, 7, 2.4, "#5a8a3a"),
                            (34, 26, 3, 2, "#a8402a"), (44, 30, 3, 1.6, "#5a8a3a"), (66, 24, 2.6, 1.6, "#3a6a9a")):
        d.ellipse([P(u - a, v - b), P(u + a, v + b)], fill=hex2(c), outline=hex2(MUREKKEP))
    # rüzgâr gülü: sekiz köşeli yıldız
    r = 7
    for k in range(8):
        a = k * math.pi / 4
        uc = (gx + math.cos(a) * r, gy + math.sin(a) * r)
        sol_ = (gx + math.cos(a + 0.4) * r * 0.35, gy + math.sin(a + 0.4) * r * 0.35)
        sag_ = (gx + math.cos(a - 0.4) * r * 0.35, gy + math.sin(a - 0.4) * r * 0.35)
        d.polygon([P(*uc), P(*sol_), P(gx, gy), P(*sag_)], fill=hex2("#a83a2a" if k % 2 else "#3a6a3a"))
    d.ellipse([P(gx - 1.6, gy - 1.6), P(gx + 1.6, gy + 1.6)], fill=hex2("#c8a040"))
    # küçük gemiler (okyanusta)
    for (u, v) in ((70, 42), (48, 92), (82, 112), (72, 86)):
        d.polygon([P(u - 3, v), P(u + 3, v), P(u + 2, v + 1.4), P(u - 2, v + 1.4)], fill=hex2("#6a3a1e"))
        d.polygon([P(u - 1.6, v - 0.4), P(u + 1.6, v - 0.4), P(u, v - 3.6)], fill=hex2("#f4ece0"))
    # kenar notları: kara üstünde mürekkep satırları (kaynak notu solda, Güney Amerika'da)
    noktalar = {"not": (14 * s, 90 * s), "kiyi": [P(*p) for p in gam[9:]], "gul": P(gx, gy)}
    if notlar:
        for k, v in enumerate(range(78, 106, 4)):
            u0, u1 = 5, 24 - (k % 3) * 2
            for u in range(u0, u1, 3):
                d.line([P(u, v), P(u + 1.6, v)], fill=hex2("#3a1e12" if k % 4 else "#8a2a1e"))
        for v in range(86, 98, 4):
            for u in range(98, 114, 3):
                d.line([P(u, v), P(u + 1.4, v)], fill=hex2("#3a1e12"))
    # kenar kararması
    for yy in range(h):
        for xx in range(w):
            if maske.getpixel((xx, yy)) and _esik(xx, yy) < 0.5:
                kn = min(xx, yy, h - 1 - yy)
                if kn < 2:
                    piksel(img, xx, yy, hex2(_ac(renk, -0.3), 120))
    return img, maske, noktalar


def parsomen_harita(img, x, zemin, s=1.0, renk=PARSOMEN, notlar=True, vurgu=None, f=0.0, golge=True):
    """Yeni figür: kuşbakışı masada yatan ceylan derisi parşömen harita (120x160·s). Alt kenarı `zemin`
    satırına (masanın görünen kenarına) oturur; masaya düşen gölgesi sağ altta. vurgu: None; "not" (kenardaki kaynak
    notu altınla parlar); "soguk" (soğuk mavi ışık, alttaki kıyı buz mavisi parlar); "buk" (alttaki kıyı boyunca
    altın noktalar akar: doğuya bükülen kıyı). Döner: dünya koordinatında önemli noktalar."""
    w, h = int(120 * s), int(160 * s)
    y = zemin_y(zemin, x, w)
    x0, y0 = x - w // 2, y - h
    lay, maske, nk = _harita_katmani(w, h, s, renk, notlar)
    if vurgu == "soguk":
        mavi = Image.new("RGBA", (w, h), hex2("#6a9ad8", 110))
        lay = Image.alpha_composite(lay, mavi)
    dl = ImageDraw.Draw(lay)
    if vurgu == "not":
        nx, ny = nk["not"]
        g = 0.5 + 0.5 * SIN(f)
        dl.rectangle([2, ny - 15 * s, 27 * s, ny + 18 * s], outline=hex2("#ffd060", int(120 + 135 * g)))
        dl.rectangle([1, ny - 16 * s, 28 * s, ny + 19 * s], outline=hex2("#ffe8a0", int(60 + 80 * g)))
    elif vurgu == "soguk":
        g = 0.5 + 0.5 * SIN(f)
        for (a, b), (c, e) in zip(nk["kiyi"], nk["kiyi"][1:]):
            dl.line([a, b, c, e], fill=hex2("#d8f4ff", int(150 + 105 * g)), width=2)
            dl.line([a, b + 2, c, e + 2], fill=hex2("#88c8f0", int(80 + 60 * g)), width=1)
    elif vurgu == "buk":
        yol = []
        for (a, b), (c, e) in zip(nk["kiyi"], nk["kiyi"][1:]):
            n = max(1, int(math.hypot(c - a, e - b)))
            yol += [(a + (c - a) * k / n, b + (e - b) * k / n) for k in range(n)]
        for k, (a, b) in enumerate(yol):
            if (k - int(f * 12)) % 6 < 3:
                dl.rectangle([a - 1, b - 1, a, b], fill=hex2("#ffd060"))
            else:
                piksel(lay, a, b, hex2("#a87818"))
    a = lay.getchannel("A")
    lay.putalpha(Image.composite(a, Image.new("L", (w, h), 0), maske))
    if golge:                                                             # masaya düşen gölge (sağ alta)
        gl = Image.new("RGBA", (w, h), hex2("#000000", 70))
        gl.putalpha(Image.composite(Image.new("L", (w, h), 70), Image.new("L", (w, h), 0), maske))
        img.alpha_composite(gl, (x0 + _u(2, s), y0 + 1))
    img.alpha_composite(lay, (x0, y0))
    return {"not": (x0 + nk["not"][0], y0 + nk["not"][1]), "x0": x0, "y0": y0, "w": w, "h": h}


def eski_tomar(img, x, zemin, s=1.0, renk="#c8a878"):
    """Yeni figür (kuşbakışı): masada yatan dürülmüş eski harita (rulo): silindir gövde, iki ucunda kıvrım."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 22 * s)
    d.rectangle([x - int(11 * s), y - _u(5, s), x + int(11 * s), y - 1], fill=hex2(renk))
    d.line([x - int(11 * s), y - _u(4, s), x + int(11 * s), y - _u(4, s)], fill=hex2(_ac(renk, 0.2)))
    d.line([x - int(11 * s), y - 2, x + int(11 * s), y - 2], fill=hex2(_ac(renk, -0.25)))
    for k in (-1, 1):
        d.ellipse([x + k * int(11 * s) - _u(1.6, s), y - _u(5, s), x + k * int(11 * s) + _u(1.6, s), y - 1],
                  fill=hex2(_ac(renk, -0.15)), outline=hex2(_ac(renk, -0.4)))
    d.line([x - _u(1, s), y - _u(5, s), x - _u(1, s), y - 1], fill=hex2("#8a2a1e"))   # bağ şeridi


def _sayfa(img, x0, y0, w, h, renk, cerceve=None):
    d = ImageDraw.Draw(img)
    d.rectangle([x0 + 1, y0 + 1, x0 + w + 1, y0 + h + 1], fill=hex2("#000000", 60))      # masaya gölge
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=hex2(renk), outline=hex2(_ac(renk, -0.35)))
    if cerceve:
        d.rectangle([x0 - 1, y0 - 1, x0 + w + 1, y0 + h + 1], outline=hex2(cerceve))
    return d


def arap_haritasi(img, x, zemin, s=1.0):
    """Yeni figür (kuşbakışı): yuvarlak dünya haritası çizilmiş kâğıt: daire içinde kara parçaları ve deniz."""
    y = zemin_y(zemin, x, 26 * s)
    w = int(26 * s)
    d = _sayfa(img, x - w // 2, y - w, w, w - 1, "#e4d4b0")
    cx, cy, r = x, y - w // 2, int(11 * s)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hex2("#6a9ab0"), outline=hex2("#3a2a1a"))
    d.polygon([(cx - r + 3, cy - 2), (cx - 2, cy - r + 3), (cx + r - 4, cy - 3), (cx + 2, cy + 2), (cx - 4, cy + r - 4)],
              fill=hex2("#b89a5a"))
    d.line([cx - r + 2, cy + 1, cx + r - 2, cy + 1], fill=hex2("#3a6a3a"))


def portekiz_haritasi(img, x, zemin, s=1.0, tohum=1):
    """Yeni figür (kuşbakışı): portolan kâğıdı: pusula hatları ve kahverengi kıyı, mavi deniz kenarı."""
    rnd = random.Random(tohum)
    w, h = int(20 * s), int(15 * s)
    y = zemin_y(zemin, x, w)
    d = _sayfa(img, x - w // 2, y - h, w, h - 1, "#e8dcc0")
    cx, cy = x + rnd.randint(-2, 2), y - h // 2
    for k in range(8):
        a = k * math.pi / 4
        d.line([cx, cy, cx + math.cos(a) * w, cy + math.sin(a) * w], fill=hex2("#a85a44", 90))
    pts = [(x - w // 2 + 2 + k * 3, y - h + 3 + rnd.randint(0, 6)) for k in range(int(w / 3))]
    d.line(pts, fill=hex2("#4a2a1a"))
    d.rectangle([x - w // 2 + 1, y - h + 1, x + w // 2 - 1, y - h + 2], fill=hex2("#5a8ab0"))


def kolomb_haritasi(img, x, zemin, s=1.0, f=0.0, parla=True):
    """Yeni figür (kuşbakışı): Kolomb'un haritası (kayıp; temsilî): adalar ve kıyı parçası çizili kâğıt; altın çerçeve
    yavaşça parlar."""
    w, h = int(24 * s), int(18 * s)
    y = zemin_y(zemin, x, w)
    g = 0.5 + 0.5 * SIN(f)
    d = _sayfa(img, x - w // 2, y - h, w, h - 1, "#ece0c4", cerceve="#e0b040" if parla else None)
    if parla:
        d.rectangle([x - w // 2 - 2, y - h - 2, x + w // 2 + 2, y + 1], outline=hex2("#ffe080", int(70 + 120 * g)))
    for (u, v, a, b, c) in ((-5, -10, 4, 1.6, "#a8402a"), (2, -12, 3, 1.4, "#5a8a3a"), (6, -7, 2.4, 1.2, "#3a6a9a"),
                            (-2, -5, 2, 1, "#a8402a")):
        d.ellipse([x + u * s - a * s, y + v * s - b * s, x + u * s + a * s, y + v * s + b * s], fill=hex2(c),
                  outline=hex2(MUREKKEP))
    d.line([x - w // 2 + 2, y - 3, x - 3, y - h + 4], fill=hex2(MUREKKEP))


def hokka(img, x, zemin, s=1.0):
    """Yeni figür (kuşbakışı): pirinç mürekkep hokkası: yuvarlak gövde, ortada kara mürekkep."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 10 * s)
    r = int(5 * s)
    d.ellipse([x - r + 1, y - 2 * r + 1, x + r + 1, y + 1], fill=hex2("#000000", 70))
    d.ellipse([x - r, y - 2 * r, x + r, y], fill=hex2("#b8903a"), outline=hex2("#5a3a10"))
    d.ellipse([x - r // 2, y - r - r // 2, x + r // 2, y - r + r // 2], fill=hex2("#14100c"))
    piksel(img, x - r + 2, y - 2 * r + 2, hex2("#f0d890"))


def yazan_el(img, uc, s=1.0, f=0.0, kol="#2a5a6a", ten="#d6a07a", yon=(1, 1)):
    """Yeni figür (kuşbakışı): kalem tutan el ve kaftan yeni. uc: kalemin ucu (kâğıda değer). Yen sprite'ın alt
    kenarına kadar uzanır (kolun gerisi kadraj dışında). f: kalem satır boyunca gidip gelir (yazma)."""
    d = ImageDraw.Draw(img)
    dx = (SIN(f) * 3 + SIN(f, 3) * 0.8) * s
    ux, uy = uc[0] + dx, uc[1] + abs(SIN(f, 3)) * 0.6
    ex, ey = ux + 7 * s * yon[0], uy + 5 * s * yon[1]                   # el
    # kaftan yeni: elden sprite'ın altına
    d.polygon([(ex + 2 * s, ey - 1 * s), (ex + 12 * s, img.height - 1 + 0 * s), (ex + 34 * s, img.height - 1),
               (ex + 8 * s, ey - 4 * s)], fill=hex2(kol))
    d.line([(ex + 3 * s, ey + 1 * s), (ex + 16 * s, img.height - 1)], fill=hex2(_ac(kol, -0.3)))
    d.line([(ex + 8 * s, ey - 4 * s), (ex + 34 * s, img.height - 1)], fill=hex2(_ac(kol, 0.25)))
    d.ellipse([ex - 4 * s, ey - 4 * s, ex + 4 * s, ey + 3 * s], fill=hex2(ten), outline=hex2(_ac(ten, -0.35)))
    d.ellipse([ex - 5 * s, ey - 1 * s, ex - 1 * s, ey + 2 * s], fill=hex2(_ac(ten, -0.05)))            # parmaklar
    # kalem: kamış, uç kâğıtta
    d.line([ux, uy, ex - 2 * s, ey - 2 * s], fill=hex2("#c8a868"), width=max(1, int(1 * s)))
    d.line([ex - 2 * s, ey - 2 * s, ex + 6 * s, ey - 10 * s], fill=hex2("#e8dcc0"), width=max(1, int(1.2 * s)))
    piksel(img, ux, uy, hex2(MUREKKEP))


def harita_masasi(img, x, zemin, s=1.0, ag="#5a3a22", ortu=None):
    """Yeni figür: üstünde parşömen harita yatan alçak ahşap masa (yandan, üst yüzü hafif görünür). Dört ayak zemine
    basar; parşömen masanın üst yüzüne oturur, ucu masanın ön kenarından hafifçe sarkar. Döner: üst yüz y'si."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 30 * s)
    temas_golgesi(img, x, y, 32 * s)
    ust = y - int(10 * s)
    derin = _u(4, s)
    for k in (-13, -9, 9, 13):
        d.rectangle([x + int(k * s) - _u(0.6, s), ust, x + int(k * s) + _u(0.6, s), y - 1], fill=hex2(_ac(ag, -0.2)))
    d.rectangle([x - int(15 * s), ust - derin, x + int(15 * s), ust + _u(1.6, s)], fill=hex2(ag))
    d.polygon([(x - int(15 * s), ust - derin), (x + int(15 * s), ust - derin), (x + int(13 * s), ust - derin - _u(3, s)),
               (x - int(13 * s), ust - derin - _u(3, s))], fill=hex2(_ac(ag, 0.2)))                  # üst yüz
    if ortu:
        d.rectangle([x - int(15 * s), ust - derin, x + int(15 * s), ust + _u(3, s)], fill=hex2(ortu))
    # parşömen: üst yüzde, perspektifte ince dörtgen; renkli kıyı ve gül izleri
    py = ust - derin
    d.polygon([(x - int(11 * s), py), (x + int(10 * s), py), (x + int(9 * s), py - _u(3, s)), (x - int(10 * s), py - _u(3, s))],
              fill=hex2(PARSOMEN))
    d.rectangle([x - int(11 * s), py, x + int(10 * s), py + _u(1.2, s)], fill=hex2(_ac(PARSOMEN, -0.15)))   # sarkan uç
    d.line([x - int(9 * s), py - _u(1, s), x - int(4 * s), py - _u(2, s)], fill=hex2(MUREKKEP))
    d.line([x + int(4 * s), py - _u(2.4, s), x + int(8 * s), py - _u(1, s)], fill=hex2(MUREKKEP))
    piksel(img, x, py - _u(1.6, s), hex2("#a83a2a"))
    piksel(img, x + 1, py - _u(1.6, s), hex2("#3a6a3a"))
    return py


def vitrin(img, x, zemin, s=1.0, ag="#3a2a20"):
    """Yeni figür: müze vitrini: ahşap kaide dört ayakla zemine basar, üstte izleyiciye eğik cam kapak; camın altında
    parşömen haritanın küçük bir görüntüsü."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 40 * s)
    temas_golgesi(img, x, y, 42 * s)
    for k in (-18, 18):
        d.rectangle([x + int(k * s) - _u(1, s), y - int(6 * s), x + int(k * s) + _u(1, s), y - 1], fill=hex2(_ac(ag, -0.2)))
    d.rectangle([x - int(20 * s), y - int(16 * s), x + int(20 * s), y - int(6 * s)], fill=hex2(ag))
    d.line([x - int(20 * s), y - int(16 * s), x + int(20 * s), y - int(16 * s)], fill=hex2(_ac(ag, 0.3)))
    # eğik yüz: parşömen (yatay döndürülmüş, perspektifte basık)
    lay, maske, _ = _harita_katmani(int(120 * 0.4), int(160 * 0.4), 0.4)
    lay.putalpha(Image.composite(lay.getchannel("A"), Image.new("L", lay.size, 0), maske))
    lay = lay.rotate(90, expand=True).resize((int(36 * s), int(9 * s)), Image.NEAREST)
    yy = y - int(16 * s) - lay.height - _u(1, s)
    d.polygon([(x - int(20 * s), y - int(16 * s)), (x + int(20 * s), y - int(16 * s)),
               (x + int(19 * s), yy - _u(1, s)), (x - int(19 * s), yy - _u(1, s))], fill=hex2("#2a2420"))
    img.alpha_composite(lay, (x - lay.width // 2, yy))
    d.line([x - int(19 * s), yy - _u(1, s), x + int(19 * s), yy - _u(1, s)], fill=hex2("#c8d8e0"))       # cam kenarı
    for k in range(3):                                                                               # camda yansıma
        piksel(img, x - int(12 * s) + k * 2, yy + 1 + k, hex2("#e8f4ff", 150))


def sandik(img, x, zemin, s=1.0, ag="#5a3a1e", rulo=True):
    """Yeni figür: demir kuşaklı ahşap sandık, zemine oturur; rulo=True: kapağının üstünde dürülmüş parşömen yatar."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 22 * s)
    temas_golgesi(img, x, y, 24 * s)
    d.rectangle([x - int(11 * s), y - int(11 * s), x + int(11 * s), y - 1], fill=hex2(ag))
    d.chord([x - int(11 * s), y - int(15 * s), x + int(11 * s), y - int(7 * s)], 180, 360, fill=hex2(_ac(ag, 0.12)))
    for k in (-7, 0, 7):
        d.line([x + int(k * s), y - int(14 * s), x + int(k * s), y - 1], fill=hex2("#3a3a40"), width=_u(1, s))
    d.line([x - int(11 * s), y - int(11 * s), x + int(11 * s), y - int(11 * s)], fill=hex2("#2a1a10"))
    d.rectangle([x - _u(1.4, s), y - int(10 * s), x + _u(1.4, s), y - int(7 * s)], fill=hex2("#c8a040"))   # kilit
    if rulo:
        ry = y - int(15 * s)
        d.rectangle([x - int(8 * s), ry - _u(3, s), x + int(8 * s), ry], fill=hex2(PARSOMEN))
        d.line([x - int(8 * s), ry - _u(3, s), x + int(8 * s), ry - _u(3, s)], fill=hex2(_ac(PARSOMEN, 0.15)))
        for k in (-1, 1):
            d.ellipse([x + k * int(8 * s) - _u(1.2, s), ry - _u(3, s), x + k * int(8 * s) + _u(1.2, s), ry],
                      fill=hex2(_ac(PARSOMEN, -0.2)))
        d.line([x + _u(2, s), ry - _u(3, s), x + _u(2, s), ry], fill=hex2("#8a2a1e"))


def kagit_destesi(img, x, zemin, s=1.0, kat=4, tohum=1):
    """Yeni figür: iple bağlanmış kâğıt ve defter desteleri üst üste; en alttaki zemine oturur."""
    d = ImageDraw.Draw(img)
    rnd = random.Random(tohum)
    y = zemin_y(zemin, x, 20 * s)
    temas_golgesi(img, x, y, 22 * s)
    yy = y
    for k in range(kat):
        w = int(rnd.uniform(16, 20) * s)
        h = _u(rnd.uniform(2.6, 3.6), s)
        dx = rnd.randint(-2, 2)
        renk = rnd.choice(("#e0d4b8", "#d4c4a0", "#c8b48c", "#8a3a2a", "#3a5a6a"))
        d.rectangle([x + dx - w // 2, yy - h, x + dx + w // 2, yy - 1], fill=hex2(renk))
        for k2 in range(yy - h + 1, yy - 1, 2):
            d.line([x + dx - w // 2 + 1, k2, x + dx + w // 2 - 1, k2], fill=hex2(_ac(renk, -0.12)))
        d.line([x + dx - 1, yy - h, x + dx - 1, yy - 1], fill=hex2("#6a4a2a"))                             # ip
        yy -= h


def hurma(img, x, zemin, s=1.0, egim=1, gov="#6a5034", yaprak=("#3a5a2a", "#4a6a32", "#5a7a3a")):
    """Yeni figür: hurma ağacı: boğumlu ince gövde zemine oturur (dibinde toprak), tepede kavisle sarkan yapraklar."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    temas_golgesi(img, x, y, 8 * s)
    boy = int(26 * s)
    tepe = (x + egim * int(3 * s), y - boy)
    for k in range(boy):
        t = k / boy
        bx = x + egim * 3 * s * t * t
        d.line([bx - _u(1, s), y - 1 - k, bx + _u(1, s), y - 1 - k], fill=hex2(gov if k % 3 else _ac(gov, -0.25)))
    for a, uz in ((-2.7, 12), (-2.2, 13), (-1.6, 10), (-0.9, 13), (-0.4, 12), (-1.2, 8), (-2.0, 9)):
        pts = []
        for k in range(10):
            t = k / 9
            pts.append((tepe[0] + math.cos(a) * uz * s * t, tepe[1] + math.sin(a) * uz * s * t + t * t * 6 * s))
        for (p, q), r in zip(zip(pts, pts[1:]), range(9)):
            d.line([p, q], fill=hex2(yaprak[r % 3]), width=max(1, int(1.4 * s * (1 - r / 12))))
    d.ellipse([tepe[0] - _u(1.6, s), tepe[1] - _u(0.8, s), tepe[0] + _u(1.6, s), tepe[1] + _u(1.6, s)], fill=hex2("#8a5a1a"))


def osmanli_camii(img, x, zemin, s=1.0, tas="#d8cdb8", kubbe="#8a96a0", minare=True):
    """takiyuddin_rasathanesi.py'deki cami silüetinin kopyası (kare gövde, yarım kubbeler, ana kubbe, tek minare).
    Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(22 * s), x + int(26 * s), "cami", tolerans=max(3, int(s)))
    temas_golgesi(img, x + int(2 * s), y, 50 * s)
    t, tk = hex2(tas), hex2(_ac(tas, -0.22))
    kb, kbk = hex2(kubbe), hex2(_ac(kubbe, -0.2))
    d.rectangle([x - int(20 * s), y - int(12 * s), x + int(20 * s), y - 1], fill=t)
    for px in (-15, -9, 9, 15):
        d.rectangle([x + int(px * s) - _u(1, s), y - int(9 * s), x + int(px * s) + _u(1, s), y - int(5 * s)], fill=hex2("#2a3040"))
    d.rectangle([x - _u(2.4, s), y - int(8 * s), x + _u(2.4, s), y - 1], fill=hex2("#3a2a20"))
    for yon in (-1, 1):
        cx = x + int(12 * s) * yon
        d.chord([cx - int(6 * s), y - int(19 * s), cx + int(6 * s), y - int(10 * s)], 180, 360, fill=kb)
    d.rectangle([x - int(10 * s), y - int(18 * s), x + int(10 * s), y - int(12 * s)], fill=t, outline=tk)
    d.chord([x - int(10 * s), y - int(29 * s), x + int(10 * s), y - int(8 * s)], 180, 360, fill=kb)
    for r in (-6, -2, 2, 6):
        d.line([x + int(r * s), y - int(18 * s), x + int(r * 0.4 * s), y - int(28 * s)], fill=kbk)
    if minare:
        mx = x + int(24 * s)
        d.rectangle([mx - _u(1.8, s), y - int(40 * s), mx + _u(1.8, s), y - 1], fill=t)
        d.line([mx + _u(1.8, s), y - int(40 * s), mx + _u(1.8, s), y - 1], fill=tk)
        d.rectangle([mx - _u(3, s), y - int(31 * s), mx + _u(3, s), y - int(30 * s)], fill=hex2(_ac(tas, -0.1)))
        d.polygon([(mx - _u(2, s), y - int(40 * s)), (mx, y - int(46 * s)), (mx + _u(2, s), y - int(40 * s))], fill=kb)


def piramit(img, x, zemin, s=1.0, renk="#c8a870"):
    """Yeni figür (uzak plan): piramit: geniş tabanı ovaya oturur, güneş alan yüzü açık, gölgede kalan yüzü koyu."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 40 * s)
    d.polygon([(x - int(20 * s), y), (x, y - int(16 * s)), (x + int(20 * s), y)], fill=hex2(renk))
    d.polygon([(x, y - int(16 * s)), (x + int(20 * s), y), (x + int(6 * s), y)], fill=hex2(_ac(renk, -0.25)))
    for k in range(2, int(16 * s), 3):
        d.line([x - int(20 * s) + int(k * 1.25), y - k, x + int(k * 0.4), y - k], fill=hex2(_ac(renk, -0.08)))


def babusselam(img, x, zemin, s=1.0, tas="#d8d0c0", kursun="#5a6470"):
    """Yeni figür: Topkapı Sarayı'nın Bâbüsselâm (Orta Kapı): iki sekizgen kule, sivri kurşun külahlar, aralarında
    kemerli kapı ve saçak; iki yanda alçak sur. Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(40 * s), x + int(40 * s), "babusselam", tolerans=max(3, int(s)))
    temel(img, zemin, x - int(40 * s), x + int(40 * s), y, "#6a604e")
    t, tk = hex2(tas), hex2(_ac(tas, -0.2))
    d.rectangle([x - int(40 * s), y - int(12 * s), x + int(40 * s), y - 1], fill=t)                      # sur
    for bx in range(x - int(40 * s), x + int(40 * s), _u(4, s)):
        d.rectangle([bx, y - int(13.5 * s), bx + _u(2, s), y - int(12 * s)], fill=t)
    for k in (-1, 1):                                                                                    # kuleler
        kx = x + k * int(12 * s)
        d.rectangle([kx - int(5 * s), y - int(26 * s), kx + int(5 * s), y - 1], fill=t)
        d.line([kx + int(2 * s), y - int(26 * s), kx + int(2 * s), y - 1], fill=tk)
        d.rectangle([kx - _u(1, s), y - int(21 * s), kx + _u(1, s), y - int(17 * s)], fill=hex2("#3a3a44"))
        d.polygon([(kx - int(6 * s), y - int(26 * s)), (kx, y - int(38 * s)), (kx + int(6 * s), y - int(26 * s))], fill=hex2(kursun))
        d.line([kx, y - int(38 * s), kx + int(6 * s), y - int(26 * s)], fill=hex2(_ac(kursun, -0.25)))
    d.rectangle([x - int(7 * s), y - int(18 * s), x + int(7 * s), y - 1], fill=t)                         # kapı gövdesi
    d.polygon([(x - int(9 * s), y - int(18 * s)), (x + int(9 * s), y - int(18 * s)), (x + int(7 * s), y - int(21 * s)),
               (x - int(7 * s), y - int(21 * s))], fill=hex2(kursun))                                      # saçak
    d.rectangle([x - int(3.4 * s), y - int(10 * s), x + int(3.4 * s), y - 1], fill=hex2("#2a2420"))
    d.chord([x - int(3.4 * s), y - int(13.4 * s), x + int(3.4 * s), y - int(6.6 * s)], 180, 360, fill=hex2("#2a2420"))
    d.rectangle([x - int(5 * s), y - int(16 * s), x + int(5 * s), y - int(15 * s)], fill=hex2("#2a6a5a"))    # yazı kuşağı


def fener(img, x, zemin, s=1.0, f=0.0):
    """Yeni figür: yere konmuş pirinç fener: kaidesi zemine oturur, camlı gövdede titreyen alev, tepe halkası;
    çevresine sıcak ışık düşer."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    temas_golgesi(img, x, y, 7 * s)
    d.rectangle([x - _u(3, s), y - _u(1.4, s), x + _u(3, s), y - 1], fill=hex2("#6a4a1a"))
    d.rectangle([x - _u(2.4, s), y - int(8 * s), x + _u(2.4, s), y - _u(1.4, s)], fill=hex2("#f8d070", 200), outline=hex2("#6a4a1a"))
    d.polygon([(x - _u(3, s), y - int(8 * s)), (x + _u(3, s), y - int(8 * s)), (x, y - int(11 * s))], fill=hex2("#8a6a2a"))
    d.ellipse([x - _u(1, s), y - int(12.6 * s), x + _u(1, s), y - int(11 * s)], outline=hex2("#8a6a2a"))
    al = 1.4 + 0.6 * SIN(f, 3)
    d.polygon([(x - _u(1, s), y - int(3 * s)), (x, y - int(3 * s) - int(al * 2 * s)), (x + _u(1, s), y - int(3 * s))],
              fill=hex2("#fff0b0"))
    for r in range(4, 18, 2):
        for a in range(0, 360, 12):
            px_, py_ = x + math.cos(math.radians(a)) * r * s * 0.5, y - 5 * s + math.sin(math.radians(a)) * r * s * 0.4
            if py_ < y - 1 and _esik(int(px_), int(py_)) < 0.4 * (1 - r / 18):
                piksel(img, px_, py_, hex2("#f8d070", 70))


def halat(img, x, zemin, s=1.0):
    """Yeni figür: güvertede kangal yapılmış halat; zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 12 * s)
    temas_golgesi(img, x, y, 13 * s)
    for k in range(3):
        d.ellipse([x - int((6 - k) * s), y - int((4 + k * 1.2) * s), x + int((6 - k) * s), y - 1 - int(k * 1.2 * s)],
                  outline=hex2("#a8885a"), width=_u(1, s))
    d.line([x + int(5 * s), y - _u(2, s), x + int(9 * s), y - 1], fill=hex2("#a8885a"), width=_u(1, s))


def fici(img, x, zemin, s=1.0, renk="#7a5232"):
    """Yeni figür: ahşap fıçı, zemine oturur; iki demir çember."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 9 * s)
    temas_golgesi(img, x, y, 10 * s)
    d.rounded_rectangle([x - int(4.5 * s), y - int(11 * s), x + int(4.5 * s), y - 1], radius=_u(2, s), fill=hex2(renk))
    for k in (3, 8):
        d.line([x - int(4.5 * s), y - int(k * s), x + int(4.5 * s), y - int(k * s)], fill=hex2("#3a3a40"), width=_u(0.8, s))
    d.line([x - _u(1.6, s), y - int(10 * s), x - _u(1.6, s), y - _u(1.6, s)], fill=hex2(_ac(renk, 0.25)))


def masa(img, x, zemin, s=1.0, ortu="#2a3a8a"):
    """celebi_mehmed_paris.py'deki örtülü küçük masanın kopyası: dört ayak zemine basar. Dönen değer: tabla üst y."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 16 * s)
    temas_golgesi(img, x, y, 17 * s)
    top = y - int(8 * s)
    for k in (-7, -3, 3, 7):
        d.rectangle([x + int(k * s) - max(1, int(0.5 * s)), top, x + int(k * s) + max(1, int(0.5 * s)), y - 1], fill=hex2("#4a2e1a"))
    d.rectangle([x - int(8 * s), top - max(1, int(1 * s)), x + int(8 * s), top + int(3 * s)], fill=hex2(ortu))
    d.line([x - int(8 * s), top + int(3 * s), x + int(8 * s), top + int(3 * s)], fill=hex2("#e0b040"))
    return top - max(1, int(1 * s))


def kitap_rafi(img, x, zemin, s=1.0, dolu=True, tohum=1, rulo=False):
    """celebi_mehmed_paris.py'deki ayaklı raf dolabının kopyası; rulo=True: raflarda kitap yerine dürülmüş kâğıtlar."""
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
        if not dolu:
            continue
        bx = x - int(8 * s)
        while bx < x + int(7.5 * s):
            if rulo:
                r = max(1, int(rnd.uniform(1.0, 1.6) * s))
                renk = rnd.choice(("#d8c4a0", "#c8b088", "#e0d0b0"))
                d.ellipse([bx, sy - 2 * r, bx + 2 * r, sy - 1], fill=hex2(renk), outline=hex2(_ac(renk, -0.35)))
                bx += 2 * r + 1
            else:
                bw = max(1, int(rnd.uniform(0.9, 1.8) * s))
                bh = int(rnd.uniform(4.2, 6.2) * s)
                renk = rnd.choice(("#8a2a2a", "#2a4a7a", "#3a6a3a", "#a8803a", "#5a3a5a", "#7a5a3a"))
                d.rectangle([bx, sy - bh, min(bx + bw, x + int(8 * s)), sy - 1], fill=hex2(renk))
                piksel(img, bx, sy - bh + 1, hex2(_ac(renk, 0.4)))
                bx += bw + 1


def portekiz_gemisi(img, x, su_y, s=1.0, yon=1, faz=0.0):
    """Portekiz gemisi (temsilî): kütüphanenin kadırgası, beyaz yelken üstünde kırmızı haç (Mesih Tarikatı haçı);
    gövde su çizgisine oturur."""
    figur(img, gemi, x, su_y, s, yon, faz, govde="#3a2a1e", yelken="#f0e8d8", hac=False)
    d = ImageDraw.Draw(img)
    y = su_y + int(math.sin(faz * 2 * math.pi) * 0.8 * s)
    sis = math.sin(faz * 2 * math.pi) * 1.2 * s
    cx = x + int(sis * 0.5)
    d.rectangle([cx - _u(1, s), y - int(24 * s), cx + _u(1, s), y - int(11 * s)], fill=hex2("#b8281e"))
    d.rectangle([cx - int(6 * s), y - int(20 * s), cx + int(6 * s), y - int(18 * s)], fill=hex2("#b8281e"))


def _gemi_denetimi(s, su, w, h, x=None):
    """Gövde su çizgisine ulaşmalı (havada gemi olmaz)."""
    for f in (0.0, 0.25, 0.5, 0.75):
        g = yeni(w, h)
        figur(g, gemi, x or w // 2, su, s, 1, f)
        if _bb(g)[3] < su:
            raise RuntimeError(f"Gemi suya ulaşmıyor: alt={_bb(g)[3]}, su_y={su}")


def _su(t, y0, renkler, f, tohum=1, dalga=1.0):
    """Sprite içindeki deniz: y0'dan aşağısı su bantları; dalga çizgileri f ile yana kayar (dikişsiz döngü)."""
    d = ImageDraw.Draw(t)
    for y in range(y0, t.height):
        d.line([0, y, t.width, y], fill=hex2(renkler[min(len(renkler) - 1, (y - y0) // 8)]))
    rnd = random.Random(tohum)
    for _ in range(int(t.width * (t.height - y0) / 50)):
        x, y = rnd.randrange(t.width), rnd.randrange(y0 + 1, t.height)
        kay = int(SIN(f + x / 97) * 3 * dalga)
        for k in range(rnd.randint(3, 7)):
            piksel(t, x + k + kay, y, hex2("#c8e0f0", 110))
    for x in range(0, t.width, 2):                                       # su yüzeyindeki köpük çizgisi
        if _esik(x + int(f * 24), y0) < 0.5:
            piksel(t, x, y0, hex2("#e8f4fc", 170))


# ==========================================================================
# Ortak katman yardımcıları
# ==========================================================================
def _orta_deniz(no, ust, renkler, kara=None, ekle=None, kenar=None):
    """Orta plan: üstte ince kara/kıyı şeridi (ust..ust+kara_h, isteğe bağlı), aşağısı deniz."""
    img = yeni(GW, H)
    d = ImageDraw.Draw(img)
    if kara:
        renk, h_ = kara
        d.rectangle([0, ust - h_, GW, ust], fill=hex2(renk))
        d.line([0, ust - h_, GW, ust - h_], fill=hex2(_ac(renk, 0.25)))
    for y in range(ust, H):
        d.line([0, y, GW, y], fill=hex2(renkler[min(len(renkler) - 1, (y - ust) // 14)]))
    rnd = random.Random(no)
    for _ in range(700):
        x, y = rnd.randrange(GW), rnd.randrange(ust + 2, H)
        for k in range(rnd.randint(3, 7)):
            piksel(img, x + k, y, hex2(kenar or "#a8c8e0", 90))
    if ekle:
        ekle(img)
    kaydet(img, f"sahne{no}-orta.png")


def _guverte(no, ahsap="#7a5232", kupeste_y=572, guverte_y=600):
    """Orta plan (yeni): kadırga güvertesi. Arkada küpeşte (ahşap korkuluk, kürek delikleri), önde güverte tahtaları;
    figürler sprite'ta güverteye basar. Küpeşte yazı bandının çok altında."""
    img = yeni(GW, H)
    d = ImageDraw.Draw(img)
    d.rectangle([0, kupeste_y, GW, guverte_y], fill=hex2(_ac(ahsap, -0.15)))
    for x in range(0, GW, 7):
        d.line([x, kupeste_y + 2, x, guverte_y], fill=hex2(_ac(ahsap, -0.28)))
    d.rectangle([0, kupeste_y - 3, GW, kupeste_y], fill=hex2(_ac(ahsap, 0.2)))
    d.line([0, kupeste_y - 3, GW, kupeste_y - 3], fill=hex2(_ac(ahsap, 0.4)))
    for x in range(20, GW, 46):                                          # kürek delikleri
        d.ellipse([x - 3, kupeste_y + 10, x + 3, kupeste_y + 16], fill=hex2("#1a120c"))
    for y in range(guverte_y, H):
        k = (y - guverte_y)
        d.line([0, y, GW, y], fill=hex2(_ac(ahsap, 0.05 - 0.15 * min(1, k / 200))))
    yy, aralik = guverte_y + 4, 4
    while yy < H:
        d.line([0, yy, GW, yy], fill=hex2(_ac(ahsap, -0.3)))
        aralik += 2
        yy += aralik
    rnd = random.Random(no)
    for _ in range(400):
        piksel(img, rnd.randrange(GW), rnd.randrange(guverte_y, H), hex2(_ac(ahsap, rnd.choice((-0.2, 0.15)))))
    kaydet(img, f"sahne{no}-orta.png")


def _masa_ustu(no, renk="#6a4426", tur="ahsap", isik=None):
    """Kuşbakışı sahnelerin orta planı: bütün kareyi kaplayan masa yüzeyi (ahşap tahtalar ya da keçe). Sprite ile
    aynı paralaksta (0.65) durur; kamera 0 verilir. gokyuzu ve uzak, orta tarafından tamamen örtülür."""
    g = yeni()
    ImageDraw.Draw(g).rectangle([0, 0, W, H], fill=hex2(_ac(renk, -0.3)))
    kaydet(g, f"sahne{no}-gokyuzu.png")
    kaydet(yeni(), f"sahne{no}-uzak.png")
    img = yeni(GW, H)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, GW, H], fill=hex2(renk))
    rnd = random.Random(no)
    if tur == "ahsap":
        for y in range(0, H, 22):                                        # tahta derzleri ve damarlar
            d.line([0, y, GW, y], fill=hex2(_ac(renk, -0.3)))
            for _ in range(18):
                x0, yy = rnd.randrange(GW), y + rnd.randrange(3, 20)
                L = rnd.randrange(20, 90)
                for k in range(L):
                    piksel(img, x0 + k, yy + int(math.sin(k / 9 + x0) * 1.2), hex2(_ac(renk, rnd.choice((-0.12, 0.1)))))
    else:                                                                # keçe/kadife
        for _ in range(9000):
            piksel(img, rnd.randrange(GW), rnd.randrange(H), hex2(_ac(renk, rnd.choice((-0.1, 0.08)))))
    if isik:                                                             # ışık havuzu (ortada açık, kenarlarda koyu)
        cx, cy = PAY + 270, 560
        for y in range(0, H, 1):
            for x in range(PAY - 40, PAY + 580, 1):
                r = math.hypot((x - cx) / 1.0, (y - cy) / 1.25)
                if r > 150 and _esik(x, y) < min(0.8, (r - 150) / 220):
                    piksel(img, x, y, hex2(isik, 70))
    kaydet(img, f"sahne{no}-orta.png")
    _bos_on(no)


def _sahne_gok(no, renkler, bulutlar=(), bulut_renk=("#fff8ec", "#f4dcc8", "#d8a8a0"), yildiz=0):
    return gokyuzu(no, renkler, None, bulutlar, bulut_renk, yildiz)


# ==========================================================================
# 330 · KAPAK + kart 1 · Kahire, alacakaranlık: avluda yaşlı denizci; karşısında fermanı tutan çavuş
# 352 · kart 29, 52-53 · aynı avlu, gece, boş: yere bırakılmış fener (idam gösterilmez)
# ==========================================================================
def _kahire_avlu(no, gok, ova, orta_renk, kenar, ev="#c8a878", tas="#d8cdb8", kubbe="#8a96a0", gece=False):
    _sahne_gok(no, gok, [(110, 404, 20), (430, 408, 18)] if not gece else [],
               ("#f0c8b8", "#d09898", "#a07080"), yildiz=0)
    uzak(no, [_ac(ova[0], -0.1), _ac(ova[0], -0.15)], [_ac(ova[1], -0.05), _ac(ova[1], -0.1)], ova,
         dag_y=(420, 456), tepe_y=470, ova_y=492)

    def ekle(img, z):
        figur(img, koy_evleri, PAY + 20, PAY + 520, duz(586), 2.2, tohum=no, kerpic=ev)
        figur(img, osmanli_camii, PAY + 360, duz(584), 1.3, tas=tas, kubbe=kubbe)
        figur(img, osmanli_camii, PAY + 150, duz(586), 1.0, tas=tas, kubbe=kubbe, minare=False)
        d = ImageDraw.Draw(img)                                             # avlu duvarı: alçak, düz zemine
        d.rectangle([0, 596, GW, 606], fill=hex2(_ac(ev, -0.2)))
        d.line([0, 596, GW, 596], fill=hex2(_ac(ev, 0.15)))

    orta(no, (556, 560), orta_renk, kenar, ekle=ekle)
    _bos_on(no)


KAHIRE_GOK = ["#2a2448", "#4a3460", "#7a4a6a", "#b0646e", "#d88a70", "#e8a878"]
KAHIRE_ORTA = ["#b89a72", "#aa8c66", "#9c7e5a", "#8e704e", "#806444"]


def sahne330():
    """'Seksenini geçmiş bir denizci...': Kahire, alacakaranlık; taş avluda yaşlı kaptan (ak sakal) dimdik durur,
    karşısında börklü çavuş fermanı açmış tutar. Geride kerpiç damlar, kubbe ve minare."""
    _kahire_avlu(330, KAHIRE_GOK, ["#a07a6a", "#94705e", "#886654"], KAHIRE_ORTA, "#e0c098")
    yk = 2.8
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 168, z, K, **PIRI_YASLI, yon=1, kol=0.02 * (1 + SIN(f)))
        figur(t, kisi, 240, z, round(0.97 * K, 1), **CAVUS, yon=-1, silah="mektup", kol=0.36 + 0.03 * SIN(f))

    _spr2(330, DW, DH, kare, yk)


def sahne352():
    """'Haritayı çizen adamın boynu vuruluyor.' (idam gösterilmez): aynı avlu, gece; kimse yok. Kaptanın durduğu
    yerde yere bırakılmış tek fener yanar."""
    _kahire_avlu(352, ["#06081a", "#0e1230", "#1a1c40", "#2a2448", "#3a2c50"], ["#3a3448", "#34303f", "#2e2a38"],
                 ["#4a4050", "#423a48", "#3a3440", "#322e38", "#2a2830"], "#7a6a80", ev="#5a5060", tas="#6a6474",
                 kubbe="#3a4250", gece=True)
    _yildiz_ekle(352, 80, 384, 470)
    yk = 2.8
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, fener, 168, z, round(0.42 * K, 1), f=f)

    _spr2(352, DW, DH, kare, yk, esik=0.5)


# ==========================================================================
# 331 · kart 2-3, 51 · Bugün, Topkapı: vitrinde parşömen harita; iki ziyaretçi bakar
# ==========================================================================
def sahne331():
    """'Harita bugün Topkapı'da.': müze odası, çini kuşaklı duvar; ortada eğik camlı vitrin, içinde parşömen. Solda ve
    sağda bugünün iki ziyaretçisi vitrine bakar."""
    ic_mekan(331, duvar=("#2a3a3a", "#344a48", "#425a56"), kemer="#1a2a28", cini="#2a6a9a",
             pencere=("#8ab0c8", "#c8dcec"), zemin_renk=("#6a5a4a", "#5a4c3e", "#4a3e32"), isik="#f8e0a0", hali=False)
    yk = 2.8
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, vitrin, 200, z, round(0.46 * K, 1))
        figur(t, kisi, 136, z, round(0.95 * K, 1), govde="#b84a3a", bas="ortu", bas_renk="#2a3a5a", sakal=None, yon=1,
              kadin=True, kemer=None, kol=0.02 * (1 + SIN(f)))
        figur(t, kisi, 262, z, K, govde="#3a5a7a", bas="takke", bas_renk="#2a1a12", sakal=None, yon=-1, kemer=None,
              kol=0.05 + 0.04 * SIN(f + 0.4))

    _spr2(331, IW, IH, kare, yk)


# ==========================================================================
# 332 · kart 4 · Korsan kadırgasının güvertesi: genç Piri ve amcası Kemal Reis; uzakta İspanya kıyısı ve kale
# ==========================================================================
def _deniz_uzak(no, gok_alt, deniz, tepe, dag_y=(452, 476), tepe_y=480, ova_y=490, kale=None, gemiler=()):
    img = uzak(no, [tepe[0], tepe[1]], [tepe[1], tepe[0]], deniz, dag_y=dag_y, tepe_y=tepe_y, ova_y=ova_y)
    d = ImageDraw.Draw(img)
    if kale:
        x0, x1, s_, tas = kale
        d.rectangle([x0 - 16, ova_y - 4, x1 + 16, ova_y], fill=hex2(tepe[1]))           # kıyı şeridi: düz
        figur(img, anadolu_kalesi, x0, x1, duz(ova_y - 3, W), s_, tas=tas, golge=_ac(tas, -0.25), kapi=True)
    for x, s_, yelken, port in gemiler:
        if port:
            portekiz_gemisi(img, x, ova_y + int(6 * s_), s_, 1, 0.0)
        else:
            figur(img, gemi, x, ova_y + int(6 * s_), s_, 1, 0.0, govde=GOVDE, yelken=yelken, hac=False)
    kaydet(img, f"sahne{no}-uzak.png")


def sahne332():
    """'Gençliğinde amcası Kemal Reis'in yanında korsan,': parlak gün; kadırganın güvertesi, arkada küpeşte. Kemal Reis
    (kızıl kaftan) kıyıyı gösterir, genç Piri yanında; uzakta İspanya kıyısında kale ve bir kadırga daha."""
    _sahne_gok(332, ["#4a7ab8", "#6a94c8", "#8aacd4", "#aac4dc", "#c8d8e0"], [(120, 404, 22), (400, 410, 20)],
               ("#ffffff", "#eef2f6", "#c8d4e0"))
    _deniz_uzak(332, None, ["#3a6a9a", "#346292", "#2e5a88"], ["#9a8a6a", "#8a7a5e"], kale=(300, 380, 0.8, "#c8b898"),
                gemiler=[(160, 0.8, YELKEN, False)])
    _guverte(332)
    _bos_on(332)
    yk = 2.6
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, halat, 122, z, round(0.32 * K, 1))
        figur(t, fici, 286, z, round(0.4 * K, 1))
        figur(t, kisi, 168, z, round(0.95 * K, 1), **PIRI_GENC, yon=1, kol=0.03 * (1 + SIN(f)))
        figur(t, kisi, 234, z, K, **KEMAL, yon=-1, silah="kilic", kol=0.25 + 0.05 * SIN(f))

    _spr2(332, DW, DH, kare, yk)


# ==========================================================================
# 333 · kart 5 · Fırtına: iki kadırga kabaran denizde; yağmur ve şimşek parıltısı (batış çizilmez)
# ==========================================================================
FIRTINA_SU = ["#2a3a4a", "#24343f", "#1e2e38", "#182830", "#142228"]


def _deniz_sprite(no, gemiler, renkler, yk, esik=0.5, kopuk=1.0, ekle=None):
    """Deniz sprite'ı: gemiler (x, su_y, s, yon, yelken, portekiz, faz_kayma) arkadan öne çizilir; her geminin
    su çizgisinden aşağısı suyla örtülür (gövdenin altı suda)."""
    sirali = sorted(gemiler, key=lambda g: g[1])
    for g in sirali:
        _gemi_denetimi(g[2], g[1], SW, SH, g[0])

    def kare(t, z, i):
        f = i / KARE
        if ekle:
            ekle(t, f, "arka")
        for j, (x, su, s_, yon, yelken, port, kay) in enumerate(sirali):
            ff = (f + kay) % 1
            if port:
                portekiz_gemisi(t, x, su, s_, yon, ff)
            else:
                figur(t, gemi, x, su, s_, yon, ff, govde=GOVDE, yelken=yelken, hac=False)
            _su(t, su, renkler, f, tohum=no + j, dalga=kopuk)
        if ekle:
            ekle(t, f, "on")

    _spr2(no, SW, SH, kare, yk, esik=esik, taban=ST)


def sahne333():
    """'Amcası fırtınada gemisiyle batıyor.': kurşuni fırtına; iki kadırga kabaran dalgalarda iner kalkar, yağmur
    yana yağar, şimşek gökyüzünü bir an aydınlatır. Batış anı çizilmez."""
    _sahne_gok(333, ["#141a24", "#1c2430", "#262e3a", "#303846", "#3a4250"], [(130, 404, 24), (420, 400, 26)],
               ("#5a6474", "#46505e", "#343c48"))
    _deniz_uzak(333, None, ["#2a3a48", "#263442", "#222e3c"], ["#30384a", "#2a3242"], dag_y=(470, 486), tepe_y=488)
    _orta_deniz(333, 552, ["#2a3a48", "#263442", "#222e3c", "#1e2a36", "#1a2630"], kenar="#8aa0b8")
    _bos_on(333)
    _hava(333, 320, "#a8b8cc", 0.35)
    _deniz_sprite(333, [(150, SU, 3.0, 1, "#c8bca0", False, 0.0), (262, SU - 14, 2.3, 1, "#b8ac90", False, 0.4)],
                  FIRTINA_SU, 2.4, kopuk=2.0)


# ==========================================================================
# 334 · kart 6 · Gelibolu kıyısı, akşam: Piri kasabaya yürür
# ==========================================================================
def sahne334():
    """'Piri Gelibolu'ya çekiliyor ve kalemi eline alıyor.': altın akşam; boğaz kıyısında Gelibolu'nun kerpiç ve taş
    evleri, bir cami; Piri kıyı yolunda kasabaya (sağa) yürür."""
    _sahne_gok(334, ["#4a5a8a", "#7a7a9a", "#b0909a", "#d8a890", "#ecc498"], [(120, 404, 20), (420, 408, 22)],
               ("#fff4e4", "#f0d4c0", "#d0a8a0"))
    _deniz_uzak(334, None, ["#6a7aa0", "#62729a", "#5a6a92"], ["#7a7a90", "#6e6e86"], dag_y=(452, 476), tepe_y=480,
                ova_y=492)

    def ekle(img, z):
        figur(img, koy_evleri, PAY + 210, PAY + 560, duz(588), 2.2, tohum=334, kerpic="#d8b890")
        figur(img, osmanli_camii, PAY + 380, duz(586), 1.2, tas="#e0d4c0")

    orta(334, (556, 560), ["#9a9a6a", "#8c8c5e", "#7e7e54", "#70704a", "#626240"], "#d8d0a0", ekle=ekle)
    on(334, ["#626240", "#70704a", "#7e7e54"], "#d8d0a0", boy=90)
    yk = 2.8
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 200, z, K, **PIRI_1513, yon=1, adim=f)

    _spr2(334, DW, DH, kare, yk, esik=0.7)


# ==========================================================================
# 335 · kart 7-8 · Gelibolu, 1513 baharı: Piri minderde, alçak masada ceylan derisi parşömen
# ==========================================================================
def sahne335():
    """'Önünde ceylan derisi bir parşömen.' / 'İmzası: Kemal Reis'in yeğeni Piri.': akşam, sıcak oda; Piri minderde
    oturur, kalemi elinde; önündeki alçak masada parşömen harita (360'taki masayla aynı çizim)."""
    ic_mekan(335, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a8a",
             pencere=("#2a3a6a", "#f0d8b0"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"), isik="#f8c060", hali=True)
    yk = 3.0
    so = s_oturan(yk, 0.30)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 262, 0, f, zincir=_kz(yk))
        mumluk(t, 292, z, f, 2)
        figur(t, oturan, 160, z, so, yon=1, el="kalem", minder="#8a2a2a", **{k: v for k, v in PIRI_1513.items()})
        figur(t, harita_masasi, 222, z, round(0.85 * so, 1))

    _spr2(335, IW, IH, kare, yk)


# ==========================================================================
# 336 · kart 9-10 · Kuşbakışı masa: kalem kenara kaynakları yazar; yanda eski haritalar (rulolar) ve Arap haritası
# 337 · kart 11, 50 · aynı masa: dört Portekiz haritası ve Kolomb'un haritası da masada (Kolomb'unki parlar)
# ==========================================================================
def _yakin_masa(no, kaynak=1, el=False, vurgu=None, renk=PARSOMEN, tur="ahsap", masa="#6a4426", isik="#1a0e06",
                ps=1.05, px=150, esik=0.6, kalem_renk="#2a5a6a"):
    _masa_ustu(no, masa, tur, isik)
    yk = 2.2

    def kare(t, z, i):
        f = i / KARE
        if kaynak >= 1:
            for x, y in ((252, 152), (266, 164), (248, 176)):
                eski_tomar(t, x, duz(y, SW), 1.1)
            arap_haritasi(t, 286, duz(214, SW), 1.15)
        if kaynak >= 2:
            for j, (x, y) in enumerate(((238, 236), (262, 240), (244, 256), (270, 260))):
                portekiz_haritasi(t, x, duz(y, SW), 1.15, tohum=j)
            kolomb_haritasi(t, 268, duz(292, SW), 1.3, f=f)
        n = figur(t, parsomen_harita, px, z, ps, renk=renk, vurgu=vurgu, f=f, kontur="#2a1a10")
        if el:
            hokka(t, 232, duz(298, SW), 1.0)
            ux, uy = n["not"]
            yazan_el(t, (ux + 2, uy + 8), 1.0, f, kol=kalem_renk)

    _spr2(no, SW, SH, kare, yk, esik=esik, taban=IT, orta_bant=False)


def sahne336():
    """'Kenara kaynaklarını yazıyor: yirmi kadar harita.' / 'eski haritalar, bir Arap haritası': kuşbakışı ahşap masa;
    ceylan derisi parşömen, kenar notunu yazan el ve kalem, hokka; sağda dürülmüş eski haritalar ve yuvarlak Arap haritası."""
    _yakin_masa(336, kaynak=1, el=True)


def sahne337():
    """'dört Portekiz haritası. Bir de Kolomb'un haritası.': aynı masa; dört portolan ve altın çerçeveli Kolomb haritası
    da eklenmiş. El yok: kaynaklar masada."""
    _yakin_masa(337, kaynak=2, el=False)


# ==========================================================================
# 338 · kart 12 · Gece odası: amcasının İspanyol esiri anlatır, Piri minderde yazar
# ==========================================================================
def sahne338():
    """'Kolomb'la üç kez o topraklara gitmiş. Anlattıklarını Piri not ediyor.': gece, mum ışığı; solda başı açık
    İspanyol esir eliyle uzakları gösterir, sağda Piri minderde rahlesine yazar."""
    ic_mekan(338, duvar=("#2a2230", "#362c3c", "#44384a"), kemer="#1a1420", cini="#6a3a2a",
             pencere=("#0e1430", "#f4f0d8"), zemin_renk=("#4a3c38", "#3e322e", "#322824"), isik="#f8c060", hali=True)
    yk = 3.0
    K = s_kisi(yk, 0.30)
    so = s_oturan(yk, 0.30)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 205, 0, f, zincir=_kz(yk))
        mumluk(t, 290, z, f, 1)
        figur(t, kisi, 146, z, K, **ESIR, yon=1, kol=0.35 + 0.2 * SIN(f))
        figur(t, oturan, 252, z, so, yon=-1, el="kalem", minder="#8a2a2a", **PIRI_GENC)
        rahle(t, 252 - int(4.2 * so), z[0], round(0.95 * so, 1))

    _spr2(338, IW, IH, kare, yk)


# ==========================================================================
# 339 · kart 13 · Mısır, 1517: otağ önünde tahtta Yavuz; diz çökmüş Piri haritayı sunar; uzakta piramitler
# ==========================================================================
def sahne339():
    """'Mısır, 1517. Yavuz Memlükleri yeni yenmiş. Piri haritayı padişaha sunuyor.': sıcak öğleden sonra; çöl ovası,
    ufukta piramitler; otağın önünde tahtta Yavuz Sultan Selim, önünde diz çökmüş Piri elinde haritayla."""
    _sahne_gok(339, ["#6a90c0", "#8aa8c8", "#b0bcc4", "#d8ccb0", "#ecd8a8"], [(110, 404, 20), (430, 408, 18)],
               ("#fff8ec", "#f4e4cc", "#d8c0a0"))
    img = uzak(339, ["#c8a878", "#bc9c6c"], ["#d0b080", "#c4a474"], ["#d8bc88", "#ccb07c", "#c0a470"],
               dag_y=(470, 484), tepe_y=486, ova_y=494)
    for x, s_ in ((96, 1.2), (130, 0.8), (440, 1.0)):
        piramit(img, x, duz(494, W), s_)
    kaydet(img, "sahne339-uzak.png")

    def ekle(img, z):
        figur(img, otag, PAY + 270, duz(586), 1.8, "#c8302a", "#e0b040", faz=0.2, acik=True)

    orta(339, (552, 558), ["#d0b07a", "#c4a46e", "#b89862", "#ac8c58", "#a0804e"], "#f0d8a0", ekle=ekle)
    on(339, ["#a0804e", "#ac8c58", "#b89862"], "#f0d8a0", boy=60)
    yk = 2.8
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        ust = figur(t, taht, 245, z, round(0.62 * K, 1), renk="#c8a040", ortu="#8a1e22")
        figur(t, oturan, 245, duz(ust, t.width), round(0.62 * K, 1), yon=-1, minder="#2a6a3a", **YAVUZ)
        figur(t, kisi, 170, z, K, **PIRI_1513, yon=1, diz=True, silah="mektup", kol=0.4 + 0.03 * SIN(f))

    _spr2(339, DW, DH, kare, yk)


# ==========================================================================
# 340 · kart 14 · Saray hazinesi: sandığın üstünde dürülmüş harita; raflarda rulolar; tek kandil
# ==========================================================================
def sahne340():
    """'Harita saraya giriyor. Dört yüz yılı aşkın unutulacak.': loş hazine odası; ortada demir kuşaklı sandık, üstünde
    dürülmüş parşömen; arkada rulo dolu raflar. Kimse yok, tek kandil sallanır."""
    ic_mekan(340, duvar=("#1e1a1a", "#282220", "#322a26"), kemer="#120e0c", cini="#5a4a2a",
             pencere=None, zemin_renk=("#3e3830", "#342e28", "#2a2620"), isik="#c89040", hali=False)
    yk = 3.0
    K = s_kisi(yk)

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 12, IW)
        kandil(t, 200, 0, f, zincir=_kz(yk))
        figur(t, kitap_rafi, 142, arka, round(0.55 * K, 1), rulo=True, tohum=1)
        figur(t, kitap_rafi, 262, arka, round(0.55 * K, 1), rulo=True, tohum=2)
        figur(t, sandik, 202, z, round(0.6 * K, 1))

    _spr2(340, IW, IH, kare, yk, esik=0.6)
