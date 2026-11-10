import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  OffthreadVideo,
  Sequence,
  cancelRender,
  continueRender,
  delayRender,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";

/* Timur serisi (3 bölüm): KayipMezar'ın veri güdümlü sahne yapısı, birden çok sprite, hava katmanı (yağmur/kar),
   mektup (parşömen) ve bölüm sonu kancası. Seslendirme gelince süreler anlatıma hizalanır; şimdilik ekran yazılı. */

export const T_FPS = 60;
const sn = (s: number) => Math.round(s * T_FPS);

const LATIN =
  "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD";
const LATIN_EXT =
  "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF";
const bekle = delayRender("Jersey 10 yazı tipi (Timur)");
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
export const ALTIN = "#ffd479";
export const KIZIL = "#ffa486";
const PIKSEL: React.CSSProperties = { imageRendering: "pixelated", position: "absolute", maxWidth: "none" };

/* Yazı tipi bağlamı: piksel seriler Jersey 10 (≈0,46 em/harf); tarz denemeleri (low-poly) başka bir yazı tipi ve
   harf genişliği verebilir. em: bir harfin yaklaşık genişliği (yazı boyuna oranla), satır sığdırma hesabında kullanılır. */
export type YaziTipi = { font: string; em: number; kontur: number };
const JERSEY: YaziTipi = { font: '"Jersey 10", monospace', em: 0.46, kontur: 7 };
const YaziTipiCtx = React.createContext<YaziTipi>(JERSEY);

const Tekrar: React.FC<{ src: string; x: number }> = ({ src, x }) => {
  const o = ((x % W) + W) % W;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 2 * W, height: H, transform: `translateX(${o - W}px)` }}>
      <Img src={staticFile(src)} style={{ ...PIKSEL, left: 0, top: 0, width: W, height: H }} />
      <Img src={staticFile(src)} style={{ ...PIKSEL, left: W, top: 0, width: W, height: H }} />
    </div>
  );
};

/* Sprite: w,h ızgara boyu (ekranda 2 kat), x ızgara konumu (sabit ya da [baş, son] yürüyüş), taban zemin satırı. */
export type Spr = { dosya?: string; w: number; h: number; fps: number; x: number | [number, number]; taban: number; adet?: number };

export type Bolum = {
  no: number;
  kamera?: number; // paralaks kayma genliği (px)
  yakin?: number; // yakın çekim oranı (figürler büyür)
  sprite?: Spr;
  hava?: number; // hava katmanının kare hızı (yağmur/kar)
  sarsinti?: number; // savaş anında kamera sarsıntısı (px)
  odakY?: number; // yakın çekimin odak satırı (ızgara y); verilmezse sprite tabanı
  mektup?: { metin: string[]; imza: string };
  yaziY?: number; // ekran yazısının üst kenarı (px); gökyüzündeki ay/güneş yazıyla çakışmasın diye aşağı alınabilir
  yazilar: { satirlar: string[]; sure: number; boy?: number; renk?: string }[];
  /* Tarz denemeleri: piksel katmanları yerine tek bir dikey görsel (public/, 1080x1920'ye oturtulur) ve kamera hareketi.
     hareket: icer (yavaş yaklaşma), disari (uzaklaşma), sol/sag (yatay kayma), yukari (aşağıdan yukarı tilt). */
  gorsel?: { dosya: string; hareket?: "icer" | "disari" | "sol" | "sag" | "yukari"; olcek?: number; odakX?: number; odakY?: number }; // odak: yakınlaşma merkezi (%)
  video?: string; // gorsel yerine hareketli klip (public/, görsel modelin image-to-video çıktısı); süresi sahneyi doldurmazsa son kare kalır
};

/* Düz görsel sahnesi (Ken Burns): görsel kadrajı kaplar, sahne boyunca yavaşça kayar/yaklaşır; alt bant yazı için koyulaşır. */
const GorselSahne: React.FC<{ b: Bolum; sure: number }> = ({ b, sure }) => {
  const frame = useCurrentFrame();
  const g = b.gorsel!;
  const t = interpolate(frame, [0, sure], [0, 1], { easing: Easing.inOut(Easing.sin), extrapolateRight: "clamp" });
  const giris = interpolate(frame, [0, sn(0.4)], [0, 1], { extrapolateRight: "clamp" });
  const taban = g.olcek ?? 1.08;
  let olcek = taban;
  let dx = 0;
  let dy = 0;
  const hareket = g.hareket ?? "icer";
  // kaydırma genliği, büyütmenin kenarlarda bıraktığı payı aşmaz: (olcek-1)*W/2 her yöne
  if (hareket === "icer") olcek = taban * (1 + 0.1 * t);
  else if (hareket === "disari") olcek = taban * (1.1 - 0.1 * t);
  else if (hareket === "sol") dx = (0.5 - t) * W * (taban - 1) * 0.9;
  else if (hareket === "sag") dx = (t - 0.5) * W * (taban - 1) * 0.9;
  else if (hareket === "yukari") dy = (0.5 - t) * H * (taban - 1) * 0.9;
  const odak = `${g.odakX ?? 50}% ${g.odakY ?? 55}%`;
  return (
    <AbsoluteFill style={{ opacity: giris, background: "#120806", overflow: "hidden" }}>
      {b.video ? (
        <OffthreadVideo
          src={staticFile(b.video)}
          muted
          style={{ position: "absolute", left: 0, top: 0, width: W, height: H, objectFit: "cover", transform: `translate(${dx}px, ${dy}px) scale(${olcek})`, transformOrigin: odak }}
        />
      ) : (
        <Img
          src={staticFile(g.dosya)}
          style={{ position: "absolute", left: 0, top: 0, width: W, height: H, objectFit: "cover", transform: `translate(${dx}px, ${dy}px) scale(${olcek})`, transformOrigin: odak }}
        />
      )}
      {/* üst yazı bandı ve alt kenar hafif koyulaşır: yazı her görselde okunur */}
      <div style={{ position: "absolute", left: 0, top: 0, width: W, height: 620, background: "linear-gradient(rgba(10,4,2,0.55), rgba(10,4,2,0))" }} />
      <div style={{ position: "absolute", left: 0, top: H - 420, width: W, height: 420, background: "linear-gradient(rgba(10,4,2,0), rgba(10,4,2,0.45))" }} />
    </AbsoluteFill>
  );
};

const Sahne: React.FC<{ b: Bolum; sure: number }> = ({ b, sure }) => {
  if (b.gorsel) return <GorselSahne b={b} sure={sure} />;
  return <PikselSahne b={b} sure={sure} />;
};

const PikselSahne: React.FC<{ b: Bolum; sure: number }> = ({ b, sure }) => {
  const frame = useCurrentFrame();
  const { no, sprite } = b;
  const kamera = b.kamera ?? 36;
  const yakin = b.yakin ?? 2.4;
  const p = interpolate(frame, [0, sure], [-1, 1], { easing: Easing.inOut(Easing.sin) });
  const akis = (frame / T_FPS) * 14;
  const kam = p * kamera;
  const adet = sprite?.adet ?? 24;
  const kare = sprite ? Math.floor((frame / T_FPS) * sprite.fps) % adet : 0;
  const sw = sprite ? sprite.w * 2 : 0;
  const sh = sprite ? sprite.h * 2 : 0;
  const sx = sprite ? (Array.isArray(sprite.x) ? interpolate(frame, [0, sure], sprite.x) : sprite.x) : 270;
  const taban = sprite ? sprite.taban : 630;
  const giris = interpolate(frame, [0, sn(0.4)], [0, 1], { extrapolateRight: "clamp" });
  // yavaş yaklaşma: sahne boyunca %6 içeri kayar (canlı kamera hissi)
  const zum = yakin * interpolate(frame, [0, sure], [1, 1.06]);
  const sars = b.sarsinti ? Math.round(Math.sin(frame * 1.7) * b.sarsinti) : 0;
  const havaKare = b.hava ? Math.floor((frame / T_FPS) * b.hava) % 24 : 0;
  return (
    <AbsoluteFill style={{ opacity: giris, background: "#120806", overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          transform: `translate(${sars}px, ${-sars / 2}px) scale(${zum})`, // zemin kadrajın %66 hizasında: Reels alt arayüzünün üstünde kalır
          transformOrigin: `${(sx / 540) * 100}% ${(((b.odakY ?? taban - 12)) / 960) * 100}%`,
        }}
      >
        <Tekrar src={`sahne${no}-gokyuzu.png`} x={kam * 0.1 - akis * 0.5} />
        <Tekrar src={`sahne${no}-uzak.png`} x={kam * 0.3 - akis} />
        <Img src={staticFile(`sahne${no}-orta.png`)} style={{ ...PIKSEL, left: -270 + kam * 0.65, top: 0, width: 1620, height: H }} />
        {sprite ? (
          <div style={{ position: "absolute", left: sx * 2 - sw / 2 + kam * 0.65, top: taban * 2 - sh, width: sw, height: sh, overflow: "hidden" }}>
            <Img
              src={staticFile(`sahne${no}-${sprite.dosya ?? "karakter"}.png`)}
              style={{ ...PIKSEL, left: -kare * sw, top: 0, width: sw * adet, height: sh }}
            />
          </div>
        ) : null}
        <Img src={staticFile(`sahne${no}-on.png`)} style={{ ...PIKSEL, left: -270 + kam * 1.25, top: 0, width: 1620, height: H }} />
      </AbsoluteFill>
      {b.hava ? (
        <div style={{ position: "absolute", left: 0, top: 0, width: W, height: H, overflow: "hidden" }}>
          <Img src={staticFile(`sahne${no}-hava.png`)} style={{ ...PIKSEL, left: -havaKare * W, top: 0, width: W * 24, height: H }} />
        </div>
      ) : null}
      {[0, 1, 2].map((i) => (
        <div key={i} style={{ position: "absolute", left: 0, top: 0, width: W, height: 760 - i * 160, background: "rgba(10,4,2,0.18)" }} />
      ))}
    </AbsoluteFill>
  );
};

const yaziStil = (boy: number, renk: string, yt: YaziTipi = JERSEY): React.CSSProperties => ({
  fontFamily: yt.font,
  fontWeight: yt === JERSEY ? 400 : 800,
  fontSize: boy,
  lineHeight: 1.12,
  color: renk,
  WebkitTextStroke: `${yt.kontur}px ${KAHVE}`,
  paintOrder: "stroke fill",
  textShadow: `0 ${yt.kontur}px 0 ${KAHVE}`,
});

const Yazi: React.FC<{ satirlar: string[]; sure: number; y?: number; boy?: number; renk?: string }> = ({
  satirlar,
  sure,
  y = 300,
  boy = 92,
  renk = KREM,
}) => {
  const frame = useCurrentFrame();
  const yt = React.useContext(YaziTipiCtx);
  const op = interpolate(frame, [0, sn(0.3), sure - sn(0.3), sure], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const kay = interpolate(frame, [0, sn(0.3)], [24, 0], { extrapolateRight: "clamp" });
  // çok uzun satırlar kelime sınırından 30 harfi aşmayacak biçimde bölünür; 30 harfe kadar satırlar planlandığı gibi (anlam birimi) kalır
  if (satirlar.some((s) => s.length > 30)) {
    // bütün metin kelime sınırından, satır uzunlukları dengeli olacak biçimde yeniden dizilir (en çok 30 harf)
    const kelimeler = satirlar.join(" ").split(" ");
    const toplam = kelimeler.join(" ").length;
    const hedef = Math.min(30, Math.ceil(toplam / Math.ceil(toplam / 30)) + 2);
    const yeni: string[] = [];
    let satir = "";
    for (const k of kelimeler) {
      if (satir && (satir + " " + k).length > hedef) {
        yeni.push(satir);
        satir = k;
      } else satir = satir ? satir + " " + k : k;
    }
    if (satir) yeni.push(satir);
    satirlar = yeni;
  }
  // her satır tek satırda kalır: en uzun satır kenarlarda %6 boşluk bırakacak boya sığdırılır (Jersey 10 ≈ 0,46 em/harf)
  const enUzun = Math.max(...satirlar.map((s) => s.length));
  const sigan = Math.min(boy, Math.floor((W - 130) / (enUzun * yt.em)));
  return (
    <div style={{ position: "absolute", top: y + kay, left: 0, width: W, textAlign: "center", opacity: op }}>
      {satirlar.map((s, i) => (
        <div key={i} style={{ ...yaziStil(sigan, i === satirlar.length - 1 ? renk : KREM, yt), whiteSpace: "nowrap" }}>
          {s}
        </div>
      ))}
    </div>
  );
};

/* Parşömen mektup: sahneden ayrı, tam ekran bir mektup çekimi (sahne kararır, parşömen ekranı kaplar); satırlar sırayla
   yazılır ve sahnenin üçte birinde tamamlanır; altta kaynak notu, sağ altta mühür. */
const Mektup: React.FC<{ metin: string[]; imza: string; sure: number }> = ({ metin, imza, sure }) => {
  const frame = useCurrentFrame();
  const ac = interpolate(frame, [0, sn(0.4)], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const kapan = interpolate(frame, [sure - sn(0.4), sure], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const harf = Math.floor(interpolate(frame, [sn(0.15), sure * 0.25], [0, metin.join(" ").length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  let kalan = harf;
  return (
    <AbsoluteFill style={{ opacity: kapan }}>
      <AbsoluteFill style={{ background: `rgba(14,6,2,${0.62 * ac})` }} />
      <div style={{ position: "absolute", left: 70, top: 560, width: 940, height: 820 * ac, overflow: "hidden" }}>
        <Img src={staticFile("parsomen.png")} style={{ ...PIKSEL, left: 0, top: 0, width: 940, height: 820 }} />
        <div style={{ position: "absolute", left: 70, top: 110, width: 800 }}>
          {metin.map((s, i) => {
            const goster = s.slice(0, Math.max(0, kalan));
            kalan -= s.length + 1;
            const boy = Math.min(s.startsWith("“") ? 104 : 80, Math.floor(780 / (Math.max(1, s.length) * 0.46)));
            return (
              <div key={i} style={{ fontFamily: '"Jersey 10", monospace', fontSize: boy, lineHeight: 1.12, whiteSpace: "nowrap", textAlign: "center",
                color: s.startsWith("“") ? "#7a1208" : "#3a1e0c" }}>
                {goster || "\u00a0"}
              </div>
            );
          })}
        </div>
        <div style={{ position: "absolute", left: 60, top: 600, width: 560, textAlign: "left", fontFamily: '"Jersey 10", monospace', fontSize: 48, color: "#8a1a10" }}>
          {kalan > -2 ? imza : ""}
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* Kapanış kartı: arka sahnenin katmanları kısık ışıkta; gece=true ise mavi gece tonu ve yanıp sönen yıldızlar
   (3. bölüm: Gür-i Emir'in kubbe silüeti yıldızlı gecede). */
const YILDIZLAR = Array.from({ length: 70 }, (_, k) => ({
  x: ((k * 379) % 1061) + 10,
  y: ((k * 233) % 1150) + 40,
  faz: (k * 37) % 60,
  b: 3 + (k % 3) * 2,
}));

const Kapanis: React.FC<{ satirlar: string[]; sonraki: string; arka: number; gece?: boolean; arkaGorsel?: string }> = ({ satirlar, sonraki, arka, gece, arkaGorsel }) => {
  const frame = useCurrentFrame();
  const yt = React.useContext(YaziTipiCtx);
  const giris = interpolate(frame, [0, sn(0.5)], [0, 1], { extrapolateRight: "clamp" });
  const nabiz = 1 + Math.round(Math.sin((frame / T_FPS) * Math.PI * 2) * 2) / 100;
  return (
    <AbsoluteFill style={{ opacity: giris, background: gece ? "#060a1e" : "#1a0806" }}>
      {arkaGorsel ? (
        <Img
          src={staticFile(arkaGorsel)}
          style={{ position: "absolute", left: 0, top: 0, width: W, height: H, objectFit: "cover", filter: "brightness(0.4) saturate(0.8)", transform: `scale(${1.05 + frame / 6000})`, transformOrigin: "50% 60%" }}
        />
      ) : (
      <AbsoluteFill
        style={{
          filter: gece ? "brightness(0.55) saturate(0.8)" : "brightness(0.45)",
          transform: gece ? "translateY(640px) scale(1.6)" : "scale(1.6)", // gece kartında kubbe silüeti yazının altına iner
          transformOrigin: "50% 66%",
        }}
      >
        <Tekrar src={`sahne${arka}-gokyuzu.png`} x={-frame * 0.2} />
        <Tekrar src={`sahne${arka}-uzak.png`} x={-frame * 0.4} />
        <Img src={staticFile(`sahne${arka}-orta.png`)} style={{ ...PIKSEL, left: -270, top: 0, width: 1620, height: H }} />
      </AbsoluteFill>
      )}
      {gece ? (
        <>
          <AbsoluteFill style={{ background: "#0a1440", mixBlendMode: "multiply", opacity: 0.55 }} />
          {YILDIZLAR.map((y, k) => (
            <div
              key={k}
              style={{
                position: "absolute",
                left: y.x,
                top: y.y,
                width: y.b,
                height: y.b,
                background: "#fff8e0",
                opacity: 0.35 + 0.65 * Math.abs(Math.sin(((frame + y.faz) / 60) * Math.PI)),
              }}
            />
          ))}
        </>
      ) : null}
      <Img
        src={staticFile("logo-pikseltarihim.png")}
        style={{ position: "absolute", left: W / 2 - 170, top: 260, width: 340, height: 340, transform: `scale(${nabiz})` }}
      />
      <div style={{ position: "absolute", top: 650, left: 30, width: W - 60, textAlign: "center" }}>
        {satirlar.map((s, i) => (
          <div key={i} style={{ ...yaziStil(Math.min(78, Math.floor((W - 160) / (Math.max(...satirlar.map((x) => x.length)) * yt.em))), i === satirlar.length - 1 ? ALTIN : KREM, yt), whiteSpace: "nowrap" }}>
            {s}
          </div>
        ))}
      </div>
      <div style={{ position: "absolute", top: 1180, left: 30, width: W - 60, textAlign: "center" }}>
        <div style={{ ...yaziStil(Math.min(104, Math.floor((W - 200) / (sonraki.length * yt.em))), ALTIN, yt), whiteSpace: "nowrap" }}>{sonraki}</div>
        <div style={yaziStil(Math.round(88 * 0.46 / yt.em), KREM, yt)}>@pikseltarihim</div>
        <div style={yaziStil(Math.round(72 * 0.46 / yt.em), KREM, yt)}>Piksel Tarih | Tarih Animasyon</div>
      </div>
    </AbsoluteFill>
  );
};

export type Seri = {
  etiket: string;
  ses?: string; // public/ altındaki seslendirme (hizala_seri.py üretir)
  kapak?: string; // sahibin hazırladığı açılış kapağı (public/, 1080x1920, olduğu gibi gösterilir)
  bolumler: Bolum[];
  kapanis: { satirlar: string[]; sonraki: string; sure: number; arka: number; gece?: boolean; arkaGorsel?: string };
  yaziTipi?: YaziTipi; // verilmezse Jersey 10 (piksel seriler)
};

const ARA = 0.25;
export const KAPAK_SURE = 2.0; // açılış kapağı ekranda kalır, sonra anlatım başlar
export const seriSure = (s: Seri) =>
  s.bolumler.reduce((t, b) => t + b.yazilar.reduce((a, y) => a + y.sure, 0) + 0.5, 0) + s.kapanis.sure + (s.kapak ? KAPAK_SURE : 0);

export const SeriVideo: React.FC<{ seri: Seri }> = ({ seri }) => {
  let t = 0;
  const parcalar: React.ReactNode[] = [];
  seri.bolumler.forEach((b, i) => {
    const sure = b.yazilar.reduce((a, y) => a + y.sure, 0) + 0.5;
    parcalar.push(
      <Sequence key={`s${i}`} from={sn(t)} durationInFrames={sn(sure + ARA)}>
        <Sahne b={b} sure={sn(sure + ARA)} />
      </Sequence>,
    );
    if (b.mektup) {
      parcalar.push(
        <Sequence key={`m${i}`} from={sn(t + sure * 0.45)} durationInFrames={sn(sure * 0.55)}>
          <Mektup metin={b.mektup.metin} imza={b.mektup.imza} sure={sn(sure * 0.55)} />
        </Sequence>,
      );
    }
    let ty = t + 0.3;
    b.yazilar.forEach((y, j) => {
      parcalar.push(
        <Sequence key={`y${i}-${j}`} from={sn(ty)} durationInFrames={sn(y.sure)}>
          <Yazi satirlar={y.satirlar} sure={sn(y.sure)} boy={y.boy} renk={y.renk} y={b.yaziY} />
        </Sequence>,
      );
      ty += y.sure;
    });
    t += sure;
  });
  const kapak = seri.kapak ? sn(KAPAK_SURE) : 0;
  const yt = seri.yaziTipi ?? JERSEY;
  return (
    <YaziTipiCtx.Provider value={yt}>
    <AbsoluteFill style={{ background: "#120806" }}>
      {seri.kapak ? (
        <Sequence from={0} durationInFrames={kapak}>
          <Img src={staticFile(seri.kapak)} style={{ position: "absolute", left: 0, top: 0, width: W, height: H }} />
        </Sequence>
      ) : null}
      <Sequence from={kapak} durationInFrames={sn(t + seri.kapanis.sure)}>
        {seri.ses ? <Audio src={staticFile(seri.ses)} /> : null}
        {parcalar}
        <Sequence from={0} durationInFrames={sn(t)}>
          <div style={{ position: "absolute", top: 150, left: 0, width: W, textAlign: "center", fontFamily: yt.font, fontWeight: yt === JERSEY ? 400 : 800,
            fontSize: Math.round(46 * 0.46 / yt.em), color: ALTIN, WebkitTextStroke: `5px ${KAHVE}`, paintOrder: "stroke fill", letterSpacing: 4 }}>
            {seri.etiket}
          </div>
        </Sequence>
        <Sequence from={sn(t)} durationInFrames={sn(seri.kapanis.sure)}>
          <Kapanis satirlar={seri.kapanis.satirlar} sonraki={seri.kapanis.sonraki} arka={seri.kapanis.arka} gece={seri.kapanis.gece} arkaGorsel={seri.kapanis.arkaGorsel} />
        </Sequence>
      </Sequence>
    </AbsoluteFill>
    </YaziTipiCtx.Provider>
  );
};
