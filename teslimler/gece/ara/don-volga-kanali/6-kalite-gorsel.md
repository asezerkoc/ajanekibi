# 🔴 Kalite Kontrol (görsel): Su Akmıyor (Don-Volga kanalı)

**İş:** Piksel Tarihim, gece vardiyası 4/10 · slug `don-volga-kanali` · 31 Ekim 2026
**Bakılan kareler:** 12 render karesi (`kare-019s` … `kare-236s`) + kontak sayfası + kritik sahnelerden 8 ek kare: kapak (kare 60), 250 (9 sn), 255 (42 sn), 258 (67 sn), 261 (85 sn), 285 (230 sn), 287 (237 sn), 289 (251 sn). Hepsi Read ile tek tek ve gerektiğinde yakınlaştırılarak açıldı. Geçiş ve yazı belirme anına denk gelen yarı saydamlık (157, 177, 216, 236, 289 sn) efekt sayıldı, hata sayılmadı.

## Karar: UYGUN DEĞİL (revize_birimi: grafiker)

Dört zorunlu düzeltme var: oyuncak boyunda bir tekne, esiri bıçaklıyormuş gibi duran bir kılıç, 1569 Moskova masasında bir fotoğraf ve kadrajın kenarında kesilen bir kadırga. Önceki işlerde reddedilen hata türlerinden üçü (oyuncak boyunda gemi, dönem dışı alet, kenarda kesilen nesne) bu videoda tekrar ediyor.

## Zorunlu düzeltmeler (kare | yer | sorun | düzeltme)

| # | Kare / sahne | Kadrajın neresi | Sorun | Düzeltme |
|---|---|---|---|---|
| 1 | `kare-039s.png` · sahne 254 (Perevoloka, kart 7) | Sol orta, x 140-430, y 920-1070 | Karadan çekilen "gemi" küçük bir tekne: yanındaki adamın ancak 1,5-2 boyu kadar uzun. Kütükler küvet ayağı gibi duruyor. Halat, arka plandaki teknenin başından (y≈975) önde duran çekenlerin ellerine (y≈1000) düz gidiyor. Tekne geride (taban y≈1060), çekenler önde (taban y≈1300) duruyor; bu derinlik farkı halatta hiç görünmüyor. Sonuç oyuncak bir tekne, ağzı da "Gemiler yüzyıllardır burada karadan çekiliyor". Bu hata türü daha önce reddedilmişti. | Teknenin boyunu en az 4-5 insan boyuna çıkar: direkli ya da direği yatırılmış bir nehir gemisi. Gemiyi çekenlerle aynı zemin bandına al (aynı taban), altına kütükleri yuvarlak kesitli ve görünür çiz. Halat geminin başından çekenlerin ellerine eğimle, aynı derinlikte insin. Gemi büyüdüğü için çekenleri biraz küçültmek gerekirse insanlar yine kadrajın en az %30'unu tutsun. Yanındaki adam gemiyi ittiriyormuş gibi gövdeye yaslansın, değmeden yüzmesin. |
| 2 | `kare-078s.png` · sahne 260 (kadırga güvertesi, kart 15) | Sol orta, x 220-530, y 1095-1140 | Yeniçerinin kılıcı yatay uzanıyor ve ucu Maltsev'in kaftanına ~30 piksel giriyor. Esir bıçaklanıyormuş gibi okunuyor. 5-grafik.md'deki "figürler birbirine değmiyor" notu bu karede doğru değil. Kaynakta böyle bir şiddet yok. | Kılıcı aşağı, güverteye doğru indir ya da ucunu Maltsev'in kaftan kenarından en az 12 piksel (540 ızgarada 6) uzakta bitir. Bekçiliği göstermek için kılıç kında da durabilir, el kabzada kalır. |
| 3 | `kare-196s.png` · sahne 279 (Moskova, Maltsev'in raporu, kart 39) | Masanın üstü, x 715-830, y 1020-1145 | Masada çerçeveli, içinde gri bir dikdörtgen olan bir nesne var. Bu, `orhun_yazitlari.masa(yuk="kagit")` içindeki "dayalı taş fotoğrafı" (19. yüzyıl). 1569 için dönem dışı bir nesne; ekranda küçük bir monitör ya da fotoğraf çerçevesi gibi okunuyor. Ayrıca sahne planı "mum ışığında raporunu yazar" diyor ama Maltsev masadan uzakta, ayakta, elinde kâğıt tutuyor. | Masayı fotoğrafsız çiz: `yuk="kitap"` ya da kâğıt yığını, hokka ve tüy kalem. `masa`'ya fotoğraf çizmeyen yeni bir yük seçeneği ekle, Orhun serisini bozma. Maltsev masanın başına geçsin (oturur ya da eğilmiş), eli kâğıdın üstünde dursun. |
| 4 | `ek-261-085s.png` · sahne 261 (kadırgalar Don'dan yukarı, kart 16), kare 5101 | Sol kenar, x 0-30, y 900-990 | Sol arkadaki kadırganın kıç köşkü ve feneri kadrajın sol kenarında kesiliyor; gövde kadraj dışından giriyor. Bu sahnede kenar denetimi "su" diye kapatılmış ama kesilen şey su değil, bir gemi. | Arka kadırgayı en az 30 piksel (540 ızgarada 15) sağa al ya da ölçeğini küçült. Sahne boyunca (x 250→290 kaydırma ve sonundaki yakınlaşma dahil) gemilerin tamamı kadrajda kalsın. 261 ve 277'de kenar denetimini gemiler için yeniden aç; yalnızca su ve kıyı muaf kalsın. |

**Görülemeyen sahneler (revizyonda kontrol edilecek):** 276 (ok saldırısı) ve 283 (1948, dikenli tel) yalnızca geçiş anında, yarı saydam olarak (`kare-177s`, `kare-216s`) görüldü; ek kare sınırı (8) doldu. 177 sn karesinde 276 katmanından gelen bir okun 275'teki diz çökmüş askerin yüzünden geçtiği ve iki kalkanlı askerin kalkanla birbirinin başını örttüğü görülüyor. Bu bir geçiş karesi olduğu için reddetme nedeni sayılmadı. Revizyondan sonra 276 (kare ≈10770) ve 283 (kare ≈13223) için birer temiz orta kare render edilip bakılmalı.

## İyileştirme önerileri

- **263 (`kare-098s`):** Devlet Giray'ın ak atının başında göz ve ağız yok; baş soluk bir kama gibi okunuyor. 1 piksel koyu göz ve burun deliği eklenmeli. 258'deki iki atın başı da aynı (`ek-258-067s`).
- **260 (`kare-078s`):** Maltsev'in küreği yukarı, gökyüzüne doğru kalkıyor (uç y≈930, küpeşte y≈995). Kürek küpeşteden aşağı, suya inmeli. Arka plandaki kürekler de küpeştenin üstünde direk gibi duruyor.
- **255 (`ek-255-042s`):** Astrahan'ın adası sağda yakın kıyıya yapışık görünüyor; adanın önünde su görünmüyor, yarımada gibi okunuyor. Adanın kumlu kıyısıyla yakın kıyı arasına 6-10 piksellik bir su şeridi eklenmeli.
- **266 (`kare-118s`):** Hendek, figürlerin önünde değil arkasında kalıyor ve yükseltilmiş toprak bir set ya da sedir gibi okunuyor. Hendeğin ön kenarı (figürlerin ayak hizasının önünde ince bir toprak dudağı) çizilirse "kazılmış yarık" olarak okunur. Aynı sahnede kazıcı azap paşaların beyaz-kırmızı kavuğunu takıyor; azaba basit bir börk ya da sarık daha doğru olur ve paşalardan ayrışır.
- **285 (`ek-285-230s`):** "Su hazneye hücum ediyor" anı yalnızca gri betonun üstünde birkaç beyaz noktayla gösteriliyor. Kapaktan taşan, haznenin tabanını kaplayan mavi bir su dili (köpüklü ön kenarıyla) bu ana güç katar.
- **287 (`ek-287-237s`):** "Dev heykel" demesine karşın kadrajda ölçek verecek bir şey yok; heykel kaidesinden kısa görünüyor. Kaidenin yanına küçük bir insan silueti ya da kaideyi alçaltıp heykeli yükseltmek "dev" sözünü görselleştirir.
- **250 (`ek-250-009s`):** Kalkık kazmanın başı uzaktaki çadırın tam üstüne biniyor (x 480-600, y 850-970). Çadır 30-40 piksel sağa alınmalı.
- **Kapak (`ek-kapak-001s`):** Başlık okunuyor ve logo bandıyla çakışmıyor. Yalnızca üçüncü satır "Sokollu'nun Don-Volga kanalı" ufuk çizgisindeki koyu şeridin üstüne düşüyor; bir tık yukarı alınırsa daha temiz durur.

## Değerlendirme (sahibe gösterilecek)

Video genelde SKONSTART tarzında: 64-bit piksel, konturlar net, sahneler aynı paletle tutarlı. Kişiler renk kimlikleriyle ayrışıyor (Sokollu yeşil ve ak sakallı, Kasım Paşa hardal ve kara sakallı, Maltsev gri-mavi ve kahve sakallı). Yazılar her karede okunuyor, Türkçe karakterler doğru ve kartlar sahnelerle örtüşüyor. Ancak dört karede, daha önce reddettiğiniz türden hatalar var: Perevoloka'da karadan çekilen gemi oyuncak boyunda, kadırgada nöbetçinin kılıcı esir elçiye saplanmış gibi duruyor, 1569 Moskova'sında masada bir fotoğraf var ve Don'daki kadırgalardan biri kadrajın kenarında kesiliyor. Grafiker bu dördünü düzeltince ok saldırısı ve 1948 sahneleriyle birlikte yeniden bakacağım; size ancak ondan sonra gösterilmeli.

## 2. tur

**Bakılan kareler:** r2 klasöründeki 13 sahne ortası (250, 254, 255, 258, 260, 261, 272, 276, 277, 279, 283, 285, 287) ve 3 ek render: 254'ün başı ve sonu (kare 2125, 2378), 261'in son yakınlaşması (kare 5248). Gerektiğinde kareler yakınlaştırılarak tek tek açıldı. 276 ve 283'ün r2'deki orta kareleri geçişe denk gelmedi, ikisi de temiz.

### Karar: UYGUN DEĞİL (revize_birimi: grafiker)

Birinci turdaki dört zorunlu düzeltme yapılmış ve kabul edildi. Ancak iki karede ana sahneyi taşıyan figürlerin yüzünde göz yok. Bu, daha önce reddedilen hata türlerinden biri ve düzeltmesi birkaç piksel.

### Birinci turun zorunlu düzeltmeleri

| # | Sahne | Durum | Not |
|---|---|---|---|
| 1 | 254 Perevoloka | **Kabul** | Tekne artık kütüklere oturan, direği yatırılmış bir nehir gemisi. Halat burundan çekenlerin omzuna eğimle iniyor; gemi ve çekenler aynı zemin hattında (taban y≈1135). Ölçüm: görünen gövde x 225-805, yani yaklaşık 2,6-3 çeken boyu. Grafikerin yazdığı "dört boy" değil, ama kıç Kasım Paşa'nın arkasında kaldığı için gerçek boy biraz daha uzun. **Kural çakışması kararı:** 9:16 kadrajda dört-beş insan boyunda bir gemi ile %30 boyunda insanlar aynı derinlikte olamaz. Bu yüzden %30 kuralını öndeki Kasım Paşa'nın karşılaması (y 730-1305, kadrajın %30'u), ölçeği ise gemi derinliğindeki çekenlerin vermesi kabul edildi. Gemi, kütükler ve çekenler kendi aralarında tutarlı; artık oyuncak gibi okunmuyor. |
| 2 | 260 kılıç | **Kabul** | Kılıç kınında, belden aşağı iniyor (x 590-720, y 1100-1220). Hiçbir figür bir başkasına değmiyor; Maltsev ile yeniçeri arasında yaklaşık 45 piksel boşluk var. |
| 3 | 279 masa | **Kabul** | Fotoğraf kalktı. Masada açık sayfa, kâğıt tomarı, hokka ve yanan mum var. Maltsev masanın başında, tüy kalemi kâğıdın üstünde. Tavandaki avize üst kenarda kesiliyor, ama tavana asılı olduğu için doğal. |
| 4 | 261 arka kadırga | **Kabul** | Sahne ortasında ve son yakınlaşmada üç kadırga da kadrajın içinde (sol arka x 100-370, sağ arka x 700-900). |

### Zorunlu düzeltmeler (kare | yer | sorun | düzeltme)

| # | Kare / sahne | Kadrajın neresi | Sorun | Düzeltme |
|---|---|---|---|---|
| 1 | `r2/sahne272.png` · sahne 272 (Rus takviyesi haberi) | Atlının yüzü, x 495-555, y 765-800 | Sahnenin tek ana figürü olan atlının profil yüzünde göz yok: sivri börk ile sakal arasında düz ten rengi bir şerit var. Atın gözü eklenmiş, binicininki eklenmemiş. | Yüze 1-2 piksellik koyu bir göz ekle. Diğer figürlerde olduğu gibi göz, börk kenarının bir piksel altında ve burun tarafında olsun. |
| 2 | `r2/sahne254.png` · sahne 254 | İki çeken, x 830-1020, y 945-960 | Gemiyi çeken iki adamın yüzünde göz yok: börk ile sakal arasında yalnızca ince bir ten şeridi kalıyor. Bu figürler sahnenin ölçek referansı ve gözsüz halleriyle maske takmış gibi okunuyor. | Börkü 1-2 piksel yukarı al ya da sakalı aşağı indir, ten şeridine birer koyu göz pikseli koy. 276'daki arka plan atlıları da aynı kalıpta; onlara da eklenirse iyi olur (bkz. öneriler). |

### İyileştirme önerileri

- **254:** Kasım Paşa'nın uzanan eli (x 230-285, y 1000-1025) teknenin gövdesinde bitiyor ve gemiye dokunuyormuş gibi okunuyor. Gemiyi 60-80 piksel sağa almak ya da Paşa'yı sola kaydırmak, eli boşluğa ve kıçı görünür hale getirir; gemi de daha uzun okunur. Ayrıca ilk çekenin sol kenarı son kütüğe (x≈835) değiyor; 10 piksel sağa alınmalı. Çekenler dimdik duruyor; öne eğik gövde "çekme" hareketini güçlendirir.
- **250:** Çadır sağa alınmış, kazma artık çadıra binmiyor. Ama çadır şimdi Sokollu'nun uzanan elinin tam ucunda (x 570-735, y 910-1020): Paşa elinde küçük bir çadır maketi tutuyormuş gibi görünüyor. Çadır x≈950'ye ya da ufukta daha yukarı alınmalı.
- **261 (son kare 5248):** Ana kadırganın mahmuz ucu sağ kenara 3 piksel kalıyor (x≈1077). Kesilmiyor, ama son yakınlaşmada 20 piksel pay bırakılması daha güvenli olur.
- **272:** Arka plandaki çadır ve uzak atlılar sol (x 0-35) ve sağ (x 1060-1080) kenarda yarım kalıyor. Kayan parallaks katmanında oldukları için hata sayılmadı.
- **276:** Arka plandaki Kazak/Çerkes atlılarının yüzleri koyu börk ile sakal arasında kayboluyor; göz pikseli eklenmeli. Sahne temiz: ok yerdeki askere saplı, uçan oklar havada mermi olarak doğal, ayakta duran asker kalkanıyla zemine oturuyor ve kimse kimseye değmiyor.
- **283:** Sahne temiz ve 1948'e uygun: kazma, kürek, dikenli tel, yastıklı ceketler. Yalnızca sağdaki yeşil figürün miğferinin üstünde gri, kubbe biçimli ikinci bir başlık kenarı var (x 840-940, y 800-850); çift şapka gibi duruyor, silinmeli.
- **Önceki öneriler:** 255 adası su şeridiyle ayrıldı. 258 atlarında göz var. 285'te su hazneyi dolduruyor. 287'de ziyaretçi silueti heykelin büyüklüğünü veriyor ve kaideye değmiyor. 260'ta kürekler suya iniyor. Bunlar uygulanmış ve iyi görünüyor.

### Değerlendirme (sahibe gösterilecek)

Grafiker ilk turdaki dört hatayı düzeltti. Perevoloka'daki gemi artık kütüklerin üstünde, halatla çekilen gerçek bir nehir gemisi. Kadırgadaki kılıç kınında, Moskova masasındaki fotoğraf yerini hokka, kâğıt ve muma bıraktı, Don'daki kadırgaların hepsi kadrajda. Ok saldırısı ve 1948 sahnelerine bu turda temiz karelerde baktım; ikisi de sorunsuz. Geriye tek tür bir hata kaldı: Rus takviyesi sahnesindeki atlının ve Perevoloka'da gemiyi çeken iki adamın yüzünde göz yok. Birkaç piksellik bu düzeltme yapılınca video size gösterilebilir.

## 3. tur

**Bakılan kareler:** r3 klasöründeki 13 sahne ortası (250, 252, 254, 256, 258, 260, 261, 265, 268, 272, 276, 279, 283) ve 6 ek render (`r3ek/`): 250'nin başı ve sonu (kare 200, 930), 254'ün sonu (2378), 261'in son yakınlaşması (5250), 268'in başı ve sonu (7545, 7950). Yüzler, çadır, kılıç ve gözcü kulesi piksel yakınlaştırmasıyla açıldı (`r3z/`). 250'nin son karesindeki soluk yazı, kartlar arası geçiş efekti.

### Karar: UYGUN DEĞİL (revize_birimi: grafiker)

Gözler tamam: 2. turun iki zorunlu düzeltmesi kabul edildi. Ancak sahnelerin yeniden çizilmesiyle yeni bir hata çıktı, ayrıca iki eski sorun tam çözülmedi. 268'de bir askerin çekili kılıcının ucu yanındaki askerin kaftanına dayanıyor (1. turda 260'ta reddedilen hatanın aynısı). 283'te küçültülen gözcü kulesi şimdi dikenli telin üstünde duran oyuncak bir kule gibi görünüyor. 250'deki çadır ise Paşa'nın böğrüne değiyor.

### 2. turun zorunlu düzeltmeleri

| # | Sahne | Durum | Not |
|---|---|---|---|
| 1 | 272 atlı | **Kabul** | Börkün kenarının altında, burun tarafında 2×2'lik koyu bir göz var (`r3z/272yuz.png`). Yüz bozulmamış, sakal ve ten bandı düzgün. |
| 2 | 254 çekenler | **Kabul** | İki çekenin de ten şeridinde koyu birer göz var (`r3z/254cek.png`). Börk ile sakal arasında açılan şerit maske etkisini kaldırmış. Ortadaki karede de, son karede de (2378) aynı. |
| – | 276 arka atlılar (öneriydi) | **Uygulanmış** | İki Kazak/Çerkes atlısının yüzünde de göz pikseli seçiliyor. Öndeki askerin gözü de yerinde. |

### Zorunlu düzeltmeler (kare | yer | sorun | düzeltme)

| # | Kare / sahne | Kadrajın neresi | Sorun | Düzeltme |
|---|---|---|---|---|
| 1 | `r3/sahne268.png`, `r3ek/k7545.png`, `r3ek/k7950.png` · sahne 268 (ordu Astrahan'a, kart "Ordu karadan Astrahan'a") | Orta ile sağ asker arası, sahne ortasında x 670-820, y 1110-1150 | Ortadaki askerin çekili kılıcı yatay uzanıyor ve ucu sağdaki askerin kaftanına dayanıyor. Sahnenin başında, ortasında ve sonunda hep böyle; arkadaşını bıçaklıyormuş gibi okunuyor. 1. turda 260'ta reddedilen hatanın aynısı. | Kılıcı kınına sok ya da ucunu yere doğru indir. Ucu yanındaki askerden en az 12 piksel (540 ızgarada 6) uzakta kalsın. Yürüyüş animasyonunun bütün karelerinde denetle. |
| 2 | `r3/sahne283.png` · sahne 283 (1948, Gulag) | Ortadaki mahkûm ile gardiyan arası, x 690-775, y 855-1005 (`r3z/283kule.png`) | Küçültülen gözcü kulesi şimdi bir insan kafası kadar (~145 px; insanlar ~500 px). Ayakları dikenli telin üst kenarında bitiyor, yani tel üstünde duran bir oyuncak kule ya da kuş evi gibi görünüyor. Kürek sapı ile tüfeğin arasına da sıkışmış. Ölçek ve zemin hatası. | Kuleyi kaldır ya da ufka (zemin çizgisi y≈800) dayalı, figürlerin başından ve aletlerden uzak bir yere al. Bacakları ufuk zeminine otursun, telin üstüne binmesin. Uzak plan ölçeği tutarlı olsun: ufuktaki bir kule, arka plandaki çadır ya da atlılarla kıyaslanacak boyda olmalı. |
| 3 | `r3/sahne250.png`, `r3ek/k200.png`, `r3ek/k930.png` · sahne 250 (ilk kazma) | Paşa'nın sağ böğrü, sahne ortasında x 905-1050, y 935-1015 (`r3z/250cadir.png`) | Çadır küçültülüp sağa alınmış, ama şimdi Paşa'nın sırtındaki elinin/böğrünün hizasında. Sol germe ipi gövdesine değiyor ve sahne boyunca öyle kalıyor. Paşa koltuğunun altında bir çadır maketi taşıyormuş gibi okunuyor. Sahnenin sonunda (kare 930) sağ ip kadrajın kenarına kadar uzanıyor (x≈1078). 2. turdaki "Paşa'nın elinde çadır maketi" sorunu çözülmedi, yalnızca öbür ele geçti. | Çadırı figürlerin hizasından çıkar. Ya ufka (taban y≈820-840) al ve iki figürün arasındaki boşluğa koy (x 450-650), ya da sahneden kaldır. Kamera kaymasının bütün karelerinde figürlere ve kadraj kenarına en az 30 piksel uzak kalsın. |

### Diğer kontroller (yeni hata yok)

- **254:** Kasım Paşa'nın kolu yanında, eli gemiye uzanmıyor. İlk çeken kütükten ayrı. Gemi kütüklere, çekenler zemine oturuyor. Son karede (2378) sağdaki çeken kenara ~30 piksel kalıyor; kesilmiyor. **Kabul.**
- **261:** Sahne ortasında ve son yakınlaşmada (5250) üç kadırga da kadrajda. Ana kadırganın mahmuzu sağ kenardan ~25 piksel, sol arka kadırganın feneri sol kenardan ~80 piksel içeride. **Kabul.**
- **283:** Gardiyanın miğferindeki çift başlık görüntüsü kalktı. Ama kulenin yeni yeri yeni bir hata getirdi (bkz. zorunlu 2).
- **252, 256, 258, 260, 272, 279:** Gözler yüzü bozmamış. Figürler zemine oturuyor, ölçek tutarlı, yazı bandı kafalara ve direklere binmiyor, kenarda kesilen nesne yok. 252 ve 279'da tavana asılı avize üst kenarda kesiliyor; tavandan sarktığı için doğal.

### İyileştirme önerileri

- **265 (`r3z/265alet.png`):** Soldaki kazıcının elindeki sap yatay uzanıp ortadaki adamın kürek sapını kesiyor ve kaftanında bitiyor; ucunda alet başı görünmüyor. İki adam tek bir T biçimli aleti tutuyormuş gibi okunuyor. Soldaki kazıcıya başı görünen bir kürek ya da kazma ver, sapı ortadaki adama değmeden bitsin.
- **276:** Soldaki arka atlının başı öndeki askerin yüzünün hemen solunda duruyor (x 640-690, y 870-940); uzaktan ikinci bir yüz gibi okunuyor. Arka atlıyı 60-80 piksel sola almak katmanları ayırır. Kalkanı tutan el/kol da görünmüyor; kalkan sakalın önünde asılı gibi. Kalkanın kenarına tutan bir el eklenmesi iyi olur.
- **258:** Öndeki atın kuyruğu arkadaki atın bacaklarının önünden geçiyor; katman doğru ama iki at birbirine yapışık okunuyor. Arkadaki atlıyı 40 piksel sağa almak yeterli.

### Değerlendirme (sahibe gösterilecek)

Grafiker gözsüz yüzleri düzeltti: Rus takviyesi sahnesindeki atlının, Perevoloka'da gemiyi çeken adamların ve ok saldırısındaki arka atlıların yüzünde artık göz var, yüzler bozulmamış. Perevoloka ve Don'daki kadırgalar sahneleri de temiz. Ancak bütün sahneler yeniden çizilince üç yerde sorun kaldı. Astrahan'a yürüyen orduda bir askerin kılıcının ucu yanındaki askere dayanıyor. 1948 sahnesindeki gözcü kulesi dikenli telin üstünde duran bir oyuncağa döndü. İlk kazma sahnesindeki çadır da Paşa'nın koltuğunun altında taşınıyormuş gibi görünüyor. Bu üçü düzelince video size gösterilebilir.
