import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import TournamentUpload from "./pages/TournamentUpload";
import TournamentResults from "./pages/TournamentResults";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={<Navigate to="/tournament/upload" replace />}
        />
        <Route path="/tournament/upload" element={<TournamentUpload />} />
        <Route path="/tournament/results" element={<TournamentResults />} />
      </Routes>
    </Router>
  );
}

export default App;
