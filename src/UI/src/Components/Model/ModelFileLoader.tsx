import { useEffect } from "react";

// The ModelFileLoader component is used to load the model file
// It takes in the runid, the file name, and a function to set the file as props
// It fetches the file from the server
// It then sets the file with the setFile function
// It renders nothing

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
    // This function fetches the image from the server
    // It then converts the image to a blob
    // It then converts the blob to an object URL
    // It then sets the file with the setFile function
    const fetchImage = async () => {
      const res = await fetch(`/${runid}/${fileName}`)
      const imageBlob = await res.blob();
      const imageObjectURL = URL.createObjectURL(imageBlob);
      setFile(imageObjectURL);
    };

    // This function fetches the file from the server
    // It then sets the file with the setFile function
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
