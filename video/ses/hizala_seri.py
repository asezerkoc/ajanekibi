"""Seri videolarını (Timur 1-3, Kayıp Mezar) seslendirmeye bire bir bağlar.

1. Baştaki sessizliği kırpar: konuşma videonun 0,3. saniyesinde (ilk ekran yazısıyla birlikte) başlar;
   sesi public/<ad>.mp3 olarak kaydeder.
2. Sessizlikleri ölçer. Her ekran yazısının başlangıcını, metnin okunma uzunluğuna göre tahmin eder ve en yakın
   konuşma duraklamasına (cümle sonu) oturtur.
3. TSX dosyasındaki her yazının `sure` değerini, bir sonraki yazı sesle aynı anda başlayacak biçimde yeniden yazar
   (sahne yapısı: yazı sahne başından 0,3 sn sonra başlar, sahneler arasında 0,5 sn boşluk vardır).

Kullanım: python3 -I video/ses/hizala_seri.py <ses.mp3> <Sahne.tsx> <public-adı> [--son "kapanışta okunan son cümle"]
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
BAS_PAYI = 0.3  # ilk yazı ve konuşma videonun bu saniyesinde başlar
SAHNE_ARASI = 0.5  # sahne süresi = yazı süreleri + 0,5; yazılar 0,3 sn geç başlar, dolayısıyla son yazı bitince sonraki sahnenin ilk yazısı 0,5 sn sonra başlar
EN_KISA = 0.9


def okunan_uzunluk(cumle: str) -> float:
    harf = len(re.sub(r"[^\wçğıöşüâÇĞİÖŞÜÂ]", "", cumle))
    return harf + sum(len(r) * 4 for r in re.findall(r"\d+", cumle))


def sessizlikler(ses: Path, ters=False) -> list[tuple[float, float]]:
    af = ("areverse," if ters else "") + "silencedetect=noise=-35dB:d=0.22"
    cikti = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(ses), "-af", af, "-f", "null", "-"],
                           capture_output=True, text=True).stderr
    bas = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", cikti)]
    son = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", cikti)]
    return list(zip(bas, son))


def sure(ses: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ses)],
                                capture_output=True, text=True).stdout)


def yazilari_bul(tsx: str):
    """TSX'teki yazı bloklarını sırayla bulur: (metin, sure başlangıç-bitiş konumu, sahne sırası)."""
    govde_bas = tsx.index("bolumler:") if "bolumler:" in tsx else tsx.index("BOLUMLER")
    govde_son = tsx.index("kapanis:") if "kapanis:" in tsx else tsx.index("const SAHNE_SURELERI")
    govde = tsx[govde_bas:govde_son]
    sahneler = re.split(r"\n    \{\n      no:|\n  \{\n    no:", govde)[1:]
    sonuc, taban = [], govde_bas
    for s_idx, blok in enumerate(sahneler):
        konum = tsx.index(blok, taban)
        for m in re.finditer(r"satirlar: \[([^\]]*)\],\s*sure: ([\d.]+)", blok):
            satirlar = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
            metin = " ".join(satirlar)
            sure_bas = konum + m.start(2)
            sure_son = konum + m.end(2)
            sonuc.append({"metin": metin, "sure_bas": sure_bas, "sure_son": sure_son, "sahne": s_idx})
        taban = konum + len(blok)
    return sonuc


def main():
    args = sys.argv[1:]
    son_cumle = None
    if "--son" in args:
        i = args.index("--son")
        son_cumle = args[i + 1]
        del args[i:i + 2]
    kaynak, tsx_yol, ad = Path(args[0]), Path(args[1]), args[2]

    bas_sessiz = sessizlikler(kaynak)
    konusma_bas = bas_sessiz[0][1] if bas_sessiz and bas_sessiz[0][0] < 0.05 else 0.0
    sondaki = sessizlikler(kaynak, ters=True)
    toplam = sure(kaynak)
    konusma_son = toplam - (sondaki[0][1] if sondaki and sondaki[0][0] < 0.05 else 0.0)
    kirp = konusma_bas - BAS_PAYI
    hedef = KOK / "public" / f"{ad}.mp3"
    girdi = ["-ss", f"{kirp:.3f}", "-i", str(kaynak)] if kirp > 0 else ["-i", str(kaynak), "-af", f"adelay={int(-kirp * 1000)}:all=1"]
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *girdi, "-c:a", "libmp3lame", "-b:a", "192k", str(hedef)], check=True)

    ara = [(a, b) for a, b in bas_sessiz if a > konusma_bas]
    parcalar, onceki = [], konusma_bas
    for a, b in ara:
        parcalar.append((onceki, a))
        onceki = b
    parcalar.append((onceki, konusma_son))
    parcalar = [(round(a - kirp, 3), round(b - kirp, 3)) for a, b in parcalar]
    duraklar = [a for a, _ in parcalar]  # konuşma parçalarının başlangıçları: cümle/öbek sınırları
    bitis = parcalar[-1][1]

    tsx = tsx_yol.read_text(encoding="utf-8")
    yazilar = yazilari_bul(tsx)
    metinler = [y["metin"] for y in yazilar] + ([son_cumle] if son_cumle else [])
    uzunluklar = [okunan_uzunluk(m) for m in metinler]
    toplam_uz = sum(uzunluklar)
    span = bitis - parcalar[0][0]
    baslar, kum = [], 0.0
    for k, u in enumerate(uzunluklar):
        tahmin = parcalar[0][0] + span * kum / toplam_uz
        kum += u
        if k == 0:
            baslar.append(parcalar[0][0])
            continue
        en_yakin = min(duraklar, key=lambda d: abs(d - tahmin))
        secim = en_yakin if abs(en_yakin - tahmin) < 0.55 else tahmin
        secim = max(secim, baslar[-1] + EN_KISA)  # sıra bozulmasın
        baslar.append(round(secim, 2))
    baslar.append(round(bitis + 0.5, 2))  # son yazının bitişi: konuşma bittikten 0,5 sn sonra

    # süreleri yaz: aynı sahnedeki sonraki yazı tam o anda, sonraki sahnenin ilk yazısı 0,8 sn boşlukla başlar
    yeni = tsx
    for k in reversed(range(len(yazilar))):
        y = yazilar[k]
        sonraki_sahne = yazilar[k + 1]["sahne"] if k + 1 < len(yazilar) else None
        fark = baslar[k + 1] - baslar[k]
        if sonraki_sahne is not None and sonraki_sahne != y["sahne"]:
            fark -= SAHNE_ARASI
        if k + 1 == len(yazilar) and son_cumle:  # son yazıdan sonra kapanış cümlesi: sahne geçişi payı düşülür
            fark -= SAHNE_ARASI
        fark = max(EN_KISA, round(fark, 2))
        yeni = yeni[:y["sure_bas"]] + f"{fark:.2f}" + yeni[y["sure_son"]:]
    tsx_yol.write_text(yeni, encoding="utf-8")

    print(f"kaydırma: {-kirp:+.2f} sn, konuşma: {parcalar[0][0]}-{bitis} sn, {len(parcalar)} parça, {len(yazilar)} yazı")
    for k, m in enumerate(metinler):
        print(f"{baslar[k]:6.2f}  {m}")


if __name__ == "__main__":
    main()
