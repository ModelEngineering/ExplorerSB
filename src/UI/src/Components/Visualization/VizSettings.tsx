import { MultiSelect } from "react-multi-select-component";
import Multiselect from "multiselect-react-dropdown";
import {BiChevronDown as ChevronDown} from "react-icons/bi";

const VizSettings = ({
  onChange,
  allVariables,
  displayedVariables,
  CSVs,
  fileName,
  onFileChange
}: {
  onChange(value: VariableSelectOption[]): void;
  allVariables: VariableSelectOption[];
  displayedVariables: VariableSelectOption[];
  CSVs: CSVSelectOption[];
  fileName: CSVSelectOption[];
  onFileChange(value: CSVSelectOption[]): void;
}) => {
  return (
    <div id="viz-settings-container" className="flex-col">
      <h3>Settings</h3>
      <Multiselect
        options={CSVs} // Options to display in the dropdown
        selectedValues={fileName} // Preselected value to persist in dropdown
        displayValue="name"
        onSelect={onFileChange}
        onRemove={onFileChange} 
        singleSelect
        customArrow={<ChevronDown className="select-dropdown-arrow"/>}
      />
      <MultiSelect
        options={allVariables}
        value={displayedVariables}
        onChange={onChange}
        labelledBy={"Select Variable"}
        hasSelectAll={false}
        overrideStrings={{ "selectSomeItems": "Select variables to display..."}}
      />
    </div>
  )
};

export default VizSettings;
