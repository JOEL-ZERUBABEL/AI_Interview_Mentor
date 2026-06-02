'''
1   Conversation Memory	Remembers previous messages in the current chat session.
2	Token Management Counts and manages tokens to control cost and context size.
3	Intent Detection & Routing	Detects user intent and switches AI behavior/mode.
4	Evaluation Engine	Scores and analyzes interview answers with feedback.
5	Persistent Memory & Analytics	Stores user performance and progress across sessions.
6	Resume Analyzer	Reads resumes and generates personalized interview questions.
8	Code Evaluator & Teaching Engine	Reviews code, explains mistakes, and teaches optimization.
'''
from groq import Groq
import re, json
import tiktoken
import json
from dotenv import load_dotenv
import PyPDF2
from docx import Document
from pypdf import PdfReader
import os
load_dotenv()
api_key=os.getenv('GROQ_API_KEY')
client=Groq(api_key=api_key)

class AT_Tutor:
    def __init__(self):
        self.tokens=tiktoken.get_encoding('cl100k_base')
        self.instant='llama-3.1-8b-instant'
        self.versatile='llama-3.3-70b-versatile'
        self.precise_versatile='llama-3.3-70b-versatile'
        self.message=[{'role':'system','content':'You are sincere AI Tutor'}] 
        self.cur='hr'
        self.analytics=self.load_history()

    def tokens_manager(self,text):
        tokens=self.tokens.encode(text)
        return len(tokens)    
    
    def conversation_memory(self,userinput): 
        self.message.append({"role":'user','content':userinput})
        model=client.chat.completions.create(model=self.instant,messages=self.message,temperature=0.7)
        ai_reply=model.choices[0].message.content
        self.message.append({"role":'system','content':ai_reply})
        return ai_reply
    
    
    def select_behaviour(self,mode,message):
        MODES={'hr':"""you are a professional HR interviewer  Ask behavioral questions.

                Evaluate communication skills,
                confidence, and clarity.

                Be friendly and professional.
                """,

                "dsa":
                """
                You are a strict FAANG DSA interviewer.

                Ask coding and algorithm questions.

                Focus on:
                - optimization
                - time complexity
                - edge cases

                Push the candidate deeply.
                """,

                "system_design":
                """
                You are a senior system design interviewer.

                Ask scalable architecture questions.

                Focus on:
                - scalability
                - databases
                - load balancing
                - caching"""}
        #remember -> select mode in call
        if mode not in MODES():
            mode='hr'
        prompt=MODES[mode]
        
        message.append({'role':'user',"content":prompt})
        model=client.chat.completions.create(model=self.versatile,messages=[{'role':'system','content':prompt}],temperature=0.5)
        ai_reply=model.choices[0].message.content
        return ai_reply
    
    #cur_mode='hr'
    #module 3 Teach AI to switch behavior.
    def switch_mode(self,mode):
        MODES = {

            "hr":"""
            You are a professional HR interviewer.

            Ask behavioral and communication questions.

            Be professional and friendly.""",

            "dsa":"""
            You are a strict FAANG DSA interviewer.

            Focus on:
                    - algorithms
                    - optimization
                    - edge cases
                    - complexity analysis
                    """,

            "system_design":
            """
            You are a senior system design interviewer.

            Focus on:
            - scalability
            - databases
            - distributed systems"""
            }
        
        
        if mode in MODES:
            self.cur_mode=mode 
            return f"switched mode{mode}"
        return f'invalid mode'
            
        
    def evaluation(self, question, answer):
        prompt = f"""
            You are a coding interviewer.

            Question:
        {question}

        Candidate Answer:
        {answer}

    Evaluate the answer.

    Return ONLY JSON.

    {{
        "technical":0,
        "communication":0,
        "optimization":0,
        "strengths":"",
        "weaknesses":"",
        "suggestions":""
    }}
    """

        model = client.chat.completions.create(
        model=self.precise_versatile,
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.1)

        ai_reply = model.choices[0].message.content

        try:
            ai_reply = ai_reply.replace("```json", "").replace("```", "").strip()
            result = json.loads(ai_reply)
            return result
        except Exception as e:
            print("JSON ERROR")
            print(ai_reply)
            return {
            "technical": 0,
            "communication": 0,
            "optimization": 0,
            "strengths": "Parsing Failed",
            "weaknesses": "Model returned invalid JSON",
            "suggestions": "Check console output",
            "error": str(e)  
        }

    
    def history(self):
        #store history
        with open('history.json','w') as file:
            json.dump(self.analytics,file,indent=4)
        #read history
        
        return f'History Saved'
    
    def load_history(self):
        if os.path.exists('history.json'):
            with open('history.json','r') as file:
                return json.load(file)
        return {

        "technical":[],

        "communication":[],

        "optimization":[] }
    
    def resume(self,resume,refinement):
        resume=resume.strip().strip('"')
        text=''
        if resume.endswith('pdf'):
            reader=PdfReader(resume)
            for page in reader.pages:
                page_text=page.extract_text()
                if page_text:
                    text+=page_text+'\n'

        elif resume.endswith('.docx'):
            doc=Document(resume)
            for para in doc:
                text+=para.text+'\n'

        elif resume.endswith('.txt'):
            with open(resume,'r',encoding='utf-8') as file:
                text=file.read()

        else:
            return 'Unsuported file format'
        
        MODES=f'''You are the Resume analyser insist improvements based on resume ,
        the resume is {text} and provide improvement in {refinement} give 
        
        Analyse:

        1. ATS Score
        2. Missing Skills
        3. Resume Strengths
        4. Weaknesses
        5. Recruiter Impression
        6.Improvement Suggestions

        
        
        '''

       
        model=client.chat.completions.create(model=self.precise_versatile,messages=[{'role':'system','content':MODES}],temperature=0.3)
        history=model.choices[0].message.content
        return history
    
    def code_review(self,user_code):

        prompt=f"""

        You are a FAANG coding mentor.

        Analyze:

        {user_code}

        Give:   1. What code does

        2. Mistakes

        3. Time Complexity

        4. Space Complexity

        5. Optimized Solution

        6. Dry Run


    
        """

        model=client.chat.completions.create(model=self.versatile,messages=[
            {"role":"user","content":prompt}],temperature=0.3
        )

        ai_reply=model.choices[0].message.content
        return ai_reply
    
    def calculate_score(self,technical,communication,optimization):
        self.analytics['technical'].append(technical)
        self.analytics['communication'].append(communication)
        self.analytics['optimization'].append(optimization)

        avg_technical=sum(self.analytics['technical'])/len(self.analytics['technical'])
        avg_communication=sum(self.analytics['communication'])/len(self.analytics['communication'])
        avg_optimization = sum(self.analytics["optimization"]) / len(self.analytics["optimization"])
        overall = (

        avg_technical +
        avg_communication +
        avg_optimization)/3

        return {
        "technical":round(avg_technical,2),
        "communication":round(avg_communication,2),
        "optimization":round(avg_optimization,2),
        "overall":round(overall,2)  
        }
    
    def generate_question(self,topic):
        prompt=f"""
        Generate one interview question from:
        {topic}

        Difficulty: Medium=
        Give only question.

        """

        model=client.chat.completions.create(
        model=self.instant,
        messages=[
            {"role":"user","content":prompt
            }
            ]
                )

        return model.choices[0].message.content   

    def safe_parse(self,ai_reply):
        try:
            return json.loads(ai_reply)
        except:
        # Try to extract JSON substring
            match = re.search(r"\{.*\}", ai_reply, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except:
                    pass
            return {
                "technical": 0,
            "communication": 0,
            "optimization": 0,
            "strengths": "Parsing Failed",
            "weaknesses": "Model returned invalid JSON",
            "suggestions": "Check console output"
            }

    
from main import AT_Tutor 


def run_cli():
    ai_tutor = AT_Tutor()

    while True:
        print("\n===== AI TUTOR =====")
        print("1. Chat")
        print("2. Switch Mode")
        print("3. Resume Analysis")
        print("4. Code Review")
        print("5. Evaluation")
        print("6. Save History")
        print("7. Exit")

        choice = input("\nEnter Choice: ")

        if choice == "1":
            user_input = input("Ask: ")
            reply = ai_tutor.conversation_memory(user_input)
            print("\nAI RESPONSE:\n")
            print(reply)

        elif choice == "2":
            mode = input("Enter Mode (hr/dsa/system_design): ")
            result = ai_tutor.switch_mode(mode)
            print(result)

        elif choice == "3":
            resume_path = input("Resume Path: ")
            refinement = input("Any specific improvement needed: ")
            result = ai_tutor.resume(resume_path, refinement)
            print(result)

        elif choice == "4":
            print("\nPaste Code (END to stop)\n")
            code = ""
            while True:
                line = input()
                if line == "END":
                    break
                code += line + "\n"
            result = ai_tutor.code_review(code)
            print(result)

        elif choice == "5":
            topic = input('Topic(Array/LinkedList/Tree/DP/Graph): ')
            question = ai_tutor.generate_question(topic)
            print('\nQuestions:\n')
            print(question)
            answer = input("Answer: ")
            result = ai_tutor.evaluation(question, answer)
            print('\nEVALUATION:\n')
            print(result)

        elif choice == "6":
            print(ai_tutor.analytics)
            save = ai_tutor.history()
            print(save)

        elif choice == "7":
            print("Bye Maame")
            break

        else:
            print("Invalid Choice")

if __name__ == "__main__":
    run_cli()
