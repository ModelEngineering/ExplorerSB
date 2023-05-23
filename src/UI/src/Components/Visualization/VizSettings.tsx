import Multiselect from "multiselect-react-dropdown";

const VizSettings = ({
  onChange,
  allVariables,
  displayedVariables,
}: {
  onChange(value: Object[]): void;
  allVariables: Object[];
  displayedVariables: Object[];
}) => {
  return (
    <div id="viz-settings-container" className="flex-col">
      <h3>Settings</h3>
      <Multiselect
        style={{ backgroundColor: "white" }}
        options={allVariables} // Options to display in the dropdown
        selectedValues={displayedVariables} // Preselected value to persist in dropdown
        displayValue="name"
        onSelect={onChange}
        onRemove={onChange}
        selectionLimit={10}
        placeholder="Select up to 10 variables"
        showCheckbox
      />
    </div>
  )
};

export default VizSettings;
