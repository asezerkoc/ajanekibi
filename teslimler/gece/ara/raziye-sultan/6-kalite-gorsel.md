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
