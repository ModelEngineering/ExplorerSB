import { useLunr } from 'react-lunr'
import { useMemo } from 'react'
import lunr from "lunr"
// allows us to store the data fields we want the search to return
const store : Record<string, SearchResult> = {};

// the lunr index, which indexes the data and allows us to search through it
const createIndex = (data: Context[]) => lunr(function () {
  this.field("title");
  this.field("abstract");
  this.ref("id");
  this.metadataWhitelist = ['position']

  for (let entry = 0; entry < data.length; entry++) {
    this.add({
      title: data[entry].title,
      abstract: data[entry].abstract,
      id: entry
    });

    store[entry] = {
      title: data[entry].title,
      abstract: data[entry].abstract,
      project_id: data[entry].project_id,
      runid: data[entry].runid,
      id: entry
    };
  }
});

const SearchIndex = ({data, query, setResult}: {data : Context[], query: string, setResult: Function}) => {
  const index = useMemo(() => createIndex(data), [data]);
  const results = useLunr(query, index, store) as SearchResult[];

  setResult(results);

  return (<></>);
}

export default SearchIndex;