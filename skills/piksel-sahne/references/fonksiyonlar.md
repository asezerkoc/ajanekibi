# Fonksiyon referansı (kaynak koddan üretildi)

Her fonksiyonun imzası ve kaynak koddaki açıklaması. `img`/`t` tuval (PIL RGBA), `zemin`/`z` zemin listesi (her x için y),
`x` ızgara x'i (figürün ayak izi merkezi), `s` ölçek (1.0 = temel boy), `yon` 1 sağa / -1 sola bakar, `faz`/`adim` 0-1 hareket döngüsü.
Figürler `figur(img, fn, x, zemin, ...)` ile çağrılır (kontur + ışık/gölge işler; bkz. SKILL.md).


## ciz — temel çizim, arazi, insan/at/yurt gibi temel figürler ve fizik denetimleri

`from ciz import ...` (dosya: `video/piksel/ciz.py`)

- **`hex2(h, a=255)`** — (açıklama yok; kaynak koda bak)
- **`yeni(w=W, h=H)`** — (açıklama yok; kaynak koda bak)
- **`buyut(img)`** — (açıklama yok; kaynak koda bak)
- **`piksel(img, x, y, renk)`** — Tek piksel; yarı saydam renk alttakiyle karışır (gölge, ışık, duman).
- **`gradyan(img, renkler, y0=0, y1=None)`** — Renk basamakları arasında Bayer titreşimli (dither) dikey geçiş.
- **`gunes(img, cx, cy, r, renkler)`** — Işıyan güneş/ay: dolu çekirdek, dışa doğru titreşimle sönen hale.
- **`bulut(img, cx, cy, boy, renkler, tohum, sar=True)`** — Düz gölgeli piksel bulut: üstte ışık, altta gölge bandı. sar=True: kenardan taşan kısım öbür kenardan girer (yatayda dikişsiz tekrar eden gökyüzü için).
- **`yildizlar(img, adet, ymax, renk, tohum)`** — (açıklama yok; kaynak koda bak)
- **`sirt(taban, genlik, tohum, dalga=2.0, puruz=0.0, w=W, dongulu=False)`** — Bir tepe ya da dağ sırtının her x için y değeri (zemin çizgisi). dongulu=True: tam sayı frekanslarla, sol ve sağ kenarı birbirine dikişsiz uyan sırt.
- **`duzle(zemin, x0, x1, y, yumusak=30)`** — Zemin çizgisinde x0-x1 arasını y'de dümdüz yapar, kenarlarda yumuşakça eski çizgiye bağlar. Yapıların ve figürlerin duracağı düz şeritleri hazırlamak için.
- **`arazi(img, zemin, renkler, kenar=None, doku_tohum=None, y_bit=None, perspektif=False)`** — Zemin çizgisinin altını doldurur: derinleştikçe koyulaşan bantlar, üstte ışıklı kenar. perspektif=True: bantlar izleyiciye yaklaştıkça genişler (yakın çayır).
- **`zemin_y(zemin, x, genislik=0)`** — Nesnenin tabanı: ayak izi boyunca zeminin en alçak noktası (nesne asla havada kalmaz).
- **`duz_zemin(zemin, x0, x1, ad, tolerans=4)`** — Fizik denetimi: yapılar ancak düz zemine kurulur. Ayak izi boyunca zemin toleranstan fazla iniş çıkış yapıyorsa (sarp sırt, tepe yamacı) çizmeyi reddeder; yoksa tabanı verir.
- **`temel(img, zemin, x0, x1, y, renk)`** — Yapının altını zemine bağlayan toprak dolgu: taban ile zemin arasında boşluk kalmaz.
- **`temas_golgesi(img, x, y, genislik, renk='#1a2410', alfa=120)`** — Ayakların bastığı satırda (y-1) koyu, bir üstünde açık titreşimli gölge şeridi.
- **`cimen_tutamlari(img, zemin, renkler, tohum, yogunluk=0.5, boy=4, x0=0, x1=None, ruzgar=0.0)`** — (açıklama yok; kaynak koda bak)
- **`cicekler(img, zemin, renkler, tohum, adet=20, derinlik=30, x0=0, x1=None)`** — (açıklama yok; kaynak koda bak)
- **`cayir_dokusu(img, zemin, renkler, tohum, yogunluk=0.035, isik=None)`** — Çayıra perspektifli çimen dokusu: uzakta (üstte) küçük ve seyrek, yakında (altta) uzun ve belirgin çimen vuruşları; her vuruşun tepesi ışık alır.
- **`patika(img, zemin, x0, x1, derinlik, renk, tohum)`** — Zemin üzerinde hafif çiğnenmiş toprak yol (titreşimli şerit).
- **`yurt(img, x, zemin, s=1.0, keçe='#efe4cc', golge='#c9b996', kapi='#c8552c', isik=False, isik_gucu=1.0)`** — Moğol yurdu (ger): silindir keçe duvar, alçak kubbe çatı, turuncu kapı, tepe halkası. Yalnızca düz zemine kurulur. Dönen değer: baca noktası (duman buradan çıkar).
- **`kapi_isigi(img, x, y, s, guc=1.0)`** — Açık kapıdan yere düşen sıcak ışık (zeminde, kapının önünde).
- **`duman(img, x, y, boy, tohum, faz=0.0, renk='#d9d2c4', ruzgar=0.35, genislik=1.0)`** — Bacadan ya da çatıdan yukarı çıkan duman. Puflar faz ile yukarı süzülür; faz 0→1 bir tam döngüdür ve döngü dikişsiz tekrar eder. Duman hep kaynağından başlar.
- **`sehir(img, x0, x1, zemin, s=1.0, duvar='#a88a6a', golge='#7a6048', toprak=None, cati='#7a4a34', tohum=1)`** — Surlu şehir: mazgallı duvar, kuleler, kapı ve duvarın üstünden görünen damlar. Yalnızca düz ovaya kurulur. Dönen değer: duman çıkabilecek çatı noktaları [(x, y)].
- **`orta_asya_sehri(img, x0, x1, zemin, s=1.0, tohum=1, kerpic='#c8a878', golge='#9a7a58', kubbe='#4a9a9a')`** — Orta Asya / İpek Yolu şehri: kerpiç sur, yuvarlak burçlar (düz, mazgallı tepe), kemerli kapı; surun üstünden kubbeli yapılar ve düz damlı evler görünür. Avrupa şatosu gibi sivri kule yok. Yalnızca düz ovaya kurulur. Dönen değer: duman çıkabilecek dam noktaları [(x, y)].
- **`piksel_ok(img, x0, x1, y, kavis=10, kalinlik=4, renk='#fff3d4', kontur='#3a2414')`** — Sağdan sola giden piksel ok: basamaklı yay gövde ve net '<' ucu, koyu konturlu.
- **`tug(img, x, zemin, s=1.0, faz=0.0, flamalar=('#c8552c', '#3a6aa8', '#e0b040'))`** — Dokuz tuğ geleneğinden esinli beyaz at kılı sancak: direk zemine dikili, dibinde toprak ve taş tümseği. faz 0→1: flamalar ve kıl püskülleri rüzgârda dalgalanır (direk hiç kıpırdamaz).
- **`at(img, x, zemin, s=1.0, yon=1, renk='#6b3f24', yele='#2b1a12', binici=None, eyer=False, faz=0.0, dur=False, bas=0.0, kulak=0.0, kuyruk=0.0, yuk=None, binici_kadin=False, adim=0.55)`** — Moğol atı (kısa bacaklı, gür yeleli). faz: 0-1 adım döngüsü; dur=True ayakta duran at. bas: 0 baş yukarıda, 1 otluyor (ağzı çimende). kulak, kuyruk: -1..1 kıpırdama. yuk: yük atı için heybe rengi. Toynaklar zemine basar; binici varsa eyerde oturur.
- **`insan(img, x, zemin, s=1.0, deel='#3a5a8a', bebek=False, kadin=False, adim=None, yon=1, ruzgar=0.0)`** — Ayakta ya da yürüyen insan. adim: None ayakta, 0-1 yürüyüş döngüsü (bir ayak hep yerde). ruzgar: pelerin ve saçın rüzgârla savrulması.
- **`okuz(img, x, zemin, s=1.0, yon=1, renk='#5a4030', faz=0.0)`** — Kağnı öküzü: iri gövde, kısa bacak, boynuz, başı önde ve alçakta. Toynaklar zemine basar.
- **`kagni(img, x, zemin, s=1.0, yon=1, faz=0.0, yuk='#d8c8a8')`** — İki büyük tekerlekli Moğol kağnısı; üstünde katlanmış yurt keçesi ve direkler. faz 0→1 tekerlekler döner. Tekerlek altları zemine basar.
- **`agac(img, x, zemin, s=1.0, yaprak=('#2f5a2a', '#477a34', '#6a9a44'), govde='#4a3022', tohum=1, sallanma=0.0)`** — Yaşlı ağaç: kalın gövde, zemine yayılan kökler, katmanlı taç. Gövde tabanı zemine oturur.
- **`taslar(img, x, zemin, s=1.0, cicek=False)`** — Ovoo: üst üste konmuş taş yığını; alttaki büyük taşlar zemine oturur.
- **`cicek(img, x, zemin, s=1.0, faz=0.0, renk='#f4d24a', orta='#c8552c')`** — Tek kır çiçeği: kalın sap, dolu yapraklar ve dolu taç yaprakları (taşlarla aynı dolu piksel dili). Sap dibi zemine sabit; üst kısmı rüzgârda salınır.
- **`figur(img, ciz_fn, *args, kontur='#24160e', f_isik=0.18, f_golge=0.22)`** — Figürü ayrı bir katmanda çizer, sonra 64-bit oyun figürü gibi işler: dışına 1 piksel koyu kontur, üst kenarlarına ışık, alt kenarlarına gölge. Sonra sahneye bindirir. Çizim fonksiyonunun döndürdüğü değeri (ör. yurdun baca noktası) geri verir.
- **`sprite_sayfasi(kare_w, kare_h, adet, ciz_kare)`** — Yatay şerit sprite sayfası. ciz_kare(tuval, zemin, i) her kareyi çizer; zemin, karenin en alt satırına basan düz bir çizgidir (ayaklar son satıra değer).
- **`taban_denetimi(sayfa, kare_w, ad, bosluk=0)`** — Fizik denetimi (sprite): her karede en alttaki opak piksel, karenin son satırında olmalı. Değilse figür zeminin üstünde havada durur.

## sahneler — katman üreticileri (gökyüzü, uzak, orta, ön, sprite)

`from sahneler import ...` (dosya: `video/piksel/sahneler.py`)

- **`gokyuzu(no, renkler, gunes_=None, bulutlar=(), bulut_renk=('#fff8ec', '#f4dcc8', '#d8a8a0'), yildiz=0)`** — (açıklama yok; kaynak koda bak)
- **`uzak(no, dag_renk, tepe_renk, ova_renk, dag_y=(346, 420), tepe_y=440, ova_y=480, kenar=None)`** — Uzak plan: dikişsiz dağ sırtı, alçak tepeler ve %50'den aşağısı dümdüz ova.
- **`orta(no, ust=(500, 557), renkler=None, kenar=None, tohum=None, ekle=None)`** — Orta plan (810 geniş): üst kenarı ust aralığında dalgalanan, aşağısı tamamen opak çayır.
- **`on(no, renkler, isik, boy=200)`** — Ön plan (810 geniş): yalnızca sol ve sağ alt köşelerde, dipten yükselen uzun çimen tutamları.
- **`sprite(no, ek, kare_w, kare_h, adet, ciz_kare, denetim=True)`** — (açıklama yok; kaynak koda bak)
- **`duz(y, w=GW)`** — (açıklama yok; kaynak koda bak)

## timur_figur — tarihî kişiler, hayvanlar, yapılar ve araçlar

`from timur_figur import ...` (dosya: `video/piksel/timur_figur.py`)

- **`kisi(img, x, zemin, s=1.0, govde='#3a5a8a', bas='bork', bas_renk='#5a3a22', sakal=None, yon=1, adim=None, aksak=False, silah=None, kol=0.0, diz=False, kadin=False, ten=TEN, uzun=True, kemer='#e0b040', pelerin=None)`** — Genel insan figürü (ciz.insan'ın oranlarıyla). adim: None ayakta, 0-1 yürüyüş; aksak=True sağ bacak sürünür (Timur). silah: kilic, mizrak, kalkan, kurek, testi, mektup, kamera, mesale, yay, kazma, sopa. kol: 0 yanda, 1 yukarı kaldırılmış (silah savurma). diz=True: tek diz üstünde (dizi zemine değer).
- **`timur(img, x, zemin, s=1.0, yon=1, adim=None, silah=None, kol=0.0, yasli=False, diz=False)`** — Timur: koyu kırmızı kaftan, altın kemer, kürklü sorguçlu külah, kızıl sakal; sağ bacağı aksak.
- **`bayezid(img, x, zemin, s=1.0, yon=1, adim=None, silah=None, kol=0.0, diz=False)`** — Yıldırım Bayezid: beyaz büyük kavuk, yeşil kaftan, kara sakal.
- **`oturan(img, x, zemin, s=1.0, govde='#3a5a8a', bas='bork', bas_renk='#5a3a22', sakal=None, yon=1, ten=TEN, el=None, minder=None)`** — Bağdaş kurup oturan kişi: dizler zemine (ya da mindere) değer. el: 'testi', 'kase', 'kalem'.
- **`sedir(img, x, zemin, s=1.0, renk='#7a4a2a', ortu='#8a2a2a')`** — Alçak ahşap sedir (yatak): dört ayağı zemine basar. Üst yüzünün y'sini döndürür.
- **`yatan(img, x, zemin, s=1.0, govde='#7a1e22', bas='sorguc', bas_renk='#2a1a14', sakal='#d8d0c8', yon=1, ortu='#e8e0d0', nefes=0.0)`** — Sedirde uzanan hasta: başı yastıkta, üstünde yorgan; nefes 0-1 göğsü hafifçe kaldırır.
- **`atli(img, x, zemin, s=1.0, yon=1, faz=0.0, at_renk='#6b3f24', yele='#2b1a12', govde='#3a5a8a', bas='bork', bas_renk='#5a3a22', sakal=None, silah=None, kol=0.0, adim=0.55, dur=False, zirh=None, cul=None, bayrak=None)`** — Atlı savaşçı: at (ciz.at) ve eyerdeki binici. zirh: binicinin zırh rengi; cul: atın zırh örtüsü (Sırp şövalyesi); bayrak: mızrak ucundaki flama rengi.
- **`koyun(img, x, zemin, s=1.0, yon=1, faz=0.0, renk='#ece4d4', kos=False)`** — Kıvırcık yünlü koyun: kara baş ve bacaklar; koşarken bacaklar açılıp kapanır.
- **`fil(img, x, zemin, s=1.0, yon=1, faz=0.0, renk='#8a8a90', kule=True, binici='#c8a040', adim=0.35)`** — Savaş fili (Delhi): kalın sütun bacaklar zemine basar, sallanan hortum, fildişi, sırtında kule (hevdec).
- **`deve(img, x, zemin, s=1.0, yon=1, faz=0.0, renk='#b08a5a', yuk='#8a3a2a', adim=0.4)`** — Çift hörgüçlü (Baktriya) devesi: uzun bacaklar, kıvrık boyun, hörgüçler arasında yük.
- **`tank(img, x, zemin, s=1.0, yon=1, faz=0.0, renk='#5a5e58')`** — 1941 tankı: palet tekerlekleri döner, alt palet zemine basar; kule ve namlu.
- **`gemi(img, x, su_y, s=1.0, yon=1, faz=0.0, govde='#5a3a22', yelken='#b8281e', hac=True)`** — Kadırga: gövde su çizgisine oturur (alt kısmı suya batık), dalgayla hafifçe iner kalkar.
- **`mancinik(img, x, zemin, s=1.0, yon=1, faz=0.0, tas_x=None)`** — Karşı ağırlıklı mancınık: ahşap çatı zemine basar, kol faz ile atış yapar (0-0.3 atış, sonra geri).
- **`otag(img, x, zemin, s=1.0, renk='#c8302a', serit='#e0b040', faz=0.0, acik=False)`** — Büyük hükümdar otağı: dikdörtgen ipek çadır, sivri tepe, dalgalanan sancak; tabanı düz zemine kurulur.
- **`koy_evleri(img, x0, x1, zemin, s=1.0, tohum=1, kerpic='#c8a878')`** — Kerpiç köy evleri: düz damlı, küçük kapı ve pencere; damda kuruyan ot. Düz zemine kurulur.
- **`anadolu_kalesi(img, x0, x1, zemin, s=1.0, tas='#9a948a', golge='#6a665e', kapi=True)`** — Taş sur: kesme taş örgü, dikdörtgen mazgallı kuleler, kemerli kapı. Düz zemine kurulur. Dönen değer: sur üstündeki (mazgal) y'si.
- **`kafa_kulesi(img, x, zemin, s=1.0, renk='#e8e0cc')`** — Kafatası kulesi (İsfahan, Bağdat): koni biçimli harç ve kafataslarından kule, tabanı zemine oturur.
- **`gur_i_emir(img, x, zemin, s=1.0, mavi='#2a7ab8', tugla='#c8a878')`** — Gür-i Emir türbesi: yüksek kasnak üstünde dilimli mavi kubbe, kemerli taç kapı (pištak), iki minare. Düz zemine kurulur.
- **`bibi_hanim(img, x, zemin, s=1.0, mavi='#2a8ac8', tugla='#c8a878', iskele=True, catlak=0.0)`** — Bibi Hanım Camii'nin dev taç kapısı ve kubbesi; iskele kurulu. catlak: 0-1 kubbede çatlak.
- **`heykel(img, x, zemin, s=1.0, tunc='#5a6a4a')`** — Taşkent'teki atlı Emir Timur heykeli: granit kaide düz zemine oturur, üstünde tunç atlı.
- **`hendek(img, x0, x1, zemin, derin=14, renk='#2a1a10')`** — Zemine kazılmış çukur: kenarları toprak yığını. Zemin listesini yerinde değiştirmez.

## timur — yardımcılar: hava, iç mekân, ateş, mum, tabut, tabela…

`from timur import ...` (dosya: `video/piksel/timur.py`)

- **`hava(no, tur='yagmur', yogunluk=260, renk='#b8c8e0', egim=0.25, simsek=())`** — Tam kare hava katmanı (24 karelik döngü): yağmur çizgileri ya da savrulan kar taneleri. Her tane bir döngüde tam sayı kez ekranı geçer, döngü dikişsiz.
- **`yatan_at(img, x, zemin, s=1.0, yon=1, renk='#5a3a24', nefes=0.0)`** — Hasta ya da ölü at: yan yatmış gövde zemine değer, boyun ve baş yerde uzanır, dört bacak dizden kırık yana uzanır; nefes 0-1 karnı hafifçe kabartır (hasta at).
- **`ok_ucusu(t, x0, y0, x1, y1, f, renk='#3a2418')`** — Uçan ok: f 0-1 arasında (x0,y0)'dan (x1,y1)'e hafif yayla; yönüne bakar.
- **`kalabalik(img, zemin, x0, x1, aralik, tohum, renkler, s=1.0, yon=1, bas='bork', adim=None)`** — (açıklama yok; kaynak koda bak)
- **`ordugah(img, zemin, x0, x1, tohum, s=1.0, mesale=False)`** — (açıklama yok; kaynak koda bak)
- **`besik(img, x, zemin, s=1.0, sallanma=0.0)`** — Ahşap beşik: kavisli iki kızak zemine değer, sallanırken hep bir noktası yerde kalır; içinde kundaklı bebek.
- **`agac_kavak(img, x, zemin, s=1.0)`** — İnce uzun kavak: dar sütun biçimli taç, gövde zemine oturur.
- **`ates(t, x, z, f, s=1.0)`** — Kamp ateşi: zemine dizili taşlar, odunlar ve titreşen alev; kıvılcımlar yükselir.
- **`parsomen()`** — Mektup sahneleri için parşömen: kıvrık uçlar, lekeler, kırmızı balmumu mühür (430x380 ızgara).
- **`su_ve_kiyi(img, y0, renkler=('#2a5a8a', '#22507a', '#1a456a', '#143a5a'), kiyi_x=None, kum='#c8b080')`** — Orta planda deniz: y0'dan aşağısı titreşimli su bantları ve dalga çizgileri; kiyi_x'e kadar kumsal.
- **`tahtirevan(img, x, zemin, s=1.0, yon=1, faz=0.0)`** — Kafesli tahtırevan: önde ve arkada aynı yöne yürüyen iki at; uzun sırıklar iki atın eyerine oturur, aralarında ahşap parmaklıklı, perdeli bir oda taşınır (demir kafes efsanesinin muhtemel gerçeği).
- **`ic_mekan(no, duvar=('#3a2a22', '#4a3628', '#5a4230'), kemer='#2a1a14', cini='#2a6a9a', pencere=None, zemin_renk=('#5a4a3a', '#4a3c2e', '#3e3226'), isik='#f8c060', hali=False)`** — İç mekân katmanları: gokyuzu = duvar, uzak = dikişsiz kemer dizisi ve çini kuşak (pencere: kemer içinde gece/kar), orta = taş döşeme (düz zemin), on = boş.
- **`kar_ortusu(no, kenar='#f4f8ff')`** — Kar: orta planın üst kenarına kar biriktirir (dosyayı yeniden işler).
- **`tas_arabasi(img, x, zemin, s=1.0, yon=1, faz=0.0)`** — Fil çekişli taş arabası: iki tekerlek zemine basar, üstünde kesme mermer blok.
- **`tabut(img, x, zemin, s=1.0, acik=True)`** — Açılmış mezar sandığı: yere oturur; içi karanlık, iskelet sandığın içinde yatar (sağ bacak dizden eğri: aksaklık, sağ kolda yara izi).
- **`lamba(img, x, zemin, s=1.0, faz=0.0)`** — Ayaklı kazı lambası: üç ayak zemine basar, ampul titrer ve çevresini aydınlatır.
- **`tabela(img, x, zemin, ad)`** — Köy girişinde ahşap tabela: iki direk zemine dikili, üstünde piksel yazılı levha.
- **`yasli_timur_yakin(img, x, zemin, f)`** — Yakın plan: minderde oturan yaşlı Timur, büyük ölçekte. Ağarmış sakal ve bıyık, ağır ve düşük göz kapakları, yavaş göz kırpışı; kürklü külahın altın şeridi alnın üstünde. Minder zemine oturur.
- **`mumluk(t, x, z, f, adet=3)`** — Ayaklı şamdan: tunç ayak zemine basar, mumlar titrer ve çevresine sıcak ışık halkası düşer.
- **`mangal(t, x, z, f)`** — Kömür mangalı: üç ayak zemine basar, korlar kızarır, ince duman yukarı çıkar.
- **`okuz_(img, x, zemin, s=1.0, yon=1, faz=0.0)`** — (açıklama yok; kaynak koda bak)
- **`kandil(t, x, ust, f, zincir=36)`** — Tavandan zincirle sarkan yağ kandili: pirinç gövde, titreyen alev, çevresine yeşil-sarı ışık halkası.
- **`abanoz_tabut(d, x0, x1, omuz)`** — Omuzlarda taşınan abanoz tabut: hacimli gövde, açık renk kapak kenarı, altın şerit ve köşe bağları; üst yüzü perspektifle görünür.
- **`silik_sehir(no, y0=560, alfa=70)`** — Uzak planın ufuk hattına silik bir savaş şehri silüeti işler (uzak katmanı yeniden işlenir): yıkık bloklar, fabrika bacaları, kırık çatılar; düşük alfa ile rüya gibi.

## kayip_mezar — orman, nöbetçi, cenaze arabası, at sürüsü

`from kayip_mezar import ...` (dosya: `video/piksel/kayip_mezar.py`)

- **`cam(img, x, zemin, s=1.0, renk='#1e3a2a', isik='#2e5a3e')`** — Çam: kat kat üçgen dallar, gövdesi zemine oturur.
- **`muhafiz(img, x, zemin, s=1.0, faz=0.0, mizrak=True, mesale=True, deel='#3a2a2a')`** — Ayakta duran nöbetçi: uzun mızrak, elinde titreyen meşale. Ayakları zemine basar.
- **`cenaze_arabasi(img, x, zemin, s=1.0, faz=0.0, yon=-1)`** — Cenaze arabası: büyük tekerlekli kağnının üstünde beyaz keçe örtülü yurt, köşelerde beyaz sancaklar.
- **`hoyuk(img, x, zemin, s=1.0)`** — Taze mezar höyüğü: koyu toprak tümsek, üstünde birkaç taş. Tabanı zemine oturur.
- **`at_suru(img, zemin, i, s, adet, x0, aralik, renkler, tohum)`** — Binicisiz dörtnala koşan atlar: sıra sıra, farklı fazlarda; toynakların arkasından toz kalkar.
- **`_alay(no, gok, gunes_, bulut_renk, ova, orta_renk, kenar, on_renk, on_isik, yildiz=0)`** — (açıklama yok; kaynak koda bak)
- **`_dag_ormani(img, z, yogunluk, tohum, renk='#1e3a2a')`** — (açıklama yok; kaynak koda bak)
