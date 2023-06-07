import { MultiSelect } from "react-multi-select-component";

const VizSettings = ({
  onChange,
  allVariables,
  displayedVariables,
}: {
  onChange(value: SelectOption[]): void;
  allVariables: SelectOption[];
  displayedVariables: SelectOption[];
}) => {
  return (
    <div id="viz-settings-container" className="flex-col">
      <h3>Settings</h3>
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
