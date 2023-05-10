import { BiSearchAlt as SearchIcon } from "react-icons/bi"

const SearchInput = ({setQuery}: {setQuery: Function}) => {

  return (
    <div id="searchbar-input-container" className="flex-row small-searchbar glassmorphism" >
      <SearchIcon id="search-icon" />
      <input id="searchbar-input" className="small-searchbar" placeholder="Search..." onChange={(event) => setQuery(event.target.value)}/>
    </div>
  )

}

export default SearchInput;