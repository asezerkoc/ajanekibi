import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Timur 2. bölüm "İki Yıldırım" (1370-1403). Mektup replikleri Osmanlı mecmualarındaki metinlerden
   (Daş 2004); sahihlikleri tartışmalı olduğu için "kaynaklara göre" diye verilir. */
export const TIMUR2: Seri = {
  bolumler: [
    {
      no: 31, yakin: 2.12, sarsinti: 2, sprite: { w: 520, h: 160, fps: 24, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Otuz yıl boyunca", "durmadı."], sure: 2.2, renk: ALTIN },
        { satirlar: ["Sığınağı olduğu Toktamış", "ona döndü; Altın Orda", "iki kez ezildi."], sure: 3.2 },
      ],
    },
    {
      no: 32, yakin: 2.25, sprite: { w: 520, h: 170, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["İsfahan, 1387:", "isyan eden şehir…"], sure: 2.4, renk: ALTIN },
        { satirlar: ["…kafatası kuleleri", "ile cezalandırıldı."], sure: 2.6, renk: KIZIL },
        { satirlar: ["Teslim olan şehir yaşadı,", "direnen şehir kule oldu."], sure: 2.8 },
      ],
    },
    {
      no: 33, yakin: 2.12, sarsinti: 2, sprite: { w: 520, h: 200, fps: 18, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Delhi, 1398:", "savaş fillerine karşı…"], sure: 2.6, renk: ALTIN },
        { satirlar: ["…şehir düştü."], sure: 1.8, boy: 110 },
      ],
    },
    {
      no: 34, yakin: 2.38, kamera: 70, sprite: { w: 260, h: 140, fps: 30, x: [330, 200], taban: 632 },
      mektup: { metin: ["Kara Yusuf ile", "Ahmed Celâyir'i", "bana teslim et!"], imza: "— Timur (özetle)" },
      yazilar: [
        { satirlar: ["Kaçaklar Yıldırım", "Bayezid'e sığındı."], sure: 2.6 },
        { satirlar: ["Timur teslim edilmelerini", "istedi."], sure: 2.8, renk: ALTIN },
      ],
    },
    {
      no: 35, yakin: 2.38, sprite: { w: 320, h: 190, fps: 12, x: 270, taban: 632 },
      mektup: { metin: ["\"Ey ihtiyar köpek…\"", "", "Savaşa gelmeyip kaçanın", "karısı üç talakla", "boş olsun!"], imza: "— mecmualarda Bayezid'e atfedilen mektup" },
      yazilar: [
        { satirlar: ["Bayezid reddetti."], sure: 1.8, renk: ALTIN },
        { satirlar: ["İki hükümdar dörder", "mektup yazdı."], sure: 2.6 },
        { satirlar: ["Kaynaklara göre", "hakaretler havada uçuştu."], sure: 2.8, boy: 80 },
      ],
    },
    {
      no: 36, yakin: 2.12, sprite: { w: 520, h: 200, fps: 14, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sivas, Ağustos 1400.", "18 gün kuşatma."], sure: 2.8, renk: ALTIN },
        { satirlar: ["Lağımcılar surun altını", "oydu, kirişleri yaktı."], sure: 2.8 },
      ],
    },
    {
      no: 37, yakin: 2.38, sprite: { w: 520, h: 170, fps: 12, x: 260, taban: 634 },
      yazilar: [
        { satirlar: ["Şehir \"kan dökülmeyecek\"", "sözüyle teslim oldu."], sure: 2.8 },
        { satirlar: ["Timur sözünü tuttu:", "kan dökmedi."], sure: 2.4, renk: ALTIN },
        { satirlar: ["3-4 bin savunucu", "diri diri gömüldü."], sure: 2.6, boy: 104, renk: KIZIL },
        { satirlar: ["Bir kronikçiye göre", "çoğu Ermeni askerdi."], sure: 2.4, boy: 76 },
      ],
    },
    {
      no: 38, yakin: 2.25, sprite: { w: 380, h: 150, fps: 10, x: 230, taban: 632 },
      yazilar: [
        { satirlar: ["Ankara, 28 Temmuz 1402."], sure: 2.2, renk: ALTIN },
        { satirlar: ["Timur, Çubuk Çayı'nı", "bentle kesti."], sure: 2.6 },
        { satirlar: ["Osmanlı ordusu savaşa", "susuz girdi."], sure: 2.6, renk: KIZIL },
      ],
    },
    {
      no: 39, yakin: 2.12, sarsinti: 3, sprite: { w: 520, h: 170, fps: 26, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Sırp şövalyeleri üç kez", "hücum etti…"], sure: 2.6 },
        { satirlar: ["…ama Tatarlar savaşın", "ortasında saf değiştirdi."], sure: 2.8, renk: ALTIN },
      ],
    },
    {
      no: 40, yakin: 2.25, sprite: { w: 520, h: 170, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bayezid dağlara kaçtı,", "kuşatıldı…"], sure: 2.6 },
        { satirlar: ["Bir Osmanlı padişahı", "ilk kez esir düştü."], sure: 2.8, renk: KIZIL },
      ],
    },
    {
      no: 41, yakin: 2.25, sprite: { w: 520, h: 200, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Rivayete göre Timur'un", "ziyafetinde…"], sure: 2.6, boy: 84 },
        { satirlar: ["…eşi Despina'ya", "şarap sundurdu."], sure: 2.6, renk: ALTIN },
      ],
    },
    {
      no: 42, yakin: 2.25, sprite: { w: 520, h: 200, fps: 14, x: 260, taban: 632 },
      yazilar: [
        { satirlar: ["İzmir, Aralık 1402:", "Rodos Şövalyeleri'nin kalesi."], sure: 2.8, renk: ALTIN },
        { satirlar: ["Liman ağzı taşla", "dolduruldu."], sure: 2.4 },
        { satirlar: ["Bayezid'in yıllarca alamadığı", "kale iki haftada düştü."], sure: 3.0, renk: ALTIN },
      ],
    },
    {
      no: 43, yakin: 2.25, kamera: 50, sprite: { w: 520, h: 170, fps: 14, x: [230, 300], taban: 632 },
      yazilar: [
        { satirlar: ["\"Demir kafes\" bir efsane."], sure: 2.4, renk: ALTIN },
        { satirlar: ["Gerçeği büyük olasılıkla", "kafesli bir tahtırevandı."], sure: 2.8 },
        { satirlar: ["Bayezid, 8 Mart 1403'te", "Akşehir'de esirken öldü."], sure: 3.0, renk: KIZIL },
      ],
    },
  ],
  kapanis: {
    satirlar: ["Yıldırım'ı yenen adam", "artık yaklaşık 68 yaşındaydı.", "Bacağını sürüyordu.", "Ama hâlâ bir hedefi vardı:", "ÇİN."],
    sonraki: "Bölüm 3: Lanetli Mezar",
    sure: 6,
    arka: 39,
  },
};

export const T2_KARE = Math.round(seriSure(TIMUR2) * T_FPS);
export const Timur2: React.FC = () => <SeriVideo seri={TIMUR2} />;
