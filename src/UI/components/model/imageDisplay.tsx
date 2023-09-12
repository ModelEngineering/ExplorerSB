import Image from "next/image";
import { TransformWrapper, TransformComponent, useControls } from "react-zoom-pan-pinch";
import { BiZoomIn as ZoomIn, BiZoomOut as ZoomOut } from "react-icons/bi";
import { GrPowerReset as Reset} from 'react-icons/gr';

// Define the ImageDisplay component
const ImageDisplay = ({
  fileName,
  data,
}: {
  fileName: string; // The name of the image file
  data: string; // The binary blob data of the image
}) => {
    // define component to create buttons for zooming in, zooming out, and resetting scale
    const Controls = () => {
      const { zoomIn, zoomOut, resetTransform } = useControls();
      return (
        <div className="m-auto inline-block">
          <button title="Zoom In" className="h-8 w-8 m-2 rounded-lg bg-slate-300 p-2 text-center text-md hover:bg-slate-500"
            onClick={() => zoomIn()}>{<ZoomIn/>}</button> 
          <button title="Zoom Out" className="h-8 w-8 m-2 rounded-lg bg-slate-300 p-2 text-center text-md hover:bg-slate-500"
            onClick={() => zoomOut()}>{<ZoomOut/>}</button>
          <button title="Reset Zoom" className="h-8 w-8 m-2 rounded-lg bg-slate-300 p-2 text-center text-md hover:bg-slate-500"
            onClick={() => resetTransform()}>{<Reset/>}</button>
        </div>
      );
    };
  
  return (
    // Wrap the image with TransformWrapper for zooming and panning functionality
    <TransformWrapper
      centerZoomedOut={true} // Center the image when zoomed out
      doubleClick={{
        mode: 'reset' // Allow double click to reset the zoom
      }}
    >
      {/* Display list of control buttons (zoom in/out, reset) */}
      <Controls/>
      {/* Apply zooming and panning to the Image component */}
      <TransformComponent wrapperStyle={{ width: "100%", height: "100%" }} contentStyle={{ width: "100%", height: "100%" }}>
        {/* Display the image using the Next.js Image component */}
        <Image className="w-full h-full object-contain" src={data} alt={fileName} width={10} height={10} />
      </TransformComponent>
    </TransformWrapper>
  );
};

export default ImageDisplay; // Export the ImageDisplay component
