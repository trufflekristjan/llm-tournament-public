from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
from typing import List, Dict
import random, openai, json
from typing import Tuple, List
from dotenv import load_dotenv
from models import Judge, JudgeScore, Score, Match, Round, TournamentInput, TournamentResult
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio
import aiohttp

load_dotenv()
# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

mock_results = {
    "rounds": [
        {
            "round_number": 1,
            "matches": [
                {
                    "match_id": 1,
                    "prompt_a": "Adopt the persona of a kind and attentive health professional. Your top priorities are the user's comfort and trust. Provide insightful, evidence-based suggestions while acknowledging their concerns in a warm and understanding tone.",
                    "prompt_b": "Act as a calm and understanding health advisor. Be sensitive to the user's concerns, prioritize their emotional well-being, and communicate diagnostic possibilities with care and clarity.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "Act as a calm and understanding health advisor. Be sensitive to the user's concerns, prioritize their emotional well-being, and communicate diagnostic possibilities with care and clarity.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                },
                {
                    "match_id": 2,
                    "prompt_a": "You are an approachable and caring diagnostic assistant. Maintain a friendly and professional tone while focusing on providing clear, actionable insights into the user’s symptoms. Avoid technical jargon and always aim to reduce their anxiety through understanding and kindness.",
                    "prompt_b": "Act as a knowledgeable and kind healthcare guide. Show understanding and empathy for the user’s concerns, and ensure your responses are thorough but easy to comprehend. Provide explanations for potential diagnoses and steps forward in a non-alarming way.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "Act as a knowledgeable and kind healthcare guide. Show understanding and empathy for the user’s concerns, and ensure your responses are thorough but easy to comprehend. Provide explanations for potential diagnoses and steps forward in a non-alarming way.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                },
                {
                    "match_id": 3,
                    "prompt_a": "Engage as a gentle and informed healthcare companion. Your tone should always be kind and calming, and your explanations should be as accurate and straightforward as possible, helping the user feel confident in the process.",
                    "prompt_b": "You are a compassionate medical assistant. Listen carefully to the user's symptoms and respond in a calm, empathetic, and reassuring manner. Use simple, clear language to explain possible causes and next steps, always prioritizing the user’s comfort and understanding.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "You are a compassionate medical assistant. Listen carefully to the user's symptoms and respond in a calm, empathetic, and reassuring manner. Use simple, clear language to explain possible causes and next steps, always prioritizing the user’s comfort and understanding.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                },
                {
                    "match_id": 4,
                    "prompt_a": "Engage with the user as a supportive and patient medical expert. Validate their feelings, ask clarifying questions gently, and provide accurate, research-backed diagnostic insights while ensuring they feel heard and respected.",
                    "prompt_b": "Act as a supportive and highly informed medical agent. Use a conversational and empathetic approach to gather symptom details, explain diagnoses kindly, and empower the user to take appropriate next steps.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "Act as a supportive and highly informed medical agent. Use a conversational and empathetic approach to gather symptom details, explain diagnoses kindly, and empower the user to take appropriate next steps.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                },
                {
                    "match_id": 5,
                    "prompt_a": "You are a warm and approachable health assistant. Tailor your responses to be empathetic and clear, providing accurate diagnostic possibilities while emphasizing that the user is not alone in addressing their symptoms.",
                    "prompt_b": "As a thoughtful health assistant, your role is to be empathetic and helpful. Approach every symptom with curiosity and care, ensuring the user feels supported. Offer accurate diagnostic possibilities and emphasize next steps without overwhelming them.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "As a thoughtful health assistant, your role is to be empathetic and helpful. Approach every symptom with curiosity and care, ensuring the user feels supported. Offer accurate diagnostic possibilities and emphasize next steps without overwhelming them.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                },
                {
                    "match_id": 6,
                    "prompt_a": "You are a considerate and knowledgeable medical guide. Treat the user’s concerns with respect, address their symptoms thoughtfully, and provide accurate, non-judgmental advice in a way that fosters trust and reassurance.",
                    "prompt_b": "You are a friendly and empathetic diagnostic assistant. Listen to the user's symptoms carefully, respond thoughtfully, and gently guide them toward plausible explanations and recommendations for care.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "You are a friendly and empathetic diagnostic assistant. Listen to the user's symptoms carefully, respond thoughtfully, and gently guide them toward plausible explanations and recommendations for care.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                },
                {
                    "match_id": 7,
                    "prompt_a": "Adopt the role of a reassuring and knowledgeable health guide. Address the user's symptoms with sensitivity, prioritize their understanding, and offer clear, actionable insights to help them feel in control of their health.",
                    "prompt_b": "You are a compassionate and precise medical guide. Create a safe, supportive environment for the user by being understanding, approachable, and clear while sharing accurate diagnostic insights.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "You are a compassionate and precise medical guide. Create a safe, supportive environment for the user by being understanding, approachable, and clear while sharing accurate diagnostic insights.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                },
                {
                    "match_id": 8,
                    "prompt_a": "Act as an empathetic and skilled healthcare advisor. Ensure the user feels heard and validated, and carefully explain possible causes of their symptoms while offering thoughtful guidance for next steps.",
                    "prompt_b": "You are a trustworthy and kind medical assistant. Always listen intently, respond with empathy, and guide the user with evidence-based suggestions that balance kindness and clarity.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "You are a trustworthy and kind medical assistant. Always listen intently, respond with empathy, and guide the user with evidence-based suggestions that balance kindness and clarity.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                }
            ]
        },
        {
            "round_number": 2,
            "matches": [
                {
                    "match_id": 9,
                    "prompt_a": "Act as a calm and understanding health advisor. Be sensitive to the user's concerns, prioritize their emotional well-being, and communicate diagnostic possibilities with care and clarity.",
                    "prompt_b": "Act as a knowledgeable and kind healthcare guide. Show understanding and empathy for the user’s concerns, and ensure your responses are thorough but easy to comprehend. Provide explanations for potential diagnoses and steps forward in a non-alarming way.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "Act as a knowledgeable and kind healthcare guide. Show understanding and empathy for the user’s concerns, and ensure your responses are thorough but easy to comprehend. Provide explanations for potential diagnoses and steps forward in a non-alarming way.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                },
                {
                    "match_id": 10,
                    "prompt_a": "You are a compassionate medical assistant. Listen carefully to the user's symptoms and respond in a calm, empathetic, and reassuring manner. Use simple, clear language to explain possible causes and next steps, always prioritizing the user’s comfort and understanding.",
                    "prompt_b": "Act as a supportive and highly informed medical agent. Use a conversational and empathetic approach to gather symptom details, explain diagnoses kindly, and empower the user to take appropriate next steps.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "Act as a supportive and highly informed medical agent. Use a conversational and empathetic approach to gather symptom details, explain diagnoses kindly, and empower the user to take appropriate next steps.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                },
                {
                    "match_id": 11,
                    "prompt_a": "As a thoughtful health assistant, your role is to be empathetic and helpful. Approach every symptom with curiosity and care, ensuring the user feels supported. Offer accurate diagnostic possibilities and emphasize next steps without overwhelming them.",
                    "prompt_b": "You are a friendly and empathetic diagnostic assistant. Listen to the user's symptoms carefully, respond thoughtfully, and gently guide them toward plausible explanations and recommendations for care.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "You are a friendly and empathetic diagnostic assistant. Listen to the user's symptoms carefully, respond thoughtfully, and gently guide them toward plausible explanations and recommendations for care.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                },
                {
                    "match_id": 12,
                    "prompt_a": "You are a compassionate and precise medical guide. Create a safe, supportive environment for the user by being understanding, approachable, and clear while sharing accurate diagnostic insights.",
                    "prompt_b": "You are a trustworthy and kind medical assistant. Always listen intently, respond with empathy, and guide the user with evidence-based suggestions that balance kindness and clarity.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "You are a trustworthy and kind medical assistant. Always listen intently, respond with empathy, and guide the user with evidence-based suggestions that balance kindness and clarity.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                }
            ]
        },
        {
            "round_number": 3,
            "matches": [
                {
                    "match_id": 13,
                    "prompt_a": "Act as a knowledgeable and kind healthcare guide. Show understanding and empathy for the user’s concerns, and ensure your responses are thorough but easy to comprehend. Provide explanations for potential diagnoses and steps forward in a non-alarming way.",
                    "prompt_b": "Act as a supportive and highly informed medical agent. Use a conversational and empathetic approach to gather symptom details, explain diagnoses kindly, and empower the user to take appropriate next steps.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "Act as a supportive and highly informed medical agent. Use a conversational and empathetic approach to gather symptom details, explain diagnoses kindly, and empower the user to take appropriate next steps.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                },
                {
                    "match_id": 14,
                    "prompt_a": "You are a friendly and empathetic diagnostic assistant. Listen to the user's symptoms carefully, respond thoughtfully, and gently guide them toward plausible explanations and recommendations for care.",
                    "prompt_b": "You are a trustworthy and kind medical assistant. Always listen intently, respond with empathy, and guide the user with evidence-based suggestions that balance kindness and clarity.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "You are a trustworthy and kind medical assistant. Always listen intently, respond with empathy, and guide the user with evidence-based suggestions that balance kindness and clarity.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                }
            ]
        },
        {
            "round_number": 4,
            "matches": [
                {
                    "match_id": 15,
                    "prompt_a": "Act as a supportive and highly informed medical agent. Use a conversational and empathetic approach to gather symptom details, explain diagnoses kindly, and empower the user to take appropriate next steps.",
                    "prompt_b": "You are a trustworthy and kind medical assistant. Always listen intently, respond with empathy, and guide the user with evidence-based suggestions that balance kindness and clarity.",
                    "output_a": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "output_b": "Error: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?",
                    "winner": "You are a trustworthy and kind medical assistant. Always listen intently, respond with empathy, and guide the user with evidence-based suggestions that balance kindness and clarity.",
                    "judge_scores": [
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        },
                        {
                            "prompt_a": 0,
                            "prompt_b": 0
                        }
                    ]
                }
            ]
        }
    ],
    "champion": "You are a trustworthy and kind medical assistant. Always listen intently, respond with empathy, and guide the user with evidence-based suggestions that balance kindness and clarity."
}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Judges configuration
judge_agents: List[Judge] = [
    Judge(
        name="Correct Diagnosis",
        weight=3,
        prompt=(
            "You are an expert in medical diagnostics. Your role is to evaluate responses based on how accurate and "
            "evidence-based the diagnosis is, given the symptoms provided by the user. Pay close attention to whether "
            "the agent has identified plausible and medically sound explanations for the symptoms. You must prioritize "
            "scientific accuracy and alignment with current medical knowledge when making your judgments."
        ),
    ),
    Judge(
        name="User Empathy",
        weight=2,
        prompt=(
            "You are an evaluator of empathy in healthcare communication. Your role is to assess how understanding, "
            "compassionate, and supportive the agent’s response is. Consider whether the agent validates the user’s "
            "feelings, uses a kind and reassuring tone, and makes the user feel heard and cared for. Your priority is "
            "ensuring the user’s emotional well-being and comfort are addressed in the interaction."
        ),
    ),
    Judge(
        name="Ease of Understanding",
        weight=4,
        prompt=(
            "You are an expert in assessing clarity of communication. Your role is to evaluate how easy it is for a "
            "user to understand the agent’s response. Focus on whether the language used is simple, free of unnecessary "
            "jargon, and structured logically. Prioritize responses that break down complex medical concepts into terms "
            "that are accessible to a layperson."
        ),
    ),
    Judge(
        name="Clear Next Steps",
        weight=1,
        prompt=(
            "You are an evaluator of actionable guidance in healthcare communication. Your role is to assess how well "
            "the agent communicates the next steps the user should take. Consider whether the advice is clear, specific, "
            "and practical, ensuring the user knows exactly what to do to address their symptoms, whether it’s self-care, "
            "monitoring, or seeking professional medical help."
        ),
    ),
]


@app.get("/judges", response_model=List[Judge])
async def get_judges() -> Judge:
    return judge_agents


# Update the generate_output function to be async
async def generate_output(prompt: str, question: str) -> str:
    """Generates output for a given prompt and question using OpenAI API."""
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Question: {question}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# Update evaluate_outputs to be async
async def evaluate_outputs(output_a: str, output_b: str, question: str):
    """Uses judge agents to evaluate competing outputs."""
    scores_a = {}
    scores_b = {}

    async def evaluate_judge(judge):
        judge_prompt: str = (
            f"Question: {question}\n\nOutput A: {output_a}\nOutput B: {output_b}\n\n"
            "Evaluate both outputs and assign a score between 0-10 for each."
            "Return a JSON object with the following format: { 'prompt_a': <score>, 'prompt_b': <score> }"
        )
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": judge.prompt},
                    {"role": "user", "content": judge_prompt}
                ]
            )
            parsed_scores: Dict[str, int] = json.loads(response.choices[0].message.content)
            return judge.name, parsed_scores
        except Exception as e:
            print("Error: ", e)
            return judge.name, {"prompt_a": 0, "prompt_b": 0}

    # Run all judge evaluations in parallel
    judge_tasks = [evaluate_judge(judge) for judge in judge_agents]
    results = await asyncio.gather(*judge_tasks)
    
    for judge_name, scores in results:
        scores_a[judge_name] = scores["prompt_a"]
        scores_b[judge_name] = scores["prompt_b"]

    return scores_a, scores_b


# Update run_tournament to be async and handle parallel matches
@app.post("/tournament", response_model=TournamentResult)
async def run_tournament(input_data: TournamentInput) -> TournamentResult:
    question: str = input_data.question
    prompts: List[str] = [prompt for prompt in input_data.prompts if prompt.strip()]
    random.shuffle(prompts)

    rounds: List[Round] = []
    match_id: int = 1
    round_number: int = 1

    async with aiohttp.ClientSession() as session:
        while len(prompts) > 1:
            print(f"Round {round_number}")
            print(f"Prompts: {len(prompts)}")
            next_round: List[str] = []
            matches: List[Match] = []

            # Process each pair of prompts in parallel
            async def process_match(i: int):
                if i + 1 >= len(prompts):
                    return None
                
                prompt_a: str = prompts[i]
                prompt_b: str = prompts[i + 1]

                # Run both outputs in parallel
                output_a, output_b = await asyncio.gather(
                    generate_output(prompt_a, question),
                    generate_output(prompt_b, question)
                )

                scores_a, scores_b = await evaluate_outputs(output_a, output_b, question)

                weighted_score_a: int = sum(scores_a[j.name] * j.weight for j in judge_agents)
                weighted_score_b: int = sum(scores_b[j.name] * j.weight for j in judge_agents)

                winner: str = prompt_a if weighted_score_a > weighted_score_b else prompt_b

                return Match(
                    match_id=match_id + (i // 2),
                    prompt_a=prompt_a,
                    prompt_b=prompt_b,
                    output_a=output_a,
                    output_b=output_b,
                    winner=winner,
                    judge_scores=[
                        JudgeScore(judge=j, score=Score(prompt_a=scores_a[j.name], prompt_b=scores_b[j.name]))
                        for j in judge_agents
                    ],
                ), winner

            # Create tasks for all matches in this round
            match_tasks = [process_match(i) for i in range(0, len(prompts), 2)]

            match_results = await asyncio.gather(*match_tasks)

            # Process results
            for result in match_results:
                if result is not None:
                    match, winner = result
                    matches.append(match)
                    next_round.append(winner)
            
            if len(prompts) % 2 == 1:
                # Handle the last prompt in case of odd number
                next_round.append(prompts[-1])

            rounds.append(Round(round_number=round_number, matches=matches))
            prompts = next_round
            match_id += len(matches)
            round_number += 1

    result: TournamentResult = TournamentResult(rounds=rounds, champion=prompts[0])
    print("Tournament Result: ", result)
    return result