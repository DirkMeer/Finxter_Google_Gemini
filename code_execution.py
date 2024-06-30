from load_env import configure_genai
from utils import safety_settings


genai = configure_genai()


model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings.low,
    tools='code_execution',
)


response = model.generate_content((
    "Please create a Python script that will print an integer in reverse order. "
    "The script should take an integer as input and return the reversed integer. "
    "For example, if the input is 123, the output should be 321. "
    "Make sure you execute the script to test if it really works. "
))

print(response.text)