import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* "Timur'un Soyundan Kalender": Ebu'l-Kâsım Bâbür Kalender Mîrzâ (Herat, 15. yy), 3 dakikalık video. Grafikerin tarifi
   (teslimler/2026-10-29-timurun-torunu-kalender-grafiker.md); süreler hizala_seri.py ile vcvcvc seslendirmesine bağlanır.
   Sahne 85 ve 87 ikinci kez kullanılır (çözümleme). */
export const KALENDER: Seri = {
  etiket: "PİKSEL TARİHİM · KALENDER",
  ses: "kalender-anlatim.mp3",
  bolumler: [
    {
      no: 72, yakin: 2.5, kamera: 10, sprite: { w: 540, h: 200, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Hükümdar mı,", "derviş mi?"], sure: 2.63, renk: ALTIN },
        { satirlar: ["Bir elinde kılıç,", "öbüründe şiir."], sure: 3.00 },
      ],
    },
    {
      no: 73, yakin: 2.2, kamera: 20, sprite: { w: 540, h: 170, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Timur'un kanı,", "Baysungur'un kalemi"], sure: 4.34, renk: ALTIN },
      ],
    },
    {
      no: 74, yakin: 2.5, kamera: 10, sprite: { w: 540, h: 200, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Hattatlar, nakkaşlar,", "müzehhipler."], sure: 3.26 },
      ],
    },
    {
      no: 75, yakin: 2.5, kamera: 20, sprite: { w: 540, h: 170, fps: 12, x: [240, 300], taban: 634 },
      yazilar: [
        { satirlar: ["Baysungur", "37 yaşında öldü"], sure: 3.88, renk: KIZIL },
      ],
    },
    {
      no: 76, yakin: 2.2, kamera: 30, sprite: { w: 300, h: 170, fps: 16, x: [230, 300], taban: 630 },
      yazilar: [
        { satirlar: ["Sarayda tuhaf", "bir şehzade beliriyor"], sure: 4.02 },
      ],
    },
    {
      no: 77, yakin: 2.5, kamera: 10, sprite: { w: 540, h: 190, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ona \"Kalender\"", "diyorlar"], sure: 2.27, renk: ALTIN },
      ],
    },
    {
      no: 78, yakin: 2.2, kamera: 20, sprite: { w: 540, h: 170, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["İlk kapıda", "misliyle ver"], sure: 2.42, renk: ALTIN },
      ],
    },
    {
      no: 79, yakin: 2.5, kamera: 20, sprite: { w: 540, h: 170, fps: 12, x: [300, 250], taban: 634 },
      yazilar: [
        { satirlar: ["Taht boşaldı"], sure: 1.10, renk: KIZIL },
      ],
    },
    {
      no: 80, yakin: 2.2, kamera: 40, sprite: { w: 540, h: 160, fps: 18, x: [220, 300], taban: 632 },
      yazilar: [
        { satirlar: ["Derviş ordu topluyor", "ve Herat'a giriyor"], sure: 5.32 },
        { satirlar: ["Dervişin elinde", "kılıç"], sure: 1.76, renk: KIZIL },
      ],
    },
    {
      no: 81, yakin: 2.5, kamera: 10, sprite: { w: 440, h: 200, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kılıçla yakışmayan", "iki satır…"], sure: 3.21, renk: ALTIN },
      ],
    },
    {
      no: 82, yakin: 2.2, kamera: 20, sprite: { w: 380, h: 170, fps: 10, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["O ay parçası gibi güzel yüze", "âşık olmayan her gönül,", "sana gönül denmez;"], sure: 8.25 },
        { satirlar: ["çünkü taş parçasından", "geri kalır yanın yok."], sure: 4.78 },
      ],
    },
    {
      no: 83, yakin: 2.4, kamera: 20, sprite: { w: 300, h: 170, fps: 12, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["Dedim: Ey sevgili,", "senin gamının karşısında", "ne yapayım?"], sure: 6.54 },
        { satirlar: ["Dedi: Burada öldürülmekten", "başka hiçbir çare yok."], sure: 5.60, renk: KIZIL },
      ],
    },
    {
      no: 84, yakin: 2.2, kamera: 25, sprite: { w: 540, h: 170, fps: 10, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["Nevruz, ilkbahar, gül,", "kadeh ve dilberler…"], sure: 4.46 },
        { satirlar: ["Dünyaya ikinci kez gelinmediği", "için hayatı güzel yaşa."], sure: 6.44, renk: ALTIN },
      ],
    },
    {
      no: 85, yakin: 2.5, kamera: 10, sprite: { w: 440, h: 190, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Zamanımızın eski", "süvarilerinden biri meydir;"], sure: 5.69 },
        { satirlar: ["her vakit durmaksızın nefes", "isteyip kabul eden", "şey nedir?"], sure: 6.50 },
      ],
    },
    {
      no: 86, yakin: 2.2, kamera: 15, sprite: { w: 400, h: 170, fps: 10, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["İyilerin keman kaşları niçin", "siyahtır, bilir misin?"], sure: 6.56 },
        { satirlar: ["Çünkü onların gönül", "dumanının köşelerinden", "halk güç almaktadır."], sure: 7.23 },
      ],
    },
    {
      no: 87, yakin: 2.2, kamera: 30, sprite: { w: 440, h: 170, fps: 10, x: [230, 300], taban: 630 },
      yazilar: [
        { satirlar: ["Bâbür, senin ağlayıp inlemen", "sevgilinin kulağına ulaştı;"], sure: 7.00 },
        { satirlar: ["Mecnun'un bu hay içinde", "olmasından", "Leyla haberdar oldu"], sure: 6.21, renk: ALTIN },
      ],
    },
    {
      no: 88, yakin: 2.5, kamera: 10, sprite: { w: 540, h: 200, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bu satırları elinde kılıç", "tutan hükümdar yazdı."], sure: 5.70 },
        { satirlar: ["Burada öldürülmekten", "başka hiçbir çare yok"], sure: 5.37, renk: KIZIL },
        { satirlar: ["Dünyaya ikinci kez", "gelinmediği için", "hayatı güzel yaşa"], sure: 6.37, renk: ALTIN },
      ],
    },
    {
      no: 85, yakin: 2.8, kamera: 10, odakY: 560, sprite: { w: 440, h: 190, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kadeh:", "şarap mı, hakikat mi?"], sure: 3.43, renk: ALTIN },
        { satirlar: ["Şeriat kadeh,", "hakikat içindeki içki"], sure: 3.51 },
      ],
    },
    {
      no: 87, yakin: 2.2, kamera: 30, sprite: { w: 440, h: 170, fps: 10, x: [230, 300], taban: 630 },
      yazilar: [
        { satirlar: ["Leyla kim?", "İnsan mı, Hak mı?"], sure: 2.41, renk: ALTIN },
      ],
    },
    {
      no: 89, yakin: 2.3, kamera: 30, sprite: { w: 300, h: 150, fps: 12, x: [280, 235], taban: 632 },
      yazilar: [
        { satirlar: ["Sonra ölüyor."], sure: 1.68, renk: KIZIL },
        { satirlar: ["Kılıcıyla değil, şiirleri", "ve bir lakapla anılıyor:", "Kalender"], sure: 7.47, renk: ALTIN },
        { satirlar: ["Timur dünyayı kılıçla titretti,", "torunu geriye şiir bıraktı"], sure: 6.54 },
      ],
    },
  ],
  kapanis: {
    satirlar: ["Ermiş mi,", "şair mi?"],
    sonraki: "Sıradaki: Uluğ Bey mi, Baysungur mu?",
    sure: 9,
    arka: 89,
    gece: true,
  },
};

export const KAL_KARE = Math.round(seriSure(KALENDER) * T_FPS);
export const Kalender: React.FC = () => <SeriVideo seri={KALENDER} />;
