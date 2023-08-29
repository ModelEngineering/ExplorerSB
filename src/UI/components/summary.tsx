import { BiLinkExternal as LinkIcon } from "react-icons/bi";

// This component displays the summary section of the results page
const Summary = ({ context }: { context: Context }) => {
  const abstract = context.abstract;
  const proj_id = context.project_id;
  let split = [""];

  // Split the abstract into paragraphs
  if (abstract !== null) {
    split = abstract.split("\n\n");
  }

  return (
    <div
      id="summary-container"
      className="glassmorphism flex max-h-[500px] flex-col p-4 lg:h-[500px] lg:w-1/2"
    >
      {/* Display the summary title */}
      <h2 className="font-bold">Summary</h2>

      {/* Display the summary content */}
      <div
        id="summary-content"
        className="styled-scrollbar flex flex-col gap-1 overflow-y-auto"
      >
        {/* Display the citation */}
        <h3 className="font-semibold">Citation</h3>
        {context.citation !== null && (
          <p className="summary-citation">{context.citation}</p>
        )}

        {/* Display the DOI */}
        {context.doi !== null && (
          <a className="flex" href={"//doi.org/" + context.doi}>
            DOI: {context.doi} <LinkIcon className="text-base" />
          </a>
        )}

        {/* Display the abstract */}
        <h3 className="font-semibold">Abstract</h3>
        {split.map((paragraph, index) => (
          <p className="summary-abstract" key={index}>
            {paragraph}
          </p>
        ))}

        {/* Display the associated links */}
        <h3 className="font-semibold">Associated Links</h3>
        {context.paper_url !== null && (
          <a className="flex" href={context.paper_url}>
            Link to Paper <LinkIcon className="text-base" />
          </a>
        )}
        <a
          className="flex"
          href={`//api.biosimulations.org/projects/${proj_id}`}
        >
          Link to BioSimulations <LinkIcon className="text-base" />
        </a>
      </div>
    </div>
  );
};

export default Summary;