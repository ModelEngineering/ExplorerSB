import "./App.css";
import Title from "./Components/Title"
import Footer from "./Components/Footer";
import Graph from "./Components/Graph";
import Model from "./Components/Model";
import Searchbar from "./Components/Searchbar";
import Summary from "./Components/Summary";

import { useState } from "react";
import Landing from "./Components/Landing";

function App() {
  const [selected, setSelected] = useState<SearchResult>();
  const onResultSelected = (value:SearchResult) => {
    setSelected(value)
    console.log(value)
  }
  return selected != null ? (
    <div id="App">
      <div id="header" className="flex-row" >
        <h1 id="logo">ExplorerSB</h1>
        <Searchbar setResult={onResultSelected}/>
      </div>
      <div className="flex-row container">
        <Title title={selected.title} proj_id={selected.project_id}/>
      </div>
      <div className="flex-row container">
        <Summary summary={selected.abstract}/>
        <Model />
      </div>
      <div className="flex-row container">
        <Graph />
      </div>
      <div id="footer" className="flex-row">
        <Footer />
      </div>
    </div>) : <Landing setResult={onResultSelected}/>
  ;
}

export default App;
