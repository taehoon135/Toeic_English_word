from quiz_generation.base_quiz_gen_class import BaseQuizModel
from typing import Tuple, List

# Global variables for database columns
WORD_COL = "word"
MEANING_COL = "meaning"


class RainQuizModel(BaseQuizModel):
    def __init__(self, db):
        super().__init__(db)
        self.pairs = []
        self.current_index = 0
        self._parse_db(db)
    
    def _parse_db(self, db):
        self.words = db[WORD_COL].tolist()
        self.meanings = db[MEANING_COL].tolist()
        self._create_pairs()

    def _create_pairs(self):
        for word, meaning in zip(self.words, self.meanings):
            question = word
            self.pairs.append((question, meaning, "hint"))

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