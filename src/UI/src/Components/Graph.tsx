import { useEffect, useState } from "react";
import { VictoryChart, VictoryLine, VictoryZoomContainer } from "victory";

const Graph = ({runid} : {runid: string}) => {
  const [data, setData] = useState([])
  const modules = import.meta.glob('../**/report.json')
  useEffect(() => {
    for (const path in modules) {
      if(path.indexOf(runid) === -1) continue
      modules[path]().then((mod) => {
        setData(mod.default)
      })
    }
  }, [runid])
  
  return (
    <div id="graph-container" className="box-style">
      <h2>Graph</h2>
      <VictoryChart containerComponent={
    <VictoryZoomContainer zoomDimension="x"/>
  }>
        <VictoryLine
          data={data}
          x="data_set_T"
          y="data_set_CD"
        />
      </VictoryChart>
    </div>
  );
};

export default Graph;
