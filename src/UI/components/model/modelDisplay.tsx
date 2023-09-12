import CodeBlock from "./codeBlock";
import ImageDisplay from "./imageDisplay";

// Define the supported file types for code files
const SUPPORTED_FILE_TYPES = [".ant", ".m", ".py", ".jl", ".r", ".txt"];
// Define the supported image file types
const SUPPORTED_IMAGE_TYPES = [".png", ".jpg", ".svg"];

// Define the ModelDisplay component
const ModelDisplay = ({
  fileName,
  data
}: {
  fileName: string; // The name of the model file
  data: string; // The binary blob data of the file
}) => {
  return (
    // Container for the model file display
    <div id="model-file-container" className="group flex flex-col -z-1 justify-start overflow-y-auto overflow-x-auto styled-scrollbar">
      {/* Render the ImageDisplay component if the file is a supported image type */}
      {SUPPORTED_IMAGE_TYPES.some((value) => fileName.toLowerCase().endsWith(value)) && data !== null ? (<ImageDisplay fileName={fileName} data={data}/>) : (<></>)}

      {/* Render the CodeBlock component if the file is a supported code type */}
      {SUPPORTED_FILE_TYPES.some((value) => fileName.toLowerCase().endsWith(value)) && data !== null ? (<CodeBlock fileName={fileName} codeString={data}/>) : (<></>)}
    </div>
  );
};

export default ModelDisplay; // Export the ModelDisplay component
