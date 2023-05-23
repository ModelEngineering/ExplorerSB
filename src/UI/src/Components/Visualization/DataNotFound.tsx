import { DisplayMode } from "../Visualization";

const DataNotFound = ({displayMode} : {displayMode: DisplayMode}) => {
  return (
    <div id="notfound-container" className={displayMode === DisplayMode.None ? "" : "hidden"}>
      {displayMode === DisplayMode.None ? <h3>Data not found!</h3> : <></>}
    </div>
  )
}

export default DataNotFound;