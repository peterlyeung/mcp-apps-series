import React from "react";
import { theme } from "../theme";
import { Heading, Small, SlideShell } from "./SlideShell";

export const RoadmapSlide: React.FC<{
  heading: string;
  items: { num: string; text: string }[];
  small?: string;
}> = ({ heading, items, small }) => {
  return (
    <SlideShell>
      <Heading>{heading}</Heading>
      <div style={{ maxWidth: 1040, margin: "0 auto" }}>
        {items.map((item, i) => (
          <div
            key={i}
            style={{
              padding: "14px 20px",
              marginBottom: 12,
              borderLeft: `4px solid ${theme.accent}`,
              background: "rgba(217, 119, 87, 0.08)",
              fontSize: 24,
              display: "flex",
            }}
          >
            <span
              style={{
                color: theme.accent,
                fontWeight: 800,
                marginRight: 16,
              }}
            >
              {item.num}
            </span>
            {item.text}
          </div>
        ))}
        {small && <Small>{small}</Small>}
      </div>
    </SlideShell>
  );
};
