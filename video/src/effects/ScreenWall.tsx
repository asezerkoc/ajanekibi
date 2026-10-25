import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  random,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export type ScreenWallProps = {
  /** One node per screen; repeated if there are fewer than cols*rows. */
  screens: React.ReactNode[];
  cols?: number;
  rows?: number;
  /** Index of the screen the camera pushes into at the end. -1 = no push. */
  focus?: number;
  /** Frame the push-in starts. */
  focusAt?: number;
};

/** Wall of monitors that flicker on, then the camera pushes into one. */
export const ScreenWall: React.FC<ScreenWallProps> = ({
  screens,
  cols = 4,
  rows = 3,
  focus = 5,
  focusAt = 60,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const gap = 14;
  const tileW = (width - gap * (cols + 1)) / cols;
  const tileH = (height - gap * (rows + 1)) / rows;

  const push = interpolate(frame, [focusAt, focusAt + 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const fc = focus % cols;
  const fr = Math.floor(focus / cols);
  const fx = gap + fc * (tileW + gap) + tileW / 2;
  const fy = gap + fr * (tileH + gap) + tileH / 2;
  const scale = focus < 0 ? 1 : interpolate(push, [0, 1], [1, width / tileW]);
  const tx = focus < 0 ? 0 : (width / 2 - fx) * push;
  const ty = focus < 0 ? 0 : (height / 2 - fy) * push;

  return (
    <AbsoluteFill style={{ background: "#050505", overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          transform: `translate(${tx * scale}px, ${ty * scale}px) scale(${scale})`,
          transformOrigin: `${fx}px ${fy}px`,
        }}
      >
        {Array.from({ length: cols * rows }).map((_, i) => {
          const c = i % cols;
          const r = Math.floor(i / cols);
          const onAt = Math.floor(random(`on-${i}`) * 30);
          const flicker =
            frame < onAt
              ? 0
              : frame < onAt + 4
                ? random(`f-${i}-${frame}`) > 0.5
                  ? 1
                  : 0.2
                : 1;
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: gap + c * (tileW + gap),
                top: gap + r * (tileH + gap),
                width: tileW,
                height: tileH,
                overflow: "hidden",
                borderRadius: 6,
                background: "#111",
                opacity: flicker,
                boxShadow: "inset 0 0 0 2px #222",
              }}
            >
              {screens[i % screens.length]}
              {/* Scanlines */}
              <AbsoluteFill
                style={{
                  background:
                    "repeating-linear-gradient(0deg, rgba(0,0,0,0.18) 0 2px, transparent 2px 4px)",
                  opacity: 1 - push * (i === focus ? 1 : 0),
                }}
              />
            </div>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
