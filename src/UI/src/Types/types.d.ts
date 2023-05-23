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

  interface Position {
    position: number[][]
  }

  interface Snippet {
    title?: Position,
    abstract?: Position,
  }

  interface ContextWithSnippets extends Context {
    snippet: string,
  }
}

export {}
