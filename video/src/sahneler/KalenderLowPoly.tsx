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

type Hareket = NonNullable<Bolum["gorsel"]>["hareket"];
/* KALENDER.bolumler sırasıyla (72…88, 85 tekrar, 87 tekrar, 89): grafikerin kamera planı. */
const KAMERA: { dosya: number; hareket: Hareket; olcek?: number }[] = [
  { dosya: 72, hareket: "icer" },
  { dosya: 73, hareket: "sag", olcek: 1.12 },
  { dosya: 74, hareket: "icer" },
  { dosya: 75, hareket: "sag", olcek: 1.12 },
  { dosya: 76, hareket: "sag", olcek: 1.12 },
  { dosya: 77, hareket: "icer" },
  { dosya: 78, hareket: "icer", olcek: 1.1 },
  { dosya: 79, hareket: "sol", olcek: 1.12 },
  { dosya: 80, hareket: "sag", olcek: 1.14 },
  { dosya: 81, hareket: "icer", olcek: 1.1 },
  { dosya: 82, hareket: "yukari", olcek: 1.12 },
  { dosya: 83, hareket: "icer", olcek: 1.04 },
  { dosya: 84, hareket: "disari", olcek: 1.06 },
  { dosya: 85, hareket: "icer" },
  { dosya: 86, hareket: "yukari", olcek: 1.1 },
  { dosya: 87, hareket: "icer" },
  { dosya: 88, hareket: "disari", olcek: 1.08 },
  { dosya: 85, hareket: "icer", olcek: 1.14 }, // 85†: kadehe doğru
  { dosya: 87, hareket: "sag", olcek: 1.15 }, // 87†: çadıra doğru
  { dosya: 89, hareket: "disari", olcek: 1.1 },
];

export const KALENDER_LOWPOLY: Seri = {
  ...KALENDER,
  etiket: "PİKSEL TARİHİM · KALENDER",
  yaziTipi: { font: "Montserrat, sans-serif", em: 0.6, kontur: 5 },
  bolumler: KALENDER.bolumler.map((b, i) => ({
    ...b,
    yaziY: undefined, // görsellerde üst %25 yazı için boş bırakıldı; piksel sahnedeki ay kaydırmaları gerekmez
    gorsel: { dosya: `lowpoly/sahne${KAMERA[i].dosya}.png`, hareket: KAMERA[i].hareket, olcek: KAMERA[i].olcek },
  })),
  kapanis: { ...KALENDER.kapanis, arkaGorsel: "lowpoly/sahne89.png" },
};

export const KAL_LP_KARE = Math.round(seriSure(KALENDER_LOWPOLY) * T_FPS);
export const KalenderLowPoly: React.FC = () => <SeriVideo seri={KALENDER_LOWPOLY} />;
