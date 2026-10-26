"""Seslendirmeyi videoya bire bir bağlar.

1. Baştaki sessizliği kırpar (konuşma 0,3. sn'de başlar) ve public/anlatim.mp3 olarak kaydeder.
2. Sessizlikleri ölçer; konuşma parçalarını metnin cümleleriyle eşleştirir (bir cümle bir ya da
   birkaç parçadan oluşabilir; virgül duraklamaları böyle birleşir). Eşleştirme, her cümlenin
   süresinin harf sayısıyla orantılı olması beklentisinden en az sapan bölmeyi seçer.
3. Sahne, ekran yazısı, başlık, ok ve kapanış zamanlarını paragraflara göre hesaplar ve
   src/sahneler/CengizHanZaman.ts dosyasına yazar.

Kullanım: python3 -I video/ses/hizala.py <ses dosyası>
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]

PARAGRAFLAR = [
    ["Elinde bir pıhtı kanla doğduğu söylenir.", "Mezarı ise hâlâ bulunamadı."],
    ["Yaklaşık 1162.", "Moğol bozkırında bir çocuk doğdu.", "Adı Temüçin'di."],
    ["Daha çocukken babasını kaybetti.", "Kabilesi ailesini yüzüstü bıraktı.",
     "Annesi Hö'elün, çocuklarını bozkırın en zor günlerinde ayakta tuttu."],
    ["Temüçin her yenilgiden bir ders çıkardı.", "Eşi Börte kaçırılınca müttefikleriyle birlikte onu geri aldı.",
     "Bu olay, yükselişinin dönüm noktası sayılır."],
    ["1206'da boylar bir araya geldi ve ona “Cengiz Han” dediler.",
     "Terfiyi soya değil yeteneğe bağladı, yazıyı benimsedi, Yam adlı ulak ağını kurdu."],
    ["Sonra orduları Çin'den Orta Asya'ya yürüdü.", "Şehirler düştü.", "Bu yürüyüş geride çok ağır bir bedel de bıraktı.",
     "Hikâyenin o yüzünü unutmamak gerek."],
    ["1227'de seferdeyken öldü.", "Mezarı hâlâ bilinmiyor.",
     "Bozkırın çocuğunun attığı temel, ardıllarının döneminde tarihin en büyük bitişik kara imparatorluğuna dönüştü."],
    ["Kahraman mı, yıkıcı mı?", "Belki de ikisinin gölgesinde geçen bir hayat."],
]
BAS_PAYI = 0.3  # konuşma videonun bu saniyesinde başlar
KAPANIS = 4.0  # son cümleden sonra "Timur mu, Attila mı?" için kalan süre


def okunan_uzunluk(cumle: str) -> float:
    """Okuma süresi tahmini: harf sayısı, rakamlar okunurken uzar (1162 -> 'bin yüz altmış iki')."""
    harf = len(re.sub(r"[^\wçğıöşüâÇĞİÖŞÜÂ]", "", cumle))
    return harf + sum(len(r) * 4 for r in re.findall(r"\d+", cumle))


def sessizlikler(ses: Path, ters=False) -> list[tuple[float, float]]:
    af = ("areverse," if ters else "") + "silencedetect=noise=-35dB:d=0.25"
    cikti = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(ses), "-af", af, "-f", "null", "-"],
                           capture_output=True, text=True).stderr
    bas = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", cikti)]
    son = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", cikti)]
    return list(zip(bas, son))


def sure(ses: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ses)],
                                capture_output=True, text=True).stdout)


def esle(parcalar, cumleler):
    """Parçaları sırayla cümlelere böler (her cümle >=1 parça); toplam sapmayı en aza indirir."""
    n, m = len(parcalar), len(cumleler)
    toplam_sure = sum(b - a for a, b in parcalar)
    hiz = toplam_sure / sum(okunan_uzunluk(c) for c in cumleler)
    INF = float("inf")
    en = [[INF] * (n + 1) for _ in range(m + 1)]
    geri = [[0] * (n + 1) for _ in range(m + 1)]
    en[0][0] = 0
    for j in range(1, m + 1):
        beklenen = okunan_uzunluk(cumleler[j - 1]) * hiz
        for i in range(j, n - (m - j) + 1):
            for k in range(j - 1, i):
                if en[j - 1][k] == INF:
                    continue
                gercek = parcalar[i - 1][1] - parcalar[k][0]
                maliyet = en[j - 1][k] + ((gercek - beklenen) / beklenen) ** 2
                if maliyet < en[j][i]:
                    en[j][i], geri[j][i] = maliyet, k
    sinirlar, i = [], n
    for j in range(m, 0, -1):
        k = geri[j][i]
        sinirlar.append((parcalar[k][0], parcalar[i - 1][1]))
        i = k
    return sinirlar[::-1]


def main():
    kaynak = Path(sys.argv[1])
    bas_sessiz = sessizlikler(kaynak)
    konusma_bas = bas_sessiz[0][1] if bas_sessiz and bas_sessiz[0][0] < 0.05 else 0.0
    sondaki = sessizlikler(kaynak, ters=True)
    toplam = sure(kaynak)
    konusma_son = toplam - (sondaki[0][1] if sondaki and sondaki[0][0] < 0.05 else 0.0)
    # Konuşma tam BAS_PAYI saniyesinde başlasın: baştaki fazla sessizlik kırpılır, eksikse başa sessizlik eklenir
    kirp = konusma_bas - BAS_PAYI
    hedef = KOK / "public" / "anlatim.mp3"
    girdi = ["-ss", f"{kirp:.3f}", "-i", str(kaynak)] if kirp > 0 else ["-i", str(kaynak), "-af", f"adelay={int(-kirp * 1000)}:all=1"]
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *girdi, "-c:a", "libmp3lame", "-b:a", "192k", str(hedef)],
                   check=True)

    ara = [(a, b) for a, b in bas_sessiz if a > konusma_bas]
    parcalar, onceki = [], konusma_bas
    for a, b in ara:
        parcalar.append((onceki, a))
        onceki = b
    parcalar.append((onceki, konusma_son))
    parcalar = [(round(a - kirp, 3), round(b - kirp, 3)) for a, b in parcalar]

    cumleler = [c for p in PARAGRAFLAR for c in p]
    sinir = esle(parcalar, cumleler)
    anlatim, i = [], 0
    paragraf_zaman = []
    for p in PARAGRAFLAR:
        ilk = i
        for c in p:
            anlatim.append({"t": c, "bas": sinir[i][0], "bit": sinir[i][1]})
            i += 1
        paragraf_zaman.append((sinir[ilk][0], sinir[i - 1][1]))

    def cumle(metin):
        return next(a for a in anlatim if a["t"].startswith(metin))

    son_konusma = paragraf_zaman[-1][1]
    toplam_sn = round(son_konusma + KAPANIS, 2)
    sahne = []
    for k, (a, _) in enumerate(paragraf_zaman):
        bas = 0.0 if k == 0 else round(a - 0.25, 2)
        sahne.append([bas, None])
    for k in range(len(sahne)):
        sahne[k][1] = sahne[k + 1][0] if k + 1 < len(sahne) else toplam_sn
    ekran = [
        {"bas": round(sahne[1][0] + 0.8, 2), "bit": sahne[1][1], "satirlar": ["Yaklaşık 1162.", "Bozkırda bir çocuk doğdu."]},
        {"bas": round(sahne[2][0] + 0.85, 2), "bit": sahne[2][1], "satirlar": ["Babasız,", "kabilesiz büyüdü."]},
        {"bas": round(cumle("1206")["bas"] + 0.3, 2), "bit": sahne[4][1], "satirlar": ["1206:", "“Cengiz Han” dediler."]},
        {"bas": round(cumle("Şehirler düştü")["bas"], 2), "bit": sahne[5][1], "satirlar": ["Şehirler düştü.", "Bedeli ağır oldu."]},
        {"bas": round(cumle("1227")["bas"], 2), "bit": round(cumle("Mezarı hâlâ bilinmiyor")["bit"] + 0.4, 2),
         "satirlar": ["1227'de öldü.", "Mezarı hâlâ bilinmiyor."]},
    ]
    zaman = {
        "TOPLAM_SN": toplam_sn,
        "SAHNE_ZAMANLARI": sahne,
        "EKRAN_METNI_ZAMANLARI": ekran,
        "ANLATIM": anlatim,
        "BASLIK_BAS": round(sahne[0][1] - 1.65, 2),
        "OK_BAS": round(sahne[3][0] + 0.95, 2),
        "CTA_BAS": round(son_konusma + 0.3, 2),
    }
    ts = ["/* Bu dosyayı video/ses/hizala.py üretir: seslendirmenin ölçülen zamanları (saniye). Elle düzenlemeyin. */"]
    for ad, deger in zaman.items():
        ts.append(f"export const {ad} = {json.dumps(deger, ensure_ascii=False)} as const;")
    (KOK / "src" / "sahneler" / "CengizHanZaman.ts").write_text("\n".join(ts) + "\n", encoding="utf-8")
    print(f"kaydırma: {-kirp:+.2f} sn, toplam video: {toplam_sn} sn, konuşma: {parcalar[0][0]}-{son_konusma} sn")
    for a in anlatim:
        print(f"{a['bas']:6.2f}-{a['bit']:6.2f}  {a['t']}")
    print("sahneler:", sahne)


if __name__ == "__main__":
    main()
