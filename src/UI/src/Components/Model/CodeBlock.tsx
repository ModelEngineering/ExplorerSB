import SyntaxHighlighter from 'react-syntax-highlighter';
import { vscDarkPlus as stylesheet } from "react-syntax-highlighter/dist/esm/styles/prism";

const CodeBlock = ({codeString} : {codeString : string}) => {
  return (
    <SyntaxHighlighter language="markup" style={stylesheet} showLineNumbers={true}>
      {codeString}
    </SyntaxHighlighter>
  );
};

export default CodeBlock;