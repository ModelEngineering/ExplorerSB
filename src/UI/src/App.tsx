import "./App.css";
import { useState } from "react";

import Title from "./Components/Title"
import Footer from "./Components/Footer";
import Visualization from "./Components/Visualization";
import Model from "./Components/Model";
import Header from "./Components/Header";
import Summary from "./Components/Summary";
import Landing from "./Components/Landing";

function App() {
  const [selected, setSelected] = useState<Context>();
  return selected != null ? (
    <div id="App">
      <Header setSelected={setSelected} / >
      <Title title={selected.title} proj_id={selected.project_id}/>
      <div id="summary-model-container" className="flex-row container">
        <Summary summary={selected.abstract}/>
        <Model />
      </div>
      <Visualization runid={selected.runid}/>
      <div id="footer" className="flex-row">
        <Footer />
      </div>
    </div>) : <Landing setSelected={setSelected}/>
  ;
}

export default App;
