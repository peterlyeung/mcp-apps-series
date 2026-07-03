import React from "react";
import { theme } from "../theme";
import { Heading, Small, SlideShell } from "./SlideShell";

export const PartnersSlide: React.FC<{
  heading: string;
  names: string[];
  small?: string;
}> = ({ heading, names, small }) => {
  return (
    <SlideShell>
      <Heading>{heading}</Heading>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: 12,
          justifyContent: "center",
          maxWidth: 1040,
          margin: "20px auto 0",
        }}
      >
        {names.map((name, i) => (
          <span
            key={i}
            style={{
              border: `1px solid ${theme.cardBorder}`,
              borderRadius: 24,
              padding: "10px 22px",
              fontSize: 22,
              background: theme.cardBg,
            }}
          >
            {name}
          </span>
        ))}
      </div>
      {small && (
        <div style={{ textAlign: "center" }}>
          <Small>{small}</Small>
        </div>
      )}
    </SlideShell>
  );
};
