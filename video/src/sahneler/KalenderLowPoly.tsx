import React from "react";
import { cancelRender, continueRender, delayRender, staticFile } from "remotion";
import { Bolum, Seri, SeriVideo, T_FPS, seriSure } from "./TimurSeri";
import { KALENDER } from "./Kalender";

/* Tarz denemesi: "Timur'un Soyundan Kalender" sahneleri (72-89) low-poly 3D görsellerle. Görseller grafikerin reçetesine
   (teslimler/2026-10-29-kalender-lowpoly-grafiker.md) göre görsel modelde üretildi (public/lowpoly/sahneNN.png, 9:16);
   süreler, ekran yazıları ve seslendirme KALENDER'den aynen alınır; kamera hareketi reçetedeki plandır. Bir sahnenin
   image-to-video klibi gelirse (public/lowpoly/sahneNN.mp4) `video` alanıyla görselin yerine geçer. */

const LATIN =
  "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD";
const LATIN_EXT =
  "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF";
const bekle = delayRender("Montserrat (Kalender low-poly)");
Promise.all(
  ([["latin", LATIN], ["latin-ext", LATIN_EXT]] as const).map(([alt, aralik]) => {
    const font = new FontFace("Montserrat", `url(${staticFile(`fonts/Montserrat-${alt}.woff2`)}) format("woff2")`, {
      weight: "100 900",
      unicodeRange: aralik,
    });
    document.fonts.add(font);
    return font.load();
  }),
).then(() => continueRender(bekle), (e) => cancelRender(e));

type Gorsel = NonNullable<Bolum["gorsel"]>;
type Hareket = Gorsel["hareket"];
/* KALENDER.bolumler sırasıyla (72…88, 85 tekrar, 87 tekrar, 89): grafikerin kamera planı + kalite kontrol düzeltmeleri.
   yaziY: görselde üst bant dolu olduğunda yazı alt banda (y≈1480-1520, zemin/halı) iner; kremYazi: gün batımında kızıl yazı
   okunmuyorsa yazı rengi kreme çekilir; odakX: figür kenardaysa yakınlaşma o kenarı korur. */
const KAMERA: { dosya: number; hareket: Hareket; olcek?: number; odakX?: number; odakY?: number; yaziY?: number; kremYazi?: boolean }[] = [
  { dosya: 72, hareket: "icer" },
  { dosya: 73, hareket: "sag", olcek: 1.1 },
  { dosya: 74, hareket: "icer", yaziY: 1480 }, // Baysungur'un başı üst bantta: yazı alta
  { dosya: 75, hareket: "sag", olcek: 1.1, kremYazi: true }, // kızıl yazı gün batımıyla karışıyordu
  { dosya: 76, hareket: "sag", olcek: 1.1 },
  { dosya: 77, hareket: "icer" },
  { dosya: 78, hareket: "icer", olcek: 1.08, odakX: 100, yaziY: 1500 }, // Kalender sağ kenarda: yakınlaşma sağı korur, yazı alta
  { dosya: 79, hareket: "sol", olcek: 1.1 },
  { dosya: 80, hareket: "sag", olcek: 1.1, yaziY: 1500 }, // kalkık kılıç üst bantta
  { dosya: 81, hareket: "icer", olcek: 1.08 },
  { dosya: 82, hareket: "yukari", olcek: 1.1, yaziY: 1480 }, // dolunay üst bantta
  { dosya: 83, hareket: "icer", olcek: 1.04 },
  { dosya: 84, hareket: "disari", olcek: 1.06 },
  { dosya: 85, hareket: "icer" },
  { dosya: 86, hareket: "yukari", olcek: 1.1, yaziY: 1480 }, // duman ve hilal üst bantta
  { dosya: 87, hareket: "icer" },
  { dosya: 88, hareket: "disari", olcek: 1.08 },
  { dosya: 85, hareket: "icer", olcek: 1.06, odakY: 70, yaziY: 1500 }, // 85†: sakinin başı yazıya girmesin
  { dosya: 87, hareket: "icer", olcek: 1.0, yaziY: 1500 }, // 87†: Mecnun tam kadrajda kalsın
  { dosya: 89, hareket: "disari", olcek: 1.1 },
];

export const KALENDER_LOWPOLY: Seri = {
  ...KALENDER,
  etiket: "PİKSEL TARİHİM · KALENDER",
  yaziTipi: { font: "Montserrat, sans-serif", em: 0.6, kontur: 5 },
  bolumler: KALENDER.bolumler.map((b, i) => {
    const k = KAMERA[i];
    return {
      ...b,
      yaziY: k.yaziY, // piksel sahnedeki ay kaydırmaları yerine görsele göre bant seçimi
      yazilar: k.kremYazi ? b.yazilar.map((y) => ({ ...y, renk: undefined })) : b.yazilar,
      gorsel: { dosya: `lowpoly/sahne${k.dosya}.png`, hareket: k.hareket, olcek: k.olcek, odakX: k.odakX, odakY: k.odakY },
    };
  }),
  kapanis: { ...KALENDER.kapanis, arkaGorsel: "lowpoly/sahne89.png" },
};

export const KAL_LP_KARE = Math.round(seriSure(KALENDER_LOWPOLY) * T_FPS);
export const KalenderLowPoly: React.FC = () => <SeriVideo seri={KALENDER_LOWPOLY} />;
