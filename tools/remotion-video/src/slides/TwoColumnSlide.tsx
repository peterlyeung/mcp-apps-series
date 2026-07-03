import React from "react";
import { theme } from "../theme";
import { Heading, Small, SlideShell } from "./SlideShell";

type Column = {
  title: string;
  caption?: string;
  middleLabel?: string;
  bottomTitle?: string;
};

const Box: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    style={{
      border: `1px solid ${theme.cardBorder}`,
      borderRadius: 8,
      background: theme.cardBg,
      padding: "18px 26px",
      fontSize: 22,
      textAlign: "center",
      minWidth: 260,
      boxSizing: "border-box",
    }}
  >
    {children}
  </div>
);

const Column: React.FC<{ col: Column }> = ({ col }) => (
  <div
    style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      width: 420,
    }}
  >
    <Box>{col.title}</Box>
    {col.middleLabel && (
      <>
        <div style={{ width: 2, height: 30, background: "#666" }} />
        <div
          style={{
            background: "rgba(120,120,120,0.5)",
            padding: "5px 16px",
            borderRadius: 4,
            fontSize: 18,
            whiteSpace: "nowrap",
          }}
        >
          {col.middleLabel}
        </div>
        <div style={{ width: 2, height: 30, background: "#666" }} />
      </>
    )}
    {col.bottomTitle && <Box>{col.bottomTitle}</Box>}
    {col.caption && (
      <div
        style={{
          marginTop: 14,
          fontSize: 17,
          color: theme.textDim,
          textAlign: "center",
          maxWidth: 340,
        }}
      >
        {col.caption}
      </div>
    )}
  </div>
);

export const TwoColumnSlide: React.FC<{
  heading: string;
  tag?: string;
  intro?: string;
  columns: Column[];
  small?: string;
}> = ({ heading, tag, intro, columns, small }) => {
  return (
    <SlideShell>
      <Heading tag={tag}>{heading}</Heading>
      {intro && (
        <p
          style={{
            fontSize: 23,
            textAlign: "center",
            maxWidth: 1040,
            margin: "0 auto 24px",
            lineHeight: 1.4,
          }}
        >
          {intro}
        </p>
      )}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: 90,
          marginTop: 20,
        }}
      >
        {columns.map((col, i) => (
          <Column key={i} col={col} />
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
