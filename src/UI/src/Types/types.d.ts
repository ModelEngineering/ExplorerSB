declare global {
  interface Context {
    project_id: string,
    runid: string,
    abstract: string,
    citation: string | null,
    doi: string | null,
    paper_url: string | null,
    title: string | null,
  }

  interface ContextWithSnippets extends Context {
    snippet: string,
  }

  interface VariableSelectOption {
    label: string,
    value: string,
    [x: string]: any,
  }

  interface CSVSelectOption {
    name: string,
    [x: string]: any,
  }

  interface ModelFileSelectOption {
    name: string,
    [x: string]: any,
  }
}

export {}
