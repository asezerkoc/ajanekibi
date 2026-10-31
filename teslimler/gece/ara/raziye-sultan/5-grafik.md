# 🟢 Grafiker: Oğullarımdan İyi (Raziye Sultan, Delhi 1236-1240)

**İş:** Piksel Tarihim (@pikseltarihim), gece vardiyası 3/10, slug `raziye-sultan`
**Girdi:** 4-kalite-metin.md → "Nihai seslendirme metni" ve "Nihai ekran kartları" (51 kart, harfi harfine; birleşimleri seslendirmeyle karakter karakter aynı, betikle doğrulandı) ve grafiker kart ipuçları.
**Sahneler:** 210-248 (39 sahne). 249 boş, yedek. Kapak sahne 210'un katmanlarıyla yapıldı. Üç sahne iki kez kullanılıyor: 212 (kart 4 ve 44), 217 (kart 10 ve 50), 238 (kart 34-35 ve 47). Toplam 42 Bolum + kapak.
**Dosyalar:**
- `video/piksel/raziye_sultan.py`: 39 sahne fonksiyonu, `SAHNELER`, `__main__`. Yeni figürler bu dosyanın içinde (aşağıda).
- `video/src/sahneler/RaziyeSultan.tsx`: `RAZIYE_SERI`, `RAZIYE_KARE`, `RaziyeSultan`. Etiket "PİKSEL TARİHİM · RAZİYE SULTAN", ses `raziye-sultan-anlatim.mp3`.
- Çıktı: `video/public/sahne210…248-{gokyuzu,uzak,orta,on,karakter}.png`
- `Root.tsx`'e ve başka konuların dosyalarına dokunulmadı.

**Kapak (3 satır, boy 112, ALTIN, 2,0 sn, yaziY 270):** "Oğullarımdan" / "İyi" / "Delhi tahtındaki tek kadın". Bu, 2-metin, 3-editör ve 4-kalite-metin'in onayladığı kapak (başlık "Oğullarımdan İyi", alt başlık "Delhi tahtındaki tek kadın"). Brifteki "Delhi'nin Tek Sultanı" seçeneği kullanılmadı, çünkü görsel kalite kontrol Çelebi Mehmed işinde onaylı kapak metninden sapmayı reddetmişti. Kapağın arka planı sahne 210'dur (Cuma avlusu), kamera sabit.

**Süre:** Kart süreleri tahmini: okunan harf sayısıyla orantılı, yavaş kartlara +0,6 sn, toplam anlatım 252,0 sn. `video/ses/hizala_seri.py` süreleri sese göre yeniden yazar. Kapak bloğu `    { // KAPAK` ile açılıyor. Diğer bloklar yalnızca `    {` ile açılıyor, yorumlar üst satırda.

**Renk dili (kalite kontrolün önerisi):** ALTIN = motif ve cevap: kart 10, 18, 19, 43 ve 50 ("Oğullarımdan iyi" motifi üç kez, sikkedeki ad, "Peçeyi."). KIZIL = "ama" dönüşleri ve kayıp: kart 16, 27, 30 ve 48.

**Yön dili:** Sol Bathinda'dır (kuzeybatı), sağ Delhi, saray ve Gwalior yolu. Raziye'nin ordusu Bathinda'ya sola yürüyor (231). Raziye ve Altuniya Delhi'ye sağa yürüyor (235). Kalabalık saray kapısına sağa akıyor (220). İbn Battûta Delhi'ye sağa giriyor (239).

**Kişi renkleri (bütün videoda aynı):**
- Raziye: lacivert-camgöbeği giysi. Kaynaksız olduğu için kırmızı yok.
  - 1236-1238 arası peçeli: beyaz başörtüsü ve yüz peçesi, yalnızca gözler açık.
  - Kart 20'den sonra peçesiz: kısa tunik, kürk kenarlı koyu külah, açık saç.
- İltutmış: mor kaftan, kır sakal, sarık, altın pelerin.
- Fîrûz: altın sarısı giysi, sakalsız.
- Şah Terken: koyu mürdüm.
- Türk köle emîrleri: kahve ve koyu yeşil giysi, kalpak ya da börk.
- Yakut: yeşil giysi, koyu ten.
- Altuniya: kahverengi giysi, kalpak.
- Behram Şah: yeşil giysi.
- Minhâc: arduvaz mavisi giysi. 1231'de koyu sakallı, 1260'ta ak sakallı.
- İbn Battûta: kum rengi giysi, asa.

**Kaynaksız ayrıntılar çizilmedi:**
- Cami adı ve minare yok. Avlu yalnızca sivri kemerli revak olarak çizildi.
- Kırmızı giysi, kadeh ve at anekdotu yok. Fîrûz'un eğlencesi meyve sinisiyle gösteriliyor.
- Yakut'un ölümü ve Raziye'nin ölümü gösterilmiyor. Yakut'un ölümü binicisiz eyerli atla anlatılıyor. Kart 35'te Minhâc'ın sahnesi kalıyor, fail yok.
- Köylü sahnesi yalnızca kart 37-39'da. Şiddet yok: uyuyan kadın ve ona bakan köylü.

## Sahne planı

Zeminler:
- Dış mekân: sprite 400×220, taban 632 (sprite'ın son satırı). Orta plandaki yapılar ve figürler `duz(586-592)` düz şeridine oturuyor.
- İç mekân: sprite 400×300, taban 634. `ic_mekan` taş döşemesi 596'dan başlıyor. Kandil zinciri tavandan iniyor (`_kz`).
- Bütün sahnelerde yazı yaziY 260'tan başlıyor, kapakta 270'ten.

Süreler tahminidir (sn, sahne arası 0,5 dahil).

| No | Süre | Konu | Zemin çizgileri | yakin / kamera | Hareket | Kartlar |
|---|---|---|---|---|---|---|
| Kapak | 2,5 | Başlık, sahne 210 arka planı | 210 ile aynı | 2.8 / 0 | 210 ile aynı | Kapak |
| 210 | 12,3 | Delhi, Kasım 1236, Cuma: revak önünde kalabalık. Taş sekide peçeli Raziye konuşuyor, iki dinleyici ona dönük | sprite 632, seki üstü 622; revak `duz(586)`, kalabalık `duz(590)` | 2.8 / 8 | Raziye'nin kolu kalkıp iniyor | 1, 2 |
| 211 | 3,9 | Alacakaranlık ova: peçeli Raziye yalnız; geride yaşlı ağaç | sprite 632; ağaç `duz(588)` | 2.8 / 8 | Ön planda otlar rüzgârda | 3 |
| 212 | 3,4 + 5,0 | Boş taht. Tavandan kandil, iki yanda şamdan, halıda ışık havuzu | iç 634 | 2.8 / 6 | Kandil ve mumlar titriyor | 4, 44 |
| 213 | 4,7 | Karanlık oda: peçeli Raziye yakın planda, yalnızca gözleri görünüyor | iç 634 | 3.2 / 6 | Mum, kandil | 5 |
| 214 | 5,4 | İltutmış tahtta; solda Minhâc (genç) rahlede yazıyor | iç 634; taht ayakları zeminde, sultan oturakta | 2.8 / 6 | Kandil | 6 |
| 215 | 6,6 | Delhi kapısı, 1231: atlı İltutmış kolunu Gwalior'a (sağa) kaldırıyor; geride sağa yürüyen ordu; peçeli kızı kapıda kalıyor | sprite 632; şehir `duz(586)`, ordu `duz(592)` | 2.6 / 8 | Kol | 7 |
| 216 | 8,4 | Divan: İltutmış ve peçeli kızı; karşılarında iki emîr, öndeki itiraz ediyor | iç 634 | 2.8 / 6 | Emîrin kolu | 8, 9 |
| 217 | 2,3 + 5,4 | Motif: İltutmış ve kızı karşı karşıya, sessiz; şamdan | iç 634 | 3.0 / 6 | Babanın eli | 10, 50 |
| 218 | 7,5 | Yeşil örtülü tabut sehpada; emîr tahttaki genç Fîrûz'u gösteriyor | iç 634; sehpa ayakları zeminde | 2.8 / 6 | Kol, kandil | 11 |
| 219 | 6,0 | Gece: Fîrûz minderde meyve sinisinin başında; sağda karanlıkta Şah Terken | iç 634 | 2.8 / 6 | Kandil | 12 |
| 220 | 4,6 | O Cuma: halk sağa, saray kapısına yürüyor; geride sekide kolu kalkık peçeli Raziye | sprite 632; saray `duz(586)`, seki `duz(590)` | 2.6 / 12, x [245, 295] | Yürüyüş (adım kaymayla uyumlu) | 13 |
| 221 | 5,1 | Peçeli Raziye tahtta; Şah Terken'i muhafız sola götürüyor | iç 634 | 2.8 / 6 | Kandil | 14 |
| 222 | 5,0 | Zindan: Fîrûz samanın üstünde oturuyor; meşaleli gardiyan | iç 634 | 2.8 / 6 | Meşale | 15 |
| 223 | 6,0 | Yakın plan: babasının adıyla gümüş sikke, ahşap yuvaya dikili | iç 634; yuva zeminde, sikke yuvanın yarığında | 3.2 / 4 | Sikkenin yüzünde kayan parıltı | 16 |
| 224 | 5,7 | Darphane: usta örsteki kalıba çekiçle vuruyor; mangalda kor | iç 634; kütük ve mangal ayakları zeminde | 2.8 / 6, fps 12 | Çekiç iniyor, vuruşta kıvılcım | 17 |
| 225 | 7,6 | Yakın plan: 1237 kalıbı. Ortadaki iki satır (ad ve unvan) altın ışıkla parlıyor | 223 ile aynı | 3.2 / 4 | Işık nabzı, parıltı | 18, 19 |
| 226 | 5,5 | Peçeli Raziye; hizmetkârın tepsisinde katlanmış tunik ve külah | iç 634 | 2.8 / 6 | Kol | 20 |
| 227 | 6,7 | Fil üstünde peçesiz, külahlı sultan sağa yürüyor; filbaşı boyunda; geride seyreden kalabalık | sprite 632; dört ayak zeminde | 2.6 / 10, x [245, 290] | Filin adımı, hortum | 21 |
| 228 | 5,3 | Raziye ovada sağa dörtnala at sürüyor (İbn Battûta'nın aktarımı) | sprite 632; ağaçlar `duz(588)` | 2.6 / 14, x [240, 300], fps 24 | Dörtnala, toz | 22 |
| 229 | 4,6 | Akşam, revak gölgesi: üç emîr; ikisi fısıldaşıyor | sprite 632; revak `duz(586)` | 2.8 / 6 | Kol | 23 |
| 230 | 8,1 | Ahırlar: Yakut atlı Raziye'nin atını dizgininden tutuyor; geride ahır bölmeleri ve iki emîr | sprite 632; ahır `duz(586)`, emîrler `duz(590)` | 2.6 / 8 | Kol, dizgin | 24, 25 |
| 231 | 7,3 | Nisan 1240: Raziye önde, arkasında bir atlı; sola, Bathinda kalesine yürüyorlar | sprite 632, arka atlı 624; kale `duz(586)` | 2.6 / 12, x [290, 250] | Yürüyüş | 26 |
| 232 | 6,2 | Kızıl akşam, Bathinda kale kapısı: iki muhafız arasında Raziye; sağ geride binicisiz at başı önde bekliyor | sprite 632; kale `duz(586)`, at `duz(592)` | 2.8 / 6 | Kol | 27 |
| 233 | 6,6 | Kale odası, gece: Raziye taş zeminde oturuyor; yerde soğuk ışık | iç 634 | 3.0 / 6 | Sabit | 28 |
| 234 | 9,5 | Behram Şah tahtta; iki emîr diz çökmüş | iç 634; dizler zeminde | 2.8 / 6 | Kandil | 29, 30 |
| 235 | 5,6 | Raziye ve Altuniya atlı, sağa (Delhi'ye) yürüyorlar; Altuniya arka sırada | sprite 632, arka 624 | 2.6 / 12, x [250, 295] | Yürüyüş | 31 |
| 236 | 6,8 | Kaithal ovası, Ekim 1240: ikisi atlarında sağa bakıyor; karşıda ordunun atlı ve yaya sırası | sprite 632, arka 624; ordu `duz(586-590)` | 2.6 / 8 | Sabit (yavaş kart) | 32 |
| 237 | 5,0 | Boş ordugâh: ipi kopmuş çadır; Raziye ve Altuniya yalnız; uzakta askerler uzaklaşıyor | sprite 632; askerler `duz(592)` | 2.8 / 6 | Kol | 33 |
| 238 | 8,5 + 5,5 | Yaşlı Minhâc rahlede yazıyor; şamdan, kitaplar | iç 634 | 2.8 / 6 | Kandil, mum | 34, 35, 47 |
| 239 | 5,0 | İbn Battûta asasıyla Delhi'ye (sağa) yürüyor; sağ geride surlar | sprite 632; şehir `duz(586)` | 2.6 / 12, x [245, 290] | Yürüyüş | 36 |
| 240 | 5,5 | Köy, ikindi: köylü ekmek uzatıyor, Raziye elini uzatıyor | sprite 632; evler `duz(586)` | 2.8 / 6 | Kol | 37 |
| 241 | 5,5 | Gece, ağaç altı: Raziye bohçaya başını koymuş uyuyor; giysisinde mücevher parıltısı; köylü bakıyor | sprite 632; ağaç `duz(588)` | 2.8 / 6 | Nefes, parıltı | 38 |
| 242 | 6,5 | Şafak, tarla: ekin sıralarının ortasında küçük kubbeli türbe | sprite 632 | 2.6 / 8 | Otlar | 39 |
| 243 | 4,3 | Bugün: sehpada harita; Delhi, Kaithal ve Tonk gerçek göreli konumlarında yanıp sönüyor | iç 634; üç ayak zeminde | 2.8 / 6 | Işık nabzı | 40 |
| 244 | 8,5 | Delhi, dar sokak: eski evler, çatısız dört duvar, içinde iki beyaz kabir; önde mavi devlet levhası | sprite 632; evler `duz(588)`, sokak 590 | 2.6 / 8 | Sabit | 41, 42 |
| 245 | 3,1 | Cevap: peçesiz Raziye ayakta, peçe ayağının dibinde yerde | iç 634 | 2.8 / 6 | Kandil | 43 |
| 246 | 9,8 | 1260: Minhâc diz çöküp ciltli kitabını tahttaki Sultan Nâsıreddin'e sunuyor | iç 634 | 2.8 / 6 | Kol | 45, 46 |
| 247 | 5,0 | Yakın plan: rahlede açık el yazması, hokka ve kalem; sayfada mum ışığı | iç 634 | 3.2 / 4 | Işık titriyor | 48, 49 |
| 248 | 2,9 | Son soru: sehpada yan yana katlanmış peçe ve yastıkta altın taç | iç 634 | 3.0 / 6 | Taşlarda parıltı | 51 |

**Kapanış:** "Piksel Tarih / @pikseltarihim", "Yorumlara yaz, arkadaşına gönder", 3 sn. Arka plan sahne 241 (gece), `gece: true`.

## Yeni figürler (hepsi `raziye_sultan.py` içinde; `ciz.py` ve paylaşılan dosyalar değişmedi)

**Başlıklar:**
- `pece`: başı ve omuzları saran örtü, ense kuyruğu ve yüz peçesi; yalnızca göz yarığı açık.
- `kulah`: tepesi yuvarlatılmış keçe külah, kürk kenar, altın süs ve açık saç.
- İkisi de `timur_figur._baslik` çiziciye yalnızca bu betik çalışırken eklenir; dosya değişmez. Bu yüzden `kisi`, `oturan` ve `atli` iki başlığı da kullanabiliyor.

**`fil_alay` (bileşik figür):** `timur_figur.fil` (kulesiz) + lacivert, altın kenarlı çul + açık hevdec + hevdecte bağdaş kurmuş Raziye + boyunda filbaşı. Parçalar ayrı ayrı konturlanıyor.
- Ölçek: fil ve insanlar aynı s değerinde. Fil omzu ≈ 28·s, insan ≈ 15,5·s. Oran ≈ 1,8, gerçeğe yakın (Asya fili omzu ~2,7 m, insan ~1,6 m).
- Dört ayak zemine basıyor.
- Not: kütüphanede `fil` zaten vardı. Gövdesi kullanıldı; kulesi ve küçük binicisi yerine sultanı gösteren yeni üst yapı çizildi.

**Diğer yeni figürler (hepsi zemine ya da düz zemine oturuyor):**
- `seki`: konuşma sekisi.
- `revak`: sivri kemerli avlu duvarı, minaresiz.
- `sikke_yuva`: büyük gümüş sikke ve ahşap yuvası. Kûfî benzeri yazı tasarım, okunmuyor. `isik` ile ad parlıyor.
- `ors`: kütük, örs ve kalıp; çekici sahne çiziyor.
- `tepsi`: tunik ve külah.
- `meyve_tepsisi`
- `sehpa_tabut`
- `ahir`
- `cadir`: kopuk ipli, terk edilmiş.
- `kubbe_turbe`
- `harita_sehpasi`
- `sokak_evleri`
- `mezar_avlusu`: çatısız dört duvar ve iki kabir.
- `levha`
- `pece_yerde`
- `uyuyan`
- `acik_kitap`
- `pece_ve_tac`
- `kitap_elde`

## Grafiker öz denetimi

**Otomatik denetimler (betikte; biri bozulursa betik durur):**
1. **Taban:** `taban_denetimi`, sprite'ın her karesinde en alt opak pikselin son satırda olduğunu doğruluyor. Havada duran figür yok.
2. **Kenar:** `_kadraj`, 4 karede (0, 6, 12, 18) tam opak piksellerin hepsinin sahne sonu yakınlaşmasında da (yakin·1,06) görünür aralıkta kaldığını doğruluyor. Kesik figür, şamdan ya da çimen tutamı yok. Figürlerin üst kenara değmediğini de denetliyor.
3. **Orta plan görünürlüğü:** `_gorunur`, orta plandaki önemli nesnelerin kayan kamerada başta ve sonda görünür kaldığını doğruluyor.
4. **Yazı bandı:** `_bant_denetimi`, bantları ve yakin değerlerini `RaziyeSultan.tsx`'ten okuyor (tek kaynak, kapak dahil). Sprite'ta ve orta planda yazı satırlarına giren opak piksel olmadığını yakin ve yakin·1,06 için doğruluyor. Figür ölçekleri (`_K`, `_A`, `_olc`) kadrajın %30'unu hedefliyor; yazıya sığmazsa sığan en büyük ölçeği alıyor.
5. **Fizik:** Yapılar (`revak`, `ahir`, `sokak_evleri`, `mezar_avlusu`, `kubbe_turbe`, `seki`) `duz_zemin` ile yalnızca düz zemine kuruluyor.
6. **Son durum:** `python3 -I video/piksel/raziye_sultan.py` 39 sahnenin hepsini hatasız çizdi. `cd video && npx tsc --noEmit -p .` temiz geçti.

**Gözle bakılanlar:**
- Remotion kamerasını taklit eden bir önizleyiciyle (katmanlar, sx/odak çevresinde yakin ve yakin·1,06 yakınlaşma, yazı bandı kutusu) 39 sahnenin ilk ve son karesine baktım.
- Sprite PNG'lerine ayrıca baktım: 227, 230, 241, 224, 232, 244, 235 ve 246.
- Figürler zemine basıyor. Atlar ve fil dört ayak üstünde. Yazı kutusu hiçbir başlıkla (sarık, külah, peçe) çakışmıyor. Gece sahnelerinde konturlar görünüyor.

**Düzelttiklerim:**
1. **Külah:** İlk çizimde sivri ve uzundu, "büyücü şapkası" gibi okunuyordu. Alçak, tepesi yuvarlatılmış, kürk kenarlı Türk külahına çevrildi.
2. **Kenarda kesilme:** 14 sahnede kenar denetimi kesilme yakaladı (214, 215, 216, 218, 219, 220, 221, 222, 231, 232, 235, 236, 237, 239). Figürler içeri alındı. Atlı sahnelerde at ölçeği kadrajın %40'ından %34'üne indirildi, ikinci atlı arka sıraya (zemin 624, %90-92 ölçek) alındı. Zindandaki saman kenardan çekildi.
3. **Deve:** 239'da deve, İbn Battûta ile aynı ölçekte kadraja sığmıyordu (kesiliyordu). Çıkarıldı; gezgin asasıyla yalnız yürüyor.
4. **Yazı bandı:** 241'de orta plandaki ağacın tepesi yazı bandına giriyordu. Ağaç küçültüldü.
5. **Gökyüzü:** Yakın çekimde gökyüzü düz gri görünüyordu, çünkü gradyan 960 satıra yayılmıştı. Gradyan görünür gök şeridine (y 360-600) sıkıştırıldı; gün, akşam ve gece renkleri artık okunuyor. Ay ve güneş konmadı (yazı bandına düşerdi).
6. **Diğer figür düzeltmeleri:**
   - Kubbe türbenin alemi kubbenin içinde kalıyordu; tepeye alındı.
   - Mezar avlusunda kabirler ön duvarın arkasında kayboluyordu. Ön duvar alçaltıldı, kabirler yükseltildi.
   - Uyuyan figürde yastık başın altına alındı. Ayak ucundaki külah köylünün ayağıyla karışıyordu; kaldırıldı.

**Kalite kontrol için notlar (ret değil, bilinçli kararlar):**
- 227'de fil grubu yazı bandı yüzünden kadrajın yaklaşık %30'u kadar. Fil insandan büyük olduğu için insanlar küçük.
- 248'deki sehpa kadrajın %16'sı (nesne yakın planı).
- 212, 217 ve 238 iki kez kullanılıyor (motif dönüşü ve kaynak etiketi).

## Görsel KK revizyonu (31 Ekim 2026, 🟢 Grafiker)

Kalite kontrolün 8 zorunlu düzeltmesi (`6-kalite-gorsel.md`) ve ucuz iyileştirme önerileri yapıldı. `RaziyeSultan.tsx` değişmedi: süreler, kartlar, yakin değerleri aynı. Değişen yalnızca `video/piksel/raziye_sultan.py` ve sprite/katman PNG'leri. Bu bölüm, yukarıdaki sahne planı tablosunda 222, 230, 233, 236 ve 248 satırlarının yerine geçer.

**Zorunlu düzeltmeler**

| # | Sahne | Ne yapıldı |
|---|---|---|
| 1-2 | 219, 221 (Şah Terken) | Başörtüsü artık alından başlıyor, göz açıkta: açık göz akı ve koyu bebek var. Örtü çenenin altını ve boynu sarıyor. Çene altındaki saydam delik kapandı. |
| 3 | 235, 236, 237 (Altuniya) | Kalpak 0,4·s yukarı alındı, kürk kenarı alnın üstünde bitiyor. Göz akı ve bebek var. Gözle sakal arasında bir piksellik ten şeridi kalıyor. |
| 4 | 230 (Yakut) | Yeni küçük sarık ("sarik_k") kaşa inmiyor. Koyu tende açık göz akı (#f2ece0) ve koyu bebek telefonda seçiliyor. 231'de Yakut yok, orada değişiklik gerekmedi. |
| 5 | 227 (filbaşı) | Küçük sarık yukarıda, sakal kaldırıldı (genç, köse filbaşı). Göz akı ve bebek görünüyor. |
| 6 | 248 | Beş dişli Avrupa tacı kaldırıldı. Yastıkta Raziye'nin videoda giydiği külah duruyor: koyu mor keçe, kürk kenar, altın süs, camgöbeği taş, ak sorguç. Son soruda Raziye'nin iki başlığı yan yana: peçe ve külah. |
| 7 | 236 | İkili kadrajın soluna alındı (atlar kadrajın %30'u). Behram Şah'ın ordusu sağdaki boşlukta, ovanın gerisinde: yeşil flamalı 4 mızraklı atlı ve önlerinde miğferli yaya sırası. Hiçbir at başının arkasında kalmıyor. `_gorunur` ordunun bütün x'lerini sahne sonu yakınlaşmasında 20 px payla denetliyor; son atlı kadrajın içinde bitiyor. |
| 8 | 222 (ve aynı gözle 233) | Yeni `_zindan` katmanı var. Kaba kesme taş duvar, yüksekte tek dar ve sivri tepeli mazgal (iki demir parmaklık, dışı gece), mazgaldan inen soluk ay ışığı, demir parmaklıklı kemerli hücre kapısı (kilitli), duvarda zincirli halka. Saray kemerleri ve yıldızlı büyük pencereler kaldırıldı. Fîrûz yeni `saman_yigini` figürünün üstünde oturuyor; yığın zemine basıyor, iki yanından taşıyor. 233 (Bathinda hücresi) de aynı katmanı kullanıyor; mazgal Raziye'nin baktığı tarafta (solda) ve kadraj içinde. |

**Bütün figürlere uygulanan göz kuralı:** `timur_figur._baslik`, bu betik çalışırken sarmalanıyor (paylaşılan dosya değişmedi). s ≥ 2,5 olan her figüre peçe dışında açık göz akı ve bakış yönünde koyu bebek çiziliyor. Kütüphanenin eski tek pikselli gözü önce ten rengiyle siliniyor. Baş ile gövde arasındaki saydam pikseller boyunla dolduruluyor. Bu yüzden bütün figürlü sahnelerin sprite'ları yeniden çizildi; yüzler videonun her yerinde aynı dili konuşuyor.

**Yapılan iyileştirme önerileri**
- 230 ölçek: Yakut atlıyla aynı insan ölçeğinde (K = A; önceki değer A·2,6/2,9'du). Arkadaki iki emîr, Yakut'un omzunun arkasından ovanın gerisine (Yakut'un başı ile atın başı arasındaki boşluğa) alındı. Eskiden "omzunda duran adam" gibi okunuyorlardı.
- 216 ve 229 emîrleri: EMIR2 artık kum rengi küçük sarıklı ve kır sakallı. Böylece kalpaklı EMIR1 ve börklü EMIR3'ten ayrılıyor.
- 234 ve 246 sultanları: Nâsıreddin altın sarıklı ve sakalsız, Behram Şah ak sarıklı ve sakallı. Giysi renkleri de farklı (yeşil ve lacivert).
- 216: İltutmış'ın bacak arasında kopuk blok gibi görünen pelerini bu sahnede kaldırıldı.
- Yapılmayanlar: kapak hiyerarşisi `RaziyeSultan.tsx`'te (dokunma yasağı var). 232'deki binicisiz at ve 227'deki kamera yakınlığı ret nedeni değildi; bilinçli olarak bırakıldı.

**Denetim**
- `python3 -I video/piksel/raziye_sultan.py` 39 sahnenin hepsini hatasız çizdi. Taban, kadraj (yakin·1,06), `_gorunur` ve yazı bandı denetimleri geçti.
- `npx tsc --noEmit -p .` temiz geçti.
- Remotion karelerine tek tek baktım: 216, 219, 221, 222, 227, 229, 230, 233, 234, 235, 236 (ortası ve sahne sonu), 237, 246, 248. Gözlü yüzleri piksel yakınlaştırmasıyla da kontrol ettim (227, 230, 235). Zemine basmayan nesne, kesik figür ya da yazıya giren nesne görmedim.
