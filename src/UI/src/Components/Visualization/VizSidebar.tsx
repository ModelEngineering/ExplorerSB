import {
  BiDownload as DownloadIcon,
  BiChart as ChartIcon,
  BiTable as TableIcon,
} from "react-icons/bi";
import { DisplayMode } from "../Visualization";

const VizSidebar = ({
  handleDownload,
  graphDisabled,
  tableDisabled,
  displayMode,
  setDisplayMode,
}: {
  handleDownload: React.MouseEventHandler<HTMLButtonElement>;
  graphDisabled: boolean;
  tableDisabled: boolean;
  displayMode: DisplayMode;
  setDisplayMode: Function;
}) => {
  return (
    <div id="viz-sidebar" className="flex-col">
      <div id="viz-sidebar-top" className="flex-col">
        <button
          className="viz-sidebar-button"
          title="View as Chart"
          disabled={graphDisabled}
          onClick={() => setDisplayMode(DisplayMode.Graph)}
        >
          <ChartIcon />
        </button>
        <button
          className="viz-sidebar-button"
          title="View as Table"
          disabled={tableDisabled}
          onClick={() => setDisplayMode(DisplayMode.Table)}
        >
          <TableIcon />
        </button>
      </div>
      <div id="viz-sidebar-bottom" className="flex-col">
        <button
          className="viz-sidebar-button"
          title="Download Project Files as Zip"
          disabled={displayMode === DisplayMode.None}
          onClick={handleDownload}
        >
          <DownloadIcon />
        </button>
      </div>
    </div>
  );
};

export default VizSidebar;
