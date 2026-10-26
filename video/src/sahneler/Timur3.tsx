import React from "react";
import { ALTIN, KIZIL, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";

/* Timur 3. bölüm "Lanetli Mezar" (1404-1942). Lanet yazıtı ve Stalingrad bağlantısı efsanedir;
   ekranda öyle işaretlenir. Ölüm günü kaynaklarda farklı olduğu için "Şubat 1405" denir. */
export const TIMUR3: Seri = {
  bolumler: [
    {
      no: 51, yakin: 2.25, kamera: 50, sprite: { w: 380, h: 180, fps: 14, x: [220, 300], taban: 632 },
      yazilar: [
        { satirlar: ["Bağdat, Şam, Kahire, Şiraz…"], sure: 2.4, renk: ALTIN },
        { satirlar: ["…hepsi Semerkant'ın", "köyleriydi."], sure: 2.4 },
        { satirlar: ["Fethettiği şehirlerin ustaları", "başkentine getirildi."], sure: 2.8 },
      ],
    },
    {
      no: 52, yakin: 2.12, sprite: { w: 480, h: 200, fps: 12, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Bibi Hanım Camii'nin taşlarını", "filler taşıdı."], sure: 2.8 },
        { satirlar: ["Timur kapıyı alçak buldu,", "yıktırdı."], sure: 2.6, renk: ALTIN },
        { satirlar: ["Aceleyle yapılan kubbeden", "tuğlalar düşmeye başladı."], sure: 2.8 },
      ],
    },
    {
      no: 53, yakin: 2.25, sprite: { w: 420, h: 190, fps: 14, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["1404: Kastilyalı elçi", "Clavijo geldi."], sure: 2.6, renk: ALTIN },
        { satirlar: ["İpek otağlar, at eti,", "bitmeyen şölenler…"], sure: 2.8 },
      ],
    },
    {
      no: 54, yakin: 2.50, kamera: 20, sprite: { w: 270, h: 160, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Ama gördüğü fatih", "artık yaşlıydı."], sure: 2.6 },
        { satirlar: ["Göz kapakları düşmüştü."], sure: 2.4, renk: ALTIN },
      ],
    },
    {
      no: 55, yakin: 2.25, hava: 24, kamera: 50, sprite: { w: 420, h: 170, fps: 16, x: [220, 300], taban: 632 },
      yazilar: [
        { satirlar: ["Kasım 1404: ordu,", "karlar içinde Çin'e yürüdü."], sure: 3.0, renk: ALTIN },
        { satirlar: ["Kayıtlardaki en sert", "kışlardan biriydi."], sure: 2.6 },
      ],
    },
    {
      no: 56, yakin: 2.50, kamera: 20, sprite: { w: 380, h: 140, fps: 8, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Otrar'da ateşlendi."], sure: 2.0 },
        { satirlar: ["Hekimler onu buzla", "serinletmeye çalıştı."], sure: 2.6 },
        { satirlar: ["Şubat 1405.", "Bir daha kalkmadı."], sure: 2.8, renk: KIZIL },
      ],
    },
    {
      no: 57, yakin: 2.25, hava: 24, kamera: 50, sprite: { w: 400, h: 160, fps: 12, x: [230, 290], taban: 632 },
      yazilar: [
        { satirlar: ["Misk ve gülsuyuyla", "abanoz bir tabuta kondu."], sure: 2.8 },
        { satirlar: ["Doğduğu Keş'in yolları", "karla kapalıydı."], sure: 2.6, renk: ALTIN },
      ],
    },
    {
      no: 58, yakin: 1.88, hava: 20, sprite: { w: 520, h: 150, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Semerkant'ta, torunu için", "yaptırdığı Gür-i Emir'e", "gömüldü."], sure: 3.4 },
      ],
    },
    {
      no: 59, yakin: 2.38, sprite: { w: 400, h: 170, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Üstüne dev, koyu yeşil", "bir yeşim taşı kondu."], sure: 2.6, renk: ALTIN },
        { satirlar: ["1740'ta Nadir Şah taşı", "İran'a götürdü; taş çatladı."], sure: 3.0 },
        { satirlar: ["Sonunda geri verdi."], sure: 2.0 },
      ],
    },
    {
      no: 60, yakin: 2.38, sprite: { w: 460, h: 160, fps: 10, x: 270, taban: 634 },
      yazilar: [
        { satirlar: ["Haziran 1941.", "Sovyet bilim insanları", "mezarı açtı."], sure: 3.0, renk: ALTIN },
        { satirlar: ["İskelette aksak sağ bacak", "ve yaralı sağ kol vardı."], sure: 2.8 },
        { satirlar: ["Kroniklerin dediği gibi."], sure: 2.0, renk: ALTIN },
      ],
    },
    {
      no: 61, yakin: 2.38, sprite: { w: 420, h: 160, fps: 10, x: 270, taban: 632 },
      yazilar: [
        { satirlar: ["Kameraman Kayumov'a göre", "yaşlılar onu uyarmıştı:"], sure: 2.8 },
        { satirlar: ["\"Mezarı açarsanız", "savaş çıkar.\""], sure: 2.6, boy: 104, renk: KIZIL },
      ],
    },
    {
      no: 62, yakin: 2.12, sarsinti: 3, kamera: 60, sprite: { w: 480, h: 120, fps: 20, x: [210, 320], taban: 632 },
      yazilar: [
        { satirlar: ["22 Haziran 1941:", "Almanya Sovyetler'e saldırdı."], sure: 3.0, renk: KIZIL },
        { satirlar: ["Tesadüf mü?"], sure: 1.8, boy: 116, renk: ALTIN },
      ],
    },
    {
      no: 63, yakin: 2.00, hava: 20, sprite: { w: 500, h: 160, fps: 12, x: [250, 280], taban: 634 },
      yazilar: [
        { satirlar: ["Kasım 1942: İslami törenle", "yeniden gömüldü."], sure: 2.8 },
        { satirlar: ["Efsaneye göre kısa süre sonra", "Stalingrad'da savaşın yönü döndü."], sure: 3.2, boy: 80, renk: ALTIN },
      ],
    },
    {
      no: 64, yakin: 2.00, sprite: { w: 420, h: 200, fps: 10, x: 230, taban: 632 },
      yazilar: [
        { satirlar: ["Bugün Taşkent'te,", "Marx heykelinin yerinde…"], sure: 2.6 },
        { satirlar: ["\"Güç adalettedir.\""], sure: 2.4, boy: 110, renk: ALTIN },
      ],
    },
  ],
  kapanis: {
    satirlar: ["Mezarı açıldı, savaş başladı.", "Yeniden gömüldü,", "savaşın yönü döndü.", "Sence tesadüf mü? 🤔"],
    sonraki: "Seri bitti! Sıradaki kim olsun?",
    sure: 6,
    arka: 58,
  },
};

export const T3_KARE = Math.round(seriSure(TIMUR3) * T_FPS);
export const Timur3: React.FC = () => <SeriVideo seri={TIMUR3} />;
