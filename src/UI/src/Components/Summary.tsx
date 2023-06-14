const Summary = ({ context }: { context: Context }) => {
  const abstract = context.abstract;
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
        {context.doi != null && (<p className="summary-doi">DOI: <a className="summary-url" href={"//doi.org/" + context.doi}>{context.doi}</a></p>)}
        <h3>Abstract</h3>
        {split.map((paragraph, index) => (
          <p className="summary-abstract" key={index}>{paragraph}</p>
        ))}
        <h3>URL</h3>
        {context.paper_url != null && (<a className="summary-url" href={context.paper_url}>{context.paper_url}</a>)}
      </div>
    </div>
  );
};

export default Summary;
