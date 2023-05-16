import { useState } from "react";
import SearchInput from "./Searchbar/SearchInput";
import SearchIndex from "./Searchbar/SearchIndex";

import contextJson from "../Assets/context.json";
import SearchDisplay from "./Searchbar/SearchDisplay";
const data = contextJson;

const Searchbar = ({ setSelected }: { setSelected: Function }) => {
  const [query, setQuery] = useState<string>("");
  const [results, setResults] = useState<Context[]>([]);
  const [displayResults, setDisplayResults] = useState<boolean>(false);

  return (
    <div id="searchbar" className="flex-col">
      <SearchInput
        setQuery={setQuery}
        onFocus={() => setDisplayResults(true)}
        onBlur={() => setDisplayResults(false)}
        query={query}
      />
      <SearchIndex data={data} query={query} setResult={setResults} />
      <SearchDisplay
        display={displayResults}
        results={results}
        setSelected={setSelected}
      />
    </div>
  );
};

export default Searchbar;
