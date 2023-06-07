import { useState, useCallback, useEffect } from "react";
import Graph from "./Visualization/Graph";
import Table from "./Visualization/Table";
import VizDataLoader from "./Visualization/VizDataLoader";
import VizSettings from "./Visualization/VizSettings";
import { useCurrentPng } from "recharts-to-png";
import FileSaver from "file-saver";
import VizSidebar from "./Visualization/VizSidebar";
import DataNotFound from "./Visualization/DataNotFound";

export enum DisplayMode {
  Graph,
  Table,
  None
}
// TODO: Refactor this component
const Visualization = ({ runid }: { runid: string }) => {
  const [displayMode, setDisplayMode] = useState<DisplayMode>(
    DisplayMode.Graph
  );
  const [data, setData] = useState<Object[]>([]);
  const [xVariable, setXVariable] = useState<string>();
  const [allVariables, setAllVariables] = useState<SelectOption[]>([]);
  const [displayedVariables, setDisplayedVariables] = useState<SelectOption[]>([]);

  const [getPng, { ref }] = useCurrentPng();

  useEffect(() => {
    if (xVariable !== undefined) {
      setDisplayMode(DisplayMode.Graph);
    } else if (data.length !== 0) {
      setDisplayMode(DisplayMode.Table);
    } else {
      setDisplayMode(DisplayMode.None)
    }
  }, [xVariable]);

  const onChange = (selectedList: SelectOption[]): void => {
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
          <Graph
            data={data}
            ref={ref}
            xVariable={xVariable}
            variables={displayedVariables}
            displayMode={displayMode}
          />
          <Table data={data} 
          xVariable={xVariable}
          variables={displayedVariables} 
          displayMode={displayMode}/>
          <DataNotFound displayMode={displayMode}/>
          <VizSidebar
            handleDownload={handleDownload}
            graphDisabled={xVariable === undefined}
            tableDisabled={data.length === 0}
            displayMode={displayMode}
            setDisplayMode={setDisplayMode}
          />
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
