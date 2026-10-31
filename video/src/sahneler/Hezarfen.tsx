import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Kalması Uygun Değil: Hezarfen Ahmed Çelebi'nin uçuşu (tek kaynak Evliya Çelebi). Grafikerin tarifi:
   teslimler/gece/ara/hezarfen/5-grafik.md; sahneler 370-406 (video/piksel/hezarfen.py), 47 kart 4-kalite-metin.md'den
   harfi harfine. Süreler tahmini (≈13 harf/sn); ses/hizala_seri.py sese göre yeniden yazar. Sahne 370 üç kez kullanılır:
   kapak, kanca (kart 1) ve "Peki Hezarfen gerçekten uçtu mu?" (kart 37) dönüşü. Yön dili: sağ = Üsküdar / lodos,
   sol = batı / sürgün. */
export const HEZARFEN_SERI: Seri = {
  etiket: "PİKSEL TARİHİM · HEZARFEN",
  ses: "hezarfen-anlatim.mp3",
  bolumler: [
    // Kapak: sahne 370 katmanları, başlık (2 satır) + alt başlık (ana motif, ALTIN). Hizalama bu bloğu atlar.
    { // KAPAK
      no: 370, yakin: 2.8, kamera: 0, yaziY: 260,
      sprite: { w: 380, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Galata'dan", "Üsküdar'a", "Kalması uygun değil"], sure: 2.0, boy: 112, renk: ALTIN },
      ],
    },
    // Galata Kulesi'nin şerefesi, lodos sabahı
    {
      no: 370, yakin: 2.8, kamera: 8,
      sprite: { w: 380, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Galata Kulesi'nin tepesinde", "bir adam duruyor.", "Sırtında kartal kanatları."], sure: 5.94 }, // kart 1
      ],
    },
    // şerefeden Boğaz ve Üsküdar
    {
      no: 371, yakin: 2.8, kamera: 8,
      sprite: { w: 380, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Aşağıda Boğaz.", "Karşıda Üsküdar.", "Üç kilometreden fazla uzakta."], sure: 5.09 }, // kart 2
      ],
    },
    // köşk odası: IV. Murad ve kese
    {
      no: 372, yakin: 3.0, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bu adam uçarsa padişah ona", "bir kese altın verecek."], sure: 4.25, renk: ALTIN }, // kart 3
        { satirlar: ["Ve aynı nefeste", "sürgüne yollayacak."], sure: 3.09, renk: KIZIL }, // kart 4
      ],
    },
    // genç IV. Murad atıyla Haliç kıyısında
    {
      no: 373, yakin: 2.6, kamera: 14,
      sprite: { w: 420, h: 230, fps: 14, x: [245, 295], taban: 632 },
      yazilar: [
        { satirlar: ["İstanbul, Dördüncü Murad'ın", "gençlik yılları.", "Bin altı yüz otuzlar."], sure: 5.48 }, // kart 5
      ],
    },
    // Hezarfen ve kanat sehpası
    {
      no: 374, yakin: 3.2, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Adamın adı Ahmed Çelebi.", "Lakabı Hezarfen:", "bin fenli adam."], sure: 4.78, renk: ALTIN }, // kart 6
        { satirlar: ["Doğumunu, ailesini, mesleğini", "kimse bilmiyor."], sure: 3.86 }, // kart 7
      ],
    },
    // Kurtuba: İbn Firnas'ın sert inişi
    {
      no: 375, yakin: 2.8, kamera: 8,
      sprite: { w: 380, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ondan önce de deneyenler var.", "Dokuzuncu yüzyılda Kurtuba'da", "İbn Firnas."], sure: 5.86 }, // kart 8
        { satirlar: ["Sert indi, sırtını incitti.", "Onu da tek kaynak anlatıyor.", "Yedi yüz elli yıl kadar sonra."], sure: 7.09 }, // kart 9
      ],
    },
    // Nişabur: Cevherî cami damında
    {
      no: 376, yakin: 2.8, kamera: 8,
      sprite: { w: 380, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["On birinci yüzyılın başında", "Nişabur'da sözlükçü Cevherî.", "Cami damından atladı. Öldü."], sure: 6.86, renk: KIZIL }, // kart 10
      ],
    },
    // Okmeydanı: taş minbere yürüyüş
    {
      no: 377, yakin: 2.8, kamera: 14,
      sprite: { w: 400, h: 230, fps: 14, x: [240, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Hezarfen kuleye hemen", "çıkmıyor. Önce Okmeydanı.", "Orada taş bir minber var."], sure: 6.02 }, // kart 11
      ],
    },
    // minberin üstünde kanat açıp kapama (talim)
    {
      no: 378, yakin: 2.8, kamera: 8,
      sprite: { w: 380, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["O minberin üstünden sekiz,", "dokuz kez kanat açıp atlıyor.", "Kuleden önce talim."], sure: 6.25 }, // kart 12
      ],
    },
    // Galata Kulesi geniş çekim, lodos
    {
      no: 379, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sonra kule. Bugünkü ölçüsüyle", "yaklaşık altmış yedi metre.", "Lodos esiyor, güneybatıdan."], sure: 6.94 }, // kart 13
      ],
    },
    // Sarayburnu: Sinan Paşa Köşkü'nün taşlığında padişah
    {
      no: 380, yakin: 2.8, kamera: 8,
      sprite: { w: 380, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Haliç'in karşı yakasında,", "Sarayburnu'nda, Sinan Paşa", "Köşkü'nden padişah izliyor."], sure: 6.55 }, // kart 14
      ],
    },
    // Boğaz üstünde süzülüş (havada olması doğru)
    {
      no: 381, yakin: 2.6, kamera: 14, odakY: 600, yaziY: 230,
      sprite: { w: 420, h: 230, fps: 10, x: [250, 300], taban: 650 },
      yazilar: [
        { satirlar: ["Adam atlıyor. Lodos", "kanatların altına giriyor.", "Boğaz'ın üstünde süzülüyor."], sure: 6.09 }, // kart 15
      ],
    },
    // Üsküdar, Doğancılar: ayaklar yere değer
    {
      no: 382, yakin: 2.8, kamera: 8,
      sprite: { w: 380, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Üsküdar, Doğancılar Meydanı.", "Ayakları yere değiyor.", "Yaşıyor."], sure: 5.02, renk: ALTIN }, // kart 16
      ],
    },
    // köşk: kese altın
    {
      no: 383, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Padişah ödülünü veriyor:", "bir kese altın."], sure: 3.48, renk: ALTIN }, // kart 17
      ],
    },
    // hüküm: kızıl akşam
    {
      no: 384, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ve aynı nefeste", "hükmünü söylüyor:", "Bu adamdan çok korkulur."], sure: 4.86, renk: KIZIL }, // kart 18
        { satirlar: ["Böylesinin kalması", "uygun değil."], sure: 2.78, renk: ALTIN }, // kart 19
      ],
    },
    // sürgün gemisi batıya
    {
      no: 385, yakin: 2.6, kamera: 14,
      sprite: { w: 420, h: 230, fps: 10, x: [300, 230], taban: 632 },
      yazilar: [
        { satirlar: ["Cezayir. Merkezden çok uzak", "bir sürgün yeri.", "Hezarfen oraya gönderiliyor."], sure: 6.02, renk: KIZIL }, // kart 20
      ],
    },
    // Cezayir gecesi (insan ve mezar yok)
    {
      no: 386, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 230, fps: 6, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Hakkında bilinen son söz", "üç kelime:", "Orada merhum oldu."], sure: 4.55, renk: KIZIL }, // kart 21
      ],
    },
    // gece Galata, şerefe boş
    {
      no: 387, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ne zaman, nasıl? Bilinmiyor.", "Kalması uygun değildi.", "Kalmadı."], sure: 5.02, renk: ALTIN }, // kart 22
      ],
    },
    // Kahire: yaşlı Evliya ayakta
    {
      no: 388, yakin: 3.2, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Peki bunu bize kim anlatıyor?", "Tek bir adam: Evliya Çelebi."], sure: 4.86, renk: ALTIN }, // kart 23
      ],
    },
    // Evliya rahlede yazar
    {
      no: 389, yakin: 3.0, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ve Evliya bu satırları", "kırk yıl kadar sonra yazıyor.", "Kahire'de, yaşlı bir adam."], sure: 6.48 }, // kart 24
        { satirlar: ["Uçuşa bir yıl bile vermiyor.", "Bugün dolaşan kesin tarih", "sonradan verilmiş."], sure: 6.02 }, // kart 25
      ],
    },
    // boş kütüphane
    {
      no: 390, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Başka hiçbir Osmanlı kroniği", "bu adamdan söz etmiyor.", "Hiçbir yabancı rapor da."], sure: 6.32 }, // kart 26
      ],
    },
    // Lagari ve fişeği
    {
      no: 391, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Aynı Evliya, aynı ciltte", "başka bir uçan adam anlatıyor.", "Lagari Hasan Çelebi. Fişekçi."], sure: 6.94 }, // kart 27
      ],
    },
    // Sarayburnu şenliği, alçak fişekler
    {
      no: 392, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Padişahın kızı Kaya Sultan'ın", "doğduğu gece.", "Sarayburnu'nda şenlik."], sure: 5.48 }, // kart 28
      ],
    },
    // fişek ve barut fıçıları
    {
      no: 393, yakin: 2.8, kamera: 8,
      sprite: { w: 380, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Yedi kollu bir fişek.", "İçinde altmış dört kilo kadar", "barut macunu."], sure: 5.4 }, // kart 29
      ],
    },
    // Lagari fişeğin tepesinde sesleniyor
    {
      no: 394, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Lagari fişeğe biniyor ve", "padişaha sesleniyor:"], sure: 3.86 }, // kart 30
        { satirlar: ["Padişahım, seni Allah'a", "ısmarladım. İsa Peygamberle", "konuşmaya gidiyorum."], sure: 5.94, renk: ALTIN }, // kart 31
      ],
    },
    // ateşleme ve kalkış
    {
      no: 395, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Fişek ateşleniyor.", "Göğe yükseliyor."], sure: 3.09 }, // kart 32
      ],
    },
    // denize iniş, yüzerek dönüş
    {
      no: 396, yakin: 2.8, kamera: 14,
      sprite: { w: 400, h: 230, fps: 8, x: [300, 240], taban: 632 },
      yazilar: [
        { satirlar: ["Lagari denize iniyor.", "Yüzerek padişahın", "önüne geliyor."], sure: 4.55 }, // kart 33
      ],
    },
    // kese akçe, sürgün yok
    {
      no: 397, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ona da bir kese akçe.", "Ve sipahilik.", "Sürgün yok."], sure: 4.02, renk: ALTIN }, // kart 34
      ],
    },
    // sipahi Lagari, sürgüne giden Hezarfen
    {
      no: 398, yakin: 2.6, kamera: 8,
      sprite: { w: 420, h: 230, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["İki uçan adam.", "Biri sipahi oluyor.", "Öteki Cezayir'e yollanıyor."], sure: 5.17, renk: KIZIL }, // kart 35
      ],
    },
    // 2009 deneyi: fişek alçakta parçalanır
    {
      no: 399, yakin: 2.6, kamera: 8,
      sprite: { w: 420, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["İki bin dokuzda Discovery", "ekibi fişeği yeniden yapıyor.", "Fişek parçalanıyor."], sure: 6.17, renk: KIZIL }, // kart 36
      ],
    },
    // açılış görüntüsüne dönüş
    {
      no: 370, yakin: 2.8, kamera: 8,
      sprite: { w: 380, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Peki Hezarfen gerçekten", "uçtu mu?"], sure: 2.86, renk: ALTIN }, // kart 37
      ],
    },
    // 'rivayet' diyen taraf konuşur
    {
      no: 400, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Rivayet diyenler: Tek kaynak,", "kırk yıl sonra yazılmış.", "Evliya harikalara düşkün."], sure: 6.55 }, // kart 38
        { satirlar: ["Bugünkü hesaplara göre durgun", "havada o yükseklikten üç", "kilometre süzülmek imkânsız."], sure: 6.78 }, // kart 39
      ],
    },
    // 'erken havacılık' diyen taraf konuşur
    {
      no: 401, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Erken havacılık diyenler:", "Bu bir şenlik abartısı değil.", "Önce talim, sonra kule."], sure: 6.48 }, // kart 40
        { satirlar: ["Kanat çırpmak imkânsız.", "Ama güçlü bir lodosla planör", "gibi süzülmek düşünülebilir."], sure: 6.63 }, // kart 41
      ],
    },
    // terazi: kitap ve kartal tüyü
    {
      no: 402, yakin: 3.0, kamera: 8,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kaynaklar ayrışıyor.", "Biz karar vermiyoruz."], sure: 3.63, renk: ALTIN }, // kart 42
      ],
    },
    // bugün: Hezarfen Havaalanı, küçük uçak
    {
      no: 403, yakin: 2.6, kamera: 14,
      sprite: { w: 420, h: 230, fps: 16, x: [220, 310], taban: 632 },
      yazilar: [
        { satirlar: ["Ama şunu biliyoruz. Bugün", "Çatalca'da onun adını taşıyan", "bir havaalanı var."], sure: 6.09 }, // kart 43
      ],
    },
    // sinema salonu
    {
      no: 404, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bir sinema filmi var:", "İstanbul Kanatlarımın Altında."], sure: 4.4 }, // kart 44
      ],
    },
    // bugün gün batımında Galata Kulesi
    {
      no: 405, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Padişah demişti:", "Böylesinin kalması", "uygun değil."], sure: 4.09, renk: ALTIN }, // kart 45
        { satirlar: ["Neredeyse dört yüz yıl kaldı."], sure: 2.63, renk: ALTIN }, // kart 46
      ],
    },
    // Üsküdar kıyısı: kese ve uzakta gemi
    {
      no: 406, yakin: 2.8, kamera: 8,
      sprite: { w: 380, h: 230, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Siz olsanız ona altın mı", "verirdiniz, sürgün mü?"], sure: 4.02, renk: ALTIN }, // kart 47
      ],
    },
  ],
  kapanis: {
    satirlar: ["Piksel Tarih", "@pikseltarihim"],
    sonraki: "Yorumlara yaz: altın mı, sürgün mü?",
    sure: 3, arka: 406,
  },
};

export const HEZARFEN_KARE = Math.round(seriSure(HEZARFEN_SERI) * T_FPS);
export const Hezarfen: React.FC = () => <SeriVideo seri={HEZARFEN_SERI} />;
