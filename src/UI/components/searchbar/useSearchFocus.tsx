import { Dispatch, RefObject, SetStateAction, useEffect } from "react";

// Custom hook for managing search focus and dropdown visibility
const useSearchFocus = (
  ref: RefObject<HTMLDivElement>, // Reference to the search component
  setDropdownVisibility: Dispatch<SetStateAction<boolean>> // State setter for dropdown visibility
) => {
  useEffect(() => {
    // Event listener to handle clicks outside the search component
    const handleClickOutside = (event: MouseEvent) => {
      // Close the dropdown if a click is detected outside the search component
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setDropdownVisibility(false);
      }
    };

    // Add event listener when the component mounts
    document.addEventListener("mousedown", handleClickOutside);

    // Remove the event listener when the component unmounts
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [ref, setDropdownVisibility]); // Re-run the effect if the ref or dropdown visibility changes
};

export default useSearchFocus; // Export the custom hook
