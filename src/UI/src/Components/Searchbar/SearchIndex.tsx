import { useMemo, useEffect } from "react";
import lunr from "lunr";
// allows us to store the data fields we want the search to return
const store: Record<string, Context> = {};

// the lunr index, which indexes the data and allows us to search through it
const createIndex = (data: Context[]) =>
  lunr(function () {
    this.field("title");
    this.field("abstract");
    this.field("citation");
    this.ref("runid");
    this.metadataWhitelist = ["position"];

    for (let entry = 0; entry < data.length; entry++) {
      let dataResult = data[entry] as Context;
      store[dataResult.runid] = dataResult;
      this.add(dataResult);
    }
  });

const SearchIndex = ({
  data,
  query,
  setResult,
}: {
  data: Context[];
  query: string;
  setResult: Function;
}) => {
  const index = useMemo(() => createIndex(data), []);
  useEffect(() => {
    if (query === "") {
      setResult([]);
      return;
    }
    let results;
    try {
      results = index.search(query);
      setResult(
        results
          .filter((result) => result.score > 0.25)
          .map((result) => {
            let contextWithSnippets = store[result.ref] as ContextWithSnippets;
            let snippetRaw = Object.values(result.matchData.metadata)[0];
            let key = Object.keys(snippetRaw)[0];
            let contextKey = key as keyof ContextWithSnippets;
            const position = snippetRaw[key];
            const index = position.position[0][0];
            let length = position.position[0][1];
            let contextValue = contextWithSnippets[contextKey];
            if (contextValue === null) {
              return "";
            }
            contextValue =
              contextValue.slice(0, index) + "**" + contextValue.slice(index);
            length += 2;
            contextValue =
              contextValue.slice(0, index + length) +
              "**" +
              contextValue.slice(index + length);
            length += 2;
            const text = contextValue.substring(index - 40, index + length + 40);
            const startIndex = index - 40;
            const endIndex = index + length + 40;
            let textTrimmed = text
              .slice(text.indexOf(" "), text.lastIndexOf(" "))
              .trim();
            if (startIndex > 0) {
              textTrimmed = "..." + textTrimmed;
            }
            if (endIndex < contextValue.length) {
              textTrimmed = textTrimmed + "...";
            }
            contextWithSnippets.snippet = textTrimmed;
            return contextWithSnippets;
          })
      );
    } catch (e) {
      console.log(e);
      setResult([]);
    }
  }, [query]);

  return <></>;
};

export default SearchIndex;
