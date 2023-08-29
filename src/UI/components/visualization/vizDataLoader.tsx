import { Dispatch, SetStateAction, useEffect } from "react";
import Papa from "papaparse";

// This component loads data from a simulation run and sets it in the parent component's state
const VizDataLoader = ({
  runid,
  fileName,
  setData,
  setXVariable,
  setAllVariables,
  setDisplayedVariables,
  setCSVs,
}: {
  runid: string;
  fileName: string | undefined;
  setData: Dispatch<SetStateAction<Object[]>>;
  setXVariable: Dispatch<SetStateAction<string>>;
  setAllVariables: Dispatch<SetStateAction<VariableSelectOption[]>>;
  setDisplayedVariables: Dispatch<SetStateAction<VariableSelectOption[]>>;
  setCSVs: (csvs: { name: string, label: string, value: string }[]) => void;
}) => {
  // UseEffect hook to load the list of CSV files when the component mounts or when the runid changes
  useEffect(() => {
    // Fetch the directory data from the server using the runid
    const getDirectory = async () => {
      const response = await fetch(`/${runid}/directory.json`)
        .then((response) => response.json())
        .then((v) => v)
        .catch((err) => console.log(err));
      return response;
    };
    // Extract the list of CSV files from the directory data and set it in the parent component's state using the setCSVs function
    getDirectory().then((dirData: { file: string }[]) => {
      let csvs: string[] = [];
      dirData.forEach(({ file }) => {
        if (file.endsWith(".csv")) {
          csvs.push(file);
        }
      });
      setCSVs(csvs.map((key) => {
        return { name: key, label: key, value: key };
      }));
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [runid]);

  // UseEffect hook to load data when the component mounts or when the runid or fileName changes
  useEffect(() => {
    // Fetch the CSV data from the server using the runid and fileName
    const getDataset = async () => {
      const response = await fetch(`/${runid}/${fileName}`)
        .then((response) => response.text())
        .then((v) =>
          Papa.parse(v, {
            delimiter: ",",
            newline: "\n",
            header: true,
            skipEmptyLines: true,
            dynamicTyping: true,
          })
        )
        .then((v) => v.data)
        .catch((err) => console.log(err));
      return response;
    };
    // If the fileName is a CSV file, extract the data and set it in the parent component's state using the setData, setXVariable, setAllVariables, and setDisplayedVariables functions
    if (fileName !== undefined && fileName.endsWith(".csv")) {
      getDataset().then((CSVdata) => {
        if (CSVdata === undefined) {
          return;
        }
        const keys = Object.keys(CSVdata[0] as Object);
        setData(CSVdata as Object[]);
        let timeSeries = keys[0];
        setXVariable(timeSeries);
        keys.splice(0, 1);
        setAllVariables(
          keys.map((key) => {
            return { name: key, label: key, value: key };
          })
        );
        setDisplayedVariables(
          keys.slice(0, 10).map((key) => {
            return { name: key, label: key, value: key };
          })
        );
      });
    // If the fileName is not a CSV file, reset the parent component's state variables
    } else {
      setData([]);
      setXVariable("");
      setAllVariables([]);
      setDisplayedVariables([]);
    }
  }, [runid, fileName, setData, setXVariable, setAllVariables, setDisplayedVariables]);

  // Return an empty JSX element, as this component doesn't render anything
  return <></>;
};

export default VizDataLoader;