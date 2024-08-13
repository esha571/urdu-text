import os
import tensorflow as tf
os.environ["USE_TF"] = "1"  # Force transformers to use TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)  # Suppress deprecation warnings

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import TFMarianMTModel, MarianTokenizer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for all domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Load the models and tokenizers for English to Urdu and Urdu to English
model_name_en_to_ur = "Helsinki-NLP/opus-mt-en-ur"
model_name_ur_to_en = "Helsinki-NLP/opus-mt-ur-en"

tokenizer_en_to_ur = MarianTokenizer.from_pretrained(model_name_en_to_ur)
model_en_to_ur = TFMarianMTModel.from_pretrained(model_name_en_to_ur)  # Use TFMarianMTModel for TensorFlow

tokenizer_ur_to_en = MarianTokenizer.from_pretrained(model_name_ur_to_en)
model_ur_to_en = TFMarianMTModel.from_pretrained(model_name_ur_to_en)  # Use TFMarianMTModel for TensorFlow

class TranslationRequest(BaseModel):
    text: str
    source_lang: str  # Can be 'en' for English or 'ur' for Urdu
    target_lang: str  # Can be 'ur' for Urdu or 'en' for English
@app.post("/translate/")
def translate(request: TranslationRequest):
    try:
        if request.source_lang == 'en' and request.target_lang == 'ur':
            tokenizer = tokenizer_en_to_ur
            model = model_en_to_ur
        elif request.source_lang == 'ur' and request.target_lang == 'en':
            tokenizer = tokenizer_ur_to_en
            model = model_ur_to_en
        else:
            raise HTTPException(status_code=400, detail="Unsupported language pair")

        # Tokenize the input text
        encoded_input = tokenizer(request.text, return_tensors="tf")

        # Generate the translation
        generated_tokens = model.generate(**encoded_input)

        # Decode the generated tokens
        translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

        return {"translated_text": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
