import { Link } from "react-router-dom";

const SearchDisplay = ({
  display,
  results,
}: {
  display: boolean;
  results: ContextWithSnippets[];
}) => {
  return results.length != 0 ? (
    <div
      id="search-result-container"
      className={display ? "glassmorphism" : "display-none"}
    >
      {results.map((result, index) => {
        const text = result.snippet.split("**", 3);
        return (
          <Link
            key={result.runid}
            to={"/model/" + result.runid}
            style={{ textDecoration: "none" }}
          >
            <button
              className="search-result"
              style={index === 0 ? { borderTop: "0px" } : {}}
            >
              <p>
                Title:{" "}
                {result.title !== null ? result.title : "<Title Missing>"}
              </p>
              <p>
                Snippet: {text[0]} <b className="snippet-match">{text[1]}</b>{" "}
                {text[2]}
              </p>
            </button>
          </Link>
        );
      })}
    </div>
  ) : (
    <></>
  );
};

export default SearchDisplay;
