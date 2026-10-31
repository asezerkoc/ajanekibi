"""Ekran yazıları tam transkript DEĞİLSE (vurgu yazıları) seslendirmeye hizalama.

hizala_seri.py yazı metinlerinin uzunluğuna göre zaman tahmin eder; yazılar anlatımın yalnızca bir kısmıysa (ör. Kalender:
33 vurgu yazısı, 354 kelimelik anlatım) tahmin kayar. Bu araç her yazıyı anlatım metnindeki bir "çapa" cümleye bağlar:
yazının başlangıcı = çapanın anlatımdaki karakter konumunun orana göre zamanı, en yakın duraklamaya oturtulur.

Kullanım: python3 -I video/ses/hizala_ankor.py <public/ses.mp3> <Sahne.tsx> <anlatim.txt> <ankorlar.txt> [--son "kapanış cümlesi"]
ankorlar.txt: her satır bir yazı için anlatımdaki çapa metin (yazı sırasıyla; satır sayısı = yazı sayısı [+1 kapanış]).
Ses dosyası hizala_seri ile kırpılmış hâl olmalı (konuşma 0,3 sn'de başlar).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hizala_seri import EN_KISA, SAHNE_ARASI, okunan_uzunluk, sessizlikler, sure, yazilari_bul  # noqa: E402


def main():
    args = sys.argv[1:]
    son_cumle = None
    if "--son" in args:
        i = args.index("--son")
        son_cumle = args[i + 1]
        del args[i:i + 2]
    ses, tsx_yol, anlatim_yol, ankor_yol = Path(args[0]), Path(args[1]), Path(args[2]), Path(args[3])
    anlatim = anlatim_yol.read_text(encoding="utf-8")
    ankorlar = [a.strip() for a in ankor_yol.read_text(encoding="utf-8").splitlines() if a.strip()]

    bas_sessiz = sessizlikler(ses)
    konusma_bas = bas_sessiz[0][1] if bas_sessiz and bas_sessiz[0][0] < 0.05 else 0.0
    sondaki = sessizlikler(ses, ters=True)
    toplam = sure(ses)
    konusma_son = toplam - (sondaki[0][1] if sondaki and sondaki[0][0] < 0.05 else 0.0)
    duraklar = [b for a, b in bas_sessiz if a > konusma_bas]  # her duraklamanın bitişi: yeni cümlenin başı
    bitis = konusma_son

    tsx = tsx_yol.read_text(encoding="utf-8")
    yazilar = yazilari_bul(tsx)
    beklenen = len(yazilar) + (1 if son_cumle else 0)
    if len(ankorlar) != beklenen:
        raise SystemExit(f"çapa sayısı {len(ankorlar)}, yazı sayısı {beklenen} (yazılar {len(yazilar)}{' + kapanış' if son_cumle else ''})")

    # anlatımdaki konum: okunan uzunluk oranı
    toplam_uz = okunan_uzunluk(anlatim)
    konumlar = []
    arama = 0
    for a in ankorlar:
        k = anlatim.find(a, arama)
        if k < 0:
            raise SystemExit(f"çapa anlatımda yok: {a!r}")
        konumlar.append(okunan_uzunluk(anlatim[:k]) / toplam_uz)
        arama = k + 1
    span = bitis - konusma_bas
    baslar = []
    for i, oran in enumerate(konumlar):
        tahmin = konusma_bas + span * oran
        if i == 0:
            baslar.append(konusma_bas)
            continue
        en_yakin = min(duraklar, key=lambda d: abs(d - tahmin)) if duraklar else tahmin
        secim = en_yakin if abs(en_yakin - tahmin) < 1.2 else tahmin
        secim = max(secim, baslar[-1] + EN_KISA)
        baslar.append(round(secim, 2))
    baslar.append(round(bitis + 0.5, 2))

    yeni = tsx
    for k in reversed(range(len(yazilar))):
        y = yazilar[k]
        sonraki_sahne = yazilar[k + 1]["sahne"] if k + 1 < len(yazilar) else None
        fark = baslar[k + 1] - baslar[k]
        if sonraki_sahne is not None and sonraki_sahne != y["sahne"]:
            fark -= SAHNE_ARASI
        if k + 1 == len(yazilar) and son_cumle:
            fark -= SAHNE_ARASI
        fark = max(EN_KISA, round(fark, 2))
        yeni = yeni[:y["sure_bas"]] + f"{fark:.2f}" + yeni[y["sure_son"]:]
    tsx_yol.write_text(yeni, encoding="utf-8")
    print(f"konuşma: {konusma_bas}-{bitis:.2f} sn, {len(duraklar)} durak, {len(yazilar)} yazı")
    for k, a in enumerate(ankorlar):
        print(f"{baslar[k]:7.2f}  {yazilar[k]['metin'] if k < len(yazilar) else '(kapanış)'}   ← {a[:40]}")


if __name__ == "__main__":
    main()
