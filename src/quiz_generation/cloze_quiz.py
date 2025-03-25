from quiz_generation.base_quiz_gen_class import BaseQuizModel
from typing import Tuple, List
from LLM.LLMResponse import get_response

# Global variables for database columns
WORD_COL = "word"
MEANING_COL = "meaning"
PROMPT_BASE = "주어진 단어에 대하여, 영어로 쓰인, 한국인 사용자가 풀 수 있는 빈칸 퀴즈를 만들어줘."\
                "각 단어 당 하나의 문제를 만들어줘."\
                "퀴즈 페어를 제외하고는 아무것도 출력하지 마."\
                "[input word format]: \"word1;word2;word3;...\" "\
                "[output format]: \"Q:question;A:answer(newline)...\" "\
                "[Example]: \"Q:His behavior was clearly ______, driven by a deep-seated need for attention;A:pathological\" "\
                "[words]:"


class ClozeQuizModel(BaseQuizModel):
    def __init__(self, db, APIKEY=None):
        super().__init__(db)
        self.pairs = []
        self.current_index = 0
        self.APIKEY = APIKEY
        self.db = db
        self._parse_db(db)
    
    def _parse_db(self, db):
        self.words = db[WORD_COL].tolist()
        self.meanings = db[MEANING_COL].tolist()
        self._create_pairs()

    def _create_pairs(self):
        # Create the prompt using the current words
        prompt = self.__create_prompt()
        
        # Get the response from the LLM
        response = get_response(prompt, "gemini-2.0-flash", self.APIKEY)
        
        # Parse the response to get question-answer pairs
        qa_pairs = self.__parse_llm_response(response)
        
        # Create quiz pairs
        for question, answer in qa_pairs:
            self.pairs.append((question, answer, "hint"))

    def get(self) -> List[Tuple[str, str, str]]:
        return self.pairs
    
    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index >= len(self.pairs):
            raise StopIteration
        pair = self.pairs[self.current_index]
        self.current_index += 1
        return pair 
    
    def __create_prompt(self) -> str:
        """
        Creates a complete prompt from the quiz pairs.
        
        Returns:
            str: A formatted string containing all questions.
        """
        prompt = PROMPT_BASE
        for word in self.words:
            prompt += f"{word};\n"
        return prompt.strip()

    def __parse_llm_response(self, response: str) -> List[Tuple[str, str]]:
        """
        Parses the response from the LLM to extract question-answer pairs.
        
        Args:
            response (str): The response string from the LLM.
        
        Returns:
            List[Tuple[str, str]]: A list of tuples containing (question, answer).
        """
        qa_pairs = []
        lines = response.strip().split('\n')
        for line in lines:
            if line.startswith("Q:") and ";A:" in line:
                q, a = line.split(';A:')
                qa_pairs.append((q.replace('Q:', '').strip(), a.strip()))
        return qa_pairs 