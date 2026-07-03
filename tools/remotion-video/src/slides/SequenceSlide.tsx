import React from "react";
import { theme } from "../theme";
import { Heading, SlideShell } from "./SlideShell";

export type SeqMessage = {
  from: string;
  to: string;
  label: string;
  dashed?: boolean;
};

const CONTENT_WIDTH = 1080;
const BOX_HEIGHT = 56;
const ROW_HEIGHT = 46;
const HEADER_TOP = 10;

export const SequenceDiagram: React.FC<{
  actors: string[];
  messages: SeqMessage[];
  compact?: boolean;
}> = ({ actors, messages, compact }) => {
  const n = actors.length;
  const slot = CONTENT_WIDTH / n;
  const actorX = (name: string) => {
    const i = actors.indexOf(name);
    return slot * i + slot / 2;
  };

  const diagramHeight =
    HEADER_TOP + BOX_HEIGHT + messages.length * ROW_HEIGHT + 20;

  const rowHeight = compact ? ROW_HEIGHT * 0.82 : ROW_HEIGHT;

  return (
    <div
      style={{
        position: "relative",
        width: CONTENT_WIDTH,
        height: HEADER_TOP + BOX_HEIGHT + messages.length * rowHeight + 20,
        margin: "0 auto",
      }}
    >
      {/* actor boxes */}
      {actors.map((a, i) => (
        <div
          key={a}
          style={{
            position: "absolute",
            top: HEADER_TOP,
            left: actorX(a) - 110,
            width: 220,
            height: BOX_HEIGHT,
            border: `1px solid ${theme.cardBorder}`,
            borderRadius: 6,
            background: theme.cardBg,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: compact ? 17 : 19,
            boxSizing: "border-box",
            textAlign: "center",
            padding: "0 8px",
          }}
        >
          {a}
        </div>
      ))}

      {/* lifelines */}
      <svg
        width={CONTENT_WIDTH}
        height={HEADER_TOP + BOX_HEIGHT + messages.length * rowHeight + 20}
        style={{ position: "absolute", top: 0, left: 0 }}
      >
        {actors.map((a) => (
          <line
            key={a}
            x1={actorX(a)}
            x2={actorX(a)}
            y1={HEADER_TOP + BOX_HEIGHT}
            y2={HEADER_TOP + BOX_HEIGHT + messages.length * rowHeight}
            stroke="#555"
            strokeWidth={1.5}
          />
        ))}

        {messages.map((m, i) => {
          const y = HEADER_TOP + BOX_HEIGHT + rowHeight * i + rowHeight / 2;
          const x1 = actorX(m.from);
          const x2 = actorX(m.to);
          const dir = x2 > x1 ? 1 : -1;
          const arrowSize = 7;
          return (
            <g key={i}>
              <line
                x1={x1}
                x2={x2 - dir * arrowSize}
                y1={y}
                y2={y}
                stroke="#eee"
                strokeWidth={1.5}
                strokeDasharray={m.dashed ? "5,4" : undefined}
              />
              <polygon
                points={`${x2},${y} ${x2 - dir * arrowSize},${y - 4} ${x2 - dir * arrowSize},${y + 4}`}
                fill="#eee"
              />
              <text
                x={(x1 + x2) / 2}
                y={y - 8}
                fill="#eee"
                fontSize={compact ? 14 : 15.5}
                fontFamily={theme.font}
                textAnchor="middle"
              >
                {m.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

export const SequenceSlide: React.FC<{
  heading: string;
  actors: string[];
  messages: SeqMessage[];
}> = ({ heading, actors, messages }) => {
  return (
    <SlideShell>
      <Heading>{heading}</Heading>
      <SequenceDiagram actors={actors} messages={messages} />
    </SlideShell>
  );
};

export const SequenceWithBulletsSlide: React.FC<{
  heading: string;
  actors: string[];
  messages: SeqMessage[];
  bullets: string[];
}> = ({ heading, actors, messages, bullets }) => {
  return (
    <SlideShell>
      <Heading>{heading}</Heading>
      <SequenceDiagram actors={actors} messages={messages} compact />
      <ul
        style={{
          fontSize: 22,
          lineHeight: 1.4,
          maxWidth: 1040,
          margin: "16px auto 0",
          paddingLeft: 28,
        }}
      >
        {bullets.map((b, i) => {
          const boldMatch = b.match(/^(.*?—)(.*)$/);
          return (
            <li key={i} style={{ marginBottom: 8 }}>
              {boldMatch ? (
                <>
                  <strong>{boldMatch[1]}</strong>
                  {boldMatch[2]}
                </>
              ) : (
                b
              )}
            </li>
          );
        })}
      </ul>
    </SlideShell>
  );
};
