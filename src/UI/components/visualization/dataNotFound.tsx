import { DisplayMode } from "../visualization";

const DataNotFound = ({displayMode} : {displayMode: DisplayMode}) => {
  return (
    <div id="notfound-container" className={"w-full" + (displayMode === DisplayMode.None ? "" : " hidden")}>
      {displayMode === DisplayMode.None ? <h3>Data not found!</h3> : <></>}
    </div>
  )
}

export default DataNotFound;