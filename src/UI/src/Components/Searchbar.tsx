import { useState } from "react"
import { useLunr } from 'react-lunr'
import json from '../Assets/context.json'
import lunr from "lunr"
import { Formik, Form, Field } from "formik";

const data = json;
interface SearchResult {
  title: string | null,
  abstract: string,
  runid: string
  id: number
}
const store : Record<string, SearchResult> = {};
const index = lunr(function () {
  this.field("title");
  this.field("abstract");
  this.field("project_id");
  this.field("runid");
  this.ref("id");

  for (let entry = 0; entry < data.length; entry++) {
    this.add({
      title: data[entry].title,
      abstract: data[entry].abstract,
      project_id: data[entry].project_id,
      runid: data[entry].runid,
      id: entry
    });
    console.log(data)

    store[entry] = {
      title: data[entry].title,
      abstract: data[entry].abstract,
      // project_id: data[entry].project_id,
      runid: data[entry].runid,
      id: entry
    };
  }
});
const Searchbar = () => {
  const [query, setQuery] = useState("");
  const results = useLunr(query, index, store);
  console.log(results)
  return (
    <div id="searchbar">
      <Formik
        initialValues={{ query: '' }}
        onSubmit={(values, { setSubmitting }) => {
          setQuery(values.query)
          setSubmitting(false)
        }}
      >
        <Form>
          <Field name="query" />
        </Form>
      </Formik>
    </div>
  )
}

export default Searchbar;
