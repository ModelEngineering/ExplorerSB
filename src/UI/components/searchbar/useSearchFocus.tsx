import { Dispatch, RefObject, SetStateAction, useEffect } from "react";

const useSearchFocus = (
  ref: RefObject<HTMLDivElement>,
  setDropdownVisibility: Dispatch<SetStateAction<boolean>>
) => {
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setDropdownVisibility(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [ref, setDropdownVisibility]);
};

export default useSearchFocus;