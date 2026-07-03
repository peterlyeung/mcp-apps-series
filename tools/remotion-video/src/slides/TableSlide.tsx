import React from "react";
import { theme } from "../theme";
import { Heading, Small, SlideShell } from "./SlideShell";

export const TableSlide: React.FC<{
  heading: string;
  rows: [string, string][];
  small?: string;
}> = ({ heading, rows, small }) => {
  return (
    <SlideShell>
      <Heading>{heading}</Heading>
      <table
        style={{
          borderCollapse: "collapse",
          fontSize: 21,
          maxWidth: 1040,
          margin: "0 auto",
          width: "100%",
        }}
      >
        <thead>
          <tr>
            <th
              style={{
                color: theme.accent,
                textAlign: "left",
                borderBottom: `2px solid ${theme.accent}`,
                padding: "8px 20px 8px 0",
              }}
            >
              Client sends
            </th>
            <th
              style={{
                color: theme.accent,
                textAlign: "left",
                borderBottom: `2px solid ${theme.accent}`,
                padding: "8px 0",
              }}
            >
              Server responds with
            </th>
          </tr>
        </thead>
        <tbody>
          {rows.map(([a, b], i) => (
            <tr key={i}>
              <td
                style={{
                  fontFamily: theme.mono,
                  color: theme.accent,
                  padding: "10px 20px 10px 0",
                  borderBottom: "1px solid #333",
                  whiteSpace: "nowrap",
                }}
              >
                {a}
              </td>
              <td style={{ padding: "10px 0", borderBottom: "1px solid #333" }}>
                {b}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {small && (
        <div style={{ maxWidth: 1040, margin: "0 auto" }}>
          <Small>{small}</Small>
        </div>
      )}
    </SlideShell>
  );
};
