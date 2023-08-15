import { useEffect } from "react";

// The ModelDataLoader component is used to load the model data
// It takes in the runid and a function to set the model files as props
// It fetches the directory.json file from the server, which lists every file associated with the runid
// It then filters the files to only include the supported file types
// It then sets the model files with the setModelFiles function
// It renders nothing

const SUPPORTED_FILE_TYPES = [".png", ".jpg", ".ant", ".m", ".py", ".jl", ".r", ".txt"];
const ModelDataLoader = ({
  runid,
  setModelFiles,
}: {
  runid: string;
  setModelFiles: (modelFiles: ModelFileSelectOption[]) => void;
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
          if (file.endsWith(fileType)) {
            modelFiles.push(file);
            break;
          }
        }
      });
      setModelFiles(modelFiles.map((key) => {
        return { name: key, label: key, value: key };
      }));
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [runid]);

  return <></>;
};

export default ModelDataLoader;
