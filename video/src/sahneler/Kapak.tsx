import React from "react";
import { AbsoluteFill, Img, cancelRender, continueRender, delayRender, staticFile } from "remotion";

/* Reels kapağı (1080x1920, tek kare): videonun 1. sahnesinin katmanları, başlık ve sayfa adı.
   Instagram profil ızgarası kapağın ortadaki 3:4 kısmını (y ≈ 240-1680) gösterir; yazılar o alanda. */

const LATIN =
  "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD";
const LATIN_EXT =
  "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF";

const bekle = delayRender("Jersey 10 yazı tipi (kapak)");
Promise.all(
  ([["latin", LATIN], ["latin-ext", LATIN_EXT]] as const).map(([alt, aralik]) => {
    const font = new FontFace("Jersey 10", `url(${staticFile(`fonts/Jersey10-${alt}.woff2`)}) format("woff2")`, {
      weight: "400",
      unicodeRange: aralik,
    });
    document.fonts.add(font);
    return font.load();
  }),
).then(() => continueRender(bekle), (e) => cancelRender(e));

const W = 1080;
const H = 1920;
const PIKSEL: React.CSSProperties = { imageRendering: "pixelated", position: "absolute", maxWidth: "none" };
const KREM = "#fff3d4";
const KAHVE = "#3a2414";
const ALTIN = "#ffd479";

/* Piksel tarzı yazı: sert kahve kontur ve aşağı düşen basamaklı gölge (bulanık gölge yok). */
const Yazi: React.FC<{ metin: string; boy: number; y: number; renk?: string; kontur?: number }> = ({
  metin,
  boy,
  y,
  renk = KREM,
  kontur = 8,
}) => (
  <div
    style={{
      position: "absolute",
      top: y,
      width: W,
      textAlign: "center",
      fontFamily: '"Jersey 10", monospace',
      fontSize: boy,
      lineHeight: 1,
      color: renk,
      WebkitTextStroke: `${kontur}px ${KAHVE}`,
      paintOrder: "stroke fill",
      textShadow: `0 ${kontur}px 0 ${KAHVE}, 0 ${kontur * 1.5}px 0 rgba(0,0,0,0.35)`,
      letterSpacing: boy * 0.02,
    }}
  >
    {metin}
  </div>
);

export const Kapak: React.FC = () => {
  // 1. sahnenin sprite'ı: 300x192 ızgara, ekranda 2 kat; tabanı y=640 (ekranda 1280), yurt ortada
  const kareW = 300 * 2;
  const kareH = 192 * 2;
  return (
    <AbsoluteFill style={{ background: "#2a1a10", overflow: "hidden" }}>
      <Img src={staticFile("sahne1-gokyuzu.png")} style={{ ...PIKSEL, left: 0, top: 0, width: W, height: H }} />
      <Img src={staticFile("sahne1-uzak.png")} style={{ ...PIKSEL, left: 0, top: 0, width: W, height: H }} />
      <Img src={staticFile("sahne1-orta.png")} style={{ ...PIKSEL, left: -270, top: 0, width: 1620, height: H }} />
      <div style={{ position: "absolute", left: W / 2 - kareW / 2, top: 1280 - kareH, width: kareW, height: kareH, overflow: "hidden" }}>
        <Img src={staticFile("sahne1-karakter.png")} style={{ ...PIKSEL, left: 0, top: 0, width: kareW * 8, height: kareH }} />
      </div>
      <Img src={staticFile("sahne1-on.png")} style={{ ...PIKSEL, left: -270, top: 0, width: 1620, height: H }} />

      {/* Yazıların okunması için üstte ve altta basamaklı koyulaşma (yumuşak gradyan yok) */}
      {[0, 1, 2, 3].map((i) => (
        <div key={`u${i}`} style={{ position: "absolute", left: 0, top: 0, width: W, height: 720 - i * 140, background: "rgba(30,18,10,0.13)" }} />
      ))}
      {[0, 1, 2].map((i) => (
        <div key={`a${i}`} style={{ position: "absolute", left: 0, bottom: 0, width: W, height: 560 - i * 140, background: "rgba(30,18,10,0.16)" }} />
      ))}

      <Yazi metin="1. BÖLÜM" boy={64} y={300} renk={ALTIN} kontur={6} />
      <Yazi metin="CENGİZ HAN" boy={210} y={380} kontur={10} />
      <Yazi metin="Bozkırın Çocuğu" boy={104} y={600} renk={ALTIN} kontur={7} />

      {/* Sayfa adı ve logo: ızgarada görünen alanın alt kısmında */}
      <div
        style={{
          position: "absolute",
          top: 1460,
          left: 0,
          width: W,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: 22,
        }}
      >
        <Img src={staticFile("logo-profil.png")} style={{ width: 120, height: 120, imageRendering: "pixelated" }} />
        <div
          style={{
            fontFamily: '"Jersey 10", monospace',
            fontSize: 84,
            color: KREM,
            WebkitTextStroke: `6px ${KAHVE}`,
            paintOrder: "stroke fill",
            textShadow: `0 6px 0 ${KAHVE}`,
          }}
        >
          @pikseltarihim
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* Portreli kapak: kılıcını kaldırmış Cengiz Han (cengiz-portre.png), gün batımı sahnesinin önünde.
   Kılıç üst bölgede yer kapladığı için sayfa adı üstte, başlık altta; hepsi ortadaki 3:4 alanda. */
export const KapakPortre: React.FC = () => (
  <AbsoluteFill style={{ background: "#2a1a10", overflow: "hidden" }}>
    <Img src={staticFile("sahne4-gokyuzu.png")} style={{ ...PIKSEL, left: 0, top: 0, width: W, height: H }} />
    <Img src={staticFile("sahne4-uzak.png")} style={{ ...PIKSEL, left: 0, top: 0, width: W, height: H }} />
    <Img src={staticFile("sahne4-orta.png")} style={{ ...PIKSEL, left: -270, top: 0, width: 1620, height: H }} />
    <Img src={staticFile("cengiz-portre.png")} style={{ ...PIKSEL, left: 0, top: 0, width: W, height: H }} />

    {[0, 1, 2].map((i) => (
      <div key={`a${i}`} style={{ position: "absolute", left: 0, bottom: 0, width: W, height: 720 - i * 150, background: "rgba(30,18,10,0.2)" }} />
    ))}
    <div style={{ position: "absolute", left: 0, top: 0, width: W, height: 360, background: "rgba(30,18,10,0.22)" }} />

    <div style={{ position: "absolute", top: 262, left: 0, width: W, display: "flex", justifyContent: "center", alignItems: "center", gap: 18 }}>
      <Img src={staticFile("logo-profil.png")} style={{ width: 84, height: 84, imageRendering: "pixelated" }} />
      <div
        style={{
          fontFamily: '"Jersey 10", monospace',
          fontSize: 64,
          color: KREM,
          WebkitTextStroke: `5px ${KAHVE}`,
          paintOrder: "stroke fill",
          textShadow: `0 5px 0 ${KAHVE}`,
        }}
      >
        @pikseltarihim
      </div>
    </div>

    <Yazi metin="1. BÖLÜM" boy={64} y={1290} renk={ALTIN} kontur={6} />
    <Yazi metin="CENGİZ HAN" boy={210} y={1360} kontur={10} />
    <Yazi metin="Bozkırın Çocuğu" boy={100} y={1572} renk={ALTIN} kontur={7} />
  </AbsoluteFill>
);

/* Savaş kapağı (sahibin örneğine göre): atının üstünde kanlı kılıçlı Cengiz Han, kızıl gün batımı, ordu
   (kapak-cengiz-arka.png). Logo sağ üstte koyu gökte, başlık altta; ikisi de ortadaki 3:4 alanda. */
export const KapakSavas: React.FC = () => (
  <AbsoluteFill style={{ background: "#1a0806", overflow: "hidden" }}>
    <Img src={staticFile("kapak-cengiz-arka.png")} style={{ ...PIKSEL, left: 0, top: 0, width: W, height: H }} />
    <Img
      src={staticFile("logo-pikseltarihim.png")}
      style={{ position: "absolute", left: 790, top: 262, width: 250, height: 250, filter: "drop-shadow(0 6px 0 rgba(20,8,4,0.8))" }}
    />
    {[0, 1, 2].map((i) => (
      <div key={`a${i}`} style={{ position: "absolute", left: 0, top: 1290 + i * 30, width: W, height: 400 - i * 60, background: "rgba(20,8,4,0.22)" }} />
    ))}
    <Yazi metin="CENGİZ HAN" boy={210} y={1330} kontur={10} />
    <Yazi metin="Bozkırın Çocuğu" boy={96} y={1545} renk={ALTIN} kontur={7} />
  </AbsoluteFill>
);

/* Gündüz kapağı (sahibin örneğine göre): yazısız; yalnızca altta Piksel Tarihim logosu. */
export const KapakGunduz: React.FC = () => (
  <AbsoluteFill style={{ background: "#1a3e8a", overflow: "hidden" }}>
    <Img src={staticFile("kapak-cengiz-gunduz.png")} style={{ ...PIKSEL, left: 0, top: 0, width: W, height: H }} />
    <Img
      src={staticFile("logo-pikseltarihim.png")}
      style={{ position: "absolute", left: W / 2 - 165, top: 1560, width: 330, height: 330, filter: "drop-shadow(0 8px 0 rgba(20,8,4,0.75))" }}
    />
  </AbsoluteFill>
);
