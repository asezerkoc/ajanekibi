# 🟢 Grafik: Fermanı Gören Yok (Osmanlı'da "matbaa yasağı" efsanesi ve İbrahim Müteferrika)

**İş:** Piksel Tarih (@pikseltarihim), gece vardiyası 2/10, slug `matbaa-yasagi`
**Girdi:** teslimler/gece/ara/matbaa-yasagi/4-kalite-metin.md (nihai seslendirme metni, 49 nihai ekran kartı, grafiker notları)
**Hazırlayan:** 🟢 SKONSTART Grafikeri · 31 Ekim 2026

## Teslim edilen dosyalar

- `video/piksel/matbaa_yasagi.py`: sahneler **170-209** (40 sahne), yeni figürler, ölçek/kadraj/yazı bandı denetimleri. Çalıştırma: `python3 -I video/piksel/matbaa_yasagi.py [no ...]` (40 sahne yaklaşık 3-4 dakika). Çıktılar `video/public/sahneNNN-{gokyuzu,uzak,orta,on,karakter}.png` (+ `sahne183-hava.png`, kar).
- `video/src/sahneler/MatbaaYasagi.tsx`: `MATBAA_SERI`, `MATBAA_KARE`, `MatbaaYasagi`; etiket "PİKSEL TARİHİM · MATBAA YASAĞI", ses `matbaa-yasagi-anlatim.mp3`. Kapak bloğu `    { // KAPAK` (sahne 170 katmanları, 2 sn, "Matbaa / Yasağı / Fermanı gören yok", boy 112, ALTIN). Diğer blokların açılışı yalnızca `    {`, yorumlar üst satırda. Kapanış: arka 209, gece.
- `Root.tsx` değiştirilmedi (kayıt kod tarafının işi). Başka konuların dosyalarına dokunulmadı.

**Tek kaynak:** Python betiği yakin, sprite ölçüleri ve kart metinlerini TSX'ten okur. Her sahne çizildikten sonra figürlerin ve orta plandaki yapıların yazı bandına girip girmediğini PNG üzerinden denetler. `hizala_seri.py` yalnızca `sure` değerlerini yeniden yazar. Yapı ve yakin değişirse betik yeniden çalıştırılmalı.

**Süre:** Kartların tahmini süresi harf/14 + 0,4 sn; yavaş/sessiz kartlara (3, 9, 17, 31, 36, 41, 42, 44, 49) +0,8 sn eklendi. Kapak 2 sn ve kapanış 3 sn ile toplam yaklaşık 267 sn; seslendirme 266 sn. Süreleri `ses/hizala_seri.py` sese göre yeniden yazacak.

**Kartlar:** 49 kart, nihai listeyle harfi harfine aynı ve aynı sırada (betikle karşılaştırıldı; TS içindeki `\"` yalnızca tırnağın kaçışı). En uzun satır 30 harf. 4 satırlı kartlar (12, 13, 14, 25, 31, 32, 33, 37, 40, 45) `boy: 72` ile küçültüldü, figür başlarının üstünde kalıyor. Renkler: KIZIL tehlike ve dönüşte (1, 8, 12, 19, 39, 41, 42), ALTIN motif, soru ve cevapta (3, 9, 16, 17, 20, 25, 28, 31, 34, 36, 44, 46, 47, 49).

**Yön dili:** Sağ İstanbul'a ve ileriye (gelen, yürüyen, basan), sol Avrupa'ya ve geriye. Bütün yürüyüş sahneleri (174, 185, 189, 191, 208) sağa gidiyor.

## Sahne planı

İç mekân: sprite 400×300, taban 634, tavandan kandil (zincir `_kz` ile kadrajın üstüne kadar). Arşivde, anakronizm olmasın diye, kandil yerine modern tavan lambası var. Dış mekân: sprite 400×230, taban 632, orta plan yapıları `duz(588)` üstünde. Figür ölçüsü `s_kisi`/`s_oturan`/`s_sandalye` ile kadraj yüksekliğinin %30-32'si (oturanlar %22-30).

| No | Süre (sn, tahmini) | Konu | Zemin çizgisi | yakin / kamera | Hareket | Kartlar |
|---|---|---|---|---|---|---|
| 170 (kapak) | 2,0 | Kapak: sahne 170 katmanları, "Matbaa / Yasağı / Fermanı gören yok" (ALTIN, boy 112) | 634 | 2.6 / 0 | sessiz | kapak |
| 170 | 7,8 | Paris, 1584, gece: Thevet masasında yazıyor (yakın) | sprite tabanı 634 (iç mekân taş döşeme); sandalye, yazar ve masa aynı zeminde | 3.0 / 6 | tüy kalem yazıyor, mum titriyor, kandil sallanıyor | 1 (K), 2 |
| 171 | 4,3 | Motif: boş rahle, kandil (fermanı gören yok) | 634; rahle ayakları zeminde | 3.0 / 4 | kandil ve tek mum titriyor (bilinçli durgunluk) | 3 (A) |
| 172 | 4,8 | Paris, 1584: Thevet'in çalışma odası (geniş) | 634; raf, sandalye, masa ve şamdan aynı zeminde | 2.6 / 8 | yazma hareketi, mumlar | 4 |
| 173 | 6,7 | Thevet'in sayfası: yanında açık Gutenberg kitabı; iddia onun kaleminden | 634; masa üstü 6,6 s'de: kitap sehpası ve kitap masaya oturur; yerde kitap yığını | 3.0 / 6 | yazma, mum | 5 |
| 174 | 4,5 | 1550'ler, İstanbul: gezgin Thevet yürüyor | 632 (orta plan duz(588): cami ve ahşap ev) | 2.6 / 8 | Thevet sağa yürür (adım 12 fps, sprite x 225→315); çimen rüzgârda | 6 |
| 175 | 10,7 | Bugün, İstanbul: rehber anlatıyor | 632; orta plan duz(588): cami ve ev | 2.6 / 8 | rehberin kolu anlatırken iner kalkar | 7, 8 (K), 9 (A) |
| 176 | 11,4 | İstanbul, 13 Aralık 1493: Nahmias kardeşlerin tahta presi | 634; pres kızakları, tabla uç ayakları ve iki kişi aynı zeminde | 2.8 / 8 | plaka iner kalkar, kol baskıcının eline bağlı, kandil | 10, 11 |
| 177 | 5,7 | Basılmış sayfalar ipte kuruyor, kitap yığını | 634; ip direkleri arka zeminde (taban−14, derinlik), rahle önde | 2.8 / 6 | asılı sayfalar hafif sallanır, kandil | 12 (K) |
| 178 | 7,5 | 1567: kilisede Abgar ve oğlu baskıda | 634; sunak arka zeminde (taban−14, küçük), pres ve iki kişi önde | 2.8 / 8 | pres basıyor, mumlar | 13 |
| 179 | 7,5 | 1588: III. Murad fermanı veriyor | 634; sedirin dört ayağı zeminde, padişah sedirin üstünde; kâtip iki dizi yerde | 2.8 / 8 | kâtibin kolu, mumlar | 14 |
| 180 | 6,6 | Roma baskısı Öklid, 453. sayfa: izin fermanı (yakın) | 634; rahle ayakları zeminde | 3.0 / 4 | sayfa köşesi kıpırdar, kandil | 15, 16 (A) |
| 181 | 7,4 | Motif: boş rahle ve Öklid | 634; iki rahle zeminde | 2.8 / 4 | kandil | 17 (A) |
| 182 | 5,8 | 1627, Pera: Metaksas kiralık evde basıyor | 634; pres, Metaksas ve kitap yığını zeminde | 2.8 / 8 | pres basıyor (tabla sola uzanır) | 18 |
| 183 | 3,6 | Ocak 1628, Pera: kış gecesi, makamlar kapıda | 632 karlı zemin; orta plan duz(588): ahşap ev (karlı dam) | 2.6 / 6 | kar yağar (hava 10), görevlinin kolu, meşale alevi | 19 (K) |
| 184 | 4,9 | Cizvitlerin kışkırtması: mektup el değiştiriyor | 634; arkadaki Cizvit taban−10'da (küçük, derinlik) | 2.8 / 8 | mektubu uzatan kol | 20 (A) |
| 185 | 4,6 | 1679, İstanbul: Marsigli yürüyor | 632; orta plan duz(588): cami ve evler | 2.6 / 8 | Marsigli sağa yürür (x 225→315) | 21 |
| 186 | 4,9 | Marsigli masasında yazıyor | 634; sandalye ve masa zeminde | 3.0 / 6 | yazma, mumlar | 22 |
| 187 | 4,0 | Kopyacılar rahle başında | 634; minder ve rahleler zeminde | 2.8 / 8 | kamış kalemler farklı fazda yazıyor | 23 |
| 188 | 5,9 | İki masa: Paris'te yazan, İstanbul'da yaşamış olan | 634; iki sandalye ve iki masa zeminde | 2.6 / 6 | iki yazar farklı fazda yazıyor | 24 |
| 189 | 8,3 | Alacakaranlıkta yolda tek bir adam: onu izleyin | 632; orta plan duz(588): patika ve ağaçlar | 2.6 / 8 | yolcu sağa yürür (x 225→315), çimen | 25 (A) |
| 190 | 4,5 | Kolozsvár, 1670'ler: beşik | 634; beşiğin kızağı (çember yayı) her karede zemine değer | 2.8 / 6 | beşik ±6° sallanır, annenin kolu, mum | 26 |
| 191 | 5,6 | Genç adam İstanbul'a geliyor | 632; orta plan: sur duz(588), cami duz(580) surun ardında | 2.6 / 8 | genç adam sağa yürür (x 225→315) | 27 |
| 192 | 6,3 | Saray kapısı: müteferrika İbrahim | 632; orta plan duz(588): saray kapısı | 2.6 / 6 | İbrahim'in kolu hafif kıpırdar | 28 (A) |
| 193 | 4,6 | 1726: sadrazama risale | 634; sedir ayakları zeminde, sadrazam sedirde | 2.8 / 8 | risale uzatan kol, mumlar | 29 |
| 194 | 5,5 | Paris, 1720: genç Said matbaayı izliyor | 634; pres, baskıcı ve Said zeminde | 2.8 / 8 | pres basıyor, Said'in kolu | 30 |
| 195 | 8,8 | Şeyhülislamın fetvası: olur | 634; minder, rahle ve kitaplar zeminde | 3.0 / 6 | kamış kalem yazıyor | 31 (A) |
| 196 | 7,0 | Temmuz 1727: III. Ahmed'in beratı | 634; tahtın ayakları zeminde, padişah tahtta; İbrahim diz çökmüş | 2.8 / 8 | beratı alan kol | 32 |
| 197 | 6,4 | 16 Aralık 1727: Yavuz Selim semti, İbrahim'in evinde tezgâhlar | 634; geride ikinci pres taban−16'da (küçük, derinlik) | 2.6 / 8 | iki pres zıt fazda basıyor, İbrahim'in kolu | 33 |
| 198 | 8,9 | 31 Ocak 1729: iki ciltlik Vankulu, ilk sayfada ferman (yakın) | 634; rahle ve yatık cilt zeminde | 3.0 / 4 | sayfa köşesi, kandil | 34 (A), 35 |
| 199 | 4,1 | Pres kendi iznini basıyor: tuğralı sayfa | 634; pres ve baskıcı zeminde, tuğralı sayfa tablanın ucunda dik | 3.0 / 6 | pres basıyor | 36 (A) |
| 200 | 7,3 | Hattatlar rahle başında | 634; minderler ve rahleler zeminde | 2.8 / 8 | iki kalem farklı fazda yazıyor | 37 |
| 201 | 6,2 | Târîh-i Hind-i Garbî: tahta baskı resim (yakın) | 634; rahle zeminde | 3.0 / 4 | sayfa köşesi, kandil | 38 |
| 202 | 5,4 | 1742: tezgâhlar susuyor | 634; pres ve tozlu yığın zeminde | 2.8 / 4 | yalnız kandil (bilinçli durgunluk) | 39 (K) |
| 203 | 8,1 | 1745, Yalova: kâğıthane, yaşlı İbrahim ve Lehistanlı usta | 632; kâğıthane ve oluk taban−36'da (geride, derinlik); kişiler önde | 2.4 / 8 | çark oluktaki suda döner, su dökülür, ustanın kolu, çimen | 40 |
| 204 | 5,3 | 1 Nisan 1747: depoda miras dökümü | 634; raf, yığınlar, kâtip ve rahle zeminde | 2.8 / 6 | kâtibin kalemi | 41 (K) |
| 205 | 5,7 | Tozlanan raflar | 634; tozlu raflar ve yığın zeminde | 2.8 / 4 | yalnız kandil | 42 (K) |
| 206 | 11,0 | Bugün: arşivde Kathryn Schwartz | 634; arşiv rafı, Schwartz ve masa zeminde | 2.8 / 6 | belgeyi tutan kol, lamba ışığı | 43, 44 (A) |
| 207 | 7,4 | Sahaf tezgâhı: kopyacı satıyor, alıcı az | 632; tezgâh ve sundurma direkleri zeminde; orta plan duz(588) evler | 2.6 / 8 | satıcının kolu | 45 |
| 208 | 7,4 | Şafak: kitaplarını alan bir alıcı yürüyor (erken gelen) | 632; orta plan duz(588): ev; güneş ufukta (y 552, tepelerin ardında) | 2.6 / 8 | alıcı sağa yürür (x 225→315), kitaplar elinde sallanır | 46 (A), 47 (A) |
| 209 | 9,3 | Üç belge yan yana: tek paragraf, Öklid'deki ferman, sözlükteki fetva | 634; üç rahle zeminde | 2.4 / 4 | sayfa köşeleri, kandil | 48, 49 (A) |

## Kurgu notları

- **Motif "fermanı gören yok"** üç kez aynı görsel dille dönüyor. 171'de boş rahle ve kandil var (kart 3). 181'de boş rahlenin yanında açık Öklid duruyor (kart 17). 206'da arşivde belgeyi okuyan tarihçi görülüyor (kart 44). Son sahne 209 üçünü birleştiriyor: tek sayfa, Öklid'in içindeki ferman ve sözlüğün başındaki fetva yan yana.
- **Yasağa karşı belgeler:** Matbaa yasaksa basılmaması gereken her baskı sahnesinde tahta pres çalışıyor. 1493 Nahmias (176), 1567 kilisede Abgar ve oğlu (178), 1627 Pera'da Metaksas (182), 1720 Paris (194), 1727 İbrahim'in evi (197) ve kendi iznini basan pres (199) böyle. Pres 202'de susuyor: boş tabla ve örümcek ağı.
- **Tempo:** Hikâye bölümlerinde sahne başına 1-2 kart var. Yakın plan belge sahneleri (180 Öklid, 198 Vankulu, 201 resimli kitap) ile kalabalık sahneler sırayla geliyor. Yürüyüş sahneleri sahneler arasına nefes olarak konuldu: 174 Thevet, 185 Marsigli, 189 "bir adamı izleyin", 191 Kolozsvár'dan gelen genç, 208 şafak.
- **Zaman ve ışık dili:** Paris sahneleri gece ve mumlu, İstanbul sokakları gündüz. Pera'nın kapatılışı karlı bir kış gecesinde geçiyor. "Bir adamı izleyin" alacakaranlıkta, kapanıştan önceki "İbrahim sadece erken gelmişti" ise şafakta: güneş ufukta doğuyor, yazı bandının çok altında.

## Grafiker notlarına uyum (4-kalite-metin.md, madde 8)

- Kart 5 Thevet'in sözü. Sahne 173'te Thevet masasında tüy kalemle yazıyor, yanında açık basılı kitap duruyor. İddia onun kâğıdında gösteriliyor, olgu gibi değil. 1483 yalnızca bu kartta.
- Kart 16: Öklid'in 453. sayfası sahne 180'de yakın planda. Sağ sayfada tuğralı izin fermanı, sol sayfada geometri çizimleri var.
- Kart 34-35: sahne 198, Vankulu'nun ilk sayfası. Sol sayfada tuğralı ferman, sağda tezhipli başlıklı fetva var; ikinci cilt yanda.
- Kart 38: sahne 201, Târîh-i Hind-i Garbî'nin tahta baskı gemi resmi.
- Kart 40: sahne 203, Yalova kâğıthanesi, Lehistanlı usta ve yaşlı İbrahim.
- Kart 37: sahne 200'de yalnızca rahle başında kalem tutan iki hattat var. Tabut, cenaze ve kalabalık yok.
- Kart 41-42: ölüm gösterilmiyor. 204'te kâtip dökümü yazıyor, 205'te yalnızca tozlu raflar ve yığınlar var.
- Ekrana girmeyenler: 1485, Vankulu adedi, kopyacı sayısı, "11 ay" ve ölüm yılı ekranda yok. Kitap yığınları sayı ima etmiyor.

## Kişiler (renk kimliği bütün sahnelerde aynı)

| Kişi | Görünüm |
|---|---|
| André Thevet | kahverengi Fransisken cüppe, geniş kenarlı siyah şapka, kır sakal |
| Marsigli | kırmızı ceket, siyah şapka, sakalsız, altın kemer |
| Nahmias kardeşler | lacivert ve kahverengi cüppe, koyu başlık, sakallı |
| Abgar ve oğlu | mor-siyah cüppe, kalpak; oğul daha küçük ve sakalsız |
| Metaksas | siyah rahip cüppesi ve siyah başlık |
| Cizvitler | siyah cüppe ve siyah şapka |
| İbrahim (Kolozsvár'dan gelen genç) | lacivert mente, kalpak, sakalsız |
| İbrahim Müteferrika | kahverengi kaftan, beyaz sarık, koyu sakal (1745'te ak sakal) |
| Said Efendi | mor kaftan, sarık, sakalsız (genç) |
| Şeyhülislam | beyaz cübbe, ak sakal |
| III. Murad / III. Ahmed | kırmızı / mavi kaftan, büyük sarık |
| Kathryn Schwartz | bugünün kıyafeti, açık başlı, omza inen saç |

## Yeni figürler (hepsi `matbaa_yasagi.py` içinde; ciz.py'ye eklenmedi)

Hepsi `piksel()`, `hex2()`, ImageDraw ve mevcut figürlerle yazıldı.

- **tahta_pres**: tahta el baskı presi (yeni figür isteği karşılandı), boyu kişi ölçeğinde yaklaşık 19 s, yani insan boyunda.
  - İki dikme kızaklarla zemine basar.
  - Tabla baskıcının karşı yanına uzanır, iki uç ayağı yere iner.
  - Plaka faz ile iner kalkar.
  - Demir kol vidadan baskıcının eline bağlıdır (`_pres_sahnesi`). El noktası `timur_figur.kisi` ile aynı formülden hesaplanır, kol hiçbir karede havada kalmaz.
  - Seçenekler: `tugra=True` dik duran basılmış sayfaya tuğra çizer; `ag=True` örümcek ağı ekler; `kagit=False` tablayı boş bırakır.
- **sandalyeli + yazi_masasi**: sandalyede oturan Avrupalı yazar ve önündeki masa.
  - Sandalye ayakları, yazarın ayakları ve masa ayakları zemine basar.
  - Eldeki tüy kalem masa üstünde yazar.
  - Masada kâğıt, hokka, mum, kitap yığını, kitap sehpasında açık basılı kitap ya da arşiv belgesi bulunabilir.
- **acik_kitap**: rahlede açık kitap; çapraz ayaklar zemine basar. Sayfa türleri: Öklid, Vankulu, resimli tarih, İbranice ve Gutenberg sayfası ile tek yaprak (Thevet'in tek paragrafı). `bos_rahle`: boş, açık kanatlı rahle (motif). `_tugra`: küçük tuğra işareti.
- **kurutma_ipi**: iki direk zemine dikili; ipte mandallı sayfalar asılı ve hafifçe sallanıyor.
- **raf**: tür olarak kitap, yığın ya da arşiv (metal raf, etiketli kutular); tozlu seçeneği var. **kitap_yigini**: her kitap bir alttakine oturur. **cilt**: yere yatık kalın cilt. **kitap_bohcasi**: alıcının elinde ip bağlı deste; elin yürüyüşte sallanan konumuna bağlı.
- **ahsap_ev**: cumbalı iki katlı İstanbul evi, karlı dam seçeneğiyle. **saray_kapisi**: Bâbüsselâm'dan esinli; iki sekizgen kule, kurşun külahlar ve kapı üstünde tuğra. Mimari ayrıntı temsilîdir.
- **kagithane**: taş değirmen evi ve su çarkı. Çarkın alt yayı, dikmeleri zemine basan tahta oluğun suyunda döner. Oluğun ucundan dökülen su yerde küçük bir gölcük yapar.
- **sunak**: örtülü masa, ucu genişleyen Ermeni haçı ve iki mum.
- **sahaf_tezgahi**: tezgâh ve sundurma direkleri zemine basar, üstünde el yazmaları durur.
- **erdel_besigi**: beşik `timur.besik` yerine yazıldı. Eski çizimde kızak yayının altı zemin satırının altında kaldığı için beşik havada duruyormuş gibi görünüyordu (öz denetimde fark edildi). Yeni beşik kızak çemberinin merkezi çevresinde ±6° döner, kızağın en alt noktası her karede zemine değer.
- **modern_kisi**: bugünün insanı: kemersiz, açık başta saç, beyaz yaka. **sarkit_lamba**: arşivin tavan lambası; kablo tavandan iner.
- **osmanli_camii**: takiyuddin_rasathanesi.py'deki onaylı figürden kopyalandı.
- Ölçek ve kadraj yardımcıları cem_sultan.py ve takiyuddin_rasathanesi.py kalıbından kopyalandı: `olcek`, `s_kisi`, `s_oturan`, `_kz`, `_kadraj`.

## Grafiker öz denetimi

**Otomatik denetimler (betik her sahnede çalıştırır, biri bozulursa durur):**

1. **taban_denetimi:** her karede en alt opak piksel son satırda; havada sprite yok. Yapılar `duz_zemin` ile yalnızca düz zemine kuruluyor.
2. **Kadraj:** opak piksellerin en az %70-80'i görünür aralıkta (sahne sonundaki %6 yakınlaşma dahil). Hiçbir figür sprite'ın üst kenarına değmiyor, yani kesik baş yok.
3. **Yazı bandı:** her kartın gerçek satır sayısı ve boyu, yaziY, yakin ve 1,06·yakin değerleriyle hesaplanan bant dünya koordinatına çevrildi. Bantta sprite'ın her 3 karesinde ve orta planda, görünür sütunlarda satır başına 2 pikselden fazla opak piksel yok. 1 px'lik kandil zinciri bilinçli bir istisna.
4. **Görünürlük:** orta plandaki önemli yapılar (cami, saray kapısı, ev) görünür aralıkta. Burada Remotion'un gerçek formülü kullanıldı: [sx − sx/z, sx + (540 − sx)/z].
5. 40 sahnenin hepsi hatasız çizildi. `cd video && npx tsc --noEmit -p .` temiz geçti.

**Gözle denetim:** Remotion kamerasını taklit eden bir önizleme betiğiyle katmanlar birleştirildi: büyütme, odak ve yazı bandı kutusu dahil. 40 sahnenin hepsinin bir karesi açılıp bakıldı. Pres, yürüyüş ve beşik sahnelerinin ayrıca farklı kareleri incelendi: 0, 3, 6, 9, 12, 14 ve 18. Kareler, yürüyüşlerde yolun başı ve sonuyla birlikte açıldı. Bakılanlar: zemin, ölçek, kenarda kesilme, havada nesne, kontur, yazı ile çakışma.

**Düzeltilenler:**

- **190 beşik:** `timur.besik`'in kızak yayının altı zemin satırının altında kalıyordu ve sepet havada asılı gibi görünüyordu. Yeni `erdel_besigi` yazıldı: kızak her karede zemine değiyor. Annenin beyaz başörtüsü yüzü bir blok gibi kapatıyordu; koyu mavi yapıldı.
- **171 / 181 boş rahle:** ilk çizimde iki kanat dik V ile çapraz ayaklardan oluşuyordu ve "iki X" gibi okunuyordu. Kanatlar kalın, sığ V biçiminde, ışıklı kenarlı, uç oymalı ve menteşeli olarak yeniden çizildi; şimdi rahle olarak okunuyor.
- **187, 195, 200, 204 rahle ölçeği:** rahleler kâtibin elinin çok altında, oyuncak gibi kalıyordu. Rahle ölçeği oturan figürün ölçeğine eşitlendi, kalem ucu rahledeki kâğıda iniyor.
- **174, 185, 191, 208 yürüyüş:** figür sprite'ın ortasında yürürken orta plandaki camiyi tam önünden kapatıyordu. Figür yerel x 170'e alındı, cami ve sur yolun sağına konuldu. Kamera figürü izlerken yapı kadraja giriyor. Yolun başı ve sonu ayrı ayrı denetlendi.
- **191:** cami surun arkasında kalıp görünmüyordu. Cami arka zemine (y 580) ve daha büyük ölçekle alındı; kubbe ve minare surun üstünden görünüyor.
- **175:** rehber camiyi kapatıyordu. Turistler sola, rehber ortaya, cami sağa alındı.
- **177:** kuruyan sayfalar kitabın arkasında kayboluyordu. İp yükseltildi ve kitap küçültüldü; sayfalar kitabın üstünde görünüyor.
- **192:** iki figür saray kapısını kapatıyordu. Figürler kapının iki yanına açıldı.
- **197:** ikinci presin kolu İbrahim'in eline değiyormuş gibi görünüyordu. Sahne yeniden kuruldu: ön pres sağda, baskıcı sağda, İbrahim solda, ikinci pres geride ve daha yüksek zeminde, küçük.
- **203:** kâğıthane insanların yanında oyuncak gibi kalıyordu (kapı insan boyunun beşte biri). Kâğıthane geriye, daha yüksek bir zemin çizgisine alındı (taban−36, derinlik kuralı). Usta ile İbrahim birbirinden ayrıldı.
- **208:** güneş kadraj dışındaydı. Güneş görünür bölgeye, ufka (y 552, tepelerin ardından doğuyor) alındı; yazı bandının çok altında. Alıcının kitap destesi, yürürken sallanan elin konumuna bağlandı, elden kopmuyor.
- **209:** soldaki "tek paragraf" çok küçük bir rahlede kalıyordu. Aynı ölçekte rahle üstünde tek yaprak ("tek" sayfa türü) çizildi; üç belge aynı dilde.

**Bilinen sınırlar (kalite kontrolün bilgisine):**

- Yüz ifadesi ve profil motorda yok, sahneler mizansenle anlatılıyor.
- Saray kapısı ve kâğıthane mimarisi temsilî, belgeye dayanmıyor.
- Kart 7-9'daki "bugün" sahnesi bugünün İstanbul'unda bir rehber ve iki turist.
- Root.tsx kaydı ve render kod tarafına kalıyor.
