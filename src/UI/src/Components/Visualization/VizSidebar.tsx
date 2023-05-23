import {
  BiDownload as DownloadIcon,
  BiChart as ChartIcon,
  BiTable as TableIcon,
} from "react-icons/bi";

const VizSidebar = ({
  handleDownload,
}: {
  handleDownload: React.MouseEventHandler<HTMLButtonElement>;
}) => {
  return (
    <div id="viz-sidebar" className="flex-col">
      <div id="viz-sidebar-top" className="flex-col">
        <button className="viz-sidebar-button" title="View as Chart">
          <ChartIcon />
        </button>
        <button className="viz-sidebar-button" title="View as Table">
          <TableIcon />
        </button>
      </div>
      <div id="viz-sidebar-bottom" className="flex-col">
        <button
          className="viz-sidebar-button"
          title="Download as PNG"
          onClick={handleDownload}
        >
          <DownloadIcon />
        </button>
      </div>
    </div>
  );
};

export default VizSidebar;
