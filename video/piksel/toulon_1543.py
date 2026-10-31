"""Küçük Konstantinopolis: Barbaros'un donanması Toulon'da kışlıyor (1543-44). Piksel Tarih (@pikseltarihim),
sahneler 450-486 (487-489 kullanılmadı). Grafikerin tarifi: teslimler/gece/ara/toulon-1543/5-grafik.md; metin ve 52 kart
4-kalite-metin.md'den. Kalıp: video/piksel/cem_sultan.py (ölçek yardımcıları), celebi_mehmed_paris.py (yazı bandı
denetimi, liman), hezarfen.py (deniz katmanları), piri_reis.py (güverte, kuşbakışı masa).
Yön dili: sağ = batıya, Fransa'ya gelen donanma; sol = eve (doğuya) dönüş ve geride kalan.
Kullanım: python3 -I video/piksel/toulon_1543.py [sahne numaraları]

Yeni figürler (bu dosyada; ciz.py'ye eklenmedi, yalnızca piksel()/hex2()/ImageDraw ve mevcut figürlerle yazıldı):
  kadirga            16. yüzyıl kadırgası, doğru oranla: boy (mahmuz dahil) 100·s, alçak gövde (su üstü ~5·s),
                     tek sıra 24 kürek (vuruş döngüsü: kürek suda çekilir, havada geri gelir), kürekçi başları,
                     kıçta tenteli köşk ve fenerler, iki direk, latin sereni (yelken açık / sarılı / indirilmiş),
                     pruvada mahmuz ve top. Gövde su çizgisine oturur, altı suyun içinde kalır.
                     İnsan ölçeği: 42 m'lik gemide insan boyu = boy/25 (kürekçi başları bu ölçekte).
  provence_evleri    bitişik 2-3 katlı sıvalı evler, alçak eğimli kiremit çatı, panjurlu pencereler (kapalı/ışıklı).
  katedral           Romanesk kilise cephesi: üçgen alınlık, kemerli kapı, gül pencere, kare çan kulesi (piramit külah).
  kaya_tepe          düz tepeli kaya (Nice'in kale tepesi, Lipari akropolü): yan yüzler zemine oturur, tepesi düz.
  yangin             çatıya/zemine oturan titreyen alevler ve yükselen kıvılcımlar.
  basortulu, cocuk   başörtülü kadın (göz açık kalır), çocuk (saçlı, küçük ölçek). bohca: sırtta yük bohçası.
  rahip, avrupali    cüppeli rahip (beyaz yaka); 19. yüzyıl tarihçisi (açık baş, favori).
  vaftiz_kurnasi, kilise_kursusu   taş kurna, açık defterli kürsü (zemine oturur).
  altin_sandigi, ipek_toplari, cuval, fici, tezgah, kuyu, sokak_feneri, tas_duvar, kayik
  harita, minyatur, kronik            kuşbakışı masa sahneleri için (masaya düz yatan kâğıtlar).
"""
import json
import math
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw  # noqa: E402

from ciz import W, H, _ac, _esik, agac, arazi, duman, duz_zemin, figur, gradyan, hex2, piksel, sehir, sirt, temas_golgesi, temel, yeni, zemin_y  # noqa: E402
from sahneler import GW, duz, gokyuzu, kaydet, on, orta, sprite, uzak  # noqa: E402
from timur_figur import anadolu_kalesi, atli, kisi, otag  # noqa: E402
from timur import ic_mekan, kandil, mumluk  # noqa: E402
from kalender import taht  # noqa: E402
from cem_sultan import _kz, s_kisi  # noqa: E402

KARE = 24      # sprite kare sayısı (SKILL.md)
PAY = 135      # orta/ön plan yan payı (SKILL.md)
SIN = lambda f, k=1: math.sin(f * 2 * math.pi * k)  # noqa: E731
COS = lambda f, k=1: math.cos(f * 2 * math.pi * k)  # noqa: E731
PUB = Path(__file__).parents[1] / "public"
TSX = Path(__file__).parents[1] / "src" / "sahneler" / "Toulon1543.tsx"


def _u(v, s):
    return max(1, int(round(v * s)))


# ==========================================================================
# Kişiler (renk dili bütün videoda aynı kalır; iki farklı kişi aynı çizilmez)
# ==========================================================================
BARBAROS = dict(govde="#7a1e22", bas="sarik", bas_renk="#f4f0e6", sakal="#c0602e", pelerin="#1e3a5a")   # kızıl sakal
FRANCOIS = dict(govde="#2a3a8a", bas="tac", bas_renk="#e0b040", sakal="#4a2a16", pelerin="#8a1e22")     # taçlı kral
POLIN = dict(govde="#4a2a5a", bas="sapka", bas_renk="#1a1a22", sakal="#3a2a1a", kemer="#c8a040")        # Fransız elçi
LEVEND_A = dict(govde="#a8381e", bas="sarik", bas_renk="#ece6d8", sakal="#2a1a12", kemer="#e0b040")      # levend (kırmızı yelek)
LEVEND_B = dict(govde="#2a5a7a", bas="bork", bas_renk="#e8e0d0", sakal="#3a2a1a", kemer="#c8a040")       # levend (mavi, ak börk)
LEVEND_C = dict(govde="#5a6a2a", bas="sarik", bas_renk="#e0d8c4", sakal=None, kemer="#c8a040")          # genç levend
FR_ASKER = dict(govde="#3a4a7a", bas="migfer", bas_renk="#a8b0b8", sakal="#3a2a1a", kemer="#8a6a3a")
FR_ASKER2 = dict(govde="#7a2a2a", bas="migfer", bas_renk="#9aa2ac", sakal=None, kemer="#8a6a3a")
TOULONLU = dict(govde="#6a4a2a", bas="takke", bas_renk="#3a2a1a", sakal="#4a3a2a", kemer=None)          # Toulonlu erkek
TOULONLU2 = dict(govde="#3a5a4a", bas="takke", bas_renk="#2a2a2a", sakal="#6a5a4a", kemer=None)         # yaşlıca komşu
TANIK = dict(govde="#2a3a5a", bas="sapka", bas_renk="#2a2a30", sakal="#5a3a22", kemer="#c8a040")        # Fransız tanık
KONSUL = dict(govde="#8a1e2a", bas="sapka", bas_renk="#1a1a1a", sakal="#3a2a1a", kemer="#1a1a1a")      # konsül: kızıl cüppe
KONSUL2 = dict(govde="#8a1e2a", bas="sapka", bas_renk="#1a1a1a", sakal="#9a9088", kemer="#1a1a1a")
KATIP = dict(govde="#3a3a2a", bas="takke", bas_renk="#1a1a1a", sakal=None, kemer=None)                  # meclis kâtibi
MUNADI = dict(govde="#2a4a8a", bas="sapka", bas_renk="#c8a040", sakal="#3a2a1a", kemer="#e0b040")      # kralın münadisi
MEMUR = dict(govde="#2a3a8a", bas="sapka", bas_renk="#1a1a2a", sakal="#2a1a12", kemer="#e0b040", pelerin="#c8a040")
EKMEKCI = dict(govde="#c8b490", bas="takke", bas_renk="#e8e0d0", sakal="#5a3a22", kemer=None)          # önlüklü fırıncı
SAVOY = dict(govde="#8a1e22", bas="migfer", bas_renk="#b8c0c8", sakal="#3a2a1a")


# ==========================================================================
# TSX okuma: yakin, kamera, sprite ve kart ayarlarının tek kaynağı Toulon1543.tsx
# ==========================================================================
def _bloklar():
    metin = TSX.read_text()
    govde = metin[metin.index("bolumler:"):metin.index("kapanis:")]
    sonuc = []
    for b in re.split(r"\n    \{", govde)[1:]:
        sp = re.search(r"sprite: \{ w: (\d+), h: (\d+), fps: (\d+), x: (\[[^\]]*\]|\d+), taban: (\d+)", b)
        x = json.loads(sp.group(4))
        od = re.search(r"odakY: (\d+)", b)
        yy = re.search(r"yaziY: (\d+)", b)
        ust = int(yy.group(1)) if yy else 300
        altlar = []
        for m in re.finditer(r"satirlar: \[([^\]]*)\], sure: [\d.]+(?:, boy: (\d+))?", b):
            sat = [json.loads('"' + s_ + '"') for s_ in re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))]
            boy = int(m.group(2) or 92)
            sig = min(boy, math.floor(950 / (max(len(s_) for s_ in sat) * 0.46)))
            altlar.append((ust + len(sat) * sig * 1.12 + 8 + 24) / 2)          # ekran px → ızgara (24: giriş kayması)
        sonuc.append(dict(no=int(re.search(r"no: (\d+)", b).group(1)), kapak="KAPAK" in b.split("\n")[0],
                          yk=float(re.search(r"yakin: ([\d.]+)", b).group(1)),
                          kam=float(re.search(r"kamera: (-?[\d.]+)", b).group(1)),
                          w=int(sp.group(1)), h=int(sp.group(2)), taban=int(sp.group(5)),
                          xs=x if isinstance(x, list) else [x], odak=int(od.group(1)) if od else None,
                          ust=ust / 2, altlar=altlar))
    return sonuc


_BLOK = {}


def P(no):
    """Sahnenin (kapak olmayan) Bolum ayarları."""
    if not _BLOK:
        for b in _bloklar():
            _BLOK.setdefault(b["no"], []).append(b)
    return [b for b in _BLOK[no] if not b["kapak"]][0]


def _hepsi(no):
    P(no)
    return _BLOK[no]


def _pan(b):
    return abs(b["kam"]) * 0.65 / 2 + 1


def _pencere(b, sx, z):
    """Görünen dünya x aralığı (yakınlaşmanın odağı sprite'ın x'i; kamera kayması payı düşülür)."""
    return sx - sx / z + _pan(b), sx + (540 - sx) / z - _pan(b)


def _yerel(no, gx, sx=None):
    """Dünya (ızgara) x'i → sprite yerel x'i (sx verilmezse sahnenin ilk sx'i)."""
    b = P(no)
    sx = b["xs"][0] if sx is None else sx
    return int(gx - (sx - b["w"] / 2))


def _ust_sinir(no, pay=4):
    """Bütün kartlar ve %6 yakınlaşma için yazı bandının en alt dünya y'si (+pay): yapılar, direkler ve duman bunun
    altında kalır."""
    sinir = 0
    for b in _hepsi(no):
        o = b["odak"] or b["taban"] - 12
        for alt in b["altlar"]:
            sinir = max(sinir, int(o - (o - alt) / (b["yk"] * 1.06)) + pay)
    return sinir


_DENETIM = [False]   # denetim çizimi: zemin dokusu (su bandı) ve tavandan sarkan kandil zinciri sayılmaz


def _kadraj(no, kare, esik=0.995):
    """Kenar denetimi: her karede opak piksellerin en az `esik` oranı görünür aralıkta (bütün sx'ler, yakin ve
    sahne sonundaki 1.06·yakin, kamera kayması payı) olmalı; figür sprite'ın üst kenarına değmemeli (kesik baş)."""
    b = P(no)
    w, h = b["w"], b["h"]
    _DENETIM[0] = True
    try:
        for i in (0, 6, 12, 18):
            t = yeni(w, h)
            kare(t, duz(h - 1, w), i)
            alfa = t.getchannel("A")
            toplam = sum(alfa.histogram()[1:])
            if not toplam:
                raise RuntimeError(f"Sahne {no}: kare {i} boş")
            if sum(alfa.crop((0, 0, w, 2)).histogram()[1:]) > 4:
                raise RuntimeError(f"Sahne {no}: kare {i} sprite'ın üst kenarına değiyor (h={h} yetmiyor)")
            for sx in b["xs"]:
                for z in (b["yk"], b["yk"] * 1.06):
                    a, bb = _pencere(b, sx, z)
                    a, bb = int(math.ceil(a - (sx - w / 2))), int(bb - (sx - w / 2))
                    ici = sum(alfa.crop((max(a, 0), 0, min(bb, w), h)).histogram()[1:])
                    if ici / toplam < esik:
                        dis = alfa.crop((0, 0, max(a, 0), h)).getbbox(), alfa.crop((min(bb, w), 0, w, h)).getbbox()
                        raise RuntimeError(f"Sahne {no}, kare {i}, sx {sx}, yakin {z:.2f}: opak piksellerin "
                                           f"%{100 * ici / toplam:.1f}'i görünür aralıkta (yerel x {a}-{bb}); dışta: {dis}")
    finally:
        _DENETIM[0] = False


def _bant_denetimi(no):
    """Yazı bandı denetimi: kartların kapladığı ekran satırları dünya y'sine çevrilir; sprite'ta ve orta planda bu
    satırlarda görünür sütunlarda opak piksel (satır başına 2'den fazla) varsa betik durur."""
    spr = Image.open(PUB / f"sahne{no}-karakter.png").convert("RGBA").getchannel("A")
    ort = Image.open(PUB / f"sahne{no}-orta.png").convert("RGBA").getchannel("A")
    for b in _hepsi(no):
        w, h, taban = b["w"], b["h"], b["taban"]
        o = b["odak"] or taban - 12
        for alt in b["altlar"]:
            for z in (b["yk"], b["yk"] * 1.06):
                y0, y1 = int(o - (o - b["ust"]) / z), int(o - (o - alt) / z) + 2
                for sx in b["xs"]:
                    a, bb = _pencere(b, sx, z)
                    a, bb = a - _pan(b) * 2, bb + _pan(b) * 2
                    la, lb = int(a - (sx - w / 2)), int(bb - (sx - w / 2))
                    for i in range(0, KARE, 3):
                        for y in range(max(y0, taban - h), min(y1, taban) + 1):
                            ly = y - (taban - h)
                            n = sum(spr.crop((i * w + max(la, 0), ly, i * w + min(lb, w), ly + 1)).histogram()[1:])
                            if n > 2:
                                raise RuntimeError(f"Sahne {no}: sprite (kare {i}) yazı bandına giriyor: dünya y {y} "
                                                   f"(bant {y0}-{y1}, yakin {z:.2f}); figürü küçült ya da alçalt")
                    for y in range(y0, y1 + 1):
                        n = sum(ort.crop((PAY + int(a), y, PAY + int(bb), y + 1)).histogram()[1:])
                        if n > 2:
                            raise RuntimeError(f"Sahne {no}: orta plandaki yapı yazı bandına giriyor: y {y} (bant {y0}-{y1})")


def _gorunur(no, araliklar, pay=3):
    """Orta plandaki tekil nesnelerin dünya x aralıkları (x0, x1) bütün sx ve yakınlaşmalarda tamamen görünür olmalı
    (kenarda kesilen nesne olmaz)."""
    b = P(no)
    for sx in b["xs"]:
        for z in (b["yk"], b["yk"] * 1.06):
            a, bb = _pencere(b, sx, z)
            for x0, x1 in araliklar:
                if x0 < a + pay or x1 > bb - pay:
                    raise RuntimeError(f"Sahne {no}: orta plan nesnesi x {x0}-{x1} görünür aralık "
                                       f"[{int(a)}, {int(bb)}] dışına taşıyor (sx {sx}, yakin {z:.2f})")


def _spr(no, kare, esik=0.995):
    b = P(no)
    _kadraj(no, kare, esik)
    sprite(no, "karakter", b["w"], b["h"], KARE, kare)
    _bant_denetimi(no)


def K_(no, oran=0.32):
    """İnsan ölçeği: kisi boyu kadraj yüksekliğinin `oran`'ı (cem_sultan.s_kisi)."""
    return s_kisi(P(no)["yk"], oran)


# ==========================================================================
# Katman yardımcıları
# ==========================================================================
def _gok(no, renkler, bulutlar=(), bulut_renk=("#fff8ec", "#f4dcc8", "#d8a8a0"), yildiz=0, y0=384, y1=470):
    img = gokyuzu(no, renkler, None, bulutlar, bulut_renk, 0)
    if yildiz:                                                       # yakın çekimde görünen gök şeridine yıldız
        rnd = random.Random(no)
        for _ in range(yildiz):
            x, y = rnd.randrange(W), rnd.randrange(y0, y1)
            piksel(img, x, y, hex2(rnd.choice(("#fff8e0", "#d8e0f8", "#a8b4d8")), rnd.choice((140, 200, 255))))
        kaydet(img, f"sahne{no}-gokyuzu.png")
    return img


def _su_doldur(img, y0, renkler, tohum, x0=0, x1=None, parilti=260, parilti_renk=None):
    """y0'dan aşağısı titreşimli deniz bantları ve yatay dalga parıltıları (yatayda dikişsiz)."""
    x1 = img.width if x1 is None else x1
    for y in range(y0, img.height):
        v = (y - y0) / 14
        i = min(len(renkler) - 1, int(v))
        fr = v - int(v)
        for x in range(x0, x1):
            j = i + 1 if (i < len(renkler) - 1 and fr > 0.5 and _esik(x, y) < (fr - 0.5) * 2) else i
            img.putpixel((x, y), hex2(renkler[j]))
    rnd = random.Random(tohum)
    pr = parilti_renk or _ac(renkler[0], 0.35)
    for _ in range(parilti):
        x, y = rnd.randrange(x0, x1), rnd.randrange(y0 + 1, min(img.height, y0 + 160))
        for k in range(rnd.randint(2, 4 + (y - y0) // 14)):
            if x + k < x1:
                piksel(img, x + k, y, hex2(pr, 150))


def _sarili(img, ciz):
    """Uzak katman yatayda dikişsiz: çizim 2W genişlikte yapılır, taşan kısım soldan girer."""
    tmp = yeni(W * 2, H)
    ciz(tmp)
    img.alpha_composite(tmp.crop((0, 0, W, H)))
    img.alpha_composite(tmp.crop((W, 0, W * 2, H)))


def _uzak_kiyi(no, dag, tepe, kara, su_renk, su_y, dag_y=(440, 480), tepe_y=None, kasaba=None, gemiler=(),
               parilti_renk=None, kara_kalin=8):
    """Uzak plan: dikişsiz dağ (ör. Faron) ve tepeler, düz kıyı şeridi (kara_kalin px; yapılar bunun üstüne,
    su_y-2 satırına oturur), su_y'den aşağısı deniz. gemiler: [(x, s, yon, mod, renkler)] demirli ufak kadırgalar."""
    img = yeni()
    if dag:
        arazi(img, sirt(dag_y[1], (dag_y[1] - dag_y[0]) / 2, no, 3, 2.5, w=W, dongulu=True), list(dag))
    if tepe:
        arazi(img, sirt(tepe_y or dag_y[1] + 14, 5, no + 50, 4, 1, w=W, dongulu=True), list(tepe))
    arazi(img, [su_y - kara_kalin] * W, list(kara))
    if kasaba:
        _sarili(img, lambda t: kasaba(t, duz(su_y - 2, W * 2)))
    _su_doldur(img, su_y, su_renk, no + 3, parilti_renk=parilti_renk)
    for gx, gs, gyon, gmod, gk in gemiler:
        _sarili(img, lambda t, gx=gx, gs=gs, gyon=gyon, gmod=gmod, gk=gk: kadirga(
            t, gx, su_y + int(4 * gs) + 3, gs, gyon, 0.0, mod=gmod, kurek=False, kontur=gs >= 0.6, **gk))
    kaydet(img, f"sahne{no}-uzak.png")
    return img


def _orta_deniz(no, ust, renkler, rihtim=None, rihtim_renk=("#7a7468", "#6a6458", "#a8a294"), ekle=None, kiyi=None):
    """Orta plan (810 geniş): ust'ten aşağısı deniz. rihtim: taş rıhtımın üst kenarı (y); kiyi: (y0, renkler)
    deniz yerine düz kara şeridi (y0..ust arası) — yapılar bunun üstüne oturur. ekle(img) en son çizilir."""
    img = yeni(GW, H)
    if kiyi:
        ky, kr = kiyi
        arazi(img, [ky] * GW, list(kr))
    _su_doldur(img, ust, renkler, no + 7)
    if rihtim:
        d = ImageDraw.Draw(img)
        d.rectangle([0, rihtim, GW, H], fill=hex2(rihtim_renk[0]))
        for k, yy in enumerate(range(rihtim + 4, H, 12)):                       # şaşırtmalı taş sıraları
            d.line([0, yy, GW, yy], fill=hex2(rihtim_renk[1]))
            for xx in range((k % 2) * 13, GW, 26):
                d.line([xx, yy, xx, yy + 11], fill=hex2(rihtim_renk[1]))
        d.rectangle([0, rihtim, GW, rihtim + 2], fill=hex2(rihtim_renk[2]))
        d.line([0, rihtim + 3, GW, rihtim + 3], fill=hex2(_ac(rihtim_renk[0], -0.35)))
    if ekle:
        ekle(img)
    kaydet(img, f"sahne{no}-orta.png")
    return img


def _orta_duz(no, ust, renkler, tur="tas", ekle=None, kenar=None):
    """Orta plan (hezarfen._orta_duz kalıbı): dümdüz taş döşeme/toprak meydan; ekle(img, z) zemin üstüne yapı çizer."""
    img = yeni(GW, H)
    d = ImageDraw.Draw(img)
    renk_y = lambda y: renkler[min(len(renkler) - 1, int((y - ust) / 22))]  # noqa: E731
    for y in range(ust, H):
        d.line([0, y, GW, y], fill=hex2(renk_y(y)))
    rnd = random.Random(no)
    if tur == "tas":
        y, ara, k = ust + 3, 3.0, 0
        while y < H:
            d.line([0, y, GW, y], fill=hex2(_ac(renk_y(y), -0.16)))
            adim = int(ara * 4.2)
            ofs = (k % 2) * adim // 2
            for x in range(ofs, GW, max(3, adim)):
                xx = x + int((x - GW / 2) * (y - ust) / 900)
                d.line([xx, y - int(ara) + 1, xx, y - 1], fill=hex2(_ac(renk_y(y), -0.12)))
            ara = ara * 1.16 + 0.35
            y += int(ara)
            k += 1
    else:                                                               # toprak: titreşimli doku
        for _ in range(2600):
            x, y = rnd.randrange(GW), rnd.randrange(ust + 1, H)
            piksel(img, x, y, hex2(_ac(renk_y(y), rnd.choice((-0.12, 0.08)))))
    d.line([0, ust, GW, ust], fill=hex2(kenar or _ac(renkler[0], 0.22)))
    if ekle:
        ekle(img, duz(ust + 2))
    kaydet(img, f"sahne{no}-orta.png")
    return img


def _bos_on(no):
    kaydet(yeni(GW, H), f"sahne{no}-on.png")


def _su_bandi(t, y0, sprite_ust, renkler, deniz_ust, f=0.0, tohum=1):
    """Sprite'ın alt satırlarına orta plandaki denizle aynı renkte su bandı (denetimde çizilmez: zemin dokusu).
    Gemiler bu suya oturur; parıltılar f ile kayar (dikişsiz)."""
    if _DENETIM[0]:
        return
    d = ImageDraw.Draw(t)
    for y in range(y0, t.height):
        v = (sprite_ust + y - deniz_ust) / 14
        i = min(len(renkler) - 1, max(0, int(v)))
        fr = v - int(v)
        for x in range(t.width):
            j = i + 1 if (i < len(renkler) - 1 and fr > 0.5 and _esik(x, sprite_ust + y) < (fr - 0.5) * 2) else i
            t.putpixel((x, y), hex2(renkler[j]))
    rnd = random.Random(tohum)
    for _ in range(70):
        x0, y = rnd.randrange(t.width), rnd.randrange(y0 + 1, t.height)
        x = int(x0 + f * 24 * (1 if rnd.random() < 0.5 else -1)) % t.width
        for k in range(rnd.randint(2, 5)):
            piksel(t, (x + k) % t.width, y, hex2(_ac(renkler[0], 0.4), 150))
    d.line([0, y0, t.width, y0], fill=hex2(_ac(renkler[0], 0.18)))


def _masa_ustu(no, renk="#6a4426", isik="#1a0e06"):
    """Kuşbakışı sahnelerin orta planı (piri_reis._masa_ustu kalıbı): bütün kareyi kaplayan ahşap masa; ışık havuzu."""
    g = yeni()
    ImageDraw.Draw(g).rectangle([0, 0, W, H], fill=hex2(_ac(renk, -0.3)))
    kaydet(g, f"sahne{no}-gokyuzu.png")
    kaydet(yeni(), f"sahne{no}-uzak.png")
    img = yeni(GW, H)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, GW, H], fill=hex2(renk))
    rnd = random.Random(no)
    for y in range(0, H, 22):
        d.line([0, y, GW, y], fill=hex2(_ac(renk, -0.3)))
        for _ in range(18):
            x0, yy = rnd.randrange(GW), y + rnd.randrange(3, 20)
            for k in range(rnd.randrange(20, 90)):
                piksel(img, x0 + k, yy + int(math.sin(k / 9 + x0) * 1.2), hex2(_ac(renk, rnd.choice((-0.12, 0.1)))))
    cx, cy = PAY + 270, 560
    for y in range(300, H):
        for x in range(PAY - 40, PAY + 580):
            r = math.hypot(x - cx, (y - cy) / 1.25)
            if r > 130 and _esik(x, y) < min(0.8, (r - 130) / 200):
                piksel(img, x, y, hex2(isik, 80))
    kaydet(img, f"sahne{no}-orta.png")
    _bos_on(no)


def _guverte(no, ahsap="#7a5232", kupeste_y=572, guverte_y=600):
    """Orta plan (piri_reis._guverte kalıbı): kadırga güvertesi. Arkada küpeşte (alçak ahşap korkuluk, kürek
    delikleri), önde güverte tahtaları; figürler sprite'ta güverteye basar."""
    img = yeni(GW, H)
    d = ImageDraw.Draw(img)
    d.rectangle([0, kupeste_y, GW, guverte_y], fill=hex2(_ac(ahsap, -0.15)))
    for x in range(0, GW, 7):
        d.line([x, kupeste_y + 2, x, guverte_y], fill=hex2(_ac(ahsap, -0.28)))
    d.rectangle([0, kupeste_y - 3, GW, kupeste_y], fill=hex2(_ac(ahsap, 0.2)))
    d.line([0, kupeste_y - 3, GW, kupeste_y - 3], fill=hex2(_ac(ahsap, 0.4)))
    for x in range(20, GW, 46):
        d.ellipse([x - 3, kupeste_y + 10, x + 3, kupeste_y + 16], fill=hex2("#1a120c"))
    for y in range(guverte_y, H):
        d.line([0, y, GW, y], fill=hex2(_ac(ahsap, 0.05 - 0.15 * min(1, (y - guverte_y) / 200))))
    yy, aralik = guverte_y + 4, 4
    while yy < H:
        d.line([0, yy, GW, yy], fill=hex2(_ac(ahsap, -0.3)))
        aralik += 2
        yy += aralik
    rnd = random.Random(no)
    for _ in range(400):
        piksel(img, rnd.randrange(GW), rnd.randrange(guverte_y, H), hex2(_ac(ahsap, rnd.choice((-0.2, 0.15)))))
    kaydet(img, f"sahne{no}-orta.png")


# ==========================================================================
# YENİ FİGÜR: kadırga
# ==========================================================================
def _kadirga_govde(img, x, su_y, s, yon, bob, govde, serit, tente, yelken, mod, fener, faz):
    d = ImageDraw.Draw(img)
    X = lambda dx: x + dx * s * yon  # noqa: E731
    Y = lambda h: su_y + bob - h * s  # noqa: E731
    gun = [(-47, 8.6), (-44, 7.4), (-38, 5.8), (-30, 5.0), (0, 4.6), (30, 5.0), (37, 5.6), (41, 6.2)]
    alt = [(41, 2.4), (40, -0.5), (36, -3.0), (-38, -3.0), (-44, -2.0), (-47.6, 2.0)]
    d.polygon([(X(a), Y(b)) for a, b in gun + alt], fill=hex2(govde))
    for k in range(len(gun) - 1):                                       # renkli kuşak (güverte altında)
        (a1, b1), (a2, b2) = gun[k], gun[k + 1]
        d.line([X(a1), Y(b1 - 1.3), X(a2), Y(b2 - 1.3)], fill=hex2(serit), width=_u(0.9, s))
        d.line([X(a1), Y(b1), X(a2), Y(b2)], fill=hex2(_ac(govde, 0.35)))
    d.polygon([(X(40), Y(5.4)), (X(53), Y(4.4)), (X(53), Y(3.8)), (X(40), Y(3.2))], fill=hex2(_ac(govde, -0.1)))  # mahmuz
    a0, a1 = sorted((X(-33), X(33)))
    d.rectangle([a0, Y(6.4), a1, Y(4.6)], fill=hex2(_ac(govde, 0.12)))  # apostis (kürek kasnağı)
    d.line([a0, Y(7.2), a1, Y(7.2)], fill=hex2(_ac(govde, 0.25)))        # küpeşte korkuluğu
    for k in range(-32, 34, 6):
        d.line([X(k), Y(7.2), X(k), Y(6.4)], fill=hex2(_ac(govde, 0.25)))
    # kıç köşkü ve tente (kemerli)
    c0, c1 = sorted((X(-47), X(-35)))
    d.rectangle([c0, Y(9.4), c1, Y(8.2)], fill=hex2(_ac(govde, 0.2)))
    d.chord([c0, Y(14.6), c1, Y(9.0) + 1], 180, 360, fill=hex2(tente))
    for k in (-44, -41, -38):
        d.line([X(k), Y(13.8), X(k), Y(9.2)], fill=hex2(_ac(tente, -0.25)))
    d.line([X(-35.5), Y(9.2), X(-35.5), Y(12.6)], fill=hex2("#4a2a16"), width=_u(0.5, s))
    # direkler
    for dx, boy in ((6, 40), (29, 28)):
        d.rectangle([X(dx) - _u(0.5, s), Y(boy), X(dx) + _u(0.5, s) - 1, Y(4.6)], fill=hex2("#4a2a16"))
    # top (pruva)
    p0, p1 = sorted((X(37), X(43)))
    d.rectangle([p0, Y(6.4), p1, Y(5.4)], fill=hex2("#3a3a40"))
    # serenler ve yelkenler
    for dx, boy, L in ((6, 40, 52), (29, 28, 34)):
        if mod == "indik":
            on_, arka = (dx + 0.42 * L, 11.0), (dx - 0.58 * L, 13.5)
        else:
            aci = math.radians(23)
            px_, ph = dx, boy - 2.5
            on_ = (px_ + 0.4 * L * math.cos(aci), ph - 0.4 * L * math.sin(aci))
            arka = (px_ - 0.6 * L * math.cos(aci), ph + 0.6 * L * math.sin(aci))
        if mod == "acik":
            sis = 1.2 * SIN(faz)
            ka = (dx - 0.5 * L, 9.0)                                    # yelkenin alt arka köşesi (iskota)
            orta_ = ((on_[0] + ka[0]) / 2 + 3 + sis, (on_[1] + ka[1]) / 2 - 1)
            d.polygon([(X(on_[0]), Y(on_[1])), (X(arka[0]), Y(arka[1])), (X(ka[0]), Y(ka[1])),
                       (X(orta_[0]), Y(orta_[1]))], fill=hex2(yelken))
            for t_ in (0.3, 0.55, 0.8):                                 # yelken dikiş çizgileri
                ux, uy = on_[0] + (arka[0] - on_[0]) * t_, on_[1] + (arka[1] - on_[1]) * t_
                d.line([X(ux), Y(uy), X(ux + (ka[0] - ux) * 0.85), Y(uy + (ka[1] - uy) * 0.85)],
                       fill=hex2(_ac(yelken, -0.12)))
        d.line([X(on_[0]), Y(on_[1]), X(arka[0]), Y(arka[1])], fill=hex2("#5a3a1e"), width=_u(0.8, s))
        if mod in ("sarili", "indik"):                                  # serene sarılı yelken
            d.line([X(on_[0] + (arka[0] - on_[0]) * 0.1), Y(on_[1] + (arka[1] - on_[1]) * 0.1 - 0.9),
                    X(on_[0] + (arka[0] - on_[0]) * 0.85), Y(on_[1] + (arka[1] - on_[1]) * 0.85 - 0.9)],
                   fill=hex2(yelken), width=_u(1.1, s))
    for k in range(fener):                                              # kıçta fenerler
        fx = X(-46.5 + k * 2.2)
        d.rectangle([fx - _u(0.7, s), Y(17.0), fx + _u(0.7, s), Y(15.2)], fill=hex2("#e0b040"))
        d.line([fx, Y(15.2), fx, Y(14.4)], fill=hex2("#4a2a16"))


def kadirga(t, x, su_y, s=1.0, yon=1, faz=0.0, govde="#3a2418", serit="#a8281e", tente="#a8281e",
            yelken="#efe6d0", mod="sarili", flama="#c8302a", fener=0, kurek=True, kurekci=True, kontur=True,
            bob=True, isik=False):
    """Yeni figür: kadırga (bkz. modül açıklaması). Dönen değer: en üst nokta y'si."""
    b = int(round(SIN(faz) * 0.5 * s)) if bob else 0
    if kontur:
        figur(t, _kadirga_govde, x, su_y, s, yon, b, govde, serit, tente, yelken, mod, fener, faz)
    else:
        _kadirga_govde(t, x, su_y, s, yon, b, govde, serit, tente, yelken, mod, fener, faz)
    d = ImageDraw.Draw(t)
    X = lambda dx: x + dx * s * yon  # noqa: E731
    Y = lambda h: su_y + b - h * s  # noqa: E731
    ang = 2 * math.pi * faz
    if kurek:
        cek = math.cos(ang)
        kalk = max(0.0, -math.sin(ang))
        for k in range(24):
            dx = -29 + k * 2.5
            uc = dx - 3.5 + 4.0 * cek
            d.line([X(dx), Y(5.0), X(uc), Y(-1.8 + 3.0 * kalk)], fill=hex2("#4a2e18"), width=1)
            if s >= 1.2:
                d.line([X(uc), Y(-1.8 + 3.0 * kalk), X(uc - 0.9), Y(-2.6 + 3.0 * kalk)], fill=hex2("#6a4a28"), width=2)
        if kurekci:
            for k in range(0, 24, 2):                                   # kürekçi başları (insan ölçeği: boy/25)
                hx = X(-28.5 + k * 2.5 + 0.6 * cek)
                hy = Y(8.0)
                r = max(1, int(0.45 * s))
                d.rectangle([hx - r + 1, hy - r + 1, hx + r - 1, hy + r - 1] if r > 1 else [hx, hy, hx, hy + 1],
                            fill=hex2("#c89070"))
                piksel(t, hx, hy - r, hex2("#e8e0d0" if k % 4 else "#3a2a1a"))
    for dx, boy in ((6, 40), (29, 28)):                                 # direk başında flama (rüzgârla geriye)
        pts = []
        for j in range(0, 13):
            pts.append((X(dx - j * 0.9), Y(boy + 0.4 - j * 0.05) + SIN(faz + j / 9) * 0.6 * s))
        for j in range(len(pts) - 1):
            d.line([*pts[j], *pts[j + 1]], fill=hex2(flama), width=max(1, int(1.4 * s * (1 - j / 14))))
    if isik and fener:                                                  # gece: fener ışığı
        for k in range(fener):
            fx, fy = X(-46.5 + k * 2.2), Y(16.1)
            for r in range(2, int(5 * s)):
                for a in range(0, 360, 20):
                    px_, py_ = fx + math.cos(math.radians(a)) * r, fy + math.sin(math.radians(a)) * r
                    if _esik(int(px_), int(py_)) < 0.5 * (1 - r / (5 * s)):
                        piksel(t, px_, py_, hex2("#ffd479", 70))
    return Y(48)


# ==========================================================================
# YENİ FİGÜRLER: yapılar
# ==========================================================================
def provence_evleri(img, x0, x1, zemin, s=1.0, tohum=1, sivalar=("#e0c494", "#d8a878", "#ecd8b0", "#c89a74", "#e4b8a0"),
                    cati="#b05a3a", panjur=("#4a7a5a", "#3a6a8a", "#6a8a4a"), kapali=False, isik=False, kat=(2, 3)):
    """Yeni figür: Provence kıyı kasabası evleri. Bitişik 2-3 katlı sıvalı evler, alçak eğimli kiremit çatı, panjurlu
    pencereler (kapali=True: panjurlar kapalı; isik=True: bazı pencerelerde lamba ışığı), zemin katta kemerli kapı.
    Düz zemine kurulur. Dönen değer: baca noktaları [(x, y)]."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "provence_evleri")
    temel(img, zemin, x0, x1, y, "#6a5a48")
    rnd = random.Random(tohum)
    kh = max(4, int(round(7.5 * s)))
    bacalar = []
    x = x0
    while x1 - x >= int(9 * s):
        gw = min(int(rnd.randint(13, 21) * s), x1 - x)
        n_kat = rnd.choice(kat)
        ust = y - n_kat * kh
        siva = rnd.choice(sivalar)
        d.rectangle([x, ust, x + gw - 1, y - 1], fill=hex2(siva))
        d.line([x, ust, x, y - 1], fill=hex2(_ac(siva, -0.28)))
        ch = max(2, int(3.2 * s))
        d.polygon([(x - _u(1, s), ust), (x + gw - 1 + _u(1, s), ust), (x + gw - 1 - int(3 * s), ust - ch), (x + int(3 * s), ust - ch)],
                  fill=hex2(cati))
        d.line([x - _u(1, s), ust, x + gw - 1 + _u(1, s), ust], fill=hex2(_ac(cati, -0.35)))
        for tx in range(x, x + gw, max(2, int(1.6 * s))):                # kiremit dalgaları
            piksel(img, tx, ust - max(1, ch // 2), hex2(_ac(cati, 0.18)))
        if rnd.random() < 0.6:
            bx = x + int(gw * rnd.uniform(0.25, 0.75))
            d.rectangle([bx, ust - ch - int(2.2 * s), bx + max(1, int(1.4 * s)), ust - ch + 1], fill=hex2(_ac(siva, -0.2)))
            bacalar.append((bx + 1, ust - ch - int(2.2 * s)))
        n = max(1, gw // max(4, int(7 * s)))
        for k in range(n_kat):
            fy = y - k * kh
            for j in range(n):
                wx = x + int((j + 0.5) * gw / n)
                if k == 0 and j == n // 2:                                  # kemerli kapı
                    kw = max(1, int(1.6 * s))
                    d.rectangle([wx - kw, fy - int(5.2 * s), wx + kw, fy - 1], fill=hex2("#4a2e1a"))
                    d.chord([wx - kw, fy - int(6.4 * s), wx + kw, fy - int(4.2 * s)], 180, 360, fill=hex2("#4a2e1a"))
                    continue
                pw = max(1, int(1.1 * s))
                a, b = fy - kh + max(1, int(2 * s)), fy - max(1, int(1.6 * s))
                pj = rnd.choice(panjur)
                if kapali:
                    d.rectangle([wx - pw, a, wx + pw, b], fill=hex2(pj))
                    d.line([wx, a, wx, b], fill=hex2(_ac(pj, -0.35)))
                else:
                    yanik = isik and rnd.random() < 0.45
                    d.rectangle([wx - pw, a, wx + pw, b], fill=hex2("#f8c860" if yanik else "#2a2a30"))
                    if s >= 1.4:
                        d.rectangle([wx - pw - max(1, int(0.8 * s)), a, wx - pw - 1, b], fill=hex2(pj))
                        d.rectangle([wx + pw + 1, a, wx + pw + max(1, int(0.8 * s)), b], fill=hex2(pj))
        x += gw
    return bacalar


def katedral(img, x, zemin, s=1.0, tas="#cdb894", cati="#a0583a", isik=False, kapi_acik=False):
    """Yeni figür: Romanesk kilise (Toulon katedrali için temsilî): üçgen alınlıklı nef cephesi, kemerli taç kapı,
    gül pencere, sağda alçak yan nef, solda kare çan kulesi (kemerli çan gözleri, kiremit piramit külah).
    Düz zemine kurulur. Dönen değer: kule tepesinin y'si."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(19 * s), x + int(18 * s), "katedral")
    temel(img, zemin, x - int(19 * s), x + int(18 * s), y, "#6a5a48")
    gol = _ac(tas, -0.2)
    d.rectangle([x + int(12 * s), y - int(17 * s), x + int(18 * s), y - 1], fill=hex2(gol))           # yan nef
    d.polygon([(x + int(12 * s), y - int(17 * s)), (x + int(12 * s), y - int(22 * s)), (x + int(19 * s), y - int(17 * s))],
              fill=hex2(cati))
    d.rectangle([x - int(10 * s), y - int(28 * s), x + int(12 * s), y - 1], fill=hex2(tas))             # nef cephesi
    d.polygon([(x - int(11 * s), y - int(28 * s)), (x + int(1 * s), y - int(37 * s)), (x + int(13 * s), y - int(28 * s))],
              fill=hex2(_ac(tas, 0.06)))
    d.line([x - int(11 * s), y - int(28 * s), x + int(1 * s), y - int(37 * s), x + int(13 * s), y - int(28 * s)],
           fill=hex2(gol), width=_u(0.6, s))
    for k in range(1, 5):                                                                           # kesme taş sıraları
        d.line([x - int(10 * s), y - int(k * 6 * s), x + int(12 * s), y - int(k * 6 * s)], fill=hex2(_ac(tas, -0.08)))
    cx = x + int(1 * s)
    kw = int(3.4 * s)
    for k, renk in ((2.2, gol), (1.2, _ac(tas, 0.15))):                                             # kemer kuşakları
        d.chord([cx - kw - int(k * s), y - int(16 * s) - int(k * s), cx + kw + int(k * s), y - int(8 * s) + int(k * s)],
                180, 360, fill=hex2(renk))
    kapi = "#f8c860" if kapi_acik else "#4a2e1a"
    d.chord([cx - kw, y - int(16 * s), cx + kw, y - int(8 * s)], 180, 360, fill=hex2(kapi))
    d.rectangle([cx - kw, y - int(12 * s), cx + kw, y - 1], fill=hex2(kapi))
    if not kapi_acik:
        d.line([cx, y - int(15 * s), cx, y - 1], fill=hex2("#2a1a10"))
    gr = int(3.2 * s)                                                                                # gül pencere
    gy = y - int(22 * s)
    d.ellipse([cx - gr - 1, gy - gr - 1, cx + gr + 1, gy + gr + 1], fill=hex2(gol))
    d.ellipse([cx - gr, gy - gr, cx + gr, gy + gr], fill=hex2("#f8c860" if isik else "#3a3a5a"))
    for a in range(0, 360, 45):
        d.line([cx, gy, cx + math.cos(math.radians(a)) * gr, gy + math.sin(math.radians(a)) * gr], fill=hex2(gol))
    tx0, tx1 = x - int(19 * s), x - int(10 * s)                                                      # çan kulesi
    d.rectangle([tx0, y - int(46 * s), tx1, y - 1], fill=hex2(_ac(tas, -0.05)))
    d.line([tx1, y - int(46 * s), tx1, y - 1], fill=hex2(gol))
    for k in range(1, 8):
        d.line([tx0, y - int(k * 6 * s), tx1, y - int(k * 6 * s)], fill=hex2(_ac(tas, -0.12)))
    for bx in (tx0 + int(2.4 * s), tx1 - int(2.4 * s)):                                               # çan gözleri
        d.rectangle([bx - int(1.2 * s), y - int(42 * s), bx + int(1.2 * s), y - int(37 * s)], fill=hex2("#2a2a32"))
        d.chord([bx - int(1.2 * s), y - int(43.4 * s), bx + int(1.2 * s), y - int(41 * s)], 180, 360, fill=hex2("#2a2a32"))
    d.rectangle([tx0 + int(3.5 * s), y - int(30 * s), tx1 - int(3.5 * s), y - int(27 * s)], fill=hex2("#2a2a32"))
    d.polygon([(tx0 - _u(0.6, s), y - int(46 * s)), (tx1 + _u(0.6, s), y - int(46 * s)), ((tx0 + tx1) / 2, y - int(53 * s))],
              fill=hex2(cati))
    tepe = y - int(53 * s)
    d.line([(tx0 + tx1) / 2, tepe, (tx0 + tx1) / 2, tepe - int(3 * s)], fill=hex2("#3a3a3a"), width=_u(0.4, s))
    d.line([(tx0 + tx1) / 2 - int(1.2 * s), tepe - int(2 * s), (tx0 + tx1) / 2 + int(1.2 * s), tepe - int(2 * s)],
           fill=hex2("#3a3a3a"), width=_u(0.4, s))
    return tepe - int(3 * s)


def kaya_tepe(img, x0, x1, ust0, ust1, taban_y, ust_y, renk=("#9a8a72", "#7a6c58", "#5e5444"), tohum=1):
    """Yeni figür: düz tepeli kaya (kale tepesi). Tabanı x0-x1 arasında taban_y satırına (düz zemine) oturur; tepesi
    ust0-ust1 arasında dümdüz (ust_y). Yan yüzler basamaklı ve çatlaklı. Dönen değer: tepedeki düz zemin listesi."""
    d = ImageDraw.Draw(img)
    rnd = random.Random(tohum)
    sol, sag = [], []
    n = 7
    for k in range(n + 1):
        t = k / n
        yy = int(taban_y + (ust_y - taban_y) * t)
        sol.append((int(x0 + (ust0 - x0) * t + rnd.randint(-3, 3) * (0 < k < n)), yy))
        sag.append((int(x1 + (ust1 - x1) * t + rnd.randint(-3, 3) * (0 < k < n)), yy))
    d.polygon(sol + sag[::-1], fill=hex2(renk[0]))
    for k in range(len(sol) - 1):                                       # gölgeli sağ yüz
        d.polygon([sag[k], sag[k + 1], (sag[k + 1][0] - 6, sag[k + 1][1]), (sag[k][0] - 8, sag[k][1])], fill=hex2(renk[1]))
    for _ in range(int((x1 - x0) * (taban_y - ust_y) / 60)):            # çatlaklar ve taş dokusu
        px_ = rnd.randint(x0, x1)
        py_ = rnd.randint(ust_y + 2, taban_y - 2)
        if img.getpixel((px_, py_))[3] > 0:
            d.line([px_, py_, px_ + rnd.randint(-3, 3), py_ + rnd.randint(2, 5)], fill=hex2(renk[2]))
    d.line([ust0, ust_y, ust1, ust_y], fill=hex2(_ac(renk[0], 0.25)))
    z = [taban_y] * img.width
    for xx in range(ust0, ust1 + 1):
        z[xx] = ust_y
    return z


def yangin(t, x, y, f, s=1.0, tohum=1):
    """Yeni figür: çatıya ya da zemine (y) oturan alev dilleri ve yükselen kıvılcımlar; f ile titrer (dikişsiz)."""
    d = ImageDraw.Draw(t)
    rnd = random.Random(tohum)
    for k in range(5):
        dx = (k - 2) * 1.6 * s + rnd.uniform(-0.5, 0.5) * s
        boy = (4.5 + 2.2 * SIN(f + k * 0.21, 2) + rnd.uniform(0, 2)) * s * (1.0 - abs(k - 2) * 0.18)
        for r, renk in ((1.6, "#c8381c"), (1.1, "#f08a2a"), (0.55, "#ffe08a")):
            d.polygon([(x + dx - r * s, y), (x + dx + 0.6 * SIN(f + k * 0.3, 3) * s, y - boy * r / 1.6), (x + dx + r * s, y)],
                      fill=hex2(renk))
    for j in range(4):
        ph = (f + j * 0.25 + rnd.random()) % 1
        piksel(t, x + (rnd.uniform(-3, 3) + ph * 2) * s, y - (6 + ph * 14) * s, hex2("#ffc860", int(255 * (1 - ph))))


# ==========================================================================
# YENİ FİGÜRLER: kişiler
# ==========================================================================
def basortulu(img, x, zemin, s=1.0, govde="#8a2a2a", ortu="#e8e0d0", yon=1, kemer=None, **kw):
    """Yeni figür (orhun_yazitlari.basortulu kalıbı): başörtülü kadın; örtü alnı ve saçı örter, göz açık kalır."""
    kisi(img, x, zemin, s, govde=govde, bas=None, kadin=True, yon=yon, kemer=kemer, **kw)
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    by = y - int(13.6 * s)
    r = max(2, int(1.7 * s))
    k = hex2(ortu)
    d.chord([x - r - 1, by - r - 1, x + r + 1, by], 180, 360, fill=k)
    arka = x - r * yon
    d.rectangle([min(arka, arka - int(0.8 * s) * yon), by - int(0.8 * s), max(arka, arka - int(0.8 * s) * yon), by + r + int(2 * s)], fill=k)


def cocuk(img, x, zemin, s=1.0, govde="#6a5a8a", sac="#4a2e1a", yon=1, adim=None, kol=0.0, kiz=False):
    """Yeni figür: çocuk. kisi gövdesi (kemersiz, küçük ölçek), açık başta saç (göz açık kalır); kiz=True: ensede örgü."""
    kisi(img, x, zemin, s, govde=govde, bas=None, yon=yon, adim=adim, kol=kol, kemer=None, kadin=kiz)
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    by = y - int(13.6 * s)
    r = max(2, int(1.7 * s))
    d.chord([x - r - 1, by - r - 1, x + r + 1, by + r // 3], 180, 360, fill=hex2(sac))
    ax = x - r * yon
    d.rectangle([min(ax, ax + (r // 3) * yon), by - r // 2, max(ax, ax + (r // 3) * yon), by + (r if kiz else r // 3)], fill=hex2(sac))


def bohca(img, x, zemin, s=1.0, yon=1, renk="#8a6a4a"):
    """Yeni figür: sırtta taşınan bohça (kisi'nin omzuna oturur; aynı x, zemin, s ile çağrılır)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    ust = y - int(11 * s)
    bx = x - int(2.6 * s) * yon
    d.ellipse([bx - int(2.4 * s), ust - int(0.6 * s), bx + int(2.4 * s), ust + int(4.4 * s)], fill=hex2(renk))
    d.line([bx - int(1.6 * s), ust + int(1 * s), bx + int(1.4 * s), ust + int(3.6 * s)], fill=hex2(_ac(renk, -0.3)))
    d.line([x - int(0.5 * s) * yon, ust + int(0.2 * s), bx, ust + int(0.4 * s)], fill=hex2(_ac(renk, -0.4)), width=_u(0.5, s))


def rahip(img, x, zemin, s=1.0, govde="#1e1e24", ust="#ece8e0", yon=1, kol=0.0, silah=None, adim=None, sapka=False,
          stol=None):
    """Yeni figür: rahip. Uzun cüppe (kemersiz), beyaz yaka; ust: cüppenin üstüne beyaz keten (surplis) rengi ya da
    None; stol: boyundan sarkan kuşak rengi. sapka=True: yolcu rahibin geniş kenarlı siyah şapkası, yoksa takke."""
    kisi(img, x, zemin, s, govde=govde, bas="sapka" if sapka else "takke", bas_renk="#141418", sakal=None, yon=yon,
         kol=kol, silah=silah, adim=adim, kemer=None)
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    u_ = y - int(11 * s)
    if ust:                                                             # surplis: göğüsten kalçaya beyaz
        d.polygon([(x - int(2.6 * s), u_ + int(6.5 * s)), (x - int(2 * s), u_ + int(1 * s)), (x + int(2 * s), u_ + int(1 * s)),
                   (x + int(2.6 * s), u_ + int(6.5 * s))], fill=hex2(ust))
    if stol:
        for k in (-1, 1):
            d.line([x + int(0.8 * s) * k, u_ + int(0.6 * s), x + int(0.9 * s) * k, u_ + int(6 * s)], fill=hex2(stol), width=_u(0.5, s))
    d.rectangle([x - int(0.9 * s), u_, x + int(0.9 * s), u_ + max(1, int(0.5 * s))], fill=hex2("#f4f0e8"))
    omuz = (x + int(0.5 * s) * yon, u_ + int(1 * s))
    el = (x + int(3.5 * s) * yon, u_ - int(4 * s * kol) + int(1 * s)) if kol > 0 else (x + int(2.5 * s) * yon, u_ + int(5 * s))
    d.line([*omuz, *el], fill=hex2(_ac(ust or govde, -0.15)), width=_u(1, s))     # kol (surplis yeni)
    piksel(img, el[0], el[1], hex2("#d6a07a"))


def avrupali(img, x, zemin, s=1.0, govde="#2a2a34", sac="#7a6a5a", sakal=None, yon=1, silah=None, kol=0.0, adim=None):
    """Yeni figür (orhun_yazitlari.avrupali kalıbı): 19. yüzyıl bilgini. Kemersiz redingot, beyaz yaka, açık başta saç."""
    kisi(img, x, zemin, s, govde=govde, bas=None, bas_renk="#1a1a1e", sakal=sakal, yon=yon, silah=silah, kol=kol,
         adim=adim, kemer=None)
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    ust = y - int(11 * s)
    d.rectangle([x - int(0.9 * s), ust, x + int(0.9 * s), ust + max(1, int(0.5 * s))], fill=hex2("#f0ece4"))
    by = y - int(13.6 * s)
    r = max(2, int(1.7 * s))
    d.chord([x - r - 1, by - r - 1, x + r + 1, by + r // 3], 180, 360, fill=hex2(sac))
    ax = x - r * yon
    d.rectangle([min(ax, ax + (r // 3) * yon), by - r // 2, max(ax, ax + (r // 3) * yon), by + r // 3], fill=hex2(sac))


def _el(x, z, s, yon, kol):
    """kisi() figürünün el ucu (timur_figur.kisi ile aynı formül; ayakta)."""
    y = zemin_y(z, x, 6 * s)
    ust = y - int(11 * s)
    if kol > 0:
        return x + int(3.5 * s) * yon, ust - int(4 * s * kol) + int(1 * s)
    return x + int(2.5 * s) * yon, ust + int(5 * s)


def kundak(img, x, y, s=1.0, yon=1):
    """Yeni figür: kundaklı bebek (elde tutulur; x, y = elin konumu, bebek elin üstünde yatar). Yüzü açık, gözü kapalı."""
    d = ImageDraw.Draw(img)
    d.ellipse([x - int(2.6 * s), y - int(1.8 * s), x + int(2.6 * s), y + int(0.6 * s)], fill=hex2("#f4f0e8"))
    d.line([x - int(1.6 * s), y - int(0.6 * s), x + int(1.4 * s), y - int(0.6 * s)], fill=hex2("#d8d0c4"))
    hx = x + int(2.2 * s) * yon
    d.ellipse([hx - int(1 * s), y - int(1.6 * s), hx + int(1 * s), y + int(0.2 * s)], fill=hex2("#e8b890"))
    piksel(img, hx + int(0.3 * s) * yon, y - int(0.8 * s), hex2("#5a3a2a"))


def mizrak_omuz(img, x, zemin, s, yon, f=0.0):
    """Omuzda eğik tutulan mızrak: elden öne-yukarı (30°); dikey mızrak yazı bandına girmesin diye."""
    d = ImageDraw.Draw(img)
    ex, ey = _el(x, zemin, s, yon, 0.0)
    ey -= int(1 * s)
    L = 19 * s
    ux, uy = ex + L * 0.86 * yon, ey - L * 0.5 + SIN(f) * 0.3 * s
    bx, by = ex - 4 * s * 0.86 * yon, ey + 4 * s * 0.5
    d.line([bx, by, ux, uy], fill=hex2("#5a3a22"), width=_u(0.7, s))
    d.polygon([(ux, uy), (ux + 2.6 * s * 0.86 * yon, uy - 2.6 * s * 0.5), (ux + 0.4 * s * yon, uy + 0.9 * s)], fill=hex2("#c8ccd0"))


# ==========================================================================
# YENİ FİGÜRLER: eşyalar
# ==========================================================================
def vaftiz_kurnasi(img, x, zemin, s=1.0, tas="#b8b0a0"):
    """Yeni figür: taş vaftiz kurnası. Sekizgen kaide zemine basar, ayak, geniş çanak; çanakta su."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 10 * s)
    temas_golgesi(img, x, y, 11 * s)
    d.rectangle([x - int(5 * s), y - int(1.6 * s), x + int(5 * s), y - 1], fill=hex2(_ac(tas, -0.2)))
    d.rectangle([x - int(1.8 * s), y - int(7 * s), x + int(1.8 * s), y - int(1.6 * s)], fill=hex2(tas))
    d.line([x - int(0.8 * s), y - int(6.6 * s), x - int(0.8 * s), y - int(2 * s)], fill=hex2(_ac(tas, 0.2)))
    d.polygon([(x - int(6 * s), y - int(11 * s)), (x + int(6 * s), y - int(11 * s)), (x + int(3.4 * s), y - int(7 * s)),
               (x - int(3.4 * s), y - int(7 * s))], fill=hex2(tas))
    d.rectangle([x - int(6.4 * s), y - int(12 * s), x + int(6.4 * s), y - int(11 * s)], fill=hex2(_ac(tas, 0.12)))
    d.line([x - int(5.4 * s), y - int(12 * s), x + int(5.4 * s), y - int(12 * s)], fill=hex2("#6a9ac8"), width=_u(0.4, s))
    for k in (-3, 0, 3):
        d.line([x + int(k * s), y - int(10.6 * s), x + int(k * 0.6 * s), y - int(7.4 * s)], fill=hex2(_ac(tas, -0.15)))


def kilise_kursusu(img, x, zemin, s=1.0, yon=1, f=0.0, yaz=False):
    """Yeni figür: ayaklı ahşap kürsü, eğik tablasında açık büyük defter (vaftiz defteri). Ayak zemine basar.
    yaz=True: defterin sağ sayfasında satırlar f ile birer birer belirir. Dönen değer: defterin yazı noktası."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 7 * s)
    temas_golgesi(img, x, y, 8 * s)
    ag = "#5a3a1e"
    d.rectangle([x - int(3.5 * s), y - int(1.2 * s), x + int(3.5 * s), y - 1], fill=hex2(_ac(ag, -0.2)))
    d.rectangle([x - int(1 * s), y - int(9.5 * s), x + int(1 * s), y - int(1.2 * s)], fill=hex2(ag))
    ty = y - int(10 * s)
    d.polygon([(x - int(5 * s) * yon, ty + int(1.4 * s)), (x + int(5 * s) * yon, ty - int(1 * s)),
               (x + int(5 * s) * yon, ty), (x - int(5 * s) * yon, ty + int(2.4 * s))], fill=hex2(_ac(ag, 0.12)))
    a, b = (x - int(4.6 * s) * yon, ty + int(0.6 * s)), (x + int(4.6 * s) * yon, ty - int(1.4 * s))
    m = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2 - int(0.6 * s))
    d.polygon([a, m, (m[0], m[1] - int(2.4 * s)), (a[0], a[1] - int(2.2 * s))], fill=hex2("#f0e6cc"))
    d.polygon([m, b, (b[0], b[1] - int(2.2 * s)), (m[0], m[1] - int(2.4 * s))], fill=hex2("#e8dcc0"))
    n = 4 if not yaz else 1 + int(f * 4)
    for k in range(n):
        t_ = 0.2 + k * 0.18
        px_ = m[0] + (b[0] - m[0]) * t_
        py_ = m[1] + (b[1] - m[1]) * t_ - int(1.8 * s) + k * 0
        d.line([px_, py_, px_ + int(0.8 * s) * yon, py_ + int(0.9 * s)], fill=hex2("#3a2a1a"))
    for k in range(4):
        t_ = 0.2 + k * 0.18
        px_ = a[0] + (m[0] - a[0]) * t_
        py_ = a[1] + (m[1] - a[1]) * t_ - int(1.8 * s)
        d.line([px_, py_, px_ + int(0.8 * s) * yon, py_ + int(0.9 * s)], fill=hex2("#3a2a1a"))
    return m[0] + int(1.5 * s) * yon, m[1] - int(1.2 * s)


def altin_sandigi(img, x, zemin, s=1.0, f=0.0, acik=True):
    """Yeni figür: demir bantlı ahşap sandık; açık kapağın altında altın sikkeler parlar. Tabanı zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 12 * s)
    temas_golgesi(img, x, y, 13 * s)
    ag = "#6a3a1e"
    d.rectangle([x - int(6 * s), y - int(6 * s), x + int(6 * s), y - 1], fill=hex2(ag))
    for k in (-4, 4):
        d.rectangle([x + int(k * s) - _u(0.4, s), y - int(6 * s), x + int(k * s) + _u(0.4, s), y - 1], fill=hex2("#3a3a40"))
    if acik:
        d.polygon([(x - int(6 * s), y - int(6 * s)), (x + int(6 * s), y - int(6 * s)), (x + int(5 * s), y - int(11 * s)),
                   (x - int(7 * s), y - int(11 * s))], fill=hex2(_ac(ag, -0.25)))
        d.chord([x - int(5.6 * s), y - int(8 * s), x + int(5.6 * s), y - int(4.4 * s)], 180, 360, fill=hex2("#e0b040"))
        rnd = random.Random(int(x))
        for k in range(int(10 * s)):
            px_ = x + rnd.uniform(-5, 5) * s
            py_ = y - int(6.2 * s) - rnd.uniform(0, 1.4) * s
            parla = (rnd.random() + f) % 1 < 0.15
            piksel(img, px_, py_, hex2("#fff4c0" if parla else "#c89a2a"))
    else:
        d.rectangle([x - int(6.4 * s), y - int(8 * s), x + int(6.4 * s), y - int(6 * s)], fill=hex2(_ac(ag, 0.1)))
    d.rectangle([x - _u(0.8, s), y - int(5 * s), x + _u(0.8, s), y - int(3.6 * s)], fill=hex2("#c8a040"))


def ipek_toplari(img, x, zemin, s=1.0, renkler=("#a8282a", "#d8b040", "#2a6a8a")):
    """Yeni figür: üst üste konmuş ipek topları (rulo kumaş); alttaki iki top zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 12 * s)
    temas_golgesi(img, x, y, 12 * s)
    r = int(2.4 * s)
    for k, (dx, dy) in enumerate(((-3, 0), (3, 0), (0, 1))):
        cx, cy = x + int(dx * s), y - r - (int(2 * r * dy * 0.86))
        renk = renkler[k % len(renkler)]
        d.rectangle([cx - int(3 * s), cy - r, cx + int(3 * s), cy + r - 1], fill=hex2(renk))
        d.ellipse([cx + int(3 * s) - r // 2, cy - r, cx + int(3 * s) + r // 2, cy + r - 1], fill=hex2(_ac(renk, 0.2)))
        d.line([cx - int(3 * s), cy - r // 2, cx + int(3 * s), cy - r // 2], fill=hex2(_ac(renk, 0.35)))


def cuval(img, x, zemin, s=1.0, renk="#c8b088"):
    """Yeni figür: erzak çuvalı (buğday/peksimet); dibi zemine yayılır, ağzı bağlı."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 7 * s)
    temas_golgesi(img, x, y, 8 * s)
    d.polygon([(x - int(3.6 * s), y - 1), (x + int(3.6 * s), y - 1), (x + int(3 * s), y - int(6 * s)), (x + int(1 * s), y - int(7.6 * s)),
               (x - int(1 * s), y - int(7.6 * s)), (x - int(3 * s), y - int(6 * s))], fill=hex2(renk))
    d.line([x - int(1.2 * s), y - int(6.8 * s), x + int(1.2 * s), y - int(6.8 * s)], fill=hex2(_ac(renk, -0.4)), width=_u(0.4, s))
    d.line([x - int(2 * s), y - int(4 * s), x + int(0.5 * s), y - int(2 * s)], fill=hex2(_ac(renk, -0.15)))


def fici(img, x, zemin, s=1.0, renk="#7a5232"):
    """Yeni figür (hezarfen.fici kalıbı): barut fıçısı; demir çemberli, tabanı zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    temas_golgesi(img, x, y, 7 * s)
    d.rounded_rectangle([x - int(3 * s), y - int(7 * s), x + int(3 * s), y - 1], radius=_u(1.5, s), fill=hex2(renk))
    for k in (1.5, 3.5, 5.5):
        d.line([x - int(3 * s), y - int(k * s), x + int(3 * s), y - int(k * s)], fill=hex2("#3a3a40"), width=_u(0.4, s))
    d.line([x - int(1.5 * s), y - int(6.6 * s), x - int(1.5 * s), y - int(0.6 * s)], fill=hex2(_ac(renk, 0.25)))


def tezgah(img, x, zemin, s=1.0, mal="ekmek", tente="#c8a040"):
    """Yeni figür: pazar tezgâhı. Dört ayak zemine basar, iki direk tenteyi taşır; tablada ekmek ya da balık."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 20 * s)
    temas_golgesi(img, x, y, 20 * s)
    ag = "#6a4a2a"
    top = y - int(7 * s)
    for k in (-9, 9):
        d.rectangle([x + int(k * s) - _u(0.5, s), top, x + int(k * s) + _u(0.5, s), y - 1], fill=hex2(ag))
        d.rectangle([x + int(k * s) - _u(0.4, s), y - int(19 * s), x + int(k * s) + _u(0.4, s), top], fill=hex2(_ac(ag, -0.2)))
    d.rectangle([x - int(10 * s), top - _u(1, s), x + int(10 * s), top + int(2 * s)], fill=hex2(_ac(ag, 0.15)))
    d.polygon([(x - int(11 * s), y - int(19 * s)), (x + int(11 * s), y - int(19 * s)), (x + int(12 * s), y - int(16 * s)),
               (x - int(12 * s), y - int(16 * s))], fill=hex2(tente))
    for k in range(-11, 12, 4):
        d.polygon([(x + int(k * s), y - int(16 * s)), (x + int((k + 2) * s), y - int(16 * s)), (x + int((k + 1) * s), y - int(15 * s))],
                  fill=hex2(_ac(tente, -0.3)))
        d.line([x + int(k * s), y - int(19 * s), x + int((k + 0.6) * s), y - int(16 * s)], fill=hex2("#f4ecd8"))
    if mal == "ekmek":
        for k in range(-8, 9, 3):
            d.ellipse([x + int((k - 1.3) * s), top - int(2.2 * s), x + int((k + 1.3) * s), top], fill=hex2("#c8883a"))
            piksel(img, x + int(k * s), top - int(1.6 * s), hex2("#f0c070"))
    else:
        for k in range(-8, 9, 4):
            d.polygon([(x + int((k - 1.6) * s), top - int(0.8 * s)), (x + int((k + 1.2) * s), top - int(1.4 * s)),
                       (x + int((k + 1.8) * s), top - int(0.2 * s)), (x + int((k - 1.6) * s), top)], fill=hex2("#a8b8c8"))


def kuyu(img, x, zemin, s=1.0, tas="#a89a84"):
    """Yeni figür: taş bilezikli meydan kuyusu; iki direk ve makara, ipte kova. Bilezik zemine oturur."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 10 * s)
    temas_golgesi(img, x, y, 11 * s)
    d.rectangle([x - int(5 * s), y - int(5 * s), x + int(5 * s), y - 1], fill=hex2(tas))
    for k in range(1, 3):
        d.line([x - int(5 * s), y - int(k * 1.8 * s), x + int(5 * s), y - int(k * 1.8 * s)], fill=hex2(_ac(tas, -0.18)))
    d.rectangle([x - int(5.6 * s), y - int(6 * s), x + int(5.6 * s), y - int(5 * s)], fill=hex2(_ac(tas, 0.15)))
    for k in (-4, 4):
        d.rectangle([x + int(k * s) - _u(0.4, s), y - int(13 * s), x + int(k * s) + _u(0.4, s), y - int(6 * s)], fill=hex2("#5a3a22"))
    d.line([x - int(4.6 * s), y - int(12.6 * s), x + int(4.6 * s), y - int(12.6 * s)], fill=hex2("#5a3a22"), width=_u(0.6, s))
    d.line([x, y - int(12.6 * s), x, y - int(8.6 * s)], fill=hex2("#8a7a5a"))
    d.rectangle([x - int(1 * s), y - int(8.6 * s), x + int(1 * s), y - int(6.6 * s)], fill=hex2("#6a4a2a"))


def sokak_feneri(t, x, zemin, s=1.0, f=0.0, yanik=True):
    """Yeni figür: ahşap direkli sokak feneri; direk zemine dikili (dibinde taş), fener kolda asılı; gece titrer."""
    d = ImageDraw.Draw(t)
    y = zemin_y(zemin, x, 4 * s)
    temas_golgesi(t, x, y, 5 * s)
    d.rectangle([x - int(1.4 * s), y - int(1.4 * s), x + int(1.4 * s), y - 1], fill=hex2("#6a6458"))
    d.rectangle([x - _u(0.4, s), y - int(18 * s), x + _u(0.4, s), y - int(1.4 * s)], fill=hex2("#4a3220"))
    d.line([x, y - int(17.4 * s), x + int(3.4 * s), y - int(17.4 * s)], fill=hex2("#4a3220"), width=_u(0.5, s))
    fx, fy = x + int(3.4 * s), y - int(15.2 * s)
    d.line([fx, y - int(17.4 * s), fx, fy - int(1.4 * s)], fill=hex2("#3a3a3a"))
    d.rectangle([fx - int(1.1 * s), fy - int(1.4 * s), fx + int(1.1 * s), fy + int(1.4 * s)], fill=hex2("#3a3a3a"))
    if yanik:
        g = 0.75 + 0.25 * SIN(f, 3)
        d.rectangle([fx - int(0.6 * s), fy - int(0.8 * s), fx + int(0.6 * s), fy + int(0.8 * s)], fill=hex2("#ffd060"))
        for r in range(int(2 * s), int(9 * s)):
            for a in range(0, 360, 12):
                px_, py_ = fx + math.cos(math.radians(a)) * r, fy + math.sin(math.radians(a)) * r
                if py_ < y - 1 and _esik(int(px_), int(py_)) < 0.45 * g * (1 - r / (9 * s)):
                    piksel(t, px_, py_, hex2("#ffd479", 60))


def tas_duvar(img, x0, x1, zemin, s=1.0, tas="#8a8070", tohum=1):
    """Yeni figür: alçak kuru taş duvar (bahçe duvarı); dibi zemine oturur. Zemin dokusu sayılır (denetimde çizilmez)."""
    if _DENETIM[0]:
        return
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "tas_duvar", tolerans=6)
    rnd = random.Random(tohum)
    h = int(5 * s)
    d.rectangle([x0, y - h, x1, y - 1], fill=hex2(tas))
    for k in range(0, h, max(2, int(1.6 * s))):
        xx = x0 + rnd.randint(0, 4)
        while xx < x1:
            ww = rnd.randint(int(2 * s), int(4 * s))
            d.rectangle([xx, y - 1 - k - max(1, int(1.4 * s)), min(x1, xx + ww), y - 1 - k], outline=hex2(_ac(tas, -0.25)),
                        fill=hex2(_ac(tas, rnd.uniform(-0.08, 0.1))))
            xx += ww + 1
    d.line([x0, y - h, x1, y - h], fill=hex2(_ac(tas, 0.25)))


def kayik(t, x, su_y, s=1.0, yon=1, faz=0.0, govde="#7a5a3a", serit="#3a6a8a"):
    """Yeni figür: demirli boş balıkçı kayığı; gövde su çizgisine oturur, dalgayla hafifçe iner kalkar."""
    d = ImageDraw.Draw(t)
    b = int(round(SIN(faz) * 0.4 * s))
    y = su_y + b
    d.polygon([(x - int(9 * s), y - int(3.4 * s)), (x + int(9 * s), y - int(3.4 * s)), (x + int(7 * s), y + int(2 * s)),
               (x - int(7.5 * s), y + int(2 * s))], fill=hex2(govde))
    d.line([x - int(9 * s), y - int(3.4 * s), x + int(9 * s), y - int(3.4 * s)], fill=hex2(_ac(govde, 0.3)))
    d.line([x - int(8.4 * s), y - int(2.2 * s), x + int(8.4 * s), y - int(2.2 * s)], fill=hex2(serit))
    d.line([x + int(9 * s) * yon, y - int(3.4 * s), x + int(10 * s) * yon, y - int(5 * s)], fill=hex2(_ac(govde, -0.2)), width=_u(0.5, s))
    d.line([x - int(2 * s), y - int(3.6 * s), x + int(3 * s), y - int(4.4 * s)], fill=hex2("#a88a5a"), width=_u(0.4, s))  # kürek


def _rakam(img, x, y, metin, renk, olcek=1):
    """3x5 piksel rakam yazısı (kuşbakışı kâğıtlarda sayı)."""
    font = {"0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"],
            "4": ["101", "101", "111", "001", "001"], "8": ["111", "101", "111", "101", "111"],
            ".": ["000", "000", "000", "000", "010"], "?": ["111", "001", "011", "000", "010"]}
    d = ImageDraw.Draw(img)
    cx = x
    for ch in metin:
        g = font[ch]
        for r, satir in enumerate(g):
            for c, v in enumerate(satir):
                if v == "1":
                    d.rectangle([cx + c * olcek, y + r * olcek, cx + c * olcek + olcek - 1, y + r * olcek + olcek - 1], fill=hex2(renk))
        cx += 4 * olcek
    return cx
