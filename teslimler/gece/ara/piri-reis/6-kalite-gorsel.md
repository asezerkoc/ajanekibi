# Haritayı Çizen Adam: görsel kalite kontrol

**İş:** Piri Reis'in haritaları ve idamı (1513-1554), gece vardiyası 6/10 · **Hazırlayan:** 🔴 SKONSTART Kalite Kontrol (görsel)
**Girdiler:** `5-grafik.md` (sahne planı, 38 sahne), `4-kalite-metin.md` (kartlar). Render kareleri `scratchpad/qc-piri-reis/`: 12 düzenli kare (kare-020s … kare-244s), kontak sayfası ve kare düşmeyen kritik sahnelerden benim render ettiğim 8 ek kare. Kareler `sahne_zaman.py` zamanlarıyla, sahnenin ortasından alındı:

| Ek kare | Sahne | Kare no |
|---|---|---|
| ek-kapak.png | kapak | 60 |
| ek-345-maskat.png | 345 Maskat kalesi | 6326 |
| ek-346-hurmuz.png | 346 Hürmüz | 6691 |
| ek-350-ucgemi.png | 350 üç gemiyle dönüş, donanma geride | 7806 |
| ek-351-ferman.png | 351 Kahire, fermanı okuyan çavuş | 8175 |
| ek-356-firtina.png | 356 Seydi Ali'nin fırtınası | 10016 |
| ek-364-mektup.png | 364 1960, Ohlmeyer'in mektubu | 12871 |
| ek-349-kapanis.png | kapanış, 349 Basra'da kalan donanma | 15859 |

Hapgood sahnesi (366) ayrı render edilmedi. 8 karelik sınır doldu; sahne kare-224s'teki geçişte görünüyor.

## Karar: UYGUN DEĞİL (revize_birimi: grafiker)

Fizik ve yazı tarafı temiz:
- 20 karenin hiçbirinde havada duran nesne yok.
- Bütün kartlar okunuyor.
- Türkçe harfler doğru (ğ, ı, İ, ş, ç, ö, ü ve "şikâyet"teki â).
- Kapak temiz.

Tek zorunlu düzeltme 1929 sahnesindeki dönem hatası. Sahibin 03:40 notu açık: "tek bir hatalı kare bile kabul değil". Bu kare yazının "1929" dediği anda yanlış bir dönem silüeti gösteriyor.

## Zorunlu düzeltmeler (kare | yer | sorun | düzeltme)

| Kare | Yer | Sorun | Düzeltme |
|---|---|---|---|
| kare-183s.png (sahne 359; kod gereği 360 da) | Kadrajın sol yarısı, iki figürün başı (y ≈ 750-860) | **Koordinatörün sorusuna cevabım: şapka *fikri* doğru, *çizimi* yanlış.** 1925 Şapka Kanunu'ndan sonra 1929 İstanbul'unda Halil Edhem'in ve bir Alman bilim insanının fötr şapka giymesi dönemine uygun. Ama çizilen şey fötr değil. Uzun, düz tepeli silindirik bir taç ve çok geniş, dümdüz bir kenar var. Bu silüet 17. yüzyıl püriten şapkası ya da Hasidik/Amiş şapkası gibi okunuyor, 1920'lerin fötrü gibi değil. İzleyici "neden bu şapka" diye yorum yazar. `sapka` başlığı Çelebi işindeki 1720 Fransızları için çizilmişti; o dönemde doğru, burada yanlış. | `piri_reis.py` içinde 1929-1960 kişileri için ayrı bir **fötr** başlığı çiz: alçak, yuvarlatılmış bir taç, tepede ortadan çökük bir çizgi ve tutam, koyu bir şapka bandı, daha dar ve hafif kıvrık bir kenar. Kenar genişliği başın yaklaşık 1,3 katı olsun, şimdiki gibi 2 katı değil. Kullanılacak yerler: `EDHEM` (tanım 56. satır; 359 ve 360'ta kullanılıyor) ve 359'daki ikinci figür (1587. satır). Ya bu fötrü ciz.py'ye yeni bir `bas` seçeneği olarak ekle ya da piri_reis.py'de yerel bir başlık olarak yaz. Çelebi ve Cem Sultan dosyalarındaki `sapka`ya dokunma. Sonra 359'u ve 360'ı yeniden üret; `taban_denetimi` ile yazı bandı denetimini tekrar çalıştır (fötr daha alçak olduğu için bant sorunu çıkmaz). |

## İyileştirme önerileri

Bunlar reddetme nedeni değil. Grafiker 359'a zaten döneceği için 1-3'ün aynı turda yapılmasını öneririm.

1. **kare-183s, Babüsselam (koordinatörün ikinci sorusu: "Avrupa şatosu gibi mi?").**
   - Kısmen öyle. Çizimin ana hatları doğru: Babüsselam'ın gerçekte de iki sekizgen, külahlı kulesi ve mazgallı yan duvarları var. Bu kapı zaten "şatoya benzer" diye bilinir. Çizimde sorun, yapının bembeyaz sıva, küçük ve süssüz olması; bu yüzden bir masal şatosu gibi okunuyor.
   - Kapı kemeri yaklaşık 95 px, kuleler adamların çenesinin altında kalıyor. "İki kişi içeri yürür" anı için kapı fazla oyuncak gibi.
   - Öneri: kapının üstüne geniş, koyu ve ahşap altlı Osmanlı saçağını belirgin çiz, kemerin üstüne yeşil-altın bir yazı/tuğra panosu koy, taş rengini kırık beyaz ya da açık griye çek ve kapıyı 1,3-1,5 kat büyüt (kuleler adamların başını geçsin).
2. **Karakter sürekliliği (kod okumasından; 360 render edilmedi).** 359'daki soldaki adam kahverengi paltolu, şapkalı ve sakalsız (1587. satır). 360'taki `DEISSMANN` ise takkeli/açık başlı ve ak sakallı. İkisi aynı kişiyse izleyici bağı kuramaz. 359'daki ikinci figür `DEISSMANN` renklerini ve ak sakalı alsın, fötrünü elinde ya da başında taşısın.
3. **kare-203s (362, Kahle).** Başlık beyaz bantlı, siperli bir kaptan kasketi gibi okunuyor (kodda `takke`). 364'teki Ohlmeyer'in kasketiyle karışıyor ve bir profesörün oda içinde başında olması tuhaf. Kahle'yi açık başlı (saç) ya da fötrü elinde çiz.
4. **ek-364-mektup (364, Ohlmeyer).**
   - Plan "lambanın altında mektup yazar" diyor. Karede ayakta, elinde kâğıt tutuyor; lamba kadrajın öbür ucunda, sehpa boş. Kart ("mektup yazıyor:") kabaca karşılanıyor ama sahne daha güçlü olabilir: Ohlmeyer sehpanın başında, lamba yanında.
   - Kasket bugünkü bir beyzbol şapkası gibi okunuyor. 1960 ABD Hava Kuvvetleri subay kasketi yüksek taçlı ve siperlidir; tacı yükselt, siperi daralt.
5. **kare-349 kapanış (ek-349-kapanis) ve 354.**
   - Karşı kıyıdaki "alçak hurmalık şeridi" (y ≈ 420-510) eşit aralıklı, kara direkler ya da babalar gibi okunuyor, hurma gibi değil.
   - Hâlâ kartın ikinci satırının ("Basra'da bırakır mıydınız?") arkasına giriyor. Yazı okunuyor, bu yüzden zorunlu değil. Ama videonun son sorusu bu karede.
   - Öneri: hurmaları seyrek ve düzensiz aralıkla diz, yaprakları yelpaze gibi açılsın; ya da şeridi tamamen yazı bandının altına (y > 560) indir.
6. **kare-101s (344 Aden), ek-345-maskat, kare-163s.** Uzak plandaki tepelerde iğne yapraklı ağaç (çam) silüetleri var. Aden'in krater dağları ve Umman kıyısı çıplak, volkanik ve çöl. Uzak plan bu sahnelerde ağaçsız, kızıl-kahve kayalık sırtlara çevrilsin. Coğrafi bir ayrıntı ama "hata istemiyorum" notuna göre düzeltmeye değer.
7. **ek-345-maskat ve ek-346-hurmuz.** Kale iki sahnede de kadraj kenarında kesiliyor: Maskat'ta sağda, Hürmüz'de solda ve kapısı yarım. Soldaki en ön gemi de Maskat'ta kenarda yarım kalıyor. Filo için kabul edilebilir bir kadraj. Kale ise kartın öznesi; kaleyi 30-40 px içeri al ki iki kulesi ve kapısı tam görünsün.
8. **kare-020s, kare-081s, kare-163s, sağ üst köşe (x ≈ 1050-1080, y ≈ 60-150).** Kenarda yarısı kesilmiş gri, yuvarlak bir gök cismi ya da bulut var; render hatası gibi duruyor. İçeri al ya da kaldır. kare-020s'te sol kenarda (y ≈ 560) yarım kalmış koyu bir uzak gemi parçası da var.
9. **kare-020s ve kare-081s.** Uzak kale (332) ve uzak gemi yelkeni (341), kartın 2. ve 3. satırlarının arkasında kalıyor. Yazı okunuyor; onaylı Çelebi işindeki gibi, grafikerin de açık bıraktığı nokta. Kabul ediyorum. Kale bir tık sağa ya da aşağı alınırsa daha temiz olur.
10. **kare-040s (335).** Kart "Piri masada çizer" anında ama Piri'nin eli parşömene değmiyor; masanın yanında oturuyor. Kolu masaya uzansın.

## Değerlendirme (sahibe gösterilecek)

Piri Reis videosu görsel olarak sağlam:
- 20 karenin hepsinde figürler ve nesneler zemine oturuyor; hiçbir şey havada değil.
- Kartların hepsi okunuyor, Türkçe harfler kusursuz.
- 64-bit piksel tarzı, kişilerin renk kodu (deniz yeşili Piri, kırmızı çavuş) ve Kahire'de açılıp kapanan kurgu baştan sona tutarlı.
- Basra'da kalan donanma, fırtına ve parşömen yakın planları hikâyeyi güçlü taşıyor.

Tek bir şeyi geri çeviriyorum: 1929 Topkapı sahnesinde Halil Edhem ve yanındaki adamın şapkası. Şapka takmaları dönemine uygun, ama çizilen silüet 1920'lerin fötrü değil, püriten ya da Amiş şapkası gibi okunuyor. Grafiker bunu fötrle değiştirip aynı turda Babüsselam'ı daha Osmanlı ve daha büyük çizdiğinde video teslime hazır olacak.
