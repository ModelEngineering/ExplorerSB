'use client'

import { useState, useEffect, useRef, useDeferredValue } from "react";
import SearchInput from "./searchbar/searchInput";
import SearchIndex from "./searchbar/searchIndex";

import SearchDisplay from "./searchbar/searchDisplay";
import useSearchFocus from "./searchbar/useSearchFocus";

const Searchbar = ({ landing = false }: { landing?: boolean }) => {
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
      className={"flex-col max-w-full w-[800px] z-10 gap-1 justify-start shrink min-w-[20%]" + (landing ? " landing-search" : "")}
    >
      <SearchInput setQuery={onQueryUpdate} query={query} numResults={results.length}/>
      <SearchIndex query={deferredQuery} setResult={setResults} />
      <SearchDisplay
        display={displayResults}
        query={query}
        results={results}
      />
    </div>
  );
};

export default Searchbar;
