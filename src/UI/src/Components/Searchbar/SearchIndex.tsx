import { useMemo } from 'react'
import lunr from "lunr"
// allows us to store the data fields we want the search to return
const store : Record<string, Context> = {};

// the lunr index, which indexes the data and allows us to search through it
const createIndex = (data: Context[]) => lunr(function () {
  this.field("title");
  this.field("abstract");
  this.ref("runid");
  this.metadataWhitelist = ['position']

  for (let entry = 0; entry < data.length; entry++) {
    let dataResult = data[entry] as Context;
    store[dataResult.runid] = dataResult;
    this.add(dataResult);
  }
});

const SearchIndex = ({data, query, setResult}: {data : Context[], query: string, setResult: Function}) => {
  const index = useMemo(() => createIndex(data), []);
  useMemo(() => 
  {
    if (query === "") {
      setResult([]);
      return;
    }
    let results = index.search(query)

    setResult(results.map((result) => store[result.ref]));

    console.log(results);
  }, [query])

  return (<></>);
}

export default SearchIndex;