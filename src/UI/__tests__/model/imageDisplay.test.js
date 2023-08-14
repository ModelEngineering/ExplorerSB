// __tests__/imageDisplay.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import ImageDisplay from '../../components/model/imageDisplay';

test('renders ImageDisplay component correctly', () => {
  const fileName = 'test-image.png';
  const imageData = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...'; // Base64 image data

  render(<ImageDisplay fileName={fileName} data={imageData} />);

  // Check if the image is rendered with the provided fileName
  const imageElement = screen.getByAltText(fileName);
  expect(imageElement).toBeInTheDocument();

  // You can also test the presence of specific elements from react-zoom-pan-pinch if needed
});
