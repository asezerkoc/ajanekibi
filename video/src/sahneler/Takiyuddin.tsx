import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Aynı Gökyüzü, İki Gözlemevi: Takiyüddin'in İstanbul Rasathanesi (1577-1580). Grafikerin tarifi
   (teslimler/gece/ara/takiyuddin-rasathanesi/5-grafik.md), sahneler 410-449 (video/piksel/takiyuddin_rasathanesi.py).
   Kartlar 4-kalite-metin.md "Nihai ekran kartları" ile harfi harfine aynı ve aynı sırada (51 kart).
   Süreler tahmini (harf/14 + 0,4 sn); ses/hizala_seri.py sese göre yeniden yazar. */
// Kapak: ajans sahibi görsel vermedi. Kapak, sahne 410 katmanlarıyla yapılan ilk Bolum'dür (2 sn, sessiz);
// başlık ve alt başlık editörün kapak önerisinden. Uzun kartlarda (11, 19, 39) yazı yukarı alınır (yaziY) ve
// küçültülür (boy) ki figürlerin ve yapıların tepesiyle çakışmasın.
export const TAKIYUDDIN_SERI: Seri = {
  etiket: "PİKSEL TARİHİM · TAKİYÜDDİN",
  ses: "takiyuddin-rasathanesi-anlatim.mp3",
  bolumler: [
    { // KAPAK
      no: 410, yakin: 2.6, kamera: 0,
      sprite: { w: 400, h: 300, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Aynı Gökyüzü,", "İki Gözlemevi", "Takiyüddin'in üç yılı"], sure: 2.0, boy: 112, renk: ALTIN },
      ],
    },
    // 410: Kanca: yıkım (anlatıya göre), Ocak 1580
    {
      no: 410, yakin: 2.6, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bir bina yıkılıyor."], sure: 1.61, renk: KIZIL }, // kart 1
        { satirlar: ["Anlatıldığına göre", "topları binaya çevirenler", "düşman değil.", "Padişahın kendi donanması."], sure: 5.28, renk: KIZIL }, // kart 2
      ],
    },
    // 411: Tophane sırtı, alacakaranlık
    {
      no: 411, yakin: 2.2, kamera: 10,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ocak 1580. Tophane'nin", "yukarısı, İstanbul."], sure: 4.47 }, // kart 3
        { satirlar: ["Bu binayı üç yıl önce", "aynı padişah kurdurmuştu."], sure: 2.95 }, // kart 4
      ],
    },
    // 412: Takiyüddin ve armilla
    {
      no: 412, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Adı: İstanbul Rasathanesi.", "Kuran: Takiyüddin."], sure: 3.03, renk: ALTIN }, // kart 5
        { satirlar: ["Bilim tarihçileri onun", "aletlerini Danimarkalı", "Tycho Brahe'nin aletleriyle", "yan yana karşılaştırıyor."], sure: 6.86 }, // kart 6
      ],
    },
    // 413: Soru: hedef
    {
      no: 413, yakin: 2.2, kamera: 10,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Peki ne oldu da padişahın", "kendi gözlemevi hedef oldu?"], sure: 3.48, renk: KIZIL }, // kart 7
      ],
    },
    // 414: Hven, 1576
    {
      no: 414, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Önce şunu bilin.", "Aynı yıllarda Danimarka'da,", "bir adada başka bir gözlemevi", "yükseliyor."], sure: 5.70 }, // kart 8
        { satirlar: ["Hven adası, 1576. Danimarka", "Kralı İkinci Frederik bu adayı", "Tycho Brahe'ye veriyor."], sure: 6.91 }, // kart 9
      ],
    },
    // 415: Uraniborg
    {
      no: 415, yakin: 2.2, kamera: 10,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Tycho oraya", "Uraniborg'u kuruyor."], sure: 1.28 }, // kart 10
      ],
    },
    // 416: İki gözlemci, iki dev alet (teleskop yok)
    {
      no: 416, yakin: 2.2, kamera: 8, yaziY: 220,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Teleskop henüz yok;", "ona daha otuz yıl var.", "Tycho da Takiyüddin de", "çıplak gözle, dev aletlerle", "bakıyor."], sure: 6.82, boy: 72 }, // kart 11
      ],
    },
    // 417: Motif: aynı gökyüzü, iki gözlemevi
    {
      no: 417, yakin: 2.0, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Aynı gökyüzü, iki gözlemevi."], sure: 2.35, renk: ALTIN }, // kart 12
        { satirlar: ["Biri yirmi bir yıl", "çalışacak.", "Öbürü üç."], sure: 1.45, renk: KIZIL }, // kart 13
      ],
    },
    // 418: Şam, 1559
    {
      no: 418, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Takiyüddin kim?", "Şam'da doğuyor."], sure: 2.67 }, // kart 14
        { satirlar: ["1559'da orada mekanik saatler", "üzerine bir kitap yazıyor."], sure: 5.11 }, // kart 15
      ],
    },
    // 419: Şam gecesi: saat ve gökyüzü
    {
      no: 419, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Derdi şu: saati gökyüzüne", "bağlamak,", "gözlemi saatle ölçmek."], sure: 3.35, renk: ALTIN }, // kart 16
      ],
    },
    // 420: İstanbul, 1571
    {
      no: 420, yakin: 2.8, kamera: 10,
      sprite: { w: 400, h: 300, fps: 16, x: [255, 285], taban: 632 },
      yazilar: [
        { satirlar: ["1571'de İstanbul'da", "müneccimbaşı oluyor."], sure: 3.96 }, // kart 17
      ],
    },
    // 421: Semerkant: Uluğ Bey
    {
      no: 421, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Hedefi büyük: Uluğ Bey'in", "Semerkant'ta hazırladığı", "yıldız cetvelini düzeltmek."], sure: 4.57 }, // kart 18
      ],
    },
    // 422: Uluğ Bey gözlemevi
    {
      no: 422, yakin: 2.2, kamera: 8, yaziY: 220,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Uluğ Bey bu cetvel için", "orada bir gözlemevi", "kurmuştu.", "Takiyüddin de kendi", "gözlemevini istiyor."], sure: 6.63, boy: 72 }, // kart 19
      ],
    },
    // 423: III. Murad onay verir
    {
      no: 423, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Padişah Üçüncü Murad", "kitabı ve resmi seven", "bir hükümdar. Onay veriyor."], sure: 4.45 }, // kart 20
      ],
    },
    // 424: 1577: aletler kuruluyor
    {
      no: 424, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 300, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Tophane'nin yukarısında", "aletler kuruluyor.", "1577, gözlemler başlıyor."], sure: 5.82, renk: ALTIN }, // kart 21
      ],
    },
    // 425: Kasım 1577: kuyruklu yıldız (İstanbul)
    {
      no: 425, yakin: 2.0, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Kasım 1577.", "Gökyüzünde bir şey beliriyor.", "Kuyruklu yıldız."], sure: 4.97, renk: ALTIN }, // kart 22
      ],
    },
    // 426: Hven: Tycho ölçer
    {
      no: 426, yakin: 2.2, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Tycho onu 13 Kasım'da görüyor.", "Yıldız Ocak 1578'e kadar,", "yaklaşık iki buçuk ay", "gökte kalıyor."], sure: 8.18 }, // kart 23
        { satirlar: ["Hven'de Tycho onu ölçüyor.", "Sonucu: yıldız Ay'ın ötesinde."], sure: 3.53, renk: ALTIN }, // kart 24
      ],
    },
    // 427: İstanbul: Takiyüddin bakar (motif yankısı)
    {
      no: 427, yakin: 2.2, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 250, taban: 632 },
      yazilar: [
        { satirlar: ["İstanbul'da aynı yıldıza", "Takiyüddin bakıyor.", "Aynı gökyüzü, aynı yıldız."], sure: 4.54, renk: ALTIN }, // kart 25
      ],
    },
    // 428: Ama: kaynaklar ayrışıyor
    {
      no: 428, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ama sonrası için", "kaynaklar ayrışıyor.", "En çok anlatılan hikâye şu."], sure: 4.11, renk: KIZIL }, // kart 26
      ],
    },
    // 429: Yorum: zafer (anlatıya göre)
    {
      no: 429, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Takiyüddin yıldızı", "Osmanlı'nın zaferine yoruyor."], sure: 3.09 }, // kart 27
      ],
    },
    // 430: Çıldır, Ağustos 1578
    {
      no: 430, yakin: 2.6, kamera: 12,
      sprite: { w: 400, h: 300, fps: 18, x: [245, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Ordu ertesi yıl", "Safevilere yürüyor.", "Çıldır, Ağustos 1578."], sure: 4.88 }, // kart 28
      ],
    },
    // 431: Veba
    {
      no: 431, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sonra İstanbul'a veba geliyor.", "Parmaklar rasathaneyi", "gösteriyor."], sure: 4.20, renk: KIZIL }, // kart 29
      ],
    },
    // 432: Şeyhülislam karşı çıkar
    {
      no: 432, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Şeyhülislam Kadızâde", "Ahmed Efendi karşı çıkıyor."], sure: 3.08, renk: KIZIL }, // kart 30
      ],
    },
    // 433: Kılıç Ali Paşa ve donanma
    {
      no: 433, yakin: 2.8, kamera: 8, yaziY: 270,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ve Ocak 1580.", "Topları çeviren donanmanın", "başında Kaptan-ı Derya", "Kılıç Ali Paşa var."], sure: 6.68, renk: KIZIL }, // kart 31
      ],
    },
    // 434: İnebahtı, 1571
    {
      no: 434, yakin: 2.4, kamera: 10,
      sprite: { w: 400, h: 300, fps: 10, x: [230, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Bu adam, 1571'de İnebahtı'dan", "gemilerini kurtarıp", "çıkan adam."], sure: 4.64 }, // kart 32
      ],
    },
    // 435: Kılıç Ali yıkımı yönetir
    {
      no: 435, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 300, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bir yıl sonra", "kaptan-ı derya olmuştu.", "Şimdi bir gözlemevini yıkıyor."], sure: 4.93, renk: KIZIL }, // kart 33
      ],
    },
    // 436: Tophane: top döküm ocağı
    {
      no: 436, yakin: 2.2, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Semtin adı zaten", "top döküm ocağından geliyor:", "Tophane."], sure: 3.19, renk: ALTIN }, // kart 34
      ],
    },
    // 437: Sinan ve Kılıç Ali Paşa Camii
    {
      no: 437, yakin: 2.8, kamera: 8, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Aynı yıllarda, aynı semtte", "Mimar Sinan, Kılıç Ali", "Paşa'ya bir cami yapıyor.", "Cami bugün ayakta."], sure: 6.03, renk: ALTIN }, // kart 35
      ],
    },
    // 438: Yer bilinmiyor
    {
      no: 438, yakin: 2.4, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Rasathanenin kesin yeri", "bile bilinmiyor."], sure: 2.36, renk: KIZIL }, // kart 36
      ],
    },
    // 439: Takvim: Sokollu, 11 Ekim 1579
    {
      no: 439, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bir başka okuma", "takvime bakıyor."], sure: 1.77 }, // kart 37
        { satirlar: ["11 Ekim 1579: dönemin güçlü", "sadrazamı Sokollu Mehmed Paşa", "bir suikastla öldürülüyor."], sure: 8.15, renk: KIZIL }, // kart 38
      ],
    },
    // 440: Rasathane yıkılıyor
    {
      no: 440, yakin: 2.2, kamera: 8, yaziY: 240,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Üç ay sonra rasathane", "yıkılıyor.", "Sadrazam gitti,", "bina da mı gitti?"], sure: 3.98, boy: 80, renk: KIZIL }, // kart 39
      ],
    },
    // 441: Boş koltuk
    {
      no: 441, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bağ mı, tesadüf mü?", "Belgesi yok."], sure: 1.91, renk: ALTIN }, // kart 40
      ],
    },
    // 442: Yaşlı Takiyüddin, 1585
    {
      no: 442, yakin: 3.2, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Takiyüddin beş yıl daha", "yaşıyor.", "1585'te İstanbul'da ölüyor."], sure: 4.74, renk: KIZIL }, // kart 41
      ],
    },
    // 443: Makam sürer
    {
      no: 443, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Müneccimbaşılık makamı", "ise sürüyor;", "Osmanlı'da gökyüzüne bakmak", "bitmiyor."], sure: 4.79, renk: ALTIN }, // kart 42
      ],
    },
    // 444: Şehinşâhnâme minyatürü
    {
      no: 444, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Binadan geriye", "bir resim kalıyor."], sure: 2.48 }, // kart 43
        { satirlar: ["Yıkımdan yaklaşık", "bir yıl sonra Şehinşâhnâme'ye", "bir rasathane minyatürü", "çiziliyor."], sure: 5.20 }, // kart 44
      ],
    },
    // 445: Sayfa yakın plan
    {
      no: 445, yakin: 2.8, kamera: 4,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Aletleri bugün en iyi", "orada görüyoruz."], sure: 3.53 }, // kart 45
        { satirlar: ["Bina yok, yer yok;", "kâğıtta bir resim var."], sure: 1.72, renk: ALTIN }, // kart 46
      ],
    },
    // 446: 1597: Tycho Hven'den ayrılır
    {
      no: 446, yakin: 2.4, kamera: 10,
      sprite: { w: 400, h: 300, fps: 10, x: [256, 220], taban: 632 },
      yazilar: [
        { satirlar: ["Peki Tycho?", "Kralı 1588'de ölüyor.", "1597'de adayı terk ediyor."], sure: 6.24 }, // kart 47
      ],
    },
    // 447: Uraniborg yıkılır
    {
      no: 447, yakin: 2.2, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Uraniborg bakımsız kalıyor,", "zamanla yıkılıyor."], sure: 2.92, renk: KIZIL }, // kart 48
      ],
    },
    // 448: Motif: ikisi de yok
    {
      no: 448, yakin: 2.2, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Aynı gökyüzü, iki gözlemevi.", "İkisi de yok."], sure: 2.94, renk: ALTIN }, // kart 49
        { satirlar: ["Biri yirmi bir yıl yaşadı.", "Öbürü üç."], sure: 1.77 }, // kart 50
      ],
    },
    // 449: Son soru
    {
      no: 449, yakin: 2.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sizce Tophane'deki binayı", "yıkan neydi: yıldız mı,", "veba mı, şeyhülislam mı,", "yoksa saraydaki boş koltuk mu?"], sure: 7.67, renk: ALTIN }, // kart 51
      ],
    },
  ],
  kapanis: {
    satirlar: ["Piksel Tarih", "@pikseltarihim"],
    sonraki: "Yorumlara yaz, arkadaşına gönder",
    sure: 3, arka: 449, gece: true,
  },
};

export const TAKIYUDDIN_KARE = Math.round(seriSure(TAKIYUDDIN_SERI) * T_FPS);
export const Takiyuddin: React.FC = () => <SeriVideo seri={TAKIYUDDIN_SERI} />;
