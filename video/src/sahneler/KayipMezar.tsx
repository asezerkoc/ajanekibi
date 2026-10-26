import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  Sequence,
  cancelRender,
  continueRender,
  delayRender,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";

/* "Kayıp Mezar": ölüm sonrası hikâyesi, ~40 sn'lik ara içerik (seslendirmesiz, ekran yazılı). Cengiz Han
   bölümünün sahnelerini ve savaş kapağını kullanır; müzik paylaşırken Instagram'dan eklenir. Kesin olmayan
   anlatılar ekranda "denir / söylenir" diye işaretlenir. */

export const KM_FPS = 60;

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
const snap = (v: number) => v; // alt piksel kaydırma: takılmasız, akıcı

/* Yatayda dikişsiz tekrar eden katman (gökyüzü, uzak plan): iki kopya yan yana, kayma W'ye göre sarılır. */
const Tekrar: React.FC<{ src: string; x: number }> = ({ src, x }) => {
  const o = ((x % W) + W) % W;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 2 * W, height: H, transform: `translateX(${o - W}px)` }}>
      <Img src={staticFile(src)} style={{ ...PIKSEL, left: 0, top: 0, width: W, height: H }} />
      <Img src={staticFile(src)} style={{ ...PIKSEL, left: W, top: 0, width: W, height: H }} />
    </div>
  );
};

/* Bir sahnenin katmanları, yavaş paralaks kaymasıyla; sprite kendi kare hızında oynar ve tabanı zemin çizgisinde. */
const Sahne: React.FC<{
  no: number;
  sure: number;
  sprite: { dosya?: string; w: number; h: number; adet: number; fps: number; x: number; taban: number; uzak?: boolean };
  kamera: number;
}> = ({ no, sure, sprite, kamera }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, sure], [-1, 1], { easing: Easing.inOut(Easing.sin) });
  const akis = (frame / KM_FPS) * 14; // gökyüzü ve uzak planın sürekli akışı (px/sn)
  const kam = p * kamera;
  const kare = Math.floor((frame / KM_FPS) * sprite.fps) % sprite.adet;
  const sw = sprite.w * 2;
  const sh = sprite.h * 2;
  const giris = interpolate(frame, [0, sn(0.5)], [0, 1], { extrapolateRight: "clamp" });
  // Sprite tabanı zemin (ya da uzak ova) çizgisinde; bulunduğu katmanla aynı hızda kayar
  const spriteDiv = (hiz: number, ek = 0) => (
    <div style={{ position: "absolute", left: snap(sprite.x * 2 - sw / 2 + kam * hiz + ek), top: sprite.taban * 2 - sh, width: sw, height: sh, overflow: "hidden" }}>
      <Img src={staticFile(`sahne${no}-${sprite.dosya ?? "karakter"}.png`)} style={{ ...PIKSEL, left: -kare * sw, top: 0, width: sw * sprite.adet, height: sh }} />
    </div>
  );
  return (
    <AbsoluteFill style={{ opacity: giris, background: "#120806", overflow: "hidden" }}>
      <Tekrar src={`sahne${no}-gokyuzu.png`} x={kam * 0.1 - akis * 0.5} />
      <Tekrar src={`sahne${no}-uzak.png`} x={kam * 0.3 - akis} />
      {sprite.uzak ? spriteDiv(0.3, -akis) : null}
      <Img src={staticFile(`sahne${no}-orta.png`)} style={{ ...PIKSEL, left: snap(-270 + kam * 0.65), top: 0, width: 1620, height: H }} />
      {sprite.uzak ? null : spriteDiv(0.65)}
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
      <Yazi satirlar={["Sence bulunmalı mı? 🤔"]} sure={sn(6)} y={700} boy={112} renk={KREM} />
      <Yazi satirlar={["Tüm hikâye profilde 👉", "@pikseltarihim"]} sure={sn(6)} y={860} boy={92} renk={ALTIN} />
    </AbsoluteFill>
  );
};

type Bolum = {
  no: number;
  kamera: number;
  sprite: { dosya?: string; w: number; h: number; adet: number; fps: number; x: number; taban: number; uzak?: boolean };
  yazilar: { satirlar: string[]; sure: number; boy?: number; renk?: string }[];
};

const BOLUMLER: Bolum[] = [
  {
    no: 6, kamera: 60, sprite: { w: 360, h: 120, adet: 24, fps: 15, x: 220, taban: 630 },
    yazilar: [{ satirlar: ["Ağustos 1227."], sure: 2, boy: 124, renk: ALTIN }, { satirlar: ["Cengiz Han,", "Batı Xia seferindeyken", "öldü."], sure: 3.2 }],
  },
  {
    no: 7, kamera: 50, sprite: { w: 192, h: 160, adet: 24, fps: 16, x: 270, taban: 600 },
    yazilar: [{ satirlar: ["Ölümü bir süre", "ordudan gizlendi,", "denir."], sure: 4.4 }],
  },
  {
    no: 3, kamera: 60, sprite: { dosya: "karakter2", w: 248, h: 68, adet: 24, fps: 16, x: 300, taban: 510, uzak: true },
    yazilar: [
      { satirlar: ["Cenaze kafilesi", "doğduğu bozkırlara", "yola çıktı…"], sure: 3.4 },
      { satirlar: ["Yolda onları görenlerin", "öldürüldüğü", "söylenir."], sure: 3.6, renk: "#ff8a6a" },
    ],
  },
  {
    no: 8, kamera: 36, sprite: { w: 140, h: 140, adet: 24, fps: 20, x: 236, taban: 640 },
    yazilar: [{ satirlar: ["Kutsal Burhan Haldun", "Dağı'nın eteklerine", "gömüldüğü düşünülüyor."], sure: 4.4 }],
  },
  {
    no: 4, kamera: 70, sprite: { w: 340, h: 150, adet: 24, fps: 18, x: 300, taban: 630 },
    yazilar: [{ satirlar: ["Mezarın üstünden", "yüzlerce at sürüldü,", "izler silindi, denir."], sure: 4.6 }],
  },
  {
    no: 5, kamera: 50, sprite: { w: 160, h: 224, adet: 24, fps: 24, x: 270, taban: 600 },
    yazilar: [
      { satirlar: ["Bölge yüzyıllarca", "\"Büyük Yasak\" oldu."], sure: 2.6, renk: ALTIN },
      { satirlar: ["Oraya girmek", "yasaktı."], sure: 2.4 },
    ],
  },
  {
    no: 8, kamera: -36, sprite: { w: 140, h: 140, adet: 24, fps: 20, x: 236, taban: 640 },
    yazilar: [
      { satirlar: ["Bugün uydularla", "bile aranıyor…"], sure: 2.6 },
      { satirlar: ["Ama 800 yıldır", "bulunamadı."], sure: 2.8, boy: 116, renk: ALTIN },
    ],
  },
];

const ARA = 0.25; // sahneler arası örtüşme (çapraz geçiş)
const SAHNE_SURELERI = BOLUMLER.map((b) => b.yazilar.reduce((t, y) => t + y.sure, 0) + 0.5);
const KAPANIS = 6;
export const KM_SURE = SAHNE_SURELERI.reduce((a, b) => a + b, 0) + KAPANIS;
export const KM_KARE = Math.round(KM_SURE * KM_FPS);

export const KayipMezar: React.FC = () => {
  let t = 0;
  const parcalar: React.ReactNode[] = [];
  BOLUMLER.forEach((b, i) => {
    const sure = SAHNE_SURELERI[i];
    parcalar.push(
      <Sequence key={`s${i}`} from={sn(t)} durationInFrames={sn(sure + ARA)}>
        <Sahne no={b.no} sure={sn(sure + ARA)} kamera={b.kamera} sprite={b.sprite} />
      </Sequence>,
    );
    let ty = t + 0.3;
    b.yazilar.forEach((y, j) => {
      parcalar.push(
        <Sequence key={`y${i}-${j}`} from={sn(ty)} durationInFrames={sn(y.sure)}>
          <Yazi satirlar={y.satirlar} sure={sn(y.sure)} boy={y.boy} renk={y.renk} />
        </Sequence>,
      );
      ty += y.sure;
    });
    t += sure;
  });
  return (
    <AbsoluteFill style={{ background: "#120806" }}>
      {parcalar}
      <Sequence from={sn(t)} durationInFrames={sn(KAPANIS)}>
        <Kapanis />
      </Sequence>
    </AbsoluteFill>
  );
};
