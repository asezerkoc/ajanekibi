# 🔴 Kalite Kontrol (görsel) · Raziye Sultan: "Oğullarımdan İyi"

**İş:** Konu 3, slug `raziye-sultan` · **Hazırlayan:** 🔴 SKONSTART Kalite Kontrol · **Tarih:** 31 Ekim 2026
**Girdiler:** `5-grafik.md` (sahne planı, 39 sahne), `4-kalite-metin.md` (51 kart), 12 render karesi (`qc-raziye-sultan/kare-*.png`) ve kontak sayfası.
**Ek kareler (8, kendim render ettim):** kapak (kare 60), 210 Cuma kalabalığı (543), 227 fil (6349), 230 Yakut ve ahırlar (7391), 235 Altuniya ile evlilik (9672), 236 Kaithal (10027), 240 köylü ve ekmek (11530), 248 son soru (15150). Kare = (başlangıç + süre/2) × 60.
**Bakılmayanlar:** 233 (Bathinda hapsi) ve kapanış kartı. Sınır 8 kareydi. Bathinda'yı 232 (kare-136s) temsil ediyor; kapanış kartının arka planı 241 ve kare-195s'de görülüyor.
**Geçiş kareleri:** kare-019s, 039s, 175s ve 195s'deki yarı saydamlık geçiş efekti. Bu karelerde yalnızca katı figürleri değerlendirdim.

## Karar: UYGUN DEĞİL (revize_birimi: grafiker)

Tek bir nesne havada durmuyor, bütün yazılar okunuyor. Ama sahibin daha önce reddettiği hatalardan biri, **gözsüz yüz**, dört karakterde var: Şah Terken, Altuniya, Yakut ve filbaşı. Altuniya ve Yakut hikâyenin ana karakterleri. Ayrıca bir figürde saydam delik, dönem dışı bir taç ve okunmayan bir ordu var. Sahibin 03:40 notu ("tek bir hatalı kare bile kabul değil") gereği iş geri dönüyor.

## Zorunlu düzeltmeler (kare | yer | sorun | düzeltme)

| # | Kare | Yer | Sorun | Düzeltme |
|---|---|---|---|---|
| 1 | kare-058s (sahne 219; aynı figür 221'de de var) | Sağ, Şah Terken'in başı (x≈790-910, y≈820-880) | **Gözsüz yüz.** Mürdüm örtünün içindeki yüz düz ten rengi bir dikdörtgen: göz yok, ağız yok. Kadın sola dönük, kolu uzanmış, ama yüzü ifadesiz bir maske. | Raziye'nin peçeli yüzündeki gibi bakış yönüne (sola) en az 2×2 px koyu göz koy. Gerekirse açık renkli bir göz akı pikseli ekle. 219 ve 221'de kontrol et. |
| 2 | kare-058s (sahne 219) | Şah Terken'in çenesinin altı (x≈820-900, y≈880-905) | **Saydam delik.** Çene ile giysi arasında figürün içinden arka plan (pencerenin noktalı deseni) görünüyor. | Boyun ve yaka bölgesini örtü rengiyle doldur. Figürde opak olmayan iç piksel kalmasın. Bu kontrol `taban_denetimi`ne benzer bir iç-boşluk denetimi olarak betiğe eklenebilir. |
| 3 | ek-09672 (235), ek-10027 (236); 237'de de aynı figür | Sol, Altuniya'nın başı (x≈345-425, y≈745-795) | **Gözsüz yüz.** Kalpak göz hizasına kadar iniyor, siyah sakal hemen altından başlıyor. Arada kalan ince ten şeridinde göz pikseli yok (piksel taramasıyla doğrulandı). Raziye'nin evlendiği adam yüzsüz görünüyor. | Kalpağı 3-4 px yukarı al ya da sakalı aşağı başlat. Göz hizasına koyu göz ve açık göz akı koy. 235, 236 ve 237'nin hepsinde kontrol et. |
| 4 | ek-07391 (sahne 230) | Sol, Yakut'un başı (x≈150-280, y≈1000-1040) | **Yüz okunmuyor.** Büyük sarık kaşa kadar iniyor, siyah sakal hemen altında. Koyu ten (106,68,40) üstündeki göz (43,26,18) telefonda görünmüyor. Kartın konusu Yakut olduğu hâlde yüzü yok. | Sarığı küçült ya da yukarı al. Koyu tenli figürlerde göze açık renkli göz akı pikseli ekle (ör. #e8e0d0 + koyu bebek). Yakut başka sahnede de varsa (231) orada da uygula. |
| 5 | ek-06349 (sahne 227) | Filin boynundaki filbaşı (x≈640-740, y≈620-700) | **Gözsüz yüz.** Sarık ve sakal arasında 1-2 px'lik ten şeridi var, göz yok. | 4. maddedeki çözüm: sarığı kaldır, göz ve göz akı ekle. |
| 6 | ek-15150 (sahne 248) | Sehpanın sağı, taç (x≈560-760, y≈1010-1110) | **Dönem dışı nesne.** Beş sivri dişli taç Avrupa ortaçağ kraliyet tacı. Delhi Türk sultanları böyle taç takmıyordu. Videonun kapanış sorusu bu nesnenin üstünde duruyor. | Yastığa Raziye'nin kendi külahını koy: videoda giydiği lacivert-mor, kürk kenarlı, altın süslü külah. İstersen mücevherli sorguç ekle. "Peçe mi, taç mı" sorusu Raziye'nin iki başlığını yan yana koyarak hem dönemle hem videonun görsel diliyle uyumlu olur. |
| 7 | ek-10027 (sahne 236) | Sağ kenar, Behram Şah'ın ordusu (x≈900-1080, y≈870-1080) | **Kart okunmuyor ve kenarda kesik figür var.** Kart "Behram Şah'ın ordusu karşılarında" diyor. Ama ordu, Raziye'nin beyaz atının başının arkasında kalıyor; görünen 2-3 minik atlı da sağ kenarda yarıya kadar kesiliyor. İzleyici bir ordu görmüyor. | Ordu sırasını beyaz atın başından ayır: atlıları sola ya da daha uzağa (yukarı) al, veya Raziye ile Altuniya'yı biraz sola kaydır. Sıranın son figürü kadrajın içinde bitsin. Kamera sonunda (yakin·1,06) da ordu görünür ve kesiksiz kalsın; `_gorunur` listesine ordunun bütün x'lerini ekle. |
| 8 | kare-078s (sahne 222) | Arka plan, bütün oda | **Sahne kartla uyuşmuyor.** "Hapiste ölüyor" kartının arkasında yıldızlı gökyüzü gösteren üç büyük sivri kemerli saray penceresi var. Mekân zindan değil, saray salonu gibi okunuyor. Kartta söz edilen saman da yerde birkaç noktadan ibaret. | 222'de saray penceresi kullanma: yüksekte tek küçük, parmaklıklı pencere ya da kapıda demir parmaklık koy. Fîrûz'un altında saman yığınını görünür kıl. 233'teki (Bathinda kale odası) pencereleri de aynı gözle kontrol et. |

## İyileştirme önerileri (ret nedeni değil)

- **Kapak (ek-00060):** Başlık okunuyor, logo bandıyla çakışmıyor. Ama "Oğullarımdan / İyi" ile alt başlık "Delhi tahtındaki tek kadın" aynı boyda ve aynı renkte. Tek başına kalan "İyi" satırı da boşlukta duruyor. Başlığı tek satıra al ("Oğullarımdan İyi") ve biraz büyüt; alt başlığı küçült ya da beyaz yap. Hiyerarşi netleşir.
- **ek-07391 (230), ölçek:** Atlı Raziye'nin gövdesi, yanında duran Yakut'tan yaklaşık 1,5 kat büyük görünüyor. Bunun nedeni kütüphanedeki `atli` oranı. At-Yakut oranı doğru. Yakut'u (K) biraz büyütmek denge sağlar.
- **kare-136s (232):** Sağ gerideki binicisiz at, muhafızın arkasından yalnızca beyaz sağrısı ve kuyruğuyla görünüyor. Koyun gibi okunabiliyor. Planda "at başı önde" yazıyordu; atı muhafızın sağına çıkar ki başı ve eyeri görünsün (Yakut'un ölümünün tek anlatıcısı bu). Kale kapısı da sol muhafızın arkasında kaybolmuş.
- **kare-039s (216) ve kare-117s (229):** İki anonim emîr aynı kalıptan çıkmış; yalnızca giysi rengi farklı. Birine kalpak, diğerine börk ya da farklı sakal ver.
- **kare-156s (234) ve kare-234s (246):** Behram Şah ve Nâsıreddin aynı tahtta, aynı sarık, aynı sakal ve aynı oturuşla çizilmiş; yalnızca giysi rengi farklı (yeşil ve lacivert). İkisi de Raziye'nin kardeşi ve iki ayrı sultan. Birine farklı başlık ya da sakal rengi vermek karışıklığı önler.
- **ek-06349 (227):** Fil grubu kadrajın yaklaşık %30'u. Kart "Yüzü açık" diyor, ama Raziye'nin yüzü yaklaşık 50 px'le küçük kalıyor. Bu kart için kamerayı hevdece biraz daha yaklaştırmak vurguyu güçlendirir. Grafiker bunu bilinçli karar olarak not etmiş.
- **kare-039s (216):** İltutmış'ın altın pelerininin alt ucu, iki figürün bacakları arasında yerden kopuk bir altın blok gibi görünüyor. Gözle bakınca pelerin olduğu anlaşılmıyor; ya kısalt ya da omuzdan aşağı kesintisiz göster.

## Değerlendirme (sahibe gösterilecek)

Video tarz olarak tutarlı ve güçlü. Raziye'nin peçeli ve peçesiz hâli bütün sahnelerde tanınıyor. Fil, atlar, sikke, darphane ve mezar avlusu zemine oturuyor, havada duran nesne yok. Bütün kartlar okunaklı ve Türkçe karakterler doğru. Ancak dört karakterin yüzü gözsüz ya da okunmaz çizilmiş (Şah Terken, Altuniya, Yakut, filbaşı). Bu, daha önce reddettiğiniz bir hata. Ayrıca son sorudaki Avrupa tipi taç dönem dışı, Kaithal sahnesinde ordu görünmüyor ve zindan saray salonu gibi duruyor. Sekiz düzeltmenin hepsi küçük, figür ve sahne düzeyinde. Grafiker düzelttikten sonra aynı kareleri yeniden kontrol edeceğim.

## 2. tur

**Tarih:** 31 Ekim 2026 · **Girdiler:** `5-grafik.md` içindeki "Görsel KK revizyonu" bölümü, 22 sahne ortası karesi (`qc-raziye-sultan/r2/sahneNNN.png`). **Ek kareler (4, kendim render ettim):** 236'nın son karesi (10190), 220'nin başı (3840) ve sonu (4065), 237'nin başı (10215). Yüzleri 4 kat piksel yakınlaştırmasıyla kontrol ettim (227, 215, 218, 220, 234, 237).

### Karar: UYGUN DEĞİL (revize_birimi: grafiker)

İlk turdaki 8 düzeltmenin 8'i de yapılmış ve doğru. Ama bu turda iki yeni hata çıktı. 237'de Raziye'nin gövdesi bacaklarından kopuk, aradaki boşluktan zemin görünüyor. 220'de ise kartın öznesi Raziye sahnenin başından sonuna kalabalığın arkasında kalıyor ve yüzü görünmüyor. Sahibin "tek bir hatalı kare bile kabul değil" notu gereği iş geri dönüyor.

### İlk turun 8 düzeltmesi: doğrulama

| # | Sahne | Sonuç |
|---|---|---|
| 1 | 219, 221 Şah Terken | ✔ Örtü alından başlıyor. Göz akı ve bebek görünüyor. |
| 2 | 219 çene altı | ✔ Saydam delik kapanmış, boyun örtüyle dolu. |
| 3 | 235, 236, 237 Altuniya | ✔ Kalpak yukarıda. Üç sahnede de göz akı ve bebek var. |
| 4 | 230 Yakut | ✔ Küçük sarık kaşa inmiyor. Koyu tende açık göz akı seçiliyor. Yakut ile atlı Raziye artık aynı ölçekte, emîrler ovanın gerisinde. |
| 5 | 227 filbaşı | ✔ Yakınlaştırmada sarığın altında göz akı ve bebek görünüyor. |
| 6 | 248 taç | ✔ Avrupa tacı kaldırılmış. Sehpada peçe ve külah yan yana, ikisi de sehpaya oturuyor. |
| 7 | 236 ordu | ✔ Mızraklı atlılar ve yaya sırası sağ geride, at başının arkasında kalmıyor. **Son karede (10190)** ordunun tamamı kadrajda; en sağdaki atın kuyruğu x≈1050'de bitiyor, kesik figür yok. |
| 8 | 222 zindan | ✔ Kesme taş duvar, parmaklıklı mazgal ve hücre kapısı var, saray penceresi yok. Fîrûz görünür saman yığınının üstünde oturuyor. 233'te de aynı katman kullanılmış, mazgal Raziye'nin baktığı tarafta. |

Yalnızca göz ve boyun kuralı yüzünden yeniden çizilen kareler (210, 214, 215, 217, 218, 220, 238, 239) ve 216, 229, 234, 246: gözsüz yüz, havada nesne, yazı bandına giren nesne ya da dönem dışı öğe yok.

### Zorunlu düzeltmeler (kare | yer | sorun | düzeltme)

| # | Kare | Yer | Sorun | Düzeltme |
|---|---|---|---|---|
| 1 | r2/sahne237.png ve ek-10215 (sahne 237) | Raziye'nin eteği ile bacakları arası (x≈760-930, y≈1120-1140) | **Gövde bacaklardan kopuk.** Mavi tuniğin alt konturu y≈1123'te bitiyor, bacaklar y≈1143'te başlıyor. Arada yaklaşık 18 px zemin rengi var (piksel taramasıyla doğrulandı). Sahnenin başında ve ortasında aynı durum var; Raziye'nin üst gövdesi havada duruyor gibi. Yanındaki Altuniya'da bu sorun yok. | Ayakta duran `RAZ` (`kadin=True, uzun=False`, kısa tunik) kalıbı tuniği kısaltıyor ama bacakları uzatmıyor. Tuniği bacak başlangıcına kadar indir ya da bacakları yukarı uzat. Aynı kalıp 232 (x=196), 240 (x=166) ve 245 (x=222) sahnelerinde de kullanılıyor; sprite'larda aynı boşluk görünüyor, üçünü de düzelt. Gövde ile bacak arasında saydam satır bırakmayan bir denetimi betiğe ekle. |
| 2 | r2/sahne220.png, ek-3840, ek-4065 (sahne 220) | Sol orta, kalabalığın arkası (x≈260-330, y≈870-1060) | **Kartın öznesi görünmüyor.** Kart "Raziye halka sesleniyor" diyor. Peçeli Raziye sekide ama sahnenin başında, ortasında ve sonunda yüzü önündeki kalpaklı emîrin başının arkasında kalıyor; yalnızca peçesinin kenarı görünüyor. İzleyici halka seslenen kadını görmüyor. | Raziye'yi ve sekiyi yürüyen kalabalıktan ayır. Sekiyi yükselt (Raziye'nin başı kalabalığın başlarından yukarıda olsun) ya da Raziye'yi kalabalığın boş kalan sol veya sağ ucuna al. Yüzü ve kalkık kolu sahnenin tamamında açık kalsın. `_gorunur` denetimine Raziye'nin baş kutusunun önündeki figürlerle çakışmamasını ekle. |

### İyileştirme önerileri (ret nedeni değil)

- **Büyük sarıklı figürler (215 İltutmış, 218 Fîrûz, 234 Behram Şah, 246 Nâsıreddin):** Göz akı sarığın alt kenarına yapışık. Krem rengi sarıkla birleşiyor, bu yüzden göz tek bir koyu nokta gibi okunuyor. Bebek görünüyor, yani gözsüz değil. Gözü 1 px aşağı alırsan yüzler 216 ve 219'daki kadar net olur.
- **222:** Muhafızın meşalesi neredeyse kendi boyu kadar uzun (sap y≈580-990). Üçte bir kısaltmak ölçeği daha inandırıcı yapar.
- **237:** Sağ gerideki kaçan askerin başı Raziye'nin uzattığı kolun ucuna değiyor. Askeri biraz sağa ya da uzağa al.
- İlk turdaki kapak önerisi `RaziyeSultan.tsx`'e dokunma yasağı yüzünden yapılmadı. Not olarak geçerliliğini koruyor.

### Değerlendirme (sahibe gösterilecek)

İlk turda istenen sekiz düzeltmenin hepsi yapıldı. Şah Terken, Altuniya, Yakut ve filbaşının artık gözleri var, son sorudaki Avrupa tacının yerini Raziye'nin kendi külahı aldı, Kaithal'da Behram Şah'ın ordusu sahnenin sonuna kadar görünüyor ve zindan gerçekten zindan gibi duruyor. Ancak yeniden çizimde iki yeni hata çıktı. Ordugâh sahnesinde (237) Raziye'nin gövdesi bacaklarından kopuk duruyor; aynı çizim kalıbı üç sahnede daha kullanılıyor. "Raziye halka sesleniyor" sahnesinde (220) ise Raziye kalabalığın arkasında kalıyor. İkisi de tek bir figür kalıbı ve yerleşim düzeltmesi. Grafiker düzelttikten sonra 220, 232, 237, 240 ve 245'i yeniden kontrol edeceğim.

## 3. tur: UYGUN
Tunik ve bacak boşluğu (232, 237, 240, 245), 220'deki görünürlük, zindan ve gözler yeni karelerde kontrol edildi, hepsi düzelmiş. Son ölçek düzeltmeleri:
- 215: Raziye, atlıyla aynı zemin çizgisinde yetişkin kadın boyunda duruyor.
- 220: Raziye, sekinin üstünde kalabalıktan yüksekte ve önü açık; halka seslenen sultan olarak okunuyor.
Kalan zorunlu düzeltme yok. Video çıktısı alınabilir.
