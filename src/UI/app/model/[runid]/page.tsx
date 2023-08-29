import Results from "@/components/results";

// Define the runtime environment as 'edge'
export const runtime = 'edge';

// Define the default function component named "Model"
export default function Model({ params }: { params: { runid: string } }) {
  // Render the Results component with the "runid" parameter passed
  return <Results runid={params.runid} />;
}