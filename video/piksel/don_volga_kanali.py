"""Su Akmıyor: Sokollu Mehmed Paşa'nın Don-Volga kanalı ve Astrahan seferi (1569 → 1952). Piksel Tarih (@pikseltarihim),
sahneler 250-289. Grafikerin tarifi: teslimler/gece/ara/don-volga-kanali/5-grafik.md; kartlar 4-kalite-metin.md
"Nihai ekran kartları" (52 kart, harfi harfine; TSX: video/src/sahneler/DonVolga.tsx).
Kalıp: cem_sultan.py (ölçek ve kadraj), celebi_mehmed_paris.py (TSX'ten okunan yazı bandı denetimi),
orhun_yazitlari.py (kenar denetimi), takiyuddin_rasathanesi.py (suda gemi: gemi sprite'ta, su sprite'ın alt satırlarında).
Yön dili: batı (Don, Azak, İstanbul, dönüş) solda; doğu (Volga, Astrahan) sağda. Hendek her sahnede zemine kazılmış sığ
bir yarık (orta planda), kazıcılar onun tabanına basar.

Yeni figürler (bu dosyada; ciz.py'ye eklenmedi, yalnızca piksel()/hex2()/ImageDraw ve mevcut figürlerle):
  kazici (iki elle kazma vuran asker), kurekci (kürekle toprak atan), toprak_yigini, hendek_yarigi (orta planda sığ yarık),
  harita_sehpasi (iki nehirli harita, ayaklı sehpada), kayik_kutuk (kütükler üstünde karadan çekilen nehir teknesi),
  ahsap_kale (Astrahan: kazık sur, ahşap kuleler, soğan kubbeli kilise), kadirga (latin yelkenli Osmanlı kadırgası, hasar=1
  kırık direk), kon_cadir (Osmanlı ordu çadırı; yikik=1 sökülmüş), harabe (eski Hacı Tarhan'ın kerpiç duvar kalıntıları),
  yatan_asker (yerde ölü asker, kan), dikenli_tel, gozcu_kulesi (alçak), el_arabasi, heykel_kaide (yüzsüz bronz heykel
  silueti ve granit kaide; kim=None boş kaide), kilit (1952 kanal kapağı, önden: iki beton kule ve çelik kapak, akan su).
Hepsi zemine oturur (zemin_y / duz_zemin); gemiler su çizgisine oturur, altları suyun içindedir.
Kullanım: python3 -I video/piksel/don_volga_kanali.py [sahne numaraları]"""
import math
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw  # noqa: E402

from ciz import (_ac, cicek, cimen_tutamlari, duman, duz_zemin, figur, gradyan, gunes, hex2, okuz, piksel,  # noqa: E402
                 temas_golgesi, yeni, yildizlar, zemin_y)
from sahneler import GW, H, duz, gokyuzu, kaydet, on, orta, sprite, uzak  # noqa: E402
from timur_figur import TEN, _u, anadolu_kalesi, atli, deve, kisi, otag, oturan  # noqa: E402
from timur import ates, hava, ic_mekan, kandil, mumluk, ok_ucusu, su_ve_kiyi, yatan_at  # noqa: E402
from takiyuddin_rasathanesi import top_  # noqa: E402
from orhun_yazitlari import avrupali, masa, masa_mumu  # noqa: E402

KARE = 24      # sprite kare sayısı (SKILL.md)
PAY = 135      # orta/ön plan yan payı (SKILL.md)
SIN = lambda f, k=1: math.sin(f * 2 * math.pi * k)  # noqa: E731
COS = lambda f, k=1: math.cos(f * 2 * math.pi * k)  # noqa: E731

# Dış mekân sprite'ı (brif: h 170-230), hendek sahnesi (taban yarığın tabanında) ve iç mekân sprite'ı (h 300)
DW, DH, DT = 400, 220, 632
HT = 640                         # hendek tabanı (dünya y): yarık orta planda 626-640 arasında, kazıcılar 640'a basar
IW, IH, IT = 400, 300, 634

# --------------------------------------------------------------------------
# KİŞİLER (renk kimlikleri bütün videoda aynı; iki kişi aynı çizilmez)
# --------------------------------------------------------------------------
SOKOLLU = dict(govde="#2a6a3a", bas="sarik", bas_renk="#f8f4ea", sakal="#d8d0c8")                # veziriazam: yeşil, ak sakal
KASIM = dict(govde="#9a5a1a", bas="sarik", bas_renk="#f4f0e6", sakal="#1e140e", pelerin="#1e2a4a")  # hardal kaftan, lacivert kürk
MALTSEV = dict(govde="#4a5a6a", bas="kalpak", bas_renk="#2e241c", sakal="#a07a4a", kemer="#8a7a5a")  # Rus elçisi: gri-mavi, açık sakal
HAN = dict(govde="#5a2a6a", bas="sorguc", bas_renk="#2a1a14", sakal="#1e140e")                    # Devlet Giray: mor, sorguç
YENICERI = dict(govde="#3a4a7a", bas="bork", bas_renk="#ece6d8", sakal="#2a1a12")
AZAP = [dict(govde="#6a5a3a", bas="bork", bas_renk="#5a3a22", sakal="#2a1a12", kemer="#c8a060"),       # kazıcılar (azap, lağımcı)
        dict(govde="#7a4a32", bas="sarik", bas_renk="#e8e0d0", sakal=None, kemer="#c8a060"),
        dict(govde="#5a5a42", bas="bork", bas_renk="#7a5a3a", sakal="#3a2a1a", kemer="#c8a060")]
NOGAY = dict(govde="#6a5a3a", bas="kalpak", bas_renk="#3a2a1a", sakal="#2a1a12")
TATAR = dict(govde="#5a4a32", bas="kalpak", bas_renk="#2a1e14", sakal="#2a1a12")
STRELETS = dict(govde="#8a1e22", bas="kalpak", bas_renk="#3a2a1a", sakal="#6a4a2a", kemer="#e0c060")  # Rus nöbetçi
KAZAK = dict(govde="#2e2a3a", bas="kalpak", bas_renk="#141018", sakal="#2a1a12")                    # Kazak / Çerkes akıncı
HACI = [dict(govde="#d8ccb0", bas="sarik", bas_renk="#f8f4ea", sakal="#8a8070", kemer="#8a6a3a"),
        dict(govde="#b8a888", bas="sarik", bas_renk="#f0ebe0", sakal="#3a2a1a", kemer="#6a4a2a")]
PETRO = dict(govde="#24402a", bas="sapka", bas_renk="#141414", sakal=None, kemer="#c8a040")          # Çar Petro: koyu yeşil
PERRY = dict(govde="#6a4a2a", bas="sapka", bas_renk="#1a1612", sakal=None, sac="#d8ccb0")            # John Perry: kahverengi, ak peruk
MUJIK = dict(govde="#a8322a", bas=None, bas_renk="#000000", sakal="#7a5a3a", kemer="#3a2a1a")        # 1697 köylü işçi (sac ayrı)
MAHKUM = [dict(govde="#5a5a54", bas="kasket", bas_renk="#44443e", sakal=None, kemer=None),           # Gulag mahkûmu: gri kapitone
          dict(govde="#4e5056", bas="kasket", bas_renk="#3a3c40", sakal="#4a4038", kemer=None)]
GARDIYAN = dict(govde="#5a6a3a", bas="kasket", bas_renk="#3e4a2a", sakal=None, kemer="#3a2a1a")       # haki asker

# ==========================================================================
# ÖLÇÜM VE DENETİM YARDIMCILARI (cem_sultan.py / orhun_yazitlari.py / celebi_mehmed_paris.py kalıbı).
# Yeni çizim fonksiyonu değil: figürü boş yüzeye çizip alfa kanalından ölçer.
# ==========================================================================


def _bb(img):
    return img.getchannel("A").getbbox()


_ONBELLEK = {}


def olcek(ad, yakin, cizim, oran=0.30):
    """Figür kutusu kadraj yüksekliğinin >= oran'ı olan en küçük s (0.1 adım). Görünen ızgara yüksekliği = 960/yakin."""
    anahtar = (ad, yakin, oran)
    if anahtar in _ONBELLEK:
        return _ONBELLEK[anahtar]
    hedef = oran * 960 / yakin
    s = 2.0
    while s <= 12.0:
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


def s_kisi(yakin, oran=0.30):
    """Ayakta insan (sarıklı) kadrajın en az %30'u."""
    return olcek("kisi", yakin, lambda t, s, z: figur(t, kisi, 280, z, s, **KASIM, yon=1), oran)


def s_atli(yakin, oran=0.30):
    """Atlı: at + binici kadrajın en az %30'u; insan/at oranı kütüphanenin onaylı oranı (atli)."""
    return olcek("atli", yakin, lambda t, s, z: figur(t, atli, 280, z, s, 1, dur=True, **TATAR), oran)


def _kz(yakin, taban=IT, h=IH):
    """Kandil zinciri: sprite'ın üst kenarından (tavan) kadrajın üst kenarının biraz altına."""
    ust_gorunen = (taban - 12) * (1 - 1 / yakin)
    return max(40, int(ust_gorunen - (taban - h)) + 10)


def _kadraj(no, kare, w, h, yakin, esik, kenar=True):
    """Görünür aralık yerel x = w/2 ± 270/yakin. Opak piksellerin en az `esik` oranı içeride olmalı; figür sprite'ın
    üstüne değmemeli (kesik baş = hata); kenar=True: sahne sonu yakınlaşmasında (yakin·1.06) tam opak hiçbir piksel
    kadraj dışında kalmamalı (kenarda kesilen figür/eşya = hata)."""
    yarim = 270 / yakin
    a, b = max(int(w / 2 - yarim), 0), min(int(w / 2 + yarim), w)
    for i in (0, 6, 12, 18):
        t = yeni(w, h)
        kare(t, duz(h - 1, w), i)
        alfa = t.getchannel("A")
        toplam = sum(alfa.histogram()[1:])
        bb = alfa.getbbox()
        ust_satir = sum(alfa.crop((0, 0, w, 2)).histogram()[1:])
        if not toplam or (bb[1] <= 1 and ust_satir > 12):
            raise RuntimeError(f"Sahne {no}: sprite yüksekliği (h={h}) yetmiyor ya da kare boş")
        if kenar:
            tam = alfa.point(lambda v: 255 if v > 200 else 0).getbbox()
            y2 = 270 / (yakin * 1.06)
            if tam and (tam[0] < w / 2 - y2 + 2 or tam[2] > w / 2 + y2 - 2):
                raise RuntimeError(f"Sahne {no}: kare {i}, opak x {tam[0]}-{tam[2]}, görünür {int(w / 2 - y2)}-"
                                   f"{int(w / 2 + y2)}: kenarda kesilen figür/eşya var")
        ici = sum(alfa.crop((a, 0, b, h)).histogram()[1:])
        if ici / toplam < esik:
            raise RuntimeError(f"Sahne {no}: figürlerin %{int(100 * ici / toplam)}'i görünür aralıkta (x {a}-{b})")


def _gorunur(no, xler, sx0, sx1, yakin, pay=12):
    """Orta plandaki önemli nesnelerin ızgara x'i, sahne başı ve sonu sx'inde (yakin·1.06) görünür aralıkta."""
    for sx in (sx0, sx1):
        y2 = 270 / (yakin * 1.06)
        a, b = sx - y2 + pay, sx + y2 - pay
        for x in xler:
            if not a <= x <= b:
                raise RuntimeError(f"Sahne {no}: orta plan nesnesi x={x} görünür aralık [{int(a)}, {int(b)}] dışında")


# --------------------------------------------------------------------------
# Yazı bandı denetimi (celebi_mehmed_paris.py kalıbı): kartların alt kenarı ve yakin değerleri DonVolga.tsx'ten okunur
# (tek kaynak). Sprite'ta ve orta planda bu banttaki satırlarda görünür sütunlarda opak piksel varsa betik durur.
# --------------------------------------------------------------------------
TSX = Path(__file__).parents[1] / "src" / "sahneler" / "DonVolga.tsx"


def _tsx_bantlari():
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
        tb = re.search(r"taban: (\d+)", b)
        taban = int(tb.group(1)) if tb else 630
        od = re.search(r"odakY: (\d+)", b)
        oy = int(od.group(1)) if od else taban - 12
        km = re.search(r"kamera: (\d+)", b)
        kam = int(km.group(1)) if km else 36
        dosya = re.search(r'dosya: "(\w+)"', b)
        alt = 0
        for m in re.finditer(r"satirlar: \[([^\]]*)\], sure: [\d.]+(?:, boy: (\d+))?", b):
            sat = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
            boy = int(m.group(2) or 92)
            sig = min(boy, math.floor(950 / (max(len(x) for x in sat) * 0.46)))
            alt = max(alt, (ust + len(sat) * sig * 1.12 + 8) / 2)          # ekran px → ızgara
        sonuc.setdefault(no, []).append(dict(yk=yk, alt=alt, ust=ust / 2, oy=oy, taban=taban, kam=kam,
                                             dosya=dosya.group(1) if dosya else "karakter"))
    return sonuc


def _bant(no, b, pay=4):
    """Bir Bolum için yazı bandının dünya y aralıkları (sahne başı ve sonu yakınlaşması): [(z, y0, y1)]."""
    o = b["oy"]
    return [(z, int(o - (o - b["ust"]) / z), int(o - (o - b["alt"]) / z) + pay) for z in (b["yk"], b["yk"] * 1.06)]


def _bant_denetimi(no, w, h, dosya="karakter"):
    pub = Path(__file__).parents[1] / "public"
    spr = Image.open(pub / f"sahne{no}-{dosya}.png").convert("RGBA").getchannel("A")
    ort = Image.open(pub / f"sahne{no}-orta.png").convert("RGBA").getchannel("A")
    for b in _tsx_bantlari().get(no, []):
        if b["dosya"] != dosya:
            continue
        taban = b["taban"]
        kg = b["kam"] * 0.65 / 2                                              # kamera kaydırması (ızgara px)
        for z, y0, y1 in _bant(no, b):
            yar = 270 / z
            for i in range(0, KARE, 3):
                for y in range(max(y0, taban - h), y1 + 1):
                    ly = y - (taban - h)
                    a, c = max(0, int(w / 2 - yar - kg)), min(w, int(w / 2 + yar + kg))
                    n = sum(spr.crop((i * w + a, ly, i * w + c, ly + 1)).histogram()[1:])
                    if n > 2:
                        raise RuntimeError(f"Sahne {no}: sprite (kare {i}) yazı bandına giriyor: dünya y {y} "
                                           f"(bant {y0}-{y1}, yakin {z:.2f}); figürü küçült ya da alçalt")
            for y in range(y0, y1 + 1):
                n = sum(ort.crop((PAY + int(270 - yar - kg - 30), y, PAY + int(270 + yar + kg + 30), y + 1)).histogram()[1:])
                if n > 2:
                    raise RuntimeError(f"Sahne {no}: orta plandaki nesne yazı bandına giriyor: y {y} (bant {y0}-{y1})")


def _bant_alt(no, pay=8):
    """Sahnenin bütün kartları ve yakınlaşma için yazı bandının en alt dünya y'si (+pay)."""
    return max((y1 + pay for b in _tsx_bantlari().get(no, []) for _, _, y1 in _bant(no, b)), default=0)


def _spr(no, w, h, kare, yakin, esik=0.75, kenar=True, dosya="karakter", denetim=True):
    """Kadraj + kenar + taban (sahneler.sprite) + yazı bandı denetimi."""
    _kadraj(no, kare, w, h, yakin, esik, kenar)
    sprite(no, dosya, w, h, KARE, kare, denetim)
    _bant_denetimi(no, w, h, dosya)


def _bos_on(no):
    """Ön plan boş (iç mekân, güverte, kilit): çimen tutamı yok."""
    kaydet(yeni(GW, H), f"sahne{no}-on.png")


def _yerel(gx, sx, w):
    """Izgara x'i → sprite yerel x'i (SKILL.md: yerel = izgara − (sx − w/2))."""
    return gx - (sx - w // 2)


# ==========================================================================
# YENİ FİGÜRLER
# ==========================================================================
TOPRAK = "#7a5a3a"


def _kol_sil(img, x, zemin, s, yon, govde, kemer, diz=False):
    """kisi'nin yanda sarkan kolunu gövde rengiyle örter (iki elle tutulan alet için kol yeniden çizilir)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 6 * s)
    yy = y + (int(3.6 * s) if diz else 0)
    ust = yy - int(11 * s)
    omuz = (x + int(0.5 * s) * yon, ust + int(1 * s))
    eski = (x + int(2.5 * s) * yon, ust + int(5 * s))
    d.line([*omuz, *eski], fill=hex2(govde), width=_u(1, s))
    piksel(img, eski[0], eski[1], hex2(govde))
    if kemer:
        d.line([x - int(2.5 * s), ust + int(4 * s), x + int(2.5 * s), ust + int(4 * s)], fill=hex2(kemer))
    return d, y, yy, ust, omuz


def _vurus_acisi(hy, L, s, y):
    """Kazmanın ön ucu tam zemine (y-1) değecek handle açısı (yerel, yon=1)."""
    en, iyi = 1e9, 0.5
    for k in range(0, 160):
        a = k * 0.01
        uc = hy + L * math.sin(a) + 2.6 * s * math.cos(a)
        if abs(uc - (y - 1)) < en:
            en, iyi = abs(uc - (y - 1)), a
    return iyi


def kazici(img, x, zemin, s=1.0, faz=0.0, yon=1, govde="#6a5a3a", bas="bork", bas_renk="#5a3a22", sakal=None,
           kemer="#c8a060", diz=False, toz=TOPRAK):
    """Yeni figür: iki elle kazma vuran asker. faz 0: kazma başın üstünde (geride); 0.5: ön ucu zemine iner (vuruş),
    vuruştan sonra toprak parçaları yukarı sıçrar. Ayakları (diz=True: dizleri) zemine basar; kazmanın ucu vuruşta
    tam zemin satırına değer, hiçbir karede zeminin altına girmez."""
    kisi(img, x, zemin, s, govde=govde, bas=bas, bas_renk=bas_renk, sakal=sakal, yon=yon, kemer=kemer, diz=diz)
    d, y, yy, ust, omuz = _kol_sil(img, x, zemin, s, yon, govde, kemer, diz)
    sw = (0.5 - 0.5 * math.cos(2 * math.pi * faz)) ** 1.5
    hx = (1.5 + 3.0 * sw) * s
    hy = (ust - 3.5 * s) * (1 - sw) + (yy - 5.5 * s) * sw
    L = 7 * s
    a_r = math.atan2(-1.0, -0.4)
    a_v = _vurus_acisi(yy - 5.5 * s, L, s, y)
    a = a_r + (a_v - a_r) * sw
    P = lambda lx, ly: (x + lx * yon, ly)  # noqa: E731
    el = P(hx, hy)
    bas_ = (hx + L * math.cos(a), hy + L * math.sin(a))
    dik = (-math.sin(a), math.cos(a))
    on_ = P(bas_[0] + dik[0] * 2.6 * s, min(y - 1, bas_[1] + dik[1] * 2.6 * s))
    arka = P(bas_[0] - dik[0] * 2.0 * s, bas_[1] - dik[1] * 2.0 * s)
    d.line([*el, *P(*bas_)], fill=hex2("#6a4a2a"), width=_u(0.7, s))
    d.line([*arka, *on_], fill=hex2("#8a8a92"), width=_u(0.8, s))
    piksel(img, on_[0], on_[1], hex2("#c8ccd4"))
    d.line([*omuz, *el], fill=hex2(_ac(govde, -0.3)), width=_u(1, s))
    piksel(img, el[0], el[1], hex2(TEN))
    p = (faz - 0.5) / 0.28
    if 0 <= p <= 1 and toz:                                # vuruştan sonra toprak sıçrar (yukarı), sonra düşer
        rnd = random.Random(int(x * 7 + s * 13))
        for k in range(7):
            vx = (rnd.random() - 0.3) * 1.6 * s * yon
            vy = (1.5 + rnd.random() * 2.5) * s
            px = on_[0] + vx * p * 2
            py = (y - 2) - vy * p * (1.6 - 1.4 * p)
            boy = max(1, int(0.5 * s))
            d.rectangle([px, py - boy, px + boy, py], fill=hex2(_ac(toz, 0.1 * (k % 3) - 0.05)))


def kurekci(img, x, zemin, s=1.0, faz=0.0, yon=1, govde="#7a4a32", bas="sarik", bas_renk="#e8e0d0", sakal=None,
            kemer="#c8a060", toz=TOPRAK):
    """Yeni figür: kürekle toprak atan asker (kisi + kurek). faz ile kürek yere iner, dolar, kalkar; kalkıkken ağzında
    toprak topağı. Ayakları zemine basar."""
    k = 0.08 + 0.42 * (0.5 - 0.5 * math.cos(2 * math.pi * faz))
    kisi(img, x, zemin, s, govde=govde, bas=bas, bas_renk=bas_renk, sakal=sakal, yon=yon, silah="kurek", kol=k,
         kemer=kemer)
    if k > 0.3:
        y = zemin_y(zemin, x, 6 * s)
        ust = y - int(11 * s)
        ex, ey = x + int(3.5 * s) * yon, ust - int(4 * s * k) + int(1 * s)
        alt_ = min(ey + int(8.5 * s), y - 2)
        d = ImageDraw.Draw(img)
        bx = ex + int(0.9 * s) * yon
        d.chord([bx - int(1.6 * s), alt_ - int(4.2 * s), bx + int(1.6 * s), alt_ - int(1.4 * s)], 180, 360, fill=hex2(toz))


def toprak_yigini(img, x, zemin, s=1.0, renk=TOPRAK, tohum=1, gen=14, boy=5):
    """Yeni figür: kazıdan atılmış toprak yığını. Tabanı zemine oturur; üstünde topaklar, kenarında taşlar."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, gen * s)
    temas_golgesi(img, x, y, gen * s + 2)
    w2, h_ = int(gen / 2 * s), int(boy * s)
    d.chord([x - w2, y - h_, x + w2, y + h_], 180, 360, fill=hex2(renk))
    d.chord([x - w2 + int(1.5 * s), y - h_ + int(0.8 * s), x + int(0.3 * w2), y + h_], 180, 270, fill=hex2(_ac(renk, 0.18)))
    rnd = random.Random(tohum)
    for _ in range(int(10 * s)):
        a = rnd.uniform(math.pi, 2 * math.pi)
        rr = rnd.uniform(0.2, 0.9)
        px, py = x + math.cos(a) * w2 * rr, y + math.sin(a) * h_ * rr
        if py < y - 1:
            piksel(img, px, py, hex2(_ac(renk, rnd.choice((-0.25, 0.25)))))
    for k in (-1, 1):
        tx = x + k * (w2 - int(1 * s))
        d.ellipse([tx - _u(0.8, s), y - _u(1.4, s), tx + _u(0.8, s), y - 1], fill=hex2("#8a8478"))


def hendek_yarigi(img, x0, x1, ust=626, taban=HT, renk=TOPRAK, yigin=True, tohum=1, kuru=True, ot=0.0):
    """Yeni figür (orta plan): bozkıra kazılmış sığ yarık, hafif yukarıdan görünüş: güneşli uzak duvar, taban (kazıcılar
    buraya basar, y=taban) ve ışıklı ön dudak. Uçları eğimli; yigin=True uzak kenarda atılmış toprak yığınları.
    kuru=True: tabanda çatlaklar (su yok). ot: 0-1 terk edilmiş hendeği saran otlar."""
    d = ImageDraw.Draw(img)
    duvar, koyu, dudak = hex2(_ac(renk, 0.12)), hex2(_ac(renk, -0.35)), hex2(_ac(renk, 0.35))
    d.polygon([(x0, ust), (x1, ust), (x1 - 10, taban - 3), (x0 + 10, taban - 3)], fill=duvar)
    rnd = random.Random(tohum)
    for _ in range((x1 - x0) // 3):                                   # kazma izleri
        px = rnd.randint(x0 + 8, x1 - 8)
        py = rnd.randint(ust + 2, taban - 5)
        d.line([px, py, px + rnd.choice((-1, 1)) * 2, py + 2], fill=hex2(_ac(renk, -0.12)))
    d.rectangle([x0 + 10, taban - 3, x1 - 10, taban + 1], fill=koyu)
    d.polygon([(x0, ust), (x0 + 10, taban - 3), (x0 + 10, taban + 1), (x0 - 4, taban + 2)], fill=hex2(_ac(renk, -0.2)))
    d.polygon([(x1, ust), (x1 - 10, taban - 3), (x1 - 10, taban + 1), (x1 + 4, taban + 2)], fill=hex2(_ac(renk, -0.2)))
    d.line([x0 - 4, taban + 2, x1 + 4, taban + 2], fill=dudak)
    d.line([x0, ust, x1, ust], fill=hex2(_ac(renk, -0.45)))
    if kuru:
        for _ in range((x1 - x0) // 22):
            px = rnd.randint(x0 + 14, x1 - 20)
            d.line([px, taban - 1, px + 5, taban], fill=hex2(_ac(renk, -0.55)))
            d.line([px + 5, taban, px + 9, taban - 1], fill=hex2(_ac(renk, -0.55)))
    if ot:
        for _ in range(int((x1 - x0) * ot)):
            px = rnd.randint(x0 - 2, x1 + 2)
            yy = rnd.choice((ust, taban + 2))
            for k in range(rnd.randint(2, 5)):
                piksel(img, px, yy - k, hex2(rnd.choice(("#8a9a4a", "#6a7a3a", "#a8a858"))))
    if yigin:
        for i, xx in enumerate(range(x0 + 18, x1 - 10, 46)):
            toprak_yigini(img, xx + rnd.randint(-6, 6), duz(ust - 1, img.width), 1.3 + 0.3 * (i % 2), renk, tohum + i)


def harita_sehpasi(img, x, zemin, s=1.0, faz=0.0):
    """Yeni figür: ayaklı, eğik bir sehpaya gerilmiş parşömen harita (Sokollu'nun haritası; yazısız). Kuzey yukarıda:
    solda Don güneye, Azak Denizi'ne; sağda Volga güneydoğuya, Hazar'a akar; iki nehrin en çok yaklaştığı yerde
    (Perevoloka) kırmızı kesik çizgi (planlanan hendek) faz ile parlar. Kara ayaklar ve arka destek zemine basar."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 28 * s)
    temas_golgesi(img, x, y, 28 * s)
    ah, ahk = hex2("#6a4426"), hex2("#3e2614")
    d.line([x + int(1 * s), y - int(29 * s), x + int(4 * s), y - 1], fill=ahk, width=_u(0.9, s))          # arka destek
    for k in (-1, 1):                                                                                   # ön ayaklar
        d.line([x + k * int(11 * s), y - int(12 * s), x + k * int(13 * s), y - 1], fill=ah, width=_u(1.0, s))
    d.rectangle([x - int(14 * s), y - int(13 * s), x + int(14 * s), y - int(11.6 * s)], fill=ah)          # alt pervaz
    L, R, T, B = x - int(13 * s), x + int(13 * s), y - int(31 * s), y - int(13 * s)
    d.polygon([(L, B), (R, B), (R - int(0.8 * s), T), (L + int(0.8 * s), T)], fill=ahk)
    m = int(1.3 * s)
    il, ir, it, ib = L + m, R - m, T + m, B - m
    d.rectangle([il, it, ir, ib], fill=hex2("#e6d4a8"))
    rnd = random.Random(253)
    for _ in range(int(40 * s)):                                                                        # eskime lekesi
        piksel(img, rnd.randint(il, ir), rnd.randint(it, ib), hex2(rnd.choice(("#d8c090", "#cdb684", "#efe0bc"))))
    W_, H_ = ir - il, ib - it
    Q = lambda u, v: (il + u * W_, it + v * H_)  # noqa: E731
    su, kiyi = hex2("#7aa0b4"), hex2("#3a5a74")
    azak = [Q(0, 0.86), Q(0.1, 0.8), Q(0.26, 0.84), Q(0.3, 0.94), Q(0.22, 1), Q(0, 1)]
    hazar = [Q(0.78, 0.66), Q(0.9, 0.6), Q(1, 0.62), Q(1, 1), Q(0.82, 1), Q(0.74, 0.86)]
    for deniz in (azak, hazar):
        d.polygon(deniz, fill=su, outline=kiyi)
    for k in range(3):                                                                                  # Kafkas dağları
        cx, cy = Q(0.42 + k * 0.1, 0.9)
        d.polygon([(cx - 1.4 * s, cy), (cx, cy - 1.8 * s), (cx + 1.4 * s, cy)], outline=hex2("#8a6a44"))
    don = [(0.16, 0.0), (0.22, 0.12), (0.32, 0.22), (0.42, 0.31), (0.465, 0.4), (0.41, 0.5), (0.31, 0.62), (0.22, 0.76),
           (0.17, 0.84)]
    volga = [(0.94, 0.0), (0.85, 0.12), (0.72, 0.24), (0.6, 0.33), (0.545, 0.4), (0.59, 0.5), (0.69, 0.58), (0.79, 0.64)]
    for nehir in (don, volga):
        d.line([Q(*p) for p in nehir], fill=hex2("#3a6a9a"), width=_u(0.5, s), joint="curve")
    for u, v, r in ((0.19, 0.83, 0.6), (0.8, 0.62, 0.6)):                                              # Azak, Astrahan
        cx, cy = Q(u, v)
        d.rectangle([cx - r * s, cy - r * s, cx + r * s, cy + r * s], fill=hex2("#6a2a1a"))
    a, b = Q(0.465, 0.4), Q(0.545, 0.4)
    parlak = 0.5 + 0.5 * SIN(faz)
    renk = hex2("#c8302a") if parlak < 0.6 else hex2("#e8a030")
    n = max(2, int((b[0] - a[0]) / max(1, s * 0.6)))
    for k in range(n):
        if k % 2 == 0:
            xx = a[0] + (b[0] - a[0]) * k / n
            d.rectangle([xx, a[1] - _u(0.3, s), xx + max(1, s * 0.5), a[1] + _u(0.3, s)], fill=renk)
    d.rectangle([il, it, ir, ib], outline=hex2("#8a6a3a"))


def kayik_kutuk(img, x, zemin, s=1.0, yon=1):
    """Yeni figür: Perevoloka'da karadan çekilen nehir teknesi: iki kütüğün (merdane) üstünde yatan ahşap gövde, yatırılmış
    direk ve sarılı yelken. Kütüklerin altı zemine değer, gövde kütüklere oturur. Dönen değer: baştaki halat halkası."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 30 * s)
    temas_golgesi(img, x, y, 30 * s)
    r = 1.6 * s
    for kx in (-8, 8):
        cx = x + kx * s
        d.ellipse([cx - r, y - 2 * r, cx + r, y - 1], fill=hex2("#6a4a2a"), outline=hex2("#3a2614"))
        piksel(img, cx, y - r, hex2("#c8a070"))
    ust = y - int(2 * r)
    P = lambda lx, ly: (x + lx * s * yon, ust + ly * s)  # noqa: E731
    govde = [P(-15, -6.5), P(-12, -5), P(12, -5), P(16, -7.5), P(13, -2), P(9, 0), P(-10, 0), P(-14, -3)]
    d.polygon(govde, fill=hex2("#6a4428"))
    for ly in (-2, -3.6):
        d.line([P(-12.5, ly), P(12.5, ly)], fill=hex2("#4a2e18"))
    d.line([P(-12, -5), P(12, -5)], fill=hex2("#a8784a"), width=_u(0.5, s))
    d.line([P(-10, -5.6), P(9, -7.2)], fill=hex2("#4a2a16"), width=_u(0.7, s))                       # yatırılmış direk
    d.polygon([P(-7, -5.4), P(5, -6.6), P(5, -8.4), P(-7, -7.0)], fill=hex2("#d8ccb0"))                # sarılı yelken
    return P(16, -7.5)


def ahsap_kale(img, x0, x1, zemin, s=1.0, ahsap="#7a5a3a"):
    """Yeni figür: 1569'un Astrahan kalesi (Rus; o yıllarda ahşap): sivri uçlu kazık sur, çadır çatılı ahşap kuleler, ortada
    kapı kulesi, surun arkasında soğan kubbeli ahşap kilise. Yalnızca düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "ahsap_kale", tolerans=3)
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0 + 6)
    koyu, acik, cati = hex2(_ac(ahsap, -0.3)), hex2(_ac(ahsap, 0.2)), hex2("#4a3020")
    kx = x0 + int((x1 - x0) * 0.62)                                                 # kilise (surun arkasında)
    d.rectangle([kx - int(3 * s), y - int(14 * s), kx + int(3 * s), y - int(8 * s)], fill=hex2("#8a6a48"))
    d.rectangle([kx - int(1.6 * s), y - int(16.5 * s), kx + int(1.6 * s), y - int(14 * s)], fill=hex2("#7a5a3a"))
    d.ellipse([kx - int(2.2 * s), y - int(20 * s), kx + int(2.2 * s), y - int(15.6 * s)], fill=hex2("#3a6a4a"))
    d.polygon([(kx - int(1.2 * s), y - int(19.2 * s)), (kx, y - int(21.6 * s)), (kx + int(1.2 * s), y - int(19.2 * s))],
              fill=hex2("#3a6a4a"))
    d.line([kx, y - int(21.6 * s), kx, y - int(23 * s)], fill=hex2("#c8a040"))
    d.line([kx - _u(0.6, s), y - int(22.4 * s), kx + _u(0.6, s), y - int(22.4 * s)], fill=hex2("#c8a040"))
    adim = max(2, int(1.3 * s))
    for xx in range(x0, x1, adim):                                                  # kazık sur
        h_ = int(9 * s) + (xx * 7 % 3)
        d.rectangle([xx, y - h_, xx + adim - 1, y - 1], fill=hex2(ahsap) if (xx // adim) % 2 else acik)
        d.polygon([(xx, y - h_), (xx + adim / 2, y - h_ - max(1, int(0.9 * s))), (xx + adim - 1, y - h_)], fill=koyu)
    d.line([x0, y - int(6 * s), x1, y - int(6 * s)], fill=koyu)
    d.line([x0, y - int(3 * s), x1, y - int(3 * s)], fill=koyu)
    for k, tx in enumerate((x0 + int(3.5 * s), (x0 + x1) // 2, x1 - int(3.5 * s))):  # kuleler
        hk = int((16 if k == 1 else 14) * s)
        gk = int(3.5 * s)
        d.rectangle([tx - gk, y - hk, tx + gk, y - 1], fill=hex2(ahsap))
        for yy in range(y - hk + int(2 * s), y, max(2, int(1.2 * s))):
            d.line([tx - gk, yy, tx + gk, yy], fill=koyu)
        d.rectangle([tx + 1, y - hk, tx + gk, y - 1], fill=hex2(_ac(ahsap, -0.15)))
        d.polygon([(tx - gk - int(1 * s), y - hk), (tx, y - hk - int(6 * s)), (tx + gk + int(1 * s), y - hk)], fill=cati)
        d.rectangle([tx - _u(0.8, s), y - hk + int(2 * s), tx + _u(0.8, s), y - hk + int(3.6 * s)], fill=hex2("#1a1410"))
        if k == 1:
            d.rectangle([tx - int(2 * s), y - int(6 * s), tx + int(2 * s), y - 1], fill=hex2("#2a1c12"))


def kadirga(img, x, su_y, s=1.0, yon=1, faz=0.0, yelken="#e8dcc0", govde="#5a3a22", hasar=0.0, bayrak="#b8281e",
            tayfa=True):
    """Yeni figür: Osmanlı kadırgası (1569). Uzun, alçak gövde; baş tarafta mahmuz; kıçta köşk ve fener; tek direkte uzun
    latin seren ve üçgen yelken; bir sıra kürek faz ile çekilir. tayfa=True: küpeştenin üstünde, gemi ölçeğinde
    kürekçi başları (geminin insana göre gerçek büyüklüğünü gösterir). Gövde su çizgisine oturur, alt kısmı suyun içinde
    kalır (suyu sahne çizer). hasar 0-1: kırık direk, suya sarkan seren ve yırtık yelken, başa doğru yan yatış."""
    d = ImageDraw.Draw(img)
    dal = math.sin(faz * 2 * math.pi) * 0.5 * s
    egim = 0.06 * hasar

    def P(lx, ly):
        rx = lx * math.cos(egim) - ly * math.sin(egim)
        ry = lx * math.sin(egim) + ly * math.cos(egim) + 2.0 * hasar
        return (x + rx * s * yon, su_y + ry * s + dal)

    kiyi = hex2(_ac(govde, -0.35))
    if not hasar:                                                                  # yelken (direğin arkasında)
        A, B = (20, -9), (-18, -31)
        sis = 1.2 * math.sin(faz * 2 * math.pi)
        d.polygon([P(*A), P(*B), P(-5 + sis, -6.2), P(6 + sis, -11)], fill=hex2(yelken))
        d.line([P(-5 + sis, -6.2), P(-18, -31)], fill=hex2(_ac(yelken, -0.18)))
        for t in (0.3, 0.55, 0.8):
            ax, ay = A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t
            d.line([P(ax, ay), P(ax - 3 + sis * t, ay + 9 - t * 3)], fill=hex2(_ac(yelken, -0.12)))
    # gövde
    d.polygon([P(-30, -8.5), P(-27, -4.5), P(24, -4.5), P(29, -5.8), P(35, -2.6), P(27, -1.0), P(24, 1.8),
               P(-22, 2.2), P(-28, 0.2)], fill=hex2(govde))
    d.line([P(-27, -4.5), P(24, -4.5)], fill=hex2(_ac(govde, 0.35)), width=_u(0.5, s))
    d.line([P(-26, -3.0), P(24, -3.0)], fill=hex2("#8a2a1a"), width=_u(0.5, s))
    for lx in range(-24, 24, 4):
        piksel(img, *P(lx, -3.0), hex2("#e0b040"))
    d.line([P(-22, -1.0), P(24, -1.0)], fill=kiyi)
    # kürekler: gövdenin yanından suya iner
    for i in range(15):
        lx = -21 + i * 3
        if hasar and i % 4 == 1:
            d.line([P(lx, -2.2), P(lx - 1.0, 0.0)], fill=hex2("#3a2418"), width=_u(0.35, s))     # kırık kürek
            continue
        sup = 1.6 * math.sin(faz * 2 * math.pi + i * 0.15) * (0.2 if hasar else 1)
        d.line([P(lx, -2.2), P(lx - 2.0 + sup, 3.0)], fill=hex2("#3a2418"), width=_u(0.35, s))
    # kıç köşkü ve fener
    d.polygon([P(-28.5, -8.6), P(-22, -8.6), P(-21.5, -4.6), P(-27, -4.6)], fill=hex2(_ac(govde, 0.12)))
    d.polygon([P(-29.5, -8.6), P(-25.5, -11.6), P(-21, -8.6)], fill=hex2("#8a2a1a"))
    d.rectangle([*P(-26.2, -7.6), *P(-24.4, -5.6)] if yon > 0 else [*P(-24.4, -7.6), *P(-26.2, -5.6)], fill=hex2("#2a1a10"))
    d.line([P(-30.2, -8.5), P(-30.6, -13.4)], fill=hex2("#3a2418"), width=_u(0.4, s))
    d.rectangle([P(-31.4, -15.4)[0] - 0.9 * s, P(-31.4, -15.4)[1], P(-31.4, -15.4)[0] + 0.9 * s, P(-31.4, -13.2)[1]],
                fill=hex2("#e0b040"))
    if tayfa:                                                                      # kürekçi başları (gemi ölçeğinde)
        for i, lx in enumerate(range(-19, 22, 3)):
            hx, hy = P(lx + 0.6, -5.6)
            r = max(1, 0.75 * s)
            d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=hex2(TEN))
            d.rectangle([hx - r, hy - r - max(1, 0.5 * s), hx + r, hy - r * 0.3], fill=hex2(("#ece6d8", "#5a3a22")[i % 2]))
    # direk ve seren
    if hasar:
        d.line([P(3, -4.5), P(3, -12.0)], fill=hex2("#4a2a16"), width=_u(1.0, s))
        d.polygon([P(2.4, -12.0), P(3.0, -13.6), P(3.6, -12.4)], fill=hex2("#6a4a2a"))                # kırık uç
        d.line([P(15, -4.6), P(-20, 1.0)], fill=hex2("#4a2a16"), width=_u(0.7, s))                   # suya düşmüş seren
        d.polygon([P(9, -3.8), P(-4, -1.6), P(-2, 0.8), P(6, -1.0)], fill=hex2(_ac(yelken, -0.25)))  # suya sarkan yırtık yelken
        d.polygon([P(-8, -1.0), P(-14, -0.2), P(-12, 1.2)], fill=hex2(_ac(yelken, -0.3)))
    else:
        d.line([P(3, -4.5), P(3, -24)], fill=hex2("#4a2a16"), width=_u(1.0, s))
        d.line([P(20, -9), P(-18, -31)], fill=hex2("#3a2214"), width=_u(0.7, s))
        dl = 0.8 * math.sin(faz * 2 * math.pi * 2)
        d.polygon([P(3, -24), P(-3, -23.4 + dl), P(3, -22.2)], fill=hex2(bayrak))


def kon_cadir(img, x, zemin, s=1.0, renk="#e8e0cc", serit="#b8281e", yikik=0.0, isik=False):
    """Yeni figür: Osmanlı ordu çadırı: silindir duvar, saçaklı (dilimli) etek bandı, konik çatı, tepede alem; iki yanda
    gergi ipleri ve kazıklar zemine çakılı. Yalnızca düz zemine kurulur. isik=True: kapıdan içerideki ışık görünür.
    yikik=1: sökülmüş çadır; yere serilmiş, katlanmış bez yığını ve üstüne yatırılmış direk (hepsi yerde)."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, int(x - 13 * s), int(x + 13 * s), "çadır", tolerans=4)
    temas_golgesi(img, x, y, 20 * s)
    if yikik:
        d.chord([x - int(11 * s), y - int(4 * s), x + int(11 * s), y + int(4 * s)], 180, 360, fill=hex2(renk))
        for k in (-6, -1, 4):
            d.arc([x + int((k - 3) * s), y - int(3.2 * s), x + int((k + 3) * s), y + int(1 * s)], 200, 340,
                  fill=hex2(_ac(renk, -0.25)))
        d.line([x - int(10 * s), y - int(1.8 * s), x + int(10 * s), y - int(1.8 * s)], fill=hex2(serit), width=_u(0.6, s))
        d.line([x - int(9 * s), y - int(2.6 * s), x + int(12 * s), y - int(4.6 * s)], fill=hex2("#5a3a22"), width=_u(0.7, s))
        d.polygon([(x + int(12 * s), y - int(4.6 * s)), (x + int(13 * s), y - int(5.4 * s)), (x + int(13.4 * s), y - int(4.4 * s))],
                  fill=hex2("#e0b040"))
        return
    ip = hex2("#6a5a44")
    for k in (-1, 1):
        d.line([x + k * int(8.5 * s), y - int(8 * s), x + k * int(13 * s), y - 1], fill=ip)
        d.rectangle([x + k * int(13 * s) - 1, y - max(2, int(0.9 * s)), x + k * int(13 * s) + 1, y - 1], fill=hex2("#3a2a1a"))
    d.rectangle([x - int(8 * s), y - int(7 * s), x + int(8 * s), y - 1], fill=hex2(renk))
    d.rectangle([x + int(3 * s), y - int(7 * s), x + int(8 * s), y - 1], fill=hex2(_ac(renk, -0.16)))
    d.polygon([(x - int(9 * s), y - int(7.4 * s)), (x, y - int(15 * s)), (x + int(9 * s), y - int(7.4 * s))],
              fill=hex2(_ac(renk, 0.06)))
    d.polygon([(x, y - int(15 * s)), (x + int(9 * s), y - int(7.4 * s)), (x + int(3 * s), y - int(7.4 * s))],
              fill=hex2(_ac(renk, -0.1)))
    for k in (-5, 0, 5):
        d.line([x, y - int(15 * s), x + int(k * 1.6 * s), y - int(7.4 * s)], fill=hex2(_ac(renk, -0.2)))
    d.rectangle([x - int(9 * s), y - int(7.6 * s), x + int(9 * s), y - int(6.4 * s)], fill=hex2(serit))
    for xx in range(x - int(9 * s), x + int(9 * s), max(3, int(2 * s))):
        d.chord([xx, y - int(7 * s), xx + max(3, int(2 * s)), y - int(5.4 * s)], 0, 180, fill=hex2(serit))
    d.line([x, y - int(15 * s), x, y - int(16.2 * s)], fill=hex2("#5a3a22"))
    d.ellipse([x - _u(0.6, s), y - int(17.2 * s), x + _u(0.6, s), y - int(16 * s)], fill=hex2("#e0b040"))
    d.polygon([(x - int(2.4 * s), y - 1), (x - int(1.6 * s), y - int(5.6 * s)), (x + int(1.6 * s), y - int(5.6 * s)),
               (x + int(2.4 * s), y - 1)], fill=hex2("#f8c060" if isik else "#2a1e14"))
    if isik:
        d.rectangle([x - int(1 * s), y - int(4 * s), x + int(1 * s), y - 1], fill=hex2("#ffe8a0"))


def harabe(img, x0, x1, zemin, s=1.0, tohum=1, renk="#b89a70"):
    """Yeni figür: eski Hacı Tarhan'ın kerpiç duvar kalıntıları: kırık tepeli duvar parçaları, yarım kemer, dibinde düşmüş
    kerpiçler. Bütün parçalar x0-x1 tabanının içinde, düz zemine oturur (dışarı taşan moloz yok)."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "harabe", tolerans=4)
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0)
    rnd = random.Random(tohum)
    koyu, acik = hex2(_ac(renk, -0.25)), hex2(_ac(renk, 0.15))
    xx = x0 + int(2 * s)
    while xx < x1 - int(6 * s):
        g = int(rnd.uniform(5, 10) * s)
        g = min(g, x1 - int(2 * s) - xx)
        h_ = rnd.uniform(4, 11) * s
        tepe = [(xx + k, y - h_ + rnd.uniform(-1.4, 1.4) * s) for k in range(0, g + 1, max(2, int(s)))]
        d.polygon([(xx, y - 1)] + tepe + [(xx + g, y - 1)], fill=hex2(renk))
        d.rectangle([xx + g - max(1, int(1.2 * s)), y - h_ * 0.8, xx + g, y - 1], fill=koyu)
        for yy in range(int(y - h_), y, max(2, int(1.6 * s))):
            d.line([xx, yy, xx + g, yy], fill=hex2(_ac(renk, -0.1)))
        if rnd.random() < 0.45 and g > 5 * s and h_ > 7 * s:
            ax = xx + g // 2
            d.chord([ax - int(1.8 * s), y - int(6.5 * s), ax + int(1.8 * s), y - int(2.5 * s)], 180, 360, fill=hex2("#2a1e14"))
            d.rectangle([ax - int(1.8 * s), y - int(4.5 * s), ax + int(1.8 * s), y - 1], fill=hex2("#2a1e14"))
        xx += g + int(rnd.uniform(2, 5) * s)
    for _ in range(int((x1 - x0) / max(2, s))):                                       # düşmüş kerpiç (tabanın içinde)
        bx = rnd.randint(x0 + int(1 * s), x1 - int(2 * s))
        d.rectangle([bx, y - max(2, int(1 * s)), bx + max(2, int(1.6 * s)), y - 1], fill=rnd.choice((koyu, acik, hex2(renk))))


def yatan_asker(img, x, zemin, s=1.0, govde="#3a4a7a", bas_renk="#ece6d8", yon=1, ok=True, kan=True):
    """Yeni figür: yolda düşmüş asker: yüzüstü yatan gövde zemine değer, börkü yanına düşmüş, sırtında ok; altında kan."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 16 * s)
    temas_golgesi(img, x, y, 16 * s)
    P = lambda lx, ly: (x + lx * s * yon, y + ly * s)  # noqa: E731
    if kan:
        d.ellipse([*P(-1, -0.8), *P(9, 0.4)] if yon > 0 else [*P(9, -0.8), *P(-1, 0.4)], fill=hex2("#8a1a14"))
    d.line([P(-8, -0.9), P(-2, -1.1)], fill=hex2("#4a3a2a"), width=_u(1.3, s))                      # bacaklar
    d.line([P(-8.5, -0.6), P(-2, -0.6)], fill=hex2(_ac(govde, -0.35)), width=_u(0.8, s))
    d.polygon([P(-2.5, -0.2), P(-2.5, -2.6), P(4.5, -2.4), P(4.8, -0.2)], fill=hex2(govde))      # gövde
    d.line([P(4, -1.8), P(8.5, -0.8)], fill=hex2(_ac(govde, -0.3)), width=_u(0.9, s))              # uzanmış kol
    hx, hy = P(6.2, -1.8)
    r = max(2, 1.6 * s)
    d.ellipse([hx - r, hy - r, hx + r, min(y - 1, hy + r)], fill=hex2(TEN))
    d.polygon([P(9.5, -0.2), P(10.6, -3.0), P(12.0, -0.2)], fill=hex2(bas_renk))                    # düşmüş börk
    if ok:
        d.line([P(1.5, -2.4), P(-0.5, -7.0)], fill=hex2("#5a3a22"), width=_u(0.4, s))
        d.polygon([P(-0.5, -7.0), P(-1.6, -7.6), P(-0.8, -6.0)], fill=hex2("#e8e0d0"))


def dikenli_tel(img, x0, x1, zemin, s=1.0):
    """Yeni figür: dikenli tel çit: ahşap kazıklar zemine çakılı, üç sıra tel ve dikenler."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, (x0 + x1) // 2, x1 - x0)
    for xx in range(x0, x1 + 1, max(6, int(12 * s))):
        d.rectangle([xx, y - int(8 * s), xx + max(1, int(0.6 * s)), y - 1], fill=hex2("#4a3a2a"))
    for k in (2.5, 5, 7.5):
        yy = y - int(k * s)
        d.line([x0, yy, x1, yy], fill=hex2("#5a5a5e"))
        for xx in range(x0 + 2, x1, max(3, int(3 * s))):
            piksel(img, xx, yy - 1, hex2("#7a7a7e"))
            piksel(img, xx + 1, yy + 1, hex2("#7a7a7e"))


def gozcu_kulesi(img, x, zemin, s=1.0):
    """Yeni figür: alçak ahşap gözcü kulesi: dört ayak (ikisi görünür) ve çaprazlar zemine basar, üstte kabin ve çatı."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, int(x - 5 * s), int(x + 5 * s), "gözcü kulesi", tolerans=4)
    temas_golgesi(img, x, y, 12 * s)
    ah = hex2("#4a3a2a")
    for k in (-1, 1):
        d.line([x + k * int(5 * s), y - 1, x + k * int(3.5 * s), y - int(16 * s)], fill=ah, width=_u(0.8, s))
    d.line([x - int(4.6 * s), y - int(4 * s), x + int(3.9 * s), y - int(12 * s)], fill=ah)
    d.line([x + int(4.6 * s), y - int(4 * s), x - int(3.9 * s), y - int(12 * s)], fill=ah)
    d.rectangle([x - int(4.5 * s), y - int(20 * s), x + int(4.5 * s), y - int(16 * s)], fill=hex2("#6a5a44"))
    d.rectangle([x - int(3 * s), y - int(19.2 * s), x + int(3 * s), y - int(17.6 * s)], fill=hex2("#2a221a"))
    d.polygon([(x - int(5.6 * s), y - int(20 * s)), (x, y - int(23 * s)), (x + int(5.6 * s), y - int(20 * s))],
              fill=hex2("#3a3028"))


def el_arabasi(img, x, zemin, s=1.0, yon=1, yuk=TOPRAK):
    """Yeni figür: tek tekerlekli el arabası: tekerleğin altı ve arka ayaklar zemine basar; kasada toprak."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 14 * s)
    temas_golgesi(img, x, y, 12 * s)
    P = lambda lx, ly: (x + lx * s * yon, y + ly * s)  # noqa: E731
    r = 2 * s
    cx, cy = P(5, -2)
    d.ellipse([cx - r, cy - r, cx + r, y - 1], outline=hex2("#2a221a"), width=_u(0.6, s))
    d.line([P(-3, -1), P(-3, -3.6)], fill=hex2("#4a3a2a"), width=_u(0.5, s))                         # arka ayak
    d.line([P(-8, -6.4), P(5, -2)], fill=hex2("#5a4430"), width=_u(0.5, s))                          # kollar
    d.polygon([P(-4, -6.6), P(4.2, -6.6), P(3.2, -3.0), P(-3.2, -3.2)], fill=hex2("#6a6a6e"))
    if yuk:
        d.chord([*P(-4.2, -8.6), *P(4.2, -5.0)] if yon > 0 else [*P(4.2, -8.6), *P(-4.2, -5.0)], 180, 360, fill=hex2(yuk))


def heykel_kaide(img, x, zemin, s=1.0, kim="stalin", tunc="#3a3834"):
    """Yeni figür: granit kaide (basamaklar, gövde, korniş, yazısız levha) ve üstünde ayakta, yüzsüz bronz heykel silueti.
    kim='stalin': uzun asker paltosu, eli göğsünde; kim='lenin': açık palto, kolu ileri uzanmış; kim=None: boş kaide.
    Basamaklar düz zemine, heykelin kaidesi kaidenin üst yüzüne oturur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, int(x - 12 * s), int(x + 12 * s), "kaide", tolerans=3)
    temas_golgesi(img, x, y, 24 * s)
    gr, grk, gra = hex2("#76727c"), hex2("#5a5660"), hex2("#9a96a0")
    d.rectangle([x - int(12 * s), y - int(2 * s), x + int(12 * s), y - 1], fill=grk)
    d.rectangle([x - int(10 * s), y - int(4 * s), x + int(10 * s), y - int(2 * s)], fill=gr)
    d.rectangle([x - int(7 * s), y - int(18 * s), x + int(7 * s), y - int(4 * s)], fill=gr)
    d.rectangle([x + int(3 * s), y - int(18 * s), x + int(7 * s), y - int(4 * s)], fill=grk)
    d.rectangle([x - int(8 * s), y - int(19.6 * s), x + int(8 * s), y - int(18 * s)], fill=gra)
    d.line([x - int(10 * s), y - int(4 * s), x + int(10 * s), y - int(4 * s)], fill=gra)
    d.rectangle([x - int(3.6 * s), y - int(13 * s), x + int(2.4 * s), y - int(9 * s)], fill=hex2("#4a464e"))
    if not kim:
        return
    ty = y - int(19.6 * s)
    t, ta = hex2(tunc), hex2(_ac(tunc, 0.3))
    d.rectangle([x - int(3.4 * s), ty - int(1 * s), x + int(3.4 * s), ty - 1], fill=hex2(_ac(tunc, -0.2)))
    if kim == "stalin":
        d.polygon([(x - int(3.2 * s), ty - int(1 * s)), (x - int(2.2 * s), ty - int(13 * s)), (x + int(2.2 * s), ty - int(13 * s)),
                   (x + int(3.2 * s), ty - int(1 * s))], fill=t)
        d.line([x - int(2.0 * s), ty - int(12 * s), x - int(2.9 * s), ty - int(2 * s)], fill=ta)
        d.line([x + int(1.8 * s), ty - int(12 * s), x, ty - int(8.5 * s)], fill=hex2(_ac(tunc, -0.3)), width=_u(0.8, s))
        d.line([x, ty - int(12.6 * s), x, ty - int(1.5 * s)], fill=hex2(_ac(tunc, -0.25)))
    else:
        d.line([x - int(1.2 * s), ty - int(1 * s), x - int(1.0 * s), ty - int(6 * s)], fill=t, width=_u(1.3, s))
        d.line([x + int(1.2 * s), ty - int(1 * s), x + int(1.0 * s), ty - int(6 * s)], fill=t, width=_u(1.3, s))
        d.polygon([(x - int(2.6 * s), ty - int(5 * s)), (x - int(2.0 * s), ty - int(13 * s)), (x + int(2.0 * s), ty - int(13 * s)),
                   (x + int(2.8 * s), ty - int(5 * s))], fill=t)
        d.line([x - int(1.9 * s), ty - int(12 * s), x - int(2.5 * s), ty - int(5.5 * s)], fill=ta)
        d.line([x + int(1.2 * s), ty - int(12.2 * s), x + int(6.8 * s), ty - int(15.4 * s)], fill=t, width=_u(1.0, s))
        d.ellipse([x + int(6.4 * s), ty - int(16.2 * s), x + int(7.6 * s), ty - int(14.8 * s)], fill=t)
    hy = ty - int(14.8 * s)
    r = int(1.6 * s)
    d.ellipse([x - r, hy - r, x + r, hy + r], fill=t)
    d.arc([x - r, hy - r, x + r, hy + r], 180, 270, fill=ta)


def kilit(t, w, h, f, durum="kapali"):
    """Yeni figür (sprite'ın tamamı): 1952 Volga-Don kanalının bir kapağı, önden. İki beton kule (kemerli pencere,
    korniş), üstte köprü, aralarında çelik kapak; önde perspektifle izleyiciye doğru genişleyen beton kanal ve su.
    durum 'kapali': kapak kapalı, önündeki hazne neredeyse kuru (dipte su birikintisi). 'akiyor': kapak açılmış,
    köpüklü su hazneye hücum eder (f ile akar). 'dolu': hazne dolu, sakin su izleyiciye doğru akar.
    Kulelerin, kanal duvarlarının ve beton düzlüğün tabanı zemindir (y = kanal kenarı); su kanalın içindedir."""
    d = ImageDraw.Draw(t)
    zy = h - 160                         # beton düzlük ve kapak eşiği (yerel y)
    cx = w // 2
    beton, betk, beta = hex2("#b8b4a8"), hex2("#8a867c"), hex2("#d8d4c8")
    d.rectangle([0, zy, w, h], fill=hex2("#9a968a"))                                      # beton düzlük (zemin)
    for yy in range(zy + 6, h, 10):
        d.line([0, yy, w, yy], fill=hex2("#8e8a7e"))

    def kenar(v):                         # v: 0 kapak eşiği, 1 alt kenar → kanalın sol/sağ x'i ve y'si
        yy = zy + v * (h - zy)
        yar = 46 + v * 210
        return cx - yar, cx + yar, yy

    sol = [kenar(v / 20) for v in range(21)]
    d.polygon([(a, yy) for a, _, yy in sol] + [(b, yy) for _, b, yy in reversed(sol)], fill=hex2("#6a6a66"))  # hazne
    for a, b, yy in sol[::2]:
        d.line([a, yy, a + 6 + (yy - zy) * 0.12, yy], fill=betk)
        d.line([b - 6 - (yy - zy) * 0.12, yy, b, yy], fill=betk)
    seviye = {"kapali": 0.0, "akiyor": 0.55 + 0.25 * f, "dolu": 1.0}[durum]
    for a, b, yy in sol:                                                                   # su
        ic = 4 + (yy - zy) * 0.14 * (1 - seviye * 0.5)
        if durum == "kapali" and yy < zy + 0.55 * (h - zy):
            continue
        renk = hex2("#3a6a8a") if durum != "kapali" else hex2("#4a5a5e")
        d.line([a + ic, yy, b - ic, yy], fill=renk)
    rnd = random.Random(285)
    if durum in ("akiyor", "dolu"):                                                         # akan su çizgileri
        for k in range(46):
            u = rnd.uniform(0.12, 0.88)
            v = (k / 46 + f * (1.0 if durum == "dolu" else 2.0)) % 1
            a, b, yy = kenar(v ** 1.4)
            xx = a + (b - a) * u
            boy = 2 + v * 14
            renk = hex2("#9ac8e0") if durum == "dolu" else hex2("#e8f4f8")
            d.line([xx, yy, xx + (0.5 - u) * boy * 0.3, yy], fill=renk)
            if durum == "akiyor" and v < 0.5:
                for j in range(3):
                    piksel(t, xx + rnd.randint(-3, 3), yy - rnd.randint(0, 3), hex2("#f8fcfc"))
    elif durum == "kapali":
        for k in range(10):
            a, b, yy = kenar(0.7 + k * 0.03)
            d.line([a + 30, yy, a + 30 + (b - a - 60) * rnd.uniform(0.2, 0.6), yy], fill=hex2("#7a96a8"))
    for a, b, yy in sol:                                                                   # kanal ağzının kenar çizgisi
        piksel(t, a, yy, beta)
        piksel(t, b, yy, beta)
    ku_y = zy - 112                                                                         # kuleler
    for k in (-1, 1):
        x0, x1 = (cx - 100, cx - 46) if k < 0 else (cx + 46, cx + 100)
        d.rectangle([x0, ku_y, x1, zy], fill=beton)
        d.rectangle([x0 if k > 0 else x1 - 12, ku_y, x0 + 12 if k > 0 else x1, zy], fill=betk)
        d.rectangle([x0 - 4, ku_y - 6, x1 + 4, ku_y], fill=beta)
        d.rectangle([x0 + 8, ku_y - 18, x1 - 8, ku_y - 6], fill=beton)
        d.rectangle([x0 + 6, ku_y - 21, x1 - 6, ku_y - 18], fill=beta)
        mx = (x0 + x1) // 2
        d.chord([mx - 9, ku_y + 14, mx + 9, ku_y + 32], 180, 360, fill=hex2("#3a4a5a"))
        d.rectangle([mx - 9, ku_y + 23, mx + 9, ku_y + 54], fill=hex2("#3a4a5a"))
        d.line([mx, ku_y + 16, mx, ku_y + 54], fill=beta)
        for yy in range(ku_y + 66, zy - 4, 12):
            d.line([x0 + 2, yy, x1 - 2, yy], fill=hex2("#a8a498"))
    d.rectangle([cx - 46, ku_y + 6, cx + 46, ku_y + 20], fill=hex2("#9a968a"))              # köprü
    d.line([cx - 46, ku_y + 6, cx + 46, ku_y + 6], fill=beta)
    for xx in range(cx - 44, cx + 46, 6):
        d.line([xx, ku_y + 1, xx, ku_y + 6], fill=hex2("#5a5a5a"))
    d.line([cx - 46, ku_y + 1, cx + 46, ku_y + 1], fill=hex2("#5a5a5a"))
    acik = {"kapali": 0.0, "akiyor": 0.6, "dolu": 1.0}[durum]
    kap_y0, kap_y1 = ku_y + 20, zy
    if acik < 1:                                                                            # çelik kapak kanatları
        g = int(46 * (1 - acik))
        for k in (-1, 1):
            xa, xb = (cx - 46, cx - 46 + g) if k < 0 else (cx + 46 - g, cx + 46)
            d.rectangle([xa, kap_y0, xb, kap_y1], fill=hex2("#3e4c5a"))
            for yy in range(kap_y0 + 6, kap_y1, 9):
                d.line([xa, yy, xb, yy], fill=hex2("#566676"))
            d.line([xa if k > 0 else xb, kap_y0, xa if k > 0 else xb, kap_y1], fill=hex2("#26303a"))
    if acik > 0:                                                                            # açıklıktan memba suyu
        g = int(46 * acik)
        d.rectangle([cx - g, zy - 26, cx + g, zy], fill=hex2("#3a6a8a"))
        for k in range(8):
            xx = cx - g + 4 + (k * 13 + int(f * 52)) % (2 * g - 8)
            d.line([xx, zy - 24 + k * 3, xx + 6, zy - 24 + k * 3], fill=hex2("#8ab8d8"))
        if durum == "akiyor":
            for k in range(30):
                xx = cx - g + rnd.randint(0, 2 * g)
                yy = zy - rnd.randint(0, 10) + int(((k * 7 + f * 40) % 12))
                piksel(t, xx, yy, hex2("#f8fcfc"))
