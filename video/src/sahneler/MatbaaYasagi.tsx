import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Fermanı Gören Yok: Osmanlı'da "matbaa yasağı" efsanesi ve İbrahim Müteferrika (1584-1747, bugün). Grafikerin tarifi
   (teslimler/gece/ara/matbaa-yasagi/5-grafik.md), sahneler 170-209 (video/piksel/matbaa_yasagi.py).
   Kartlar 4-kalite-metin.md "Nihai ekran kartları" ile harfi harfine aynı ve aynı sırada (49 kart).
   Süreler tahmini (harf/14 + 0,4 sn; yavaş kartlara +0,8 sn); ses/hizala_seri.py sese göre yeniden yazar.
   Bu dosya piksel betiğinin de tek kaynağıdır: matbaa_yasagi.py yakin/sprite/yazı değerlerini buradan okur
   ve figürlerin yazı bandına girmediğini denetler. 4 satırlı kartlar boy 72 ile küçültülür (figür başlarının üstünde kalsın). */
// Kapak: ajans sahibi görsel vermedi. Kapak, sahne 170 katmanlarıyla yapılan ilk Bolum'dür (2 sn, sessiz).
export const MATBAA_SERI: Seri = {
  etiket: "PİKSEL TARİHİM · MATBAA YASAĞI",
  ses: "matbaa-yasagi-anlatim.mp3",
  bolumler: [
    { // KAPAK
      no: 170, yakin: 2.6, kamera: 0,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Matbaa", "Yasağı", "Fermanı gören yok"], sure: 2.0, boy: 112, renk: ALTIN },
      ],
    },
    // 170: Paris, 1584, gece: Thevet masasında yazıyor (yakın)
    {
      no: 170, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Basılı kitap kullanana", "ölüm cezası."], sure: 2.83, renk: KIZIL }, // kart 1
        { satirlar: ["Matbaa yasağı hikâyesinin", "bilinen en eski kaynağı", "bu cümle."], sure: 4.47 }, // kart 2
      ],
    },
    // 171: Motif: boş rahle, kandil (fermanı gören yok)
    {
      no: 171, yakin: 3.0, kamera: 4,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ama bu cezayı koyan", "fermanı gören yok."], sure: 3.84, renk: ALTIN }, // kart 3
      ],
    },
    // 172: Paris, 1584: Thevet'in çalışma odası (geniş)
    {
      no: 172, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Paris, 1584.", "André Thevet masasında", "Gutenberg'i yazıyor."], sure: 4.26 }, // kart 4
      ],
    },
    // 173: Thevet'in sayfası: yanında açık Gutenberg kitabı; iddia onun kaleminden
    {
      no: 173, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Araya bu cezayı sıkıştırıyor:", "İkinci Bayezid 1483'te koymuş,", "Yavuz Selim onaylamış."], sure: 6.19 }, // kart 5
      ],
    },
    // 174: 1550'ler, İstanbul: gezgin Thevet yürüyor
    {
      no: 174, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 16, x: [235, 305], taban: 632 },
      yazilar: [
        { satirlar: ["Thevet Osmanlı ülkesini", "gezmiş ama fermanı görmemiş."], sure: 4.04 }, // kart 6
      ],
    },
    // 175: Bugün, İstanbul: rehber anlatıyor
    {
      no: 175, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bugün bile deniyor:", "\"Osmanlı matbaayı", "270 yıl yasakladı.\""], sure: 4.33 }, // kart 7
        { satirlar: ["Koca bir medeniyete tek damga:", "kitaptan korktu."], sure: 3.69, renk: KIZIL }, // kart 8
        { satirlar: ["Peki doğru mu?"], sure: 2.20, renk: ALTIN }, // kart 9
      ],
    },
    // 176: İstanbul, 13 Aralık 1493: Nahmias kardeşlerin tahta presi
    {
      no: 176, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["İstanbul, 13 Aralık 1493.", "İspanya'dan sürülmüş", "Nahmias kardeşler tezgâhta."], sure: 5.54 }, // kart 10
        { satirlar: ["İbranice bir din hukuku", "kitabı basıyorlar.", "Son sayfaya günü yazıyorlar."], sure: 5.33 }, // kart 11
      ],
    },
    // 177: Basılmış sayfalar ipte kuruyor, kitap yığını
    {
      no: 177, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Thevet'in yasağından", "on yıl sonra.", "Yasak varsa bu kitap", "nasıl basıldı?"], sure: 5.19, boy: 72, renk: KIZIL }, // kart 12
      ],
    },
    // 178: 1567: kilisede Abgar ve oğlu baskıda
    {
      no: 178, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["1567. Ermeni usta Abgar", "Venedik'ten tezgâh getiriyor.", "İstanbul'da bir kilisede", "oğluyla basıyor."], sure: 6.97, boy: 72 }, // kart 13
      ],
    },
    // 179: 1588: III. Murad fermanı veriyor
    {
      no: 179, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["1588. Üçüncü Murad'ın fermanı:", "Avrupa'da basılan, dinî", "olmayan Arap harfli kitaplar", "satılabilir."], sure: 7.04, boy: 72 }, // kart 14
      ],
    },
    // 180: Roma baskısı Öklid, 453. sayfa: izin fermanı (yakın)
    {
      no: 180, yakin: 3.0, kamera: 4,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ferman bugün elimizde.", "Nerede?"], sure: 2.47 }, // kart 15
        { satirlar: ["Roma'da basılmış bir Öklid'in", "453. sayfasında."], sure: 3.61, renk: ALTIN }, // kart 16
      ],
    },
    // 181: Motif: boş rahle ve Öklid
    {
      no: 181, yakin: 2.8, kamera: 4,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Yasak fermanını gören yok.", "İzin fermanı ise bir geometri", "kitabının içinde duruyor."], sure: 6.91, renk: ALTIN }, // kart 17
      ],
    },
    // 182: 1627, Pera: Metaksas kiralık evde basıyor
    {
      no: 182, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["1627. Londra'dan gelen", "Rum rahip Metaksas", "Pera'da kiralık evde basıyor."], sure: 5.33 }, // kart 18
      ],
    },
    // 183: Ocak 1628, Pera: kış gecesi, makamlar kapıda
    {
      no: 183, yakin: 2.6, kamera: 6, hava: 10,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ocak 1628:", "makamlar matbaayı kapatıyor."], sure: 3.11, renk: KIZIL }, // kart 19
      ],
    },
    // 184: Cizvitlerin kışkırtması: mektup el değiştiriyor
    {
      no: 184, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Yasak bu mu? Hayır.", "Arkasında Cizvitlerin", "kışkırtması var."], sure: 4.40, renk: ALTIN }, // kart 20
      ],
    },
    // 185: 1679, İstanbul: Marsigli yürüyor
    {
      no: 185, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 16, x: [235, 305], taban: 632 },
      yazilar: [
        { satirlar: ["1679. Bolognalı Marsigli", "aylarca İstanbul'da kalıyor."], sure: 4.11 }, // kart 21
      ],
    },
    // 186: Marsigli masasında yazıyor
    {
      no: 186, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Sonra yazıyor: Türkler", "basmıyor, ama yasak", "yüzünden değil."], sure: 4.40 }, // kart 22
      ],
    },
    // 187: Kopyacılar rahle başında
    {
      no: 187, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ona göre sebep: bu işten", "geçinen kopyacılar."], sure: 3.47 }, // kart 23
      ],
    },
    // 188: İki masa: Paris'te yazan, İstanbul'da yaşamış olan
    {
      no: 188, yakin: 2.6, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Yasak diyen, Paris'te", "yazıyordu. Yasak yok diyen,", "İstanbul'da yaşamıştı."], sure: 5.40 }, // kart 24
      ],
    },
    // 189: Alacakaranlıkta yolda tek bir adam: onu izleyin
    {
      no: 189, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 16, x: [230, 305], taban: 632 },
      yazilar: [
        { satirlar: ["Asıl soru: Müslüman Osmanlılar", "neden 1729'a kadar", "kendi kitaplarını basmadı?", "Cevap için bir adamı izleyin."], sure: 7.76, boy: 72, renk: ALTIN }, // kart 25
      ],
    },
    // 190: Kolozsvár, 1670'ler: beşik
    {
      no: 190, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kolozsvár, Erdel, 1670'ler.", "Bir Macar çocuk doğuyor."], sure: 4.04 }, // kart 26
      ],
    },
    // 191: Genç adam İstanbul'a geliyor
    {
      no: 191, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 16, x: [235, 305], taban: 632 },
      yazilar: [
        { satirlar: ["Yıllar sonra İstanbul'a", "geliyor, Müslüman oluyor.", "Adı artık İbrahim."], sure: 5.11 }, // kart 27
      ],
    },
    // 192: Saray kapısı: müteferrika İbrahim
    {
      no: 192, yakin: 2.6, kamera: 6,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Saraydaki unvanı: müteferrika.", "Tarih onu bu adla tanıyor:", "İbrahim Müteferrika."], sure: 5.83, renk: ALTIN }, // kart 28
      ],
    },
    // 193: 1726: sadrazama risale
    {
      no: 193, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["1726. Sadrazama bir risale:", "basılı kitabın faydaları."], sure: 4.11 }, // kart 29
      ],
    },
    // 194: Paris, 1720: genç Said matbaayı izliyor
    {
      no: 194, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ortağı genç Said Efendi", "elçi babasıyla Paris'te", "matbaaları görmüş."], sure: 4.97 }, // kart 30
      ],
    },
    // 195: Şeyhülislamın fetvası: olur
    {
      no: 195, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Şeyhülislamın fetvası:", "\"olmaz\" değil, \"olur\".", "Sözlük, mantık, astronomi.", "Yalnız dinî kitaplar dışarıda."], sure: 8.34, boy: 72, renk: ALTIN }, // kart 31
      ],
    },
    // 196: Temmuz 1727: III. Ahmed'in beratı
    {
      no: 196, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Temmuz 1727.", "Üçüncü Ahmed'in beratı.", "Bir şart daha: dört düzeltmen", "her sayfayı okuyacak."], sure: 6.47, boy: 72 }, // kart 32
      ],
    },
    // 197: 16 Aralık 1727: Yavuz Selim semti, İbrahim'in evinde tezgâhlar
    {
      no: 197, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["16 Aralık 1727.", "Yavuz Selim semti,", "İbrahim'in evi.", "Tezgâhlar çalışmaya başlıyor."], sure: 5.90, boy: 72 }, // kart 33
      ],
    },
    // 198: 31 Ocak 1729: iki ciltlik Vankulu, ilk sayfada ferman (yakın)
    {
      no: 198, yakin: 3.0, kamera: 4,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["31 Ocak 1729. İlk kitap:", "iki ciltlik sözlük,", "Vankulu Lügati."], sure: 4.54, renk: ALTIN }, // kart 34
        { satirlar: ["İlk sayfalarında", "padişahın fermanı", "ve fetvalar var."], sure: 3.90 }, // kart 35
      ],
    },
    // 199: Pres kendi iznini basıyor: tuğralı sayfa
    {
      no: 199, yakin: 3.0, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Matbaa ilk iş", "kendi iznini basıyor."], sure: 3.63, renk: ALTIN }, // kart 36
      ],
    },
    // 200: Hattatlar rahle başında
    {
      no: 200, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kaynaklara göre hattatlar", "karşı çıkıyor.", "İbrahim yine de basıyor.", "On üç yılda on yedi kitap."], sure: 6.76, boy: 72 }, // kart 37
      ],
    },
    // 201: Târîh-i Hind-i Garbî: tahta baskı resim (yakın)
    {
      no: 201, yakin: 3.0, kamera: 4,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Biri Amerika'yı anlatan tarih:", "13 resimle, Türkçe basılan", "ilk resimli kitap."], sure: 5.69 }, // kart 38
      ],
    },
    // 202: 1742: tezgâhlar susuyor
    {
      no: 202, yakin: 2.8, kamera: 4,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["1742'de son kitap.", "Tezgâhlar susuyor.", "Neden? Belgeler söylemiyor."], sure: 4.90, renk: KIZIL }, // kart 39
      ],
    },
    // 203: 1745, Yalova: kâğıthane, yaşlı İbrahim ve Lehistanlı usta
    {
      no: 203, yakin: 2.4, kamera: 8,
      sprite: { w: 400, h: 230, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["1745. Yetmişini aşmış İbrahim", "Yalova'da kâğıthane kuruyor.", "Lehistan'dan usta getirtiyor.", "Hâlâ uğraşıyor."], sure: 7.61, boy: 72 }, // kart 40
      ],
    },
    // 204: 1 Nisan 1747: depoda miras dökümü
    {
      no: 204, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["1 Nisan 1747, miras dökümü:", "2.981 satılmamış kitap."], sure: 4.77, renk: KIZIL }, // kart 41
      ],
    },
    // 205: Tozlanan raflar
    {
      no: 205, yakin: 2.8, kamera: 4,
      sprite: { w: 400, h: 300, fps: 6, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kolozsvár'dan gelen adamdan", "geriye kalan:", "tozlanan raflar."], sure: 5.20, renk: KIZIL }, // kart 42
      ],
    },
    // 206: Bugün: arşivde Kathryn Schwartz
    {
      no: 206, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["İşte cevap. Tarihçi", "Kathryn Schwartz", "Osmanlı fermanlarını tarıyor."], sure: 4.97 }, // kart 43
        { satirlar: ["2017'de yazıyor:", "böyle bir ferman bulamadı.", "Fermanı gören yok."], sure: 5.49, renk: ALTIN }, // kart 44
      ],
    },
    // 207: Sahaf tezgâhı: kopyacı satıyor, alıcı az
    {
      no: 207, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Belgeler başka şey anlatıyor:", "kopyacılar geçiniyordu,", "alıcı azdı, kutsal metne", "dokunulmuyordu."], sure: 6.90, boy: 72 }, // kart 45
      ],
    },
    // 208: Şafak: kitaplarını alan bir alıcı yürüyor (erken gelen)
    {
      no: 208, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 16, x: [235, 305], taban: 632 },
      yazilar: [
        { satirlar: ["Sabev'in hesabı: her on", "nüshadan yaklaşık yedisi", "satılmış."], sure: 4.40, renk: ALTIN }, // kart 46
        { satirlar: ["İbrahim sadece", "erken gelmişti."], sure: 2.47, renk: ALTIN }, // kart 47
      ],
    },
    // 209: Üç belge yan yana: tek paragraf, Öklid'deki ferman, sözlükteki fetva
    {
      no: 209, yakin: 2.4, kamera: 4,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Paris'te tek paragraf.", "Öklid'in içinde ferman,", "sözlüğün başında fetva."], sure: 5.26 }, // kart 48
        { satirlar: ["Siz bu yasağı", "ilk kimden duydunuz?"], sure: 3.56, renk: ALTIN }, // kart 49
      ],
    },
  ],
  kapanis: {
    satirlar: ["Piksel Tarih", "@pikseltarihim"],
    sonraki: "Yorumlara yaz, arkadaşına gönder",
    sure: 3, arka: 209, gece: true,
  },
};

export const MATBAA_KARE = Math.round(seriSure(MATBAA_SERI) * T_FPS);
export const MatbaaYasagi: React.FC = () => <SeriVideo seri={MATBAA_SERI} />;
