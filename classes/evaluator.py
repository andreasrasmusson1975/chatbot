"""
Module: evaluator

This module defines the Evaluator class, which facilitates automated testing and evaluation of a
local question-answering assistant (ManualAssistant) using GPT-4.1 via the OpenAI API as a judge
and question generator.

The module is intended for evaluating the factual and qualitative performance of local QA systems
against a trusted language model.
"""

# Perform necessary imports
import os
import json
import joblib
import pandas as pd
from pathlib import Path
from openai import OpenAI
from .manual_assistant import ManualAssistant


class Evaluator:
    """
    Evaluator class for benchmarking a local manual assistant (ManualAssistant)
    against GPT-4.1 using OpenAI's API.

    This class performs evaluation as follows:

    1. Loads a set of text chunks from a specified manual.
    2. Uses GPT-4.1 to generate a mix of answerable and unanswerable user questions.
    3. Gets answers to those questions from the local assistant.
    4. Uses GPT-4.1 again to score and justify the quality of the local answers.
    5. Produces a pandas DataFrame summarizing all the results.

    Attributes:
        manual_name (str): Name of the manual to evaluate.
        client (OpenAI): OpenAI client for GPT-4.1 communication.
        model_name (str): The model identifier used for GPT-based tasks.
        local_ma (ManualAssistant): The local assistant used to generate manual-based answers.
        records (list[dict]): A filtered and sorted list of manual chunks for context.
        questions (dict): A dictionary of generated [question, correct answer] pairs.
        question_and_answers (dict): A dictionary of [question, correct answer, local answer] triples.
        evaluation (dict): A dictionary of full evaluations, including scores and justifications.
        evaluation_df (pd.DataFrame): A DataFrame summarizing the evaluation for analysis or export.
    """
    def __init__(self, manual_name: str):
        """
        Initialize the Evaluator for a specific product manual.

        This method sets up the evaluation pipeline by:
        - Loading manual content from disk
        - Initializing the OpenAI client (GPT-4.1)
        - Creating a local ManualAssistant for querying manual content
        - Generating synthetic user questions and reference answers using GPT
        - Collecting local model responses to the generated questions
        - Running an automated evaluation to score the local answers

        Parameters:
            manual_name (str): The name or identifier of the manual to evaluate.
        """
        self.manual_name = manual_name
        
        # Initialize OpenAI client and choose the model name
        self.client = OpenAI(api_key=os.getenv('openai_api_key'))
        self.model_name = "gpt-4.1"

        # Initialize a manual assistant, fetch records from disk
        # and filter them to appropriate size.
        self.local_ma = ManualAssistant(manual_name)
        self.records = joblib.load(Path('vector_databases') / 'records.pkl')
        self.records = sorted(
            [x for x in self.records if x['manual'] == manual_name],
            key=lambda x: (x['path'], x['chunk'])
        )[:10]

        # Generate questions, answers and perform evaluation
        self.questions = self._generate_questions()
        self.question_and_answers = self._collect_local_answers(self.questions)
        self.evaluation = self._evaluate()
        self.evaluation_df = self._evaluation_to_df()

    def _run_gpt(self, prompt: str) -> str:
        """
        Sends a prompt to the OpenAI GPT model and returns the response.

        Parameters:
            prompt (str): The full prompt string to be sent to the model.

        Returns:
            str: The model's response as plain text, stripped of leading and trailing whitespace.
        """
        # Send the request to the model
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()

    def _generate_questions(self, n: int = 5) -> dict:
        """
        Generates a set of user questions and reference answers based on manual excerpts.

        Produces (n-2) answerable questions strictly grounded in the provided manual pages,
        and 2 additional questions for which the correct response is:
        "I'm afraid I can't find that in the manual."

        The output is expected to be a JSON dictionary where each key is a stringified integer,
        and each value is a list of two strings: [question, answer].

        Parameters:
            n (int): Total number of questions to generate (default is 5).

        Returns:
            dict: A dictionary mapping string keys ("1", "2", ...) to [question, answer] pairs.
        """
        # create an instruction string
        instructions = f"""
            Based only on the following manual pages, generate exactly {n-2} diverse and challenging 
            user questions a person might ask, along with accurate answers grounded strictly in the content.
            Also generate two questions, where the answers cannot be found in the manual excerpts. 
            **BE CAREFULL TO MAKE SURE** that the answers **CANNOT** be found in the manual for these last two questions. 
            For these last two questions, the answer should be: "I'm afraid I can't find that in the manual."

            Your output should be a **JSON dictionary**. Each key should be a string integer ("1", "2", ...) and 
            each value should be a list of two elements: [question_string, answer_string].

            Don't add any text before or after the JSON. Dont add any ```json or backticks or similar things.
            Here are the manual excerpts:
        """ + '\n'.join(x['text'] for x in self.records)

        # Send the prompt to the model and return the result as a dict.
        raw = self._run_gpt(instructions)
        return json.loads(raw)


    def _collect_local_answers(self, questions: dict) -> dict:
        """
        Uses the local ManualAssistant to answer a set of questions and collects the results.

        For each question in the input dictionary, retrieves the corresponding answer from
        the local model and stores it along with the original question and the reference answer.

        Parameters:
            questions (dict): A dictionary where each key is a stringified integer and each value
                            is a [question, reference_answer] list.

        Returns:
            dict: A dictionary where each key is the same as in the input, and each value is a list:
                [question, reference_answer, local_model_answer].
        """
        local_answers = {}
        # Iterate over the items in the questions dictionary
        # to get answers from the local manual assistant.
        for key, (question, correct_answer) in questions.items():
            local_response = self.local_ma.send_user_query(question)
            local_answers[key] = [question, correct_answer, local_response]
        return local_answers

    def _evaluate(self) -> dict:
        """
        Evaluates the quality of answers produced by the local model against reference answers.

        Sends a JSON-serialized dictionary containing [question, reference_answer, local_answer] entries
        to the GPT model, requesting an augmented dictionary that includes:
            4. A score from 1 to 5 assessing factual accuracy, relevance, and clarity.
            5. A brief justification for the score.

        The evaluation penalizes hallucinated answers and rewards accurate, clear responses.

        Returns:
            dict: A dictionary where each key is a stringified integer and each value is a list of:
                [question, reference_answer, local_answer, score (1-5), justification].
        """
        # Create the evaluation prompt
        evaluation_prompt = f"""
            I will give you a JSON dictionary. Each key is an integer string. Each value is a list with:

            1. A question
            2. A correct reference answer
            3. An answer from a local model

            Your task is to append two more elements to each list:

            4. A score from 1 to 5 where 5 is best. 
               The score should be based on
                    a. Whether the answer from the local model is factually accurate with regards to the manual. High accuracy gives higher score.
                    b. Whether a made up answer is given when the answer should have been "I'm afraid I can't find that in the manual.". If that is
                        the case a lower score should be given
                    c. Clarity
               
            5. A short justification for the score

            Return **only** a valid JSON dictionary. No explanations or markdown.

            Here is the input:

            {json.dumps(self.question_and_answers)}
        """
        # Send the prompt to the model and return the answer as a dict
        raw = self._run_gpt(evaluation_prompt)
        return json.loads(raw)

    def _evaluation_to_df(self):
        """
        Converts the evaluation dictionary into a structured pandas DataFrame.

        Each record in the evaluation dictionary contains:
            - The question
            - The reference (ground-truth) answer
            - The answer from the local manual assistant
            - A numerical score (1-5)
            - A textual justification for the score

        These are transformed into a DataFrame with corresponding columns, along with the manual name
        to enable identification across evaluations.

        Returns:
            pd.DataFrame: A DataFrame with columns:
                ['Manual', 'Question', 'Reference answer', 'Local answer', 'Score', 'Motivation']
        """
        # Iterate over the items in the evaluation dict and build a dataframe from it
        records = []
        for key, value in self.evaluation.items():
            records.append({
                'Manual': self.manual_name,
                'Question': value[0],
                'Reference answer': value[1],
                'Local answer': value[2],
                'Score': value[3],
                'Motivation': value[4]
            })
        return pd.DataFrame(records)
