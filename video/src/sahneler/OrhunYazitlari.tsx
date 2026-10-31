import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Taş Konuşuyor: Orhun yazıtları ve Vilhelm Thomsen (1893). Grafikerin tarifi
   (teslimler/gece/ara/orhun-yazitlari/5-grafik.md), sahneler 130-161, çizim video/piksel/orhun_yazitlari.py.
   Kartlar 4-kalite-metin.md "Nihai ekran kartları" ile bire bir (42 kart, harfi harfine).
   Süreler tahmini (seslendirme ≈240 sn); ses/hizala_seri.py sese göre yeniden yazar. */
// Kapak: ajans sahibi görsel vermedi. Kapak, sahne 130 katmanlarıyla yapılan ilk Bolum'dür (2 sn, sessiz);
// ekranda etiket (PİKSEL TARİHİM · ORHUN YAZITLARI) ve başlık durur; logo/@pikseltarihim bandı yalnız kapanış
// kartındadır (seri.kapak tanımlı değil). yaziY 240 olan sahnelerde kart 4-5 satırdır:
// yazı yukarı alınır, figürler yazının altında kalır (orhun_yazitlari.py YAZI_ALT denetimi).
export const ORHUN_SERI: Seri = {
  etiket: "PİKSEL TARİHİM · ORHUN YAZITLARI",
  ses: "orhun-yazitlari-anlatim.mp3",
  bolumler: [
    { // KAPAK
      no: 130, yakin: 2.8, kamera: 0,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Taş Konuşuyor", "Bin yüz altmış bir yıl", "sonra çözüldü"], sure: 2.0, boy: 112, renk: ALTIN },
      ],
    },
    // Kart 1-2: bozkırda yalnız yazıt taşı, şafak; harfler ışıyıp söner (taş konuşuyor).
    {
      no: 130, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Moğolistan bozkırında bir taş.", "Üstünde kimsenin", "okuyamadığı harfler."], sure: 5.06 }, // kart 1
        { satirlar: ["Taş konuşuyor.", "Kimse anlamıyor."], sure: 2.37, renk: ALTIN }, // kart 2
      ],
    },
    // Kart 3: Kopenhag 1893, gece; Thomsen masasında taşın fotoğraflarına bakar.
    {
      no: 131, yakin: 2.8, kamera: 6,
      yaziY: 240,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kopenhag, 1893. Bir adam", "masasında bu taşın", "fotoğraflarına bakıyor.", "Taş o gün bin yüz", "altmış bir yaşında."], sure: 8.20, boy: 72 }, // kart 3
      ],
    },
    // Kart 4-5: Thomsen yakın plan.
    {
      no: 132, yakin: 3.2, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Adamın adı Vilhelm Thomsen.", "Elli bir yaşında, Danimarkalı.", "Türk değil, Rus değil."], sure: 5.98 }, // kart 4
        { satirlar: ["Dilbilimci. Taştan neredeyse", "altı bin kilometre uzakta.", "Peki bu taş ne diyor?"], sure: 4.83, renk: ALTIN }, // kart 5
      ],
    },
    // Kart 6: Orhun Vadisi 732; taş dikilir, Bilge Kağan izler.
    {
      no: 133, yakin: 2.6, kamera: 10,
      sprite: { w: 400, h: 230, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Orhun Vadisi, 732.", "Bilge Kağan kardeşi için", "anıt taş diktiriyor."], sure: 5.19 }, // kart 6
      ],
    },
    // Kart 7: Kül Tigin'in höyüğü, binicisiz at, koyunlar.
    {
      no: 134, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Kül Tigin bir yıl önce,", "koyun yılında öldü.", "Kırk yedi yaşındaydı."], sure: 4.13 }, // kart 7
      ],
    },
    // Kart 8-9: usta taşı kazır, yazıcı Yollıg Tigin yazar.
    {
      no: 135, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 230, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ağabeyi savaşlarını", "taşa kazıtıyor."], sure: 3.18 }, // kart 8
        { satirlar: ["Yazıcı Yollıg Tigin adını da", "taşa koyuyor:", "Bunu ben yazdım, diyor."], sure: 3.88 }, // kart 9
      ],
    },
    // Kart 10: otağda yatan Bilge Kağan, gece.
    {
      no: 136, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["İki yıl sonra Bilge Kağan", "da ölür. Çin kaynaklarına", "göre zehirlenir."], sure: 4.80, renk: KIZIL }, // kart 10
      ],
    },
    // Kart 11: 735, aynı vadide iki taş.
    {
      no: 137, yakin: 2.6, kamera: 10,
      yaziY: 240,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["735'te onun taşı da dikilir.", "İki taş, aynı vadide,", "birbirine yakın.", "Biri ağabeyin, biri kardeşin."], sure: 6.40 }, // kart 11
      ],
    },
    // Kart 12: Tuul vadisi, Tonyukuk ve iki dikili taşı.
    {
      no: 138, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Daha doğuda, Tuul vadisinde", "üçüncü bir taş. Yaşlı danışman", "Tonyukuk sağlığında diktirmiş."], sure: 7.16 }, // kart 12
      ],
    },
    // Kart 13: yüzyıllar; kar fırtınasında yalnız taş (motif).
    {
      no: 139, yakin: 2.8, kamera: 6,
      hava: 10,
      yaziY: 240,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Kağanlık yıkılır.", "Taşlar kalır. Yüzyıllar geçer.", "Taş hâlâ konuşuyor.", "Kimse anlamıyor."], sure: 5.24, renk: ALTIN }, // kart 13
      ],
    },
    // Kart 14: Poltava 1709; Strahlenberg esir, sola yürür.
    {
      no: 140, yakin: 2.8, kamera: 10,
      sprite: { w: 400, h: 230, fps: 16, x: [300, 240], taban: 632 },
      yazilar: [
        { satirlar: ["Poltava, 1709. İsveçli subay", "Strahlenberg Ruslara", "esir düşüyor."], sure: 5.67, renk: KIZIL }, // kart 14
      ],
    },
    // Kart 15-16: Sibirya; Strahlenberg Yenisey taşının kopyasını çıkarır.
    {
      no: 141, yakin: 2.8, kamera: 8,
      hava: 10,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Çar onu Sibirya'ya, Tobolsk'a", "sürüyor. Yenisey boylarında", "garip işaretli taşlar görüyor."], sure: 6.49 }, // kart 15
        { satirlar: ["Kopyalarını çıkarıyor.", "1730'da Stockholm'de basıyor.", "Avrupa bakıyor, okuyamıyor."], sure: 6.57 }, // kart 16
      ],
    },
    // Kart 17: Yenisey taşı ve Orhun taşı; aynı harfler ışır.
    {
      no: 142, yakin: 2.6, kamera: 8,
      yaziY: 240,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bunlar Orhun'daki taşlar", "değil. Ama yazı akraba.", "Çözüme daha", "yüz altmış üç yıl var."], sure: 5.53, renk: ALTIN }, // kart 17
      ],
    },
    // Kart 18: 1889, Yadrintsev taşı bulur; arkada çadırı ve ikinci taş.
    {
      no: 143, yakin: 2.6, kamera: 10,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Orhun Vadisi, 1889. Sibiryalı", "gezgin Yadrintsev iki taşı", "buluyor. Dünya haberi alıyor."], sure: 7.05 }, // kart 18
      ],
    },
    // Kart 19: Fin seferi; fotoğraf ve kopya.
    {
      no: 144, yakin: 2.8, kamera: 8,
      yaziY: 240,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ertesi yıl Fin-Ugor", "Cemiyeti'nin seferi geliyor.", "Fotoğraf çekiyor,", "kopya çıkarıyorlar."], sure: 6.26 }, // kart 19
      ],
    },
    // Kart 20: Radloff ve Ruslar, elleri kâğıt dolu.
    {
      no: 145, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bir yıl sonra Ruslar.", "Başlarında Türkolog Radloff.", "Kopya çok. Okuyan hâlâ yok."], sure: 5.10 }, // kart 20
      ],
    },
    // Kart 21-22: taşın Çince yan yüzü kızıl ışır.
    {
      no: 146, yakin: 3.0, kamera: 6,
      yaziY: 240,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Kül Tigin'in taşında", "bir ipucu var. Bir yüzü Çince.", "Çinceyi okuyan var."], sure: 4.91 }, // kart 21
        { satirlar: ["Yazdıran, Çin imparatoru", "Xuanzong. Bir Türk kahramanın", "taşında Çin imparatorunun", "sözleri."], sure: 6.15 }, // kart 22
      ],
    },
    // Kart 23: Leiden 1892, Schlegel Çince yüzü çevirir.
    {
      no: 147, yakin: 2.8, kamera: 6,
      yaziY: 240,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["1892'de Leidenli sinolog", "Schlegel o yüzü çeviriyor.", "Taşın kime dikildiği", "artık belli."], sure: 7.43 }, // kart 23
      ],
    },
    // Kart 24: gece; Türkçe yüz sessiz.
    {
      no: 148, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ama Türkçe yüzler", "hâlâ sessiz.", "Bilge Kağan'ın sözü orada."], sure: 3.60, renk: KIZIL }, // kart 24
      ],
    },
    // Kart 25-26: Thomsen'in masasında Helsingfors albümü.
    {
      no: 149, yakin: 2.8, kamera: 6,
      yaziY: 240,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Aynı yıl Fin fotoğrafları", "Helsingfors'ta basılıyor.", "Bir nüsha", "Thomsen'in masasında."], sure: 6.73 }, // kart 25
        { satirlar: ["Önünde bilinmeyen harfler.", "Bilinmeyen kelimeler.", "Sözlük yok, öğretmen yok."], sure: 4.51 }, // kart 26
      ],
    },
    // Kart 27: Ruslar, Radloff, Finler taşın önünde.
    {
      no: 150, yakin: 2.6, kamera: 8,
      yaziY: 240,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Çözümü ilk yayımlayan,", "taşı bulan Ruslar değil.", "Türkolog Radloff değil.", "Kopyayı çıkaran Finler değil."], sure: 6.97, renk: KIZIL }, // kart 27
      ],
    },
    // Kart 28-29: Kraliyet Akademisi, Thomsen kürsüde.
    {
      no: 151, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["1893'te Danimarka Kraliyet", "Akademisi'nde çözümü duyuran", "adam Danimarkalı Thomsen."], sure: 7.66, renk: ALTIN }, // kart 28
        { satirlar: ["Bildirisi Fransızca. Başlığı:", "Orhun ve Yenisey", "yazıtlarının çözümü."], sure: 4.59 }, // kart 29
      ],
    },
    // Kart 30: gün doğumu; taşın bütün harfleri altın.
    {
      no: 152, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Taş konuşuyor. Bu kez", "Kopenhag'da biri anlıyor.", "Peki taş ne diyor?"], sure: 4.37, renk: ALTIN }, // kart 30
      ],
    },
    // Kart 31-32: mavi gök, yağız yer, arada insanoğlu.
    {
      no: 153, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Taşın ilk kelimesi Tengri.", "Tanrı. Bir başka yüzünde", "yaratılış:"], sure: 4.27 }, // kart 31
        { satirlar: ["Üstte mavi gök, altta yağız", "yer yaratılmış. İkisinin", "arasında insanoğlu."], sure: 4.61, renk: ALTIN }, // kart 32
      ],
    },
    // Kart 33: Bilge Kağan halkına seslenir.
    {
      no: 154, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Taşta konuşan, Bilge Kağan.", "Halkına sesleniyor.", "Tekin çevirisiyle:"], sure: 4.63 }, // kart 33
      ],
    },
    // Kart 34-35: Çin elçisi ipek uzatır; arkada Çin şehri.
    {
      no: 155, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Çin'in sözü tatlı,", "ipeği yumuşak, diyor."], sure: 2.47 }, // kart 34
        { satirlar: ["Tatlı sözle uzak halkı", "yanına çeker. Yerleştikten", "sonra kötülüğünü gösterir."], sure: 5.18, renk: KIZIL }, // kart 35
      ],
    },
    // Kart 36: taşın iki yüzü: Türkçe uyarı ve Çince yazı.
    {
      no: 156, yakin: 3.0, kamera: 6,
      yaziY: 240,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Aynı taşın bir yüzünde", "Çin'e karşı uyarı,", "öbür yüzünde Çin", "imparatorunun yazısı."], sure: 5.35, boy: 80, renk: KIZIL }, // kart 36
      ],
    },
    // Kart 37-38: Bilge Kağan taşının yanında; arkada yurtlar.
    {
      no: 157, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bin üç yüz yıl önce bir kağan", "halkını uyarıyor.", "Uyarı taşa kazılı, bozkırda."], sure: 5.76 }, // kart 37
        { satirlar: ["Taşta bir dilek daha var:", "Türk halkının adı sanı", "yok olmasın."], sure: 4.12, renk: ALTIN }, // kart 38
      ],
    },
    // Kart 39: Radloff'un masasında basılı okumalar.
    {
      no: 158, yakin: 2.8, kamera: 6,
      yaziY: 240,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Taşı bulan Yadrintsev", "bir yıl sonra ölür. Radloff'un", "okumaları 1894'te", "basılmaya başlar."], sure: 6.82 }, // kart 39
      ],
    },
    // Kart 40: Tonyukuk'un taşları yalnız; 1897'de bulunacak.
    {
      no: 159, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ve üçüncü taş, Tonyukuk,", "hâlâ keşfedilmemiş. Dört yıl", "sonra, 1897'de bulunacak."], sure: 7.02, renk: ALTIN }, // kart 40
      ],
    },
    // Kart 41: Thomsen şafakta pencere önünde.
    {
      no: 160, yakin: 3.0, kamera: 6,
      yaziY: 240,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bilge Kağan'ın sesi bin yüz", "altmış bir yıl sonra yeniden", "duyuluyor. Duyuran,", "bir Danimarkalı."], sure: 5.89, renk: ALTIN }, // kart 41
      ],
    },
    // Kart 42: gece, yıldızlar; taşın harfleri ışır.
    {
      no: 161, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sizce o uyarı", "bugün hâlâ geçerli mi?"], sure: 3.38, renk: ALTIN }, // kart 42
      ],
    },
  ],
  kapanis: {
    satirlar: ["Piksel Tarih", "@pikseltarihim"],
    sonraki: "Yorumlara yaz, arkadaşına gönder",
    sure: 3, arka: 161, gece: true,
  },
};

export const ORHUN_KARE = Math.round(seriSure(ORHUN_SERI) * T_FPS);
export const OrhunYazitlari: React.FC = () => <SeriVideo seri={ORHUN_SERI} />;
