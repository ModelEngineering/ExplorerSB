'use client';
import Header from "@/components/header";
import Title from "@/components/title";
import Footer from "@/components/footer";
import Visualization from "@/components/visualization";
import Viewer from "@/components/viewer";
import Summary from "@/components/summary";
import notFound from "@/app/not-found";
import { useEffect, useState } from "react";

export default function Results({ runid }: { runid: string }) {
  const [result, setResult] = useState<Context>();
  const [loading, setLoading] = useState<boolean>(true);
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
  
  if (result === undefined) {
    notFound();
  } else {
    return ( loading ? <div>Loading... </div> :
      <div className="flex flex-col m-4 gap-4">
        <Header / >
        <Title title={result.title} proj_id={result.project_id}/>
        <div id="summary-model-container" className="flex flex-col lg:flex-row gap-4">
          <Summary context={result}/>
          <Viewer runid={runid}/>
        </div>
        <Visualization runid={runid}/>
        <div id="footer" className="flex-row">
          <Footer />
        </div>
      </div>
    )
  }
}