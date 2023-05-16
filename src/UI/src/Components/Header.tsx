import Searchbar from "./Searchbar";

const Header = ({
  setSelected,
}: {
  setSelected(value: Context | undefined): void;
}) => {
  return (
    <div id="header" className="flex-row">
      <h1 id="logo" onClick={() => setSelected(undefined)}>
        Reproducibility Portal
      </h1>
      <Searchbar setSelected={setSelected} />
    </div>
  );
};

export default Header;
