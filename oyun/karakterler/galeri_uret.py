"""Galeri sayfalarını kadrodan yeniden üretir: galeri.html (kartlar), galeri3b.html (KADRO verisi), kadro.png.
Kullanım: python3 -I oyun/karakterler/galeri_uret.py"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).parent
sys.path.insert(0, str(KOK))
from PIL import Image  # noqa: E402

import karakterler as k  # noqa: E402

GRUPLAR = [("Halk", "Köyden kervana, tekkeden dağa"), ("Kapıkulu", "Ocağın merdiveni: acemiden ağaya"),
           ("Taşra ve Saray", "Uçtan divana, tımardan tahta"), ("Karşı Cephe", "Tuna'nın öte yakası"),
           ("Gölgeler", "Mühürlü mektuplar, sahte kimlikler")]
RENK = {"Halk": "#7aa05a", "Kapıkulu": "#4a7ad8", "Taşra ve Saray": "#d8a83a", "Karşı Cephe": "#d0443a", "Gölgeler": "#a87ad8"}


def galeri():
    s = (KOK / "galeri.html").read_text()
    bolum, n = [], 0
    for g, alt in GRUPLAR:
        kartlar = []
        for d in k.KADRO:
            if d["sinif"] != g:
                continue
            n += 1
            kartlar.append(f'''<figure class="kart" style="--sinif:{RENK[g]}">
  <img src="cikti/{d["kod"]}.png" width="512" height="704" alt="{html.escape(d["ad"])} piksel portresi" loading="lazy">
  <figcaption><span class="no">{n:02d}</span><h3>{html.escape(d["ad"])}</h3><p>{html.escape(d["aciklama"])}</p></figcaption>
</figure>''')
        bolum.append(f'<section style="--sinif:{RENK[g]}"><header class="bolum"><h2>{g}</h2><span>{alt} · {len(kartlar)} karakter</span>'
                     f'</header>\n<div class="izgara">{"".join(kartlar)}</div></section>')
    bas = s.index("<section"), s.index("<footer>")
    s = s[:bas[0]] + "".join(bolum) + "\n" + s[bas[1]:]
    s = re.sub(r"ilk \d+ karakteri", f"{len(k.KADRO)} karakteri", s)
    s = re.sub(r"<b>\d+</b> karakter", f"<b>{len(k.KADRO)}</b> karakter", s)
    s = re.sub(r"<b>\d+</b> sınıf", f"<b>{len(GRUPLAR)}</b> sınıf", s)
    (KOK / "galeri.html").write_text(s)


def galeri3b():
    s = (KOK / "galeri3b.html").read_text()
    veri = json.dumps([dict(kod=d["kod"], ad=d["ad"], sinif=d["sinif"], aciklama=d["aciklama"], renk=RENK[d["sinif"]])
                       for d in k.KADRO], ensure_ascii=False)
    s = re.sub(r"const KADRO = \[.*?\];\n", lambda m: f"const KADRO = {veri};\n", s, flags=re.S)
    s = re.sub(r"goster\((\d+|KADRO\.findIndex\([^)]*\))\); requestAnimationFrame",
               'goster(KADRO.findIndex(k => k.kod === "yeniceri_neferi")); requestAnimationFrame', s)
    (KOK / "galeri3b.html").write_text(s)


def toplu():
    ims = [Image.open(KOK / "cikti" / f"{d['kod']}.png") for d in k.KADRO]
    w, h = ims[0].width // 2, ims[0].height // 2
    sut = 6
    sat = -(-len(ims) // sut)
    s = Image.new("RGB", (w * sut, h * sat), (20, 17, 26))
    for i, im in enumerate(ims):
        s.paste(im.resize((w, h), Image.NEAREST), ((i % sut) * w, (i // sut) * h))
    s.save(KOK / "kadro.png")


if __name__ == "__main__":
    k.uret(KOK / "cikti")
    galeri()
    galeri3b()
    toplu()
    print("tamam:", len(k.KADRO), "karakter")
