import os
import base64
from groq import Groq
import streamlit as st
from prompts import *

class IELTSTask2Evaluator:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama3-8b-8192"

    def evaluate_essay(self, essay_question, essay_content):
        score_prompt = t1_band
        return self._get_completion(score_prompt.format(essay_question, essay_content))

    def analyze_grammar(self, essay_content):
        gram_prompt = grammar
        return self._get_completion(gram_prompt.format(essay_content))

    def analyze_vocabulary(self, essay_content):
        vocab_prompt = vocabulary
        return self._get_completion(vocab_prompt.format(essay_content))

    def analyze_cohesion_coherence(self, essay_content):
        coh_coh_prompt = cohesion_coherence
        return self._get_completion(coh_coh_prompt.format(essay_content))

    def analyze_task_achievement(self, essay_question, essay_content):
        task_ach_prompt = task_response
        return self._get_completion(task_ach_prompt.format(essay_question, essay_content))

    def _get_completion(self, prompt):
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model
        )
        return response.choices[0].message.content


class IELTSTask2ExerciseGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama3-8b-8192"

    def generate_grammar_exercises(self, grammar_analysis, essay_content):
        # Fixed: Added the missing prompt template
        gram_exer_prompt = grammar_exercise
        return self._get_completion(gram_exer_prompt.format(grammar_analysis, essay_content))

    def generate_vocabulary_exercises(self, vocab_analysis):
        vocab_exer_prompt = vocabulary_exercise
        return self._get_completion(vocab_exer_prompt.format(vocab_analysis))

    def _get_completion(self, prompt):
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model
        )
        return response.choices[0].message.content


class IELTSTask1Evaluator:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.text_model = "llama3-8b-8192"
        self.vision_model = "llama-3.2-11b-vision-preview"

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_graph(self, image_path, question):
        base64_image = self.encode_image(image_path)
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": f"""Given this IELTS Task 1 question: {question}
                            
                            Please analyze the graph/chart/process diagram or map and:
                            1. List the key features that need to be described based on the question requirements
                            2. Identify the main trends, patterns, or comparisons required by the question
                            3. Note any significant data points that should be highlighted
                            4. Specify what should be included in the overview
                            5. Indicate what details should be included in the body paragraphs
                            
                            Provide your analysis in a structured format that can be used to evaluate student responses."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model=self.vision_model,
        )
        return response.choices[0].message.content
        
    def evaluate_task1_response(self, question, graph_analysis, written_response):
        # Fixed: Added the missing prompt template
        score_prompt = t1_band
        return self._get_completion(score_prompt.format(question, graph_analysis, written_response))

    def analyze_grammar(self, written_response):
        gram_prompt = grammar
        return self._get_completion(gram_prompt.format(written_response))

    def analyze_vocabulary(self, written_response):
        vocab_prompt = vocabulary
        return self._get_completion(vocab_prompt.format(written_response))

    def analyze_task_achievement(self, question, graph_analysis, written_response):
        task_ach_prompt = task_achievement
        return self._get_completion(task_ach_prompt.format(question, graph_analysis, written_response))

    def analyze_cohesion_coherence(self, written_response, graph_analysis):
        coh_coh_prompt = cohesion_coherence
        return self._get_completion(coh_coh_prompt.format(graph_analysis, written_response))
    
    def _get_completion(self, prompt):
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.text_model
        )
        return response.choices[0].message.content


class IELTSTask1ExerciseGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama3-8b-8192"

    def generate_grammar_exercises(self, grammar_analysis, essay_content):
        gram_exer_prompt = grammar_exercise
        return self._get_completion(gram_exer_prompt.format(grammar_analysis, essay_content))

    def generate_vocabulary_exercises(self, vocab_analysis):
        vocab_prompt = vocabulary_exercise
        return self._get_completion(vocab_prompt.format(vocab_analysis))

    def _get_completion(self, prompt):
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model
        )
        return response.choices[0].message.content


def llm_responder_t1(image_path, question, written_response):
    task1_evaluator = IELTSTask1Evaluator()
    task1_generator = IELTSTask1ExerciseGenerator()
    graph_analysis = task1_evaluator.analyze_graph(image_path, question)
    # Fixed: Added missing graph_analysis parameter
    general_analysis = task1_evaluator.evaluate_task1_response(question, graph_analysis, written_response)
    ga = task1_evaluator.analyze_grammar(written_response)
    lr = task1_evaluator.analyze_vocabulary(written_response)
    ta = task1_evaluator.analyze_task_achievement(question, graph_analysis, written_response)
    ga_exercise = task1_generator.generate_grammar_exercises(ga, written_response)
    lr_exercise = task1_generator.generate_vocabulary_exercises(lr)
    print('done')
    return general_analysis, ga, lr, ta, ga_exercise, lr_exercise


def llm_responder_t2(essay_question, essay_content):
    task2_evaluator = IELTSTask2Evaluator()
    task2_generator = IELTSTask2ExerciseGenerator()
    general_analysis = task2_evaluator.evaluate_essay(essay_question, essay_content)
    ga = task2_evaluator.analyze_grammar(essay_content)
    lr = task2_evaluator.analyze_vocabulary(essay_content)
    ta = task2_evaluator.analyze_task_achievement(essay_question, essay_content)
    ga_exercise = task2_generator.generate_grammar_exercises(ga, essay_content)
    lr_exercise = task2_generator.generate_vocabulary_exercises(lr)
    print('done')
    return general_analysis, ga, lr, ta, ga_exercise, lr_exercise


def llm_responder_t1(image_path, question, written_response):
    task1_evaluator = IELTSTask1Evaluator()
    task1_generator = IELTSTask1ExerciseGenerator()
    graph_analysis = task1_evaluator.analyze_graph(image_path, question)
    general_analysis = task1_evaluator.evaluate_essay(question, graph_analysis, written_response)
    ga =  task1_evaluator.analyze_grammar(written_response)
    lr =  task1_evaluator.analyze_vocabulary(written_response)
    ta =  task1_evaluator.analyze_task_achievement(question, graph_analysis, written_response)
