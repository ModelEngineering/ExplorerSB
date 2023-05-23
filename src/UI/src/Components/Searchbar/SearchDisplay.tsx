const SearchDisplay = ({
  display,
  results,
  setSelected,
}: {
  display: boolean;
  results: ContextWithSnippets[];
  setSelected: Function;
}) => {
  return results.length != 0 ? (
    <div
      id="search-result-container"
      className={display ? "glassmorphism" : "display-none"}
    >
      {results.map((result, index) => {
        const text = result.snippet.split("**", 3)
        return (<button
          className="search-result"
          key={result.runid}
          style={index === 0 ? { borderTop: "0px" } : {}}
          onClick={() => setSelected(result)}
          onKeyDown={(e) => {
            if (["Enter"].includes(e.code)) {
              setSelected(result);
            }
          }}
        >
          <p>Title: {result.title !== null ? result.title : "<Title Missing>"}</p>
          <p>Snippet: {text[0]} <b className="snippet-match">{text[1]}</b> {text[2]}</p>
        </button>)
      })}
    </div>
  ) : (
    <></>
  );
};

export default SearchDisplay;
