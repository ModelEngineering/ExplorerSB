// __tests__/viewer.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import Viewer from '../components/viewer';

describe('Viewer component', () => {
  test('renders Viewer component correctly', () => {
    const runid = 'test-runid';

    render(<Viewer runid={runid} />);

    // Check if the Viewer component renders the header
    const headerElement = screen.getByText('Model');
    expect(headerElement).toBeInTheDocument();

    //TODO: add tests for dropdown menu
  });
});
