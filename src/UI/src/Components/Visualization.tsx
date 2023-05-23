import { useState, useCallback } from "react";
import Graph from "./Visualization/Graph";
import Table from "./Visualization/Table";
import VizDataLoader from "./Visualization/VizDataLoader";
import VizSettings from "./Visualization/VizSettings";
import { useCurrentPng } from "recharts-to-png";
import FileSaver from "file-saver";
import VizSidebar from "./Visualization/VizSidebar";

// TODO: Refactor this component
const Visualization = ({ runid }: { runid: string }) => {
  const [data, setData] = useState<Object[]>([]);
  const [xVariable, setXVariable] = useState<string>();
  const [allVariables, setAllVariables] = useState<Object[]>([]);
  const [displayedVariables, setDisplayedVariables] = useState<Object[]>([]);

  const [getPng, { ref }] = useCurrentPng();

  const onChange = (selectedList: Object[]): void => {
    setDisplayedVariables(selectedList);
  };

  const handleDownload = useCallback(async () => {
    const png = await getPng();

    if (png) {
      FileSaver.saveAs(png, "Chart.png");
    }
  }, [getPng]);

  return (
    <div
      id="data-frame-container"
      className="box-style glassmorphism flex-col container"
    >
      <h2>Data</h2>
      <VizDataLoader
        runid={runid}
        setData={setData}
        setXVariable={setXVariable}
        setAllVariables={setAllVariables}
        setDisplayedVariables={setDisplayedVariables}
      />

      <div id="viz-container" className="flex-row">
        <div id="viz-frame" className="flex-row">
          {/* if we found a matching time series X variable, we can display a graph, otherwise we display a table */}
          {xVariable !== undefined ? (
            <Graph
              data={data}
              ref={ref}
              xVariable={xVariable}
              variables={displayedVariables}
            />
          ) : (
            <Table data={data} />
          )}
          <VizSidebar handleDownload={handleDownload} />
        </div>
        <VizSettings
          onChange={onChange}
          displayedVariables={displayedVariables}
          allVariables={allVariables}
        />
      </div>
    </div>
  );
};

export default Visualization;
