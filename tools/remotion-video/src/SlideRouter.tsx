import React from "react";
import { TitleSlide } from "./slides/TitleSlide";
import { TextSlide } from "./slides/TextSlide";
import { BulletsSlide } from "./slides/BulletsSlide";
import { StepsSlide } from "./slides/StepsSlide";
import { TwoColumnSlide } from "./slides/TwoColumnSlide";
import { GridSlide } from "./slides/GridSlide";
import { TableSlide } from "./slides/TableSlide";
import { GlossarySlide } from "./slides/GlossarySlide";
import { RoadmapSlide } from "./slides/RoadmapSlide";
import { PartnersSlide } from "./slides/PartnersSlide";
import { LayersSlide } from "./slides/LayersSlide";
import {
  SequenceSlide,
  SequenceWithBulletsSlide,
} from "./slides/SequenceSlide";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const SlideRouter: React.FC<{ slide: any }> = ({ slide }) => {
  switch (slide.type) {
    case "title":
      return (
        <TitleSlide
          title={slide.title}
          subtitle={slide.subtitle}
          eyebrow={slide.eyebrow}
        />
      );
    case "text":
      return (
        <TextSlide
          heading={slide.heading}
          paragraphs={slide.paragraphs}
          bullets={slide.bullets}
          small={slide.small}
          warn={slide.warn}
        />
      );
    case "bullets":
      return <BulletsSlide heading={slide.heading} items={slide.items} />;
    case "steps":
      return <StepsSlide heading={slide.heading} items={slide.items} />;
    case "twoColumn":
      return (
        <TwoColumnSlide
          heading={slide.heading}
          tag={slide.tag}
          intro={slide.intro}
          columns={slide.columns}
          small={slide.small}
        />
      );
    case "grid":
      return (
        <GridSlide
          heading={slide.heading}
          cards={slide.cards}
          columns={slide.columns}
        />
      );
    case "table":
      return (
        <TableSlide heading={slide.heading} rows={slide.rows} small={slide.small} />
      );
    case "glossary":
      return <GlossarySlide heading={slide.heading} terms={slide.terms} />;
    case "roadmap":
      return (
        <RoadmapSlide heading={slide.heading} items={slide.items} small={slide.small} />
      );
    case "partners":
      return (
        <PartnersSlide heading={slide.heading} names={slide.names} small={slide.small} />
      );
    case "layers":
      return <LayersSlide heading={slide.heading} items={slide.items} />;
    case "sequence":
      return (
        <SequenceSlide
          heading={slide.heading}
          actors={slide.actors}
          messages={slide.messages}
        />
      );
    case "sequenceWithBullets":
      return (
        <SequenceWithBulletsSlide
          heading={slide.heading}
          actors={slide.actors}
          messages={slide.messages}
          bullets={slide.bullets}
        />
      );
    default:
      return <div>Unknown slide type: {slide.type}</div>;
  }
};
