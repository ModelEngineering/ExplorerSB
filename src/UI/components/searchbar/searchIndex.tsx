import { useMemo, useEffect, useState } from "react";
import lunr from "lunr";

// Define an object to store data fields for search results
const store: Record<string, Context> = {};

// Create a lunr index for searching data
const createIndex = (data: Context[]) =>
  lunr(function () {
    this.field("title");
    this.field("abstract");
    this.field("citation");
    this.ref("runid");
    this.metadataWhitelist = ["position"];

    // Add data entries to the index
    for (let entry = 0; entry < data.length; entry++) {
      let dataResult = data[entry] as Context;
      store[dataResult.runid] = dataResult; // Store the data for reference
      this.add(dataResult);
    }
  });

// Define the SearchIndex component
const SearchIndex = ({
  query,
  setResult,
}: {
  query: string;
  setResult: Function;
}) => {
  const [data, setData] = useState<Context[]>([]);

  // Fetch context data on component mount
  useEffect(() => {
    const getDirectory = async () => {
      const response = await fetch(`/context.json`)
        .then((response) => response.json())
        .then((v) => v)
        .catch((err) => console.log(err));
      return response;
    };
    getDirectory().then((context: Context[]) => {
      setData(context);
    });
  }, []);

  // Create a lunr index when the data changes
  const index = useMemo(() => createIndex(data), [data]);

  // Perform search and generate search results
  useEffect(() => {
    if (query === "") {
      setResult([]);
      return;
    }

    let results;
    try {
      // Search the index for results
      results = index.search(query);

      // Filter and process results
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

            // Add highlight markers to the snippet
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

            // Extract a snippet with context around the match
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
  }, [query, index, setResult]);

  return <></>; // Return an empty fragment
};

export default SearchIndex; // Export the SearchIndex component
