"use client";
import Header from "@/components/header";
import Title from "@/components/title";
import Footer from "@/components/footer";
import Visualization from "@/components/visualization";
import Viewer from "@/components/viewer";
import Summary from "@/components/summary";
import notFound from "@/app/not-found";
import { useEffect, useState } from "react";

// This component displays the results of a single run
export default function Results({ runid }: { runid: string }) {
  const [result, setResult] = useState<Context>();
  const [loading, setLoading] = useState<boolean>(true);

  // Fetch the context data for the run ID
  useEffect(() => {
    const getDirectory = async () => {
      const response = await fetch(`/context.json`)
        .then((response) => response.json())
        .then((v) => v)
        .catch((err) => console.log(err));
      return response;
    };
    getDirectory().then((dirData: Context[]) => {
      for (let entry = 0; entry < dirData.length; entry++) {
        let dataResult = dirData[entry] as Context;
        if (dataResult.runid === runid) {
          setResult(dataResult);
          setLoading(false);
          break;
        }
      }
    });
  }, [runid, setResult]);

  // Display the results if they exist, otherwise display a "not found" message
  if (result === undefined) {
    notFound();
  } else {
    return (
      loading ? <div>Loading... </div> :
      <div className="flex flex-col gap-4 p-4 w-full items-center">
        {/* Display the header */}
        <Header / >
        {/* Display the title */}
        <Title title={result.title} proj_id={result.project_id}/>
        {/* Display the summary and viewer */}
        <section id="summary-model-container" className="flex flex-col lg:flex-row gap-4 w-full">
          <Summary context={result}/>
          <Viewer runid={runid}/>
        </section>
        {/* Display the visualization */}
        <Visualization runid={runid}/>
        {/* Display the footer */}
        <footer id="footer" className="flex-row]">
          <Footer />
        </footer>
      </div>
    )
  }
}