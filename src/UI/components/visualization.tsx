"use client";
import { useState, useEffect } from "react";
import Graph from "./visualization/graph";
import Table from "./visualization/table";
import VizDataLoader from "./visualization/vizDataLoader";
import VizSettings from "./visualization/vizSettings";
import VizSidebar from "./visualization/vizSidebar";
import DataNotFound from "./visualization/dataNotFound";
import VizDownloader from "./visualization/vizDownloader";

export enum DisplayMode {
  Graph,
  Table,
  None,
}
// TODO: Refactor this component
const Visualization = ({ runid }: { runid: string }) => {
  const [displayMode, setDisplayMode] = useState<DisplayMode>(
    DisplayMode.Graph,
  );
  const [CSVs, setCSVs] = useState<CSVSelectOption[]>([]);
  const [fileName, setFileName] = useState<CSVSelectOption[]>([]);
  const [data, setData] = useState<Object[]>([]);
  const [xVariable, setXVariable] = useState<string>("");
  const [allVariables, setAllVariables] = useState<VariableSelectOption[]>([]);
  const [displayedVariables, setDisplayedVariables] = useState<
    VariableSelectOption[]
  >([]);

  useEffect(() => {
    if (data.length > 1) {
      setDisplayMode(DisplayMode.Graph);
    } else if (data.length > 0) {
      setDisplayMode(DisplayMode.Table);
    } else {
      setDisplayMode(DisplayMode.None);
    }
  }, [xVariable, data]);

  const onChange = (selectedList: VariableSelectOption[]): void => {
    setDisplayedVariables(selectedList);
  };

  const onFileChange = (selectedList: CSVSelectOption[]): void => {
    setFileName(selectedList);
  };

  const handleDownload = () => VizDownloader(runid);

  return (
    <section
      id="data-frame-container"
      className="glassmorphism flex w-full flex-col gap-2 p-4 lg:max-h-[700px]"
    >
      <h2>Data (Uncurated)</h2>
      <VizDataLoader
        runid={runid}
        fileName={fileName.length === 0 ? undefined : fileName[0].name}
        setCSVs={(csvs) => {
          setCSVs(csvs);
          setFileName(csvs.slice(0, 1));
        }}
        setData={setData}
        setXVariable={setXVariable}
        setAllVariables={setAllVariables}
        setDisplayedVariables={setDisplayedVariables}
      />

      <div
        id="viz-container"
        className="z-1 flex h-full flex-col justify-between gap-2 lg:flex-row lg:gap-4"
      >
        <div
          id="viz-frame"
          className="flex h-[300px] w-full flex-col md:h-[600px] lg:w-3/4 lg:flex-row-reverse"
        >
          <VizSidebar
            handleDownload={handleDownload}
            graphDisabled={xVariable === ""}
            tableDisabled={data.length === 0}
            setDisplayMode={setDisplayMode}
          />
          <Graph
            data={data}
            xVariable={xVariable}
            variables={displayedVariables}
            displayMode={displayMode}
          />
          <Table
            data={data}
            xVariable={xVariable}
            variables={displayedVariables}
            displayMode={displayMode}
          />
          <DataNotFound displayMode={displayMode} />
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
    </section>
  );
};

export default Visualization;
