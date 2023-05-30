import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Landing from "./Components/Landing";
import Results from "./Components/Results";

function App() {
  return(
  <div id="App">
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/model/:run_id" element={<Results />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
    </BrowserRouter>
  </div>
  );
}

export default App;
