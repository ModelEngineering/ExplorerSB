import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";

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
    >
      <TransformComponent wrapperStyle={{width: "100%", height: "100%"}} contentStyle={{width: "100%", height: "100%"}}>
        <img className="model-image" src={data} alt={fileName} />
      </TransformComponent>
    </TransformWrapper>
  );
};

export default ImageDisplay;
