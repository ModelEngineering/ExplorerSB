import CodeBlock from "./CodeBlock";
import ImageDisplay from "./ImageDisplay";

// The ModelDisplay component is used to display the model file
// It wraps the ImageDisplay and CodeBlock components
// It takes in the file name and the binary blob data of the file as props
// It renders the ImageDisplay component if the file is an image
// It renders the CodeBlock component if the file is an ant file
// It renders nothing if the file is not an image or an ant file

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