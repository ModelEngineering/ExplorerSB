import {BiLinkExternal as LinkIcon} from "react-icons/bi";

const Title = ({
  title,
  proj_id,
}: {
  title: string | null;
  proj_id: string;
}) => {
  return (
    <div id="title" className="glassmorphism flex-col container">
      <h2 id="title-text">Title: {title !== null ? title : "N/A"}</h2>
      <h3 id="subtitle-text">Project ID: <a href={`//api.biosimulations.org/projects/${proj_id}`} id="subtitle-text">{proj_id} <LinkIcon className="external-icon"/></a> </h3>
      
    </div>
  );
};

export default Title;
