import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { theme } from "../theme";

export const SlideShell: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const translateY = interpolate(frame, [0, 12], [12, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.bg,
        color: theme.text,
        fontFamily: theme.font,
        padding: "70px 90px",
        boxSizing: "border-box",
        opacity,
        transform: `translateY(${translateY}px)`,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

export const Heading: React.FC<{ children: React.ReactNode; tag?: string }> = ({
  children,
  tag,
}) => (
  <div
    style={{
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      marginBottom: 28,
    }}
  >
    <h2
      style={{
        color: theme.accent,
        fontSize: 44,
        fontWeight: 800,
        textAlign: "center",
        margin: 0,
        textTransform: "uppercase",
        letterSpacing: 0.5,
      }}
    >
      {children}
    </h2>
    {tag && (
      <span
        style={{
          marginLeft: 16,
          background: theme.accent,
          color: "#1a1a1a",
          borderRadius: 14,
          padding: "4px 14px",
          fontSize: 18,
          fontWeight: 700,
          textTransform: "uppercase",
        }}
      >
        {tag}
      </span>
    )}
  </div>
);

export const Small: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => (
  <div style={{ fontSize: 20, color: theme.textDim, marginTop: 20 }}>
    {children}
  </div>
);
