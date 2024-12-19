import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import TournamentBracket from "../components/TournamentBracket";
import MatchDetails from "../components/MatchDetails";
import { Match } from "../types/Match";
import { TournamentResults } from "../types/TournamentResults";

const TournamentResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [selectedMatch, setSelectedMatch] = React.useState<Match | null>(null);

  const results = location.state?.results as TournamentResults;

  if (!results) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            No tournament results found
          </h2>
          <button
            onClick={() => navigate("/tournament/upload")}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            Start New Tournament
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900">
              Tournament Results
            </h1>
            <button
              onClick={() => navigate("/tournament/upload")}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            >
              New Tournament
            </button>
          </div>

          {/* Champion Section */}
          <div className="mt-8 p-6 bg-green-50 rounded-xl border border-green-200">
            <h2 className="text-xl font-semibold text-green-800 mb-3">
              Tournament Champion
            </h2>
            <p className="text-green-700">{results.champion}</p>
          </div>

          <div className="bg-gray-50 rounded-xl border border-gray-200 p-6">
            <TournamentBracket
              results={results}
              onMatchClick={(match) => setSelectedMatch(match)}
            />
          </div>

          {/* Match Details */}
          {selectedMatch && (
            <MatchDetails
              match={selectedMatch}
              onClose={() => setSelectedMatch(null)}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default TournamentResultsPage;
