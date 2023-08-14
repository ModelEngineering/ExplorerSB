import Image from "next/image";
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";

// The ImageDisplay component is used to display the image
// It uses the react-zoom-pan-pinch library to allow the user to zoom in and out of the image
// It takes in the file name and the binary blob data of the image as props
// It renders the image and allows the user to zoom in and out of the image
// It also allows the user to double click to reset the zoom

const ImageDisplay = ({
  fileName,
  data,
}: {
  fileName: string;
  data: string;
}) => {
  return (
    <TransformWrapper
      centerZoomedOut={true}
      doubleClick={{
        mode: 'reset'
      }}
    >
      <TransformComponent wrapperStyle={{width: "100%", height: "100%"}} contentStyle={{width: "100%", height: "100%"}}>
        <Image className="w-full h-full object-contain" src={data} alt={fileName} width={10} height={10}/>
      </TransformComponent>
    </TransformWrapper>
  );
};

export default ImageDisplay;
