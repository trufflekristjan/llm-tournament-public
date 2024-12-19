import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Judge } from "../types/Judge";

const TournamentUpload = () => {
  const [question, setQuestion] = useState("");
  const [prompts, setPrompts] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [judges, setJudges] = useState<Judge[]>([]);
  const [selectedJudge, setSelectedJudge] = useState<number | null>(null);
  const navigate = useNavigate();

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;

    const fileReader = new FileReader();
    fileReader.onload = (event) => {
      if (event.target?.result) {
        const uploadedPrompts = JSON.parse(event.target.result as string);
        setPrompts(uploadedPrompts);
      }
    };
    fileReader.readAsText(e.target.files[0]);
  };

  const handleSubmit = async () => {
    try {
      setIsLoading(true);
      const response = await axios.post("http://localhost:8000/tournament", {
        question,
        prompts,
      });

      // Navigate to results page with the tournament data
      navigate("/tournament/results", { state: { results: response.data } });
    } catch (error) {
      console.error("Tournament error:", error);
      alert("Failed to run tournament. Please check console for details.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const fetchJudges = async () => {
      try {
        const response = await axios.get("http://localhost:8000/judges");
        setJudges(response.data);
      } catch (error) {
        console.error("Failed to fetch judges:", error);
      }
    };

    fetchJudges();
  }, []);

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
              disabled={isLoading}
              className="w-full sm:w-auto px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-300 transition-colors flex items-center justify-center disabled:opacity-50"
            >
              {isLoading ? (
                <span className="flex items-center">
                  <svg
                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Running Tournament...
                </span>
              ) : (
                <span className="flex items-center">
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
                </span>
              )}
            </button>
          </div>
          {/* Judges Section */}
          <div className="mt-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Tournament Judges
            </h2>

            {/* Horizontal Judge Display */}
            <div className="grid grid-cols-4 gap-4 w-full">
              {" "}
              {/* Changed to grid */}
              {judges.map((judge, index) => (
                <button
                  key={index}
                  onClick={() =>
                    setSelectedJudge(selectedJudge === index ? null : index)
                  }
                  className={`flex flex-col items-center p-4 rounded-lg transition-all w-full
                    ${
                      selectedJudge === index
                        ? "bg-indigo-50 border-2 border-indigo-500 shadow-lg"
                        : "bg-gray-50 border-2 border-transparent hover:bg-gray-100"
                    }`}
                >
                  <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mb-3">
                    <svg
                      className="w-6 h-6 text-indigo-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                    </svg>
                  </div>
                  <h3 className="text-sm font-semibold text-gray-900">
                    Judge {index + 1}
                  </h3>
                  <p className="text-xs text-gray-500 mt-1">{judge.name}</p>
                </button>
              ))}
            </div>

            {/* Selected Judge Prompt */}
            {selectedJudge !== null && (
              <div className="mt-6 p-6 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Judge {selectedJudge + 1} Prompt
                  </h3>
                  <button
                    onClick={() => setSelectedJudge(null)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <svg
                      className="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {judges[selectedJudge].prompt}
                </p>
              </div>
            )}
          </div>{" "}
        </div>
      </div>
    </div>
  );
};

export default TournamentUpload;
