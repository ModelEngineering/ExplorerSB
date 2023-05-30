import { useEffect, useState, forwardRef } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Brush,
} from "recharts";
import { DisplayMode } from "../Visualization";

const ChromaticScale = [
  "#4e79a7",
  "#f28e2c",
  "#e15759",
  "#76b7b2",
  "#59a14f",
  "#edc949",
  "#af7aa1",
  "#ff9da7",
  "#9c755f",
  "#bab0ab",
];

const Graph = forwardRef(function Graph(
  { data, xVariable, variables, displayMode}: { data: Object[]; xVariable: string | undefined; variables: { name: string }[]; displayMode: DisplayMode},
  ref: any
  ) {
  const [localVariables, setLocalVariables] = useState<string[]>([]);
  useEffect(() => {
    const updateVariables = setTimeout(() => {
      setLocalVariables(variables.map((variable: any) => variable.name));
    }, 1000);

    return () => clearTimeout(updateVariables);
  }, [variables]);
  return (
    <div id="graph-container" className={displayMode === DisplayMode.Graph ? "" : "hidden"}>
      {xVariable === undefined ? <p>Graph not Available</p> :
      <ResponsiveContainer minWidth="0" width="100%" height="100%">
        <LineChart
          width={500}
          height={300}
          data={data}
          ref={ref}
          margin={{
            top: 30,
            right: 50,
            left: 20,
            bottom: 40,
          }}
          style={{ border: "1px solid black" }}
        >
          <CartesianGrid strokeDasharray="3 10" />
          <XAxis
            height={70}
            dataKey={xVariable}
            label={{ offset: 20, value: "Time", position: "insideBottom" }}
            interval={"equidistantPreserveStart"}
            domain={['auto', 'auto']}
          />
          <YAxis label={{ value: "Value", angle: "-90", position: "left" }} domain={['auto', 'auto']}/>
          <Tooltip
            isAnimationActive={false}
            position={{ y: 0 }}
            contentStyle={{ background: "#FFFFFF" }}
            wrapperStyle={{ zIndex: 1000 }}
          />
          <Legend
            verticalAlign="bottom"
            align="center"
            wrapperStyle={{ bottom: "10px" }}
          />
          {localVariables.map((variable, index) => {
            return (
              <Line
                key={variable}
                type="monotone"
                dataKey={variable}
                stroke={ChromaticScale[index]}
                activeDot={{ r: 1 }}
                dot={false}
                isAnimationActive={false}
              />
            );
          })}
          <Brush dataKey={xVariable}/>
        </LineChart>
      </ResponsiveContainer>
      }
    </div>
  );
});
export default Graph;
