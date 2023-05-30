import Multiselect from "multiselect-react-dropdown";

const Model = ({ runid }: { runid: string }) => {
  const displayedVariables = [{ name: `${runid}.xml` }];
  const options = [{name: `${runid}.xml`}, {name: "b.png"}, {name: "c.jpg"}, {name: "d.pdf"}];
  const onChange = (value: Object[]) => {
    console.log(value);
  };
  return (
    <div id="model" className="box-style glassmorphism flex-col">
      <h2>Model</h2>
      <Multiselect
        style={{ backgroundColor: "white" }}
        options={options} // Options to display in the dropdown
        selectedValues={displayedVariables} // Preselected value to persist in dropdown
        displayValue="name"
        onSelect={onChange}
        onRemove={onChange}
        singleSelect
      />
    </div>
  );
}

export default Model;
