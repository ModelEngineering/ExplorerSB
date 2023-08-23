import { useState, useEffect } from "react";
import { DisplayMode } from "../visualization";
import { VegaLite } from "react-vega";
import { useMediaQuery } from "react-responsive";

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
  const isMobile = useMediaQuery({ query: '(max-width: 640px)' })
  const [graphData, setGraphData] = useState<any>({});
  useEffect(() => {
    if (!xVariable) {
      return;
    }
    if (!variables || variables.length === 0) {
      return;
    }
    let dataMorph: Object[] = [];
    variables.forEach((value, index) => {
      dataMorph = dataMorph.concat(
        data.map((row) => {
          return {
            // @ts-ignore
            time: row[xVariable],
            // @ts-ignore
            value: row[value.label],
            variable: value.label,
          };
        }),
      );
    });
    setGraphData({ data: dataMorph });
  }, [data, variables, xVariable]);
  if (graphData === undefined || Object.keys(graphData).length === 0) {
    return <></>;
  }
  const legendOrientation = isMobile ? "bottom" : "right";
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
