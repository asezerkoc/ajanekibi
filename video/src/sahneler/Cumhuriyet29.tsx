import React from "react";
import { AbsoluteFill, Img, Sequence, cancelRender, continueRender, delayRender, interpolate, staticFile, useCurrentFrame } from "remotion";
import { KineticCaptions } from "../effects/KineticCaptions";
import { PullBackReveal } from "../effects/PullBackReveal";
import { Spotlight } from "../effects/Spotlight";

/* 29 Ekim Cumhuriyet Bayramı story videosu (1080x1920, 12 sn). Piksel katmanlar (gök + ay-yıldız + güneş, dağlar + atlı
   Atatürk silüeti, ön bozkır) paralaksla yavaşça yaklaşır. Efektler: Pull-back reveal (ay-yıldızdan açılır), Spotlight
   (ışık silüete gider, sonra bütün kare aydınlanır), Kinetic captions (yazılar kelime kelime). */
export const C29_FPS = 60;
const SURE_SN = 12;
export const C29_KARE = SURE_SN * C29_FPS;
const sn = (s: number) => Math.round(s * C29_FPS);

const bekle = delayRender("Montserrat (29 Ekim)");
Promise.all(
  (["latin", "latin-ext"] as const).map((alt) => {
    const font = new FontFace("Montserrat", `url(${staticFile(`fonts/Montserrat-${alt}.woff2`)}) format("woff2")`, { weight: "900" });
    document.fonts.add(font);
    return font.load();
  }),
).then(() => continueRender(bekle), (e) => cancelRender(e));

const PIKSEL: React.CSSProperties = { position: "absolute", imageRendering: "pixelated", left: 0, top: 0, width: 1080, height: 1920 };

/* Üç piksel katman, kamera 12 sn boyunca %8 yaklaşır; katmanlar farklı hızda kayar (paralaks). */
const Sahne: React.FC = () => {
  const frame = useCurrentFrame();
  const p = frame / C29_KARE;
  const zum = 1 + 0.08 * p;
  const kay = Math.sin(p * Math.PI) * 18;
  return (
    <AbsoluteFill style={{ background: "#0c0618", overflow: "hidden" }}>
      <AbsoluteFill style={{ transform: `scale(${zum})`, transformOrigin: "50% 58%" }}>
        <Img src={staticFile("29ekim-gok.png")} style={{ ...PIKSEL, transform: `translate(${kay * 0.2}px, ${p * 10}px)` }} />
        <Img src={staticFile("29ekim-orta.png")} style={{ ...PIKSEL, transform: `translate(${kay * 0.6}px, 0)` }} />
        <Img src={staticFile("29ekim-on.png")} style={{ ...PIKSEL, transform: `translate(${kay * 1.2}px, 0)` }} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const ms = (s: number) => Math.round(s * 1000);
const KELIMELER = [
  { text: "29", startMs: ms(1.3), endMs: ms(1.9) },
  { text: "EKİM", startMs: ms(1.9), endMs: ms(3.3) },
  { text: "CUMHURİYET", startMs: ms(3.5), endMs: ms(4.3) },
  { text: "BAYRAMI", startMs: ms(4.3), endMs: ms(5.8) },
  { text: "103.", startMs: ms(6.0), endMs: ms(6.6) },
  { text: "YIL", startMs: ms(6.6), endMs: ms(7.6) },
  { text: "NE", startMs: ms(7.9), endMs: ms(8.3) },
  { text: "MUTLU", startMs: ms(8.3), endMs: ms(9.2) },
  { text: "TÜRKÜM", startMs: ms(9.4), endMs: ms(10.1) },
  { text: "DİYENE!", startMs: ms(10.1), endMs: ms(12.2) },
];

const Imza: React.FC = () => {
  const frame = useCurrentFrame();
  const op = interpolate(frame, [sn(9.6), sn(10.4)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: op, alignItems: "center", justifyContent: "flex-end", paddingBottom: 130 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <Img src={staticFile("logo-profil.png")} style={{ width: 64, height: 64, borderRadius: 32 }} />
        <div style={{ fontFamily: "Montserrat, sans-serif", fontWeight: 900, fontSize: 36, color: "#ffd060", letterSpacing: 2 }}>@pikseltarihim</div>
      </div>
    </AbsoluteFill>
  );
};

export const Cumhuriyet29: React.FC = () => (
  <AbsoluteFill style={{ background: "#0c0618" }}>
    {/* 0-3 sn: ay-yıldızın içinden geri çekilerek bütün sahne açılır */}
    <PullBackReveal focusX={44} focusY={25} startScale={2.6} startAt={sn(0.4)} duration={sn(2.4)}>
      {/* 2,8-7,5 sn: ışık Atatürk silüetine iner, sonra kare tamamen aydınlanır */}
      <Spotlight
        dim={0.72}
        feather={160}
        stops={[
          { at: 0, x: 50, y: 50, r: 2600 },
          { at: sn(2.8), x: 50, y: 50, r: 2600 },
          { at: sn(3.6), x: 56, y: 51, r: 250 },
          { at: sn(6.2), x: 56, y: 51, r: 300 },
          { at: sn(7.4), x: 50, y: 50, r: 2600 },
        ]}
      >
        <Sahne />
      </Spotlight>
    </PullBackReveal>
    <Sequence from={0} durationInFrames={C29_KARE}>
      <KineticCaptions words={KELIMELER} perPage={2} fontSize={118} highlight="#ffd060" onlyVisible popFrom={0.7} />
    </Sequence>
    <Imza />
  </AbsoluteFill>
);
