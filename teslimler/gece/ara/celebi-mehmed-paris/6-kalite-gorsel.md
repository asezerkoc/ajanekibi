# Çelebi Mehmed Paris'te: kalite kontrol (görsel kapı)

**İş:** Yirmisekiz Çelebi Mehmed Efendi'nin Paris sefareti (1720-21) · **Hazırlayan:** 🔴 SKONSTART Kalite Kontrol · **Girdiler:** 5-grafik.md (sahne planı), 4-kalite-metin.md (45 kart ve kapak), 12 render karesi (kare-018s … kare-225s) ve kontak sayfası. Bunlara ek olarak 6 kareyi kendim render ettim: ek-60 (kapak, 1. sn), ek-5760 (96. sn), ek-6900 (115. sn), ek-9060 (151. sn), ek-10860 (181. sn), ek-13740 (229. sn). Kareler `scratchpad/qc-celebi-mehmed-paris/` klasöründe.

## Karar: UYGUN DEĞİL (revize_birimi: grafiker)

Bütün kartlar okunuyor. Havada duran bir nesne yok. Atlı karelerde binici eyerde oturuyor. Reddin nedeni şu: kapakta ve 297'de gemi insandan küçük ve elçinin eli gövdesine değiyor, bu yüzden oyuncak gibi okunuyor (ölçek hatası). Ayrıca 311'deki kâtip elçinin birebir aynısı, izleyici fermanı elçinin yazdığını sanır (hikâye hatası). Bunlara iki küçük düzeltme ekleniyor. Dört düzeltmenin hepsi grafikerin işi; metin ve kartlar olduğu gibi kalır.

## Zorunlu düzeltmeler (kare | yer | sorun | düzeltme)

| # | Kare | Yer | Sorun | Düzeltme |
|---|---|---|---|---|
| 1 | ek-60.png (kapak, sahne 290) ve kare-056s.png (sahne 297) | Sol orta, y≈720-1110: gemi | **Ölçek.** Geminin gövde altı y≈1105'te, rıhtım kenarının (y≈1130) hemen üstünde. Bu yüzden gemi uzakta değil, rıhtımın dibinde duruyor gibi görünüyor. Gemi yelkeniyle birlikte yaklaşık 390 px; yanındaki elçi 570 px. Kapakta elçinin uzanan sol eli (x≈405, y≈1000) gövdenin sağ ucuna değiyor; elçi oyuncak bir kayık tutuyor gibi okunuyor. 056s'de de gemi elçinin hemen arkasında, onunla üst üste. | Kapak videonun ilk karesi olduğu için bu ölçek hatası kabul edilemez. Gemiyi gerçekten uzağa al: su çizgisini karşı kıyıya yaklaştır (dünya y≈566-572, ekranda ufka yakın). Küçük ölçek o zaman "uzak" diye okunur. Gemiyi yatayda da kaydır; elçinin kolu ve kavuğuyla hiçbir karede örtüşmesin. Kapakta elçinin kolu gemiye değil denize doğru uzansın, aralarında boşluk kalsın. 290'ın ve 297'nin bütün karelerini (kamera 290→262 kayarken) yeniden kontrol et. |
| 2 | kare-150s.png ve ek-9060.png (sahne 311, kart 29) | Sağ orta, x≈540-920: minderde yazan kâtip | **Kimlik karışıyor.** Kâtip, elçiyle aynı figür: mavi kaftan (#3a5a8a; elçinin kaftanı #1f4f7a), beyaz kavuk, koyu sakal, kırmızı minder, rahle, yanında şamdan. 131s'deki elçi karesiyle poz da kurgu da aynı. İzleyici 1727 fermanını elçinin yazdığını sanır; metinde böyle bir şey yok. 309'da kalfanın rengini tam bu nedenle değiştirmiştin. | Kâtibe elçiden belirgin biçimde ayrılan bir renk ver (örneğin toprak/kahverengi ya da koyu kırmızı kaftan; mavi ve mor tonlarından uzak dur). Sakalını kır ya da kısa yap. Minderin rengini de değiştir (kırmızı değil). Yeni hâli 131s/299 ile yan yana koyup karşılaştır. |
| 3 | ek-60.png (kapak) | Orta, y≈300-620: kapak yazısı | **Onaylı kapak metninden sapma.** Ekranda "Paris'teki / Elçi / Bak, öğren, anlat" yazıyor. Metin ve kalite kontrol kapağı "Çelebi Mehmed Paris'te" büyük başlık, "Bak, öğren, anlat" alt başlık olarak onayladı (2-metin, 3-editor, 4-kalite-metin). Değişikliğin gerekçesi 5-grafik.md'de yazmıyor. | `CelebiMehmed.tsx` KAPAK bloğunu onaylı metne göre yaz: `["Çelebi Mehmed", "Paris'te", "Bak, öğren, anlat"]`. Yeni metin 3 satır kalıyor; `yaziY: 270` ile figürlerin başına değmediğini doğrula. |
| 4 | kare-056s.png (sahne 297) | Sağ kenar, x≈1060-1080, y≈990-1060 | **Kenarda kesilen figür.** Sağdaki ikinci yeniçerinin kaftan eteği sağ kenarda kesiliyor: x=1079'da kontur yok, kaftan rengi devam ediyor. Kamera sola kaydıkça (x 290→262) sahne sonuna doğru kesik büyüyor. | Yeniçeri çiftini 8-10 px (dünya ≈4 px) sola al ya da çifti biraz aralayıp sağdakini içeri çek. Kenar raporunu kameranın son karesinde yeniden çalıştır. 1. madde için gemi kaydırılırken bunu da birlikte yap. |

## İyileştirme önerileri

- **Atlı kareler (kare-075s, kare-225s, ek-13740):** Binici eyerde oturuyor. Gövdenin altı eyerin üstünde, eyer de atın sırt çizgisinde (y≈985/995). Bacak atın yanından iniyor, üzengi kayışı ve üzengi yerinde. Fizik hatası yok. Ancak kütüphane `atli` oranında binicinin belden yukarısı (≈370 px) atın sırt yüksekliğinden (≈325 px) uzun. Profildeki "insan boyu at boyunun %65-70'i" kuralına göre at küçük kalıyor. Aynı fonksiyon Timur serisinde onaylandığı için bu iş için reddetmiyorum. Sonraki işlerde bant izin verdiği ölçüde atı biraz büyütmek ya da binici gövdesini kısaltmak düşünülebilir.
- **kare-206s (318, kart 38-39):** "Solan laleler", genel `cicek` fonksiyonuyla çizilmiş. Bu yüzden yuvarlak açık çiçekler gibi, gül ya da şakayık gibi okunuyor, lale gibi değil. Lale Devri'nin kapandığı karede bu simge önemli. Kadeh biçimli (üç taç yapraklı, dik) bir lale figürü eklenmesi şiddetle önerilir; aynı figür 310'daki mesire lalelerinde de kullanılabilir.
- **kare-187s (316, kart 35):** Ortadaki isyancının beyaz sarığı, elçinin ve Said'in sarığıyla aynı. Gece karesinde koyu mavi kaftanla birlikte bir an "elçi isyancıların arasında mı?" diye okunabiliyor. Ortadaki figüre de kalpak ya da renkli bir sarık verilebilir.
- **kare-112s (306, kart 21):** Sahnedeki taçlı ve beyaz giysili şarkıcı, 304-305'teki çocuk kralı hatırlatıyor. Taç yerine sorguçlu bir başlık kullanılırsa opera sahnesi kral sahnesiyle karışmaz.
- **ek-6900 (307, kart 22):** Rasathane binası Tuileries ile aynı `saray_cephesi`. Çatıya bir teras ya da kubbe gibi ayırt edici bir öğe eklenirse iki yapı birbirinden ayrılır. Figürler, dürbün ve çeyrek daire zemine basıyor; bunlarda sorun yok.
- **kare-093s / ek-5760 (303, kart 16-17):** Kart Tuileries'yi anlatıyor ama sarayın orta köşkü elçinin kavuğunun arkasında kalıyor. Kamerayı biraz yana ya da yukarı açmak sarayı görünür kılar.
- **kare-075s, kare-225s (301, 320):** Planda "bahar mavisi" ve "altın ikindi" yazıyor. Yakın kamerada gökyüzünün yalnızca gri dağ şeridi görünüyor ve Paris kasvetli okunuyor. Uzak plan renkleri plana göre ısıtılabilir.
- **ek-10860 (315, kart 34):** Planda "elçi pencereye dönük" yazıyor ama elçi sağ kenara bakıyor ve kolu boşluğa uzanıyor. Elçi pencereye (sola) döndürülürse kart 34'ün duygusu güçlenir.
- **Kapak (ek-60):** Kapakta logo ve @pikseltarihim bandı yok. TSX yorumundaki "logo ve alt bandı kapak bileşeni ekler" cümlesi doğru değil; `SeriVideo` bunu yalnızca kapanışta yapıyor. Onaylı Cem Sultan videosu da aynı biçimdeydi, o yüzden reddetmiyorum. Ya yorum düzeltilmeli ya da kapağa bant eklenmeli.

## Değerlendirme (sahibe gösterilecek)

Video tarzına sadık: 64-bit piksel, konturlu figürler, gece sahnelerinde de (rasathane, 1730 isyanı) her şey okunuyor. 45 kartın hepsi net, Türkçe harfler doğru ve hiçbir kart figürlerin başına değmiyor. Atlı Paris karelerinde elçi ve Said atın sırtında, eyerde oturuyor; havada duran ya da zeminden kopan bir nesne yok. Göndermeden önce iki hata düzeltilmeli. Birincisi kapakta: gemi insandan küçük çizilmiş ve elçinin eli ona değiyor, bu yüzden oyuncak kayık gibi duruyor. İkincisi 1727 fermanı karesinde: fermanı yazan kâtip elçinin aynısı. Bunlarla birlikte kapak başlığı onaylı metne ("Çelebi Mehmed Paris'te") döndürülecek ve kenarda kesilen bir yeniçeri içeri alınacak; bu dört düzeltmeden sonra kareler yeniden kontrol edilecek.

## 2. tur: UYGUN

**Bakılan kareler:** `scratchpad/qc-celebi-mehmed-paris/r2/` içindeki kapak, 290 (ikinci kullanımı), 297, 310, 311, 316, 317 ve 318. Hepsi yeniden render edilmiş kareler; Read ile tek tek açıldı.

**Dört zorunlu düzeltme yapılmış:**
1. **Gemi (kapak, 290, 297):** Gemi artık ufka yakın suda duruyor. Gövde altı y≈990'da, rıhtım kenarı y≈1130'da. Gemi yaklaşık 240 px, elçi 570 px; ölçek "uzak gemi" diye okunuyor. Elçinin uzanan kolu (x≈515, 297'de x≈385) ile geminin kıçı (x≈285-290) arasında açık boşluk var, hiçbir yerde örtüşme yok.
2. **Kâtip (311):** Kahverengi kaftan, yeşil takke, kır sakal ve yeşil minder var. Mavi kaftanlı, beyaz kavuklu, koyu sakallı elçiden açıkça ayrılıyor. Soldaki beyaz giysili, fetvayı tutan figür de ayrı bir kimlik olarak okunuyor.
3. **Kapak başlığı:** "Çelebi Mehmed / Paris'te" beyaz büyük başlık, altında altın renkte "Bak, öğren, anlat" var. Yazı okunuyor, Türkçe harfler doğru ve figürlerin başlarına değmiyor (en alt satır y≈620, kavuklar y≈735'ten başlıyor).
4. **Yeniçeriler (297):** Çiftin sağ kenarı x≈995'te, kadrajın içinde, kesik yok. Ben bu tek kareye baktım; grafikerin 24 karelik kenar raporu kameranın son karesini de temiz gösteriyor.

**Yeni sorun yok:**
- 310: Yeni `lale` figürü kadeh biçimli ve lale gibi okunuyor. Laleler havuzun yanında zemine basıyor (y≈1300).
- 316: Ortadaki isyancının başında kırmızı börk var, elçiyle karışmıyor. Ateş ve figürler zemine oturuyor.
- 317: Boş taht ile yere düşmüş kavuk ve minder zemine oturuyor. Kart okunuyor ve kırmızı vurgu yerinde.
- 318: Ön plandaki lale sırası lale gibi okunuyor, elçi de zemine basıyor.
Hiçbir karede havada duran nesne, kesilen yazı ya da yazı bandıyla çakışma yok.

**İyileştirme önerileri (red nedeni değil):**
- 317: Düşen kavuk tahtın oturağının yarısı kadar büyük. Biraz küçültülürse ölçek daha inandırıcı olur.
- 318: Lalelerin "solgun" hâli renkte belli oluyor ama sarkma pek seçilmiyor. Çanakları biraz daha eğmek "kapanan dönem" duygusunu güçlendirir.
