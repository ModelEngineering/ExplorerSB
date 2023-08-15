import Link from "next/link";
import Searchbar from "./searchbar";

const Header = () => {
  return (
    <header id="header" className="flex flex-col gap-4 z-10 justify-start items-start w-full h-26 md:h-14 md:flex-row md:justify-between">
      <Link id="logo" href="/" className="flex shrink-0 font-bold text-2xl self-center md:text-3xl no-underline text-black bg-sky-300 p-2 rounded-md bg-opacity-20">
        Reproducibility Portal
      </Link>
      <Searchbar />
    </header>
  );
};

export default Header;
