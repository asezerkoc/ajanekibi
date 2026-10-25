import React, { useId } from "react";
import { AbsoluteFill } from "remotion";

export type GreenScreenProps = {
  /** Footage shot on green: <OffthreadVideo>, <Video> or <Img>. */
  children: React.ReactNode;
  /** What shows through where the green was. */
  background: React.ReactNode;
  /** Higher = more aggressive key. 2 is a good start. */
  strength?: number;
  /** Pulls green tint off edges and hair. */
  despill?: boolean;
};

/**
 * Chroma key with an SVG filter. Runs on the GPU in Chrome, so it is fast to
 * render and works on any element (video, image, even HTML).
 *
 * alpha = 1 + r + b - strength * g  -> pure green goes to 0, everything else stays opaque.
 */
export const GreenScreen: React.FC<GreenScreenProps> = ({
  children,
  background,
  strength = 2,
  despill = true,
}) => {
  const id = useId().replace(/:/g, "");
  return (
    <AbsoluteFill>
      <svg width="0" height="0" style={{ position: "absolute" }}>
        <filter id={`key-${id}`} colorInterpolationFilters="sRGB">
          {/* Despill: clamp green to the average of red and blue */}
          {despill ? (
            <feColorMatrix
              type="matrix"
              values="1 0 0 0 0
                      0.5 0 0.5 0 0
                      0 0 1 0 0
                      0 0 0 1 0"
              result="despilled"
            />
          ) : null}
          <feColorMatrix
            in="SourceGraphic"
            type="matrix"
            values={`0 0 0 0 0
                     0 0 0 0 0
                     0 0 0 0 0
                     1 ${-strength} 1 0 1`}
            result="mask"
          />
          <feComposite
            in={despill ? "despilled" : "SourceGraphic"}
            in2="mask"
            operator="in"
          />
        </filter>
      </svg>
      <AbsoluteFill>{background}</AbsoluteFill>
      <AbsoluteFill style={{ filter: `url(#key-${id})` }}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};
