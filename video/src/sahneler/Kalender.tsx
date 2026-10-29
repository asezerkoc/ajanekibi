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
      no: 72, yakin: 2.6, kamera: 10, sprite: { w: 540, h: 200, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Hükümdar mı,", "derviş mi?"], sure: 8.19, renk: ALTIN },
        { satirlar: ["Bir elinde kılıç,", "öbüründe şiir."], sure: 2.23 },
      ],
    },
    {
      no: 73, yakin: 2.2, kamera: 20, sprite: { w: 540, h: 170, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Timur'un kanı,", "Baysungur'un kalemi"], sure: 13.82, renk: ALTIN },
      ],
    },
    {
      no: 74, yakin: 2.3, kamera: 10, sprite: { w: 540, h: 200, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Hattatlar, nakkaşlar,", "müzehhipler."], sure: 6.21 },
      ],
    },
    {
      no: 75, yakin: 2.5, kamera: 20, sprite: { w: 540, h: 170, fps: 12, x: [240, 300], taban: 634 },
      yazilar: [
        { satirlar: ["Baysungur", "37 yaşında öldü"], sure: 3.74, renk: KIZIL },
      ],
    },
    {
      no: 76, yakin: 2.2, kamera: 30, sprite: { w: 300, h: 170, fps: 16, x: [230, 300], taban: 630 },
      yazilar: [
        { satirlar: ["Sarayda tuhaf", "bir şehzade beliriyor"], sure: 9.90 },
      ],
    },
    {
      no: 77, yakin: 2.6, kamera: 10, sprite: { w: 540, h: 190, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ona \"Kalender\"", "diyorlar"], sure: 2.71, renk: ALTIN },
      ],
    },
    {
      no: 78, yakin: 2.2, kamera: 20, sprite: { w: 540, h: 170, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["İlk kapıda", "misliyle ver"], sure: 9.61, renk: ALTIN },
      ],
    },
    {
      no: 79, yakin: 2.5, kamera: 20, sprite: { w: 540, h: 170, fps: 12, x: [300, 250], taban: 634 },
      yazilar: [
        { satirlar: ["Taht boşaldı"], sure: 4.59, renk: KIZIL },
      ],
    },
    {
      no: 80, yakin: 2.2, kamera: 20, sprite: { w: 540, h: 160, fps: 18, x: [255, 268], taban: 632 },
      yazilar: [
        { satirlar: ["Derviş ordu topluyor", "ve Herat'a giriyor"], sure: 7.79 },
        { satirlar: ["Dervişin elinde", "kılıç"], sure: 1.15, renk: KIZIL },
      ],
    },
    {
      no: 81, yakin: 2.6, kamera: 10, sprite: { w: 440, h: 200, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kılıçla yakışmayan", "iki satır…"], sure: 3.38, renk: ALTIN },
      ],
    },
    {
      no: 82, yakin: 2.2, kamera: 20, yaziY: 740, sprite: { w: 380, h: 170, fps: 10, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["O ay parçası gibi güzel yüze", "âşık olmayan her gönül,", "sana gönül denmez;"], sure: 5.25 },
        { satirlar: ["çünkü taş parçasından", "geri kalır yanın yok."], sure: 2.49 },
      ],
    },
    {
      no: 83, yakin: 2.4, kamera: 20, sprite: { w: 300, h: 170, fps: 12, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["Dedim: Ey sevgili,", "senin gamının karşısında", "ne yapayım?"], sure: 4.29 },
        { satirlar: ["Dedi: Burada öldürülmekten", "başka hiçbir çare yok."], sure: 3.36, renk: KIZIL },
      ],
    },
    {
      no: 84, yakin: 2.2, kamera: 25, sprite: { w: 540, h: 170, fps: 10, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["Nevruz, ilkbahar, gül,", "kadeh ve dilberler…"], sure: 2.48 },
        { satirlar: ["Dünyaya ikinci kez gelinmediği", "için hayatı güzel yaşa."], sure: 3.19, renk: ALTIN },
      ],
    },
    {
      no: 85, yakin: 2.6, kamera: 10, sprite: { w: 440, h: 190, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Zamanımızın eski", "süvarilerinden biri meydir;"], sure: 3.33 },
        { satirlar: ["her vakit durmaksızın nefes", "isteyip kabul eden", "şey nedir?"], sure: 3.61 },
      ],
    },
    {
      no: 86, yakin: 2.2, kamera: 15, yaziY: 740, sprite: { w: 400, h: 170, fps: 10, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["İyilerin keman kaşları niçin", "siyahtır, bilir misin?"], sure: 4.63 },
        { satirlar: ["Çünkü onların gönül", "dumanının köşelerinden", "halk güç almaktadır."], sure: 3.67 },
      ],
    },
    {
      no: 87, yakin: 2.2, kamera: 30, sprite: { w: 440, h: 170, fps: 10, x: [230, 300], taban: 630 },
      yazilar: [
        { satirlar: ["Bâbür, senin ağlayıp inlemen", "sevgilinin kulağına ulaştı;"], sure: 4.04 },
        { satirlar: ["Mecnun'un bu hay içinde", "olmasından", "Leyla haberdar oldu"], sure: 3.44, renk: ALTIN },
      ],
    },
    {
      no: 88, yakin: 2.6, kamera: 10, sprite: { w: 540, h: 200, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Bu satırları elinde kılıç", "tutan hükümdar yazdı."], sure: 4.47 },
        { satirlar: ["Burada öldürülmekten", "başka hiçbir çare yok"], sure: 4.96, renk: KIZIL },
        { satirlar: ["Dünyaya ikinci kez", "gelinmediği için", "hayatı güzel yaşa"], sure: 4.29, renk: ALTIN },
      ],
    },
    {
      no: 85, yakin: 3.0, kamera: 10, odakY: 560, sprite: { w: 440, h: 190, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kadeh:", "şarap mı, hakikat mi?"], sure: 2.47, renk: ALTIN },
        { satirlar: ["Şeriat kadeh,", "hakikat içindeki içki"], sure: 5.30 },
      ],
    },
    {
      no: 87, yakin: 2.2, kamera: 30, sprite: { w: 440, h: 170, fps: 10, x: [230, 300], taban: 630 },
      yazilar: [
        { satirlar: ["Leyla kim?", "İnsan mı, Hak mı?"], sure: 8.57, renk: ALTIN },
      ],
    },
    {
      no: 89, yakin: 2.3, kamera: 30, sprite: { w: 300, h: 150, fps: 12, x: [280, 235], taban: 632 },
      yazilar: [
        { satirlar: ["Sonra ölüyor."], sure: 1.20, renk: KIZIL },
        { satirlar: ["Kılıcıyla değil, şiirleri", "ve bir lakapla anılıyor:", "Kalender"], sure: 5.19, renk: ALTIN },
        { satirlar: ["Atası Timur dünyayı kılıçla", "titretti; torunu bir şehri", "alıp geriye şiir bıraktı"], sure: 5.17 },
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
