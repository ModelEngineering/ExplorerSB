import React from 'react';
import { render } from '@testing-library/react';
import Footer from '../components/footer';

test('renders Footer component correctly', () => {
  const { getByText } = render(<Footer />);
  const copyrightText = getByText(/Center for Reproducible Biomedical Modeling © 2023/i);
  expect(copyrightText).toBeInTheDocument();
});
