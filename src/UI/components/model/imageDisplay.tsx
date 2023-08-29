import Image from "next/image";
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";

// Define the ImageDisplay component
const ImageDisplay = ({
  fileName,
  data,
}: {
  fileName: string; // The name of the image file
  data: string; // The binary blob data of the image
}) => {
  return (
    // Wrap the image with TransformWrapper for zooming and panning functionality
    <TransformWrapper
      centerZoomedOut={true} // Center the image when zoomed out
      doubleClick={{
        mode: 'reset' // Allow double click to reset the zoom
      }}
    >
      {/* Apply zooming and panning to the Image component */}
      <TransformComponent wrapperStyle={{ width: "100%", height: "100%" }} contentStyle={{ width: "100%", height: "100%" }}>
        {/* Display the image using the Next.js Image component */}
        <Image className="w-full h-full object-contain" src={data} alt={fileName} width={10} height={10} />
      </TransformComponent>
    </TransformWrapper>
  );
};

export default ImageDisplay; // Export the ImageDisplay component
