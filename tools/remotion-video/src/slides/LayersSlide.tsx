import React from "react";
import { theme } from "../theme";
import { Heading, SlideShell } from "./SlideShell";

export const LayersSlide: React.FC<{
  heading: string;
  items: { title: string; body: string }[];
}> = ({ heading, items }) => {
  return (
    <SlideShell>
      <Heading>{heading}</Heading>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 16,
          alignItems: "center",
        }}
      >
        {items.map((item, i) => (
          <div
            key={i}
            style={{
              width: 780,
              maxWidth: "100%",
              border: `1px solid ${theme.cardBorder}`,
              borderRadius: 8,
              background: theme.cardBg,
              padding: "18px 26px",
              boxSizing: "border-box",
            }}
          >
            <h3 style={{ color: theme.accent, margin: "0 0 6px 0", fontSize: 24 }}>
              {item.title}
            </h3>
            <p style={{ margin: 0, fontSize: 20, color: "#ddd", lineHeight: 1.4 }}>
              {item.body}
            </p>
          </div>
        ))}
      </div>
    </SlideShell>
  );
};
