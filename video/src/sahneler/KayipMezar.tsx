import React from "react";
import {
  AbsoluteFill,
  Img,
  Sequence,
  cancelRender,
  continueRender,
  delayRender,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";

/* "Kayıp Mezar": 18 sn'lik ara içerik (seslendirmesiz, ekran yazılı). Cengiz Han bölümünün 7. ve 8.
   sahnelerini ve savaş kapağını kullanır; müzik paylaşırken Instagram'dan eklenir. */

export const KM_FPS = 60;
export const KM_KARE = 18 * KM_FPS;
const sn = (s: number) => Math.round(s * KM_FPS);

const LATIN =
  "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD";
const LATIN_EXT =
  "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF";
const bekle = delayRender("Jersey 10 yazı tipi (Kayıp Mezar)");
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
const KREM = "#fff3d4";
const KAHVE = "#2a1408";
const ALTIN = "#ffd479";
const PIKSEL: React.CSSProperties = { imageRendering: "pixelated", position: "absolute", maxWidth: "none" };
const snap = (v: number) => Math.round(v / 2) * 2;

/* Bir sahnenin katmanları, yavaş paralaks kaymasıyla; sprite kendi kare hızında oynar ve tabanı zemin çizgisinde. */
const Sahne: React.FC<{
  no: number;
  sure: number;
  sprite: { w: number; h: number; adet: number; fps: number; x: number; taban: number };
  kamera: number;
}> = ({ no, sure, sprite, kamera }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, sure], [-1, 1]);
  const kam = p * kamera;
  const kare = Math.floor((frame / KM_FPS) * sprite.fps) % sprite.adet;
  const sw = sprite.w * 2;
  const sh = sprite.h * 2;
  const giris = interpolate(frame, [0, sn(0.5)], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: giris, background: "#120806", overflow: "hidden" }}>
      <Img src={staticFile(`sahne${no}-gokyuzu.png`)} style={{ ...PIKSEL, left: snap(kam * 0.1), top: 0, width: W, height: H }} />
      <Img src={staticFile(`sahne${no}-uzak.png`)} style={{ ...PIKSEL, left: snap(kam * 0.3), top: 0, width: W, height: H }} />
      <Img src={staticFile(`sahne${no}-orta.png`)} style={{ ...PIKSEL, left: snap(-270 + kam * 0.65), top: 0, width: 1620, height: H }} />
      <div style={{ position: "absolute", left: snap(sprite.x * 2 - sw / 2 + kam * 0.65), top: sprite.taban * 2 - sh, width: sw, height: sh, overflow: "hidden" }}>
        <Img src={staticFile(`sahne${no}-karakter.png`)} style={{ ...PIKSEL, left: -kare * sw, top: 0, width: sw * sprite.adet, height: sh }} />
      </div>
      <Img src={staticFile(`sahne${no}-on.png`)} style={{ ...PIKSEL, left: snap(-270 + kam * 1.25), top: 0, width: 1620, height: H }} />
      {/* yazı için üstte basamaklı koyulaşma */}
      {[0, 1, 2].map((i) => (
        <div key={i} style={{ position: "absolute", left: 0, top: 0, width: W, height: 760 - i * 160, background: "rgba(10,4,2,0.18)" }} />
      ))}
    </AbsoluteFill>
  );
};

/* Ekran yazısı: piksel yazı tipi, sert kontur ve basamaklı gölge; kısa bir yukarı kayma ile belirir. */
const Yazi: React.FC<{ satirlar: string[]; sure: number; y?: number; boy?: number; renk?: string }> = ({
  satirlar,
  sure,
  y = 300,
  boy = 92,
  renk = KREM,
}) => {
  const frame = useCurrentFrame();
  const op = interpolate(frame, [0, sn(0.35), sure - sn(0.35), sure], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const kay = snap(interpolate(frame, [0, sn(0.35)], [24, 0], { extrapolateRight: "clamp" }));
  return (
    <div style={{ position: "absolute", top: y + kay, left: 40, width: W - 80, textAlign: "center", opacity: op }}>
      {satirlar.map((s, i) => (
        <div
          key={i}
          style={{
            fontFamily: '"Jersey 10", monospace',
            fontSize: boy,
            lineHeight: 1.12,
            color: i === satirlar.length - 1 ? renk : KREM,
            WebkitTextStroke: `7px ${KAHVE}`,
            paintOrder: "stroke fill",
            textShadow: `0 7px 0 ${KAHVE}`,
          }}
        >
          {s}
        </div>
      ))}
    </div>
  );
};

const Kapanis: React.FC = () => {
  const frame = useCurrentFrame();
  const giris = interpolate(frame, [0, sn(0.5)], [0, 1], { extrapolateRight: "clamp" });
  const nabiz = 1 + Math.round(Math.sin((frame / KM_FPS) * Math.PI * 2) * 2) / 100;
  return (
    <AbsoluteFill style={{ opacity: giris, background: "#1a0806" }}>
      <Img src={staticFile("kapak-cengiz-arka.png")} style={{ ...PIKSEL, left: 0, top: 0, width: W, height: H }} />
      <div style={{ position: "absolute", left: 0, top: 0, width: W, height: H, background: "rgba(10,4,2,0.35)" }} />
      <Img
        src={staticFile("logo-pikseltarihim.png")}
        style={{ position: "absolute", left: W / 2 - 170, top: 300, width: 340, height: 340, transform: `scale(${nabiz})` }}
      />
      <Yazi satirlar={["Hikâyenin tamamı", "profilde 👉", "@pikseltarihim"]} sure={sn(5)} y={760} boy={104} renk={ALTIN} />
    </AbsoluteFill>
  );
};

export const KayipMezar: React.FC = () => (
  <AbsoluteFill style={{ background: "#120806" }}>
    <Sequence from={0} durationInFrames={sn(6.6)}>
      <Sahne no={7} sure={sn(6.6)} kamera={30} sprite={{ w: 192, h: 160, adet: 6, fps: 4, x: 270, taban: 600 }} />
    </Sequence>
    <Sequence from={sn(6.4)} durationInFrames={sn(6.8)}>
      <Sahne no={8} sure={sn(6.8)} kamera={20} sprite={{ w: 140, h: 140, adet: 6, fps: 5, x: 236, taban: 640 }} />
    </Sequence>
    <Sequence from={sn(13)} durationInFrames={sn(5)}>
      <Kapanis />
    </Sequence>

    <Sequence from={sn(0.3)} durationInFrames={sn(2.9)}>
      <Yazi satirlar={["1227.", "Cengiz Han öldü."]} sure={sn(2.9)} boy={120} renk={ALTIN} />
    </Sequence>
    <Sequence from={sn(3.3)} durationInFrames={sn(3.2)}>
      <Yazi satirlar={["Cenazesini görenlerin", "öldürüldüğü söylenir…"]} sure={sn(3.2)} />
    </Sequence>
    <Sequence from={sn(6.7)} durationInFrames={sn(3.2)}>
      <Yazi satirlar={["Mezarın üstünden atlar", "sürülüp izler silindi,", "denir."]} sure={sn(3.2)} />
    </Sequence>
    <Sequence from={sn(10)} durationInFrames={sn(3)}>
      <Yazi satirlar={["800 yıldır", "kimse bulamadı."]} sure={sn(3)} boy={120} renk={ALTIN} />
    </Sequence>
  </AbsoluteFill>
);
