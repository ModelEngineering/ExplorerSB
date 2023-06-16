import SyntaxHighlighter from 'react-syntax-highlighter';
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

const CodeBlock = ({codeString} : {codeString : string}) => {
  return (
    <SyntaxHighlighter language="javascript" style={vscDarkPlus} showLineNumbers={true}>
      {codeString}
    </SyntaxHighlighter>
  );
};

export default CodeBlock;