import { useState, useEffect } from "react";
import { DisplayMode } from "../visualization";
import { VegaLite } from "react-vega";
import { useMediaQuery } from "react-responsive";


// Define the Graph component
const Graph = ({
  data,
  xVariable,
  variables,
  displayMode,
}: {
  data: Object[];
  xVariable: string;
  variables: VariableSelectOption[];
  displayMode: DisplayMode;
}) => {
  // Check if the screen width matches a mobile size
  const isMobile = useMediaQuery({ query: '(max-width: 640px)' })
  
  // State to store the transformed graph data
  const [graphData, setGraphData] = useState<any>({});
  useEffect(() => {
    // Check if the necessary variables are provided
    if (!xVariable) {
      return;
    }
    if (!variables || variables.length === 0) {
      return;
    }
    
    // Transform data for graph display
    let dataMorph: Object[] = [];
    variables.forEach((value, index) => {
      dataMorph = dataMorph.concat(
        data.map((row) => {
          return {
            // @ts-ignore: Ignore type checking for this line
            time: row[xVariable],
            // @ts-ignore: Ignore type checking for this line
            value: row[value.label],
            variable: value.label,
          };
        }),
      );
    });
    // Update the graph data state
    setGraphData({ data: dataMorph });
  }, [data, variables, xVariable]);

  // If graph data is unavailable, return an empty fragment
  if (graphData === undefined || Object.keys(graphData).length === 0) {
    return <></>;
  }
  
  // Determine the orientation of the legend based on screen size
  const legendOrientation = isMobile ? "bottom" : "right";
  
  // Define the specification for the VegaLite graph
  const spec = {
    padding: 10,
    background: "#f0f9ff",
    width: "container",
    height: "container",
    mark: {type: "line", tooltip: true},
    encoding: {
      x: { field: "time", type: "quantitative" },
      y: { field: "value", type: "quantitative" },
      color: {
        field: "variable",
        type: "nominal",
        legend: {
          title: "Variables",
          symbolStrokeWidth: 10,
          orient: legendOrientation,
          columns: 1,
        },
        scale: {
          scheme: "category20",
        },
      },
    },
    data: { name: "data" },
  } as const;

  // Return the graph component
  return (
    <div
      id="graph-container"
      className={
        "h-[560px] w-full md:h-[560px] lg:h-[600px]" +
        (displayMode === DisplayMode.Graph ? "" : " hidden")
      }
    >
      <VegaLite spec={spec} data={graphData} actions={false} />
    </div>
  );
};
export default Graph;
