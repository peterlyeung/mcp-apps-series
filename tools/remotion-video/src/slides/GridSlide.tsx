import React from "react";
import { theme } from "../theme";
import { Heading, SlideShell } from "./SlideShell";

type Card = {
  title: string;
  body?: string;
  items?: string[];
};

export const GridSlide: React.FC<{
  heading: string;
  cards: Card[];
  columns?: number;
}> = ({ heading, cards, columns = 2 }) => {
  return (
    <SlideShell>
      <Heading>{heading}</Heading>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: `repeat(${columns}, 1fr)`,
          gap: 18,
          maxWidth: columns === 3 ? 1040 : 900,
          margin: "0 auto",
        }}
      >
        {cards.map((card, i) => (
          <div
            key={i}
            style={{
              border: `1px solid ${theme.cardBorder}`,
              borderRadius: 8,
              background: "#1a1a1a",
              padding: "16px 20px",
              boxSizing: "border-box",
              minWidth: 0,
            }}
          >
            <h3
              style={{
                color: theme.accent,
                fontSize: columns === 3 ? 20 : 22,
                margin: "0 0 10px 0",
              }}
            >
              {card.title}
            </h3>
            {card.body && (
              <div style={{ fontSize: columns === 3 ? 16 : 19, lineHeight: 1.4 }}>
                {card.body}
              </div>
            )}
            {card.items && (
              <ul style={{ fontSize: 16, margin: 0, paddingLeft: 18 }}>
                {card.items.map((it, j) => (
                  <li key={j} style={{ marginBottom: 4 }}>
                    {it}
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    </SlideShell>
  );
};
