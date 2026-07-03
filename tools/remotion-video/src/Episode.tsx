import React from "react";
import { Audio, Sequence, staticFile } from "remotion";
import { SlideRouter } from "./SlideRouter";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const Episode: React.FC<{ slides: any[] }> = ({ slides }) => {
  let cursor = 0;
  return (
    <>
      {slides.map((slide, i) => {
        const from = cursor;
        const duration = slide.durationInFrames || 90;
        cursor += duration;
        return (
          <Sequence key={i} from={from} durationInFrames={duration}>
            <SlideRouter slide={slide} />
            {slide.audioFile && (
              <Audio src={staticFile(slide.audioFile)} />
            )}
          </Sequence>
        );
      })}
    </>
  );
};

export const getEpisodeDuration = (slides: { durationInFrames?: number }[]) =>
  slides.reduce((sum, s) => sum + (s.durationInFrames || 90), 0);
