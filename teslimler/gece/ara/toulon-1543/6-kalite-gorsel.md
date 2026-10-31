# Küçük Konstantinopolis: görsel kalite kontrol (toulon-1543)

**Hazırlayan:** 🔴 SKONSTART Kalite Kontrol (görsel) · **Girdi:** 5-grafik.md, 4-kalite-metin.md, `Toulon1543` render kareleri

**Bakılan kareler (20):** verilen 12 kare (`kare-019s` 453, `kare-039s` 455, `kare-059s` 458, `kare-079s` 461, `kare-098s` 463, `kare-118s` 466, `kare-138s` 470, `kare-158s` 473, `kare-177s` 476, `kare-197s` 478, `kare-217s` 481, `kare-237s` 484) ve kritik sahnelerden benim aldığım 8 ek kare: `ek-000s` kapak (kare 60), `ek-052s` 457 Nice (3148), `ek-108s` 464 boşaltma (6509), `ek-127s` 468 kadırgalar limanda (7671), `ek-148s` 472 vaftiz (8910), `ek-171s` 475 altın sandığı (10262), `ek-208s` 480 Lipari (12466), `ek-250s` 486 kapanış (15032). Ek kareler sahne ortasından, geçişlerden uzak alındı. Barbaros 455 ve 475'te görüldü; 451 ve 459 için ayrı kare alınmadı (8 kare sınırı).
`kare-158s` (473) ve `kare-197s` (478) ile `kare-237s` (484) karelerinde kart yarı saydam; bunlar yazı belirme ya da geçiş anı, efekt olarak değerlendirildi, hata sayılmadı.

## Karar: UYGUN DEĞİL (revize_birimi: grafiker)

Beş sahnede, önceki işlerde reddedilen türden hatalar var: gözsüz yüz, insandan küçük ağaç, insan karşısında oyuncak kalan yapılar, kenarda kesilen gemi, kesilen rakam.

## Zorunlu düzeltmeler (kare | yer | sorun | düzeltme)

| # | Sahne / kare | Yer | Sorun | Düzeltme |
|---|---|---|---|---|
| 1 | **458** · `kare-059s.png` | iki atlının başı, orta (y ≈ 770-960) | Miğfer yüzü sakala kadar kapatıyor; iki atlının da **gözü yok** (gözsüz yüz). Sivri, külah biçimli miğfer 1543'teki Savoy ve İmparatorluk ağır süvarisine de uymuyor; Orta Asya miğferi gibi okunuyor. | Yüzü açık bir 16. yy Avrupa miğferi kullan (burgonet ya da morion: siperlikli, tepesi sırtlı). Göz ve sakal görünsün. İki atlı birbirinden ayrılsın (biri tüylü miğfer ya da farklı renk). |
| 2 | **464** · `ek-108s.png` | sağ, kapıda kalan adam ve arkadaki surlar (x ≈ 660-1080, y ≈ 700-1080) | Adamın ayakları surların tabanıyla neredeyse aynı derinlikte, ama adam (~370 px) kuleleri (~310 px) geçiyor. Surlar **oyuncak boyunda** kalıyor. Sur sağ kenarda da kesiliyor. | İki yol var. Birincisi: surları ve kapıyı en az iki insan boyu yüksekliğe büyüt, adamı kapı açıklığının içine ya da önüne koy. İkincisi: surları açıkça uzak plana al (pus, aradaki zemin), adamı da yürüyenlerin önüne ya da yanına, kendi tabanına koy. Surun sağ ucu kadrajın içinde bitsin. |
| 3 | **480** · `ek-208s.png` | sol alt, zeytin ağacı (x ≈ 130-330, y ≈ 1075-1300) | Ağaç ön planda, duvar hizasında (632). Esirler ise bir sıra geride (616). Buna rağmen ağaç (~220 px) esirlerden (~300 px) **kısa**: aynı derinlikte insandan küçük ağaç. | Zeytin ağacını en az 1,5-2 insan boyuna büyüt; taç yazı bandına girerse ağacı kenara yasla ama kesme. Ağaç sığmıyorsa çıkar. `_zeytin` 479 ve 483'te de kullanılıyor; aynı oranı orada da düzelt. |
| 4 | **480** · `ek-208s.png` | sol ve sağ kenardaki evler (y ≈ 990-1120) ve kale | İki katlı evler (~130 px) önlerindeki esirlerin (~300 px) yarısından kısa. Aralarında yalnızca 20 dünya pikseli var, bu yüzden evler **oyuncak boyunda** okunuyor. Sağdaki ev kenarda da kesiliyor. | Esirleri ölçek kuralına göre geri al ve küçült. Ya da evleri ve kaleyi açıkça uzak plana it: aradaki kıyı ya da su şeridi görünsün, uzaklık pus ile verilsin. Kenardaki evler kadrajın içinde bitsin. |
| 5 | **481** · `kare-217s.png` | sağdaki lacivert kronik, "11000" (x ≈ 805-1020, y ≈ 870-925) | İlk "1"in sol bayrağı kitabın orta cildine (gutter) giriyor ve **kesiliyor**. Videonun anahtar rakamlarından biri yarım görünüyor. | Rakamı 2-3 px sağa kaydır ya da sayfa genişliğine göre küçült. Bütün haneler sayfanın içinde, cilt çizgisinden en az 2 px uzakta dursun. |
| 6 | **486** · `ek-250s.png` | sağ, orta plandaki kadırgalar (x ≈ 640-1080, y ≈ 830-955) | İkinci kadırga sağ kenarda **kesiliyor**: yalnızca kıçı ve tek direği görünüyor. Kadırgalar arkadaki evlere göre de küçük kalıyor (gövde ~2 ev genişliği, direk tek katlı ev boyunda): **oyuncak gemi** izlenimi veriyor. | İki kadırga da kadrajın içinde tam görünsün (gerekirse tek kadırga yeter). Kadırgayı kıyıdaki evlere göre büyüt: boy en az 3-4 ev genişliği, direk ev boyunun iki katı. Rıhtımla aradaki su bandını ve adamla temas etmeme kuralını koru. |

## İyileştirme önerileri (reddetme nedeni değil)

- **468** (`ek-127s`): Üç sıra demirli kadırga gövde, direk ve seren olarak birbirine giriyor; "koy dolu" fikri geçiyor ama kalabalık bir karmaşa gibi okunuyor. Sıralar arasına ince su bandı bırakılabilir, ön sıranın direkleri seyreltilebilir. Yakın kadırganın kıçındaki gri duman sütunu nereden çıktığı belli olmadan duruyor.
- **480** (`ek-208s`): Esir sırasının sonundaki mavi giysili, ak börklü levend esirlerle aynı yöne bakıyor ve aynı sırada duruyor; esir mi bekçi mi olduğu anlaşılmıyor. Sıradan biraz ayrılıp yüzünü esirlere dönerse rolü okunur (silah kaldırmadan).
- **457** (`ek-052s`): Yanan evler iki yanda kenara dayanıyor. Ön planın yarısı boş, koyu zemin. Kale ve şehir biraz aşağı alınabilir ya da ön plana duvar ve dikenli çalı gibi bir öğe eklenebilir.
- **478** (`kare-197s`): Okunabilirlik için konan koyu katmanın bandı (y ≈ 660-760) haritanın üst şeridini ayrı bir tona boyuyor. Kuşbakışı masa sahnelerinde bu bant harita kâğıdının üstünde kalmasın.
- **486 / 465**: Direğe asılı sokak feneri 1540'ların Toulon'u için kuşkulu (kamusal sokak aydınlatması 17. yy sonrası). Elde taşınan fener ya da duvar kancasına asılı fener daha güvenli olur.
- **472** (`ek-148s`): Babanın ve rahibin başlığı aynı biçimde (yalnız rengi farklı). Rahibe dönemine uygun biret (dört köşeli kep) verilirse iki karakter daha net ayrılır.
- **476 / 484**: Latin yelkenin arka kenarı (leech) dimdik bir çizgi; hafif kavisli olursa daha doğal görünür.

## Değerlendirme (sahibe gösterilecek)

Video genel olarak SKONSTART imzasını taşıyor. Kapak okunuyor; Türkçe karakterler bütün kartlarda doğru. Işık dili (altın saat, kızıl yangın, mavi gece) hikâyeyi taşıyor. Barbaros, Kral François, Polin ve kraliyet memuru birbirinden net ayrılıyor; Marsilya, Toulon meclisi, vaftiz ve altın sandığı sahneleri temiz. Buna karşılık beş sahnede, daha önce reddettiğimiz türden hatalar var. 458'de atlıların yüzünde göz yok. 480'de zeytin ağacı insandan kısa, evler de oyuncak gibi kalıyor. 464'te surlar kapıdaki adamdan alçak. 486'da kadırgalardan biri kenarda kesiliyor. 481'de "11000" rakamının ilk hanesi kesiliyor. Grafiker bu altı maddeyi düzeltip ilgili kareleri yeniden render ettikten sonra iş tekrar kontrol edilmeli.

## 2. tur

**Bakılan kareler (19):** grafikerin yeniden render ettiği 14 sahne ortası (`r2/sahne458` … `sahne486`: 458, 464, 465, 468, 469, 471, 472, 478, 479, 480, 481, 483, 485, 486) ve sahnelerin başka anlarından benim aldığım 5 ek kare (`r2ek/`): 458 kare 3588, 464 kare 6600, 480 kare 12534, 486 kare 14880 ve 15360. 481'in orta karesi kartın belirme anına denk geliyor; rakamlar net olduğu için ek kare gerekmedi.

### Karar: UYGUN

### Altı zorunlu düzeltme

| # | Sahne | Durum |
|---|---|---|
| 1 | 458 | Yapıldı. İki atlının da gözü ve sakalı açıkta (yakın kesitte 2×2 göz net). Miğfer siperlikli, yüzü açık morion. Atlılar tüy ve miğfer rengiyle ayrılıyor. Kare 3588'de de aynı. |
| 2 | 464 | Yapıldı. Sur uzak planda, kapıdaki adam onunla aynı ölçekte, kuleler adamın iki katından yüksek. Sur iki karede de kadrajın içinde bitiyor (sağ uç x ≈ 1050). Yürüyenlerle adam üst üste binmiyor. |
| 3 | 479, 480, 483 (zeytin) | Yapıldı. Ağaç çıkarıldı, yerine duvar önünde alçak çalılar var; ölçek sorunu kalmadı. |
| 4 | 480 Lipari | Yapıldı. Kale kayası suyun karşı kıyısında; aradaki su şeridi solda ve sağda görünüyor. Evler kayanın dibinde, uzakta okunuyor ve kadrajın içinde bitiyor. Kule yazı bandının altında. |
| 5 | 481 | Yapıldı. "11000" bütün haneleriyle sağ sayfada, cilt çizgisine değmiyor. |
| 6 | 486 | Yapıldı. Tek kadırga, büyütülmüş, iki karede de (14880, 15360) kadrajın içinde tam. Direkler ev boyunun iki katına yakın. Adamla ve rıhtımla arasında su var. |

**Yeni hata:** Görmedim. Gözsüz yüz, havada nesne, kenarda kesilen ana nesne, yazı bandına giren nesne, figürlerin gemiye değmesi yok. 480'deki levend esirlerle aynı zemin çizgisinde; uzun görünmesinin sebebi sivri börkü, gövde boyu esirlerle aynı ve onlara değmiyor. Fener düzeltmeleri (465 el feneri, 469 duvar feneri, 486 el feneri) dönem açısından sorunu çözüyor.

### Kalan zorunlu düzeltmeler

Yok.

### İyileştirme önerileri (reddetme nedeni değil)

- **458:** Miğfer siperliğinin altında ten rengi ince bir şerit, onun altında gri bir bant var (`r2/sahne458`, y ≈ 820-840). Alın miğferin içinden görünüyormuş gibi okunuyor. Şerit kaldırılıp siperlik doğrudan alına oturtulabilir.
- **485:** Minyatürde sağ sütundaki kadırgaların burnu mavi denizi geçip altın çerçeveye 2-4 px taşıyor (`r2/sahne485`, x ≈ 1030-1040). Sütun birkaç piksel sola alınabilir.
- **468:** Sıralar seyreltilmiş ama orta sıranın direkleri hâlâ arka sıranın gövdelerine giriyor. Koyun kalabalığı okunuyor; sorun değil, istenirse orta sıra biraz daha aşağı alınabilir.
- **471 / 472:** Biret basamaklı siyah bir kule gibi duruyor; dört köşe sırtları daha belirgin olursa biret olduğu daha iyi anlaşılır.

### Değerlendirme (sahibe gösterilecek)

İlk turda istenen altı düzeltmenin hepsi yapılmış. Atlıların artık gözü var, Toulon surları ve Lipari kalesi uzakta duruyor ve oyuncak gibi görünmüyor, kenarda kesilen kadırga ve rakam kalmadı. Düzeltmeler yeni bir hata getirmedi. Kalan notlar yalnızca küçük estetik öneriler. Video sahibin onayına sunulabilir.
