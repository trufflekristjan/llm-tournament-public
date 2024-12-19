import { JudgeScore } from "./JudgeScore";

export interface Match {
  match_id: number;
  prompt_a: string;
  prompt_b: string;
  output_a: string;
  output_b: string;
  winner: string;
  judge_scores: Array<JudgeScore>;
}
