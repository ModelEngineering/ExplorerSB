import "./App.css";
import Searchbar from "./Components/Searchbar";

function App() {
  return (
    <div className="App">
      <div id="header" className="flex-row" >
        <h1>ExplorerSB</h1>
        <Searchbar/>
      </div>
      <div id="container-1" className="flex-row">
        <div id="summary">
          <h1>Summary</h1>
        </div>
        <div id="model">
          <h1>Model</h1>
        </div>
      </div>
      <div id="container-2" className="flex-row">
        <div id="graph">
          <h1>Graph</h1>
        </div>
      </div>
    </div>
  );
}

export default App;
