# 🟢 Grafik: Kalması Uygun Değil (Hezarfen Ahmed Çelebi'nin uçuşu, tek kaynak Evliya Çelebi)

**İş:** Piksel Tarihim (@pikseltarihim), gece vardiyası 7/10 · **Girdi:** 4-kalite-metin.md (nihai seslendirme, 47 kart) · **Hazırlayan:** SKONSTART Grafikeri · 31 Ekim 2026

**Dosyalar**
- Çizim: `video/piksel/hezarfen.py` (sahneler **370-406**, 37 sahne; aralık 370-409). Çalıştırma: `python3 -I video/piksel/hezarfen.py` → `video/public/sahne370…406-{gokyuzu,uzak,orta,on,karakter}.png`.
- Remotion: `video/src/sahneler/Hezarfen.tsx` → `HEZARFEN_SERI`, `HEZARFEN_KARE`, `Hezarfen`; etiket "PİKSEL TARİHİM · HEZARFEN", ses `hezarfen-anlatim.mp3`. Root.tsx'e dokunulmadı (kayıt kod tarafında).
- 39 Bolum: KAPAK + 38 anlatım bölümü. Sahne 370 üç kez kullanılır: kapak, kanca (kart 1) ve kart 37 "Peki Hezarfen gerçekten uçtu mu?" (açılış görüntüsüne dönüş).
- Tahmini süre ≈ 269 sn (kart başına ≈13 harf/sn + 0,5 sn bölüm payı + 2 sn kapak + 3 sn kapanış); `ses/hizala_seri.py` sese göre yeniden yazar.

**Kapak (3 satır, boy 112, son satır ALTIN):** "Galata'dan / Üsküdar'a / Kalması uygun değil" (başlık + ana motif alt başlık). Sahne 370 katmanları, yaziY 260, sure 2.0.
**Kapanış:** "Piksel Tarih / @pikseltarihim", sonraki: "Yorumlara yaz: altın mı, sürgün mü?", arka 406 (Üsküdar kıyısı, gün batımı).

## Kurgu ve yön dili

- **Sağ = doğu, Üsküdar, lodosun ittiği yön; sol = batı, sürgün (Cezayir).** Süzülüş sağa, sürgün gemisi sola, padişah köşkten sola (Galata'ya) bakar, Hezarfen son karede sola (geri, Galata'ya) bakar.
- Dört perde: (1) kanca, kule, Boğaz, kese ve sürgün tohumu (370-374); (2) öncüller İbn Firnas ve Cevherî, talim, kule, köşk, süzülüş, iniş, ödül ve hüküm, Cezayir (375-387); (3) Evliya ve Lagari'nin gecesi, 2009 deneyi (388-399); (4) tartışma, terazi, bugün, soru (370 dönüşü, 400-406).
- Renk/ışık: lodos sabahı ılık-puslu (uçuş günü), hüküm kızıl akşam, Cezayir ve Lagari gecesi lacivert, bugün gün batımı.
- **Vurgu kartları:** ALTIN 3, 6, 16, 17, 19, 22, 23, 31, 34, 37, 42, 45, 46, 47 (motif "Böylesinin kalması / uygun değil" kart 19 ve 45'te ALTIN); KIZIL 4, 10, 18, 20, 21, 35, 36. Kart metinleri betikle 4-kalite-metin.md'den alındı, sıra ve harfler bire bir (47/47 denetlendi), her satır ≤30 harf.

## Sahne planı

Zemin y değerleri ızgara satırıdır; sprite'ın son satırı `taban`. Dış mekânlarda sprite h 230, iç mekânlarda h 300 (kandil zinciri tavana kadar).

| No | Süre (sn, tahmini) | Konu | Kartlar | yakin / kamera | Sprite | Zemin çizgileri | Hareket |
|---|---|---|---|---|---|---|---|
| 370 | 2.5 | Kapak: sahne 370 katmanları, başlık (2 satır) + alt başlık (ana motif, ALTIN). Hizalama bu bloğu atlar. | kapak | 2.8 / 0 | 380×230, x 270, taban 632, 10 fps | şerefe döşemesi: orta üst kenar 600 + 8 px korkuluk; sprite tabanı 632 | kanatlar rüzgârla hafifçe kıpırdar; yazı yaziY 260 |
| 370 | 6.4 | Galata Kulesi'nin şerefesi, lodos sabahı | 1 | 2.8 / 8 | 380×230, x 270, taban 632, 10 fps | şerefe döşemesi 600 (uzak kenarda korkuluk); karşı kıyı silüeti su çizgisi 536'ya oturur; Hezarfen 632 | kapalı kanatlar lodosta kıpırdar |
| 371 | 5.6 | şerefeden Boğaz ve Üsküdar | 2 | 2.8 / 8 | 380×230, x 270, taban 632, 10 fps | şerefe döşemesi 606; Hezarfen 632 | kanatlar yarı açık, uçları salınır |
| 372 | 7.8 | köşk odası: IV. Murad ve kese | 3, 4 | 3.0 / 8 | 400×300, x 270, taban 634, 10 fps | iç mekân döşemesi 596; minder ve kese 634; kandil zinciri tavana kadar | kandil ve mumlar titrer |
| 373 | 6.0 | genç IV. Murad atıyla Haliç kıyısında | 5 | 2.6 / 14 | 420×230, x [245, 295], taban 632, 14 fps | kaldırım rıhtım 592; atın toynakları 632; karşı kıyı 536 | beyaz at yürür, sprite sağa kayar |
| 374 | 9.1 | Hezarfen ve kanat sehpası | 6, 7 | 3.2 / 8 | 400×300, x 270, taban 634, 10 fps | iç mekân 634; kanat sehpasının iki ayağı yerde | kandil, mum; Hezarfen nefes alır |
| 375 | 13.4 | Kurtuba: İbn Firnas'ın sert inişi | 8, 9 | 2.8 / 8 | 380×230, x 270, taban 632, 10 fps | orta çayır 560-566, Kurtuba suru düz zemin 588; İbn Firnas diz üstü 632 | dizlerin yanından toz kalkar ve söner |
| 376 | 7.4 | Nişabur: Cevherî cami damında | 10 | 2.8 / 8 | 380×230, x 270, taban 632, 8 fps | toprak dam 600 + 7 px korkuluk; kubbe kasnağı dama (632) oturur; aşağıda şehir damları uzak planda 544+ | Cevherî kolunu kaldırır, indirir |
| 377 | 6.5 | Okmeydanı: taş minbere yürüyüş | 11 | 2.8 / 14 | 400×230, x [240, 290], taban 632, 14 fps | çayır 560-566; taş minber ve ağaç düz zemin 584-588; Hezarfen 632 | Hezarfen sağa yürür (adım), sprite kayar |
| 378 | 6.8 | minberin üstünde kanat açıp kapama (talim) | 12 | 2.8 / 8 | 380×230, x 270, taban 632, 8 fps | minber sahanlığı 604 + 6 px korkuluk; Hezarfen 632; uzakta küçük Galata Kulesi 548'e oturur | kanatlar açılıp kapanır (talim) |
| 379 | 7.4 | Galata Kulesi geniş çekim, lodos | 13 | 2.6 / 8 | 400×230, x 270, taban 632, 10 fps | kaldırım 562; Galata surları 586; kule ve evler 632; şerefe zemini kuleden ölçülür | bacadan duman lodosla sağa yatar; şerefede küçük kanatlı adam |
| 380 | 7.0 | Sarayburnu: Sinan Paşa Köşkü'nün taşlığında padişah | 14 | 2.8 / 8 | 380×230, x 270, taban 632, 8 fps | taş taşlık 598 + korkuluk; padişah minderde 632; karşı kıyıda kule silüeti 536'ya oturur | durgun; padişah sola, Galata'ya bakar |
| 381 | 6.6 | Boğaz üstünde süzülüş (havada olması doğru) | 15 | 2.6 / 14 | 420×230, x [250, 300], taban 650, 10 fps | orta deniz 552'den aşağı; sprite alt 14 satırı aynı renkte su (taban 650); figür havada (yalnız bu sahne), gölgesi silinmiş | süzülme: kanat uçları salınır, gövde hafifçe iner kalkar, sprite sağa kayar; odakY 600, yaziY 230 |
| 382 | 5.5 | Üsküdar, Doğancılar: ayaklar yere değer | 16 | 2.8 / 8 | 380×230, x 270, taban 632, 10 fps | meydan kaldırımı 572; evler ve cami 588; Hezarfen 632 | kanatlar iner kalkar, ayak dibinden toz kalkar |
| 383 | 4.0 | köşk: kese altın | 17 | 2.8 / 8 | 400×300, x 270, taban 634, 8 fps | iç mekân 634 | kandil; Hezarfen'in kolu hafifçe kıpırdar |
| 384 | 8.1 | hüküm: kızıl akşam | 18, 19 | 2.8 / 8 | 400×300, x 270, taban 634, 8 fps | iç mekân 634 (kızıl pencere) | padişahın kolu kalkık, hafifçe salınır |
| 385 | 6.5 | sürgün gemisi batıya | 20 | 2.6 / 14 | 420×230, x [300, 230], taban 632, 10 fps | orta deniz 556; gemi sprite'taki su çizgisine (h-14) oturur | kadırga sola (batıya) yol alır, dalgada iner kalkar |
| 386 | 5.0 | Cezayir gecesi (insan ve mezar yok) | 21 | 2.8 / 8 | 400×230, x 270, taban 632, 6 fps | koyu zemin 566; Cezayir evleri ve cami 632; hilal 524 (yazının altında) | pencerelerde kandil ışığı titrer |
| 387 | 5.5 | gece Galata, şerefe boş | 22 | 2.6 / 8 | 400×230, x 270, taban 632, 8 fps | 379 ile aynı, gece; şerefe boş | pencereler yanık, duman |
| 388 | 5.4 | Kahire: yaşlı Evliya ayakta | 23 | 3.2 / 8 | 400×300, x 270, taban 634, 10 fps | iç mekân 634 | Evliya defteri hafifçe kaldırır; kandil, mum |
| 389 | 13.0 | Evliya rahlede yazar | 24, 25 | 3.0 / 8 | 400×300, x 270, taban 634, 10 fps | iç mekân 634; rahle ve kitaplar yerde | kandil, mum |
| 390 | 6.8 | boş kütüphane | 26 | 2.8 / 8 | 400×300, x 270, taban 634, 8 fps | iç mekân 634; sedir, sandık, rulo mektuplar yerde | kandil titrer |
| 391 | 7.4 | Lagari ve fişeği | 27 | 2.6 / 8 | 400×230, x 270, taban 632, 10 fps | gece taşlık 598 + korkuluk; fişek sehpasının dört ayağı ve Lagari 632 | Lagari'nin kolu kıpırdar |
| 392 | 6.0 | Sarayburnu şenliği, alçak fişekler | 28 | 2.8 / 8 | 400×230, x 270, taban 632, 10 fps | taşlık 586; ışıklı köşk 592; fenerler, fişek sehpası, fişekçi 632 | küçük fişekler sehpadan yükselir, alçakta (yazının altında) patlar, kıvılcımlar düşer |
| 393 | 5.9 | fişek ve barut fıçıları | 29 | 2.8 / 8 | 380×230, x 270, taban 632, 10 fps | taşlık 598; fişek ve fıçılar 632 | fener titrer |
| 394 | 10.3 | Lagari fişeğin tepesinde sesleniyor | 30, 31 | 2.6 / 8 | 400×230, x 270, taban 632, 10 fps | taşlık 586; köşk 592; fişek sehpası 632, Lagari fişeğin oturağında | Lagari kolunu köşke doğru sallar |
| 395 | 3.6 | ateşleme ve kalkış | 32 | 2.6 / 8 | 400×230, x 270, taban 632, 8 fps | 394 ile aynı | fitil, alev, duman (yukarı); fişek Lagari ile yükselip kadrajdan çıkar, sehpada duman kalır (bilinçli olarak yazı bandından 1 sn geçer) |
| 396 | 5.0 | denize iniş, yüzerek dönüş | 33 | 2.8 / 14 | 400×230, x [300, 240], taban 632, 8 fps | orta deniz 552; sprite alt 30 satırı aynı renkte su; Lagari su çizgisinde (gövdesi suda) | kulaç, V izi; sağda düştüğü yerde köpük halkası; sprite sola kayar |
| 397 | 4.5 | kese akçe, sürgün yok | 34 | 2.8 / 8 | 400×300, x 270, taban 634, 8 fps | iç mekân 634 (gece) | ıslak Lagari'den damla düşer; kandil, mum |
| 398 | 5.7 | sipahi Lagari, sürgüne giden Hezarfen | 35 | 2.6 / 8 | 420×230, x 270, taban 632, 12 fps | taşlık 598 + korkuluk; iki figür 632; uzakta gemi su çizgisine oturur | durgun |
| 399 | 6.7 | 2009 deneyi: fişek alçakta parçalanır | 36 | 2.6 / 8 | 420×230, x 270, taban 632, 8 fps | kuru göl zemini 572; sehpa, beton bariyer 632; ekip bir sıra geride 622 | fitil yanar, fişek az kalkar ve alçakta parçalanır; parçalar yere düşer, manken sehpanın dibinde kalır; duman |
| 370 | 3.4 | açılış görüntüsüne dönüş | 37 | 2.8 / 8 | 380×230, x 270, taban 632, 10 fps | 370 ile aynı katmanlar | açılış görüntüsüne dönüş (soru) |
| 400 | 13.8 | 'rivayet' diyen taraf konuşur | 38, 39 | 2.8 / 8 | 400×300, x 270, taban 634, 10 fps | iç mekân 634; sedir ve kitaplar yerde | soldaki konuşur (kitabı kaldırır), mum onun yanında |
| 401 | 13.6 | 'erken havacılık' diyen taraf konuşur | 40, 41 | 2.8 / 8 | 400×300, x 270, taban 634, 10 fps | 400 ile aynı | sağdaki konuşur |
| 402 | 4.1 | terazi: kitap ve kartal tüyü | 42 | 3.0 / 8 | 400×300, x 270, taban 634, 8 fps | iç mekân 634; terazi tabanı yerde, kefeler zincirle asılı | terazi kolu hafifçe salınır, dengede |
| 403 | 6.6 | bugün: Hezarfen Havaalanı, küçük uçak | 43 | 2.6 / 14 | 420×230, x [220, 310], taban 632, 16 fps | çayır + asfalt pist 562; hangar ve rüzgâr tulumu 574-576; uçak tekerlekleri 632 | pervane döner, uçak sağa ilerler |
| 404 | 4.9 | sinema salonu | 44 | 2.8 / 8 | 400×300, x 270, taban 634, 8 fps | iç mekân 634; perde sahnede (618), koltuklar 634 | perde ışığı titrer, perdede kanatlı silüet süzülür |
| 405 | 7.2 | bugün gün batımında Galata Kulesi | 45, 46 | 2.6 / 8 | 400×230, x 270, taban 632, 8 fps | kaldırım 562; bugünkü yapılar 588; kule, evler, sokak lambaları 632 | durgun; lambalar ve pencereler yanık |
| 406 | 4.5 | Üsküdar kıyısı: kese ve uzakta gemi | 47 | 2.8 / 8 | 380×230, x 270, taban 632, 10 fps | rıhtım 600 + korkuluk; Hezarfen ve kese 632; karşı kıyıda kule silüeti ve gemi su çizgisi 536 | kanatlar rüzgârda kıpırdar |

## Kaynak sadakati (görselde ne yok)

- **Kalabalık yok** (KAYNAKSIZ 2): uçuşta, köşkte, şenlikte izleyici kalabalığı çizilmedi; sahnede yalnızca kaynağın andığı kişiler (Hezarfen, padişah, Lagari, Evliya) ve 2009 ekibi var.
- **Cezayir'de mezar ve Hezarfen yok** (KAYNAKSIZ 19): sahne 386 yalnızca gece şehri; "Orada merhum oldu" yazıyla kalır.
- **Cevherî'de kanat yok** (araştırma 7.6, B): damda kollarını açmış adam; İbn Firnas'ta tüylü kanat var (A).
- **Kanat malzemesi:** yalnızca "kartal kanadı" (kahverengi tüy, koyu birincil tüyler); başka malzeme, iskelet, ölçü yok.
- **Kart 36 (kalite notu):** fişek sehpadan yalnızca birkaç piksel kalkar ve **alçakta** parçalanır; yüksekte patlama yok, manken havalanmaz (sehpanın dibine düşer). Fişeğin kol sayısı vurgulanmaz: bütün fişeklerde yalnızca gövde ve yanlarda iki kol görünür.
- **Kart 13-16 coğrafyası:** kule Galata'da (379), padişah Haliç'in öbür yakasında taşlıktan Galata silüetine bakar (380), süzülüş Boğaz üstünde (381), iniş Doğancılar meydanında ayaklar yerde (382). Kart 33: Lagari denize iner, kıyıya yüzer (396). Kart 23-26: Kahire'de yaşlı Evliya, rahle ve kandil (388-389).
- Sinan Paşa Köşkü'nün mimarisi bilinmediği için sade, genel bir Osmanlı sahil köşkü çizildi (adı yazıda yalnızca "Sinan Paşa Köşkü").

## Yeni figürler (hezarfen.py içinde; ciz.py'ye eklenmedi)

Hepsi yalnızca `piksel()`, `hex2()`, `ImageDraw` ve mevcut figürlerle yazıldı; yapılar `duz_zemin` ile düz zemin denetiminden geçer.

| Figür | Boy (ölçek s ile) | Zemine nasıl basar | Sahneler |
|---|---|---|---|
| `kanat` / `kanatli` (kartal kanatlı adam) | kisi + iki kanat (kanat 7,6-12,5·s) | kisi'nin ayakları; kapalı kanatlar omzun üstünden bedenin iki yanına iner, yere değmez. `havada=True` yalnız 381'de (temas gölgesi silinir) | 370, 371, 375, 377, 378, 379, 381, 382, 398, 406 |
| `galata_kulesi` | 42·s (s 2,8 → 118 px) | kaide düz zemine; şerefe y'si döndürülür, küçük adam ona basar | 379, 387, 405 |
| `tas_minber` | 9·s sahanlık + merdiven | taş kürsü ve merdiven düz zemine | 377 |
| `kubbeli_cami`, `siluet` | 26·s (minare dahil) / uzak silüet ≤20 px | düz zemin / kıyı çizgisi | 382, 386; bütün deniz sahneleri |
| `ev` (cumbalı İstanbul evi), `kosk` (sahil köşkü) | 13·s / 23·s | düz zemin | 379, 382, 387, 405 / 392, 394, 395 |
| `kese`, `fici` | 6·s / 7·s | gövde yere oturur, sikkeler yerde | 372, 383, 384, 397, 406 / 393 |
| `fisek`, `fisek_sehpa` | 23·s | dört sehpa ayağı zeminde; Lagari oturağa oturur | 391, 393, 394, 395, 399 |
| `yuzen` | baş + omuz | su çizgisinin altı çizilmez | 396 |
| `terazi` | 16·s | taban yerde, kefeler zincirle asılı | 402 |
| `ucak`, `hangar`, `ruzgar_tulumu` | 9·s yükseklik / 16·s / 12·s | tekerlekler pistte / düz zemin / direk zeminde | 403 |
| `perde`, `koltuk_sirasi` | 22·s / 6,6·s | iki ayak sahnede / arkalıklar yerde | 404 |
| `manken`, `beton_set`, `rampa` | 12·s / 5·s | oturağa ya da yere değer | 399 (rampa kullanılmadı, fişek sehpası tercih edildi) |
| `fener` | 13·s | direk zeminde | 391-395 |
| `_kanat_sehpasi`, `_cezayir_evleri`, `_toz`, `_hilal`, `_su_bandi` | yardımcılar | sehpa ayakları yerde; Cezayir evleri düz zeminde; toz yerden kalkar; su bandı orta plandaki denizle aynı renk | 374, 386, 375/382, 386, 381/385/396 |

Katman yardımcıları (yeni): `_uzak_deniz` (karşı kıyı tepeleri + kıyıya oturan silüet + titreşimli deniz, dikişsiz), `_uzak_kara` (tepeler + silüet + ova; 376'da aşağıda kalan şehrin damları), `_orta_duz` (taş döşeme, kaldırım, toprak dam, pist; uzak kenarda alçak korkuluk), `_orta_deniz`, `_on_bos`.

## Grafiker öz denetimi

**Otomatik denetimler (her sahne, her çizimde):**
- `taban_denetimi` (kütüphane): 37 sprite'ın 24 karesinin hepsinde en alt opak piksel son satırda. Havada tek nesne yok; süzülme sahnesi 381'de figür havada ama sprite tabanı orta plandaki denizle aynı renkte bir su bandı.
- `_kadraj` (Cem kalıbının geliştirilmiş hâli): sahne sonundaki %6 yakınlaşma dahil (yakin×1,06), yakınlaşmanın odağı sprite'ın x'i olduğundan görünen aralık **asimetrik** hesaplanır (`[w/2 − sx/yakin, w/2 + (540 − sx)/yakin]`) ve kayan sprite'larda baş ve son x'in ikisi de denetlenir. Kesik baş yok.
- **Yazı bandı denetimi (yeni):** 3 satırlık kartın alt kenarının dünya y'si (odakY ve yaziY dahil) hesaplanır; görünür aralıkta bu çizginin üstüne çıkan opak piksel varsa betik durur. Tek bilinçli istisna: 395'te fişeğin kadrajdan çıkışı (≈1 sn hareket). Tavandan sarkan kandiller yazı bandı denetiminde sayılmaz (zincir tavana kadar kuralı).
- `olcek`/`s_kisi`/`s_oturan` (Cem kalıbı): figürler kadraj yüksekliğinin %30-32'si (yakin 2.8'de 110 px). Atlı (373) at+binici %33, insan/at oranı at 2.9 ↔ kisi 2.6 kuralına göre.

**Gözle baktıklarım:** Önizleme betiği (TSX dönüşümünü taklit eder, yazı bandını kırmızı kutuyla işaretler) ile 37 sahnenin hepsini en az bir karede, yeniden çizdiklerimi ikinci bir karede (k6-k18) açıp baktım; ayrıca 9 sahnenin sprite PNG'sini (370, 375, 381, 382, 383, 392, 395, 396, 399) 0/8/16. karelerden kesip açtım. Bakılanlar: zemin, ölçek, kesilme, havada nesne, kontur, yazıyla çakışma.

**Bulup düzelttiklerim:**
1. Kapalı kanatlar bacaklarda "etek" gibi duruyordu ve uçları zeminin altına iniyordu → kanat kökü omzun üstüne alındı, boy kısaltıldı; artık sırtta kanat olarak okunuyor, yere değmiyor.
2. 381 ve 385'te sprite'ın su bandı orta plandaki denizden açık renkte, yoğun parıltılı bir şerit gibi görünüyordu → `_su_bandi`: her satır orta planın aynı satırının rengiyle, dikiş yok.
3. 381'de baş yazı bandına giriyordu (ilk denetim 52 px yakaladı) → odakY 600, yaziY 230; açık kanat uçları ekran kenarında kesiliyordu → ölçek %28, kayma [250, 300].
4. Görünür aralık hesabı simetrik varsayıyordu (sx 270 dışında yanlış) → asimetrik hesap; bütün kayan sahneler yeniden denetlendi.
5. 373 atlının sarığı yazı bandındaydı → yakin 2.6, at s 3.9.
6. 379/387/405'te evler kuleye göre çok büyüktü → ev ölçeği yarıya indi (kule 67 m, ev iki kat).
7. 380, 378, 406'da karşı kıyıdaki kule silüetinin tepesi yazı bandının alt kenarına değiyordu → silüet 31 px'ten 20 px'e.
8. 392'de meşalenin alevi yazı bandındaydı → fişekçi kolu aşağıda, ölçek %95; patlamalar çok küçük ve kadraj dışındaydı → sehpa ve patlamalar merkeze, kıvılcımlar büyüdü, yerçekimiyle düşüyor.
9. 394/395'te Lagari ince bir çubuğun üstünde dengede gibi duruyordu → fişek gövdesi 1,6 kat kalınlaştı, oturak genişledi.
10. 396'da yüzen adam yalnız yuvarlak bir baştı → omuzlar, sırayla suya giren iki kol, V izi ve köpük eklendi; düşüş halkası görünür aralığa alındı.
11. 375'te Kurtuba Avrupa şatosu gibiydi → kerpiç sur, kubbeli Orta Asya/Endülüs şehri.
12. 376'da dam bir çayır gibi okunuyordu → uzak planda, korkuluğun ötesinde aşağıda kalan şehrin damları (perspektifli sıralar).
13. İç mekân pencerelerinde krem renkli "kar yığını" görünüyordu (Kahire, köşk) → pencere ikinci rengi koyu tona çekildi.
14. 380'de padişahın yanındaki hizmetli ikiz gibi duruyordu ve kalabalık izlenimi riski vardı → çıkarıldı; 386, 390, 391, 398, 399, 403'te kadraj dışında kalan nesneler (evler, mektuplar, fener, gemi, ekip, rüzgâr tulumu) görünür aralığa alındı.
15. 400/401 birbirinin aynısıydı → konuşan kitabı yükseğe kaldırır, dinleyen kâğıdı belde tutar, mum konuşanın yanında.

**Bilinçli kararlar (kalite kontrol için not):**
- 379, 387, 405 (kule geniş çekim): ana figür kule (%32); şerefedeki kanatlı adam ölçek gereği küçüktür (67 m'lik kulede insan).
- 396 (yüzme): suda yalnız baş ve omuzlar görünür; %30 kuralı yüzen figüre uygulanamaz, ölçek diğer sahnelerin 1,3 katı.
- 403 (uçak): yatay bir araç; boyu kadrajın ~%15'i, eni görünür alanın ~%90'ı.
- 385, 386, 390, 402, 404: insansız sahneler (gemi, şehir, kütüphane, terazi, sinema), Cem Sultan'daki boş oda (102) gibi.
- Gök ve uzak plan motorun sabit kaymasıyla sola akar; lodosun yönü (sağa) duman, kanat ve süzülüşle verilir.
- Seslendirme yaklaşık 4 dakika; kısaltma yapılmadı (sahibin kararı).

**Son durum:** `python3 -I video/piksel/hezarfen.py` 37 sahneyi hatasız çiziyor (fizik, kadraj ve yazı bandı denetimleri geçti). `cd video && npx tsc --noEmit -p .` temiz (çıkış 0). Kart metinleri 4-kalite-metin.md ile 47/47 aynı.
