"""Gündüz kapağı (sahibin ikinci örneğine göre): mavi gök, ufukta turuncu gün batımı, yeşil bozkır ve mavi nehir,
sağda sancaklı atlı ordu, solda büyük sancak; ortada açık renk kürk börklü Cengiz Han, kılıcı aşağıda çapraz,
sağ altta atının başı. Başlık üstte, logo altta (Remotion: KapakGunduz).

Çıktı: video/public/kapak-cengiz-gunduz.png (540x960 ızgara).
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import ImageDraw  # noqa: E402

import kapak_cengiz as kc  # noqa: E402
from ciz import H, W, _esik, arazi, at, bulut, buyut, figur, gradyan, gunes, hex2, piksel, sirt, yeni  # noqa: E402

UFUK = 600


def gok(img):
    gradyan(img, ["#1a3e8a", "#2456a8", "#3a74c0", "#6a9ad0", "#c8a890", "#f0a050", "#f8c060"], 0, UFUK)
    for i, (x, y, b) in enumerate([(60, 40, 34), (470, 50, 30), (130, 245, 30), (300, 268, 26), (480, 238, 34), (220, 330, 22)]):
        bulut(img, x, y, b, ["#fff0d8", "#f8c898", "#d88a60"], 30 + i)


def daglar(img):
    z = sirt(548, 28, 33, 6, 6)
    for x, zz in enumerate(z):
        for y in range(zz, UFUK + 2):
            yuk = y - zz
            if yuk < 10 + (x * 5 % 7) and zz < 552:
                renk = "#f4f0f0" if _esik(x, y) < 0.8 or yuk < 4 else "#b8c0d8"
            else:
                renk = "#5a6aa0" if (x // 9) % 2 else "#4a5a90"
            piksel(img, x, y, hex2(renk))
        piksel(img, x, zz, hex2("#ffd0a0"))


def ova(img):
    z = [UFUK] * W
    arazi(img, z, ["#8ab84a", "#7aa842", "#6a983a", "#5a8832", "#4a782a", "#3a6824", "#2e581e"], "#c8e078", doku_tohum=4,
          perspektif=True)
    d = ImageDraw.Draw(img)
    for i in range(420):  # kıvrılan mavi nehir, sağa doğru açılır
        t = i / 420
        x = 300 + t * 260 + math.sin(t * 6) * 26
        y = UFUK + 3 + t * t * 120
        gen = 2 + t * 18
        d.line([(x - gen, y), (x + gen, y)], fill=hex2("#6aa8e0" if (i // 7) % 3 else "#b8dcf8"))
        d.line([(x - gen - 1, y + 1), (x - gen + 2, y + 1)], fill=hex2("#2e581e"))


def ordu(img):
    rnd = random.Random(21)
    for sira, (yz, s) in enumerate(((UFUK + 30, 1.0), (UFUK + 58, 1.35), (UFUK + 92, 1.7))):
        z = [yz] * W
        for x in range(300 + sira * 6, 548, int(26 * s)):
            figur(img, at, x + rnd.randint(-5, 5), z, s, -1, rnd.choice(("#3a2418", "#4a2e1e", "#5a3a24", "#2a1810")), "#120806",
                  binici=rnd.choice(("#4a2a2a", "#3a3a4a", "#5a3a22")), faz=rnd.random(), kontur="#1a0a06")
        for x in range(316 + sira * 10, 548, int(70 * s)):
            kc.sancak(img, x, yz, x, yz - int(46 * s), int(18 * s), faz=x * 0.1, sus=False)
    z = [UFUK + 40] * W  # sol tarafta, büyük sancağın arkasında ikinci birlik
    for x in range(8, 150, 22):
        figur(img, at, x, z, 1.15, 1, rnd.choice(("#3a2418", "#4a2e1e")), "#120806", binici="#3a2a2a", faz=rnd.random(), kontur="#1a0a06")
    for x in (30, 90, 140):
        kc.sancak(img, x, UFUK + 40, x, UFUK - 12, 24, faz=x * 0.2, sus=False)


def main():
    img = yeni()
    gok(img)
    gunes(img, 380, 552, 52, ["#ffe090", "#ffb050"])
    kc.kartal(img, 392, 196, 1.9, faz=0.25)  # büyük kartal göğü boydan geçer
    for x, y, s in ((300, 150, 0.45), (330, 128, 0.35), (470, 300, 0.4), (120, 180, 0.38)):
        kc.kartal(img, x, y, s, faz=0.6)
    daglar(img)
    ova(img)
    ordu(img)
    kc.sancak(img, 12, 960, 22, 300, 170, faz=0.4)  # büyük sancak
    kc.BORK.update({"kenar": "#d8c8a8", "tel": ("#f4ecd8", "#b8a888", "#e8dcc0"), "tuy": ("#a81a14", "#d8301e")})
    figur(img, kc.han, 226, 540, 1.75, kontur="#120604", f_isik=0.1, f_golge=0.18)
    figur(img, kc.at_basi, 452, 858, 2.3, kontur="#0a0402", f_isik=0.12, f_golge=0.2)
    for x in range(W):  # ön planda çimen
        for k in range(int(6 + 6 * (0.5 + 0.5 * math.sin(x / 7)))):
            piksel(img, x, H - 1 - k, hex2("#3a6a24" if k < 6 else "#5a8a32"))
    hedef = Path(__file__).parents[1] / "public" / "kapak-cengiz-gunduz.png"
    img.save(hedef)
    print("yazıldı:", hedef)
    if "--onizleme" in sys.argv:
        buyut(img).save(sys.argv[sys.argv.index("--onizleme") + 1])


if __name__ == "__main__":
    main()
