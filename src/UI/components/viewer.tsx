// Import the required modules
"use client";
import Multiselect from "multiselect-react-dropdown";
import { BiChevronDown as ChevronDown } from "react-icons/bi";
import ModelDataLoader from "./model/modelDataLoader";
import ModelFileLoader from "./model/modelFileLoader";
import ModelDisplay from "./model/modelDisplay";
import { useState } from "react";

// This component displays the model section of the results page
const Viewer = ({ runid }: { runid: string }) => {
  const [displayedModelFile, setDisplayedModelFile] = useState<
    ModelFileSelectOption[]
  >([]);
  const [modelFiles, setModelFiles] = useState<ModelFileSelectOption[]>([]);
  const [file, setFile] = useState<string>("");

  // This function is called when the user selects a model file from the dropdown
  const onChange = (value: ModelFileSelectOption[]) => {
    setDisplayedModelFile(value);
  };

  return (
    <div
      id="model"
      className="glassmorphism flex max-h-[500px] grow-0 flex-col gap-2 p-4 lg:h-[500px] lg:w-1/2"
    >
      {/* Display the model title */}
      <h2>Viewer</h2>

      {/* Load the model data */}
      <ModelDataLoader
        runid={runid}
        setModelFiles={(modelfiles) => {
          setModelFiles(modelfiles);
          setDisplayedModelFile(modelfiles.slice(0, 1));
        }}
      />

      {/* Load the model file */}
      <ModelFileLoader
        runid={runid}
        fileName={
          displayedModelFile.length === 0 ? "" : displayedModelFile[0].name
        }
        setFile={setFile}
      />

      {/* Display the model file dropdown */}
      <Multiselect className="z-20"
        data-testid="model-select"
        options={modelFiles} // Options to display in the dropdown
        selectedValues={displayedModelFile} // Preselected value to persist in dropdown
        displayValue="name"
        onSelect={onChange}
        onRemove={onChange}
        singleSelect
        customArrow={<ChevronDown className="select-dropdown-arrow" />}
      />

      {/* Display the model */}
      <ModelDisplay
        fileName={
          displayedModelFile.length === 0 ? "" : displayedModelFile[0].name
        }
        runID={runid}
        data={file}
      />
    </div>
  );
};

export default Viewer;