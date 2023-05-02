import "./App.css";
import Title from "./Components/Title"
import Footer from "./Components/Footer";
import Graph from "./Components/Graph";
import Model from "./Components/Model";
import Searchbar from "./Components/Searchbar";
import Summary from "./Components/Summary";

import {useState} from "react";
import Landing from "./Components/Landing";

function App() {
  const [selected, setSelected] = useState();
  return selected == null ? (
    <div id="App">
      <div id="header" className="flex-row" >
        <h1>ExplorerSB</h1>
        <Searchbar />
      </div>
      <div className="flex-row container">
        <Title />
      </div>
      <div className="flex-row container">
        <Summary />
        <Model />
      </div>
      <div className="flex-row container">
        <Graph />
      </div>
      <div id="footer" className="flex-row">
        <Footer />
      </div>
    </div>) : <Landing />
  ;
}

export default App;
