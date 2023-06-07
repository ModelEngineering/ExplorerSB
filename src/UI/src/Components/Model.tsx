import Multiselect from "multiselect-react-dropdown";
import {BiChevronDown as ChevronDown} from "react-icons/bi";

const Model = ({ runid }: { runid: string }) => {
  const displayedVariables = [{ name: `${runid}.ant` }];
  const options = [{name: `${runid}.ant`}, {name: "b.png"}, {name: "c.ant"}, {name: "d.png"}];
  const onChange = (value: Object[]) => {
    console.log(value);
  };
  return (
    <div id="model" className="box-style glassmorphism flex-col">
      <h2>Model</h2>
      <Multiselect
        options={options} // Options to display in the dropdown
        selectedValues={displayedVariables} // Preselected value to persist in dropdown
        displayValue="name"
        onSelect={onChange}
        onRemove={onChange} 
        singleSelect
        customArrow={<ChevronDown className="select-dropdown-arrow"/>}
      />
    </div>
  );
}

export default Model;
