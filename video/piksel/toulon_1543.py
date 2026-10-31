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
from kalender import kitaplar, taht  # noqa: E402
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


def _bant_denetimi(no, orta_bant=True):
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
                    for y in range(y0, y1 + 1) if orta_bant else ():
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


def _spr(no, kare, esik=0.995, orta_bant=True):
    b = P(no)
    _kadraj(no, kare, esik)
    sprite(no, "karakter", b["w"], b["h"], KARE, kare)
    _bant_denetimi(no, orta_bant)


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
            uc = dx - 4.5 + 4.5 * cek
            uy = -0.6 + 2.6 * kalk
            d.line([X(dx), Y(5.6), X(uc), Y(uy)], fill=hex2("#2a1a0e"), width=2 if s >= 1.2 else 1)
            if s >= 1.2:
                d.line([X(dx), Y(5.6), X(uc), Y(uy)], fill=hex2("#9a7448"), width=1)
                d.line([X(uc), Y(uy), X(uc - 0.8), Y(uy - 1.2)], fill=hex2("#9a7448"), width=2)
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
    bx = x - int(2.2 * s) * yon
    d.rounded_rectangle([bx - int(1.6 * s), ust + int(0.2 * s), bx + int(1.6 * s), ust + int(4.2 * s)], radius=_u(0.8, s), fill=hex2(renk))
    d.line([bx - int(1.6 * s), ust + int(2.2 * s), bx + int(1.6 * s), ust + int(2.2 * s)], fill=hex2(_ac(renk, -0.3)))
    d.polygon([(bx - int(0.6 * s), ust + int(0.2 * s)), (bx, ust - int(0.8 * s)), (bx + int(0.6 * s), ust + int(0.2 * s))], fill=hex2(renk))
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
    L = 12 * s
    ux, uy = ex + L * 0.77 * yon, ey - L * 0.64 + SIN(f) * 0.3 * s
    bx, by = ex - 3 * s * 0.77 * yon, ey + 3 * s * 0.64
    d.line([bx, by, ux, uy], fill=hex2("#5a3a22"), width=_u(0.7, s))
    d.polygon([(ux, uy), (ux + 2.4 * s * 0.77 * yon, uy - 2.4 * s * 0.64), (ux + 0.4 * s * yon, uy + 0.9 * s)], fill=hex2("#c8ccd0"))


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


# ==========================================================================
# Paletler
# ==========================================================================
ALTIN_GOK = ["#4a3a6a", "#8a5a7a", "#c8786a", "#e89a6a", "#f4bc7a", "#f8d494"]
GUN = ["#3a78c0", "#5a90cc", "#7aa8d8", "#9cc0e2", "#bcd4ea", "#d8e6f0"]
SONBAHAR = ["#5a6a9a", "#7a86a8", "#a49cac", "#cfb4a4", "#e8c8a0", "#f2d8b0"]
AKSAM = ["#2a2a58", "#5a3a6a", "#a05a78", "#d88a7a", "#f0b088", "#f4c898"]
GECE = ["#070a1c", "#0e1430", "#162046", "#1e2c5a", "#28386a"]
KIS = ["#5a6478", "#6e7688", "#888c98", "#a2a2a8", "#b8b4b0"]
SIS = ["#8a96a8", "#a2acba", "#bac2cc", "#d0d4d8", "#e0e0dc"]
KIZIL_GOK = ["#2a1a3a", "#5a2a4a", "#9a3a4a", "#d0604a", "#ec8c4e", "#f4b070"]
DUMANLI = ["#3a2a2e", "#5a3a36", "#7a4a3a", "#9a5a42", "#b8704a", "#c8885a"]
MOR = ["#1e1e40", "#3a2e58", "#6a4268", "#9a5a6e", "#c07a70", "#d89a7c"]
BULUT_GUN = ("#ffffff", "#e8ecf0", "#c0c8d8")
BULUT_ALTIN = ("#fff4e4", "#f0d0b8", "#c8a0a0")
BULUT_KIS = ("#d8d8dc", "#b8b8c0", "#9898a4")

D_GUN = ("#3e74a8", "#33669a", "#2a5a8c", "#224e7e")
D_ALTIN = ("#7a6a8a", "#6a5e80", "#5a5272", "#4a4666")
D_AKSAM = ("#6a5a88", "#544c7a", "#44406c", "#38365e")
D_GECE = ("#1a2848", "#16223e", "#121c34", "#0e162a")
D_SIS = ("#7a8ca0", "#6a7e94", "#5e7288", "#52667c")
D_KIZIL = ("#6a3a4a", "#5a3242", "#4a2a3a", "#3e2232")
D_YAZ = ("#2a7ab0", "#2470a4", "#1e6698", "#185c8c")
D_KIS = ("#5a6a80", "#4e5e76", "#44546c", "#3a4a62")

OSMANLI = dict(govde="#3a2418", serit="#a8281e", tente="#a8281e", yelken="#efe6d0", flama="#c8302a")
FRANSIZ = dict(govde="#2a2a3a", serit="#2a4a9a", tente="#2a4a9a", yelken="#e8e4dc", flama="#2a4aa8")

FARON = ("#7a8a7a", "#6a7a6c")          # Faron: gri-yeşil kireçtaşı sırt
KARA = ("#b8a07a", "#a89070", "#988064")


def _toulon(s=0.75, katedral_x=300, isik=False, x0=110, x1=470):
    """Uzak plandaki Toulon: kıyı şeridine oturan evler ve katedralin çan kulesi."""
    def ciz(t, z):
        katedral(t, katedral_x, z, round(s * 0.55, 2), isik=isik)
        provence_evleri(t, x0, katedral_x - 14, z, s, tohum=7, isik=isik)
        provence_evleri(t, katedral_x + 14, x1, z, s, tohum=8, isik=isik)
    return ciz


def _gemi_sp(no, f, gemiler, renkler, deniz_ust, band_y=None):
    """Deniz sprite'ı: gemiler [(x_yerel, su_yerel, s, yon, mod, renk_dict, ek)] uzaktan yakına; altta su bandı."""
    def kare(t, z, i):
        fz = i / KARE
        b = P(no)
        for k, (gx, gsu, gs, gyon, gmod, gk, ek) in enumerate(gemiler):     # uzaktan yakına: her geminin altı kendi suyunda
            kadirga(t, gx, gsu, gs, gyon, (fz + gx * 0.003) % 1, mod=gmod, **gk, **ek)
            _su_bandi(t, gsu - 2, b["taban"] - b["h"], renkler,
                      deniz_ust, fz, no + k)
    return kare


# ==========================================================================
# 450 · KAPAK + kart 1-2 · Toulon koyu: Barbaros'un kadırgası koya girer
# ==========================================================================
def sahne450():
    _gok(450, ALTIN_GOK, [(110, 404, 20), (430, 408, 18)], BULUT_ALTIN)
    _uzak_kiyi(450, FARON, ("#9a8a6a", "#8a7a5e"), KARA, D_ALTIN, 542, dag_y=(452, 500), tepe_y=520, kasaba=_toulon())
    _orta_deniz(450, 556, D_ALTIN, ekle=lambda img: [kadirga(img, PAY + x, 568 + k * 4, 0.45 + k * 0.08, 1, 0.0, mod="indik",
                                                           kurek=False, **OSMANLI) for k, x in enumerate((-60, 40, 470, 560))])
    _bos_on(450)
    b = P(450)
    _spr(450, _gemi_sp(450, 0, [(198, b["h"] - 14, 1.7, 1, "sarili", OSMANLI, dict(fener=3))], D_ALTIN, 556))


# ==========================================================================
# 451 · kart 3 · Barbaros kadırgasının güvertesinde
# ==========================================================================
def sahne451():
    _gok(451, GUN, [(120, 404, 22), (400, 400, 20)], BULUT_GUN)
    _uzak_kiyi(451, None, ("#8a9aa8", "#7c8c9c"), ("#8a9aa8", "#7c8c9c", "#6e7e90"), D_GUN, 548, tepe_y=536, kara_kalin=4)
    _guverte(451)
    _bos_on(451)
    K = K_(451)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 150, z, K, **BARBAROS, yon=1, kol=0.45 + 0.04 * SIN(f))
        figur(t, kisi, 262, z, round(0.97 * K, 1), **LEVEND_B, yon=-1, kol=0.03 * (1 + SIN(f + 0.4)))

    _spr(451, kare)


# ==========================================================================
# 452 · kart 4 · açık denizde kadırga; arkada başka kadırgalar
# ==========================================================================
def sahne452():
    _gok(452, GUN, [(100, 402, 22), (420, 406, 20)], BULUT_GUN)
    _uzak_kiyi(452, None, ("#8aa0b4", "#7c92a8"), ("#8aa0b4", "#7c92a8", "#6e84a0"), D_YAZ, 546, tepe_y=538, kara_kalin=3)
    _orta_deniz(452, 556, D_YAZ, ekle=lambda img: [kadirga(img, PAY + x, su, s_, 1, 0.0, mod="acik", kurek=True, kurekci=False,
                                                          **OSMANLI) for x, su, s_ in ((185, 563, 0.42), (395, 566, 0.5))])
    _bos_on(452)
    b = P(452)
    _spr(452, _gemi_sp(452, 0, [(198, b["h"] - 14, 1.7, 1, "acik", OSMANLI, dict(fener=1))], D_YAZ, 556))


# ==========================================================================
# 453 · kart 5-6 · I. François sarayında
# ==========================================================================
def sahne453():
    ic_mekan(453, duvar=("#2a3458", "#34406a", "#425080"), kemer="#1a2038", cini="#c8a040",
             pencere=("#6a8ab8", "#7c9cc8"), zemin_renk=("#6a5a4a", "#5a4c3e", "#4a3e32"), isik="#f8d080", hali=True)
    K = K_(453)

    def kare(t, z, i):
        f = i / KARE
        if not _DENETIM[0]:
            kandil(t, 268, 0, f, zincir=_kz(P(453)["yk"]))
        figur(t, taht, 232, duz(z[0] - 12, t.width), round(0.55 * K, 1), renk="#e0b040", ortu="#2a3a8a")
        mumluk(t, 128, z, f, 3)
        figur(t, kisi, 178, z, K, **FRANCOIS, yon=1, kol=0.05 + 0.04 * (1 + SIN(f)))

    _spr(453, kare)


# ==========================================================================
# 454 · kart 7 · alacakaranlıkta Osmanlı ve Fransız kadırgası yan yana
# ==========================================================================
def sahne454():
    _gok(454, AKSAM, [(120, 404, 20), (420, 402, 22)], ("#f0c8b8", "#d09898", "#a07080"))
    _uzak_kiyi(454, None, ("#5a4a6a", "#4e4060"), ("#5a4a6a", "#4e4060", "#443a56"), D_AKSAM, 546, tepe_y=538, kara_kalin=3)
    _orta_deniz(454, 556, D_AKSAM)
    _bos_on(454)
    b = P(454)
    _spr(454, _gemi_sp(454, 0, [(236, b["h"] - 40, 0.95, 1, "sarili", FRANSIZ, dict(fener=1)),
                                (182, b["h"] - 10, 1.45, 1, "sarili", OSMANLI, dict(fener=3))], D_AKSAM, 556, band_y=b["h"] - 44))


# ==========================================================================
# 455 · kart 8-9 · Marsilya rıhtımı: Barbaros ve Kaptan Polin
# ==========================================================================
def sahne455():
    _gok(455, GUN, [(110, 404, 22), (430, 404, 20)], BULUT_GUN)
    _uzak_kiyi(455, ("#9aa0a8", "#8a909a"), ("#a8a08a", "#9a927e"), KARA, D_YAZ, 544, dag_y=(456, 500), tepe_y=522,
               kasaba=lambda t, z: [sehir(t, 120, 460, z, 0.8, duvar="#c8b898", golge="#9a8a72", cati="#b05a3a", tohum=455)])
    _orta_deniz(455, 556, D_YAZ, rihtim=600)
    _bos_on(455)
    K = K_(455)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 165, z, K, **POLIN, yon=1, kol=0.28 + 0.08 * SIN(f))
        figur(t, kisi, 236, z, K, **BARBAROS, yon=-1, kol=0.03 * (1 + SIN(f + 0.5)))

    _spr(455, kare)


# ==========================================================================
# 456 · kart 10 · Nice kuşatması   457 · kart 11 · aşağı şehir yanar, kale direnir
# ==========================================================================
def _nice_orta(no, renkler, kenar, kaya, cati, gece=False):
    damlar = []

    def ekle(img, z):
        zt = kaya_tepe(img, PAY + 215, PAY + 345, PAY + 238, PAY + 322, 592, 552, kaya, tohum=no)
        figur(img, anadolu_kalesi, PAY + 244, PAY + 316, zt, 0.75, tas=_ac(kaya[0], 0.1), golge=kaya[1])
        damlar.extend(figur(img, provence_evleri, PAY + 330, PAY + 700, duz(594), 1.25, tohum=no, cati=cati,
                            sivalar=(("#8a7a6a", "#7a6a5e", "#6a5e54") if gece else ("#e0c494", "#d8a878", "#ecd8b0")), kat=(2,)))
        damlar.extend(figur(img, provence_evleri, PAY - 60, PAY + 214, duz(594), 1.25, tohum=no + 1, cati=cati,
                            sivalar=(("#8a7a6a", "#7a6a5e", "#6a5e54") if gece else ("#e0c494", "#d8a878", "#ecd8b0")), kat=(2,)))
    orta(no, (562, 566), renkler, kenar, ekle=ekle)
    return damlar


def sahne456():
    _gok(456, DUMANLI[2:] + ["#d8a070"], [(120, 404, 20)], ("#e8c8a8", "#c8a088", "#a08070"))
    img = _uzak_kiyi(456, None, ("#8a7a6a", "#7c6c5e"), ("#8a7a6a", "#7c6c5e", "#6e6052"), D_ALTIN, 548, tepe_y=540,
                     kara_kalin=3, gemiler=[(205, 0.36, -1, "sarili", OSMANLI), (232, 0.32, -1, "sarili", OSMANLI),
                                            (352, 0.36, -1, "sarili", OSMANLI), (380, 0.32, -1, "sarili", OSMANLI)])
    for x in (191, 218, 338, 366):                                         # top dumanı (pruva topları)
        duman(img, x, 548, 22, x, faz=0.4, renk="#d8d0c4", ruzgar=0.4, genislik=1.2)
    kaydet(img, "sahne456-uzak.png")
    _nice_orta(456, ["#9a8a5a", "#8c7c50", "#7e6e46", "#70603e", "#625436"], "#c8b880", ("#a89a80", "#8a7e68", "#6a604e"), "#b05a3a")
    on(456, ["#625436", "#70603e", "#7e6e46"], "#c8b880", boy=90)
    _gorunur(456, [(238, 322)])
    K = K_(456, 0.30)

    def kare(t, z, i):
        f = i / KARE
        for j, (x, kk) in enumerate(((140, FR_ASKER), (178, FR_ASKER2), (216, FR_ASKER))):
            ad = (f + j * 0.37) % 1
            figur(t, kisi, x, z, K, **kk, yon=1, adim=ad)
            mizrak_omuz(t, x, z, K, 1, ad)

    _spr(456, kare)


def sahne457():
    _gok(457, KIZIL_GOK, [(110, 404, 20), (420, 402, 22)], ("#a85a4a", "#7a3a3a", "#5a2a30"))
    _uzak_kiyi(457, None, ("#4a2a3a", "#40243a"), ("#4a2a3a", "#40243a", "#3a2034"), D_KIZIL, 548, tepe_y=540, kara_kalin=3)
    damlar = _nice_orta(457, ["#4a3a3a", "#423232", "#3a2c2c", "#322626", "#2a2020"], "#8a5a4a",
                        ("#6a5a52", "#544840", "#3e3630"), "#5a2a22", gece=True)
    _bos_on(457)
    _gorunur(457, [(238, 322)])
    b = P(457)
    sinir = _ust_sinir(457)
    ates = [(x - (b["xs"][0] - b["w"] // 2), 571 - (b["taban"] - b["h"])) for x in (184, 198, 212, 330, 344)]
    kale_x = _yerel(457, 280)
    kale_y = 552 - int(0.75 * 22) - (b["taban"] - b["h"])

    def kare(t, z, i):
        f = i / KARE
        for j, (x, y) in enumerate(ates):
            if 6 < x < b["w"] - 6:
                duman(t, x, y - 4, min(40, y + (b["taban"] - b["h"]) - sinir - 6), 457 + j, faz=(f + j * 0.27) % 1,
                      renk="#3a2a2a", ruzgar=0.3, genislik=1.3)
                yangin(t, x, y + 2, (f + j * 0.31) % 1, 1.6, tohum=j)
        d = ImageDraw.Draw(t)                                        # kalede Savoy sancağı (direk surun üstüne dikili)
        d.line([kale_x, kale_y, kale_x, kale_y - 16], fill=hex2("#3a2a1a"))
        for k in range(10):
            yy = kale_y - 16 + int(SIN(f + k / 10) * 1.2)
            d.line([kale_x + 1 + k, yy, kale_x + 1 + k, yy + 6], fill=hex2("#c8282a" if not 3 < k < 6 else "#f0f0f0"))
        d.line([kale_x + 1, kale_y - 13, kale_x + 10, kale_y - 13], fill=hex2("#f0f0f0"))
        tas_duvar(t, 0, b["w"] - 1, z, 3.0, tas="#4a4040", tohum=457)

    _spr(457, kare, esik=0.97)


# ==========================================================================
# 458 · kart 12 · Savoy ve del Vasto'nun zırhlı atlıları
# ==========================================================================
def sahne458():
    _gok(458, ["#6a7a98", "#8a94a8", "#aaaab0", "#c8bca8", "#dccaa8"], [(120, 404, 22), (420, 402, 20)], BULUT_KIS)
    uzak(458, ["#7a7a7e", "#6e6e74"], ["#8a8a6a", "#7c7c5e"], ["#9a9468", "#8c865c", "#7e7852"], dag_y=(440, 488), tepe_y=500, ova_y=520)
    orta(458, (560, 566), ["#a09460", "#928654", "#84784a", "#766a40", "#685e38"], "#c8bc88")
    on(458, ["#685e38", "#766a40", "#84784a"], "#c8bc88", boy=90)
    sa = 3.3

    def kare(t, z, i):
        f = i / KARE
        arka = duz(z[0] - 8, t.width)
        figur(t, atli, 230, arka, round(0.9 * sa, 1), -1, faz=(f + 0.5) % 1, at_renk="#3a2a22", yele="#1a120c", adim=0.55,
              zirh="#a8b0b8", cul="#2a3a6a", **dict(SAVOY, govde="#2a3a6a"))
        figur(t, atli, 170, z, sa, -1, faz=f, at_renk="#8a5a3a", yele="#2a1a12", adim=0.55, zirh="#b8c0c8", cul="#8a1e22", **SAVOY)
        for j in range(6):                                           # toynaklardan toz
            ph = (f + j / 6) % 1
            px_ = 170 + 20 + ph * 30 + j * 3
            piksel(t, px_, z[0] - 1 - int(ph * 8), hex2("#c8b890", int(200 * (1 - ph))))
            piksel(t, px_ + 1, z[0] - 2 - int(ph * 6), hex2("#d8c8a0", int(160 * (1 - ph))))

    _spr(458, kare)


# ==========================================================================
# 459 · kart 13 · sahildeki ordugâh; ufukta Doria
# ==========================================================================
def sahne459():
    _gok(459, ["#4a5a8a", "#6a6e98", "#9a88a0", "#c8a0a0", "#e0b8a0"], [(110, 404, 20), (420, 402, 22)], BULUT_ALTIN)
    _uzak_kiyi(459, None, ("#7a7088", "#6c647c"), ("#7a7088", "#6c647c", "#5e5870"), D_AKSAM, 536, tepe_y=528, kara_kalin=3,
               gemiler=[(326, 0.24, -1, "acik", FRANSIZ), (342, 0.26, -1, "acik", FRANSIZ), (358, 0.23, -1, "acik", FRANSIZ)])

    def ekle(img):
        d = ImageDraw.Draw(img)
        d.rectangle([0, 562, GW, H], fill=hex2("#c8b088"))
        for y in range(566, H, 9):
            for x in range((y // 9) % 2 * 7, GW, 14):
                piksel(img, x, y, hex2("#b09870"))
        d.line([0, 562, GW, 562], fill=hex2("#e8dcc0"))
        figur(img, otag, PAY + 268, duz(586), 1.0, "#2a6a3a", "#e0b040", faz=0.2)
    _orta_deniz(459, 548, D_AKSAM, ekle=ekle)
    _bos_on(459)
    _gorunur(459, [(246, 290)])
    K = K_(459)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 148, z, K, **BARBAROS, yon=1, kol=0.62 + 0.04 * SIN(f))
        figur(t, cuval, 212, z, round(0.6 * K, 1), "#2a6a3a")               # katlanmış çadır bezi
        figur(t, cuval, 238, z, round(0.5 * K, 1), "#c8302a")

    _spr(459, kare)


# ==========================================================================
# 460 · kart 14 · kadırga denize açılır (sola)
# ==========================================================================
def sahne460():
    _gok(460, AKSAM, [(110, 404, 20), (430, 402, 22)], ("#f0c8b8", "#d09898", "#a07080"))
    _uzak_kiyi(460, None, ("#5a4a6a", "#4e4060"), ("#5a4a6a", "#4e4060", "#443a56"), D_AKSAM, 546, tepe_y=532, kara_kalin=4)
    _orta_deniz(460, 556, D_AKSAM, ekle=lambda img: [kadirga(img, PAY + x, 570 + k * 5, 0.5 + k * 0.08, -1, 0.0, mod="sarili",
                                                            kurekci=False, **OSMANLI) for k, x in enumerate((-40, 560, 650))])
    _bos_on(460)
    b = P(460)
    _spr(460, _gemi_sp(460, 0, [(202, b["h"] - 14, 1.7, -1, "sarili", OSMANLI, dict(fener=3))], D_AKSAM, 556))


# ==========================================================================
# 461 · kart 15-16 · Toulon: Provence evleri, katedral, Faron
# ==========================================================================
def sahne461():
    _gok(461, SONBAHAR, [(110, 404, 22), (430, 406, 20)], BULUT_ALTIN)
    uzak(461, list(FARON), ["#8a9a7a", "#7c8c6e"], ["#9a9a7a", "#8c8c6e", "#7e7e62"], dag_y=(452, 504), tepe_y=520, ova_y=540)

    def ekle(img):
        figur(img, provence_evleri, -20, PAY + 238, duz(592), 1.6, tohum=461)
        figur(img, katedral, PAY + 270, duz(592), 1.25)
        figur(img, provence_evleri, PAY + 302, GW + 20, duz(592), 1.6, tohum=462)
    _orta_deniz(461, 596, D_GUN, kiyi=(556, ("#a89a80", "#9a8c72", "#8c7e66")), ekle=ekle)
    _bos_on(461)
    b = P(461)

    def kare(t, z, i):
        f = i / KARE
        _su_bandi(t, b["h"] - 22, b["taban"] - b["h"], D_GUN, 596, f, 461)
        figur(t, kayik, 160, b["h"] - 14, 3.0, 1, f)
        figur(t, kayik, 248, b["h"] - 8, 3.2, -1, (f + 0.4) % 1, govde="#5a6a7a", serit="#a8382a")

    _spr(461, kare)


# ==========================================================================
# 462 · kart 17-18 · münadi meydanda kralın emrini okur
# 474 · kart 33 · kış: memur vergi muafiyetini okur
# ==========================================================================
def _meydan(no, gok, bulut_renk, tas, ev_s=2.2, kapali=False, isik=False, sivalar=None, cati="#b05a3a", yildiz=0):
    _gok(no, gok, [(120, 404, 20), (420, 402, 22)], bulut_renk, yildiz=yildiz)
    uzak(no, ["#7a8090", "#6e7484"], ["#8a8a80", "#7c7c74"], ["#8a8478", "#7c766c", "#6e6860"], dag_y=(460, 500), tepe_y=520, ova_y=560)
    kw = dict(kapali=kapali, isik=isik, cati=cati)
    if sivalar:
        kw["sivalar"] = sivalar
    _orta_duz(no, 588, tas, ekle=lambda img, z: figur(img, provence_evleri, -30, GW + 30, z, ev_s, tohum=no, **kw))
    _bos_on(no)


TAS_GUN = ["#b8a888", "#ac9c7e", "#a09074", "#94846a", "#887860"]
TAS_KIS = ["#8a8680", "#7e7a74", "#726e68", "#66625c", "#5a5650"]
TAS_GECE = ["#4e4a54", "#46424c", "#3e3a44", "#36323c", "#2e2a34"]


def sahne462():
    _meydan(462, ["#7a8aa8", "#94a0b4", "#b0b4bc", "#cac4bc", "#dcd0bc"], BULUT_KIS, TAS_GUN)
    K = K_(462)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 136, z, K, **TOULONLU, yon=1)
        figur(t, basortulu, 168, z, round(0.95 * K, 1), "#7a3a3a", "#e8e0d0", 1)
        figur(t, cocuk, 196, z, round(0.62 * K, 1), "#5a6a3a", "#5a3a1e", 1)
        figur(t, kisi, 254, z, K, **MUNADI, yon=-1, silah="mektup", kol=0.42 + 0.04 * SIN(f))

    _spr(462, kare)


def sahne474():
    _meydan(474, KIS, BULUT_KIS, TAS_KIS, sivalar=("#c8b8a0", "#b8a890", "#d0c4b0", "#a89a88"), cati="#8a4a3a")
    K = K_(474)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 138, z, K, **TOULONLU, yon=1, kol=0.55 + 0.25 * SIN(f))
        figur(t, basortulu, 170, z, round(0.95 * K, 1), "#3a4a6a", "#ece6dc", 1)
        figur(t, kisi, 202, z, K, **TOULONLU2, yon=1, kol=0.35 + 0.2 * SIN(f + 0.4))
        figur(t, kisi, 254, z, K, **MEMUR, yon=-1, silah="mektup", kol=0.42 + 0.04 * SIN(f))

    _spr(474, kare)


# ==========================================================================
# 463 · kart 19-20 · şehir meclisi: konsüller ve tutanak
# ==========================================================================
def sahne463():
    ic_mekan(463, duvar=("#4a3a2a", "#5a4632", "#6a523c"), kemer="#2a1e14", cini="#8a2a2a",
             pencere=("#8aa0b8", "#9ab0c4"), zemin_renk=("#6a5a48", "#5a4c3c", "#4c4032"), isik="#f8c060", hali=False)
    K = K_(463)

    def kare(t, z, i):
        f = i / KARE
        if not _DENETIM[0]:
            kandil(t, 200, 0, f, zincir=_kz(P(463)["yk"]))
        figur(t, kisi, 138, z, K, **KONSUL2, yon=1, kol=0.05)
        figur(t, kisi, 174, z, K, **KONSUL, yon=1, kol=0.35 + 0.15 * SIN(f))
        figur(t, kilise_kursusu, 226, z, round(0.62 * K, 1), -1, f, True)
        figur(t, kisi, 258, z, K, **KATIP, yon=-1, kol=0.22 + 0.03 * SIN(f, 3))

    _spr(463, kare)


# ==========================================================================
# 464 · kart 21 · çocuklar ve kadınlar yola düşer; kapıda kalan erkek
# ==========================================================================
def sahne464():
    _gok(464, ["#4a4a6a", "#6a6480", "#8a7a8a", "#a8908e", "#bca094"], [(120, 404, 20), (420, 402, 22)], ("#c8b0b0", "#a89098", "#887080"))
    uzak(464, ["#5a5a6e", "#4e4e62"], ["#6a6a6a", "#5e5e60"], ["#6a6a5a", "#5e5e50", "#525246"], dag_y=(450, 494), tepe_y=512, ova_y=540)
    K = K_(464)

    def ekle(img, z):
        figur(img, sehir, PAY + 300, PAY + 760, duz(588), 1.6, duvar="#8a8274", golge="#5e584e", cati="#6a3a30", tohum=464)
        figur(img, kisi, PAY + 344, duz(592), round(0.7 * K, 1), **TOULONLU2, yon=-1)
    orta(464, (560, 566), ["#6a6a4a", "#5e5e42", "#52523a", "#464632", "#3a3a2a"], "#9a9a6a", ekle=ekle)
    on(464, ["#3a3a2a", "#464632", "#52523a"], "#8a8a5a", boy=80)

    def kare(t, z, i):
        f = i / KARE
        kisiler = ((134, "k", "#6a2a3a", "#e8e0d0"), (163, "c", "#3a5a6a", "#4a2e1a"), (190, "k", "#4a5a3a", "#d8d0c0"),
                   (219, "c", "#7a4a3a", "#6a3a1a"), (250, "k", "#5a3a5a", "#ece4d4"))
        for j, (x, tur, g, r) in enumerate(kisiler):
            ad = (f + j * 0.37) % 1
            if tur == "k":
                figur(t, basortulu, x, z, round(0.95 * K, 1), g, r, -1, adim=ad)
                figur(t, bohca, x, z, round(0.95 * K, 1), -1, "#8a6a4a" if j else "#6a5a7a")
            else:
                figur(t, cocuk, x, z, round(0.62 * K, 1), g, r, -1, ad, kiz=j == 3)

    _spr(464, kare)


# ==========================================================================
# 465 · kart 22 · boş sokak; kapısında tek başına bir adam
# ==========================================================================
def sahne465():
    _meydan(465, ["#141a3a", "#1e2650", "#2a3466", "#3a4478", "#4a5288"], ("#3a4478", "#2e3866", "#242c54"), TAS_GECE,
            kapali=True, sivalar=("#8a8090", "#7a7084", "#9a90a0", "#6e6678"), cati="#5a3a44", yildiz=40)
    K = K_(465)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kuyu, 140, z, round(0.55 * K, 1), "#6a6470")
        sokak_feneri(t, 210, z, round(0.55 * K, 1), f)
        figur(t, kisi, 268, z, K, **TOULONLU2, yon=-1)

    _spr(465, kare)


# ==========================================================================
# 466 · kart 23 · sabah pusu: kadırgalar sıra hâlinde koya girer
# ==========================================================================
def sahne466():
    _gok(466, SIS, [(120, 404, 24), (410, 400, 22)], ("#f0f0f0", "#dcdee2", "#c4c8d0"))
    _uzak_kiyi(466, ("#9aa4ac", "#8e98a2"), ("#a8aea8", "#9aa29c"), ("#b0aa98", "#a49e8c", "#98927e"), D_SIS, 544,
               dag_y=(456, 504), tepe_y=524, kasaba=_toulon())
    _orta_deniz(466, 556, D_SIS)
    _bos_on(466)
    b = P(466)
    _spr(466, _gemi_sp(466, 0, [(240, b["h"] - 44, 0.9, 1, "sarili", OSMANLI, {}),
                                (184, b["h"] - 10, 1.5, 1, "sarili", OSMANLI, dict(fener=3))], D_SIS, 556, band_y=b["h"] - 48))


# ==========================================================================
# 467 · kart 24 · rıhtımda sarıklılar ve Fransız tanık
# ==========================================================================
def sahne467():
    _gok(467, GUN, [(120, 404, 22), (410, 400, 20)], BULUT_GUN)
    _uzak_kiyi(467, FARON, ("#9a8a6a", "#8a7a5e"), KARA, D_GUN, 544, dag_y=(460, 506), tepe_y=524, kasaba=_toulon())
    _orta_deniz(467, 556, D_GUN, rihtim=600)
    _bos_on(467)
    K = K_(467)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 140, z, K, **TANIK, yon=1, kol=0.12 + 0.03 * SIN(f))
        figur(t, fici, 182, z, round(0.5 * K, 1))
        figur(t, kisi, 212, z, K, **LEVEND_A, yon=-1, kol=0.03 * (1 + SIN(f)))
        figur(t, kisi, 256, z, round(0.97 * K, 1), **LEVEND_C, yon=-1, kol=0.25 + 0.05 * SIN(f + 0.3))

    _spr(467, kare)


# ==========================================================================
# 468 · kart 25 · koy kadırgalarla dolu: Küçük Konstantinopolis
# ==========================================================================
def sahne468():
    _gok(468, ALTIN_GOK, [(100, 404, 20), (440, 406, 18)], BULUT_ALTIN)
    _uzak_kiyi(468, FARON, ("#9a8a6a", "#8a7a5e"), KARA, D_ALTIN, 542, dag_y=(452, 500), tepe_y=520, kasaba=_toulon())

    def ekle(img):
        for sira, (su, s_, ara) in enumerate(((562, 0.36, 30), (571, 0.48, 40), (582, 0.62, 52))):
            for x in range(-20 + sira * 13, GW + 20, ara):
                kadirga(img, x, su, s_, 1 if (x // ara) % 3 else -1, 0.0, mod="indik", kurek=False, kontur=sira > 0, **OSMANLI)
    _orta_deniz(468, 556, D_ALTIN, ekle=ekle)
    _bos_on(468)
    b = P(468)
    gem = [(200, b["h"] - 12, 1.4, 1, "indik", OSMANLI, dict(fener=3, kurek=False))]
    gk = _gemi_sp(468, 0, gem, D_ALTIN, 556)
    sinir = _ust_sinir(468)

    def kare(t, z, i):
        gk(t, z, i)
        su_w = b["taban"] - 12 + b["taban"] - b["h"] - (b["taban"] - b["h"])
        duman(t, 200 - 40, b["h"] - 30, min(36, b["taban"] - 30 - sinir - 8), 468, faz=i / KARE, renk="#d8d0c4", ruzgar=0.4)

    _spr(468, kare)


# ==========================================================================
# 469 · kart 26-27 · kış gecesi: katedralin cephesi
# ==========================================================================
def sahne469():
    _gok(469, GECE, [(130, 404, 18)], ("#3a4a6a", "#2a3a5a", "#1e2a46"), yildiz=90)
    uzak(469, ["#1a2240", "#151c38"], ["#1e2846", "#18203e"], ["#1c2638", "#161e30", "#121a28"], dag_y=(456, 500), tepe_y=520, ova_y=560)
    _orta_duz(469, 588, TAS_GECE, ekle=lambda img, z: figur(img, provence_evleri, -30, GW + 30, z, 1.9, tohum=469, isik=True,
                                                            sivalar=("#6a6478", "#5e586c", "#76708a"), cati="#4a3040"))
    _bos_on(469)

    def kare(t, z, i):
        f = i / KARE
        figur(t, katedral, 186, z, 1.9, "#8a8698", "#5a3a3a", True)
        sokak_feneri(t, 262, z, 3.0, f)

    _spr(469, kare)


# ==========================================================================
# 470 · kart 28 · 19. yüzyıl tarihçisi
# ==========================================================================
def sahne470():
    ic_mekan(470, duvar=("#2e2a24", "#3a342c", "#463e34"), kemer="#1a1612", cini="#5a4a2a",
             pencere=("#1a2440", "#c8d0e0"), zemin_renk=("#4a3e32", "#3e342a", "#322a22"), isik="#f8c060", hali=False)
    K = K_(470)

    def kare(t, z, i):
        f = i / KARE
        if not _DENETIM[0]:
            kandil(t, 140, 0, f, zincir=_kz(P(470)["yk"]))
        mumluk(t, 150, z, f, 2)
        for k, x in enumerate((236, 262)):
            kitaplar(t, x, z[0], round(0.7 * K, 1))
            kitaplar(t, x, z[0] - int(4.5 * K * 0.7), round(0.6 * K, 1))
        figur(t, avrupali, 196, z, K, "#2a2a34", "#a8a49c", "#a8a49c", 1, "mektup", 0.32 + 0.04 * SIN(f))

    _spr(470, kare)


# ==========================================================================
# 471 · kart 29 · katedral içi: defter   472 · kart 30 · vaftiz
# ==========================================================================
KILISE = dict(duvar=("#4a4a52", "#5a5a62", "#6a6a72"), kemer="#2a2a32", cini="#6a2a2a",
              pencere=("#3a4a7a", "#e8e0c0"), zemin_renk=("#5a5650", "#4c4844", "#403c38"), isik="#f8c060", hali=False)


def sahne471():
    ic_mekan(471, **KILISE)
    K = K_(471)

    def kare(t, z, i):
        f = i / KARE
        if not _DENETIM[0]:
            kandil(t, 270, 0, f, zincir=_kz(P(471)["yk"]))
        mumluk(t, 128, z, f, 3)
        figur(t, rahip, 180, z, K, "#1e1e24", None, 1, 0.22 + 0.04 * SIN(f, 3))
        figur(t, kilise_kursusu, 210, z, round(0.62 * K, 1), 1, f, True)
        mumluk(t, 266, z, (f + 0.5) % 1, 3)

    _spr(471, kare)


def sahne472():
    ic_mekan(472, **KILISE)
    K = K_(472)

    def kare(t, z, i):
        f = i / KARE
        if not _DENETIM[0]:
            kandil(t, 140, 0, f, zincir=_kz(P(472)["yk"]))
        figur(t, kisi, 136, z, K, **TOULONLU, yon=1)
        figur(t, basortulu, 166, z, round(0.95 * K, 1), "#3a5a7a", "#f0ece4", 1)
        figur(t, vaftiz_kurnasi, 204, z, round(0.55 * K, 1))
        kol = 0.4
        figur(t, rahip, 248, z, K, "#1e1e24", "#ece8e0", -1, kol, stol="#6a2a6a")
        ex, ey = _el(248, z, K, -1, kol)
        figur(t, kundak, ex - int(1 * K), ey - 1 + int(SIN(f) * 0.6), round(0.85 * K, 1), -1)

    _spr(472, kare)


# ==========================================================================
# 473 · kart 31-32 · kış sabahı pazar: ekmekçi ve levend
# ==========================================================================
def sahne473():
    _meydan(473, ["#7a8aa8", "#94a0b4", "#b0b4bc", "#cac4bc", "#dcd0bc"], BULUT_KIS, TAS_GUN, sivalar=("#e0c8a0", "#d4b088", "#e8d8b8"))
    K = K_(473)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 150, duz(z[0] - 10, t.width), round(0.95 * K, 1), **EKMEKCI, yon=1, kol=0.3 + 0.06 * SIN(f))
        figur(t, tezgah, 152, z, round(0.45 * K, 1), "ekmek", "#3a6a8a")
        figur(t, kisi, 214, z, K, **LEVEND_B, yon=-1, kol=0.32 + 0.04 * SIN(f + 0.3))
        figur(t, kisi, 256, z, K, **TOULONLU2, yon=-1, kol=0.02 * (1 + SIN(f)))

    _spr(473, kare)


# ==========================================================================
# 475 · kart 34-35 · rıhtım: altın, ipek, erzak, mühimmat
# ==========================================================================
def sahne475():
    _gok(475, GUN, [(110, 404, 22), (430, 404, 20)], BULUT_GUN)
    _uzak_kiyi(475, FARON, ("#9a8a6a", "#8a7a5e"), KARA, D_GUN, 544, dag_y=(460, 506), tepe_y=524, kasaba=_toulon())
    _orta_deniz(475, 556, D_GUN, rihtim=600)
    _bos_on(475)
    K = K_(475)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 138, z, K, **MEMUR, yon=1, kol=0.3 + 0.05 * SIN(f))
        figur(t, altin_sandigi, 176, z, round(0.55 * K, 1), f)
        figur(t, ipek_toplari, 207, z, round(0.45 * K, 1))
        figur(t, cuval, 230, z, round(0.5 * K, 1))
        figur(t, kisi, 258, z, K, **BARBAROS, yon=-1, kol=0.03 * (1 + SIN(f + 0.5)))

    _spr(475, kare)


# ==========================================================================
# 476 · kart 36 · Mayıs 1544: kadırga eve yol alır (yelkenler açık)
# ==========================================================================
def sahne476():
    _gok(476, ["#5a8ac8", "#78a2d4", "#98b8dc", "#b8cce0", "#d4dce0"], [(100, 402, 22), (420, 404, 24)], BULUT_GUN)
    _uzak_kiyi(476, ("#8a9a8a", "#7c8c7e"), ("#9aa080", "#8c9274"), KARA, D_YAZ, 546, dag_y=(470, 510), tepe_y=528,
               kasaba=_toulon(0.5, 260, x0=200, x1=330))
    _orta_deniz(476, 556, D_YAZ, ekle=lambda img: [kadirga(img, PAY + x, 568 + k * 6, 0.5 + k * 0.08, -1, 0.0, mod="acik",
                                                          kurekci=False, **(FRANSIZ if k == 1 else OSMANLI)) for k, x in enumerate((-50, 560, 640))])
    _bos_on(476)
    b = P(476)
    _spr(476, _gemi_sp(476, 0, [(202, b["h"] - 14, 1.7, -1, "acik", OSMANLI, dict(fener=3))], D_YAZ, 556))


# ==========================================================================
# 477 · kart 37-38 · Fransız kadırgasının güvertesinde rahip Maurand çizer
# ==========================================================================
def sahne477():
    _gok(477, GUN, [(120, 404, 22), (410, 400, 20)], BULUT_GUN)
    _uzak_kiyi(477, ("#8a9aa8", "#7c8c9c"), ("#9aa49a", "#8c968c"), KARA, D_YAZ, 548, dag_y=(490, 520), tepe_y=534,
               kasaba=_toulon(0.4, 380, x0=330, x1=440), kara_kalin=5)
    _guverte(477, ahsap="#6a5a4a")
    _bos_on(477)
    K = K_(477)

    def kare(t, z, i):
        f = i / KARE
        kol = 0.3
        figur(t, rahip, 190, z, K, "#1e1e24", None, 1, kol, "mektup", sapka=True)
        ex, ey = _el(190, z, K, 1, kol)
        d = ImageDraw.Draw(t)
        ux = ex + int((0.4 + 0.5 * SIN(f, 2)) * K * 0.5)
        d.line([ux, ey - int(0.6 * K), ux + int(0.6 * K), ey - int(2.2 * K)], fill=hex2("#2a1a10"))   # kalem
        figur(t, fici, 266, z, round(0.5 * K, 1), "#6a4a2a")

    _spr(477, kare)


# ==========================================================================
# Kuşbakışı masa sahneleri: 478 harita, 481 kronikler, 485 minyatür
# ==========================================================================
HX0, HY0, HW, HH = 108, 140, 184, 159       # kâğıdın sprite içindeki yeri (görünür aralık ve yazı bandının altı)


def _kagit(t, x0, y0, w, h, renk="#d8bc8c"):
    d = ImageDraw.Draw(t)
    d.rectangle([x0 + 2, y0 + 2, x0 + w, y0 + h], fill=hex2("#000000", 60))
    d.rectangle([x0, y0, x0 + w - 2, y0 + h - 2 if y0 + h < t.height else t.height - 1], fill=hex2(renk))
    rnd = random.Random(x0 * 7 + y0)
    for _ in range(w * h // 30):
        px_, py_ = rnd.randrange(x0, x0 + w - 2), rnd.randrange(y0, min(t.height, y0 + h - 2))
        piksel(t, px_, py_, hex2(_ac(renk, rnd.choice((-0.08, 0.06)))))
    d.rectangle([x0, y0, x0 + w - 2, min(t.height - 1, y0 + h - 2)], outline=hex2(_ac(renk, -0.3)))


def harita(t, f):
    """Yeni figür: masaya yatan portolan deniz haritası: Provence, Korsika, Sardunya, İtalya, Sicilya; pusula gülü ve
    kerte hatları; rota noktaları f ile ilerler, geçilen dört yerde ve Lipari'de alev işareti yanar."""
    x0, y0, w, h = HX0, HY0, HW, HH + 1
    _kagit(t, x0, y0, w, h)
    d = ImageDraw.Draw(t)
    U = lambda u, v: (x0 + u * w, y0 + v * h)  # noqa: E731
    pu = U(0.3, 0.72)
    kl = yeni(t.width, t.height)
    dk = ImageDraw.Draw(kl)
    for a in range(0, 360, 22):                                         # kerte hatları (kâğıda kırpılır)
        dk.line([pu, (pu[0] + math.cos(math.radians(a)) * 220, pu[1] + math.sin(math.radians(a)) * 220)], fill=hex2("#c8a878"))
    maske = Image.new("L", t.size, 0)
    ImageDraw.Draw(maske).rectangle([x0 + 1, y0 + 1, x0 + w - 3, min(t.height - 1, y0 + h - 3)], fill=255)
    kl.putalpha(Image.composite(kl.getchannel("A"), Image.new("L", t.size, 0), maske))
    t.alpha_composite(kl)
    _kagit_kenar = [x0, y0, x0 + w - 2, y0 + h - 2]
    kara = "#b8a070"
    for poly in ([(0, 0), (0.4, 0), (0.38, 0.1), (0.24, 0.12), (0.1, 0.16), (0, 0.15)],
                 [(0.44, 0), (1, 0), (1, 0.62), (0.93, 0.7), (0.84, 0.66), (0.76, 0.56), (0.66, 0.46), (0.56, 0.32),
                  (0.49, 0.2), (0.45, 0.1)],
                 [(0.62, 0.86), (0.96, 0.82), (0.84, 0.99), (0.66, 0.96)]):
        d.polygon([U(u, v) for u, v in poly], fill=hex2(kara), outline=hex2("#6a4a2a"))
    for cx, cy, rx, ry in ((0.31, 0.3, 0.035, 0.07), (0.28, 0.52, 0.05, 0.09), (0.47, 0.33, 0.012, 0.012),
                           (0.71, 0.56, 0.014, 0.012), (0.79, 0.78, 0.012, 0.01), (0.83, 0.76, 0.01, 0.01)):
        a_, b_ = U(cx - rx, cy - ry), U(cx + rx, cy + ry)
        d.ellipse([*a_, *b_], fill=hex2(kara), outline=hex2("#6a4a2a"))
    d.ellipse([pu[0] - 7, pu[1] - 7, pu[0] + 7, pu[1] + 7], outline=hex2("#8a2a2a"))   # pusula gülü
    for a in range(0, 360, 90):
        d.polygon([pu, (pu[0] + math.cos(math.radians(a + 10)) * 3, pu[1] + math.sin(math.radians(a + 10)) * 3),
                   (pu[0] + math.cos(math.radians(a)) * 9, pu[1] + math.sin(math.radians(a)) * 9)], fill=hex2("#8a2a2a"))
    rota = [(0.14, 0.15), (0.36, 0.2), (0.5, 0.27), (0.53, 0.3), (0.48, 0.34), (0.6, 0.46), (0.7, 0.55), (0.72, 0.68),
            (0.79, 0.77)]
    yerler = {2: 0, 3: 1, 4: 2, 6: 3, 8: 4}
    pts = []
    for (a, b), (c, e) in zip(rota, rota[1:]):
        n = int(math.hypot((c - a) * w, (e - b) * h) / 3) + 1
        pts += [(a + (c - a) * k / n, b + (e - b) * k / n) for k in range(n)]
    ilerle = min(1.0, f * 1.15)
    son = int(ilerle * (len(pts) - 1))
    for k in range(0, son, 2):
        px_, py_ = U(*pts[k])
        d.rectangle([px_, py_, px_ + 1, py_], fill=hex2("#7a1e12"))
    gx, gy = U(*pts[son])                                               # rota başında küçük kadırga işareti
    d.polygon([(gx - 4, gy - 1), (gx + 4, gy - 1), (gx + 3, gy + 1), (gx - 3, gy + 1)], fill=hex2("#3a2418"))
    d.line([gx, gy - 1, gx, gy - 6], fill=hex2("#3a2418"))
    d.polygon([(gx, gy - 6), (gx + 3, gy - 3), (gx, gy - 2)], fill=hex2("#efe6d0"))
    d.ellipse([*U(0.13, 0.14), *U(0.15, 0.16)], fill=hex2("#2a4a8a"))   # Toulon
    for ri, k in yerler.items():
        ux, uy = U(*rota[ri])
        gecti = son >= sum(1 for _ in pts[:1]) and U(*pts[son])[1] >= uy - 1 and ilerle * len(rota) >= ri
        d.ellipse([ux - 2, uy - 2, ux + 2, uy + 2], fill=hex2("#7a1e12"))
        if gecti:
            yangin(t, ux, uy + 1, (f * 3 + k * 0.3) % 1, 0.7, tohum=k)


def kronik(t, x0, y0, w, h, sayi, renk="#e8dcc0", kapak="#5a2a1a", f=0.0):
    """Yeni figür: masada açık duran kronik (kuşbakışı): deri kapak, iki sayfa, yazı satırları; sağ sayfada büyük sayı."""
    d = ImageDraw.Draw(t)
    d.rectangle([x0 - 2, y0 - 2, x0 + w + 2, y0 + h + 2], fill=hex2(kapak))
    d.rectangle([x0, y0, x0 + w // 2 - 1, y0 + h], fill=hex2(renk))
    d.rectangle([x0 + w // 2 + 1, y0, x0 + w, y0 + h], fill=hex2(_ac(renk, -0.05)))
    d.line([x0 + w // 2, y0, x0 + w // 2, y0 + h], fill=hex2(_ac(renk, -0.4)))
    rnd = random.Random(x0)
    for yy in range(y0 + 5, y0 + h - 3, 4):
        for xa, xb in ((x0 + 4, x0 + w // 2 - 4), (x0 + w // 2 + 4, x0 + w - 4)):
            if xa > x0 + w // 2 and yy > y0 + h // 2 - 10 and yy < y0 + h // 2 + 12:
                continue
            xx = xa
            while xx < xb:
                L = rnd.randint(2, 7)
                d.line([xx, yy, min(xb, xx + L), yy], fill=hex2("#5a4a3a"))
                xx += L + 2
    ol = 2
    gen = len(sayi) * 4 * ol
    _rakam(t, x0 + w * 3 // 4 - gen // 2, y0 + h // 2 - 5, sayi, "#8a1e12", ol)


def sahne478():
    _masa_ustu(478, "#6a4426")

    def kare(t, z, i):
        harita(t, i / KARE)

    _spr(478, kare, orta_bant=False)


def sahne481():
    _masa_ustu(481, "#5a3a22")

    def kare(t, z, i):
        f = i / KARE
        kronik(t, 112, 146, 86, 70, "8000")
        kronik(t, 206, 150, 86, 70, "11000", renk="#e0d4b8", kapak="#2a3a4a")
        _kagit(t, 150, 236, 100, 64, renk="#f0ece0")
        dd = ImageDraw.Draw(t)
        for yy in range(244, 296, 6):
            dd.line([156, yy, 244, yy], fill=hex2("#b8c8d8"))
        _rakam(t, 170, 258, "4000", "#2a3a6a", 3)
        dd.line([246, 290 - int(SIN(f) * 2), 266, 270 - int(SIN(f) * 2)], fill=hex2("#f0f0f0"), width=2)  # tüy kalem
        dd.line([246, 290 - int(SIN(f) * 2), 248, 288 - int(SIN(f) * 2)], fill=hex2("#2a1a10"))

    _spr(481, kare, orta_bant=False)


def minyatur(t, f):
    """Yeni figür: açık yazma (kuşbakışı): sol sayfada satırlar, sağ sayfada altın çerçeveli Toulon minyatürü
    (Matrakçı üslubunda düz perspektif: koyda sıra sıra kadırgalar, surlu kent, yeşil tepeler)."""
    x0, y0, w, h = HX0, HY0, HW, HH + 1
    d = ImageDraw.Draw(t)
    d.rectangle([x0 - 3, y0 - 3, x0 + w + 3, min(t.height - 1, y0 + h + 3)], fill=hex2("#6a2a1a"))
    sayfa = "#efe2c0"
    d.rectangle([x0, y0, x0 + w // 2 - 1, t.height - 1], fill=hex2(sayfa))
    d.rectangle([x0 + w // 2 + 1, y0, x0 + w, t.height - 1], fill=hex2(_ac(sayfa, -0.04)))
    d.line([x0 + w // 2, y0, x0 + w // 2, t.height - 1], fill=hex2("#8a6a4a"))
    rnd = random.Random(1608)
    for yy in range(y0 + 10, y0 + h - 8, 6):                            # sol sayfa: sağdan sola satırlar
        xx = x0 + w // 2 - 8
        while xx > x0 + 8:
            L = rnd.randint(3, 9)
            for k in range(L):
                piksel(t, xx - k, yy + int(math.sin((xx - k) * 0.9) * 1.2), hex2("#2a1a10"))
            xx -= L + 2
    d.rectangle([x0 + 6, y0 + 6, x0 + w // 2 - 6, y0 + h - 6], outline=hex2("#c8302a"))
    mx0, my0, mx1, my1 = x0 + w // 2 + 6, y0 + 6, x0 + w - 6, y0 + h - 6
    d.rectangle([mx0 - 2, my0 - 2, mx1 + 2, my1 + 2], fill=hex2("#d8a840"))
    d.rectangle([mx0, my0, mx1, my1], fill=hex2("#3a8a9a"))            # deniz (yeşil-mavi)
    for yy in range(my0 + 2, my1, 4):
        for xx in range(mx0 + (yy // 4) % 2 * 3, mx1, 6):
            d.line([xx, yy, xx + 2, yy - 1], fill=hex2("#6ab0b8"))
    d.polygon([(mx0, my0), (mx1, my0), (mx1, my0 + 40), (mx0, my0 + 30)], fill=hex2("#8aa84a"))   # tepeler
    for k in range(6):
        cx = mx0 + 6 + k * 14
        d.ellipse([cx - 6, my0 + 4 + (k % 2) * 4, cx + 6, my0 + 18 + (k % 2) * 4], fill=hex2("#5a8a3a"))
    d.rectangle([mx0 + 8, my0 + 22, mx1 - 8, my0 + 44], fill=hex2("#e8d8b0"))                     # surlu kent
    for xx in range(mx0 + 8, mx1 - 8, 4):
        d.rectangle([xx, my0 + 20, xx + 1, my0 + 22], fill=hex2("#e8d8b0"))
    for k in range(8):
        hx = mx0 + 12 + k * 9
        d.rectangle([hx, my0 + 28 + (k % 3) * 4, hx + 6, my0 + 34 + (k % 3) * 4], fill=hex2("#f4ecd8"))
        d.polygon([(hx - 1, my0 + 28 + (k % 3) * 4), (hx + 3, my0 + 25 + (k % 3) * 4), (hx + 7, my0 + 28 + (k % 3) * 4)],
                  fill=hex2("#c8402a"))
    for sira in range(5):                                               # kadırgalar
        for k in range(5):
            gx = mx0 + 8 + k * 16 + (sira % 2) * 8
            gy = my0 + 56 + sira * 18
            if gy > my1 - 6:
                continue
            d.polygon([(gx - 6, gy), (gx + 6, gy), (gx + 4, gy + 3), (gx - 4, gy + 3)], fill=hex2("#2a1a10"))
            d.line([gx, gy, gx, gy - 7], fill=hex2("#2a1a10"))
            d.line([gx - 4, gy - 3, gx + 3, gy - 7], fill=hex2("#c8302a"))
            for j in range(-5, 6, 2):
                piksel(t, gx + j, gy + 4, hex2("#2a1a10"))
    for k in range(10):                                                 # altın çerçevede parıltı
        ph = (f + k / 10) % 1
        if ph < 0.12:
            px_ = mx0 - 2 + int((mx1 - mx0 + 4) * (k / 10))
            piksel(t, px_, my0 - 2, hex2("#fff8d0"))
            piksel(t, px_, my1 + 2, hex2("#fff8d0"))


def sahne485():
    _masa_ustu(485, "#5a3a22")

    def kare(t, z, i):
        minyatur(t, i / KARE)

    _spr(485, kare, orta_bant=False)


# ==========================================================================
# 479 · kart 41 · Lipari   480 · kart 42 yanan Lipari   483 · kart 47 sessiz alacakaranlık
# ==========================================================================
def _lipari(no, gok, bulut_renk, kara, su, kaya, gece=False, yildiz=0):
    _gok(no, gok, [(110, 404, 20), (430, 402, 22)], bulut_renk, yildiz=yildiz)
    img = _uzak_kiyi(no, None, None, kara, su, 546, kara_kalin=2)

    def vulkan(t):
        d = ImageDraw.Draw(t)
        for cx, r, hh in ((120, 46, 30), (420, 30, 18)):
            d.polygon([(cx - r, 546), (cx - 8, 546 - hh), (cx + 8, 546 - hh), (cx + r, 546)], fill=hex2(_ac(kara[0], -0.1)))
            d.line([cx - 8, 546 - hh, cx + 8, 546 - hh], fill=hex2(_ac(kara[0], 0.2)))
    _sarili(img, vulkan)
    kaydet(img, f"sahne{no}-uzak.png")
    sonuc = {}

    def ekle(img, z):
        zt = kaya_tepe(img, PAY + 196, PAY + 352, PAY + 214, PAY + 334, 594, 556, kaya, tohum=no)
        katedral(img, PAY + 300, zt, 0.8, tas=_ac(kaya[0], 0.15), cati="#7a4a3a" if gece else "#a0583a")
        sonuc["sur"] = figur(img, anadolu_kalesi, PAY + 218, PAY + 330, zt, 0.5, tas=_ac(kaya[0], 0.1), golge=kaya[1])
        for a_, b_, tt in ((-40, PAY + 196, no), (PAY + 352, GW + 40, no + 1)):
            figur(img, provence_evleri, a_, b_, duz(596), 1.2, tohum=tt, kat=(2,), cati="#7a4a3a" if gece else "#b05a3a",
                  sivalar=("#9a8a7a", "#8a7a6c") if gece else ("#ece0c8", "#e0d0b0", "#d8c4a0"))
    renk = (["#5a4a3a", "#504234", "#463a2e", "#3c3228", "#322a22"] if gece
            else ["#9a8a5a", "#8c7c50", "#7e6e46", "#70603e", "#625436"])
    orta(no, (564, 568), renk, _ac(renk[0], 0.3), ekle=ekle)
    on(no, renk[::-1][:3], _ac(renk[0], 0.3), boy=70)
    _gorunur(no, [(214, 334)])
    return sonuc


def _zeytin(t, z, f, gece=False):
    figur(t, agac, 140, z, 0.8, ("#3a4a3a", "#4a5a44", "#5a6a50") if gece else ("#5a6a4a", "#6a7a5a", "#8a9a6e"),
          "#4a3a2a", 479, 0.4 * SIN(f))


def sahne479():
    _lipari(479, GUN, BULUT_GUN, ("#7a8a9a", "#6c7c8c"), D_YAZ, ("#a89a86", "#8a7e6c", "#6a6050"))

    def kare(t, z, i):
        f = i / KARE
        tas_duvar(t, 0, P(479)["w"] - 1, z, 3.0, tas="#9a8e7a", tohum=479)
        _zeytin(t, z, f)

    _spr(479, kare)


def _kale_atesleri(no, n=5):
    b = P(no)
    ofs = b["xs"][0] - b["w"] // 2
    return [(x - ofs, 556 - 11 - (b["taban"] - b["h"])) for x in range(226, 330, 104 // n)]


def sahne480():
    _lipari(480, KIZIL_GOK, ("#a85a4a", "#7a3a3a", "#5a2a30"), ("#4a2a3a", "#40243a"), D_KIZIL,
            ("#6a5a52", "#544840", "#3e3630"), gece=True)
    b = P(480)
    sinir = _ust_sinir(480)
    noktalar = _kale_atesleri(480)
    K = K_(480, 0.30)
    kk = round(0.62 * K, 1)

    def kare(t, z, i):
        f = i / KARE
        for j, (x, y) in enumerate(noktalar):
            duman(t, x, y - 3, max(8, min(40, y + b["taban"] - b["h"] - sinir - 6)), 480 + j, faz=(f + j * 0.23) % 1,
                  renk="#3a2a2a", ruzgar=0.3, genislik=1.2)
            yangin(t, x, y + 1, (f + j * 0.29) % 1, 1.1, tohum=j)
        arka = duz(z[0] - 16, t.width)
        renk = ("#6a4a3a", "#4a4a5a", "#7a3a3a", "#5a5a3a", "#3a4a5a")
        for j, x in enumerate((150, 172, 194, 216, 238)):
            if j % 2:
                figur(t, basortulu, x, arka, kk, renk[j], "#d8d0c0", -1)
            else:
                figur(t, kisi, x, arka, kk, govde=renk[j], bas="takke", bas_renk="#2a2a2a", sakal="#4a3a2a", yon=-1, kemer=None)
        figur(t, kisi, 266, arka, kk, **LEVEND_B, yon=-1)
        tas_duvar(t, 0, b["w"] - 1, z, 3.0, tas="#4a4040", tohum=480)
        _zeytin(t, z, f, True)

    _spr(480, kare, esik=0.97)


def sahne483():
    _lipari(483, MOR, ("#e8c0b8", "#c098a0", "#906c84"), ("#3e3a5e", "#363254"), D_AKSAM,
            ("#6a5e66", "#544a54", "#3e3640"), gece=True, yildiz=30)
    b = P(483)
    sinir = _ust_sinir(483)
    noktalar = _kale_atesleri(483, 3)

    def kare(t, z, i):
        f = i / KARE
        for j, (x, y) in enumerate(noktalar):
            duman(t, x, y + 2, max(8, min(46, y + b["taban"] - b["h"] - sinir - 6)), 483 + j, faz=(f + j * 0.3) % 1,
                  renk="#5a5060", ruzgar=0.25, genislik=0.9)
        tas_duvar(t, 0, b["w"] - 1, z, 3.0, tas="#5a5266", tohum=483)
        _zeytin(t, z, f, True)

    _spr(483, kare, esik=0.97)


# ==========================================================================
# 482 · kart 45-46 · yanmış arşiv odası
# ==========================================================================
def sahne482():
    ic_mekan(482, duvar=("#1a1214", "#241a1a", "#2e2220"), kemer="#0e0a0a", cini="#3a1a14",
             pencere=("#6a1e14", "#d8602a"), zemin_renk=("#2e2622", "#26201c", "#1e1a16"), isik="#d8602a", hali=False)
    K = K_(482)
    sinir = _ust_sinir(482)
    b = P(482)

    def kare(t, z, i):
        f = i / KARE
        d = ImageDraw.Draw(t)
        y = z[0]
        s = 0.62 * K                                                    # kömürleşmiş raf
        x0, x1 = 128, 128 + int(18 * s)
        temas_golgesi(t, (x0 + x1) // 2, y, x1 - x0 + 2)
        d.rectangle([x0, y - int(30 * s), x1, y - 1], fill=hex2("#1a1210"))
        for k in (x0, x1 - int(1.2 * s)):
            d.rectangle([k, y - int(30 * s), k + int(1.2 * s), y - 1], fill=hex2("#2e2420"))
        for sy in (y - int(1.2 * s), y - int(8.6 * s), y - int(16 * s), y - int(23.2 * s)):
            d.rectangle([x0, sy, x1, sy + max(1, int(0.8 * s))], fill=hex2("#3a2a22"))
            for k in range(x0 + 3, x1 - 3, 5):
                if (k + sy) % 3:
                    d.rectangle([k, sy - int(2.6 * s), k + 2, sy - 1], fill=hex2("#2a1e1a"))
        d.line([x0 + 3, y - int(20 * s), x0 + 9, y - int(26 * s)], fill=hex2("#0a0606"), width=2)
        for j, (px_, w_) in enumerate(((202, 12), (226, 10), (248, 14), (268, 10))):   # yerde yanan kâğıtlar
            d.polygon([(px_ - w_ // 2, y - 1), (px_ + w_ // 2, y - 1), (px_ + w_ // 2 - 2, y - 4), (px_ - w_ // 2 + 3, y - 4)],
                      fill=hex2("#c8b890" if j % 2 else "#a89870"))
            d.line([px_ - w_ // 2, y - 2, px_ - w_ // 2 + 4, y - 3], fill=hex2("#2a1a10"))
            yangin(t, px_, y - 2, (f + j * 0.27) % 1, 0.9 + 0.2 * (j % 2), tohum=j)
            duman(t, px_ + 2, y - 10, max(10, min(60, y + b["taban"] - b["h"] - sinir - 16)), 482 + j,
                  faz=(f + j * 0.31) % 1, renk="#4a4040", ruzgar=0.2, genislik=1.1)

    _spr(482, kare)


# ==========================================================================
# 484 · kart 48 · İstanbul silüeti; kadırga eve döner
# ==========================================================================
def _istanbul(t, z):
    d = ImageDraw.Draw(t)
    y = z[0]
    renk = "#5a3a5a"
    rnd = random.Random(484)
    for x in range(0, W, 6):
        d.rectangle([x, y - rnd.randint(4, 9), x + 5, y], fill=hex2(_ac(renk, rnd.uniform(-0.05, 0.08))))
    for cx, r, minare in ((150, 14, 4), (300, 10, 2), (400, 8, 1), (60, 7, 1)):
        d.rectangle([cx - r - 4, y - r - 4, cx + r + 4, y], fill=hex2(renk))
        d.chord([cx - r, y - 2 * r - 4, cx + r, y - 4], 180, 360, fill=hex2(_ac(renk, 0.08)))
        d.line([cx, y - 2 * r - 4, cx, y - 2 * r - 7], fill=hex2(_ac(renk, 0.15)))
        for k in range(minare):
            mx = cx - r - 10 + k * ((2 * r + 20) // max(1, minare - 1)) if minare > 1 else cx + r + 8
            d.rectangle([mx - 1, y - 2 * r - 10, mx + 1, y], fill=hex2(renk))
            d.polygon([(mx - 1, y - 2 * r - 10), (mx, y - 2 * r - 15), (mx + 2, y - 2 * r - 10)], fill=hex2(_ac(renk, 0.1)))


def sahne484():
    _gok(484, KIZIL_GOK, [(110, 404, 20), (430, 402, 22)], ("#f0b098", "#c87878", "#904a5a"))
    _uzak_kiyi(484, None, None, ("#5a3a5a", "#4e3250"), D_KIZIL, 546, kasaba=_istanbul, kara_kalin=4)
    _orta_deniz(484, 556, D_KIZIL)
    _bos_on(484)
    b = P(484)
    _spr(484, _gemi_sp(484, 0, [(202, b["h"] - 14, 1.7, -1, "acik", OSMANLI, dict(fener=3))], D_KIZIL, 556))


# ==========================================================================
# 486 · kart 50-52 + kapanış · Toulon gecesi: rıhtımda kalan bir Toulonlu
# ==========================================================================
def sahne486():
    _gok(486, GECE, [(120, 404, 18)], ("#3a4a6a", "#2a3a5a", "#1e2a46"), yildiz=90)
    _uzak_kiyi(486, ("#1a2238", "#161c30"), ("#202838", "#1a2230"), ("#2a2a34", "#24242e", "#1e1e28"), D_GECE, 542,
               dag_y=(452, 500), tepe_y=520, kasaba=_toulon(isik=True))
    _orta_deniz(486, 556, D_GECE, rihtim=600, rihtim_renk=("#3a3842", "#302e38", "#5a5866"),
                ekle=lambda img: [kadirga(img, PAY + x, 568, 0.45, -1, 0.0, mod="indik", kurek=False, fener=3, isik=True,
                                          **OSMANLI) for x in (312, 368, 470, 580)])
    _bos_on(486)
    K = K_(486)

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 168, z, K, **TOULONLU, yon=1, kol=0.02 * (1 + SIN(f)))
        sokak_feneri(t, 124, z, round(0.55 * K, 1), f)

    _spr(486, kare)


SAHNELER = {n: globals()[f"sahne{n}"] for n in range(450, 487)}

if __name__ == "__main__":
    for n in ([int(a) for a in sys.argv[1:]] or sorted(SAHNELER)):
        SAHNELER[n]()
        print(f"sahne {n} çizildi", flush=True)
