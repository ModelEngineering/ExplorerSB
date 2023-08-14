import React from "react";
import { render } from "@testing-library/react";
import CodeBlock from "../../components/model/codeBlock";

describe("CodeBlock component", () => {
  it("renders correctly", () => {
    const codeString = `const greeting = "Hello, world!";\nconsole.log(greeting);`;
    const { container } = render(<CodeBlock codeString={codeString} />);
    expect(container).toMatchSnapshot();
  });
});
