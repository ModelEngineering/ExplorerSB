import { useEffect } from "react";

// Define the ModelFileLoader component
const ModelFileLoader = ({
  runid,
  fileName,
  setFile,
}: {
  runid: string; // The runid associated with the model
  fileName: string; // The name of the model file
  setFile: (fileContent: string) => void; // Function to set the file content
}) => {
  useEffect(() => {
    if (fileName === "") {
      return; // If the file name is empty, do nothing
    }

    // This function fetches the image from the server
    // It then converts the image to a blob
    // It then converts the blob to an object URL
    // It then sets the file with the setFile function
    const fetchImage = async () => {
      const res = await fetch(`/${runid}/${fileName}`);
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
        .catch((err) => {
          console.log(err);
          return "";
        });
      setFile(response);
    };

    // Determine whether the file is an image or not
    if (fileName.endsWith(".png") || fileName.endsWith(".jpg")) {
      fetchImage(); // Fetch and display image files
    } else {
      getFile(); // Fetch and display other types of files
    }
  }, [runid, fileName, setFile]); // Effect will run when runid, fileName, or setFile changes

  return <></>; // Return nothing
};

export default ModelFileLoader; // Export the ModelFileLoader component
