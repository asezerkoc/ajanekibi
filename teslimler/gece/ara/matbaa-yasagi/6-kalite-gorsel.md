# 🔴 Kalite Kontrol (görsel): Fermanı Gören Yok (matbaa-yasagi)

**Hazırlayan:** 🔴 SKONSTART Kalite Kontrol · 31 Ekim 2026
**Bakılan kareler:** 12 render karesi (`kare-020s` … `kare-247s`), kontak sayfası ve 10 ek kare. Ek karelerden 8'i istenen kritik sahneler, 2'si ise benim saniye hesabı hatamdan dolayı yeniden render edildi:
`ek-kapak` (kapak), `ek-080s-oklid` (180), `ek-092s-pera-baski` (182), `ek-098s-pera-kapatma` (183), `ek-135s-kolozsvar-besik` (190), `ek-140s-istanbula-gelis` (191), `ek-220s-yalova` (203), `ek-241s-schwartz` (206), `ek-263s-ucbelge` (209), `ek-271s-kapanis`.
Klasör: `/tmp/claude-0/-home-user-ajanekibi/c16877a7-2389-58d4-b7bc-7d115caa39eb/scratchpad/qc-matbaa-yasagi/`

## Karar: UYGUN DEĞİL (revize_birimi: grafiker)

Havada duran nesne ve okunmayan yazı yok. Kartların hepsi okunuyor ve Türkçe karakterler doğru (İ, ş, ğ, ı, â, î, á). Ancak orta plan yapılarında ölçek hatası var: saray kapısı, kâğıthane, ahşap ev ve sur kapısı yanlarındaki figürlere göre oyuncak boyunda kalıyor. Bu hata özellikle figürün yapıya dokunduğu karelerde göze batıyor. Ayrıca bir figür hatalı: Kolozsvár sahnesindeki anne sakallı görünüyor ve yüzünde göz yok. Sahibin "tek bir hatalı kare bile kabul değil" kuralı gereği bu kareler düzeltilmeden video gönderilmez.

## Zorunlu düzeltmeler (kare | yer | sorun | düzeltme)

| # | Kare | Yer | Sorun | Düzeltme |
|---|---|---|---|---|
| 1 | kare-144s.png (sahne 192, kart 28) | Orta plan, kadrajın ortası (y≈680-1070) | **Saray kapısı oyuncak ölçeğinde.** Kemerli kapı yaklaşık 150 px, önündeki figürler ise 610 px boyunda. Yapı orta derinlikte olsa bile kapı orada duran bir insanın yarısı kadar kalıyor. Soldaki İbrahim'in uzattığı el (x≈290, y≈985) sur duvarına değiyor. Böylece yapı figürlerle aynı derinlikte okunuyor ve ölçek hatası açıkça görülüyor. Ayrıca beyaz düz duvarlar, mavi-gri sivri külahlar ve Osmanlı imi taşımayan gövde birlikte yapıyı Avrupa şatosu gibi gösteriyor. Bâbüsselâm'ın iki külahlı kulesi tarihte doğru; sorun külahlarda değil, Osmanlı ayrıntısının olmamasında. | `saray_kapisi` ölçeğini (s) en az 2,5 kat büyütün. Kapı kemeri figür boyunun en az 1,3 katı olsun. Kuleler kadrajın üstüne taşarsa yapıyı daha geriye ve yukarıya alın. Figürün kolu duvara değmesin: İbrahim'i 30-40 px sağa çekin ya da kolunu indirin. Osmanlı imlerini artırın: kurşun rengi külah ve saçak, kapı üstünde büyük ve okunur altın tuğra, kemer çevresinde yeşil ya da lacivert çini bordür, kulelerde sekizgen yüz çizgileri. |
| 2 | ek-220s-yalova.png (sahne 203, kart 40) | Sağ orta (kâğıthane, x≈660-1050, y≈775-1120) | **Kâğıthane bebek evi boyunda.** Evin kapısı yaklaşık 110 px, ustanın boyu yaklaşık 600 px. Kapı ustanın beline bile yetişmiyor. Usta elini çarka uzatıyor, dolayısıyla çark, oluk ve ev figürlerle aynı derinlikte okunuyor. Sonuçta ev, figürlerin yanında maket gibi duruyor. | Kâğıthane ve oluğu figürlerle aynı ölçeğe getirin: kapı figür boyunun en az 1,1 katı olsun. Ev kadraja sığmıyorsa yalnız sol duvarı ve çarkı gösterin, evin geri kalanı sağdan kadraj dışına çıkabilir. Bir seçenek de yapıyı belirgin biçimde geriye almak ve ustanın elini çarktan ayırmaktır. Yaşlı İbrahim kadrajın sol kenarına yapışık duruyor (sarığın solu x≈12). Onu 40-60 px içeri alın. |
| 3 | ek-135s-kolozsvar-besik.png (sahne 190, kart 26) | Sol, anne figürünün yüzü (x≈270-360, y≈880-990) | **Anne sakallı ve gözsüz görünüyor.** Yüzün altında, çene hizasında koyu kahverengi bir blok var ve sakal gibi okunuyor. Yüzde göz pikseli yok. "Bir Macar çocuk doğuyor" kartında bu figür sakallı ve yüzsüz bir adam gibi okunuyor. | `KADIN_ERDEL` (`bas="ortu"`) için çene altını başörtüsünün rengiyle (#3a3a6a) ya da ten rengiyle kapatın. Koyu blok kalmasın. Öteki figürlerdeki gibi göz pikselini çizin. Başörtüsü, gözün olduğu tarafı örtmemeli. |
| 4 | ek-098s-pera-kapatma.png (sahne 183, kart 19) ve ek-140s-istanbula-gelis.png (sahne 191, kart 27) | Orta plan yapıları | **Ölçek hatası 1 ve 2'dekiyle aynı.** 183'te ahşap ev iki katlı olmasına rağmen boyu figürlerden kısa; pencereler yaklaşık 70 px. Görevlinin meşalesi evin damını aşıyor. 191'de sur kapısı yaklaşık 140 px ve yürüyen figürün yarısı kadar. | `duz(588)` üstüne kurulan orta plan yapılarına (ahsap_ev, sur, saray_kapisi, kagithane) tek bir ölçek kuralı koyun: yapıların kapısı, o derinlikte duran bir figürün boyundan küçük olmasın. Kontrol: (yapı tabanı − ufuk) / (figür tabanı − ufuk) × figür boyu ≤ kapı yüksekliği. Bu kural betiğin otomatik denetimine eklensin. Render görmediğim 174, 175, 185, 207 ve 208 (cami, ev, sundurma) aynı kuralla yeniden denetlensin. |

## İyileştirme önerileri

- **kare-226s.png (sahne 204, kart 41): koordinatörün sorusu.** Benim değerlendirmem: kare hatalı değil. Masadaki figür mor kaftanlı ve koyu sakallı. Altı saniye önce (sahne 203) görülen ak sakallı, kahverengi kaftanlı yaşlı İbrahim'den ayrı biri olarak okunuyor; kimlik tablosuna göre de dökümü yazan kâtip. Ancak sarık ve sakal kalıbı İbrahim'in sarığı ve sakalıyla aynı. Hızlı izleyen biri "İbrahim kendi mirasını sayıyor" diye düşünebilir. Bunu önlemek için kâtibe ayırt edici bir görünüm verin: sarık yerine kavuk ya da küçük, renkli bir sarık, sakalsız ya da kısa sakal, elde açık bir defter. Odada İbrahim'i hatırlatan boş bir minder ya da yere bırakılmış sarık gibi bir "yokluk" işareti de anlamı güçlendirir.
- **kare-247s.png:** 206→207 geçişindeki yaklaşık 0,4 saniyelik çapraz geçiş anı. Üst üste binen katmanlar normal; kart bu sırada sönük. Sorun yok.
- **ek-263s-ucbelge.png (sahne 209, kart 48-49):** Kapanışın "üç belge" sahnesinde nesneler kadraj yüksekliğinin yalnızca yaklaşık %14'ünü kaplıyor (y≈1030-1300). Alt üçte bir boş taş zemin. Belgeler telefonda zor seçiliyor. `yakin` değerini 2,4'ten yaklaşık 3,0'a çıkarın ya da rahleleri büyütün. Öklid ve Vankulu kitapları birbirine değiyor (x≈675-690); aralarına boşluk bırakın.
- **Dış mekân kareleri (kare-144s, ek-098s, ek-220s, ek-140s):** Alt %30-35 boş çayır, kum ya da kar. Kamera odağını biraz aşağı alın ya da ön plana çimen, taş veya kar yığını gibi bir öğe ekleyin.
- **kare-041s.png (sahne 176) ve benzeri iç mekânlar:** Kandil kadrajın üst kenarına çok yakın. 041s'te zincir neredeyse görünmüyor: (80,69,40) rengi (53,40,27) zemin üstünde kalıyor ve kesik çiziliyor. Kandil asılı değil, havada duruyormuş gibi algılanabilir. Zinciri bir ton açın ve kesintisiz çizin. Kapakta (ek-kapak) zincir iyi görünüyor; ölçü o olsun.
- **ek-140s-istanbula-gelis.png (sahne 191):** Genç İbrahim'in gövdesinin tam ortasından boynundan ayağına inen kahverengi bir çubuk geçiyor (x≈375-410). Asayı tutan el görünmediği için bu çubuk elbise üstünde bir şerit gibi okunuyor. Asayı gövdenin yanına alın ve eli çizin, ya da asayı kaldırın. Aynı durum ek-220s'te yaşlı İbrahim'in asasında da var (x≈170-190), ama orada yaşlı adam asası olarak okunuyor.
- **kare-061s.png (sahne 178):** Sunaktaki haç düz Latin haçı. Planda "ucu genişleyen Ermeni haçı" yazıyor; kolların uçlarını genişletin.
- **ek-135s-kolozsvar-besik.png:** Plan "anne beşiği sallıyor" diyor, ama annenin eli beşikten yaklaşık 160 px uzakta. Anneyi beşiğe yaklaştırın, eli beşiğin kenarına değsin. Sağdaki mumluk, haça benzer bir siluet veriyor; kollarını kısaltın.
- **kare-103s.png (sahne 184):** "Mektup el değiştiriyor" deniyor, ama Osmanlı görevlisinin eli mektuptan yaklaşık 150 px uzakta. Figürleri yaklaştırın.
- **ek-080s-oklid.png (sahne 180):** Kart "453. sayfasında" diyor; sayfanın alt köşesine küçük bir "453" numarası eklenirse görsel kartı doğrular.
- **ek-271s-kapanis.png:** Gece arka planında iki kemer sırası üst üste biniyor: büyük karanlık kemerler (y≈840-1750) ve küçük aydınlık pencereler (y≈1200-1630). Kalabalık görünüyor. Kapanış bileşeni öteki videolarla ortaksa sorun değil; değilse arka planı tek katmana indirin.

## Değerlendirme (sahibe gösterilecek)

Video genel olarak SKONSTART tarzında. 64-bit piksel çizim, konturlu figürler ve sıcak mum ışıklı iç mekânlar sahneden sahneye tutarlı. 49 kartın hepsi okunuyor ve Türkçe harfler doğru. Presler, rahleler, beşik ve kitap yığınları zemine oturuyor. Kurgu, "fermanı gören yok" motifini boş rahleden üç belgeye kadar düzgün taşıyor. Ama dış mekânlardaki yapılar figürlerin yanında maket gibi küçük kalıyor. Saray kapısı insanın yarısı boyunda ve bir Avrupa şatosunu andırıyor. Yalova'daki kâğıthanenin kapısı ustanın beline yetişmiyor. Kolozsvár'daki anne figürü de sakallı ve gözsüz görünüyor. Grafiker bu dört noktayı düzeltince video tekrar kontrol edilecek; düzeltilmeden size gönderilmeyecek.

## 2. tur

**Bakılan kareler:** `qc-matbaa-yasagi/r2/` klasöründeki kapak ile 174, 175, 178, 180, 183, 184, 185, 190, 191, 192, 203, 204, 207, 208 ve 209 sahnelerinin orta kareleri. Bunlara ek olarak iki kare render ettim: `ek-sahne176.png` (kandil zinciri) ve `ek-sahne206.png`. Bütün kareler tek tek açıldı.

### Karar: UYGUN

**Gerekçe: ilk turdaki 4 zorunlu düzeltmenin hepsi karelerde yapılmış.**

1. **Sahne 192, saray kapısı:** Kapı artık ufkun önünde, açıkça uzakta duruyor. Önde duran figürlerle ölçek çelişkisi kalmadı. Sura değen el de yok. Kapının üstünde altın tuğra ve lacivert levha var, kemerin çevresinde çini bordür, saçakta lacivert-yeşil şerit var. Yapı artık Avrupa şatosu gibi okunmuyor.
2. **Sahne 203, Yalova:** Kâğıthane, çark ve oluk ufuk derinliğine alınmış, maket gibi durmuyorlar. Ustanın eli çarka değmiyor (arada yaklaşık 60 px var). Yaşlı İbrahim kenardan içeri alınmış, sarığın solu x≈140'ta.
3. **Sahne 190, anne:** Sakal gibi okunan blok kalkmış. Göz pikseli var, başörtüsü düzgün. Figür artık kadın olarak okunuyor. Haça benzeyen şamdan, üç mumlu şamdanla değiştirilmiş.
4. **Sahne 183 ve 191:** Pera evi ve sur ufkun önünde, figürlerle ölçek çelişkisi yok. 183'teki meşale damla çakışmıyor. 191'de gövdeyi ortadan bölen asa kaldırılmış.

Ölçek kuralının uygulandığı öteki sahneler de temiz: 174, 175, 185, 207 ve 208. 207'de tezgâh bel hizasında, satıcının başı damdan taşmıyor.

Düzeltmeler yeni hata getirmemiş. Havada duran nesne, gözsüz yüz, kenarda kesilen figür, yazı bandına giren nesne ya da dönem dışı öğe görmedim. 206'daki modern lamba ve çelik raf 2017 arşiv sahnesine ait, dönem dışı değil.

Ucuz iyileştirmeler de görünüyor:
- 178'de Ermeni haçı var.
- 180'de sayfa numarası "453" okunuyor.
- 184'te görevlinin eli mektuba değiyor.
- 204'teki kâtip kırmızı takkeli ve sakalsız, İbrahim'le karışmıyor.
- 209'da belgeler büyümüş ve aralarında boşluk var.
- Kapaktaki kandil zinciri kesintisiz.

175 ve 206 karelerinde kart soluk görünüyor. Bunun nedeni orta karenin iki kart arasındaki geçişe denk gelmesi. Kart metinleri ve süreler bu turda değişmedi ve 1. turda okunur bulundu.

### Kalan zorunlu düzeltmeler

Yok.

### İyileştirme önerileri (ret nedeni değil)

- **Sahne 192:** Sağdaki figürün sarığı sağ kenara yaklaşık 8 px, soldakinin sarığı sol kenara yaklaşık 22 px uzaklıkta. Kesilme yok ama kenara çok yakınlar. İki figür 30-40 px içeri alınabilir.
- **Sahne 203:** Raporda "ustanın kolu indirildi" deniyor, ama karede kol hâlâ yatay uzanıyor. Ucu oluğun ağzına yakın duruyor (x≈540'a karşı x≈555). Hata değil: işaret ediyormuş gibi okunuyor.
- **Sahne 190:** Annenin eli beşiğin yaklaşık 100 px üstünde kalıyor, kenarına değmiyor. Eli 80-100 px aşağı indirmek "beşiği sallıyor" anlamını güçlendirir.
- **İç mekânlar (176, 178, 184, 190, 204, 209):** Kandil kadrajın üst kenarına yapışık ve zinciri kadraj dışında kalıyor. Tavana asılı olduğu yine de okunuyor; kapaktaki gibi biraz aşağı indirilirse zincir de görünür.
- **Sahne 209:** Belgeler hâlâ kadraj yüksekliğinin yalnızca yaklaşık %16'sını kaplıyor. `yakin` değeri biraz daha artırılabilir.

### Değerlendirme (sahibe gösterilecek)

Grafiker ilk turdaki dört sorunun hepsini düzeltti. Saray kapısı, Pera evi, sur ve Yalova kâğıthanesi artık ufukta, gerçek uzaklıklarında duruyor. Figürlerin yanında maket gibi görünmüyorlar. Saray kapısı tuğrası ve çinileriyle Osmanlı yapısı olarak okunuyor. Kolozsvár'daki anne artık gözlü, başörtülü bir kadın. Düzeltmeler yeni bir hata getirmedi; kalan notlar küçük estetik öneriler. Video size gönderilebilir.
