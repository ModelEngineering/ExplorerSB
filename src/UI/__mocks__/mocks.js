import { rest } from "msw";

export const handlers = [
  rest.get("/context.json", (req, res, ctx) => {
    const mockContext = [
      {
        abstract: "mock abstract for runid 1000",
        citation: "mock citation for runid 1000",
        doi: "mock doi for runid 1000",
        paper_url: "http://mock.url/runid/1000",
        project_id: "mock project_id for runid 1000",
        runid: "1000",
        title: "mock title for runid 1000",
        is_biomodels: false,
      },
      {
        abstract: "mock abstract for runid 2000",
        citation: "mock citation for runid 2000",
        doi: "mock doi for runid 2000",
        paper_url: "http://mock.url/runid/2000",
        project_id: "mock project_id for runid 2000",
        runid: "2000",
        title: "mock title for runid 2000",
        is_biomodels: false,
      },
      {
        abstract: "mock abstract for runid 3000",
        citation: "mock citation for runid 3000",
        doi: "mock doi for runid 3000",
        paper_url: "http://mock.url/runid/3000",
        project_id: "mock project_id for runid 3000",
        runid: "3000",
        title: "mock title for runid 3000",
        is_biomodels: false,
      },
    ];
    return res(ctx.json(mockContext));
  }),
  rest.get("/runid/1000/directory.json", (req, res, ctx) => {
    const mockDirectory = [{"file": "report.csv"}, {"file": "Figure_1c.csv"}, {"file": "Repressilator-Elowitz-Nature-2000.ant"}, {"file": "Figure_1a.png"}]
    return res(ctx.json(mockDirectory));
  }),
];
