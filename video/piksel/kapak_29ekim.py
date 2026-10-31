"""29 Ekim Cumhuriyet Bayramı story posteri (1080x1920), 64-bit piksel sanatı.

Kızıl şafak göğü, büyük ay-yıldız, ufukta doğan güneş; Kocatepe'de atının üstünde pelerinli Atatürk silüeti
(doğan güneşe bakar); önde koyu bozkır ve çimen; yazılar: 29 EKİM · CUMHURİYET BAYRAMI · 103. YIL ·
NE MUTLU TÜRKÜM DİYENE! · @pikseltarihim. Story güvenli alanı: üst 250 / alt 250 px boş bırakılır.

Kullanım: python3 -I video/piksel/kapak_29ekim.py  →  video/public/kapak-29-ekim.png, teslimler/kapak-29-ekim-story.png
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from ciz import H, W, _ac, _esik, arazi, buyut, cimen_tutamlari, gradyan, gunes, hex2, piksel, sirt, yeni, yildizlar  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SILUET = "#140a10"
YIL = 2026


def piksel_yazi(img, metin, y, boy, renk, kontur="#3a0a10", golge=None, aralik=1):
    """Ortalanmış piksel yazı: font ızgarada küçük çizilir, eşikle keskinleştirilir (kenar yumuşatma yok)."""
    font = ImageFont.truetype(FONT, boy)
    katman = Image.new("L", (W, boy * 2))
    d = ImageDraw.Draw(katman)
    genislik = sum(d.textlength(h, font=font) + aralik for h in metin)
    x = (W - genislik) / 2
    for h in metin:
        d.text((x, 0), h, font=font, fill=255)
        x += d.textlength(h, font=font) + aralik
    piks = katman.load()
    k, r = hex2(kontur), hex2(renk)
    for yy in range(katman.height):
        for xx in range(W):
            if piks[xx, yy] > 110:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1)):
                    if 0 <= xx + dx < W:
                        img.putpixel((xx + dx, y + yy + dy), k)
                if golge:
                    img.putpixel((xx, min(H - 1, y + yy + 2)), hex2(golge))
    for yy in range(katman.height):
        for xx in range(W):
            if piks[xx, yy] > 110:
                img.putpixel((xx, y + yy), r)


def ay_yildiz(img, cx, cy, r, renk="#ffffff"):
    """Bayraktaki oranlarla hilal ve beş köşeli yıldız (hilal sağa açık, yıldız ağzında)."""
    d = ImageDraw.Draw(img)
    beyaz = hex2(renk)
    dis = Image.new("L", img.size, 0)
    dd = ImageDraw.Draw(dis)
    dd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    ic_r = r * 0.8
    ic_cx = cx + r * 0.4375 / 0.5 * 0.5  # bayrak oranı: iç daire merkezi dışın 1/16 boy kadar sağda
    dd.ellipse([ic_cx - ic_r, cy - ic_r, ic_cx + ic_r, cy + ic_r], fill=0)
    yildiz_cx = cx + r * 1.25
    yr = r * 0.5
    noktalar = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = yr if i % 2 == 0 else yr * 0.4
        noktalar.append((yildiz_cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    dd.polygon(noktalar, fill=255)
    piks = dis.load()
    for y in range(max(0, int(cy - r - 2)), min(H, int(cy + r + 3))):
        for x in range(max(0, int(cx - r - 2)), min(W, int(yildiz_cx + yr + 3))):
            if piks[x, y] > 127:
                img.putpixel((x, y), beyaz)


def siluet(img, ciz_fn, *args, renk=SILUET, **kw):
    """Figürü ayrı katmanda çizip tek renk silüete çevirir, sonra sahneye bindirir."""
    kat = yeni(img.width, img.height)
    ciz_fn(kat, *args, **kw)
    piks = kat.load()
    k = hex2(renk)
    for y in range(kat.height):
        for x in range(kat.width):
            if piks[x, y][3] > 40:
                piks[x, y] = k
    img.alpha_composite(kat)
    return kat


def ata_siluet(kat, x, y, s):
    """Kocatepe anıt duruşu: uzun bacaklı at, dik oturan binici, kalpak, rüzgârda geriye uçan pelerin; tek renk."""
    d = ImageDraw.Draw(kat)
    k = (0, 0, 0, 255)
    gov_y = y - int(11 * s)
    d.ellipse([x - int(9 * s), gov_y - int(4 * s), x + int(8 * s), gov_y + int(3.5 * s)], fill=k)  # gövde
    d.polygon([(x + int(5 * s), gov_y - int(3 * s)), (x + int(9 * s), gov_y - int(2 * s)), (x + int(13 * s), gov_y - int(11 * s)),
               (x + int(10.5 * s), gov_y - int(12.5 * s))], fill=k)  # boyun
    d.polygon([(x + int(10 * s), gov_y - int(12.5 * s)), (x + int(14 * s), gov_y - int(12 * s)), (x + int(17 * s), gov_y - int(9 * s)),
               (x + int(15.5 * s), gov_y - int(8 * s)), (x + int(12 * s), gov_y - int(9.5 * s))], fill=k)  # baş
    d.polygon([(x + int(11.5 * s), gov_y - int(12.5 * s)), (x + int(12.5 * s), gov_y - int(15 * s)), (x + int(13.5 * s), gov_y - int(12.5 * s))], fill=k)  # kulak
    for lx0, lx1 in ((-7.5, -8.5), (-5, -4.5), (4, 3.5), (6.5, 7.5)):  # dört uzun bacak zemine basar
        d.line([x + int(lx0 * s), gov_y + int(1 * s), x + int(lx1 * s), y - 1], fill=k, width=max(2, int(1.7 * s)))
        d.line([x + int(lx1 * s) - int(1 * s), y - 1, x + int(lx1 * s) + int(1.2 * s), y - 1], fill=k, width=max(1, int(0.8 * s)))
    d.polygon([(x - int(9 * s), gov_y - int(2 * s)), (x - int(15 * s), gov_y + int(4 * s)), (x - int(13 * s), gov_y + int(6 * s)),
               (x - int(8.5 * s), gov_y + int(1 * s))], fill=k)  # kuyruk
    # binici: dik oturur, sağa (güneşe) bakar; at boyuna göre insan oranı
    bel = gov_y - int(3.5 * s)
    omuz = bel - int(7 * s)
    d.polygon([(x - int(1.6 * s), bel), (x + int(1.8 * s), bel), (x + int(2.1 * s), omuz), (x - int(2.0 * s), omuz)], fill=k)  # gövde
    d.line([x + int(1.2 * s), bel, x + int(2.4 * s), gov_y + int(3.5 * s)], fill=k, width=max(2, int(1.4 * s)))  # bacak üzengide
    d.line([x + int(1.6 * s), omuz + int(1.2 * s), x + int(6.5 * s), omuz + int(5.5 * s)], fill=k, width=max(2, int(1.1 * s)))  # kol dizgine
    bas_y = omuz - int(2.2 * s)
    r = int(1.7 * s)
    d.ellipse([x - r, bas_y - r, x + r, bas_y + r], fill=k)
    d.chord([x - r - 1, bas_y - r - int(2.4 * s), x + r + 1, bas_y + int(0.6 * s)], 180, 360, fill=k)  # kalpak (yuvarlak tepe)
    d.rectangle([x - r - 1, bas_y - r - int(0.3 * s), x + r + 1, bas_y - int(0.2 * s)], fill=k)
    # pelerin: omuzdan geriye rüzgârla uçar, ucu iki dilli ve dalgalı
    d.polygon([(x - int(2.0 * s), omuz + int(0.5 * s)), (x - int(1.2 * s), bel + int(1 * s)), (x - int(7 * s), bel + int(2.5 * s)),
               (x - int(10 * s), bel), (x - int(13 * s), bel - int(2 * s)), (x - int(11 * s), bel - int(3.5 * s)),
               (x - int(14.5 * s), bel - int(6 * s)), (x - int(9 * s), bel - int(5.5 * s)), (x - int(5 * s), omuz + int(1 * s))], fill=k)
    return kat


def poster():
    img = yeni()
    # gökyüzü: tepede lacivert gece, aşağıda kızıl şafak, ufukta altın
    gradyan(img, ["#0c0618", "#2a0a24", "#6a1020", "#a8161e", "#d42a22", "#e8562a", "#f4a040"])
    yildizlar(img, 110, 300, "#ffe8d0", 29)
    ay_yildiz(img, 236, 240, 76)
    gunes(img, 300, 578, 52, ["#fff4c8", "#ffd060", "#f08030"])
    # uzak sıradağlar, önde Kocatepe sırtı; tepe üstü düz (atın durduğu yer)
    uzak = sirt(575, 24, 7, 3, 2, w=W)
    arazi(img, uzak, ["#5a1a22", "#4a141e", "#3a1018"], None, doku_tohum=1)
    tepe = sirt(640, 26, 29, 2.2, 1.5, w=W)
    for x in range(W):
        kubbe = 78 * math.exp(-((x - 300) / 150) ** 2)
        tepe[x] = int(tepe[x] - kubbe)
    for x in range(230, 372):
        tepe[x] = min(tepe[x], 562)
    arazi(img, tepe, ["#2a0c14", "#200a10", "#18080c", "#120608"], None, doku_tohum=29, perspektif=True)
    cimen_tutamlari(img, tepe, ["#2a0c14", "#3a1018", "#200a10"], 29, 0.5, 4)
    siluet(img, ata_siluet, 300, 562, 4.3)
    # ön plan: koyu bozkır bandı (yazılar buraya gelir)
    on_z = sirt(612, 8, 31, 2, 1, w=W)
    arazi(img, on_z, ["#120408", "#0e0306", "#0a0204", "#080204"], None, doku_tohum=5)
    cimen_tutamlari(img, on_z, ["#1a0408", "#2a0a10"], 31, 0.6, 6)
    # yazılar (story güvenli alanı: ızgara y 125-835)
    piksel_yazi(img, "29 EKİM", 628, 60, "#fff4e0", "#2a0408", golge="#5a0a10", aralik=2)
    piksel_yazi(img, "CUMHURİYET BAYRAMI", 708, 23, "#ffd060", "#2a0408", aralik=2)
    piksel_yazi(img, f"1923 · {YIL - 1923}. YIL", 742, 16, "#fff4e0", "#2a0408", aralik=2)
    piksel_yazi(img, "NE MUTLU TÜRKÜM DİYENE!", 778, 28, "#fff4e0", "#2a0408", golge="#5a0a10", aralik=2)
    piksel_yazi(img, "@pikseltarihim", 818, 13, "#c89a70", "#0a0204", aralik=1)
    # ince kenar çerçeve (piksel)
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, W - 5, H - 5], outline=hex2("#ffd060"))
    d.rectangle([6, 6, W - 7, H - 7], outline=hex2("#8a1018"))
    return buyut(img)


def katmanlar():
    """Remotion için yazısız katmanlar (1080x1920): 29ekim-gok (gök, ay-yıldız, güneş), 29ekim-orta (dağlar + atlı silüet,
    saydam), 29ekim-on (ön bozkır bandı, saydam)."""
    gok = yeni()
    gradyan(gok, ["#0c0618", "#2a0a24", "#6a1020", "#a8161e", "#d42a22", "#e8562a", "#f4a040"])
    yildizlar(gok, 110, 300, "#ffe8d0", 29)
    ay_yildiz(gok, 236, 240, 76)
    gunes(gok, 300, 578, 52, ["#fff4c8", "#ffd060", "#f08030"])
    orta = yeni()
    uzak = sirt(575, 24, 7, 3, 2, w=W)
    arazi(orta, uzak, ["#5a1a22", "#4a141e", "#3a1018"], None, doku_tohum=1)
    tepe = sirt(640, 26, 29, 2.2, 1.5, w=W)
    for x in range(W):
        kubbe = 78 * math.exp(-((x - 300) / 150) ** 2)
        tepe[x] = int(tepe[x] - kubbe)
    for x in range(230, 372):
        tepe[x] = min(tepe[x], 562)
    arazi(orta, tepe, ["#2a0c14", "#200a10", "#18080c", "#120608"], None, doku_tohum=29, perspektif=True)
    cimen_tutamlari(orta, tepe, ["#2a0c14", "#3a1018", "#200a10"], 29, 0.5, 4)
    siluet(orta, ata_siluet, 300, 562, 4.3)
    on_ = yeni()
    on_z = sirt(612, 8, 31, 2, 1, w=W)
    arazi(on_, on_z, ["#120408", "#0e0306", "#0a0204", "#080204"], None, doku_tohum=5)
    cimen_tutamlari(on_, on_z, ["#1a0408", "#2a0a10"], 31, 0.6, 6)
    hedef = KOK / "video" / "public"
    for ad, im in (("29ekim-gok", gok), ("29ekim-orta", orta), ("29ekim-on", on_)):
        buyut(im).save(hedef / f"{ad}.png")
    print("katmanlar:", hedef)


if __name__ == "__main__":
    if "--katmanlar" in sys.argv:
        katmanlar()
        sys.exit()
    out = poster()
    (KOK / "video" / "public").mkdir(exist_ok=True)
    out.save(KOK / "video" / "public" / "kapak-29-ekim.png")
    out.save(KOK / "teslimler" / "kapak-29-ekim-story.png")
    print("kapak-29-ekim.png", out.size)
