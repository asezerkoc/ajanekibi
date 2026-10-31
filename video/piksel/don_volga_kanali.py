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
