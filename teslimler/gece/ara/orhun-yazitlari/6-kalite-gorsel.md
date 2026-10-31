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
