
import Searchbar from "./Searchbar";

const Landing = ({setSelected}: {setSelected(value:SearchResult): void}) => {
  return (
    <div id="landing" className="flex-col">
      <h1 id="logo">ExplorerSB</h1>
      <Searchbar setSelected={setSelected}/>
    </div>
  )
}


export default Landing;
