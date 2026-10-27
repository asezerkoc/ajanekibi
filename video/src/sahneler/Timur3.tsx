import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Timur 3. bölüm "Lanetli Mezar" (1404-1942). Ekran yazıları ekibin onaylı seslendirme metniyle (149 kelime)
   bire birdir. Lanet ve Stalingrad bağlantısı efsanedir; ekranda öyle işaretlenir. Ses gelince süreler sese hizalanır. */
export const TIMUR3: Seri = {
  etiket: "PİKSEL TARİHİM · TİMUR 3/3",
  bolumler: [
    {
      no: 51, yakin: 1.9, kamera: 50, sprite: { w: 380, h: 180, fps: 14, x: [220, 300], taban: 632 },
      yazilar: [
        { satirlar: ["Kaynaklara göre Semerkant", "çevresinde Bağdat, Dımaşk,", "Şiraz, Mısır köyleri vardı;"], sure: 3.2, renk: ALTIN },
        { satirlar: ["fethedilen şehirlerin", "ustaları getirildi."], sure: 2.4 },
      ],
    },
    {
      no: 52, yakin: 1.8, sprite: { w: 480, h: 200, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Clavijo'ya göre", "filler taş taşıdı;", "Timur alçak kapıyı yıktırdı."], sure: 3.0 },
        { satirlar: ["Rivayete göre aceleyle", "yapılan kubbeden", "tuğlalar düştü."], sure: 2.8, renk: ALTIN },
      ],
    },
    {
      no: 53, yakin: 2.0, sprite: { w: 420, h: 190, fps: 14, x: 270, taban: 632 },
      yazilar: [{ satirlar: ["1404'te Clavijo", "Kânigil çayırında şölendeydi."], sure: 2.6, renk: ALTIN }],
    },
    {
      no: 54, yakin: 3.6, kamera: 10, odakY: 574, sprite: { w: 270, h: 160, fps: 10, x: 270, taban: 632 },
      yazilar: [{ satirlar: ["Timur yaşlıydı,", "göz kapakları düşmüştü."], sure: 2.4 }],
    },
    {
      no: 55, yakin: 2.0, hava: 24, kamera: 50, sprite: { w: 420, h: 170, fps: 16, x: [220, 300], taban: 632 },
      yazilar: [{ satirlar: ["Kasım 1404:", "ordu karda Çin'e yürüdü."], sure: 2.6, renk: ALTIN }],
    },
    {
      no: 56, yakin: 2.2, kamera: 20, sprite: { w: 380, h: 140, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Şubat 1405, Otrar:", "ateşli hastalık."], sure: 2.2 },
        { satirlar: ["Rivayete göre hekimler", "buzla tedavi", "etmeye çalıştı;"], sure: 2.6 },
        { satirlar: ["Timur öldü."], sure: 1.6, boy: 120, renk: KIZIL },
      ],
    },
    {
      no: 57, yakin: 2.0, hava: 24, kamera: 50, sprite: { w: 400, h: 160, fps: 12, x: [230, 290], taban: 632 },
      yazilar: [{ satirlar: ["Kaynaklara göre", "misk ve gülsuyuyla", "tahnit edildi;"], sure: 2.6 }],
    },
    {
      no: 58, yakin: 1.6, hava: 20, sprite: { w: 520, h: 150, fps: 10, x: 270, taban: 634 },
      yazilar: [{ satirlar: ["abanoz tabutla", "Gür-i Emir'e ulaştı."], sure: 2.4, renk: ALTIN }],
    },
    {
      no: 59, yakin: 2.1, sprite: { w: 400, h: 170, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Yeşim taşını Uluğ Bey", "1425'te getirdi;"], sure: 2.2, renk: ALTIN },
        { satirlar: ["Nadir Şah 1740'ta götürdü;", "rivayete göre kırıldı,", "geri verildi."], sure: 3.0 },
      ],
    },
    {
      no: 60, yakin: 2.1, sprite: { w: 460, h: 160, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Haziran 1941:", "Gerasimov mezarı açtı."], sure: 2.4, renk: ALTIN },
        { satirlar: ["Topal sağ bacak,", "yaralı sağ kol;"], sure: 2.0 },
        { satirlar: ["yanda, kaynaklara göre,", "Uluğ Bey'in kesik başı."], sure: 2.6, renk: KIZIL },
      ],
    },
    {
      no: 61, yakin: 2.1, sprite: { w: 420, h: 160, fps: 10, x: 270, taban: 632 },
      yazilar: [{ satirlar: ["Efsaneye göre yaşlılar", "Kayumov'u lanetle uyardı;"], sure: 2.8 }],
    },
    {
      no: 62, yakin: 1.9, sarsinti: 3, kamera: 60, sprite: { w: 480, h: 120, fps: 20, x: [210, 320], taban: 632 },
      yazilar: [{ satirlar: ["22 Haziran'da Almanya", "SSCB'ye saldırdı."], sure: 2.6, renk: KIZIL }],
    },
    {
      no: 63, yakin: 1.8, hava: 20, sprite: { w: 500, h: 160, fps: 12, x: [250, 280], taban: 634 },
      yazilar: [
        { satirlar: ["Kasım 1942:", "İslami törenle yeniden defin;"], sure: 2.6 },
        { satirlar: ["efsaneye göre halk", "Stalingrad zaferini", "buna bağlar."], sure: 2.8, renk: ALTIN },
      ],
    },
    {
      no: 64, yakin: 1.8, sprite: { w: 420, h: 200, fps: 10, x: 230, taban: 632 },
      yazilar: [
        { satirlar: ["Taşkent'te, Marx'ın yerinde", "atlı Timur:"], sure: 2.4 },
        { satirlar: ["“Güç adalettedir.”"], sure: 2.0, boy: 110, renk: ALTIN },
      ],
    },
  ],
  kapanis: {
    satirlar: ["Efsaneye göre mezarı", "açılınca savaş başladı,", "yeniden gömülünce", "savaşın yönü döndü.", "Tesadüf mü?"],
    sonraki: "Sıradaki kim olsun?",
    sure: 4.5,
    arka: 41,
  },
};

export const T3_KARE = Math.round(seriSure(TIMUR3) * T_FPS);
export const Timur3: React.FC = () => <SeriVideo seri={TIMUR3} />;
