# Küçük Konstantinopolis: grafik teslimi (toulon-1543)

**İş:** Barbaros'un donanması Toulon'da kışlıyor (1543-44) · **Hazırlayan:** 🟢 SKONSTART Grafiker · **Girdi:** 4-kalite-metin.md (nihai seslendirme metni ve 52 ekran kartı, grafiker notları)

**Dosyalar**
- Çizim: `video/piksel/toulon_1543.py`, sahneler **450-486** (37 sahne; 487-489 kullanılmadı). Çalıştırma: `python3 -I video/piksel/toulon_1543.py [no ...]`. Çıktılar `video/public/sahne450-*.png` … `sahne486-*.png` (gokyuzu, uzak, orta, on, karakter).
- Video: `video/src/sahneler/Toulon1543.tsx`. Dışa aktarılanlar: `TOULON_SERI`, `TOULON_KARE`, `Toulon1543`. Etiket "PİKSEL TARİHİM · BARBAROS TOULON'DA", ses `toulon-1543-anlatim.mp3`. `Root.tsx`'e dokunulmadı (kayıt kod tarafında).
- Kapak (2 sn) + 37 anlatım bölümü + kapanış (3 sn, arka 486, gece). Kart süreleri metin uzunluğuna göre orantılı yazıldı; anlatım toplamı 255,0 sn (seslendirme 255 sn). `ses/hizala_seri.py` sese göre yeniden yazar.
- Kartlar 4-kalite-metin.md'den **betikle** alındı: 52 kart, her satır ≤30 harf, birleşimleri seslendirme metniyle karakter karakter aynı (betik doğruladı). Python çizimi yakin/kamera/sprite/kart ayarlarını TSX'ten okur; tek kaynak TSX.
- Kapak: "Barbaros / Toulon'da / Küçük Konstantinopolis" (3 satır, boy 112, ALTIN, yaziY 270). Başlık brifteki gibi "Barbaros Toulon'da"; alt başlık olarak metnin kendi motifi ve kalite kontrolün başlığı "Küçük Konstantinopolis" seçildi (yazarın kapak notundaki "Bir kral şehrini Barbaros'a verdi" 3 satıra sığmıyordu).

## Kurgu ve yön dili

Yön dili: **sağ** = batıya, Fransa'ya gelen donanma; **sol** = eve (doğuya) dönüş, geride kalan ve şehri terk eden. Barbaros'un kadırgası Toulon'a sağa girer (450, 452, 466), Nice'ten (460), Provence'tan (476) ve İstanbul'a (484) sola gider. Toulon'dan çıkan kadınlar ve çocuklar sola yürür (464).

Işık hikâyeyi taşır: altın saat (kapak, Küçük Konstantinopolis), Nice'te turuncu duman ve kızıl yangın, boşaltmada kurşuni akşam, boş sokakta mavi gece (motif kart 22), kışın kurşuni gündüz ve mum ışıklı katedral, ilkbaharda parlak sabah, Lipari'de kızıl yangın ve mor sessizlik (motif kart 47), kapanışta yıldızlı Toulon gecesi.

Kişiler bütün videoda aynı renkte; iki farklı kişi aynı çizilmedi:
- **Barbaros:** kızıl kaftan, lacivert pelerin, büyük beyaz kavuk, **kızıl sakal** (lakabının görsel karşılığı). 451, 455, 459, 475.
- **I. François:** mavi kaftan, kızıl pelerin, **altın taç**, kahverengi sakal (453).
- **Kaptan Polin:** mor kaftan, siyah şapka (455). **Münadi:** mavi, sarı şapka (462). **Kraliyet memuru:** mavi, altın pelerin (474, 475).
- **Levendler:** kızıl yelekli sarıklı / mavi ak börklü / zeytin yeşili genç; Barbaros'tan ayrılsın diye pelerinsiz ve daha küçük kavuklu.
- **Toulonlular:** takkeli, kahverengi ve yeşil giysili; kadınlar başörtülü (göz açık); çocuklar saçlı, %62 ölçekte.
- **Rahipler iki ayrı kişi:** katedral rahibi siyah cüppe + takke; vaftizde beyaz surplis ve mor stol (471-472). **Jérôme Maurand:** siyah cüppe ve geniş kenarlı yolcu şapkası (477).
- **19. yüzyıl tarihçisi:** redingot, açık baş, kır favori (470).

Kaynak sadakati (görselde ne yok): kart 27'de cami görseli yok, yalnızca katedral cephesi (469); katedral sahneleri vaftizdir (471-472). Kral ile Barbaros hiçbir karede yan yana değil (KAYNAKSIZ: görüşme). Nice'te ve Lipari'de şiddet gösterilmez: yanan çatılar uzaktan, esirler kıyıda sıra hâlinde bekler, kimse silah kaldırmaz. Matrakçı minyatürü temsilîdir (üslup taklidi, kopya değil).

## Sahne planı

Zemin: dış mekânda sprite tabanı 632, iç mekânda ve kuşbakışı masada 634 (son satır; `taban_denetimi` her karede doğrular). Deniz sahnelerinde gövdenin altı sprite'ın kendi su bandında (orta plandaki denizle aynı renk) kalır.

| No | Süre (sn, tahmini) | Konu | Zemin çizgileri | yakin / kamera | Hareket | Kartlar |
|---|---|---|---|---|---|---|
| 450 | 7.7 (+2 kapak) | Toulon koyu, 1543 sonbaharı: Barbaros'un kadırgası kürek çekerek koya girer; arkada kasaba ve Faron | Deniz sprite'ı: kadırga su çizgisi 618 (gövde altı suda). Uzak: kıyı şeridi 534-542, evler 540'a oturur; deniz 542↓; orta deniz 556↓ | 2.6 / 6 | sprite kayar [262, 278] | 1, 2 |
| 451 | 3.1 | Barbaros kadırgasının güvertesinde; uzakta donanma | Güverte: küpeşte 572, güverte 600; figürler 632 | 2.8 / 6 | sabit | 3 |
| 452 | 4.3 | açık deniz: uzun kadırga tek sıra kürekle sağa yol alır, arkada başka kadırgalar | Kadırga su çizgisi 618; orta plandaki iki uzak kadırga 563/566 | 2.6 / 8 | sprite kayar [262, 278] | 4 |
| 453 | 10.5 | Fontainebleau tarzı salon: taçlı I. François tahtının önünde | İç mekân 634; taht bir sıra geride (622) | 2.8 / 6 | sabit | 5, 6 |
| 454 | 6.0 | alacakaranlık: Osmanlı ve Fransız kadırgası yan yana | Uzak Fransız kadırgası 586, yakın Osmanlı 620 (her gövdenin altı kendi su bandında) | 2.6 / 8 | sprite kayar [262, 278] | 7 (ALTIN) |
| 455 | 11.0 | Marsilya rıhtımı, 1543 yazı: Barbaros ve Kaptan Polin; karşı kıyıda Marsilya surları | Rıhtım 600; figürler 632; Marsilya surları uzak kıyı şeridinde 544 | 2.8 / 6 | sabit | 8, 9 |
| 456 | 5.5 | Nice kuşatması: tepedeki kale, aşağı şehir; koyda kadırgalar, önde Fransız piyadesi | Figürler 632; kaya tabanı 592 (düz), kale kayanın düz tepesinde 552; aşağı şehir 594; kadırgalar uzak denizde 548 | 2.6 / 8 | sprite kayar [262, 278] | 10 |
| 457 | 6.0 | aşağı şehir yanar, tepedeki kale direnir (sancak dalgalanır) | Kaya 592/552, evler 594; alevler çatı hattına (571) oturur; ön planda taş duvar 632 | 2.6 / 6 | sabit | 11 (KIZIL) |
| 458 | 5.3 | Savoy ve del Vasto'nun zırhlı atlıları sola gelir, toz kalkar | Atlılar 632 ve 624 (arka); toz toynaktan kalkar | 2.6 / 10 | sprite kayar [278, 262] | 12 |
| 459 | 6.5 | sahildeki ordugâh: Barbaros ufku gösterir, çadırlar toplanır; ufukta Doria'nın yelkenleri | Kum 562↓; figür ve çuvallar 632; otağ 586; Doria'nın yelkenleri ufukta 536 | 2.8 / 6 | sabit | 13 (KIZIL) |
| 460 | 6.3 | alacakaranlık: Barbaros'un kadırgası sola, denize açılır | Kadırga su çizgisi 618 | 2.6 / 8 | sprite kayar [278, 262] | 14 |
| 461 | 10.3 | Toulon, sonbahar sabahı: Provence evleri, katedral, arkada Faron; rıhtımda boş kayıklar | Kara şeridi 556-596, evler ve katedral 592; deniz 596↓; kayıklar 618/622 | 2.6 / 8 | sabit | 15, 16 |
| 462 | 7.9 | meydanda münadi açık mektubu okur; dinleyen halk | Meydan 588↓ (taş döşeme), evler 590; figürler 632 | 2.8 / 6 | sabit | 17, 18 (KIZIL) |
| 463 | 11.8 | şehir meclisi: konsüller ve tutanağı yazan kâtip | İç mekân 634; kürsü ayağı 634 | 2.8 / 6 | sabit | 19, 20 |
| 464 | 4.9 | çocuklar ve kadınlar yola düşer (sola); kapıda kalan erkek | Yürüyenler 632; kapıdaki adam ve surlar orta planda 588-592 | 2.8 / 8 | sprite kayar [278, 262] | 21 (KIZIL) |
| 465 | 4.2 | boş sokak, mavi alacakaranlık; kapısında tek başına bir adam | Meydan 588; kuyu, fener ve adam 632 | 2.8 / 6 | sabit | 22 (ALTIN) |
| 466 | 4.8 | sabah pusu: kadırgalar sıra hâlinde koya girer | Uzak kadırga 586, yakın 620 (her gövdenin altı kendi su bandında) | 2.6 / 8 | sprite kayar [262, 278] | 23 |
| 467 | 6.1 | rıhtımda sarıklı levendler ve onlara bakan Fransız tanık | Rıhtım 600; figürler ve fıçı 632; Toulon uzak kıyıda 544 | 2.8 / 6 | sabit | 24 |
| 468 | 4.3 | gün batımı: koy kadırgalarla dolu; Küçük Konstantinopolis | Orta planda üç sıra demirli kadırga 562/571/582; yakın kadırga 618 | 2.6 / 10 | sabit | 25 (ALTIN) |
| 469 | 7.7 | kış gecesi: katedralin cephesi, kapı fenerinin ışığı | Meydan 588; katedral ve fener 632 | 2.8 / 6 | sabit | 26, 27 |
| 470 | 5.5 | 19. yüzyıl: Toulonlu tarihçi kitaplarının başında | İç mekân 634; kitaplar zeminde | 2.8 / 6 | sabit | 28 (KIZIL) |
| 471 | 4.3 | katedral içi: rahip vaftiz defterine yazar | İç mekân 634; kürsü ve şamdanlar 634 | 2.8 / 6 | sabit | 29 |
| 472 | 6.0 | vaftiz: rahip bebeği kurnanın üstünde tutar, anne ve baba yanında | İç mekân 634; kurna, aile, rahip 634 | 2.8 / 6 | sabit | 30 (ALTIN) |
| 473 | 7.8 | kış sabahı pazar: Provenceli ekmekçi ve sarıklı levend | Meydan 588; tezgâh ve figürler 632; ekmekçi tezgâhın arkasında 622 | 2.8 / 6 | sabit | 31, 32 |
| 474 | 6.3 | kış: kraliyet memuru vergi muafiyetini okur; halk sevinir | Meydan 588; figürler 632 | 2.8 / 6 | sabit | 33 |
| 475 | 9.1 | rıhtım: altın sandığı, ipek, erzak, barut fıçıları; Fransız memur ve Barbaros | Rıhtım 600; sandık, ipek, çuval ve figürler 632 | 2.8 / 6 | sabit | 34, 35 (ALTIN) |
| 476 | 4.4 | Mayıs 1544 sabahı: yelkenler açık, kadırga sola (eve) yol alır | Kadırga su çizgisi 618; orta plandaki kadırgalar 568-580 | 2.6 / 8 | sprite kayar [278, 262] | 36 |
| 477 | 9.6 | Fransız kadırgasının güvertesi: rahip Maurand defterine çizer; kıyı geride kalır | Güverte 600; figür ve fıçı 632 | 2.8 / 6 | sabit | 37, 38 |
| 478 | 9.4 | kuşbakışı masa: portolan harita, rota noktaları ilerler; dört yer işaretlenir | Kuşbakışı masa; harita alt kenarı sprite'ın son satırı | 2.6 / 0 | sabit | 39 (KIZIL), 40 |
| 479 | 5.1 | Lipari: düz tepeli kayada surlu katedral kenti; ufukta Vulcano | Kaya tabanı 594, düz tepe 556 (kale ve katedral tepede); evler 596; zeytin ve duvar 632 | 2.6 / 8 | sabit | 41 |
| 480 | 4.1 | Lipari yanar; esirler kıyıda sıra hâlinde bekler (uzaktan, şiddetsiz) | Kaya 594/556; alevler surun üstünde (545); esirler 616 (arka sıra), duvar 632 | 2.6 / 6 | sabit | 42 (KIZIL) |
| 481 | 10.0 | kuşbakışı masa: iki kronik ve bir not kâğıdı; üç farklı sayı | Kuşbakışı masa; not kâğıdı alt kenarı son satır | 2.6 / 0 | sabit | 43, 44 |
| 482 | 8.0 | yanmış arşiv odası: kömürleşmiş raf, yerde için için yanan kâğıtlar | İç mekân 634; raf ve kâğıtlar zeminde | 2.8 / 4 | sabit | 45 (KIZIL), 46 |
| 483 | 4.4 | Lipari, sessiz alacakaranlık: kaledeki ince duman | 479'un zemini; ince duman kaleden | 2.6 / 6 | sabit | 47 (ALTIN) |
| 484 | 5.7 | Ağustos 1544: İstanbul silüeti, kadırga eve döner | Kadırga su çizgisi 618; İstanbul uzak kıyı şeridinde 542 | 2.6 / 8 | sprite kayar [278, 262] | 48 |
| 485 | 6.2 | kuşbakışı: Matrakçı Nasuh'un Toulon minyatürü açık yazmada | Kuşbakışı masa; yazma alt kenarı son satır | 2.6 / 0 | sabit | 49 |
| 486 | 14.8 | Toulon gecesi: rıhtımda kalan bir Toulonlu, koyda fenerli kadırgalar | Rıhtım 600; adam ve fener 632; kadırgalar orta planda 568 (rıhtımdan 32 px su ile ayrı) | 2.8 / 6 | sabit | 50 (ALTIN), 51 (ALTIN), 52 (ALTIN) |
Kamera notu: kuşbakışı masa sahnelerinde (478, 481, 485) `odakY: 560`, kamera 0; kâğıtlar yazı bandının altında ve görünür aralığın içinde.

## Yeni figürler (toulon_1543.py içinde; ciz.py'ye eklenmedi)

- **kadirga** (`kadirga(t, x, su_y, s, yon, faz, mod, fener, kurek, isik…)`): 16. yy kadırgası, rapordaki ölçüyle. Boy (mahmuz dahil) 100·s; alçak gövde (su üstü ~5·s), tek sıra 24 kürek, vuruş döngüsü (kürek suda geriye çekilir, havada öne gelir; dikişsiz). Kürekçi başları insan ölçeğinde (boy/25). Kıçta kemerli tente, fenerler (Barbaros'un gemisinde üç), iki direk, latin sereni (`acik`: üçgen latin yelken; `sarili`: serene sarılı; `indik`: limanda indirilmiş), pruvada mahmuz ve top, direk başında rüzgârla geriye akan flama. Gövde su çizgisine oturur, altı suyun içinde kalır. Osmanlı: koyu gövde, kızıl kuşak ve tente; Fransız: lacivert kuşak ve tente. **Ölçek kuralı:** kadırga hiçbir karede insanla aynı derinlikte durmaz. Yakın kadırga sahnelerinde insan yok (yalnızca kürekçi başları); insanlı sahnelerde kadırgalar ya güverte (451, 477) ya da rıhtımdan su ile ayrılmış uzak plan (486).
- **provence_evleri**: bitişik 2-3 katlı sıvalı evler, alçak kiremit çatı, panjurlu pencereler (kapalı / lamba ışıklı), kemerli kapılar; düz zemine kurulur.
- **katedral**: Romanesk kilise cephesi (üçgen alınlık, kemerli kapı, gül pencere, yan nef, kare çan kulesi). Toulon katedrali için temsilî; bugünkü 17. yy cephesi ve 18. yy kulesi çizilmedi.
- **kaya_tepe**: düz tepeli kaya (Nice'in kale tepesi, Lipari akropolü). Kale ve katedral yalnızca düz tepeye kurulur.
- **yangin**: çatıya oturan titreşen alev ve kıvılcım.
- **basortulu, cocuk, bohca, rahip, avrupali, kundak**: başörtülü kadın (göz açık), saçlı çocuk, sırt bohçası, surplisli/şapkalı rahip, 19. yy bilgini, kundaklı bebek.
- **vaftiz_kurnasi, kilise_kursusu, altin_sandigi, ipek_toplari, cuval, fici, tezgah, kuyu, sokak_feneri, tas_duvar, kayik**: hepsi zemine oturur (temas gölgeli).
- **harita, kronik, minyatur**: kuşbakışı masa kâğıtları. Harita: Provence, Korsika, Sardunya, İtalya, Sicilya; rota noktaları ilerler, Talamone, Porto Ercole, Giglio, Ischia ve Lipari'de alev işareti yanar. Kronikler: "8000" ve "11000", not kâğıdı "4000" (3x5 piksel rakam). Minyatür: sol sayfada satırlar, sağ sayfada altın çerçeveli Toulon (koyda sıra sıra kadırga, surlu kent, tepeler).

## Grafiker öz denetimi

**Otomatik denetimler (betik bunlar geçmeden sprite yazmaz):**
1. *Taban:* her sprite karesinde en alt opak piksel son satırda (`taban_denetimi`).
2. *Kenar/kadraj:* opak piksellerin en az %99,5'i (yangınlı 457, 480, 483'te %97) görünür aralıkta; bütün sx'lerde, hem yakin hem sahne sonundaki 1,06·yakin ile, kamera kayması payı düşülerek. Sprite'ın üst kenarına değen kare yok.
3. *Yazı bandı:* her kartın (kapak dahil) ekran satırları dünya y'sine çevrildi; sprite'ta ve orta planda bu satırlarda (bütün sx ve iki yakınlaşmada) opak piksel yok. Duman boyları bu sınıra göre kısaltılır (`_ust_sinir`). Kuşbakışı masa sahnelerinde orta plan masanın kendisi olduğu için yalnız sprite denetlendi.
4. *Orta plan nesneleri:* Nice kalesi, Lipari kalesi ve otağ için `_gorunur` (kenarda kesilmez).
5. Bulutlar gokyuzu() denetiminden geçti; güneş/ay yok (yazıyla çakışma riski).

**Gözle baktıklarım** (her sahnenin ilk ve son karesini kamera yakınlığında birleştiren önizleme, yazı bandı çerçevesiyle; 37 sahnenin hepsi): zemine oturma, ölçek, kesilme, havada nesne, kontur, gemi-insan ilişkisi.

**Düzelttiklerim:**
- İlk çizimde 19 sahne kenar denetiminden kaldı. 2,8 yakınlıkta ve %6 yaklaşmayla görünür aralık yalnızca 176 px. Bu yüzden figürler içeri çekildi, 467'de ve 475'te bir nesne çıkarıldı, 472'de şamdan kaldırıldı.
- Kürekler gövdenin dibinde kayboluyordu. Daha uzun ve iki tonlu çizildiler, vuruş daha geniş yapıldı.
- Nice piyadesinin mızrakları dikey olsa yazı bandına girecekti. Omuzda eğik taşınıyorlar (`mizrak_omuz`); uzunluk, sağ kenara taşmayacak biçimde kısaltıldı.
- 457'de yangın noktaları görünür aralığın dışında kalıyordu. Alevler görünen çatılara alındı, Savoy sancağı kalede kaldı.
- 454 ve 466'da uzaktaki kadırga, yakın geminin su bandının altında kalıyordu. Artık her geminin altı kendi su bandında; 466'da üç gemi yerine iki gemi var, böylece birbirine karışmıyorlar.
- 459'da Doria'nın yelkenleri levendin başına değiyordu ("gemiye değen figür" riski). Levend çıkarıldı. Yelkenler ufukta, Barbaros'un gösterdiği boş yere alındı; otağ figürlerle çakışmayacak yere taşındı.
- 486'da Toulonlunun eli orta plandaki kadırgaya değiyordu. Kadırgalar küçültüldü ve sağa alındı (rıhtım kenarıyla aralarında 32 px su var). Adam ve fener sola alındı.
- 464'te bohçalar kalkan gibi görünüyordu. Küçük, bağlı bohça çizildi. Kapıda kalan adam yürüyenlerin arasından surun önüne alındı.
- 461'de kayıklar su bandının altında kalıyordu; çizim sırası düzeltildi. Lipari'de (479, 480, 483) katedral kulesi surların arkasında kayboluyordu; kule büyütüldü, sur alçaltıldı.
- 453 ve 463'te pencerelerde kar vardı, oysa sahneler kış öncesi. Kar kaldırıldı (cama soluk ışık noktaları kondu).

**Bilinen sınırlar (kalite kontrolün dikkatine):**
- Uzak katman motor gereği sahne boyunca yavaşça sola kayar. Bu yüzden uzak plandaki küçük kadırgalar (456, 459) birkaç piksel yer değiştirir; hiçbiri figürlerle çakışmaz.
- Matrakçı minyatürü temsilîdir; gerçek minyatürün kopyası değildir.
- Remotion render'ı alınmadı (`Root.tsx`'e kayıt kod tarafında). Önizlemeler Python birleşimiyle yapıldı. `npx tsc --noEmit -p .` temiz geçti.

## Görsel KK revizyonu (6-kalite-gorsel.md'deki 6 zorunlu düzeltme ve öneriler)

`Toulon1543.tsx`'e dokunulmadı (sese hizalı). Yalnızca `toulon_1543.py` ve sprite'lar değişti. Bütün sahneler yeniden çizildi: kenar, yazı bandı ve taban denetimleri geçti, `tsc` temiz. Değişen 13 sahnenin önizlemesine tek tek baktım.

| # | Sahne | Düzeltme |
|---|---|---|
| 1 | 458 | Atlılara yeni figür `zirhli_atli`: yüzü açık 16. yy morion miğfer (yuvarlak kubbe, sırt, iki ucu kalkık siperlik). Göz 2×2 piksel ve net, sakal açıkta. İki atlı birbirinden ayrılıyor: öndeki açık gri miğferli, beyaz tüylü; arkadaki koyu miğferli, mavi tüylü. Sivri miğfer kaldırıldı. |
| 2 | 464 | Surlar uzak plana alındı (orta planın uzak kenarı, 556). Kapıda kalan adam da aynı derinlikte ve surla aynı ölçekte (s 1,0): kapı adamın yaklaşık iki katı, kuleler daha da yüksek. Sur kadrajın içinde bitiyor (`_gorunur`). Yürüyenler 4 kişi (2 kadın, 2 çocuk); adamla üst üste binmiyorlar. |
| 3 | 479, 480, 483 | Zeytin ağacı çıkarıldı. Ağacı insandan uzun çizmek yazı bandına giriyordu. Yerine ön planda alçak çalılar var (yeni figür `cali`); bir çalının insandan kısa olması doğal. |
| 4 | 479, 480, 483 | Lipari yeniden kuruldu. Kale kayası koyun karşı kıyısında duruyor; yakın kıyı ile kaya arasında su şeridi var, karşı kıyı pusla soluklaştırıldı. Böylece kale ve evlerin küçüklüğü uzaklık olarak okunuyor. Kenara dayanan ev dizisi kaldırıldı; kayanın dibindeki iki küçük ev kümesi kadrajın içinde bitiyor (`_gorunur`). Kaya, katedral kulesi yazı bandının altında kalacak kadar alçaltıldı. |
| 5 | 481 | Rakam yerleşimi sayfa içine sabitlendi: cilt çizgisinden en az 2 px uzakta. Sayfaya sığmazsa betik durur (`assert`). "11000" tamamen sağ sayfada. |
| 6 | 486 | Tek kadırga kaldı, ölçeği büyütüldü (s 0,45 → 0,8). Gövde kıyıdaki 5 ev genişliğinde, direk ev boyunun yaklaşık iki katı. Kadırga kadrajın içinde (`_gorunur`). Rıhtımla arasında su bandı korundu; adamla arası açık. |

**İyileştirmeler**
- **480:** Levend artık ön planda, esirlerden ayrı duruyor. Elinde (kaldırılmamış) değnek var, yüzü esirlere dönük; bekçi olduğu okunuyor.
- **465, 469, 486:** Direkteki sokak fenerleri kaldırıldı. 465 ve 486'da adam elinde fener taşıyor (`el_feneri`). 469'da fener katedral duvarındaki demir kolda asılı (`duvar_feneri`).
- **472:** Rahibe dört köşeli biret verildi (471'de de); babanın başında kırmızı keçe kalpak var.
- **468:** Kadırga sıraları seyreltildi, aralarına su bırakıldı (3 sıra: 40/54/74 px aralık). Kaynağı belirsiz duman sütunu kaldırıldı.
- **478, 485:** Kâğıtlar 24 px aşağı alındı; böylece üstteki koyulaşma bandının altında kalıyorlar.
