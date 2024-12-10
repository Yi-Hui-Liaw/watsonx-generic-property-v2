import os
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.extensions.langchain import (
    WatsonxLLM,
)

from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

GENERATE_PARAMS = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 1024,
    GenParams.TEMPERATURE: 0,
    GenParams.RANDOM_SEED: 12345,
    # GenParams.STOP_SEQUENCES: ["\n\n"],
}

EMBEDDING = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3", multi_process=False, show_progress=True
)

# models = [
#     ModelTypes.FLAN_T5_XXL,
#     ModelTypes.LLAMA_2_70B_CHAT,
#     "meta-llama/llama-3-70b-instruct",
# ]

MODEL = Model(
            model_id="meta-llama/llama-3-70b-instruct",
            credentials={
                "url": "https://us-south.ml.cloud.ibm.com",
                "apikey": os.getenv("IBM_API_KEY", None),
            },
            project_id=os.getenv("PROJECT_ID", None),
            params=GENERATE_PARAMS,
        )