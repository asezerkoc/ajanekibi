# Paris'teki Elçi: grafik teslimi

**İş:** Yirmisekiz Çelebi Mehmed Efendi'nin Paris sefareti (1720-21) · **Hazırlayan:** 🟢 SKONSTART Grafiker · **Girdi:** 4-kalite-metin.md (nihai seslendirme metni ve 45 ekran kartı)

**Dosyalar**
- Çizim: `video/piksel/celebi_mehmed_paris.py`, sahneler **290-321** (32 sahne; 322-329 kullanılmadı). Çalıştırma: `python3 -I video/piksel/celebi_mehmed_paris.py [no ...]`. Çıktılar `video/public/sahne290-*.png` … `sahne321-*.png` altında (gokyuzu, uzak, orta, on, karakter).
- Video: `video/src/sahneler/CelebiMehmed.tsx`. Dışa aktarılanlar: `CELEBI_MEHMED_SERI`, `CELEBI_MEHMED_KARE`, `CelebiMehmed`. Etiket "PİKSEL TARİHİM · ÇELEBİ MEHMED", ses `celebi-mehmed-paris-anlatim.mp3`. `Root.tsx`'e dokunulmadı (kayıt kod tarafında).
- Kapak + 33 anlatım bölümü + kapanış. Tahmini süre 2,5 sn kapak + 257,5 sn anlatım + 3 sn kapanış ≈ 4:23. Seslendirme 241 sn; kart süreleri metin uzunluğuna göre orantılı yazıldı, `ses/hizala_seri.py` sese göre yeniden yazacak.
- Kart metinleri kalite kontrolün nihai listesinden **betikle** alındı. Betik 45 kartı, her satırın en çok 30 harf olduğunu ve kartların birleşiminin seslendirme metniyle karakter karakter aynı olduğunu doğruladı. Parantez içindeki ipuçları ekrana yazılmadı.

## Kurgu ve yön dili

Hikâye beş durakta ilerliyor. Toulon'da karantina (gri, kurşuni ışık), İstanbul'da görev (yeşil ve altın saray odaları), Paris (bahar mavisi, alacakaranlık saray, gece rasathane), İstanbul'da Lale Devri (yeşil mesire, aydınlık atölye) ve 1730 kırılması (gece, ateş, boş taht). Final 1742'de Said'le kapanıyor.

Yön dili şöyle: sağ, Paris'e ve Batı'ya giden yol; sol, eve dönüş ve geride kalan. Elçi ve Said İstanbul'da gemiye **sola** yürür (297). Paris'e **sağa** girerler (300, 303). Elçi 318'de **sola** uzaklaşır. Said 1742'de aynı sokağa yine **sağa**, bu kez tek başına girer (320, 300'ün aynası). Son sahnede (321) Said minderde yazar; bu, babasının 292'deki karesinin aynasıdır ve "bak, öğren, anlat" motifini görselde de kapatır.

Kişilerin renkleri bütün videoda aynı kalır:
- **Elçi:** mavi kaftan, kırmızı pelerin, beyaz kavuk, koyu sakal. Orta yaşlı; hiçbir karede ihtiyar çizilmedi.
- **Said:** mor kaftan. 1720'de sakalsız; 1729 ve 1742'de sakallı.
- **Sadrazam:** yeşil. **Padişah:** kızıl kaftan, altın pelerin.
- **Fransızlar:** geniş kenarlı şapka. **Çocuk kral:** mavi kaftan, altın taç, tahtta oturur.

## Sahne planı

Zemin: dış mekânda sprite tabanı 632, iç mekânda 634 (ayakların bastığı son satır; `taban_denetimi` her karede doğrular). "Orta" sütunu orta plandaki yapıların oturduğu düz zemin çizgisidir.

| No | Süre (tahmini) | Konu | Zemin çizgileri | yakin / kamera | Hareket | Kartlar |
|---|---|---|---|---|---|---|
| 290 | 2,5 (kapak) + 6,5 | Toulon limanı, 1720 sonu, alacakaranlık. Taş rıhtımda elçi ve Said denize bakar; geride demirli gemi | Sprite 632 (rıhtımın içinde). Rıhtım üst kenarı 600. Deniz 556'dan aşağısı. Gemi su çizgisi 590 (gövdenin altı suda) | 2,8 / 0 (kapak), 8 | Kollar ve pelerin hafifçe kıpırdar | Kapak, 1 |
| 291 | 4,0 | Veba: çitle kapatılmış yol, meşaleli nöbetçi; geride Toulon surları, damlardan kısa duman | Sprite 632 (çit kazıkları ve nöbetçi). Şehir duz(590) | 2,8 / 8 | Meşale titrer, duman yukarı süzülür | 2 (KIZIL) |
| 292 | 4,1 | Gece, sıcak oda: elçi minderde rahlesine yazar (kart 25'te tekrar kullanılır) | 634; minder, rahle, şamdan ve kitaplar zeminde. Kandil zinciri tavana kadar | 3,0 / 6 | Mum ve kandil titrer | 3 (ALTIN), 25 (ALTIN) |
| 293 | 7,3 | İstanbul sarayı: sadrazam ve padişah karşı karşıya; arkada boş taht | 634; taht bir sıra geride (622) | 2,8 / 6 | İki kandil, hafif kol hareketi | 4 (KIZIL) |
| 294 | 6,9 | Pasarofça 1718: ovada iki müzakere çadırı; Habsburg ve Venedik elçileri, karşılarında antlaşmayı uzatan Osmanlı murahhası | 632; Venedikli bir sıra geride (622). Çadırlar duz(586), küçük ölçek (uzakta) | 2,8 / 10 | Belge tutan kol, flamalar | 5 |
| 295 | 12,6 | Divanhane: Damat İbrahim Paşa minderde kâğıtlarıyla, elçi ayakta dinler | 634 | 2,8 / 6 | Kandil, mum, elçinin kolu | 6 (ALTIN), 7 |
| 296 | 5,2 | Bonnac, Boğaz'a bakan pencereli odada mektubunu okur | 634 | 3,0 / 6 | Mektubu tutan kol | 8 |
| 297 | 12,8 | İstanbul rıhtımı, gri sabah: baba ve oğul sola, gemiye yürür; rıhtımda iki yeniçeri | 632. Yeniçeriler orta planda 606 (rıhtımın içinde). Gemi 590 | 2,8 / 10, x 290→262 | Yürüyüş (adım fazları kaydırılmış) | 9, 10 (KIZIL) |
| 298 | 6,0 | Marsilya: kül rengi gök, deniz kıyısında surlar, damlardan duman; önde boş yol ve çit. İnsan yok | 632 (çit). Şehir duz(590) | 2,8 / 8 | Duman | 11 (KIZIL) |
| 299 | 6,1 | Toulon karantinası: soğuk taş oda, halı yok, tek mum; elçi yazar | 634 | 3,0 / 6 | Mum, kandil | 12 (ALTIN) |
| 300 | 5,4 | Paris, Mart 1721: sokağın sonunda taş evler, kaldırımda kalabalık; elçi (beyaz at) ve Said atlarıyla sağa ilerler | 632 (toynaklar). Said bir sıra geride (624). Kalabalık 594, evler 562 | 2,6 / 12, x 250→290 | Atlar yürür | 13 |
| 301 | 5,5 | Elçi duran atının üstünde defterini tutar; arkada kalabalık | 632. Kalabalık 594, evler 570 | 3,0 / 8 | Defter tutan kol | 14 |
| 302 | 6,4 | Molière'in sahnesi: alçak ahşap sahnede "Türk" kılığında oyuncu ve Fransız oyuncu; ön kenarda sahne mumları | 634 (sahnenin ön yüzü). Oyuncular sahne tahtasının üst yüzünde | 2,8 / 6 | Oyuncular el kol oynatır, mumlar titrer | 15 |
| 303 | 12,4 | Tuileries, kızıl alacakaranlık: uzun saray cephesi; heyet saraya yürür | 632; Fransız rehber 622. Saray duz(584) | 2,8 / 10, x 255→285 | Yürüyüş | 16 (ALTIN), 17 (KIZIL) |
| 304 | 6,5 | Tuileries salonu (mavi ve altın, gündüz pencereleri): solda elçi, sağda tahtta çocuk kral | 634; kral tahtın oturma yüzünde | 3,0 / 6 | Kandil, elçinin kolu | 18 (ALTIN) |
| 305 | 9,3 | Geniş plan: naip, tahtta kral, karşıda elçi | 634 | 2,6 / 8 | İki kandil | 19, 20 (ALTIN) |
| 306 | 4,6 | Palais-Royal operası: sağda sahnede iki şarkıcı, solda önde elçi izler | 634 (elçi). Sahne bir sıra geride (620) | 2,8 / 6 | Şarkıcıların kolları, mumlar | 21 |
| 307 | 5,8 | Paris Rasathanesi, yıldızlı gece: çeyrek daire, dürbün, astronom ve elçi; arkada rasathane binası | 632 (dürbün ve çeyrek dairenin ayakları). Bina duz(584) | 2,8 / 8 | Astronomun gösteren kolu | 22 |
| 308 | 10,3 | Versailles bahçeleri, öğle: uzakta saray, budanmış ağaçlar; önde fıskiyeli havuz, elçi not alır | 632 (havuzun ön duvarı, elçi). Saray duz(574), ağaçlar duz(590) | 2,8 / 8 | Fıskiye (su sütunu kaynağa bağlı, damlalar kavisten havuza iner), yazan kol | 23, 24 |
| 309 | 5,6 | Kâğıthane 1722: dere kıyısında iskeleli köşk; kürek ve kazmalı işçiler, planlı kalfa | 632. Köşk duz(586), dere 560-572 | 2,8 / 10 | Kürek ve kazma iner kalkar | 26 |
| 310 | 9,9 | Mesire: uzakta çadırlar ve ağaçlar; önde havuz ve laleler, elçi kıyıda | 632. Çadırlar 586, ağaçlar 584 | 2,8 / 8 | Fıskiye, laleler rüzgârda | 27 (ALTIN), 28 |
| 311 | 6,2 | 1727: ayakta fetvayı tutan şeyhülislam, minderde fermanı yazan kâtip | 634 | 2,8 / 6 | Kandil, mum | 29 |
| 312 | 7,1 | Atölye: arkada üç ayrı baskı tezgâhı (plakalar iner kalkar), önde basılı sayfalarıyla üç baskıcı | 634; tezgâhlar 620 | 2,6 / 6 | Pres plakaları (faz kaydırılmış) | 30 |
| 313 | 6,9 | Müteferrika tezgâhın kolunu çeker | 634 | 2,8 / 6 | Plaka iner, kol (vidadan ele) her karede elin konumuna bağlı | 31 (ALTIN) |
| 314 | 12,6 | Said elinde belge, Müteferrika ilk sayfayla; aradaki masada kitaplar, arkada tezgâh | 634; tezgâh 622; kitaplar masanın tablasında | 2,8 / 6 | Belge tutan kollar | 32, 33 (ALTIN) |
| 315 | 6,8 | Akşam: boş raf, tek mum; elçi pencereye dönük durur (orta yaşlı) | 634 | 2,8 / 6 | Mum, kandil | 34 (ALTIN) |
| 316 | 3,7 | Eylül 1730, gece: meşaleli isyancılar sağa yürür, yerde ateş, arkada kalabalık ve surlar | 632. Kalabalık 592, şehir 590 | 2,8 / 12 | Yürüyüş, alev, kıvılcım | 35 (KIZIL) |
| 317 | 10,3 | Karanlık saray odası: boş taht, yerde devrilmiş kavuk. Ölüm gösterilmez | 634 | 2,8 / 4 | Kandil sallanır, tek mum titrer | 36, 37 (KIZIL) |
| 318 | 9,8 | Mor alacakaranlık: önde solgun laleler, elçi sola uzaklaşır | 632. Laleler orta planda 684-696 (ayakların önünde, örtüşmez) | 2,8 / 10, x 290→250 | Yürüyüş | 38, 39 (ALTIN) |
| 319 | 12,3 | Kitapçı: dolu raflar, kitap tutan kitapçı; mavi örtülü masada 1757 Fransızca, kırmızı örtülü masada 1866 İstanbul baskısı (iki yığın) | 634; raflar 622 | 2,8 / 6 | Kandil, kol | 40, 41 (ALTIN) |
| 320 | 12,1 | 1742, altın ikindi: Said aynı Paris sokağına tek başına atıyla girer | 632. Kalabalık 594, evler 562 | 2,6 / 12, x 250→290 | At yürür | 42 (ALTIN), 43 |
| 321 | 11,5 | Gece: Said minderde yazar (292'nin aynası). Kapanışın arkası | 634 | 3,0 / 6 | Mum, kandil | 44 (ALTIN), 45 (ALTIN) |

**Kapak:** sahne 290 katmanları, `yaziY: 270`, tek yazı bloğu `["Paris'teki", "Elçi", "Bak, öğren, anlat"]`, boy 112, ALTIN, 2,0 sn. Kapak yazısı 3 satır ve 112 boyunda olduğu için 300'den başlasaydı figürlerin başına değecekti; bu yüzden 30 px yukarı alındı. Yazı yine etiketin (ekran y 150-200) altında kalıyor.

**Kapanış:** `["Piksel Tarih", "@pikseltarihim"]`, "Yorumlara yaz, arkadaşına gönder", 3 sn, arka 321, gece.

**Ses önerisi (müzik platform kütüphanesinden):**
- Toulon: rüzgâr, martı, uzak çan.
- Paris: kalabalık uğultusu, nal sesi.
- Saray: sessizlik, kâğıt hışırtısı.
- Atölye: tahta gıcırtısı ve pres sesi.
- 1730: kalabalık ve çıtırdayan ateş.
- Final: tek mum, kalem cızırtısı.

## Yeni figürler

Yeni figürler yalnızca `celebi_mehmed_paris.py` içinde, `ImageDraw`, `piksel`/`hex2` ve `ciz` denetimleriyle yazıldı. `ciz.py` ve öbür paylaşılan dosyalar değişmedi. Docstring'lerinde "Yeni figür" yazıyor.

- **`paris_evleri(img, x0, x1, zemin, s, tohum, pencerede)`:** 18. yüzyıl Paris sokağı. Bitişik 3-4 katlı taş evler, mansart çatı, çatı pencereleri, kapılar, bacalar; pencerelerde baş. `duz_zemin` + `temel` ile düz zemine kurulur. Uzak fonda küçük ölçekle kullanıldı (s 1,5), böylece öndeki kalabalıkla ölçek çelişmiyor.
- **`saray_cephesi(img, x0, x1, zemin, s, kubbe)`:** Fransız saray cephesi. Kemerli pencere dizisi, pilastrlar, köşe köşkleri, merkez köşkü (kubbeli ya da alınlıklı). Tuileries, Versailles ve rasathanede kullanıldı. Düz zemine kurulur.
- **`havuz(img, x, zemin, s, faz)`:** Oval taş havuz. Ön duvarın alt kenarı zemine oturur. Fıskiyenin su sütunu vazoya bağlıdır, iki kavisle havuza düşer; 24 karelik dikişsiz döngü.
- **`teleskop` / `kadran`:** Üç ayaklı sehpada pirinç dürbün; kaideli çeyrek daire. Ayaklar zemine basar.
- **`baski_tezgahi(img, x, zemin, s, faz)`:** İki dikme kızaklarla yere basar. Başlık, vida, plaka, uç ayaklı tabla, harf kalıbı ve kâğıt var. Plaka fazla iner kalkar. Kol, vidadan baskıcının eline her karede ayrıca çizilir (`_el`, `kisi`'nin el formülüyle), iki ucu da bağlıdır.
- **`kitap_rafi(..., dolu)`:** Raf dolabı. `dolu=False` boş raf verir: kart 34, "belge yok".
- **`kavuk_yerde`:** Yan yatmış kavuk; sargı bantları ve kırmızı külahı yere değer.
- **`kosk(..., iskele)`:** Temsili Lale Devri köşkü: taş zemin kat, ahşap üst kat, geniş saçak. İskele direkleri zemine dikili, çatının yarısı açık mertek.
- **`masa`, `sahne_tahtasi`, `cit`:** Örtülü masa (dönen tabla y'sine kitaplar oturur); alçak tiyatro sahnesi ve sahne mumları; karantina çiti.
- **Yardımcılar:** `_yildiz_ekle` gece göğünün görünen şeridine yıldız ekler (`gokyuzu` yıldızları y 300'ün üstüne koyduğu için yakın kamerada görünmüyordu). `_duman_noktalari` orta plandaki çatı noktalarını sprite koordinatına çevirir ve dumanı yazı bandının altında keser.

## Grafiker öz denetimi

**Çalıştırma:** `python3 -I video/piksel/celebi_mehmed_paris.py` 32 sahnenin hepsini hatasız çiziyor. Her sahne üç denetimden geçiyor:
1. `taban_denetimi`: her karede en alt opak piksel son satırda; havada figür yok.
2. Cem Sultan dosyasından `_kadraj`: figürler görünür aralıkta, baş kesilmiyor.
3. Bu seri için yazılan `_bant_denetimi`: TSX'teki her kartın gerçek yazı yüksekliğini (satır sayısı, sığdırılan font boyu, `yaziY`) okur. Bunu kameranın başlangıç ve sonundaki yakınlığında (yakin ve 1,06·yakin) dünya y'sine çevirir. Sprite'ta ya da orta planda bu satırlara giren opak piksel varsa betiği durdurur; 1-2 piksellik kandil zinciri hariç.

**TypeScript:** `cd video && npx tsc --noEmit -p .` temiz.

**Neye baktım:** Remotion kamerasını (sx/odakY çevresinde yakınlaşma) taklit eden bir önizleyiciyle 32 sahnenin ilk ve son karesini yazı bandı çerçevesiyle birlikte birleştirip tek tek açtım. Ayrıca 12 sahnenin ham sprite karelerini (0 ve 12) açtım: 290, 297, 300, 304, 308, 312, 313, 316, 317, 318, 320, 321. Ayaklar son satırda, havada nesne yok; tavandan sarkan tek şey kandil zinciri. Konturlar koyu sahnelerde de (299, 307, 316, 317) okunuyor.

**Düzelttiklerim:**
1. **Yazı bandına giren yapılar:**
   - 294 ve 310'da çadır direkleri ile bayraklar, 308'de servi ağaçları, 309'da iskele direkleri, 318'de ağaç tepeleri, 291 ve 298'de şehir damları, 303'te saray çatısı banda giriyordu. Hepsi uzak ölçeğe küçültüldü ya da alçaltıldı.
   - 291'deki nöbetçinin mızrağı kaldırıldı; nöbetçi meşale tutuyor (direk yasağı).
2. **Yazıya değen başlar:**
   - 300 ve 320'de atlıların kavukları yazıya değiyordu. Sahneler yakin 2,6'ya alındı, atlı ölçeği bant denetimiyle bulundu (3,8 / 3,9).
   - 316'da meşaleler başın üstündeydi; artık yanda taşınıyor.
   - 313'te baskı tezgâhı küçültüldü.
   - 290'da kapak yazısı `yaziY` ile yukarı alındı.
3. **Kenarda kesilen figürler:** Bir kenar raporu betiğiyle her sahnenin 24 karesi tarandı. Kesilenler ortaya çekildi:
   - 304 ve 305'te taht ve Said (305'ten Said çıkarıldı; naip pelerinsiz).
   - 307'de çeyrek daire ve elçi, 312'de tezgâhlar, 315 ve 319'da raflar, 317'de kavuk.
   - 297'de gemi ve yeniçeriler, 294'te Venedikli, 300'de at kuyruğu ve başı, 311'de şamdan, 316'da ateş ve meşale, 310'da laleler, 295'te şamdan.
4. **Üst üste binme ve derinlik:**
   - 290'da elçi ve Said ayrıldı.
   - 297'de yeniçeriler figürlerin arkasından yana alındı.
   - 318'de laleler elçinin bacaklarıyla örtüşüyordu; ayakların önüne (y 684+) indirildi.
   - 300, 301 ve 320'de evler kalabalıktan büyük görünüp ölçeği bozuyordu; sokağın sonuna, küçük ölçeğe alındı.
5. **Okunurluk ve imge:**
   - 316'da beyaz sivri börkler kötü bir çağrışım yapabilirdi; kalpak ve sarığa çevrildi.
   - 317'deki kavuk "beyaz yumurta" gibi okunuyordu; sargı bantları ve külahla yeniden çizildi.
   - 296'da pencerede "kar" vardı; Boğaz parıltısına çevrildi.
   - 304 ve 305'teki salonun gece pencereleri gündüze çevrildi.
   - 307'de gece göğü görünmüyordu; uzak dağ alçaltıldı, yıldız eklendi.
   - 309'da kalfanın kaftanı elçininkiyle karışmasın diye renk değişti.
   - 312 yeniden kuruldu: kalabalık tezgâh dizisi yerine arkada üç tezgâh, önde basılı sayfalı üç baskıcı.
   - 319'da kitap yığınları büyütüldü.
   - 299'a karantina odası için halısız zemin ve tek mum verildi.

**Kalite kontrol notlarına uyum:**
- Kart 34'te elçi ihtiyar çizilmedi (315, aynı koyu sakallı orta yaşlı figür).
- Hiçbir karede metin dışı yazı ya da rakam yok. Mektup ve defterler boş kâğıt; kart 17 ve 41'in kareleri yalnızca yapı ve kitaplardan oluşuyor.
- 1730 sahnelerinde ölüm gösterilmiyor (boş taht, devrilmiş kavuk).
- Sâdâbâd köşkü temsili bir Lale Devri köşkü olarak çizildi; tarihçilerin tartışması metinde zaten belirtiliyor.

**Bilerek bıraktıklarım:**
- 291 ve 298'deki çit ile 306'daki sahne platformu kadrajın kenarından taşıyor. Bunlar figür değil, kadrajı boydan boya geçen yapılar.
- Gemi (290, 297) uzak su çizgisinde olduğu için öndeki insanlardan küçük görünüyor. Direği yazı bandına girmesin diye büyütülmedi.
- Paris evleri uzak fonda olduğu için pencerelerdeki başlar birer nokta kadar.
- Sahne sayısı 32, aralığın üst sınırında; 241 sn seslendirme için sahne başına ortalama 7,5 sn düşüyor. Kart 25, yazı odası 292'ye bilinçli bir dönüş olarak aynı sahneyi kullanıyor.

**Kod tarafına not:** Render öncesi `Root.tsx` kaydı ve sesin `hizala_seri.py` ile hizalanması gerekiyor. Hizalama TSX'teki kart sürelerini değiştirdiği için `_bant_denetimi` her zaman güncel TSX'i okur; süreler bant hesabını etkilemez.
