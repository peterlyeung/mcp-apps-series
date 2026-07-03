import { Composition } from "remotion";
import { Episode, getEpisodeDuration } from "./Episode";
import { W, H } from "./theme";

import ep00 from "../content/00.json";
import ep01 from "../content/01.json";
import ep02 from "../content/02.json";
import ep03 from "../content/03.json";
import ep04 from "../content/04.json";
import ep05 from "../content/05.json";

const episodes = [ep00, ep01, ep02, ep03, ep04, ep05];

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {episodes.map((ep) => (
        <Composition
          key={ep.id}
          id={ep.id}
          component={Episode}
          durationInFrames={getEpisodeDuration(ep.slides)}
          fps={30}
          width={W}
          height={H}
          defaultProps={{ slides: ep.slides }}
        />
      ))}
    </>
  );
};
