import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Timur 1. bölüm "Topal Kurt" (1336-1370). Sahne sırası araştırma raporundaki öneriyi izler;
   tartışmalı bilgiler ekranda "kroniklere göre / rivayete göre" diye işaretli. */
export const TIMUR1: Seri = {
  bolumler: [
    {
      no: 21, sprite: { w: 300, h: 180, fps: 16, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["8 Nisan 1336, Keş."], sure: 2.2, boy: 124, renk: ALTIN },
        { satirlar: ["Barlas boyundan Taragay'ın", "bir oğlu oldu: Timur."], sure: 3.2 },
        { satirlar: ["Kroniklere göre…", "Gerçek yaşı belki daha büyüktü."], sure: 3.0, boy: 76 },
      ],
    },
    {
      no: 22, yakin: 2.12, kamera: 50, sprite: { w: 420, h: 150, fps: 30, x: [200, 320], taban: 632 },
      yazilar: [
        { satirlar: ["Gençliğinde küçük bir", "çetenin başındaydı."], sure: 2.8 },
        { satirlar: ["At ve koyun", "yağmalıyordu."], sure: 2.4, renk: ALTIN },
      ],
    },
    {
      no: 23, yakin: 2.00, sprite: { w: 540, h: 160, fps: 18, x: [320, 230], taban: 632 },
      yazilar: [
        { satirlar: ["1360: Moğol hanı", "Tuğluk Timur geldi."], sure: 2.8, renk: ALTIN },
        { satirlar: ["Amcası kaçtı.", "Timur ise istilacıya bağlandı"], sure: 3.0 },
        { satirlar: ["ve Keş'in başına geçti."], sure: 2.2 },
      ],
    },
    {
      no: 24, yakin: 2.12, sprite: { w: 460, h: 170, fps: 16, x: 270, taban: 630 },
      yazilar: [
        { satirlar: ["Sonra Emir Hüseyin'le", "ittifak kurdu…"], sure: 2.6 },
        { satirlar: ["…kız kardeşi", "Olcay Türkan'la evlenerek."], sure: 3.0, renk: ALTIN },
      ],
    },
    {
      no: 25, yakin: 2.25, sprite: { w: 440, h: 160, fps: 10, x: 250, taban: 630 },
      yazilar: [
        { satirlar: ["Sistan, 1363 civarı."], sure: 2.0, renk: ALTIN },
        { satirlar: ["İki ok: biri sağ dizine,", "biri sağ eline."], sure: 2.8, renk: KIZIL },
        { satirlar: ["Artık adı", "Aksak Timur'du."], sure: 2.6, boy: 110, renk: ALTIN },
        { satirlar: ["1941'de iskeleti", "bunu doğruladı."], sure: 2.4, boy: 76 },
      ],
    },
    {
      no: 26, yakin: 2.25, hava: 30, sarsinti: 2, sprite: { w: 480, h: 160, fps: 20, x: 250, taban: 632 },
      yazilar: [
        { satirlar: ["1365, Çamur Savaşı."], sure: 2.2, renk: ALTIN },
        { satirlar: ["Sağanak ovayı", "bataklığa çevirdi."], sure: 2.6 },
        { satirlar: ["Timur ile Hüseyin", "ağır bir yenilgi aldı."], sure: 2.8, renk: KIZIL },
      ],
    },
    {
      no: 27, yakin: 2.12, sprite: { w: 480, h: 140, fps: 16, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Semerkant'ı onlar değil,", "halk milisi Serbedarlar", "savundu."], sure: 3.4 },
        { satirlar: ["Moğol atlarında salgın çıktı,", "ordu çekildi."], sure: 3.0, renk: ALTIN },
      ],
    },
    {
      no: 28, sprite: { w: 400, h: 170, fps: 14, x: [300, 235], taban: 632 },
      yazilar: [
        { satirlar: ["Olcay ölünce", "ittifak bitti."], sure: 2.4 },
        { satirlar: ["1370, Belh: Hüseyin, canı", "bağışlanacak sözüyle", "teslim oldu…"], sure: 3.4, renk: ALTIN },
        { satirlar: ["…ve öldürüldü.", "(Rivayete göre bir kan davası yüzünden.)"], sure: 3.0, boy: 80, renk: KIZIL },
      ],
    },
    {
      no: 29, yakin: 2.38, sprite: { w: 400, h: 200, fps: 14, x: 230, taban: 632 },
      yazilar: [
        { satirlar: ["Cengiz soyundan", "Saray Mülk Hatun'la evlendi."], sure: 2.8 },
        { satirlar: ["Unvanı: Gürkan,", "yani hanın damadı."], sure: 2.8, renk: ALTIN },
        { satirlar: ["Tahta kukla bir han oturttu.", "Kendisi hep \"Emir\" kaldı."], sure: 3.2 },
      ],
    },
  ],
  kapanis: {
    satirlar: ["Dünyanın yarısını fethedecekti,", "ama kendine hiç \"han\" diyemedi.", "Otuz yıl sonra bir sultan", "ona şöyle yazacaktı:", "\"Ey ihtiyar köpek…\""],
    sonraki: "Bölüm 2: İki Yıldırım",
    sure: 6,
    arka: 29,
  },
};

export const T1_KARE = Math.round(seriSure(TIMUR1) * T_FPS);
export const Timur1: React.FC = () => <SeriVideo seri={TIMUR1} />;
