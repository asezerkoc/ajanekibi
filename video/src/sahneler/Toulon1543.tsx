import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Küçük Konstantinopolis: Barbaros'un donanması Toulon'da kışlıyor (1543-44). Grafikerin tarifi:
   teslimler/gece/ara/toulon-1543/5-grafik.md; sahneler 450-486 (video/piksel/toulon_1543.py).
   Kartlar kalite kontrolün nihai 52 kartıyla harfi harfine aynı; süreler tahmini (seslendirme 255 sn),
   ses/hizala_seri.py sese göre yeniden yazar. Python çizimi yakin/sprite/yazı ayarlarını bu dosyadan okur. */
// Kapak: sahne 450 katmanlarıyla yapılan ilk Bolum (2 sn, sessiz).
export const TOULON_SERI: Seri = {
  etiket: "PİKSEL TARİHİM · BARBAROS TOULON'DA",
  ses: "toulon-1543-anlatim.mp3",
  bolumler: [
    { // KAPAK (hizala_seri bu bloğu atlar: kapak yazıları anlatımda yok)
      no: 450, yakin: 2.6, kamera: 0, yaziY: 270,
      sprite: { w: 400, h: 230, fps: 14, x: [262, 278], taban: 632 },
      yazilar: [
        { satirlar: ["Barbaros", "Toulon'da", "Küçük Konstantinopolis"], sure: 2.0, boy: 112, renk: ALTIN },
      ],
    },
    // Toulon koyu, 1543 sonbaharı: Barbaros'un kadırgası kürek çekerek koya girer; arkada kasaba ve Faron
    {
      no: 450, yakin: 2.6, kamera: 6,
      sprite: { w: 400, h: 230, fps: 14, x: [262, 278], taban: 632 },
      yazilar: [
        { satirlar: ["Bir Fransız kralı", "kendi şehrini boşalttırıyor."], sure: 3.44 }, // kart 1
        { satirlar: ["Düşman geldiği için değil.", "Müttefiki geldiği için."], sure: 3.71 }, // kart 2
      ],
    },
    // Barbaros kadırgasının güvertesinde; uzakta donanma
    {
      no: 451, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Müttefik:", "Barbaros Hayreddin Paşa."], sure: 2.64 }, // kart 3
      ],
    },
    // açık deniz: uzun kadırga tek sıra kürekle sağa yol alır, arkada başka kadırgalar
    {
      no: 452, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 14, x: [262, 278], taban: 632 },
      yazilar: [
        { satirlar: ["Yüzü aşkın kadırga,", "on binlerce adam.", "Çoğu kürekçi."], sure: 3.77 }, // kart 4
      ],
    },
    // Fontainebleau tarzı salon: taçlı I. François tahtının önünde
    {
      no: 453, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Avrupa buna skandal diyor.", "Kral Birinci François'nın", "resmî sıfatı:"], sure: 4.77 }, // kart 5
        { satirlar: ["\"Çok Hristiyan Kral\".", "Ortak düşmanları: Habsburg", "imparatoru Beşinci Karl."], sure: 5.24 }, // kart 6
      ],
    },
    // alacakaranlık: Osmanlı ve Fransız kadırgası yan yana
    {
      no: 454, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 12, x: [262, 278], taban: 632 },
      yazilar: [
        { satirlar: ["Şimdi kral bir Osmanlı", "donanmasıyla aynı safta.", "Bu kışın bedelini kim ödüyor?"], sure: 5.51, renk: ALTIN }, // kart 7
      ],
    },
    // Marsilya rıhtımı, 1543 yazı: Barbaros ve Kaptan Polin; karşı kıyıda Marsilya surları
    {
      no: 455, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["1543 yazı. Barbaros donanmayı", "Marsilya'ya getiriyor.", "Yanında Fransız elçisi"], sure: 5.37 }, // kart 8
        { satirlar: ["Kaptan Polin. Hedef,", "Habsburgların müttefiki", "Savoy Dükü'nün şehri: Nice."], sure: 5.17 }, // kart 9
      ],
    },
    // Nice kuşatması: tepedeki kale, aşağı şehir; koyda kadırgalar, önde Fransız piyadesi
    {
      no: 456, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 220, fps: 14, x: [262, 278], taban: 632 },
      yazilar: [
        { satirlar: ["6 Ağustos. Kuşatma başlıyor.", "Karadan Fransızlar,", "denizden Osmanlılar."], sure: 4.97 }, // kart 10
      ],
    },
    // aşağı şehir yanar, tepedeki kale direnir (sancak dalgalanır)
    {
      no: 457, yakin: 2.6, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Aşağı şehir teslim oluyor,", "yakılıp yağmalanıyor.", "Ama tepedeki kale direniyor."], sure: 5.51, renk: KIZIL }, // kart 11
      ],
    },
    // Savoy ve del Vasto'nun zırhlı atlıları sola gelir, toz kalkar
    {
      no: 458, yakin: 2.6, kamera: 10,
      sprite: { w: 400, h: 220, fps: 16, x: [278, 262], taban: 632 },
      yazilar: [
        { satirlar: ["7 Eylül. Savoy Dükü ve", "Milano valisi del Vasto", "ordularıyla geliyor."], sure: 4.84 }, // kart 12
      ],
    },
    // sahildeki ordugâh: Barbaros ufku gösterir, çadırlar toplanır; ufukta Doria'nın yelkenleri
    {
      no: 459, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ufukta Habsburgların amirali", "Andrea Doria'nın filosu.", "Barbaros çadırları toplatıyor."], sure: 5.97, renk: KIZIL }, // kart 13
      ],
    },
    // alacakaranlık: Barbaros'un kadırgası sola, denize açılır
    {
      no: 460, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 14, x: [278, 262], taban: 632 },
      yazilar: [
        { satirlar: ["Doria'dan saatler önce denize", "açılıyor. İki büyük amiral", "aynı koyda karşılaşmıyor."], sure: 5.84 }, // kart 14
      ],
    },
    // Toulon, sonbahar sabahı: Provence evleri, katedral, arkada Faron; rıhtımda boş kayıklar
    {
      no: 461, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Kış yaklaşıyor. Donanmaya", "kışlayacak bir liman gerek.", "Kral Toulon'u veriyor."], sure: 5.44 }, // kart 15
        { satirlar: ["Provence'ta, yaklaşık", "beş bin nüfuslu küçük", "bir liman kenti."], sure: 4.37 }, // kart 16
      ],
    },
    // meydanda münadi açık mektubu okur; dinleyen halk
    {
      no: 462, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["8 Eylül 1543.", "Kralın açık mektubu ve", "vali Grignan'ın emri:"], sure: 4.24 }, // kart 17
        { satirlar: ["Toulon tümüyle boşaltılsın.", "Herkes gitsin."], sure: 3.17, renk: KIZIL }, // kart 18
      ],
    },
    // şehir meclisi: konsüller ve tutanağı yazan kâtip
    {
      no: 463, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Şehir meclisi toplanıyor:", "16 Eylül, sonra 25 Eylül.", "Konsüller kralı yumuşatıyor."], sure: 5.71 }, // kart 19
        { satirlar: ["Tutanakta şöyle yazıyor:", "yalnızca çocuklar ve gitmek", "isteyen kadınlar ayrılsın."], sure: 5.64 }, // kart 20
      ],
    },
    // çocuklar ve kadınlar yola düşer (sola); kapıda kalan erkek
    {
      no: 464, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 220, fps: 14, x: [278, 262], taban: 632 },
      yazilar: [
        { satirlar: ["Erkekler kalıyor.", "Çocuklar ve isteyen kadınlar", "yola düşüyor."], sure: 4.37, renk: KIZIL }, // kart 21
      ],
    },
    // boş sokak, mavi alacakaranlık; kapısında tek başına bir adam
    {
      no: 465, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sokaklar sessizleşiyor.", "Bedeli önce Toulon ödüyor."], sure: 3.71, renk: ALTIN }, // kart 22
      ],
    },
    // sabah pusu: kadırgalar sıra hâlinde koya girer
    {
      no: 466, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 14, x: [262, 278], taban: 632 },
      yazilar: [
        { satirlar: ["1543 sonbaharı.", "Kadırgalar koya giriyor.", "Rıhtımda sarıklar."], sure: 4.31 }, // kart 23
      ],
    },
    // rıhtımda sarıklı levendler ve onlara bakan Fransız tanık
    {
      no: 467, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Dönemin bir Fransız tanığı:", "Toulon'a bakan, kendini", "Konstantinopolis'te sanır."], sure: 5.57 }, // kart 24
      ],
    },
    // gün batımı: koy kadırgalarla dolu; Küçük Konstantinopolis
    {
      no: 468, yakin: 2.6, kamera: 10,
      sprite: { w: 400, h: 230, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Şehre yeni bir ad takılıyor:", "Küçük Konstantinopolis."], sure: 3.84, renk: ALTIN }, // kart 25
      ],
    },
    // kış gecesi: katedralin cephesi, kapı fenerinin ışığı
    {
      no: 469, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Peki şehrin içinde", "o kış ne oluyor?"], sure: 2.71 }, // kart 26
        { satirlar: ["Bugün çok anlatılan", "bir hikâye var:", "katedral camiye çevrilmiş."], sure: 4.51 }, // kart 27
      ],
    },
    // 19. yüzyıl: Toulonlu tarihçi kitaplarının başında
    {
      no: 470, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ama on dokuzuncu yüzyılın", "Toulon tarihçileri bile", "camiden söz etmiyor."], sure: 5.04, renk: KIZIL }, // kart 28
      ],
    },
    // katedral içi: rahip vaftiz defterine yazar
    {
      no: 471, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Katedralin kendi defteri de", "başka bir şey söylüyor."], sure: 3.77 }, // kart 29
      ],
    },
    // vaftiz: rahip bebeği kurnanın üstünde tutar, anne ve baba yanında
    {
      no: 472, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Vaftizler kış boyunca sürüyor.", "Her ay yaklaşık on bebek.", "Katedral kapanmıyor."], sure: 5.51, renk: ALTIN }, // kart 30
      ],
    },
    // kış sabahı pazar: Provenceli ekmekçi ve sarıklı levend
    {
      no: 473, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Tarihçi Jean Bérenger yazıyor:", "Provencelılar Türklerin", "disiplinine şaşırıyor."], sure: 5.51 }, // kart 31
        { satirlar: ["İki taraf kaynaşıyor."], sure: 1.77 }, // kart 32
      ],
    },
    // kış: kraliyet memuru vergi muafiyetini okur; halk sevinir
    {
      no: 474, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Peki bedel? Aralık 1543.", "Toulon halkı on yıl boyunca", "kraliyet vergisi ödemeyecek."], sure: 5.77 }, // kart 33
      ],
    },
    // rıhtım: altın sandığı, ipek, erzak, barut fıçıları; Fransız memur ve Barbaros
    {
      no: 475, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Yerel tarihçilere göre", "Barbaros'a sekiz yüz bin", "altın écu, ipek, erzak"], sure: 5.04 }, // kart 34
        { satirlar: ["ve mühimmat veriliyor.", "Bedeli şimdi kral ödüyor."], sure: 3.57, renk: ALTIN }, // kart 35
      ],
    },
    // Mayıs 1544 sabahı: yelkenler açık, kadırga sola (eve) yol alır
    {
      no: 476, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 14, x: [278, 262], taban: 632 },
      yazilar: [
        { satirlar: ["23 Mayıs 1544. Donanma", "Provence kıyısından ayrılıyor."], sure: 3.91 }, // kart 36
      ],
    },
    // Fransız kadırgasının güvertesi: rahip Maurand defterine çizer; kıyı geride kalır
    {
      no: 477, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Arkada beş Fransız kadırgası.", "Birinde Antibes'li bir rahip:", "Jérôme Maurand."], sure: 5.37 }, // kart 37
        { satirlar: ["Yolu çizimlerle kaydediyor.", "Toulon geride kalıyor."], sure: 3.71 }, // kart 38
      ],
    },
    // kuşbakışı masa: portolan harita, rota noktaları ilerler; dört yer işaretlenir
    {
      no: 478, yakin: 2.6, kamera: 0, odakY: 560,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ama donanma eve boş dönmüyor.", "Önce İtalya kıyısındaki", "kasabalar ve adalar vuruluyor:"], sure: 5.97, renk: KIZIL }, // kart 39
        { satirlar: ["Talamone, Porto Ercole,", "Giglio, Ischia."], sure: 2.97 }, // kart 40
      ],
    },
    // Lipari: düz tepeli kayada surlu katedral kenti; ufukta Vulcano
    {
      no: 479, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Temmuz 1544. Lipari.", "Eolie Adaları'nda", "surlu bir katedral kenti."], sure: 4.64 }, // kart 41
      ],
    },
    // Lipari yanar; esirler gemilere götürülür (uzaktan, şiddetsiz)
    {
      no: 480, yakin: 2.6, kamera: 6,
      sprite: { w: 400, h: 220, fps: 12, x: [278, 262], taban: 632 },
      yazilar: [
        { satirlar: ["Şehir yağmalanıyor.", "Halk esir alınıyor.", "Kaç kişi?"], sure: 3.64, renk: KIZIL }, // kart 42
      ],
    },
    // kuşbakışı masa: iki kronik ve bir not kâğıdı; üç farklı sayı
    {
      no: 481, yakin: 2.6, kamera: 0, odakY: 560,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kaynaklar ayrışıyor:", "sekiz bin diyen de var,", "on bir bin diyen de."], sure: 4.71 }, // kart 43
        { satirlar: ["Bir araştırmacı ise adanın", "bütün nüfusunu", "en çok dört bin sayıyor."], sure: 4.77 }, // kart 44
      ],
    },
    // yanmış arşiv odası: kömürleşmiş raf, yerde için için yanan kâğıtlar
    {
      no: 482, yakin: 2.8, kamera: 4,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Katedral ağır hasar görüyor.", "Adanın arşivleri", "o gün yok oluyor."], sure: 4.57, renk: KIZIL }, // kart 45
        { satirlar: ["Lipari kendi hikâyesini de", "kaybediyor."], sure: 2.91 }, // kart 46
      ],
    },
    // Lipari, sessiz alacakaranlık: kaledeki ince duman
    {
      no: 483, yakin: 2.6, kamera: 6,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bedeli en ağır ödeyen,", "Toulon'u hiç görmemiş", "bir ada."], sure: 3.91, renk: ALTIN }, // kart 47
      ],
    },
    // Ağustos 1544: İstanbul silüeti, kadırga eve döner
    {
      no: 484, yakin: 2.6, kamera: 8,
      sprite: { w: 400, h: 230, fps: 14, x: [278, 262], taban: 632 },
      yazilar: [
        { satirlar: ["Ağustos 1544. Donanma", "İstanbul'a dönüyor. İki yıl", "sonra Barbaros ölüyor."], sure: 5.17 }, // kart 48
      ],
    },
    // kuşbakışı: Matrakçı Nasuh'un Toulon minyatürü açık yazmada
    {
      no: 485, yakin: 2.6, kamera: 0, odakY: 560,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["O kışı bir Osmanlı ressamı", "da çizdi: Matrakçı Nasuh.", "Minyatürü bugün Topkapı'da."], sure: 5.71 }, // kart 49
      ],
    },
    // Toulon gecesi: rıhtımda kalan bir Toulonlu, koyda fenerli kadırgalar
    {
      no: 486, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 220, fps: 8, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Kral şehrini neden boşalttı?", "Müttefikinin donanmasına", "kışlık bir liman gerekiyordu."], sure: 5.91, renk: ALTIN }, // kart 50
        { satirlar: ["Bedelini kim ödedi?", "Toulon'un aileleri, kralın", "hazinesi ve Lipari."], sure: 4.77, renk: ALTIN }, // kart 51
        { satirlar: ["Siz Toulonlu olsaydınız,", "şehirde kalır mıydınız?"], sure: 3.57, renk: ALTIN }, // kart 52
      ],
    },
  ],
  kapanis: {
    satirlar: ["Piksel Tarih", "@pikseltarihim"],
    sonraki: "Yorumlara yaz, arkadaşına gönder",
    sure: 3, arka: 486, gece: true,
  },
};

export const TOULON_KARE = Math.round(seriSure(TOULON_SERI) * T_FPS);
export const Toulon1543: React.FC = () => <SeriVideo seri={TOULON_SERI} />;
