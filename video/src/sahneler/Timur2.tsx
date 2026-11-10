import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Timur 2. bölüm "İki Yıldırım" (1370-1403). Ekran yazıları ekibin onaylı seslendirme metniyle (150 kelime)
   bire birdir. Mektup replikleri Osmanlı mecmualarındaki metinlerden (Daş 2004); sahihlikleri tartışmalı
   olduğu için "mecmualara göre" diye verilir. Ses gelince süreler sese hizalanır. */
export const TIMUR2: Seri = {
  etiket: "PİKSEL TARİHİM · TİMUR 2/3",
  ses: "timur-2-anlatim.mp3",
  kapak: "timur-2-kapak.png",
  bolumler: [
    {
      no: 31, yakin: 1.9, sarsinti: 2, sprite: { w: 520, h: 160, fps: 24, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Toktamış ihanet etti,", "Altın Orda yenildi."], sure: 2.97, renk: ALTIN },
      ],
    },
    {
      no: 32, yakin: 1.9, sprite: { w: 520, h: 170, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["İsfahan'da kafa kuleleri…"], sure: 1.26, renk: KIZIL },
      ],
    },
    {
      no: 33, yakin: 1.9, sarsinti: 2, sprite: { w: 520, h: 200, fps: 18, x: [285, 245], taban: 632 },
      yazilar: [
        { satirlar: ["…Delhi'de filler."], sure: 1.00 },
      ],
    },
    {
      no: 30, yakin: 1.8, kamera: 40, sprite: { w: 520, h: 170, fps: 12, x: 245, taban: 632 },
      yazilar: [
        { satirlar: ["Teslim olan şehir yaşadı,", "direnen şehir kule oldu."], sure: 2.74, boy: 72, renk: ALTIN },
      ],
    },
    {
      no: 46, yakin: 1.8, kamera: 10, sprite: { w: 360, h: 170, fps: 12, x: 262, taban: 632 },
      yazilar: [
        { satirlar: ["Kara Yusuf ile Ahmed Celayir", "Bayezid'e sığındı;"], sure: 3.58 },
      ],
    },
    {
      no: 34, yakin: 2.4, kamera: 70, sprite: { w: 260, h: 140, fps: 30, x: [330, 210], taban: 632 },
      yazilar: [
        { satirlar: ["Timur teslimlerini istedi."], sure: 1.61, renk: ALTIN },
      ],
    },
    {
      no: 35, yakin: 2.2, sprite: { w: 320, h: 190, fps: 12, x: 250, taban: 632 },
      yazilar: [
        { satirlar: ["Mektuplarda, mecmualara göre,", "“Ey ihtiyar köpek” ve", "“kaçanın karısı üç talakla", "boş olsun” geçer."], sure: 5.94, boy: 66, renk: ALTIN },
      ],
    },
    {
      no: 36, yakin: 2.1, sprite: { w: 520, h: 200, fps: 14, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sivas, 1400: lağımlar,", "“kan dökülmeyecek” sözü."], sure: 3.86, renk: ALTIN },
      ],
    },
    {
      no: 37, yakin: 1.9, sprite: { w: 520, h: 204, fps: 12, x: 262, taban: 668 },
      yazilar: [
        { satirlar: ["Bir kronikçiye göre", "savunucular", "diri diri gömüldü."], sure: 3.84, renk: KIZIL },
      ],
    },
    {
      no: 38, yakin: 2.0, sprite: { w: 520, h: 172, fps: 10, x: 230, taban: 654 },
      yazilar: [
        { satirlar: ["Ankara, 28 Temmuz 1402."], sure: 3.84, renk: ALTIN },
        { satirlar: ["Kaynaklara göre çay kesildi,", "Osmanlı susuz kaldı."], sure: 3.25, boy: 72 },
      ],
    },
    {
      no: 39, yakin: 1.7, sarsinti: 3, sprite: { w: 520, h: 170, fps: 26, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Tatarlar saf değiştirdi."], sure: 1.42, renk: ALTIN },
      ],
    },
    {
      no: 40, yakin: 2.0, sprite: { w: 520, h: 170, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bayezid esir düştü;", "ilk esir Osmanlı hükümdarı."], sure: 3.07, renk: KIZIL },
      ],
    },
    {
      no: 41, yakin: 2.4, sprite: { w: 520, h: 220, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Rivayete göre ziyafette", "Despina Hatun şarap sundu."], sure: 3.44, renk: ALTIN },
      ],
    },
    {
      no: 42, yakin: 1.9, sprite: { w: 520, h: 200, fps: 14, x: 262, taban: 632 },
      yazilar: [
        { satirlar: ["İzmir kalesi iki haftada düştü;", "rivayete göre gemilere", "kesik başlar fırlatıldı."], sure: 5.63 },
      ],
    },
    {
      no: 43, yakin: 2.0, kamera: 50, sprite: { w: 520, h: 170, fps: 14, x: [240, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Efsaneye göre Bayezid", "demir kafeste taşındı;"], sure: 3.48 },
        { satirlar: ["muhtemelen kafesli", "tahtırevandı."], sure: 2.15, renk: ALTIN },
      ],
    },
    {
      no: 44, yakin: 2.0, kamera: 0, sprite: { w: 400, h: 140, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["1403'te Akşehir'de", "esirken öldü."], sure: 3.61, renk: KIZIL },
      ],
    },
    {
      no: 54, yakin: 2.0, kamera: 10, sprite: { w: 270, h: 200, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Yıldırım'ı yenen adam", "68 yaşındaydı;"], sure: 2.96 },
        { satirlar: ["göz kapakları düşmüştü,"], sure: 1.12 },
      ],
    },
    {
      no: 45, yakin: 2.3, kamera: 40, sprite: { w: 300, h: 150, fps: 12, x: [290, 250], taban: 632 },
      yazilar: [
        { satirlar: ["bacağını sürüyordu."], sure: 1.48 },
        { satirlar: ["Ama hâlâ bir hedefi vardı:"], sure: 2.13 },
        { satirlar: ["ÇİN."], sure: 1.10, boy: 150, renk: ALTIN },
      ],
    },
  ],
  kapanis: {
    satirlar: ["Timur · 2/3 · İki Yıldırım"],
    sonraki: "Bölüm 3'ü kaçırma · Takip et",
    sure: 3.0,
    arka: 45,
  },
};

export const T2_KARE = Math.round(seriSure(TIMUR2) * T_FPS);
export const Timur2: React.FC = () => <SeriVideo seri={TIMUR2} />;
