
import Searchbar from "./Searchbar";

const Landing = ({setResult}: {setResult(value:SearchResult): void}) => {
  return (
    <div id="landing" className="flex-col">
      <h1 id="logo">ExplorerSB</h1>
      <Searchbar setResult={setResult}/>
    </div>
  )
}


export default Landing;
