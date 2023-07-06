import { useState } from "react";
import SyntaxHighlighter from "react-syntax-highlighter";
import { vscDarkPlus as stylesheet } from "react-syntax-highlighter/dist/esm/styles/prism";
import { BiCopy as CopyIcon, BiCheck as CheckIcon } from "react-icons/bi";
import { CopyToClipboard } from "react-copy-to-clipboard";

// The CodeBlock component is used to display code
// It uses the react-syntax-highlighter library to display the code
// It uses the react-copy-to-clipboard library to allow the user to copy the code to their clipboard
// It takes in the code string as a prop
// It renders the code string in a code block
// It also allows the user to copy the code to their clipboard with a button
// It displays a check mark for 2.5 seconds when the code is copied

const CodeBlock = ({ codeString }: { codeString: string }) => {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    setCopied(true);
    setTimeout(() => {
      setCopied(false);
    }, 2500);
  };
  return (
    <div style={{position: "relative"}}>
      <CopyToClipboard text={codeString} onCopy={copy}>
        <button className="copy-button">{copied ? <CheckIcon /> : <CopyIcon />}</button>
      </CopyToClipboard>
      <SyntaxHighlighter
        language="markup"
        style={stylesheet}
        showLineNumbers={true}
        customStyle={{margin: "0"}}
      >
        {codeString}
      </SyntaxHighlighter>
    </div>
  );
};

export default CodeBlock;
