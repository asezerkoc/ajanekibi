import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  Sequence,
  useCurrentFrame,
} from "remotion";

export type ZoomThroughCutProps = {
  from: React.ReactNode;
  to: React.ReactNode;
  /** Frame of the cut. */
  cutAt: number;
  /** Frames on each side of the cut. */
  duration?: number;
  /** Point to zoom into on the outgoing scene, % of the frame. */
  originX?: number;
  originY?: number;
};

/**
 * Transition: scene A rushes toward the camera into a point, hard cut,
 * scene B arrives from behind the camera and settles.
 */
export const ZoomThroughCut: React.FC<ZoomThroughCutProps> = ({
  from,
  to,
  cutAt,
  duration = 10,
  originX = 50,
  originY = 50,
}) => {
  const frame = useCurrentFrame();
  const clamp = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };

  const outP = interpolate(frame, [cutAt - duration, cutAt], [0, 1], {
    ...clamp,
    easing: Easing.in(Easing.exp),
  });
  const inP = interpolate(frame, [cutAt, cutAt + duration * 1.5], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.exp),
  });

  return (
    <AbsoluteFill style={{ background: "black", overflow: "hidden" }}>
      <Sequence durationInFrames={cutAt} layout="none">
        <AbsoluteFill
          style={{
            transform: `scale(${interpolate(outP, [0, 1], [1, 6])})`,
            transformOrigin: `${originX}% ${originY}%`,
            filter: `blur(${outP * 20}px)`,
            opacity: interpolate(outP, [0.8, 1], [1, 0.6], clamp),
          }}
        >
          {from}
        </AbsoluteFill>
      </Sequence>
      <Sequence from={cutAt} layout="none">
        <AbsoluteFill
          style={{
            transform: `scale(${interpolate(inP, [0, 1], [2.5, 1])})`,
            filter: `blur(${(1 - inP) * 20}px)`,
          }}
        >
          {to}
        </AbsoluteFill>
      </Sequence>
      {/* White flash on the cut */}
      <AbsoluteFill
        style={{
          background: "white",
          opacity: interpolate(frame, [cutAt - 2, cutAt, cutAt + 4], [0, 0.5, 0], clamp),
        }}
      />
    </AbsoluteFill>
  );
};
