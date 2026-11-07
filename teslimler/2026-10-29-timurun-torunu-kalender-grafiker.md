# Timur'un Soyundan Kalender · 🟢 Grafiker sahne tarifleri

- **Tarih:** 2026-10-29 18:18
- **Durum:** ÇİZİM BEKLİYOR

# Timur'un Soyundan Kalender: tasarım teslimi (Sahne 72–89)

**Seri adı:** `kalender` · **Dosyalar:** `video/piksel/kalender.py`, `video/src/sahneler/Kalender.tsx`
**Format:** 1080×1920, 60 fps, 540×960 ızgara ×2, Jersey 10 yazı.
**Süre:** 179 sn (ses ~178 sn), 18 sahne.

> **Süre notu.** SKILL.md Reels için 90 sn sınırı koyuyor. Bu işte 3 dakika açıkça istendiği için işteki süreye uydum. Seslendirmeye göre `video/ses/hizala_seri.py` sürelerini düzeltir.

> **Kapak.** Ajans sahibi kapak vermedi, bu yüzden TSX'te `kapak` alanı yok.

> **Ara yazılar.** Ekran metni tablosundakilere ek olarak bazı sahnelere onaylı seslendirme metninden alıntı ara yazılar koydum. Sahne 72, 74, 76 ve 80 bunlardan bazılarını taşıyor. İstemezseniz silinir, sahne süresi bozulmaz.

---

## 1) Sahne planı

| No | Zaman | Sn | Bölüm | Konu | Mekân |
|---|---|---|---|---|---|
| 72 | 0:00–0:10 | 10 | Kanca | Tahtta Kalender; solda kılıçlı muhafız, sağda yazan kâtip | iç mekân, kandil + mum |
| 73 | 0:10–0:20 | 10 | Herat | Herat silüeti; Timur (ata) ve tahtta oğlu Şahruh | dış, altın saat |
| 74 | 0:20–0:28 | 8 | Herat | Baysungur'un sanat akademisi; hattat, nakkaş, müzehhip; çocuk Bâbür | iç mekân, kandil |
| 75 | 0:28–0:34 | 6 | Herat | Baysungur'un cenazesi; önde genç Bâbür | dış, alacakaranlık |
| 76 | 0:34–0:40 | 6 | Kalender | Saray avlusunda asalı derviş şehzade yürür, saray ehli bakar | dış, gündüz |
| 77 | 0:40–0:50 | 10 | Kalender | Kalender yazar, Câmî risale uzatır | iç mekân, gece penceresi |
| 78 | 0:50–0:59 | 9 | Kalender | Kapıda yoksula sadaka (rivayet) | dış, öğleden sonra |
| 79 | 0:59–1:05 | 6 | Dönüş | Şahruh'un cenazesi; arkada birbirine düşen torunlar | dış, bulutlu gün |
| 80 | 1:05–1:12 | 7 | Dönüş | Ordu, Herat kapısı, atlı Kalender elinde kılıç | dış, parlak gün |
| 81 | 1:12–1:19 | 7 | Gazele giriş | Kadehle ve kalemle şiir yazan hükümdar | iç mekân, mum |
| 82 | 1:19–1:27 | 8 | Gazel b.1 | Gece gökyüzü, ay parçası, taş yığını | dış, gece |
| 83 | 1:27–1:36 | 9 | Gazel b.2 | Gün batımında gül | dış, kızıl gün batımı |
| 84 | 1:36–1:46 | 10 | Gazel b.3 | Nevruz bahar bahçesi: kadeh, gül, dilberler | dış, gündüz |
| 85 | 1:46–1:54 | 8 | Gazel b.4 | Kadeh: Kalender ve saki | iç mekân, mum |
| 86 | 1:54–2:00 | 6 | Gazel b.5 | Gece, ince ay, mangaldan yükselen "gönül dumanı", halk | dış, gece |
| 87 | 2:00–2:06 | 6 | Gazel b.6 | Mecnun çölde yürür, ufukta Leyla'nın ışıklı çadırı | dış, akşam çöl |
| 88 | 2:06–2:20 | 14 | Çözümleme | Kılıçlı gölge siluet ve yazan Kalender | iç mekân, mum |
| 85† | 2:20–2:31 | 11 | Çözümleme | Kadeh sorusu (Sahne 85 yeniden kullanılır, yakın çekim) | iç mekân |
| 87† | 2:31–2:40 | 9 | Çözümleme | Leyla kim? (Sahne 87 yeniden kullanılır) | çöl |
| 89 | 2:40–2:50 + kapanış 9 sn | 19 | Kapanış | Alacakaranlıkta derviş silüeti uzaklaşır; soru | dış, alacakaranlık |

† Aynı sahne numarası ikinci kez `Bolum` olur. Motor bunu desteklemezse 88'in ardına iki ek sahne açılır (90 = kadeh yakın çekim, 91 = Leyla çölü kopyası). Bu durumda sahne sayısı 20 olur, bu yüzden önce bu yolu denemenizi öneririm.

**Ortak kurallar (her sahne için geçerli):**
- Sprite tabanı iç mekânda 634, dışta 630–634. Orta plan figürleri `duz(588)` ile `duz(596)` arasına oturur.
- İnsan ölçeği `s=2.4–2.6`, at `s=2.9`. İnsan boyu at boyunun yaklaşık %65–70'idir.
- Orta plandaki figürler `s≈1.1` ve daha yüksek zeminde durur, yani arkadadır.
- İç mekânların hepsinde kandil ve/veya mumluk ışığı var.
- Yazı bandı y 95–245'tir. Bulutlar ve dağ tepeleri y ≥ 330'da.

### Sahne sahne plan

**Sahne 72: Kanca (10 sn).** Sarayın iç mekânı. Ortada alçak taht (sedir, altın ve kızıl örtü) üzerinde sade yeşil-gri kaftanlı, sarıklı Kalender oturur ve elinde kalem vardır. Solunda miğferli, kılıçlı muhafız, sağında oturan kâtip yazı yazar. Yani "bir elinde kılıç, öbüründe şiir" iki yandaki figürlerle anlatılır.
- Zemin: sprite tabanı 634 (`z`). Taht tabanı `z`'de, Kalender tahtın üst yüzünde (`duz(ust, 540)`).
- Ölçek: hepsi `s≈2.4–2.6`, taht `s=3.4`.
- Hareket: kandil ve mum titrer (fps 8).
- Kamera: `yakin 2.0`, `kamera 10`.
- Ses: mum çıtırtısı, uzaktan ney.

**Sahne 73: Herat, Timur ve Şahruh (10 sn).** Altın saat. Arkada Herat (`orta_asya_sehri`) ve türbe/medrese (`gur_i_emir`). Önde soy tablosu: solda tuğ yanında yaşlı Timur kılıçla, sağda alçak tahtta Şahruh (`sorguc`).
- Zemin: sprite tabanı 632; arka yapılar `duz(588)`.
- Ölçek: Timur ve Şahruh `s=2.6/2.4`.
- Hareket: tuğ flamaları dalgalanır, Timur'un kolu hafif oynar.
- Kamera: `yakin 1.9`, `kamera 20`.
- Ses: rüzgâr, bozkır davulu uzaktan.

**Sahne 74: Akademi (8 sn).** İç mekân, kitap ve mürekkep dünyası. Üç usta yere oturup yazar: hattat, nakkaş, müzehhip. Sağda Baysungur (`sorguc`) ayakta onaylar, yanında çocuk Bâbür (`s=1.8`).
- Zemin: tabanı 634.
- Hareket: iki kandil ve mum titrer, Baysungur'un kolu hafif oynar.
- Kamera: `yakin 1.8`, `kamera 10`.
- Ses: kalem hışırtısı, sayfa sesi, hafif ney.

**Sahne 75: Baysungur'un cenazesi (6 sn).** Alacakaranlık. Dört taşıyıcı omuzda abanoz tabutu sağa yürütür. Önde başı eğik çocuk Bâbür (`s=1.8`). Arkada yas tutanlar ve şehir silüeti.
- Zemin: sprite tabanı 634; yas tutanlar `duz(588)`.
- Hareket: taşıyıcılar yavaş adım atar, ağırlık nedeniyle sırayla.
- Kamera: `yakin 2.0`, `kamera 20`.
- Ses: ağır adım sesleri, ezan sessizliği.

**Sahne 76: Saray avlusu (6 sn).** Gündüz. Sade kaftanlı, sarıklı, asalı Kalender sağa yürür. Orta planda renkli kaftanlı saray ehli şaşkınlıkla bakar. Arkada kerpiç sur ve mavi kubbe, çınar ağacı.
- Zemin: sprite tabanı 630; orta plan figürleri `duz(596)`, yapılar `duz(588)`.
- Hareket: Kalender yürür (`adim=f`), sprite 70 px kayar.
- Kamera: `yakin 2.2`, `kamera 30`.
- Ses: avlu uğultusu, kuş sesi.

**Sahne 77: Câmî ve Kalender (10 sn).** Gece penceresi. Solda oturan Kalender yazar, sağda beyaz sakallı Câmî ayakta risale (rulo) uzatır. Ortada mumluk, tavanda kandil.
- Zemin: tabanı 634; ikisi de `z`'de.
- Hareket: Câmî'nin kolu yavaşça uzanır ve geri çekilir.
- Kamera: `yakin 2.1`, `kamera 10`.
- Ses: sakin fon, mum.

**Sahne 78: Sadaka (9 sn, rivayet).** Öğleden sonra. Arkada taş sur ve kapı, dibinde bekleyen yoksullar. Önde sağda Kalender, solda yamalı kaftanlı yoksul ve kadın, ellerini açmış. `f` 0.35–0.75 arasında bir altın sikke Kalender'in elinden yoksulun eline geçer.
- Zemin: tabanı 632; sur `duz(588)`, bekleyen kalabalık `duz(596)`.
- Hareket: Kalender'in kolu uzanıp iner.
- Kamera: `yakin 2.0`, `kamera 20`.
- Ses: kapı gıcırtısı, madeni para sesi.

**Sahne 79: Şahruh'un cenazesi (6 sn).** Bulutlu gün. Taşıyıcılar abanoz tabutu sola taşır. Arka planda iki küçük atlı grup (zırhlı, mızraklı) karşılıklı yüzleşir, yani torunlar birbirine düşer. Arkada şehir, yas tutanlar.
- Zemin: sprite tabanı 634; arka atlılar `duz(584)`, kalabalık ve şehir `duz(588)`.
- Hareket: taşıyıcılar yavaş yürür; arka atlılar tuğla flamalarıyla dururlar.
- Kamera: `yakin 2.0`, `kamera 20`.
- Ses: matem davulu, rüzgâr.

**Sahne 80: Ordu ve Herat kapısı (7 sn).** Parlak gün. Önde atlı Kalender kılıcı kaldırmış (`kol=0.6`) sağa, Herat'a yürür. Arkasında iki atlı. Orta planda ordu ve tuğ, sağda Herat surları ve kapısı.
- Zemin: sprite tabanı 632; ordu `duz(596)`, tuğ `duz(592)`, şehir `duz(588)`.
- Ölçek: at `s=2.9`, binici insan boyu %65–70.
- Hareket: atlar yürür (fazlar kaydırılmış).
- Kamera: `yakin 2.0`, `kamera 40`.
- Ses: nal sesleri, boru.

**Sahne 81: Gazele giriş (7 sn).** İç mekân. Oturan Kalender kalemle yazar, ara ara kadehi kaldırır (`el` kalem ↔ kase). Etrafta iki mumluk, tavanda kandil.
- Zemin: tabanı 634.
- Hareket: kalem ve kadeh evreleri değişir.
- Kamera: `yakin 2.3`, `kamera 10`.
- Ses: mum, çok hafif ney.

**Sahne 82: Beyit 1, gece ve ay (8 sn).** Dolunay, yıldızlı gök. Kalender ayağa kalkıp aya bakar. Yanında koca bir taş yığını ("taş parçasından geri kalır yanın yok").
- Zemin: sprite tabanı 630; taşlar `duz(588)`.
- Hareket: yıldızlar ve çimen sakin.
- Kamera: `yakin 2.1`, `kamera 20`.
- Ses: gece rüzgârı, cırcırböcek.

**Sahne 83: Beyit 2, gül (9 sn).** Kızıl gün batımı. Büyük bir gül (`cicek`, kızıl taç, sarı orta) ve iki küçük gül rüzgârda salınır. Bir gül yaprağı yavaşça düşer.
- Zemin: tabanı 630; güller `z`'de.
- Hareket: güller sallanır, yaprak yerçekimiyle aşağı iner.
- Kamera: `yakin 2.4`, `kamera 20`.
- Ses: rüzgâr, uzaktan bülbül.

**Sahne 84: Beyit 3, bahar bahçesi (10 sn).** Pastel gündüz, çiçekli pembe ağaç, ağaç altında kadehle oturan Kalender, yanında iki dilber (kadın figür), gül. Ağaçtan yapraklar düşer.
- Zemin: tabanı 630; orta plandaki ağaçlar `duz(590)`.
- Hareket: ağaç sallanır, yapraklar düşer.
- Kamera: `yakin 1.9`, `kamera 25`.
- Ses: kuş, su, bahar rüzgârı.

**Sahne 85: Beyit 4, kadeh (8 sn).** İç mekân. Solda oturan Kalender kadeh tutar, sağda saki testiyle doldurur. Arada mumluk, tavanda kandil.
- Zemin: tabanı 634.
- Hareket: saki'nin kolu eğilir.
- Kamera: `yakin 2.2`, `kamera 10`.
- Ses: mum, su dökme.

**Sahne 86: Beyit 5, gönül dumanı (6 sn).** Gece, ince ay. Ortada mangal, duman yukarı yükselir. Etrafında iki dervişle halk (orta planda).
- Zemin: sprite tabanı 630; halk `duz(596)`.
- Hareket: duman yukarı kıvrılır, korlar kızarır.
- Kamera: `yakin 2.2`, `kamera 15`.
- Ses: ateş çıtırtısı, gece.

**Sahne 87: Beyit 6, Mecnun çölde (6 sn).** Akşam çölü. Yırtık kaftanlı Mecnun sağa, ufuktaki Leyla'nın ışıklı çadırına doğru yavaşça yürür. Çadırdan duman yükselir.
- Zemin: sprite tabanı 630; çadır `duz(588)`.
- Hareket: yürüyüş, sprite 70 px kayar.
- Kamera: `yakin 2.0`, `kamera 30`.
- Ses: çöl rüzgârı, uzaktan ney.

**Sahne 88: Çözümleme (14 sn).** İç mekân. Solda kılıç kaldırmış koyu siluet (hükümdarın öbür yüzü), sağda yazan ve kadehi kaldıran Kalender. Ortada mumluk ve kandil.
- Zemin: tabanı 634.
- Hareket: Kalender'in el evreleri değişir, mum titrer.
- Kamera: `yakin 2.0`, `kamera 10`.
- Ses: derin sessizlik, hafif tını.

**Sahne 89: Kapanış (10 sn + 9 sn kapanış).** Alacakaranlık. Önde asalı derviş silüeti sola, uzaktaki şehre doğru yürür. Orta planda silik Herat ve mavi türbe. Kapanışta `arka` olarak bu sahne durur.
- Zemin: sprite tabanı 632; arka yapılar `duz(588)`.
- Hareket: yürüyüş, sprite 45 px kayar.
- Kamera: `yakin 2.3`, `kamera 30`.
- Ses: rüzgâr, ney.

---

## 2) Python tarifi: `video/piksel/kalender.py`

```python
"""Timur'un Soyundan Kalender — sahneler 72-89."""
import math
from ciz import (figur, piksel, duman, tug, agac, taslar, cicek, cicekler, yurt,
                 orta_asya_sehri)
from timur_figur import (kisi, timur, oturan, sedir, atli, anadolu_kalesi, gur_i_emir)
from timur import (ic_mekan, mumluk, mangal, kandil, abanoz_tabut, kalabalik)
from sahneler import gokyuzu, uzak, orta, on, sprite, duz, KARE, PAY


# ---------------------------------------------------------------- 72
def sahne72():
    """Kanca: tahtta Kalender; solda kılıçlı muhafız, sağda yazan kâtip. İç mekân, kandil + mum."""
    ic_mekan(72, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a",
             pencere=("#1a2a4a", "#f8e0a0"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 270, 0, f, 64)
        mumluk(t, 150, z, f, 3)
        mumluk(t, 395, z, (f + 0.3) % 1, 3)
        ust = figur(t, sedir, 270, z, 3.4, renk="#c8a040", ortu="#8a1e22")     # taht: sedir (tabanı z)
        figur(t, oturan, 270, duz(ust, 540), 2.6, govde="#6a7a5a", bas="sarik",
              bas_renk="#e8e0cc", sakal="#2a1a12", el="kalem", minder="#8a2a2a")
        figur(t, kisi, 175, z, 2.6, govde="#7a1e22", bas="migfer", bas_renk="#9aa2ac",
              yon=1, silah="kilic", kol=0.15)                                   # kılıç tarafı
        figur(t, oturan, 370, z, 2.4, govde="#3a5a8a", bas="bork", bas_renk="#5a3a22",
              sakal="#2a1a12", yon=-1, el="kalem", minder="#6a3a2a")            # şiir tarafı

    sprite(72, "karakter", 540, 200, KARE, kare)


# ---------------------------------------------------------------- 73
def sahne73():
    """Herat: Timur (ata) ve tahtta oğlu Şahruh; arkada Herat silüeti ve türbe. Altın saat."""
    gokyuzu(73, ["#5a5a98", "#8a78a8", "#d09aa0", "#f0b890", "#f8d8a0", "#fce8b8"],
            (420, 360, 30, ["#fff4d0", "#ffd890"]), [(130, 340, 24), (300, 370, 18)],
            ("#fff4e0", "#f4dcc8", "#d8a8a0"))
    uzak(73, ["#7a6a98", "#8a7aa0"], ["#9a82a0", "#a88aa0"], ["#c89a98", "#b88a90", "#a87a84"],
         dag_y=(350, 425))
    orta(73, (524, 558), ["#a8885a", "#987a50", "#887048", "#78603e", "#685036"], "#d8b878",
         ekle=lambda img, z: [
             figur(img, orta_asya_sehri, PAY + 10, PAY + 330, duz(588), 2.2, tohum=73),
             figur(img, gur_i_emir, PAY + 430, duz(588), 1.5)])
    on(73, ["#685036", "#887048", "#78603e"], "#d8b878")

    def kare(t, z, i):
        f = i / KARE
        figur(t, tug, 105, z, 1.4, f)                                              # flamalar dalgalanır
        figur(t, timur, 190, z, 2.6, 1, silah="kilic",
              kol=0.25 + 0.1 * math.sin(f * 2 * math.pi), yasli=True)
        ust = figur(t, sedir, 360, z, 3.0, renk="#8a6a3a", ortu="#2a6a3a")
        figur(t, oturan, 360, duz(ust, 540), 2.4, govde="#2a6a3a", bas="sorguc",
              bas_renk="#e0b040", sakal="#2a1a12", yon=-1)

    sprite(73, "karakter", 540, 170, KARE, kare)


# ---------------------------------------------------------------- 74
def sahne74():
    """Baysungur'un akademisi: hattat, nakkaş, müzehhip; Baysungur ve çocuk Bâbür. İç mekân, kandil."""
    ic_mekan(74, duvar=("#4a3626", "#5a4430", "#6a5238"), kemer="#2a1a14", cini="#2a8a8a",
             pencere=("#f0c890", "#fff4d8"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 215, 0, f, 56)
        kandil(t, 335, 0, (f + 0.4) % 1, 56)
        figur(t, oturan, 150, z, 2.3, govde="#8a3a2a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", el="kalem", minder="#8a2a2a")                       # hattat
        figur(t, oturan, 220, z, 2.3, govde="#2a6a5a", bas="bork", bas_renk="#5a3a22",
              el="kalem", minder="#6a4a2a")                                         # nakkaş
        figur(t, oturan, 290, z, 2.3, govde="#6a4a8a", bas="sarik", bas_renk="#f4f0e6",
              sakal="#2a1a12", el="kalem", minder="#2a4a6a")                        # müzehhip
        figur(t, kisi, 360, z, 2.6, govde="#2a3a6a", bas="sorguc", bas_renk="#e0b040",
              sakal="#2a1a12", yon=-1, kol=0.2 + 0.1 * math.sin(f * 2 * math.pi))   # Baysungur
        figur(t, kisi, 405, z, 1.8, govde="#8a7a5a", bas="bork", bas_renk="#5a3a22",
              yon=-1)                                                               # genç Bâbür

    sprite(74, "karakter", 540, 200, KARE, kare)


# ---------------------------------------------------------------- 75
def sahne75():
    """Baysungur'un cenazesi: omuzlarda abanoz tabut, önde çocuk Bâbür. Alacakaranlık."""
    gokyuzu(75, ["#3a3a6a", "#6a5a88", "#a87a8a", "#d8908a", "#e8b090", "#f0c8a0"],
            (150, 380, 26, ["#ffe0b0", "#f0a878"]), [(380, 340, 22), (120, 320, 18)],
            ("#f0d8d0", "#d8b0b0", "#a88090"))
    uzak(75, ["#5a5a88", "#6a6a90"], ["#7a6a88", "#8a7088"], ["#8a6a78", "#7a5a6a", "#6a4a5c"],
         dag_y=(352, 430))
    orta(75, (526, 560), ["#6a5a58", "#5a4a4c", "#4a3c40", "#3c3036", "#30262c"], "#9a8078",
         ekle=lambda img, z: [
             figur(img, orta_asya_sehri, PAY + 260, PAY + 560, duz(588), 2.0, tohum=75),
             kalabalik(img, duz(596), PAY + 20, PAY + 230, 26, 75, ("#2a2430", "#3a3038"),
                       s=1.1, yon=1)])
    on(75, ["#30262c", "#4a3c40", "#3c3036"], "#9a8078")

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((180, 225, 285, 325)):                               # taşıyıcılar
            figur(t, kisi, x, z, 2.5, govde="#24202c", bas="bork", bas_renk="#2a2420",
                  yon=1, adim=(f + (j % 2) * 0.5) % 1)
        abanoz_tabut(t, 170, 335, z[0] - 58)           # omuz y'si önizlemede ayarlanır
        figur(t, kisi, 395, z, 1.8, govde="#3a3a5a", bas="bork", bas_renk="#5a3a22",
              yon=1, adim=f)                                                        # genç Bâbür

    sprite(75, "karakter", 540, 170, KARE, kare)


# ---------------------------------------------------------------- 76
def sahne76():
    """Herat sarayı avlusu: asalı derviş şehzade yürür, saray ehli bakar. Gündüz."""
    gokyuzu(76, ["#7aa0c8", "#a8c0d0", "#d8d0c0", "#f4dcb0", "#f8e4b8"],
            (110, 360, 26, ["#fff8e0", "#ffe8b0"]), [(380, 340, 24), (250, 380, 18)],
            ("#fff8ec", "#f4e4d0", "#d8c4b0"))
    uzak(76, ["#8a9ab0", "#9aa8b8"], ["#a8b4a0", "#b4bc9c"], ["#c4c090", "#b4b080", "#a4a070"],
         dag_y=(350, 425))
    orta(76, (524, 558), ["#b8a870", "#a89860", "#988850", "#887842", "#786838"], "#e0d090",
         ekle=lambda img, z: [
             figur(img, orta_asya_sehri, PAY + 10, PAY + 520, duz(588), 2.4, tohum=76),
             kalabalik(img, duz(596), PAY + 60, PAY + 420, 38, 76,
                       ("#8a2a2a", "#2a5a8a", "#2a6a3a", "#8a6a2a"), s=1.1, yon=1),
             figur(img, agac, PAY + 590, duz(592), 1.6)])
    on(76, ["#786838", "#988850", "#887842"], "#e0d090")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 150, z, 2.6, govde="#8a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=1, adim=f, silah="sopa")                         # derviş şehzade

    sprite(76, "karakter", 300, 170, KARE, kare)


# ---------------------------------------------------------------- 77
def sahne77():
    """Kalender yazar, Câmî muamma risalesini uzatır. İç mekân, gece penceresi, kandil + mum."""
    ic_mekan(77, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a",
             pencere=("#1a2a4a", "#f4f8ff"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 270, 0, f, 60)
        mumluk(t, 270, z, f, 3)
        figur(t, oturan, 185, z, 2.5, govde="#6a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=1, el="kalem", minder="#8a2a2a")                 # Kalender
        figur(t, kisi, 350, z, 2.5, govde="#2a4a6a", bas="sarik", bas_renk="#f4f0e6",
              sakal="#e8e4dc", yon=-1, silah="mektup",
              kol=0.35 + 0.2 * math.sin(f * 2 * math.pi))                           # Câmî

    sprite(77, "karakter", 540, 190, KARE, kare)


# ---------------------------------------------------------------- 78
def sahne78():
    """Kapıda sadaka (rivayet): Kalender yoksula altın verir. Öğleden sonra."""
    gokyuzu(78, ["#7aa0c8", "#a8c0d0", "#d8d0c0", "#f4dcb0", "#f8e4b8"],
            (420, 360, 26, ["#fff8e0", "#ffe8b0"]), [(140, 340, 24), (300, 380, 18)],
            ("#fff8ec", "#f4e4d0", "#d8c4b0"))
    uzak(78, ["#8a9ab0", "#9aa8b8"], ["#a8b4a0", "#b4bc9c"], ["#c4c090", "#b4b080", "#a4a070"],
         dag_y=(350, 425))
    orta(78, (524, 558), ["#b8a870", "#a89860", "#988850", "#887842", "#786838"], "#e0d090",
         ekle=lambda img, z: [
             figur(img, anadolu_kalesi, PAY + 120, PAY + 470, duz(588), 1.8),
             kalabalik(img, duz(596), PAY + 20, PAY + 130, 28, 78, ("#6a5a4a", "#5a4a3a"),
                       s=1.1, yon=1)])
    on(78, ["#786838", "#988850", "#887842"], "#e0d090")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 145, z, 2.6, govde="#6a4a4a", bas="bork", bas_renk="#4a3a2a",
              kadin=True, yon=1)                                                    # yoksul kadın
        figur(t, kisi, 195, z, 2.6, govde="#6a5a4a", bas="kalpak", bas_renk="#4a3a2a",
              sakal="#3a2a1a", yon=1, kol=0.6)                                      # yoksul
        figur(t, kisi, 330, z, 2.6, govde="#8a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=-1,
              kol=0.2 + 0.4 * (0.5 - 0.5 * math.cos(f * 2 * math.pi)))              # Kalender
        if 0.35 < f < 0.75:                                                         # altın sikke: ele
            p = (f - 0.35) / 0.4
            xk = int(320 - 90 * p)
            yk = int(z[0] - 52 - 10 * math.sin(p * math.pi))
            piksel(t, xk, yk, "#f8d860")
            piksel(t, xk, yk + 1, "#c8a030")

    sprite(78, "karakter", 540, 170, KARE, kare)


# ---------------------------------------------------------------- 79
def sahne79():
    """Şahruh'un cenazesi; arkada birbirine düşen torunlar (karşılıklı atlı gruplar). Bulutlu gün."""
    gokyuzu(79, ["#8a9ab0", "#a8b0b8", "#c8c0b8", "#e0d0b8", "#ece0c4"],
            (400, 360, 22, ["#fffbe8", "#f4e8c8"]), [(140, 340, 26), (300, 330, 20)],
            ("#f4f0ea", "#d8d4d0", "#a8a8b0"))
    uzak(79, ["#7a8498", "#8a92a4"], ["#98a09c", "#a4aaa0"], ["#b4b090", "#a4a080", "#949070"],
         dag_y=(352, 428))
    orta(79, (526, 560), ["#a09870", "#908862", "#807854", "#706a48", "#625c40"], "#c8c090",
         ekle=lambda img, z: [
             figur(img, orta_asya_sehri, PAY + 250, PAY + 520, duz(588), 2.0, tohum=79),
             kalabalik(img, duz(596), PAY + 20, PAY + 230, 26, 79, ("#2a2430", "#3a3038"),
                       s=1.1, yon=-1),
             figur(img, atli, PAY + 470, duz(584), 1.1, 1, dur=True, zirh="#9aa2ac",
                   silah="mizrak", bayrak="#8a1e22"),
             figur(img, atli, PAY + 490, duz(584), 1.1, 1, dur=True, zirh="#9aa2ac",
                   silah="mizrak", bayrak="#8a1e22"),
             figur(img, atli, PAY + 540, duz(584), 1.1, -1, dur=True, zirh="#9aa2ac",
                   silah="mizrak", bayrak="#2a5a8a"),
             figur(img, atli, PAY + 560, duz(584), 1.1, -1, dur=True, zirh="#9aa2ac",
                   silah="mizrak", bayrak="#2a5a8a")])
    on(79, ["#625c40", "#807854", "#706a48"], "#c8c090")

    def kare(t, z, i):
        f = i / KARE
        for j, x in enumerate((210, 250, 310, 350)):
            figur(t, kisi, x, z, 2.5, govde="#24202c", bas="sarik", bas_renk="#2a2420",
                  yon=-1, adim=(f + (j % 2) * 0.5) % 1)
        abanoz_tabut(t, 200, 360, z[0] - 58)

    sprite(79, "karakter", 540, 170, KARE, kare)


# ---------------------------------------------------------------- 80
def sahne80():
    """Ordu Herat kapısına: atlı Kalender elinde kılıç, arkasında iki atlı; orta planda ordu ve tuğ."""
    gokyuzu(80, ["#6a9ad0", "#98b8dc", "#c8d8e0", "#f0e4c0", "#f8ecc8"],
            (110, 360, 28, ["#fffbe8", "#fff0b8"]), [(380, 340, 26), (250, 380, 18)],
            ("#ffffff", "#f0eef0", "#c8ccd8"))
    uzak(80, ["#7a9ab8", "#8aa6c0"], ["#98b098", "#a4bc98"], ["#c4c488", "#b4b478", "#a4a468"],
         dag_y=(350, 425))
    orta(80, (524, 558), ["#b8b070", "#a8a460", "#989450", "#888442", "#787438"], "#e0dc90",
         ekle=lambda img, z: [
             figur(img, orta_asya_sehri, PAY + 250, PAY + 530, duz(588), 2.4, tohum=80),
             kalabalik(img, duz(596), PAY + 20, PAY + 220, 18, 80,
                       ("#2a2420", "#3a3030", "#5a2a2a"), s=1.1, yon=1, bas="migfer"),
             figur(img, tug, PAY + 60, duz(592), 1.2, 0.0)])
    on(80, ["#787438", "#988850", "#888442"], "#e0dc90")

    def kare(t, z, i):
        f = i / KARE
        figur(t, atli, 145, z, 2.9, 1, faz=(f + 0.71) % 1, at_renk="#5a3a22", yele="#2b1a12",
              govde="#6a2a2a", bas="migfer", bas_renk="#9aa2ac", silah="mizrak", adim=0.45,
              zirh="#9aa2ac")
        figur(t, atli, 235, z, 2.9, 1, faz=(f + 0.37) % 1, at_renk="#6b3f24", yele="#2b1a12",
              govde="#7a1e22", bas="migfer", bas_renk="#9aa2ac", silah="mizrak", adim=0.45,
              zirh="#9aa2ac")
        figur(t, atli, 330, z, 2.9, 1, faz=f, at_renk="#3a2a22", yele="#1a1210",
              govde="#8a7a5a", bas="sarik", bas_renk="#e8e0cc", sakal="#2a1a12",
              silah="kilic", kol=0.6, adim=0.45)                                    # Kalender

    sprite(80, "karakter", 540, 160, KARE, kare)


# ---------------------------------------------------------------- 81
def sahne81():
    """Gazele giriş: kadehle ve kalemle şiir yazan hükümdar. İç mekân, mum + kandil."""
    ic_mekan(81, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a",
             pencere=("#1a2a4a", "#f4f8ff"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 220, 0, f, 60)
        mumluk(t, 135, z, f, 3)
        mumluk(t, 305, z, (f + 0.3) % 1, 2)
        el = "kase" if 0.55 <= f < 0.85 else "kalem"
        figur(t, oturan, 220, z, 2.8, govde="#6a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=1, el=el, minder="#8a2a2a")

    sprite(81, "karakter", 440, 200, KARE, kare)


# ---------------------------------------------------------------- 82
def sahne82():
    """Beyit 1: gece gökyüzü, dolunay; Kalender aya bakar, yanında taş yığını."""
    gokyuzu(82, ["#0a1228", "#16204a", "#26306a", "#3a407a", "#4a4a84"],
            (390, 340, 34, ["#fff8e0", "#f4e8b8"]), [(150, 340, 20), (300, 390, 16)],
            ("#8890b8", "#6a70a0", "#4a5088"), yildiz=70)
    uzak(82, ["#1e2a52", "#26305a"], ["#2a3460", "#323c68"], ["#2a3254", "#242c4a", "#1e2640"],
         dag_y=(352, 430))
    orta(82, (526, 560), ["#3a4060", "#323852", "#2a3048", "#242a3e", "#1e2434"], "#6a7098",
         ekle=lambda img, z: [
             figur(img, taslar, PAY + 80, duz(588), 1.2),
             figur(img, taslar, PAY + 440, duz(588), 1.2)])
    on(82, ["#1e2434", "#2a3048", "#242a3e"], "#6a7098")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 130, z, 2.6, govde="#6a6a5a", bas="sarik", bas_renk="#d8d4c4",
              sakal="#2a1a12", yon=1)
        figur(t, taslar, 250, z, 2.6, cicek=False)

    sprite(82, "karakter", 380, 170, KARE, kare)


# ---------------------------------------------------------------- 83
def sahne83():
    """Beyit 2: gün batımı, büyük gül ve düşen yaprak."""
    gokyuzu(83, ["#4a2a5a", "#8a3a62", "#c85a5a", "#e88a58", "#f4b868", "#f8d890"],
            (270, 370, 30, ["#fff0c0", "#ffb868"]), [(130, 340, 22), (420, 330, 20)],
            ("#f8d0b8", "#e0a090", "#a86078"))
    uzak(83, ["#6a3a62", "#7a4268"], ["#8a4a68", "#9a5870"], ["#a8607a", "#985470", "#884a66"],
         dag_y=(352, 430))
    orta(83, (526, 560), ["#7a4a52", "#6a4048", "#5a363e", "#4a2c34", "#3c242a"], "#c08070")
    on(83, ["#3c242a", "#5a363e", "#4a2c34"], "#c08070")

    def kare(t, z, i):
        f = i / KARE
        figur(t, cicek, 70, z, 2.4, (f + 0.3) % 1, "#c8302a", "#f4d24a")
        figur(t, cicek, 150, z, 4.2, f, "#c8302a", "#f4d24a")
        figur(t, cicek, 230, z, 2.8, (f + 0.6) % 1, "#c8302a", "#f4d24a")
        ytop = z[0] - 50                                                            # yaprak aşağı düşer
        xk = int(165 + 6 * math.sin(f * 2 * math.pi))
        yk = int(ytop + f * (z[0] - ytop))
        piksel(t, xk, yk, "#c8302a")
        piksel(t, xk + 1, yk, "#e85a4a")

    sprite(83, "karakter", 300, 170, KARE, kare)


# ---------------------------------------------------------------- 84
def sahne84():
    """Beyit 3: Nevruz, bahar bahçesi; ağaç altında kadehli Kalender, dilberler, gül."""
    gokyuzu(84, ["#78b0e0", "#a0c8e8", "#c8def0", "#e8eed8", "#f8f0d0"],
            (90, 360, 26, ["#fffbe8", "#fff0b8"]), [(380, 340, 28), (210, 330, 22), (470, 380, 20)],
            ("#ffffff", "#eef0f8", "#c8d0e0"))
    uzak(84, ["#7a9ab8", "#8aa8c0"], ["#90b090", "#a0bc98"], ["#a8c878", "#98b868", "#88a858"],
         dag_y=(350, 420))
    orta(84, (524, 558), ["#7aa850", "#6a9844", "#5a8838", "#4c7830", "#406a2a"], "#b8e078",
         ekle=lambda img, z: [
             cicekler(img, z, ["#f4d24a", "#e86a8a", "#ffffff", "#8a6ae0"], 84, adet=60,
                      derinlik=26),
             figur(img, agac, PAY + 60, duz(590), 1.6,
                   yaprak=("#d8789a", "#f0a0b8", "#f8d0d8"), govde="#4a3022", tohum=84),
             figur(img, agac, PAY + 470, duz(590), 1.6,
                   yaprak=("#d8789a", "#f0a0b8", "#f8d0d8"), govde="#4a3022", tohum=85)])
    on(84, ["#406a2a", "#5a8838", "#4c7830"], "#b8e078")

    def kare(t, z, i):
        f = i / KARE
        figur(t, agac, 380, z, 1.8, yaprak=("#d8789a", "#f0a0b8", "#f8d0d8"),
              govde="#4a3022", tohum=84, sallanma=math.sin(f * 2 * math.pi))
        figur(t, kisi, 150, z, 2.5, govde="#c8508a", bas="sarik", bas_renk="#f0d0e0",
              kadin=True, yon=1)
        figur(t, kisi, 190, z, 2.5, govde="#8a5ac8", bas="sarik", bas_renk="#f0d0e0",
              kadin=True, yon=1)
        figur(t, oturan, 245, z, 2.5, govde="#6a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=1, el="kase", minder="#8a2a2a")
        figur(t, cicek, 300, z, 3.0, f, "#c8302a", "#f4d24a")
        for j in range(6):                                                          # düşen yapraklar
            y = 20 + ((f + j / 6) % 1) * (z[0] - 20)
            x = 330 + j * 12 + 5 * math.sin((f + j / 6) * 2 * math.pi)
            piksel(t, int(x), int(y), "#f8c0d0")

    sprite(84, "karakter", 540, 170, KARE, kare)


# ---------------------------------------------------------------- 85
def sahne85():
    """Beyit 4: kadeh; oturan Kalender kadeh tutar, saki testiyle doldurur. İç mekân."""
    ic_mekan(85, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a",
             pencere=("#1a2a4a", "#f4f8ff"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 225, 0, f, 56)
        mumluk(t, 225, z, f, 3)
        figur(t, oturan, 165, z, 2.6, govde="#6a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=1, el="kase", minder="#8a2a2a")
        figur(t, kisi, 285, z, 2.6, govde="#7a4a8a", bas="bork", bas_renk="#5a3a22",
              yon=-1, silah="testi", kol=0.35 + 0.3 * math.sin(f * 2 * math.pi))      # saki

    sprite(85, "karakter", 440, 190, KARE, kare)


# ---------------------------------------------------------------- 86
def sahne86():
    """Beyit 5: gece, ince ay, mangaldan yükselen gönül dumanı, halk."""
    gokyuzu(86, ["#0a1228", "#16204a", "#26306a", "#3a407a", "#4a4a84"],
            (130, 340, 14, ["#f4ecd0", "#c8c0a0"]), [(380, 350, 18)],
            ("#8890b8", "#6a70a0", "#4a5088"), yildiz=90)
    uzak(86, ["#1e2a52", "#26305a"], ["#2a3460", "#323c68"], ["#2a3254", "#242c4a", "#1e2640"],
         dag_y=(352, 430))
    orta(86, (526, 560), ["#3a4060", "#323852", "#2a3048", "#242a3e", "#1e2434"], "#6a7098",
         ekle=lambda img, z: [
             kalabalik(img, duz(596), PAY + 30, PAY + 260, 30, 86,
                       ("#2a2a40", "#3a3050", "#2a3a48"), s=1.1, yon=1)])
    on(86, ["#1e2434", "#2a3048", "#242a3e"], "#6a7098")

    def kare(t, z, i):
        f = i / KARE
        mangal(t, 200, z, f)
        duman(t, 200, z[0] - 34, 120, 86, faz=f, renk="#d9d2c4", ruzgar=0.2)
        figur(t, oturan, 130, z, 2.5, govde="#6a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=1, minder="#8a2a2a")
        figur(t, oturan, 270, z, 2.5, govde="#4a5a7a", bas="sarik", bas_renk="#d8d4c4",
              sakal="#e8e4dc", yon=-1, minder="#4a3a2a")

    sprite(86, "karakter", 400, 170, KARE, kare)


# ---------------------------------------------------------------- 87
def sahne87():
    """Beyit 6: Mecnun çölde yürür; ufukta Leyla'nın ışıklı çadırı (yurt). Akşam çölü."""
    def ekle(img, z):
        baca = figur(img, yurt, PAY + 470, duz(588), 2.2, keçe="#d8c8a8", golge="#b0986e",
                     isik=True)
        duman(img, baca[0], baca[1], 80, 87, faz=0.0)
        figur(img, taslar, PAY + 70, duz(588), 1.2)

    gokyuzu(87, ["#3a2a5a", "#7a3a6a", "#c05a5a", "#e88a58", "#f4b868", "#f8d890"],
            (400, 370, 32, ["#fff0c0", "#ffb868"]), [(130, 340, 22)],
            ("#f8d0b8", "#e0a090", "#a86078"))
    uzak(87, ["#8a5a62", "#9a6a68"], ["#aa7a6a", "#ba8a70"], ["#c89a78", "#b88a6c", "#a87a60"],
         dag_y=(352, 428))
    orta(87, (526, 560), ["#d0a870", "#c09862", "#b08856", "#a0784a", "#90683e"], "#f0c888",
         ekle=ekle)
    on(87, ["#90683e", "#b08856", "#a0784a"], "#f0c888")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 150, z, 2.6, govde="#7a6a52", bas="sarik", bas_renk="#a89878",
              sakal="#3a2a1a", yon=1, adim=f)                                       # Mecnun
        figur(t, taslar, 330, z, 1.8)

    sprite(87, "karakter", 440, 170, KARE, kare)


# ---------------------------------------------------------------- 88
def sahne88():
    """Çözümleme: kılıçlı siluet (öbür yüz) ve yazan, kadeh kaldıran Kalender. İç mekân."""
    ic_mekan(88, duvar=("#3a2a22", "#4a3628", "#5a4230"), kemer="#2a1a14", cini="#2a6a9a",
             pencere=("#1a2a4a", "#f4f8ff"), zemin_renk=("#5a4a3a", "#4a3c2e", "#3e3226"),
             isik="#f8c060", hali=True)

    def kare(t, z, i):
        f = i / KARE
        kandil(t, 260, 0, f, 60)
        mumluk(t, 260, z, f, 3)
        figur(t, kisi, 185, z, 2.6, govde="#1a1620", bas="sarik", bas_renk="#1a1620",
              sakal="#1a1620", yon=1, silah="kilic", kol=0.5, ten="#1e1824")        # gölge siluet
        el = "kalem" if f < 0.5 else "kase"
        figur(t, oturan, 330, z, 2.6, govde="#6a7a5a", bas="sarik", bas_renk="#e8e0cc",
              sakal="#2a1a12", yon=-1, el=el, minder="#8a2a2a")

    sprite(88, "karakter", 540, 200, KARE, kare)


# ---------------------------------------------------------------- 89
def sahne89():
    """Kapanış: alacakaranlık, uzaklaşan derviş silüeti, silik Herat ve mavi türbe."""
    gokyuzu(89, ["#1a1a3a", "#3a2a5a", "#7a3a6a", "#c05a62", "#e88a60", "#f4b878"],
            (270, 370, 28, ["#fff0c0", "#ffb868"]), [(110, 340, 20), (430, 330, 18)],
            ("#f0d0d0", "#d8a8b0", "#a07088"), yildiz=50)
    uzak(89, ["#3a2a52", "#4a3258"], ["#5a3a5e", "#6a4264"], ["#6a4668", "#5a3a5a", "#4a304c"],
         dag_y=(352, 430))
    orta(89, (526, 560), ["#4a3050", "#402848", "#382240", "#301c38", "#281630"], "#7a5068",
         ekle=lambda img, z: [
             figur(img, orta_asya_sehri, PAY + 300, PAY + 560, duz(588), 2.0, tohum=89,
                   kerpic="#6a4a60", golge="#4a3248", kubbe="#5a5a8a"),
             figur(img, gur_i_emir, PAY + 120, duz(588), 1.6, mavi="#3a4a7a", tugla="#6a4a60")])
    on(89, ["#281630", "#402848", "#382240"], "#7a5068")

    def kare(t, z, i):
        f = i / KARE
        figur(t, kisi, 150, z, 2.6, govde="#140e1c", bas="sarik", bas_renk="#140e1c",
              sakal="#140e1c", yon=-1, adim=f, silah="sopa", ten="#140e1c")

    sprite(89, "karakter", 300, 150, KARE, kare)


SAHNELER = {72: sahne72, 73: sahne73, 74: sahne74, 75: sahne75, 76: sahne76, 77: sahne77,
            78: sahne78, 79: sahne79, 80: sahne80, 81: sahne81, 82: sahne82, 83: sahne83,
            84: sahne84, 85: sahne85, 86: sahne86, 87: sahne87, 88: sahne88, 89: sahne89}

if __name__ == "__main__":
    import sys
    for a in sys.argv[1:]:
        SAHNELER[int(a)]()
```

---

## 3) Seri nesnesi (TSX): `video/src/sahneler/Kalender.tsx`

```ts
import { ALTIN, KIZIL, type Seri } from "./TimurSeri";

// kapak: ajans sahibi vermedi, alan boş bırakıldı.
export const Kalender: Seri = {
  etiket: "Timur'un Soyundan Kalender",
  bolumler: [
    // ---- Kanca 0:00-0:10
    { no: 72, yakin: 2.0, kamera: 10, sprite: { w: 540, h: 200, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Hükümdar mı,", "derviş mi?"], sure: 5.0, renk: ALTIN },
        { satirlar: ["Bir elinde kılıç,", "öbüründe şiir."], sure: 4.5 },
      ] },
    // ---- Herat 0:10-0:34
    { no: 73, yakin: 1.9, kamera: 20, sprite: { w: 540, h: 170, fps: 10, x: 270, taban: 632 },
      yazilar: [{ satirlar: ["Timur'un kanı,", "Baysungur'un kalemi"], sure: 9.5, renk: ALTIN }] },
    { no: 74, yakin: 1.8, kamera: 10, sprite: { w: 540, h: 200, fps: 8, x: 270, taban: 634 },
      yazilar: [{ satirlar: ["Hattatlar, nakkaşlar,", "müzehhipler."], sure: 7.5 }] },
    { no: 75, yakin: 2.0, kamera: 20, sprite: { w: 540, h: 170, fps: 12, x: [240, 300], taban: 634 },
      yazilar: [{ satirlar: ["Baysungur", "37 yaşında öldü"], sure: 5.5, renk: KIZIL }] },
    // ---- Kalender 0:34-0:59
    { no: 76, yakin: 2.2, kamera: 30, sprite: { w: 300, h: 170, fps: 16, x: [230, 300], taban: 630 },
      yazilar: [{ satirlar: ["Sarayda tuhaf", "bir şehzade beliriyor"], sure: 5.5 }] },
    { no: 77, yakin: 2.1, kamera: 10, sprite: { w: 540, h: 190, fps: 8, x: 270, taban: 634 },
      yazilar: [{ satirlar: ["Ona \"Kalender\"", "diyorlar"], sure: 9.5, renk: ALTIN }] },
    { no: 78, yakin: 2.0, kamera: 20, sprite: { w: 540, h: 170, fps: 10, x: 270, taban: 632 },
      yazilar: [{ satirlar: ["İlk kapıda", "misliyle ver"], sure: 8.5, renk: ALTIN }] },
    // ---- Dönüş 0:59-1:12
    { no: 79, yakin: 2.0, kamera: 20, sprite: { w: 540, h: 170, fps: 12, x: [300, 250], taban: 634 },
      yazilar: [{ satirlar: ["Taht boşaldı"], sure: 5.5, renk: KIZIL }] },
    { no: 80, yakin: 2.0, kamera: 40, sprite: { w: 540, h: 160, fps: 18, x: [220, 300], taban: 632 },
      yazilar: [
        { satirlar: ["Derviş ordu topluyor", "ve Herat'a giriyor"], sure: 3.0 },
        { satirlar: ["Dervişin elinde", "kılıç"], sure: 3.5, renk: KIZIL },
      ] },
    // ---- Gazele giriş 1:12-1:19
    { no: 81, yakin: 2.3, kamera: 10, sprite: { w: 440, h: 200, fps: 8, x: 270, taban: 634 },
      yazilar: [{ satirlar: ["Kılıçla yakışmayan", "iki satır…"], sure: 6.5, renk: ALTIN }] },
    // ---- Gazel 1:19-2:06 (altyazı + vurgu)
    { no: 82, yakin: 2.1, kamera: 20, sprite: { w: 380, h: 170, fps: 10, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["O ay parçası gibi güzel yüze", "âşık olmayan her gönül,", "sana gönül denmez;"], sure: 4.2 },
        { satirlar: ["çünkü taş parçasından", "geri kalır yanın yok."], sure: 3.3 },
      ] },
    { no: 83, yakin: 2.4, kamera: 20, sprite: { w: 300, h: 170, fps: 12, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["Dedim: Ey sevgili,", "senin gamının karşısında", "ne yapayım?"], sure: 3.8 },
        { satirlar: ["Dedi: Burada öldürülmekten", "başka hiçbir çare yok."], sure: 4.7, renk: KIZIL },
      ] },
    { no: 84, yakin: 1.9, kamera: 25, sprite: { w: 540, h: 170, fps: 10, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["Nevruz, ilkbahar, gül,", "kadeh ve dilberler…"], sure: 3.8 },
        { satirlar: ["Dünyaya ikinci kez gelinmediği", "için hayatı güzel yaşa."], sure: 5.7, renk: ALTIN },
      ] },
    { no: 85, yakin: 2.2, kamera: 10, sprite: { w: 440, h: 190, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Zamanımızın eski", "süvarilerinden biri meydir;"], sure: 3.2 },
        { satirlar: ["her vakit durmaksızın nefes", "isteyip kabul eden", "şey nedir?"], sure: 4.3 },
      ] },
    { no: 86, yakin: 2.2, kamera: 15, sprite: { w: 400, h: 170, fps: 10, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["İyilerin keman kaşları niçin", "siyahtır, bilir misin?"], sure: 2.6 },
        { satirlar: ["Çünkü onların gönül", "dumanının köşelerinden", "halk güç almaktadır."], sure: 2.9 },
      ] },
    { no: 87, yakin: 2.0, kamera: 30, sprite: { w: 440, h: 170, fps: 10, x: [230, 300], taban: 630 },
      yazilar: [
        { satirlar: ["Bâbür, senin ağlayıp inlemen", "sevgilinin kulağına ulaştı;"], sure: 2.6 },
        { satirlar: ["Mecnun'un bu hay içinde", "olmasından", "Leyla haberdar oldu"], sure: 2.9, renk: ALTIN },
      ] },
    // ---- Çözümleme 2:06-2:40
    { no: 88, yakin: 2.0, kamera: 10, sprite: { w: 540, h: 200, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bu satırları elinde kılıç", "tutan hükümdar yazdı."], sure: 4.5 },
        { satirlar: ["Burada öldürülmekten", "başka hiçbir çare yok"], sure: 4.5, renk: KIZIL },
        { satirlar: ["Dünyaya ikinci kez", "gelinmediği için", "hayatı güzel yaşa"], sure: 4.5, renk: ALTIN },
      ] },
    // Sahne 85'in yeniden kullanımı, yakın çekim (yakin 2.8)
    { no: 85, yakin: 2.8, kamera: 10, odakY: 560, sprite: { w: 440, h: 190, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kadeh:", "şarap mı, hakikat mi?"], sure: 5.5, renk: ALTIN },
        { satirlar: ["Şeriat kadeh,", "hakikat içindeki içki"], sure: 5.0 },
      ] },
    // Sahne 87'nin yeniden kullanımı
    { no: 87, yakin: 2.0, kamera: 30, sprite: { w: 440, h: 170, fps: 10, x: [230, 300], taban: 630 },
      yazilar: [{ satirlar: ["Leyla kim?", "İnsan mı, Hak mı?"], sure: 8.5, renk: ALTIN }] },
    // ---- Kapanış 2:40-2:59
    { no: 89, yakin: 2.3, kamera: 30, sprite: { w: 300, h: 150, fps: 12, x: [280, 235], taban: 632 },
      yazilar: [
        { satirlar: ["Sonra ölüyor."], sure: 2.5, renk: KIZIL },
        { satirlar: ["Kılıcıyla değil, şiirleri", "ve bir lakapla anılıyor:", "Kalender"], sure: 4.0, renk: ALTIN },
        { satirlar: ["Timur dünyayı kılıçla titretti,", "torunu geriye şiir bıraktı"], sure: 3.0 },
      ] },
  ],
  kapanis: {
    satirlar: ["Ermiş mi,", "şair mi?"],
    sonraki: "Sıradaki: Uluğ Bey mi, Baysungur mu?",
    sure: 9, arka: 89, gece: true,
  },
};
```

`Root.tsx` kaydı: `Kalender` bileşeni `TimurSeri` kalıbıyla eklenecek.

---

## 4) Yeni figür isteği

Aşağıdaki tüm figürler `figur()` ile çağrılacak şekilde düşünüldü.

| # | Figür | Boy / ölçek | Zemine nasıl bastığı | Sahne | Şimdiki yedek çözüm |
|---|---|---|---|---|---|
| 1 | **Taht** (oyma ahşap, altın ve kızıl minderli) | oturan Kalender'den ~%60 yüksek, `s≈3.4` | Dört ayak `z`'ye basar; üst yüz `y` döndürür (`sedir` gibi) | 72, 73 | `sedir` (altın renk) |
| 2 | **Kitap rafı** (kitap sırtları, kandil nişi) | insandan ~%30 yüksek; tabanı `z`'de | Ahşap alt kasası zemine oturur | 74, 77 | `ic_mekan` kemer nişleri |
| 3 | **Yazı masası / rahle** (alçak, üstünde kâğıt ve kalem) | oturan dizi hizası | Ayakları `z`'de | 74, 77, 81, 88 | `oturan el='kalem'` |
| 4 | **Kadeh ve sürahi** (yerde ya da rahlede) | el boyu, ~6–8 px (`s=1`) | Dibi zemine ya da rahle üstüne oturur | 81, 84, 85, 88 | `oturan el='kase'`, saki `silah='testi'` |
| 5 | **Duvara dayalı kılıç** | insan boyunun ~%70'i | Alt ucu zemine, üstü duvara yaslanır | 72, 81, 88 | `kisi silah='kilic'` (muhafız) |
| 6 | **Hilal ay** | küçük, ince | gökyüzünde, yazı bandı dışında | 86 | `gokyuzu`'nda küçük `gunes_` |
| 7 | **Gül çalısı** (dikenli, kızıl çiçekli) | insan dizi hizasından göğse | Gövdesi zemine sabit, üst kısım rüzgârda salınır | 83, 84 | `cicek renk='#c8302a'` büyük ölçek |
| 8 | **Arap kara çadırı** (Leyla) | yurt boyunda, ışıklı kapı | Taban düz zemine oturur | 87 | `yurt isik=True` |
| 9 | **Takke / derviş külahı** (`kisi bas='takke'`) | baş boyu | baş figürüne ait | 76, 78, 89 | `bas='sarik'` (`'takke'` değeri fonksiyon referansında yok) |
| 10 | **Altın sikke ve kese** | 2–3 px | elden ele (kısa süreli) | 78 | `piksel()` ile sarı iki piksel |

---

## Kod tarafına notlar (doğrulanması gerekenler)

1. `abanoz_tabut(d, x0, x1, omuz)` imzasındaki `d` için kare tuvali (`t`) verdim. Sahne 63'teki çağrı kalıbı farklıysa onu kullanın. `omuz = z[0] − 58` tahminidir, önizlemede taşıyıcı omuzlarına göre ayarlanmalı.
2. `KARE` ve `PAY` sabitlerini `sahneler` içinden import ettim. Başka modülde tanımlıysa import satırı değişir.
3. `oturan(minder=...)` için renk dizesi verdim. Parametre mantıksal değerse dize de doğru kabul edilir. Renk olarak kullanılıyorsa renk görünür.
4. İç mekân sahnelerinde (72, 74, 77, 81, 85, 88) kare boyutları ve x konumları görünür aralığa göre seçildi. Oturan figürlerin gerçek genişliği `onizleme`'de kontrol edilmeli, çakışma olursa x değerleri 10–15 px kaydırılır.
5. Sahne 85 ve 87'nin ikinci `Bolum` olarak kullanılması motorda doğrulanmalı. Desteklenmezse yedek: 90 ve 91 numaralı iki ek sahne.
6. Dönem uyumu için Timurlu şehzadelerde taç yerine `sorguc` kullandım. Hâtim-i Tâî sözü ve sadaka sahnesi (78) rivayet olarak yazıda zaten işaretli.
