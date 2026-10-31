# 🟢 Grafiker: Aynı Gökyüzü, İki Gözlemevi (Takiyüddin'in İstanbul Rasathanesi, 1577-1580)

**İş:** Piksel Tarihim (@pikseltarihim), gece vardiyası 8/10, slug `takiyuddin-rasathanesi`
**Girdi:** 4-kalite-metin.md → "Nihai seslendirme metni" ve "Nihai ekran kartları" (51 kart, harfi harfine)
**Sahneler:** 410-449 (40 sahne, aralığın tamamı) + kapak (sahne 410'un katmanlarıyla)
**Dosyalar:**
- `video/piksel/takiyuddin_rasathanesi.py`: 40 sahne fonksiyonu, `SAHNELER`, `__main__`; 15 yeni figür bu dosyanın içinde
- `video/src/sahneler/Takiyuddin.tsx`: `TAKIYUDDIN_SERI`, `TAKIYUDDIN_KARE`, `Takiyuddin`; etiket "PİKSEL TARİHİM · TAKİYÜDDİN", ses `takiyuddin-rasathanesi-anlatim.mp3`
- Çıktı: `video/public/sahne410…449-{gokyuzu,uzak,orta,on,karakter}.png`
- `Root.tsx`'e dokunulmadı (kayıt kod tarafında).

**Kapak (3 satır, boy 112, ALTIN, 2,0 sn):** "Aynı Gökyüzü," / "İki Gözlemevi" / "Takiyüddin'in üç yılı" (editörün kapak önerisi). Arka plan sahne 410 (yıkım anı), kamera sabit.

**Süre:** Kart süreleri tahmini (harf/14 + 0,4 sn), toplam ≈ 4 dk; `video/ses/hizala_seri.py` sese göre yeniden yazar. Kapak bloğu `    { // KAPAK` ile açılır; diğer bloklar yalnızca `    {` ile açılır, yorumlar üst satırda.

**Renk dili:** KIZIL = tehlike/dönüş/kayıp (kart 1, 2, 7, 13, 26, 29, 30, 31, 33, 36, 38, 39, 41, 48); ALTIN = motif ve cevap (kart 5, 12, 16, 21, 22, 24, 25, 34, 35, 40, 42, 46, 49, 51). Motif "Aynı gökyüzü, iki gözlemevi" (kart 12 ve 49) ALTIN.

**Yön dili:** Sağ = İstanbul, rasathane; sol = Hven, Avrupa (Tycho'nun gemisi 1597'de sola gider; ordu doğuya, sağa yürür).

## Sahne planı

Zemin: dış mekânda sprite tabanı 632, iç mekânda 634 (sprite'ın son satırı; `taban_denetimi` her karede doğrular). Orta plandaki yapılar `duz(588)` düz şeridine ya da onun üstündeki teras platformuna oturur. Sprite 400×300, `x` 270 (aksi yazılmadıkça). Süre tahminidir.

| No | Süre | Konu | Zemin çizgileri | yakin / kamera | Hareket | Kartlar |
|---|---|---|---|---|---|---|
| Kapak | 2,0 | Başlık, sahne 410 arka planı | 410 ile aynı | 2.6 / 0 | 410 ile aynı | Kapak |
| 410 | 8,0 | Ocak 1580, kış alacakaranlığı: topçu (levend) binayı gösterir, tunç top binaya dönük ateşler; sağ geride terastaki rasathane kısmen yıkık | sprite 632; teras duz(588), üstü 578; rasathane teras üstünde | 2.6 / 8, yaziY 250 | Namlu alevi (f<0.12), namlu dumanı ve moloz tozu yukarı çıkar, topçunun kolu | 1, 2 |
| 411 | 6,9 | Tophane'nin yukarısı: alacakaranlıkta sağlam rasathane, pencerelerde kandil; arkada Boğaz | sprite 632; sprite içinde teras (16 px), bina teras üstünde | 2.2 / 10 | Terasın dibinde çimen salınır | 3, 4 |
| 412 | 7,7 | Gece: Takiyüddin halkalı kürenin yanında; sağ geride ışıklı rasathane | sprite 632; orta teras duz(588) | 2.6 / 8 | Armillanın iç halkası döner, Takiyüddin'in eli | 5, 6 |
| 413 | 3,6 | Soru: gece, terastaki ışıklı bina; sol önde ona dönük tek top (topçu yok) | sprite 632; teras 14 px | 2.2 / 10 | Pencere ışığı titrer, çimen | 7 |
| 414 | 8,4 | Hven 1576: Kral II. Frederik belgeyi Tycho'ya uzatır; arkada Uraniborg; çevre deniz | sprite 632; Uraniborg duz(588) | 2.8 / 8 | Kral ve Tycho'nun kolları, çimen | 8, 9 |
| 415 | 2,7 | Uraniborg büyük plan, altın saat | sprite 632 | 2.2 / 10 | Çimen | 10 |
| 416 | 7,7 | Gece: solda Tycho duvar çeyrek dairesinde, sağda Takiyüddin armillada; teleskop yok | sprite 632; çeyrek dairenin taş ayağı ve yay ayağı zeminde | 2.2 / 8, yaziY 220, boy 72 | Nişangâh cetveli, armilla halkası | 11 |
| 417 | 4,0 | Motif: tek yıldızlı gök altında Uraniborg (sol) ve İstanbul Rasathanesi (sağ, terasta), pencereler yanar | sprite 632; teras 10 px | 2.0 / 8 | Çimen | 12, 13 |
| 418 | 4,5 | Şam 1559: Takiyüddin minderde rahlede yazar; sehpada mekanik masa saati; kandil, mum | iç mekân 634 | 3.0 / 6 | Saat akrebi döner, kandil ve mum titrer | 14, 15 |
| 419 | 3,6 | Şam gecesi: Takiyüddin yıldızları gösterir, yanında masa saati; arkada şehrin kubbeleri | sprite 632; şehir duz(588) | 2.6 / 8 | Kol, saat akrebi | 16 |
| 420 | 3,2 | İstanbul 1571: müneccimbaşı Takiyüddin elinde beratla sağa yürür; arkada kurşun kubbeli cami | sprite 632; cami duz(588) | 2.8 / 10, x [255, 285] | Yürüyüş (adim), sprite kayar | 17 |
| 421 | 4,9 | Semerkant (geçmiş): Uluğ Bey elinde cetvel; arkada Gür-i Emir ve silindir gözlemevi | sprite 632; yapılar duz(584/590) | 2.8 / 8 | Kol | 18 |
| 422 | 6,6 | Semerkant gecesi: Uluğ Bey gözlemevi büyük plan, meridyen yuvası | sprite 632 | 2.2 / 8, yaziY 220, boy 72 | Çimen | 19 |
| 423 | 4,9 | Saray: III. Murad sedirde; Takiyüddin diz çöküp kitabını sunar; kitaplar, kandil | iç mekân 634; sedir ayakları zeminde, Murad sedirin üstünde | 2.8 / 6 | Kandil, mum, Takiyüddin'in kolu | 20 |
| 424 | 4,8 | 1577 gündüz: çeyrek daire kurulur; Takiyüddin yön verir, işçi kazma sallar; geride rasathane | sprite 632; orta teras duz(588) | 2.6 / 8 | Kazma inip kalkar | 21 |
| 425 | 4,3 | Kasım 1577 gecesi: rasathanenin üstünde kuyruklu yıldız (insan yok) | sprite 632; alçak ufuk (deniz 584), orta 598 | 2.0 / 8 | Çimen; gök kayar | 22 |
| 426 | 9,8 | Hven gecesi: Tycho çeyrek dairede elini yıldıza kaldırır; alçakta Ay, yukarıda kuyruklu yıldız | sprite 632; alçak ufuk | 2.2 / 8 | Kol, nişangâh | 23, 24 |
| 427 | 4,9 | İstanbul gecesi: Takiyüddin armillanın yanında kuyruklu yıldıza bakar | sprite 632; alçak ufuk | 2.2 / 8, x 250 | Kol, halka | 25 |
| 428 | 4,9 | "Kaynaklar ayrışıyor": vakanüvis rahlede yazar, iki yanında ayrı kitap yığınları; gece penceresi | iç mekân 634 | 3.0 / 6 | Kandil | 26 |
| 429 | 3,6 | Takiyüddin eliyle gökyüzünü gösterir, III. Murad sedirde dinler (anlatıya göre) | iç mekân 634 | 2.8 / 6 | Kol, kandil | 27 |
| 430 | 4,0 | Ağustos 1578, Çıldır: börklü yeniçeriler sağa (doğuya) yürür; geride küçük atlı birlikler | sprite 632 ve arka sıra 620; atlılar duz(584) | 2.6 / 12, x [245, 290] | Yürüyüş, ayak dibinden toz | 28 |
| 431 | 4,4 | Veba: yeşil örtülü tabutun başında iki yaslı; biri tepedeki rasathaneyi gösterir | sprite 632; tabut sehpaları zeminde; orta teras | 2.6 / 8 | Kol | 29 |
| 432 | 3,6 | Şeyhülislam Kadızâde ayakta elini kaldırır; kitaplar, mum | iç mekân 634 | 3.0 / 6 | Kol, mum, kandil | 30 |
| 433 | 5,4 | Ocak 1580: Kaptan-ı Derya Kılıç Ali Paşa taş rıhtımda kılıçla; arkada koyda iki kadırga | sprite 632; rıhtım 600; kadırgalar su 572 | 2.8 / 8, yaziY 270 | Kol | 31 |
| 434 | 4,0 | İnebahtı 1571: kızıl gün batımı, ufukta dumanlar; kadırga sağa kaçar | sprite 300, su çizgisi 284 | 2.4 / 10, x [230, 290] | Kürekler, dalga | 32 |
| 435 | 4,6 | Kılıç Ali kılıcıyla binayı gösterir, top ateşler; rasathane büyük ölçüde yıkık, toz | 410 ile aynı | 2.6 / 8 | Ateş (f 0.5), duman, toz | 33 |
| 436 | 4,2 | Tophane-i Âmire: kurşun kubbeli döküm ocağı, kızıl ocak ağızları, bacalardan duman | sprite 632 | 2.2 / 8 | Duman yukarı çıkar | 34 |
| 437 | 5,8 | Mimar Sinan elinde planla; arkada Kılıç Ali Paşa Camii (tek minare) | sprite 632; cami duz(588) | 2.8 / 8, yaziY 260 | Kol | 35 |
| 438 | 3,2 | Yer bilinmiyor: boş tepe, otlar arasında dağınık kesme taşlar | sprite 632 | 2.4 / 8 | Uzun otlar rüzgârda | 36 |
| 439 | 7,1 | 11 Ekim 1579: Sokollu sedirde, önünde dilekçeli derviş diz çökmüş (ölüm gösterilmez) | iç mekân 634 | 2.8 / 6 | Kandil, mum | 37, 38 |
| 440 | 4,8 | Rasathane yıkılıyor: büyük plan, kubbe düşmüş, kule kırık; molozdan toz | sprite 632; teras 16 px | 2.2 / 8, yaziY 240, boy 80 | Toz yukarı çıkar | 39 |
| 441 | 2,8 | Boş koltuk: divanda boş sedir, dokunulmamış minder | iç mekân 634 | 2.8 / 6 | Kandil, mum | 40 |
| 442 | 4,6 | Yaşlı Takiyüddin gece odasında yalnız; yanında masa saati | iç mekân 634 | 3.2 / 6 | Mum, akrep | 41 |
| 443 | 5,8 | Sonraki müneccimbaşı halkalı kürenin başında gökyüzünü gösterir | sprite 632 | 2.6 / 8 | Halka, kol | 42 |
| 444 | 7,6 | Nakkaşhane: nakkaş Şehinşâhnâme sayfasına rasathane minyatürünü çizer | iç mekân 634; rahle ayakları zeminde | 2.8 / 6 | Kandil | 43, 44 |
| 445 | 5,2 | Açık sayfa yakın plan: minyatürde sarıklı gökbilimciler, yay ve küre | iç mekân 634 | 2.8 / 4 | Mum | 45, 46 |
| 446 | 4,0 | 1597: Tycho'yu götüren gemi sola gider; arkada adada Uraniborg | su çizgisi 284; Uraniborg duz(552) | 2.4 / 10, x [300, 235] | Kürekler, dalga, sprite kayar | 47 |
| 447 | 3,0 | Uraniborg yıkık, otlar sarmış | sprite 632 | 2.2 / 8 | Uzun otlar | 48 |
| 448 | 4,4 | Motif: aynı yıldızlı gök altında iki yıkıntı yan yana | sprite 632 | 2.0 / 6 | Otlar | 49, 50 |
| 449 | 5,0 | Son soru: gece, terasın üstünde moloz; gökte kuyruklu yıldız | sprite 632; alçak ufuk | 2.0 / 6 | Otlar | 51 |
| Kapanış | 3,0 | Logo, @pikseltarihim, "Yorumlara yaz, arkadaşına gönder" | arka 449, gece | — | Yıldızlar | — |

## Yeni figürler (hepsi `takiyuddin_rasathanesi.py` içinde, docstring'lerinde "Yeni figür")

| Figür | Ne | Zemine nasıl basar | Sahneler |
|---|---|---|---|
| `teras` | Yamaç üstündeki düz set: kesme taş istinat duvarı, dümdüz platform (araştırma §1 kararı) | `duz_zemin` (tolerans 3), dönen değer platform y'si; bina onun üstüne kurulur | 410-413, 417, 424, 425, 431, 435, 440, 448, 449 |
| `rasathane` | İstanbul Rasathanesi: iki katlı taş blok, kurşun kubbe, korkuluklu gözlem kulesi; `yikik` 0-1 (kubbe düşer, duvar dişli kırılır, gedikler, moloz) | `duz_zemin`; moloz yığınları da zemine oturur | 410-413, 417, 424, 425, 431, 435, 440, 448, 449 |
| `ceyrek_daire` | Duvar çeyrek dairesi: taş ayak, pirinç yay, derece çizgileri, nişangâh | Taş ayak + kaide zeminde; yayın açık ucu ahşap ayakla yere bağlı | 416, 424, 426 |
| `armilla` | Halkalı küre: üç ayaklı kaide, sütun, sabit ve dönen halkalar | Üç ayak zeminde | 412, 416, 427, 443 |
| `top_` | Tunç top, ahşap kundak, tekerlek; ateş anında namlu alevi | Tekerlek ve kundak kuyruğu zeminde | 410, 413, 435 |
| `kuyruklu_yildiz` | 1577 kuyruklu yıldızı: çekirdek, hale, titreşimle sönen kuyruk | Gökyüzü katmanında (gök cismi) | 425, 426, 427, 449 |
| `uraniborg` | Kırmızı tuğla simetrik köşk, bakır kubbe ve fener, yan kuleler; `yikik` | `duz_zemin` | 414, 415, 417, 446-448 |
| `osmanli_camii` | Kılıç Ali Paşa Camii: gövde, yarım kubbeler, kurşun kubbe, kalem minare | `duz_zemin` | 420, 437 |
| `ulugbey_rasathanesi` | Üç katlı silindir gövde, mavi çini kuşaklar, meridyen yuvası | `duz_zemin` | 421, 422 |
| `dokumhane` | Tophane-i Âmire döküm ocağı: kâgir yapı, kurşun kubbeler, iki baca, kızıl ocak ağızları | `duz_zemin`; duman baca ağzından | 436 |
| `masa_saati` | Mekanik masa saati, ahşap sehpanın üstünde; akrep döner | Sehpa ayakları zeminde | 418, 419, 442 |
| `minyatur_kitap` | Şehinşâhnâme'nin açık sayfası rahlede: altın çerçeveli minyatür + yazı satırları | Rahlenin çapraz ayakları zeminde | 444, 445 |
| `bos_sedir` | Boş makam: sedir, minder, yaslanma yastığı | Sedir ayakları zeminde (`sedir`) | 441 |
| `ortulu_tabut` | Yeşil örtülü tabut, iki alçak sehpa | Sehpa ayakları zeminde | 431 |
| `kesme_taslar` | Otlar arasında dağınık kesme taş blokları | Her blok zemine oturur | 424, 438 |

Kütüphaneden: `kisi`, `oturan`, `atli`, `gemi`, `sedir`, `gur_i_emir`, `orta_asya_sehri`, `kandil`, `mumluk`, `su_ve_kiyi`, `ic_mekan`, `duman`, `gunes` (ay), `cimen_tutamlari`; `kalender.py`'den `rahle`, `kitaplar`. Ölçek ve kadraj yardımcıları (`olcek`, `s_kisi`, `s_oturan`, `s_atli`, `_kz`, `_kadraj`, `_gorunur`) Cem Sultan dosyasından kopyalandı.

**Kişi renkleri (bütün sahnelerde aynı):** Takiyüddin koyu turkuaz kaftan + beyaz sarık + koyu sakal (yaşlıyken ak sakal); Tycho siyah giysi, geniş kenarlı şapka, kahverengi sakal, kızıl pelerin; II. Frederik kırmızı + taç; III. Murad kızıl kaftan + büyük beyaz kavuk; Uluğ Bey mavi + Timurlu külah; Kılıç Ali Paşa koyu kırmızı + lacivert pelerin + kır sakal; Şeyhülislam koyu yeşil + ak sakal; Sokollu yeşil + ak sakal; topçu kırmızı + kalpak.

## Kaynak ve dönem notları (görsel)

- Teleskop hiçbir sahnede yok (kart 11). Aletler: duvar çeyrek dairesi ve halkalı küre; ikisi de çıplak gözle kullanılır.
- Rasathanenin gerçek mimarisi bilinmiyor (araştırma §9-7): sade bir Osmanlı taş yapısı çizildi; ölçü, kat, alet sayısı iddia edilmiyor. Bina araştırmanın önerdiği gibi yamaç üstündeki düz teras üzerinde.
- Top sahneleri (410, 413, 435) tek top ve tek topçu gösterir; gemi ya da top sayısı vurgulanmaz, topların konumu belirtilmez (§9-3). Yıkım sahneleri "anlatıya göre" kartlarıyla eşleşir.
- Veba sahnesinde (431) rakam, tarih, ölü sayısı yok; yalnızca yas ve işaret eden el.
- Sokollu sahnesinde (439) ölüm anı gösterilmez: dilekçeli derviş ve divan; ardından boş sedir (441).
- Hilal ya da tarih dışı sancak yok; 430'da sancak/mızrak kullanılmadı (yazı bandına dikey nesne girmesin diye de).

## Grafiker öz denetimi

**a) Çizim:** `python3 -I video/piksel/takiyuddin_rasathanesi.py` 40 sahnenin hepsini hatasız çizdi (`taban_denetimi`, `duz_zemin`, `_kadraj`, `_gorunur`, `_gemi_denetimi` geçti).

**b) Bakış yöntemi:** Sprite PNG'lerini tek tek açmanın yanında, Remotion'daki `PikselSahne` düzenini (paralaks, `yakin` ile odak çevresinde büyütme, sahne boyunca %6 yaklaşma, üst koyulaştırma, yazı bloğu ve etiket) Python'da birebir taklit eden bir önizleme betiğiyle her sahnenin başlangıç ve bitiş karesini 1080×1920 düzeninde Jersey 10 yazısıyla birleştirip baktım (40 sahne, iki tur). Betik ayrıca her kartın yazı alt kenarını sprite'ın opak üst sınırıyla karşılaştırdı. Ayrıca 410, 426, 435, 439, 440, 446 sprite şeritlerinden olay karelerini (top alevi, toz, nişangâh, mum) açıp baktım.

**Baktığım şeyler:** zemin (her figür, sehpa, tabut, rahle, top tekerleği ve yapının tabanı zemin satırında; havada nesne yok, gök cisimleri yalnızca gökyüzü katmanında), ölçek (ana figürler kadrajın %30-32'si; arka plandaki yapı ve atlılar hem küçük hem yüksek zeminde), kesilme (görünür aralık w/2 ± 270/yakin, %6 yaklaşmayla daralan son kare dahil), yazı bandı çakışması (baş, sarık, minare, direk, yelken, ay ve kuyruklu yıldız), koyu sahnelerde kontur ve okunurluk.

**Bulup düzelttiklerim:**
1. 410: topçunun elindeki meşale (fitil) kapak yazısının bandına giriyordu → meşale kaldırıldı, topçu eliyle binayı gösteriyor; topçu sol kenarda kesiliyordu → içeri alındı, top küçültüldü (insan/top oranı).
2. 410/412/431: arka plandaki rasathane görünür aralığın dışına taşıyordu (`_gorunur` hatası) → x kaydırıldı.
3. 430: atlının mızrağı ve sancağı yazı bandına giriyordu (önizleme uyarısı, ekran y 413 < yazı alt 609) → sancak ve mızrak kaldırıldı; büyük at yerine önde yürüyen yeniçeriler, geride küçük atlı birlikler (insan/at oranı korunarak).
4. 433: orta plandaki kadırgaların yelkenleri yazı bandının arkasına çıkıyordu → kadırgalar küçültüldü (s 1.25/1.1), yazı yaziY 270'e alındı.
5. 434: kadırga yelkeni yazı bandına giriyordu → s 3.6 → 2.6.
6. 444/445: minyatürlü kitap hem kenardan kesiliyor hem yazıya değiyordu → küçültüldü (3.2 / 4.8) ve ortalandı.
7. 413, 416, 417/448, 418, 421, 424, 427, 428, 431, 432, 449: kenarda kesilen top, Tycho, çeyrek daire yayı, armilla, Uraniborg, masa saati, Uluğ Bey, işçi, kitap yığınları, mum ve kuyruklu yıldız → konumlar ya da yakin (416: 2.4 → 2.2) düzeltildi.
8. 423/429: III. Murad'ın kızıl sakalı kızıl kaftanla birleşip yüzü okunmuyordu → sakal koyulaştırıldı. 426: Tycho'nun turuncu sakalı gaga gibi görünüyordu → kahverengi.
9. 438 ve 424: kütüphanedeki `taslar` Moğol ovoo'su (dinî taş yığını) gibi okunuyordu, dönem dışı → yerine yeni `kesme_taslar` (dağınık kesme taş blokları).
10. 418: rahle oturan figüre göre çok küçüktü → büyütüldü.
11. Uzun kartlar (11, 19: 5 satır; 39: 4 satır) figür başlarına iniyordu → bu sahnelerde yaziY 220-240 ve boy 72-80.

**Kalan, bilerek bırakılanlar:** İç mekânlarda kandil zinciri tavandan (sprite'ın üst kenarından) iner ve yazının arkasından geçer; Cem Sultan'da onaylanan kalıp budur (önizleme betiği bunları "uyarı" diye saydı, figür değildir). Gece sahnelerinde zemin koyu ve geniştir; figürler ve yapılar açık renkli olduğundan kontur ve siluet okunuyor.

**c) TypeScript:** `cd video && npx tsc --noEmit -p .` temiz.

**d) Kart denetimi:** TSX'teki 51 kart, 4-kalite-metin.md'deki nihai kart listesinden betikle üretildi (harfi harfine, aynı sırada, kart numarası satır sonu yorumunda); en uzun satır 30 harf.

**Kod tarafına not:** `Root.tsx` kaydı (`Takiyuddin`, `TAKIYUDDIN_KARE`, 1080×1920, 60 fps) ve ses geldiğinde `python3 -I video/ses/hizala_seri.py <ses.mp3> video/src/sahneler/Takiyuddin.tsx takiyuddin-rasathanesi-anlatim` kalite kontrolün görsel kapısından önce yapılmalı. Görsel kontrol için önerilen kareler: 410 (kapak + yıkım), 416 (iki alet), 417 (motif), 425-427 (kuyruklu yıldız), 435, 440, 445, 448, 449.

## Görsel KK revizyonu

6-kalite-gorsel.md'deki 3 zorunlu düzeltme ve ucuz iyileştirmeler yapıldı. Takiyuddin.tsx'teki `sure` değerlerine ve kart metinlerine dokunulmadı; yalnızca iki sahne ayarı değişti (446 sprite x, 448 yakin).

**Zorunlu düzeltmeler**
1. **446 (Uraniborg suyun üstünde):** Orta plana Hven adası çizildi (yeni yardımcı `_hven_adasi`): Uraniborg'un iki yanında 20'şer px taşan düz çimen şeridi, suya inen kumsal, köpük çizgisi. Uraniborg bu çimen şeridine oturuyor. Yeni fizik denetimi `_kara_denetimi`, yapının taban satırının hemen altında su rengi bulursa çizimi durduruyor. Öneri 6 için gemi yolu `x: [300, 235]` → `[256, 220]` yapıldı, Uraniborg ızgara x 298'e alındı. Yelken artık sahnenin başında binayı yalnızca kenarından örtüyor, sonra ondan uzaklaşıyor. `_gorunur` %6 yaklaşmalı son kareyle (yakin·1,06) çalıştırıldı.
2. **448 (moloz terastan taşıyor):** `rasathane()` fonksiyonuna `sinir=(x0, x1)` eklendi. Moloz yığınları teras platformunun içine sıkıştırılıyor, kenardan boşluğa taşamıyor. 448 kendi düzeniyle çiziliyor: teras 206-306, rasathane 254, Uraniborg 142, ölçek 1.9. Öneri 5 için yakin 2.0'dan 2.2'ye çıkarıldı; iki yıkıntı son karede de görünür aralıkta (84-316) kalıyor. 417'de moloz yok, değişmedi.
3. **439 (şamdan kenarda kesik):** Şamdan ızgarada 112'den 134'e alındı. Sokollu'nun sediri 262'den 248'e kaydı (öneri 1).

**İyileştirmeler**
- 423 ve 429: III. Murad'ın sediri 248'e alındı, sağ ucu artık kadrajda. 423'te sağ kenarda kesilen şamdan kaldırıldı; kandil yerinde duruyor.
- 426: Ay (196, 552, r 6) içeri alındı, halesi kesilmiyor.
- 416: armilla 280'den 270'e, Takiyüddin 228'den 222'ye alındı; kenarla arasında pay var.
- 433: rıhtıma şaşırtmalı derzli kesme taş dokusu eklendi. Kadırgalardaki kürekler `gemi()` fonksiyonunda zaten çiziliyor, ama 1,1-1,25 ölçekte birer piksel kalıyor. Gemiler büyütülürse yelkenler yazı bandına giriyor (ilk denetimdeki ret nedeni), bu yüzden ölçek korundu.

**Kontrol:** `python3 -I video/piksel/takiyuddin_rasathanesi.py 439 446 448` ve iyileştirilen sahneler (416, 423, 426, 429, 433) hatasız çizildi. 446, 448, 439 ve 423'ün sprite karelerine, ayrıca 446, 448, 439, 423, 426, 416 ve 433'ün yazılı ilk ve son karelerine önizleme betiğiyle bakıldı. Su üstünde yapı, taşan moloz, kesik şamdan ya da sedir kalmadı; yazı-figür çakışması yok. `npx tsc --noEmit -p .` temiz.
