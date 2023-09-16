import { useEffect } from "react";

// Define the supported file types for the model files
const SUPPORTED_FILE_TYPES = [".png", ".svg", ".jpg", ".ant", ".m", ".py", ".jl", ".r", ".txt"];

// Define the ModelDataLoader component
const ModelDataLoader = ({
  runid,
  setModelFiles,
}: {
  runid: string; // The runid associated with the model
  setModelFiles: (modelFiles: ModelFileSelectOption[]) => void; // Function to set the model files
}) => {
  useEffect(() => {
    // Fetches the directory.json file from the server
    const getDirectory = async () => {
      const response = await fetch(`/${runid}/directory.json`)
        .then((response) => response.json())
        .then((v) => v)
        .catch((err) => console.log(err));
      return response;
    };

    // Filters the files to only include the supported file types
    getDirectory().then((dirData: { file: string }[]) => {
      let modelFiles: string[] = [];
      dirData.forEach(({ file }) => {
        for (const fileType of SUPPORTED_FILE_TYPES) {
          if (file.toLowerCase().endsWith(fileType)) {
            modelFiles.push(file);
            break;
          }
        }
      });

      // Set the model files with the setModelFiles function
      setModelFiles(
        modelFiles.map((key) => {
          return { name: key, label: key, value: key };
        })
      );
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [runid]);

  return <></>; // Return empty fragment
};

export default ModelDataLoader; // Export the ModelDataLoader component
