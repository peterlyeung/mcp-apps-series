import React from "react";
import { theme } from "../theme";
import { Heading, SlideShell } from "./SlideShell";

export const StepsSlide: React.FC<{ heading: string; items: string[] }> = ({
  heading,
  items,
}) => {
  return (
    <SlideShell>
      <Heading>{heading}</Heading>
      <div style={{ maxWidth: 1040, margin: "0 auto" }}>
        {items.map((item, i) => {
          const boldMatch = item.match(/^([^—]+—)(.*)$/);
          return (
            <div
              key={i}
              style={{
                display: "flex",
                alignItems: "flex-start",
                marginBottom: 20,
              }}
            >
              <div
                style={{
                  width: 42,
                  height: 42,
                  borderRadius: "50%",
                  background: theme.accent,
                  color: "#1a1a1a",
                  fontWeight: 800,
                  fontSize: 22,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexShrink: 0,
                  marginRight: 20,
                }}
              >
                {i + 1}
              </div>
              <div style={{ fontSize: 25, lineHeight: 1.4, paddingTop: 4 }}>
                {boldMatch ? (
                  <>
                    <strong>{boldMatch[1]}</strong>
                    {boldMatch[2]}
                  </>
                ) : (
                  item
                )}
              </div>
            </div>
          );
        })}
      </div>
    </SlideShell>
  );
};
