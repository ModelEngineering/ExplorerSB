import { Dispatch, SetStateAction, useEffect } from "react";
import Papa from "papaparse";

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
  useEffect(() => {
    const getDirectory = async () => {
      const response = await fetch(`/${runid}/directory.json`)
        .then((response) => response.json())
        .then((v) => v)
        .catch((err) => console.log(err));
      return response;
    };
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

  useEffect(() => {
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
      setData([]);
      setXVariable("");
      setAllVariables([]);
      setDisplayedVariables([]);
    }
  }, [runid, fileName, setData, setXVariable, setAllVariables, setDisplayedVariables]);
  return <></>;
};

export default VizDataLoader;
