import "./App.css";
import Title from "./Components/Title"
import Footer from "./Components/Footer";
import Visualization from "./Components/Visualization";
import Model from "./Components/Model";
import Searchbar from "./Components/Searchbar";
import Summary from "./Components/Summary";

import { useState } from "react";
import Landing from "./Components/Landing";

function App() {
  const [selected, setSelected] = useState<SearchResult>();
  return selected != null ? (
    <div id="App">
      <div id="header" className="flex-row" >
        <h1 id="logo" onClick={() => setSelected(undefined)}>ExplorerSB</h1>
        <Searchbar setSelected={setSelected}/>
      </div>
      <div className="flex-row container">
        <Title title={selected.title} proj_id={selected.project_id}/>
      </div>
      <div className="flex-row container">
        <Summary summary={selected.abstract}/>
        <Model />
      </div>
      <div className="flex-row container">
        <Visualization runid={selected.runid}/>
      </div>
      <div id="footer" className="flex-row">
        <Footer />
      </div>
    </div>) : <Landing setSelected={setSelected}/>
  ;
}

export default App;
