import React from "react";
import { Match } from "../types/Match";
import { JudgeScore } from "../types/JudgeScore";

interface MatchDetailsProps {
  match: Match;
  onClose: () => void;
}

const MatchDetails: React.FC<MatchDetailsProps> = ({ match, onClose }) => {
  // Calculate average scores
  const averageScores = {
    prompt_a:
      match.judge_scores.reduce(
        (acc, judgeScore) => acc + judgeScore.score.prompt_a,
        0
      ) / match.judge_scores.length,
    prompt_b:
      match.judge_scores.reduce(
        (acc, judgeScore) => acc + judgeScore.score.prompt_b,
        0
      ) / match.judge_scores.length,
  };

  return (
    <div className="bg-gray-900 rounded-xl p-8 max-w-4xl mx-auto mt-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-gray-100">
          Match {match.match_id}
        </h2>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-200 transition-colors"
        >
          <svg
            className="w-6 h-6"
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

      <div className="grid grid-cols-2 gap-8">
        <div
          className={`p-6 rounded-lg border-2 ${
            match.winner === match.prompt_a
              ? "border-green-500 bg-green-500/10"
              : "border-gray-700 bg-gray-800/50"
          }`}
        >
          <h3 className="text-lg font-medium text-gray-200 mb-3">Prompt A</h3>
          <p className="text-gray-300 mb-4">{match.prompt_a}</p>
          <div className="text-sm text-gray-400">
            Average Score: {averageScores.prompt_a.toFixed(2)}
          </div>
        </div>

        <div
          className={`p-6 rounded-lg border-2 ${
            match.winner === match.prompt_b
              ? "border-green-500 bg-green-500/10"
              : "border-gray-700 bg-gray-800/50"
          }`}
        >
          <h3 className="text-lg font-medium text-gray-200 mb-3">Prompt B</h3>
          <p className="text-gray-300 mb-4">{match.prompt_b}</p>
          <div className="text-sm text-gray-400">
            Average Score: {averageScores.prompt_b.toFixed(2)}
          </div>
        </div>
      </div>

      <div className="mt-8">
        <h3 className="text-lg font-medium text-gray-200 mb-4">Judge Scores</h3>
        <div className="grid grid-cols-4 gap-4">
          {match.judge_scores.map((judgeScore: JudgeScore, index: number) => (
            <div key={index} className="bg-gray-800/50 p-4 rounded-lg">
              <h4 className="text-sm font-medium text-gray-300 mb-2">
                Judge {judgeScore.judge.name}
              </h4>
              <div className="space-y-2 text-sm">
                <div className="text-gray-400">
                  Prompt A: {judgeScore.score.prompt_a}
                </div>
                <div className="text-gray-400">
                  Prompt B: {judgeScore.score.prompt_b}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-8 p-4 bg-green-500/10 rounded-lg border border-green-500/20">
        <h3 className="text-lg font-medium text-green-400 mb-2">Winner</h3>
        <p className="text-gray-200">{match.winner}</p>
      </div>
    </div>
  );
};

export default MatchDetails;
