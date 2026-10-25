import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  useCurrentFrame,
} from "remotion";

export type TriptychProps = {
  panels: [React.ReactNode, React.ReactNode, React.ReactNode];
  /** Frames between each panel reveal. */
  stagger?: number;
  /** Frames each wipe takes. */
  wipe?: number;
  gap?: number;
  background?: string;
};

/** Three panels side by side, each revealed with a vertical wipe. */
export const Triptych: React.FC<TriptychProps> = ({
  panels,
  stagger = 10,
  wipe = 18,
  gap = 16,
  background = "#0b0b0b",
}) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ background, flexDirection: "row", gap, padding: gap }}>
      {panels.map((panel, i) => {
        const p = interpolate(frame, [i * stagger, i * stagger + wipe], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.out(Easing.cubic),
        });
        // Alternate wipe direction: down, up, down
        const clip =
          i % 2 === 0
            ? `inset(0 0 ${(1 - p) * 100}% 0)`
            : `inset(${(1 - p) * 100}% 0 0 0)`;
        const zoom = interpolate(frame, [i * stagger, i * stagger + 90], [1.15, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        return (
          <div
            key={i}
            style={{
              flex: 1,
              position: "relative",
              overflow: "hidden",
              clipPath: clip,
            }}
          >
            <AbsoluteFill style={{ transform: `scale(${zoom})` }}>{panel}</AbsoluteFill>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
