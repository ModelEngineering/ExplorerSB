import {BiLinkExternal as LinkIcon} from "react-icons/bi";

import "./CSS/Summary.css";
const Summary = ({ context }: { context: Context }) => {
  const abstract = context.abstract;
  const proj_id = context.project_id;
  let split = [""]
  if(abstract !== null) {
    split = abstract.split("\n\n");
  }
  return (
    <div id="summary-container" className="box-style glassmorphism flex-col">
      <h2>Summary</h2>
      <div id="summary-content">
        <h3>Citation</h3>
        {context.citation != null && (<p className="summary-citation">{context.citation}</p>)}
        {context.doi != null && (<p className="summary-doi">DOI: <a className="summary-url" href={"//doi.org/" + context.doi}>{context.doi} <LinkIcon className="external-icon"/></a></p>)}
        <h3>Abstract</h3>
        {split.map((paragraph, index) => (
          <p className="summary-abstract" key={index}>{paragraph}</p>
        ))}
        <h3>Associated Links</h3>
        {context.paper_url != null && (<p> <a className="summary-url" href={context.paper_url}>Link to Paper <LinkIcon className="external-icon"/></a></p>)}
        <p><a className="summary-url" href={`//api.biosimulations.org/projects/${proj_id}`}>Link to BioSimulations <LinkIcon className="external-icon"/></a></p> 
      </div>
    </div>
  );
};

export default Summary;
