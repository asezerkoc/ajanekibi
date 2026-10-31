import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Defterde Bin Yazıyor: Abdülmecid'in İrlanda Büyük Kıtlığı yardımı, belge ile efsane (1847). Grafikerin tarifi:
   teslimler/gece/ara/irlanda-kitligi/5-grafik.md; sahneler 490-524 (video/piksel/irlanda_kitligi.py).
   Kartlar kalite kontrolün nihai 52 kartıyla harfi harfine aynı; süreler tahmini (seslendirme 245 sn),
   ses/hizala_seri.py sese göre yeniden yazar. Hilal ve yıldız yalnızca efsane (514), mühür (516) ve Kral John (517) sahnelerinde. */
// Kapak: sahne 490 katmanlarıyla yapılan ilk Bolum (2 sn, sessiz); başlık editörün kapak önerisi.
export const IRLANDA_SERI: Seri = {
  etiket: "PİKSEL TARİHİM · İRLANDA KITLIĞI",
  ses: "irlanda-kitligi-anlatim.mp3",
  bolumler: [
    { // KAPAK (hizala_seri bu bloğu atlar: kapak yazıları anlatımda yok)
      no: 490, yakin: 2.8, kamera: 0, yaziY: 270,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Defterde", "Bin Yazıyor", "Bir iyilik nasıl efsane olur?"], sure: 2.0, boy: 112, renk: ALTIN },
      ],
    },
    // İstanbul, saray odası: genç padişah masada bağış kesesini mühürlü kâğıtla gönderir
    {
      no: 490, yakin: 2.8, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bir padişah", "bin lira gönderiyor."], sure: 1.99, renk: ALTIN }, // kart 1
      ],
    },
    // efsane: gece, sisli nehirde üç soluk yelkenli (hayal gibi)
    {
      no: 491, yakin: 2.6, kamera: 10, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bugün anlatılan hikâyede", "ise üç gizli gemi var.", "Bin lira nasıl gemi oluyor?"], sure: 4.90, renk: ALTIN }, // kart 2
      ],
    },
    // defter yakın plan: kâtip kürsüsünde açık defter, mum
    {
      no: 492, yakin: 3.2, kamera: 4, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Oysa defterde", "hâlâ bin yazıyor."], sure: 1.31, renk: ALTIN }, // kart 3
      ],
    },
    // İstanbul, 1847 baharı: saray bahçesinde erguvanlar, padişah yürür; uzakta Boğaz ve camiler
    {
      no: 493, yakin: 2.8, kamera: 10, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 14, x: [258, 284], taban: 632 },
      yazilar: [
        { satirlar: ["İstanbul, 1847 baharı.", "Padişah Abdülmecid", "yirmi üç yaşında."], sure: 5.54 }, // kart 4
        { satirlar: ["On altı yaşından beri tahtta.", "Nisan sonunda", "yirmi dört olacak."], sure: 3.84 }, // kart 5
      ],
    },
    // İstanbul: kahvehane önü, peykede gazete okuyanlar
    {
      no: 494, yakin: 2.8, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["İstanbul gazeteleri", "uzak bir adayı yazıyor:", "İrlanda."], sure: 3.15 }, // kart 6
      ],
    },
    // İrlanda, 1845 sonbaharı: çürüyen patates tarlası, köylü kazar; taş kulübe
    {
      no: 495, yakin: 2.8, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["İrlanda'da patates 1845", "sonbaharından beri çürüyor.", "Ada aç."], sure: 4.82, renk: KIZIL }, // kart 7
      ],
    },
    // göç yolu: bohçalı aile limana yürür; geride damı çökmüş boş kulübe
    {
      no: 496, yakin: 2.6, kamera: 12, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 14, x: [286, 254], taban: 632 },
      yazilar: [
        { satirlar: ["Kıtlık bittiğinde yaklaşık", "bir milyon ölü, bir milyon", "göçmen olacak."], sure: 5.65, renk: KIZIL }, // kart 8
        { satirlar: ["Sekiz milyonluk ada", "altı buçuk milyona inecek."], sure: 2.33, renk: KIZIL }, // kart 9
      ],
    },
    // Londra, Ocak 1847: yardım derneğinin odası, beyefendiler masa başında
    {
      no: 497, yakin: 2.8, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Londra, Ocak 1847.", "Bir yardım derneği kuruluyor."], sure: 4.70 }, // kart 10
      ],
    },
    // Kraliçe Victoria (taç) bağışını kâğıtla uzatır; saray odası
    {
      no: 498, yakin: 3.0, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kraliçe Victoria", "iki bin sterlin veriyor.", "İlk bağışçılardan."], sure: 3.59 }, // kart 11
      ],
    },
    // aynı dernek odası: kâtip deftere yazar
    {
      no: 497, yakin: 2.8, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Dernek sonunda yaklaşık", "dört yüz yetmiş bin", "sterlin toplayacak."], sure: 3.65 }, // kart 12
      ],
    },
    // İstanbul: Osmanlı nazırı bağış kesesini İngiliz elçisi Wellesley'e emanet eder
    {
      no: 499, yakin: 2.8, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Aynı bahar, İstanbul.", "İngiliz elçisi Wellesley'e", "bir bağış emanet ediliyor."], sure: 4.52 }, // kart 13
      ],
    },
    // Londra: kâtip yüksek yazı kürsüsünde deftere yazar
    {
      no: 500, yakin: 3.0, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Gönderen padişah. Tutar: bin.", "Londra defterine", "bin sterlin diye geçiyor."], sure: 5.27 }, // kart 14
      ],
    },
    // Osmanlı kâtibi rahlede kayıt düşer; sedir ve mum
    {
      no: 501, yakin: 3.0, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Osmanlı arşivindeki kayıt", "ise bin lira diyor.", "Sterlin değil, lira."], sure: 3.78 }, // kart 15
      ],
    },
    // iki defter yan yana: deri ciltli İngiliz defteri ve kırmızı ciltli Osmanlı defteri
    {
      no: 502, yakin: 3.2, kamera: 4, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["İki imparatorluk aynı iyiliği", "kendi parasıyla yazıyor."], sure: 3.51, renk: ALTIN }, // kart 16
      ],
    },
    // Dublin, 1847: soylular masada teşekkür mektubunu imzalar
    {
      no: 503, yakin: 2.8, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Dublin, 1847. İrlanda'nın", "soyluları ve beyefendileri", "bir mektup imzalıyor."], sure: 6.92 }, // kart 17
        { satirlar: ["Aç bir ülkenin soyluları,", "genç bir padişaha", "teşekkür ediyor."], sure: 3.59 }, // kart 18
      ],
    },
    // bugün: kütüphane, camlı vitrinde mektup; bir okur bakar
    {
      no: 504, yakin: 2.8, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Mektubun aslı bugün", "İstanbul'da. Sureti Dublin'de,", "Ulusal Kütüphane'de."], sure: 4.32 }, // kart 19
      ],
    },
    // Drogheda, Mayıs 1847: Boyne kıyısında taş rıhtım, karşı kıyıda kasaba
    {
      no: 505, yakin: 2.6, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Drogheda, Mayıs 1847.", "Boyne nehri kıyısında", "bir liman kasabası."], sure: 5.71 }, // kart 20
      ],
    },
    // üç yabancı yelkenli rıhtıma yanaşır; rıhtımda halat bekleyen hamallar
    {
      no: 506, yakin: 2.6, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Üç yabancı gemi yanaşıyor.", "İkisi Selanik'ten, biri", "Prusya'daki Stettin'den."], sure: 4.57 }, // kart 21
      ],
    },
    // rıhtımda tahıl çuvalları, tüccar defteriyle; biri gazete okur
    {
      no: 507, yakin: 2.8, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ambarlarda buğday ve mısır.", "Alıcılar kasabanın", "tüccarları."], sure: 4.21 }, // kart 22
        { satirlar: ["Kasabanın gazeteleri", "\"yabancı gemiler\" yazıyor.", "Padişahın adı yok."], sure: 4.08 }, // kart 23
      ],
    },
    // Selanik limanı: Beyaz Kule, minareler; demirli yelkenli
    {
      no: 508, yakin: 2.6, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Selanik ise o yıllarda", "bir Osmanlı limanı.", "Bu üç gemiyi aklınızda tutun."], sure: 4.38, renk: ALTIN }, // kart 24
      ],
    },
    // New York, 1849: tuğla binalar, gazete satan çocuk
    {
      no: 509, yakin: 2.8, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["New York, 21 Temmuz 1849.", "Olaydan iki yıl sonra,", "okyanusun öbür yakası."], sure: 6.76 }, // kart 25
      ],
    },
    // basımhane: demir el baskı makinesi, baskıcı kolu çeker, çırak kâğıt alır
    {
      no: 510, yakin: 2.8, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Albion gazetesi yazıyor:", "Padişah başta on bin sterlin", "ve erzak gemileri önermişti."], sure: 5.21 }, // kart 26
      ],
    },
    // rivayet: aynı salonda elçi elini kaldırıp araya girer
    {
      no: 499, yakin: 2.8, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Rivayete göre İngiliz elçisi", "araya girmiş:", "Kimse Kraliçe'yi geçemez."], sure: 4.58 }, // kart 27
      ],
    },
    // gece: defterin üstünde katlanmış gazete, mum
    {
      no: 511, yakin: 3.2, kamera: 4, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["On bin, 1847 belgelerinde yok.", "Defterde bin yazıyor.", "Ama hikâye artık yolda."], sure: 5.54, renk: KIZIL }, // kart 28
      ],
    },
    // Londra, 1851: yazar masasında biyografiyi yazar; kitap yığını
    {
      no: 512, yakin: 2.8, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["1851'de Londra'da eski", "Başbakan Peel'in", "biyografisine giriyor."], sure: 5.46 }, // kart 29
      ],
    },
    // Drogheda, yıllar sonra: kasaba sokağında kasketli adamlar konuşur
    {
      no: 513, yakin: 2.8, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Drogheda, yıllar sonra.", "Kasabada başka bir hikâye", "dolaşıyor."], sure: 3.83 }, // kart 30
      ],
    },
    // efsane: soluk üç gemi gece nehirde
    {
      no: 491, yakin: 2.6, kamera: 10, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Efsaneye göre o üç gemi", "padişahındı, gizlice gelmişti;"], sure: 3.09 }, // kart 31
      ],
    },
    // efsane: kasaba kapısında hilal ve yıldızlı kalkan (soluk, hayal gibi)
    {
      no: 514, yakin: 2.6, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["kasaba da teşekkür için", "armasına hilal ve yıldız", "koymuştu."], sure: 4.14 }, // kart 32
      ],
    },
    // 1844: tarihçi D'Alton masasında kitabını yazar
    {
      no: 515, yakin: 2.8, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ama hilal ve yıldız", "yardımdan üç yıl önce", "bir kitapta zaten var."], sure: 3.45, renk: KIZIL }, // kart 33
      ],
    },
    // mühür yakın planı: kürsüde belge, kırmızı balmumu mühürde hilal ve yıldız
    {
      no: 516, yakin: 3.2, kamera: 4, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["1844. Tarihçi D'Alton", "belediye başkanının mührünü", "yazıyor: hilal ve yıldız."], sure: 6.54 }, // kart 34
      ],
    },
    // 13. yüzyıl: Kral John taçlı, eski armalı sancak ve kalkan; taş kale
    {
      no: 517, yakin: 2.6, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Arma uzmanları onu İngiltere", "Kralı John'un nişanına", "bağlıyor: on üçüncü yüzyıl."], sure: 5.28 }, // kart 35
        { satirlar: ["Yardımdan yaklaşık", "altı yüz yıl önce."], sure: 2.29, renk: ALTIN }, // kart 36
      ],
    },
    // arşiv: boş raflar, fenerle arayan arşivci
    {
      no: 518, yakin: 2.8, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Peki gemiler için belge?", "Türk, İrlanda arşivleri: yok.", "Drogheda liman kayıtları: yok."], sure: 5.08, renk: KIZIL }, // kart 37
      ],
    },
    // yerel tarihçi kitaplarla dolu odasında; elinde açık kitap
    {
      no: 519, yakin: 2.8, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kasabanın bir tarihçisi", "padişahın gemilerini", "olası buluyor."], sure: 4.43 }, // kart 38
        { satirlar: ["O bile belge olmadığını", "kabul ediyor.", "Hikâye yine de durmuyor."], sure: 3.43, renk: KIZIL }, // kart 39
      ],
    },
    // Drogheda, 1995: West Street'te otel cephesi, plaket; belediye başkanı ve büyükelçi
    {
      no: 520, yakin: 2.8, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Drogheda, 2 Mayıs 1995.", "West Street'te bir plaket", "açılıyor."], sure: 6.11 }, // kart 40
        { satirlar: ["Belediye başkanı ve Türk", "büyükelçisi yan yana."], sure: 3.32 }, // kart 41
        { satirlar: ["Plaket, Türk halkının", "cömertliğini anıyor."], sure: 2.57 }, // kart 42
      ],
    },
    // Ankara, 2010: resmî yemek, uzun masa; Cumhurbaşkanı ayakta konuşur
    {
      no: 521, yakin: 2.8, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ankara, 23 Mart 2010.", "İrlanda Cumhurbaşkanı Mary", "McAleese resmî bir yemekte."], sure: 6.89 }, // kart 43
        { satirlar: ["Üç gemi dolusu yiyeceği", "ve armayı anlatıyor."], sure: 3.16 }, // kart 44
      ],
    },
    // ertesi gün: ofiste basın görevlisi düzeltme metnini okur
    {
      no: 522, yakin: 3.0, kamera: 6, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ertesi gün ofisi düzeltiyor:", "Arma bağı doğru görünmüyor.", "İddia ancak bir gün dayanıyor."], sure: 5.26, renk: KIZIL }, // kart 45
      ],
    },
    // 1861: boş taht, sönmeye yüz tutmuş şamdanlar
    {
      no: 523, yakin: 2.8, kamera: 4, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Peki padişah?", "1861'de veremden ölüyor.", "Otuz sekiz yaşında."], sure: 5.73, renk: KIZIL }, // kart 46
        { satirlar: ["İyiliği onsuz", "büyümeye devam ediyor.", "Her anlatımda biraz daha."], sure: 3.93 }, // kart 47
      ],
    },
    // belgeler masası: defter, teşekkür mektubu ve mühür
    {
      no: 524, yakin: 3.2, kamera: 4, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Belge ne diyor? Bin lira.", "Kraliçe'nin iki bini.", "Bir teşekkür mektubu."], sure: 4.45 }, // kart 48
        { satirlar: ["Mektup bin sterline", "teşekkür ediyor.", "Gemilere değil."], sure: 3.08, renk: ALTIN }, // kart 49
      ],
    },
    // Drogheda: kasaba sokağı (hikâye eklenir)
    {
      no: 513, yakin: 2.8, kamera: 8, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Gerisini iki yıl sonra bir", "gazete, yıllar sonra bir", "kasaba ekliyor."], sure: 4.50 }, // kart 50
      ],
    },
    // defter yakın plan (motif)
    {
      no: 492, yakin: 3.2, kamera: 4, yaziY: 250,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Defterde hâlâ bin yazıyor."], sure: 1.11, renk: ALTIN }, // kart 51
      ],
    },
    // efsanenin üç gemisi soluklaşır
    {
      no: 491, yakin: 2.6, kamera: 10, yaziY: 250,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sizce hangisi daha uzun yaşar:", "belgedeki bin lira mı,", "efsanedeki üç gemi mi?"], sure: 5.95, renk: ALTIN }, // kart 52
      ],
    },
  ],
  kapanis: {
    satirlar: ["Piksel Tarih", "@pikseltarihim"],
    sonraki: "Yorumlara yaz, arkadaşına gönder",
    sure: 3, arka: 491, gece: true,
  },
};

export const IRLANDA_KARE = Math.round(seriSure(IRLANDA_SERI) * T_FPS);
export const IrlandaKitligi: React.FC = () => <SeriVideo seri={IRLANDA_SERI} />;
