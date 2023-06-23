"""
class where user input a model and a paragraph 
and receive a segmented paragraph from the paragraph
"""

import os
import re

from dotenv import load_dotenv
from langchain import chains, llms
from langchain.chat_models import ChatOpenAI

from syn2act.segment.prompt import example, ptemplate

# Load OPENAI API key
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
openai_key_for_anthropic = os.getenv("OPENAI_API_KEY_FOR_ANTHROPIC")

class Segmentor():
    def __init__(self, model: str, parag: str) -> None:
        self.model = model
        self.parag = parag

    # define functions
    def chain_select(self):
        if self.model == "gpt-4":
            llm = ChatOpenAI(
                model_name="gpt-4",
                temperature=0.1,
                max_tokens=2048,
                request_timeout=3000,
                openai_api_key=openai_key,
            )

            chain = chains.LLMChain(prompt=ptemplate, llm=llm)
            return chain

        elif self.model == "gpt-3.5-turbo-16k":
            llm = ChatOpenAI(
                model_name="gpt-3.5-turbo-16k",
                temperature=0.1,
                max_tokens=2048,
                request_timeout=3000,
                openai_api_key=openai_key,
            )

            chain = chains.LLMChain(prompt=ptemplate, llm=llm)
            return chain

        elif self.model == "anthropicai":
            llm = llms.Anthropic(
                model="claude-v1.3",
                temperature=0.1,
                anthropic_api_key=anthropic_api_key,
                max_tokens_to_sample=2000,
            )

            chain = chains.LLMChain(prompt=ptemplate, llm=llm)
            return chain

    def _parse_llm_segm(self, llm_segm: str):
        """
        Parse the output of LLMChain for paragraph segmentation into a JSON object.

        Input:
            llm_segm: the output of the segmentation LLM.

        Output:
            a formated JSON object with all information.
        """

        output = []
        segments = re.split(
            "Step end #", llm_segm
        )  # split the paragraph text into segments by step

        for segment in range(0, len(segments)):
            dict_temp = {}
            sentences = re.split(
                "\n", segments[segment]
            )  # split text segment, text class, explanation and step order
            for j in range(0, len(sentences)):
                item = sentences[j].split(": ")  # split label and its content
                #            print('item:', item)
                try:
                    if (
                        item[0] == "text segment"
                        or item[0] == "text class"
                        or item[0] == "explanation"
                        or item[0] == "step order"
                    ):  # continue if the label does not exist
                        dict_temp[item[0]] = item[1]  # save index and value in the dictionary

                    else:
                        continue
                except:
                    if item[0] == "":  # continue if the label does not exist
                        continue

                    else:
                        dict_temp[item[0]] = item[1]  # save index and value in the dictionary

            output.append(dict_temp)  # save the dictionary into the list
        return output

    def syn2segment(self):
        """
        Semantical segmentation of synthesis paragraph into
        ['reaction set-up', 'workup', 'purification', 'analysis']

        Input:
            parag: a string containing synthesis paragraph text

        Output:
            json object with ['segment', 'class', 'order'] properties for each segment.
        """

        chain = self.chain_select()
        segmented_paragraph = chain.run({"example": example, "paragraph": self.parag})

        paragraph = self._parse_llm_segm(segmented_paragraph)
        paragraph.pop()
        return paragraph
