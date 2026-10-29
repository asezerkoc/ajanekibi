import React from "react";
import { Composition } from "remotion";
import { Tanitim } from "./sahneler/Tanitim";
import { CengizHan, FPS, TOPLAM_KARE } from "./sahneler/CengizHan";
import { Kapak, KapakGunduz, KapakKayipMezar, KapakPortre, KapakSavas } from "./sahneler/Kapak";
import { KM_FPS, KM_KARE, KayipMezar } from "./sahneler/KayipMezar";
import { T1_KARE, Timur1 } from "./sahneler/Timur1";
import { T2_KARE, Timur2 } from "./sahneler/Timur2";
import { T3_KARE, Timur3 } from "./sahneler/Timur3";
import { T_FPS } from "./sahneler/TimurSeri";
import { C29_FPS, C29_KARE, Cumhuriyet29 } from "./sahneler/Cumhuriyet29";
import { KAL_KARE, Kalender } from "./sahneler/Kalender";

export const Root: React.FC = () => (
	<>
		<Composition id="Tanitim" component={Tanitim} durationInFrames={540} fps={30} width={1920} height={1080} />
		<Composition
			id="CengizHan"
			component={CengizHan}
			durationInFrames={TOPLAM_KARE}
			fps={FPS}
			width={1080}
			height={1920}
			defaultProps={{ sesler: true }}
		/>
		<Composition id="CengizHanKapak" component={Kapak} durationInFrames={1} fps={30} width={1080} height={1920} />
		<Composition id="CengizHanKapakPortre" component={KapakPortre} durationInFrames={1} fps={30} width={1080} height={1920} />
		<Composition id="CengizHanKapakSavas" component={KapakSavas} durationInFrames={1} fps={30} width={1080} height={1920} />
		<Composition id="KayipMezarKapak" component={KapakKayipMezar} durationInFrames={1} fps={30} width={1080} height={1920} />
		<Composition id="CengizHanKapakGunduz" component={KapakGunduz} durationInFrames={1} fps={30} width={1080} height={1920} />
		<Composition id="KayipMezar" component={KayipMezar} durationInFrames={KM_KARE} fps={KM_FPS} width={1080} height={1920} />
		<Composition id="Timur1" component={Timur1} durationInFrames={T1_KARE} fps={T_FPS} width={1080} height={1920} />
		<Composition id="Timur2" component={Timur2} durationInFrames={T2_KARE} fps={T_FPS} width={1080} height={1920} />
		<Composition id="Timur3" component={Timur3} durationInFrames={T3_KARE} fps={T_FPS} width={1080} height={1920} />
		<Composition id="Cumhuriyet29" component={Cumhuriyet29} durationInFrames={C29_KARE} fps={C29_FPS} width={1080} height={1920} />
		<Composition id="Kalender" component={Kalender} durationInFrames={KAL_KARE} fps={T_FPS} width={1080} height={1920} />
	</>
);
