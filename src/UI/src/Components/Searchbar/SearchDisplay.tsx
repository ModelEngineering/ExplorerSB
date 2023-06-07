import { Link } from "react-router-dom";

const SearchDisplay = ({
  display,
  query,
  results,
}: {
  display: boolean;
  query: string;
  results: ContextWithSnippets[];
}) => {
  if (query === ""){
    return <></>;
  }
  return (
    <div
      id="search-result-container"
      className={display ? "glassmorphism" : "display-none"}
    >
    {results.length != 0 ? (
      results.map((result, index) => {
        let text = null;
        if (result.snippet !== undefined){
          text = result.snippet.split("**", 3);
        }
        return (
          <Link
            key={result.runid !== undefined ? result.runid : 0}
            to={result.runid !== undefined ? "/model/" + result.runid : "/"}
            style={{ textDecoration: "none" }}
          >
            <button
              className="search-result"
              style={index === 0 ? { borderTop: "0px" } : {}}
            >
              <p className="search-result-title">
                {result.title !== null ? result.title : "<Title Missing>"}
              </p>
              {text !== null ? (
              <p className="search-result-snippet">
                {text[0]} <b className="search-snippet-highlight">{text[1]}</b>{" "}
                {text[2]} 
              </p>) : <></>}
            </button>
          </Link>
        );
      })
      ) : (
        <button
          className="search-result"
          style={{borderTop: "0px"}}
        >
          <p className="search-result-title">
            No Results Found
          </p>
        </button>
    )}
    </div>)
  ;
};

export default SearchDisplay;
