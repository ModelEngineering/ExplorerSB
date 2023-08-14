import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center w-screen h-screen gap-8 md:gap-12">
      <div className="flex flex-col items-center justify-center gap-2 md:gap-4">
      <h2 className="text-3xl md:text-5xl">Page Not Found</h2>
      <p className="text-sm md:text-base">Could not find requested resource</p>
      </div>
      <button className="p-2 border-2 rounded-lg text-sm bg-sky-100 border-sky-200 md:p-3 md:text-base">
        <Link href="/">Back to Main page</Link>
      </button>
    </div>
  )
}