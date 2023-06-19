import { saveAs } from "file-saver";
import JSZip from "jszip";

const VizDownloader = async (runid: string) => {
  var zip = new JSZip();
  const getDirectory = async () => {
    const response = await fetch(`/${runid}/directory.json`)
      .then((response) => response.json())
      .then((v) => v)
      .catch((err) => console.log(err));
    return response;
  };
  var directory = await getDirectory();
  const list = directory.map(async ({ file }: { file: string }) => {
    console.log(file)
    const url = `/${runid}/${file}`;
    const response = await fetch(url);
    const data = await response.blob();
    zip.file(file, data);
    return data;
  });
  Promise.all(list).then(() => {
    zip
      .generateAsync({ type: "blob" })
      .then((blob) => saveAs(blob, `${runid}.zip`))
      .catch((err) => console.log(err));
  });
};

export default VizDownloader;
