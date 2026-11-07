"""Grafikerin skill referanslarını kaynak koddan üretir (skills/piksel-sahne/references/).

- fonksiyonlar.md: ciz, sahneler, timur_figur, timur ve kayip_mezar modüllerindeki çizim fonksiyonlarının imzaları ve
  açıklamaları (sahneNN fonksiyonları hariç).
- sahne-katalogu.md: bütün sahneNN fonksiyonları: konu (docstring), katmanlar, sprite kare boyu, kaynak satırı ve
  videodaki Bolum ayarı (TSX dosyalarından okunur).

Yeni bir figür ya da sahne fonksiyonu eklendikten sonra çalıştır: python3 -I video/piksel/skill_uret.py
Kod çalıştırmaz, yalnızca kaynak dosyaları okur (ast).
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
PIKSEL = KOK / "video" / "piksel"
SAHNELER_TSX = KOK / "video" / "src" / "sahneler"
HEDEF = KOK / "skills" / "piksel-sahne" / "references"

MODULLER = [
    ("ciz.py", "ciz — temel çizim, arazi, insan/at/yurt gibi temel figürler ve fizik denetimleri"),
    ("sahneler.py", "sahneler — katman üreticileri (gökyüzü, uzak, orta, ön, sprite)"),
    ("timur_figur.py", "timur_figur — tarihî kişiler, hayvanlar, yapılar ve araçlar"),
    ("timur.py", "timur — yardımcılar: hava, iç mekân, ateş, mum, tabut, tabela…"),
    ("kayip_mezar.py", "kayip_mezar — orman, nöbetçi, cenaze arabası, at sürüsü"),
    ("pasa.py", "pasa — darağacı, asılı adam, kahkaha atan paşa"),
]
SAHNE_DOSYALARI = ["sahneler.py", "kayip_mezar.py", "timur.py", "pasa.py"]
ATLA = {"main", "kaydet", "onizleme"}
OZEL_ALT = {"_alay", "_dag_ormani"}  # alt çizgili ama grafikerin kullanabileceği yardımcılar

# Docstring'i olmayan eski sahneler (Cengiz Han ve Kayıp Mezar) için kısa konu açıklamaları
KONULAR = {
    1: "Şafakta yurt, bacadan duman, otlayan iki at (Cengiz Han açılışı).",
    2: "Gün batımı: büyük yurt, kapı ışığı, kucağında bebekle anne; orta planda duran atlar.",
    3: "Göç: yürüyen aile (anne ve üç çocuk) önde, ufukta öküzlü kağnı kervanı (ikinci sprite 'ufuk' tabanında).",
    4: "Kafile: beş atlı sola gider, haritada piksel ok (sahne4-ok.png).",
    5: "Kurultay kampı: sekiz yurt, boylar, ortada dalgalanan tuğ (sprite), kamp ateşleri.",
    6: "Ordu kolonu ve ufukta surlu Orta Asya şehri, damlardan duman (iki sprite: zemin + ufuk).",
    7: "Alacakaranlık: ağaç altında eyerli at, ateş böcekleri (parıltı pikselleri), yıldızlı gök.",
    8: "Gece: ovoo taş yığını, sallanan kır çiçeği yakın plan; yıldızlar.",
    11: "Gece kampı (Kayıp Mezar): yurtlar, ateşler, tuğ ve iki meşaleli nöbetçi.",
    12: "Cenaze alayı gündüz: yas tutanlar, öküzlü cenaze arabası, atlı muhafızlar; arkada ikinci kalabalık sırası.",
    13: "Aynı alay kızıl gün batımında (aynı _alay kalıbı, farklı palet).",
    14: "Dağ ormanında yas tutanlar, taze mezar höyüğü.",
    15: "Binicisiz at sürüsü dörtnala, toz; iki atlı sürücü (at_suru).",
    16: "Gece sınır: sınır taşları ve nöbetçiler; dağ ormanı.",
    17: "Bugün: yıldızlı gece, ormanlı dağ; gökte kodla süzülen uydu (sahne17-uydu.png).",
}


def imza(n: ast.FunctionDef) -> str:
    args = []
    d, pos = n.args.defaults, n.args.args
    nd = len(pos) - len(d)
    for i, a in enumerate(pos):
        args.append(f"{a.arg}={ast.unparse(d[i - nd])}" if i >= nd else a.arg)
    if n.args.vararg:
        args.append("*" + n.args.vararg.arg)
    for a, dv in zip(n.args.kwonlyargs, n.args.kw_defaults):
        args.append(f"{a.arg}={ast.unparse(dv)}" if dv else a.arg)
    return f"{n.name}({', '.join(args)})"


def fonksiyonlar() -> int:
    cik = [
        "# Fonksiyon referansı (kaynak koddan üretildi)\n",
        "Her fonksiyonun imzası ve kaynak koddaki açıklaması. `img`/`t` tuval (PIL RGBA), `zemin`/`z` zemin listesi (her x için y),",
        "`x` ızgara x'i (figürün ayak izi merkezi), `s` ölçek (1.0 = temel boy), `yon` 1 sağa / -1 sola bakar, `faz`/`adim` 0-1 hareket döngüsü.",
        "Figürler `figur(img, fn, x, zemin, ...)` ile çağrılır (kontur + ışık/gölge işler; bkz. SKILL.md).\n",
    ]
    say = 0
    for dosya, baslik in MODULLER:
        yol = PIKSEL / dosya
        tree = ast.parse(yol.read_text(encoding="utf-8"))
        cik.append(f"\n## {baslik}\n\n`from {yol.stem} import ...` (dosya: `video/piksel/{dosya}`)\n")
        for n in tree.body:
            if not isinstance(n, ast.FunctionDef) or n.name.startswith("sahne") or n.name in ATLA:
                continue
            if n.name.startswith("_") and n.name not in OZEL_ALT:
                continue
            doc = ast.get_docstring(n) or "(açıklama yok; kaynak koda bak)"
            doc = " ".join(satir.strip() for satir in doc.splitlines())
            cik.append(f"- **`{imza(n)}`** — {doc}")
            say += 1
    (HEDEF / "fonksiyonlar.md").write_text("\n".join(cik) + "\n", encoding="utf-8")
    return say


def bolum_ayarlari() -> dict[int, tuple[str, str]]:
    """TSX dosyalarındaki `no: N, ...` satırlarından her sahnenin Bolum ayarını okur."""
    ayar = {}
    for tsx in sorted(SAHNELER_TSX.glob("*.tsx")):
        if tsx.name in ("TimurSeri.tsx", "Kapak.tsx", "Tanitim.tsx"):
            continue
        for m in re.finditer(r"no: (\d+),([^\n]*)", tsx.read_text(encoding="utf-8")):
            ayar[int(m.group(1))] = (tsx.name, m.group(2).strip().rstrip(","))
    return ayar


def katalog() -> int:
    ayar = bolum_ayarlari()
    kat = [
        "# Örnek sahne kataloğu\n",
        "Ajansın onaylanmış videolarındaki bütün sahneler. Yeni bir sahne tasarlarken en yakın örneği bul,",
        "kaynak satırlarını oku ve aynı kalıpla yaz. Sütunlar: sprite = `sprite(no, ek, w, h, KARE, kare)` çağrısındaki kare boyu; TSX = videodaki `Bolum` ayarı.\n",
    ]
    say = 0
    for dosya in SAHNE_DOSYALARI:
        yol = PIKSEL / dosya
        src = yol.read_text(encoding="utf-8")
        tree = ast.parse(src)
        kat.append(f"\n## video/piksel/{dosya}\n")
        kat.append("| Sahne | Konu | Katmanlar / sprite | Kaynak | TSX `Bolum` |\n|---|---|---|---|---|")
        sahneler = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("sahne") and n.name[5:].isdigit()]
        for n in sorted(sahneler, key=lambda n: int(n.name[5:])):
            no = int(n.name[5:])
            govde = ast.get_source_segment(src, n) or ""
            konu = (ast.get_docstring(n) or KONULAR.get(no, "")).replace("\n", " ").replace("|", "/")
            katmanlar = [k.rstrip("(") for k in ("ic_mekan", "gokyuzu", "uzak", "orta", "on(", "hava", "kar_ortusu", "silik_sehir", "parsomen") if k in govde]
            spritelar = re.findall(r"sprite\(\s*(?:no|\d+)\s*,\s*\"(\w+)\",\s*(\d+),\s*(\d+)", govde)
            if "_alay(" in govde:  # ortak kalıp: katmanlar ve sprite _alay içinde
                katmanlar, spritelar = ["gokyuzu", "uzak", "orta", "on"], [("karakter", "540", "150")]
            sp = ", ".join(f"{e} {w}×{h}" for e, w, h in spritelar) or "—"
            if no in ayar:
                tsx = f"{ayar[no][0]}: `{ayar[no][1]}`"
            else:
                tsx = "CengizHan.tsx (kendi sahne yapısı)"
            kat.append(f"| {no} | {konu} | {' + '.join(katmanlar)}; sprite: {sp} | `video/piksel/{dosya}:{n.lineno}` | {tsx} |")
            say += 1
    (HEDEF / "sahne-katalogu.md").write_text("\n".join(kat) + "\n", encoding="utf-8")
    return say


if __name__ == "__main__":
    HEDEF.mkdir(parents=True, exist_ok=True)
    print(f"fonksiyon: {fonksiyonlar()}, sahne: {katalog()} → {HEDEF}")
