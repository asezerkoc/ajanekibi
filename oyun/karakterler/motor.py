"""SKONSTART karakter motoru: 128-bit tarzı ayrıntılı piksel sanatı figürler.

64-bit sahne figürlerinden farkı: figür 128x176 ızgarada ~145 piksel boyunda çizilir (yaklaşık 7 kat daha
büyük), her malzeme 5 tonlu, renk kaydırmalı (gölgeler moru/maviye, ışıklar sarıya kayar) bir paletle
gölgelenir. Işık sol üstten gelir. Parçalar arasında koyu iç kontur, figürün dışında renge göre seçilen
(sel-out) kontur vardır. Kenar yumuşatma yoktur.

Bir karakter parçalardan kurulur: t.parca(z, renk, [şekiller], golge=...). Şekiller standart yetişkin
koordinatlarında yazılır; t.olcek(...) ile çocuk ya da genç boyuna ölçeklenir.
"""
from __future__ import annotations

import colorsys
import math
from contextlib import contextmanager

import numpy as np
from PIL import Image, ImageDraw

W, H = 128, 176
ZEMIN = 167  # ayak tabanının son satırı
CX = 64
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16 + 1 / 32
KONTUR = (22, 12, 18)


def _hex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _kaydir(h, hedef, miktar):
    """Ton açısını (0-1) hedef tona doğru en kısa yoldan kaydırır."""
    fark = ((hedef - h + 0.5) % 1.0) - 0.5
    return (h + fark * miktar) % 1.0


def palet(renk, n=5, kontrast=1.0):
    """Renk kaydırmalı ton dizisi: [en koyu ... en açık]; orta ton verilen renktir."""
    r, g, b = (c / 255 for c in _hex(renk))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    sonuc = []
    for i in range(n):
        k = (i - (n // 2)) / (n // 2) * kontrast  # -1..1
        if k < 0:
            hh = _kaydir(h, 0.72, 0.10 * -k)
            ll = l * (1 + 0.55 * k)
            ss = min(1, s * (1 + 0.12 * -k))
        else:
            hh = _kaydir(h, 0.13, 0.08 * k)
            ll = l + (1 - l) * 0.45 * k
            ss = s * (1 - 0.15 * k)
        rr, gg, bb = colorsys.hls_to_rgb(hh, max(0, min(1, ll)), max(0, min(1, ss)))
        sonuc.append((int(rr * 255), int(gg * 255), int(bb * 255)))
    return sonuc


# ---------------------------------------------------------------- şekiller


def E(x0, y0, x1, y1):
    return ("e", [(x0, y0), (x1, y1)])


def P(*pts):
    return ("p", list(pts))


def R(x0, y0, x1, y1):
    return ("r", [(x0, y0), (x1, y1)])


def L(*pts, w=2):
    return ("l", list(pts), w)


def C(x, y, r):
    return E(x - r, y - r, x + r, y + r)


def EKSI(sekil):
    """Şekli maskeden çıkarır."""
    return ("-",) + tuple(sekil)


# ---------------------------------------------------------------- dokular (değer üzerinde)


def kivrim(aralik=6, guc=0.14, faz=0.0, egim=0.0):
    """Kumaş kıvrımları: dikey dalgalı açık-koyu şeritler."""
    def f(x, y, v):
        return v + guc * np.sin((x + y * egim + faz) * 2 * np.pi / aralik)
    return f


def zincir():
    """Zırh örgüsü: halka deseni."""
    def f(x, y, v):
        m = ((x + (y // 2) % 2) % 2 == 0) & (y % 2 == 0)
        return v + np.where(m, 0.18, -0.05)
    return f


def kurk(tohum=1, guc=0.25):
    rnd = np.random.default_rng(tohum)
    gurultu = rnd.random((H, W))

    def f(x, y, v):
        return v + (gurultu[y, x] - 0.5) * guc + 0.08 * np.sin(y * 1.3 + x * 0.4)
    return f


def yatay_cizgi(aralik=3, guc=0.15):
    def f(x, y, v):
        return v + np.where(y % aralik == 0, -guc, 0.0)
    return f


def birlestir(*dokular):
    def f(x, y, v):
        for d in dokular:
            v = d(x, y, v)
        return v
    return f


# ---------------------------------------------------------------- tuval


class Tuval:
    def __init__(self, w=W, h=H):
        self.w, self.h = w, h
        self.parcalar = []
        self.ayrinti = []
        self._donusum = []

    # -------- dönüşüm (çocuk, genç boyu)
    @contextmanager
    def olcek(self, s, ax=CX, ay=ZEMIN):
        self._donusum.append((s, ax, ay))
        try:
            yield
        finally:
            self._donusum.pop()

    def _d(self, x, y):
        for s, ax, ay in reversed(self._donusum):
            x, y = ax + (x - ax) * s, ay + (y - ay) * s
        return x, y

    def _s(self):
        s = 1.0
        for k, _, _ in self._donusum:
            s *= k
        return s

    def _maske(self, sekiller):
        im = Image.new("L", (self.w, self.h), 0)
        d = ImageDraw.Draw(im)
        for sk in sekiller:
            eksi = sk[0] == "-"
            if eksi:
                sk = sk[1:]
            renk = 0 if eksi else 255
            tur, pts = sk[0], [self._d(*p) for p in sk[1]]
            if tur == "e":
                (x0, y0), (x1, y1) = pts
                d.ellipse([min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)], fill=renk)
            elif tur == "r":
                (x0, y0), (x1, y1) = pts
                d.rectangle([min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)], fill=renk)
            elif tur == "p":
                d.polygon(pts, fill=renk)
            elif tur == "l":
                w = max(1, int(round(sk[2] * self._s())))
                d.line(pts, fill=renk, width=w, joint="curve")
                if w >= 3:
                    r = w / 2 - 0.5
                    for x, y in (pts[0], pts[-1]):
                        d.ellipse([x - r, y - r, x + r, y + r], fill=renk)
        return np.array(im) > 127

    def parca(self, z, renk, sekiller, golge="silindir", doku=None, isik=0.0, desen=None, kontur=True,
              kontrast=1.0, ramp=None):
        """renk: ana renk (hex) ya da hazır palet listesi. golge: silindir, kure, duz, yatay.
        desen: (satırlar, renk, adim_x, adim_y): desen pikselleri aynı gölge tonunda başka paletten boyanır."""
        p = ramp if ramp is not None else palet(renk, kontrast=kontrast)
        if desen:
            satirlar, drenk, ax, ay = desen
            desen = (satirlar, palet(drenk) if isinstance(drenk, str) else drenk, ax, ay)
        self.parcalar.append(dict(z=z, palet=p, maske=self._maske(sekiller), golge=golge, doku=doku,
                                  isik=isik, desen=desen, kontur=kontur, sira=len(self.parcalar)))

    def px(self, x, y, renk, z=1000):
        """Ayrıntı pikseli (göz, düğme, mücevher): gölgelenmez, en üste basılır."""
        x, y = self._d(x, y)
        self.ayrinti.append((z, int(round(x)), int(round(y)), _hex(renk) if isinstance(renk, str) else renk))

    def cizgi(self, x0, y0, x1, y1, renk, z=1000):
        (a, b), (c, d) = self._d(x0, y0), self._d(x1, y1)
        n = int(max(abs(c - a), abs(d - b))) + 1
        for i in range(n):
            t = i / max(1, n - 1)
            self.ayrinti.append((z, int(round(a + (c - a) * t)), int(round(b + (d - b) * t)),
                                 _hex(renk) if isinstance(renk, str) else renk))

    # -------- çizim
    def _deger(self, prc):
        m = prc["maske"]
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            return ys, xs, np.array([])
        # satır ve sütun açıklıkları
        sol = np.full(self.h, 10 ** 6)
        sag = np.full(self.h, -1)
        np.minimum.at(sol, ys, xs)
        np.maximum.at(sag, ys, xs)
        ust = np.full(self.w, 10 ** 6)
        alt = np.full(self.w, -1)
        np.minimum.at(ust, xs, ys)
        np.maximum.at(alt, xs, ys)
        u = (xs - (sol[ys] + sag[ys]) / 2) / np.maximum(1, (sag[ys] - sol[ys]) / 2)  # -1 sol, +1 sağ
        v = (ys - (ust[xs] + alt[xs]) / 2) / np.maximum(1, (alt[xs] - ust[xs]) / 2)  # -1 üst, +1 alt
        g = prc["golge"]
        if g == "silindir":
            val = 0.62 - 0.36 * u - 0.10 * v - 0.12 * np.clip(u - 0.6, 0, 1) * 2
        elif g == "kure":
            val = 0.66 - 0.30 * u - 0.28 * v - 0.18 * np.clip(np.hypot(u, v) - 0.75, 0, 1) * 3
        elif g == "yatay":
            val = 0.62 - 0.34 * v - 0.12 * u
        else:  # duz
            val = 0.58 - 0.12 * v - 0.06 * u
        val = val + prc["isik"]
        if prc["doku"] is not None:
            val = prc["doku"](xs, ys, val)
        return ys, xs, val

    def ciz(self, dis_kontur=True):
        n = 5
        idx = np.full((self.h, self.w), -1)
        pid = np.full((self.h, self.w), -1)
        sira = sorted(range(len(self.parcalar)), key=lambda i: (self.parcalar[i]["z"], self.parcalar[i]["sira"]))
        renk = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        for i in sira:
            prc = self.parcalar[i]
            ys, xs, val = self._deger(prc)
            if len(xs) == 0:
                continue
            t = np.clip(val, 0, 0.999) * n
            taban = np.floor(t)
            kesir = t - taban
            kesir = np.clip((kesir - 0.5) * 3.0 + 0.5, 0, 1)  # titreşim yalnızca ton sınırlarında
            esik = BAYER[ys % 4, xs % 4]
            k = np.clip(taban + (kesir > esik), 0, n - 1).astype(int)
            idx[ys, xs] = k
            pid[ys, xs] = i
            pal = np.array(prc["palet"])
            renk[ys, xs] = pal[k]
            if prc["desen"]:
                satirlar, dpal, ax, ay = prc["desen"]
                dh, dw = len(satirlar), len(satirlar[0])
                yy = (ys // 1) % ay
                xx = (xs + (ys // ay % 2) * (ax // 2)) % ax
                icinde = (yy < dh) & (xx < dw)
                sec = np.zeros(len(xs), dtype=bool)
                sec[icinde] = np.array([satirlar[a][b] != "." for a, b in zip(yy[icinde], xx[icinde])])
                dpal = np.array(dpal)
                renk[ys[sec], xs[sec]] = dpal[np.clip(k[sec] + 1, 0, n - 1)]
        # iç kontur: önde duran parçanın, arkadaki parçaya değen kenarı koyulaşır
        zz = np.full((self.h, self.w), -10 ** 6)
        for i, prc in enumerate(self.parcalar):
            zz[pid == i] = prc["z"]
        yeni = renk.copy()
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            komsu_pid = np.roll(np.roll(pid, dy, 0), dx, 1)
            komsu_z = np.roll(np.roll(zz, dy, 0), dx, 1)
            sinir = (pid >= 0) & (komsu_pid >= 0) & (komsu_pid != pid) & (zz > komsu_z)
            for y, x in zip(*np.nonzero(sinir)):
                prc = self.parcalar[pid[y, x]]
                if prc["kontur"]:
                    yeni[y, x] = prc["palet"][max(0, idx[y, x] - 3)]
        renk = yeni
        alfa = (pid >= 0).astype(np.uint8) * 255
        img = np.dstack([renk, alfa])
        # ayrıntılar
        for z, x, y, c in sorted(self.ayrinti, key=lambda a: a[0]):
            if 0 <= x < self.w and 0 <= y < self.h:
                img[y, x, :3] = c[:3]
                img[y, x, 3] = 255
        if not dis_kontur:  # 3B render: kontur yerine gerçek gölge kullanılır
            return Image.fromarray(img.astype(np.uint8), "RGBA")
        # dış kontur (sel-out): komşu rengin koyusu
        opak = img[:, :, 3] > 0
        dis = np.zeros_like(opak)
        kaynak = np.zeros((self.h, self.w, 3))
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            k = np.roll(np.roll(opak, dy, 0), dx, 1)
            kr = np.roll(np.roll(img[:, :, :3], dy, 0), dx, 1)
            yeni_kenar = (~opak) & k & (~dis)
            kaynak[yeni_kenar] = kr[yeni_kenar]
            dis |= yeni_kenar
        kc = np.array(KONTUR)
        kont = (kaynak * 0.28 + kc * 0.72).astype(np.uint8)
        img[dis, :3] = kont[dis]
        img[dis, 3] = 255
        return Image.fromarray(img.astype(np.uint8), "RGBA")


# ---------------------------------------------------------------- kart


def kart(figur: Image.Image, gok=("#2a2440", "#4a3a5a", "#8a5a5a", "#d89a6a"), toprak="#5a4a32",
         vurgu="#e0b040", olcek=4) -> Image.Image:
    """Karakter kartı: titreşimli gökyüzü, zemin şeridi, ayağın altına temas gölgesi, figür, çerçeve."""
    w, h = figur.size
    arka = np.zeros((h, w, 3), dtype=np.uint8)
    ramp = [np.array(_hex(c), dtype=float) for c in gok]
    ufuk = ZEMIN - 14
    adim = 12  # gökyüzü 12 ayrı renk bandına bölünür, bant sınırlarında dar titreşim
    for y in range(ufuk):
        t = y / max(1, ufuk - 1) * (len(ramp) - 1)
        i = min(int(t), len(ramp) - 2)
        f = t - i
        q = f * adim
        alt_k, kes = int(q), q - int(q)
        kes = min(1, max(0, (kes - 0.5) * 2.5 + 0.5))
        for x in range(w):
            k = alt_k + (1 if kes > BAYER[y % 4, x % 4] else 0)
            arka[y, x] = (ramp[i] + (ramp[i + 1] - ramp[i]) * min(1, k / adim)).astype(np.uint8)
    tp = palet(toprak)
    for y in range(ufuk, h):
        for x in range(w):
            d = (y - ufuk) / (h - ufuk)
            k = 3 if d < 0.15 else (2 if d < 0.5 else 1)
            if d > 0.15 and BAYER[y % 4, x % 4] < 0.12:
                k -= 1
            arka[y, x] = tp[k]
    for x in range(w):
        arka[ufuk, x] = tp[4]
    img = Image.fromarray(arka).convert("RGBA")
    # temas gölgesi: figürün ayaklarının basa olduğu genişlikte
    a = np.array(figur)[:, :, 3]
    taban = [x for x in range(w) if a[ZEMIN - 1:ZEMIN + 1, x].any()]
    golge = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(golge)
    if taban:
        x0, x1 = min(taban) - 6, max(taban) + 6
        gd.ellipse([x0, ZEMIN - 3, x1, ZEMIN + 4], fill=(20, 12, 10, 110))
    img = Image.alpha_composite(img, golge)
    img = Image.alpha_composite(img, figur)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline=_hex(vurgu))
    d.rectangle([1, 1, w - 2, h - 2], outline=KONTUR)
    return img.resize((w * olcek, h * olcek), Image.NEAREST)
