"""Cengiz Han animasyonunun 8 sahnesini Grafiker'in planına göre çizer (64-bit piksel sanatı).

Her sahne için video/public/ altına: sahneN-gokyuzu.png ve sahneN-uzak.png (540x960, yatayda
dikişsiz), sahneN-orta.png ve sahneN-on.png (810x960, kadrajdan 1,5 kat geniş; görünen kadraj
x 135-675) ve sprite sayfaları (sahneN-karakter.png, sahneN-karakter2.png).

Zemin çizgileri plandaki gibidir: sprite'ın son satırı sahnenin ZEMIN ya da UFUK satırına oturur.
Her sprite sayfası taban_denetimi'nden geçer; havada duran kare varsa betik durur.

Kullanım: python3 -I video/piksel/sahneler.py [sahne numaraları] [--cikti klasör] [--onizleme klasör]
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ciz import (W, H, KOYU, _ac, _esik, agac, arazi, at, bulut, buyut, cayir_dokusu, cicek, cicekler, cimen_tutamlari, duman, duzle,  # noqa: E402
                 figur, gradyan, gunes, hex2, insan, kagni, okuz, orta_asya_sehri, patika, piksel, piksel_ok, sirt, sprite_sayfasi,
                 taban_denetimi, taslar, tug, yeni, yildizlar, yurt)

GW = 810  # orta ve ön plan genişliği
KARE = 24  # her animasyon döngüsünün kare sayısı (akıcı hareket için ara pozlar)
PAY = (GW - W) // 2  # görünen kadrajın orta plandaki başlangıcı (135)

CIKTI = Path(sys.argv[sys.argv.index("--cikti") + 1]) if "--cikti" in sys.argv else Path(__file__).parents[1] / "public"
ONIZLEME = Path(sys.argv[sys.argv.index("--onizleme") + 1]) if "--onizleme" in sys.argv else None


def kaydet(img, ad):
    CIKTI.mkdir(parents=True, exist_ok=True)
    img.save(CIKTI / ad)


# ---------------------------------------------------------------- ortak katmanlar


YAZI_BANDI = (95, 245)  # ekran metni ve CTA'nın durduğu bant (ızgara y); buraya bulut konmaz


def gokyuzu(no, renkler, gunes_=None, bulutlar=(), bulut_renk=("#fff8ec", "#f4dcc8", "#d8a8a0"), yildiz=0):
    for x, y, b in bulutlar:
        if y - b * 0.6 < YAZI_BANDI[1] and y + b * 0.4 > YAZI_BANDI[0]:
            raise ValueError(f"sahne {no}: bulut (y {y}) ekran yazısının bandına giriyor, okunurluğu bozar")
    img = yeni()
    gradyan(img, renkler)
    if yildiz:
        yildizlar(img, yildiz, 300, "#fff8e0", no)
    if gunes_:
        gunes(img, *gunes_)
    for i, (x, y, b) in enumerate(bulutlar):
        bulut(img, x, y, b, list(bulut_renk), no * 10 + i)
    kaydet(img, f"sahne{no}-gokyuzu.png")
    return img


def uzak(no, dag_renk, tepe_renk, ova_renk, dag_y=(346, 420), tepe_y=440, ova_y=480, kenar=None):
    """Uzak plan: dikişsiz dağ sırtı, alçak tepeler ve %50'den aşağısı dümdüz ova."""
    img = yeni()
    dag = sirt(dag_y[1], (dag_y[1] - dag_y[0]) / 2, no, 4, 6, w=W, dongulu=True)
    arazi(img, dag, dag_renk, kenar)
    tepe = sirt(tepe_y, 14, no + 50, 6, 0, w=W, dongulu=True)
    arazi(img, tepe, tepe_renk)
    for y in range(ova_y - 4, ova_y):  # ova kenarı: sert çizgi yerine titreşimli geçiş
        for x in range(W):
            if (ova_y - y) / 5 < _esik(x, y) * 0.9:
                img.putpixel((x, y), hex2(_ac(ova_renk[0], 0.12)))
    arazi(img, [ova_y] * W, ova_renk, None, doku_tohum=no + 3)
    cayir_dokusu(img, [ova_y] * W, ova_renk, no + 4, yogunluk=0.02)
    kaydet(img, f"sahne{no}-uzak.png")
    return img


def orta(no, ust=(500, 557), renkler=None, kenar=None, tohum=None, ekle=None):
    """Orta plan (810 geniş): üst kenarı ust aralığında dalgalanan, aşağısı tamamen opak çayır."""
    img = yeni(GW, H)
    ust_y = (ust[0] + ust[1]) // 2
    z = sirt(ust_y, (ust[1] - ust[0]) / 2, (tohum or no) + 7, 3, 1.5, w=GW)
    arazi(img, z, renkler, kenar, doku_tohum=no, perspektif=True)
    cayir_dokusu(img, z, [_ac(r, 0.1) for r in renkler[:3]] + [_ac(r, -0.15) for r in renkler[2:]], no, isik=kenar)
    cimen_tutamlari(img, z, [kenar or renkler[0], renkler[0], renkler[1]], no, 0.55, 5)
    cicekler(img, z, ["#f4d24a", "#e88a9a", "#f8f4e8"], no, 70, 300)
    if ekle:
        ekle(img, z)
    kaydet(img, f"sahne{no}-orta.png")
    return img


def on(no, renkler, isik, boy=200):
    """Ön plan (810 geniş): yalnızca sol ve sağ alt köşelerde, dipten yükselen uzun çimen tutamları."""
    img = yeni(GW, H)
    rnd = random.Random(no * 3)
    d_renk = [hex2(r) for r in renkler]
    for bolge in ((0, 250), (GW - 250, GW)):
        for _ in range(140):
            x = rnd.randint(*bolge)
            kenar_uzaklik = min(x - bolge[0], bolge[1] - x) / 125
            if bolge[0] == 0:
                kenar_uzaklik = 1 - x / 250
            else:
                kenar_uzaklik = (x - bolge[0]) / 250
            h = int(rnd.uniform(0.25, 1.0) * boy * (0.35 + 0.65 * kenar_uzaklik))
            egim = rnd.uniform(-0.35, 0.35)
            renk = rnd.choice(d_renk)
            for i in range(h):
                t = i / max(1, h)
                bx = x + egim * i * t
                genis = 3 if t < 0.5 else (2 if t < 0.85 else 1)
                for k in range(genis):
                    piksel(img, bx + k, H - 1 - i, renk if k else hex2(isik) if t > 0.6 else renk)
    kaydet(img, f"sahne{no}-on.png")
    return img


def sprite(no, ek, kare_w, kare_h, adet, ciz_kare, denetim=True):
    sayfa = sprite_sayfasi(kare_w, kare_h, adet, ciz_kare)
    if denetim:
        taban_denetimi(sayfa, kare_w, f"sahne{no}-{ek}")
    kaydet(sayfa, f"sahne{no}-{ek}.png")
    return sayfa


def onizleme(no, gk, uz, ort, onp, spriteler):
    """Kodun ilk karede göstereceğine yakın bir birleşim (kamera 0, sprite'lar ilk konumda)."""
    if not ONIZLEME:
        return
    img = yeni()
    img.alpha_composite(gk)
    img.alpha_composite(uz)
    def koy(tur):
        for sayfa, kare_w, x, taban, t in spriteler:
            if t == tur:
                kare = sayfa.crop((0, 0, kare_w, sayfa.height))
                img.paste(kare, (int(x - kare_w / 2), taban - sayfa.height), kare)

    koy("ufuk")
    img.alpha_composite(ort.crop((PAY, 0, PAY + W, H)))
    koy("zemin")
    img.alpha_composite(onp.crop((PAY, 0, PAY + W, H)))
    ONIZLEME.mkdir(parents=True, exist_ok=True)
    buyut(img).save(ONIZLEME / f"sahne{no}.png")




def duz(y, w=GW):
    return [y] * w


# ---------------------------------------------------------------- sahneler


def sahne1():
    gk = gokyuzu(1, ["#4a6aa8", "#6a90c8", "#9ab8d8", "#d8d0b8", "#f0c898", "#f8b880"], (400, 430, 16, ["#fff2c0", "#ffd890"]),
                 [(110, 300, 44), (380, 285, 36), (230, 350, 28), (500, 50, 30)])
    uz = uzak(1, ["#8a98b8", "#7a88a8"], ["#8aa080", "#7a9070"], ["#9ab07a", "#8aa46c", "#7a985e"])
    ort = orta(1, (500, 557), ["#7aa84a", "#6a9a3e", "#5a8a36", "#4a7a2e", "#3f6b2a"], "#a8d063",
               ekle=lambda img, z: patika(img, z, 0, GW, 120, "#a88a5a", 1))
    onp = on(1, ["#3f6b2a", "#5a8f36", "#8a7a3a"], "#d8e070")

    def kare(t, z, i):
        f = i / KARE
        baca = figur(t, yurt, 150, z, 3.8, isik=True)  # yurt ile atlar arasında en az 20 px boşluk
        duman(t, baca[0], baca[1], 115, 1, faz=f, ruzgar=0.3, genislik=1.4)
        figur(t, at, 34, z, 2.3, 1, dur=True, bas=0.8 + 0.2 * math.sin(f * 2 * math.pi), kuyruk=math.sin(f * 4 * math.pi))
        figur(t, at, 247, z, 2.0, 1, "#c8a070", "#5a3a22", dur=True, bas=0.55 + 0.45 * math.sin(f * 2 * math.pi + 1.5),
              kuyruk=math.sin(f * 4 * math.pi + 1))

    sp = sprite(1, "karakter", 300, 192, KARE, kare)
    onizleme(1, gk, uz, ort, onp, [(sp, 300, 367, 640, "zemin")])


def sahne2():
    gk = gokyuzu(2, ["#3a4a88", "#5a62a0", "#9a86b0", "#d8a0a0", "#f0b890", "#f8c898"], (120, 470, 14, ["#ffe0b0", "#f8b888"]),
                 [(380, 300, 40), (150, 290, 34), (460, 360, 26)], ("#f8e0e0", "#e8b8c0", "#b88aa8"))
    uz = uzak(2, ["#5a6a98", "#4a5a88"], ["#4a7a6a", "#3f6a5e"], ["#6a8a5a", "#5a7a4e", "#4a6a42"])

    def atlar(img, z):
        for x, s, yon, renk in ((205, 2.0, 1, "#6b3f24"), (262, 1.7, 1, "#c8a070"), (625, 1.9, -1, "#4a2e1e")):
            figur(img, at, x, duz(600), s, yon, renk, dur=True, bas=0.9)

    ort = orta(2, (505, 555), ["#5a8a40", "#4a7a36", "#3f6b2e", "#355a28", "#2a4a20"], "#8ab858", ekle=atlar)
    onp = on(2, ["#2a4a20", "#3f6b2a", "#6a5a3a"], "#e8b888")

    def kare(t, z, i):
        f = i / KARE
        guc = 0.75 + 0.25 * math.sin(f * 2 * math.pi * 2) * math.sin(f * 2 * math.pi + 0.7)
        baca = figur(t, yurt, 150, z, 5.6, isik=True, isik_gucu=guc)
        duman(t, baca[0], baca[1], 140, 2, faz=f, ruzgar=-0.25, genislik=1.5)
        figur(t, insan, 108, z, 3.3, "#7a3a4a", bebek=True, kadin=True, yon=1)  # kapının solunda; boyu kapıdan biraz uzun

    sp = sprite(2, "karakter", 256, 256, KARE, kare)
    onizleme(2, gk, uz, ort, onp, [(sp, 256, 270, 600, "zemin")])


def sahne3():
    gk = gokyuzu(3, ["#5a80b8", "#7aa0c8", "#a8c4d8", "#d8d8c8", "#e8d8a8", "#f0d098"], (90, 400, 14, ["#fff4d0", "#f8e0a0"]),
                 [(300, 310, 46), (90, 290, 38), (440, 50, 34)], ("#f8f8f4", "#dce4ec", "#a8b4c8"))
    uz = uzak(3, ["#a0aab8", "#9098a8"], ["#a8b08a", "#98a07a"], ["#b8b88a", "#a8aa7c", "#98a070"])
    ort = orta(3, (557, 576), ["#8aa860", "#7a9a54", "#6a8a4a", "#5a7a40", "#4a6a36"], "#b8c878")
    onp = on(3, ["#5a6a36", "#8a8a4a", "#a89a5a"], "#e8e0a0")

    def aile(t, z, i):
        f = i / KARE
        figur(t, insan, 62, z, 4.0, "#6a4a5a", kadin=True, adim=f, ruzgar=1.0)  # ölçek: insan = at boyunun ~%68'i
        for j, (x, s, renk) in enumerate(((122, 2.9, "#4a6a8a"), (160, 2.6, "#8a5a3a"), (194, 2.3, "#5a7a4a"))):
            figur(t, insan, x, z, s, renk, adim=(f + 0.3 * (j + 1)) % 1, ruzgar=1.0)

    sp1 = sprite(3, "karakter", 270, 170, KARE, aile)

    def kervan(t, z, i):
        f = i / KARE
        for ox, kx in ((34, 80), (150, 196)):
            figur(t, okuz, ox, z, 1.5, -1, "#6a5040", faz=f)
            figur(t, kagni, kx, z, 1.5, -1, faz=f)

    sp2 = sprite(3, "karakter2", 248, 68, KARE, kervan)
    onizleme(3, gk, uz, ort, onp, [(sp2, 248, 375, 510, "ufuk"), (sp1, 270, 90, 600, "zemin")])


def sahne4():
    gk = gokyuzu(4, ["#5a70b0", "#8a90c0", "#c8a8b8", "#f0b898", "#f8b880", "#f8d0a0"], (430, 470, 20, ["#fff0c0", "#ffc888"]),
                 [(140, 300, 42), (400, 290, 32), (260, 360, 26)], ("#fff0e0", "#f8c8a8", "#d8988a"))
    uz = uzak(4, ["#b89888", "#a88a7a"], ["#c8a868", "#b8985a"], ["#d0b070", "#c0a064", "#b09058"])
    ort = orta(4, (480, 537), ["#a8b058", "#98a04e", "#889044", "#78803c", "#687034"], "#e0d070",
               ekle=lambda img, z: patika(img, z, 0, GW, 110, "#c8a870", 4))
    onp = on(4, ["#8a8a3a", "#a89a4a", "#6a6a2e"], "#f8e098")

    def kafile(t, z, i):
        f = i / KARE
        for j, (x, renk, deel, kadin) in enumerate(((295, "#6b3f24", "#3a5a8a", False), (232, "#4a2e1e", "#7a2e3e", False),
                                                    (170, "#d8d0c0", "#9a2e3e", True), (107, "#8a5a34", "#5a6a3a", False),
                                                    (45, "#5a3a24", "#4a4a7a", False))):
            figur(t, at, x, z, 3.1, -1, renk, binici=deel, binici_kadin=kadin, faz=(f + j * 0.37) % 1, adim=0.45)

    ok = yeni()
    piksel_ok(ok, 115, 465, 496, kavis=14, kalinlik=4)
    kaydet(ok, "sahne4-ok.png")

    sp = sprite(4, "karakter", 340, 150, KARE, kafile)
    onizleme(4, gk, uz, ort, onp, [(sp, 340, 510 - 170, 630, "zemin")])


def sahne5():
    gk = gokyuzu(5, ["#7a90c8", "#a0b0d8", "#d8c0d0", "#f0d0c0", "#f8e0c0", "#fff0d0"], (270, 470, 22, ["#fff8d8", "#ffe0a8"]),
                 [(100, 300, 44), (420, 285, 38), (260, 50, 30)], ("#fffaf0", "#f8d8d8", "#d8a8b8"))
    uz = uzak(5, ["#8aa0a0", "#7a9090"], ["#6a9a5a", "#5a8a4e"], ["#8ab070", "#7aa064", "#6a9058"], dag_y=(326, 400), tepe_y=430, ova_y=461)

    def kamp(img, z):
        zemin = duz(600)
        rnd = random.Random(5)
        merkez = PAY + 270  # tuğ burada (sprite); flamaları sağa doğru ~75 px uzanır
        for x, s in ((60, 2.0), (172, 2.2), (240, 2.7), (305, 1.9), (505, 1.8), (568, 2.6), (636, 2.0), (760, 2.2)):
            figur(img, yurt, x, zemin, s, keçe=rnd.choice(("#efe4cc", "#e8dcc0", "#f4ecd8")))
        renkler = ("#3a5a8a", "#7a2e3e", "#5a6a3a", "#8a5a3a", "#4a4a7a", "#9a6a2a")
        # tuğun iki yanında toplanan boylar (sağda flamaların altından uzak)
        for x in (338, 349, 360, 371, 382, 488, 499, 510, 521, 532, 543) + (205, 272, 337 - 60, 600, 470 + 130):
            figur(img, insan, x + rnd.randint(-3, 3), zemin, rnd.uniform(1.5, 1.9), rnd.choice(renkler),
                  kadin=rnd.random() < 0.35, yon=1 if x < merkez else -1)
        for x in (205, 600):
            for k, renk in enumerate(("#e8a040", "#f8d070", "#c8552c")):
                piksel(img, x + k - 1 + 14, 598 - k % 2, hex2(renk))
            duman(img, x + 14, 596, 90, x, faz=0.0, ruzgar=0.1, genislik=0.9)

    ort = orta(5, (480, 518), ["#7ab050", "#6aa046", "#5a903e", "#4a8036", "#3f702e"], "#b0e070", ekle=kamp)
    onp = on(5, ["#3f702e", "#5a903e", "#8a8a3a"], "#f0f0a0")

    def kare(t, z, i):
        figur(t, tug, 70, z, 2.2, faz=i / KARE)  # yurdun ~2 katı boyunda (tuğ direği birkaç metre)

    sp = sprite(5, "karakter", 160, 224, KARE, kare)
    onizleme(5, gk, uz, ort, onp, [(sp, 160, 270, 600, "zemin")])


def sahne6():
    gk = gokyuzu(6, ["#6a7088", "#8a8488", "#b09a80", "#c8a878", "#d8b880", "#e0c890"], (150, 380, 18, ["#f8e8c0", "#e8c890"]),
                 [(380, 300, 46), (120, 290, 40), (470, 60, 30)], ("#e8d8c0", "#c8b098", "#9a8478"))
    uz = uzak(6, ["#8a90a0", "#7a8090"], ["#a8a07a", "#98906c"], ["#b0a478", "#a0966c", "#908860"], dag_y=(326, 410))
    ort = orta(6, (557, 576), ["#a8a478", "#98966c", "#888860", "#787a54", "#686a48"], "#c8c08a")
    onp = on(6, ["#787a54", "#988a5a", "#6a6a48"], "#e8d8a0", boy=190)

    def kolon(t, z, i):
        f = i / KARE
        for j, x in enumerate((320, 262, 205, 148, 90, 32)):
            yuk = j % 2 == 1
            figur(t, at, x, z, 2.4, 1, ("#5a3a24", "#8a6a4a", "#4a2e1e", "#7a5a3a", "#6b3f24", "#9a7a5a")[j],
                  binici=None if yuk else ("#5a4a3a", "#4a4a5a", "#6a3a2e")[j // 2], yuk="#a89070" if yuk else None,
                  faz=(f + j * 0.29) % 1, adim=0.35)

    sp1 = sprite(6, "karakter", 360, 120, KARE, kolon)

    def sehir_kare(t, z, i):
        damlar = figur(t, orta_asya_sehri, 22, 274, z, 3.0, tohum=6)
        # kubbe ve minareden uzak damlar: duman görünür dam çizgisinden çıksın
        w_ = 274 - 22
        engeller = [22 + w_ * 0.35, 22 + w_ * 0.68, 22 + w_ * 0.52]
        acik = [dm for dm in damlar if min(abs(dm[0] - e) for e in engeller) > 34]
        secilen = [acik[1], acik[-2]]
        for k, (dx, dy) in enumerate(secilen):
            duman(t, dx, dy, min(dy - 4, 150), 6 + k * 3, faz=(i / KARE + k * 0.5) % 1, renk="#6a6058", ruzgar=0.2, genislik=1.8)

    sp2 = sprite(6, "karakter2", 296, 248, KARE, sehir_kare)
    onizleme(6, gk, uz, ort, onp, [(sp2, 296, 378, 518, "ufuk"), (sp1, 360, 10 + 180, 630, "zemin")])


def sahne7():
    gk = gokyuzu(7, ["#2a2a5a", "#4a4a88", "#7a62a0", "#b07a9a", "#d89a90", "#e8b088"], (410, 470, 12, ["#ffd8a0", "#e8a080"]),
                 [(140, 300, 36), (420, 330, 28)], ("#d8b8d0", "#a888b0", "#7a6098"), yildiz=60)
    uz = uzak(7, ["#4a4a7a", "#3f3f6a"], ["#5a4a6a", "#4e405e"], ["#4a5a50", "#40504a", "#384642"])

    def agac_ekle(img, z):
        figur(img, agac, PAY + 118, duz(600), 4.0, ("#2a3a3a", "#38504a", "#4a6a5a"), govde="#3a2a2a", tohum=7)

    ort = orta(7, (500, 557), ["#3f5a40", "#36503a", "#2e4632", "#263c2c", "#203226"], "#6a8a6a", ekle=agac_ekle)
    onp = on(7, ["#203226", "#2e4632", "#4a3a5a"], "#a888c8")

    def kare(t, z, i):
        f = i / KARE
        figur(t, at, 86, z, 4.6, 1, "#5a3a2a", "#1e140e", eyer=True, dur=True, bas=0.1,
              kulak=math.sin(f * 2 * math.pi) * 1.2, kuyruk=math.sin(f * 2 * math.pi + 0.8) * 1.5)
        rnd = random.Random(70)
        for k in range(5):
            bx, by = rnd.randint(10, 182), rnd.randint(20, 120)
            fx = bx + math.sin(f * 2 * math.pi + k) * 6
            fy = by + math.cos(f * 2 * math.pi + k * 1.7) * 4
            parlak = 0.5 + 0.5 * math.sin(f * 2 * math.pi * 2 + k)
            piksel(t, fx, fy, hex2("#fff4a0", int(140 + 115 * parlak)))
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                piksel(t, fx + dx, fy + dy, hex2("#f8e070", int(60 * parlak)))

    sp = sprite(7, "karakter", 192, 160, KARE, kare)
    onizleme(7, gk, uz, ort, onp, [(sp, 192, 270, 600, "zemin")])


def sahne8():
    gk = gokyuzu(8, ["#2a3a78", "#4a6aa8", "#8a8ab8", "#c8a0b0", "#e8b0a0", "#f0c098"], None,
                 [(120, 300, 44), (400, 310, 40), (280, 380, 32)], ("#fff0e0", "#f0c8c0", "#b898b8"), yildiz=70)
    uz = uzak(8, ["#7a6a98", "#6a5a88"], ["#8a7a8a", "#7a6a7a"], ["#5a6a5a", "#4e5e50", "#445446"], dag_y=(384, 440), tepe_y=455)

    def tas_ekle(img, z):
        figur(img, taslar, PAY + 162, duz(640), 3.5)

    ort = orta(8, (500, 557), ["#4a6a44", "#405e3c", "#365234", "#2e462e", "#263c28"], "#7a9a70", ekle=tas_ekle)
    onp = on(8, ["#263c28", "#365234", "#5a4a6a"], "#c8a8d8")

    def kare(t, z, i):
        figur(t, cicek, 70, z, 5.4, faz=i / KARE, renk="#ffe25a", orta="#e0602c", kontur="#3a2a14")

    sp = sprite(8, "karakter", 140, 140, KARE, kare)
    onizleme(8, gk, uz, ort, onp, [(sp, 140, 236, 640, "zemin")])


if __name__ == "__main__":
    secim = [int(a) for a in sys.argv[1:] if a.isdigit() and 1 <= int(a) <= 8] or range(1, 9)
    for n in secim:
        globals()[f"sahne{n}"]()
        print(f"sahne {n} tamam")
