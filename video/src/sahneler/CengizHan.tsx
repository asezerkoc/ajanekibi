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
import { DoodleBoil } from "../effects/DoodleBoil";
import { KineticCaptions } from "../effects/KineticCaptions";
import type { CaptionWord } from "../effects/KineticCaptions";

/* ------------------------------------------------------------------ */
/*  Yazı tipleri. latin-ext şart: ğ, ş, İ, ı bu alt kümede.            */
/*  loadFont, font yüklenene kadar render'ı bekletir (delayRender).    */
/*  KineticCaptions "Montserrat" adını ister, o da burada yüklenir.    */
/* ------------------------------------------------------------------ */
/* Yazı tipleri video/public/fonts/ içinden yüklenir: render ortamı internete çıkamasa da çalışır. */
const LATIN =
  "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD";
const LATIN_EXT =
  "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF";

const yaziTipiYukle = (aile: string, agirlik: string) => {
  const bekle = delayRender(`${aile} yazı tipi`);
  Promise.all(
    ([["latin", LATIN], ["latin-ext", LATIN_EXT]] as const).map(([alt, aralik]) => {
      const font = new FontFace(aile, `url(${staticFile(`fonts/${aile}-${alt}.woff2`)}) format("woff2")`, {
        weight: agirlik,
        unicodeRange: aralik,
      });
      document.fonts.add(font);
      return font.load();
    }),
  ).then(() => continueRender(bekle), (e) => cancelRender(e));
};

yaziTipiYukle("Caveat", "700");
yaziTipiYukle("Montserrat", "900");
const caveat = { fontFamily: "Caveat" };

/* ------------------------------------------------------------------ */
/*  Genel ayarlar: 1080x1920, 30 fps, 1800 kare (60 sn)                */
/* ------------------------------------------------------------------ */
const W = 1080;
const H = 1920;
const FADE = 18; // sahneler arası yumuşak çapraz geçiş (0,6 sn)
const BOIL_HOLD = 2; // DoodleBoil: iki karede bir titreşim
const CLAMP = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
};

const YAZI_FONTU = `"${caveat.fontFamily}", "Patrick Hand", "Segoe Print", "Bradley Hand", cursive`;

/* DoodleBoil içindeki SVG 1920x1080 viewBox'lı. 1080x1920 ekranda 0,5625 ölçeğiyle
   dikey ortalanır. X/Y, ekran pikselini (1080x1920) SVG koordinatına çevirir.
   Satır içi svg'nin kırpma alanı öğenin kendi kutusudur (1080x1920), viewBox değil;
   bu yüzden letterbox alanına da çizilebilir. */
const K = 1080 / 1920;
const OFF = (1920 - 1080 * K) / 2;
const X = (sx: number) => sx / K;
const Y = (sy: number) => (sy - OFF) / K;

/* ------------------------------------------------------------------ */
/*  Sahne zaman çizelgesi (kare)                                       */
/* ------------------------------------------------------------------ */
type SahneTanimi = {
  baslangic: number;
  bitis: number;
  gorsel: string;
  /** Ken-Burns: [başlangıç zoom, bitiş zoom, yatay kayma px, dikey kayma px] */
  hareket: [number, number, number, number];
};

const SAHNELER: SahneTanimi[] = [
  { baslangic: 0, bitis: 150, gorsel: "sahne1-bozkir-yurt.png", hareket: [1, 1, 0, 0] }, // PullBackReveal
  { baslangic: 150, bitis: 270, gorsel: "sahne2-dogum.png", hareket: [1.06, 1.14, -10, 12] },
  { baslangic: 270, bitis: 492, gorsel: "sahne3-yetim.png", hareket: [1.1, 1.08, -28, 0] },
  { baslangic: 492, bitis: 750, gorsel: "sahne4-borte-donus.png", hareket: [1.07, 1.13, 26, -8] },
  { baslangic: 750, bitis: 1032, gorsel: "sahne5-kurultay.png", hareket: [1.06, 1.15, 0, 14] },
  { baslangic: 1032, bitis: 1302, gorsel: "sahne6-sefer.png", hareket: [1.14, 1.07, 20, 0] },
  { baslangic: 1302, bitis: 1545, gorsel: "sahne7-bos-eyer.png", hareket: [1.06, 1.13, 0, -16] },
  { baslangic: 1545, bitis: 1800, gorsel: "sahne8-son-bozkir.png", hareket: [1, 1, 0, 0] }, // PullBackReveal
];

/* Ekran metinleri (onaylı metindeki 5 ekran metni) */
type EkranMetniTanimi = { from: number; sure: number; satirlar: string[] };
const EKRAN_METINLERI: EkranMetniTanimi[] = [
  { from: 174, sure: 270 - 174, satirlar: ["Yaklaşık 1162.", "Bozkırda bir çocuk doğdu."] },
  { from: 295, sure: 492 - 295, satirlar: ["Babasız, kabilesiz büyüdü."] },
  { from: 780, sure: 1032 - 780, satirlar: ["1206: “Cengiz Han” dediler."] },
  { from: 1135, sure: 1302 - 1135, satirlar: ["Şehirler düştü.", "Bedeli ağır oldu."] },
  { from: 1320, sure: 1545 - 1320, satirlar: ["1227'de öldü.", "Mezarı hâlâ bilinmiyor."] },
];

/* ------------------------------------------------------------------ */
/*  Anlatım ve altyazı zamanlaması                                     */
/*  Gerçek seslendirme gelince bas/bit değerlerini güncelle.           */
/* ------------------------------------------------------------------ */
const ANLATIM: { t: string; bas: number; bit: number }[] = [
  { t: "Elinde bir pıhtı kanla doğduğu söylenir. Mezarı ise hâlâ bulunamadı.", bas: 0.3, bit: 4.9 },
  { t: "Yaklaşık 1162. Moğol bozkırında bir çocuk doğdu. Adı Temüçin'di.", bas: 5.15, bit: 8.9 },
  {
    t: "Daha çocukken babasını kaybetti. Kabilesi ailesini yüzüstü bıraktı. Annesi Hö'elün, çocuklarını bozkırın en zor günlerinde ayakta tuttu.",
    bas: 9.15,
    bit: 16.25,
  },
  {
    t: "Temüçin her yenilgiden bir ders çıkardı. Eşi Börte kaçırılınca müttefikleriyle birlikte onu geri aldı. Bu olay, yükselişinin dönüm noktası sayılır.",
    bas: 16.5,
    bit: 24.8,
  },
  {
    t: "1206'da boylar bir araya geldi ve ona “Cengiz Han” dediler. Terfiyi soya değil yeteneğe bağladı, yazıyı benimsedi, Yam adlı ulak ağını kurdu.",
    bas: 25.05,
    bit: 34.25,
  },
  {
    t: "Sonra orduları Çin'den Orta Asya'ya yürüdü. Şehirler düştü. Bu yürüyüş geride çok ağır bir bedel de bıraktı. Hikâyenin o yüzünü unutmamak gerek.",
    bas: 34.5,
    bit: 43.25,
  },
  {
    t: "1227'de seferdeyken öldü. Mezarı hâlâ bilinmiyor. Bozkırın çocuğunun attığı temel, ardıllarının döneminde tarihin en büyük bitişik kara imparatorluğuna dönüştü.",
    bas: 43.5,
    bit: 51.4,
  },
  { t: "Kahraman mı, yıkıcı mı? Belki de ikisinin gölgesinde geçen bir hayat.", bas: 51.65, bit: 56.25 },
];

/* Her cümlenin süresi kelimelere uzunluklarına göre bölünür (rakamlar ve noktalama daha uzun okunur).
   Metin Türkçe kurallarla önceden büyütülür (i→İ, ı→I). Efektin text-transform'u bundan sonra
   zaten büyük olan metne dokunmaz, böylece TEMÜÇİN / BİLİNMİYOR tarayıcıdan bağımsız doğru çıkar. */
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
/*  Yardımcı bileşenler                                                */
/* ------------------------------------------------------------------ */

/** Yavaş Ken-Burns: yumuşak yakınlaşma ve kayma. */
const KenBurns: React.FC<{ src: string; sure: number; hareket: [number, number, number, number] }> = ({
  src,
  sure,
  hareket,
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, sure], [0, 1], { ...CLAMP, easing: Easing.inOut(Easing.sin) });
  const [z0, z1, dx, dy] = hareket;
  const scale = interpolate(p, [0, 1], [z0, z1]);
  const tx = interpolate(p, [0, 1], [-dx, dx]);
  const ty = interpolate(p, [0, 1], [-dy, dy]);
  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#2a1a10" }}>
      <Img
        src={staticFile(src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `translate(${tx}px, ${ty}px) scale(${scale})`,
        }}
      />
    </AbsoluteFill>
  );
};

/** Sahne girişinde yumuşak çapraz geçiş (ilk sahne hariç). */
const YumusakGiris: React.FC<{ aktif: boolean; children: React.ReactNode }> = ({ aktif, children }) => {
  const frame = useCurrentFrame();
  const opacity = aktif ? interpolate(frame, [0, FADE], [0, 1], CLAMP) : 1;
  return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
};

/** El yazısı ekran metni: DoodleBoil ile titreşen yazı + elle çizilmiş altı çizgi. */
const EkranMetni: React.FC<{
  satirlar: string[];
  sure: number;
  fs?: number;
  topY?: number;
  lineH?: number;
  cikis?: boolean;
}> = ({ satirlar, sure, fs = 72, topY = 250, lineH = 100, cikis = true }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const giris = spring({ frame, fps, config: { damping: 200 } });
  const son = cikis ? interpolate(frame, [sure - 16, sure], [1, 0], CLAMP) : 1;
  const yAlt = topY + (satirlar.length - 1) * lineH + 34;
  const genis = Math.min(900, Math.max(...satirlar.map((s) => s.length)) * fs * 0.42);

  return (
    <AbsoluteFill
      style={{
        opacity: giris * son,
        transform: `translateY(${interpolate(giris, [0, 1], [18, 0])}px)`,
      }}
    >
      <DoodleBoil hold={BOIL_HOLD} amount={9} drawOn={36}>
        {satirlar.map((s, i) => {
          const y = topY + i * lineH;
          return (
            <g key={i}>
              {/* yumuşak gölge */}
              <text
                x={X(540 + 4)}
                y={Y(y + 5)}
                textAnchor="middle"
                fontFamily={YAZI_FONTU}
                fontWeight={700}
                fontSize={fs / K}
                fill="rgba(70,40,20,0.55)"
              >
                {s}
              </text>
              <text
                x={X(540)}
                y={Y(y)}
                textAnchor="middle"
                fontFamily={YAZI_FONTU}
                fontWeight={700}
                fontSize={fs / K}
                fill="#fff3d4"
              >
                {s}
              </text>
            </g>
          );
        })}
        <path
          d={`M ${X(540 - genis / 2)} ${Y(yAlt)} Q ${X(540)} ${Y(yAlt + 18)} ${X(540 + genis / 2)} ${Y(yAlt - 6)}`}
          fill="none"
          stroke="#f3b441"
          strokeWidth={9 / K}
          strokeLinecap="round"
          pathLength={1}
        />
      </DoodleBoil>
    </AbsoluteFill>
  );
};

/** Sahne 4: Börte'yi geri getiren dönüş yolu, elle çizilmiş ok. */
const DonusOku: React.FC<{ sure: number }> = ({ sure }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [sure - 20, sure], [1, 0], CLAMP);
  return (
    <AbsoluteFill style={{ opacity }}>
      <DoodleBoil hold={BOIL_HOLD} amount={8} drawOn={60}>
        <path
          d={`M ${X(930)} ${Y(640)} C ${X(740)} ${Y(520)} ${X(470)} ${Y(740)} ${X(230)} ${Y(600)}`}
          fill="none"
          stroke="#fff3d4"
          strokeWidth={8 / K}
          strokeLinecap="round"
          pathLength={1}
        />
        <path
          d={`M ${X(290)} ${Y(602)} L ${X(230)} ${Y(600)} L ${X(262)} ${Y(651)}`}
          fill="none"
          stroke="#fff3d4"
          strokeWidth={8 / K}
          strokeLinecap="round"
          strokeLinejoin="round"
          pathLength={1}
        />
      </DoodleBoil>
    </AbsoluteFill>
  );
};

/** Rüzgârda sallanan çimen (en altta, ince bir şerit, y>1760). Altyazı bölgesinin (≈1450–1700) altında kalır. */
const Cimen: React.FC = () => {
  const frame = useCurrentFrame();
  const renkler = ["#4f7a35", "#6f9a45", "#93b457", "#b9c46a"];
  const adet = 46;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%">
        {Array.from({ length: adet }).map((_, i) => {
          const r1 = random(`cimen-x-${i}`);
          const r2 = random(`cimen-h-${i}`);
          const r3 = random(`cimen-p-${i}`);
          const r4 = random(`cimen-c-${i}`);
          const x = (i / adet) * (W + 60) - 30 + r1 * 20;
          const h = 70 + r2 * 90;
          const sal = Math.sin(frame / (26 + r3 * 22) + r3 * 6.28) * (14 + r2 * 12);
          const renk = renkler[Math.floor(r4 * renkler.length)];
          return (
            <path
              key={i}
              d={`M${x - 7} ${H} Q${x - 2 + sal * 0.35} ${H - h * 0.55} ${x + sal} ${H - h} Q${x + 4 + sal * 0.35} ${H - h * 0.5} ${x + 7} ${H} Z`}
              fill={renk}
              opacity={0.88}
            />
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};

/** Süzülen polen ve ateş böceği parçacıkları. */
const Parcaciklar: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {Array.from({ length: 28 }).map((_, i) => {
        const r1 = random(`pc-x-${i}`);
        const r2 = random(`pc-y-${i}`);
        const r3 = random(`pc-s-${i}`);
        const r4 = random(`pc-f-${i}`);
        const hiz = 0.3 + r3 * 0.5;
        const x = (r1 * W + frame * hiz) % W;
        const y = (((r2 * H - frame * (0.2 + r3 * 0.3)) % H) + H) % H + Math.sin(frame / 40 + r4 * 6.28) * 24;
        const boyut = 4 + r3 * 7;
        const parilti = 0.25 + 0.3 * (0.5 + 0.5 * Math.sin(frame / 18 + r4 * 6.28));
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x,
              top: y,
              width: boyut,
              height: boyut,
              borderRadius: "50%",
              background: "#fff1b8",
              opacity: parilti,
              boxShadow: "0 0 14px 5px rgba(255,226,150,0.55)",
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

/** Sıcak ışık, kağıt dokusu, kenar kararması. Üstte ve altta yumuşak gölge (alt gölge ≈ y>1420, altyazı okunurluğu için). */
const SulubotyaKatmani: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    <AbsoluteFill style={{ background: "rgba(255,200,120,0.10)", mixBlendMode: "soft-light" }} />
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(ellipse at 50% 45%, rgba(255,214,140,0) 45%, rgba(90,50,30,0.38) 100%)",
        mixBlendMode: "multiply",
      }}
    />
    <AbsoluteFill
      style={{
        background: "linear-gradient(180deg, rgba(70,40,25,0.36) 0%, rgba(70,40,25,0) 28%)",
      }}
    />
    <AbsoluteFill
      style={{
        background: "linear-gradient(0deg, rgba(50,30,20,0.46) 0%, rgba(50,30,20,0) 26%)",
      }}
    />
    <svg width="100%" height="100%" style={{ position: "absolute", inset: 0, opacity: 0.14, mixBlendMode: "multiply" }}>
      <filter id="kagit-dokusu">
        <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed={7} />
        <feColorMatrix type="matrix" values="0 0 0 0 0.55  0 0 0 0 0.42  0 0 0 0 0.30  0 0 0 0.9 0" />
      </filter>
      <rect width="100%" height="100%" filter="url(#kagit-dokusu)" />
    </svg>
  </AbsoluteFill>
);

/* KineticCaptions'ın dış çizgisi efektin içinde siyaha sabit ve prop sunmuyor.
   Efekt dosyasına dokunmadan, sarmalayıcı altındaki kelime span'larında sıcak kahverengiye çekiyoruz. */
const ALTYAZI_CSS = `
.altyazi-sicak span {
  -webkit-text-stroke-color: #5a3418 !important;
  text-shadow: 0 6px 0 rgba(70, 38, 16, 0.38) !important;
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
  return (
    <AbsoluteFill style={{ background: "#2a1a10" }}>
      {/* 1) Sahneler */}
      {SAHNELER.map((s, i) => {
        const from = i === 0 ? 0 : s.baslangic - FADE;
        const dur = s.bitis - from;
        const sureSahne = s.bitis - s.baslangic;

        let icerik: React.ReactNode;
        if (i === 0) {
          // Açılış: yurt detayından geniş bozkıra çekilme
          icerik = (
            <PullBackReveal focusX={68} focusY={62} startScale={3.2} startAt={10} duration={90}>
              <Img
                src={staticFile(s.gorsel)}
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
            </PullBackReveal>
          );
        } else if (i === SAHNELER.length - 1) {
          // Kapanış: taş ve çiçekten (kadrajın %30 x, %62 y noktası) sonsuz bozkıra çekilme.
          // Odak y=62 → taş ≈ y 1190 px, altyazı (≈1450–1700) ve alt gradyanın (y>1420) üstünde.
          icerik = (
            <PullBackReveal focusX={30} focusY={62} startScale={3} startAt={12} duration={130}>
              <Img
                src={staticFile(s.gorsel)}
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
            </PullBackReveal>
          );
        } else {
          icerik = <KenBurns src={s.gorsel} sure={sureSahne + FADE} hareket={s.hareket} />;
        }

        return (
          <Sequence key={i} from={from} durationInFrames={dur}>
            <YumusakGiris aktif={i !== 0}>{icerik}</YumusakGiris>
          </Sequence>
        );
      })}

      {/* 2) Sulu boya ışığı, doku, kenar kararması */}
      <SulubotyaKatmani />

      {/* 3) Yaşayan detaylar: parçacıklar ve çimen */}
      <Parcaciklar />
      <Cimen />

      {/* 4) Elle çizilmiş yazı ve çizimler (DoodleBoil) */}
      {/* Başlık: PullBackReveal bittikten sonra */}
      <Sequence from={100} durationInFrames={50} layout="none">
        <EkranMetni satirlar={["Bozkırın Çocuğu"]} sure={50} fs={112} topY={330} />
      </Sequence>

      {EKRAN_METINLERI.map((m, i) => (
        <Sequence key={i} from={m.from} durationInFrames={m.sure} layout="none">
          <EkranMetni satirlar={m.satirlar} sure={m.sure} />
        </Sequence>
      ))}

      {/* Sahne 4: Börte'nin dönüş yolu */}
      <Sequence from={520} durationInFrames={230} layout="none">
        <DonusOku sure={230} />
      </Sequence>

      {/* Kapanış çağrısı: 56,2. sn'den itibaren, anlatım bittikten sonra */}
      <Sequence from={1686} durationInFrames={114} layout="none">
        <EkranMetni
          satirlar={["Sıradaki karakter?", "Timur mu, Attila mı?"]}
          sure={114}
          fs={84}
          topY={300}
          lineH={110}
          cikis={false}
        />
      </Sequence>

      {/* 5) Altyazı: kelimeler Türkçe kurallarla önceden büyütüldü, lang="tr" ek güvence.
             Dış çizgi rengi sıcak kahverengi (ALTYAZI_CSS). */}
      <div className="altyazi-sicak" lang="tr" style={{ position: "absolute", inset: 0 }}>
        <style>{ALTYAZI_CSS}</style>
        <KineticCaptions words={KELIMELER} perPage={3} highlight="#ffd479" fontSize={72} />
      </div>

      {/* 6) Ses (isteğe bağlı) */}
      {sesler ? (
        <>
          <Audio src={staticFile("anlatim.mp3")} />
          <Audio
            src={staticFile("muzik-bozkir.mp3")}
            loop
            volume={(f) => interpolate(f, [0, 45, 1700, 1800], [0, 0.22, 0.22, 0], CLAMP)}
          />
          <Audio
            src={staticFile("ruzgar.mp3")}
            loop
            volume={(f) => interpolate(f, [0, 30, 1740, 1800], [0, 0.18, 0.18, 0], CLAMP)}
          />
          <Sequence from={492} durationInFrames={258}>
            <Audio
              src={staticFile("nal-sesi.mp3")}
              volume={(f) => interpolate(f, [0, 40, 200, 258], [0, 0.18, 0.18, 0], CLAMP)}
            />
          </Sequence>
          <Sequence from={750} durationInFrames={200}>
            <Audio
              src={staticFile("kalabalik.mp3")}
              volume={(f) => interpolate(f, [0, 30, 150, 200], [0, 0.16, 0.16, 0], CLAMP)}
            />
          </Sequence>
        </>
      ) : null}
    </AbsoluteFill>
  );
};
