import { render } from '@testing-library/react'
import Home from '../app/page'
 
it('renders Home page correctly', () => {
  const { container } = render(<Home />);
  expect(container).toMatchSnapshot();
});