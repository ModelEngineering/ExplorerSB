import { useState, useRef } from "react";
import SearchInput from "./Searchbar/SearchInput";
import SearchIndex from "./Searchbar/SearchIndex";

import contextJson from "../Assets/context.json";
import SearchDisplay from "./Searchbar/SearchDisplay";
import useSearchFocus from "./Searchbar/useSearchFocus";
const data = contextJson;

const Searchbar = ({ setSelected }: { setSelected: Function }) => {
  const [query, setQuery] = useState<string>("");
  const [results, setResults] = useState<Context[]>([]);
  const [displayResults, setDisplayResults] = useState<boolean>(false);
  const ref = useRef<HTMLDivElement>(null);
  useSearchFocus(ref, setDisplayResults);

  const onQueryUpdate = (query: string) => {
    setQuery(query);
    setDisplayResults(true);
  }

  const onResultSelect = (result: Context) => {
    setSelected(result);
    setDisplayResults(false);
  }

  return (
    <div
      ref={ref}
      id="searchbar"
      className="flex-col"
    >
      <SearchInput setQuery={onQueryUpdate} query={query} />
      <SearchIndex data={data} query={query} setResult={setResults} />
      <SearchDisplay
        display={displayResults}
        results={results}
        setSelected={onResultSelect}
      />
    </div>
  );
};

export default Searchbar;
