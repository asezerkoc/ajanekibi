# 🟢 Grafiker: Taş Konuşuyor (Orhun yazıtları ve Vilhelm Thomsen, 1893)

**İş:** Piksel Tarihim (@pikseltarihim), dikey 1080x1920, 60 fps, 64-bit piksel; gece vardiyası 1/10
**Girdi:** teslimler/gece/ara/orhun-yazitlari/4-kalite-metin.md ("Nihai seslendirme metni", "Nihai ekran kartları", 42 kart)
**Çıktılar:**
- `video/piksel/orhun_yazitlari.py`: sahne 130-161 (32 sahne), `python3 -I video/piksel/orhun_yazitlari.py` hepsini hatasız çizer (sprite + gökyüzü/uzak/orta/ön, 139 ve 141'de kar katmanı)
- `video/src/sahneler/OrhunYazitlari.tsx`: `ORHUN_SERI`, `ORHUN_KARE`, `OrhunYazitlari`; etiket "PİKSEL TARİHİM · ORHUN YAZITLARI", ses "orhun-yazitlari-anlatim.mp3". Root.tsx'e dokunulmadı (kayıt kod tarafında).
- Sahne aralığı 130-169 verildi; 130-161 kullanıldı, 162-169 boş.

## Kurgu özeti

Tek eksen "taş ne diyor, ilk kim duydu?". Görsel motif: **taşın harfleri ışır** (taş konuşuyor). Kimse anlamazken ışık
sütunlar boyunca soluk akar (130, 139, 142); Türkçe yüz sessizken yalnız Çince yan yüz kızıl ışır (146, 148); Thomsen
çözünce (152) bütün harfler sabit altın yanar; 156'da iki yüz aynı kadrajda (Türkçe altın, Çince kızıl); 161'de gece
yıldızları altında harfler akar ve kapanış onun üstüne gelir. Bozkır sahneleri şafak, gün, akşam, gece ve kar paletleriyle
yüzyılların geçişini taşır; Avrupa sahneleri (Kopenhag, Leiden, Petersburg, Akademi) mum ve kandil ışıklı iç mekândır.
Motif kartları ("Taş konuşuyor. Kimse anlamıyor." 2, 13; "Bu kez Kopenhag'da biri anlıyor" 30) ALTIN; dönüşler
(10, 14, 24, 27, 35, 36) KIZIL; cevap ve soru kartları (5, 17, 28, 32, 38, 40, 41, 42) ALTIN.

**Kapak** (ilk Bolum, `{ // KAPAK`, sahne 130 katmanları, 2 sn): "Taş Konuşuyor" / "Bin yüz altmış bir yıl" /
"sonra çözüldü" (boy 112, son satır ALTIN). Alt başlık 36 harf olduğu için iki satıra bölündü; metin editörün kapak önerisiyle aynı.

## Sahne planı

Süreler tahminidir (Σ ≈ 246 sn: kapak 2,5 + anlatım ≈240 + kapanış 3); `video/ses/hizala_seri.py` sese göre yeniden yazar
(betiğin TSX ayrıştırıcısıyla denendi: kapak atlanır, 42 kart bulunur). Kartlar 4-kalite-metin.md ile harfi harfine aynı,
aynı sırada; en uzun satır 30 harf. Bütün dış sahnelerde ana sprite 400x230, iç sahnelerde 400x300.

| No | Süre (sn) | Konu | Zemin çizgileri | yakin / kamera | Hareket | Kartlar |
|---|---|---|---|---|---|---|
| 130 | 7.6 | Moğolistan bozkırı, şafak. Kaplumbağa kaideli yazıt taşı yalnız; harfleri yavaşça ışıyıp söner (taş konuşuyor), çiçekler rüzgârda. | sprite tabanı 632; orta plan duz(584-588) | 2.8 / 8 | fps 8 | 1, 2 (2 ALTIN) |
| 131 | 8.9 | Kopenhag, 1893, gece. Çalışma odası: kitaplık, masada kâğıtlar ve taşın fotoğrafı, mum; Thomsen ayakta bir fotoğrafa bakar. | iç mekân: taş döşeme; sprite tabanı 634; arka sıra taban−8 | 2.8 / 6 | fps 10, yaziY 240 | 3 |
| 132 | 11.1 | Thomsen yakın plan; elli bir yaşında Danimarkalı dilbilimci, elinde fotoğraf. Tek şamdan, kandil. | iç mekân: taş döşeme; sprite tabanı 634 | 3.2 / 6 | fps 10 | 4, 5 (5 ALTIN) |
| 133 | 5.8 | Orhun Vadisi, 732. Yazıt taşı dikilmiş; iki işçi kaidenin dibine toprak atar, Bilge Kağan izler. Orta planda iki atlı bekler. | sprite tabanı 632; orta plan duz(584-588); arka sıra taban−16 | 2.6 / 10 | fps 12 | 6 |
| 134 | 4.8 | Kül Tigin'in höyüğü, alacakaranlık. Eyerli, binicisiz atı başı önde bekler; koyunlar otlar (koyun yılı). | sprite tabanı 632; orta plan duz(584-588) | 2.8 / 8 | fps 10 | 7 |
| 135 | 7.5 | taş ustası çekiçle kazır; yazıcı Yollıg Tigin bağdaş kurmuş, yazıyı kâğıda yazar. Gündüz. | sprite tabanı 632; orta plan duz(584-588); arka sıra taban−14 | 2.8 / 8 | fps 12 | 8, 9 |
| 136 | 5.2 | Bilge Kağan'ın otağı, gece. Kağan sedirde yatar (nefes yavaşlar), başucunda bir hizmetkâr; şamdan ve kandil. | iç mekân: taş döşeme; sprite tabanı 634 | 2.8 / 6 | fps 8 | 10 (10 KIZIL) |
| 137 | 7.8 | 735. Aynı vadide iki yazıt taşı yan yana: Kül Tigin'in ve Bilge Kağan'ın. Gündüz, rüzgârda çiçekler. | sprite tabanı 632; orta plan duz(584-588) | 2.6 / 10 | fps 10, yaziY 240 | 11 |
| 138 | 6.7 | Tuul vadisi. Yaşlı danışman Tonyukuk, sağlığında diktirdiği iki kaba dikili taşın yanında, asasına dayanır. | sprite tabanı 632; orta plan duz(584-588); arka sıra taban−10 | 2.8 / 8 | fps 10 | 12 |
| 139 | 6.3 | yüzyıllar. Kar fırtınası; kağanlık yıkılmış, taş yalnız. Tepesinde ve kaidesinde kar birikmiş, harfleri hâlâ soluk ışıkla kıpırdar. | sprite tabanı 632; orta plan duz(584-588) | 2.8 / 6 | fps 8, kar katmanı (hava 10), yaziY 240 | 13 (13 ALTIN) |
| 140 | 6.2 | Poltava, 1709. Barut dumanlı gri ova; İsveçli subay Strahlenberg iki Rus askerinin arasında esir, sola yürür (tüfekler omuzda). | sprite tabanı 632; orta plan duz(584-588) | 2.8 / 10 | fps 16, x 300→240 | 14 (14 KIZIL) |
| 141 | 13.4 | Sibirya, Yenisey boyu, kar. Çamlar; Strahlenberg (kürk kalpak) garip işaretli kaba bir taşın önünde durmuş, kâğıda kopyasını çıkarır. | sprite tabanı 632; orta plan duz(584-588) | 2.8 / 8 | fps 10, kar katmanı (hava 10) | 15, 16 |
| 142 | 6.0 | akşam. Solda kaba Yenisey taşı, sağda kaplumbağalı Orhun taşı: aynı harfler, ikisinde birden ışır. | sprite tabanı 632; orta plan duz(584-588) | 2.6 / 8 | fps 8, yaziY 240 | 17 (17 ALTIN) |
| 143 | 7.7 | Orhun Vadisi, 1889. Gezgin Yadrintsev taşın önünde durur, eliyle gösterir; arkada çadırı ve uzakta ikinci taş. | sprite tabanı 632; orta plan duz(584-588); arka sıra taban−14 | 2.6 / 10 | fps 10 | 18 |
| 144 | 6.5 | 1890, Fin-Ugor Cemiyeti'nin seferi. Fotoğrafçı tripodlu makinesini taşa çevirir; yanında biri kopya çıkarır. | sprite tabanı 632; orta plan duz(584-588); arka sıra taban−14 | 2.8 / 8 | fps 10, yaziY 240 | 19 |
| 145 | 5.7 | 1891, Rus seferi. Ortada ak sakallı Radloff, iki yanında Ruslar; hepsinin elinde kopya kâğıtları. Arkada (orta planda) taş. | sprite tabanı 632; orta plan duz(584-588) | 2.8 / 8 | fps 10 | 20 |
| 146 | 11.5 | Kül Tigin taşı yakın plan; ön yüzde Göktürk harfleri, yan yüzde Çince yazı soluk kızıl ışıkla belirir (Çin imparatoru Xuanzong'un sözleri). | sprite tabanı 632; orta plan duz(584-588) | 3.0 / 6 | fps 8, yaziY 240 | 21, 22 |
| 147 | 7.7 | Leiden, 1892, gündüz. Sinolog Schlegel masasında Çince yüzün kopyasını okur; arkada kitaplık. | iç mekân: taş döşeme; sprite tabanı 634; arka sıra taban−8 | 2.8 / 6 | fps 10, yaziY 240 | 23 |
| 148 | 4.3 | gece, bozkır. Taşın Türkçe yüzü karanlık ve sessiz; yalnız Çince yan yüz soluk ışır. | sprite tabanı 632; orta plan duz(584-588) | 2.8 / 6 | fps 8 | 24 (24 KIZIL) |
| 149 | 11.4 | Kopenhag, gece. Helsingfors albümü Thomsen'in masasında açık; Thomsen önündeki bilinmeyen harflere bakar. | iç mekân: taş döşeme; sprite tabanı 634 | 2.8 / 6 | fps 10, yaziY 240 | 25, 26 |
| 150 | 7.5 | bozkırda taşın önünde üç grup: Rus subayı, Türkolog Radloff ve fotoğraf makineli Fin. Hepsi taşa bakar; hiçbiri çözümü yayımlamaz. | sprite tabanı 632; orta plan duz(584-588) | 2.6 / 8 | fps 10, yaziY 240 | 27 (27 KIZIL) |
| 151 | 12.4 | Danimarka Kraliyet Akademisi, 1893. Thomsen kürsüde konuşur, eli kalkar; solda dinleyiciler. | iç mekân: taş döşeme; sprite tabanı 634; arka sıra taban−12 | 2.8 / 6 | fps 10 | 28, 29 (28 ALTIN) |
| 152 | 4.8 | gün doğumu, bozkır. Taşın bütün harfleri altın renginde yanar: bu kez biri anlıyor. | sprite tabanı 632; orta plan duz(584-588) | 2.8 / 8 | fps 10 | 30 (30 ALTIN) |
| 153 | 9.7 | üstte mavi gök, altta yağız (kara) yer; arada iki insan, bir erkek ve bir kadın, taşa bakar. Taşın ilk harfleri ışır (Tengri). | sprite tabanı 632; orta plan duz(584-588); arka sıra taban−14 | 2.6 / 8 | fps 8 | 31, 32 (32 ALTIN) |
| 154 | 5.1 | Bilge Kağan halkına seslenir, eli kalkık; önde iki dinleyici, orta planda halk. | sprite tabanı 632; orta plan duz(584-588) | 2.6 / 8 | fps 10 | 33 |
| 155 | 8.5 | akşam. Çin elçisi bir Türk'e ipek uzatır; arkada (orta planda) surlu Çin şehri. | sprite tabanı 632; orta plan duz(584-588) | 2.6 / 8 | fps 10 | 34, 35 (35 KIZIL) |
| 156 | 6.0 | taşın iki yüzü aynı kadrajda: ön yüzde Göktürk harfleri altın, yan yüzde Çince yazı kızıl. | sprite tabanı 632; orta plan duz(584-588) | 3.0 / 6 | fps 8, yaziY 240 | 36 (36 KIZIL) |
| 157 | 9.6 | Bilge Kağan taşının yanında halkını uyarır gibi elini kaldırır; orta planda yurtlar ve dumanları. | sprite tabanı 632; orta plan duz(584-588); arka sıra taban−14 | 2.6 / 8 | fps 10 | 37, 38 (38 ALTIN) |
| 158 | 7.9 | Petersburg, 1894. Radloff'un masasında basılmaya başlayan okumaları (kitap yığını); Radloff ayakta. | iç mekân: taş döşeme; sprite tabanı 634 | 2.8 / 6 | fps 10, yaziY 240 | 39 |
| 159 | 7.1 | Tuul vadisi, alacakaranlık. Tonyukuk'un iki taşı yalnız; kimse bilmiyor. Koyunlar otlar. | sprite tabanı 632; orta plan duz(584-588) | 2.8 / 8 | fps 10 | 40 (40 ALTIN) |
| 160 | 6.8 | Kopenhag, şafak. Thomsen pencerenin önünde elinde kâğıtla durur; şafak ışığı odaya düşer. | iç mekân: taş döşeme; sprite tabanı 634 | 3.0 / 6 | fps 10, yaziY 240 | 41 (41 ALTIN) |
| 161 | 2.9 | gece, yıldızlı bozkır. Taşın harfleri yavaşça altın ışıkla akar. | sprite tabanı 632; orta plan duz(584-588) | 2.8 / 6 | fps 8 | 42 (42 ALTIN) |
Kapanış: "Piksel Tarih / @pikseltarihim", "Yorumlara yaz, arkadaşına gönder", 3 sn, arka sahne 161 (gece).

## Yeni figürler (hepsi orhun_yazitlari.py içinde, `ciz.piksel/hex2` + PIL ile; ciz.py'ye eklenmedi)

| Figür | Ne | Zemine nasıl basar | Sahneler |
|---|---|---|---|
| `yazit` / `tas()` | Kaplumbağa kaideli yazıt taşı: mermer gövde (ön yüz + perspektif yan yüz), ejder kabartmalı kemerli tepe, ön yüzde dikey sütunlarda Göktürk harfi benzeri işaretler (okunur metin değil, desen), `yuz="iki"` ile yan yüzde kare Çince işaretler. `kaplumbaga=False`: Tonyukuk ve Yenisey taşları gibi kaidesiz, kaba yontulmuş dikili taş. `isik`/`dalga`/`cin_isik` harfleri altın ya da kızıl yakar; `kar=True` tepeye ve kabuğa oturan kar | kaplumbağanın ayakları ve düz kabuk alt kenarı zemine; kaidesiz taşın dibinde toprak dolgu; temas gölgesi | 130, 133, 135, 137-139, 141-146, 148, 150, 152, 153, 156, 157, 159, 161 |
| `avrupali` | 19. yy Avrupalı (Thomsen, Schlegel, Radloff, Strahlenberg, Finler, Ruslar): `kisi` gövdesi, açık başta saç ya da şapka/kalpak/kasket, beyaz yaka | `kisi` gibi ayaklar zeminde | 131, 132, 140, 141, 143-145, 147, 149-151, 158, 160 |
| `masa` | Çalışma masası; üstünde kâğıt + dayalı taş fotoğrafı, açık albüm ya da kitap yığını | dört ayak zeminde | 131, 147, 149, 158 |
| `masa_mumu` | Masa üstünde pirinç şamdanda mum, titreyen alev, ışık halesi | masa üstüne oturur | 131, 149, 158 |
| `kitaplik` | Alçak kitaplık (insan boyundan kısa) | yan tahtalar zeminde | 131, 147 |
| `kursu` | Konuşma kürsüsü (Akademi) | ayaklı taban zeminde | 151 |
| `cadir` | Gezgin çadırı (A biçimi, 3/4), gergi ipleri ve kazıklar | etekler, kazıklar zeminde | 143 (orta plan) |
| `ipek_sunan` | Elinden rüzgârda kıpırdayan ipek kumaş sarkan elçi (`kisi` + kumaş) | `kisi` gibi | 155 |
| `fotograf_makinesi`, `basortulu`, `asker_1709`, `cin_suru` | KK revizyonunda eklendi (aşağıya bakın) | sehpa ayakları, ayaklar, sur tabanı zeminde | 144, 150, 153, 154, 140, 155 |

Bilinçli kararlar:
- Yazıt taşı gerçekte insan boyunun ~2 katı. Figürlerin kadrajın %30'u olması ve yazının üst bantta durması birlikte
  istenince taş ve insan aynı sırada gerçek oranla sığmıyor. Çözüm: insanlı sahnelerde taş **arka sırada** (zemini
  10-16 px yukarıda) duruyor, yani hem küçük hem yüksek; taş tek başına olduğunda öne geliyor ve kadrajın ~%35-38'i.
- Bilge Kağan'ın ölümü (136) "Çin kaynaklarına göre zehirlenir" dendiği için zehir gösterilmedi: yatan kağan, başucunda hizmetkâr.
- Poltava (140) ve Fin seferi (144, 150) ilk çizimde kütüphanedeki `sapka` ve `kisi(silah="kamera")` ile yapılmıştı;
  KK revizyonunda dönemine uygun yeni figürlerle değiştirildi (üç köşeli şapkalı `asker_1709`, levhalı `fotograf_makinesi`).
- Tonyukuk taşları kaplumbağasız iki dikili taş olarak çizildi (gerçekte de kaidesiz iki taş).

## Grafiker öz denetimi

**Otomatik denetimler (orhun_yazitlari.py, her sahne çizilirken çalışır; biri bozulursa betik durur):**
1. `taban_denetimi` (sahneler.sprite): her karede en alt opak piksel son satırda; havada duran figür yok.
2. `_ust_sinir`: sprite'ın 3 px'ten geniş her satırı, sahne başında ve sonundaki yakınlaşmada (yakin·1,06) ekran yazısının
   bandına (ekran y 230 ile o sahnenin en uzun kartının alt kenarı +12) düşmüyor. Yazı alt kenarı her sahne için
   TimurSeri.tsx `Yazi` formülüyle (satır sayısı, en uzun satır, boy, yaziY) hesaplandı (`YAZI_ALT`). Kandil zinciri
   1 px olduğu için sayılmaz; kandil kadrajın tepesinde, etiketin üstünde kalır.
3. `_orta_kontrol`: orta plana eklenen atlılar, yurtlar, çadır, Çin şehri, kalabalık ve uzak taşların tepesi de yazının altında.
4. `_kadraj`: tam opak bütün pikseller sahne sonu yakınlaşmasında görünür aralıkta (yerel x 200 ± 270/(yakin·1,06)), 2 px payla;
   kenarda kesik figür yok; figür sprite'ın üst kenarına değmiyor.
5. Ölçek: ön sıradaki insanlar başlıksız boyla kadrajın %30'u (`_K`, `olcek`); 4-5 satırlı kartların sahnelerinde yazı
   `yaziY: 240` ile yukarı alındı, kart 3 ve 36'da boy 72/80. Taçlı Bilge Kağan'ın olduğu 133, 154, 157'de tacın ucu esas alındı.
   At = insan × 2,9/2,6 (134); orta plandakiler hem küçük hem yüksek zeminde (duz 584-588).

**Gözle bakış:** 32 sahnenin hepsinin sprite PNG'lerinden kare 0 ve 12'yi büyütüp açtım; ayrıca TSX dönüşümünü
(yakın çekim, odak, paralaks, yazı kutuları) taklit eden bir önizleyiciyle her sahneyi sahne başı ve sonu yakınlaşmasında,
kart kutularıyla birlikte inceledim.

**Bulup düzelttiklerim:**
- Taşın yan yüzü ilk çizimde tepede boynuz gibi sivri bir üçgen yapıyordu → yan yüz ön yüzün kaydırılmış kopyasıyla
  (ekstrüzyon) yeniden çizildi; kemerli tepe yan yüzde de düzgün.
- Kar örtüsü taşın ve kabuğun üstünde taşan, havada duruyormuş gibi görünen bir "şapka"ydı → kar artık şeklin kendi
  üst kenarında 1-2 px beyaz şerit (139, 141).
- 134: at kadraja sığmıyordu (sağdan kesik) → ölçek ve konum küçültüldü, höyük ve koyunlar yeniden dizildi.
- 143: orta plandaki yük atı sol kenarda kesiliyordu → çıkarıldı; çadır büyütülüp Yadrintsev'in arkasına alındı.
- 133: arka plandaki atlılar Bilge Kağan kadar büyük görünüyordu → küçültüldü (derinlik).
- 155: orta plandaki deve, öndeki Türk'ün başının arkasında karışık bir leke yapıyordu → çıkarıldı (ipek elçinin elinde).
- 150: fotoğraf makinesi Radloff'un gövdesini örtüyordu → sıralama Fin–Rus–Radloff yapıldı; makine taşa dönük.
- 153: kadının sarı başörtüsü sarı saç gibi okunuyordu → beyaz başörtüsü.
- Thomsen'in saçı yüzünü örtüyordu → saç başın üst üçte birine ve enseye indirildi, yüz görünüyor.
- İlk ölçek, figürü taçlı kağana göre ayarladığı için başlıksız figürler kadrajın ~%26'sında kalıyordu → ölçek başlıksız
  boya göre yeniden ayarlandı (%30); ardından kenara taşan 131, 134, 135, 136, 140, 147, 149, 150, 151, 157 konumları düzeltildi.
- Uzak taşlar ve orta plan şehri ilk ölçekte yazı bandına giriyordu (143, 145, 150, 155) → küçültüldü (otomatik denetim yakaladı).

**Son durum:** `python3 -I video/piksel/orhun_yazitlari.py` 32 sahneyi hatasız çiziyor (bütün denetimler geçti);
`cd video && npx tsc --noEmit -p .` temiz; TSX'teki 42 kart nihai kart listesiyle bire bir aynı (betikle karşılaştırıldı).

**Kalite kontrol için notlar (bilinen sınırlar):**
- 147 (Leiden, gündüz) pencerelerinde `ic_mekan` pencere çiziminin kar taneleri ve denizlik birikintisi var; kış günü gibi okunuyor.
- 155'te Çin şehri, 136'da kilim kadraj kenarından taşar: bunlar arka plan dokusu, figür değil.
- Taşın üstündeki işaretler Göktürk harflerine benzeyen bir desendir, gerçek bir metin okunmaz.
- Render ve ses hizalama bu teslimde yapılmadı (ses dosyası henüz yok; Root.tsx kaydı kod tarafında).

## Görsel KK revizyonu (6-kalite-gorsel.md, 5 zorunlu düzeltme + iyileştirmeler)

`OrhunYazitlari.tsx`'teki `sure` değerlerine ve kart metinlerine dokunulmadı (sese hizalı); TSX'te yalnız kapak yorumu düzeltildi.
Bütün değişiklikler `video/piksel/orhun_yazitlari.py` içinde; ilgili sahneler yeniden çizildi, otomatik denetimler geçti.

| # | Sahne | Sorun | Yapılan |
|---|---|---|---|
| 1 | 136 | Yatan Bilge Kağan çocuk boyunda (ölçek 0,58·K), sakal yana gaga gibi | Yatan figür ayaktaki hizmetkârla aynı ölçekte (K): baş aynı boyda, sedir boyu buna göre. Sakal çizilmedi (sırtüstü yatan). Hizmetkâr yatağın arkasında, başucunda (arka sıra, zemin −12). Kadraja sığmayan şamdan çıkarıldı; tavanda kandil kaldı |
| 2 | 150 | Taş makinenin arkasında kalıyor, objektif kadraj dışına bakıyor | Yeni düzen: solda Radloff (taşa döner), ortada taş, açıkta (arka sıra), sağında levhalı makine, objektif taşa dönük; sağda Fin fotoğrafçı ve Rus subayı. Harfli yüzü hiçbir şey örtmüyor |
| 3 | 144, 150 | İki makaralı sinema kamerası (1941 çizimi) 1890 için yanlış | Yeni figür `fotograf_makinesi`: üç ayaklı ahşap sehpa (ayaklar zeminde), ahşap kutu, öne uzanan körük, pirinç objektif, arkada sarkan siyah örtü. Fotoğrafçı makinenin arkasında elini makineye uzatır. `kisi(silah="kamera")` artık kullanılmıyor |
| 4 | 130 ve kapak | Uzaktaki ovoo uçan daire gibi, havada duruyor izlenimi | Ovoo 130'dan çıkarıldı (planda yoktu); orta plan boş bozkır |
| 5 | 153 (ve 154) | Kadının başörtüsü göz satırını örtüyor, yüz boş | Yeni figür `basortulu`: örtü yalnız alnı ve saçı örter, yüzü iki yandan çerçeveler, göz pikseli açık. 154'teki kadın da aynı figürle çizildi |

İyileştirmeler:
- 134: at başı yukarıda (bas 0,15), köşeli otlayan baş yerine okunur profil.
- 130, 137, 152: çiçekler 0,32·K'den 0,15·K'ye (insan ölçeğinde kır çiçeği).
- 140: yeni figür `asker_1709`: üç köşeli şapka (altın kenar), tüfek omuzda çapraz; esir Strahlenberg (mavi, silahsız) elleri sırtında bağlı, arkadaki Rus askerinin elindeki iple yürür.
- 155: Avrupa şatosu gibi okunan `sehir` yerine yeni figür `cin_suru`: sıkıştırılmış toprak sur, mazgallar, kırmızı direkli iki katlı, kıvrık saçaklı kapı köşkü, insan boyundan büyük kapı; iki figürün arasında görünür.
- 149, 158: masa mumu masanın içine alındı (214).
- 151: ak sakallı dinleyici koyu sakallı yapıldı (Radloff sanılmasın).
- 158: Petersburg odası penceresiz, yeşil duvarlı (Kopenhag odasından ayrılsın).
- TSX kapak yorumu düzeltildi: logo/@pikseltarihim bandı yalnız kapanış kartında, kapakta etiket ve başlık var.

Öz denetim (revizyon): 136, 140, 144, 150, 153, 155'in sprite karelerini (0 ve 12) büyütüp açtım; TSX dönüşümünü taklit eden
önizlemeyle 130, 134, 136, 140, 144, 149, 150, 153, 155, 158'e sahne sonu yakınlaşmasında, kart kutularıyla baktım. Kenarda
kesilme, yazı bandına giren nesne ve havada duran nesne yok (otomatik denetimler: taban, yazı bandı, kadraj, orta plan).
`npx tsc --noEmit -p .` temiz. Önceki turda kare düşmeyen sahneler (132, 133, 135, 138, 139, 142, 143, 145, 147, 148, 152, 154,
157, 159, 160, 161) bu revizyonda değişmedi (154 yalnız kadının yüzü); yeniden kontrolde bunlardan da kare alınması önerilir.

Kalan bilinen sınırlar: 136'da sedir kadrajın büyük bölümünü kaplıyor (aynı ölçek kuralının sonucu); 147'nin pencerelerinde
`ic_mekan` kar taneleri var; 149'da Thomsen hâlâ ayakta okuyor (albüme eğilme pozu kütüphanede yok).
