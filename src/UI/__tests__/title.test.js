import React from "react";
import { render, screen } from "@testing-library/react";
import Title from "../components/title"; // Update the import path based on your project structure

describe("Title component", () => {
  it("renders the title and project ID correctly", () => {
    const title = "Sample Title";
    const projId = "12345";

    // Render the Title component with the provided props
    render(<Title title={title} proj_id={projId} />);

    // Check if the title and project ID are rendered correctly
    const titleElement = screen.getByText(`Title: ${title}`);
    const projIdElement = screen.getByText(`Project ID: ${projId}`);

    expect(titleElement).toBeInTheDocument();
    expect(projIdElement).toBeInTheDocument();
  });

  it("renders 'N/A' for title when it's null", () => {
    const projId = "12345";

    // Render the Title component with a null title
    render(<Title title={null} proj_id={projId} />);

    // Check if 'N/A' is rendered for the title
    const naTitleElement = screen.getByText("Title: N/A");
    const projIdElement = screen.getByText(`Project ID: ${projId}`);

    expect(naTitleElement).toBeInTheDocument();
    expect(projIdElement).toBeInTheDocument();
  });
});
