'use client'
import React, { useEffect } from "react";
import { Document, Page, pdfjs } from 'react-pdf';
import type { PDFDocumentProxy } from 'pdfjs-dist';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';
import { TransformWrapper, TransformComponent, useControls } from "react-zoom-pan-pinch";
import { BiZoomIn as ZoomIn, BiZoomOut as ZoomOut, BiReset as Reset } from "react-icons/bi";

// import worker
import "pdfjs-dist/build/pdf.worker.entry";
pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.js',
  import.meta.url,
).toString();

// define union type for pdf files
type PDFFile = File | null;

// define pdfDisplay component
const PdfDisplay = (
    { runID, fileName }: { runID: string, fileName: string }
) => {

    const [pdfFile, setPdfFile] = React.useState<PDFFile>(null) // stores data for specified file
    const [numPages, setNumPages] = React.useState<number>(0); // stores total number of pages in the document
  
    // defines control buttons for user to be able to zoom in and out
    // will be displayed along with the pdf
    const Controls = () => {
      const { zoomIn, zoomOut, resetTransform } = useControls();
      return (
        <div className="flex justify-center items-center relative w-full bg-gray-800">
          <button title="Zoom In" onClick={() => zoomIn()} className="bg-transparent rounded-lg text-white text-center p-2 m-1 flex items-center justify-center hover:bg-gray-500">{<ZoomIn />}</button>
          <button title="Zoom Out" onClick={() => zoomOut()} className="bg-transparent rounded-lg text-white text-center p-2 m-1 flex items-center justify-center hover:bg-gray-500"><ZoomOut /></button>
          <button title="Reset Zoom" onClick={() => resetTransform()} className="bg-transparent rounded-lg text-white text-center p-2 m-1 flex items-center justify-center hover:bg-gray-500">{<Reset/>}</button>
        </div>
      );
    };

    // fetch the pdf data
    // convert it to a blob, then create and store File object for easy display
    useEffect(() => { 
        const getPdfData = async () => {
          const res = await fetch(`/${runID}/${fileName}`);
          const blob = await res.blob();
          setPdfFile(new File ([blob], "pdf")) // converting blob to File
        }
  
        getPdfData();
        
      }, [runID, fileName])

    // sets page numbers once document finishes loading
    function onDocumentLoadSuccess({ numPages: nextNumPages }: PDFDocumentProxy): void {
        setNumPages(nextNumPages);
    }


    if (pdfFile) {
        return (
          <div className="flex flex-col items-center">
            <div className="bg-gray-600 m-auto">
              {/* Render the pdf document */}
              <Document className="flex flex-col items-center max-w-full m-0 p-0 relative" file={pdfFile} onLoadSuccess={onDocumentLoadSuccess}>
                
                {/* Wrap the pdf document with a TransformWrapper to enable zooming */}
                <TransformWrapper
                    centerZoomedOut={true}
                    wheel = {{disabled: true}} // Disable panning with mousepad so it doesn't interfere with scroll action
                    doubleClick={{
                      mode: 'reset' // Allow double click to reset zoom
                    }}
                    centerOnInit={true}
                >

                  {/* Render header containing zoom controls */}
                  <header className="bg-gray-800 relative w-full z-10 justify-center items-center overflow-hidden">
                      <Controls />
                  </header>

                  <TransformComponent>
                    {/* Render each individual page of the pdf with a unique key */}
                    {Array.from(new Array(numPages), (__, index) => (
                        <Page 
                            className="m-auto"
                            key={`page_${index + 1}`} 
                            pageNumber={index + 1} 
                        />
                    ))}
                    </TransformComponent>
                </TransformWrapper>
              </Document>
            </div>
          </div>
        );
      } else {
        return <></> // if the data is missing or file is invalid, return nothing
      }
  
}

export default PdfDisplay;