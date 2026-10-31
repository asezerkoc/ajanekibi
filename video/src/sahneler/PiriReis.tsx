import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Haritayı Çizen Adam: Piri Reis'in haritaları ve idamı (1513-1554). Grafikerin tarifi:
   teslimler/gece/ara/piri-reis/5-grafik.md; sahneler 330-367 (video/piksel/piri_reis.py).
   Kartlar kalite kontrolün nihai 54 kartıyla harfi harfine aynı; süreler tahmini (seslendirme 263 sn),
   ses/hizala_seri.py sese göre yeniden yazar. */
// Kapak: sahne 330 katmanlarıyla yapılan ilk Bolum (2 sn, sessiz); logo ve @pikseltarihim alt bandını kapak bileşeni ekler.
export const PIRI_REIS_SERI: Seri = {
  etiket: "PİKSEL TARİHİM · PİRİ REİS",
  ses: "piri-reis-anlatim.mp3",
  bolumler: [
    { // KAPAK
      no: 330, yakin: 2.8, kamera: 0, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Haritayı", "Çizen Adam", "Piri Reis'in sonu"], sure: 2.0, boy: 112, renk: ALTIN },
      ],
    },
    // Kahire, alacakaranlık: yaşlı denizci avluda, karşısında fermanı tutan çavuş
    {
      no: 330, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Seksenini geçmiş bir denizci.", "Kahire'de, kendi devletinin", "fermanıyla boynu vurulacak."], sure: 6.48, renk: KIZIL }, // kart 1
      ],
    },
    // bugün, Topkapı: vitrinde parşömen harita, iki ziyaretçi
    {
      no: 331, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kırk yıl önce bu adam", "bir harita çizdi. Amerika'yı", "gösteren ilk Osmanlı haritası."], sure: 6.17 }, // kart 2
        { satirlar: ["Harita bugün Topkapı'da.", "Peki haritayı çizen adamı", "devleti neden öldürttü?"], sure: 5.64, renk: ALTIN }, // kart 3
      ],
    },
    // korsan kadırgasının güvertesi: genç Piri ve Kemal Reis; uzakta İspanya kıyısı
    {
      no: 332, yakin: 2.6, kamera: 10,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Adı Piri. Gelibolulu.", "Gençliğinde amcası", "Kemal Reis'in yanında korsan,"], sure: 5.33 }, // kart 4
      ],
    },
    // fırtına: kadırgalar dalgalarda, şimşek
    {
      no: 333, yakin: 2.4, kamera: 14, hava: 30, sarsinti: 2,
      sprite: { w: 400, h: 300, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["İspanya kıyılarında.", "Amcası fırtınada", "gemisiyle batıyor."], sure: 4.27, renk: KIZIL }, // kart 5
      ],
    },
    // Gelibolu kıyısı, akşam: Piri kasabaya yürür
    {
      no: 334, yakin: 2.8, kamera: 10,
      sprite: { w: 400, h: 220, fps: 16, x: [250, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Piri Gelibolu'ya çekiliyor", "ve kalemi eline alıyor."], sure: 3.81 }, // kart 6
      ],
    },
    // Gelibolu, 1513: Piri masada ceylan derisi parşömene çizer
    {
      no: 335, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Gelibolu, 1513 baharı.", "Önünde ceylan derisi", "bir parşömen."], sure: 4.34 }, // kart 7
        { satirlar: ["İmzası: Kemal Reis'in", "yeğeni Piri. Ölen amcasının", "adı haritada."], sure: 4.80, renk: ALTIN }, // kart 8
      ],
    },
    // kuşbakışı masa: kalem kenara yazar; eski haritalar ve Arap haritası
    {
      no: 336, yakin: 2.2, kamera: 0, odakY: 560,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kenara kaynaklarını yazıyor:", "yirmi kadar harita."], sure: 3.66 }, // kart 9
        { satirlar: ["İskender zamanına dayandırdığı", "eski haritalar,", "bir Arap haritası,"], sure: 4.95 }, // kart 10
      ],
    },
    // kuşbakışı masa: dört Portekiz haritası ve Kolomb'un haritası da masada
    {
      no: 337, yakin: 2.2, kamera: 0, odakY: 560,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["dört Portekiz haritası.", "Bir de Kolomb'un haritası.", "Amcasının İspanyol esiri,"], sure: 5.79 }, // kart 11
      ],
    },
    // gece odası: İspanyol esir anlatır, Piri yazar
    {
      no: 338, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kolomb'la üç kez o topraklara", "gitmiş. Anlattıklarını Piri", "not ediyor."], sure: 5.26 }, // kart 12
      ],
    },
    // Mısır, 1517: otağ önünde tahtta Yavuz, diz çökmüş Piri haritayı sunar
    {
      no: 339, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Mısır, 1517. Yavuz Memlükleri", "yeni yenmiş. Piri haritayı", "padişaha sunuyor."], sure: 5.64 }, // kart 13
      ],
    },
    // hazine odası: sandıkta dürülmüş harita, raflar, toz
    {
      no: 340, yakin: 3.0, kamera: 4,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Harita saraya giriyor.", "Dört yüz yılı aşkın", "unutulacak."], sure: 4.11, renk: ALTIN }, // kart 14
      ],
    },
    // 1524, güverte: Pargalı İbrahim Paşa ve el yazması kılavuzuyla Piri
    {
      no: 341, yakin: 2.6, kamera: 10,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["1524. Kaptan Piri, Mısır", "yolunda Pargalı İbrahim", "Paşa'ya kılavuzluk ediyor."], sure: 5.71 }, // kart 15
        { satirlar: ["Paşa görüyor: kaptan yolu", "kendi el yazması", "kılavuzundan buluyor."], sure: 4.88 }, // kart 16
        { satirlar: ["Ondan kılavuzu temize çekip", "padişaha sunmasını istiyor."], sure: 4.19 }, // kart 17
      ],
    },
    // 1526: tahtta Kanuni, rahlede Kitab-ı Bahriye, Piri ayakta
    {
      no: 342, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["1526. Kitab-ı Bahriye,", "iki yüzü aşkın haritayla", "Kanuni'nin önünde."], sure: 5.03, renk: ALTIN }, // kart 18
      ],
    },
    // Süveyş, 1547: rıhtımda yaşlı Piri beratı alır; demirli kadırgalar
    {
      no: 343, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["1547, Süveyş. Piri yetmişini", "çoktan geçmiş. Devlet ona", "Hint kaptanlığını veriyor."], sure: 6.17 }, // kart 19
      ],
    },
    // Aden: krater dağlarının önünde surlu şehir, önde kadırgalar
    {
      no: 344, yakin: 2.4, kamera: 10,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Görev: Portekizlilerle savaş.", "Aden'i geri alıyor."], sure: 3.73 }, // kart 20
      ],
    },
    // 1552: donanma sağa, Maskat kalesine yol alır
    {
      no: 345, yakin: 2.4, kamera: 12,
      sprite: { w: 400, h: 300, fps: 12, x: [240, 300], taban: 632 },
      yazilar: [
        { satirlar: ["1552. Süveyş'ten yaklaşık otuz", "gemiyle çıkıyor. Maskat kalesi", "on sekiz günde düşüyor."], sure: 6.48 }, // kart 21
      ],
    },
    // Hürmüz surları; ufukta Portekiz yelkenleri
    {
      no: 346, yakin: 2.4, kamera: 10,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sonra Hürmüz. Surlar", "dayanıyor. Goa'dan Portekiz", "donanması geliyor haberi."], sure: 5.64, renk: KIZIL }, // kart 22
      ],
    },
    // alacakaranlık: filo sola, hurmalı Basra kıyısına çekilir
    {
      no: 347, yakin: 2.4, kamera: 12,
      sprite: { w: 400, h: 300, fps: 12, x: [300, 240], taban: 632 },
      yazilar: [
        { satirlar: ["Piri kuşatmayı kaldırıyor,", "filoyu Basra'ya çekiyor."], sure: 3.89 }, // kart 23
      ],
    },
    // Basra sarayı: Kubad Paşa minderde şikâyet yazar, Piri ayakta
    {
      no: 348, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Basra'da beylerbeyi", "Kubad Paşa. Kürekçi vermiyor.", "İstanbul'a şikâyet yazıyor."], sure: 5.87, renk: KIZIL }, // kart 24
      ],
    },
    // Basra limanı, akşam: demirli donanma; rıhtımda yaşlı kaptan
    {
      no: 349, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Yaşlı kaptan bir karar", "veriyor. Donanmayı", "Basra'da bırakıyor."], sure: 4.65 }, // kart 25
      ],
    },
    // ganimet yüklü üç kadırga sola döner; donanma geride kalır
    {
      no: 350, yakin: 2.4, kamera: 12,
      sprite: { w: 400, h: 300, fps: 12, x: [300, 240], taban: 632 },
      yazilar: [
        { satirlar: ["Ganimet yüklü üç gemiyle", "Mısır'a dönüyor.", "Gemiler Basra'da kalıyor."], sure: 5.10, renk: ALTIN }, // kart 26
      ],
    },
    // Kahire, divan odası: çavuş fermanı okur, Piri ayakta dinler
    {
      no: 351, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kahire. Yıllar önce bu ülkede", "haritayı padişaha sunmuştu."], sure: 4.34 }, // kart 27
        { satirlar: ["Şimdi Kanuni'nin fermanı", "geliyor. Suçlama:", "görev ihmali."], sure: 4.27, renk: KIZIL }, // kart 28
      ],
    },
    // aynı avlu, gece: boş
    {
      no: 352, yakin: 2.8, kamera: 4,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Haritayı çizen adamın", "boynu vuruluyor."], sure: 2.90, renk: KIZIL }, // kart 29
      ],
    },
    // arşiv: raflar, masada iki defter, tek mum
    {
      no: 353, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Yıl için kaynaklar ayrışıyor:", "1553 sonu ya da 1554."], sure: 3.89 }, // kart 30
        { satirlar: ["Gerçek neden hâlâ", "tartışılıyor. İhmal mi,", "saray çekişmesi mi?"], sure: 4.65, renk: ALTIN }, // kart 31
      ],
    },
    // Basra rıhtımı, Şubat 1554: Seydi Ali Reis donanmayı devralır
    {
      no: 354, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Peki Basra'da kalan gemiler?", "Şubat 1554. Seydi Ali Reis", "on beş kadırgayı devralıyor."], sure: 6.40 }, // kart 32
      ],
    },
    // Umman Denizi: kadırgalar ve Portekiz gemileri, top dumanı
    {
      no: 355, yakin: 2.4, kamera: 14, sarsinti: 2,
      sprite: { w: 400, h: 300, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ağustosta Umman Denizi'nde", "Portekizlilerle çarpışıyor."], sure: 4.11 }, // kart 33
      ],
    },
    // fırtına donanmayı sağa, Hindistan'a sürükler
    {
      no: 356, yakin: 2.4, kamera: 14, hava: 30, sarsinti: 2,
      sprite: { w: 400, h: 300, fps: 12, x: [240, 300], taban: 632 },
      yazilar: [
        { satirlar: ["Fırtına donanmayı", "Hindistan'a sürüklüyor.", "Gemiler elden çıkıyor."], sure: 4.88, renk: KIZIL }, // kart 34
      ],
    },
    // kara yolu: Seydi Ali atlı, yanında yaya yoldaş ve deve; sola, eve
    {
      no: 357, yakin: 2.8, kamera: 12,
      sprite: { w: 400, h: 220, fps: 16, x: [300, 250], taban: 632 },
      yazilar: [
        { satirlar: ["Seydi Ali Osmanlı topraklarına", "karadan dönüyor. Basra'dan", "çıkalı üç yıl yedi ay olmuş."], sure: 6.55 }, // kart 35
      ],
    },
    // Seydi Ali minderde kitabını yazar
    {
      no: 358, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Hepsini bir kitaba yazıyor.", "Piri'nin bıraktığı donanma", "eve dönmüyor."], sure: 5.18, renk: ALTIN }, // kart 36
      ],
    },
    // Topkapı, 1929: Babüsselam kapısı; iki kişi içeri yürür
    {
      no: 359, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 14, x: [250, 280], taban: 632 },
      yazilar: [
        { satirlar: ["Topkapı Sarayı, 1929.", "Saray beş yıldır müze."], sure: 3.35 }, // kart 37
      ],
    },
    // 1929, saray deposu: kâğıt desteleri; Halil Edhem ve parşömene eğilen Deissmann
    {
      no: 360, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Müzeler müdürü Halil Edhem", "bir deste içinde ceylan", "derisi bir parşömen buluyor."], sure: 6.02 }, // kart 38
        { satirlar: ["Alman ilahiyatçı Deissmann", "inceliyor."], sure: 2.82 }, // kart 39
      ],
    },
    // kuşbakışı: parşömen keçe üstünde, kenar notu parlar
    {
      no: 361, yakin: 2.2, kamera: 0, odakY: 560,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Şarkiyatçı Paul Kahle teşhis", "ediyor: Piri Reis, 1513.", "Kenarda Kolomb'un adı."], sure: 5.79, renk: ALTIN }, // kart 40
      ],
    },
    // 1933: Kahle çalışma odasında yazısını tutar
    {
      no: 362, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kahle 1933'te yazıyor:", "Kolomb'un kayıp haritasının", "izi bir Türk haritasında."], sure: 5.79 }, // kart 41
      ],
    },
    // kuşbakışı: parça ve kayıp kısmın noktalı çizgisi
    {
      no: 363, yakin: 2.2, kamera: 0, odakY: 560,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Elde kalan, haritanın", "yaklaşık üçte biri."], sure: 3.12, renk: KIZIL }, // kart 42
      ],
    },
    // 1960, gece: Yarbay Ohlmeyer lambanın altında mektup yazar
    {
      no: 364, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ama harita ünlenince", "başka bir hikâye doğuyor."], sure: 3.50, renk: KIZIL }, // kart 43
        { satirlar: ["1960. ABD Hava Kuvvetleri'nden", "Yarbay Ohlmeyer, yazar Charles", "Hapgood'a bir mektup yazıyor:"], sure: 6.93 }, // kart 44
      ],
    },
    // kuşbakışı, soğuk mavi: haritanın altındaki kıyı
    {
      no: 365, yakin: 2.2, kamera: 0, odakY: 560,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["haritanın altı Antarktika", "kıyısını gösteriyor gibi."], sure: 3.89 }, // kart 45
      ],
    },
    // kitap yığınları: Hapgood elinde kitabı
    {
      no: 366, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bir araştırma değil,", "kısa bir cevap. Altı yıl sonra", "Hapgood bunu kitabına taşıyor."], sure: 6.25 }, // kart 46
        { satirlar: ["İki yıl sonra von Däniken", "daha ileri gidiyor: haritayı", "havadan çekilmiş sayıyor."], sure: 6.10 }, // kart 47
      ],
    },
    // kuşbakışı, sıcak ışık: doğuya bükülmüş kıyı altınla izlenir
    {
      no: 367, yakin: 2.2, kamera: 0, odakY: 560,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["2000'de harita", "tarihçisi Gregory McIntosh", "cevap veriyor."], sure: 4.27 }, // kart 48
        { satirlar: ["O kıyı Antarktika değil.", "Parşömene sığsın diye doğuya", "bükülmüş Güney Amerika."], sure: 5.87, renk: ALTIN }, // kart 49
      ],
    },
    // kenardaki kaynaklar: 337'ye dönüş
    {
      no: 337, yakin: 2.2, kamera: 0, odakY: 560,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Piri kaynaklarını zaten", "kenara yazmıştı: haritalar", "ve bir esirin anlattıkları."], sure: 5.94, renk: ALTIN }, // kart 50
      ],
    },
    // bugün: vitrindeki harita (331'e dönüş)
    {
      no: 331, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Harita dört yüz yılı aşkın", "unutuldu, bulundu,", "dünya konuştu."], sure: 4.57, renk: ALTIN }, // kart 51
      ],
    },
    // boş avlu, gece (352)
    {
      no: 352, yakin: 2.8, kamera: 4,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Haritayı çizen adam ise", "seksenini geçmişken,"], sure: 3.35, renk: KIZIL }, // kart 52
        { satirlar: ["Gelibolu'dan çok uzakta", "boynunu verdi."], sure: 2.90, renk: KIZIL }, // kart 53
      ],
    },
    // Basra'da kalan donanma: soru (349)
    {
      no: 349, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Siz olsanız o donanmayı", "Basra'da bırakır mıydınız?"], sure: 3.81, renk: ALTIN }, // kart 54
      ],
    },
  ],
  kapanis: {
    satirlar: ["Piksel Tarih", "@pikseltarihim"],
    sonraki: "Yorumlara yaz, arkadaşına gönder",
    sure: 3, arka: 349, gece: true,
  },
};

export const PIRI_REIS_KARE = Math.round(seriSure(PIRI_REIS_SERI) * T_FPS);
export const PiriReis: React.FC = () => <SeriVideo seri={PIRI_REIS_SERI} />;
