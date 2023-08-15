import { useState, useEffect } from "react";
import { DisplayMode } from "../visualization";
import { VegaLite } from "react-vega";
import { LayerSpec } from "vega-lite/build/src/spec";

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
  const [layers, setLayers] = useState<any[]>([]);
  const graphData = {
    table: data,
  };
  useEffect(() => {
    if (!xVariable) {
      return;
    }
    if (!variables || variables.length === 0) {
      return;
    }
    const layersUpdate = variables.map((value, index) => {
      return {
        mark: {
          stroke: ChromaticScale[index % ChromaticScale.length],
          strokeWidth: 3,
          type: "line",
          tooltip: true,
        },
        encoding: {
          x: { field: `${xVariable}`, type: "quantitative", title: "Time" },
          y: { field: `${value.label}`, type: "quantitative" },
        },
      };
    });
    setLayers(layersUpdate);
  }, [variables, xVariable]);
  if (layers.length === 0) {
    return <></>;
  }
  const spec = {
    padding: 10,
    background: "#f0f9ff",
    width: "container",
    height: "container",
    encoding: {
      y: {
        axis: { title: "Value" },
      }
    },
    // title: "Title",
    layer: layers,
    data: { name: "table" },
  } as const;
  return (
    <div
      id="graph-container"
      className={
        "h-[260px] md:h-[560px] lg:h-[600px] w-full" +
        (displayMode === DisplayMode.Graph ? "" : " hidden")
      }
    >
      <VegaLite spec={spec} data={graphData} actions={false} />
    </div>
  );
};
export default Graph;
