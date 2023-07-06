import { useState, useEffect } from "react";
import Graph from "./Visualization/Graph";
import Table from "./Visualization/Table";
import VizDataLoader from "./Visualization/VizDataLoader";
import VizSettings from "./Visualization/VizSettings";
import VizSidebar from "./Visualization/VizSidebar";
import DataNotFound from "./Visualization/DataNotFound";
import VizDownloader from "./Visualization/VizDownloader";

import "./CSS/Visualization.css";

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
  const [CSVs, setCSVs] = useState<CSVSelectOption[]>([]);
  const [fileName, setFileName] = useState<CSVSelectOption[]>([]);
  const [data, setData] = useState<Object[]>([]);
  const [xVariable, setXVariable] = useState<string>("");
  const [allVariables, setAllVariables] = useState<VariableSelectOption[]>([]);
  const [displayedVariables, setDisplayedVariables] = useState<VariableSelectOption[]>([])

  useEffect(() => {
    if (data.length > 1) {
      setDisplayMode(DisplayMode.Graph);
    } else if (data.length > 0) {
      setDisplayMode(DisplayMode.Table);
    } else {
      setDisplayMode(DisplayMode.None)
    }
  }, [xVariable]);

  const onChange = (selectedList: VariableSelectOption[]): void => {
    setDisplayedVariables(selectedList);
  };

  const onFileChange = (selectedList: CSVSelectOption[]): void => {
    setFileName(selectedList);
  };

  const handleDownload = () => VizDownloader(runid)

  return (
    <div
      id="data-frame-container"
      className="box-style glassmorphism flex-col container"
    >
      <h2>Data</h2>
      <VizDataLoader
        runid={runid}
        fileName={fileName.length === 0 ? undefined : fileName[0].name}
        setCSVs={(csvs) => {setCSVs(csvs); setFileName(csvs.slice(0, 1));}}
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
            graphDisabled={xVariable === ""}
            tableDisabled={data.length === 0}
            setDisplayMode={setDisplayMode}
          />
        </div>
        <VizSettings
          onChange={onChange}
          displayedVariables={displayedVariables}
          allVariables={allVariables}
          CSVs={CSVs}
          fileName={fileName}
          onFileChange={onFileChange}
        />
      </div>
    </div>
  );
};

export default Visualization;
