"""Parsing documents."""

import asyncio
import base64
import os
from typing import Literal, Optional

import requests
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pdf2image import convert_from_path
from pydantic import BaseModel, Field, model_validator

from jasyntho.document.synthpar import SynthParagraph


class Substance(BaseModel):
    """Basic substance model"""

    name: str = Field(..., description="Name used for the substance.")
    reference_key: Optional[str] = Field(
        ..., description="Reference key used for the substance."
    )
    role: str = Field(
        ...,
        description="Role of the substance in the reaction. Can be [product, main reactant, reagent, solvent, catalyst, other].",
    )


class VisionParser(BaseModel):
    """Vision parser model."""

    ptype: Literal["text", "vision"] = Field(
        ..., description="Type of the parser. Can be [vision, text]."
    )
    api_key: Optional[str] = Field(
        ..., description="API key for the OpenAI API."
    )

    def encode_image(self, image_path):
        """Encode image to base64."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def load_imagerange(self, pdf, indices):
        """Load images from a range of pages."""
        img_messages = []
        for i in indices:
            img_path = f".tmp/page{i}.jpg"
            base64_image = self.encode_image(img_path)
            img_messages.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                }
            )
        return img_messages

    def calc_cost(self, response):
        """Calculate the cost of a response."""
        intok = response.usage.prompt_tokens
        outtok = response.usage.completion_tokens

        incost = intok * (5 / 1e6)
        outcost = outtok * (15 / 1e6)
        return incost + outcost

    async def vision_parse_batch(
        self, img_messages, model="gpt-4o", prgr_sep="##---##", client=None
    ):
        """Parse a batch of images."""

        prompt = """These are some pages from the SI of an organic chemistry paper.
        Describe all the reactions shown there, if any.
        Separate each reaction with \"{}\", describe products and reactants for each reaction.
        Ignore all characterization data. Consider work-up and purification as part of the same reaction.
        Use the following format to represent the products and main reactants: {}.
        Do not rewrite the reaction procedures, just describe the substances involved."""

        messages = [
            {
                "role": "system",
                "content": "You are an expert chemist. Your task is to read and extract data from chemistry papers.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt.format(prgr_sep, Substance.schema()),
                    },
                    *img_messages,
                ],
            },
        ]

        response = await client.chat.completions.create(
            model=model, messages=messages, max_tokens=4096
        )
        cost = self.calc_cost(response)
        print(f"Finished processing batch. Cost: {cost}")
        return response.choices[0].message.content

    def split_images(self, pdf):
        """Split PDF into a sequence of images."""
        images = convert_from_path(pdf)
        # Store images into .tmp
        os.makedirs(".tmp", exist_ok=True)
        for i in range(len(images)):
            images[i].save(f".tmp/page{i}.jpg", "JPEG")
        return images

    def create_overlapping_batches(self, N, batch_size, overlap):
        """Create overlapping batches."""
        start = 0
        batches = []
        while start < N:
            end = start + batch_size
            if end > N:
                end = N
            batches.append((start, end))
            start += batch_size - overlap
        return batches

    async def vision_parse(
        self, pdf, batch_size=10, model="gpt-4o", prgr_sep="##---##"
    ):
        """Parse a PDF using vision models."""
        images = self.split_images(pdf)
        img_messages = []
        N = len(images)
        start = 0
        client = AsyncOpenAI()

        paragraphs = []

        # divide the images into batches
        indices = list(range(N))
        tasks = []

        for b0, b1 in self.create_overlapping_batches(
            N, batch_size, overlap=1
        ):
            img_messages = self.load_imagerange(pdf, indices[b0:b1])
            tasks.append(
                self.vision_parse_batch(
                    img_messages, model=model, prgr_sep=prgr_sep, client=client
                )
            )

        responses = await asyncio.gather(*tasks)

        for response in responses:
            paragraphs += response.split(prgr_sep)

        return [SynthParagraph(p) for p in paragraphs]

    @model_validator(mode="after")
    def validate_api_key(self):
        """Initialize API key."""
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key is None and self.ptype == "vision":
            raise ValueError("API key is required for vision parsing.")
        return self
