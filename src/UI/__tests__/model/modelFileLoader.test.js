import React from 'react';
import { render, waitFor } from '@testing-library/react';
import ModelFileLoader from '../../components/model/modelFileLoader';

test('fetches and sets file content correctly', async () => {
  const setFileMock = jest.fn();

  // Mock fetch to return the expected response
  global.fetch = jest.fn().mockResolvedValueOnce({
    text: jest.fn().mockResolvedValueOnce('file content'),
  });

  render(
    <ModelFileLoader runid="test-runid" fileName="file.txt" setFile={setFileMock} />
  );

  // Wait for the component's useEffect to complete
  await waitFor(() => {
    expect(setFileMock).toHaveBeenCalledTimes(1);
    expect(setFileMock).toHaveBeenCalledWith('file content');
  });
});
