import {
  BiSearchAlt as SearchIcon,
  BiXCircle as ClearIcon,
} from "react-icons/bi";

const SearchInput = ({
  setQuery,
  query,
}: {
  setQuery: Function;
  query: string;
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
        placeholder="Search..."
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        onFocus={() => setQuery(query)}
      />
      <ClearIcon
        id="clear-icon"
        className={query === "" && "display-none"}
        onClick={() => setQuery("")}
      />
    </div>
  );
};

export default SearchInput;
