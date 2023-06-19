import CodeBlock from "./CodeBlock";
const ModelDisplay = ({
  fileName,
  data
}: {
  fileName: string;
  data: string;
}) => {
  return (
    <div id="model-file-container">
      {fileName.endsWith(".png") || fileName.endsWith(".jpg") && data !== null ? (<img src={data} alt={fileName} />) : (<></>)}
      {fileName.endsWith(".ant") && data !== null ? (<CodeBlock codeString={data}/>) : (<></>)}
    </div>
  )
}

export default ModelDisplay;