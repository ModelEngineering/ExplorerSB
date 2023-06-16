import { useEffect } from "react";

const ModelFileLoader = ({
  runid,
  fileName,
  setFile,
}: {
  runid: string;
  fileName: string;
  setFile: (fileContent: string) => void;
}) => {
  useEffect(() => {
    const fetchImage = async () => {
      const res = await fetch(`/${runid}/${fileName}`)
      const imageBlob = await res.blob();
      const imageObjectURL = URL.createObjectURL(imageBlob);
      setFile(imageObjectURL);
    };
    const getFile = async () => {
      const response = await fetch(`/${runid}/${fileName}`)
        .then((response) => response.text())
        .then((v) => v)
        .catch((err) => {console.log(err); return "";});
        setFile(response);
    };
    if (fileName.endsWith(".png") || fileName.endsWith(".jpg")) {
      fetchImage();
    } else {
      getFile();
    }
  }, [runid, fileName]);

  return <></>;
};

export default ModelFileLoader;
