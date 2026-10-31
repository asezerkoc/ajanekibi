import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Su Akmıyor: Sokollu Mehmed Paşa'nın Don-Volga kanalı ve Astrahan seferi (1569 → 1952). Grafikerin tarifi:
   teslimler/gece/ara/don-volga-kanali/5-grafik.md; sahneler 250-289 (video/piksel/don_volga_kanali.py).
   Kartlar kalite kontrolün nihai 52 kartıyla harfi harfine aynı; süreler tahmini (seslendirme 254 sn),
   ses/hizala_seri.py sese göre yeniden yazar. */
// Kapak: sahne 250 katmanlarıyla yapılan ilk Bolum (2 sn, sessiz); başlık editörün ve kalite kontrolün onayladığı metin.
// Sahne 264 panoramadır: kamera 300 ile orta plan ve sprite birlikte kayar (sağdan sola), iki nehir aynı karede görünmez.
// Sahne 284-286 kanal kapağını önden gösterir: sprite tabanı 760, odak 620 (kanal kadrajın altına kadar uzanır).
export const DON_VOLGA_SERI: Seri = {
  etiket: "PİKSEL TARİHİM · DON-VOLGA KANALI",
  ses: "don-volga-kanali-anlatim.mp3",
  bolumler: [
    { // KAPAK
      no: 250, yakin: 2.8, kamera: 0, yaziY: 270,
      sprite: { w: 400, h: 230, fps: 12, x: 270, taban: 640 },
      yazilar: [
        { satirlar: ["383 Yıl", "Akmayan Su", "Sokollu'nun Don-Volga kanalı"], sure: 2.0, boy: 112, renk: ALTIN },
      ],
    },
    // şafak, bozkır: ilk kazma toprağa iner; Kasım Paşa izler
    {
      no: 250, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 230, fps: 12, x: 270, taban: 640 },
      yazilar: [
        { satirlar: ["Don ile Volga'yı birleştirmek", "için ilk kazma toprağa iniyor.", "Yıl 1569."], sure: 5.60 }, // kart 1
        { satirlar: ["Su ise ancak 1952'de akıyor.", "Arada üç yüz seksen üç yıl", "ve iki imparatorluk var."], sure: 6.40, renk: ALTIN }, // kart 2
      ],
    },
    // alacakaranlık: yarım kalmış sığ hendek, toprağa saplı kazma, tek asker
    {
      no: 251, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 640 },
      yazilar: [
        { satirlar: ["Peki bu hendek", "neden yarım kaldı?"], sure: 2.64, renk: ALTIN }, // kart 3
      ],
    },
    // İstanbul 1568: Sokollu harita sehpasının başında
    {
      no: 252, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["İstanbul, 1568.", "Veziriazam Sokollu Mehmed Paşa", "haritaya bakıyor."], sure: 5.12 }, // kart 4
      ],
    },
    // harita yakın: Don Azak'a, Volga Hazar'a; aradaki dar boğaz
    {
      no: 253, yakin: 3.2, kamera: 4,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bozkırda iki nehir", "birbirine neredeyse değiyor.", "Don, Azak Denizi'ne akıyor,"], sure: 6.00 }, // kart 5
        { satirlar: ["oradan Karadeniz'e.", "Volga, Hazar'a.", "Arada dar bir kara boğazı var:"], sure: 5.28 }, // kart 6
      ],
    },
    // Perevoloka: kütükler üstünde karadan çekilen tekne; önde halat çeken üç adam
    {
      no: 254, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Perevoloka.", "Gemiler yüzyıllardır burada", "karadan çekiliyor."], sure: 4.64 }, // kart 7
      ],
    },
    // Astrahan: Volga'daki adada ahşap Rus kalesi; önde iki Rus nöbetçi
    {
      no: 255, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sokollu'nun derdi bir kale:", "Astrahan.", "1556'da Ruslar aldı."], sure: 4.64, renk: KIZIL }, // kart 8
      ],
    },
    // alacakaranlık: yolu kapalı Türkistan hacıları ve develeri bekler
    {
      no: 256, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["O günden beri Türkistan", "hacılarının yolu kapalı."], sure: 3.84 }, // kart 9
        { satirlar: ["İran yolu da Safevîlerle", "düşmanlık yüzünden kapalı."], sure: 4.08 }, // kart 10
      ],
    },
    // Sokollu fermanı defterdar Kasım'a uzatır; arkada harita
    {
      no: 257, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Hendek açılırsa gemiler", "Volga'ya inecek. Astrahan", "düşecek. Hac yolu açılacak."], sure: 6.16, renk: ALTIN }, // kart 11
        { satirlar: ["Sokollu işi", "defterdar Kasım'a veriyor.", "Onu Kefe beylerbeyi yapıyor."], sure: 5.36 }, // kart 12
      ],
    },
    // 14 Mart 1569: Maltsev ve uşağı Volga kıyısında at sürer; buzlu nehir
    {
      no: 258, yakin: 2.6, kamera: 10,
      sprite: { w: 400, h: 220, fps: 14, x: [300, 250], taban: 632 },
      yazilar: [
        { satirlar: ["14 Mart 1569. Perevoloka.", "Bir Rus elçisi Volga'yı", "geçiyor: Semen Maltsev."], sure: 5.84 }, // kart 13
      ],
    },
    // Nogay atlısı yaralı ve bağlı Maltsev'i Azak'a götürür
    {
      no: 259, yakin: 2.6, kamera: 10,
      sprite: { w: 400, h: 220, fps: 12, x: [300, 252], taban: 632 },
      yazilar: [
        { satirlar: ["Yakalanıyor, yaralanıyor,", "Don'un ağzındaki", "Azak kalesine götürülüyor."], sure: 5.52, renk: KIZIL }, // kart 14
      ],
    },
    // kadırga güvertesi: kürek başında esir Maltsev, nöbetçi, kıçta Kasım Paşa
    {
      no: 260, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sonra Kasım Paşa'nın gemisine,", "esir olarak. Bütün seferi", "içeriden izleyecek."], sure: 6.08, renk: ALTIN }, // kart 15
      ],
    },
    // Ağustos 1569: kadırgalar Don'dan yukarı çıkar
    {
      no: 261, yakin: 2.6, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 260, fps: 12, x: [250, 290], taban: 640 },
      yazilar: [
        { satirlar: ["Ağustos 1569.", "Kadırgalar Don'dan", "yukarı çıkıyor."], sure: 3.84 }, // kart 16
      ],
    },
    // bozkırda Devlet Giray ak atında; arkasında atlıları
    {
      no: 262, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bozkırda Kırım Hanı", "Devlet Giray bekliyor,", "on binlerce atlıyla."], sure: 5.04 }, // kart 17
        { satirlar: ["Yüzü asık.", "Çünkü bu hendek", "onun için tehdit."], sure: 3.52, renk: KIZIL }, // kart 18
      ],
    },
    // Han uzakta nehirdeki kadırgalara bakar
    {
      no: 263, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Osmanlı gemileri Volga'ya", "girerse Kırım'ın", "özerkliği biter."], sure: 4.72, renk: KIZIL }, // kart 19
      ],
    },
    // panorama: solda Don, sağda Volga; arada hendek boyunca kazıcılar
    {
      no: 264, yakin: 2.6, kamera: 300,
      sprite: { w: 560, h: 230, fps: 12, x: 270, taban: 640 },
      yazilar: [
        { satirlar: ["Kazmalar toprağa iniyor.", "Düz, ağaçsız bozkır. Bir yanda", "Don, öbür yanda Volga."], sure: 6.24 }, // kart 20
      ],
    },
    // öğle güneşi: hendekte kazan askerler; su yok
    {
      no: 265, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 230, fps: 12, x: 270, taban: 640 },
      yazilar: [
        { satirlar: ["Asker kazıyor.", "Günler geçiyor.", "Su akmıyor."], sure: 3.36, renk: ALTIN }, // kart 21
      ],
    },
    // akşam: kazı bırakılır; kazmalar toprakta, askerler sola gider
    {
      no: 266, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 230, fps: 14, x: [292, 258], taban: 640 },
      yazilar: [
        { satirlar: ["Bir ay bile dolmuyor. Kazı", "bırakılıyor. Ne kadar kazıldı?", "Kaynaklar ayrışıyor:"], sure: 6.24 }, // kart 22
        { satirlar: ["kimine göre kanalın üçte biri,", "kimine göre kazma neredeyse", "toprağa değmedi."], sure: 6.00 }, // kart 23
      ],
    },
    // Kasım Paşa Azak'ı gösterir; ağır top kağnıda, öküzler koşulu
    {
      no: 267, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Kasım Paşa karar veriyor.", "Ağır toplar ve büyük gemiler", "Azak'a geri."], sure: 5.36 }, // kart 24
      ],
    },
    // ordu karadan doğuya, Astrahan'a yürür; toplar yok
    {
      no: 268, yakin: 2.8, kamera: 10,
      sprite: { w: 400, h: 220, fps: 16, x: [250, 296], taban: 632 },
      yazilar: [
        { satirlar: ["Ordu karadan Astrahan'a.", "Kaleyi almaya gidiyorlar."], sure: 4.00 }, // kart 25
        { satirlar: ["Ama kale yıkacak toplar", "artık yanlarında değil."], sure: 3.76, renk: KIZIL }, // kart 26
      ],
    },
    // Eylül 1569: harabeler arasında kamp; asker çadır kazığı çakar
    {
      no: 269, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Eylül 1569. Astrahan önleri.", "Ordu şehrin eski yerinde,", "harabelerde kamp kuruyor."], sure: 6.40 }, // kart 27
      ],
    },
    // Kasım Paşa ve ağa uzaktaki adalı kaleye bakar; top yok
    {
      no: 270, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Kuşatma topu yok. Hücum yok.", "Kasım Paşa kışı burada geçirip", "baharda saldırmayı planlıyor."], sure: 7.12 }, // kart 28
      ],
    },
    // gece: ateş başında iki asker fısıldaşır; uzakta Han'ın otağı
    {
      no: 271, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sonra çadırlarda", "bir fısıltı dolaşıyor:", "\"Burada kış dokuz ay sürer.\""], sure: 5.44, renk: KIZIL }, // kart 29
        { satirlar: ["Asker huzursuz. Fısıltıyı", "kim yaydı? Tarihçiler", "Kırım Hanı'nı işaret ediyor."], sure: 6.08 }, // kart 30
      ],
    },
    // şafak: ulak dörtnala kampa girer
    {
      no: 272, yakin: 2.8, kamera: 10,
      sprite: { w: 400, h: 220, fps: 24, x: [330, 214], taban: 632 },
      yazilar: [
        { satirlar: ["Derken Rus takviyesinin", "yaklaştığı haberi geliyor."], sure: 4.00 }, // kart 31
      ],
    },
    // Eylül sonu, yağmur: çadırlar sökülür, asker yüklerle batıya döner
    {
      no: 273, yakin: 2.8, kamera: 8, hava: 30,
      sprite: { w: 400, h: 220, fps: 14, x: [286, 256], taban: 632 },
      yazilar: [
        { satirlar: ["Eylül sonu.", "Kuşatma kaldırılıyor.", "İki haftayı bulmadı."], sure: 4.32, renk: KIZIL }, // kart 32
      ],
    },
    // boş kamp yeri: sönmüş ateşten duman, yerde sökülmüş çadır
    {
      no: 274, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Orduyu Ruslar yenmedi.", "Meydan savaşı bile olmadı.", "Bir söylenti yendi."], sure: 5.52, renk: ALTIN }, // kart 33
      ],
    },
    // Kuzey Kafkasya, kavurucu güneş: diz çökmüş asker kuru dere yatağında su için kazar
    {
      no: 275, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Dönüş yolu Kuzey Kafkasya'dan.", "Erzak azalıyor. Su yok.", "Kazmayı vuran eller su arıyor."], sure: 6.80, renk: KIZIL }, // kart 34
      ],
    },
    // saldırı: oklar yağar, kalkanlı asker, düşmüş asker; uzakta Kazak atlıları
    {
      no: 276, yakin: 2.8, kamera: 8, sarsinti: 2,
      sprite: { w: 400, h: 220, fps: 18, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Kazaklar ve Çerkesler", "yol boyu saldırıyor.", "Binlerce asker yolda ölüyor."], sure: 5.68, renk: KIZIL }, // kart 35
      ],
    },
    // Azak, fırtına sonrası: kırık direkli kadırga; uzakta barut deposundan duman
    {
      no: 277, yakin: 2.6, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 260, fps: 10, x: 270, taban: 640 },
      yazilar: [
        { satirlar: ["Azak'a varıyorlar. Donanma", "fırtınada ağır hasar görmüş."], sure: 4.40, renk: KIZIL }, // kart 36
        { satirlar: ["Rivayete göre bir barut", "deposu da patlamış."], sure: 3.44 }, // kart 37
      ],
    },
    // Maltsev yalnız, kuzeye (sola) yürür; ilk kar
    {
      no: 278, yakin: 2.8, kamera: 8, hava: 10,
      sprite: { w: 400, h: 220, fps: 14, x: [292, 256], taban: 632 },
      yazilar: [
        { satirlar: ["Esir elçi Maltsev", "hepsini görüyor.", "Sonra Moskova'ya dönüyor."], sure: 4.80 }, // kart 38
      ],
    },
    // Moskova, ahşap oda: Maltsev mum ışığında raporunu yazar
    {
      no: 279, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Rus tarafının en ayrıntılı", "tanıklığı, o esirin raporu."], sure: 4.32, renk: ALTIN }, // kart 39
      ],
    },
    // alacakaranlık: otlarla örtülmüş kuru hendek, paslı kazma
    {
      no: 280, yakin: 2.8, kamera: 4,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 640 },
      yazilar: [
        { satirlar: ["Osmanlı bir daha", "Astrahan'a yürümüyor.", "Su akmıyor."], sure: 4.00, renk: ALTIN }, // kart 40
      ],
    },
    // 1697: Çar Petro ve mühendis Perry; köylü kazar
    {
      no: 281, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 230, fps: 12, x: 270, taban: 640 },
      yazilar: [
        { satirlar: ["1697. Çar Petro daha kuzeyde,", "aynı iki nehir arasında", "kazı başlatıyor."], sure: 5.60 }, // kart 41
        { satirlar: ["Ertesi yıl işin başına", "İngiliz mühendis", "John Perry geçiyor."], sure: 4.72 }, // kart 42
      ],
    },
    // kuzeyde terk edilmiş hendek, kar; el arabası ve kürek
    {
      no: 282, yakin: 2.8, kamera: 4, hava: 10,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 640 },
      yazilar: [
        { satirlar: ["Savaş çıkıyor, iş bırakılıyor.", "Su yine akmıyor."], sure: 3.76, renk: ALTIN }, // kart 43
      ],
    },
    // 1948: dikenli tel ardında mahkûmlar kazar; gardiyan, gözcü kulesi
    {
      no: 283, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 230, fps: 12, x: 270, taban: 640 },
      yazilar: [
        { satirlar: ["1948.", "Aynı boğaz, aynı bozkır."], sure: 2.40 }, // kart 44
        { satirlar: ["Bu kez kazmayı yüz binlerce", "Gulag mahkûmu ve savaş esiri", "vuruyor."], sure: 5.20, renk: KIZIL }, // kart 45
      ],
    },
    // 1952: beton kapak, kapalı; önündeki hazne kuru
    {
      no: 284, yakin: 2.6, kamera: 4, odakY: 620,
      sprite: { w: 400, h: 360, fps: 10, x: 270, taban: 760 },
      yazilar: [
        { satirlar: ["Yüz bir kilometre,", "on üç kapak."], sure: 2.48 }, // kart 46
      ],
    },
    // 31 Mayıs 1952, 13.55: kapak açılır, su hazneye hücum eder
    {
      no: 285, yakin: 2.6, kamera: 4, odakY: 620,
      sprite: { w: 400, h: 360, fps: 16, x: 270, taban: 760 },
      yazilar: [
        { satirlar: ["31 Mayıs 1952,", "saat on üç elli beş. Don ile", "Volga'nın suları birleşiyor."], sure: 5.76 }, // kart 47
      ],
    },
    // su, nihayet akıyor: dolu kanal, sakin akan su
    {
      no: 286, yakin: 2.6, kamera: 4, odakY: 620,
      sprite: { w: 400, h: 360, fps: 12, x: 270, taban: 760 },
      yazilar: [
        { satirlar: ["Su, nihayet akıyor."], sure: 1.52, renk: ALTIN }, // kart 48
      ],
    },
    // kanal girişinde dev Stalin heykeli (yüzsüz siluet)
    {
      no: 287, yakin: 2.8, kamera: 4, yaziY: 240,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Kanalın girişine dev bir", "Stalin heykeli dikiliyor."], sure: 4.00 }, // kart 49
      ],
    },
    // kaide boş; sonra aynı kaidede Lenin
    {
      no: 288, yakin: 2.8, kamera: 4, yaziY: 240,
      sprite: { w: 400, h: 220, fps: 2, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["On yıl sonra kaldırılıyor.", "1973'te aynı kaideye", "Lenin dikiliyor."], sure: 5.12 }, // kart 50
      ],
    },
    // gün batımı: kanalda akan su; önde toprağa saplı eski kazma
    {
      no: 289, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Osmanlı'nın hendeği değil bu.", "Ama aynı bozkır, aynı fikir,", "aynı iki nehir."], sure: 5.92, renk: ALTIN }, // kart 51
        { satirlar: ["Sizce Kasım Paşa o kışa", "dayansaydı, su üç yüz", "seksen üç yıl bekler miydi?"], sure: 5.84, renk: ALTIN }, // kart 52
      ],
    },
  ],
  kapanis: {
    satirlar: ["Piksel Tarih", "@pikseltarihim"],
    sonraki: "Yorumlara yaz, arkadaşına gönder",
    sure: 3, arka: 289,
  },
};

export const DON_VOLGA_KARE = Math.round(seriSure(DON_VOLGA_SERI) * T_FPS);
export const DonVolga: React.FC = () => <SeriVideo seri={DON_VOLGA_SERI} />;
