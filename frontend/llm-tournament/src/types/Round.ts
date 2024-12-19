import { Match } from "./Match";

export interface Round {
  round_number: number;
  matches: Match[];
}
