import { useState } from "react";
import SyntaxHighlighter from "react-syntax-highlighter";
import { vscDarkPlus as stylesheet } from "react-syntax-highlighter/dist/cjs/styles/prism";
import { BiCopy as CopyIcon, BiCheck as CheckIcon } from "react-icons/bi";
import { CopyToClipboard } from "react-copy-to-clipboard";
import { Roboto_Mono } from "next/font/google";

// The CodeBlock component is used to display code
// It uses the react-syntax-highlighter library to display the code
// It uses the react-copy-to-clipboard library to allow the user to copy the code to their clipboard
// It takes in the code string as a prop
// It renders the code string in a code block
// It also allows the user to copy the code to their clipboard with a button
// It displays a check mark for 2.5 seconds when the code is copied

const roboto_mono = Roboto_Mono({ subsets: ["latin"] });

const CodeBlock = ({ codeString }: { codeString: string }) => {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    setCopied(true);
    setTimeout(() => {
      setCopied(false);
    }, 2500);
  };
  return (
    <div className="relative">
      <CopyToClipboard text={codeString} onCopy={copy}>
        <button className="absolute right-0 top-0 m-4 hidden rounded-md border-2 border-slate-700 bg-slate-700 bg-opacity-50 px-4 py-2 text-white hover:border-slate-600 hover:bg-opacity-70 group-hover:block">
          {copied ? <CheckIcon /> : <CopyIcon />}
        </button>
      </CopyToClipboard>
      <SyntaxHighlighter
        codeTagProps={{ className: roboto_mono.className }}
        language="markup"
        style={stylesheet}
        showLineNumbers={true}
        customStyle={{ margin: "0"}}
        lineNumberContainerStyle={{ minWidth: "4.25em" }}
      >
        {codeString}
      </SyntaxHighlighter>
    </div>
  );
};

export default CodeBlock;
