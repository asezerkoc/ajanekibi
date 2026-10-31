import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Cem Sultan'ın Zehirli Tıraşı (revize, 194 kelime): grafikerin tarifi (teslimler/2026-10-30-1652-...-reels.md), sahneler 90-121.
   Süreler ses/hizala_seri.py ile sese bağlanır. */
// Kapak: ajans sahibi görsel vermedi (kapak: alanı boş). Kapak, sahne 90 katmanlarıyla yapılan
// ilk Bolum'dur (2,5 sn, sessiz). Logo ve @pikseltarihim alt bandını kapak bileşeni ekler;
// yazılar ortadaki 3:4 alanda kalır. Sahne 104 kullanılmıyor.
// Süreler tahmini (≈120 sn); hizala_seri.py sese göre düzeltir.
export const CEM_SULTAN: Seri = {
  etiket: "PİKSEL TARİHİM · CEM SULTAN",
  ses: "cem-sultan-anlatim.mp3", // Mehmet - Warm tone (ElevenLabs), revize metin; kapak 2,5 sn kadar ötelendi
  bolumler: [
    { // KAPAK (hizala_seri bu bloğu atlar: kapak yazıları anlatımda yok)
      no: 90, yakin: 2.9, kamera: 0,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Cem Sultan'ın", "Zehirli Tıraşı", "Eve dönemeyen şehzade"], sure: 2.0, boy: 112, renk: ALTIN }, // kapak 2,5 sn (ses bu kadar ötelendi); başlık ve alt başlık birlikte
      ],
    },
    {
      no: 90, yakin: 2.9, kamera: 8,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Napoli, 1495."], sure: 2.67 },
        { satirlar: ["Rivayete göre bir berber", "şehzadeyi zehirli usturayla", "tıraş ediyor."], sure: 4.17, renk: KIZIL },
      ],
    },
    {
      no: 106, yakin: 3.2, kamera: 6,
      sprite: { w: 300, h: 260, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Tıraş olan adam,", "Fatih'in oğlu Cem."], sure: 2.08, renk: ALTIN },
      ],
    },
    {
      no: 107, yakin: 2.2, kamera: 8,
      sprite: { w: 360, h: 150, fps: 8, x: [215, 245], taban: 556 },
      yazilar: [
        { satirlar: ["Evi, denizin", "öbür yanında."], sure: 1.37 },
      ],
    },
    {
      no: 111, yakin: 3.2, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Babası ölünce Cem yirmi bir,", "yirmi iki yaşındadır."], sure: 3.03 },
      ],
    },
    {
      no: 91, yakin: 2.8, kamera: 10,
      sprite: { w: 420, h: 300, fps: 14, x: [280, 255], taban: 632 },
      yazilar: [
        { satirlar: ["Haziran 1481, Yenişehir.", "Kardeşi Bayezid'in orduları", "onu yener."], sure: 5.18, renk: KIZIL },
      ],
    },
    {
      no: 112, yakin: 2.8, kamera: 10,
      sprite: { w: 400, h: 300, fps: 14, x: [265, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Kahire'de Memlük Sultanı", "Kayıtbay'a sığınır."], sure: 3.81 },
      ],
    },
    {
      no: 113, yakin: 2.8, kamera: 10,
      sprite: { w: 420, h: 300, fps: 14, x: [255, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Anadolu'ya döner,", "bir kez daha dener."], sure: 1.81 },
      ],
    },
    {
      no: 114, yakin: 2.8, kamera: 10,
      sprite: { w: 420, h: 300, fps: 12, x: [285, 250], taban: 632 },
      yazilar: [
        { satirlar: ["Yine yenilir."], sure: 0.90, renk: KIZIL },
      ],
    },
    {
      no: 92, yakin: 2.2, kamera: 10,
      sprite: { w: 420, h: 300, fps: 10, x: [262, 272], taban: 632 },
      yazilar: [
        { satirlar: ["Sonra Rodos. Şövalyelere", "sığınır, gemiye biner."], sure: 2.48 },
      ],
    },
    {
      no: 115, yakin: 2.4, kamera: 10,
      sprite: { w: 420, h: 300, fps: 10, x: [290, 230], taban: 632 },
      yazilar: [
        { satirlar: ["Gemi Fransa'ya gider."], sure: 0.90 },
      ],
    },
    {
      no: 116, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bourganeuf'te onun için", "bir kule yapılır."], sure: 2.97 },
      ],
    },
    {
      no: 117, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bugün de ayakta:", "Zizim Kulesi."], sure: 0.94, renk: ALTIN },
      ],
    },
    {
      no: 93, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 14, x: [285, 255], taban: 634 },
      yazilar: [
        { satirlar: ["Rodos, Fransa, Roma.", "Elden ele, yaklaşık", "on üç yıl."], sure: 3.44, renk: ALTIN },
      ],
    },
    {
      no: 94, yakin: 3.2, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kimse onu", "eve göndermez."], sure: 1.29, renk: KIZIL },
      ],
    },
    {
      no: 118, yakin: 3.2, kamera: 6,
      sprite: { w: 400, h: 300, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Siz olsanız", "dayanabilir miydiniz?"], sure: 2.39, renk: ALTIN },
      ],
    },
    {
      no: 108, yakin: 3.2, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Kardeşi Bayezid tahtta.", "Cem hâlâ Papa'nın elinde."], sure: 2.78 },
      ],
    },
    {
      no: 119, yakin: 2.8, kamera: 10,
      sprite: { w: 420, h: 300, fps: 14, x: [330, 250], taban: 632 },
      yazilar: [
        { satirlar: ["O sırada Roma'ya", "bir hediye gelir."], sure: 2.41 },
      ],
    },
    {
      no: 97, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ama o hediye Cem'e değil,", "Papa'ya."], sure: 1.22, renk: ALTIN },
      ],
    },
    {
      no: 96, yakin: 3.2, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["31 Mayıs 1492."], sure: 3.47, renk: ALTIN },
        { satirlar: ["Papa'nın tören ustası", "Burchard yazar:"], sure: 2.19 },
      ],
    },
    {
      no: 109, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["İsa'yı deldiğine inanılan", "Kutsal Mızrak", "Roma'ya geliyor."], sure: 3.16, renk: ALTIN },
      ],
    },
    {
      no: 95, yakin: 2.8, kamera: 14,
      sprite: { w: 420, h: 300, fps: 22, x: [335, 255], taban: 632 },
      yazilar: [
        { satirlar: ["Gönderen Bayezid.", "Alan, kardeşini elinde", "tutan Papa."], sure: 3.60 },
      ],
    },
    {
      no: 120, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Hediye mi, pazarlık mı?", "Bilmiyoruz."], sure: 2.27, renk: ALTIN },
      ],
    },
    {
      no: 98, yakin: 2.8, kamera: 10,
      sprite: { w: 420, h: 300, fps: 14, x: [285, 255], taban: 632 },
      yazilar: [
        { satirlar: ["Ocak 1495. Papa, Cem'i", "Fransa Kralı'na teslim eder."], sure: 4.39 },
      ],
    },
    {
      no: 121, yakin: 2.8, kamera: 10,
      sprite: { w: 420, h: 300, fps: 14, x: [285, 255], taban: 632 },
      yazilar: [
        { satirlar: ["Yabancı ordu, yabancı şehir:", "Napoli."], sure: 1.62, renk: KIZIL },
      ],
    },
    {
      no: 99, yakin: 2.8, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Yaklaşık dört hafta sonra", "Cem ölür."], sure: 2.36, renk: KIZIL },
      ],
    },
    {
      no: 110, yakin: 2.8, kamera: 8,
      sprite: { w: 420, h: 300, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Naaşı yıllar sonra", "Bursa'ya döner."], sure: 2.50 },
        { satirlar: ["Eve ancak ölü döner."], sure: 0.93, renk: ALTIN }, // ana motif: mor gökte kızıl okunmuyordu
      ],
    },
    {
      no: 100, yakin: 3.2, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Peki ustura?"], sure: 1.22, renk: ALTIN },
        { satirlar: ["Guicciardini zehir der."], sure: 1.35 },
        { satirlar: ["Olaydan yaklaşık kırk yıl", "sonra yazar."], sure: 2.47 },
      ],
    },
    {
      no: 101, yakin: 3.2, kamera: 6,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Burchard zehirden", "söz etmez."], sure: 2.15 },
        { satirlar: ["Napoli'de değildi."], sure: 0.90 },
      ],
    },
    {
      no: 102, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 9, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["İnalcık gibi tarihçiler", "hastalık der."], sure: 2.36, renk: ALTIN },
      ],
    },
    {
      no: 103, yakin: 2.8, kamera: 8,
      sprite: { w: 400, h: 300, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Ustura için dönem belgesi", "gösterilemiyor."], sure: 3.59 },
        { satirlar: ["Belgeler zehiri", "kanıtlamıyor."], sure: 1.63, renk: ALTIN },
      ],
    },
    {
      no: 105, yakin: 2.9, kamera: 8,
      sprite: { w: 400, h: 300, fps: 6, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Sizce o ustura", "zehirli miydi?"], sure: 2.47, renk: ALTIN },
      ],
    },
  ],
  kapanis: {
    satirlar: ["Piksel Tarih", "@pikseltarihim"],
    sonraki: "Yorumlara yaz, arkadaşına gönder",
    sure: 3, arka: 105, gece: true,
  },
};

export const CEM_KARE = Math.round(seriSure(CEM_SULTAN) * T_FPS);
export const CemSultan: React.FC = () => <SeriVideo seri={CEM_SULTAN} />;
