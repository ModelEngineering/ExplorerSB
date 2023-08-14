import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import { rest } from "msw";
import { setupServer } from "msw/node";
import Results from "../components/results"; // Update the import path based on your project structure

// Import the mock server handler
import { handlers } from "../__mocks__/mocks";

// Set up mock server
const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("Results component", () => {
  it("renders the loading state while fetching data", async () => {
    const runid = "your-test-runid";

    render(<Results runid={runid} />);

    // Check if the loading message is displayed
    const loadingElement = screen.getByText("Loading...");
    expect(loadingElement).toBeInTheDocument();

    // Wait for data fetching to complete
    await waitFor(() =>
      expect(screen.queryByText("Loading...")).not.toBeInTheDocument()
    );
  });

  it("renders the results when data is available", async () => {
    const runid = "1000";

    // Mock the context data
    const mockContext = {
      abstract: "mock abstract for runid 1000",
      citation: "mock citation for runid 1000",
      doi: "mock doi for runid 1000",
      paper_url: "http://mock.url/runid/1000",
      project_id: "mock project_id for runid 1000",
      runid: runid,
      title: "mock title for runid 1000",
      is_biomodels: false,
    };

    // Set up the server response
    server.use(
      rest.get("/context.json", (req, res, ctx) => {
        return res(ctx.json([mockContext]));
      })
    );

    render(<Results runid={runid} />);

    // Wait for data fetching to complete
    await waitFor(() =>
      expect(screen.queryByText("Loading...")).not.toBeInTheDocument()
    );

    // Check if the title and project ID are rendered correctly
    const titleElement = screen.getByText("Title: mock title for runid 1000");
    const projIdElement = screen.getByText("Project ID: mock project_id for runid 1000");

    expect(titleElement).toBeInTheDocument();
    expect(projIdElement).toBeInTheDocument();
  });
});
