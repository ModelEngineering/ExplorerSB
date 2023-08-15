const Title = ({
  title,
  proj_id,
}: {
  title: string | null;
  proj_id: string;
}) => {
  return (
    <section id="title" className="glassmorphism flex flex-col p-4 w-full">
      <h2 id="title-text" className="font-semibold">Title: {title !== null ? title : "N/A"}</h2>
      <h3 id="subtitle-text" className="italic break-words font-normal">Project ID: {proj_id}</h3>
    </section>
  );
};

export default Title;
