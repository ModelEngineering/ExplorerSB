import {
  BiSearchAlt as SearchIcon,
  BiXCircle as ClearIcon,
} from "react-icons/bi";

// Define the SearchInput component
const SearchInput = ({
  setQuery,
  query,
  numResults,
}: {
  setQuery: Function; // Function to update the search query state
  query: string; // Current search query
  numResults: number; // Number of search results
}) => {
  return (
    <div
      id="searchbar-input-container"
      className="glassmorphism flex h-[55px] w-full flex-shrink-0 flex-row items-center justify-start gap-2 rounded-none border-0 px-4 text-black"
    >
      {/* Search Icon */}
      <SearchIcon id="search-icon" className="flex-shrink-0 text-2xl" />

      {/* Input field for search */}
      <input
        id="searchbar-input"
        className="h-full w-full flex-grow border-0 bg-transparent text-black placeholder-slate-500 focus:outline-none"
        placeholder="Type in keyword to search models (e.g. 'glucose', 'glycolysis', 'MAPK pathway')..."
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        onFocus={() => setQuery(query)} // Restore query when input is focused
      />

      {/* Display number of results */}
      <p
        id="num-results"
        className={
          "margin-0 self-center justify-self-end whitespace-nowrap px-4" +
          (query === "" ? " hidden" : "")
        }
      >
        {numResults} results
      </p>

      {/* Clear Icon to reset the search query */}
      <ClearIcon
        id="clear-icon"
        className={
          "flex-shrink-0 cursor-pointer text-2xl text-black" +
          (query === "" ? " hidden" : "")
        }
        onClick={() => setQuery("")} // Clear the search query when clicked
      />
    </div>
  );
};

export default SearchInput; // Export the SearchInput component
