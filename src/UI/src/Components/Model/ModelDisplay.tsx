import CodeBlock from "./CodeBlock";
import ImageDisplay from "./ImageDisplay";
const ModelDisplay = ({
  fileName,
  data
}: {
  fileName: string;
  data: string;
}) => {
  return (
    <div id="model-file-container">
      {fileName.endsWith(".png") || fileName.endsWith(".jpg") && data !== null ? (<ImageDisplay fileName={fileName} data={data}/>) : (<></>)}
      {fileName.endsWith(".ant") && data !== null ? (<CodeBlock codeString={data}/>) : (<></>)}
    </div>
  )
}

export default ModelDisplay;