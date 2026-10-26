import React from "react";
import { Composition } from "remotion";
import { Tanitim } from "./sahneler/Tanitim";
import { CengizHan } from "./sahneler/CengizHan";

export const Root: React.FC = () => (
	<>
		<Composition id="Tanitim" component={Tanitim} durationInFrames={540} fps={30} width={1920} height={1080} />
		<Composition
			id="CengizHan"
			component={CengizHan}
			durationInFrames={3600}
			fps={60}
			width={1080}
			height={1920}
			defaultProps={{ sesler: false }}
		/>
	</>
);
