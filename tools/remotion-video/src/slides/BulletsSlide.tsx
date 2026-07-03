import React from "react";
import { Heading, SlideShell } from "./SlideShell";

export const BulletsSlide: React.FC<{
  heading: string;
  items: string[];
}> = ({ heading, items }) => {
  return (
    <SlideShell>
      <Heading>{heading}</Heading>
      <ul
        style={{
          fontSize: 26,
          lineHeight: 1.5,
          maxWidth: 1040,
          margin: "0 auto",
          paddingLeft: 32,
        }}
      >
        {items.map((item, i) => {
          const boldMatch = item.match(/^([^—]+—)(.*)$/);
          return (
            <li key={i} style={{ marginBottom: 16 }}>
              {boldMatch ? (
                <>
                  <strong>{boldMatch[1]}</strong>
                  {boldMatch[2]}
                </>
              ) : (
                item
              )}
            </li>
          );
        })}
      </ul>
    </SlideShell>
  );
};
