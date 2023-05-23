import Searchbar from "./Searchbar";

const Landing = ({ setSelected }: { setSelected(value: Context): void }) => {
  return (
    <div id="landing" className="flex-col">
      <h1 id="logo">Reproducibility Portal</h1>
      <Searchbar setSelected={setSelected} landing={true}/>
    </div>
  );
};

export default Landing;
