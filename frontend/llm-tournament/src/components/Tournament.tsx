import React, { useState } from "react";
import axios from "axios";
import MatchDetails from "./MatchDetails";
import TournamentBracket from "./TournamentBracket";
import { Match } from "../types/Match";
import { TournamentResults } from "../types/TournamentResults";

const Tournament = () => {
  const [question, setQuestion] = useState("");
  const [prompts, setPrompts] = useState([]);
  const [results, setResults] = useState<TournamentResults | null>(null);
  const [selectedMatch, setSelectedMatch] = useState<Match | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileUpload = (e) => {
    const fileReader = new FileReader();
    fileReader.onload = (event) => {
      const uploadedPrompts = JSON.parse(event.target.result);
      setPrompts(uploadedPrompts);
    };
    fileReader.readAsText(e.target.files[0]);
  };

  const handleSubmit = async () => {
    try {
      setIsLoading(true);
      const response = await axios.post("http://localhost:8000/tournament", {
        // TODO: change to backend url from env
        question,
        prompts,
      });
      console.log("tournament response", response.data);
      setResults(response.data.tournament_results);
    } catch (error) {
      console.error("Tournament error:", error);
      // Optionally add error handling UI here
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">
            LLM Tournament
          </h1>

          <div className="space-y-8">
            {/* Question Input */}
            <div>
              <label
                htmlFor="question"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Input Question
              </label>
              <input
                id="question"
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-colors"
                placeholder="Enter your medical question here..."
              />
            </div>

            {/* Prompts Section */}
            <div>
              <label
                htmlFor="prompts"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Prompts
              </label>
              <textarea
                id="prompts"
                value={prompts.join("\n")}
                onChange={(e) => setPrompts(e.target.value.split("\n"))}
                placeholder="Enter prompts, one per line..."
                className="w-full h-40 px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-colors resize-none mb-3"
              />

              <div className="flex items-center space-x-4">
                <label className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 cursor-pointer transition-colors">
                  <svg
                    className="w-5 h-5 mr-2 text-gray-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                    />
                  </svg>
                  Upload Prompts
                  <input
                    type="file"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                </label>
              </div>
            </div>

            {/* Submit Button */}
            <button
              onClick={handleSubmit}
              className="w-full sm:w-auto px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-300 transition-colors flex items-center justify-center"
            >
              <svg
                className="w-5 h-5 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
              Run Tournament
            </button>
          </div>

          {/* Results Section */}
          {results && (
            <div className="mt-12">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                Tournament Results
              </h2>
              <div className="bg-gray-50 rounded-xl border border-gray-200 p-6">
                <TournamentBracket
                  results={results}
                  onMatchClick={(match) => setSelectedMatch(match)}
                />
              </div>
            </div>
          )}

          {/* Match Details Modal */}
          {selectedMatch && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
              <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                <MatchDetails
                  match={selectedMatch}
                  onClose={() => setSelectedMatch(null)}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Tournament;
