from typing import List, Optional
from pydantic import BaseModel


class Judge(BaseModel):
    name: str
    weight: int
    prompt: str


class Score(BaseModel):
    prompt_a: int
    prompt_b: int


class JudgeScore(BaseModel):
    judge: Judge
    score: Score


class Match(BaseModel):
    match_id: int
    prompt_a: str
    prompt_b: str
    output_a: str
    output_b: str
    winner: str
    judge_scores: List[JudgeScore]


class Round(BaseModel):
    round_number: int
    matches: List[Match]


class TournamentInput(BaseModel):
    question: str
    prompts: List[str]


class TournamentResult(BaseModel):
    rounds: List[Round]
    champion: str
