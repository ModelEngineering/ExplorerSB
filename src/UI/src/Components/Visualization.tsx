import { useEffect, useState } from "react";
import { VictoryChart, VictoryLine, VictoryZoomContainer } from "victory";

const Visualization = ({runid} : {runid: string}) => {
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
    <div id="viz-container" className="box-style glassmorphism">
      <h2>Data</h2>
      <div id="graph-container">
        <VictoryChart 
          containerComponent={<VictoryZoomContainer zoomDimension="x"/>}
          style={{parent: {
            height: "fit-content",
            width: "fit-content",
            border: "2px solid #ccc"
          },}}
        >
          <VictoryLine
            data={data}
            x="data_set_time"
            y="data_set_laci_protein"
          />
        </VictoryChart>
      </div>
    </div>
  );
};

export default Visualization;
