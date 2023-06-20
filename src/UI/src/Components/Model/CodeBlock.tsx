import { useState } from "react";
import SyntaxHighlighter from "react-syntax-highlighter";
import { vscDarkPlus as stylesheet } from "react-syntax-highlighter/dist/esm/styles/prism";
import { BiCopy as CopyIcon, BiCheck as CheckIcon } from "react-icons/bi";
import { CopyToClipboard } from "react-copy-to-clipboard";

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
