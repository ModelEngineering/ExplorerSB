import { Dispatch, SetStateAction, useEffect } from "react";

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
  setAllVariables: Dispatch<SetStateAction<Object[]>>;
  setDisplayedVariables: Dispatch<SetStateAction<Object[]>>;
}) => {
  const modules = import.meta.glob("/src/Assets/**/report.json");
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
      break;
    }
    setData([]);
    setXVariable(undefined);
    setAllVariables([]);
    setDisplayedVariables([]);
  }, [runid]);

  return <></>
}

export default VizDataLoader;