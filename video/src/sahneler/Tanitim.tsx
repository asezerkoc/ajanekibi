import React from "react";
import {
	AbsoluteFill,
	interpolate,
	Sequence,
	spring,
	useCurrentFrame,
	useVideoConfig,
} from "remotion";
import { PaperCut, type PaperLayer } from "../effects/PaperCut";
import { DoodleBoil } from "../effects/DoodleBoil";
import { Checklist } from "../effects/Checklist";
import { Orbit } from "../effects/Orbit";
import { KineticCaptions } from "../effects/KineticCaptions";
import { WhipPan } from "../effects/WhipPan";
import { ZoomThroughCut } from "../effects/ZoomThroughCut";

// SKONSTART's look: soft, warm, hand-painted hills under a sunny sky
const tepeler: PaperLayer[] = [
	{ color: "#d8e8bf", d: "M0 600 Q480 420 960 560 T1920 520 V1080 H0Z" },
	{ color: "#a9cf8f", d: "M0 720 Q400 560 900 700 T1920 660 V1080 H0Z" },
	{ color: "#74b07b", d: "M0 820 Q520 700 1000 820 T1920 780 V1080 H0Z" },
	{ color: "#467f5e", d: "M0 940 Q600 840 1100 940 T1920 900 V1080 H0Z" },
];

const ekip = ["Araştırmacı", "Metin yazarı", "Editör", "Grafiker", "Kalite kontrol"];

const Baslik: React.FC = () => {
	const frame = useCurrentFrame();
	const { fps } = useVideoConfig();
	const s = spring({ frame: frame - 25, fps, config: { damping: 200 } });
	return (
		<AbsoluteFill style={{ alignItems: "center", paddingTop: 170, fontFamily: "Georgia, serif" }}>
			<div
				style={{
					fontSize: 190,
					fontWeight: 700,
					letterSpacing: 8,
					color: "#3d405b",
					opacity: s,
					transform: `translateY(${interpolate(s, [0, 1], [40, 0])}px)`,
				}}
			>
				SKONSTART
			</div>
			<div style={{ fontSize: 54, color: "#6b5b4b", opacity: s, marginTop: 10 }}>
				yapay zekâ ajansı
			</div>
		</AbsoluteFill>
	);
};

const Sahne1: React.FC = () => (
	<PaperCut layers={tepeler}>
		<DoodleBoil>
			<circle cx={1730} cy={150} r={70} fill="none" stroke="#f2a65a" strokeWidth={12} pathLength={1} />
		</DoodleBoil>
		<Baslik />
	</PaperCut>
);

const Sahne2: React.FC = () => (
	<AbsoluteFill style={{ background: "linear-gradient(160deg, #2f5d73, #5f8f78)" }}>
		<Checklist title="SKONSTART ekibi" items={ekip} startAt={8} every={14} accent="#f2a65a" />
	</AbsoluteFill>
);

const Cip: React.FC<{ yazi: string; renk: string; buyuk?: boolean }> = ({ yazi, renk, buyuk }) => (
	<div
		style={{
			padding: buyuk ? "40px 56px" : "22px 34px",
			borderRadius: 999,
			background: renk,
			color: "white",
			fontFamily: "Inter, Helvetica, Arial, sans-serif",
			fontSize: buyuk ? 64 : 38,
			fontWeight: 800,
			whiteSpace: "nowrap",
			boxShadow: "0 12px 30px rgba(0,0,0,0.25)",
		}}
	>
		{yazi}
	</div>
);

const Sahne3: React.FC = () => (
	<AbsoluteFill style={{ background: "radial-gradient(circle at 50% 45%, #3b5b7a, #1c2738)" }}>
		<Orbit
			center={<Cip yazi="SEN" renk="#f2a65a" buyuk />}
			items={ekip.map((e, i) => (
				<Cip key={e} yazi={e} renk={["#467f5e", "#7a6fb0", "#c0607a", "#3f8fb0", "#b08a3f"][i]} />
			))}
			radiusX={600}
			radiusY={200}
			speed={0.12}
		/>
	</AbsoluteFill>
);

const kelimeler = "İşi sen ver. Ekip hemen çalışsın. Sen sadece onayla.".split(" ").map((text, i) => ({
	text,
	startMs: 300 + i * 380,
	endMs: 300 + i * 380 + 360,
}));

const Sahne4: React.FC = () => (
	<PaperCut layers={tepeler} stagger={3}>
		<KineticCaptions words={kelimeler} perPage={3} highlight="#f2a65a" fontSize={110} />
	</PaperCut>
);

/** SKONSTART tanıtım videosu: 1920x1080, 30 fps, 18 saniye. */
export const Tanitim: React.FC = () => (
	<WhipPan
		at={150}
		duration={12}
		from={<Sahne1 />}
		to={
			<Sequence from={144}>
				<ZoomThroughCut
					cutAt={276}
					duration={10}
					from={
						<WhipPan
							at={140}
							duration={12}
							direction="right"
							from={<Sahne2 />}
							to={
								<Sequence from={134}>
									<Sahne3 />
								</Sequence>
							}
						/>
					}
					to={<Sahne4 />}
				/>
			</Sequence>
		}
	/>
);
