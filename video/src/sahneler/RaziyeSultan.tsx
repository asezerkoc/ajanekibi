import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Oğullarımdan İyi: Raziye Sultan, Delhi Türk Sultanlığı'nın kadın hükümdarı (1236-1240). Grafikerin tarifi:
   teslimler/gece/ara/raziye-sultan/5-grafik.md; sahneler 210-248 (video/piksel/raziye_sultan.py).
   Kartlar 4-kalite-metin.md "Nihai ekran kartları" ile harfi harfine aynı ve aynı sırada (51 kart).
   Süreler tahmini (seslendirme 252 sn); ses/hizala_seri.py sese göre yeniden yazar. */
// Kapak: sahne 210 katmanlarıyla yapılan ilk Bolum (2 sn, sessiz); başlık ve alt başlık 4-kalite-metin.md'deki onaylı
// kapak önerisi ("Oğullarımdan İyi" / "Delhi tahtındaki tek kadın"). Bütün sahnelerde yazı yaziY 260'tan başlar;
// raziye_sultan.py bu dosyadan yazı bantlarını okur ve figürlerin, yapıların bu banda girmediğini denetler.
// Vurgu: ALTIN = motif ve cevap (kart 10, 18, 19, 43, 50), KIZIL = "ama" dönüşleri ve kayıp (kart 16, 27, 30, 48).
export const RAZIYE_SERI: Seri = {
  etiket: "PİKSEL TARİHİM · RAZİYE SULTAN",
  ses: "raziye-sultan-anlatim.mp3",
  bolumler: [
    { // KAPAK
      no: 210, yakin: 2.8, kamera: 0, yaziY: 270,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Oğullarımdan", "İyi", "Delhi tahtındaki tek kadın"], sure: 2.0, boy: 112, renk: ALTIN },
      ],
    },
    // 210: Delhi, Kasım 1236, Cuma: avlu revakları önünde kalabalık; peçeli Raziye taş sekide konuşur
    {
      no: 210, yakin: 2.8, kamera: 8, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Delhi, Kasım 1236.", "Cuma namazı. Kalabalığın önüne", "bir kadın çıkıyor, konuşuyor."], sure: 6.30 }, // kart 1
        { satirlar: ["Sarayda onu öldürtmek isteyen", "biri var. Kadın kılıçla değil,", "sözle karşılık veriyor."], sure: 5.51 }, // kart 2
      ],
    },
    // 211: alacakaranlık ova, rüzgâr: peçeli Raziye yalnız, yanında yaşlı ağaç
    {
      no: 211, yakin: 2.8, kamera: 8, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Adı Raziye. Dört yıl sonra", "bir ovada ölecek."], sure: 3.35 }, // kart 3
      ],
    },
    // 212: boş taht: tavandan kandil, iki yanda şamdan, tahtın önüne ışık düşer
    {
      no: 212, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Arada, Delhi tahtına oturan", "tek kadın olacak."], sure: 2.91 }, // kart 4
      ],
    },
    // 213: karanlık oda: peçeli Raziye yakın plan, yüzü görünmez; tek kandil
    {
      no: 213, yakin: 3.2, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Peki bu kadın neyi çıkarıp", "atacak? Bunu sona", "saklıyorum."], sure: 4.22 }, // kart 5
      ],
    },
    // 214: saray: Sultan İltutmış tahtta; köşede tarihçi Minhâc rahlede yazar
    {
      no: 214, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Önce babası. Sultan İltutmış,", "eski bir köle. Saray tarihçisi", "Minhâc yazıyor:"], sure: 4.88 }, // kart 6
      ],
    },
    // 215: Delhi kapısı, 1231: atlı İltutmış Gwalior'a (sağa) yönelir, geride ordu; peçeli kızı kapıda kalır
    {
      no: 215, yakin: 2.6, kamera: 8, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["1231'de Gwalior seferine", "giderken Delhi'nin yönetimini", "kızına bırakıyor."], sure: 6.14 }, // kart 7
      ],
    },
    // 216: divan: İltutmış ve peçeli kızı; karşılarında iki emîr itiraz eder
    {
      no: 216, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Dönüşte onu veliaht görüyor.", "Emîrler itiraz ediyor:", "Oğulların varken?"], sure: 4.56 }, // kart 8
        { satirlar: ["Cevabı:", "Oğullarım zevke dalmış.", "Kızım onlardan iyi."], sure: 3.31 }, // kart 9
      ],
    },
    // 217: motif: İltutmış ve kızı yan yana, sessiz; şamdan ışığı
    {
      no: 217, yakin: 3.0, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Oğullarımdan iyi."], sure: 1.78, renk: ALTIN }, // kart 10
      ],
    },
    // 218: örtülü tabut sehpada; Fîrûz tahta oturtulur, emîr onu gösterir
    {
      no: 218, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["30 Nisan 1236. İltutmış", "ölüyor. Emîrler kızı değil,", "oğlu Fîrûz'u tahta çıkarıyor."], sure: 7.00 }, // kart 11
      ],
    },
    // 219: gece: Fîrûz minderde meyve tepsisinin başında; arkada ayakta Şah Terken
    {
      no: 219, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Fîrûz eğlencede. Devleti", "annesi Şah Terken yönetiyor.", "Raziye'yi öldürtmek isteyen o."], sure: 5.51 }, // kart 12
      ],
    },
    // 220: Cuma: halk saray kapısına (sağa) yürür; geride sekide kolunu kaldırmış peçeli Raziye
    {
      no: 220, yakin: 2.6, kamera: 12, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 16, x: [245, 295], taban: 632 },
      yazilar: [
        { satirlar: ["İşte o Cuma. Raziye halka", "sesleniyor. Kalabalık", "sarayı basıyor."], sure: 4.09 }, // kart 13
      ],
    },
    // 221: taht odası: peçeli Raziye tahtta; Şah Terken muhafızla götürülür
    {
      no: 221, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Şah Terken tutuklanıyor.", "Ordunun bir bölümü Raziye'yi", "tahta çıkarıyor."], sure: 4.64 }, // kart 14
      ],
    },
    // 222: zindan: Fîrûz taş zeminde oturur; kapıda meşaleli gardiyan
    {
      no: 222, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Fîrûz yakalanıyor; saltanatı", "yedi ayı bile bulmuyor.", "Hapiste ölüyor."], sure: 4.49 }, // kart 15
      ],
    },
    // 223: sikke yakın plan: babasının adıyla gümüş sikke, ahşap yuvada
    {
      no: 223, yakin: 3.2, kamera: 4, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ama sikkeye bakın. Üstünde", "babasının adı var. Raziye", "yalnızca halifenin destekçisi."], sure: 5.51, renk: KIZIL }, // kart 16
      ],
    },
    // 224: darphane: usta örste çekiçle kalıba vurur; mangalda kor
    {
      no: 224, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 12, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ertesi yıl, 1237'de kalıp", "değişiyor. Sikkede artık", "şu yazıyor:"], sure: 5.19 }, // kart 17
      ],
    },
    // 225: yeni sikke yakın plan: Raziye'nin adı altın ışıkla parlar
    {
      no: 225, yakin: 3.2, kamera: 4, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Sultan Celâletü'd-dünyâ", "ve'd-dîn."], sure: 2.65, renk: ALTIN }, // kart 18
        { satirlar: ["Babasının adının yerini,", "oğullarından iyi dediği", "kızın adı alıyor."], sure: 4.41, renk: ALTIN }, // kart 19
      ],
    },
    // 226: saray odası: peçeli Raziye; hizmetkâr tepside tunik ve külahı sunar
    {
      no: 226, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Sonra bir gün Delhi başka", "bir şey görüyor. Sultan,", "kadın giysisini bırakıyor."], sure: 4.96 }, // kart 20
      ],
    },
    // 227: fil üstünde peçesiz, külahlı sultan; geride seyreden kalabalık
    {
      no: 227, yakin: 2.6, kamera: 10, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 12, x: [245, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Tunik ve külah giyiyor. Tahta", "peçesiz oturuyor. Fil üstünde", "halka görünüyor. Yüzü açık."], sure: 6.19 }, // kart 21
      ],
    },
    // 228: ovada at süren Raziye (tunik, külah, peçesiz); toynaklardan toz
    {
      no: 228, yakin: 2.6, kamera: 14, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 24, x: [240, 300], taban: 632 },
      yazilar: [
        { satirlar: ["Yüz yıl sonra bile", "anlatılacak: erkekler gibi", "at sürerdi, yüzünü örtmezdi."], sure: 4.80 }, // kart 22
      ],
    },
    // 229: akşam, revak gölgesi: üç Türk köle emîri fısıldaşır
    {
      no: 229, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Türk köle emîrleri bunu", "izliyor. Onları rahatsız", "eden biri var:"], sure: 4.09 }, // kart 23
      ],
    },
    // 230: ahırlar: Habeşli Yakut, atlı Raziye'nin atını dizgininden tutar; geride emîrler
    {
      no: 230, yakin: 2.6, kamera: 8, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Habeşli bir köle, Cemâleddin", "Yakut. Raziye onu ahırların", "başına getiriyor."], sure: 4.88 }, // kart 24
        { satirlar: ["Ona yakın davranıyor.", "Emîrler kıskanıyor."], sure: 2.75 }, // kart 25
      ],
    },
    // 231: Nisan 1240: Raziye ve atlıları sola, Bathinda kalesine yürür
    {
      no: 231, yakin: 2.6, kamera: 12, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 18, x: [290, 250], taban: 632 },
      yazilar: [
        { satirlar: ["Nisan 1240. Bathinda valisi", "Altuniya isyan ediyor. Raziye", "ordusuyla üzerine yürüyor."], sure: 6.85 }, // kart 26
      ],
    },
    // 232: Bathinda kale kapısı, kızıl akşam: iki muhafız arasında Raziye; binicisiz at başı önde
    {
      no: 232, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bathinda önünde Yakut", "öldürülüyor. Raziye yakalanıp", "Bathinda kalesine kapatılıyor."], sure: 5.67, renk: KIZIL }, // kart 27
      ],
    },
    // 233: kale odası, gece: Raziye taş zeminde oturur, pencereden soğuk ışık
    {
      no: 233, yakin: 3.0, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Üç buçuk yıl önce halk onun", "için sarayı basmıştı. Şimdi", "bir kale duvarının arkasında."], sure: 6.11 }, // kart 28
      ],
    },
    // 234: Delhi: Behram Şah tahtta; iki emîr diz çöker
    {
      no: 234, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Aynı ay Delhi'de kardeşi", "Behram Şah tahta çıkarılıyor."], sure: 3.54 }, // kart 29
        { satirlar: ["Ama Delhi'deki yeni düzende", "Altuniya'ya pay düşmüyor.", "Ve beklenmedik bir şey oluyor:"], sure: 5.43, renk: KIZIL }, // kart 30
      ],
    },
    // 235: Raziye ve Altuniya yan yana atlı, Delhi'ye (sağa) yürür
    {
      no: 235, yakin: 2.6, kamera: 12, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 18, x: [250, 295], taban: 632 },
      yazilar: [
        { satirlar: ["Raziye, kendisini hapseden", "adamla evleniyor. İkisi", "birlikte Delhi'ye yürüyor."], sure: 5.11 }, // kart 31
      ],
    },
    // 236: Ekim 1240, Kaithal ovası: Raziye ve Altuniya atlarında; karşıda Behram Şah'ın ordusu
    {
      no: 236, yakin: 2.6, kamera: 8, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ekim 1240, Kaithal ovası.", "Behram Şah'ın ordusu", "karşılarında. Yenilgi."], sure: 6.27 }, // kart 32
      ],
    },
    // 237: boş ordugâh: terk edilmiş çadır; Raziye ve Altuniya yalnız, askerler uzaklaşır
    {
      no: 237, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Askerleri onları bırakıp", "kaçıyor. Raziye Delhi'yi", "bir daha görmüyor."], sure: 4.49 }, // kart 33
      ],
    },
    // 238: tarihçi Minhâc (yaşlı) rahlede yazar; şamdan, kitaplar
    {
      no: 238, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Sonrası için iki anlatım var.", "Minhâc tek cümle yazıyor:"], sure: 3.54 }, // kart 34
        { satirlar: ["Hinduların eline düştüler,", "öldürüldüler.", "Kim olduklarını yazmıyor."], sure: 4.49 }, // kart 35
      ],
    },
    // 239: Faslı gezgin İbn Battûta asasıyla Delhi'ye (sağa) yürür; yükü taşıyan deve
    {
      no: 239, yakin: 2.6, kamera: 12, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 16, x: [245, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Yaklaşık yüz yıl sonra", "Delhi'ye Faslı bir gezgin", "geliyor: İbn Battûta."], sure: 4.49 }, // kart 36
      ],
    },
    // 240: köy, ikindi: köylü kaçan sultana ekmek uzatır
    {
      no: 240, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Halktan başka bir hikâye", "dinliyor. Kaçan sultan bir", "köylüden ekmek istiyor."], sure: 4.96 }, // kart 37
      ],
    },
    // 241: gece, ağaç altı: Raziye uyur, giysisinde mücevher parıltısı; köylü bakar
    {
      no: 241, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Yiyor, uyuyor. Köylü, onun", "giysisindeki mücevherleri", "görüyor. Onu öldürüyor,"], sure: 4.96 }, // kart 38
      ],
    },
    // 242: tarla: ekin sıralarının ortasında küçük kubbeli türbe
    {
      no: 242, yakin: 2.6, kamera: 8, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["tarlasına gömüyor. Sonra", "mezarının üstüne bir kubbe", "yapılıyor. Ziyaretgâh oluyor."], sure: 6.03 }, // kart 39
      ],
    },
    // 243: bugün: sehpada harita; Delhi, Kaithal, Tonk üç ışık
    {
      no: 243, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bugün üç şehir mezarını", "paylaşamıyor:", "Delhi, Kaithal, Tonk."], sure: 3.78 }, // kart 40
      ],
    },
    // 244: Delhi, dar sokak: çatısız dört duvar, iki mezar, önde mavi levha
    {
      no: 244, yakin: 2.6, kamera: 8, yaziY: 260,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Delhi'de dar bir sokakta", "çatısız dört duvar, iki mezar."], sure: 3.46 }, // kart 41
        { satirlar: ["Devletin levhası bile", "temkinli: Raziye'nin", "olduğu söylenir."], sure: 4.53 }, // kart 42
      ],
    },
    // 245: kancanın cevabı: Raziye ayakta, peçe ayağının dibinde yerde
    {
      no: 245, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Peki neyi çıkarıp attı?", "Peçeyi."], sure: 2.57, renk: ALTIN }, // kart 43
      ],
    },
    // 212: bedel: yine boş taht (sahne 212)
    {
      no: 212, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Yüzünü açtı, sikkeye adını", "yazdırdı. Saltanatı", "dört yıl bile sürmedi."], sure: 4.49 }, // kart 44
      ],
    },
    // 246: 1260: yaşlı Minhâc diz çöküp kitabını tahttaki Sultan Nâsıreddin'e sunar
    {
      no: 246, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Minhâc'ın kariyeri", "Raziye döneminde yükselmişti."], sure: 3.31 }, // kart 45
        { satirlar: ["1260'ta kitabını Raziye'nin", "kardeşine sunuyor. Raziye için", "şunu yazıyor:"], sure: 5.98 }, // kart 46
      ],
    },
    // 238: Minhâc'ın övgüsü: yine rahlede yazar (sahne 238)
    {
      no: 238, yakin: 2.8, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["akıllıydı, âdildi, cömertti,", "savaşçıydı. Bir hükümdarda", "aranan her şey vardı."], sure: 4.96 }, // kart 47
      ],
    },
    // 247: yakın plan: rahlede açık kitap, kalem ve mum
    {
      no: 247, yakin: 3.2, kamera: 4, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ama erkek yaratılmamıştı."], sure: 2.33, renk: KIZIL }, // kart 48
        { satirlar: ["Bütün bu meziyetler", "ona ne yaradı?"], sure: 2.20 }, // kart 49
      ],
    },
    // 217: motif 3: İltutmış ve kızı (sahne 217)
    {
      no: 217, yakin: 3.0, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Babası \"oğullarımdan iyi\"", "demişti. Tarihçi", "\"ama erkek değildi\" diyor."], sure: 4.93, renk: ALTIN }, // kart 50
      ],
    },
    // 248: soru: sehpada yan yana peçe ve taç
    {
      no: 248, yakin: 3.0, kamera: 6, yaziY: 260,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Sizce Raziye'yi peçe mi", "öldürdü, taç mı?"], sure: 2.44 }, // kart 51
      ],
    },
  ],
  kapanis: {
    satirlar: ["Piksel Tarih", "@pikseltarihim"],
    sonraki: "Yorumlara yaz, arkadaşına gönder",
    sure: 3, arka: 241, gece: true,
  },
};

export const RAZIYE_KARE = Math.round(seriSure(RAZIYE_SERI) * T_FPS);
export const RaziyeSultan: React.FC = () => <SeriVideo seri={RAZIYE_SERI} />;
