---
name: piksel-sahne
description: SKONSTART'ın 64-bit piksel sahne motoru (video/piksel/) için grafiker el kitabı. Katman ve koordinat kuralları, fizik denetimleri, 94 çizim fonksiyonu (insan, at, yurt, Timur, Bayezid, fil, deve, tank, kadırga, mancınık, otağ, kale, türbe, cami, iç mekân, hava…) ve ajansın onaylanmış 55 örnek sahnesi. Piksel sanatı bir sahne, sprite ya da Remotion Bolum planı istendiğinde yükle.
---

# Piksel sahne motoru

Ajansın her videosu aynı motorla üretilir: Python/PIL ile 540×960 ızgarada katmanlar çizilir, Remotion bunları
2 kat büyütüp paralaksla kaydırır ve sprite'ları kare kare oynatır. Bu dosya o motorun kurallarını anlatır.
Sen (grafiker) resim çizmezsin; **hangi fonksiyonun, hangi ölçek ve konumla çağrılacağını yazarsın**. Kod
fonksiyonlarından uydurma: yalnızca `references/fonksiyonlar.md` içindekileri kullan. Yeni bir figür gerekiyorsa
bunu teslimde "yeni figür isteği" diye ayrıca belirt, var olanlarla en yakın çözümü de ver.

## Bu skill nasıl kullanılır

1. Metindeki her sahne için `references/sahne-katalogu.md` tablosundan **en yakın örneği** bul (aynı mekân türü,
   aynı figür sayısı, gündüz/gece, iç/dış mekân).
2. Kullanacağın figürlerin imzalarını `references/fonksiyonlar.md` dosyasından oku; parametre adlarını aynen kullan.
3. Sahneyi `references/sahne-tarifi.md` şablonuyla yaz: önce Türkçe sahne planı, sonra `sahneNN()` Python tarifi,
   sonra TSX `Bolum` satırı.
4. Teslimden önce "Fizik ve ölçek denetim listesi"ni satır satır uygula.

## Tuval ve katmanlar

| Katman | Dosya | Boyut (ızgara) | Paralaks | Ne var |
|---|---|---|---|---|
| gökyüzü | `sahneNN-gokyuzu.png` | 540×960, yatayda dikişsiz | kamera·0.1 | dither gradyan, güneş/ay, bulutlar, yıldızlar |
| uzak | `sahneNN-uzak.png` | 540×960, dikişsiz | kamera·0.3 | dağ sırtı, tepeler, ova (ufuk); `ekle` ile ufuk figürleri |
| orta | `sahneNN-orta.png` | **810**×960 | kamera·0.65 | çayır/çöl/kar; `ekle=` ile arka plandaki yurtlar, şehir, otağlar, ikinci sıra kalabalık |
| karakter | `sahneNN-karakter.png` (+`karakter2`) | w×h × 24 kare şerit | kamera·0.65 | animasyonlu figürler (sprite) |
| ön | `sahneNN-on.png` | 810×960 | kamera·1.25 | köşelerden yükselen uzun çimen; sahnenin önünde |
| hava | `sahneNN-hava.png` | 540×960 × 24 kare | sabit | yağmur ya da kar (`hava()`), döngü dikişsiz |

- Izgara 540×960; ekranda tam 2 kat (1080×1920), en yakın komşu büyütme, kenar yumuşatma yok. Bütün katmanlarda
  piksel boyutu aynıdır; sprite içinde "yakın plan" diye daha ince piksel kullanılmaz.
- Orta ve ön plan 810 geniştir: görünen kadraj orta planda x **135–675** arasıdır (`PAY = 135`). Orta plana bir şey
  koyarken ızgara x'ine 135 ekle (`PAY + x`).
- Yazı bandı: ekran yazıları ızgara y **95–245** arasında durur (`YAZI_BANDI`). Bu banda bulut konmaz (`gokyuzu` hata verir);
  uzak plandaki yüksek dağ tepeleri de buraya girmesin.

## Zemin çizgileri (en önemli kural)

Her katmanın kendi zemin çizgisi vardır ve her nesnenin **tabanı** bu çizgiye oturur:

| Nerede | Zemin (ızgara y) | Not |
|---|---|---|
| sprite'ın ayak izi | sprite'ın **son satırı** = `taban` (TSX'te) | karakter sprite'larında taban **630–634**; `taban_denetimi` her karede en alt opak pikselin son satırda olduğunu doğrular |
| orta plandaki figürler (`ekle=`) | **586–600** (genelde `duz(588)`) | orta planın üst kenarı `ust=(500,557)` civarında dalgalanır; figürler bu kenarın altında, dümdüz `duz(y)` çizgisine oturur |
| ufuk sprite'ı (uzak plandaki kervan, şehir) | **510–518** | `onizleme`'de tür `"ufuk"`; TSX'te ikinci sprite `dosya: "karakter2"`, `taban: 510` civarı |
| iç mekân (`ic_mekan`) | sprite tabanı 634, zemin katmanı `zemin_renk` | pencere, kemer ve çini kuşağı uzak katmandadır |
| su (`su_ve_kiyi`, `gemi`) | gemi `su_y` çizgisine oturur, alt kısmı suda | `gemi(img, x, su_y, ...)` |

Kurallar:
- Yapılar (`yurt`, `otag`, `koy_evleri`, `anadolu_kalesi`, `gur_i_emir`, `bibi_hanim`, `heykel`, `sehir`…) **yalnızca düz
  zemine** kurulur: `duz_zemin` toleransı aşan yamaçta `FizikHatasi` verir. Orta planda her zaman `duz(588)` gibi düz bir
  liste ver.
- Ayakta duran her figürün altına temas gölgesi düşer (`figur` bunu yapar). Havada duran tek nesne bile iş reddi sebebidir.
- Derinlik: arkadaki figür hem **daha küçük** hem **daha yüksek** bir zeminde durur (`duz(y - 12)` gibi); öndeki figür
  daha büyük ve daha alçakta. Aynı satırda duran iki figür aynı ölçekte olmalıdır.
- Ölçek oranları (sahibin kuralı): insan boyu = at boyunun ~%65–70'i. Örnek çiftler: `at s=2.9` ↔ `kisi/timur s=2.6`;
  `at s=3.4` ↔ `bayezid s=3.1`; yurt `s=3.8` yanında at `s=2.3`. Fil atın ~2 katı, deve atın ~1.3 katı, yurt kapısı
  insandan biraz kısa, tuğ direği yurdun ~2 katı.

## Sprite kuralları

- Her sprite sayfası yatay şerit, **24 kare** (`KARE`). `kare(t, z, i)` fonksiyonu i. kareyi çizer; `f = i / KARE` 0–1
  arası döngü fazıdır. Yürüyen figüre `adim=f`, ata `faz=f`, dumana `faz=f`, ateşe `f` verilir. Birden çok figürde
  fazları kaydır: `(f + j * 0.37) % 1` (aynı anda adım atan sürü robot görünür).
- Döngü dikişsiz olmalı: 24. kareden 1. kareye dönüşte sıçrama olmasın (sin/cos ile `f * 2π` kullan; kare sayısına bağlı
  rastgele değerleri `random.Random(sabit)` ile üret).
- Kare boyutu: sprite'taki en geniş figür grubunu 10–20 px pay ile saracak kadar; genellikle **w 300–540, h 140–200**.
  Kare yüksekliği ızgara y 960'a değil tabana göredir: sprite ekranda `top = taban*2 - h*2` konumuna gelir.
- Yürüyüş: `x: [baş, son]` TSX'te sprite'ı sahne boyunca kaydırır; sprite içinde figür yürür (`adim`), sayfa kayar.
  Bir ayak hep yerde kalır; kayma hızı adım hızıyla uyumlu olsun (fps 16–20, kayma 60–120 px/sahne).
- Oran: Sprite'ta hiçbir figür tuvalin dışına taşmaz (kesik baş = hata). `figur()` 1 px kontur için kenarlarda 2 px pay ister.
- Olay anı: sahnede bir şey oluyorsa (ok saplanır, kubbe çatlar, kol iner) `f < 0.5` / `f >= 0.5` ile iki evre çiz
  (sahne25 örneği); fps'i düşük tut (8–12) ki olay okunsun.

## Kamera ve görünür alan (TSX)

`Bolum` alanları: `no`, `yakin` (varsayılan 2.4; 1.8 geniş, 2.0–2.3 standart, 2.6+ yakın), `kamera` (paralaks genliği px,
varsayılan 36; 20 sakin, 50 hareketli), `sprite {w,h,fps,x,taban,dosya?,adet?}`, `hava` (kare hızı; yağmur 30, kar 10),
`sarsinti` (savaş 2–3 px), `odakY` (yakınlaşmanın odak satırı; verilmezse taban−12), `mektup`, `yazilar[]`.

- Yakın çekim `sx` (sprite x) ve `odakY` çevresinde büyütür. Görünen ızgara aralığı yaklaşık **sx ± 270/yakin**, kamera
  pan ile iki yana `kamera·0.65` px kayar. `yakin 2.0` ve `sx 270` için görünen x ≈ 135–405: sprite'taki önemli figürleri
  bu aralığa koy; kenarlara koyduğun figür görünmez.
- Sprite yerel x ↔ ızgara x: `yerel = izgara − (sx − w/2)`. Sprite 440 geniş ve `sx 270` ise yerel 0 = ızgara 50.
- Zemin kadrajın ~%66 hizasındadır (taban 630 → ekran 1260/1920): Reels alt arayüzünün üstünde kalır. Tabanı 600'ün üstüne
  çekme (figür yazı bandına girer), 650'nin altına indirme (arayüz örter).
- `yazilar`: her yazı `{satirlar, sure, boy?, renk?}`; satır ≤30 harf (uzunsa kod yeniden böler), 1–3 satır, son satır
  renkli (`ALTIN` vurgu, `KIZIL` ölüm/yenilgi). Sahne süresi = Σsure + 0.5 sn; yazı sahne başından 0.3 sn sonra başlar.
  Seslendirme varsa süreler `video/ses/hizala_seri.py` ile sese hizalanır; sen tahminî süre yaz (okuma hızı ≈ 14 harf/sn).
- `kapanis`: `{satirlar, sonraki, sure, arka, gece?}`; `arka` kapanış arkasında duran sahne numarası.
- Toplam süre (Reels): **90 saniyenin altında**; kapak varsa 2 sn kapak + anlatım.

## İş akışı ve komutlar (kod tarafı çalıştırır, sen tarifini yazarsın)

```sh
python3 -I video/piksel/<seri>.py 21 22      # sahneleri çiz; fizik denetimi geçmeyen sahnede betik durur
npx remotion still Timur1 --frame=N out.png  # kare al (video/ içinde)
uv run gorsel_kontrol teslimler/<teslim>.md <kare-klasörü>   # kalite kontrol kareleri değerlendirir
```

Yeni bir seri için: `video/piksel/<seri>.py` (sahne fonksiyonları, `timur.py` kalıbı), `video/src/sahneler/<Seri>.tsx`
(`TimurSeri.tsx` içindeki `Seri` tipi; `Timur1.tsx` kalıbı), `video/src/Root.tsx` kaydı. Sahne numaraları ajans
genelinde benzersizdir: 1–8 Cengiz, 11–17 Kayıp Mezar, 21–64 Timur; yeni seri **71**'den başlar.

## Fizik ve ölçek denetim listesi (teslimden önce)

1. Her figürün zemin listesi yazılı mı (`z`, `duz(588)`, `duz(set_y, w)`)? Havada duran nesne yok mu?
2. Yapılar düz zemine mi kuruldu? (orta planda `duz(...)`, sprite'ta `z`)
3. Aynı satırdaki figürler aynı ölçekte mi; insan/at oranı %65–70 mi; arkadaki figür hem küçük hem yüksek mi?
4. Yürüyen figürlerin yönü (`yon`) hareket yönüyle (`x: [baş, son]`) aynı mı? Sola giden figür `yon=-1` ve x azalır.
5. Duman/toz/kıvılcım yukarı; yağmur aşağı ve rüzgâr yönünde (`egim`); flamalar rüzgârla aynı yöne.
6. Önemli figürler görünür aralıkta mı (sx ± 270/yakin)? Bulut ve dağ tepesi yazı bandı dışında mı?
7. Sprite kare boyu figürleri kesmiyor mu; 24 kare döngü dikişsiz mi?
8. Dönem uyumu: anakronizm yok (ör. 1402'de hilalli sancak yok, 1941'de `tank`/`lamba` var). Tartışmalı sahneler yazıda
   "rivayete göre" diye işaretli.
9. Sahibin kapak görselleri varsa olduğu gibi kullanılır (`kapak:`), piksel tarzına çevrilmez.
