import Searchbar from "@/components/searchbar";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-normal gap-10 px-6 py-12 md:p-16 lg:p-24">
      <h1 className="flex shrink-0 self-center px-1 text-center text-3xl font-bold text-inherit decoration-inherit md:text-4xl lg:text-5xl">
        Reproducibility Portal
      </h1>
      <Searchbar landing={true} />
    </main>
  );
}
