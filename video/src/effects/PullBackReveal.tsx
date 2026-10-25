import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  useCurrentFrame,
} from "remotion";

export type PullBackRevealProps = {
  children: React.ReactNode;
  /** Detail to start on, % of the frame. */
  focusX?: number;
  focusY?: number;
  /** Starting zoom. */
  startScale?: number;
  /** Frame the pull-back starts and how long it takes. */
  startAt?: number;
  duration?: number;
  /** Optional overlay that fades in once the full picture is revealed. */
  overlay?: React.ReactNode;
};

/** Starts tight on a detail, then pulls back to reveal the whole scene. */
export const PullBackReveal: React.FC<PullBackRevealProps> = ({
  children,
  focusX = 50,
  focusY = 50,
  startScale = 4,
  startAt = 15,
  duration = 60,
  overlay,
}) => {
  const frame = useCurrentFrame();
  const clamp = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
  const p = interpolate(frame, [startAt, startAt + duration], [0, 1], {
    ...clamp,
    easing: Easing.inOut(Easing.quad),
  });
  // Interpolate in log space so the zoom feels constant speed.
  const scale = Math.exp(interpolate(p, [0, 1], [Math.log(startScale), 0]));
  // A gentle rotation settle sells the camera move.
  const rotate = interpolate(p, [0, 1], [-3, 0]);
  const overlayIn = interpolate(frame, [startAt + duration - 10, startAt + duration + 10], [0, 1], clamp);

  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "black" }}>
      <AbsoluteFill
        style={{
          transform: `scale(${scale}) rotate(${rotate}deg)`,
          transformOrigin: `${focusX}% ${focusY}%`,
        }}
      >
        {children}
      </AbsoluteFill>
      {overlay ? <AbsoluteFill style={{ opacity: overlayIn }}>{overlay}</AbsoluteFill> : null}
    </AbsoluteFill>
  );
};
