import { useEffect } from "react";

const SUPPORTED_FILE_TYPES = [".png", ".jpg", ".ant"];
const ModelDataLoader = ({
  runid,
  setModelFiles,
}: {
  runid: string;
  setModelFiles: (modelFiles: ModelFileSelectOption[]) => void;
}) => {
  useEffect(() => {
    const getDirectory = async () => {
      const response = await fetch(`/${runid}/directory.json`)
        .then((response) => response.json())
        .then((v) => v)
        .catch((err) => console.log(err));
      return response;
    };
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
  }, [runid]);

  return <></>;
};

export default ModelDataLoader;
