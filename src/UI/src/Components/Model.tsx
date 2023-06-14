import Multiselect from "multiselect-react-dropdown";
import {BiChevronDown as ChevronDown} from "react-icons/bi";
import ModelDataLoader from "./Model/ModelDataLoader";
import { useState } from "react";

const Model = ({ runid }: { runid: string }) => {
  const [displayedModelFile, setDisplayedModelFile] = useState<ModelFileSelectOption[]>([]);
  const [modelFiles, setModelFiles] = useState<ModelFileSelectOption[]>([]);
  const onChange = (value: ModelFileSelectOption[]) => {
    setDisplayedModelFile(value);
  };
  return (
    <div id="model" className="box-style glassmorphism flex-col">
      <h2>Model</h2>
      <ModelDataLoader runid={runid} setModelFiles={(modelfiles) => {setModelFiles(modelfiles); console.log(modelfiles.slice(0,1)); setDisplayedModelFile(modelfiles.slice(0, 1));}}/>
      <Multiselect
        options={modelFiles} // Options to display in the dropdown
        selectedValues={displayedModelFile} // Preselected value to persist in dropdown
        displayValue="name"
        onSelect={onChange}
        onRemove={onChange} 
        singleSelect
        customArrow={<ChevronDown className="select-dropdown-arrow"/>}
      />
      <p>{displayedModelFile.length === 0 ? "nothing" : displayedModelFile[0].name}</p>
    </div>
  );
}

export default Model;
