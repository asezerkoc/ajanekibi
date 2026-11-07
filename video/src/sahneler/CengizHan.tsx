import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  cancelRender,
  continueRender,
  delayRender,
  Img,
  Sequence,
  interpolate,
  random,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { PullBackReveal } from "../effects/PullBackReveal";
import * as ZAMAN from "./CengizHanZaman";
import { DoodleBoil } from "../effects/DoodleBoil";
import { KineticCaptions } from "../effects/KineticCaptions";
import type { CaptionWord } from "../effects/KineticCaptions";

/* ------------------------------------------------------------------ */
/*  Yazı tipi: piksel yazı tipi (ekran metni ve altyazı).              */
/*  latin-ext şart (ğ, ş, İ, ı). loadFont, yüklenene kadar render'ı     */
/*  bekletir (delayRender).                                             */
/* ------------------------------------------------------------------ */
/* Yazı tipi video/public/fonts/ içinden yüklenir: render ortamı Google Fonts'a çıkamıyor. */
const LATIN =
  "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD";
const LATIN_EXT =
  "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF";

const yaziTipiBekle = delayRender("Jersey 10 yazı tipi");
/* Jersey 10: kalın, dar, okunaklı piksel yazı tipi (Pixelify Sans'ta B ve C, G ve O'ya benziyordu).
   Tek ağırlık (400) var; daha kalın istenirse tarayıcı yapay kalınlaştırır, harfler kapanır. */
Promise.all(
  ([["latin", LATIN], ["latin-ext", LATIN_EXT]] as const).map(([alt, aralik]) => {
    const font = new FontFace("Jersey 10", `url(${staticFile(`fonts/Jersey10-${alt}.woff2`)}) format("woff2")`, {
      weight: "400",
      unicodeRange: aralik,
    });
    document.fonts.add(font);
    return font.load();
  }),
).then(() => continueRender(yaziTipiBekle), (e) => cancelRender(e));
const YAZI_FONTU = `"Jersey 10", monospace`;

/* ------------------------------------------------------------------ */
/*  Genel ayarlar: 1080x1920, 60 fps, 3600 kare (60 sn)                */
/*  Bütün süreler saniyeden türetilir: sn(s) = round(s * FPS).         */
/* ------------------------------------------------------------------ */
export const FPS = 60;
/* Süre seslendirmeden gelir (video/ses/hizala.py → CengizHanZaman.ts): konuşma + kapanış sorusu */
export const TOPLAM_SN = ZAMAN.TOPLAM_SN;
export const TOPLAM_KARE = Math.round(TOPLAM_SN * FPS);
const sn = (s: number) => Math.round(s * FPS);

const W = 1080;
const H = 1920;

/* Piksel ızgarası: bütün sahnelerde 540x960, ekranda TAM 2 kat. */
const OLCEK = 2;
/* Konum yuvarlama adımı (ekran px). 2 = ızgara pikseline oturur. 1 yapılırsa kaydırma
   daha akıcı olur, ama katmanlar arası piksel ızgarası kayar. */
const SNAP = 2;
/* Kaydırma alt piksel hassasiyetinde: tam piksele yuvarlamak yavaş kaymalarda takılma gibi görünüyordu.
   Görseller yine pixelated çizilir, pikseller keskin kalır. */
const snap = (v: number) => v;
/* Çimen ve parçacık blokları (ekran px) = 2x2 ızgara pikseli. */
const BLOK = 4;
const PIKSEL_STIL: React.CSSProperties = { imageRendering: "pixelated" };

const FADE = sn(0.6); // sahneler arası yumuşak çapraz geçiş (36 kare)
const BOIL_HOLD = Math.round(FPS / 15); // DoodleBoil: saniyede 15 titreşim = 4 kare
/* DoodleBoil titreşimi (displacement) piksel kenarlarını hafif bozar. Keskin yazı istenirse 0 yapın. */
const BOIL_MIKTAR = 0;
const CLAMP = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
};

/* Paralaks katsayıları: gökyüzü en yavaş, ön plan en hızlı. */
const HIZ = { gokyuzu: 0.1, uzak: 0.3, orta: 0.65, karakter: 0.65, on: 1.25 };
/* Gökyüzü ve uzak planın sürekli akışı (ekran px / sn). */
const AKIS = { gokyuzu: 6, uzak: 12 };

/* DoodleBoil içindeki SVG 1920x1080 viewBox'lı. 1080x1920 ekranda 0,5625 ölçeğiyle
   dikey ortalanır. X/Y, ekran pikselini (1080x1920) SVG koordinatına çevirir. */
const K = 1080 / 1920;
const OFF = (1920 - 1080 * K) / 2;
const X = (sx: number) => sx / K;
const Y = (sy: number) => (sy - OFF) / K;

/* ------------------------------------------------------------------ */
/*  Sahne tanımları                                                    */
/*  Konumlar "ızgara birimi"dir (540x960). Ekran = ızgara x 2.         */
/*  Sprite'lar TABANLA konumlanır: top = tabanY*2 - kareH*2            */
/*  Taban, sahnenin zemin çizgisidir (zemin ya da ufuk).               */
/*  Yapılar yalnızca düz zemine oturur: ZEMIN (yakın) ya da UFUK (uzak ova). */
/* ------------------------------------------------------------------ */
type OrtamModu = "polen" | "atesbocegi" | "yildiz" | "yok";

type SpriteTanimi = {
  /** "karakter" ya da "karakter2" → sahneN-karakter.png */
  dosya: string;
  /** Kare boyutu (ızgara birimi) ve kare sayısı. Sheet = yatay şerit, URET 1. */
  kareW: number;
  kareH: number;
  kare: number;
  /** Sprite kare hızı (saniyede kare). */
  fps: number;
  /** Kare merkezinin yatay konumu: [başlangıç, bitiş]. Dikey konum zemin çizgisinden gelir. */
  x: [number, number];
  /** "zemin": yakın zemin (orta plan üstü). "ufuk": uzak ova (orta planın arkası). */
  taban: "zemin" | "ufuk";
  opaklik?: [number, number];
};

type SahneTanimi = {
  no: number;
  bas: number; // saniye
  bit: number; // saniye
  yon: 1 | -1;
  kamera: [number, number];
  /** Yakın zemin çizgisi (ızgara y). Yakın sprite'ların tabanı burada. */
  zemin: number;
  /** Uzak ova çizgisi (ızgara y). Kervan ve şehir tabanı burada. */
  ufuk?: number;
  ortam: OrtamModu;
  /** Yerden doğan toz: ilk sprite'ın tabanından çıkar. arka: tozun sprite'a göre tarafı. */
  toz?: { arka: 1 | -1 };
  spriteler: SpriteTanimi[];
  pullBack?: { focusX: number; focusY: number; startScale: number; startAt: number; sure: number };
};

const SAHNELER: SahneTanimi[] = [
  {
    // Yurt ve iki at: 300x192 (atlar yurttan ayrı), tabanı y=640 (ekranda 1280)
    no: 1, bas: 0, bit: 5, yon: -1, kamera: [0, -30], zemin: 640, ortam: "polen",
    pullBack: { focusX: 68, focusY: 60, startScale: 3.2, startAt: 1 / 3, sure: 3 },
    spriteler: [{ dosya: "karakter", kareW: 300, kareH: 192, kare: 24, fps: 24, x: [367, 367], taban: "zemin" }],
  },
  {
    // Yurt, anne ve bebek: 256x256 (büyütüldü), tabanı y=600 (1200)
    no: 2, bas: 5, bit: 9, yon: -1, kamera: [30, -30], zemin: 600, ortam: "polen",
    spriteler: [{ dosya: "karakter", kareW: 256, kareH: 256, kare: 24, fps: 24, x: [270, 270], taban: "zemin" }],
  },
  {
    no: 3, bas: 9, bit: 16.4, yon: -1, kamera: [70, -70], zemin: 600, ufuk: 510, ortam: "yok",
    toz: { arka: -1 },
    spriteler: [
      // Aile: 270x170 (sahibin isteğiyle büyütüldü), ZEMIN. 36 birim/sn, döngü 8 kare / 6 fps = 1,33 sn = 48 birim adım (kayma yok)
      { dosya: "karakter", kareW: 270, kareH: 170, kare: 24, fps: 18, x: [90, 378], taban: "zemin" },
      // Kervan: 248x68, tekerlekleri uzak düz ovada (UFUK)
      { dosya: "karakter2", kareW: 248, kareH: 68, kare: 24, fps: 16, x: [375, 255], taban: "ufuk", opaklik: [1, 0.4] },
    ],
  },
  {
    // Atlı kafile: 340x150 (1,25 kat büyük), ZEMIN. 36 birim/sn, döngü 1,33 sn = 48 birim (sakin tırıs)
    no: 4, bas: 16.4, bit: 25, yon: 1, kamera: [-70, 70], zemin: 630, ortam: "yok",
    toz: { arka: 1 },
    spriteler: [{ dosya: "karakter", kareW: 340, kareH: 150, kare: 24, fps: 18, x: [510, 179], taban: "zemin" }],
  },
  {
    // Tuğ: 160x224, ZEMIN. Çadırlar orta planda, hepsi aynı düz ZEMIN satırında
    no: 5, bas: 25, bit: 34.4, yon: 1, kamera: [-40, 40], zemin: 600, ortam: "polen",
    spriteler: [{ dosya: "karakter", kareW: 160, kareH: 224, kare: 24, fps: 24, x: [270, 270], taban: "zemin" }],
  },
  {
    no: 6, bas: 34.4, bit: 43.4, yon: -1, kamera: [40, -40], zemin: 630, ufuk: 518, ortam: "yok",
    toz: { arka: -1 },
    spriteler: [
      // Kolon: 360x120 (1,25 kat büyük), ZEMIN. 30 birim/sn, döngü 8 kare / 5 fps = 1,6 sn = 48 birim
      { dosya: "karakter", kareW: 360, kareH: 120, kare: 24, fps: 15, x: [10, 298], taban: "zemin" },
      // Şehir ve duman: 296x248, tek sprite, duman çatı hizasından çıkar, taban uzak düz ovada (UFUK)
      { dosya: "karakter2", kareW: 296, kareH: 248, kare: 24, fps: 12, x: [378, 378], taban: "ufuk" },
    ],
  },
  {
    // Boş eyerli at: 192x160, ZEMIN. Ağacın gövde tabanı aynı çizgide (orta planda)
    no: 7, bas: 43.4, bit: 51.5, yon: -1, kamera: [20, -20], zemin: 600, ortam: "atesbocegi",
    spriteler: [{ dosya: "karakter", kareW: 192, kareH: 160, kare: 24, fps: 16, x: [270, 270], taban: "zemin" }],
  },
  {
    no: 8, bas: 51.5, bit: 60, yon: -1, kamera: [0, 0], zemin: 640, ortam: "yildiz",
    // Taş yığını (x≈162, orta planda) ve çiçek (x=236) aynı zemin çizgisinde (y=640 → ekran 1280)
    pullBack: { focusX: 30, focusY: 62, startScale: 3, startAt: 0.4, sure: 13 / 3 },
    spriteler: [{ dosya: "karakter", kareW: 140, kareH: 140, kare: 24, fps: 20, x: [236, 236], taban: "zemin" }],
  },
];

/* Her sahne kendi paragrafı okunduğu sürece ekranda kalır (ölçülen zamanlar). */
SAHNELER.forEach((s, i) => {
  s.bas = ZAMAN.SAHNE_ZAMANLARI[i][0];
  s.bit = ZAMAN.SAHNE_ZAMANLARI[i][1];
});

/* Ekran metinleri (onaylı metindeki 5 ekran metni), saniye cinsinden */
type EkranMetniTanimi = { bas: number; bit: number; satirlar: string[] };
const EKRAN_METINLERI: EkranMetniTanimi[] = ZAMAN.EKRAN_METNI_ZAMANLARI.map((m) => ({
  bas: m.bas,
  bit: m.bit,
  satirlar: [...m.satirlar],
}));

/* ------------------------------------------------------------------ */
/*  Anlatım ve altyazı zamanlaması (saniye). Gerçek seslendirme gelince */
/*  bas/bit değerlerini güncelle.                                      */
/* ------------------------------------------------------------------ */
/* Cümle cümle, seslendirmeden ölçülen başlangıç ve bitişler. Kelimeler cümle içinde uzunluklarına göre dağılır. */
const ANLATIM: { t: string; bas: number; bit: number }[] = ZAMAN.ANLATIM.map((a) => ({ t: a.t, bas: a.bas, bit: a.bit }));

/* Her cümlenin süresi kelimelere uzunluklarına göre bölünür. Metin Türkçe kurallarla
   önceden büyütülür (i→İ, ı→I). KineticCaptions zaman olarak ms bekler. */
const KELIMELER: CaptionWord[] = ANLATIM.flatMap((seg) => {
  const tokenlar = seg.t.split(/\s+/);
  const agirlik = tokenlar.map(
    (tk) => tk.length + (/[.,?!]$/.test(tk) ? 3 : 0) + (/\d/.test(tk) ? 6 : 0),
  );
  const toplam = agirlik.reduce((a, b) => a + b, 0);
  const sureMs = (seg.bit - seg.bas) * 1000;
  let t = seg.bas * 1000;
  return tokenlar.map((tk, i) => {
    const startMs = t;
    t += (sureMs * agirlik[i]) / toplam;
    return { text: tk.toLocaleUpperCase("tr-TR"), startMs, endMs: t };
  });
});

/* ------------------------------------------------------------------ */
/*  Paralaks katmanları (hepsi piksel net: pixelated + tam sayı ölçek) */
/* ------------------------------------------------------------------ */

/** Yatayda dikişsiz tekrarlanan katman (gökyüzü, uzak plan). Kaynak 540x960, ekranda 2 kat. */
const TileKatman: React.FC<{ src: string; ofset: number }> = ({ src, ofset }) => {
  const o = snap(((ofset % W) + W) % W);
  const stil: React.CSSProperties = { width: W, height: H, flexShrink: 0, maxWidth: "none", ...PIKSEL_STIL };
  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: 2 * W,
        height: H,
        display: "flex",
        transform: `translateX(${o - W}px)`,
      }}
    >
      <Img src={staticFile(src)} style={stil} />
      <Img src={staticFile(src)} style={stil} />
    </div>
  );
};

/** Kadrajdan 1,5 kat geniş katman (orta, ön plan). Kaynak 810x960, ekranda 1620x1920, kayma ±270 px. */
const GENIS = Math.round(W * 1.5);
const PAY = (GENIS - W) / 2;
const GenisKatman: React.FC<{ src: string; ofset: number }> = ({ src, ofset }) => {
  const o = snap(Math.max(-PAY, Math.min(PAY, ofset)));
  return (
    <Img
      src={staticFile(src)}
      style={{ position: "absolute", top: 0, left: -PAY + o, width: GENIS, height: H, maxWidth: "none", ...PIKSEL_STIL }}
    />
  );
};

/** Yatay şerit sprite sheet (URET 1: dosya = ızgara boyutu, ekranda tam 2 kat).
    Konum TABANLA verilir: top = tabanY*2 - kareH*2. Dikey konum hiç değişmez.
    Yatay konum 2 px'lik piksel ızgarasına yuvarlanır, kare değişimi sprite fps'inde. */
const Sprite: React.FC<{
  d: SpriteTanimi;
  no: number;
  p: number;
  ofsetX: number;
  tabanY: number;
  frame: number;
}> = ({ d, no, p, ofsetX, tabanY, frame }) => {
  const kare = Math.floor((frame / FPS) * d.fps) % d.kare;
  const w = d.kareW * OLCEK;
  const h = d.kareH * OLCEK;
  const cx = interpolate(p, [0, 1], d.x) * OLCEK + ofsetX;
  const left = snap(cx - w / 2);
  const top = Math.round(tabanY * OLCEK - h); // kare tabanı = zemin çizgisi
  const op = d.opaklik ? interpolate(p, [0, 1], d.opaklik) : 1;
  return (
    <div style={{ position: "absolute", left, top, width: w, height: h, overflow: "hidden", opacity: op }}>
      <Img
        src={staticFile(`sahne${no}-${d.dosya}.png`)}
        style={{
          position: "absolute",
          top: 0,
          left: -kare * w,
          width: d.kare * w,
          height: h,
          maxWidth: "none",
          ...PIKSEL_STIL,
        }}
      />
    </div>
  );
};

/** Yerden doğan toz: ilk sprite'ın tabanında doğar, yukarı yükselir, solar. Kare bloklardan oluşur.
    Havada gezmez, zemin çizgisinin altına inmez (blok tabanı doğum anında zemin satırında). */
const Toz: React.FC<{ s: SahneTanimi; sure: number; ofsetX: number }> = ({ s, sure, ofsetX }) => {
  const frame = useCurrentFrame();
  if (!s.toz) return null;
  const t = frame / FPS;
  const d = s.spriteler[0];
  const zeminPx = s.zemin * OLCEK;
  const adet = 16;
  const bloklar: React.ReactNode[] = [];
  for (let i = 0; i < adet; i++) {
    const omur = 1.6 + random(`toz-${s.no}-o-${i}`) * 1.2;
    const faz = t / omur + random(`toz-${s.no}-f-${i}`);
    const k = Math.floor(faz);
    const u = faz - k; // 0 = yerde doğar, 1 = solar
    const tb = t - u * omur; // doğum anı
    const p = Math.max(0, Math.min(1, tb / (sure / FPS)));
    const rx = random(`toz-${s.no}-x-${i}-${k}`);
    const ry = random(`toz-${s.no}-y-${i}-${k}`);
    const cx = interpolate(p, [0, 1], d.x) * OLCEK + ofsetX;
    const x = cx + s.toz.arka * (rx * d.kareW * 0.5 * OLCEK + u * 36);
    const boy = BLOK * (1 + Math.floor(ry * 3)); // 4, 8 ya da 12 px
    // Doğumda blok tabanı tam zemin satırında; sonra yükselir
    const y = zeminPx - boy - u * (40 + ry * 70);
    const op = u < 0.33 ? 0.55 : u < 0.66 ? 0.4 : 0.22; // basamaklı solma (yumuşak gradyan yok)
    bloklar.push(
      <rect
        key={i}
        x={Math.round(x / BLOK) * BLOK}
        y={Math.round(y / BLOK) * BLOK}
        width={boy}
        height={boy}
        fill="rgb(236,208,160)"
        opacity={op}
      />,
    );
  }
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" shapeRendering="crispEdges">
        {bloklar}
      </svg>
    </AbsoluteFill>
  );
};

/** Bir sahnenin katmanları: gökyüzü, uzak, [uzak sprite'lar], orta, [yakın sprite'lar], toz, ön plan. */
const ParalaksSahne: React.FC<{ s: SahneTanimi; sure: number }> = ({ s, sure }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const pLin = interpolate(frame, [0, sure], [0, 1], CLAMP);
  const pYumusak = interpolate(frame, [0, sure], [0, 1], { ...CLAMP, easing: Easing.inOut(Easing.sin) });
  const kam = interpolate(pYumusak, [0, 1], s.kamera);
  const dosya = (k: string) => `sahne${s.no}-${k}.png`;
  const uzakSpr = s.spriteler.filter((d) => d.taban === "ufuk");
  const yakinSpr = s.spriteler.filter((d) => d.taban === "zemin");
  const tabanOf = (d: SpriteTanimi) => (d.taban === "ufuk" ? (s.ufuk as number) : s.zemin);

  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#3a2a1c" }}>
      <TileKatman src={dosya("gokyuzu")} ofset={kam * HIZ.gokyuzu + s.yon * t * AKIS.gokyuzu} />
      <TileKatman src={dosya("uzak")} ofset={kam * HIZ.uzak + s.yon * t * AKIS.uzak} />
      {uzakSpr.map((d) => (
        <Sprite
          key={d.dosya}
          d={d}
          no={s.no}
          p={pLin}
          ofsetX={kam * HIZ.uzak + s.yon * t * AKIS.uzak}
          tabanY={tabanOf(d)}
          frame={frame}
        />
      ))}
      <GenisKatman src={dosya("orta")} ofset={kam * HIZ.orta} />
      {yakinSpr.map((d) => (
        <Sprite
          key={d.dosya}
          d={d}
          no={s.no}
          p={pLin}
          ofsetX={kam * HIZ.karakter}
          tabanY={tabanOf(d)}
          frame={frame}
        />
      ))}
      <Toz s={s} sure={sure} ofsetX={kam * HIZ.karakter} />
      <GenisKatman src={dosya("on")} ofset={kam * HIZ.on} />
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/*  Yardımcı bileşenler                                                */
/* ------------------------------------------------------------------ */

/** Sahne girişinde yumuşak çapraz geçiş (ilk sahne hariç). */
const YumusakGiris: React.FC<{ aktif: boolean; children: React.ReactNode }> = ({ aktif, children }) => {
  const frame = useCurrentFrame();
  const opacity = aktif ? interpolate(frame, [0, FADE], [0, 1], CLAMP) : 1;
  return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
};

/** Süzülen piksel parçacıklar: polen (kare), ateş böceği ve yıldız (artı şekli). Kare bloklar, basamaklı
    opaklık, gradyan yok. Sürekli hareket eder. Yıldızlar yalnızca gökte (üst %30). */
const ORTAM: Record<
  Exclude<OrtamModu, "yok">,
  {
    renk: string; adet: number; vx: number; vy: number; salim: number;
    y0: number; y1: number; yan: number; boy: [number, number]; arti: boolean;
  }
> = {
  polen: { renk: "255,238,170", adet: 22, vx: 12, vy: -8, salim: 22, y0: 0.28, y1: 0.8, yan: 0.35, boy: [5, 9], arti: false },
  atesbocegi: { renk: "220,245,120", adet: 18, vx: 5, vy: -4, salim: 26, y0: 0.45, y1: 0.74, yan: 0.5, boy: [5, 9], arti: true },
  yildiz: { renk: "255,246,208", adet: 26, vx: 0, vy: 0, salim: 0, y0: 0.02, y1: 0.3, yan: 0.4, boy: [4, 8], arti: true },
};

const Parcaciklar: React.FC<{ mod: OrtamModu }> = ({ mod }) => {
  const frame = useCurrentFrame();
  if (mod === "yok") return null;
  const t = frame / FPS;
  const m = ORTAM[mod];
  const aralik = (m.y1 - m.y0) * H;
  const bloklar: React.ReactNode[] = [];
  const q = (v: number) => Math.round(v / BLOK) * BLOK;
  for (let i = 0; i < m.adet; i++) {
    const r1 = random(`pc-${mod}-x-${i}`);
    const r2 = random(`pc-${mod}-y-${i}`);
    const r3 = random(`pc-${mod}-s-${i}`);
    const r4 = random(`pc-${mod}-f-${i}`);
    const hizK = 0.6 + r3 * 0.8;
    const x = (((r1 * W + t * m.vx * hizK) % W) + W) % W;
    const yRel = (((r2 * aralik + t * m.vy * hizK) % aralik) + aralik) % aralik;
    const y = m.y0 * H + yRel + Math.sin(t * 0.75 + r4 * 6.283) * m.salim;
    const boy = BLOK * Math.max(1, Math.round((m.boy[0] + r3 * (m.boy[1] - m.boy[0])) / BLOK));
    const fx = x / W;
    const fy = yRel / aralik;
    const env = Math.min(1, fx * 10, (1 - fx) * 10, fy * 6, (1 - fy) * 6);
    const puls = 0.35 + 0.65 * (0.5 + 0.5 * Math.sin(2 * Math.PI * m.yan * t + r4 * 6.283));
    const op = Math.round(puls * env * 4) / 4; // basamaklı opaklık
    if (op <= 0) continue;
    const px = q(x);
    const py = q(y);
    const renk = `rgb(${m.renk})`;
    bloklar.push(<rect key={`c${i}`} x={px} y={py} width={boy} height={boy} fill={renk} opacity={op} />);
    if (m.arti) {
      const yari = op / 2;
      bloklar.push(
        <rect key={`a${i}`} x={px - boy} y={py} width={boy} height={boy} fill={renk} opacity={yari} />,
        <rect key={`b${i}`} x={px + boy} y={py} width={boy} height={boy} fill={renk} opacity={yari} />,
        <rect key={`c2${i}`} x={px} y={py - boy} width={boy} height={boy} fill={renk} opacity={yari} />,
        <rect key={`d${i}`} x={px} y={py + boy} width={boy} height={boy} fill={renk} opacity={yari} />,
      );
    }
  }
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" shapeRendering="crispEdges">
        {bloklar}
      </svg>
    </AbsoluteFill>
  );
};

/** Sahne içeriği: paralaks yığını (Sahne 1 ve 8'de PullBackReveal içinde) + ortam parçacıkları. */
const SahneIcerigi: React.FC<{ s: SahneTanimi; sure: number }> = ({ s, sure }) => {
  const yigin = <ParalaksSahne s={s} sure={sure} />;
  return (
    <AbsoluteFill>
      {s.pullBack ? (
        <PullBackReveal
          focusX={s.pullBack.focusX}
          focusY={s.pullBack.focusY}
          startScale={s.pullBack.startScale}
          startAt={sn(s.pullBack.startAt)}
          duration={sn(s.pullBack.sure)}
        >
          {yigin}
        </PullBackReveal>
      ) : (
        yigin
      )}
      <Parcaciklar mod={s.ortam} />
    </AbsoluteFill>
  );
};

const KONTUR_RENK = "#5a3a22";
const GOLGE_RENK = "rgba(60,35,15,0.45)";

/** Basamaklı (piksel) yol: her noktaya önce yatay, sonra dikey gider. Köşeler sert, eğri yok. */
const basamak = (pts: [number, number][]) =>
  pts.map(([x, y], i) => (i === 0 ? `M ${X(x)} ${Y(y)}` : `H ${X(x)} V ${Y(y)}`)).join(" ");

/** Ekran metni: DoodleBoil ile titreşen piksel yazı, sert kontur ve basamaklı dalgalı altı çizgi. */
const EkranMetni: React.FC<{
  satirlar: string[];
  sure: number;
  fs?: number;
  topY?: number;
  lineH?: number;
  cikis?: boolean;
}> = ({ satirlar, sure, fs = 84, topY = 250, lineH = 96, cikis = true }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const giris = spring({ frame, fps, config: { damping: 200 } });
  const son = cikis ? interpolate(frame, [sure - sn(0.5), sure], [1, 0], CLAMP) : 1;
  const enUzun = Math.max(...satirlar.map((s) => s.length));
  // Jersey 10, 1,2 kat büyütülmüş hâliyle yaklaşık 0,58 em/harf tutar. Metin 900 px'e sığar.
  const fsE = Math.min(fs, 900 / (enUzun * 0.58));
  const genis = Math.round((enUzun * fsE * 0.5) / 24) * 24;
  const yAlt = Math.round((topY + (satirlar.length - 1) * lineH + 34) / 8) * 8;
  const kayma = Math.round(interpolate(giris, [0, 1], [18, 0]) / SNAP) * SNAP;

  const ortak = {
    textAnchor: "middle" as const,
    fontFamily: YAZI_FONTU,
    fontWeight: 400,
    fontSize: (fsE * 1.2) / K, // Jersey 10, Pixelify Sans'tan küçük çizer
    strokeLinejoin: "miter" as const,
  };
  const a = Math.round((540 - genis / 2) / 8) * 8;
  const adim = 24;
  const n = Math.round(genis / adim);
  // Basamaklı dalga: her adımda 8 px yukarı ya da aşağı
  const dalgaPts: [number, number][] = Array.from({ length: n + 1 }, (_, i) => [
    a + i * adim,
    yAlt - (i % 2 === 1 ? 8 : 0),
  ]);
  const dalga = basamak(dalgaPts);

  return (
    <AbsoluteFill style={{ opacity: giris * son, transform: `translateY(${kayma}px)` }}>
      <DoodleBoil hold={BOIL_HOLD} amount={BOIL_MIKTAR} drawOn={sn(1.2)}>
        {satirlar.map((s, i) => {
          const y = topY + i * lineH;
          return (
            <g key={i}>
              {/* sert gölge */}
              <text
                x={X(540)}
                y={Y(y + 6)}
                fill={GOLGE_RENK}
                stroke={GOLGE_RENK}
                strokeWidth={6 / K}
                style={{ strokeDasharray: "none", paintOrder: "stroke" }}
                {...ortak}
              >
                {s}
              </text>
              {/* kahve kontur + krem dolgu */}
              <text
                x={X(540)}
                y={Y(y)}
                fill="#fff3d4"
                stroke={KONTUR_RENK}
                strokeWidth={4 / K}
                style={{ strokeDasharray: "none", paintOrder: "stroke" }}
                {...ortak}
              >
                {s}
              </text>
            </g>
          );
        })}
        {/* basamaklı altı çizgi: kahve kontur + amber çizgi, sert uçlar */}
        <path d={dalga} fill="none" stroke={KONTUR_RENK} strokeWidth={16 / K} strokeLinecap="butt" strokeLinejoin="miter" pathLength={1} />
        <path d={dalga} fill="none" stroke="#f3b441" strokeWidth={8 / K} strokeLinecap="butt" strokeLinejoin="miter" pathLength={1} />
      </DoodleBoil>
    </AbsoluteFill>
  );
};

/* Börte'nin dönüş oku: atlıların hemen üstünde, sağdan sola giden piksel ok (sahne4-ok.png, tam kare
   saydam katman). Titreşimli çizim piksel kenarlarını bozduğu için görsel kullanılır; sağdan sola açılarak
   belirir, sonda solar. */
const DonusOku: React.FC<{ sure: number }> = ({ sure }) => {
  const frame = useCurrentFrame();
  const acilma = interpolate(frame, [0, sn(2)], [0, 100], { ...CLAMP, easing: Easing.inOut(Easing.sin) });
  const opacity = interpolate(frame, [sure - sn(0.65), sure], [1, 0], CLAMP);
  return (
    <AbsoluteFill style={{ opacity, clipPath: `inset(0 0 0 ${snap((100 - acilma) * (W / 100))}px)` }}>
      <Img src={staticFile("sahne4-ok.png")} style={{ width: W, height: H, ...PIKSEL_STIL }} />
    </AbsoluteFill>
  );
};

/** Rüzgârda sallanan piksel çimen şeridi: 4 px'lik kare bloklar, ekranın alt kenarına kök salar
    (en alt blok y = H - 4). Blur yok, gradyan yok. Salınım blok adımlarıyla olur. */
const CIMEN_RENKLERI = ["#5b8a47", "#6f9a4a", "#8fb85f", "#a9c874"];
const Cimen: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const adet = 40;
  const yollar = CIMEN_RENKLERI.map(() => "");

  for (let i = 0; i < adet; i++) {
    const r1 = random(`cimen-x-${i}`);
    const r2 = random(`cimen-h-${i}`);
    const r3 = random(`cimen-p-${i}`);
    const r4 = random(`cimen-c-${i}`);
    const x0 = Math.round(((i / adet) * (W + 60) - 30 + r1 * 24) / BLOK) * BLOK;
    const n = 18 + Math.floor(r2 * 24); // 18–41 blok = 72–164 px (hepsi y > 1750)
    const gen = r3 > 0.5 ? 2 : 1; // taban genişliği (blok)
    const w = 30 / (26 + r3 * 22); // açısal hız (rad/sn)
    const sal = Math.sin(t * w + r3 * 6.283) * (12 + r2 * 14);
    const ci = Math.floor(r4 * CIMEN_RENKLERI.length);
    for (let j = 0; j < n; j++) {
      const k = j / n;
      const dx = Math.round((sal * k * k) / BLOK) * BLOK;
      const y = H - (j + 1) * BLOK; // j=0: en alt satır, kök ekranın altında
      const bw = (j < n * 0.45 ? gen : 1) * BLOK;
      const renk = j >= n - 2 ? CIMEN_RENKLERI.length - 1 : ci; // uç açık renk
      yollar[renk] += `M${x0 + dx} ${y}h${bw}v${BLOK}h${-bw}z`;
    }
  }

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" shapeRendering="crispEdges">
        {yollar.map((d, i) => (
          <path key={i} d={d} fill={CIMEN_RENKLERI[i]} />
        ))}
      </svg>
    </AbsoluteFill>
  );
};

/** Basamaklı sıcak gölge (gradyan yok): üstte hafif bantlar, altta altyazı okunurluğu için
    y≈1300'den başlayan bantlar. Piksel sanatındaki "banding" gibi. */
const GOLGE_BANTLARI: [number, number, number][] = [
  [0, 200, 0.22],
  [200, 400, 0.12],
  [400, 560, 0.05],
  [1300, 1380, 0.08],
  [1380, 1460, 0.16],
  [1460, 1560, 0.26],
  [1560, 1680, 0.36],
  [1680, 1920, 0.48],
];
const SicakGolge: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    {GOLGE_BANTLARI.map(([y0, y1, a], i) => (
      <div
        key={i}
        style={{ position: "absolute", left: 0, right: 0, top: y0, height: y1 - y0, background: `rgba(50,28,14,${a})` }}
      />
    ))}
  </AbsoluteFill>
);

/* KineticCaptions içindeki yazı tipi, kontur ve gölge efekt dosyasında sabit. Efekt dosyasına
   dokunmadan sarmalayıcıdan CSS ile piksel yazı tipine ve sert gölgeye çekiliyor. */
const ALTYAZI_CSS = `
img { image-rendering: pixelated; }
.altyazi-sicak div {
  font-family: ${YAZI_FONTU} !important;
  font-weight: 400 !important;
}
.altyazi-sicak span {
  -webkit-text-stroke: 8px #4a2e1a !important;
  paint-order: stroke fill !important;
  text-shadow: 0 6px 0 rgba(60,35,15,0.55) !important;
}
`;

/* ------------------------------------------------------------------ */
/*  Ana bileşen                                                        */
/* ------------------------------------------------------------------ */
export type CengizHanProps = {
  /** Ses dosyaları video/public/ içinde hazırsa true yap. */
  sesler?: boolean;
};

export const CengizHan: React.FC<CengizHanProps> = ({ sesler = false }) => {
  const baslikBas = sn(ZAMAN.BASLIK_BAS);
  const baslikBit = sn(ZAMAN.SAHNE_ZAMANLARI[0][1]);
  const ctaBas = sn(ZAMAN.CTA_BAS);
  const okBas = sn(ZAMAN.OK_BAS);
  const okBit = sn(ZAMAN.SAHNE_ZAMANLARI[3][1]);

  return (
    <AbsoluteFill style={{ background: "#3a2a1c" }}>
      {/* Genel piksel netliği kuralı ve altyazı stili */}
      <style>{ALTYAZI_CSS}</style>

      {/* 1) Sahneler: beş katmanlı paralaks, çapraz solmayla bağlı */}
      {SAHNELER.map((s, i) => {
        const from = i === 0 ? 0 : sn(s.bas) - FADE;
        const dur = sn(s.bit) - from;
        return (
          <Sequence key={s.no} from={from} durationInFrames={dur}>
            <YumusakGiris aktif={i !== 0}>
              <SahneIcerigi s={s} sure={dur} />
            </YumusakGiris>
          </Sequence>
        );
      })}

      {/* 2) Basamaklı sıcak gölge (kâğıt dokusu katmanı kaldırıldı) */}
      <SicakGolge />

      {/* 3) Piksel çimen blokları */}
      <Cimen />

      {/* 4) Elle çizilmiş piksel yazı ve çizimler (DoodleBoil) */}
      <Sequence from={baslikBas} durationInFrames={baslikBit - baslikBas} layout="none">
        <EkranMetni satirlar={["Bozkırın Çocuğu"]} sure={baslikBit - baslikBas} fs={110} topY={330} />
      </Sequence>

      {EKRAN_METINLERI.map((m, i) => (
        <Sequence key={i} from={sn(m.bas)} durationInFrames={sn(m.bit) - sn(m.bas)} layout="none">
          <EkranMetni satirlar={m.satirlar} sure={sn(m.bit) - sn(m.bas)} />
        </Sequence>
      ))}

      {/* Sahne 4: Börte'nin dönüş yolu */}
      <Sequence from={okBas} durationInFrames={okBit - okBas} layout="none">
        <DonusOku sure={okBit - okBas} />
      </Sequence>

      {/* Kapanış çağrısı: 56,2. sn'den videonun sonuna */}
      <Sequence from={ctaBas} durationInFrames={TOPLAM_KARE - ctaBas} layout="none">
        <EkranMetni
          satirlar={["Sıradaki karakter?", "Timur mu, Attila mı?"]}
          sure={TOPLAM_KARE - ctaBas}
          fs={88}
          topY={300}
          lineH={104}
          cikis={false}
        />
      </Sequence>

      {/* 5) Altyazı: kelimeler Türkçe kurallarla önceden büyütüldü, lang="tr" ek güvence. */}
      <div className="altyazi-sicak" lang="tr" style={{ position: "absolute", inset: 0, transform: "translateY(-100px)" }}>
        <KineticCaptions words={KELIMELER} perPage={3} highlight="#ffd479" fontSize={68} onlyVisible popFrom={0.85} />
      </div>

      {/* 6) Seslendirme. Müzik paylaşırken Instagram'ın kütüphanesinden eklenir (telif güvenli). */}
      {sesler ? <Audio src={staticFile("anlatim.mp3")} /> : null}
    </AbsoluteFill>
  );
};
