# 🔴 Kalite Kontrol (görsel kapı): Aynı Gökyüzü, İki Gözlemevi (Takiyüddin'in İstanbul Rasathanesi, 1577-1580)

**İş:** Piksel Tarihim (@pikseltarihim), gece vardiyası 8/10, slug `takiyuddin-rasathanesi`
**Girdi:** 5-grafik.md (sahne planı), 4-kalite-metin.md (51 kart), 12 render karesi (`kare-018s` … `kare-219s`) + kontak sayfası
**Ek kareler (kendim render ettim, 6 adet):** `ek-001s` (kapak), `ek-157s` (435), `ek-186s` (440), `ek-222s` (446), `ek-228s` (448), `ek-235s` (449)
**Kontrol eden:** SKONSTART Kalite Kontrol · 31 Ekim 2026

Not: `kare-018s` sahne 411 ile 412 arasındaki çapraz geçişe denk geliyor; üst üste binen yarı saydam görüntü geçiş efekti, hata sayılmadı. `kare-054s` sahne 416'nın son anı; kart 11'in soluk rengi çıkış geçişinin solmasıdır.

## Karar: UYGUN DEĞİL (revize_birimi: grafiker)

Bir yapı suyun üstünde duruyor (446), bir moloz yığını teras kenarından boşluğa taşıyor (448). Bu iki hata kesin ret nedeni. Ayrıca kenarda yarısı kesilmiş bir şamdan var (439).

## Zorunlu düzeltmeler (kare | yer | sorun | düzeltme)

| # | Kare | Yer | Sorun | Düzeltme |
|---|---|---|---|---|
| 1 | `kare-219s`, `ek-222s` (sahne 446, kart 47) | Orta plan, sağ: Uraniborg (ekran x≈680-910, taban y≈900) | Uraniborg denizin üstünde duruyor. Altında kara yok: tabanı doğrudan su yüzeyine oturuyor. Yeşil ada şeridi çok daha geride ve yukarıda (y≈690-780), binayla bağlantısı yok. Bina suda yüzüyormuş gibi görünüyor. | `takiyuddin_rasathanesi.py` sahne 446: Uraniborg'un taban satırına (`duz(552)`) binadan her iki yana en az 30-40 ızgara px geniş bir ada zemini çiz: düz çimen/kumsal şeridi, suya inen kıyı çizgisi, köpük. Ya da Uraniborg'u geri plandaki adanın düz kısmına taşıyıp küçült. `_gemi_denetimi`/`duz_zemin` denetimine "taban satırının altında su değil kara var" kontrolü ekle. Bu sahnenin ilk ve son karesini tekrar render edip bak. |
| 2 | `ek-228s` (sahne 448, kart 49-50) | Sağdaki İstanbul Rasathanesi yıkıntısı (ekran x≈578-1080, y≈1165-1290) | `rasathane(yikik)` molozu terastan geniş. Sol uçtaki moloz eğimi (x≈578-625, y≈1245) terasın sol kenarından dışarı taşıyor ve altı boş: teras yüksekliği (~35 ekran px) kadar havada. Sağ uçta da moloz terasın sağ kenarını aşıyor ve kadrajın sağ kenarında kesiliyor (x≈1080). Sahne boyunca %6 yaklaşma olduğu için sondaki kesik daha da büyüyor. | Terası moloz genişliğinden geniş çiz (449'da doğru: teras x≈330-980, moloz terasın içinde). Ya da `rasathane` fonksiyonunda moloz yığınını teras genişliğiyle sınırla. Yapıyı sola kaydır ki sağ uç son karede de görünür aralıkta kalsın (`_gorunur`'u son kare için çalıştır). |
| 3 | `kare-183s` (sahne 439, kart 37-38) | Sol kenar, alt: şamdan (mumluk), x≈0-80, y≈1110-1310 | Şamdan kadrajın sol kenarında ikiye kesilmiş: kaidesinin ve sol mumlarının yarısı kadraj dışında. Grafikerin 432'de düzelttiği "kenarda kesilen mum" hatası burada tekrar ediyor. | Mumluğu ızgarada 25-30 px sağa al (derviş ile arasında boşluk var) ya da kaldır. %6 yaklaşmalı son karede `_gorunur` ile doğrula. |

## İyileştirme önerileri (ret nedeni değil)

1. **Sedir kenardan taşıyor** (`kare-091s` 423, `kare-128s` 429, `kare-183s` 439): Sağdaki sedirin sağ ucu kadraj dışında. Oturan figür tam göründüğü için divan ekran dışına uzanıyor gibi okunuyor, kabul edilebilir. Sedir 20-30 px sola alınırsa daha derli toplu olur.
2. **Ay'ın halesi kesik** (`kare-109s`, 426, sol kenar x≈0-130, y≈860-1010): Ay diski görünüyor, halesinin sol yarısı kesik. Ay 15-20 px içeri alınabilir.
3. **Armilla kenara değiyor** (`kare-054s`, 416 son anı): Sağdaki halkalı kürenin dış halkası x≈1075'te, sağ kenara 5 px kalıyor. Kesilmiyor, ama 10-15 px sola alınırsa nefes payı olur.
4. **Kadırgalar** (`kare-146s`, 433): Arkadaki iki gemide kürek yok, kadırgadan çok tek yelkenli tekneye benziyor. Bir sıra kürek eklenirse "donanma" daha iyi okunur. Ön plandaki taş rıhtım kadrajın alt %40'ında dümdüz gri; derz/taş dokusu eklenebilir.
5. **448 motif karesi** (`ek-228s`): İki yıkıntı kadraj yüksekliğinin yalnızca ~%7'si, üst %60 boş gök. Motif kartı ("İkisi de yok") için `yakin` 2.0 → 2.4 yapılırsa yıkıntılar daha güçlü okunur. Önce 2 numaralı düzeltme yapılmalı.
6. **446 kurgusu** (`kare-219s`): Sahnenin ilk yarısında yelken Uraniborg'u neredeyse tamamen kapatıyor. 1 numaralı düzeltme yapılırken Uraniborg biraz daha sağa alınırsa "adadan ayrılış" baştan anlaşılır.
7. **â harfi:** "â" geçen kartlar (26 hikâye, 30 Kadızâde, 44 Şehinşâhnâme, 46 kâğıtta) bu karelerin hiçbirine denk gelmedi; yazı tipi alt kümesi (Jersey 10 latin, U+0000-00FF) bu harfi kapsıyor. Revizyondan sonraki kontrolde 428 ve 444'ten birer kare alınsın.

## Kontrol edilip sorunsuz bulunanlar

- **Kapak** (`ek-001s`): "Aynı Gökyüzü, / İki Gözlemevi / Takiyüddin'in üç yılı" net okunuyor. Üstteki etiketle ve figürlerle çakışmıyor. Topçu, top (tekerlek ve kundak kuyruğu zeminde) ve terastaki yıkık rasathane zemine oturuyor; namlu dumanı yukarı çıkıyor.
- **Fizik:** 410, 414, 416, 420, 423, 426, 429, 433, 435, 436, 439, 440, 443, 449'da bütün figürler, sehpa ve sedir ayakları, armilla ve çeyrek daire ayakları, top, döküm ocağı ve teraslı yapılar zemine oturuyor. Duman ve toz yukarı çıkıyor (435, 436, 440). 440 ve 449'da moloz terasın içinde kalıyor.
- **Kadraj ve yazı:** Ana figürler kadraj yüksekliğinin ~%30-32'si. 4-5 satırlık kartlar (8, 11, 23, 31, 39, 42, 51) dahil hiçbir kart sarık, kavuk, minare, yelken, kılıç ya da kuyruklu yıldızla çakışmıyor. Yazılar kesilmiyor. Türkçe harfler (İ, ı, ş, ğ, ü, ö, ç) doğru. Kartlar sahnelerin anına uyuyor: Tycho + kuyruklu yıldız (23), Kılıç Ali rıhtımda (31), Tophane döküm ocağı (34), Sokollu ve dilekçeli derviş (38), yıkılan rasathane (39), Tycho'nun gemisi (47).
- **Tarz:** 64-bit piksel, 1 px koyu kontur, dither'lı gökyüzü, paralaks katmanları her sahnede aynı. Kişi renkleri tutarlı (Takiyüddin turkuaz, Tycho siyah + kızıl pelerin, Murad kızıl, Kılıç Ali koyu kırmızı + lacivert, Sokollu yeşil). Gece sahnelerinde (416, 426, 443, 448, 449) figürler ve aletler siyaha gömülmüyor. Hiçbir sahnede teleskop yok.

## Değerlendirme (sahibe gösterilecek)

Video tarz, renk ve yazı bakımından onaylı işlerle aynı çizgide. Kapak net, 51 kartın hiçbiri figürlerle çakışmıyor, Türkçe harfler doğru. Gece sahneleri okunaklı. Ama iki karede fizik kuralı bozuluyor: Tycho'nun adadan ayrıldığı sahnede Uraniborg denizin üstünde duruyor, kapanıştaki "iki yıkıntı" karesinde de moloz terasın kenarından boşluğa taşıyor. Ayrıca Sokollu sahnesinde bir şamdan kenarda yarısından kesilmiş. Üçü de grafikere küçük, yerel düzeltmeler olarak geri gönderildi. Düzeltilmiş kareler tekrar kontrol edilmeden video size gelmeyecek.
