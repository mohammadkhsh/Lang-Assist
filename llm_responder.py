import os
import base64
from groq import Groq

class IELTSTask2Evaluator:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama3-8b-8192"

    def evaluate_essay(self, essay_question, essay_content):
        score_prompt = """ Provide the scores for the following IELTS task 2 essay in terms of Cohesion & Coherence, Task Achievement, Lexical Resouces and Grammatical Range & Accuracy critera. The scores should be in IELTS framework. Each criterion should be scored between 1 to 9 and should be integer. E.g. 5.5 is not acceptable! For each criteria that you score also provide 3 different comments using the following band descriptors and by referncing the essay.

            IELTS Scoring band descriptor: 
            Task Achievement: Score 9: •	fully addresses all parts of the task
                                       •	presents a fully developed position in answer to the question with relevant, fully extended and well supported ideas

                                    8:  •	sufficiently addresses all parts of the task
                                        •	presents a well-developed response to the question with relevant, extended and supported ideas

                                    7:  •	addresses all parts of the task
                                        •	presents a clear position throughout the response
                                        •	presents, extends and supports main ideas, but there may be a tendency to over-generalise and/or supporting ideas may lack focus
                                    
                                    6:	•	addresses all parts of the task although some parts may be more fully covered than others
                                        •	presents a relevant position although the conclusions may become unclear or repetitive
                                        •	presents relevant main ideas but some may be inadequately developed/unclear
                                    
                                    5:	•	addresses the task only partially; the format may be inappropriate in places
                                        •	expresses a position but the development is not always clear and there may be no conclusions drawn
                                        •	presents some main ideas but these are limited and not sufficiently developed; there may be irrelevant detail
                                    
                                    4:	•	responds to the task only in a minimal way or the answer is tangential; the format may be inappropriate
                                        •	presents a position but this is unclear
                                        •	presents some main ideas but these are difficult to identify and may be repetitive, irrelevant or not well supported
                                    
                                    3:	•	does not adequately address any part of the task
                                        •	does not express a clear position
                                        •	presents few ideas, which are largely undeveloped or irrelevant
                                    
                                    2:	•	barely responds to the task
                                        •	does not express a position
                                        •	may attempt to present one or two ideas but there is no development
                                    1:	•	answer is completely unrelated to the task

             Cohesion and Coherence: Score 9:   •	uses cohesion in such a way that it attracts no attention
                                                •	skilfully manages paragraphing
                                            
                                            
                                    Score 8:       •	sequences information and ideas logically
                                            •	manages all aspects of cohesion well
                                                •	uses paragraphing sufficiently and appropriately
                                                
                                               Score 7:  •	logically organises information and ideas; there is clear progression throughout
                                                •	uses a range of cohesive devices appropriately although there may be some under-/over-use
                                                •	presents a clear central topic within each paragraph
                                                
                                            Score 6:     •	arranges information and ideas coherently and there is a clear overall progression
                                                •	uses cohesive devices effectively, but cohesion within and/or between sentences may be faulty or mechanical
                                                •	may not always use referencing clearly or appropriately
                                                •	uses paragraphing, but not always logically
                                                
                                            Score 5:     •	presents information with some organisation but there may be a lack of overall progression
                                                •	makes inadequate, inaccurate or over-use of cohesive devices
                                                •	may be repetitive because of lack of referencing and substitution
                                                •	may not write in paragraphs, or paragraphing may be inadequate
                                                                                            
                                            Score 4:     •	presents information and ideas but these are not arranged coherently and there is no clear progression in the response
                                                •	uses some basic cohesive devices but these may be inaccurate or repetitive
                                                •	may not write in paragraphs or their use may be confusing

                                           Score 3:     •	does not organise ideas logically
                                                •	may use a very limited range of cohesive devices, and those used may not indicate a logical relationship between ideas
                                                
                                             Score 2:    •	has very little control of organisational features
                                                
                                              Score 1:   •	fails to communicate any message
                                            

            Lexical Resouce:    Score 9:	•	uses a wide range of vocabulary with very natural and sophisticated control of lexical features; rare minor errors occur only as 'slips'
                                
                                
                                Score 8:	•	uses a wide range of vocabulary fluently and flexibly to convey precise meanings
                                            •	skilfully uses uncommon lexical items but there may be occasional inaccuracies in word choice and collocation
                                            •	produces rare errors in spelling and/or word formation
                                
                                
                                
                                Score 7:	•	uses a sufficient range of vocabulary to allow some flexibility and precision
                                            •	uses less common lexical items with some awareness of style and collocation
                                            •	may produce occasional errors in word choice, spelling and/or word formation
                                
                                
                                Score 6:	•	uses an adequate range of vocabulary for the task
                                            •	attempts to use less common vocabulary but with some inaccuracy
                                            •	makes some errors in spelling and/or word formation, but they do not impede communication
                                
                                
                                Score 5:	•	uses a limited range of vocabulary, but this is minimally adequate for the task
                                •	may make noticeable errors in spelling and/or word formation that may cause some difficulty for the reader
                                
                                
                                Score 4:	•	uses only basic vocabulary which may be used repetitively or which may be inappropriate for the task
                                •	has limited control of word formation and/or spelling; errors may cause strain for the reader
                                
                                
                                Score 3:	•	uses only a very limited range of words and expressions with very limited control of word formation and/or spelling
                                •	errors may severely distort the message
                                
                                
                                Score 2:	•	uses an extremely limited range of vocabulary; essentially no control of word formation and/or spelling
                                
                                
                                Score 1:	•	can only use a few isolated words





        Grammatical Range and Accuracy:  Score 9:	•	uses a wide range of structures with full flexibility and accuracy; rare minor errors occur only as 'slips'
                                        
                                        
                                        Score 8:	•	uses a wide range of structures
                                        •	the majority of sentences are error-free
                                        •	makes only very occasional errors or inappropriacies
                                        
                                        
                                        Score 7:	•	uses a variety of complex structures
                                        •	produces frequent error-free sentences
                                        •	has good control of grammar and punctuation but may make a few errors
                                        
                                        
                                        Score 6:	•	uses a mix of simple and complex sentence forms
                                        •	makes some errors in grammar and punctuation but they rarely reduce communication
                                        
                                        
                                        Score 5:	•	uses only a limited range of structures
                                        •	attempts complex sentences but these tend to be less accurate than simple sentences
                                        •	may make frequent grammatical errors and punctuation may be faulty; errors can cause some difficulty for the reader
                                        
                                        
                                        Score 4:	•	uses only a very limited range of structures with only rare use of subordinate clauses
                                        •	some structures are accurate but errors predominate, and punctuation is often faulty
                                        
                                        
                                        Score 3:	•	attempts sentence forms but errors in grammar and punctuation predominate and distort the meaning
                                        
                                        
                                        Score 2:	•	cannot use sentence forms except in memorised phrases
                                        
                                        
                                        Score 1:	•	cannot use sentence forms at all
            
            Essay Question: {}
            Essay: {}
            """
        return self._get_completion(score_prompt.format(essay_question, essay_content))

    def analyze_grammar(self, essay_content):
        gram_prompt = """ Provide a grammatical analysis of the following essay with respect to the content a B1 leanrner must know. Provide all the grammars used and their accuracy pecentage. E.g. "Simple Present: 70%". Also provide comments for inaccurate structures. Don't give me any exercises.

    Essay: {}
    """
        return self._get_completion(gram_prompt.format(essay_content))

    def analyze_vocabulary(self, essay_content):
        vocab_prompt = """ Provide the lexical errors and provide their correct forms. For each of the vocabulary related to the context of the essay that you think could be improved, give suggesions. Provide full sentence examples for these suggestions.

    Essay: {}
    """
        return self._get_completion(vocab_prompt.format(essay_content))

    def analyze_cohesion_coherence(self, essay_content):
        coh_coh_prompt = """ Evaluate the cohesion and coherence of essay based on the following aspects. DO NOT SCORE THEM:

    - paraphrasing ability
    - logical sequencing of ideas
    - use and accuracy of cohesive devices
    - existence of a clear central topic in each paragrpah
    - correct paragraphing
    
    
    Essay: {}
    """
        return self._get_completion(coh_coh_prompt.format(essay_content))

    def analyze_task_achievement(self, essay_question, essay_content):
        task_ach_prompt = """ Evaluate the Task Achievement factor of this IELTS essay based on the following question and essay. Do NOT provide scores. Just mention analysis and how it could be imporved.

    Question: {}
    
    
    Essay: {}
    """
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
        gram_exer_prompt = """ Based on the content of the grammar analysis provided in JSON format, make 4 different exercise types and provide 10 exercises for each. All the items should be in the context of the essay. Avoid providing exercises that are exact replica of the candidates' mistakes.

    Grammar Analysis: {}
    
    Essay: {}
    """
        return self._get_completion(gram_exer_prompt.format(grammar_analysis, essay_content))

    def generate_vocabulary_exercises(self, vocab_analysis):
        vocab_exer_prompt = """ Based on the lexical errors, provide exercises in the same context of the essay. Avoid providing exercises that are exact replica of the candidates' mistakes.

    Lexical Errors: {}
    """
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

    def analyze_graph(self, image_path):
        """Analyzes the graph/chart provided for Task 1"""
        base64_image = self.encode_image(image_path)
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Please analyze this graph/chart and list the key features that should be described in an IELTS Task 1 response:"},
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

    def evaluate_task1_response(self, graph_analysis, written_response):
        score_prompt = """Provide the scores for the following IELTS Task 1 essay based on the graph analysis provided and the written response. Score in terms of Task Achievement, Coherence and Cohesion, Lexical Resource, and Grammatical Range & Accuracy criteria. The scores should be in IELTS framework. Each criterion should be scored between 1 to 9 and should be integer. E.g. 5.5 is not acceptable! For each criteria that you score, provide 3 different comments using the following band descriptors and by referencing both the key features of the graph and how well they were described in the response.

IELTS Task 1 Band Descriptors:

Band 9:
• Fully satisfies all requirements of the task
• Clearly presents a fully developed response
• Uses cohesion in such a way that it attracts no attention
• Skilfully manages paragraphing
• Uses a wide range of vocabulary with very natural and sophisticated control of lexical features; rare minor errors occur only as 'slips'
• Uses a wide range of structures with full flexibility and accuracy; rare minor errors occur only as 'slips'

Band 8:
• Covers all requirements of the task sufficiently
• Presents, highlights and illustrates key features/bullet points clearly and appropriately
• Sequences information and ideas logically
• Manages all aspects of cohesion well
• Uses paragraphing sufficiently and appropriately
• Uses a wide range of vocabulary fluently and flexibly to convey precise meanings
• Skilfully uses uncommon lexical items but there may be occasional inaccuracies in word choice and collocation
• Produces rare errors in spelling and/or word formation
• Uses a wide range of structures
• The majority of sentences are error-free
• Makes only very occasional errors or inappropriacies

Band 7:
• Covers the requirements of the task
• Presents a clear overview of main trends, differences or stages
• Clearly presents and highlights key features/bullet points but could be more fully extended
• Logically organises information and ideas; there is clear progression throughout
• Uses a range of cohesive devices appropriately although there may be some under-/over-use
• Uses a sufficient range of vocabulary to allow some flexibility and precision
• Uses less common lexical items with some awareness of style and collocation
• May produce occasional errors in word choice, spelling and/or word formation
• Uses a variety of complex structures
• Produces frequent error-free sentences
• Has good control of grammar and punctuation but may make a few errors

Band 6:
• Addresses the requirements of the task
• Presents an overview with information appropriately selected
• Presents and adequately highlights key features/bullet points but details may be irrelevant, inappropriate or inaccurate
• Arranges information and ideas coherently and there is a clear overall progression
• Uses cohesive devices effectively, but cohesion within and/or between sentences may be faulty or mechanical
• May not always use referencing clearly or appropriately
• Uses an adequate range of vocabulary for the task
• Attempts to use less common vocabulary but with some inaccuracy
• Makes some errors in spelling and/or word formation, but they do not impede communication
• Uses a mix of simple and complex sentence forms
• Makes some errors in grammar and punctuation but they rarely reduce communication

Band 5:
• Generally addresses the task; the format may be inappropriate in places
• Recounts detail mechanically with no clear overview; there may be no data to support the description
• Presents, but inadequately covers, key features/bullet points; there may be a tendency to focus on details
• Presents information with some organisation but there may be a lack of overall progression
• Makes inadequate, inaccurate or over-use of cohesive devices
• May be repetitive because of lack of referencing and substitution
• Uses a limited range of vocabulary, but this is minimally adequate for the task
• May make noticeable errors in spelling and/or word formation that may cause some difficulty for the reader
• Uses only a limited range of structures
• Attempts complex sentences but these tend to be less accurate than simple sentences
• May make frequent grammatical errors and punctuation may be faulty; errors can cause some difficulty for the reader

Band 4:
• Attempts to address the task but does not cover all key features/bullet points; the format may be inappropriate
• May confuse key features/bullet points with detail; parts may be unclear, irrelevant, repetitive or inaccurate
• Presents information and ideas but these are not arranged coherently and there is no clear progression
• Uses some basic cohesive devices but these may be inaccurate or repetitive
• Uses only basic vocabulary which may be used repetitively or which may be inappropriate for the task
• Has limited control of word formation and/or spelling; errors may cause strain for the reader
• Uses only a very limited range of structures with only rare use of subordinate clauses
• Some structures are accurate but errors predominate, and punctuation is often faulty

Band 3:
• Fails to address the task, which may have been completely misunderstood
• Presents limited ideas which may be largely irrelevant/repetitive
• Does not organise ideas logically
• May use a very limited range of cohesive devices, and those used may not indicate a logical relationship between ideas
• Uses only a very limited range of words and expressions with very limited control of word formation and/or spelling
• Errors may severely distort the message
• Attempts sentence forms but errors in grammar and punctuation predominate and distort the meaning

Band 2:
• Answer is barely related to the task
• Has very little control of organisational features
• Uses an extremely limited range of vocabulary; essentially no control of word formation and/or spelling
• Cannot use sentence forms except in memorised phrases

Band 1:
• Answer is completely unrelated to the task
• Fails to communicate any message
• Can only use a few isolated words
• Cannot use sentence forms at all

Band 0:
• Does not attend
• Does not attempt the task in any way
• Writes a totally memorised response

Graph Analysis: {}
Written Response: {}
"""
        return self._get_completion(score_prompt.format(graph_analysis, written_response))

    def analyze_grammar(self, written_response):
        gram_prompt = """Provide a grammatical analysis of the following Task 1 response with respect to describing trends, comparisons, and data. Provide all the grammars used and their accuracy percentage. E.g. "Past tense: 70%". Also provide comments for inaccurate structures. Focus especially on:
- Tense usage for trends
- Comparative structures
- Passive voice
- Articles with data
- Prepositions with trends

Response: {}
"""
        return self._get_completion(gram_prompt.format(written_response))

    def analyze_vocabulary(self, written_response):
        vocab_prompt = """Analyze the vocabulary used in this Task 1 response, focusing on:
- Language for describing trends
- Comparison vocabulary
- Data reporting vocabulary
- Graph/chart-specific terminology
Provide suggestions for improvement with examples in similar contexts.

Response: {}
"""
        return self._get_completion(vocab_prompt.format(written_response))

    def analyze_task_achievement(self, graph_analysis, written_response):
        task_ach_prompt = """Compare the key features identified in the graph analysis with how they were covered in the written response. Evaluate:
- Overview presence and quality
- Key feature selection
- Data accuracy
- Trend description completeness
Do NOT provide scores, only analysis and suggestions for improvement.

Graph Analysis: {}
Written Response: {}
"""
        return self._get_completion(task_ach_prompt.format(graph_analysis, written_response))

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
        gram_exer_prompt = """ Based on the content of the grammar analysis provided in JSON format, make 4 different exercise types and provide 10 exercises for each. All the items should be in the context of the essay. Avoid providing exercises that are exact replica of the candidates' mistakes.

    Grammar Analysis: {}
    
    Essay: {}
    """
        return self._get_completion(gram_exer_prompt.format(grammar_analysis, essay_content))
    
    def generate_graph_description_exercises(self, graph_analysis):
        exercise_prompt = """Based on the graph analysis provided, create exercises to practice:
1. Writing overviews (1 exercise)
2. Describing trends (1 exercise)
3. Comparing data points (1 exercises)
4. Selecting key features (1 exercises)

Keep all exercises relevant to the graph context.

Graph Analysis: {}
"""
        return self._get_completion(exercise_prompt.format(graph_analysis))

    def generate_vocabulary_exercises(self, vocab_analysis):
        vocab_prompt = """Create targeted vocabulary exercises for Task 1 writing based on the vocabulary analysis. Include:
1. Trend description vocabulary
2. Comparison language
3. Data reporting phrases
4. Graph-specific terminology

Analysis: {}
"""
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
    graph_analysis = task1_evaluator.analyze_graph(image_path)
    general_analysis = task1_evaluator.evaluate_task1_response(graph_analysis, written_response)
    ga =  task1_evaluator.analyze_grammar(written_response)
    lr =  task1_evaluator.analyze_vocabulary(written_response)
    ta =  task1_evaluator.analyze_task_achievement(graph_analysis, written_response)
    ga_exercise = task1_generator.generate_grammar_exercises(ga, written_response)
    lr_exercise = task1_generator.generate_graph_description_exercises(graph_analysis)
    
    return general_analysis, ga, lr, ta, ga_exercise, lr_exercise
