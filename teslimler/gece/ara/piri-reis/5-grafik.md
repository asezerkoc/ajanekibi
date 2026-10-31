# Haritayı Çizen Adam: grafik teslimi

**İş:** Piri Reis'in haritaları ve idamı (1513-1554), gece vardiyası 6/10 · **Hazırlayan:** 🟢 SKONSTART Grafiker · **Girdi:** 4-kalite-metin.md (nihai seslendirme metni, 54 ekran kartı, grafiker notları)

**Dosyalar**
- Çizim: `video/piksel/piri_reis.py`, sahneler **330-367** (38 sahne; 368-369 boş kaldı). Çalıştırma: `python3 -I video/piksel/piri_reis.py [no ...]`. Çıktılar `video/public/sahne330-*.png` … `sahne367-*.png` (gokyuzu, uzak, orta, on, karakter; 333 ve 356'da ayrıca `hava`).
- Video: `video/src/sahneler/PiriReis.tsx`. Dışa aktarılanlar: `PIRI_REIS_SERI`, `PIRI_REIS_KARE`, `PiriReis`. Etiket "PİKSEL TARİHİM · PİRİ REİS", ses `piri-reis-anlatim.mp3`. `Root.tsx`'e ve başka konuların dosyalarına dokunulmadı.
- Bir kapak, 42 anlatım bölümü ve kapanış var. Tahmini süre: 2 sn kapak + yaklaşık 284 sn anlatım (kartlar 263 sn, sahne araları 0,5 sn) + 3 sn kapanış. Kart süreleri harf sayısına göre dağıtıldı; `ses/hizala_seri.py` bunları sese göre yeniden yazacak.
- Kapak: `{ // KAPAK }` bloğu sahne 330'un katmanlarını kullanır. Tek yazı bloğu var: "Haritayı / Çizen Adam / Piri Reis'in sonu" (boy 112, ALTIN, sure 2.0, yaziY 250).
- Kart metinleri kalite kontrolün nihai listesinden betikle alındı. Betik şunları doğruladı: 54 kart var, her satır en çok 30 harf, kartlar birleştirilince seslendirme metniyle karakter karakter aynı. Kart 41'de ve hiçbir sahnede rakam ya da yazı çizilmedi; "1498" hiçbir yerde yok.
- Sahne sayısı brifteki 22-32'nin üstünde. Gerekçe: aralık 3 dakikalık iş için yazılmış, bu video yaklaşık 4:50. Oranlanınca 38 sahne, her 7 saniyede bir sahne değişimi demek.

## Kurgu ve yön dili

Video Kahire'de açılır ve orada kapanır. Kart 1'de avluda yaşlı kaptan ve fermanı tutan çavuş var (330). Kart 29'da ve 52-53'te aynı avlu gece boş görünür; kaptanın durduğu yerde yalnızca yere bırakılmış bir fener yanar (352). İdam, cellat ve son an gösterilmez. Divan anlatımı ferman üzerinden kuruldu: 351'de Kahire'de taş divan odası var, çavuş fermanı okur, kaptan ayakta dinler. Divanda yargılama sahnesi çizilmedi, çünkü kaynak yok.

Yön dili şöyle: sağ sefere ve doğuya gidiş, sol eve dönüş ve geride kalan.
- Filo Maskat'a sağa yol alır (345).
- Basra'ya çekilirken (347) ve üç gemiyle dönerken (350) sola gider.
- Seydi Ali'nin donanmasını fırtına sağa, Hindistan'a sürükler (356).
- Seydi Ali karadan eve sola döner (357).

Motifler görselde de tekrar eder:
- **Ceylan derisi parşömen:** Aynı `harita_masasi` çizimi kart 7'de (335, Piri'nin masası) ve kart 38'de (360, 1929 deposu) var. Aynı kuşbakışı parşömen beş yakın planda kullanılır: 336, 337, 361, 363, 365, 367.
- **Basra'da kalan donanma:** 349 (kart 25), 350 (yalnızca üç gemi çıkar, geride donanma kalır), 354 (aynı rıhtım, gündüz) ve kapanış sorusu kart 54'te yine 349.

Kişilerin renkleri bütün videoda aynı kalır:
- **Piri:** deniz yeşili kaftan, beyaz kavuk. Gençken kara sakallı (332, 338), 1513'te kır sakallı. 1524'ten sonra lacivert kaptan pelerini var. 1547'den sonra ak sakallı.
- **Kemal Reis:** kızıl kaftan. **Çavuş:** kırmızı kaftan, beyaz börk. **Kubad Paşa:** hardal kaftan. **Seydi Ali:** lacivert kaftan, kızıl pelerin.
- **Yavuz:** kızıl, sakalsız. **İbrahim Paşa:** yeşil kaftan, altın pelerin. **Kanuni:** mor.
- **1929-1960 kişileri:** şapkalı ve ceketli. Halil Edhem ak sakallı. Ohlmeyer'in üstünde mavi-gri üniforma ve kasket var.

## Sahne planı

Zemin: dış mekânda sprite tabanı 632, iç mekânda 634. Bu satırlar ayakların bastığı son satırdır; `taban_denetimi` her karede doğrular. Deniz sahnelerinde su sprite'ın içinde çizilir: önde gemilerin su çizgisi 614, arkada 600 ve gövdenin altı suda kalır. Kuşbakışı sahnelerde zemin masa düzlemidir: parşömen, kaynak haritalar ve hokka masada yatar, gölgeleri masaya düşer. Bu sahnelerde masa orta plandadır ve sprite'la aynı paralakstadır (kamera 0), bu yüzden kâğıt masada kaymaz. Süre sütunu tahmindir: kartlar artı 0,5 sn.

| No | Süre (sn) | Konu | Zemin çizgileri | yakin / kamera | Hareket | Kartlar |
|---|---|---|---|---|---|---|
| 330 | 7.0 | Kahire, alacakaranlık: yaşlı denizci avluda, karşısında fermanı tutan çavuş | 632; orta plandaki yapılar 584-588 | 2.8 / 6, x 270 | fps 8 | 1 (KIZIL) |
| 331 | 12.3 | bugün, Topkapı: vitrinde parşömen harita, iki ziyaretçi | 634 (iç mekân döşemesi) | 2.8 / 6, x 270 | fps 10 | 2, 3 (ALTIN) |
| 332 | 5.8 | korsan kadırgasının güvertesi: genç Piri ve Kemal Reis; uzakta İspanya kıyısı | 632; orta plandaki yapılar 584-588 | 2.6 / 10, x 270 | fps 10 | 4 |
| 333 | 4.8 | fırtına: kadırgalar dalgalarda, şimşek | Su sprite'ın içinde; gemi su çizgisi 614 (arka sıra 600) | 2.4 / 14, x 270 | fps 12 | 5 (KIZIL) |
| 334 | 4.3 | Gelibolu kıyısı, akşam: Piri kasabaya yürür | 632; orta plandaki yapılar 584-588 | 2.8 / 10, x 250→290 | fps 16 | 6 |
| 335 | 9.6 | Gelibolu, 1513: Piri masada ceylan derisi parşömene çizer | 634 (iç mekân döşemesi) | 3.0 / 6, x 270 | fps 10 | 7, 8 (ALTIN) |
| 336 | 9.1 | kuşbakışı masa: kalem kenara yazar; eski haritalar ve Arap haritası | Kuşbakışı masa: masa düzlemi; parşömenin alt kenarı 634 | 2.2 / 0, x 270 | fps 10 | 9, 10 |
| 337 | 6.3 | kuşbakışı masa: dört Portekiz haritası ve Kolomb'un haritası da masada | Kuşbakışı masa: masa düzlemi; parşömenin alt kenarı 634 | 2.2 / 0, x 270 | fps 8 | 11 |
| 338 | 5.8 | gece odası: İspanyol esir anlatır, Piri yazar | 634 (iç mekân döşemesi) | 3.0 / 6, x 270 | fps 10 | 12 |
| 339 | 6.1 | Mısır, 1517: otağ önünde tahtta Yavuz, diz çökmüş Piri haritayı sunar | 632; orta plandaki yapılar 584-588 | 2.8 / 8, x 270 | fps 10 | 13 |
| 340 | 4.6 | hazine odası: sandıkta dürülmüş harita, raflar, toz | 634 (iç mekân döşemesi) | 3.0 / 4, x 270 | fps 8 | 14 (ALTIN) |
| 341 | 15.3 | 1524, güverte: Pargalı İbrahim Paşa ve el yazması kılavuzuyla Piri | 632; orta plandaki yapılar 584-588 | 2.6 / 10, x 270 | fps 10 | 15, 16, 17 |
| 342 | 5.5 | 1526: tahtta Kanuni, rahlede Kitab-ı Bahriye, Piri ayakta | 634 (iç mekân döşemesi) | 2.8 / 6, x 270 | fps 10 | 18 (ALTIN) |
| 343 | 6.7 | Süveyş, 1547: rıhtımda yaşlı Piri beratı alır; demirli kadırgalar | 632; orta plandaki yapılar 584-588 | 2.8 / 8, x 270 | fps 10 | 19 |
| 344 | 4.2 | Aden: krater dağlarının önünde surlu şehir, önde kadırgalar | Su sprite'ın içinde; gemi su çizgisi 614 (arka sıra 600) | 2.4 / 10, x 270 | fps 10 | 20 |
| 345 | 7.0 | 1552: donanma sağa, Maskat kalesine yol alır | Su sprite'ın içinde; gemi su çizgisi 614 (arka sıra 600) | 2.4 / 12, x 240→300 | fps 12 | 21 |
| 346 | 6.1 | Hürmüz surları; ufukta Portekiz yelkenleri | Su sprite'ın içinde; gemi su çizgisi 614 (arka sıra 600) | 2.4 / 10, x 270 | fps 10 | 22 (KIZIL) |
| 347 | 4.4 | alacakaranlık: filo sola, hurmalı Basra kıyısına çekilir | Su sprite'ın içinde; gemi su çizgisi 614 (arka sıra 600) | 2.4 / 12, x 300→240 | fps 12 | 23 |
| 348 | 6.4 | Basra sarayı: Kubad Paşa minderde şikâyet yazar, Piri ayakta | 634 (iç mekân döşemesi) | 2.8 / 6, x 270 | fps 10 | 24 (KIZIL) |
| 349 | 5.1 | Basra limanı, akşam: demirli donanma; rıhtımda yaşlı kaptan | 632; orta plandaki yapılar 584-588 | 2.8 / 8, x 270 | fps 8 | 25 |
| 350 | 5.6 | ganimet yüklü üç kadırga sola döner; donanma geride kalır | Su sprite'ın içinde; gemi su çizgisi 614 (arka sıra 600) | 2.4 / 12, x 300→240 | fps 12 | 26 (ALTIN) |
| 351 | 9.1 | Kahire, divan odası: çavuş fermanı okur, Piri ayakta dinler | 634 (iç mekân döşemesi) | 2.8 / 6, x 270 | fps 10 | 27, 28 (KIZIL) |
| 352 | 3.4 | aynı avlu, gece: boş | 632; orta plandaki yapılar 584-588 | 2.8 / 4, x 270 | fps 8 | 29 (KIZIL) |
| 353 | 9.0 | arşiv: raflar, masada iki defter, tek mum | 634 (iç mekân döşemesi) | 2.8 / 6, x 270 | fps 8 | 30, 31 (ALTIN) |
| 354 | 6.9 | Basra rıhtımı, Şubat 1554: Seydi Ali Reis donanmayı devralır | 632; orta plandaki yapılar 584-588 | 2.8 / 8, x 270 | fps 10 | 32 |
| 355 | 4.6 | Umman Denizi: kadırgalar ve Portekiz gemileri, top dumanı | Su sprite'ın içinde; gemi su çizgisi 614 (arka sıra 600) | 2.4 / 14, x 270 | fps 12 | 33 |
| 356 | 5.4 | fırtına donanmayı sağa, Hindistan'a sürükler | Su sprite'ın içinde; gemi su çizgisi 614 (arka sıra 600) | 2.4 / 14, x 240→300 | fps 12 | 34 (KIZIL) |
| 357 | 7.1 | kara yolu: Seydi Ali atlı, yanında yaya yoldaş ve deve; sola, eve | 632; orta plandaki yapılar 584-588 | 2.6 / 12, x 300→250 | fps 16 | 35 |
| 358 | 5.7 | Seydi Ali minderde kitabını yazar | 634 (iç mekân döşemesi) | 3.0 / 6, x 270 | fps 10 | 36 (ALTIN) |
| 359 | 3.9 | Topkapı, 1929: Babüsselam kapısı; iki kişi içeri yürür | 632; orta plandaki yapılar 584-588 | 2.8 / 8, x 250→280 | fps 14 | 37 |
| 360 | 9.3 | 1929, saray deposu: kâğıt desteleri; Halil Edhem ve parşömene eğilen Deissmann | 634 (iç mekân döşemesi) | 2.8 / 6, x 270 | fps 10 | 38, 39 |
| 361 | 6.3 | kuşbakışı: parşömen keçe üstünde, kenar notu parlar | Kuşbakışı masa: masa düzlemi; parşömenin alt kenarı 634 | 2.2 / 0, x 270 | fps 8 | 40 (ALTIN) |
| 362 | 6.3 | 1933: Kahle çalışma odasında yazısını tutar | 634 (iç mekân döşemesi) | 2.8 / 6, x 270 | fps 10 | 41 |
| 363 | 3.6 | kuşbakışı: parça ve kayıp kısmın noktalı çizgisi | Kuşbakışı masa: masa düzlemi; parşömenin alt kenarı 634 | 2.2 / 0, x 270 | fps 8 | 42 (KIZIL) |
| 364 | 10.9 | 1960, gece: Yarbay Ohlmeyer lambanın altında mektup yazar | 634 (iç mekân döşemesi) | 2.8 / 6, x 270 | fps 8 | 43 (KIZIL), 44 |
| 365 | 4.4 | kuşbakışı, soğuk mavi: haritanın altındaki kıyı | Kuşbakışı masa: masa düzlemi; parşömenin alt kenarı 634 | 2.2 / 0, x 270 | fps 8 | 45 |
| 366 | 12.8 | kitap yığınları: Hapgood elinde kitabı | 634 (iç mekân döşemesi) | 2.8 / 6, x 270 | fps 10 | 46, 47 |
| 367 | 10.6 | kuşbakışı, sıcak ışık: doğuya bükülmüş kıyı altınla izlenir | Kuşbakışı masa: masa düzlemi; parşömenin alt kenarı 634 | 2.2 / 0, x 270 | fps 8 | 48, 49 (ALTIN) |
| 337 | 6.4 | kenardaki kaynaklar: 337'ye dönüş | Kuşbakışı masa: masa düzlemi; parşömenin alt kenarı 634 | 2.2 / 0, x 270 | fps 8 | 50 (ALTIN) |
| 331 | 5.1 | bugün: vitrindeki harita (331'e dönüş) | 634 (iç mekân döşemesi) | 2.8 / 6, x 270 | fps 10 | 51 (ALTIN) |
| 352 | 6.7 | boş avlu, gece (352) | 632; orta plandaki yapılar 584-588 | 2.8 / 4, x 270 | fps 8 | 52 (KIZIL), 53 (KIZIL) |
| 349 | 4.3 | Basra'da kalan donanma: soru (349) | 632; orta plandaki yapılar 584-588 | 2.8 / 8, x 270 | fps 8 | 54 (ALTIN) |

Özel ayarlar:
- 333 ve 356'da yağmur katmanı var (`hava: 30`) ve kamera sarsılır (`sarsinti: 2`). Şimşek, yazı bandını kesecek bir zikzak olarak çizilmedi; bütün karede soluk bir parlama olarak görünür.
- 355'te kamera sarsılır (`sarsinti: 2`).
- Kuşbakışı sahnelerde `odakY: 560` kullanıldı, böylece parşömen yazının altında büyük görünür.

## Yeni figürler (hepsi `piri_reis.py` içinde, ciz.py'ye eklenmedi)

- **`parsomen_harita`** (kuşbakışı ceylan derisi parşömen, 120×160·s): Solda Güney Amerika kıyısı var; altta doğuya bükülür. Sağda Afrika ve İberya kıyısı, ortada rüzgâr gülü ve pusula hatları, Antiller, küçük gemiler, kara üstünde kenar notları ve yırtık sağ kenar var. `vurgu` parametresi şunları seçer: "not" (kaynak notu altınla nabız gibi parlar, 361), "soguk" (mavi ışık, alttaki kıyı buz mavisi parlar, 365), "buk" (bükülen kıyı boyunca altın noktalar akar, 367). Haritanın bire bir kopyası değildir. Buz kıtası, uzaylı ya da uçan cisim çizilmedi.
- **Masadaki kaynaklar** (kuşbakışı, kâğıtlar masaya gölge düşürür):
  - `eski_tomar`: dürülmüş eski haritalar
  - `arap_haritasi`: yuvarlak dünya haritası
  - `portekiz_haritasi`: portolan; pusula hatları kâğıdın içinde kalır
  - `kolomb_haritasi`: temsilî; altın çerçevesi parlar
  - `hokka`
  - `yazan_el`: kalem tutan el ve kaftan yeni; yen sprite'ın alt kenarına kadar uzanır
- **Yandan görünen figürler:**
  - `harita_masasi`: üstünde parşömen yatan alçak masa
  - `vitrin`: eğik camlı müze vitrini; camın altında parşömenin küçük görüntüsü var
  - `sandik`: demir kuşaklı sandık; üstünde dürülmüş parşömen yatar
  - `kagit_destesi`: iple bağlı desteler
  - `hurma`
  - `piramit` (uzak plan)
  - `babusselam`: Topkapı Orta Kapı; iki külahlı kule, saçaklı kapı
  - `fener`: yere bırakılmış fener
  - `halat`, `fici` (güverte eşyaları)
  - `portekiz_gemisi`: kütüphanedeki kadırga, beyaz yelkende kırmızı haç ile
- **Katman yardımcıları:**
  - `_guverte`: orta planda kadırga güvertesi; küpeşte ve kürek delikleri var, direk çizilmez
  - `_masa_ustu`: kuşbakışı masa ya da keçe yüzeyi
  - `_liman`, `_orta_deniz`, `_kiyi_orta`, `_deniz_sprite`: gemi çizilir, ardından o geminin su çizgisinden aşağısı suyla örtülür
  - `_su`, `_hava`
- **Kopyalananlar:** `masa` ve `kitap_rafi` (raflarda rulo seçeneği eklendi) Çelebi dosyasından; `osmanli_camii` ve gemi denetimi Takiyüddin dosyasından. Ölçek ve kadraj yardımcıları (`s_kisi`, `s_oturan`, `_kz`, `_spr`) cem_sultan'dan import edilir.

## Grafiker öz denetimi

**Çalıştırma:** `python3 -I video/piksel/piri_reis.py` 38 sahnenin hepsini hatasız çiziyor (çıkış 0). Her sahne üç denetimden geçiyor:
1. **`taban_denetimi`:** Her karede en alttaki opak piksel son satırda.
2. **`_kadraj`:** Figürler görünür aralıkta ve baş kesilmiyor.
3. **Yazı bandı denetimi:** Çelebi dosyasının denetimi alındı ve `odakY` desteği eklendi. PiriReis.tsx'teki her kartın gerçek yazı yüksekliği, yakin ile 1,06·yakin yakınlıkta dünya y'sine çevrilir. Sprite'ta ya da orta planda o satırlara giren opak piksel varsa betik durur. Kuşbakışı sahnelerde orta plan tamamen masa olduğu için yalnızca sprite denetlenir.

**TypeScript:** `cd video && npx tsc --noEmit -p .` temiz (çıkış 0).

**Neye baktım:**
- Önizleyici Remotion kamerasını taklit ediyor: katmanları birleştirip sx/odakY çevresinde ilk karede yakin, son karede 1,06·yakin büyütüyor ve yazı bandını çerçeveyle gösteriyor. 38 sahnenin hepsini bununla açıp baktım.
- Sahnelerin bir kısmını düzeltmelerden sonra yeniden açtım.
- Ham sprite karelerine ayrıca baktım: 336, 350, 357, 333. Hepsi son satıra basıyor; havada nesne yok. Tavandan sarkan tek şey kandil zinciri.
- Bir kenar raporu betiği 24 karenin hepsinde kadraj kenarına değen pikselleri taradı. Denizdeki sprite'larda kenara değen tek şey su; bu bilinçli bir seçim.

**Düzelttiklerim:**
1. **Yazı bandı ve kadraj:**
   - 357'de atlının kavuğu yazıya giriyordu (denetim durdurdu). Atlı ölçeği Çelebi dosyasındaki atlı/kişi oranına çekildi, sahne yakin 2,6'ya alındı. Deve küçültülüp içeri alındı.
   - 330 ve 352'deki minareli cami kadraj kenarında kesiliyordu; iki figürün arasına alındı.
   - 343'te demirli gemiler kenarda kesiliyordu; 356'da gemiler kadrajın solunda kalıyordu. İkisi de ortaya çekildi.
   - 359'da iki adam kapıyı örtüyordu; kapı sağa, adamlar sola alındı.
   - 340, 353, 362 ve 366'da raflar, 332'de fıçı, 342'de taht, 360'ta lamba ve desteler kenara değiyordu. Hepsi içeri çekildi.
2. **Ölçek:**
   - 335'te parşömen masası Piri'yi örtüyordu; masa küçültülüp yanına alındı.
   - 353 ve 360'ta kâğıt desteleri masadan büyüktü; küçültüldü.
   - 342'de rahle ve kitaplar okunmuyordu; büyütüldü.
   - 336'da kalem tutan el ve hokka çok küçüktü; büyütüldü.
3. **İmge ve okunurluk:**
   - 332'de Kemal Reis'in kaldırdığı kılıç, yeğenine saldırıyor gibi okunuyordu. Kılıç kaldırıldı; Kemal Reis eliyle kıyıyı gösteriyor.
   - 331'deki müze penceresinde "kar" vardı; düz cama çevrildi.
   - 337'de Portekiz haritalarının pusula hatları kâğıdın dışına taşıyordu; kâğıda kırpıldı.
   - 339'da piramitler kadraj dışında kalıyordu; görünür alana alındı.
   - 352'de fener büyütüldü.
   - 365'teki mavi ışık griye kaçıyordu; daha soğuk bir maviye çevrildi.
   - 349 ve 354'te karşı kıyıdaki hurmalar yazının arkasına uzanıyordu; alçak bir hurmalık şeridine indirildi.
   - Deniz sahnelerinde su yüzündeki köpük çizgisi seyreltildi; arka gemilerde kaldırıldı, ikinci bir ufuk çizgisi gibi görünmesin diye.
   - 332'deki uzak kale küçültüldü.

**Kalite kontrol notlarına uyum:**
- Kart 41'de "1498" yok; hiçbir sahnede rakam ya da yazı çizilmedi.
- Basra'dan yalnızca üç gemi çıkar (350). Güvertelerinde ganimet sandıkları var; batan gemi çizilmedi.
- İdam, cellat ve son an yok.
- Efsane bölümünde (kart 43-50) uzaylı, uçan cisim ve buz kıtası çizilmedi. Antarktika iddiası yalnızca soğuk mavi ışıkla verildi; cevap bükülen kıyının altınla izlenmesiyle verildi.
- Kart 21 Maskat sahnesinde (345) duruyor: filo sağa, kaleye doğru yol alıyor. Kartın ortasında sahne değiştirmek kartı bölmeyi gerektirirdi, bu da harfi harfine kuralıyla çelişirdi.
- Kart 22'nin tamamı Hürmüz'de: surlar ve ufukta Portekiz yelkenleri (346).

**Açık kalan, kalite kontrolün karar vereceği noktalar:**
- Dış mekân sahnelerinde uzak plandaki tepeler, kıyı ve uzak gemiler yazının arkasında kalıyor. Bu, onaylı Çelebi işindeki gibi; motor uzak planı sürekli kaydırdığı için uzak gemiler de akar.
- Deniz sprite'larının su kenarı yerel x 0 ve 400'de, görünür alanın çok dışında kalıyor.
