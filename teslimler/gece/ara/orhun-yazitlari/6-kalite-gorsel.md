# 🔴 Kalite Kontrol (görsel): Taş Konuşuyor (Orhun yazıtları ve Vilhelm Thomsen, 1893)

**İncelenen:** 12 render karesi (`qc-orhun-yazitlari/kare-018s … kare-224s`), kontak sayfası, ayrıca 6 ek kare:
kapak (`ek-00060`, 1,0 sn), sahne 136 (`ek-03058`, 51,0 sn), 140 (`ek-04620`, 77,0 sn), 150 (`ek-09519`, 158,7 sn),
155 (`ek-11916`, 198,6 sn), kapanış (`ek-14730`, 245,5 sn). Sahne zamanları `sahne_zaman.py` çıktısından.
Kare ↔ sahne ↔ kart eşleşmesi: 018s=131/kart 3, 037s=134/7, 056s=137/11, 074s=139→140 geçişi (crossfade, efekt; kart yok),
093s=141/16, 112s=144/19, 130s=146/22, 149s=149/25, 168s=151/28, 186s=153/32, 205s=156/36, 224s=158/39;
ek kareler 136/10, 140/14, 150/27, 155/35. Bakılan bütün karelerde kart doğru sahnede.

## Karar: UYGUN DEĞİL (revize_birimi: grafiker)

Havada duran nesne ya da okunmayan yazı yok. Ama 5 karede sahibin göreceği çizim hatası var: yanlış ölçekte bir figür,
yüzü olmayan bir figür, sahnenin konusu olan taşın görünmemesi, 1890 için yanlış fotoğraf makinesi ve kapakta ne olduğu
anlaşılmayan, uçan daireye benzeyen bir nesne. Sahibin 03:40 notu ("görselde tek bir hatalı kare bile kabul değil") gereği iş geri dönüyor.

## Zorunlu düzeltmeler (kare | yer | sorun | düzeltme)

| # | Kare | Yer | Sorun | Düzeltme |
|---|---|---|---|---|
| 1 | `ek-03058` (sahne 136, 48,3-53,6 sn) | Sol-orta, sedir üstü (x 220-720, y 1040-1160) | Yatan Bilge Kağan'ın başı (~65 px) ayaktaki hizmetkârın başının (~135 px) yarısı; gövde de hizmetkârdan belirgin kısa. Sakal yana, battaniye boyunca gaga gibi uzanıyor. Kağan çocuk ya da oyuncak gibi okunuyor (yanlış ölçek). | Yatan figürü hizmetkârla aynı `K` ölçeğiyle çiz: baş aynı boyda, boy (baş+gövde) hizmetkârın şapkasız boyu kadar (~560 px). Sırtüstü yatana uygun olarak sakal yukarı, tavana doğru dursun ya da çıkarılsın. Sedir boyu yeni gövdeye göre uzatılsın; ayaklar yine zeminde kalsın. |
| 2 | `ek-09519` (sahne 150, 154,9-162,4 sn) | Sol kenar (x 35-250, y 650-1300) | Sahnenin konusu olan yazıt taşı fotoğraf makinesinin ve makaralarının arkasında kalmış, neredeyse görünmüyor. Makinenin objektifi sola, kadraj dışına bakıyor; taş makinenin arkasında kalıyor. Plan "hepsi taşa bakar, makine taşa dönük" diyor. | Taşı makinenin önünden çek: 144'teki gibi taş solda ve açıkta dursun, tripod onun sağında, objektif taşa (sola) baksın. Taşın ön yüzü ve harfleri görünür olsun, hiçbir figür ya da makine harfli yüzü örtmesin. |
| 3 | `kare-112s` (sahne 144, 107,2-114,0 sn) ve `ek-09519` (sahne 150) | Tripodlu makine (112s: x 320-540, y 735-1305; 150: x 35-255) | Çizilen makine, üstünde iki film makarası olan sinema kamerası (grafikerin notu: 1941 film kamerası çizimi). 1890-91'de Fin seferi levhalı fotoğraf makinesi kullanıyor, kart da "Fotoğraf çekiyor" diyor. Tarih izleyicisinin göreceği bir dönem hatası. | Makaraları kaldır; tripod üstünde ahşap kutu, körüklü öne uzanan objektif ve arkada siyah örtü olan bir levhalı fotoğraf makinesi çiz (`kisi(silah="kamera")` yerine yeni bir `fotograf_makinesi` figürü; tripod ayakları yine zeminde). |
| 4 | `ek-00060` (KAPAK) ve sahne 130 (0-10,4 sn) | Sağ-orta (x 845-985, y 935-1065) | Uzaktaki ovoo (taş yığını, `taslar`, s=0,9) bu boyda gri bir disk, üstünde kubbe ve anten gibi bir uç: uçan daireye benziyor. Orta plan zemini düz yeşil olduğu için nesnenin yere bastığı da okunmuyor, havada asılı gibi duruyor. Videonun ilk karesi bu. | En temiz çözüm: ovoo'yu 130'dan çıkar (planda yok, hikâyeye gerek yok). Kalacaksa tanınır çiz: enine değil yukarı doğru sivrilen koni biçimli taş yığını, tepesinde dal ve mavi hadak bezi, altında belirgin, geniş temas gölgesi, en az 2 kat büyük. |
| 5 | `kare-186s` (sahne 153, 180,0-189,4 sn) | Sağ figür, kadın (x 830-960, y 750-890) | Kadının yüzünde göz yok: beyaz başörtüsünün alt kenarı göz satırını örtüyor, yüz boş bir ten rengi alan olarak kalmış. Yanındaki erkeğin gözü var, kadın yüzsüz görünüyor. | Başörtüsü alnın üstünde bitsin, yüz `kisi`deki gibi göz pikseliyle çizilsin. Göz taşa bakacak yönde, solda olsun. Başörtüsü beyaz kalabilir ama yüzü çerçevelesin, örtmesin. |

## İyileştirme önerileri (reddetme nedeni değil)

- **kare-037s (134):** Atın otlayan başı köşeli, kaba bir çokgen (x 190-520, y 880-1160); ağız ve burun belli değil, gem kayışı boyunda kalın bir siyah bant. Başı ağzı ve burnu belli bir profil olarak yeniden çiz; gemi başa al.
- **kare-056s ve kapak (130, 137):** Çiçekler ~180 px; insan ölçeğine göre ~1 m boyunda, taşın dörtte biri kadar. Ölçeği `0.32*K` yerine ~`0.15*K` yap.
- **Taş ölçeği tutarlılığı (112s, 186s, 150):** İnsanlı sahnelerde taş insan boyunda ya da ondan kısa, oysa yalnız olduğu sahnelerde (056s, 130s, kapak) kadrajın %35'ini dolduruyor. Grafikerin gerekçesi (yazı bandı) geçerli; yine de taşın daha geride durduğunu hissettirmek için taşın zemin çizgisini ufka biraz daha yaklaştır, ya da taşı yarım kadraj dışına taşırıp (sol kenardan girerek) tam boyuyla göster.
- **ek-04620 (140, Poltava):** Üç figürün başında da Amish/Püriten tipi yüksek, geniş kenarlı siyah şapka var. 1709'da üç köşeli şapka giyiliyor. Esir ile muhafızlar da birbirinden ayrılmıyor: Strahlenberg'in elleri bağlı değil, muhafızın onu tuttuğu da görülmüyor. Tüfekler planda yazdığı gibi omuzda değil, yere dayalı dik çubuk. Üç köşeli şapka varyantı ve önde bağlı eller önerilir.
- **ek-11916 (155):** Çin şehri yeşil konik kule çatılarıyla bir Avrupa şatosu gibi okunuyor; kapı insan boyunun yarısı kadar, perspektife göre küçük. Kıvrık saçaklı kapı kulesi ve biraz daha büyük bir kapı önerilir.
- **kare-149s (149):** Mumun pirinç tabağı masanın sağ kenarından ~20 px taşıyor (x 720-740). Mumu 30 px sola al.
- **Kopenhag ve Petersburg iç mekânları (018s, 149s, 224s):** Oda aynı (pencereler, kandil, döşeme). Figür de hep aynı pozda: sağda, elinde kırmızı noktalı boş bir kâğıt. Petersburg'da (158) duvar rengi ya da pencere biçimi değişsin; Thomsen 149'da albüme eğilsin.
- **kare-168s (151):** Akademideki ak sakallı dinleyici, Radloff'un figürüyle aynı. İzleyici onu Radloff sanabilir (Radloff orada değildi). Sakal rengini değiştir.
- **Kapak (ek-00060):** Kapak, kart yazısıyla aynı kutuda duruyor; logo ya da @pikseltarihim bandı yok. TSX yorumu "logo ve alt bandı kapak bileşeni ekler" diyor ama `seri.kapak` tanımlı olmadığı için hiçbir şey eklenmiyor. Ya yorum düzeltilsin ya da kapağa logo ve kanal adı eklensin.
- **Yeniden kontrol:** Bu turda 132, 133, 135, 138, 139, 142, 143, 145, 147, 148, 152, 154, 157, 159, 160 ve 161 sahnelerine kare düşmedi. Revizyondan sonra bunlardan da kare alınmalı.

## Değerlendirme (sahibe gösterilecek)

Video tarz olarak tutarlı: 64-bit piksel, belirgin konturlar ve şafak, gece, kar ve mum ışığı paletleriyle yüzyılların geçişi okunuyor. Taşın harflerinin altın ve kızıl ışıması anlatıyı güzel taşıyor. Bütün kartlar okunuyor, Türkçe harfler doğru, her kart doğru sahnede; havada duran nesne yok. Yine de beş karede gözünüze takılacak hata var: Bilge Kağan'ın ölüm sahnesinde kağan çocuk boyunda, Fin seferinde 1890'a uymayan bir sinema kamerası var, 150'de konuşulan taş kameranın arkasında kaybolmuş, 153'te kadın figürün yüzü yok, kapakta da ne olduğu anlaşılmayan, uçan daireye benzeyen bir nesne duruyor. Bunlar grafikere düzeltilmek üzere geri gönderildi; düzeltilmiş hâli yeniden kontrol edilmeden size gelmeyecek.

## 2. tur: UYGUN DEĞİL (revize_birimi: grafiker)

**İncelenen:** revizyondan sonra render edilen 28 sahne karesi (`qc-orhun-yazitlari/r2/sahne130 … sahne161`), kontak sayfası
`qc-orhun-r2.png` ve ek kapak karesi `r2/kapak.png` (60. kare). 1. turda hiç bakılmamış 16 sahneye de bakıldı (132, 133, 135, 138, 139, 142,
143, 145, 147, 148, 152, 154, 157, 159, 160, 161). 150, 135 ve 136 büyütülerek incelendi.

Beş zorunlu düzeltmeden dördü tam yapılmış. Beşincisi (150) yarım kalmış: taş artık görünüyor ama makinenin objektifi taşın harfli yüzüne
giriyor. 1. tur düzeltmesi "hiçbir figür ya da makine harfli yüzü örtmesin" diyordu; grafikerin notu da "harfli yüzü hiçbir şey örtmüyor" diyor,
ama karede durum bu değil. Sahibin "görselde tek bir hatalı kare bile kabul değil" notu gereği iş geri dönüyor. Kalan iş tek sahne ve küçük.

### 1. tur düzeltmelerinin durumu

| # | Sahne | Durum | Karede görülen |
|---|---|---|---|
| 1 | 136 | Yapıldı | `sahne136`: Yatan kağanın başı (~130 px) hizmetkârın başıyla (~120 px) aynı boyda; battaniye boyu ayaktaki hizmetkârın boyuna yakın. Yana uzanan sakal yok. Sedir ayakları ve hizmetkârın ayakları zeminde (hizmetkâr arka sırada, daha yüksek zemin çizgisinde). Çocuk ya da oyuncak gibi okunmuyor. |
| 2 | 150 | **Yarım** | `sahne150`: Taş ortada, açıkta ve büyük ölçüde görünüyor; objektif taşa dönük. Ama objektif ve körüğün ucu (x 390-515, y 870-950) taşın harfli yüzünün sağ yarısına giriyor, 4-6. satırlardaki son iki-üç harfi örtüyor. Objektif taşa dayanmış gibi duruyor. |
| 3 | 144, 150 | Yapıldı | `sahne144` ve `sahne150`: Makaralı sinema kamerası gitmiş. Yerine ahşap kutulu, körüklü, pirinç objektifli, üç ayaklı ahşap sehpalı levhalı makine var; sehpa ayakları zeminde. Döneme uygun. |
| 4 | 130 ve kapak | Yapıldı | `sahne130` ve `kapak.png`: Ovoo kaldırılmış, orta plan boş bozkır. Uçan daireye benzeyen nesne yok. Çiçekler de 0,15·K'ye inmiş (~100 px), insan ölçeğinde. |
| 5 | 153 (ve 154) | Yapıldı | `sahne153`: Kadının yüzünde göz var. Beyaz başörtüsü alnı örtüyor, yüzü iki yandan çerçeveliyor. `sahne154`: mavi başörtülü kadının da gözü görünüyor. |

1. turdaki iyileştirme önerileri de büyük ölçüde uygulanmış: 140'ta üç köşeli şapka, omuzda tüfek ve bağlı eller, iple çekilen esir; 155'te
kıvrık saçaklı kapı köşkü olan Çin suru; 149 ve 158'de mum masanın içinde; 151'deki dinleyicinin sakalı koyu; 158'de Petersburg odası yeşil
duvarlı ve penceresiz, Kopenhag'dan ayrılıyor; 134'te at başı yukarıda.

### 1. turda görülmeyen 16 sahne

Hiçbirinde havada duran nesne, okunmayan ya da kesilen yazı, yazı bandına giren figür yok. Türkçe karakterler doğru, her kart doğru sahnede.
Figürler ve nesneler zemine basıyor; arka sıradakilerin (133'teki atlılar, 143'teki çadır ve taş, 145'teki taş, 151'deki dinleyiciler, 154'teki
kalabalık, 155'teki sur, 157'deki otağlar) zemin çizgisi daha yüksekte, perspektife uygun. Tarz öteki sahnelerle tutarlı. 153'teki kart karede
yarı saydam; bu kartın giriş geçişi, hata değil.

### Zorunlu düzeltme (kare | yer | sorun | düzeltme)

| # | Kare | Yer | Sorun | Düzeltme |
|---|---|---|---|---|
| 1 | `r2/sahne150` (sahne 150) | Orta, taşın harfli yüzü ile makinenin ön ucu (x 390-515, y 860-950) | Objektif ve körük taşın harfli yüzünün sağ yarısına giriyor, 4-6. satırların son harflerini örtüyor. Makine taşa dayanmış gibi; 1. tur düzeltme #2'nin "hiçbir figür ya da makine harfli yüzü örtmesin" şartı karşılanmıyor. | Objektifin ucu taşın sağ kenarının (x ≈ 520) en az 30 px sağında kalsın; makine ile taş arasında çimen görünsün. Bunun için körüğü kısalt, makine, sehpa ve fotoğrafçıyı sağa kaydır; yer açmak gerekirse Rus subayını fotoğrafçının arkasına, arka sıraya al. Kamera hareketi ve paralaks katmanları kaydırdığı için sahnenin başında, ortasında ve sonunda (3 kare) objektifin harflere girmediğini kontrol et. |

### İyileştirme önerileri (reddetme nedeni değil; düzeltme sırasında yapılırsa iyi olur)

- **sahne138 (Tonyukuk):** Asanın alt ucu y ≈ 1160'ta bitiyor, figürün ayakları y ≈ 1305'te; ihtiyarın asası yere değmiyor. Elde tutulduğu için havada durmuyor, ama yaşlı adamın asası yere basmalı. Asayı zemine kadar uzat.
- **sahne150:** Sağdaki yeşil paltolu subayın önündeki dikey sopa (x 830-880, y 820-1300) bir ele bağlı değil; üst ucu fotoğrafçının sakalında bitiyor. Sopayı subayın eline ver (ya da omuza alınmış tüfek yap) ya da kaldır.
- **sahne135:** Diz çöken yazıcının mavi kaftanı yerde geniş bir çan gibi açılıyor; dizi ve bacakları görünmediği için büyücü şapkasına benziyor. Önde bir diz ve yere değen bir ayak ucu çizilirse diz çöktüğü okunur.
- **sahne145:** Radloff'un kasket siperi sağa doğru uzun, ince siyah bir çubuk gibi uzanıyor (x 610-680, y 740-760). Siperi kısalt.
- **sahne143:** Sağdaki arka plan taşının kaplumbağa kaidesi sağ kenarda kesiliyor (x 1080). Taşı 40-60 px sola al.
- **sahne140:** Soldaki Rus askerinin sol kolu boşluğa, kadraj dışına uzanıyor. Kolu tüfeğe ya da esire yönelt.

### Değerlendirme (sahibe gösterilecek)

Grafiker ilk turdaki beş hatadan dördünü tam düzeltti: Bilge Kağan artık hizmetkârıyla aynı boyda; 1890'a uymayan sinema kamerasının yerinde
körüklü, ahşap bir fotoğraf makinesi var; kapaktaki uçan daireye benzeyen nesne kalktı; başörtülü kadının yüzü göründü. İlk turda bakılmayan
16 sahneye de baktım; hepsi temiz, yazılar okunuyor, figürler yere basıyor. Tek bir sorun kaldı: Fin seferi sahnesinde (150) fotoğraf
makinesinin objektifi taşın yazılı yüzüne girip birkaç harfi örtüyor, makine taşa dayanmış gibi görünüyor. Bu küçük bir yerleşim düzeltmesi;
grafikere geri gönderildi, düzeltildikten sonra yalnız bu sahneye yeniden bakılıp size gelecek.
