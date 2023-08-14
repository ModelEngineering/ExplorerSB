import Results from "@/components/results";

export const runtime = 'edge';

export default function Model({ params }: { params: { runid: string } }) {
  return <Results runid={params.runid} />;
}