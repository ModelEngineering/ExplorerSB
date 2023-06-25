import { Link } from "react-router-dom";
import Searchbar from "./Searchbar";

const Header = () => {
  return (
    <div id="header" className="flex-row">
      <Link to="/" style={{ textDecoration: "inherit", color: "inherit", flexShrink: 0 }}>
        <h1 id="logo">
          Reproducibility Portal
        </h1>
      </Link>
      <Searchbar />
    </div>
  );
};

export default Header;
