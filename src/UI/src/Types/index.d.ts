declare global {
  interface SearchResult {
    title: string | null,
    abstract: string,
    project_id: string,
    runid: string,
    id: number
  }
}

export {}
