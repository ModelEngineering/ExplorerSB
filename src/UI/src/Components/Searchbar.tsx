import { useState, useRef, useDeferredValue } from "react";
import SearchInput from "./Searchbar/SearchInput";
import SearchIndex from "./Searchbar/SearchIndex";

import contextJson from "../Assets/context.json";
import SearchDisplay from "./Searchbar/SearchDisplay";
import useSearchFocus from "./Searchbar/useSearchFocus";
const data = contextJson;

const Searchbar = ({ landing }: { landing?: boolean}) => {
  const [query, setQuery] = useState<string>("");
  const [results, setResults] = useState<ContextWithSnippets[]>([]);
  const [displayResults, setDisplayResults] = useState<boolean>(false);
  const ref = useRef<HTMLDivElement>(null);
  const deferredQuery = useDeferredValue(query);
  useSearchFocus(ref, setDisplayResults);

  const onQueryUpdate = (query: string) => {
    setQuery(query);
    setDisplayResults(true);
  }
  
  return (
    <div
      ref={ref}
      id="searchbar"
      className={landing ? "flex-col landing-search" : "flex-col"}
    >
      <SearchInput setQuery={onQueryUpdate} query={query} numResults={results.length}/>
      <SearchIndex data={data} query={deferredQuery} setResult={setResults} />
      <SearchDisplay
        display={displayResults}
        query={query}
        results={results}
      />
    </div>
  );
};

export default Searchbar;
