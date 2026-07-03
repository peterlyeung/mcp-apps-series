import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { theme } from "../theme";

export const TitleSlide: React.FC<{
  title: string;
  subtitle?: string;
  eyebrow?: string;
}> = ({ title, subtitle, eyebrow }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.bg,
        justifyContent: "center",
        alignItems: "center",
        fontFamily: theme.font,
        opacity,
      }}
    >
      <div
        style={{
          color: theme.accent,
          fontSize: 68,
          fontWeight: 800,
          textAlign: "center",
          textTransform: "uppercase",
          maxWidth: 1050,
          lineHeight: 1.1,
        }}
      >
        {title}
      </div>
      {subtitle && (
        <div
          style={{
            color: theme.text,
            fontSize: 30,
            marginTop: 22,
            textAlign: "center",
            maxWidth: 950,
          }}
        >
          {subtitle}
        </div>
      )}
      {eyebrow && (
        <div style={{ color: theme.textDim, fontSize: 20, marginTop: 18 }}>
          {eyebrow}
        </div>
      )}
    </AbsoluteFill>
  );
};
