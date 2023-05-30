import Searchbar from "./Searchbar";

const Landing = () => {
  return (
    <div id="landing" className="flex-col">
      <h1 id="logo">Reproducibility Portal</h1>
      <Searchbar landing={true}/>
    </div>
  );
};

export default Landing;
