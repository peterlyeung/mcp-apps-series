import React from "react";
import { theme } from "../theme";
import { Heading, Small, SlideShell } from "./SlideShell";

export const TextSlide: React.FC<{
  heading: string;
  paragraphs?: string[];
  bullets?: string[];
  small?: string;
  warn?: string;
}> = ({ heading, paragraphs, bullets, small, warn }) => {
  return (
    <SlideShell>
      <Heading>{heading}</Heading>
      <div style={{ maxWidth: 1040, margin: "0 auto" }}>
        {paragraphs?.map((p, i) => (
          <p key={i} style={{ fontSize: 26, lineHeight: 1.5, margin: "0 0 18px 0" }}>
            {p}
          </p>
        ))}
        {bullets && (
          <ul style={{ fontSize: 24, lineHeight: 1.5, paddingLeft: 30 }}>
            {bullets.map((b, i) => (
              <li key={i} style={{ marginBottom: 12 }}>
                {b}
              </li>
            ))}
          </ul>
        )}
        {warn && (
          <div
            style={{
              borderLeft: `4px solid ${theme.warnBorder}`,
              background: theme.warnBg,
              padding: "14px 20px",
              fontSize: 20,
              marginTop: 20,
            }}
          >
            {warn}
          </div>
        )}
        {small && <Small>{small}</Small>}
      </div>
    </SlideShell>
  );
};
