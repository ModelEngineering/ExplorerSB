import { useState } from "react";
import SyntaxHighlighter from "react-syntax-highlighter";
import { vscDarkPlus as stylesheet } from "react-syntax-highlighter/dist/cjs/styles/prism";
import { BiCopy as CopyIcon, BiCheck as CheckIcon } from "react-icons/bi";
import { CopyToClipboard } from "react-copy-to-clipboard";
import { Roboto_Mono } from "next/font/google";

// Load the Roboto Mono font subset for Latin characters
const roboto_mono = Roboto_Mono({ subsets: ["latin"] });

// Define the CodeBlock component
const CodeBlock = ({ codeString }: { codeString: string }) => {
  const [copied, setCopied] = useState(false);

  // Function to handle copying to clipboard
  const copy = () => {
    setCopied(true);
    setTimeout(() => {
      setCopied(false);
    }, 2500);
  };

  return (
    <div className="relative">
      {/* Button for copying code to clipboard */}
      <CopyToClipboard text={codeString} onCopy={copy}>
        <button className="absolute right-0 top-0 m-4 hidden rounded-md border-2 border-slate-700 bg-slate-700 bg-opacity-50 px-4 py-2 text-white hover:border-slate-600 hover:bg-opacity-70 group-hover:block">
          {copied ? <CheckIcon /> : <CopyIcon />}
        </button>
      </CopyToClipboard>

      {/* SyntaxHighlighter component for code display */}
      <SyntaxHighlighter
        codeTagProps={{ className: roboto_mono.className }} // Apply the font to the code
        language="markup" // Specify the code language (markup syntax highlighting)
        style={stylesheet} // Apply the selected code highlighting style
        showLineNumbers={true} // Show line numbers
        customStyle={{ margin: "0" }} // Apply custom styling to the syntax highlighter
        lineNumberContainerStyle={{ minWidth: "4.25em" }} // Styling for line number container
      >
        {codeString} {/* Display the code content */}
      </SyntaxHighlighter>
    </div>
  );
};

export default CodeBlock; // Export the CodeBlock component
