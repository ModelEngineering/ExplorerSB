import { Link } from "react-router-dom";
import Searchbar from "./Searchbar";

import "./CSS/Header.css";

const Header = () => {
  return (
    <div id="header" className="flex-row">
      <Link id="logo" to="/">
        <p>
          Reproducibility Portal
        </p>
      </Link>
      <Searchbar />
    </div>
  );
};

export default Header;
