from fsrs import Scheduler, Card, Rating, ReviewLog
from datetime import datetime, timezone, timedelta
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
from config import CLAUDE_API_KEY, CARDS_CHEKER
import os

class FlashCard:
    def __init__(self, question: str, answer: str, card: Card = None):
        self.question = question
        self.answer = answer
        self.card = Card() if card is None else card
        self.llm = ChatAnthropic(api_key=CLAUDE_API_KEY, model_name="claude-3-5-sonnet-20240620", max_tokens=300)

    def get_card(self):
        return {
            "_id": self.card.card_id,
            "front_card": self.question,
            "back_card": self.answer,
            "flashcard_data": self.card.to_dict()
        }

    def check_answer(self, user_answer: str):
        chek = PromptTemplate(
                input_variables=['question', 'complete_answer', 'user_answer'],
                template=CARDS_CHEKER
            )
        cheker_chain = chek | self.llm | StrOutputParser()

        response = cheker_chain.invoke({'question': self.question, 'complete_answer': self.answer, 'user_answer': user_answer})

        # Parse the response to extract evaluation, score, and expand
        evaluation = response.split("<evaluation>")[1].split("</evaluation>")[0].strip()
        score = int(response.split("<score>")[1].split("</score>")[0].strip())
        expand = response.split("<expand>")[1].split("</expand>")[0].strip()

        return evaluation, score, expand

    def review(self):
        results = self.check_answer()
        evaulation = results[0]
        score = results[1]
        expand = results[2]
        print(evaulation)
        print(expand)

        # Determine rating based on score
        if score >= 90:
            rating = Rating(4)
        elif 70 <= score < 90:
            rating = Rating(3)
        elif 50 <= score < 70:
            rating = Rating(2)
        else:
            rating = Rating(1)
        
        return rating
    
scheduler = Scheduler(
    parameters = (
            0.4072,
            1.1829,
            3.1262,
            15.4722,
            7.2102,
            0.5316,
            1.0651,
            0.0234,
            1.616,
            0.1544,
            1.0824,
            1.9813,
            0.0953,
            0.2975,
            2.2042,
            0.2407,
            2.9466,
            0.5034,
            0.6567,
        ),
    desired_retention = 0.9,
    learning_steps = (timedelta(minutes=1), timedelta(minutes=10)),
    relearning_steps = (timedelta(minutes=10),),
    maximum_interval = 365,
    enable_fuzzing = True
)
'''def main():
    cards_list = []
    cards_list += os.listdir('save_cards')
    for i in cards_list:
        print(i)
    card_path = f'save_cards/{cards_list[0]}'
    print(card_path)
    with open(card_path, "r") as file:
        data = json.load(file)
        flashcard = FlashCard(data['question'], data['answer'], Card.from_dict(data['card_info']))
        r = flashcard.review()
        flashcard.card, review_log = scheduler.review_card(flashcard.card, r)
        print(f"Card rated {review_log.rating} at {review_log.review_datetime}")

        due = flashcard.card.due

        card_dict = {
            "question":flashcard.question,
            "answer":flashcard.answer,
            "card_info": flashcard.card.to_dict()
        }
        print(card_dict)
    with open(card_path, "w") as file:
        json.dump(card_dict, file, sort_keys=True, indent=2)

if __name__ == "__main__":
    main()'''