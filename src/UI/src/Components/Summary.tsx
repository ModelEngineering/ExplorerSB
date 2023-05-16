const Summary = ({ summary }: { summary: string }) => {
  let split = summary.split("\n\n");
  return (
    <div id="summary-container" className="box-style glassmorphism flex-col">
      <h2>Summary</h2>
      <div id="summary-content">
        
        {split.map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>
    </div>
  );
};

export default Summary;
