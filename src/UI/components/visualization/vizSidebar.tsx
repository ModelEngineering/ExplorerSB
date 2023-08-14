import {
  BiDownload as DownloadIcon,
  BiChart as ChartIcon,
  BiTable as TableIcon,
} from "react-icons/bi";
import { DisplayMode } from "../visualization";

const VizSidebar = ({
  handleDownload,
  graphDisabled,
  tableDisabled,
  setDisplayMode,
}: {
  handleDownload: React.MouseEventHandler<HTMLButtonElement>;
  graphDisabled: boolean;
  tableDisabled: boolean;
  setDisplayMode: Function;
}) => {
  return (
    <div id="viz-sidebar" className="flex flex-col h-full justify-between">
      <div id="viz-sidebar-top" className="flex flex-col">
        <button
          className="rounded-r-lg pl-1 text-center text-2xl h-10 w-9 bg-slate-700 bg-opacity-50 hover:bg-opacity-70"
          title="View as Chart"
          disabled={graphDisabled}
          onClick={() => setDisplayMode(DisplayMode.Graph)}
        >
          <ChartIcon />
        </button>
        <button
          className="rounded-r-lg pl-1 text-center text-2xl h-10 w-9 bg-slate-700 bg-opacity-50 hover:bg-opacity-70"
          title="View as Table"
          disabled={tableDisabled}
          onClick={() => setDisplayMode(DisplayMode.Table)}
        >
          <TableIcon />
        </button>
      </div>
      <div id="viz-sidebar-bottom" className="flex flex-col self-end">
        <button
          className="rounded-r-lg pl-1 text-center text-2xl h-10 w-9 bg-slate-700 bg-opacity-50 hover:bg-opacity-70"
          title="Download Project Files as Zip"
          onClick={handleDownload}
        >
          <DownloadIcon />
        </button>
      </div>
    </div>
  );
};

export default VizSidebar;
