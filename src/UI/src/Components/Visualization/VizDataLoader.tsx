import { Dispatch, SetStateAction, useEffect } from "react";
import Papa from "papaparse";

const timeData = [
  "data_set_time",
  "data_set_T",
  "data_set_value_component_environment_variable_time",
];

const VizDataLoader = ({
  runid,
  setData,
  setXVariable,
  setAllVariables,
  setDisplayedVariables
}: {
  runid: string;
  setData: Dispatch<SetStateAction<Object[]>>;
  setXVariable: Dispatch<SetStateAction<string | undefined>>;
  setAllVariables: Dispatch<SetStateAction<SelectOption[]>>;
  setDisplayedVariables: Dispatch<SetStateAction<SelectOption[]>>;
}) => {
  useEffect(() => {
    const getDataset = async () => {
      const response = await fetch(`/${runid}/report.csv`)
        .then(response => response.text())
        .then(v => Papa.parse(v, { delimiter: "," , newline: "\n", header: true, skipEmptyLines: true, dynamicTyping: true}))
        .then(v => v.data)
        .catch(err => console.log(err))
        return response
    }
    getDataset().then((data) => {
      if (data === undefined) {
        return;
      }
      const keys = Object.keys(data[0] as Object);
      setData(data as Object[]);
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
          return {name: key, label: key, value: key};
        })
      );
      setDisplayedVariables(
        keys.slice(0, 10).map((key) => {
          return {name: key, label: key, value: key};
        })
      );
    });
    setData([]);
    setXVariable(undefined);
    setAllVariables([]);
    setDisplayedVariables([]);
  }, [runid]);

  return <></>
}

export default VizDataLoader;