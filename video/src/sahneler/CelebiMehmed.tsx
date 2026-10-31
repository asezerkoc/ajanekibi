import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Paris'teki Elçi: Yirmisekiz Çelebi Mehmed Efendi'nin Paris sefareti (1720-21). Grafikerin tarifi:
   teslimler/gece/ara/celebi-mehmed-paris/5-grafik.md; sahneler 290-321 (video/piksel/celebi_mehmed_paris.py).
   Kartlar kalite kontrolün nihai 45 kartıyla harfi harfine aynı; süreler tahmini (seslendirme 241 sn),
   ses/hizala_seri.py sese göre yeniden yazar. */
// Kapak: sahne 290 katmanlarıyla yapılan ilk Bolum (2 sn, sessiz); logo ve @pikseltarihim alt bandını kapak bileşeni ekler.
export const CELEBI_MEHMED_SERI: Seri = {
  etiket: "PİKSEL TARİHİM · ÇELEBİ MEHMED",
  ses: "celebi-mehmed-paris-anlatim.mp3",
  bolumler: [
    { // KAPAK (hizala_seri bu bloğu atlar: kapak yazıları anlatımda yok)
      no: 290, yakin: 2.6, kamera: 0,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Paris'teki", "Elçi", "Bak, öğren, anlat"], sure: 2.0, boy: 112, renk: ALTIN },
      ],
    },
    // Toulon limanı, 1720 sonu: rıhtımda elçi ve Said, geride demirli gemi
    {
      no: 290, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Toulon limanı, 1720'nin sonu.", "Osmanlı elçisi karantinada.", "Paris'e gidemiyor."], sure: 5.97 }, // kart 1
      ],
    },
    // veba: çitle kapalı yol, nöbetçi; şehirden duman
    {
      no: 291, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Dışarıda veba var.", "Fransa'nın güneyi ölüyor."], sure: 3.46, renk: KIZIL }, // kart 2
      ],
    },
    // elçi minderde yazar: bak, öğren, anlat
    {
      no: 292, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Görevi üç kelimeye sığıyor:", "bak, öğren, anlat."], sure: 3.61, renk: ALTIN }, // kart 3
      ],
    },
    // İstanbul sarayı: sadrazam ve padişah, arkada taht
    {
      no: 293, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Onu gönderenler bir sadrazam", "ve bir padişah. On yıl içinde", "ikisi de yerinde olmayacak."], sure: 6.76, renk: KIZIL }, // kart 4
      ],
    },
    // Pasarofça 1718: barış çadırları ve murahhaslar
    {
      no: 294, yakin: 2.8, kamera: 10,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Neden gönderildi? 1718,", "Pasarofça. Osmanlı, Habsburg", "ve Venedik'le barış imzalar."], sure: 6.36 }, // kart 5
      ],
    },
    // divanhane: sadrazam kâğıtlarıyla, elçi talimat dinler
    {
      no: 295, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Barış dönemi başlar. Sadrazam", "Damat İbrahim Paşa'nın derdi", "artık asker değil, bilgi."], sure: 6.60, renk: ALTIN }, // kart 6
        { satirlar: ["Fransa'nın kalelerini,", "ordusunu, fabrikalarını,", "âdetlerini gör ve yaz."], sure: 5.50 }, // kart 7
      ],
    },
    // Bonnac, Boğaz'a bakan odada
    {
      no: 296, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["İstanbul'daki Fransız elçisi", "Bonnac da bu yolculuğu", "istiyor."], sure: 4.71 }, // kart 8
      ],
    },
    // İstanbul rıhtımı: baba ve oğul gemiye yürür
    {
      no: 297, yakin: 2.8, kamera: 10,
      sprite: { w: 400, h: 220, fps: 16, x: [290, 262], taban: 632 },
      yazilar: [
        { satirlar: ["Elçi, Yirmisekiz Çelebi Mehmed", "Efendi. Lakabı yeniçerilerin", "yirmi sekizinci ortasından."], sure: 6.83 }, // kart 9
        { satirlar: ["Yanında oğlu Said. O da", "bakacak, o da öğrenecek.", "Onları veba karşılar."], sure: 5.50, renk: KIZIL }, // kart 10
      ],
    },
    // Marsilya: damlardan duman, boş yol
    {
      no: 298, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Marsilya'da salgın başlamış.", "Provence'ta tahminen yüz bin", "kişi ölecek."], sure: 5.50, renk: KIZIL }, // kart 11
      ],
    },
    // Toulon karantinası: soğuk oda, elçi yazar
    {
      no: 299, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Heyet Toulon'da tutulur.", "Karantina. Elçi bekler.", "Bakar, öğrenir, yazar."], sure: 5.58, renk: ALTIN }, // kart 12
      ],
    },
    // Paris, Mart 1721: kalabalık sokakta atlı elçi ve Said
    {
      no: 300, yakin: 2.8, kamera: 12,
      sprite: { w: 400, h: 220, fps: 16, x: [250, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Mart 1721. Paris.", "Sefaretname'ye göre", "şehir onu görmeye koşar."], sure: 4.87 }, // kart 13
      ],
    },
    // elçi atının üstünde defterini tutar
    {
      no: 301, yakin: 3.0, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bunu yazan, elçinin kendisi.", "Türk modası Paris için", "yeni değil."], sure: 4.95 }, // kart 14
      ],
    },
    // Molière'in sahnesi: 'Türk' kılığında oyuncu
    {
      no: 302, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Molière elli yıl önce", "sahneye koymuştu. Şimdi", "sokaklarda yeniden alevlenir."], sure: 5.89 }, // kart 15
      ],
    },
    // Tuileries cephesi, alacakaranlık: heyet saraya yürür
    {
      no: 303, yakin: 2.8, kamera: 10,
      sprite: { w: 400, h: 220, fps: 16, x: [255, 285], taban: 632 },
      yazilar: [
        { satirlar: ["Resmî kabul. Versailles'ı mı", "bekliyorsun? Hayır. Saray", "Paris'te, Tuileries'de."], sure: 6.13, renk: ALTIN }, // kart 16
        { satirlar: ["Versailles'a ancak 1722'de", "dönecek. Tuileries bugün yok;", "1871'de yanacak."], sure: 5.73, renk: KIZIL }, // kart 17
      ],
    },
    // taht salonu: tahtta çocuk kral, karşısında elçi
    {
      no: 304, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Elçi salona girer. Karşısında", "Fransa Kralı On Beşinci Louis.", "On bir yaşında."], sure: 5.97, renk: ALTIN }, // kart 18
      ],
    },
    // geniş plan: naip, tahtta kral, elçi ve Said
    {
      no: 305, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ülkeyi onun adına naip", "Philippe d'Orléans yönetiyor."], sure: 4.08 }, // kart 19
        { satirlar: ["Koca imparatorluğun sözcüsü,", "bir çocuğun karşısında", "duruyor."], sure: 4.71, renk: ALTIN }, // kart 20
      ],
    },
    // Palais-Royal operası: sahnede iki şarkıcı, önde elçi
    {
      no: 306, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Sonra Paris'i gezer.", "Palais-Royal'de", "opera seyreder."], sure: 4.08 }, // kart 21
      ],
    },
    // Paris Rasathanesi, gece: dürbün ve çeyrek daire
    {
      no: 307, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Yarım asırlık Paris", "Rasathanesi'nde gökyüzünü", "ölçen aletleri görür."], sure: 5.26 }, // kart 22
      ],
    },
    // Versailles bahçeleri: fıskiyeli havuz, elçi not alır
    {
      no: 308, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Versailles'a da gider;", "elçi olarak değil,", "gezgin olarak."], sure: 4.40 }, // kart 23
        { satirlar: ["Bahçeler, havuzlar, çeşmeler.", "Sefaretname bunları", "sayfalarca anlatır."], sure: 5.42 }, // kart 24
      ],
    },
    // bir rapor: 292'deki yazı odasına dönüş
    {
      no: 292, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bir Batılılaşma planı", "değil bu. Bir rapor.", "Bak, öğren, anlat."], sure: 4.79, renk: ALTIN }, // kart 25
      ],
    },
    // Kâğıthane 1722: iskeleli köşk, işçiler
    {
      no: 309, yakin: 2.8, kamera: 10,
      sprite: { w: 400, h: 220, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["1722. İstanbul.", "Kâğıthane'de Sâdâbâd Kasrı", "ve bahçesi yükseliyor."], sure: 5.11 }, // kart 26
      ],
    },
    // mesire: çadırlar, havuz, laleler; elçi kıyıda
    {
      no: 310, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Elçi daha yeni dönmüştür.", "Paris bahçelerinin izi mi?"], sure: 4.08, renk: ALTIN }, // kart 27
        { satirlar: ["Tarihçiler bunu tartışıyor;", "Osmanlı'nın mesire geleneği", "zaten köklü."], sure: 5.34 }, // kart 28
      ],
    },
    // ferman ve fetva: şeyhülislam ve kâtip
    {
      no: 311, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["1727. Padişahın yazılı onayı,", "şeyhülislamın fetvası:", "matbaaya izin çıkar."], sure: 5.73 }, // kart 29
      ],
    },
    // üç baskı tezgâhı ve baskıcıları
    {
      no: 312, yakin: 2.6, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Osmanlı'da matbaa zaten var.", "Yahudi, Ermeni, Rum matbaaları", "yüz yıllardır çalışıyor."], sure: 6.60 }, // kart 30
      ],
    },
    // Müteferrika tezgâhın kolunu çeker
    {
      no: 313, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Yeni olan, Müslümanlar için", "Türkçe basan bir matbaa.", "Kurucusu İbrahim Müteferrika."], sure: 6.44, renk: ALTIN }, // kart 31
      ],
    },
    // Said belgeyle, Müteferrika ilk sayfayla; masada kitaplar
    {
      no: 314, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["İzin sürecinde bir ad", "daha geçer: Said.", "Paris'e babasıyla giden oğul."], sure: 5.42 }, // kart 32
        { satirlar: ["1729'da ilk kitap basılır:", "Vankulu Lügati. Said, Paris'te", "gördüğü için mi destekledi?"], sure: 6.68, renk: ALTIN }, // kart 33
      ],
    },
    // boş raf, tek mum; elçi pencereye dönük (orta yaşlı)
    {
      no: 315, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bunu kanıtlayan bir belge yok.", "Elçi görevini yapmıştır.", "Baktı, öğrendi, anlattı."], sure: 6.28, renk: ALTIN }, // kart 34
      ],
    },
    // Patrona 1730: meşaleli kalabalık, ateş
    {
      no: 316, yakin: 2.8, kamera: 12,
      sprite: { w: 400, h: 220, fps: 16, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ama. Eylül 1730.", "Patrona Halil ayaklanır."], sure: 3.22, renk: KIZIL }, // kart 35
      ],
    },
    // boş taht, devrilmiş kavuk; ölüm gösterilmez
    {
      no: 317, yakin: 2.8, kamera: 4,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Onu gönderen sadrazam", "Damat İbrahim Paşa", "öldürülür."], sure: 4.01, renk: KIZIL }, // kart 36
        { satirlar: ["Onu gönderen padişah, matbaaya", "izin veren Üçüncü Ahmed,", "tahttan indirilir."], sure: 5.81, renk: KIZIL }, // kart 37
      ],
    },
    // solan laleler; elçi sola uzaklaşır
    {
      no: 318, yakin: 2.8, kamera: 10,
      sprite: { w: 400, h: 220, fps: 14, x: [290, 250], taban: 632 },
      yazilar: [
        { satirlar: ["Sonradan Lale Devri denecek", "dönem kapanır.", "On iki yıl sürmüştür."], sure: 5.03 }, // kart 38
        { satirlar: ["Peki elçi? Ne zaman, nerede", "öldü? Kaynaklar ayrışıyor."], sure: 4.24, renk: ALTIN }, // kart 39
      ],
    },
    // kitapçı: iki masa, iki kitap yığını
    {
      no: 319, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bildiğimiz şu: Paris'i", "anlattığı kitap 1757'de", "Fransızcaya çevrilir."], sure: 5.34 }, // kart 40
        { satirlar: ["İstanbul'da basılması için", "1866'yı bekler. Fransa onu", "yüz küsur yıl önce basmıştı."], sure: 6.44, renk: ALTIN }, // kart 41
      ],
    },
    // 1742: Said aynı Paris sokağında yalnız atlı
    {
      no: 320, yakin: 2.8, kamera: 12,
      sprite: { w: 400, h: 220, fps: 18, x: [250, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Bir iz daha var. 1742.", "Paris'e bir Osmanlı", "elçisi daha gelir. Adı Said."], sure: 5.58, renk: ALTIN }, // kart 42
        { satirlar: ["Yirmi bir yıl önce babasının", "yanında yürüdüğü yolu,", "bu kez tek başına yürür."], sure: 5.97 }, // kart 43
      ],
    },
    // Said minderde yazar; soru ekranda
    {
      no: 321, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bakar, öğrenir, anlatır.", "Bir elçinin gördükleri bir", "imparatorluğu değiştirir mi?"], sure: 6.28, renk: ALTIN }, // kart 44
        { satirlar: ["Yoksa onu gönderenlerle", "birlikte mi unutulur?", "Sen ne dersin?"], sure: 4.71, renk: ALTIN }, // kart 45
      ],
    },
  ],
  kapanis: {
    satirlar: ["Piksel Tarih", "@pikseltarihim"],
    sonraki: "Yorumlara yaz, arkadaşına gönder",
    sure: 3, arka: 321, gece: true,
  },
};

export const CELEBI_MEHMED_KARE = Math.round(seriSure(CELEBI_MEHMED_SERI) * T_FPS);
export const CelebiMehmed: React.FC = () => <SeriVideo seri={CELEBI_MEHMED_SERI} />;
