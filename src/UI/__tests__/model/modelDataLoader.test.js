import React from 'react';
import { render, waitFor } from '@testing-library/react';
import ModelDataLoader from '../../components/model/modelDataLoader';

test('fetches and sets model files correctly', async () => {
  const setModelFilesMock = jest.fn();

  // Mock fetch to return the expected response
  global.fetch = jest.fn().mockResolvedValueOnce({
    json: jest.fn().mockResolvedValueOnce([
      { file: 'file1.png' },
      { file: 'file2.jpg' },
      { file: 'file3.txx' }, // Not supported
    ]),
  });

  render(<ModelDataLoader runid="test-runid" setModelFiles={setModelFilesMock} />);

  // Wait for the component's useEffect to complete
  await waitFor(() => {
    expect(setModelFilesMock).toHaveBeenCalledTimes(1);
    expect(setModelFilesMock).toHaveBeenCalledWith([
      { name: 'file1.png', label: 'file1.png', value: 'file1.png' },
      { name: 'file2.jpg', label: 'file2.jpg', value: 'file2.jpg' },
    ]);
  });
});
