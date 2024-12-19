import React from "react";
import { Match } from "../types/Match";
import { TournamentResults } from "../types/TournamentResults";

interface TournamentBracketProps {
  results: TournamentResults;
  onMatchClick: (match: Match) => void;
}

const TournamentBracket: React.FC<TournamentBracketProps> = ({
  results,
  onMatchClick,
}) => {
  const finalRound = results.rounds[results.rounds.length - 1];

  // Helper function to split matches into left and right sides
  const splitMatches = (round: any) => {
    const midpoint = Math.ceil(round.matches.length / 2);
    return {
      leftMatches: round.matches.slice(0, midpoint),
      rightMatches: round.matches.slice(midpoint),
    };
  };

  return (
    <div className="w-full overflow-x-auto bg-gray-900 p-8 rounded-lg shadow-2xl">
      <div className="flex justify-between min-w-fit">
        {/* Left Side */}
        <div className="flex gap-16">
          {results.rounds.slice(0, -1).map((round, roundIndex) => {
            const { leftMatches } = splitMatches(round);
            return (
              <div
                key={`left-${round.round_number}`}
                className="flex flex-col"
                style={{
                  gap: `${Math.pow(2, roundIndex + 4)}px`, // Base spacing for matches within a round
                  marginTop:
                    roundIndex > 0
                      ? `${Math.pow(2, roundIndex + 2)}px` // Adjust top margin for inner rounds
                      : "0",
                }}
              >
                <h3 className="text-lg font-semibold text-gray-300 mb-4">
                  Round {round.round_number}
                </h3>
                {leftMatches.map((match) => (
                  <MatchCircle
                    key={match.match_id}
                    match={match}
                    onClick={() => onMatchClick(match)}
                    showConnector="right"
                  />
                ))}
              </div>
            );
          })}
        </div>

        {/* Final */}
        <div className="flex flex-col justify-center mx-16">
          <h3 className="text-lg font-semibold text-gray-300 mb-4 text-center">
            Final
          </h3>
          {finalRound?.matches.map((match) => (
            <MatchCircle
              key={match.match_id}
              match={match}
              onClick={() => onMatchClick(match)}
              isFinal
              showWinner
            />
          ))}
        </div>

        {/* Right Side */}
        <div className="flex gap-16 flex-row-reverse">
          {" "}
          {/* Added flex-row-reverse */}
          {results.rounds.slice(0, -1).map((round, roundIndex) => {
            const { rightMatches } = splitMatches(round);
            return (
              <div
                key={`right-${round.round_number}`}
                className="flex flex-col"
                style={{
                  gap: `${Math.pow(2, roundIndex + 4)}px`, // Base spacing for matches within a round
                  marginTop:
                    roundIndex > 0
                      ? `${Math.pow(2, roundIndex + 2)}px` // Adjust top margin for inner rounds
                      : "0",
                }}
              >
                <h3 className="text-lg font-semibold text-gray-300 mb-4">
                  Round {round.round_number}
                </h3>
                {rightMatches.map((match) => (
                  <MatchCircle
                    key={match.match_id}
                    match={match}
                    onClick={() => onMatchClick(match)}
                    showConnector="left"
                  />
                ))}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

const MatchCircle: React.FC<{
  match: Match;
  onClick: () => void;
  showConnector?: "left" | "right";
  isFinal?: boolean;
  showWinner?: boolean;
}> = ({ match, onClick, showConnector, isFinal, showWinner }) => (
  <div className="relative">
    <div
      onClick={onClick}
      className="w-12 h-12 rounded-full bg-gray-800 border-2 border-gray-700 
                 hover:border-indigo-500 hover:shadow-indigo-500/20 
                 transition-all duration-300 cursor-pointer
                 flex items-center justify-center"
    >
      <span className="text-gray-300 text-sm font-medium">
        {match.match_id}
      </span>
    </div>

    {showWinner && (
      <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 w-48 text-center">
        <div className="text-indigo-400 text-sm font-medium truncate">
          {match.winner}
        </div>
      </div>
    )}

    {!isFinal && showConnector === "right" && (
      <div className="absolute top-1/2 -right-16 w-16 h-[2px] bg-gray-700" />
    )}
    {!isFinal && showConnector === "left" && (
      <div className="absolute top-1/2 -left-16 w-16 h-[2px] bg-gray-700" />
    )}
  </div>
);

export default TournamentBracket;
