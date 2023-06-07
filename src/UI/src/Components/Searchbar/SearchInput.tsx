import {
  BiSearchAlt as SearchIcon,
  BiXCircle as ClearIcon,
} from "react-icons/bi";

const SearchInput = ({
  setQuery,
  query,
  numResults,
}: {
  setQuery: Function;
  query: string;
  numResults: number;
}) => {
  return (
    <div
      id="searchbar-input-container"
      className="flex-row small-searchbar glassmorphism"
    >
      <SearchIcon id="search-icon" />
      <input
        id="searchbar-input"
        className="small-searchbar"
        placeholder="Type in keyword to search models (e.g. 'glucose', 'glycolysis', 'MAPK pathway')..."
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        onFocus={() => setQuery(query)}
      />
      <p id="num-results" className={query === "" ? "display-none" : ""}>
        {numResults} results
      </p>
      <ClearIcon
        id="clear-icon"
        className={query === "" ? "display-none" : ""}
        onClick={() => setQuery("")}
      />
    </div>
  );
};

export default SearchInput;
