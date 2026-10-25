import React from "react";
import { Composition } from "remotion";
import { Tanitim } from "./sahneler/Tanitim";

export const Root: React.FC = () => (
	<>
		<Composition id="Tanitim" component={Tanitim} durationInFrames={540} fps={30} width={1920} height={1080} />
	</>
);
