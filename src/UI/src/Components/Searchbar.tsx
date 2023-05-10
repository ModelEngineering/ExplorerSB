import { useState } from "react"
import SearchInput from "./Searchbar/SearchInput"
import SearchIndex from "./Searchbar/SearchIndex"

import contextJson from '../Assets/context.json'
import SearchDisplay from "./Searchbar/SearchDisplay";
const data = contextJson;


const Searchbar = ({setSelected} : {setSelected : Function}) => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  
  return (
    <div id="searchbar" className="flex-col">
      <SearchInput setQuery={setQuery}/>
      <SearchIndex data={data} query={query} setResult={setResults}/>
      <SearchDisplay results={results} setSelected={setSelected}/>
    </div>
  )
}

export default Searchbar;
