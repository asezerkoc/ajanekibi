"""Oğullarımdan İyi: Raziye Sultan, Delhi Türk Sultanlığı'nın kadın hükümdarı (1236-1240). Piksel Tarih (@pikseltarihim),
sahneler 210-248 (249 boş, yedek). Grafikerin tarifi: teslimler/gece/ara/raziye-sultan/5-grafik.md; metin ve 51 kart
4-kalite-metin.md'den. Kalıp: video/piksel/cem_sultan.py (ölçek/kadraj yardımcıları), celebi_mehmed_paris.py (yazı bandı
denetimi: bantlar RaziyeSultan.tsx'ten okunur), orhun_yazitlari.py (kenar denetimi), takiyuddin_rasathanesi.py.
Yön dili: sol = Bathinda (kuzeybatı), sağ = Delhi / saray / Gwalior yolu.
Kaynaksız ayrıntı çizilmez: Raziye'nin giysisi kırmızı değil (lacivert-camgöbeği), cami adı ve minare yok (avlu yalnızca revak),
kadeh ve at anekdotu yok, ölüm anı ve fail gösterilmez (köylü sahnesi kart 37-39'da, İbn Battûta'nın dinlediği hikâye).
Kullanım: python3 -I video/piksel/raziye_sultan.py [sahne numaraları]

Yeni figürler (bu dosyada; ciz.py'ye eklenmedi, yalnızca piksel()/hex2()/ImageDraw ve mevcut figürlerle):
  başlıklar "pece" (başörtüsü + yüz peçesi, yalnızca gözler açık) ve "kulah" (sivri külah, açık saç) timur_figur'un başlık
  çiziciye bu betik çalışırken eklenir (dosya değişmez); fil_alay (timur_figur.fil + işlemeli çul + açık hevdec + üstünde
  oturan sultan + boynunda filbaşı), seki, revak, sikke_yuva (büyük sikke), ors, tepsi, sehpa_tabut, ahir, cadir, kubbe_turbe,
  harita_sehpasi, mezar_avlusu, levha, pece_yerde, uyuyan, acik_kitap, pece_ve_tac, meyve_tepsisi. Hepsi zemine oturur.
"""
import math
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw  # noqa: E402

import timur_figur as _tf  # noqa: E402
from ciz import KOYU, _ac, agac, duman, duz_zemin, figur, gradyan, hex2, orta_asya_sehri, piksel, temas_golgesi, yeni, zemin_y  # noqa: E402
from sahneler import GW, H, duz, gokyuzu, kaydet, on, orta, sprite, uzak  # noqa: E402
from timur_figur import TEN, anadolu_kalesi, at, atli, deve, fil, kisi, koy_evleri, oturan, sedir  # noqa: E402
from timur import ic_mekan, kalabalik, kandil, mangal, mumluk  # noqa: E402
from kalender import kitaplar, rahle, taht  # noqa: E402

KARE = 24      # sprite kare sayısı (SKILL.md)
PAY = 135      # orta/ön plan yan payı (SKILL.md)
SIN = lambda f, k=1: math.sin(f * 2 * math.pi * k)  # noqa: E731
DW, DH, DT = 400, 220, 632     # dış mekân sprite'ı (brif: h 170-230)
IW, IH, IT = 400, 300, 634     # iç mekân sprite'ı (brif: h 300, kandil zinciri tavana)
ALTIN_R = "#e0b040"


def _u(v, s):
    return max(1, int(round(v * s)))


# ==========================================================================
# YENİ BAŞLIKLAR: "pece" ve "kulah". timur_figur.kisi / oturan / atli başlığı _baslik ile çizer; bu betik çalışırken
# iki yeni tür eklenir, diğer türler (sarik, kalpak, ortu, bork...) aynen eski çiziciye gider. Paylaşılan dosya değişmez.
# ==========================================================================
_ESKI_BASLIK = _tf._baslik


def _baslik(d, img, x, bas_y, r, s, yon, tur, renk):
    if tur == "pece":
        # Yeni figür: peçeli kadın başı. Başı ve omuzları saran örtü, ensede sırta düşen uzun kuyruk, yüzün alt yarısını
        # çeneden göğse kadar kapatan açık renk peçe; yalnızca göz yarığı açık.
        k = hex2(renk)
        e = _u(0.5, s)
        d.chord([x - r - 1 - e, bas_y - r - 1 - e, x + r + 1 + e, bas_y + r + 1 + e], 180, 360, fill=k)
        d.rectangle([x - r - 1 - e, bas_y - e, x - r + e, bas_y + r + _u(2.6, s)], fill=k)
        d.rectangle([x + r - e, bas_y - e, x + r + 1 + e, bas_y + r + _u(2.6, s)], fill=k)
        arka = x - (r + e) * yon
        d.polygon([(arka, bas_y - e), (arka - _u(1.4, s) * yon, bas_y + r + _u(5, s)), (arka + _u(0.8, s) * yon, bas_y + r + _u(5, s)),
                   (arka + _u(0.8, s) * yon, bas_y)], fill=hex2(_ac(renk, -0.12)))
        pe = hex2(_ac(renk, 0.1))
        d.polygon([(x - r, bas_y + _u(0.5, s)), (x + r, bas_y + _u(0.5, s)), (x + r + e, bas_y + r + _u(2.2, s)),
                   (x - r - e, bas_y + r + _u(2.2, s))], fill=pe)
        d.line([x - r + e, bas_y + r + _u(1.2, s), x + r - e, bas_y + r + _u(1.2, s)], fill=hex2(_ac(renk, -0.15)))
        d.rectangle([x - r + e, bas_y - _u(0.6, s), x + r - e, bas_y + _u(0.4, s)], fill=hex2(TEN))   # göz yarığı
        gx = x + _u(0.7, s) * yon
        d.rectangle([min(gx, gx + _u(0.3, s) * yon), bas_y - _u(0.4, s), max(gx, gx + _u(0.3, s) * yon), bas_y], fill=hex2(KOYU))
    elif tur == "kulah":
        # Yeni figür: Raziye'nin külahı (Minhâc: kaba ve külah). Başa oturan, tepesi yuvarlatılmış alçak keçe külah
        # (boyu yaklaşık baş kadar), kalın koyu kürk kenar ve önde küçük altın süs; yüz açık, ensede omza inen koyu saç.
        sac = hex2("#2a1a12")
        a0, a1 = x - (r + _u(0.6, s)) * yon, x - (r - _u(1.1, s)) * yon
        d.rectangle([min(a0, a1), bas_y - _u(0.8, s), max(a0, a1), bas_y + r + _u(1.8, s)], fill=sac)
        k = hex2(renk)
        tepe = bas_y - r - _u(3.4, s)
        d.polygon([(x - r - _u(0.4, s), bas_y - r + _u(0.6, s)), (x - r + _u(0.4, s), tepe + _u(1.2, s)), (x - _u(0.6, s), tepe),
                   (x + _u(0.6, s), tepe), (x + r - _u(0.4, s), tepe + _u(1.2, s)), (x + r + _u(0.4, s), bas_y - r + _u(0.6, s))], fill=k)
        d.line([x - r + _u(0.6, s) * (yon < 0) + _u(0.4, s), tepe + _u(1.4, s), x - _u(0.4, s), tepe + _u(0.4, s)], fill=hex2(_ac(renk, 0.25)))
        d.rectangle([x - r - _u(0.8, s), bas_y - r - _u(0.3, s), x + r + _u(0.8, s), bas_y - r + _u(1.0, s)], fill=hex2("#5a4030"))
        for kx in range(x - r - _u(0.8, s), x + r + _u(0.8, s), 2):            # kürk dokusu
            piksel(img, kx, bas_y - r - _u(0.3, s), hex2("#7a5a42"))
        sx_ = x + _u(0.8, s) * yon
        d.rectangle([sx_ - _u(0.4, s), bas_y - r - _u(1.6, s), sx_ + _u(0.4, s), bas_y - r - _u(0.3, s)], fill=hex2(ALTIN_R))
        piksel(img, sx_, bas_y - r - _u(1.0, s), hex2("#2a8a8a"))
    else:
        _ESKI_BASLIK(d, img, x, bas_y, r, s, yon, tur, renk)


_tf._baslik = _baslik

# ==========================================================================
# KİŞİLER (renk kimlikleri bütün videoda aynı; Raziye kırmızı giymez: kaynaksız)
# ==========================================================================
RAZ_PECE = dict(govde="#2a5a7a", bas="pece", bas_renk="#ece4d4", kadin=True, kemer=ALTIN_R)          # peçeli, uzun giysi
RAZ = dict(govde="#2a5a7a", bas="kulah", bas_renk="#3a2a4a", kadin=True, kemer=ALTIN_R, uzun=False)  # tunik + külah, peçesiz
RAZ_O_PECE = dict(govde="#2a5a7a", bas="pece", bas_renk="#ece4d4")                                  # oturan (peçeli)
RAZ_O = dict(govde="#2a5a7a", bas="kulah", bas_renk="#3a2a4a")                                       # oturan (külahlı)
ILTUTMIS = dict(govde="#4a3a6a", bas="sarik", bas_renk="#f4f0e6", sakal="#b8b2a8", pelerin="#8a6a2a")
ILTUTMIS_O = dict(govde="#4a3a6a", bas="sarik", bas_renk="#f4f0e6", sakal="#b8b2a8")
FIRUZ = dict(govde="#c8902a", bas="sarik", bas_renk="#f4f0e6", sakal=None)                            # genç, altın sarısı
SAH_TERKEN = dict(govde="#4a2a4a", bas="ortu", bas_renk="#2a1a2a", kadin=True, kemer="#a88030")
EMIR1 = dict(govde="#5a4a32", bas="kalpak", bas_renk="#2a1a12", sakal="#2a1a12", kemer="#a88030")      # Türk köle emîrleri
EMIR2 = dict(govde="#34483e", bas="kalpak", bas_renk="#3a2a1a", sakal="#3a2a1a", kemer="#a88030")
EMIR3 = dict(govde="#4a3a2e", bas="bork", bas_renk="#6a4a2a", sakal="#1a1210", kemer="#a88030")
YAKUT = dict(govde="#3a6a4a", bas="sarik", bas_renk="#e8e0cc", sakal="#1a1210", ten="#6a4428")      # Habeşli, ahır emîri
ALTUNIYA = dict(govde="#6a4a2a", bas="kalpak", bas_renk="#1a1210", sakal="#1a1210", kemer="#a88030")
BEHRAM = dict(govde="#2a6a3a", bas="sarik", bas_renk="#f4f0e6", sakal="#3a2a1a")
NASIR = dict(govde="#2a3a6a", bas="sarik", bas_renk="#f4f0e6", sakal="#2a1a12")                      # Sultan Nâsıreddin (1260)
MINHAC_GENC = dict(govde="#4a5a6a", bas="sarik", bas_renk="#f8f4ea", sakal="#4a3a2a")                 # 1231: 38 yaşında
MINHAC = dict(govde="#4a5a6a", bas="sarik", bas_renk="#f8f4ea", sakal="#d8d0c8")                      # 1260: yaşlı
BATTUTA = dict(govde="#c8b48a", bas="sarik", bas_renk="#f4f0e6", sakal="#2a1a12", kemer="#6a4a2a")
KOYLU = dict(govde="#8a7a5a", bas="takke", bas_renk="#e0d8c4", sakal="#3a2a1a", kemer=None)
ASKER = dict(govde="#5a5a6a", bas="migfer", bas_renk="#8a8a90", sakal="#2a1a12", kemer="#6a4a2a")
HIZMET = dict(govde="#7a6a8a", bas="ortu", bas_renk="#d8d0c0", kadin=True, kemer=None)
USTA = dict(govde="#6a4a32", bas="takke", bas_renk="#d8d0c0", sakal="#2a1a12", kemer=None)


def _el(x, z0, s, yon, kol):
    """kisi'nin (ayakta, diz=False) el noktası: timur_figur.kisi formülü."""
    ust = z0 - int(11 * s)
    if kol > 0:
        return x + int(3.5 * s) * yon, ust - int(4 * s * kol) + int(1 * s)
    return x + int(2.5 * s) * yon, ust + int(5 * s)


# ==========================================================================
# YENİ FİGÜRLER
# ==========================================================================
def _cul_hevdec(img, x, zemin, s=1.0, yon=1, cul="#22346a"):
    """Filin sırtına oturan işlemeli çul (lacivert, altın kenar, saçak) ve üstünde açık, alçak korkuluklu oturak (hevdec).
    Konum timur_figur.fil'in gövde geometrisinden: gövde y = zemin - 10·s, sırt tepesi gövde - 18·s."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 30 * s)
    gy = y - int(10 * s)

    def p(dx, dy):
        return (x + int(round(dx * s)) * yon, gy + int(round(dy * s)))

    d.polygon([p(-10.5, -16.2), p(-3, -17.6), p(5, -16.8), p(6.5, -5.5), p(-11, -5.5)], fill=hex2(cul))
    d.line([p(-11, -5.5), p(6.5, -5.5)], fill=hex2(ALTIN_R), width=_u(0.6, s))
    d.line([p(-10.3, -14), p(-10.8, -5.5)], fill=hex2(ALTIN_R), width=_u(0.4, s))
    d.line([p(6, -15), p(6.5, -5.5)], fill=hex2(ALTIN_R), width=_u(0.4, s))
    for k in range(-10, 7, 2):                                               # saçak
        a, b = p(k, -5.5), p(k, -4.3)
        d.line([a, b], fill=hex2(ALTIN_R))
    for k in range(-8, 5, 4):                                                # çul deseni: baklava
        cx, cy = p(k, -11)
        d.polygon([(cx, cy - _u(1.4, s)), (cx + _u(1.2, s), cy), (cx, cy + _u(1.4, s)), (cx - _u(1.2, s), cy)], fill=hex2("#3a5a9a"))
        piksel(img, cx, cy, hex2(ALTIN_R))
    # hevdec: alçak oturak tablası ve ön/arka korkuluk babaları
    d.rectangle([min(p(-8, -19.5)[0], p(4, -19.5)[0]), p(0, -19.5)[1], max(p(-8, -17)[0], p(4, -17)[0]), p(0, -17)[1]],
                fill=hex2("#8a5a2a"), outline=hex2("#3a2410"))
    for k in (-8, 4):
        a = p(k, -23)
        b = p(k, -19.5)
        d.line([a, b], fill=hex2(ALTIN_R), width=_u(0.7, s))
        d.rectangle([a[0] - _u(0.6, s), a[1] - _u(0.6, s), a[0] + _u(0.6, s), a[1]], fill=hex2(ALTIN_R))
    return p(-2, -19.5)[1]


def fil_alay(t, x, z, s=1.0, yon=1, faz=0.0, adim=0.28, kalpak_mahut=True):
    """Yeni figür (bileşik): fil üstünde sultan. timur_figur.fil (kulesiz) + işlemeli çul + açık hevdec; hevdecte bağdaş
    kurmuş peçesiz, külahlı Raziye (oturan, fil ile aynı insan ölçeği: s), boynunda filbaşı. Her parça ayrı konturlanır.
    Ölçek: fil s=1'de omuz ≈ 28 px, insan ≈ 15,5 px (gerçek oran ~1,7: Asya fili omzu 2,7 m, insan 1,6 m)."""
    figur(t, fil, x, z, s, yon, faz, renk="#8a8a92", kule=False, adim=adim)
    oturak = figur(t, _cul_hevdec, x, z, s, yon)
    rx = x + int(round(-2 * s)) * yon
    figur(t, oturan, rx, duz(oturak, t.width), s, **RAZ_O, yon=yon)
    gy = zemin_y(z, x, 30 * s) - int(10 * s)
    mx = x + int(round(11.5 * s)) * yon
    figur(t, oturan, mx, duz(gy - int(round(18.6 * s)), t.width), round(0.92 * s, 2), govde="#6a5a3a", bas="sarik",
          bas_renk="#e8e0cc", sakal="#2a1a12", yon=yon)


def seki(img, x0, x1, zemin, h, tas="#b8a888"):
    """Yeni figür: kesme taştan alçak seki (konuşma yeri). Düz zemine oturur; üstü düz, yeni zemin olarak döner."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "seki", tolerans=3)
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0 + 4)
    ust = y - h
    d.rectangle([x0, ust, x1, y - 1], fill=hex2(tas))
    koyu = hex2(_ac(tas, -0.25))
    for k, yy in enumerate(range(ust + 4, y - 1, 4)):
        d.line([x0, yy, x1, yy], fill=koyu)
        for xx in range(x0 + (k % 2) * 6, x1, 12):
            d.line([xx, yy - 3, xx, yy], fill=koyu)
    d.rectangle([x0 - 1, ust - 1, x1 + 1, ust + 1], fill=hex2(_ac(tas, 0.2)))
    return ust


def revak(img, x0, x1, zemin, s=1.0, tas="#c8a27a", golge="#8a6a4a", ic="#3a2a22"):
    """Yeni figür: sivri kemerli revak duvarı (avlu ya da saray avlusu; belirli bir cami değil, minaresiz). Düz zemine
    kurulur: duvar tabanı zemin satırında, kemer ayakları duvarın içinde; üstte düz silme ve mazgalsız parapet."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "revak", tolerans=3)
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0)
    yuk = int(26 * s)
    ust = y - yuk
    d.rectangle([x0, ust, x1, y - 1], fill=hex2(tas))
    for yy in range(ust + _u(3, s), y - 1, _u(3, s)):
        d.line([x0, yy, x1, yy], fill=hex2(_ac(tas, -0.08)))
    aral = int(14 * s)
    for kx in range(x0 + int(4 * s), x1 - int(10 * s), aral):
        kw = int(9 * s)
        ka = y - int(17 * s)
        d.rectangle([kx, ka, kx + kw, y - 1], fill=hex2(ic))
        d.polygon([(kx, ka), (kx + kw // 2, ka - int(6 * s)), (kx + kw, ka)], fill=hex2(ic))
        d.line([kx - 1, ka, kx + kw // 2, ka - int(6 * s) - 1, kx + kw + 1, ka], fill=hex2(_ac(tas, 0.25)), width=_u(0.6, s))
        d.rectangle([kx, y - int(3 * s), kx + kw, y - 1], fill=hex2(_ac(ic, 0.15)))
    d.rectangle([x0 - _u(1, s), ust - _u(1.2, s), x1 + _u(1, s), ust], fill=hex2(_ac(tas, 0.2)))
    d.rectangle([x0, ust - _u(3, s), x1, ust - _u(1.2, s)], fill=hex2(golge))
    for kx in range(x0, x1, int(6 * s)):                                      # parapet: alçak kabartma şerit
        d.rectangle([kx, ust - _u(3, s), kx + _u(2, s), ust - _u(2.2, s)], fill=hex2(_ac(golge, 0.25)))
    return ust - _u(3, s)


# --- sikke ---------------------------------------------------------------------------------------------------------
def _yazi_satiri(img, x0, x1, y, h, renk, rnd):
    """Kûfî benzeri yazı şeridi (tasarım; okunur metin değil): taban çizgisi üstünde dikey elifler, kanca ve noktalar."""
    for xx in range(x0, x1):
        piksel(img, xx, y, renk)
    xx = x0 + rnd.randint(0, 2)
    while xx < x1 - 1:
        tur = rnd.random()
        if tur < 0.35:
            for k in range(1, h):
                piksel(img, xx, y - k, renk)
        elif tur < 0.6:
            for k in range(1, max(2, h // 2)):
                piksel(img, xx, y - k, renk)
            piksel(img, xx + 1, y - max(2, h // 2) + 1, renk)
        elif tur < 0.75:
            piksel(img, xx, y + 2, renk)
        elif tur < 0.85:
            piksel(img, xx, y - h // 2 - 2, renk)
            piksel(img, xx + 1, y - h // 2 - 2, renk)
        xx += rnd.randint(2, 4)


def sikke_yuva(img, x, zemin, r=44, tur="baba", isik=0.0, f=0.0):
    """Yeni figür: büyük sikke (yakın plan) ahşap yuvaya dikilmiş: yuvanın tabanı zemine (masa yüzü) basar, sikkenin alt
    kenarı yuvanın yarığına oturur. Gümüş tanka: noktalı kenar, iç halka, ortada üç-dört satır kûfî benzeri yazı (okunmaz,
    tasarım), kenarda dairesel yazı. tur='baba': babasının adıyla ilk sikke (koyu oyuk harfler); tur='raziye': 1237 kalıbı,
    farklı satır düzeni; isik 0-1 harfleri altına yakar (ad parlıyor). Dönen değer: sikke merkezi."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 2 * r)
    temas_golgesi(img, x, y, int(r * 1.4))
    yh = max(8, r // 4)
    d.rectangle([x - int(r * 0.6), y - yh, x + int(r * 0.6), y - 1], fill=hex2("#5a3a1e"), outline=hex2("#2a1a0c"))
    d.line([x - int(r * 0.6) + 1, y - yh + 1, x + int(r * 0.6) - 1, y - yh + 1], fill=hex2("#8a5a2e"))
    cy = y - yh - r + 4                                                     # alt kenar yarığa 4 px gömülü
    gum, gum_k, gum_a = ("#c4c8cc", "#8a9096", "#eef0f2")
    d.ellipse([x - r, cy - r, x + r, cy + r], fill=hex2(gum_k))
    d.ellipse([x - r + 2, cy - r + 1, x + r - 1, cy + r - 2], fill=hex2(gum))
    for a in range(0, 360, 6):                                              # noktalı kenar
        piksel(img, x + math.cos(math.radians(a)) * (r - 4), cy + math.sin(math.radians(a)) * (r - 4), hex2(gum_k))
    d.ellipse([x - r + 9, cy - r + 9, x + r - 9, cy + r - 9], outline=hex2(gum_k))
    for a in range(200, 300, 3):                                            # sol üstte parlak yay
        piksel(img, x + math.cos(math.radians(a)) * (r - 2), cy + math.sin(math.radians(a)) * (r - 2), hex2(gum_a))
    d.rectangle([x - int(r * 0.6), y - yh, x + int(r * 0.6), y - yh + 3], fill=hex2("#5a3a1e"))   # yuva ön dudağı sikkenin önünde
    rnd = random.Random(7 if tur == "baba" else 1237)
    harf = hex2("#4a4e54")
    yan = hex2("#f8d878") if isik > 0.5 else (hex2("#c8a050") if isik > 0.1 else harf)
    satirlar = (-14, -3, 8) if tur == "baba" else (-17, -7, 3, 13)
    for j, sy in enumerate(satirlar):
        gen = int(math.sqrt(max(0, (r - 12) ** 2 - sy ** 2))) - 2
        _yazi_satiri(img, x - gen, x + gen, cy + sy, 7, yan if (tur == "raziye" and j in (1, 2)) else harf, rnd)
    for a in range(0, 360, 9):                                              # kenar yazısı: dairesel kısa çizgiler
        if rnd.random() < 0.7:
            rr = r - 7
            px_, py_ = x + math.cos(math.radians(a)) * rr, cy + math.sin(math.radians(a)) * rr
            piksel(img, px_, py_, harf)
            piksel(img, x + math.cos(math.radians(a)) * (rr - 1.5), cy + math.sin(math.radians(a)) * (rr - 1.5), harf)
    if isik > 0.5:                                                          # parlayan adın çevresinde altın hale
        for j in (1, 2):
            sy = satirlar[j]
            gen = int(math.sqrt(max(0, (r - 12) ** 2 - sy ** 2))) - 2
            for xx in range(x - gen, x + gen):
                if (xx + j) % 3 == 0:
                    piksel(img, xx, cy + sy - 9, hex2("#ffe08a", 70))
                    piksel(img, xx, cy + sy + 3, hex2("#ffe08a", 70))
    # dönen yansıma: sikkenin yüzünde soldan sağa kayan ince parıltı (f ile dikişsiz)
    gx = x - r + int(((f * 2) % 1) * 2 * r)
    for k in range(-r, r):
        px_, py_ = gx + k // 4, cy + k
        if (px_ - x) ** 2 + (py_ - cy) ** 2 < (r - 3) ** 2:
            piksel(img, px_, py_, hex2("#ffffff", 70))
    return x, cy


def ors(img, x, zemin, s=1.0):
    """Yeni figür: darphane örsü. Ahşap kütük zemine basar, üstünde demir örs; örsün üstünde sikke kalıbı (alt kalıp) ve
    gümüş pul. Dönen değer: kalıbın üst y'si (çekicin vurduğu nokta)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 8 * s)
    temas_golgesi(img, x, y, 9 * s)
    d.rectangle([x - int(3.5 * s), y - int(5 * s), x + int(3.5 * s), y - 1], fill=hex2("#6a4426"), outline=hex2("#2a1a0c"))
    for k in range(1, 3):
        d.line([x - int(3.5 * s), y - int(k * 1.7 * s), x + int(3.5 * s), y - int(k * 1.7 * s)], fill=hex2("#4a2e18"))
    ust = y - int(5 * s)
    d.rectangle([x - int(2.5 * s), ust - int(2 * s), x + int(2.5 * s), ust], fill=hex2("#3a3c42"))
    d.polygon([(x - int(4.5 * s), ust - int(3.6 * s)), (x + int(4 * s), ust - int(3.6 * s)), (x + int(2.5 * s), ust - int(2 * s)),
               (x - int(2.5 * s), ust - int(2 * s))], fill=hex2("#4a4c54"))
    d.line([x - int(4.5 * s), ust - int(3.6 * s), x + int(4 * s), ust - int(3.6 * s)], fill=hex2("#8a8e98"))
    ku = ust - int(3.6 * s)
    d.rectangle([x - int(1 * s), ku - int(1.6 * s), x + int(1 * s), ku], fill=hex2("#6a6e76"))
    d.rectangle([x - int(1.1 * s), ku - int(2 * s), x + int(1.1 * s), ku - int(1.6 * s)], fill=hex2("#d8dce0"))
    return ku - int(2 * s)


def tepsi(img, x, y, s=1.0, ic=("#2a5a7a", "#3a2a4a")):
    """Yeni figür: hizmetkârın elindeki pirinç tepsi; üstünde katlanmış tunik (Raziye'nin rengi) ve sivri külah."""
    d = ImageDraw.Draw(img)
    d.rectangle([x - int(3.4 * s), y, x + int(3.4 * s), y + _u(0.5, s)], fill=hex2("#c8a040"), outline=hex2("#6a4a10"))
    d.rectangle([x - int(2.8 * s), y - int(1.4 * s), x + int(0.6 * s), y - 1], fill=hex2(ic[0]))
    d.line([x - int(2.8 * s), y - int(0.8 * s), x + int(0.6 * s), y - int(0.8 * s)], fill=hex2(_ac(ic[0], 0.25)))
    d.polygon([(x + int(1 * s), y - 1), (x + int(2 * s), y - int(3.4 * s)), (x + int(3 * s), y - 1)], fill=hex2(ic[1]))
    d.line([x + int(1 * s), y - int(0.6 * s), x + int(3 * s), y - int(0.6 * s)], fill=hex2(ALTIN_R))


def meyve_tepsisi(img, x, zemin, s=1.0):
    """Yeni figür: alçak ayaklı pirinç sini; üstünde üzüm, nar, kavun dilimi (eğlence sofrası; kadeh yok). Ayak zemine basar."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 8 * s)
    temas_golgesi(img, x, y, 8 * s)
    d.rectangle([x - int(1.2 * s), y - int(1.6 * s), x + int(1.2 * s), y - 1], fill=hex2("#8a6a20"))
    d.rectangle([x - int(4 * s), y - int(2.2 * s), x + int(4 * s), y - int(1.6 * s)], fill=hex2("#d8b048"), outline=hex2("#6a4a10"))
    u = y - int(2.2 * s)
    for k, (dx, renk) in enumerate(((-2.4, "#5a2a6a"), (-1.4, "#6a3a7a"), (-1.9, "#7a4a8a"))):   # üzüm salkımı
        d.ellipse([x + int(dx * s) - _u(0.6, s), u - int((0.9 + 0.5 * (k == 2)) * s) - _u(0.6, s), x + int(dx * s) + _u(0.6, s),
                   u - int((0.9 + 0.5 * (k == 2)) * s) + _u(0.6, s)], fill=hex2(renk))
    d.ellipse([x + int(0.2 * s), u - int(2.2 * s), x + int(2.2 * s), u - 1], fill=hex2("#b83a2a"))            # nar
    piksel(img, x + int(1.2 * s), u - int(2.2 * s), hex2("#e0b040"))
    d.chord([x + int(2.2 * s), u - int(1.8 * s), x + int(4.2 * s), u + int(1.6 * s)], 180, 360, fill=hex2("#e8c060"))   # kavun dilimi
    d.line([x + int(2.4 * s), u - 1, x + int(4 * s), u - 1], fill=hex2("#5a8a3a"))


def sehpa_tabut(img, x, zemin, s=1.0, ortu="#2a5a3a"):
    """Yeni figür: sehpa üstünde yeşil örtülü tabut. Dört ayak zemine basar; örtü tabutun iki yanından sarkar, altın şerit."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 22 * s)
    temas_golgesi(img, x, y, 22 * s)
    ust = y - int(4.5 * s)
    for ax in (-10, -7, 7, 10):
        d.rectangle([x + int(ax * s) - _u(0.5, s), ust, x + int(ax * s) + _u(0.5, s), y - 1], fill=hex2("#4a2e18"))
    d.rectangle([x - int(11 * s), ust - _u(0.8, s), x + int(11 * s), ust], fill=hex2("#6a4426"))
    tu = ust - int(4.5 * s)
    d.polygon([(x - int(10 * s), ust - 1), (x - int(9.5 * s), tu + int(1 * s)), (x - int(7 * s), tu), (x + int(7 * s), tu),
               (x + int(9.5 * s), tu + int(1 * s)), (x + int(10 * s), ust - 1)], fill=hex2(ortu))
    d.line([x - int(9.6 * s), tu + int(1.6 * s), x + int(9.6 * s), tu + int(1.6 * s)], fill=hex2(ALTIN_R), width=_u(0.4, s))
    for k in range(-9, 10, 2):                                              # örtü kıvrımları ve saçak
        d.line([x + int(k * s), tu + int(2 * s), x + int(k * s), ust - 1], fill=hex2(_ac(ortu, -0.15)))
    d.line([x - int(7 * s), tu, x + int(7 * s), tu], fill=hex2(_ac(ortu, 0.25)))


def ahir(img, x0, x1, zemin, s=1.0):
    """Yeni figür: saray ahırı. Kerpiç arka duvar, ahşap direkler zemine dikili, eğimli saz saçak; bölmelerde yemlik ve
    saman. Düz zemine kurulur."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "ahir", tolerans=3)
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0)
    yuk = int(22 * s)
    d.rectangle([x0, y - yuk, x1, y - 1], fill=hex2("#b08a62"))
    for yy in range(y - yuk + _u(3, s), y - 1, _u(3, s)):
        d.line([x0, yy, x1, yy], fill=hex2("#a07a54"))
    for kx in range(x0 + int(4 * s), x1 - int(6 * s), int(12 * s)):         # bölmeler: koyu iç, yemlik, saman
        d.rectangle([kx, y - int(15 * s), kx + int(9 * s), y - 1], fill=hex2("#3a2a1c"))
        d.rectangle([kx + int(1 * s), y - int(6 * s), kx + int(8 * s), y - int(4.5 * s)], fill=hex2("#6a4a2a"))
        for k in range(int(8 * s)):
            piksel(img, kx + int(1 * s) + k, y - int(6 * s) - (k % 3), hex2("#d8c070"))
        for k in range(int(9 * s)):
            piksel(img, kx + k, y - 1 - (k % 2), hex2("#c8b060"))
    for kx in range(x0, x1 + 1, int(12 * s)):                               # direkler
        d.rectangle([kx, y - int(19 * s), kx + _u(1.4, s), y - 1], fill=hex2("#5a3a1e"))
    d.polygon([(x0 - int(3 * s), y - int(18 * s)), (x0 + int(2 * s), y - int(25 * s)), (x1 - int(2 * s), y - int(25 * s)),
               (x1 + int(3 * s), y - int(18 * s))], fill=hex2("#a8884a"))
    for kx in range(x0 - int(2 * s), x1 + int(2 * s), 3):
        piksel(img, kx, y - int(18 * s), hex2("#7a5a2a"))
        piksel(img, kx + 1, y - int(21 * s), hex2("#c8a868"))


def cadir(img, x, zemin, s=1.0, renk="#c8bc9a", yikik=False):
    """Yeni figür: ordugâh çadırı (A biçimi, 3/4 görünüş). Etekler, direk ve kazıklı gergi ipleri zemine basar; kapısı
    açık ve içi boş. yikik=True: bir gergi ipi kopmuş, ön etek gevşek (terk edilmiş)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x + int(4.5 * s), 32 * s)
    temas_golgesi(img, x + int(5 * s), y, 26 * s)
    sirt_on = (x, y - int(10 * s))
    sirt_arka = (x + int(9 * s), y - int(11 * s))
    ip = hex2("#5a4a38")
    if not yikik:
        d.line([*sirt_on, x - int(11 * s), y - 1], fill=ip)
    d.line([*sirt_arka, x + int(20 * s), y - 1], fill=ip)
    for kx in ((x + int(20 * s),) if yikik else (x - int(11 * s), x + int(20 * s))):
        d.rectangle([kx - 1, y - max(2, int(0.8 * s)), kx + 1, y - 1], fill=hex2("#3a2a1a"))
    d.polygon([sirt_on, sirt_arka, (x + int(16 * s), y - 1), (x + int(7 * s), y - 1)], fill=hex2(_ac(renk, -0.22)))
    d.polygon([(x - int(7 * s), y - 1), sirt_on, (x + int(7 * s), y - 1)], fill=hex2(renk))
    d.polygon([(x - int(2.6 * s), y - 1), (x, y - int(6.5 * s)), (x + int(2.6 * s), y - 1)], fill=hex2("#2a221a"))
    d.polygon([(x, y - int(6.5 * s)), (x + int(2.6 * s), y - 1), (x + int(4 * s), y - 1)], fill=hex2(_ac(renk, 0.12)))
    d.line([sirt_on[0], sirt_on[1] - int(1.5 * s), *sirt_on], fill=hex2("#4a3420"), width=max(1, int(0.5 * s)))
    d.line([*sirt_on, *sirt_arka], fill=hex2(_ac(renk, 0.3)))
    if yikik:                                                               # kopuk ip yerde
        d.line([x - int(4 * s), y - 1, x - int(11 * s), y - 1], fill=ip)


def kubbe_turbe(img, x, zemin, s=1.0, tas="#c8b89a", kubbe="#a89a84"):
    """Yeni figür: tarlada küçük kubbeli türbe (İbn Battûta: mezarın üstüne kubbe yapıldı). Kare gövde düz zemine oturur,
    kemerli kapı, sekizgen kasnak, yarım küre kubbe ve kısa alem."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x - int(9 * s), x + int(9 * s), "turbe", tolerans=3)
    temas_golgesi(img, x, y, 20 * s)
    d.rectangle([x - int(9 * s), y - int(13 * s), x + int(9 * s), y - 1], fill=hex2(tas))
    d.rectangle([x - int(9.6 * s), y - int(14 * s), x + int(9.6 * s), y - int(13 * s)], fill=hex2(_ac(tas, 0.2)))
    d.rectangle([x - int(3 * s), y - int(8 * s), x + int(3 * s), y - 1], fill=hex2("#3a2e24"))
    d.polygon([(x - int(3 * s), y - int(8 * s)), (x, y - int(11 * s)), (x + int(3 * s), y - int(8 * s))], fill=hex2("#3a2e24"))
    for kx in (-6.5, 6.5):
        d.rectangle([x + int(kx * s) - _u(0.8, s), y - int(9 * s), x + int(kx * s) + _u(0.8, s), y - int(6 * s)], fill=hex2("#4a3a2e"))
    d.rectangle([x - int(7 * s), y - int(16 * s), x + int(7 * s), y - int(14 * s)], fill=hex2(_ac(tas, -0.08)))
    d.chord([x - int(7 * s), y - int(23 * s), x + int(7 * s), y - int(9 * s)], 180, 360, fill=hex2(kubbe))
    d.arc([x - int(5 * s), y - int(21 * s), x + int(3 * s), y - int(11 * s)], 200, 260, fill=hex2(_ac(kubbe, 0.3)))
    d.line([x, y - int(23 * s), x, y - int(25.5 * s)], fill=hex2(ALTIN_R), width=_u(0.5, s))
    piksel(img, x + 1, y - int(25.5 * s), hex2(ALTIN_R))
    for k in range(int(18 * s)):
        piksel(img, x - int(9 * s) + k, y - 1 - (k % 3 == 0), hex2(_ac(tas, -0.3)))


def harita_sehpasi(img, x, zemin, s=1.0, isik=1.0):
    """Yeni figür: üç ayaklı ahşap sehpaya dayalı parşömen harita (bugün: mezarın üç iddia yeri). Ayaklar zemine basar.
    Haritada Yamuna ve Ganj kolları, Racastan çölü tonu; Delhi, Kaithal (Delhi'nin kuzey-kuzeybatısı) ve Tonk
    (güney-güneybatısı) gerçek göreli konumlarında üç ışık (isik 0-1 nabız)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 16 * s)
    temas_golgesi(img, x, y, 16 * s)
    ah = hex2("#5a3a1e")
    d.line([x - int(7 * s), y - 1, x - int(3 * s), y - int(26 * s)], fill=ah, width=_u(0.9, s))
    d.line([x + int(7 * s), y - 1, x + int(3 * s), y - int(26 * s)], fill=ah, width=_u(0.9, s))
    d.line([x + int(1 * s), y - 1, x, y - int(20 * s)], fill=hex2("#3a2410"), width=_u(0.7, s))
    d.rectangle([x - int(9 * s), y - int(9.5 * s), x + int(9 * s), y - int(8.6 * s)], fill=ah)         # tabla rafı
    x0, x1, y0, y1 = x - int(9 * s), x + int(9 * s), y - int(26 * s), y - int(9.5 * s)
    d.rectangle([x0, y0, x1, y1], fill=hex2("#e4d0a0"), outline=hex2("#8a6a3a"))
    rnd = random.Random(40)
    for _ in range(int(40 * s)):
        piksel(img, rnd.randint(x0 + 1, x1 - 1), rnd.randint(y0 + 1, y1 - 1), hex2("#d0b888"))
    d.polygon([(x0 + 1, y1 - int(6 * s)), (x0 + int(6 * s), y1 - int(4 * s)), (x0 + int(7 * s), y1 - 1), (x0 + 1, y1 - 1)],
              fill=hex2("#e0c088"))                                                                   # Racastan çölü
    nehir = hex2("#4a7aa8")

    def harita(lon, lat):
        return (x0 + (lon - 74.6) / 4.0 * (x1 - x0), y0 + (31.0 - lat) / 6.0 * (y1 - y0))

    yol = [(77.6, 31.0), (77.5, 30.2), (77.3, 29.4), (77.25, 28.6), (77.6, 27.9), (78.0, 27.2), (78.6, 26.6)]   # Yamuna
    for a, b in zip(yol, yol[1:]):
        d.line([harita(*a), harita(*b)], fill=nehir, width=_u(0.4, s))
    for nokta in ((76.4, 29.8), (77.2, 28.6), (75.8, 26.2)):                # Kaithal, Delhi, Tonk
        px_, py_ = harita(*nokta)
        r = _u(0.7 + 0.6 * isik, s)
        d.ellipse([px_ - r - 2, py_ - r - 2, px_ + r + 2, py_ + r + 2], fill=hex2("#ffd479", int(60 + 80 * isik)))
        d.ellipse([px_ - r, py_ - r, px_ + r, py_ + r], fill=hex2("#c8302a"), outline=hex2("#5a1a10"))
    d.line([harita(77.2, 28.6), harita(76.4, 29.8)], fill=hex2("#8a6a3a"))
    d.line([harita(77.2, 28.6), harita(75.8, 26.2)], fill=hex2("#8a6a3a"))


def mezar_avlusu(img, x, zemin, s=1.0, tas="#c8b498"):
    """Yeni figür: çatısız dört duvar ve iki mezar (Delhi, Bulbul-i Hâne). Cutaway 3/4 görünüş: arkada yüksek, sıvaları
    dökülmüş duvar (gökyüzü açık: çatı yok), iki yanda perspektifli yan duvarlar, önde bel hizasında alçak duvar ve
    giriş aralığı; içeride iki beyaz, basamaklı kabir (biri biraz küçük). Bütün duvarlar düz zemine oturur."""
    d = ImageDraw.Draw(img)
    gen = int(26 * s)
    y = duz_zemin(zemin, x - gen, x + gen, "avlu", tolerans=3)
    temas_golgesi(img, x, y, 2 * gen + 4)
    arka_y = y - int(7 * s)                                                 # avlu zemininin arka kenarı (perspektif)
    koyu = hex2(_ac(tas, -0.25))
    d.polygon([(x - gen, y - 1), (x - gen + int(5 * s), arka_y), (x + gen - int(5 * s), arka_y), (x + gen, y - 1)], fill=hex2("#8a7a5a"))
    d.rectangle([x - gen + int(5 * s), arka_y - int(18 * s), x + gen - int(5 * s), arka_y], fill=hex2(tas))   # arka duvar
    rnd = random.Random(244)
    for _ in range(int(14 * s)):                                            # dökülmüş sıva lekeleri
        lx, ly = rnd.randint(x - gen + int(6 * s), x + gen - int(7 * s)), rnd.randint(arka_y - int(17 * s), arka_y - 2)
        d.rectangle([lx, ly, lx + rnd.randint(1, 3), ly + rnd.randint(1, 2)], fill=hex2("#a8927a"))
    d.chord([x - int(5 * s), arka_y - int(14 * s), x + int(5 * s), arka_y - int(4 * s)], 180, 360, fill=koyu)    # mihrap nişi
    d.rectangle([x - int(5 * s), arka_y - int(9 * s), x + int(5 * s), arka_y - int(1 * s)], fill=koyu)
    for k in (-1, 1):                                                       # yan duvarlar (perspektif)
        dx0, dx1 = x + k * gen, x + k * (gen - int(5 * s))
        d.polygon([(dx0, y - int(12 * s)), (dx1, arka_y - int(18 * s)), (dx1, arka_y), (dx0, y - 1)], fill=hex2(_ac(tas, -0.12 if k < 0 else -0.18)))
        d.line([dx0, y - int(12 * s), dx1, arka_y - int(18 * s)], fill=hex2(_ac(tas, 0.2)))
    for k, (mx, ml, mh) in enumerate(((-7.5, 6, 6.0), (7, 5, 5.0))):           # iki kabir: basamaklı beyaz mermer
        cx = x + int(mx * s)
        by = y - int(3 * s)
        d.rectangle([cx - int(ml * s), by - int(mh * 0.45 * s), cx + int(ml * s), by], fill=hex2("#e8e2d6"), outline=hex2("#8a8478"))
        d.rectangle([cx - int((ml - 1.2) * s), by - int(mh * s), cx + int((ml - 1.2) * s), by - int(mh * 0.45 * s)], fill=hex2("#f4f0e8"),
                    outline=hex2("#8a8478"))
        d.line([cx - int((ml - 2) * s), by - int(mh * s) - 1, cx + int((ml - 2) * s), by - int(mh * s) - 1], fill=hex2("#d8d2c4"))
    for k in (-1, 1):                                                       # ön alçak duvar, ortada giriş
        a, b = (x - gen, x - int(4 * s)) if k < 0 else (x + int(4 * s), x + gen)
        d.rectangle([a, y - int(2.2 * s), b, y - 1], fill=hex2(_ac(tas, -0.05)), outline=koyu)
        d.line([a, y - int(2.2 * s), b, y - int(2.2 * s)], fill=hex2(_ac(tas, 0.25)))


def levha(img, x, zemin, s=1.0):
    """Yeni figür: devlet levhası (koruma levhası). İki demir direk zemine gömülü (dibinde toprak), mavi tabela, beyaz
    yazı satırları (okunmaz, tasarım; içerik ekran kartında)."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 14 * s)
    temas_golgesi(img, x, y, 14 * s)
    for kx in (-5.5, 5.5):
        d.rectangle([x + int(kx * s) - _u(0.5, s), y - int(17 * s), x + int(kx * s) + _u(0.5, s), y - 1], fill=hex2("#3a3c40"))
        d.chord([x + int(kx * s) - _u(1.4, s), y - _u(1.2, s), x + int(kx * s) + _u(1.4, s), y + _u(1.2, s)], 180, 360, fill=hex2("#5a4a38"))
    x0, x1, y0, y1 = x - int(7.5 * s), x + int(7.5 * s), y - int(18 * s), y - int(8 * s)
    d.rectangle([x0, y0, x1, y1], fill=hex2("#1f4a8a"), outline=hex2("#e8ecf4"))
    d.rectangle([x0 + 1, y0 + 1, x1 - 1, y0 + _u(1.6, s)], fill=hex2("#1a3e76"))
    rnd = random.Random(42)
    for j, yy in enumerate(range(y0 + _u(2.6, s), y1 - _u(1, s), _u(1.3, s))):
        xx = x0 + _u(1, s)
        son = x1 - _u(1, s) - (rnd.randint(0, int(4 * s)) if j % 3 == 2 else 0)
        while xx < son:
            kl = rnd.randint(2, 6)
            d.line([xx, yy, min(son, xx + kl), yy], fill=hex2("#e8ecf4"))
            xx += kl + 2


def pece_yerde(img, x, zemin, s=1.0, renk="#ece4d4"):
    """Yeni figür: yere bırakılmış peçe: zemine yayılmış ince kumaş, kıvrımları ve gölgesiyle tamamen yerde."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 9 * s)
    temas_golgesi(img, x, y, 10 * s, alfa=90)
    d.polygon([(x - int(5 * s), y - 1), (x - int(3 * s), y - int(1.6 * s)), (x - int(0.5 * s), y - int(2.2 * s)), (x + int(2 * s), y - int(1.4 * s)),
               (x + int(4.5 * s), y - int(1.8 * s)), (x + int(5.5 * s), y - 1)], fill=hex2(renk))
    for kx in (-3, -1, 1.5, 3.5):
        d.line([x + int(kx * s), y - int(1.6 * s), x + int((kx + 0.6) * s), y - 1], fill=hex2(_ac(renk, -0.15)))
    d.line([x - int(4.5 * s), y - 1, x + int(5 * s), y - 1], fill=hex2(_ac(renk, -0.2)))


def uyuyan(img, x, zemin, s=1.0, yon=1, f=0.0):
    """Yeni figür: yerde yan yatmış uyuyan Raziye: başı bir bohçaya dayalı, gövde ve bacaklar zemine değer; külahı yanında
    yerde. Giysisinde mücevherler f ile sırayla parıldar (köylünün gördüğü). Nefesle gövde hafifçe kalkar."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 18 * s)
    temas_golgesi(img, x, y, 20 * s)
    nef = int(round((0.5 + 0.5 * SIN(f)) * 0.4 * s))
    g = hex2(RAZ["govde"])
    bx = x - int(5.6 * s) * yon                                             # baş tarafı: yere konmuş bohça (yastık)
    d.ellipse([min(bx, bx - int(4.6 * s) * yon), y - int(2.2 * s), max(bx, bx - int(4.6 * s) * yon), y - 1], fill=hex2("#8a7a5a"))
    d.line([bx - int(0.6 * s) * yon, y - int(1.6 * s), bx - int(4 * s) * yon, y - int(1.6 * s)], fill=hex2("#6a5a3e"))
    d.polygon([(x - int(6 * s) * yon, y - int(1 * s)), (x - int(5 * s) * yon, y - int(4.2 * s) - nef), (x + int(3 * s) * yon, y - int(4 * s) - nef),
               (x + int(4 * s) * yon, y - int(1 * s))], fill=g)
    d.rectangle([min(x + int(3 * s) * yon, x + int(9 * s) * yon), y - int(2 * s), max(x + int(3 * s) * yon, x + int(9 * s) * yon), y - 1],
                fill=hex2(_ac(RAZ["govde"], -0.3)))                         # bacaklar (şalvar)
    d.rectangle([min(x + int(9 * s) * yon, x + int(10.2 * s) * yon), y - int(1.6 * s), max(x + int(9 * s) * yon, x + int(10.2 * s) * yon), y - 1],
                fill=hex2(KOYU))
    d.line([x - int(5 * s) * yon, y - int(2.4 * s), x + int(3 * s) * yon, y - int(2.4 * s)], fill=hex2(ALTIN_R))   # kemer
    r = max(2, int(1.7 * s))
    hx, hy = x - int(7.6 * s) * yon, y - int(2.0 * s) - r
    d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=hex2(TEN))
    d.rectangle([min(hx, hx - r * yon), hy - r, max(hx, hx - r * yon), hy + r], fill=hex2("#2a1a12"))         # saç
    d.line([hx + int(0.4 * s) * yon, hy - _u(0.2, s), hx + int(1.2 * s) * yon, hy - _u(0.2, s)], fill=hex2(KOYU))  # kapalı göz
    kx = x + int(14.5 * s) * yon                                           # külah ayak ucunda yerde yan yatmış
    d.polygon([(kx, y - 1), (kx - int(4.5 * s) * yon, y - int(1.2 * s)), (kx, y - int(2.6 * s))], fill=hex2(RAZ["bas_renk"]))
    d.line([kx, y - 1, kx, y - int(2.6 * s)], fill=hex2(ALTIN_R), width=_u(0.6, s))
    for k, (mx, my) in enumerate(((-3, -3.2), (-1, -3.6), (1, -3.4), (-2, -2.4), (0.5, -2.6))):
        px_, py_ = x + int(mx * s) * yon, y + int(my * s) - nef
        piksel(img, px_, py_, hex2(("#e0b040", "#c8302a", "#3ab0a0", "#e0b040", "#f4f0e6")[k]))
        if int(f * 10 + k * 2) % 5 == 0:                                    # sırayla parıltı
            for dx_, dy_ in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                piksel(img, px_ + dx_, py_ + dy_, hex2("#fff4c0", 200))


def acik_kitap(img, x, zemin, s=1.0, f=0.0):
    """Yeni figür (yakın plan): rahle üstünde açık el yazması. Çapraz ahşap rahlenin ayakları zemine basar; sayfalarda
    mürekkep satırları (okunmaz, tasarım), sağ sayfada son satır yarım; yanında hokka ve kamış kalem."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 20 * s)
    temas_golgesi(img, x, y, 20 * s)
    ah = hex2("#6a4426")
    d.line([x - int(9 * s), y - 1, x + int(6 * s), y - int(9 * s)], fill=ah, width=_u(1.2, s))
    d.line([x + int(9 * s), y - 1, x - int(6 * s), y - int(9 * s)], fill=ah, width=_u(1.2, s))
    d.rectangle([x - int(10 * s), y - _u(1, s), x - int(7 * s), y - 1], fill=hex2("#4a2e18"))
    d.rectangle([x + int(7 * s), y - _u(1, s), x + int(10 * s), y - 1], fill=hex2("#4a2e18"))
    u = y - int(9 * s)
    sol = [(x - int(10 * s), u - int(1 * s)), (x, u + int(0.6 * s)), (x, u - int(5.4 * s)), (x - int(9.6 * s), u - int(6.6 * s))]
    sag = [(x + int(10 * s), u - int(1 * s)), (x, u + int(0.6 * s)), (x, u - int(5.4 * s)), (x + int(9.6 * s), u - int(6.6 * s))]
    d.polygon(sol, fill=hex2("#efe4c8"), outline=hex2("#8a7a5a"))
    d.polygon(sag, fill=hex2("#f4ead2"), outline=hex2("#8a7a5a"))
    d.line([x, u - int(5.4 * s), x, u + int(0.6 * s)], fill=hex2("#b8a888"))
    rnd = random.Random(1260)
    for k in range(6):                                                     # satırlar (sayfanın eğimini izler)
        for yon in (-1, 1):
            son = 8.4 if not (yon > 0 and k == 5) else 4.0
            xx = 0.8
            while xx < son:
                kl = rnd.uniform(0.6, 1.6)
                x_a, x_b = x + int(xx * s) * yon, x + int(min(son, xx + kl) * s) * yon
                yy = u - int((5.2 - k * 0.85) * s) - int(xx * 0.12 * s) + int(0.0 * s)
                d.line([x_a, yy, x_b, yy], fill=hex2("#3a2a1e"))
                if rnd.random() < 0.3:
                    piksel(img, x_a, yy - _u(0.5, s), hex2("#3a2a1e"))
                xx += kl + 0.35
    hx = x + int(12 * s)                                                    # hokka ve kalem (zeminde)
    d.ellipse([hx - int(1.4 * s), y - int(2.4 * s), hx + int(1.4 * s), y - 1], fill=hex2("#2a2a3a"), outline=hex2("#0a0a14"))
    d.rectangle([hx - _u(0.6, s), y - int(3 * s), hx + _u(0.6, s), y - int(2.2 * s)], fill=hex2("#2a2a3a"))
    d.line([hx, y - int(2.8 * s), hx + int(2.5 * s), y - int(8 * s)], fill=hex2("#c8a868"), width=_u(0.4, s))


def pece_ve_tac(img, x, zemin, s=1.0, f=0.0):
    """Yeni figür: alçak ahşap sehpa (dört ayak zemine basar), üstünde kadife yastık; solda katlanmış beyaz peçe, sağda
    yastıkta altın taç (taşları f ile parıldar). Son sorunun iki nesnesi yan yana."""
    d = ImageDraw.Draw(img)
    y = zemin_y(zemin, x, 22 * s)
    temas_golgesi(img, x, y, 22 * s)
    ust = y - int(6 * s)
    for ax in (-9.5, -6.5, 6.5, 9.5):
        d.rectangle([x + int(ax * s) - _u(0.5, s), ust, x + int(ax * s) + _u(0.5, s), y - 1], fill=hex2("#4a2e18"))
    d.rectangle([x - int(11 * s), ust - _u(1, s), x + int(11 * s), ust], fill=hex2("#6a4426"), outline=hex2("#2a1a0c"))
    d.line([x - int(11 * s), ust - _u(1, s), x + int(11 * s), ust - _u(1, s)], fill=hex2("#8a5a2e"))
    tu = ust - _u(1, s)
    # peçe (solda): katlanmış ince kumaş, uçları tabladan sarkar
    px0 = x - int(9 * s)
    d.polygon([(px0, tu), (px0 + int(1 * s), tu - int(2 * s)), (px0 + int(7.5 * s), tu - int(2.4 * s)), (px0 + int(8 * s), tu)], fill=hex2("#ece4d4"))
    d.line([px0 + int(1.5 * s), tu - int(1.2 * s), px0 + int(7.5 * s), tu - int(1.4 * s)], fill=hex2("#c8c0b0"))
    d.polygon([(px0, tu), (px0 - int(0.6 * s), tu + int(3 * s)), (px0 + int(1.2 * s), tu + int(2.6 * s)), (px0 + int(1.2 * s), tu)], fill=hex2("#e0d8c8"))
    # taç (sağda): kadife yastık + altın taç
    tx = x + int(5 * s)
    d.ellipse([tx - int(4.5 * s), tu - int(2 * s), tx + int(4.5 * s), tu + _u(0.4, s)], fill=hex2("#2a3a6a"))
    d.line([tx - int(3.5 * s), tu - int(1.6 * s), tx + int(3.5 * s), tu - int(1.6 * s)], fill=hex2("#3a5a9a"))
    tb = tu - int(1.6 * s)
    d.rectangle([tx - int(3 * s), tb - int(2.2 * s), tx + int(3 * s), tb], fill=hex2(ALTIN_R), outline=hex2("#6a4a10"))
    for dx in (-3, -1, 1, 3):
        d.polygon([(tx + int(dx * s) - _u(0.7, s), tb - int(2.2 * s)), (tx + int(dx * s), tb - int(4 * s)),
                   (tx + int(dx * s) + _u(0.7, s), tb - int(2.2 * s))], fill=hex2(ALTIN_R))
    for k, (dx, renk) in enumerate(((-2, "#c8302a"), (0, "#2a8a8a"), (2, "#c8302a"))):
        piksel(img, tx + int(dx * s), tb - int(1.1 * s), hex2(renk))
        if int(f * 12 + k * 4) % 6 == 0:
            for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                piksel(img, tx + int(dx * s) + a, tb - int(1.1 * s) + b, hex2("#fff4c0", 200))


def kitap_elde(img, x, z0, s, yon, kol):
    """Diz çökmüş kisi'nin (diz=True) uzattığı elde ciltli kitap (Tabakât-ı Nâsırî'nin sunuluşu)."""
    d = ImageDraw.Draw(img)
    yy = z0 + int(3.6 * s)
    ust = yy - int(11 * s)
    ex, ey = x + int(3.5 * s) * yon, ust - int(4 * s * kol) + int(1 * s)
    d.rectangle([min(ex, ex + int(3.2 * s) * yon), ey - int(2.2 * s), max(ex, ex + int(3.2 * s) * yon), ey + int(0.6 * s)],
                fill=hex2("#6a2a1a"), outline=hex2("#2a0a04"))
    d.line([ex + _u(0.4, s) * yon, ey - int(0.8 * s), ex + int(2.8 * s) * yon, ey - int(0.8 * s)], fill=hex2(ALTIN_R))


# ==========================================================================
# ÖLÇEK, KADRAJ VE YAZI BANDI DENETİMLERİ (cem_sultan.py / orhun_yazitlari.py / celebi_mehmed_paris.py kalıbı).
# Yeni çizim fonksiyonu DEĞİL: figürü boş yüzeye çizip alfa kanalından ölçer; sprite ve orta planı denetler.
# ==========================================================================
def _bb(img):
    return img.getchannel("A").getbbox()


TSX = Path(__file__).parents[1] / "src" / "sahneler" / "RaziyeSultan.tsx"
_BANT = {}


def _tsx_bantlari():
    """RaziyeSultan.tsx'teki her Bolum için (yakin, yazı alt kenarı, yazı üst kenarı) (ızgara y). Yazı yüksekliği
    TimurSeri.tsx Yazi bileşeninin formülüyle: satır boyu = min(boy, (1080-130)/(en uzun satır · 0,46)), satır aralığı 1,12."""
    if _BANT:
        return _BANT
    metin = TSX.read_text()
    govde = metin[metin.index("bolumler:"):metin.index("kapanis:")]
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
            alt = max(alt, (ust + len(sat) * sig * 1.12 + 8) / 2)
        _BANT.setdefault(no, []).append((yk, alt, ust / 2))
    return _BANT


def _yk(no):
    return _tsx_bantlari()[no][-1][0]


def _ust_limit(no, taban, pay=6):
    """Yazı bandının en alt dünya y'si (sahnenin bütün kartları ve sahne sonu yakınlaşması yakin·1.06 için) + pay."""
    o = taban - 12
    return max(o - (o - alt) / (yk * 1.06) for yk, alt, _ in _tsx_bantlari()[no]) + pay


def _bant_denetimi(no, w, h, taban, pay=4):
    """Sprite'ta ve orta planda, görünür sütunlarda, yazı bandı satırlarında 2 pikselden fazla opak piksel olmamalı
    (1-2 piksellik kandil zinciri hariç). Kapak dahil her Bolum ve sahne başı/sonu yakınlaşması için."""
    pub = Path(__file__).parents[1] / "public"
    spr = Image.open(pub / f"sahne{no}-karakter.png").convert("RGBA").getchannel("A")
    ort = Image.open(pub / f"sahne{no}-orta.png").convert("RGBA").getchannel("A")
    o = taban - 12
    for yk, alt, ust in _tsx_bantlari()[no]:
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
            for y in range(y0, y1 + 1):
                if sum(ort.crop((PAY + int(270 - yar - 30), y, PAY + int(270 + yar + 30), y + 1)).histogram()[1:]) > 2:
                    raise RuntimeError(f"Sahne {no}: orta plandaki yapı yazı bandına giriyor: y {y} (bant {y0}-{y1})")


_ONBELLEK = {}


def olcek(ad, yakin, cizim, oran=0.30):
    """Figür kutusu kadraj yüksekliğinin >= oran'ı olan en küçük s (0.1 adım). Görünen ızgara yüksekliği = 960/yakin."""
    anahtar = (ad, yakin, oran)
    if anahtar in _ONBELLEK:
        return _ONBELLEK[anahtar]
    hedef = oran * 960 / yakin
    s = 1.0
    while s <= 12.0:
        t = yeni(600, 560)
        cizim(t, round(s, 1), duz(557, 600))
        bb = _bb(t)
        if bb and bb[1] <= 1:
            break
        if bb and bb[3] - bb[1] >= hedef:
            _ONBELLEK[anahtar] = round(s, 1)
            return _ONBELLEK[anahtar]
        s += 0.1
    raise RuntimeError(f"olcek({ad}, yakin={yakin}): %{int(oran * 100)} boya ulaşılamadı")


def _boy(cizim, s):
    t = yeni(600, 560)
    cizim(t, s, duz(557, 600))
    bb = _bb(t)
    return bb[3] - bb[1]


def _sigdir(cizim, hmax, s0=1.0, s1=12.0):
    """Çizimin kutu yüksekliği hmax'ı aşmayan en büyük s (0.1 adım)."""
    s, iyi = s0, s0
    while s <= s1:
        if _boy(cizim, round(s, 1)) > hmax:
            break
        iyi = round(s, 1)
        s += 0.1
    return iyi


def _olc(no, cizim, oran=0.30, ic=False, geri=0, ad=None):
    """Hedef oranı (kadraj yüksekliğinin) karşılayan en küçük ölçek; yazı bandına değecekse sığan en büyük ölçek."""
    taban = IT if ic else DT
    yk = _yk(no)
    hmax = (taban - geri) - _ust_limit(no, taban)
    s = olcek((ad or id(cizim), no, geri), yk, cizim, oran)
    if _boy(cizim, s) <= hmax:
        return s
    return _sigdir(cizim, hmax)


def _K(no, ic=False, oran=0.30, geri=0, govde=ILTUTMIS):
    """Ayakta insan ölçeği (sarıklı adam kutusu kadrajın %30'u; yazıya sığmazsa sığan en büyük)."""
    return _olc(no, lambda t, s, z: figur(t, kisi, 280, z, s, **govde), oran, ic, geri, ad=("kisi", govde["bas"]))


def _A(no, oran=0.42, geri=0):
    """Atlı ölçeği (at + binici + külah); insan/at oranı için kisi = atli·2.6/2.9 (SKILL.md)."""
    return _olc(no, lambda t, s, z: figur(t, atli, 280, z, s, 1, dur=True, govde=RAZ["govde"], bas="kulah", bas_renk="#3a2a4a"),
                oran, False, geri, ad="atli")


def _kz(yakin, taban=IT, h=IH):
    """Kandil zinciri: sprite'ın üst kenarından (tavan) kadrajın üst kenarının biraz altına."""
    ust_gorunen = (taban - 12) * (1 - 1 / yakin)
    return max(40, int(ust_gorunen - (taban - h)) + 10)


def _kadraj(no, kare, w, h, yakin, esik=0.75):
    """Görünür aralık yerel x = w/2 ± 270/yakin. Tam opak piksellerin hepsi sahne sonu yakınlaşmasında (yakin·1.06) da
    görünür aralıkta olmalı (kenarda kesilen figür/eşya yok); opak piksellerin en az `esik` oranı içeride; figür sprite'ın
    üstüne değmemeli (kesik baş). Kandil halesi gibi yarı saydam ışık sayılmaz."""
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
        tam = alfa.point(lambda v: 255 if v > 200 else 0).getbbox()
        y2 = 270 / (yakin * 1.06)
        if tam and (tam[0] < w / 2 - y2 + 3 or tam[2] > w / 2 + y2 - 3):
            raise RuntimeError(f"Sahne {no}: kare {i}, figürler x {tam[0]}-{tam[2]}, görünür aralık "
                               f"{int(w / 2 - y2)}-{int(w / 2 + y2)}: kenarda kesilen figür var")
        ici = sum(alfa.crop((a, 0, b, h)).histogram()[1:])
        if ici / toplam < esik:
            raise RuntimeError(f"Sahne {no}: figürlerin %{int(100 * ici / toplam)}'i görünür aralıkta (x {a}-{b})")


def _gorunur(no, xler, sx0=270, sx1=270, pay=14):
    """Orta plandaki önemli figürlerin ızgara x'i (PAY'sız), sprite'ın başlangıç ve bitiş sx'inde, sahne sonu
    yakınlaşmasında görünür aralıkta."""
    yk = _yk(no) * 1.06
    for sx in (sx0, sx1):
        a, b = sx - 270 / yk + pay, sx + 270 / yk - pay
        for x in xler:
            if not a <= x <= b:
                raise RuntimeError(f"Sahne {no}: orta plan figürü x={x} görünür aralık [{int(a)}, {int(b)}] dışında")


def _spr(no, kare, ic=False, esik=0.75):
    """Kadraj + taban denetimi, sprite'ı kaydet, sonra yazı bandı denetimi (sprite ve orta plan)."""
    w, h, taban = (IW, IH, IT) if ic else (DW, DH, DT)
    _kadraj(no, kare, w, h, _yk(no), esik)
    sprite(no, "karakter", w, h, KARE, kare)       # taban_denetimi varsayılan açık
    _bant_denetimi(no, w, h, taban)


# ==========================================================================
# KATMAN YARDIMCILARI VE PALETLER
# ==========================================================================
def _gok(no, renkler, yildiz=0, y0=380, y1=560):
    """Gökyüzü + (gece) görünür bölgeye yıldız: sahneler.gokyuzu yıldızları y<300'e serper, yakın çekimde görünen gök
    y≈380-560 arasıdır. Ay ve güneş yok: yakın çekimde yazı bandına düşerdi."""
    img = gokyuzu(no, renkler, None, (), ("#fff8ec", "#f4dcc8", "#d8a8a0"), 0)
    if yildiz:
        rnd = random.Random(no * 13)
        for _ in range(yildiz):
            x, y = rnd.randrange(img.width), rnd.randrange(y0, y1)
            a = rnd.choice((110, 170, 255))
            piksel(img, x, y, hex2("#fff8e0", a))
            if a == 255 and rnd.random() < 0.3:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    piksel(img, (x + dx) % img.width, y + dy, hex2("#fff8e0", 80))
    kaydet(img, f"sahne{no}-gokyuzu.png")


PALET = {
    # Delhi gündüzü: puslu sıcak ufuk, düz ova, toprak avlu
    "gun": dict(gok=["#5a86b8", "#7a9cc4", "#9ab2cc", "#bcc6cc", "#dcd2bc", "#ecdcb4"],
                dag=["#9a9aa8", "#8a8a9a"], tepe=["#a8a088", "#98907a"], ova=["#c0aa7a", "#b29c6e", "#a48e62"],
                orta=["#c8a874", "#ba9a68", "#ac8c5e", "#9e7e54", "#90704a"], kenar="#e8d4a0",
                on=["#8a6a44", "#9a7a4e", "#aa8a58"], isik="#e0c890"),
    "ikindi": dict(gok=["#4a6aa0", "#7a88b0", "#b49aa8", "#dcb094", "#ecc490", "#f4d4a0"],
                   dag=["#8a7a94", "#7a6c88"], tepe=["#a08a7a", "#907c6e"], ova=["#c09a6a", "#b28c60", "#a48056"],
                   orta=["#b8945e", "#aa8656", "#9c7a4e", "#8e6e46", "#80623e"], kenar="#e8c88c",
                   on=["#6a5030", "#7a5c38", "#8a6a42"], isik="#e8c88c"),
    "aksam": dict(gok=["#2a2a58", "#5a3a6a", "#a05078", "#d07a78", "#e8a080", "#f0bc90"],
                  dag=["#6a4a6a", "#5a3e5a"], tepe=["#7a5a6a", "#6a4a5a"], ova=["#8a6a54", "#7a5c48", "#6a503e"],
                  orta=["#7a6444", "#6c583c", "#5e4c34", "#50402c", "#423424"], kenar="#c0a070",
                  on=["#423424", "#50402c", "#5e4c34"], isik="#c0a070"),
    "kizil": dict(gok=["#2a1430", "#5a2236", "#8a3238", "#b84a38", "#d8683a", "#e88a48"],
                  dag=["#5a2a30", "#4a2228"], tepe=["#6a3430", "#5a2c2a"], ova=["#7a4434", "#6a3a2e", "#5a3028"],
                  orta=["#6a4430", "#5c3a2a", "#4e3224", "#422a1e", "#362218"], kenar="#c07850",
                  on=["#362218", "#422a1e", "#4e3224"], isik="#c07850"),
    "gece": dict(gok=["#070a1c", "#0e1430", "#162046", "#1e2c5a", "#28386a", "#324478"],
                 dag=["#1a2240", "#161d38"], tepe=["#1e2846", "#19223e"], ova=["#22304a", "#1e2a42", "#1a253a"],
                 orta=["#2e3a4a", "#283342", "#222c3a", "#1c2532", "#161e2a"], kenar="#5a6a8a",
                 on=["#161e2a", "#1c2532", "#222c3a"], isik="#5a6a8a"),
    "safak": dict(gok=["#2a3a6a", "#5a5a8a", "#a87a8a", "#e8a07a", "#f8c890", "#fce0a8"],
                  dag=["#7a6a98", "#6a5a88"], tepe=["#8a8a7a", "#7a7a6c"], ova=["#a8a86a", "#98985e", "#8a8c54"],
                  orta=["#8a9a54", "#7c8c4a", "#6e7e42", "#60703a", "#526232"], kenar="#d0c888",
                  on=["#526232", "#60703a", "#6e7e42"], isik="#d8d090"),
}


def _dis(no, palet, ekle=None, dag_y=(470, 500), tepe_y=506, ova_y=516, yildiz=0, orta_ust=(548, 556), on_boy=120, bos_on=False):
    """Dış mekân katmanları (Delhi ovası: dağ yok, alçak sırt; ufuk yazı bandının altında)."""
    p = PALET[palet]
    _gok(no, p["gok"], yildiz)
    uzak(no, p["dag"], p["tepe"], p["ova"], dag_y=dag_y, tepe_y=tepe_y, ova_y=ova_y)
    orta(no, orta_ust, p["orta"], p["kenar"], ekle=ekle)
    if bos_on:
        kaydet(yeni(GW, H), f"sahne{no}-on.png")
    else:
        on(no, p["on"], p["isik"], boy=on_boy)


SARAY = dict(duvar=("#26302e", "#30403a", "#3e5048"), kemer="#16201c", cini="#c8a040",
             pencere=("#2a3a5a", "#f4d8a0"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"), isik="#f8c060", hali=True)
SARAY_GECE = dict(duvar=("#14181e", "#1c2228", "#262e34"), kemer="#0a0e12", cini="#8a6a30",
                  pencere=("#0e1630", "#4a5a8a"), zemin_renk=("#3a3028", "#30281e", "#282018"), isik="#f8c060", hali=True)
ZINDAN = dict(duvar=("#1e1e22", "#28282c", "#323236"), kemer="#121214", cini="#3a3a3e",
              pencere=("#0e1630", "#6a7aa8"), zemin_renk=("#3a3630", "#302c28", "#282420"), isik="#c8a060", hali=False)
CALISMA = dict(duvar=("#2e2620", "#3c3028", "#4a3c30"), kemer="#1e1814", cini="#2a6a7a",
               pencere=("#14203a", "#c8d4f0"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"), isik="#f8c060", hali=True)
DARPHANE = dict(duvar=("#3a2418", "#4a2e20", "#5a3a28"), kemer="#24140c", cini="#8a5a30",
                pencere=None, zemin_renk=("#4a3a2e", "#3e3026", "#32261e"), isik="#f89040", hali=False)


def _oda(no, palet):
    ic_mekan(no, **palet)


def _zemin_satir(no, y, renk):
    """Orta planda düz bir satırdan aşağısını tek renk zemin yapar (avlu taşı, sokak)."""
    def ekle(img, z):
        d = ImageDraw.Draw(img)
        d.rectangle([0, y, GW, H], fill=hex2(renk))
        for yy in range(y + 6, H, 10):
            d.line([0, yy, GW, yy], fill=hex2(_ac(renk, -0.08)))
    return ekle


def _cimen(t, z, f, renkler, tohum, no, boy=6):
    """Sprite'ın zemin satırında rüzgârla salınan çimen (dibi zemine basar); yalnızca sahne sonu yakınlaşmasında da
    görünen aralıkta (kenarda kesik tutam kalmasın)."""
    from ciz import cimen_tutamlari
    yar = int(270 / (_yk(no) * 1.06)) - 10
    cimen_tutamlari(t, z, renkler, tohum, 0.45, boy, t.width // 2 - yar, t.width // 2 + yar, ruzgar=0.6 * SIN(f))


def sokak_evleri(img, x0, x1, zemin, s=1.0, tohum=1):
    """Yeni figür: eski Delhi'nin dar sokağı: bitişik, iki-üç katlı, düz damlı tuğla/sıva evler; kemerli kapılar, kafesli
    çıkma pencereler (cumba), damda alçak korkuluk. Düz zemine kurulur; her ev tabanı zemin satırında."""
    d = ImageDraw.Draw(img)
    y = duz_zemin(zemin, x0, x1, "sokak", tolerans=3)
    rnd = random.Random(tohum)
    temas_golgesi(img, (x0 + x1) // 2, y, x1 - x0)
    x = x0
    while x < x1:
        gen = min(int(rnd.uniform(14, 22) * s), x1 - x)
        if gen < int(6 * s):
            break
        kat = rnd.choice((2, 2, 3))
        yuk = int(kat * 9 * s)
        renk = rnd.choice(("#c8a888", "#b89878", "#d0b898", "#a88a6a", "#c0a080"))
        d.rectangle([x, y - yuk, x + gen, y - 1], fill=hex2(renk))
        d.rectangle([x, y - yuk - _u(1.6, s), x + gen, y - yuk], fill=hex2(_ac(renk, -0.2)))       # dam korkuluğu
        d.line([x + gen, y - yuk, x + gen, y - 1], fill=hex2(_ac(renk, -0.3)))
        for k in range(int(6 * s)):                                                               # eskimiş sıva
            piksel(img, rnd.randint(x + 1, x + gen - 1), rnd.randint(y - yuk + 2, y - 2), hex2(_ac(renk, -0.12)))
        kx = x + gen // 2
        d.rectangle([kx - int(2 * s), y - int(7 * s), kx + int(2 * s), y - 1], fill=hex2("#3a2a1e"))
        d.chord([kx - int(2 * s), y - int(9 * s), kx + int(2 * s), y - int(5 * s)], 180, 360, fill=hex2("#3a2a1e"))
        for k in range(1, kat):
            py = y - int(k * 9 * s) - int(6 * s)
            if rnd.random() < 0.6:                                                                # çıkma pencere
                d.rectangle([kx - int(3.5 * s), py, kx + int(3.5 * s), py + int(5 * s)], fill=hex2("#6a4a2e"))
                for c in range(-3, 4, 2):
                    d.line([kx + int(c * s), py + 1, kx + int(c * s), py + int(5 * s) - 1], fill=hex2("#3a2a1a"))
                d.rectangle([kx - int(4 * s), py + int(5 * s), kx + int(4 * s), py + int(5.8 * s)], fill=hex2("#4a3220"))
            else:
                d.rectangle([kx - int(1.5 * s), py + int(1 * s), kx + int(1.5 * s), py + int(4.5 * s)], fill=hex2("#2a2a32"))
        x += gen + 1


# ==========================================================================
# SAHNELER
# ==========================================================================
def _kisi(t, x, z, s, kim, **kw):
    a = dict(kim)
    a.update(kw)
    figur(t, kisi, x, z, s, **a)


def _oturan(t, x, z, s, kim, **kw):
    a = {k: v for k, v in kim.items() if k in ("govde", "bas", "bas_renk", "sakal", "ten")}
    a.update(kw)
    figur(t, oturan, x, z, s, **a)


def _tahtta(t, x, z, so, kim, yon=-1):
    """Taht (kalender.taht, ölçek so·0.52) ve üstünde oturan kişi (ölçek so)."""
    ust = figur(t, taht, x, z, round(0.52 * so, 2), renk="#c8a040", ortu="#2a3a6a")
    _oturan(t, x, duz(ust, t.width), so, kim, yon=yon)


def _S_tahtta(no, kim=ILTUTMIS_O, oran=0.32):
    return _olc(no, lambda t, s, z: _tahtta(t, 280, z, s, kim), oran, ic=True, ad=("tahtta", kim["bas"]))


def _S_oturan(no, kim=MINHAC, oran=0.24, ic=True):
    return _olc(no, lambda t, s, z: _oturan(t, 280, z, s, kim, yon=1), oran, ic=ic, ad=("oturan", kim["bas"]))


def sahne210():
    """Kart 1-2 (ve kapak): Delhi, Kasım 1236, Cuma sabahı. Arkada avlunun sivri kemerli revakı (adı verilmez, minaresiz),
    önünde dinleyen kalabalık; önde taş sekide peçeli Raziye kolunu kaldırıp halka konuşur, iki dinleyici ona döner."""
    no = 210

    def ekle(img, z):
        figur(img, revak, PAY + 40, PAY + 500, duz(586), 2.3)
        kalabalik(img, duz(590), PAY + 150, PAY + 330, 8, 210, ("#5a4a3a", "#3a4a5a", "#6a5a4a", "#7a6a5a"), s=2.1, yon=1, bas="sarik")

    _dis(no, "gun", ekle=ekle)
    K = min(_K(no), _K(no, geri=10, govde=RAZ_PECE))

    def kare(t, z, i):
        f = i / KARE
        _kisi(t, 140, z, K, EMIR3, yon=1, kemer=None)
        _kisi(t, 178, z, K, dict(govde="#3a4a5a", bas="sarik", bas_renk="#e8e0d0", sakal="#3a2a1a"), yon=1, kemer=None)
        ust = figur(t, seki, 222, 282, z, 10)
        _kisi(t, 254, duz(ust, t.width), K, RAZ_PECE, yon=-1, kol=0.45 + 0.25 * SIN(f))

    _spr(no, kare)


def sahne211():
    """Kart 3: alacakaranlıkta uçsuz ova (Kaithal'in habercisi): peçeli Raziye yalnız, sağa bakar; geride yaşlı ağaç,
    önde rüzgârda salınan otlar."""
    no = 211

    def ekle(img, z):
        figur(img, agac, PAY + 200, duz(588), 1.5, tohum=211)

    _dis(no, "aksam", ekle=ekle, dag_y=(500, 518), tepe_y=522, ova_y=530, orta_ust=(556, 562), on_boy=150)
    K = _K(no, govde=RAZ_PECE)

    def kare(t, z, i):
        f = i / KARE
        _kisi(t, 210, z, K, RAZ_PECE, yon=1)
        _cimen(t, z, f, ["#7a6a44", "#6a5a3a", "#8a7a52"], 211, no, boy=8)

    _spr(no, kare)


def sahne212():
    """Kart 4 ve 44: boş taht. Tavandan kandil, iki yanda şamdan; tahtın önündeki halıya sıcak ışık düşer."""
    no = 212
    _oda(no, SARAY)
    yk = _yk(no)
    st = _olc(no, lambda t, s, z: figur(t, taht, 280, z, s, renk="#c8a040", ortu="#2a3a6a"), 0.33, ic=True, ad="taht")

    def kare(t, z, i):
        f = i / KARE
        for r in range(10, 70, 6):                                         # yerde ışık havuzu
            for a in range(0, 360, 5):
                px_, py_ = 200 + math.cos(math.radians(a)) * r * 1.4, z[0] - 3 + math.sin(math.radians(a)) * r * 0.12
                if (int(px_) + int(py_)) % 2 == 0 and py_ < z[0]:
                    piksel(t, px_, py_, hex2("#f8d070", int(70 * (1 - r / 70))))
        kandil(t, 200, 0, f, zincir=_kz(yk))
        figur(t, taht, 200, z, st, renk="#c8a040", ortu="#2a3a6a")
        mumluk(t, 136, z, f, 3)
        mumluk(t, 264, z, (f + 0.5) % 1, 3)

    _spr(no, kare, ic=True)


def sahne213():
    """Kart 5: karanlık oda, tek kandil: peçeli Raziye yakın plan, sola döner; yüzü görünmez, yalnızca gözleri."""
    no = 213
    _oda(no, SARAY_GECE)
    yk = _yk(no)
    K = _K(no, ic=True, oran=0.32, govde=RAZ_PECE)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 240, 0, f, zincir=_kz(yk))
        mumluk(t, 150, z, f, 1)
        _kisi(t, 214, z, K, RAZ_PECE, yon=-1, kol=0.04 * (1 + SIN(f)))

    _spr(no, kare, ic=True)


def sahne214():
    """Kart 6: saray, 1231 öncesi: Sultan İltutmış (eski köle; kır sakal, mor kaftan) tahtta; sol köşede saray tarihçisi
    Minhâc (o yıllarda orta yaşlı, koyu sakal) minderde rahlesine yazar. Kandil."""
    no = 214
    _oda(no, SARAY)
    yk = _yk(no)
    so = _S_tahtta(no)
    sm = round(so * 0.95, 1)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, zincir=_kz(yk))
        _tahtta(t, 250, z, so, ILTUTMIS_O)
        _oturan(t, 146, z, sm, MINHAC_GENC, yon=1, el="kalem", minder="#5a6a3a")
        rahle(t, 146 + int(4.2 * sm), z[0], round(0.9 * sm, 1))

    _spr(no, kare, ic=True)


def sahne215():
    """Kart 7: Delhi'nin kapısı, 1231: atlı Sultan İltutmış kolunu kaldırıp Gwalior yoluna (sağa) yönelir; geride sağa
    yürüyen ordunun atlıları; sol önde peçeli kızı kapıda kalır (yönetim ona bırakılıyor)."""
    no = 215

    def ekle(img, z):
        figur(img, orta_asya_sehri, PAY + 40, PAY + 230, duz(586), 1.7, tohum=215, kerpic="#c08a6a", golge="#8a5a44", kubbe="#9a9a8a")
        for j, x in enumerate(range(290, 420, 26)):
            figur(img, atli, PAY + x, duz(592), 1.25, 1, faz=(j * 0.31) % 1, govde=("#5a5a6a", "#4a3a2a")[j % 2], bas="migfer",
                  bas_renk="#8a8a90", adim=0.4)

    _dis(no, "gun", ekle=ekle)
    A = _A(no, 0.40)
    K = round(A * 2.6 / 2.9, 1)

    def kare(t, z, i):
        f = i / KARE
        _kisi(t, 134, z, K, RAZ_PECE, yon=1)
        figur(t, atli, 238, z, A, 1, faz=f, dur=True, govde=ILTUTMIS["govde"], bas="sarik", bas_renk="#f4f0e6",
              sakal=ILTUTMIS["sakal"], kol=0.35 + 0.1 * SIN(f), at_renk="#e8e0d0", yele="#8a8478")

    _spr(no, kare)


def sahne216():
    """Kart 8-9: divan: İltutmış ve peçeli kızı yan yana (sola bakar); karşılarında iki Türk emîri, öndeki elini kaldırıp
    itiraz eder (Oğulların varken?)."""
    no = 216
    _oda(no, SARAY)
    yk = _yk(no)
    K = _K(no, ic=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 196, 0, f, zincir=_kz(yk))
        _kisi(t, 128, z, K, EMIR2, yon=1)
        _kisi(t, 160, z, K, EMIR1, yon=1, kol=0.35 + 0.25 * max(0.0, SIN(f, 2)))
        _kisi(t, 228, z, K, ILTUTMIS, yon=-1, kol=0.1)
        _kisi(t, 262, z, K, RAZ_PECE, yon=-1)

    _spr(no, kare, ic=True)


def sahne217():
    """Kart 10 ve 50 (motif, ALTIN): İltutmış ve kızı karşı karşıya, sessiz; babanın eli hafifçe kızına uzanır. Şamdan."""
    no = 217
    _oda(no, SARAY)
    yk = _yk(no)
    K = _K(no, ic=True, oran=0.31)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 206, 0, f, zincir=_kz(yk))
        mumluk(t, 132, z, f, 3)
        _kisi(t, 182, z, K, ILTUTMIS, yon=1, kol=0.12 + 0.03 * SIN(f))
        _kisi(t, 236, z, K, RAZ_PECE, yon=-1)

    _spr(no, kare, ic=True)


def sahne218():
    """Kart 11: 30 Nisan 1236. Solda sehpada yeşil örtülü tabut (İltutmış); sağda genç Fîrûz tahta oturtulmuş; aradaki emîr
    kolunu ona uzatır (emîrler oğlu seçiyor)."""
    no = 218
    _oda(no, SARAY_GECE)
    yk = _yk(no)
    so = _S_tahtta(no, FIRUZ)
    K = _K(no, ic=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, zincir=_kz(yk))
        figur(t, sehpa_tabut, 144, z, round(0.36 * K, 2))
        _kisi(t, 198, z, K, EMIR1, yon=1, kol=0.3 + 0.03 * SIN(f))
        _tahtta(t, 256, z, so, FIRUZ)

    _spr(no, kare, ic=True)


def sahne219():
    """Kart 12: gece: genç Fîrûz minderde, önünde meyve sinisi (eğlence; kadeh çizilmez); sağda ayakta, karanlıkta annesi
    Şah Terken (kancanın faili)."""
    no = 219
    _oda(no, SARAY_GECE)
    yk = _yk(no)
    K = _K(no, ic=True, govde=SAH_TERKEN)
    so = round(K * 0.98, 1)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 196, 0, f, zincir=_kz(yk))
        _oturan(t, 140, z, so, FIRUZ, yon=1, minder="#8a6a2a")
        figur(t, meyve_tepsisi, 188, z, round(0.75 * so, 1))
        _kisi(t, 258, z, K, SAH_TERKEN, yon=-1, kol=0.05 + 0.03 * SIN(f))

    _spr(no, kare, ic=True)


def sahne220():
    """Kart 13: o Cuma: halk sağa, sarayın kapısına yürür (kalabalık sarayı basıyor); geride taş sekide kolunu kaldırmış
    peçeli Raziye. Sprite sağa kayar, yürüyenlerin adımı kaymayla uyumlu."""
    no = 220

    def ekle(img, z):
        figur(img, orta_asya_sehri, PAY + 300, PAY + 560, duz(586), 1.8, tohum=220, kerpic="#c08a6a", golge="#8a5a44", kubbe="#9a9a8a")
        u = figur(img, seki, PAY + 210, PAY + 240, duz(590), 5)
        figur(img, kisi, PAY + 225, duz(u), 2.2, **dict(RAZ_PECE, yon=1, kol=0.7))
        kalabalik(img, duz(592), PAY + 250, PAY + 330, 9, 220, ("#5a4a3a", "#3a4a5a", "#6a5a4a"), s=2.0, yon=1, bas="sarik", adim=0.3)

    _gorunur(no, [225], 245, 295)
    _dis(no, "gun", ekle=ekle)
    K = _K(no)
    renk = (("#5a4a3a", "sarik", "#e8e0d0"), ("#3a4a5a", "kalpak", "#3a2a1a"), ("#6a5a3a", "sarik", "#f0e8d8"),
            ("#4a3a4a", "bork", "#5a3a22"))

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((122, 162, 204, 246)):
            g, b, br = renk[j]
            _kisi(t, x, z, round(K * (0.96 if j % 2 else 1.0), 1), dict(govde=g, bas=b, bas_renk=br, sakal="#2a1a12"), yon=1,
                  adim=(f * 2 + j * 0.37) % 1, kemer=None, kol=0.5 if j == 1 else 0.0)

    _spr(no, kare)


def sahne221():
    """Kart 14: taht odası: peçeli Raziye tahtta (sağda); solda Şah Terken'i bir muhafız götürür (ikisi de çıkışa, sola
    döner). Kandil."""
    no = 221
    _oda(no, SARAY)
    yk = _yk(no)
    so = _S_tahtta(no, RAZ_O_PECE)
    K = _K(no, ic=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 206, 0, f, zincir=_kz(yk))
        _kisi(t, 132, z, K, SAH_TERKEN, yon=-1)
        _kisi(t, 172, z, K, ASKER, yon=-1, silah="kalkan", kol=0.05)
        _tahtta(t, 254, z, so, RAZ_O_PECE)

    _spr(no, kare, ic=True)


def sahne222():
    """Kart 15: zindan: Fîrûz taş zeminde, samanın üstünde oturur; kapıda meşaleli gardiyan. Pencereden gece."""
    no = 222
    _oda(no, ZINDAN)
    K = _K(no, ic=True, govde=ASKER)
    so = round(K * 0.98, 1)
    rnd = random.Random(222)
    saman = [(rnd.randint(100, 210), rnd.randint(0, 2), rnd.choice(("#c8b060", "#a89048", "#d8c070"))) for _ in range(90)]

    def kare(t, z, i):
        f = i / KARE
        for x, dy, renk in saman:
            piksel(t, x, z[0] - dy, hex2(renk))
        _oturan(t, 156, z, so, FIRUZ, yon=1)
        _kisi(t, 250, z, K, ASKER, yon=-1, silah="mesale", kol=0.35 + 0.03 * SIN(f))

    _spr(no, kare, ic=True)


def _sikke_sahnesi(no, tur):
    ic_mekan(no, duvar=("#1a1410", "#221a14", "#2a2018"), kemer="#120c08", cini="#5a3a20", pencere=None,
             zemin_renk=("#4a2e1c", "#3e2616", "#321e12"), isik="#f8c060", hali=False)
    r = 30
    while True:
        t = yeni(IW, IH)
        sikke_yuva(t, 200, duz(IH - 1, IW), r + 1, tur)
        if (IH - 1) - _bb(t)[1] > IT - _ust_limit(no, IT) or r > 60:
            break
        r += 1

    def kare(t, z, i):
        f = i / KARE
        isik = 0.0 if tur == "baba" else 0.78 + 0.22 * SIN(f)
        figur(t, sikke_yuva, 200, z, r, tur, isik, f)

    _spr(no, kare, ic=True)


def sahne223():
    """Kart 16 (KIZIL): yakın plan: babası İltutmış'ın adıyla basılmış gümüş sikke ahşap yuvaya dikili; yüzünde soldan
    sağa ince bir parıltı kayar. Yazı kûfî benzeri tasarım, okunmaz."""
    _sikke_sahnesi(223, "baba")


def sahne224():
    """Kart 17: darphane, 1237: usta örsteki kalıba çekiçle vurur (f 0-0.5 kalkar, sonra iner); solda mangalda kor."""
    no = 224
    _oda(no, DARPHANE)
    K = _K(no, ic=True, govde=USTA)
    so_ = round(K * 0.62, 1)

    def kare(t, z, i):
        f = i / KARE
        mangal(t, 130, z, f)
        ux = 196
        kol = 0.15 + 0.75 * (0.5 + 0.5 * math.cos(f * 2 * math.pi))
        _kisi(t, ux, z, K, USTA, yon=1, kol=kol)
        ex, ey = _el(ux, z[0], K, 1, kol)
        d = ImageDraw.Draw(t)
        bx, by = ex + int(2.6 * K), ey - int(0.4 * K)
        d.line([ex, ey, bx, by], fill=hex2("#6a4426"), width=_u(0.5, K))                     # çekiç sapı
        d.rectangle([bx - _u(0.6, K), by - int(1.4 * K), bx + _u(0.8, K), by + int(1.2 * K)], fill=hex2("#4a4c54"), outline=hex2(KOYU))
        ku = figur(t, ors, ux + int(4.6 * K), z, so_)
        if f < 0.08 or f > 0.92:                                           # vuruş anı: kıvılcım
            for k in range(8):
                a = math.radians(200 + k * 18)
                piksel(t, ux + int(4.6 * K) + math.cos(a) * (4 + k % 3 * 3), ku + math.sin(a) * (4 + k % 3 * 3), hex2("#ffd479"))

    _spr(no, kare, ic=True)


def sahne225():
    """Kart 18-19 (ALTIN): yakın plan: 1237 kalıbıyla basılmış yeni sikke; ortadaki iki satır (Raziye'nin adı ve unvanı)
    altın ışıkla parlar."""
    _sikke_sahnesi(225, "raziye")


def sahne226():
    """Kart 20: saray odası: peçeli Raziye (solda) ile hizmetkâr kadın; hizmetkârın tepsisinde katlanmış tunik ve külah."""
    no = 226
    _oda(no, SARAY)
    yk = _yk(no)
    K = _K(no, ic=True, govde=RAZ_PECE)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 206, 0, f, zincir=_kz(yk))
        _kisi(t, 160, z, K, RAZ_PECE, yon=1, kol=0.12 + 0.05 * SIN(f))
        kol = 0.3
        _kisi(t, 244, z, K, HIZMET, yon=-1, kol=kol)
        ex, ey = _el(244, z[0], K, -1, kol)
        figur(t, tepsi, ex - int(1.8 * K), ey, round(K * 0.8, 1))

    _spr(no, kare, ic=True)


def sahne227():
    """Kart 21 (yavaş): fil üstünde peçesiz, külahlı sultan sağa yürür (filbaşı boynunda); geride seyreden kalabalık ve
    saray revakı. Fil ile insan aynı ölçekte; filin dört ayağı zemine basar."""
    no = 227

    def ekle(img, z):
        figur(img, revak, PAY + 60, PAY + 520, duz(586), 2.2, tas="#c89a72")
        kalabalik(img, duz(592), PAY + 150, PAY + 430, 10, 227, ("#5a4a3a", "#3a4a5a", "#6a5a4a", "#7a6a5a"), s=2.0, yon=1, bas="sarik")

    _dis(no, "gun", ekle=ekle)
    s = _olc(no, lambda t, s_, z: fil_alay(t, 280, z, s_, 1, 0.0), 0.38, ad="fil")

    def kare(t, z, i):
        f = i / KARE
        fil_alay(t, 196, z, s, 1, f)

    _spr(no, kare)


def sahne228():
    """Kart 22: İbn Battûta'nın aktardığı (anlam): erkekler gibi at sürer, yüzünü örtmez: peçesiz, külahlı Raziye ovada
    sağa dörtnala at sürer; toynakların arkasından toz kalkar."""
    no = 228
    _dis(no, "ikindi", ekle=lambda img, z: [figur(img, agac, PAY + x, duz(588), 1.2, tohum=x) for x in (170, 330)])
    _gorunur(no, [330], 240, 300, pay=0)
    A = _A(no, 0.40)

    def kare(t, z, i):
        f = i / KARE
        for k in range(3):
            duman(t, 150 - k * 10, z[0] - 1, 20, 228 + k, faz=(f + k * 0.33) % 1, renk="#d8c09a", ruzgar=-0.6, genislik=1.2)
        figur(t, atli, 210, z, A, 1, faz=f, govde=RAZ["govde"], bas="kulah", bas_renk=RAZ["bas_renk"], adim=0.75,
              at_renk="#3a2a22", yele="#1a120c")

    _spr(no, kare)


def sahne229():
    """Kart 23: akşam, revakın gölgesi: üç Türk köle emîri; ikisi karşı karşıya fısıldaşır, üçüncüsü saraya (sağa) bakar."""
    no = 229
    _dis(no, "aksam", ekle=lambda img, z: figur(img, revak, PAY + 40, PAY + 520, duz(586), 2.4, tas="#9a7a64", golge="#6a4a3a",
                                               ic="#1e1410"))
    K = _K(no, govde=EMIR1)

    def kare(t, z, i):
        f = i / KARE
        _kisi(t, 140, z, K, EMIR2, yon=1, kol=0.18 + 0.04 * SIN(f))
        _kisi(t, 182, z, K, EMIR1, yon=-1)
        _kisi(t, 252, z, K, EMIR3, yon=1)

    _spr(no, kare)


def sahne230():
    """Kart 24-25: saray ahırları: Habeşli Cemâleddin Yakut (ahır emîri) atlı Raziye'nin atını dizgininden tutar; geride
    ahır bölmeleri ve uzakta iki emîr seyreder."""
    no = 230

    def ekle(img, z):
        figur(img, ahir, PAY + 250, PAY + 420, duz(586), 2.2)
        for x, g in ((196, EMIR1), (214, EMIR2)):
            figur(img, kisi, PAY + x, duz(590), 2.1, **dict(g, yon=1))

    _gorunur(no, [196, 214])
    _dis(no, "gun", ekle=ekle)
    A = _A(no, 0.40)
    K = round(A * 2.6 / 2.9, 1)

    def kare(t, z, i):
        f = i / KARE
        _kisi(t, 138, z, K, YAKUT, yon=1, kol=0.25 + 0.03 * SIN(f))
        figur(t, atli, 232, z, A, -1, faz=f, dur=True, govde=RAZ["govde"], bas="kulah", bas_renk=RAZ["bas_renk"],
              at_renk="#e8e0d0", yele="#8a8478")
        ex, ey = _el(138, z[0], K, 1, 0.25 + 0.03 * SIN(f))
        d = ImageDraw.Draw(t)
        d.line([ex, ey, 232 - int(13 * A), z[0] - int(16.5 * A)], fill=hex2("#3a2410"))       # dizgin: elden atın ağzına

    _spr(no, kare)


def sahne231():
    """Kart 26: Nisan 1240: Raziye önde, arkasında bir atlı; sola, Bathinda kalesine yürür (sprite sola kayar)."""
    no = 231
    _dis(no, "gun", ekle=lambda img, z: figur(img, anadolu_kalesi, PAY + 150, PAY + 300, duz(586), 1.4, tas="#a86a4a", golge="#7a4a34"))
    _gorunur(no, [225], 290, 250)
    A = _A(no, 0.40)
    A2 = round(A * 0.9, 1)

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 250, duz(z[0] - 8, t.width), A2, -1, faz=(f + 0.37) % 1, govde="#5a5a6a", bas="migfer", bas_renk="#8a8a90",
              sakal="#2a1a12", adim=0.45, at_renk="#5a3a24")
        figur(t, atli, 168, z, A, -1, faz=f, govde=RAZ["govde"], bas="kulah", bas_renk=RAZ["bas_renk"], adim=0.45,
              at_renk="#e8e0d0", yele="#8a8478")

    _spr(no, kare)


def sahne232():
    """Kart 27 (KIZIL): Bathinda kale kapısı, kızıl akşam: Raziye iki muhafızın arasında kapıya (sola) götürülür; sağda,
    geride binicisiz eyerli at başı önde bekler (Yakut'un düşüşü; ölüm gösterilmez)."""
    no = 232

    def ekle(img, z):
        figur(img, anadolu_kalesi, PAY + 60, PAY + 300, duz(586), 1.5, tas="#a86a4a", golge="#7a4a34")
        figur(img, at, PAY + 322, duz(592), 2.2, -1, "#e8e0d0", "#8a8478", eyer=True, dur=True, bas=0.75)

    _gorunur(no, [180, 322])
    _dis(no, "kizil", ekle=ekle)
    K = _K(no, govde=RAZ)

    def kare(t, z, i):
        f = i / KARE
        _kisi(t, 136, z, K, ASKER, yon=-1, silah="kalkan", kol=0.05)
        _kisi(t, 182, z, K, RAZ, yon=-1)
        _kisi(t, 226, z, K, ASKER, yon=-1, silah="kalkan", kol=0.05 + 0.02 * SIN(f))

    _spr(no, kare)


def sahne233():
    """Kart 28 (yavaş): kale odası, gece: Raziye taş zeminde oturur, başı pencereye dönük; yerde soğuk ay ışığı."""
    no = 233
    _oda(no, ZINDAN)
    so = _S_oturan(no, RAZ_O, oran=0.26)

    def kare(t, z, i):
        f = i / KARE
        for yy in range(z[0] - 4, z[0]):                                    # yerde soğuk ışık şeridi
            for xx in range(150, 250):
                if (xx + yy) % 2 == 0:
                    piksel(t, xx, yy, hex2("#a8b8e0", 50))
        _oturan(t, 206, z, so, RAZ_O, yon=-1)

    _spr(no, kare, ic=True)


def sahne234():
    """Kart 29-30: Delhi, Nisan 1240: kardeşi Behram Şah tahtta; önünde iki emîr diz çöker (yeni düzen)."""
    no = 234
    _oda(no, SARAY)
    yk = _yk(no)
    so = _S_tahtta(no, BEHRAM)
    K = _K(no, ic=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 206, 0, f, zincir=_kz(yk))
        _kisi(t, 134, z, K, EMIR2, yon=1, diz=True)
        _kisi(t, 180, z, K, EMIR3, yon=1, diz=True, kol=0.06 + 0.03 * SIN(f))
        _tahtta(t, 254, z, so, BEHRAM)

    _spr(no, kare, ic=True)


def sahne235():
    """Kart 31: Raziye ve Altuniya yan yana atlı, Delhi'ye (sağa) yürür; Altuniya bir adım geride (arka sıra, küçük)."""
    no = 235
    _dis(no, "safak", ekle=lambda img, z: [figur(img, agac, PAY + x, duz(588), 1.1, tohum=x) for x in (180, 360)])
    A = _A(no, 0.40)
    A2 = round(A * 0.92, 1)

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 160, duz(z[0] - 8, t.width), A2, 1, faz=(f + 0.4) % 1, govde=ALTUNIYA["govde"], bas="kalpak",
              bas_renk=ALTUNIYA["bas_renk"], sakal=ALTUNIYA["sakal"], adim=0.45, at_renk="#4a2e1e")
        figur(t, atli, 226, z, A, 1, faz=f, govde=RAZ["govde"], bas="kulah", bas_renk=RAZ["bas_renk"], adim=0.45,
              at_renk="#e8e0d0", yele="#8a8478")

    _spr(no, kare)


def sahne236():
    """Kart 32 (yavaş): Ekim 1240, Kaithal ovası, alacakaranlık: Raziye ve Altuniya atlarında sağa bakar; karşıda (geride,
    sağda) Behram Şah'ın ordusunun atlı ve yaya sırası."""
    no = 236

    def ekle(img, z):
        kalabalik(img, duz(590), PAY + 300, PAY + 380, 7, 236, ("#3a3a44", "#4a3a2a"), s=1.6, yon=-1, bas="migfer")
        for j, x in enumerate(range(296, 384, 22)):
            figur(img, atli, PAY + x, duz(586), 1.2, -1, faz=(j * 0.3) % 1, dur=True, govde="#3a3a44", bas="migfer",
                  bas_renk="#8a8a90", silah="mizrak", bayrak="#2a6a3a")

    _gorunur(no, [320])
    _dis(no, "aksam", ekle=ekle, dag_y=(500, 518), tepe_y=522, ova_y=530, orta_ust=(556, 562))
    A = _A(no, 0.38)
    A2 = round(A * 0.92, 1)

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 160, duz(z[0] - 8, t.width), A2, 1, faz=0.0, dur=True, govde=ALTUNIYA["govde"], bas="kalpak",
              bas_renk=ALTUNIYA["bas_renk"], sakal=ALTUNIYA["sakal"], at_renk="#4a2e1e")
        figur(t, atli, 212, z, A, 1, faz=0.0, dur=True, govde=RAZ["govde"], bas="kulah", bas_renk=RAZ["bas_renk"],
              at_renk="#e8e0d0", yele="#8a8478", kol=0.04 * (1 + SIN(f)))

    _spr(no, kare)


def sahne237():
    """Kart 33: boş ordugâh, karanlık: gergi ipi kopmuş terk edilmiş çadır; Raziye ve Altuniya yalnız, sağa bakar; uzakta
    askerler sırtlarını dönüp uzaklaşır."""
    no = 237

    def ekle(img, z):
        kalabalik(img, duz(592), PAY + 300, PAY + 360, 12, 237, ("#3a3a44", "#4a3a2a"), s=1.6, yon=1, bas="migfer", adim=0.6)

    _gorunur(no, [320])
    _dis(no, "kizil", ekle=ekle, dag_y=(500, 518), tepe_y=522, ova_y=530, orta_ust=(556, 562))
    K = _K(no, govde=ALTUNIYA)

    def kare(t, z, i):
        f = i / KARE
        figur(t, cadir, 120, z, round(0.42 * K, 1), yikik=True)
        _kisi(t, 210, z, K, ALTUNIYA, yon=1)
        _kisi(t, 250, z, K, RAZ, yon=1, kol=0.04 * (1 + SIN(f)))

    _spr(no, kare)


def _minhac_yazar(no):
    _oda(no, CALISMA)
    yk = _yk(no)
    so = _S_oturan(no, MINHAC, oran=0.26)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 246, 0, f, zincir=_kz(yk))
        mumluk(t, 140, z, f, 3)
        kitaplar(t, 262, z[0], round(0.5 * so, 1))
        _oturan(t, 184, z, so, MINHAC, yon=1, el="kalem", minder="#5a6a3a")
        rahle(t, 184 + int(4.2 * so), z[0], round(0.9 * so, 1))

    _spr(no, kare, ic=True)


def sahne238():
    """Kart 34-35 ve 47: tarihçi Minhâc (yaşlı, ak sakal) minderde rahlesine yazar; şamdan, kitaplar, kandil."""
    _minhac_yazar(238)


def sahne239():
    """Kart 36: yaklaşık yüz yıl sonra: Faslı gezgin İbn Battûta asasıyla Delhi'ye (sağa) yürür; arkasında yüklü deve;
    sağ geride Delhi'nin surları ve kubbeleri."""
    no = 239
    _dis(no, "gun", ekle=lambda img, z: figur(img, orta_asya_sehri, PAY + 330, PAY + 600, duz(586), 1.8, tohum=239,
                                             kerpic="#c08a6a", golge="#8a5a44", kubbe="#9a9a8a"))
    K = _K(no, govde=BATTUTA)
    sd = round(K * 1.25 * 2.9 / 2.6 * 0.82, 1)

    def kare(t, z, i):
        f = i / KARE
        figur(t, deve, 150, z, sd, 1, faz=(f * 2) % 1, renk="#b08a5a", yuk="#6a4a3a", adim=0.35)
        _kisi(t, 236, z, K, BATTUTA, yon=1, adim=(f * 2) % 1, silah="sopa", kol=0.0)

    _spr(no, kare)


def sahne240():
    """Kart 37: köy, ikindi (İbn Battûta'nın dinlediği hikâye): köylü kaçan sultana ekmek uzatır; Raziye elini uzatır."""
    no = 240
    _dis(no, "ikindi", ekle=lambda img, z: figur(img, koy_evleri, PAY + 150, PAY + 400, duz(586), 2.0, tohum=240))
    K = _K(no, govde=RAZ)

    def kare(t, z, i):
        f = i / KARE
        _kisi(t, 166, z, K, RAZ, yon=1, kol=0.18 + 0.04 * SIN(f))
        kol = 0.3
        _kisi(t, 240, z, K, KOYLU, yon=-1, kol=kol)
        ex, ey = _el(240, z[0], K, -1, kol)
        d = ImageDraw.Draw(t)
        d.ellipse([ex - int(2.6 * K), ey - int(0.9 * K), ex - int(0.2 * K), ey + int(0.5 * K)], fill=hex2("#b07a3a"), outline=hex2("#5a3a14"))
        d.line([ex - int(2.2 * K), ey - int(0.5 * K), ex - int(0.6 * K), ey - int(0.5 * K)], fill=hex2("#d8a860"))

    _spr(no, kare)


def sahne241():
    """Kart 38: gece, ağaç altı: Raziye yere serilmiş bohçaya başını koymuş uyur, giysisinde mücevherler parıldar; köylü
    ayakta ona bakar (şiddet gösterilmez)."""
    no = 241
    _dis(no, "gece", ekle=lambda img, z: figur(img, agac, PAY + 220, duz(588), 1.6, tohum=241,
                                              yaprak=("#1a2a2a", "#22343a", "#2a3e44"), govde="#2a2024"), yildiz=160)
    K = _K(no, govde=KOYLU, oran=0.28)

    def kare(t, z, i):
        f = i / KARE
        figur(t, uyuyan, 172, z, round(K * 0.92, 1), 1, f)
        _kisi(t, 258, z, K, KOYLU, yon=-1, kol=0.04)

    _spr(no, kare)


def sahne242():
    """Kart 39 (yavaş): tarla, şafak: ekin sıralarının ortasında küçük kubbeli türbe (mezarın üstüne kubbe yapıldı)."""
    no = 242

    def ekle(img, z):
        d = ImageDraw.Draw(img)
        for yy in range(566, 600, 4):                                       # tarla sıraları
            d.line([0, yy, GW, yy], fill=hex2("#6e7e42"))
        for k in range(0, GW, 7):
            piksel(img, k, 566 + (k % 3) * 8, hex2("#a8b860"))

    _dis(no, "safak", ekle=ekle, dag_y=(500, 518), tepe_y=522, ova_y=530, orta_ust=(556, 560))
    st = _olc(no, lambda t, s, z: figur(t, kubbe_turbe, 280, z, s), 0.30, ad="turbe")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kubbe_turbe, 200, z, st)
        _cimen(t, z, f, ["#7c8c4a", "#6e7e42", "#a8b860"], 242, no, boy=9)

    _spr(no, kare)


def sahne243():
    """Kart 40: bugün: sehpada harita; Delhi, Kaithal ve Tonk gerçek göreli konumlarında yanıp söner. Şamdan."""
    no = 243
    _oda(no, CALISMA)
    yk = _yk(no)
    sh = _olc(no, lambda t, s, z: figur(t, harita_sehpasi, 280, z, s), 0.34, ic=True, ad="harita")

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 252, 0, f, zincir=_kz(yk))
        mumluk(t, 140, z, f, 3)
        figur(t, harita_sehpasi, 214, z, sh, isik=0.5 + 0.5 * SIN(f))

    _spr(no, kare, ic=True)


def sahne244():
    """Kart 41-42 (42 yavaş): Delhi, bugün: iki yanında eski evler olan dar sokakta çatısız dört duvar ve içinde iki beyaz
    kabir; önde devletin mavi levhası. İnsan yok."""
    no = 244

    def ekle(img, z):
        figur(img, sokak_evleri, PAY + 20, PAY + 520, duz(588), 2.4, tohum=244)
        _zemin_satir(no, 590, "#8a7a62")(img, z)

    _dis(no, "gun", ekle=ekle, bos_on=True)
    sa = _olc(no, lambda t, s, z: figur(t, mezar_avlusu, 280, z, s), 0.18, ad="avlu")
    sa = min(sa, 3.2)

    def kare(t, z, i):
        f = i / KARE
        figur(t, mezar_avlusu, 186, z, sa)
        figur(t, levha, 262, z, round(sa * 1.0, 1))

    _spr(no, kare)


def sahne245():
    """Kart 43 (ALTIN, yavaş): kancanın cevabı: saray odasında peçesiz, külahlı Raziye ayakta; peçe ayağının dibinde yerde."""
    no = 245
    _oda(no, SARAY)
    yk = _yk(no)
    K = _K(no, ic=True, govde=RAZ, oran=0.32)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 210, 0, f, zincir=_kz(yk))
        figur(t, pece_yerde, 168, z, round(K * 0.8, 1))
        _kisi(t, 222, z, K, RAZ, yon=-1, kol=0.03 * (1 + SIN(f)))

    _spr(no, kare, ic=True)


def sahne246():
    """Kart 45-46: 1260: yaşlı Minhâc diz çöküp ciltli kitabını tahttaki Sultan Nâsıreddin'e (Raziye'nin kardeşi) sunar."""
    no = 246
    _oda(no, SARAY)
    yk = _yk(no)
    so = _S_tahtta(no, NASIR)
    K = _K(no, ic=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 206, 0, f, zincir=_kz(yk))
        kol = 0.3 + 0.03 * SIN(f)
        _kisi(t, 168, z, K, MINHAC, yon=1, diz=True, kol=kol)
        figur(t, kitap_elde, 168, z[0], K, 1, kol)
        _tahtta(t, 254, z, so, NASIR)

    _spr(no, kare, ic=True)


def sahne247():
    """Kart 48-49 (48 KIZIL, yavaş): yakın plan: rahlede açık el yazması, hokka ve kalem; mum ışığı sayfada titrer."""
    no = 247
    ic_mekan(no, duvar=("#1a1410", "#221a14", "#2a2018"), kemer="#120c08", cini="#5a3a20", pencere=None,
             zemin_renk=("#4a2e1c", "#3e2616", "#321e12"), isik="#f8c060", hali=False)
    sk = _olc(no, lambda t, s, z: figur(t, acik_kitap, 280, z, s), 0.30, ic=True, ad="kitap")

    def kare(t, z, i):
        f = i / KARE
        figur(t, acik_kitap, 190, z, sk, f=f)
        u = z[0] - int(9 * sk)
        for r in range(4, int(9 * sk), 3):                                  # sayfada titreyen mum ışığı
            for a in range(0, 360, 8):
                px_, py_ = 190 + math.cos(math.radians(a)) * r * 1.3, u - int(3 * sk) + math.sin(math.radians(a)) * r * 0.4
                if (int(px_) + int(py_)) % 2 == 0 and random.Random(int(px_) * 7 + int(py_) + i).random() < 0.25:
                    piksel(t, px_, py_, hex2("#ffd479", 40))

    _spr(no, kare, ic=True)


def sahne248():
    """Kart 51: son soru: alçak sehpada yan yana katlanmış peçe ve yastıkta altın taç; kandil, şamdan."""
    no = 248
    _oda(no, SARAY_GECE)
    yk = _yk(no)
    sp = _olc(no, lambda t, s, z: figur(t, pece_ve_tac, 280, z, s), 0.16, ic=True, ad="pecetac")
    sp = min(sp, 6.4)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 200, 0, f, zincir=_kz(yk))
        figur(t, pece_ve_tac, 200, z, sp, f=f)

    _spr(no, kare, ic=True)


SAHNELER = {n: globals()[f"sahne{n}"] for n in range(210, 249)}

if __name__ == "__main__":
    for n in ([int(a) for a in sys.argv[1:]] or sorted(SAHNELER)):
        SAHNELER[n]()
        print(f"sahne {n} tamam")
