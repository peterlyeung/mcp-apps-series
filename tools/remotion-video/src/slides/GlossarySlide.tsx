import React from "react";
import { theme } from "../theme";
import { Heading, SlideShell } from "./SlideShell";

export const GlossarySlide: React.FC<{
  heading: string;
  terms: { term: string; def: string }[];
}> = ({ heading, terms }) => {
  return (
    <SlideShell>
      <Heading>{heading}</Heading>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "220px 1fr",
          rowGap: 16,
          columnGap: 24,
          maxWidth: 1040,
          margin: "0 auto",
          fontSize: 21,
        }}
      >
        {terms.map((t, i) => (
          <React.Fragment key={i}>
            <div
              style={{
                color: theme.accent,
                fontFamily: theme.mono,
                textAlign: "right",
                fontWeight: 700,
              }}
            >
              {t.term}
            </div>
            <div>{t.def}</div>
          </React.Fragment>
        ))}
      </div>
    </SlideShell>
  );
};
