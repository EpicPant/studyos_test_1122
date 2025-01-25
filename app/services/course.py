from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
import asyncio
from services.config import PARTS_PROMT, CARDS_PROMT, BORDERLINES_PROMT, CARDS_PROMT2
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
import json
from dotenv import load_dotenv
import os

load_dotenv()

DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')


class Course:
    def __init__(self, course_file):
        self.course = course_file
        self.llm = ChatAnthropic(api_key=CLAUDE_API_KEY, model_name="claude-3-5-sonnet-20240620", max_tokens=8192)
        self.dg_client = DeepgramClient(DEEPGRAM_API_KEY)

    def get_transcript(self):
        try:
            with open(self.course, "rb") as file:
                buffer_data = file.read()

            payload: FileSource = {
                "buffer": buffer_data,
            }

            options = PrerecordedOptions(
                model="nova-2",
                language="en",
                punctuate=True,
            )

            # Transcribe the audio file asynchronously
            response = self.dg_client.listen.prerecorded.v("1").transcribe_file(payload, options, timeout=6000)
            transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
            print('TRANSCRIPT!!!!')
            return transcript
            
        except Exception as e:
            print(f"Exception: {e}")
            return None

    def split_text(self, text):

        parts_promt = PromptTemplate(
                input_variables=['lecture_transcribe'],
                template=PARTS_PROMT
            )
        
        split_text = PromptTemplate(
                input_variables=['topics', 'lecture_text', 'format'],
                template=BORDERLINES_PROMT
            )
        form = '''
{
  "topics": [
    {
      "name": "Topic 1",
      "starts": "beginning of first sentence",
      "ends": "end of last sentence",
      "subtopics": [
        {
          "name": "Subtopic 1.1",
          "starts": "beginning of first sentence",
          "ends": "end of last sentence"
        },
        {
          "name": "Subtopic 1.2",
          "starts": "beginning of first sentence",
          "ends": "end of last sentence"
        }
      ]
    },
    {
      "name": "Topic 2",
      "starts": "beginning of first sentence",
      "ends": "end of last sentence",
      "subtopics": [
        {
          "name": "Subtopic 2.1",
          "starts": "beginning of first sentence",
          "ends": "end of last sentence"
        },
        {
          "name": "Subtopic 2.2",
          "starts": "beginning of first sentence",
          "ends": "end of last sentence"
        }
      ]
    }
  ]
}
'''
        try:

            chain_part = parts_promt | self.llm | StrOutputParser()
            chain_split = split_text | self.llm | StrOutputParser()
            parts = chain_part.invoke({'lecture_transcribe': text})
            result = chain_split.invoke({'topics': parts, 'lecture_text': text, 'format': form})

            topics_data = json.loads(result)
            print('DATA!!!!')
            return topics_data
            
        except Exception as e:
            print(f"Exception: {e}")
            return None
        
    def extract_boundaries(self, json_data):

        boundaries = {}

        for topic in json_data['topics']:
            for subtopic in topic.get('subtopics', []):
                segment_name = subtopic['name']
                start_boundary = subtopic['starts']
                end_boundary = subtopic['ends']
                boundaries[segment_name] = [start_boundary, end_boundary]
        print('BOUNDARIES!!!')
        return boundaries


    def get_segment(self, text, boundaries):
        segments = {}
        for name_segment in boundaries:
            start_index = text.find(boundaries[name_segment][0])
            print(f'start_ind: {start_index}')
            end_index = text.find(boundaries[name_segment][1], start_index) + len(boundaries[name_segment][1])
            print(f'end_ind: {end_index}')
            segments[name_segment] = text[start_index:end_index ]
        print('SEGMENTS!!!')
        return segments

    def get_cards(self, text):

        cards_promt = PromptTemplate(
                input_variables=['TOPIC_TEXT', 'format', 'example'],
                template=CARDS_PROMT2
            )
        form = '''
    {
     "card#№": {
       "question": "[First part of the question about the concept's definition or structure] [Second part of the question about the concept's application, purpose, or critical analysis]",
       "answer": "[Provide a comprehensive answer to both parts of the question based on the lecture text]"
     }
    }
'''
        example = '''
{
  "card#1": {
    "question": "What is the law of supply and demand? How is this economic principle applied in real-world markets?",
    "answer": "The law of supply and demand is an economic principle that describes the relationship between the availability of a product or service and its price in the market. It states that as supply increases, prices tend to decrease, and as demand increases, prices tend to rise. In real-world markets, this principle is applied in various ways. For example, during peak travel seasons, airline ticket prices often increase due to higher demand. Conversely, when there's an oversupply of a product, such as excess inventory of last season's clothing, prices are typically reduced to encourage sales."
  }
}
'''
        try:
            chain_cards = cards_promt | self.llm | JsonOutputParser()
            cards = chain_cards.invoke({"TOPIC_TEXT": text, "format": form, "example": example})
            print('CARDS!!!')
            return cards
        except Exception as e:
            print(f"Exception: {e}")

    def run(self):
        # 1) Получение транскрипта
        transcript = self.get_transcript()
        if transcript is None:
            return None  # Возвращаем None, если транскрипт не получен

        # 2) Передача транскрипта в split_text
        json_data = self.split_text(transcript)
        if json_data is None:
            return None  # Возвращаем None, если не удалось разделить текст

        # 3) Передача JSON из split_text в extract_boundaries
        boundaries = self.extract_boundaries(json_data)

        # 4) Получение сегментов с помощью get_segment
        segments = self.get_segment(transcript, boundaries)

        # 5) Передача каждого сегмента в get_cards
        cards = {}
        for segment_name, segment_text in segments.items():
            cards[segment_name] = self.get_cards(segment_text)

        # 6) Создание JSON-файла с необходимой структурой
        course_data = {
            "course": {
                "topics": {

                }
            }
        }

        for topic_name, topic_cards in cards.items():
            course_data["course"]["topics"][topic_name] = {
                "name": topic_name,
                "text": segments[topic_name],
                "cards": topic_cards
            }
        return course_data

'''def main():
    create_course = Course('output_audio.mp3')
    cource_data = create_course.run()

    print(cource_data)
    with open("testing_data.json", "w", encoding="utf-8") as file:
        json.dump(cource_data, file, sort_keys=True, indent=2)

if __name__ == "__main__":
    main()'''