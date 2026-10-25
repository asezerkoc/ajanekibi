import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  useCurrentFrame,
} from "remotion";

export type SpotlightStop = {
  /** Frame at which the light arrives here. */
  at: number;
  /** Center, in % of the frame. */
  x: number;
  y: number;
  /** Radius in px. */
  r: number;
};

export type SpotlightProps = {
  children: React.ReactNode;
  stops: SpotlightStop[];
  /** Darkness outside the light, 0-1. */
  dim?: number;
  /** Soft edge size in px. */
  feather?: number;
};

/** Darkens everything except a moving circle of light. */
export const Spotlight: React.FC<SpotlightProps> = ({
  children,
  stops,
  dim = 0.78,
  feather = 60,
}) => {
  const frame = useCurrentFrame();
  const at = stops.map((s) => s.at);
  const opts = {
    extrapolateLeft: "clamp" as const,
    extrapolateRight: "clamp" as const,
    easing: Easing.inOut(Easing.cubic),
  };
  const pick = (key: "x" | "y" | "r") =>
    stops.length === 1
      ? stops[0][key]
      : interpolate(frame, at, stops.map((s) => s[key]), opts);
  const x = pick("x");
  const y = pick("y");
  const r = pick("r");
  const fadeIn = interpolate(frame, [0, 12], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill>
      {children}
      <AbsoluteFill
        style={{
          opacity: fadeIn,
          background: `radial-gradient(circle at ${x}% ${y}%, transparent ${r}px, rgba(0,0,0,${dim}) ${r + feather}px)`,
        }}
      />
    </AbsoluteFill>
  );
};
