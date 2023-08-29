import { DisplayMode } from "../visualization";

// Define the DataNotFound component
const DataNotFound = ({ displayMode }: { displayMode: DisplayMode }) => {
  // This component is meant to display a message when data is not found.
  // It takes the 'displayMode' prop to determine whether to show the message or not.

  return (
    <div
      id="notfound-container"
      className={"w-full" + (displayMode === DisplayMode.None ? "" : " hidden")}
    >
      {/* Display the "Data not found!" message if displayMode is set to None */}
      {displayMode === DisplayMode.None ? <h3>Data not found!</h3> : <></>}
    </div>
  );
};

export default DataNotFound; // Export the DataNotFound component
