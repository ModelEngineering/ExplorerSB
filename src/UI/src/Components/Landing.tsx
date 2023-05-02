
import Searchbar from "./Searchbar";

const Landing = ({setResult}: {setResult(value:string): void}) => {
  return (
    <div id="landing" className="flex-col">
      <h1>ExplorerSB</h1>
      <Searchbar setResult={setResult}/>
    </div>
  )
}


export default Landing;
