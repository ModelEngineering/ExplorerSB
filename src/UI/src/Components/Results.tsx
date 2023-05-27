import Title from "./Title"
import Footer from "./Footer";
import Visualization from "./Visualization";
import Model from "./Model";
import Header from "./Header";
import Summary from "./Summary";

import contextJson from "../Assets/context.json";
import { Navigate, useParams } from "react-router-dom";
import { useMemo } from "react";

const store: Record<string, Context> = {};

const createStoreDict = (data: Context[]) => {
  for (let entry = 0; entry < data.length; entry++) {
    let dataResult = data[entry] as Context;
    store[dataResult.runid] = dataResult;
  }
}

const Results = () => {
  useMemo(() => createStoreDict(contextJson), [contextJson])
  const { run_id } = useParams();
  if (run_id === undefined) {
    return <Navigate to="/" replace />
  }
  const selected = store[run_id];
  
  if (!Object.keys(store).includes(run_id)) {
    return <Navigate to="/" replace />
  }

  return (
    <>
      <Header / >
      <Title title={selected.title} proj_id={selected.project_id}/>
      <div id="summary-model-container" className="flex-row container">
        <Summary context={selected}/>
        <Model />
      </div>
      <Visualization runid={selected.runid}/>
      <div id="footer" className="flex-row">
        <Footer />
      </div>
    </>
  );
}

export default Results;