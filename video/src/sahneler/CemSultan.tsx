import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Cem Sultan'ın Zehirli Tıraşı: grafikerin tarifi (teslimler/2026-10-30-1652-...-reels.md), sahneler 90-105.
   Seslendirme gelince süreler ses/hizala_seri.py ile sese bağlanır. */
// Kapak: ajans sahibi görsel vermedi (kapak: alanı boş). Kapak, sahne 72 katmanlarıyla yapılan
// ilk Bolum'dur (2,5 sn, sessiz). Logo ve @pikseltarihim alt bandını kapak bileşeni ekler.
// Sahne 72 ikinci kez, seslendirmeyle birlikte oynar.
export const CEM_SULTAN: Seri = {
  etiket: "PİKSEL TARİHİM · CEM SULTAN",
  ses: "cem-sultan-anlatim.mp3", // Mehmet - Warm tone (ElevenLabs), 2. kayıt; kapak 2,5 sn kadar ötelendi
  bolumler: [
    { // KAPAK
      no: 90, yakin: 2.4, kamera: 0, odakY: 590,
      sprite: { w: 440, h: 170, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Cem Sultan'ın", "Zehirli Tıraşı"], sure: 1.2, boy: 120, renk: ALTIN },
        { satirlar: ["O ustura gerçekten", "zehirli miydi?"], sure: 0.8, renk: KIZIL },
      ],
    },
    {
      no: 90, yakin: 2.4, kamera: 14, odakY: 590,
      sprite: { w: 440, h: 170, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Napoli, 1495.", "Bir berber şehzadeyi", "tıraş ediyor."], sure: 4.87 },
        { satirlar: ["Rivayete göre", "ustura zehirli."], sure: 1.85, renk: KIZIL },
      ],
    },
    {
      no: 91, yakin: 2.0, kamera: 30,
      sprite: { w: 520, h: 160, fps: 14, x: [235, 300], taban: 632 },
      yazilar: [
        { satirlar: ["Koltuktaki adam,", "Fatih'in oğlu Cem."], sure: 1.90 },
        { satirlar: ["Kardeşi Bayezid'e", "taht savaşında yenilir,"], sure: 2.45, renk: KIZIL },
      ],
    },
    {
      no: 92, yakin: 1.7, kamera: 40,
      sprite: { w: 540, h: 170, fps: 12, x: [330, 270], taban: 632 },
      yazilar: [
        { satirlar: ["Rodos'a sığınır."], sure: 1.45 },
        { satirlar: ["Şövalyeler onu Fransa'ya,", "sonra Roma'ya gönderir."], sure: 2.53 },
      ],
    },
    {
      no: 93, yakin: 1.9, kamera: 40,
      sprite: { w: 540, h: 170, fps: 14, x: [255, 285], taban: 634 },
      yazilar: [
        { satirlar: ["Elden ele,", "yaklaşık on üç yıl."], sure: 1.46 },
        { satirlar: ["Siz olsanız", "dayanır mıydınız?"], sure: 2.09, renk: ALTIN },
      ],
    },
    {
      no: 94, yakin: 2.3, kamera: 10,
      sprite: { w: 300, h: 170, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Umudu sultan kardeşi."], sure: 1.52 },
        { satirlar: ["Ama Bayezid kurtarmaz."], sure: 0.90, renk: KIZIL },
      ],
    },
    {
      no: 95, yakin: 2.0, kamera: 50,
      sprite: { w: 420, h: 170, fps: 22, x: [330, 210], taban: 632 },
      yazilar: [
        { satirlar: ["Roma'ya hediye yollar."], sure: 1.96 },
        { satirlar: ["31 Mayıs 1492."], sure: 2.45, renk: ALTIN },
      ],
    },
    {
      no: 96, yakin: 2.1, kamera: 10,
      sprite: { w: 400, h: 170, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Papa'nın tören ustası", "Burchard günlüğüne yazar:"], sure: 3.69 },
        { satirlar: ["İsa'yı deldiğine inanılan", "Kutsal Mızrak", "Roma'ya geliyor."], sure: 3.21, renk: ALTIN },
      ],
    },
    {
      no: 97, yakin: 1.9, kamera: 20,
      sprite: { w: 520, h: 170, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Gönderen kardeşi.", "Alan, onu elinde tutan Papa."], sure: 3.07 },
        { satirlar: ["Hediye mi, pazarlık mı?", "Bilmiyoruz."], sure: 1.73, renk: ALTIN },
      ],
    },
    {
      no: 98, yakin: 1.8, kamera: 30,
      sprite: { w: 500, h: 170, fps: 14, x: [250, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Ocak 1495.", "Papa, Cem'i Fransa Kralı'na", "teslim eder."], sure: 4.28 },
      ],
    },
    {
      no: 99, yakin: 2.1, kamera: 10,
      sprite: { w: 300, h: 170, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Yaklaşık dört hafta sonra", "Cem ölür."], sure: 1.95, renk: KIZIL },
      ],
    },
    {
      no: 100, yakin: 2.2, kamera: 10,
      sprite: { w: 420, h: 170, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Peki ustura?"], sure: 0.90, renk: ALTIN },
        { satirlar: ["Guicciardini zehir der,", "ama yaklaşık kırk yıl sonra", "yazar."], sure: 3.50 },
      ],
    },
    {
      no: 101, yakin: 2.1, kamera: 10,
      sprite: { w: 340, h: 170, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Burchard zehirden", "söz etmez."], sure: 1.53 },
      ],
    },
    {
      no: 102, yakin: 2.2, kamera: 14,
      sprite: { w: 300, h: 170, fps: 9, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["İnalcık gibi tarihçiler", "hastalık der."], sure: 2.20, renk: ALTIN },
      ],
    },
    {
      no: 103, yakin: 1.8, kamera: 10,
      sprite: { w: 440, h: 170, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Belgeler zehiri", "kanıtlamıyor."], sure: 2.68, renk: ALTIN },
        { satirlar: ["Ustura için dönem belgesi", "gösterilemiyor;"], sure: 2.14 },
      ],
    },
    {
      no: 104, yakin: 2.0, kamera: 20,
      sprite: { w: 380, h: 150, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["ayrıntı halk anlatısında", "geçer."], sure: 1.71 },
      ],
    },
    {
      no: 105, yakin: 2.4, kamera: 10, odakY: 590,
      sprite: { w: 440, h: 170, fps: 6, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Sizce o ustura", "zehirli miydi?"], sure: 2.51, renk: ALTIN },
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
