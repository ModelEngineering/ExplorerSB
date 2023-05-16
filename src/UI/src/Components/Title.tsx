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
      <h3 id="subtitle-text">Project ID: {proj_id}</h3>
    </div>
  );
};

export default Title;
