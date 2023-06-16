import CodeBlock from "./CodeBlock";
const ModelDisplay = ({
  fileName,
  data
}: {
  fileName: string;
  data: string;
}) => {
  if(fileName.endsWith(".png") || fileName.endsWith(".jpg")) {
    return (
      <div id="model-file-container">
        <img src={data} alt={fileName} />
      </div>
    );
  } else if(fileName.endsWith(".ant")) {
    return (
    <div id="model-file-container">
      <CodeBlock codeString={data}/>
    </div>
    );
  }
}

export default ModelDisplay;