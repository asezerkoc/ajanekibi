import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Timur 2. bölüm "İki Yıldırım" (1370-1403). Ekran yazıları ekibin onaylı seslendirme metniyle (150 kelime)
   bire birdir. Mektup replikleri Osmanlı mecmualarındaki metinlerden (Daş 2004); sahihlikleri tartışmalı
   olduğu için "mecmualara göre" diye verilir. Ses gelince süreler sese hizalanır. */
export const TIMUR2: Seri = {
  etiket: "PİKSEL TARİHİM · TİMUR 2/3",
  bolumler: [
    {
      no: 31, yakin: 1.9, sarsinti: 2, sprite: { w: 520, h: 160, fps: 24, x: 270, taban: 632 },
      yazilar: [{ satirlar: ["Toktamış ihanet etti,", "Altın Orda yenildi."], sure: 2.5, renk: ALTIN }],
    },
    {
      no: 32, yakin: 1.9, sprite: { w: 520, h: 170, fps: 12, x: 270, taban: 632 },
      yazilar: [{ satirlar: ["İsfahan'da kafa kuleleri…"], sure: 1.9, renk: KIZIL }],
    },
    {
      no: 33, yakin: 1.9, sarsinti: 2, sprite: { w: 520, h: 200, fps: 18, x: [285, 245], taban: 632 },
      yazilar: [{ satirlar: ["…Delhi'de filler (1398)."], sure: 1.8 }],
    },
    {
      no: 30, yakin: 1.9, kamera: -240, sprite: { w: 520, h: 170, fps: 12, x: 262, taban: 632 },
      yazilar: [{ satirlar: ["Teslim olan şehir yaşadı,", "direnen şehir kule oldu."], sure: 2.7, renk: ALTIN, boy: 72 }],
    },
    {
      no: 46, yakin: 1.9, kamera: 20, sprite: { w: 360, h: 170, fps: 12, x: 270, taban: 632 },
      yazilar: [{ satirlar: ["Kara Yusuf ile", "Ahmed Celayir,", "Yıldırım Bayezid'e", "sığındı."], sure: 2.8 }],
    },
    {
      no: 34, yakin: 2.4, kamera: 70, sprite: { w: 260, h: 140, fps: 30, x: [330, 210], taban: 632 },
      yazilar: [{ satirlar: ["Timur teslimlerini istedi."], sure: 2.6, renk: ALTIN }],
    },
    {
      no: 35, yakin: 2.2, sprite: { w: 320, h: 190, fps: 12, x: 250, taban: 632 },
      yazilar: [
        { satirlar: ["Mektuplarda, mecmualara göre,", "“Ey ihtiyar köpek” ve", "“kaçanın karısı üç talakla", "boş olsun” geçer."], sure: 5.0, renk: ALTIN, boy: 66 },
      ],
    },
    {
      no: 36, yakin: 2.1, sprite: { w: 520, h: 200, fps: 14, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sivas, Ağustos 1400:", "lağımlar, yakılan kirişler,"], sure: 2.5, renk: ALTIN },
        { satirlar: ["“kan dökülmeyecek” sözü."], sure: 1.8 },
      ],
    },
    {
      no: 37, yakin: 1.9, sprite: { w: 520, h: 204, fps: 12, x: 262, taban: 668 },
      yazilar: [
        { satirlar: ["Bir kronikçiye göre", "savunucular", "diri diri gömüldü."], sure: 2.8, renk: KIZIL },
        { satirlar: ["3-4 bin kadar; çoğu Ermeni."], sure: 1.6, boy: 76 },
      ],
    },
    {
      no: 38, yakin: 2.0, sprite: { w: 520, h: 166, fps: 10, x: 230, taban: 648 },
      yazilar: [
        { satirlar: ["Ankara, 28 Temmuz 1402."], sure: 1.8, renk: ALTIN },
        { satirlar: ["Kaynaklara göre çay kesildi,", "Osmanlı susuz kaldı."], sure: 2.6, boy: 72 },
      ],
    },
    {
      no: 39, yakin: 1.7, sarsinti: 3, sprite: { w: 520, h: 170, fps: 26, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Tatarlar saf değiştirdi."], sure: 1.7, renk: ALTIN },
        { satirlar: ["Anlatılara göre Sırp süvarisi", "üç kez hücum etti."], sure: 2.6 },
      ],
    },
    {
      no: 40, yakin: 2.0, sprite: { w: 520, h: 170, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bayezid dağlarda kuşatılıp", "esir düştü;"], sure: 2.2 },
        { satirlar: ["ilk esir Osmanlı hükümdarı."], sure: 1.8, renk: KIZIL },
      ],
    },
    {
      no: 41, yakin: 2.4, sprite: { w: 520, h: 220, fps: 12, x: 270, taban: 632 },
      yazilar: [{ satirlar: ["Rivayete göre ziyafette", "Despina Hatun şarap sundu."], sure: 2.6, renk: ALTIN }],
    },
    {
      no: 42, yakin: 1.9, sprite: { w: 520, h: 200, fps: 14, x: 262, taban: 632 },
      yazilar: [
        { satirlar: ["Bayezid'in yıllarca alamadığı", "İzmir kalesi iki haftada düştü."], sure: 3.0, renk: ALTIN },
        { satirlar: ["Rivayete göre gemilere", "kesik başlar fırlatıldı."], sure: 2.4 },
      ],
    },
    {
      no: 43, yakin: 2.0, kamera: 50, sprite: { w: 520, h: 170, fps: 14, x: [240, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Efsaneye göre Bayezid", "demir kafeste taşındı;"], sure: 2.2 },
        { satirlar: ["muhtemelen kafesli", "tahtırevandı."], sure: 1.8, renk: ALTIN },
      ],
    },
    {
      no: 44, yakin: 2.0, kamera: 0, sprite: { w: 400, h: 140, fps: 8, x: 270, taban: 634 },
      yazilar: [{ satirlar: ["Bayezid, 8 Mart 1403'te", "Akşehir'de esirken öldü."], sure: 2.6, renk: KIZIL }],
    },
    {
      no: 54, yakin: 2.0, kamera: 10, sprite: { w: 270, h: 200, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Yıldırım'ı yenen adam artık", "yaklaşık 68 yaşındaydı;"], sure: 2.4 },
        { satirlar: ["göz kapakları düşmüştü,"], sure: 1.4 },
      ],
    },
    {
      no: 45, yakin: 2.3, kamera: 40, sprite: { w: 300, h: 150, fps: 12, x: [290, 250], taban: 632 },
      yazilar: [
        { satirlar: ["bacağını sürüyordu."], sure: 1.4 },
        { satirlar: ["Ama hâlâ bir hedefi vardı:"], sure: 1.6 },
        { satirlar: ["ÇİN."], sure: 1.3, boy: 150, renk: ALTIN },
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
