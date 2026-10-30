import React from "react";
import {
  AbsoluteFill,
  Easing,
  Sequence,
  cancelRender,
  continueRender,
  delayRender,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

/* İstanbul'un Fethi 1453: 5 dakikalık motion graphics örneği (1920x1080, 30 fps, sessiz).
   Piksel tarzı değil; düz vektör şekiller, çizilen harita ve kinetik tipografi. 11 bölüm, her biri sürekli hareketli. */
export const F_FPS = 30;
const sn = (s: number) => Math.round(s * F_FPS);

const BOLUMLER: { bas: number; sure: number }[] = [
  { bas: 0, sure: 24 },
  { bas: 24, sure: 32 },
  { bas: 56, sure: 32 },
  { bas: 88, sure: 32 },
  { bas: 120, sure: 30 },
  { bas: 150, sure: 32 },
  { bas: 182, sure: 36 },
  { bas: 218, sure: 30 },
  { bas: 248, sure: 22 },
  { bas: 270, sure: 18 },
  { bas: 288, sure: 12 },
];
export const F_KARE = sn(300);

const R = {
  gece: "#0f1b2d",
  gece2: "#16263d",
  deniz: "#1d3b5a",
  kara: "#e9dcc0",
  kara2: "#d6c49f",
  altin: "#e8b04a",
  kirmizi: "#c8423b",
  krem: "#f4ead5",
  turkuaz: "#2a9d8f",
  soluk: "#8aa0b8",
};
const FONT = "Montserrat, sans-serif";

const bekle = delayRender("Montserrat (Fetih 1453)");
Promise.all(
  (["latin", "latin-ext"] as const).map((alt) => {
    const font = new FontFace("Montserrat", `url(${staticFile(`fonts/Montserrat-${alt}.woff2`)}) format("woff2")`, {
      weight: "100 900",
    });
    document.fonts.add(font);
    return font.load();
  }),
).then(() => continueRender(bekle), (e) => cancelRender(e));

/* 0→1 arası yumuşak ilerleme; a ve b saniye cinsinden. */
const ac = (f: number, a: number, b: number) =>
  interpolate(f, [sn(a), sn(b)], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

/* Bir noktalar dizisi boyunca t (0-1) konumundaki nokta. */
const yolNoktasi = (yol: [number, number][], t: number): [number, number] => {
  const uz = yol.slice(1).map((p, i) => Math.hypot(p[0] - yol[i][0], p[1] - yol[i][1]));
  let kalan = Math.max(0, Math.min(1, t)) * uz.reduce((a, b) => a + b, 0);
  for (let i = 0; i < uz.length; i++) {
    if (kalan <= uz[i]) {
      const k = uz[i] === 0 ? 0 : kalan / uz[i];
      return [yol[i][0] + (yol[i + 1][0] - yol[i][0]) * k, yol[i][1] + (yol[i + 1][1] - yol[i][1]) * k];
    }
    kalan -= uz[i];
  }
  return yol[yol.length - 1];
};

/* ---------- Ortak parçalar ---------- */

/* Arka plan: koyu lacivert, yavaşça kayan ızgara ve süzülen halkalar. */
const Fon: React.FC<{ renk?: string }> = ({ renk = R.gece }) => {
  const f = useCurrentFrame();
  const kay = (f * 0.4) % 80;
  return (
    <AbsoluteFill style={{ background: renk, overflow: "hidden" }}>
      <svg width={1920} height={1080} style={{ position: "absolute", opacity: 0.08 }}>
        {Array.from({ length: 26 }, (_, i) => (
          <line key={`d${i}`} x1={i * 80 - kay} y1={0} x2={i * 80 - kay} y2={1080} stroke={R.krem} strokeWidth={1} />
        ))}
        {Array.from({ length: 15 }, (_, i) => (
          <line key={`y${i}`} x1={0} y1={i * 80 + kay * 0.5} x2={1920} y2={i * 80 + kay * 0.5} stroke={R.krem} strokeWidth={1} />
        ))}
      </svg>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {[0, 1, 2, 3, 4].map((i) => (
          <circle
            key={i}
            cx={(300 + i * 380 + Math.sin(f / 90 + i) * 60) % 1920}
            cy={540 + Math.cos(f / 110 + i * 2) * 380}
            r={60 + i * 24}
            fill="none"
            stroke={i % 2 ? R.altin : R.turkuaz}
            strokeOpacity={0.12}
            strokeWidth={3}
          />
        ))}
      </svg>
    </AbsoluteFill>
  );
};

/* Kelime kelime yükselen yazı. bas saniye cinsinden (bölüm başına göre). */
const Kelimeler: React.FC<{
  metin: string;
  bas: number;
  boyut?: number;
  renk?: string;
  kalinlik?: number;
  hizala?: "left" | "center";
  stil?: React.CSSProperties;
}> = ({ metin, bas, boyut = 64, renk = R.krem, kalinlik = 800, hizala = "left", stil }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div
      style={{
        position: "absolute",
        fontFamily: FONT,
        fontSize: boyut,
        fontWeight: kalinlik,
        color: renk,
        lineHeight: 1.15,
        textAlign: hizala,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: hizala === "center" ? "center" : "flex-start",
        gap: `0 ${boyut * 0.28}px`,
        ...stil,
      }}
    >
      {metin.split(" ").map((k, i) => {
        const s = spring({ frame: f - sn(bas) - i * 3, fps, config: { damping: 16, stiffness: 120 } });
        return (
          <span
            key={i}
            style={{ display: "inline-block", opacity: Math.min(1, s * 1.4), transform: `translateY(${(1 - s) * boyut * 0.7}px)` }}
          >
            {k}
          </span>
        );
      })}
    </div>
  );
};

/* Sayıyı a'dan b'ye sayar. */
const Sayac: React.FC<{ a: number; b: number; bas: number; bit: number; ek?: string; stil?: React.CSSProperties }> = ({
  a,
  b,
  bas,
  bit,
  ek = "",
  stil,
}) => {
  const f = useCurrentFrame();
  const d = Math.round(a + (b - a) * ac(f, bas, bit));
  return (
    <div style={{ position: "absolute", fontFamily: FONT, fontWeight: 900, color: R.altin, opacity: ac(f, bas - 0.3, bas + 0.2), ...stil }}>
      {d.toLocaleString("tr-TR")}
      {ek}
    </div>
  );
};

/* Bölüm kartı: önce ortada büyük, sonra sol üst köşeye küçülür ve orada etiket olarak kalır. */
const BolumKarti: React.FC<{ no: string; ad: string }> = ({ no, ad }) => {
  const f = useCurrentFrame();
  const gir = ac(f, 0.1, 0.9);
  const kucul = ac(f, 2.6, 3.4);
  const olcek = interpolate(kucul, [0, 1], [1, 0.32]);
  const x = interpolate(kucul, [0, 1], [960, 90]);
  const y = interpolate(kucul, [0, 1], [540, 70]);
  const cizgi = ac(f, 0.4, 1.6);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `translate(${-50 * (1 - kucul)}%, -50%) scale(${olcek})`,
        transformOrigin: "0% 50%",
        fontFamily: FONT,
        opacity: gir,
        zIndex: 10,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 36 }}>
        <div style={{ fontSize: 200, fontWeight: 900, color: R.altin, lineHeight: 1 }}>{no}</div>
        <div style={{ width: 10, height: 170 * cizgi, background: R.kirmizi }} />
        <div style={{ fontSize: 130, fontWeight: 800, color: R.krem, whiteSpace: "nowrap", clipPath: `inset(0 ${100 - cizgi * 100}% 0 0)` }}>
          {ad}
        </div>
      </div>
    </div>
  );
};

/* İçerik bölüm kartı küçüldükten sonra görünür. */
const Icerik: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{ opacity: ac(f, 3.0, 3.8) }}>{children}</AbsoluteFill>;
};

/* Bölümler arası geçiş: başta ve sonda 0,5 sn kararma. */
const Gecis: React.FC<{ sure: number; children: React.ReactNode }> = ({ sure, children }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 15, sn(sure) - 15, sn(sure)], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

/* ---------- Harita ---------- */

const TRAKYA = "M0,170 L560,250 L600,560 L640,860 L0,960 Z";
const SEHIR = "M560,262 L640,860 Q900,840 1150,800 Q1300,760 1400,640 Q1330,560 1180,480 Q950,380 560,262 Z";
const GALATA = "M0,0 H1560 V420 Q1500,520 1425,565 Q1300,470 1180,408 Q900,290 560,215 L0,150 Z";
const ASYA = "M1650,0 H1920 V1080 H1500 Q1570,900 1610,700 Q1630,400 1650,0 Z";
const GEMI_YOLU: [number, number][] = [
  [1600, 470],
  [1520, 380],
  [1380, 300],
  [1200, 230],
  [1020, 230],
  [930, 290],
  [900, 345],
];

const Harita: React.FC<{ ciz: number; children?: React.ReactNode }> = ({ ciz, children }) => (
  <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: "absolute" }}>
    <rect width={1920} height={1080} fill={R.deniz} opacity={ciz} />
    {[TRAKYA, GALATA, ASYA].map((d, i) => (
      <path key={i} d={d} fill={R.kara2} opacity={ciz} stroke={R.gece} strokeWidth={4} />
    ))}
    <path d={SEHIR} fill={R.kara} stroke={R.altin} strokeWidth={6} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - ciz} fillOpacity={ciz} />
    {children}
  </svg>
);

const HaritaEtiketi: React.FC<{ x: number; y: number; metin: string; bas: number; renk?: string; boyut?: number }> = ({
  x,
  y,
  metin,
  bas,
  renk = R.krem,
  boyut = 34,
}) => {
  const f = useCurrentFrame();
  const o = ac(f, bas, bas + 0.6);
  return (
    <text
      x={x}
      y={y + (1 - o) * 20}
      fill={renk}
      opacity={o}
      fontFamily={FONT}
      fontWeight={800}
      fontSize={boyut}
      textAnchor="middle"
      letterSpacing={4}
      style={{ paintOrder: "stroke", stroke: R.gece, strokeWidth: 6 }}
    >
      {metin}
    </text>
  );
};

/* ---------- Bölümler ---------- */

const Acilis: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const halka = ac(f, 0.5, 3);
  const yukari = ac(f, 14, 16);
  const ikonlar = ["kale", "gemi", "top"] as const;
  return (
    <AbsoluteFill>
      <Fon />
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <circle
          cx={960}
          cy={interpolate(yukari, [0, 1], [440, 300])}
          r={330}
          fill="none"
          stroke={R.altin}
          strokeWidth={8}
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - halka}
          transform={`rotate(${-90 + f * 0.3} 960 ${interpolate(yukari, [0, 1], [440, 300])})`}
          opacity={1 - yukari * 0.6}
        />
      </svg>
      <div
        style={{
          position: "absolute",
          width: 1920,
          top: interpolate(yukari, [0, 1], [300, 170]),
          display: "flex",
          justifyContent: "center",
          fontFamily: FONT,
          fontWeight: 900,
          fontSize: interpolate(yukari, [0, 1], [280, 200]),
          color: R.krem,
          letterSpacing: 10,
        }}
      >
        {"1453".split("").map((r, i) => {
          const s = spring({ frame: f - sn(0.6) - i * 6, fps, config: { damping: 12 } });
          return (
            <span key={i} style={{ display: "inline-block", transform: `translateY(${(1 - s) * -300}px)`, opacity: Math.min(1, s * 2) }}>
              {r}
            </span>
          );
        })}
      </div>
      <Kelimeler
        metin="İSTANBUL'UN FETHİ"
        bas={5}
        boyut={110}
        kalinlik={900}
        renk={R.altin}
        hizala="center"
        stil={{ width: 1920, top: interpolate(yukari, [0, 1], [640, 430]) }}
      />
      <Kelimeler
        metin="53 gün süren kuşatmanın hikâyesi"
        bas={9}
        boyut={48}
        kalinlik={500}
        hizala="center"
        stil={{ width: 1920, top: interpolate(yukari, [0, 1], [790, 570]) }}
      />
      {ikonlar.map((ad, i) => {
        const s = spring({ frame: f - sn(16) - i * 8, fps, config: { damping: 12 } });
        const x = 560 + i * 400;
        return (
          <svg key={ad} width={240} height={240} viewBox="0 0 240 240" style={{ position: "absolute", left: x - 120, top: 700, transform: `scale(${s}) translateY(${Math.sin(f / 15 + i) * 6}px)` }}>
            <circle cx={120} cy={120} r={110} fill={R.gece2} stroke={i === 1 ? R.turkuaz : R.altin} strokeWidth={6} />
            {ad === "kale" && (
              <g fill={R.krem}>
                <rect x={60} y={100} width={120} height={70} />
                {[60, 90, 120, 150].map((xx) => (
                  <rect key={xx} x={xx} y={84} width={20} height={20} />
                ))}
                <rect x={105} y={130} width={30} height={40} fill={R.gece2} />
              </g>
            )}
            {ad === "gemi" && (
              <g>
                <path d="M55,140 L185,140 L165,170 L75,170 Z" fill={R.krem} />
                <path d="M120,60 L120,138 L170,138 Z" fill={R.altin} />
                <path d="M115,70 L115,138 L75,138 Z" fill={R.krem} />
              </g>
            )}
            {ad === "top" && (
              <g>
                <rect x={60} y={95} width={120} height={36} rx={14} fill={R.krem} transform="rotate(-15 120 113)" />
                <circle cx={95} cy={150} r={22} fill={R.altin} />
                <circle cx={150} cy={150} r={22} fill={R.altin} />
              </g>
            )}
          </svg>
        );
      })}
    </AbsoluteFill>
  );
};

const Sehir: React.FC = () => {
  const f = useCurrentFrame();
  const zum = interpolate(f, [0, sn(32)], [1.0, 1.12]);
  return (
    <AbsoluteFill>
      <Fon />
      <Icerik>
        <AbsoluteFill style={{ transform: `scale(${zum})`, transformOrigin: "50% 55%" }}>
          <Harita ciz={ac(f, 3, 7)}>
            <HaritaEtiketi x={1020} y={980} metin="MARMARA DENİZİ" bas={7} />
            <HaritaEtiketi x={1010} y={345} metin="HALİÇ" bas={9} boyut={28} />
            <HaritaEtiketi x={1575} y={760} metin="BOĞAZ" bas={11} />
            <HaritaEtiketi x={980} y={640} metin="KONSTANTİNOPOLİS" bas={13} renk={R.gece} boyut={40} />
          </Harita>
        </AbsoluteFill>
        <div
          style={{
            position: "absolute",
            left: 60,
            bottom: 60,
            width: 640,
            padding: "36px 40px",
            background: R.gece,
            borderLeft: `10px solid ${R.altin}`,
            opacity: ac(f, 16, 17),
          }}
        >
          <Kelimeler metin="MS 330'dan beri Doğu Roma'nın (Bizans) başkenti" bas={16.5} boyut={40} kalinlik={600} stil={{ position: "relative" }} />
          <div style={{ position: "relative", height: 130, marginTop: 20 }}>
            <Sayac a={0} b={1123} bas={21} bit={25} ek=" yıl" stil={{ fontSize: 110, left: 0, top: 0 }} />
          </div>
        </div>
      </Icerik>
      <BolumKarti no="01" ad="Şehir" />
    </AbsoluteFill>
  );
};

const Sultan: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const portre = spring({ frame: f - sn(3.5), fps, config: { damping: 14 } });
  const kuleBloklari = 9;
  return (
    <AbsoluteFill>
      <Fon renk={R.gece2} />
      <Icerik>
        <svg width={700} height={800} viewBox="0 0 700 800" style={{ position: "absolute", left: 120, top: 180, transform: `scale(${portre})` }}>
          <circle cx={350} cy={400} r={300} fill={R.gece} stroke={R.altin} strokeWidth={8} />
          <path d="M150,700 Q350,520 550,700 Z" fill={R.kirmizi} />
          <rect x={300} y={420} width={100} height={120} fill={R.kara2} />
          <ellipse cx={350} cy={380} rx={95} ry={115} fill={R.kara} />
          <ellipse cx={350} cy={250} rx={150} ry={110} fill={R.krem} />
          <path d="M310,180 Q350,110 390,180 Z" fill={R.kirmizi} />
          <path d="M290,440 Q350,520 410,440 Q350,470 290,440 Z" fill="#5b3a29" />
          <circle cx={318} cy={370} r={8} fill={R.gece} />
          <circle cx={382} cy={370} r={8} fill={R.gece} />
        </svg>
        <Kelimeler metin="II. Mehmed" bas={4.5} boyut={110} kalinlik={900} stil={{ left: 900, top: 200 }} />
        <Sayac a={0} b={21} bas={7.5} bit={9.5} stil={{ left: 900, top: 340, fontSize: 160 }} />
        <Kelimeler metin="yaşında bir sultan" bas={8.5} boyut={60} kalinlik={600} stil={{ left: 1110, top: 400 }} />
        <Kelimeler metin="1451: tahta ikinci kez çıktı" bas={12.5} boyut={52} kalinlik={500} renk={R.soluk} stil={{ left: 900, top: 560 }} />
        <svg width={260} height={340} viewBox="0 0 260 340" style={{ position: "absolute", left: 900, top: 680, opacity: ac(f, 18, 18.5) }}>
          {Array.from({ length: kuleBloklari }, (_, i) => {
            const s = ac(f, 18.5 + i * 0.35, 18.9 + i * 0.35);
            return <rect key={i} x={40} y={300 - (i + 1) * 30} width={180} height={28} fill={i % 2 ? R.kara : R.kara2} opacity={s} transform={`translate(0 ${(1 - s) * -60})`} />;
          })}
          {[40, 90, 140, 190].map((x, i) => (
            <rect key={x} x={x} y={10} width={30} height={22} fill={R.kara} opacity={ac(f, 22 + i * 0.15, 22.4 + i * 0.15)} />
          ))}
        </svg>
        <Kelimeler metin="1452: Rumelihisarı" bas={20} boyut={64} kalinlik={800} renk={R.altin} stil={{ left: 1200, top: 720 }} />
        <Kelimeler metin="Boğaz'ı kontrol için yaklaşık 4,5 ayda yükseldi" bas={23} boyut={40} kalinlik={500} stil={{ left: 1200, top: 820, width: 640 }} />
      </Icerik>
      <BolumKarti no="02" ad="Sultan" />
    </AbsoluteFill>
  );
};

const Surlar: React.FC = () => {
  const f = useCurrentFrame();
  const hendek = ac(f, 4, 5.5);
  const dis = ac(f, 7.5, 9);
  const ic = ac(f, 11, 12.5);
  const zincirBas = 18;
  return (
    <AbsoluteFill>
      <Fon />
      <Icerik>
        <svg width={1920} height={1080} style={{ position: "absolute", top: 90 }}>
          <rect x={0} y={560} width={1920} height={6} fill={R.soluk} opacity={0.5} />
          {/* hendek */}
          <path d={`M220,566 L260,${566 + 120 * hendek} L520,${566 + 120 * hendek} L560,566 Z`} fill={R.deniz} stroke={R.turkuaz} strokeWidth={4} />
          {/* dış sur */}
          <rect x={640} y={566 - 170 * dis} width={110} height={170 * dis} fill={R.kara2} />
          {[640, 685, 730].map((x) => (
            <rect key={x} x={x} y={566 - 170 * dis - 22} width={20} height={22 * dis} fill={R.kara2} />
          ))}
          {/* iç sur ve kule */}
          <rect x={900} y={566 - 260 * ic} width={150} height={260 * ic} fill={R.kara} />
          <rect x={1060} y={566 - 340 * ic} width={140} height={340 * ic} fill={R.kara} stroke={R.altin} strokeWidth={4 * ic} />
          {[1060, 1105, 1150].map((x) => (
            <rect key={x} x={x} y={566 - 340 * ic - 26} width={30} height={26 * ic} fill={R.kara} />
          ))}
          <rect x={1210} y={566 - 260 * ic} width={260} height={260 * ic} fill={R.kara} />
        </svg>
        <Kelimeler metin="Hendek" bas={5} boyut={44} renk={R.turkuaz} stil={{ left: 300, top: 810 }} />
        <Kelimeler metin="Dış sur" bas={8.5} boyut={44} renk={R.kara2} stil={{ left: 620, top: 690 }} />
        <Kelimeler metin="İç sur ve kuleler" bas={12} boyut={44} renk={R.kara} stil={{ left: 960, top: 690 }} />
        <Kelimeler metin="Kara tarafında üç katlı bir savunma" bas={14.5} boyut={58} kalinlik={800} renk={R.altin} stil={{ left: 220, top: 150 }} />
        <svg width={1920} height={260} style={{ position: "absolute", top: 800, opacity: ac(f, zincirBas, zincirBas + 0.5) }}>
          <rect x={0} y={60} width={1920} height={200} fill={R.deniz} />
          {Array.from({ length: 30 }, (_, i) => {
            const o = ac(f, zincirBas + 0.5 + i * 0.12, zincirBas + 0.8 + i * 0.12);
            return (
              <ellipse key={i} cx={120 + i * 58} cy={70 + Math.sin(i / 3 + f / 20) * 6} rx={30} ry={16} fill="none" stroke={R.soluk} strokeWidth={8} opacity={o} />
            );
          })}
        </svg>
        <Kelimeler metin="Haliç'in ağzına demir zincir gerildi" bas={20} boyut={46} kalinlik={700} stil={{ left: 120, top: 950 }} />
        <Kelimeler metin="Deniz yolu kapandı." bas={24} boyut={50} kalinlik={900} renk={R.kirmizi} stil={{ left: 1300, top: 950 }} />
      </Icerik>
      <BolumKarti no="03" ad="Surlar" />
    </AbsoluteFill>
  );
};

const Gucler: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const nokta = (i: number, bas: number, renk: string, x0: number, sutun: number) => {
    const s = spring({ frame: f - sn(bas) - i * 1.2, fps, config: { damping: 14 } });
    return <circle key={i} cx={x0 + (i % sutun) * 46} cy={330 + Math.floor(i / sutun) * 46} r={17 * s} fill={renk} />;
  };
  return (
    <AbsoluteFill>
      <Fon renk={R.gece2} />
      <Icerik>
        <Kelimeler metin="Osmanlı ordusu" bas={4} boyut={56} renk={R.kirmizi} stil={{ left: 140, top: 200 }} />
        <svg width={1920} height={1080} style={{ position: "absolute" }}>
          {Array.from({ length: 80 }, (_, i) => nokta(i, 5, R.kirmizi, 160, 16))}
          {Array.from({ length: 8 }, (_, i) => nokta(i, 12, R.altin, 1300, 4))}
        </svg>
        <Sayac a={0} b={80000} bas={5} bit={9} ek=" ~" stil={{ left: 140, top: 600, fontSize: 120, color: R.kirmizi }} />
        <Kelimeler metin="Şehrin savunucuları" bas={11} boyut={56} renk={R.altin} stil={{ left: 1280, top: 200 }} />
        <Sayac a={0} b={8000} bas={12} bit={14} ek=" ~" stil={{ left: 1280, top: 600, fontSize: 120 }} />
        <Kelimeler metin="her nokta ≈ 1.000 kişi" bas={15} boyut={32} kalinlik={500} renk={R.soluk} stil={{ left: 140, top: 760 }} />
        <Kelimeler metin="≈ 10 : 1" bas={18} boyut={150} kalinlik={900} hizala="center" stil={{ width: 1920, top: 780 }} />
        <Kelimeler
          metin="Rakamlar tahminîdir, kaynaklara göre değişir."
          bas={22}
          boyut={30}
          kalinlik={500}
          renk={R.soluk}
          hizala="center"
          stil={{ width: 1920, top: 990 }}
        />
      </Icerik>
      <BolumKarti no="04" ad="Güçler" />
    </AbsoluteFill>
  );
};

const Toplar: React.FC = () => {
  const f = useCurrentFrame();
  const atislar = [6, 11, 16, 21, 26];
  const darbe = atislar.filter((t) => f >= sn(t + 1.2)).length;
  return (
    <AbsoluteFill>
      <Fon />
      <Icerik>
        <svg width={1920} height={1080} style={{ position: "absolute" }}>
          <rect x={0} y={860} width={1920} height={220} fill={R.gece2} />
          {/* top */}
          <g transform={`translate(${260 - atislar.reduce((a, t) => a + Math.max(0, 1 - Math.abs(f - sn(t)) / 6) * 20, 0)} 0)`}>
            <rect x={180} y={720} width={340} height={90} rx={36} fill={R.altin} transform="rotate(-12 350 765)" />
            <circle cx={260} cy={830} r={46} fill={R.kara2} stroke={R.gece} strokeWidth={8} />
            <circle cx={420} cy={830} r={46} fill={R.kara2} stroke={R.gece} strokeWidth={8} />
          </g>
          {/* sur: her darbede bir parça kopar */}
          <rect x={1420} y={460} width={300} height={400} fill={R.kara} />
          {[1420, 1480, 1540, 1600, 1660].map((x, i) => (
            <rect key={x} x={x} y={430} width={40} height={30} fill={R.kara} opacity={i < darbe ? 0 : 1} />
          ))}
          {Array.from({ length: darbe }, (_, i) => (
            <path key={i} d={`M${1430 + i * 8},${520 + i * 60} l40,30 l-20,40 l50,25`} stroke={R.gece} strokeWidth={6} fill="none" />
          ))}
          {atislar.map((t) => {
            const p = interpolate(f, [sn(t), sn(t + 1.2)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
            const parla = Math.max(0, 1 - Math.abs(f - sn(t)) / 5);
            const toz = interpolate(f, [sn(t + 1.2), sn(t + 2.4)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
            const x = 620 + (1420 - 620) * p;
            const y = 650 - Math.sin(p * Math.PI) * 300 + p * -60;
            return (
              <g key={t}>
                <circle cx={640} cy={665} r={70 * parla} fill={R.altin} opacity={parla} />
                {p > 0 && p < 1 && <circle cx={x} cy={y} r={22} fill={R.krem} />}
                {toz > 0 && toz < 1 && <circle cx={1430} cy={600} r={40 + toz * 140} fill={R.kara2} opacity={0.7 * (1 - toz)} />}
              </g>
            );
          })}
        </svg>
        <Kelimeler metin="Macar usta Urban'ın döktüğü dev toplar" bas={4} boyut={58} kalinlik={800} stil={{ left: 140, top: 160, width: 1100 }} />
        <Kelimeler metin="Yüzlerce kiloluk taş gülleler" bas={11} boyut={48} kalinlik={600} renk={R.altin} stil={{ left: 140, top: 330 }} />
        <Kelimeler metin="Surlar haftalarca dövüldü." bas={18} boyut={48} kalinlik={600} renk={R.kirmizi} stil={{ left: 140, top: 420 }} />
      </Icerik>
      <BolumKarti no="05" ad="Toplar" />
    </AbsoluteFill>
  );
};

const Gemiler: React.FC = () => {
  const f = useCurrentFrame();
  const gemiSayisi = 14;
  return (
    <AbsoluteFill>
      <Fon />
      <Icerik>
        <Harita ciz={ac(f, 3, 4.5)}>
          <line x1={1395} y1={628} x2={1430} y2={560} stroke={R.soluk} strokeWidth={8} strokeDasharray="10 6" />
          <HaritaEtiketi x={1500} y={640} metin="ZİNCİR" bas={5} boyut={24} />
          <HaritaEtiketi x={1250} y={160} metin="GALATA" bas={6} />
          <polyline
            points={GEMI_YOLU.map((p) => p.join(",")).join(" ")}
            fill="none"
            stroke={R.kirmizi}
            strokeWidth={6}
            strokeDasharray="18 12"
            strokeDashoffset={-f}
            opacity={ac(f, 9, 10)}
          />
          {Array.from({ length: gemiSayisi }, (_, i) => {
            const t = interpolate(f, [sn(11 + i * 0.9), sn(19 + i * 0.9)], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.inOut(Easing.quad),
            });
            if (t === 0) return null;
            const [x, y] = yolNoktasi(GEMI_YOLU, t);
            const varis = t >= 1;
            const sx = varis ? 900 - (i % 5) * 60 + 40 : x;
            const sy = varis ? 345 + Math.floor(i / 5) * 10 - 20 + (i % 5) * -14 : y;
            return (
              <g key={i} transform={`translate(${sx} ${sy})`}>
                <path d="M-18,4 L18,4 L12,14 L-12,14 Z" fill={R.kirmizi} />
                <path d="M0,-20 L0,3 L14,3 Z" fill={R.krem} />
              </g>
            );
          })}
        </Harita>
        <div style={{ position: "absolute", left: 60, bottom: 50, width: 760, padding: "30px 36px", background: R.gece, borderLeft: `10px solid ${R.kirmizi}`, opacity: ac(f, 4, 5) }}>
          <Kelimeler metin="22 Nisan 1453 gecesi" bas={4.5} boyut={52} kalinlik={900} renk={R.altin} stil={{ position: "relative" }} />
          <Kelimeler metin="Gemiler yağlanmış kızaklarla Galata sırtlarından aşırıldı" bas={9} boyut={36} kalinlik={600} stil={{ position: "relative", marginTop: 14 }} />
          <Kelimeler metin="Zincire dokunmadan Haliç'e inildi." bas={25} boyut={36} kalinlik={800} renk={R.kirmizi} stil={{ position: "relative", marginTop: 14 }} />
        </div>
        <Sayac a={0} b={70} bas={12} bit={30} ek=" gemi ~" stil={{ right: 80, top: 860, fontSize: 90 }} />
      </Icerik>
      <BolumKarti no="06" ad="Karadan Gemiler" />
    </AbsoluteFill>
  );
};

const Takvim: React.FC = () => {
  const f = useCurrentFrame();
  const X0 = 200;
  const X1 = 1720;
  const gunX = (g: number) => X0 + ((g - 1) / 53) * (X1 - X0);
  const ilerle = ac(f, 5, 26);
  const gun = Math.max(1, Math.round(1 + ilerle * 52));
  const olaylar = [
    { g: 1, tarih: "6 Nisan", metin: "Kuşatma başlar", ust: true },
    { g: 15, tarih: "20 Nisan", metin: "Yardım gemileri Haliç'e girer", ust: false },
    { g: 17, tarih: "22 Nisan", metin: "Gemiler karadan Haliç'e", ust: true },
    { g: 54, tarih: "29 Mayıs", metin: "Son saldırı", ust: false },
  ];
  return (
    <AbsoluteFill>
      <Fon renk={R.gece2} />
      <Icerik>
        <svg width={1920} height={1080} style={{ position: "absolute" }}>
          <line x1={X0} y1={560} x2={X1} y2={560} stroke={R.soluk} strokeWidth={6} opacity={0.4} />
          <line x1={X0} y1={560} x2={X0 + (X1 - X0) * ilerle} y2={560} stroke={R.altin} strokeWidth={10} />
          <circle cx={X0 + (X1 - X0) * ilerle} cy={560} r={20} fill={R.kirmizi} />
          {olaylar.map((o) => {
            const x = gunX(Math.min(o.g, 54) * (53 / 54) + 1 * (1 / 54));
            const gor = ac(f, 5 + ((o.g - 1) / 53) * 21, 5.6 + ((o.g - 1) / 53) * 21);
            const y2 = o.ust ? 420 : 700;
            return (
              <g key={o.tarih} opacity={gor}>
                <line x1={x} y1={560} x2={x} y2={y2} stroke={R.krem} strokeWidth={3} />
                <circle cx={x} cy={560} r={12} fill={R.krem} />
                <text x={x} y={o.ust ? y2 - 60 : y2 + 50} fill={R.altin} fontFamily={FONT} fontWeight={900} fontSize={40} textAnchor="middle">
                  {o.tarih}
                </text>
                <text x={x} y={o.ust ? y2 - 15 : y2 + 95} fill={R.krem} fontFamily={FONT} fontWeight={600} fontSize={30} textAnchor="middle">
                  {o.metin}
                </text>
              </g>
            );
          })}
        </svg>
        <div style={{ position: "absolute", right: 120, top: 150, fontFamily: FONT, textAlign: "right" }}>
          <div style={{ fontSize: 40, fontWeight: 600, color: R.soluk }}>GÜN</div>
          <div style={{ fontSize: 170, fontWeight: 900, color: R.altin, lineHeight: 1 }}>{gun}</div>
        </div>
        <Kelimeler metin="Kuşatma takvimi, 1453" bas={4} boyut={56} kalinlik={800} stil={{ left: 140, top: 180 }} />
      </Icerik>
      <BolumKarti no="07" ad="53 Gün" />
    </AbsoluteFill>
  );
};

const SonSaldiri: React.FC = () => {
  const f = useCurrentFrame();
  const safak = ac(f, 3, 16);
  const gok = `linear-gradient(180deg, ${safak < 0.5 ? R.gece : "#3a2d55"} 0%, ${interpolate(safak, [0, 1], [0, 1]) > 0.5 ? "#e07a4f" : R.gece2} 75%, ${R.altin} 100%)`;
  const dalgalar = [5, 8.5, 12];
  const bayrak = ac(f, 14.5, 16.5);
  return (
    <AbsoluteFill style={{ background: gok }}>
      <AbsoluteFill style={{ background: R.gece, opacity: 1 - safak * 0.75 }} />
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <circle cx={1500} cy={900 - safak * 260} r={120} fill={R.altin} opacity={safak} />
        <rect x={0} y={880} width={1920} height={200} fill="#0a121f" />
        <path d="M900,880 V560 H980 V520 H1020 V560 H1100 V480 H1260 V560 H1360 V520 H1400 V560 H1920 V880 Z" fill="#0a121f" />
        {dalgalar.map((t, d) =>
          Array.from({ length: 12 }, (_, i) => {
            const p = interpolate(f, [sn(t) + i * 3, sn(t + 2) + i * 3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
            if (p === 0 || p === 1) return null;
            const x = 80 + p * 900;
            const y = 840 - d * 25 - i * 22 - Math.sin(p * Math.PI) * 260;
            return <line key={`${d}-${i}`} x1={x} y1={y} x2={x - 30} y2={y + 10 - Math.cos(p * Math.PI) * 18} stroke={R.krem} strokeWidth={4} />;
          }),
        )}
        <line x1={1180} y1={480} x2={1180} y2={480 - 200 * bayrak} stroke={R.krem} strokeWidth={8} />
        <rect x={1184} y={480 - 200 * bayrak} width={130 * bayrak} height={80 * bayrak} fill={R.kirmizi} transform={`skewY(${Math.sin(f / 6) * 3})`} />
      </svg>
      <Icerik>
        <Kelimeler metin="Şafak vakti, üç dalga hâlinde saldırı" bas={4.5} boyut={56} kalinlik={800} stil={{ left: 140, top: 160 }} />
        <Kelimeler metin="Şehir düştü." bas={17} boyut={120} kalinlik={900} renk={R.krem} stil={{ left: 140, top: 270 }} />
      </Icerik>
      <BolumKarti no="08" ad="29 Mayıs" />
    </AbsoluteFill>
  );
};

const Sonrasi: React.FC = () => {
  const f = useCurrentFrame();
  const ayir = ac(f, 11, 13);
  return (
    <AbsoluteFill>
      <Fon />
      <Icerik>
        <Kelimeler metin="İstanbul, Osmanlı'nın başkenti oldu" bas={3.8} boyut={58} kalinlik={800} stil={{ left: 140, top: 200 }} />
        <Kelimeler metin="II. Mehmed artık “Fatih”" bas={7} boyut={58} kalinlik={800} renk={R.altin} stil={{ left: 140, top: 300 }} />
        <svg width={1920} height={400} style={{ position: "absolute", top: 520 }}>
          <rect x={140} y={120} width={(960 - 140) * ayir} height={120} fill={R.soluk} opacity={0.5} />
          <rect x={960} y={120} width={(1780 - 960) * ayir} height={120} fill={R.turkuaz} />
          <text x={180} y={198} fill={R.krem} fontFamily={FONT} fontWeight={800} fontSize={44} opacity={ayir}>ORTA ÇAĞ</text>
          <text x={1000} y={198} fill={R.krem} fontFamily={FONT} fontWeight={800} fontSize={44} opacity={ayir}>YENİ ÇAĞ</text>
          <line x1={960} y1={60} x2={960} y2={300} stroke={R.kirmizi} strokeWidth={10} opacity={ayir} />
          <text x={960} y={40} fill={R.kirmizi} fontFamily={FONT} fontWeight={900} fontSize={54} textAnchor="middle" opacity={ayir}>1453</text>
        </svg>
        <Kelimeler
          metin="Pek çok tarihçiye göre bir çağ burada kapandı."
          bas={13.5}
          boyut={40}
          kalinlik={500}
          renk={R.soluk}
          hizala="center"
          stil={{ width: 1920, top: 870 }}
        />
      </Icerik>
      <BolumKarti no="09" ad="Yeni Çağ" />
    </AbsoluteFill>
  );
};

const Kapanis: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Fon />
      <Kelimeler metin="53 gün." bas={0.5} boyut={120} kalinlik={900} hizala="center" stil={{ width: 1920, top: 240 }} />
      <Kelimeler metin="Bir şehir." bas={2} boyut={120} kalinlik={900} renk={R.altin} hizala="center" stil={{ width: 1920, top: 390 }} />
      <Kelimeler metin="Yeni bir çağ." bas={3.5} boyut={120} kalinlik={900} renk={R.kirmizi} hizala="center" stil={{ width: 1920, top: 540 }} />
      <div
        style={{
          position: "absolute",
          width: 1920,
          top: 820,
          textAlign: "center",
          fontFamily: FONT,
          fontWeight: 800,
          fontSize: 40,
          letterSpacing: 16,
          color: R.soluk,
          opacity: ac(f, 6.5, 7.5),
        }}
      >
        SKONSTART
      </div>
    </AbsoluteFill>
  );
};

const SAHNELER = [Acilis, Sehir, Sultan, Surlar, Gucler, Toplar, Gemiler, Takvim, SonSaldiri, Sonrasi, Kapanis];

export const Fetih1453: React.FC = () => (
  <AbsoluteFill style={{ background: R.gece }}>
    {SAHNELER.map((Sahne, i) => (
      <Sequence key={i} from={sn(BOLUMLER[i].bas)} durationInFrames={sn(BOLUMLER[i].sure)}>
        <Gecis sure={BOLUMLER[i].sure}>
          <Sahne />
        </Gecis>
      </Sequence>
    ))}
  </AbsoluteFill>
);
