# 🟢 Grafik: Su Akmıyor (Don-Volga kanalı, 1569 → 1952)

**İş:** Piksel Tarihim, gece vardiyası 4/10 · slug `don-volga-kanali` · **Hazırlayan:** 🟢 SKONSTART Grafikeri · 31 Ekim 2026
**Dosyalar:** `video/piksel/don_volga_kanali.py` (sahneler 250-289, 40 sahne) · `video/src/sahneler/DonVolga.tsx` (export `DON_VOLGA_SERI`, `DON_VOLGA_KARE`, `DonVolga`; etiket "PİKSEL TARİHİM · DON-VOLGA KANALI"; ses `don-volga-kanali-anlatim.mp3`)
**Girdi:** 4-kalite-metin.md, 52 kart harfi harfine (TSX üretici kartları dosyadan okuyup birleşimini seslendirmeyle karşılaştırarak doğruladı). Süreler harf oranıyla 254 sn'ye dağıtılmış tahmindir; `ses/hizala_seri.py` yeniden yazar.
**Kapak:** sahne 250 katmanları, `["383 Yıl", "Akmayan Su", "Sokollu'nun Don-Volga kanalı"]`, boy 112, ALTIN, 2.0 sn, yaziY 270, açılış satırı `    { // KAPAK`.

## Sahne planı

Sprite ölçüleri: dış 400×220 (taban 632), hendek 400×230 (taban 640 = yarığın tabanı), iç 400×300 (taban 634), su 400×260 (taban 640, su çizgisi 610), kapak/kilit 400×360 (taban 760, odak 620), panorama 560×230.

| No | Süre (sn, tahmini) | Konu | Zemin çizgisi | Yakın / kamera | Hareket | Kartlar |
|---|---|---|---|---|---|---|
| 250 | 12.5 | şafak, bozkır: ilk kazma toprağa iner; Kasım Paşa izler | sprite tabanı 640 (hendek tabanı; yarık orta planda 626-640) | yakin 2.8, kamera 8 | sabit, fps 12 | 1, 2 |
| 251 | 3.1 | alacakaranlık: yarım kalmış sığ hendek, toprağa saplı kazma, tek asker | sprite tabanı 640 (hendek tabanı; yarık orta planda 626-640) | yakin 2.8, kamera 6 | sabit, fps 8 | 3 |
| 252 | 5.6 | İstanbul 1568: Sokollu harita sehpasının başında | iç mekân, taban 634 | yakin 3.0, kamera 6 | sabit, fps 10 | 4 |
| 253 | 11.8 | harita yakın: Don Azak'a, Volga Hazar'a; aradaki dar boğaz | iç mekân, taban 634 | yakin 3.2, kamera 4 | sabit, fps 8 | 5, 6 |
| 254 | 5.1 | Perevoloka: kütükler üstünde karadan çekilen tekne; önde halat çeken üç adam | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 8 | sabit, fps 10 | 7 |
| 255 | 5.1 | Astrahan: Volga'daki adada ahşap Rus kalesi; önde iki Rus nöbetçi | sprite tabanı 632; orta plan duz(586) | yakin 2.6, kamera 8 | sabit, fps 10 | 8 |
| 256 | 8.4 | alacakaranlık: yolu kapalı Türkistan hacıları ve develeri bekler | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 8 | sabit, fps 8 | 9, 10 |
| 257 | 12.0 | Sokollu fermanı defterdar Kasım'a uzatır; arkada harita | iç mekân, taban 634 | yakin 3.0, kamera 6 | sabit, fps 10 | 11, 12 |
| 258 | 6.3 | 14 Mart 1569: Maltsev ve uşağı Volga kıyısında at sürer; buzlu nehir | sprite tabanı 632; orta plan duz(586) | yakin 2.6, kamera 10 | x 300→250, fps 14 | 13 |
| 259 | 6.0 | Nogay atlısı yaralı ve bağlı Maltsev'i Azak'a götürür | sprite tabanı 632; orta plan duz(586) | yakin 2.6, kamera 10 | x 300→252, fps 12 | 14 |
| 260 | 6.6 | kadırga güvertesi: kürek başında esir Maltsev, nöbetçi, kıçta Kasım Paşa | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 6 | sabit, fps 10 | 15 |
| 261 | 4.3 | Ağustos 1569: kadırgalar Don'dan yukarı çıkar | su çizgisi dünya y 610 (gemi suya oturur) | yakin 2.6, kamera 8, yaziY 250 | x 250→290, fps 12 | 16 |
| 262 | 9.1 | bozkırda Devlet Giray ak atında; arkasında atlıları | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 8 | sabit, fps 10 | 17, 18 |
| 263 | 5.2 | Han uzakta nehirdeki kadırgalara bakar | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 8 | sabit, fps 10 | 19 |
| 264 | 6.7 | panorama: solda Don, sağda Volga; arada hendek boyunca kazıcılar | sprite tabanı 640 (hendek tabanı; yarık orta planda 626-640) | yakin 2.6, kamera -300 | sabit, fps 12 | 20 |
| 265 | 3.9 | öğle güneşi: hendekte kazan askerler; su yok | sprite tabanı 640 (hendek tabanı; yarık orta planda 626-640) | yakin 2.8, kamera 6 | sabit, fps 12 | 21 |
| 266 | 12.7 | akşam: kazı bırakılır; kazmalar toprakta, askerler sola gider | sprite tabanı 640 (hendek tabanı; yarık orta planda 626-640) | yakin 2.8, kamera 8 | x 292→258, fps 14 | 22, 23 |
| 267 | 5.9 | Kasım Paşa Azak'ı gösterir; ağır top kağnıda, öküzler koşulu | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 8 | sabit, fps 10 | 24 |
| 268 | 8.3 | ordu karadan doğuya, Astrahan'a yürür; toplar yok | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 10 | x 250→296, fps 16 | 25, 26 |
| 269 | 6.9 | Eylül 1569: harabeler arasında kamp; asker çadır kazığı çakar | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 8 | sabit, fps 12 | 27 |
| 270 | 7.6 | Kasım Paşa ve ağa uzaktaki adalı kaleye bakar; top yok | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 6 | sabit, fps 10 | 28 |
| 271 | 12.0 | gece: ateş başında iki asker fısıldaşır; uzakta Han'ın otağı | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 6 | sabit, fps 10 | 29, 30 |
| 272 | 4.5 | şafak: ulak dörtnala kampa girer | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 10 | x 330→214, fps 24 | 31 |
| 273 | 4.8 | Eylül sonu, yağmur: çadırlar sökülür, asker yüklerle batıya döner | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 8, hava 30 | x 286→256, fps 14 | 32 |
| 274 | 6.0 | boş kamp yeri: sönmüş ateşten duman, yerde sökülmüş çadır | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 6 | sabit, fps 10 | 33 |
| 275 | 7.3 | Kuzey Kafkasya, kavurucu güneş: diz çökmüş asker kuru dere yatağında su için kazar | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 8 | sabit, fps 10 | 34 |
| 276 | 6.2 | saldırı: oklar yağar, kalkanlı asker, düşmüş asker; uzakta Kazak atlıları | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 8, sarsinti 2 | sabit, fps 18 | 35 |
| 277 | 8.3 | Azak, fırtına sonrası: kırık direkli kadırga; uzakta barut deposundan duman | su çizgisi dünya y 610 (gemi suya oturur) | yakin 2.6, kamera 8, yaziY 250 | sabit, fps 10 | 36, 37 |
| 278 | 5.3 | Maltsev yalnız, kuzeye (sola) yürür; ilk kar | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 8, hava 10 | x 292→256, fps 14 | 38 |
| 279 | 4.8 | Moskova, ahşap oda: Maltsev mum ışığında raporunu yazar | iç mekân, taban 634 | yakin 3.0, kamera 6 | sabit, fps 10 | 39 |
| 280 | 4.5 | alacakaranlık: otlarla örtülmüş kuru hendek, paslı kazma | sprite tabanı 640 (hendek tabanı; yarık orta planda 626-640) | yakin 2.8, kamera 4 | sabit, fps 8 | 40 |
| 281 | 10.8 | 1697: Çar Petro ve mühendis Perry; köylü kazar | sprite tabanı 640 (hendek tabanı; yarık orta planda 626-640) | yakin 2.8, kamera 8 | sabit, fps 12 | 41, 42 |
| 282 | 4.3 | kuzeyde terk edilmiş hendek, kar; el arabası ve kürek | sprite tabanı 640 (hendek tabanı; yarık orta planda 626-640) | yakin 2.8, kamera 4, hava 10 | sabit, fps 10 | 43 |
| 283 | 8.1 | 1948: dikenli tel ardında mahkûmlar kazar; gardiyan, gözcü kulesi | sprite tabanı 640 (hendek tabanı; yarık orta planda 626-640) | yakin 2.8, kamera 8 | sabit, fps 12 | 44, 45 |
| 284 | 3.0 | 1952: beton kapak, kapalı; önündeki hazne kuru | beton düzlük, sprite tabanı 760 (odak 620) | yakin 2.6, kamera 4, odakY 620 | sabit, fps 10 | 46 |
| 285 | 6.3 | 31 Mayıs 1952, 13.55: kapak açılır, su hazneye hücum eder | beton düzlük, sprite tabanı 760 (odak 620) | yakin 2.6, kamera 4, odakY 620 | sabit, fps 16 | 47 |
| 286 | 2.0 | su, nihayet akıyor: dolu kanal, sakin akan su | beton düzlük, sprite tabanı 760 (odak 620) | yakin 2.6, kamera 4, odakY 620 | sabit, fps 12 | 48 |
| 287 | 4.5 | kanal girişinde dev Stalin heykeli (yüzsüz siluet) | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 4, yaziY 240 | sabit, fps 8 | 49 |
| 288 | 5.6 | kaide boş; sonra aynı kaidede Lenin | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 4, yaziY 240 | sabit, fps 2 | 50 |
| 289 | 12.3 | gün batımı: kanalda akan su; önde toprağa saplı eski kazma | sprite tabanı 632; orta plan duz(586) | yakin 2.8, kamera 6 | sabit, fps 8 | 51, 52 |

Vurgu renkleri: ALTIN 2, 3, 11, 15, 21 (motif), 33, 39, 40 (motif), 43 (motif), 48 (motif çözümü), 51, 52; KIZIL 8, 14, 18, 19, 26 ("ama"), 29, 32, 34, 35, 36, 45. Yavaş kartlar 3, 21, 40, 43, 48 ve 52 tek kartlık sakin sahnelere konuldu (kamera 4-6). Yazı süreleri hizalamayla değişir.

## Kurgu kararları

- **İki nehir aynı karede yok (kart 20):** Sahne 264 bir panorama. `kamera: -300` ile orta plan ve sprite birlikte kayıyor. Başta solda Don, sonda sağda Volga görünüyor, ortada sığ hendek boyunca beş kazıcı var. Gök ve uzak plan paralaksla daha yavaş akıyor, ön plan boş.
- **Hendek her zaman sığ bir yarık.** Orta planda, dünya y 626-640 arasında: güneşli uzak duvar, kuru ve çatlak taban, toprak yığınları. Kazıcılar yarığın tabanına (640) basıyor. Kazmanın ucu vuruş anında tam zemin satırına iniyor, ardından toprak yukarı sıçrıyor. Derin kanal hiçbir sahnede yok.
- **Su motifi:** 251 yarım hendek → 265 kuru hendek → 280 otlanmış kuru hendek → 282 kuzeyde karla dolu terk edilmiş hendek → 284 kapalı beton kapak, kuru hazne → 285 kapak açılıyor, su hücum ediyor → 286 dolu kanal (kart 48 "Su, nihayet akıyor."). Kapanışta (289) geride akan kanal, önde toprağa saplı eski bir kazma var.
- **Gemi ölçeği:** Kadırgalarda tek bir insan yok. Ölçeği güvertedeki, gemi ölçeğinde çizilmiş kürekçi başları veriyor. Sahne 260'ta kamera güvertede: arkada küpeşte, suya inen kürekler ve Don var, figürler güverte zeminine basıyor. Uzaktaki kadırgalar (261, 263, 267, 277) küçük ve ufka yakın, hepsi suyun içinde oturuyor. Hiçbir figür bir gemiye dokunmuyor.
- **Su üstünde yapı yok:** Astrahan kalesi (255, 270) nehrin ortasındaki adanın düz çimen üstünde duruyor; adanın kumlu kıyısı ve köpük çizgisi görünüyor. Azak kalesi (277) karadaki kıyı şeridinde. Kanal kuleleri beton düzlükte.
- **Maltsev'i yakalayanlar:** Araştırmaya göre elçiyi alıkoyan bir Nogay; bu yüzden 259'daki atlı Osmanlı değil, Nogay (kalpaklı) olarak çizildi. 260'ta Maltsev kürek sırasında oturuyor (rapor: "kürekçi/esir").
- **Han ve söylenti (271):** Ateş başında iki asker fısıldaşıyor. Uzaktaki mor-altın çadır Han'ın otağı. Söylentiyi kimin yaydığı gösterilmiyor; kart "tarihçiler işaret ediyor" diyor, görüntü yalnızca otağı uzakta tutuyor.
- **Heykeller (287-288):** Yüzsüz bronz siluetler. Stalin uzun paltolu, kasketli, eli göğsünde. 288'de fps 2 ile ilk 4 saniye kaide boş, sonra aynı kaidede kolunu uzatmış Lenin beliriyor.
- **Ay ve güneş çizilmedi.** Yakın kamerada görünen gök şeridi yazı bandının arkasında kalıyor (önceki işlerde ret nedeniydi); ışık paletle veriliyor. Bozkır sahnelerinde uzak planda dağ ve ağaç yok (`_uzak_duz`). Dağ yalnızca Kuzey Kafkasya sahnelerinde (275-276) var.

## Kişiler (renk kimlikleri; iki kişi aynı çizilmedi)

Sokollu: yeşil kaftan, ak sakal, beyaz sarık · Kasım Paşa: hardal kaftan, lacivert kürk, kara sakal · Maltsev: gri-mavi kaftan, koyu kalpak, açık kahve sakal · Devlet Giray: mor kaftan, sorguç, ak at · Nogay ve Tatarlar: kalpaklı, toprak tonları · Rus nöbetçiler: kırmızı kaftan · Yeniçeri: mavi, ak börk · Kazıcılar (azap): üç ayrı renk · Çar Petro: koyu yeşil, siyah şapka, diğerlerinden 1,12 kat uzun · Perry: kahverengi, ak peruk · Gulag mahkûmları: gri, kasketli · Gardiyan: haki.

## Yeni figürler (don_volga_kanali.py içinde; ciz.py'ye eklenmedi)

`kazici`, `kurekci`, `toprak_yigini`, `hendek_yarigi` (orta plan), `sapli_kazma`, `harita_sehpasi` (yazısız, iki nehirli harita; planlanan hendek kesik çizgi hâlinde parlıyor), `kayik_kutuk`, `ahsap_kale` (1569'da Astrahan ahşaptı), `kadirga` (latin yelken, mahmuz, kıç köşkü, gemi ölçeğinde tayfa; `hasar=1` ile kırık direk, suya sarkan seren, yan yatma), `kon_cadir` (`yikik=1` sökülmüş), `harabe`, `yatan_asker`, `dikenli_tel`, `gozcu_kulesi` (alçak), `el_arabasi`, `heykel_kaide`, `kilit`.

Hepsi `zemin_y` ya da `duz_zemin` ile zemine oturuyor. Başka serilerden alınanlar: `top_` (takiyuddin), `avrupali`, `masa`, `masa_mumu` (orhun).

## Grafiker öz denetimi

**Otomatik denetimler** (betik bir sahnede hata verirse durur; 40 sahnenin hepsi geçti):
- `taban_denetimi` her karede uygulandı.
- `_kadraj`: kare 0, 6, 12, 18. Sahne sonundaki yakınlaşmada (yakin·1.06) tam opak hiçbir piksel kadraj dışında kalmıyor. Kenar denetiminin bilerek kapatıldığı sahneler: 254'teki halat, 261/277'deki su, 264 panorama, 284-286'daki kilit ve kanal. Bunlar kadrajı boydan boya geçen su, zemin ve yapılar.
- `_bant_denetimi`: kartlar ve yakin değerleri DonVolga.tsx'ten okunuyor. Sprite'ın ve orta planın görünür sütunları, hiçbir kartta ve sahne sonu yakınlaşmasında yazı bandına girmiyor; panoramada kamera kaydırması da hesaba katıldı.
- `_gorunur`: orta plandaki önemli nesneler (kaleler, kayık, atlılar, gözcü kulesi) kadrajın içinde.
- `_sigdir`: harita, heykel, gemi ve kişiler yazıya değmeyen en büyük ölçekte. Kişiler kadrajın %30'unu hedefliyor; yazıya değecekleri sahnelerde sığan en büyük ölçek kullanıldı.

**Bakılan kareler:** 40 sahnenin hepsinin başlangıç ve son kareleri birleşik önizlemeyle (kamera, yakınlaşma ve yazı kutularıyla) açılıp tek tek incelendi.

**Bakarken düzelttiklerim:**
- 253: şamdan kenarda kesiliyordu, içeri alındı.
- 256: deve kenarda kesiliyordu ve başı hacının arkasında kalıyordu; deve sola döndürülüp kaydırıldı.
- 250: uzaktaki çadırlar kazıcının başının arkasında kalıyordu, iki figürün arasına alındı. Kalkık kazmanın sapı yüzün önünden geçiyordu, kalkış açısı dikleştirildi.
- 254: çekenler halatı yanlış yönde tutuyordu. Tekneye dönük, halatı elden ele çeker hâle getirildi; tekne kadraja alınıp küçültüldü.
- 255: kale nöbetçilerin arkasında kayboluyordu, kale sağa, nöbetçiler sola alındı.
- Uzak planda bozkırın ufkunda ağaç gibi görünen sivri dağ sırtı vardı; ağaçsız düz ufukla değiştirildi.
- Saray pencerelerinde kar gibi görünen beyaz noktalar vardı, giderildi.
- 258, 259, 262, 263: atlılar kenarda kesiliyordu, yerleri ayarlandı.
- 260: Maltsev'in küreği güverteye saplanmış gibi duruyordu; artık küpeşteden suya iniyor.
- 267: top oyuncak gibi küçüktü, büyütüldü ve öküz çıkarıldı. Geride dönen kadırga Kasım Paşa'nın arkasından alındı.
- 273: çadırlar kenarda kesiliyordu, içeri alındı.
- 276: oklar yazı bandına giriyordu, aşağı alındı. Kazak atlıları görünür aralığa çekildi.
- 280: sprite tabanı boştu (taban denetimi); nesneler yarığın tabanına indirildi.
- 284-286: kule tepeleri 3 satırlık kartta yazıya değiyordu, kuleler alçaltıldı.
- 287: Stalin silueti satranç taşı gibi okunuyordu; omuzlar ve kasket eklendi.

**Bilerek bıraktıklarım:**
- 260'ta yeniçeri nöbetçinin kılıcı esire doğru duruyor (bekçilik); figürler birbirine değmiyor.
- Hendek ve nehir gibi zemin öğeleri kenardan kenara uzanabiliyor; bunlar figür değil, arazi.
- 274, 280, 282 ve 284-289'da insan figürü yok. Bunlar sakin motif ve anıt kareleri; ana nesne kadrajın büyük kısmını kaplıyor.

**Kod tarafına not:** Root.tsx kaydı yapılmadı (brif gereği). Render öncesi Root kaydı ve `hizala_seri.py` ile ses hizalaması gerekiyor. `npx tsc --noEmit -p .` temiz.
