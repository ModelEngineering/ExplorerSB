"use client";
import Multiselect from "multiselect-react-dropdown";
import { BiChevronDown as ChevronDown } from "react-icons/bi";
import ModelDataLoader from "./model/modelDataLoader";
import { useState } from "react";
import ModelFileLoader from "./model/modelFileLoader";
import ModelDisplay from "./model/modelDisplay";

const Viewer = ({ runid }: { runid: string }) => {
  const [displayedModelFile, setDisplayedModelFile] = useState<
    ModelFileSelectOption[]
  >([]);
  const [modelFiles, setModelFiles] = useState<ModelFileSelectOption[]>([]);
  const [file, setFile] = useState<string>("");
  const onChange = (value: ModelFileSelectOption[]) => {
    setDisplayedModelFile(value);
  };
  return (
    <div
      id="model"
      className="glassmorphism flex max-h-[500px] grow-0 flex-col gap-2 p-4 lg:h-[500px] lg:w-1/2"
    >
      <h2>Model</h2>
      <ModelDataLoader
        runid={runid}
        setModelFiles={(modelfiles) => {
          setModelFiles(modelfiles);
          setDisplayedModelFile(modelfiles.slice(0, 1));
        }}
      />
      <ModelFileLoader
        runid={runid}
        fileName={
          displayedModelFile.length === 0 ? "" : displayedModelFile[0].name
        }
        setFile={setFile}
      />
      <Multiselect
        data-testid="model-select"
        options={modelFiles} // Options to display in the dropdown
        selectedValues={displayedModelFile} // Preselected value to persist in dropdown
        displayValue="name"
        onSelect={onChange}
        onRemove={onChange}
        singleSelect
        customArrow={<ChevronDown className="select-dropdown-arrow" />}
      />
      <ModelDisplay
        fileName={
          displayedModelFile.length === 0 ? "" : displayedModelFile[0].name
        }
        data={file}
      />
    </div>
  );
};

export default Viewer;
