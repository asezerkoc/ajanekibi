# 🟢 Grafik: Defterde Bin Yazıyor · irlanda-kitligi

**İş:** Piksel Tarihim (@pikseltarihim), gece vardiyası 10/10 · **Hazırlayan:** 🟢 SKONSTART Grafiker · 31 Ekim 2026
**Girdi:** 4-kalite-metin.md (nihai seslendirme metni, 52 nihai kart, grafiker notları)
**Dosyalar:** `video/piksel/irlanda_kitligi.py` (sahneler 490-524, 35 sahne) · `video/src/sahneler/IrlandaKitligi.tsx`
(export: `IRLANDA_SERI`, `IRLANDA_KARE`, `IrlandaKitligi`; etiket "PİKSEL TARİHİM · İRLANDA KITLIĞI"; ses `irlanda-kitligi-anlatim.mp3`).
Root.tsx'e ve başka konuların dosyalarına dokunulmadı.

## Kurgu özeti

- **Kapak** (2 sn, sahne 490 katmanları): "Defterde / Bin Yazıyor / Bir iyilik nasıl efsane olur?" (3 satır, boy 112, ALTIN; editörün kapak önerisi).
- 41 anlatım bloğu, 35 farklı sahne. Açılış üçlüsü (kart 1-3: padişah, efsanenin üç gemisi, defter) sonda aynı sırayla döner
  (kart 51 defter = 492, kart 52 gemiler = 491): kanca ile cevap görsel olarak da kapanır. Motif "Defterde hâlâ bin yazıyor"
  (kart 3, 28, 51) her seferinde aynı kâtip kürsüsü ve açık defterle (492, 511) gösterilir, kart rengi ALTIN.
- Hilal ve yıldız yalnızca efsane kapısında (514, soluk gece sisi), mühür yakın planında (516) ve Kral John'un kalkanında (517).
  Efsane sahneleri (491, 514) soğuk gri-mavi, sisli, "hayal gibi" paletle; belge sahneleri sıcak mum ışığında.
- Drogheda "nehir kıyısında liman" olarak çizildi (grafiker notu): karşı kıyıda taş sette kasaba ve kilise kuleleri, Boyne,
  önde taş rıhtım (505-507). Nehir ağzı / deniz yok.
- Defter ve belgelerde rakam ya da yazı yok: yalnız satır çizgileri, sütun çizgisi, mühür. "1000" hiçbir sahnede yazılmadı.
- Süreler tahmini (toplam ≈ 245 sn + kapak + 3 sn kapanış); `video/ses/hizala_seri.py` sese göre yeniden yazar. Kart blokları
  `    {` satırıyla, kapak `    { // KAPAK` satırıyla açılır. Bütün bloklarda `yaziY: 250` (yazı bandı figürlerin başına değmesin
  diye 25 px yukarıda; etiketle çakışmıyor).
- Kart renkleri: KIZIL 7, 8, 9, 28, 33, 37, 39, 45, 46 (açlık, ölüm, "ama" dönüşleri, belgenin yokluğu); ALTIN 1, 2, 3, 16, 24, 36,
  49, 51, 52 (motif, cevap, soru) ve kapak.

## Sahne planı

| No | Süre (tahmin) | Konu | Zemin | yakin / kamera | Hareket | Kartlar |
|---|---|---|---|---|---|---|
| 490 | 2.9 sn | İstanbul, saray odası: genç padişah masada bağış kesesini mühürlü kâğıtla gönderir | iç: sprite tabanı 634, döşeme 596 | 2.8 / 6 | sabit, 10 fps | 1 |
| 491 | 5.7 sn | efsane: gece, sisli nehirde üç soluk yelkenli (hayal gibi) | dış: sprite tabanı 632, orta zemin 588-600 | 2.6 / 10 | sabit, 8 fps | 2 |
| 492 | 2.8 sn | defter yakın plan: kâtip kürsüsünde açık defter, mum | iç: sprite tabanı 634, döşeme 596 | 3.2 / 4 | sabit, 8 fps | 3 |
| 493 | 8.9 sn | İstanbul, 1847 baharı: saray bahçesinde erguvanlar, padişah yürür; uzakta Boğaz ve camiler | dış: sprite tabanı 632, orta zemin 588-600 | 2.8 / 10 | x 258→284 (yürüyüş) | 4, 5 |
| 494 | 4.2 sn | İstanbul: kahvehane önü, peykede gazete okuyanlar | dış: sprite tabanı 632, orta zemin 588-600 | 2.8 / 8 | sabit, 10 fps | 6 |
| 495 | 4.6 sn | İrlanda, 1845 sonbaharı: çürüyen patates tarlası, köylü kazar; taş kulübe | dış: sprite tabanı 632, orta zemin 588-600 | 2.8 / 8 | sabit, 10 fps | 7 |
| 496 | 8.5 sn | göç yolu: bohçalı aile limana yürür; geride damı çökmüş boş kulübe | dış: sprite tabanı 632, orta zemin 588-600 | 2.6 / 12 | x 286→254 (yürüyüş) | 8, 9 |
| 497 | 4.0 sn | Londra, Ocak 1847: yardım derneğinin odası, beyefendiler masa başında | iç: sprite tabanı 634, döşeme 596 | 2.8 / 6 | sabit, 10 fps | 10 |
| 498 | 4.7 sn | Kraliçe Victoria (taç) bağışını kâğıtla uzatır; saray odası | iç: sprite tabanı 634, döşeme 596 | 3.0 / 6 | sabit, 10 fps | 11 |
| 497 | 4.9 sn | aynı dernek odası: kâtip deftere yazar | iç: sprite tabanı 634, döşeme 596 | 2.8 / 6 | sabit, 10 fps | 12 |
| 499 | 5.7 sn | İstanbul: Osmanlı nazırı bağış kesesini İngiliz elçisi Wellesley'e emanet eder | iç: sprite tabanı 634, döşeme 596 | 2.8 / 6 | sabit, 10 fps | 13 |
| 500 | 5.5 sn | Londra: kâtip yüksek yazı kürsüsünde deftere yazar | iç: sprite tabanı 634, döşeme 596 | 3.0 / 6 | sabit, 10 fps | 14 |
| 501 | 5.1 sn | Osmanlı kâtibi rahlede kayıt düşer; sedir ve mum | iç: sprite tabanı 634, döşeme 596 | 3.0 / 6 | sabit, 10 fps | 15 |
| 502 | 4.4 sn | iki defter yan yana: deri ciltli İngiliz defteri ve kırmızı ciltli Osmanlı defteri | iç: sprite tabanı 634, döşeme 596 | 3.2 / 4 | sabit, 8 fps | 16 |
| 503 | 9.8 sn | Dublin, 1847: soylular masada teşekkür mektubunu imzalar | iç: sprite tabanı 634, döşeme 596 | 2.8 / 6 | sabit, 10 fps | 17, 18 |
| 504 | 5.4 sn | bugün: kütüphane, camlı vitrinde mektup; bir okur bakar | iç: sprite tabanı 634, döşeme 596 | 2.8 / 6 | sabit, 10 fps | 19 |
| 505 | 4.9 sn | Drogheda, Mayıs 1847: Boyne kıyısında taş rıhtım, karşı kıyıda kasaba | dış: sprite tabanı 632, orta zemin 588-600 | 2.6 / 8 | sabit, 8 fps | 20 |
| 506 | 5.7 sn | üç yabancı yelkenli rıhtıma yanaşır; rıhtımda halat bekleyen hamallar | dış: sprite tabanı 632, orta zemin 588-600 | 2.6 / 8 | sabit, 8 fps | 21 |
| 507 | 9.1 sn | rıhtımda tahıl çuvalları, tüccar defteriyle; biri gazete okur | dış: sprite tabanı 632, orta zemin 588-600 | 2.8 / 8 | sabit, 10 fps | 22, 23 |
| 508 | 5.5 sn | Selanik limanı: Beyaz Kule, minareler; demirli yelkenli | dış: sprite tabanı 632, orta zemin 588-600 | 2.6 / 8 | sabit, 8 fps | 24 |
| 509 | 5.4 sn | New York, 1849: tuğla binalar, gazete satan çocuk | dış: sprite tabanı 632, orta zemin 588-600 | 2.8 / 8 | sabit, 10 fps | 25 |
| 510 | 6.1 sn | basımhane: demir el baskı makinesi, baskıcı kolu çeker, çırak kâğıt alır | iç: sprite tabanı 634, döşeme 596 | 2.8 / 6 | sabit, 10 fps | 26 |
| 499 | 5.2 sn | rivayet: aynı salonda elçi elini kaldırıp araya girer | iç: sprite tabanı 634, döşeme 596 | 2.8 / 6 | sabit, 10 fps | 27 |
| 511 | 5.7 sn | gece: defterin üstünde katlanmış gazete, mum | iç: sprite tabanı 634, döşeme 596 | 3.2 / 4 | sabit, 8 fps | 28 |
| 512 | 4.8 sn | Londra, 1851: yazar masasında biyografiyi yazar; kitap yığını | iç: sprite tabanı 634, döşeme 596 | 2.8 / 6 | sabit, 10 fps | 29 |
| 513 | 4.7 sn | Drogheda, yıllar sonra: kasaba sokağında kasketli adamlar konuşur | dış: sprite tabanı 632, orta zemin 588-600 | 2.8 / 8 | sabit, 10 fps | 30 |
| 491 | 4.4 sn | efsane: soluk üç gemi gece nehirde | dış: sprite tabanı 632, orta zemin 588-600 | 2.6 / 10 | sabit, 8 fps | 31 |
| 514 | 4.5 sn | efsane: kasaba kapısında hilal ve yıldızlı kalkan (soluk, hayal gibi) | dış: sprite tabanı 632, orta zemin 588-600 | 2.6 / 8 | sabit, 8 fps | 32 |
| 515 | 4.9 sn | 1844: tarihçi D'Alton masasında kitabını yazar | iç: sprite tabanı 634, döşeme 596 | 2.8 / 6 | sabit, 10 fps | 33 |
| 516 | 5.7 sn | mühür yakın planı: kürsüde belge, kırmızı balmumu mühürde hilal ve yıldız | iç: sprite tabanı 634, döşeme 596 | 3.2 / 4 | sabit, 8 fps | 34 |
| 517 | 8.7 sn | 13. yüzyıl: Kral John taçlı, eski armalı sancak ve kalkan; taş kale | dış: sprite tabanı 632, orta zemin 588-600 | 2.6 / 8 | sabit, 10 fps | 35, 36 |
| 518 | 6.3 sn | arşiv: boş raflar, fenerle arayan arşivci | iç: sprite tabanı 634, döşeme 596 | 2.8 / 6 | sabit, 10 fps | 37 |
| 519 | 8.9 sn | yerel tarihçi kitaplarla dolu odasında; elinde açık kitap | iç: sprite tabanı 634, döşeme 596 | 2.8 / 6 | sabit, 10 fps | 38, 39 |
| 520 | 11.0 sn | Drogheda, 1995: West Street'te otel cephesi, plaket; belediye başkanı ve büyükelçi | dış: sprite tabanı 632, orta zemin 588-600 | 2.8 / 8 | sabit, 10 fps | 40, 41, 42 |
| 521 | 8.9 sn | Ankara, 2010: resmî yemek, uzun masa; Cumhurbaşkanı ayakta konuşur | iç: sprite tabanı 634, döşeme 596 | 2.8 / 6 | sabit, 10 fps | 43, 44 |
| 522 | 6.5 sn | ertesi gün: ofiste basın görevlisi düzeltme metnini okur | iç: sprite tabanı 634, döşeme 596 | 3.0 / 6 | sabit, 10 fps | 45 |
| 523 | 8.9 sn | 1861: boş taht, sönmeye yüz tutmuş şamdanlar | iç: sprite tabanı 634, döşeme 596 | 2.8 / 4 | sabit, 8 fps | 46, 47 |
| 524 | 8.9 sn | belgeler masası: defter, teşekkür mektubu ve mühür | iç: sprite tabanı 634, döşeme 596 | 3.2 / 4 | sabit, 8 fps | 48, 49 |
| 513 | 5.1 sn | Drogheda: kasaba sokağı (hikâye eklenir) | dış: sprite tabanı 632, orta zemin 588-600 | 2.8 / 8 | sabit, 10 fps | 50 |
| 492 | 2.6 sn | defter yakın plan (motif) | iç: sprite tabanı 634, döşeme 596 | 3.2 / 4 | sabit, 8 fps | 51 |
| 491 | 5.7 sn | efsanenin üç gemisi soluklaşır | dış: sprite tabanı 632, orta zemin 588-600 | 2.6 / 10 | sabit, 8 fps | 52 |
Ortak zemin kuralları: dış mekânda sprite tabanı 632 (figürlerin ayakları son satırda, `taban_denetimi`), orta plandaki yapılar
`duz(590)` düz zemine (`duz_zemin` toleranslı) oturur; liman sahnelerinde rıhtım üst kenarı orta planda y 600, gemi gövdeleri bu
kenarın ardında suya oturur. İç mekânda duvar ve döşeme tek parça orta planda (FL 596), sprite tabanı 634; avize-kandil zinciri
tavana kadar (`_kz`). Kişi ölçeği `K(no)`: başlıksız ayakta insan kadraj yüksekliğinin %30'u (sahneye göre s 5.7-6.5).

## Yeni figürler (hepsi `irlanda_kitligi.py` içinde; ciz.py'ye eklenmedi)

- **beyefendi**: 19-20. yy erkeği (kisi gövdesi, kemersiz setre/redingot, beyaz yaka, düğmeler, saç). Başlık: `fes` (püsküllü;
  padişahta elmas iğneli kısa sorguç), `silindir` şapka, `kasket`. Ek: bıyık, sakal, nişan, belediye başkanı zinciri, kravat,
  yelek, gözlük, iki elle açılmış gazete. Göz satırı hiçbir başlık ya da saçla örtülmez.
- **hanim**: çan etekli kadın (ayak ucu yerde); `tac` (Victoria, mavi kuşak), `sal` (İrlandalı köylü kadın, göz açık), bugünün kısa
  saçı (`topuz=False`), bohça/mektup.
- **oturan_fesli** (bağdaş, fes, gazete), **oturan_masada** (örtülü masanın ardında oturan; bacaklar örtünün arkasında).
- **yelkenli**: 1840'ların iki direkli tüccar brikı (kara gövde, boya şeridi, baş bodoslama, seren, arma; yelken sarılı ya da açık),
  su çizgisine oturur; `gemi_suda` gövdenin batık kısmını orta plandaki suyla aynı renkte yamayla örter ve köpük çizer.
- **kulube** (saz damlı taş kulübe; `cokmus=True` terk edilmiş), **patates** (kararmış fide), **kursu** (yüksek kâtip kürsüsü,
  açık satır çizgili defter, hokka, tüy kalem), **masa**, **raf** (dolu/boş), **vitrin**, **baski_makinesi** (demir el baskı
  makinesi, pres faz ile iner kalkar), **kese**, **peyke**, **kahvehane**, **ambar**, **tugla_evler**, **eski_ev_sirasi**,
  **otel_cephesi** (yazısız bronz plaket), **kale_kapisi** (iki kuleli barbakan), **arma_kalkani** (hilal-yıldız / eski aslanlı),
  **sancak**, **beyaz_kule**, **cami**, **cuval**/**cuval_yigini**, **samdan** (kısalmış mumlu, 1861), **mum**, **kandil**,
  **lamba_tavan** (bugünün sahneleri), **dizustu** (2010 ofisi), **fener_el**.
- Katman yardımcıları: `oda` (Batı tarzı iç mekân: duvar kâğıdı/damask/tuğla/lambri, pencere, perde, tablo, şömine, halı; her
  oda farklı renk ve döşemeyle), `liman_orta`, `nehir_orta`, `zemin_orta` (kaldırım, tarla, çayır, toprak), `kasaba_uzak`, `uzak_tepe`.

## Grafiker öz denetimi

**Otomatik denetimler (her sahnede `_bitir`; biri bile geçmezse betik durur).** Ayarlar TSX'ten okunur (tek kaynak):
1. `_kadraj`: 24 karenin HEPSİNDE tam opak piksellerin sol ve sağ ucu, sahne başında (yakin, ±kamera) ve sonundaki %6
   yakınlaşmada (yakin·1.06, ±kamera) görünür aralığın 6 px içinde; yürüyen sahnelerde (493, 496) baş ve son sx'in ikisinde de.
   Sprite'ın üst kenarına değen figür yok. Görünür alanın formülü TimurSeri.tsx'teki dönüşümden (odak sx, origin sx·2) türetildi.
2. `taban_denetimi`: her karede en alt opak piksel son satırda (havada figür yok).
3. `_bant`: sprite'ın (ve dış mekânda orta planın) görünür sütunlarında, kartın dünya y bandında opak satır yok; bütün Bolum'lar
   ve iki yakınlaşma için ayrı ayrı.
4. `_orta_gorunur`: orta plandaki konu nesneleri (493 korkuluk/çalı, 495 ve 496 kulübe, 508 Beyaz Kule, 517 kale) görünür aralıkta.
5. Yapılar `duz_zemin` ile düz zemine kurulur; gemi gövdeleri su çizgisine oturur, batık kısım su yamasıyla örtülür.

**Gözle bakılan (TimurSeri dönüşümünü taklit eden önizleme ile sahne başı ve sonu, yazı bandı çerçeveli; ayrıca ham sprite
şeritleri):** 35 sahnenin hepsi. Düzelttiklerim:
- 493: erguvan ağaçlarının tepeleri başların arkasına denk geliyor, karşı kıyıdaki cami padişahın başının üstünde "oturuyordu";
  ağaçlar kaldırıldı, yerine korkuluk dibinde çiçekli erguvan çalıları; karşı kıyı puslu, alçak silüet. Sorguç tüyü anten gibi
  yana uzanıyordu: kısa, dik tüy.
- 490: kese vazo gibi büyüktü, küçültüldü; bıyık ağız gibi okunuyordu, ince çizgi yapıldı.
- 492/511/516: defter ince bir şerit gibi okunuyordu; kürsünün eğik tablası büyütüldü (defter sayfaları ve satırlar okunuyor).
- 497/498/503/512: "favori" (yanak sakalı) yüzde kara bir şerit gibi duruyordu (göz bandı izlenimi): kaldırıldı. Masada oturanların
  yalnız başı görünüyordu: masa alçaltıldı, gövde görünür.
- 498: Victoria'nın sekreteri 497'deki dernek başkanıyla aynı renklerdeydi (iki karakter aynı): ayrı renk ve yelek.
- 501: kütüphanenin `ic_mekan` penceresi kar yağışı çiziyordu (İstanbul baharında yanlış): Batı/Osmanlı karması kendi odamız,
  çini mavisi lambri, kemerli bahar penceresi. Rahle büyütüldü.
- 505/507/509: silindir şapkalar kırmızı çıkıyordu (varsayılan fes rengi): siyah.
- 506: hamallar gemi yanında çok küçük kalıyordu: ölçek gemiyle tutarlı biçimde 1.2; halat gemiden rıhtıma bağlı.
- 508: Beyaz Kule rıhtımda hamallarla yan yana insanın ancak 5 katıydı (ölçek hatası): karşı kıyının taş seddine, uzağa alındı;
  rıhtımda yalnız çuvallar kaldı.
- 517: kalkan başın yanında havada asılı gibiydi: kral kalkanı kalça hizasında elinde tutuyor.
- 519: kasabanın tarihçisi 515'teki D'Alton'la aynı kompozisyon ve kır saçla çiziliyordu: kahverengi saç, yeşil kazak, gözlük;
  kompozisyon aynalandı (raf sağda).
- 511/512: kenara dayanan pencere ve rafın arkasında kalan tablo içeri alındı.
- Kenar denetiminin yakaladıkları (495, 504, 506, 508, 512, 515, 518, 519): raflar, ilk ve son gemiler, patates sırası 4-12 px içeri.
- Kaba yazı bandı: 493'te fesin tepesi 3 satırlık kartlara değiyordu; bütün bloklarda yaziY 250.

**Bilerek verilen kararlar (kalite kontrolün bilgisine):**
- 506 ve 508 gemi sahneleri: konu gemiler; insanlar gemiye göre doğru ölçekte (direk ≈ 100 px, insan ≈ 18 px). Bu iki sahnede
  insan figürü kadrajın %30'u değil; "insandan küçük oyuncak gemi" hatasına düşmemek için bilinçli. Büyük figürlü Drogheda
  sahnelerinde (505, 507) gemi gösterilmedi.
- 492, 502, 511, 516, 524 yakın plan nesne sahneleri (defter, mühür); insan yok, nesne kadrajın üçte birini dolduruyor.
- Uzak plan ve gökyüzü her sahnede olduğu gibi yavaşça kayar (motorun standardı); iç mekân duvarları ise orta planda, kaymaz.
- Seslendirme dosyası (`irlanda-kitligi-anlatim.mp3`) public/ altında henüz yok; hizalama aşamasında üretilir.

**Kontrol komutları:** `python3 -I video/piksel/irlanda_kitligi.py` (35/35 sahne, bütün denetimler geçti) ·
`cd video && npx tsc --noEmit -p .` (temiz).

## Görsel KK revizyonu (6-kalite-gorsel.md, 9 zorunlu düzeltme + iyileştirmeler)

Kural: aynı derinlikteki yapı insandan belirgin büyük; olamıyorsa ufka/uzağa alınır ve arada zemin okunur. TSX'te yalnız kapak
bloğu değişti; kapak dışı blokların süreleri, kart metinleri ve sprite ayarları sese hizalı hâliyle aynen kaldı.

| # | Sahne | Düzeltme |
|---|---|---|
| 1 | 496 | Oyuncak kulübe kaldırıldı; yolun gerisinde bel hizasında kuru taş duvar (insan ölçeğinde, başların altında). |
| 2 | 509 | Yeni `cephe` yardımcısı: tuğla evler insan ölçeğinde, figürlerin 5 px gerisinde; kapı insandan yüksek, üst katlar kadrajın tepesine uzanan düz tuğla duvar. |
| 3 | 520 | Otel cephesi insan ölçeğinde; yeşil kapı insandan yüksek, plaket kapının yanında göz hizasında ve küçük. |
| 4 | 517 | Kale ufka alındı: çayırın uzak kenarında küçük ve puslu (kralın başıyla, sancakla çakışmıyor). |
| 4b | 494, 495, 507, 513 | Aynı gözle tarandı: 494 kahvehane ve 507 taş ambar (çifte kapı) ve 513 sıvalı ev insan ölçeğinde cepheye çevrildi; 495'teki küçük kulübe kaldırıldı. |
| 5 | 506 | Üç gemi ayrıldı: önde solda büyük (s 2.0), ortada (1.5), en geride sağda (1.1); direk grupları birbirini kesmiyor, her biri kendi su çizgisinde. Gövde altı rıhtım kenarının üstünde suda (su yaması kenarda biter). Rıhtım babaları (koyu çıkıntı) kaldırıldı. |
| 6 | 491 | Efsanenin üç gemisi aynı düzende ayrı ve sayılabilir; soluk, sisli palet korundu (kart 2, 31, 52). |
| 7 | 505, 506 (513, 509) | Beyzbol şapkası gibi okunan kasket kaldırıldı: 1840'lar hamalına geniş kenarlı yumuşak keçe şapka (`kece`); `kasket` artık basık, yumuşak tepeli, çok kısa siperlikli yassı kasket (513'teki 1930'lar adamları, 509'daki gazeteci çocuk). |
| 8 | 490, 497-500, 504, 510, 512, 515, 519, 521, 522 | Avize, kandil ve tavan lambaları kaldırıldı (yarım görünen nesne kalmadı). |
| 9 | bütün iç mekânlar ve cepheler | `_bant` denetimi duvar katmanına genişletildi: yazı bandında satır başına en çok 5 renk (düz duvar ve deseni); pencere, perde, tablo, kapı, korniş banda girerse betik durur. `oda` pencereleri ve tabloları bandın altından başlatır, sığmayanı çizmez (490, 498'de pencere kalktı; 499, 511, 521, 503'te alçaldı). |

İyileştirmeler: Abdülmecid'e kısa koyu sakal (490, 493); pencere camları titreşimsiz düz renk (kar izlenimi yok); 503'te imzalayan
soylunun elinde tüy kalem. Kapak: Jersey yazı bileşeni bir karttaki bütün satırları en uzun satıra göre aynı boya sığdırdığı için
alt başlık iki kısa satıra bölündü ("Bir iyilik nasıl" / "efsane olur?"); başlık 68 yerine 88 boyda, 4 satır, yaziY 215 (figürlerin
başı yazıya değmez, denetimle doğrulandı). Gerçek boy farkı (büyük başlık, küçük alt başlık) TimurSeri.tsx'te değişiklik gerektirir;
o dosyaya dokunulmadı.

Kontrol: `python3 -I video/piksel/irlanda_kitligi.py` 35/35 sahne bütün denetimlerden geçti (kenar, taban, yazı bandı + duvar modu,
orta plan görünürlüğü, cephe öğelerinin kadraj içinde kalması). Değişen sahnelerin önizlemesine (sahne başı ve sonu, yazı bandı
çerçeveli) tek tek bakıldı. `cd video && npx tsc --noEmit -p .` temiz.
