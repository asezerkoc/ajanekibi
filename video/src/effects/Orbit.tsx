import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export type OrbitProps = {
  center: React.ReactNode;
  items: React.ReactNode[];
  radiusX?: number;
  radiusY?: number;
  /** Full revolutions per second. */
  speed?: number;
  /** Tilt of the orbit plane in degrees. */
  tilt?: number;
};

export const Orbit: React.FC<OrbitProps> = ({
  center,
  items,
  radiusX = 520,
  radiusY = 160,
  speed = 0.08,
  tilt = -8,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Items fly out from the center at the start.
  const intro = spring({ frame, fps, config: { damping: 200 } });
  const rotation = (frame / fps) * speed * Math.PI * 2;

  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <div style={{ position: "relative", transform: `rotate(${tilt}deg)` }}>
        {items.map((item, i) => {
          const angle = rotation + (i / items.length) * Math.PI * 2;
          // depth: 1 = front, -1 = back
          const depth = Math.sin(angle);
          const x = Math.cos(angle) * radiusX * intro;
          const y = depth * radiusY * intro;
          const scale = interpolate(depth, [-1, 1], [0.6, 1.15]);
          const opacity = interpolate(depth, [-1, 1], [0.45, 1]);
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: 0,
                top: 0,
                transform: `translate(-50%, -50%) translate(${x}px, ${y}px) rotate(${-tilt}deg) scale(${scale})`,
                opacity,
                zIndex: depth > 0 ? 2 : 0,
                filter: `blur(${interpolate(depth, [-1, 0], [3, 0], {
                  extrapolateRight: "clamp",
                })}px)`,
              }}
            >
              {item}
            </div>
          );
        })}
        <div
          style={{
            position: "absolute",
            left: 0,
            top: 0,
            transform: `translate(-50%, -50%) rotate(${-tilt}deg)`,
            zIndex: 1,
          }}
        >
          {center}
        </div>
      </div>
    </AbsoluteFill>
  );
};
