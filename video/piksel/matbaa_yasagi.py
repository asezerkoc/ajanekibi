"""Fermanı Gören Yok: Osmanlı'da "matbaa yasağı" efsanesi ve İbrahim Müteferrika (1584-1747, bugün). Piksel Tarih
(@pikseltarihim), sahneler 170-209. Grafikerin tarifi: teslimler/gece/ara/matbaa-yasagi/5-grafik.md; metin ve 49 kart
4-kalite-metin.md'den. Kalıp: takiyuddin_rasathanesi.py ve cem_sultan.py (ölçek/kadraj yardımcıları buraya kopyalandı).
Yön dili: sağ = İstanbul'a / ileriye (gelen, basan), sol = Avrupa'ya / geriye.
Tek kaynak: yakin, sprite ölçüleri ve kart metinleri video/src/sahneler/MatbaaYasagi.tsx'ten okunur; her sahne çizildikten
sonra figürlerin ve orta plandaki yapıların yazı bandına girmediği PNG üzerinden denetlenir (betik durur).
Kullanım: python3 -I video/piksel/matbaa_yasagi.py [sahne numaraları]

Yeni figürler (bu dosyada; ciz.py'ye eklenmedi, yalnızca piksel()/hex2()/ImageDraw ve mevcut figürlerle yazıldı):
  tahta_pres        tahta el baskı presi: iki dikme kızaklarla zemine basar, başlık, vida, inen kalkan plaka, yana uzanan
                    tabla (uç ayakları yere iner), harf kalıbı ve kâğıt. Kol, baskıcının eline bağlanır (_pres_kolu).
  sandalyeli        sandalyede oturan Avrupalı yazar: sandalyenin dört ayağı ve yazarın ayakları zemine basar; eli masada,
                    tüy kalem elinde (yazma hareketi f ile).
  yazi_masasi       ahşap masa: ayakları zemine basar; üstünde kâğıt, hokka, mum, kitap ya da açık basılı kitap.
  acik_kitap        rahlede açık kitap (rahlenin çapraz ayakları zemine basar): Öklid (geometri + izin fermanı), Vankulu
                    (tuğralı ilk sayfa), resimli tarih (tahta baskı gemi resmi), Gutenberg (iki sütun), İbranice sayfa.
  bos_rahle         üstü boş rahle (motif: "fermanı gören yok").
  kurutma_ipi       iki direk zemine dikili, aralarındaki ipte basılmış sayfalar asılı kuruyor.
  raf, kitap_yigini kitap rafı (dolu / tozlu / arşiv kutulu) ve yerde kitap yığınları; hepsi zemine oturur.
  ahsap_ev          iki katlı İstanbul ahşap evi (cumbalı), düz zemine kurulur; karlı dam seçeneği.
  saray_kapisi      Bâbüsselâm'dan esinli saray kapısı: iki sekizgen kule, kurşun külahlar, kemerli kapı; düz zemine kurulur.
  kagithane         Yalova kâğıthanesi: taş değirmen evi düz zemine kurulur; yanındaki su çarkının alt kısmı zemine oturan
                    tahta oluğun suyunda döner.
  sunak             kilise sunağı: masa ayakları zemine basar, üstünde ayaklı haç ve iki mum.
  sahaf_tezgahi     çarşı tezgâhı: tezgâh ve sundurma direkleri zemine basar, üstünde el yazması kitaplar.
  modern_kisi       bugünün insanı: timur_figur.kisi gövdesi, açık başta saç, kemersiz.
  sarkit_lamba      bugünün tavan lambası (arşiv): kablo tavandan iner, metal şapka, ampul (kandilin modern karşılığı).
  cilt              kapalı kalın cilt (yere yatık), kitap_bohcasi (alıcının kolunun altındaki kitaplar).
"""
import math
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw  # noqa: E402

from ciz import KOYU, _ac, _esik, agac, cimen_tutamlari, duz_zemin, figur, gunes, hex2, patika, piksel, temas_golgesi, yeni, zemin_y  # noqa: E402
from sahneler import GW, duz, gokyuzu, kaydet, on, orta, sprite, uzak  # noqa: E402
from timur_figur import _baslik, anadolu_kalesi, kisi, oturan, sedir  # noqa: E402
from timur import besik, hava, ic_mekan, kandil, mumluk, su_ve_kiyi  # noqa: E402
from kalender import kitaplar, rahle, taht  # noqa: E402

KARE = 24      # sprite kare sayısı (SKILL.md)
PAY = 135      # orta/ön plan yan payı (SKILL.md)
SIN = lambda f, k=1: math.sin(f * 2 * math.pi * k)  # noqa: E731
PUBLIC = Path(__file__).parents[1] / "public"
TSX = Path(__file__).parents[1] / "src" / "sahneler" / "MatbaaYasagi.tsx"


def _u(v, s):
    return max(1, int(round(v * s)))


def _r(d, x0, y0, x1, y1, **kw):
    """Köşeleri sıralı dikdörtgen (PIL ters sırayı kabul etmez)."""
    d.rectangle([min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)], **kw)


# ==========================================================================
# TSX: tek kaynak (yakin, sprite, kartlar)
# ==========================================================================
def _tsx_oku():
    metin = TSX.read_text()
    govde = metin[metin.index("bolumler:"):metin.index("kapanis:")]
    sonuc = {}
    for b in re.split(r"\n    \{", govde)[1:]:
        no = int(re.search(r"no: (\d+)", b).group(1))
        yk = float(re.search(r"yakin: ([\d.]+)", b).group(1))
        sp = re.search(r"sprite: \{ w: (\d+), h: (\d+), fps: (\d+), x: (\[[\d, ]+\]|\d+), taban: (\d+) \}", b)
        x = [int(v) for v in re.findall(r"\d+", sp.group(4))]
        yy = re.search(r"yaziY: (\d+)", b)
        od = re.search(r"odakY: (\d+)", b)
        kartlar = []
        for m in re.finditer(r"satirlar: \[([^\]]*)\], sure: [\d.]+(?:, boy: (\d+))?", b):
            kartlar.append((re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1)), int(m.group(2) or 92)))
        kayit = dict(no=no, yk=yk, w=int(sp.group(1)), h=int(sp.group(2)), fps=int(sp.group(3)),
                     x=x if len(x) > 1 else x[0], taban=int(sp.group(5)), yaziY=int(yy.group(1)) if yy else 300,
                     odak=int(od.group(1)) if od else None, kartlar=kartlar, kapak="// KAPAK" in b.split("\n")[0])
        sonuc.setdefault(no, []).append(kayit)
    return sonuc


_BOLUM = _tsx_oku()


class _P(dict):
    __getattr__ = dict.get


def P(no):
    """Sahnenin (kapak olmayan) Bolum ayarları."""
    return _P([b for b in _BOLUM[no] if not b["kapak"]][0])


# ==========================================================================
# Ölçek ve kadraj yardımcıları (cem_sultan.py / takiyuddin_rasathanesi.py kalıbı; yeni çizim fonksiyonu DEĞİL:
# figürü boş yüzeye çizip alfa kanalından ölçer).
# ==========================================================================
def _bb(img):
    return img.getchannel("A").getbbox()


_ONBELLEK = {}


def olcek(ad, yakin, cizim, oran=0.32):
    """Figür kutusu kadraj yüksekliğinin >= oran'ı olan en küçük s (0.1 adım). Görünen ızgara yüksekliği = 960/yakin."""
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
            break
        if bb and bb[3] - bb[1] >= hedef:
            _ONBELLEK[anahtar] = round(s, 1)
            return _ONBELLEK[anahtar]
        s += 0.1
    raise RuntimeError(f"olcek({ad}, yakin={yakin}): %{int(oran * 100)} boya ulaşılamadı")


def s_kisi(yakin, oran=0.32):
    return olcek("kisi", yakin, lambda t, s, z: figur(t, kisi, 280, z, s, govde="#5a4a3a", bas="sarik",
                                                       bas_renk="#ece6d8", sakal="#4a3a2a", yon=1), oran)


def s_oturan(yakin, oran=0.30):
    return olcek("oturan", yakin, lambda t, s, z: figur(t, oturan, 280, z, s, govde="#5a4a3a", bas="sarik",
                                                         bas_renk="#ece6d8", sakal="#4a3a2a", yon=1, minder="#c8a040"), oran)


def s_sandalye(yakin, oran=0.30):
    return olcek("sandalye", yakin, lambda t, s, z: figur(t, sandalyeli, 280, z, s, govde="#5a4632", bas="sapka",
                                                           bas_renk="#1e1a18", sakal="#6a5a4a", yon=1), oran)


def _kz(yakin, taban=634, h=300):
    """Kandil zinciri: sprite'ın üst kenarından (tavan) kadrajın üst kenarının biraz altına."""
    ust_gorunen = (taban - 12) * (1 - 1 / yakin)
    return max(40, int(ust_gorunen - (taban - h)) + 10)


def _kadraj(no, kare, w, h, yakin, esik):
    """Görünür aralık yerel x = w/2 ± 270/yakin (sahne sonundaki %6 yakınlaşma dahil). Opak piksellerin en az `esik`
    oranı içeride olmalı; figür sprite'ın üstüne değmemeli (kesik baş = hata)."""
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
            raise RuntimeError(f"Sahne {no}: figürlerin %{int(100 * ici / toplam)}'i görünür aralıkta (x {a}-{b})")


def _bantlar(no):
    """Sahnenin her kartı için yazı bandı (dünya y'si, ızgara). Ekranda yazı (yaziY)/2'den başlar; satır yüksekliği
    TimurSeri.Yazi ile aynı hesap (boy, 30 harf sığdırma, 1,12 satır aralığı, 7 px gölge). Yakınlaşma odakY çevresinde
    yakin..1,06·yakin: en sıkı durum ikisinden biri."""
    sonuc = []
    for b in _BOLUM[no]:
        o = b["odak"] if b["odak"] is not None else b["taban"] - 12
        ust = b["yaziY"] / 2
        for sat, boy in b["kartlar"]:
            sig = min(boy, math.floor(950 / (max(len(x) for x in sat) * 0.46)))
            alt = (b["yaziY"] + len(sat) * sig * 1.12 + 8) / 2
            for z in (b["yk"], b["yk"] * 1.06):
                sonuc.append((z, int(o - (o - ust) / z), int(o - (o - alt) / z) + 3, b))
    return sonuc


def _bant_denetimi(no):
    """Sprite (her 3 karede bir) ve orta plan: görünür sütunlarda yazı bandına giren opak piksel (alfa > 200) satırı
    2 pikselden fazla olamaz (tavandan inen 1 px kandil zinciri/kablo bilinçli istisna)."""
    p = P(no)
    spr = Image.open(PUBLIC / f"sahne{no}-karakter.png").convert("RGBA").getchannel("A").point(lambda v: 255 if v > 200 else 0)
    ort = Image.open(PUBLIC / f"sahne{no}-orta.png").convert("RGBA").getchannel("A").point(lambda v: 255 if v > 200 else 0)
    xs = p.x if isinstance(p.x, list) else [p.x]
    for z, y0, y1, b in _bantlar(no):
        yar = 270 / z
        for i in range(0, KARE, 3):
            for y in range(max(y0, p.taban - p.h), y1 + 1):
                ly = y - (p.taban - p.h)
                n = sum(spr.crop((i * p.w + int(p.w / 2 - yar), ly, i * p.w + int(p.w / 2 + yar), ly + 1)).histogram()[1:])
                if n > 2:
                    raise RuntimeError(f"Sahne {no}: sprite (kare {i}) yazı bandına giriyor: dünya y {y} (bant {y0}-{y1}, "
                                       f"yakin {z:.2f}); figürü küçült ya da alçalt")
        for sx in xs:
            for y in range(y0, y1 + 1):
                n = sum(ort.crop((PAY + int(sx - yar), y, PAY + int(sx + yar), y + 1)).histogram()[1:])
                if n > 2:
                    raise RuntimeError(f"Sahne {no}: orta plandaki yapı yazı bandına giriyor: y {y} (bant {y0}-{y1})")


def bant_alt(no):
    """Sahnenin bütün kartları ve yakınlaşma için yazı bandının en alt dünya y'si."""
    return max(y1 for _, _, y1, _ in _bantlar(no))


def _spr(no, kare, esik=0.75):
    p = P(no)
    _kadraj(no, kare, p.w, p.h, p.yk * 1.06, esik)
    sprite(no, "karakter", p.w, p.h, KARE, kare)      # taban_denetimi varsayılan açık
    _bant_denetimi(no)


def _gorunur(no, xler, pay=12):
    """Orta plandaki (hareketsiz) önemli figürlerin ızgara x'i, sprite'ın baş ve son sx'inde görünür aralıkta."""
    p = P(no)
    for sx in (p.x if isinstance(p.x, list) else [p.x]):
        a, b = sx - 270 / (p.yk * 1.06) + pay, sx + 270 / (p.yk * 1.06) - pay
        for x in xler:
            if not a <= x <= b:
                raise RuntimeError(f"Sahne {no}: orta plan figürü x={x} görünür aralık [{int(a)}, {int(b)}] dışında (sx={sx})")


def _el(x, z, s, yon, kol):
    """kisi() figürünün el ucu (timur_figur.kisi ile aynı formül; ayakta, diz=False, yürümüyor)."""
    y = zemin_y(z, x, 6 * s)
    ust = y - int(11 * s)
    if kol > 0:
        return x + int(3.5 * s) * yon, ust - int(4 * s * kol) + int(1 * s)
    return x + int(2.5 * s) * yon, ust + int(5 * s)


def _oturan_el(x, z, s, yon, minder=True):
    """oturan() figürünün el ucu (timur_figur.oturan ile aynı formül)."""
    y = zemin_y(z, x, 10 * s) - (int(1.6 * s) if minder else 0)
    return x + int(3 * s) * yon, y - int(4.5 * s)


# ==========================================================================
# KİŞİLER (renk kimlikleri bütün sahnelerde aynı)
# ==========================================================================
THEVET = dict(govde="#5a4632", bas="sapka", bas_renk="#1e1a18", sakal="#6a5a4a", kemer="#2a1e14")       # Fransisken kahvesi
MARSIGLI = dict(govde="#7a2a2a", bas="sapka", bas_renk="#1a1a22", sakal=None, kemer="#c8a040")
NAHMIAS1 = dict(govde="#3a3a5a", bas="kalpak", bas_renk="#2a2a30", sakal="#2a1a12", kemer="#8a7a5a")
NAHMIAS2 = dict(govde="#4a3a2a", bas="kalpak", bas_renk="#2a2a30", sakal="#4a3020", kemer="#8a7a5a")
ABGAR = dict(govde="#3a2a3a", bas="kalpak", bas_renk="#1a1418", sakal="#3a2a1a", kemer="#a88a4a")
ABGAR_OGUL = dict(govde="#4a4a5a", bas="kalpak", bas_renk="#1a1418", sakal=None, kemer="#a88a4a")
MURAD = dict(govde="#8a1e22", bas="sarik", bas_renk="#f8f4ea", sakal="#4a2a16")                       # III. Murad
AHMED = dict(govde="#2a4a7a", bas="sarik", bas_renk="#f8f4ea", sakal="#2a1a12")                       # III. Ahmed
KATIP = dict(govde="#5a4a6a", bas="sarik", bas_renk="#ece6d8", sakal="#4a3a2a")
METAKSAS = dict(govde="#1e1e24", bas="kalpak", bas_renk="#141418", sakal="#6a5a4a", kemer=None)         # Rum rahip, siyah
CIZVIT = dict(govde="#1a1a20", bas="sapka", bas_renk="#101014", sakal=None, kemer=None)
MEMUR = dict(govde="#2a5a3a", bas="sarik", bas_renk="#f2ece0", sakal="#2a1a12")
YENICERI = dict(govde="#3a4a7a", bas="bork", bas_renk="#ece6d8", sakal="#2a1a12")
KOPYACI = dict(govde="#4a5a4a", bas="sarik", bas_renk="#ece6d8", sakal="#3a2a1a")
KOPYACI2 = dict(govde="#6a4a3a", bas="sarik", bas_renk="#ece6d8", sakal="#d8d0c8")
IBRAHIM_MACAR = dict(govde="#2a3a5a", bas="kalpak", bas_renk="#3a2a1a", sakal=None, kemer="#c8a040")   # Kolozsvár'dan gelen genç
IBRAHIM = dict(govde="#5a4a3a", bas="sarik", bas_renk="#ece6d8", sakal="#4a3a2a")                     # Müteferrika
IBRAHIM_YASLI = dict(IBRAHIM, sakal="#e0dcd4")
SADRAZAM = dict(govde="#2a6a3a", bas="sarik", bas_renk="#f2ece0", sakal="#3a2a1a")
SAID = dict(govde="#6a3a6a", bas="sarik", bas_renk="#f2ece0", sakal=None)                              # genç Said, 1720
FRANSIZ = dict(govde="#6a5a44", bas="sapka", bas_renk="#1a1a22", sakal=None, kemer="#e8e0d0")          # Paris'li baskıcı
SEYHULISLAM = dict(govde="#e4e0d4", bas="sarik", bas_renk="#f8f6f0", sakal="#d8d0c8")
HATTAT = dict(govde="#3a4a6a", bas="sarik", bas_renk="#ece6d8", sakal="#2a1a12")
HATTAT2 = dict(govde="#5a3a3a", bas="sarik", bas_renk="#ece6d8", sakal="#a8a098")
USTA_LEH = dict(govde="#4a3a2a", bas="kalpak", bas_renk="#6a4a30", sakal="#8a6a4a", kemer="#8a2a2a")    # Lehistanlı kâğıt ustası
BASKICI = dict(govde="#6a5a44", bas="sarik", bas_renk="#ece6d8", sakal="#3a2a1a")
SAHAF = dict(govde="#6a5a3a", bas="sarik", bas_renk="#ece6d8", sakal="#8a8078")
ALICI = dict(govde="#3a5a6a", bas="sarik", bas_renk="#ece6d8", sakal="#2a1a12")
KADIN_ERDEL = dict(govde="#6a2a2a", bas="ortu", bas_renk="#e8e0d0", sakal=None, kadin=True, kemer="#e0b040")
YOLCU = dict(govde="#4a4a3a", bas="kalpak", bas_renk="#3a2a1a", sakal=None, kemer="#8a6a3a")


# ==========================================================================
# YENİ FİGÜRLER
# ==========================================================================
AGAC = "#6a4a2a"
DEMIR = "#3a3a40"


def _tugra(img, cx, cy, s, renk="#2a2a6a", altin="#c8a040"):
    """Küçük tuğra işareti (sayfa ve ferman üstünde): üç dikey kol, solda iç içe iki kavis, sağa uzanan kol."""
    d = ImageDraw.Draw(img)
    k = hex2(renk)
    for dx in (-0.6, 0.0, 0.6):
        d.line([cx + int(dx * s), cy, cx + int(dx * s), cy - int(2.8 * s)], fill=k)
    d.ellipse([cx - int(3.2 * s), cy - int(1.4 * s), cx - int(0.4 * s), cy + int(0.6 * s)], outline=k)
    d.ellipse([cx - int(2.4 * s), cy - int(0.9 * s), cx - int(1.0 * s), cy + int(0.2 * s)], outline=hex2(altin))
    d.line([cx - int(0.4 * s), cy + 1, cx + int(2.6 * s), cy - int(0.4 * s)], fill=k)
    d.line([cx - int(1 * s), cy + int(0.9 * s), cx + int(2 * s), cy + int(0.9 * s)], fill=hex2(altin))


def _satirlar(img, x0, y0, x1, y1, renk="#3a2a1a", aralik=2, tohum=1, rtl=False, kirmizi=None):
    """Sayfada yazı satırları: kelime kelime kesik piksel çizgiler (okunmaz, yazı dokusu)."""
    rnd = random.Random(tohum)
    for k, yy in enumerate(range(int(y0), int(y1), aralik)):
        x = x1 if rtl else x0
        while (x > x0 + 1) if rtl else (x < x1 - 1):
            boy = rnd.randint(2, 5)
            a, b = (x - boy, x) if rtl else (x, x + boy)
            a, b = max(a, x0), min(b, x1)
            r = kirmizi if (kirmizi and k == 0) else renk
            ImageDraw.Draw(img).line([a, yy, b, yy], fill=hex2(r))
            x = x - boy - 1 if rtl else x + boy + 1


def tahta_pres(img, x, zemin, s=1.0, faz=0.0, yon=1, kagit=True, tugra=False, ag=False, kol_el=None):
    """Yeni figür: tahta el baskı presi (s, kisi ölçeğiyle aynı birim: pres ≈ 19 s, insan boyu kadar). İki dikme
    kızaklarla zemine basar; başlık, vida, inen kalkan plaka; tabla baskıcının karşı yanına uzanır, uç ayağı yere
    iner; tablada harf kalıbı ve kâğıt (tugra=True: kâğıtta tuğra). faz 0→1 plaka iner kalkar (dikişsiz).
    kol_el: baskıcının el noktası verilirse kol vidadan ele uzanır; yoksa kol yana dayalı durur. ag: köşede örümcek ağı.
    Dönen değer: vidanın kol bağlantı noktası."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 10 * s)
    temas_golgesi(img, x + int(2.5 * s) * yon, y, 22 * s)
    koyu, acik = hex2(_ac(AGAC, -0.3)), hex2(_ac(AGAC, 0.2))
    bw = max(2, int(1.3 * s))
    for k in (-1, 1):                                                                    # kızaklar ve dikmeler
        cx = x + k * int(4 * s)
        _r(d, cx - int(1.8 * s), y - _u(1.0, s), cx + int(1.8 * s), y - 1, fill=koyu)
        _r(d, cx - bw // 2, y - int(18.4 * s), cx + bw // 2, y - 2, fill=hex2(AGAC))
        d.line([cx - bw // 2, y - int(18.4 * s), cx - bw // 2, y - 2], fill=acik)
    _r(d, x - int(5.4 * s), y - int(19.2 * s), x + int(5.4 * s), y - int(17.2 * s), fill=koyu)          # başlık
    d.line([x - int(5.4 * s), y - int(19.2 * s), x + int(5.4 * s), y - int(19.2 * s)], fill=acik)
    _r(d, x - int(4 * s), y - int(13.6 * s), x + int(4 * s), y - int(12.9 * s), fill=hex2(AGAC))     # ara kiriş (dolap)
    ty = y - int(8.6 * s)                                                                # tabla
    t0, t1 = x - int(4.6 * s) * yon, x + int(10.5 * s) * yon
    _r(d, t0, ty, t1, ty + _u(1.0, s), fill=acik)
    _r(d, t1 - _u(0.6, s) * yon, ty + 1, t1, y - 1, fill=koyu)                          # tablanın uç ayağı
    _r(d, x + int(6.6 * s) * yon - _u(0.4, s), ty + 1, x + int(6.6 * s) * yon + _u(0.4, s), y - 1, fill=koyu)
    _r(d, x - int(3 * s), ty - _u(0.7, s), x + int(3 * s), ty - 1, fill=hex2("#2a2a2e"))   # harf kalıbı
    for k in range(-2, 3):
        piksel(img, x + int(k * s), ty - 1, hex2("#8a8a90"))
    if kagit:                                                                            # tablada bekleyen kâğıt
        k0, k1 = x + int(4.6 * s) * yon, x + int(9.8 * s) * yon
        _r(d, k0, ty - _u(0.5, s), k1, ty - 1, fill=hex2("#f0e8d4"))
        if tugra:                                                                        # basılmış sayfa: tuğra + satırlar
            sx0, sx1 = min(k0, k1), max(k0, k1)
            _r(d, sx0, ty - int(5.6 * s), sx1, ty - 1, fill=hex2("#f4ecd8"), outline=hex2("#b8a888"))  # kâğıt kapakta dik
            _tugra(img, (sx0 + sx1) // 2, ty - int(3.8 * s), s * 0.55)
            _satirlar(img, sx0 + _u(0.6, s), ty - int(2.4 * s), sx1 - _u(0.6, s), ty - _u(0.6, s), aralik=2, tohum=3, rtl=True)
    bas = (1 - math.cos(faz * 2 * math.pi)) / 2
    py = y - int(12.4 * s) + int(bas * 2.8 * s)
    py = min(py, ty - _u(0.7, s) - _u(1.0, s) - 1)
    _r(d, x - _u(0.5, s), y - int(17.2 * s), x + _u(0.5, s), py, fill=hex2("#8a8a96"))   # vida
    for vy in range(y - int(17 * s), py, max(2, _u(0.8, s))):
        d.line([x - _u(0.5, s), vy, x + _u(0.5, s), vy + 1], fill=hex2("#5a5a66"))
    _r(d, x - int(3.4 * s), py, x + int(3.4 * s), py + _u(1.0, s), fill=koyu)            # plaka
    vida = (x, y - int(14.8 * s))
    if kol_el is None:                                                                   # kol yana dayalı
        _pres_kolu(img, vida, (x - int(5.5 * s) * yon, y - int(14.2 * s)))
    if ag:                                                                               # örümcek ağı: dikme-başlık köşesi
        ax, ay = x + int(4 * s) - bw // 2, y - int(17.2 * s)
        for k in range(1, 5):
            d.line([ax, ay + int(k * 1.1 * s), ax - int(k * 1.1 * s), ay], fill=hex2("#c8c8c8", 150))
        d.line([ax, ay, ax - int(4.4 * s), ay + int(4.4 * s)], fill=hex2("#c8c8c8", 150))
    return vida


def _pres_kolu(img, vida, el):
    """Pres kolu: vidadan baskıcının eline uzanan demir çubuk (iki ucu da bağlı)."""
    d = ImageDraw.Draw(img)
    d.line([*vida, *el], fill=hex2(DEMIR), width=2)
    d.line([vida[0], vida[1] - 1, el[0], el[1] - 1], fill=hex2("#7a7a84"))


def _baskici(t, px, z, K, pres_x, ps, f, yon=1, **kisi_kw):
    """Presin başında baskıcı: kolu çeker (kol 0.2-0.45, plaka ile aynı fazda); demir kol vidadan eline bağlı."""
    kol = 0.2 + 0.25 * (1 - math.cos(f * 2 * math.pi)) / 2
    vida = figur(t, tahta_pres, pres_x, z, ps, faz=f, yon=yon, kol_el=True, **kisi_kw.pop("pres", {}))
    figur(t, kisi, px, z, K, yon=yon, kol=kol, **kisi_kw)
    _pres_kolu(t, vida, _el(px, z, K, yon, kol))


def sandalyeli(img, x, zemin, s=1.0, govde="#5a4632", bas="sapka", bas_renk="#1e1a18", sakal=None, yon=1, f=0.0,
               masa_ust=None, sac=None, kemer="#2a1e14", ten="#d6a07a"):
    """Yeni figür: sandalyede oturan yazar (Avrupa masası). Sandalyenin ayakları ve yazarın ayakları zemine basar;
    masa_ust verilirse eli masada, tüy kalemle yazar (f ile küçük yazma hareketi); verilmezse eli dizinde."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 8 * s)
    temas_golgesi(img, x + int(1 * s) * yon, y, 10 * s)
    ah, ahk = hex2("#6a4428"), hex2("#4a2e1a")
    oy = y - int(4.2 * s)                                                                # oturak
    for lx in (-2.4, 1.8):
        _r(d, x + int(lx * s) * yon - _u(0.35, s), oy, x + int(lx * s) * yon + _u(0.35, s), y - 1, fill=ahk)
    _r(d, x - int(2.8 * s) * yon, oy - _u(0.7, s), x + int(2.2 * s) * yon, oy, fill=ah)
    sx = x - int(2.6 * s) * yon                                                          # arkalık
    _r(d, sx - _u(0.4, s), y - int(11.2 * s), sx + _u(0.4, s), oy, fill=ah)
    _r(d, sx - _u(0.7, s), y - int(11.8 * s), sx + _u(0.7, s), y - int(11.2 * s), fill=ahk)
    gv, koyu = hex2(govde), hex2(_ac(govde, -0.3))
    kalca = y - int(4.9 * s)                                                             # bacaklar: uyluk yatay, baldır dik
    diz = (x + int(3.2 * s) * yon, kalca)
    d.line([x, kalca, *diz], fill=koyu, width=_u(1.5, s))
    ayak = (x + int(3.5 * s) * yon, y - 1)
    d.line([*diz, *ayak], fill=hex2("#3a2a1e"), width=_u(1.2, s))
    d.line([ayak[0], ayak[1], ayak[0] + _u(1.1, s) * yon, ayak[1]], fill=hex2(KOYU))
    ust = y - int(10.6 * s)
    d.polygon([(x - int(2.4 * s), kalca + _u(0.6, s)), (x - int(1.8 * s), ust), (x + int(1.8 * s), ust),
               (x + int(2.4 * s), kalca + _u(0.6, s))], fill=gv)
    if kemer:
        d.line([x - int(2 * s), ust + int(3.6 * s), x + int(2 * s), ust + int(3.6 * s)], fill=hex2(kemer))
    omuz = (x + int(0.5 * s) * yon, ust + int(1 * s))
    if masa_ust is not None:
        el = (x + int(4.6 * s) * yon + int(0.7 * s * SIN(f, 2)) * yon, masa_ust - _u(0.6, s) - int(0.3 * s * abs(SIN(f, 4))))
    else:
        el = (x + int(3 * s) * yon, kalca - _u(0.8, s))
    d.line([*omuz, *el], fill=koyu, width=_u(1, s))
    piksel(img, el[0], el[1], hex2(ten))
    if masa_ust is not None:                                                             # tüy kalem: elden yukarı-geriye
        uc = (el[0] - int(1.4 * s) * yon, el[1] - int(3.4 * s))
        d.line([*el, *uc], fill=hex2("#e8e4d8"), width=_u(0.4, s))
        d.polygon([(uc[0], uc[1]), (uc[0] + int(0.9 * s) * yon, uc[1] + int(1.4 * s)), (uc[0] - int(0.3 * s) * yon,
                   uc[1] + int(2.2 * s))], fill=hex2("#f4f0e8"))
    bas_y = ust - int(2.6 * s)
    r = max(2, int(1.7 * s))
    d.ellipse([x - r, bas_y - r, x + r, bas_y + r], fill=hex2(ten))
    if s >= 3:
        _r(d, x + int(0.6 * s) * yon, bas_y - int(0.3 * s), x + int(0.6 * s) * yon + _u(0.3, s), bas_y, fill=hex2(KOYU))
    else:
        piksel(img, x + int(1 * s) * yon, bas_y, hex2(KOYU))
    if sakal:
        d.polygon([(x - r + _u(0.5, s), bas_y + _u(0.4, s)), (x + r, bas_y + _u(0.4, s)),
                   (x + int(0.6 * s) * yon, bas_y + r + _u(1.6, s))], fill=hex2(sakal))
    if bas:
        _baslik(d, img, x, bas_y, r, s, yon, bas, bas_renk)
    elif sac:
        _sac(d, x, bas_y, r, s, yon, sac, uzun=False)


def _sac(d, x, by, r, s, yon, sac, uzun=False):
    """Açık başta saç (orhun_yazitlari.avrupali kalıbı); uzun=True: omza inen saç (kadın)."""
    d.chord([x - r - 1, by - r - 1, x + r + 1, by + r // 3], 180, 360, fill=hex2(sac))
    ax = x - r * yon
    alt = by + (r + int(2.2 * s) if uzun else r // 3)
    _r(d, ax, by - r // 2, ax + (r // 2 if uzun else r // 3) * yon, alt, fill=hex2(sac))


def modern_kisi(img, x, zemin, s=1.0, govde="#3a4a5a", sac="#4a3a2a", yon=1, adim=None, silah=None, kol=0.0,
                kadin=False, yaka="#e8e4dc"):
    """Yeni figür: bugünün insanı. timur_figur.kisi gövdesi (kemersiz, kısa ceket), açık başta saç ve beyaz yaka.
    Ayakları kisi gibi zemine basar."""
    kisi(img, x, zemin, s, govde=govde, bas=None, sakal=None, yon=yon, adim=adim, silah=silah, kol=kol, kemer=None,
         kadin=kadin, uzun=kadin)
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    ust = y - int(11 * s)
    _r(d, x - int(0.9 * s), ust, x + int(0.9 * s), ust + _u(0.5, s), fill=hex2(yaka))
    by = y - int(13.6 * s)
    _sac(d, x, by, max(2, int(1.7 * s)), s, yon, sac, uzun=kadin)


def yazi_masasi(img, x, zemin, s=1.0, esya=("kagit", "hokka"), f=0.0, renk="#6a4426", yon=1, tohum=1):
    """Yeni figür: ahşap yazı masası (yan görünüş). Dört ayak zemine basar; üstünde esya: kagit, hokka, mum, kitap
    (kapalı yığın), basili (açık basılı kitap, kitap sehpasında), belge (arşiv belgesi). Masa üstünün y'sini döndürür."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 12 * s)
    temas_golgesi(img, x, y, 13 * s)
    w2 = int(6 * s)
    ust = y - int(6.6 * s)
    k = hex2(_ac(renk, -0.35))
    for ax in (-w2 + int(1.4 * s), w2 - int(2.2 * s)):                       # arka ayaklar
        _r(d, x + ax, ust, x + ax + _u(0.6, s), y - 1 - _u(0.3, s), fill=hex2(_ac(renk, -0.5)))
    for ax in (-w2 + int(0.4 * s), w2 - int(1.2 * s)):                       # ön ayaklar
        _r(d, x + ax, ust, x + ax + _u(0.8, s), y - 1, fill=k)
    _r(d, x - w2 + int(0.4 * s), ust + _u(0.8, s), x + w2 - int(0.4 * s), ust + int(1.8 * s), fill=hex2(_ac(renk, -0.15)))
    _r(d, x - w2, ust, x + w2, ust + _u(0.8, s), fill=hex2(renk))
    d.line([x - w2, ust, x + w2, ust], fill=hex2(_ac(renk, 0.3)))
    yuz = ust - 1
    for e in esya:
        if e == "kagit":                                                     # yazılan kâğıt (yazarın önünde)
            kx = x - int(2.5 * s) * yon
            _r(d, kx - int(2.2 * s), yuz - _u(0.4, s), kx + int(2.2 * s), yuz, fill=hex2("#f4ecd8"))
            for j in range(3):
                piksel(img, kx - int(1.5 * s) + j * _u(1.2, s), yuz - _u(0.4, s), hex2("#3a2a1a"))
        elif e == "hokka":
            hx = x + int(0.8 * s) * yon
            _r(d, hx - _u(0.8, s), yuz - int(1.4 * s), hx + _u(0.8, s), yuz, fill=hex2("#2a2420"), outline=hex2("#0e0a08"))
            d.line([hx, yuz - int(1.4 * s), hx + int(0.8 * s) * yon, yuz - int(4 * s)], fill=hex2("#e8e4d8"))
        elif e == "mum":
            mx = x + int(4.6 * s) * yon
            _masa_mumu(img, mx, yuz, f, s * 0.9)
        elif e == "kitap":
            bx = x + int(3 * s) * yon
            for j, rk in enumerate(("#8a2a2a", "#2a4a7a", "#6a5a2a")):
                yy = yuz - int(j * 1.1 * s)
                _r(d, bx - int(2 * s) + j, yy - int(1.1 * s) + 1, bx + int(2 * s) + j, yy, fill=hex2(rk), outline=hex2("#2a1a10"))
        elif e == "basili":                                                  # kitap sehpasında açık Gutenberg
            bx = x + int(2.2 * s) * yon
            d.polygon([(bx - int(1 * s), yuz), (bx + int(1 * s), yuz), (bx, yuz - int(1.6 * s))], fill=hex2("#4a2e1a"))
            by = yuz - int(1.4 * s)
            sol = [(bx - int(4 * s), by - int(4.2 * s)), (bx, by - int(3.4 * s)), (bx, by), (bx - int(4 * s), by - int(0.8 * s))]
            sag = [(bx, by - int(3.4 * s)), (bx + int(4 * s), by - int(4.2 * s)), (bx + int(4 * s), by - int(0.8 * s)), (bx, by)]
            d.polygon([(p[0], p[1] + _u(0.5, s)) for p in sol + sag[1:3]], fill=hex2("#5a2a1e"))
            d.polygon(sol, fill=hex2("#f0e4c4"))
            d.polygon(sag, fill=hex2("#ece0c0"))
            for kx0 in (bx - int(3.6 * s), bx + int(0.5 * s)):                # iki sütun siyah harf dokusu, kırmızı baş harf
                _satirlar(img, kx0, by - int(3.2 * s), kx0 + int(3 * s), by - int(1 * s), aralik=2, tohum=kx0)
                _r(d, kx0, by - int(3.4 * s), kx0 + _u(0.6, s), by - int(2.8 * s), fill=hex2("#a8281e"))
        elif e == "belge":
            bx = x
            _r(d, bx - int(3 * s), yuz - _u(0.4, s), bx + int(1 * s), yuz, fill=hex2("#e8dcc0"))
            _r(d, bx + int(1.6 * s), yuz - int(1.6 * s), bx + int(4.4 * s), yuz, fill=hex2("#8a8478"), outline=hex2("#5a564e"))
    return ust


def _masa_mumu(t, x, y, f, s=1.0):
    """Masa üstünde pirinç şamdanda tek mum (orhun_yazitlari.masa_mumu kalıbı; y = masa üstü). Alev titrer."""
    d = ImageDraw.Draw(t)
    _r(d, x - int(1.2 * s), y - _u(0.5, s), x + int(1.2 * s), y - 1, fill=hex2("#c8a040"), outline=hex2("#5a3a10"))
    _r(d, x - _u(0.3, s), y - int(1.4 * s), x + _u(0.3, s), y - int(0.5 * s), fill=hex2("#a88030"))
    _r(d, x - _u(0.45, s), y - int(4 * s), x + _u(0.45, s), y - int(1.4 * s), fill=hex2("#f4ecd8"))
    alev = 1.3 + 0.35 * SIN(f, 3) + 0.15 * SIN(f, 7)
    ay = y - int(4 * s)
    d.polygon([(x - _u(0.5, s), ay), (x, ay - int(alev * 1.6 * s)), (x + _u(0.5, s), ay)], fill=hex2("#f8c040"))
    piksel(t, x, ay - 1, hex2("#fff4c0"))
    for r in range(int(2 * s), int(9 * s), 2):
        for a in range(0, 360, 10):
            px_, py_ = x + math.cos(math.radians(a)) * r * 1.2, ay + math.sin(math.radians(a)) * r
            if (int(px_) + int(py_)) % 2 == 0 and py_ < y - 1 and random.Random(int(px_) * 31 + int(py_)).random() < 0.5 * (1 - r / (9 * s)):
                piksel(t, px_, py_, hex2("#ffd479", 55))


def _rahle_ayak(d, img, x, y, s):
    """Rahlenin çapraz ayakları (zemine basar) ve kitabın oturduğu yükseklik."""
    ah = hex2("#5a3a1e")
    d.line([x - int(8 * s), y - 1, x + int(6 * s), y - int(9 * s)], fill=ah, width=_u(1.2, s))
    d.line([x + int(8 * s), y - 1, x - int(6 * s), y - int(9 * s)], fill=ah, width=_u(1.2, s))
    d.line([x - int(8 * s), y - 1, x - int(6 * s), y - 1], fill=hex2("#3a2410"), width=_u(0.8, s))
    d.line([x + int(6 * s), y - 1, x + int(8 * s), y - 1], fill=hex2("#3a2410"), width=_u(0.8, s))
    return y - int(9 * s)


def bos_rahle(img, x, zemin, s=1.0):
    """Yeni figür: üstü boş rahle (motif: "fermanı gören yok"). Çapraz ayaklar zemine basar; iki kanat açık ve boş."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 18 * s)
    temas_golgesi(img, x, y, 20 * s)
    by = _rahle_ayak(d, img, x, y, s)
    ah, ahk = hex2("#7a5232"), hex2("#4a2e1a")
    d.polygon([(x - int(9 * s), by - int(6 * s)), (x, by - int(1 * s)), (x, by), (x - int(9 * s), by - int(5 * s))], fill=ah, outline=ahk)
    d.polygon([(x, by - int(1 * s)), (x + int(9 * s), by - int(6 * s)), (x + int(9 * s), by - int(5 * s)), (x, by)], fill=ah, outline=ahk)


def acik_kitap(img, x, zemin, s=1.0, sayfa="oklid", f=0.0):
    """Yeni figür: rahlede açık kitap (takiyuddin.minyatur_kitap kalıbı). Rahlenin çapraz ayakları zemine basar.
    sayfa: oklid (solda üçgen ve daire, sağda tuğralı izin fermanı), vankulu (solda tuğralı ferman, sağda fetva),
    resim (solda tahta baskı gemi resmi, sağda yazı), ibrani (sağdan sola satırlar, son satırda kolofon), gutenberg."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 20 * s)
    temas_golgesi(img, x, y, 22 * s)
    by = _rahle_ayak(d, img, x, y, s)
    sol = [(x - int(15 * s), by - int(12 * s)), (x, by - int(10 * s)), (x, by), (x - int(15 * s), by - int(2 * s))]
    sag = [(x, by - int(10 * s)), (x + int(15 * s), by - int(12 * s)), (x + int(15 * s), by - int(2 * s)), (x, by)]
    d.polygon([(p[0], p[1] + _u(1, s)) for p in sol + sag[1:3]], fill=hex2("#5a2a1e" if sayfa != "vankulu" else "#6a1e1e"))
    d.polygon(sol, fill=hex2("#f0e4c4"))
    d.polygon(sag, fill=hex2("#ece0c0"))
    d.line([x, by - int(10 * s), x, by], fill=hex2("#b8a888"))
    # sayfa kenarı kıpırtısı (mum ışığında): sağ sayfanın köşesi
    if SIN(f) > 0.6:
        piksel(img, x + int(15 * s), by - int(12 * s) - 1, hex2("#f8f0d8"))
    L0, L1 = x - int(13.5 * s), x - int(1.5 * s)
    R0, R1 = x + int(1.5 * s), x + int(13.5 * s)
    ust, alt = by - int(10 * s), by - int(3 * s)
    if sayfa == "oklid":
        d.polygon([(L0 + int(1 * s), alt - int(1 * s)), (L1 - int(1 * s), alt - int(1 * s)), (L0 + int(4 * s), ust)],
                  outline=hex2("#2a2a2a"))                                                    # üçgen
        d.ellipse([L0 + int(5 * s), ust + int(1.5 * s), L0 + int(10 * s), ust + int(6.5 * s)], outline=hex2("#8a1e1e"))  # daire
        d.line([L0 + int(1 * s), ust + int(3 * s), L1 - int(1 * s), alt - int(2 * s)], fill=hex2("#2a2a2a"))
        _tugra(img, (R0 + R1) // 2, ust + int(2.4 * s), s * 0.9)                               # izin fermanı (453. sayfa)
        _satirlar(img, R0 + _u(0.6, s), ust + int(4 * s), R1 - _u(0.6, s), alt, aralik=max(2, _u(1, s)), tohum=453, rtl=True)
    elif sayfa == "vankulu":
        _tugra(img, (L0 + L1) // 2, ust + int(2.6 * s), s * 0.95)
        _satirlar(img, L0 + _u(0.6, s), ust + int(4.2 * s), L1 - _u(0.6, s), alt, aralik=max(2, _u(1, s)), tohum=1729, rtl=True)
        _r(d, R0 + int(3 * s), ust, R1 - int(3 * s), ust + int(1 * s), fill=hex2("#c8a040"))   # fetva başlığı (tezhip)
        _satirlar(img, R0 + _u(0.6, s), ust + int(2.4 * s), R1 - _u(0.6, s), alt, aralik=max(2, _u(1, s)), tohum=1727, rtl=True)
    elif sayfa == "resim":
        fx0, fy0, fx1, fy1 = L0, ust, L1, alt
        _r(d, fx0, fy0, fx1, fy1, outline=hex2("#2a2a2a"))
        sy = fy1 - int(2.4 * s)                                                                 # tahta baskı: dalga + gemi
        for k in range(fx0 + 1, fx1, max(2, _u(1, s))):
            piksel(img, k, sy + (k // 2) % 2, hex2("#2a2a2a"))
        gx = (fx0 + fx1) // 2
        d.polygon([(gx - int(4 * s), sy - int(1.4 * s)), (gx + int(4 * s), sy - int(1.4 * s)), (gx + int(3 * s), sy),
                   (gx - int(3 * s), sy)], fill=hex2("#2a2a2a"))
        d.line([gx, sy - int(1.4 * s), gx, fy0 + int(1 * s)], fill=hex2("#2a2a2a"))
        d.polygon([(gx + 1, fy0 + int(1.4 * s)), (gx + int(3 * s), fy0 + int(2.6 * s)), (gx + 1, sy - int(2 * s))], outline=hex2("#2a2a2a"))
        d.polygon([(gx - 1, fy0 + int(2 * s)), (gx - int(2.6 * s), sy - int(2 * s)), (gx - 1, sy - int(2 * s))], outline=hex2("#2a2a2a"))
        _satirlar(img, R0 + _u(0.6, s), ust, R1 - _u(0.6, s), alt, aralik=max(2, _u(1, s)), tohum=38, rtl=True)
    elif sayfa == "ibrani":
        for a0, a1, t in ((L0, L1, 1493), (R0, R1, 1494)):
            _satirlar(img, a0 + _u(0.6, s), ust, a1 - _u(0.6, s), alt, aralik=max(2, _u(1, s)), tohum=t, rtl=True)
        _r(d, L0 + int(3 * s), alt - int(1.2 * s), L1 - int(3 * s), alt, fill=hex2("#a8281e"))  # kolofon (tarihli son satır)
    elif sayfa == "gutenberg":
        for a0, a1 in ((L0, L1), (R0, R1)):
            m = (a0 + a1) // 2
            _satirlar(img, a0, ust, m - 1, alt, aralik=2, tohum=a0)
            _satirlar(img, m + 1, ust, a1, alt, aralik=2, tohum=a1)
            _r(d, a0, ust, a0 + _u(1, s), ust + _u(1, s), fill=hex2("#a8281e"))


def kurutma_ipi(img, x0, x1, zemin, s=1.0, f=0.0, adet=5):
    """Yeni figür: basılmış sayfaların kuruduğu ip. İki direk zemine dikili (dipte tahta ayak), ip hafif sarkar; mandallı
    sayfalar ipten sarkar ve hafifçe sallanır (ipe bağlı, havada değil)."""
    d = ImageDraw.Draw(img)
    for x in (x0, x1):
        y = zemin_y(zemin, x, 4 * s)
        temas_golgesi(img, x, y, 5 * s)
        _r(d, x - int(2 * s), y - _u(0.8, s), x + int(2 * s), y - 1, fill=hex2(_ac(AGAC, -0.3)))
        _r(d, x - _u(0.4, s), y - int(13 * s), x + _u(0.4, s), y - 1, fill=hex2(AGAC))
    y0 = zemin_y(zemin, x0, 4 * s) - int(12.6 * s)
    y1 = zemin_y(zemin, x1, 4 * s) - int(12.6 * s)
    nokta = []
    for k in range(x1 - x0 + 1):
        u = k / (x1 - x0)
        nokta.append((x0 + k, y0 + (y1 - y0) * u + 4 * s * 0.25 * math.sin(math.pi * u) * 2))
    d.line(nokta, fill=hex2("#d8c8a8"))
    for j in range(adet):
        u = (j + 0.75) / (adet + 0.5)
        px = int(x0 + (x1 - x0) * u)
        py = int(nokta[px - x0][1])
        sal = int(0.5 * s * SIN(f + j * 0.21))
        w, h = int(2.6 * s), int(3.6 * s)
        d.polygon([(px - w // 2, py), (px + w // 2, py), (px + w // 2 + sal, py + h), (px - w // 2 + sal, py + h)], fill=hex2("#f0e6cc"))
        for k in range(1, 5):
            d.line([px - w // 2 + 1 + sal * k // 5, py + int(k * h / 5.5), px + w // 2 - 1 + sal * k // 5, py + int(k * h / 5.5)],
                   fill=hex2("#5a4a3a"))
        piksel(img, px, py, hex2("#6a4a2a"))
        piksel(img, px, py + 1, hex2("#6a4a2a"))


def raf(img, x, zemin, s=1.0, tur="kitap", tohum=1, toz=False):
    """Yeni figür: kitap rafı (s = kisi ölçeği; raf ≈ 15 s, insandan kısa). Yan tahtaları zemine basar. tur: kitap
    (renkli sırtlar), yigin (yatık yığınlar), arsiv (gri metal raf, etiketli kutular). toz: gri toz örtüsü, örümcek ağı."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 12 * s)
    temas_golgesi(img, x, y, 13 * s)
    w2 = int(6 * s)
    ust = y - int(15 * s)
    govde = "#8a8e94" if tur == "arsiv" else "#4a2e1a"
    _r(d, x - w2, ust, x + w2, y - 1, fill=hex2(_ac(govde, -0.45)))
    for k in (-1, 1):
        _r(d, x + k * w2 - _u(0.4, s), ust, x + k * w2 + _u(0.4, s), y - 1, fill=hex2(govde))
    _r(d, x - w2 - _u(0.4, s), ust - _u(0.8, s), x + w2 + _u(0.4, s), ust, fill=hex2(_ac(govde, 0.15)))
    rnd = random.Random(tohum)
    katlar = 4
    h = (y - 1 - ust) / katlar
    for k in range(katlar):
        sy = int(ust + (k + 1) * h)
        _r(d, x - w2, sy - _u(0.5, s), x + w2, sy, fill=hex2(govde))
        bx = x - w2 + _u(0.6, s)
        while bx < x + w2 - _u(1.2, s):
            if tur == "arsiv":
                bw = int(rnd.uniform(2.2, 3.2) * s)
                bh = int(h * 0.7)
                b1 = min(bx + bw, x + w2 - _u(0.6, s))
                _r(d, bx, sy - _u(0.5, s) - bh, b1, sy - _u(0.5, s) - 1, fill=hex2(rnd.choice(("#c8b898", "#b8a888", "#d0c4a8"))),
                   outline=hex2("#6a5e4a"))
                _r(d, bx + _u(0.5, s), sy - bh + int(h * 0.15), min(bx + int(1.6 * s), b1 - 1), sy - bh + int(h * 0.15) + _u(0.6, s),
                   fill=hex2("#f4f0e8"))
                bx = b1 + 1
            elif tur == "yigin":
                bh = int(rnd.uniform(0.9, 1.3) * s)
                b1 = min(bx + int(rnd.uniform(3, 4.4) * s), x + w2 - _u(0.6, s))
                yy = sy - _u(0.5, s)
                while yy - bh > sy - h + _u(1, s):
                    renk = rnd.choice(("#8a2a2a", "#2a4a7a", "#3a5a3a", "#a8803a", "#5a3a5a"))
                    _r(d, bx + rnd.randint(0, 1), yy - bh, b1 + rnd.randint(-1, 0), yy - 1, fill=hex2(renk), outline=hex2("#2a1a10"))
                    yy -= bh
                bx = b1 + _u(0.8, s)
            else:
                bw = max(1, int(rnd.uniform(0.7, 1.3) * s))
                bh = int(rnd.uniform(0.6, 0.85) * h)
                renk = rnd.choice(("#8a2a2a", "#2a4a7a", "#3a6a3a", "#a8803a", "#5a3a5a", "#7a5a3a"))
                _r(d, bx, sy - _u(0.5, s) - bh, min(bx + bw - 1, x + w2 - 1), sy - _u(0.5, s) - 1, fill=hex2(renk))
                piksel(img, bx, sy - _u(0.5, s) - bh, hex2(_ac(renk, 0.4)))
                bx += bw + (1 if rnd.random() < 0.3 else 0)
    if toz:
        px = img.load()
        for yy in range(ust, y - 1):
            for xx in range(x - w2, x + w2 + 1):
                if 0 <= xx < img.width and 0 <= yy < img.height and px[xx, yy][3] > 0 and _esik(xx, yy) < 0.3:
                    piksel(img, xx, yy, hex2("#b8b0a0", 90))
        for k in range(1, 5):                                                    # örümcek ağı: üst sol köşe
            d.line([x - w2, ust + int(k * 0.9 * s), x - w2 + int(k * 0.9 * s), ust], fill=hex2("#d0ccc4", 130))
        d.line([x - w2, ust, x - w2 + int(3.6 * s), ust + int(3.6 * s)], fill=hex2("#d0ccc4", 130))


def kitap_yigini(img, x, zemin, s=1.0, kat=8, tohum=1, toz=False):
    """Yeni figür: yerde üst üste yığılmış kitaplar (satılmamış nüshalar): en alttaki zemine basar, her kitap altındakine
    oturur (hafif kaymalarla). toz: üst yüzlerde gri toz."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    temas_golgesi(img, x, y, 7 * s)
    rnd = random.Random(tohum)
    yy = y
    for k in range(kat):
        bh = max(2, int(rnd.uniform(0.8, 1.2) * s))
        w = int(rnd.uniform(2.6, 3.2) * s)
        kx = x + rnd.randint(-_u(0.4, s), _u(0.4, s))
        renk = rnd.choice(("#7a3a2a", "#3a4a6a", "#5a5a3a", "#8a6a3a", "#4a3a4a", "#6a2a2a"))
        if toz:
            renk = _ac(renk, 0.25)
        _r(d, kx - w, yy - bh, kx + w, yy - 1, fill=hex2(renk), outline=hex2("#2a1a10"))
        d.line([kx - w + 1, yy - bh + 1, kx + w - 1, yy - bh + 1], fill=hex2("#e8dcc0" if not toz else "#c8c0b0"))
        yy -= bh
    return yy


def cilt(img, x, zemin, s=1.0, renk="#6a1e1e"):
    """Yeni figür: kapalı kalın cilt (Vankulu'nun ikinci cildi), yere yatık: alt yüzü zemine oturur; sırtta altın şerit."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 10 * s)
    temas_golgesi(img, x, y, 11 * s)
    _r(d, x - int(5 * s), y - int(3 * s), x + int(5 * s), y - 1, fill=hex2("#f0e4c4"))                     # sayfa kenarı
    for yy in range(y - int(3 * s) + 1, y - 1, 2):
        d.line([x - int(5 * s) + 1, yy, x + int(5 * s) - 1, yy], fill=hex2("#d8c8a4"))
    _r(d, x - int(5.4 * s), y - int(3.8 * s), x + int(5.4 * s), y - int(3 * s), fill=hex2(renk))           # kapak
    _r(d, x - int(5.4 * s), y - int(3.8 * s), x - int(4.4 * s), y - 1, fill=hex2(_ac(renk, -0.2)))         # sırt
    d.line([x - int(5.2 * s), y - int(2.4 * s), x - int(4.6 * s), y - int(2.4 * s)], fill=hex2("#e0b040"))
    d.ellipse([x - int(1.2 * s), y - int(3.7 * s), x + int(1.2 * s), y - int(3.1 * s)], fill=hex2("#c8a040"))  # şemse


def ahsap_ev(img, x, zemin, s=1.0, duvar="#b89a74", cati="#8a3e2a", isik=False, kar=False):
    """Yeni figür: iki katlı İstanbul ahşap evi: düz zemine oturan taş temel, ahşap gövde, üst katta cumba (çıkma),
    kırma kiremit dam, kapı ve pencereler (isik: gece yanan pencereler, kar: damda kar). Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    g = int(12 * s)
    y = duz_zemin(zemin, x - g, x + g, "ahsap_ev", tolerans=max(3, int(s)))
    temas_golgesi(img, x, y, 2 * g + 4, alfa=90)
    _r(d, x - g, y - int(3 * s), x + g, y - 1, fill=hex2("#8a8478"))                                      # taş temel
    _r(d, x - g, y - int(13 * s), x + g, y - int(3 * s), fill=hex2(duvar))
    for xx in range(x - g + _u(2, s), x + g, _u(2, s)):                                                   # tahta kaplama
        d.line([xx, y - int(13 * s), xx, y - int(3 * s)], fill=hex2(_ac(duvar, -0.12)))
    _r(d, x - g - int(2 * s), y - int(24 * s), x + g + int(2 * s), y - int(13 * s), fill=hex2(_ac(duvar, 0.05)))  # cumbalı üst kat
    for xx in range(x - g - int(2 * s) + _u(2, s), x + g + int(2 * s), _u(2, s)):
        d.line([xx, y - int(24 * s), xx, y - int(13 * s)], fill=hex2(_ac(duvar, -0.1)))
    for k in range(-1, 2):                                                                                # cumba payandaları
        d.line([x + k * int(10 * s), y - int(13 * s), x + k * int(10 * s) + int(1.6 * s), y - int(10.4 * s)], fill=hex2(_ac(duvar, -0.35)),
               width=_u(0.5, s))
    pen = hex2("#f8c860") if isik else hex2("#3a2a22")
    for px_ in (-9, -3, 3, 9):
        _r(d, x + int(px_ * s) - _u(1.2, s), y - int(21.5 * s), x + int(px_ * s) + _u(1.2, s), y - int(16 * s), fill=pen,
           outline=hex2(_ac(duvar, -0.4)))
        d.line([x + int(px_ * s), y - int(21.5 * s), x + int(px_ * s), y - int(16 * s)], fill=hex2(_ac(duvar, -0.4)))
    for px_ in (-8, 7):
        _r(d, x + int(px_ * s) - _u(1.2, s), y - int(11 * s), x + int(px_ * s) + _u(1.2, s), y - int(6.5 * s), fill=pen,
           outline=hex2(_ac(duvar, -0.4)))
    _r(d, x - int(2.2 * s), y - int(10 * s), x + int(2.2 * s), y - 1, fill=hex2("#4a2a1a"), outline=hex2("#2a1a10"))  # kapı
    d.line([x, y - int(10 * s), x, y - 1], fill=hex2("#2a1a10"))
    piksel(img, x + _u(1, s), y - int(5 * s), hex2("#c8a040"))
    d.polygon([(x - g - int(4 * s), y - int(24 * s)), (x - int(5 * s), y - int(30 * s)), (x + int(5 * s), y - int(30 * s)),
               (x + g + int(4 * s), y - int(24 * s))], fill=hex2(cati))
    d.line([x - g - int(4 * s), y - int(24 * s), x + g + int(4 * s), y - int(24 * s)], fill=hex2(_ac(cati, -0.3)))
    for k in range(1, 3):
        yy = y - int((24 + k * 2) * s)
        d.line([x - g - int((4 - k * 1.8) * s), yy, x + g + int((4 - k * 1.8) * s), yy], fill=hex2(_ac(cati, -0.15)))
    if kar:
        d.polygon([(x - g - int(4 * s), y - int(24 * s)), (x - int(5 * s), y - int(30 * s) - _u(1, s)), (x + int(5 * s), y - int(30 * s) - _u(1, s)),
                   (x + g + int(4 * s), y - int(24 * s)), (x + g + int(2 * s), y - int(25 * s)), (x - g - int(2 * s), y - int(25 * s))],
                  fill=hex2("#e8eef8"))
        _r(d, x - g - int(2 * s), y - int(13.6 * s), x + g + int(2 * s), y - int(13 * s), fill=hex2("#e8eef8"))
    _r(d, x + int(6 * s), y - int(33 * s), x + int(8 * s), y - int(27 * s), fill=hex2("#7a6a5a"))         # baca
    return (x + int(7 * s), y - int(33 * s))


def saray_kapisi(img, x, zemin, s=1.0, tas="#d8d0c0", kursun="#7a8490"):
    """Yeni figür: Bâbüsselâm'dan esinli saray kapısı: iki sekizgen kule (kurşun külahlı), aralarında mazgalsız duvar ve
    kemerli büyük kapı, iki yanda sur. Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    g = int(26 * s)
    y = duz_zemin(zemin, x - g, x + g, "saray_kapisi", tolerans=max(3, int(s)))
    temas_golgesi(img, x, y, 2 * g + 4, alfa=90)
    t, tk = hex2(tas), hex2(_ac(tas, -0.2))
    _r(d, x - g, y - int(12 * s), x + g, y - 1, fill=t)                                                    # sur
    for yy in range(y - int(12 * s) + _u(2, s), y - 1, _u(2, s)):
        d.line([x - g, yy, x + g, yy], fill=tk)
    _r(d, x - int(9 * s), y - int(16 * s), x + int(9 * s), y - 1, fill=t, outline=tk)                     # kapı gövdesi
    d.polygon([(x - int(11 * s), y - int(16 * s)), (x + int(11 * s), y - int(16 * s)), (x + int(9 * s), y - int(18 * s)),
               (x - int(9 * s), y - int(18 * s))], fill=hex2(kursun))                                         # saçak
    _r(d, x - int(3.4 * s), y - int(9 * s), x + int(3.4 * s), y - 1, fill=hex2("#3a2a20"))                   # kemerli kapı
    d.chord([x - int(3.4 * s), y - int(12.4 * s), x + int(3.4 * s), y - int(5.6 * s)], 180, 360, fill=hex2("#3a2a20"))
    d.arc([x - int(4.2 * s), y - int(13.2 * s), x + int(4.2 * s), y - int(4.8 * s)], 180, 360, fill=hex2("#c8a040"))
    _tugra(img, x, y - int(13.6 * s), s * 0.45, renk="#c8a040", altin="#e8d080")                           # kapı üstü tuğra
    for k in (-1, 1):                                                                                     # sekizgen kuleler
        cx = x + k * int(13 * s)
        _r(d, cx - int(4 * s), y - int(22 * s), cx + int(4 * s), y - 1, fill=t)
        d.line([cx - int(1.4 * s), y - int(22 * s), cx - int(1.4 * s), y - 1], fill=tk)
        d.line([cx + int(1.4 * s), y - int(22 * s), cx + int(1.4 * s), y - 1], fill=tk)
        _r(d, cx - int(0.6 * s), y - int(19 * s), cx + int(0.6 * s), y - int(16 * s), fill=hex2("#2a3040"))
        d.polygon([(cx - int(4.6 * s), y - int(22 * s)), (cx, y - int(30 * s)), (cx + int(4.6 * s), y - int(22 * s))], fill=hex2(kursun))
        d.line([cx, y - int(30 * s), cx, y - int(31.5 * s)], fill=hex2("#e0b040"))


def kagithane(img, x, zemin, s=1.0, f=0.0):
    """Yeni figür: Yalova kâğıthanesi. Taş değirmen evi düz zemine kurulur; sol duvarındaki su çarkı yatay mile bağlı,
    alt kısmı zemine oturan tahta oluğun (dikmeleri yere basar) suyunda döner (f ile; dikişsiz). Oluktan su dökülür."""
    d = ImageDraw.Draw(img)
    g = int(14 * s)
    y = duz_zemin(zemin, x - g, x + g, "kagithane", tolerans=max(3, int(s)))
    temas_golgesi(img, x, y, 2 * g + 4, alfa=90)
    tas = "#b8ac94"
    _r(d, x - g, y - int(20 * s), x + g, y - 1, fill=hex2(tas))
    rnd = random.Random(1745)
    for k, yy in enumerate(range(y - int(20 * s) + _u(2.4, s), y - 1, _u(2.4, s))):
        d.line([x - g, yy, x + g, yy], fill=hex2(_ac(tas, -0.2)))
        for xx in range(x - g + (k % 2) * _u(2.5, s), x + g, _u(5, s)):
            d.line([xx, yy - _u(2.4, s), xx, yy], fill=hex2(_ac(tas, -0.2)))
    _r(d, x + int(3 * s), y - int(9 * s), x + int(8 * s), y - 1, fill=hex2("#4a2e1a"), outline=hex2("#2a1a10"))   # kapı
    _r(d, x - int(6 * s), y - int(16 * s), x - int(2 * s), y - int(12 * s), fill=hex2("#2a2420"))
    d.polygon([(x - g - int(2 * s), y - int(20 * s)), (x, y - int(27 * s)), (x + g + int(2 * s), y - int(20 * s))], fill=hex2("#8a4a32"))
    d.line([x - g - int(2 * s), y - int(20 * s), x + g + int(2 * s), y - int(20 * s)], fill=hex2("#5a2a1a"))
    # oluk: tahta kanal, dikmeleri zemine basar; çarkın altı oluğun içinde
    cx, R = x - g - int(6 * s), int(11 * s)
    oy = y - int(3.4 * s)
    o0, o1 = cx - int(14 * s), cx + int(9 * s)
    for ox in (o0 + _u(1, s), cx - int(6 * s), o1 - _u(1, s)):
        _r(d, ox - _u(0.5, s), oy, ox + _u(0.5, s), y - 1, fill=hex2(_ac(AGAC, -0.3)))
    cy = oy + int(1.6 * s) - R
    # çark: çember, kaşıklar, göbek ve mil (mil duvara girer)
    a0 = f * 2 * math.pi
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=hex2("#5a3a1e"), width=_u(1.0, s))
    for k in range(8):
        a = a0 + k * math.pi / 4
        d.line([cx, cy, cx + math.cos(a) * (R - 1), cy + math.sin(a) * (R - 1)], fill=hex2("#6a4a2a"), width=_u(0.6, s))
        kx, ky = cx + math.cos(a) * R, cy + math.sin(a) * R
        _r(d, kx - _u(1, s), ky - _u(1, s), kx + _u(1, s), ky + _u(1, s), fill=hex2("#7a5232"))
    d.ellipse([cx - _u(1.4, s), cy - _u(1.4, s), cx + _u(1.4, s), cy + _u(1.4, s)], fill=hex2("#3a2a1a"))
    _r(d, cx, cy - _u(0.5, s), x - g, cy + _u(0.5, s), fill=hex2("#3a2a1a"))                                # mil
    # oluğun önü (çarkın altını örter) ve içindeki su
    _r(d, o0, oy - int(2.2 * s), o1, oy, fill=hex2("#4a7aa8"))
    for xx in range(o0, o1, 3):
        piksel(img, xx + int(4 * f * 3) % 3, oy - int(2.2 * s) + (xx // 3) % 2, hex2("#c8e0f0"))
    _r(d, o0, oy - int(1.2 * s), o1, oy, fill=hex2(AGAC))
    d.line([o0, oy - int(1.2 * s), o1, oy - int(1.2 * s)], fill=hex2(_ac(AGAC, 0.25)))
    # oluğun ucundan yere dökülen su ve küçük gölcük
    for k in range(int(3 * s)):
        piksel(img, o0 - 1 - (k % 2), oy - int(1.2 * s) + k + int(f * 6) % 2, hex2("#a8c8e0"))
    _r(d, o0 - int(3 * s), y - _u(0.8, s), o0 + _u(1, s), y - 1, fill=hex2("#4a7aa8"))


def sunak(img, x, zemin, s=1.0, f=0.0):
    """Yeni figür: kilise sunağı: örtülü masanın ayakları zemine basar; üstünde ayaklı haç (ucu genişleyen Ermeni haçı)
    ve iki mum (alev titrer)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 10 * s)
    temas_golgesi(img, x, y, 11 * s)
    ust = y - int(6 * s)
    for ax in (-4, 4):
        _r(d, x + int(ax * s) - _u(0.5, s), ust, x + int(ax * s) + _u(0.5, s), y - 1, fill=hex2("#4a2e1a"))
    _r(d, x - int(5 * s), ust - _u(0.8, s), x + int(5 * s), ust + int(2.6 * s), fill=hex2("#8a1e22"))
    d.line([x - int(5 * s), ust + int(2.6 * s), x + int(5 * s), ust + int(2.6 * s)], fill=hex2("#e0b040"))
    hy = ust - _u(0.8, s)
    _r(d, x - _u(0.4, s), hy - int(6 * s), x + _u(0.4, s), hy, fill=hex2("#c8a040"))
    _r(d, x - int(1.8 * s), hy - int(4.8 * s), x + int(1.8 * s), hy - int(4.2 * s), fill=hex2("#c8a040"))
    for px_, py_ in ((x, hy - int(6.4 * s)), (x - int(2 * s), hy - int(4.5 * s)), (x + int(2 * s), hy - int(4.5 * s))):
        _r(d, px_ - _u(0.5, s), py_ - _u(0.3, s), px_ + _u(0.5, s), py_ + _u(0.3, s), fill=hex2("#e0b040"))
    _r(d, x - int(1 * s), hy - _u(0.5, s), x + int(1 * s), hy, fill=hex2("#a88030"))
    for k in (-1, 1):
        _masa_mumu(img, x + k * int(3.6 * s), hy + 1, (f + 0.3 * k) % 1, s * 0.5)


def sahaf_tezgahi(img, x, zemin, s=1.0, tohum=1):
    """Yeni figür: çarşıda sahaf/kopyacı tezgâhı: tahta tezgâhın ayakları ve sundurmanın iki direği zemine basar; tezgâhta
    yatık el yazması kitaplar. Dönen değer: tezgâh üstü y."""
    d = ImageDraw.Draw(img)
    g = int(9 * s)
    y = zemin_y(zemin, x, g)
    temas_golgesi(img, x, y, 2 * g + 2)
    for k in (-1, 1):                                                                    # sundurma direkleri
        _r(d, x + k * g - _u(0.4, s), y - int(17 * s), x + k * g + _u(0.4, s), y - 1, fill=hex2(AGAC))
    d.polygon([(x - g - int(2 * s), y - int(16 * s)), (x + g + int(2 * s), y - int(16 * s)), (x + g, y - int(18 * s)),
               (x - g, y - int(18 * s))], fill=hex2("#8a3a2a"))
    for k in range(-g - int(2 * s), g + int(2 * s), _u(2, s)):
        d.line([x + k, y - int(16 * s), x + k, y - int(15 * s)], fill=hex2("#e0c8a0" if (k // _u(2, s)) % 2 else "#8a3a2a"))
    ust = y - int(7 * s)
    _r(d, x - g + _u(1, s), ust, x + g - _u(1, s), y - 1, fill=hex2(_ac(AGAC, -0.15)), outline=hex2(_ac(AGAC, -0.45)))
    _r(d, x - g, ust - _u(0.8, s), x + g, ust, fill=hex2(_ac(AGAC, 0.2)))
    rnd = random.Random(tohum)
    bx = x - g + _u(1, s)
    while bx < x + g - int(3 * s):
        kat = rnd.randint(1, 3)
        yy = ust - _u(0.8, s)
        w = int(rnd.uniform(2.4, 3.2) * s)
        for k in range(kat):
            renk = rnd.choice(("#7a3a2a", "#3a4a6a", "#5a5a3a", "#8a6a3a", "#6a2a2a"))
            _r(d, bx, yy - _u(0.9, s), bx + w, yy - 1, fill=hex2(renk), outline=hex2("#2a1a10"))
            yy -= _u(0.9, s)
        bx += w + _u(0.8, s)
    return ust


def sarkit_lamba(t, x, ust, f, zincir=60):
    """Yeni figür: bugünün tavan lambası (arşiv okuma salonu): kablo tavandan iner, metal şapka, sarı ampul ve altına
    düşen ışık konisi (kandilin modern karşılığı; anakronizm olmasın diye arşiv sahnesinde kullanılır)."""
    d = ImageDraw.Draw(t)
    for k in range(0, zincir, 2):
        piksel(t, x, ust + k, hex2("#4a4a4e"))
    ky = ust + zincir
    d.polygon([(x - 3, ky), (x + 3, ky), (x + 9, ky + 7), (x - 9, ky + 7)], fill=hex2("#3a5a4a"), outline=hex2("#1a2a22"))
    d.ellipse([x - 3, ky + 5, x + 3, ky + 9], fill=hex2("#fff4c0"))
    for r in range(4, 40, 3):
        for a in range(30, 150, 6):
            px_, py_ = x + math.cos(math.radians(a)) * r * 1.2, ky + 8 + math.sin(math.radians(a)) * r
            if _esik(int(px_), int(py_)) < 0.3 * (1 - r / 40) + 0.03 * SIN(f):
                piksel(t, px_, py_, hex2("#fff0b0", 45))


def kitap_bohcasi(t, el, s, yon=1):
    """Alıcının elinde ip bağlı kitap destesi: elin hemen altında, ele bağlı (havada değil)."""
    d = ImageDraw.Draw(t)
    ex, ey = el
    for k, renk in enumerate(("#7a3a2a", "#3a4a6a", "#8a6a3a")):
        yy = ey + int((k + 0.2) * 1.0 * s)
        _r(d, ex - int(1.8 * s), yy, ex + int(1.8 * s), yy + _u(0.9, s), fill=hex2(renk), outline=hex2("#2a1a10"))
    d.line([ex, ey, ex, ey + int(3 * s)], fill=hex2("#d8c8a0"))


def _kalem(t, el, s, yon, f):
    """Oturan kâtibin elinde kamış kalem: elden öne-aşağı rahleye iner, f ile yazma hareketi."""
    d = ImageDraw.Draw(t)
    ex, ey = el
    dx = int(0.5 * s * SIN(f, 2))
    d.line([ex, ey, ex + int(1.6 * s) * yon + dx, ey + int(1.4 * s)], fill=hex2("#c8a878"), width=_u(0.35, s))
