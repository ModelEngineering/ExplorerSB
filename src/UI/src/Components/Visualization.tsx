import { useEffect, useState } from "react";
import Multiselect from "multiselect-react-dropdown";
import Graph from "./Visualization/Graph";
import Table from "./Visualization/Table";

const timeData = [
  "data_set_time",
  "data_set_T",
  "data_set_value_component_environment_variable_time",
];

// TODO: Refactor this component 
const Visualization = ({ runid }: { runid: string }) => {
  const [data, setData] = useState([]);
  const [xVariable, setXVariable] = useState<string>();
  const [allVariables, setAllVariables] = useState<Object[]>([]);
  const [displayedVariables, setDisplayedVariables] = useState<Object[]>([]);
  const modules = import.meta.glob("../**/report.json");
  useEffect(() => {
    for (const path in modules) {
      if (path.indexOf(runid) === -1) continue;
      modules[path]().then((mod) => {
        const keys = Object.keys(mod.default[0]);
        setData(mod.default);
        timeData.some((name) => {
          let index = keys.indexOf(name);
          if (index !== -1) {
            setXVariable(name);
            keys.splice(index, 1);
            return true;
          }
        });
        setAllVariables(
          keys.map((key) => {
            return { name: key };
          })
        );
        setDisplayedVariables(
          keys.slice(0, 10).map((key) => {
            return { name: key };
          })
        );
      });
    }
  }, [runid]);

  const onChange = (selectedList: any): void => {
    setDisplayedVariables(selectedList);
  };

  return (
    <div
      id="data-frame-container"
      className="box-style glassmorphism flex-col container"
    >
      <h2>Data</h2>
      <div id="viz-container" className="flex-row">
        {/* if we found a matching time series X variable, we can display a graph, otherwise we display a table */}
        {xVariable !== undefined ? (
          <Graph
            data={data}
            xVariable={xVariable}
            variables={displayedVariables}
          />
        ) : (
          <Table />
        )}
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
      </div>
    </div>
  );
};

export default Visualization;
