import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Timur 1. bölüm "Topal Kurt" (1336-1370). Ekran yazıları ekibin onaylı seslendirme metniyle (149 kelime)
   bire birdir; seslendirme gelince süreler sese hizalanır. Tartışmalılar "kroniklere / kaynaklara / rivayete
   göre" ve "düşman anlatısı" diye işaretli. */
export const TIMUR1: Seri = {
  etiket: "PİKSEL TARİHİM · TİMUR 1/3",
  ses: "timur-1-anlatim.mp3",
  kapak: "timur-1-kapak.png",
  bolumler: [
    {
      no: 21, yakin: 2.0, sprite: { w: 300, h: 180, fps: 16, x: 250, taban: 630 },
      yazilar: [
        { satirlar: ["Kroniklere göre 1336'da", "Hoca Ilgar köyünde", "Taragay'ın oğlu doğdu."], sure: 5.81, renk: ALTIN },
        { satirlar: ["Yaşı belki daha büyük."], sure: 1.34, boy: 80 },
      ],
    },
    {
      no: 22, yakin: 2.1, kamera: 50, sprite: { w: 420, h: 150, fps: 30, x: [200, 320], taban: 632 },
      yazilar: [
        { satirlar: ["Bozkırda çete kurdu;", "kaynaklara göre at ve", "koyun yağmalıyordu."], sure: 4.26 },
      ],
    },
    {
      no: 23, yakin: 2.0, sprite: { w: 520, h: 160, fps: 18, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["1360'ta Moğol hanı", "Tuğluk Timur saldırdı."], sure: 4.25, renk: ALTIN },
        { satirlar: ["Amcası kaçtı; Timur istilacıya", "bağlanıp Keş'in başına geçti."], sure: 3.37 },
      ],
    },
    {
      no: 24, yakin: 2.1, sprite: { w: 460, h: 170, fps: 16, x: 262, taban: 630 },
      yazilar: [
        { satirlar: ["Emir Hüseyin'le ittifak kurup", "kız kardeşiyle evlendi."], sure: 3.95, renk: ALTIN },
      ],
    },
    {
      no: 25, yakin: 1.9, sprite: { w: 440, h: 160, fps: 10, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["Sistan'da iki ok yedi:", "sağ dizine, sağ koluna."], sure: 3.18, renk: KIZIL },
        { satirlar: ["Artık", "Aksak Timur'du."], sure: 1.38, boy: 110, renk: ALTIN },
        { satirlar: ["İbn Arapşah koyun çalarken", "vurulduğunu yazar;", "düşman anlatısı."], sure: 4.52, boy: 80 },
      ],
    },
    {
      no: 26, yakin: 1.8, hava: 30, sarsinti: 2, sprite: { w: 520, h: 170, fps: 20, x: 250, taban: 632 },
      yazilar: [
        { satirlar: ["1365 Çamur Savaşı:", "sağanak, saplanan atlar."], sure: 4.65, renk: ALTIN },
        { satirlar: ["Timur yenildi."], sure: 0.90, boy: 110, renk: KIZIL },
      ],
    },
    {
      no: 27, yakin: 2.1, sprite: { w: 520, h: 160, fps: 16, x: 260, taban: 634 },
      yazilar: [
        { satirlar: ["Semerkant'ı Serbedarlar savundu;", "kaynaklara göre at salgını", "Moğolları çekilmeye zorladı."], sure: 5.95 },
      ],
    },
    {
      no: 28, yakin: 2.3, sprite: { w: 400, h: 170, fps: 14, x: [300, 235], taban: 632 },
      yazilar: [
        { satirlar: ["1370'te Belh'te Hüseyin,", "canı bağışlanacak sözüyle", "teslim oldu;"], sure: 6.32, renk: ALTIN },
        { satirlar: ["sonra öldürüldü."], sure: 0.90, boy: 110, renk: KIZIL },
        { satirlar: ["Timur'un rolü tartışmalı."], sure: 0.90, boy: 80 },
      ],
    },
    {
      no: 29, yakin: 2.3, sprite: { w: 400, h: 200, fps: 14, x: 230, taban: 632 },
      yazilar: [
        { satirlar: ["Cengiz soyundan Saray Mülk", "Hatun'la evlenip Gürkan,", "han damadı oldu;"], sure: 4.90 },
        { satirlar: ["tahta kukla han oturttu."], sure: 1.51, renk: ALTIN },
      ],
    },
    {
      no: 34, yakin: 2.4, kamera: 70, sprite: { w: 260, h: 140, fps: 30, x: [330, 210], taban: 632 },
      mektup: { metin: ["Otuz yıl sonra, batıdan…", "", "“Ey ihtiyar köpek…”"], imza: "" },
      yazilar: [
        { satirlar: ["Dünyanın yarısını fethedecekti", "ama kendine han diyemedi."], sure: 4.53, renk: ALTIN },
        { satirlar: ["Otuz yıl sonra bir sultan", "ona şöyle yazacaktı:"], sure: 3.33 },
        { satirlar: ["“Ey ihtiyar köpek…”"], sure: 1.73, boy: 110, renk: KIZIL },
      ],
    },
  ],
  kapanis: {
    satirlar: ["Timur · 1/3 · Topal Kurt"],
    sonraki: "Bölüm 2'yi takip et",
    sure: 3.5,
    arka: 34,
  },
};

export const T1_KARE = Math.round(seriSure(TIMUR1) * T_FPS);
export const Timur1: React.FC = () => <SeriVideo seri={TIMUR1} />;
