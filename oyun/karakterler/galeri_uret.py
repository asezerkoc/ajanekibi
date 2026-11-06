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


def render_listesi():
    """render/render.js için kadro: her karakterin arka plan ve zemin renkleri."""
    from motor import palet
    liste = []
    for d in k.KADRO:
        r = k.SINIF_RENK[d["sinif"]]
        z = palet(r["toprak"])
        liste.append(dict(kod=d["kod"], gok=list(r["gok"]), zemin=["#%02x%02x%02x" % z[0], "#%02x%02x%02x" % z[1]], aci=0.2))
    (KOK / "render" / "kadro.json").write_text(json.dumps(liste, ensure_ascii=False, indent=1))


def cerceve():
    """Ham render'lara sınıf renginde ince çerçeve: cikti/render/<kod>.png"""
    from PIL import ImageDraw
    for d in k.KADRO:
        ham = KOK / "cikti" / "render" / f"{d['kod']}_ham.png"
        if not ham.exists():
            continue
        im = Image.open(ham).convert("RGB")
        dr = ImageDraw.Draw(im)
        renk = k.SINIF_RENK[d["sinif"]]["vurgu"]
        for i in range(6):
            dr.rectangle([i, i, im.width - 1 - i, im.height - 1 - i], outline=renk)
        dr.rectangle([6, 6, im.width - 7, im.height - 7], outline=(22, 12, 18))
        im.save(KOK / "cikti" / "render" / f"{d['kod']}.png")


def toplu(alt="", ad="kadro.png"):
    ims = [Image.open(KOK / "cikti" / alt / f"{d['kod']}.png") for d in k.KADRO]
    w, h = ims[0].width // 2, ims[0].height // 2
    sut = 6
    sat = -(-len(ims) // sut)
    s = Image.new("RGB", (w * sut, h * sat), (20, 17, 26))
    for i, im in enumerate(ims):
        s.paste(im.resize((w, h), Image.NEAREST), ((i % sut) * w, (i // sut) * h))
    s.save(KOK / ad)


def galeri_render():
    """Aynı galerinin voksel render'lı hâli: galeri_render.html"""
    s = (KOK / "galeri.html").read_text()
    s = s.replace('src="cikti/', 'src="cikti/render/').replace('width="512" height="704"', 'width="768" height="1056"')
    s = s.replace("<title>Ocak ve Rumeli Kadrosu</title>", "<title>Ocak ve Rumeli Kadrosu 3B</title>")
    s = s.replace("<h1>Ocak ve Rumeli Kadrosu</h1>", "<h1>Ocak ve Rumeli Kadrosu 3B</h1>")
    s = s.replace("piksel portresi", "voksel render")
    s = re.sub(r"<p>Osmanlı Balkanlarında.*?</p>", "<p>Piksel kadronun her karakteri küplere dönüştürüldü ve stüdyo ışığında render edildi: "
               "köşelerde birikmiş gölge, pahlı küp kenarları, yere düşen yumuşak gölge. Bütün karakterler aynı ışık ve kamera "
               "açısıyla, birbirleriyle tutarlı.</p>", s, flags=re.S)
    s = s.replace("<span>ızgara <b>128×176</b></span><span>ekranda <b>4×</b></span>", "<span>render <b>768×1056</b></span>")
    (KOK / "galeri_render.html").write_text(s)


if __name__ == "__main__":
    k.uret(KOK / "cikti")
    galeri()
    galeri3b()
    render_listesi()
    cerceve()
    galeri_render()
    toplu()
    toplu("render", "kadro_render.png")
    print("tamam:", len(k.KADRO), "karakter")
