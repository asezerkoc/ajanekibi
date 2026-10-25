import React, { useId } from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export type PaperLayer = {
  color: string;
  /** SVG path in a 1920x1080 viewBox. */
  d: string;
};

export type PaperCutProps = {
  /** Back to front. */
  layers: PaperLayer[];
  /** Frames between each layer sliding in. */
  stagger?: number;
  /** Parallax drift strength, px. */
  drift?: number;
  children?: React.ReactNode;
};

/** Stacked cut-paper layers with soft shadows, grain and parallax. */
export const PaperCut: React.FC<PaperCutProps> = ({
  layers,
  stagger = 6,
  drift = 30,
  children,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const id = useId().replace(/:/g, "");

  return (
    <AbsoluteFill style={{ background: "#f4ecdf" }}>
      <svg viewBox="0 0 1920 1080" width="100%" height="100%">
        <defs>
          <filter id={`grain-${id}`} x="0" y="0" width="100%" height="100%">
            <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3" />
            <feColorMatrix type="saturate" values="0" />
            <feComponentTransfer>
              <feFuncA type="linear" slope="0.08" />
            </feComponentTransfer>
            <feComposite in2="SourceGraphic" operator="in" />
            <feBlend in="SourceGraphic" mode="multiply" />
          </filter>
        </defs>
        {layers.map((layer, i) => {
          const enter = spring({
            frame: frame - i * stagger,
            fps,
            config: { damping: 14, mass: 0.8 },
          });
          // Front layers move more: parallax.
          const depth = (i + 1) / layers.length;
          const parallax = interpolate(frame, [0, durationInFrames], [0, -drift * depth]);
          const y = interpolate(enter, [0, 1], [700, 0]);
          return (
            <g
              key={i}
              transform={`translate(${parallax}, ${y})`}
              style={{
                filter: `drop-shadow(0 ${6 + 10 * depth}px ${8 + 10 * depth}px rgba(60,40,20,0.35))`,
              }}
            >
              <path d={layer.d} fill={layer.color} filter={`url(#grain-${id})`} />
            </g>
          );
        })}
      </svg>
      {children ? <AbsoluteFill>{children}</AbsoluteFill> : null}
    </AbsoluteFill>
  );
};

/** Ready-made hills you can pass as `layers` for a quick scene. */
export const paperHills: PaperLayer[] = [
  { color: "#f2b880", d: "M0 600 Q480 420 960 560 T1920 520 V1080 H0Z" },
  { color: "#e07a5f", d: "M0 720 Q400 560 900 700 T1920 660 V1080 H0Z" },
  { color: "#81b29a", d: "M0 820 Q520 700 1000 820 T1920 780 V1080 H0Z" },
  { color: "#3d405b", d: "M0 940 Q600 840 1100 940 T1920 900 V1080 H0Z" },
];
