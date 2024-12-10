import sys
sys.path.append("../")
import importlib
import os
import pathlib
import shutil
import re
import action
import prompt
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.extensions.langchain import (
    WatsonxLLM,
)
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from hf_hub import HuggingFaceHubEmbeddings

import sys
sys.path.append("../")

import importlib
import os
import pathlib
import shutil

import numpy as np
import pandas as pd
import prompt
from dotenv import load_dotenv
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.extensions.langchain import (
    WatsonxLLM,
)
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.schema.embeddings import Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text

load_dotenv()

engine = create_engine("sqlite://", echo=False)

MODELS = [
    ModelTypes.FLAN_T5_XXL,
    ModelTypes.LLAMA_2_70B_CHAT,
    "meta-llama/llama-3-70b-instruct",
]

MODELS = {
    x: WatsonxLLM(
        model=Model(
            model_id=x,
            credentials={
                "apikey": os.getenv("IBM_API_KEY"),
                "url": "https://us-south.ml.cloud.ibm.com",
            },
            params={
                GenParams.DECODING_METHOD: "greedy",
                GenParams.MAX_NEW_TOKENS: 300,
                GenParams.TEMPERATURE: 0,
                GenParams.RANDOM_SEED: 12345,
                GenParams.STOP_SEQUENCES: ["\n\n"],
            },
            project_id=os.getenv("PROJECT_ID"),
        )
    )
    for x in MODELS
}

print(MODELS)
