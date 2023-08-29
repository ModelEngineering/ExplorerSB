import { saveAs } from "file-saver";
import JSZip from "jszip";

// This function downloads all files from a simulation run and saves them as a zip file
const VizDownloader = async (runid: string) => {
  // Create a new JSZip object to hold the downloaded files
  var zip = new JSZip();

  // Fetch the directory data from the server using the runid
  const getDirectory = async () => {
    const response = await fetch(`/${runid}/directory.json`)
      .then((response) => response.json())
      .then((v) => v)
      .catch((err) => console.log(err));
    return response;
  };
  var directory = await getDirectory();

  // Download each file in the directory and add it to the JSZip object
  const list = directory.map(async ({ file }: { file: string }) => {
    const url = `/${runid}/${file}`;
    const response = await fetch(url);
    const data = await response.blob();
    zip.file(file, data);
    return data;
  });

  // Wait for all files to be downloaded, then generate the zip file and save it using the file-saver library
  Promise.all(list).then(() => {
    zip
      .generateAsync({ type: "blob" })
      .then((blob) => saveAs(blob, `${runid}.zip`))
      .catch((err) => console.log(err));
  });
};

export default VizDownloader;