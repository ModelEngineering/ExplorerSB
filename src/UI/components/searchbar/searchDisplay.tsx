import Link from "next/link";

const SearchDisplay = ({
  display,
  query,
  results,
}: {
  display: boolean;
  query: string;
  results: ContextWithSnippets[];
}) => {
  if (query === "") {
    return <></>;
  }
  return (
    <div
      id="search-result-container"
      className={
        "styled-scrollbar z-10 max-h-[50vh] overflow-hidden overflow-y-auto" +
        (display ? " glassmorphism" : " hidden")
      }
    >
      {results.length != 0 ? (
        results.map((result, index) => {
          let text = null;
          if (result.snippet !== undefined) {
            text = result.snippet.split("**", 3);
          }
          return (
            <Link
              key={result.runid !== undefined ? result.runid : 0}
              href={result.runid !== undefined ? "/model/" + result.runid : "/"}
              className="w-fit h-fit"
              style={{ textDecoration: "none" }}
            >
              <div
                className="background-transparent z-10 w-full rounded-none border-0 border-t-2 border-t-slate-500 p-3 lg:p-4 text-left text-black hover:bg-sky-200 hover:border-t-2 focus:bg-sky-200 focus:border-t-2 [&>p]:overflow-hidden [&>p]:text-ellipsis [&>p]:whitespace-nowrap"
                style={index === 0 ? { borderTop: "0px" } : {}}
              >
                <p className="font-bold">
                  {result.title !== null ? result.title : "<Title Missing>"}
                </p>
                {text !== null ? (
                  <p className="italic text-gray-500">
                    {text[0]}{" "}
                    <b className="text-black font-medium">{text[1]}</b>{" "}
                    {text[2]}
                  </p>
                ) : (
                  <></>
                )}
              </div>
            </Link>
          );
        })
      ) : (
        <button className="background-transparent z-10 w-full rounded-none border-0 border-t-2 border-t-slate-500 p-3 lg:p-4 text-left text-black hover:bg-sky-200 hover:border-t-2 focus:bg-sky-200 focus:border-t-2 [&>p]:overflow-hidden [&>p]:text-ellipsis [&>p]:whitespace-nowrap"
        style={{ borderTop: "0px" }}>
          <p className="font-bold">No Results Found</p>
        </button>
      )}
    </div>
  );
};

export default SearchDisplay;
