from load_env import configure_genai
from utils import safety_settings
from cost_calculator import print_cost_in_dollars


genai = configure_genai()
MODEL_NAME = "gemini-1.5-flash"

character = input("What is your favorite movie character? (e.g. Gollum): ")
movie = input("What movie are they from? (e.g. Lord of the Rings): ")

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    safety_settings=safety_settings.low,
    system_instruction=f"You are helpful and provide good information but you are {character} from {movie}. You will stay in character as {character} no matter what. Make sure you find some way to relate your responses to {character}'s personality or the movie {movie} at least once every response.",
)

chat_session = model.start_chat(history=[])


def upload_image():
    while True:
        try:
            image_path = input("Please provide the path to the image: ")
            image_upload = genai.upload_file(path=image_path, display_name="User Image")
            return image_upload
        except FileNotFoundError:
            print("File not found. Please try again with the correct path.")


if __name__ == "__main__":
    try:
        while True:
            text_query = input("\nPlease ask a question or type `/image` to upload an image first: ")

            image_upload = None
            if text_query.lower() == "/image":
                image_upload = upload_image()
                text_query = input("Please ask a question to go with your image upload: ")

            full_query = [image_upload, text_query] if image_upload else text_query

            response = chat_session.send_message(full_query, stream=True)
            for chunk in response:
                if chunk.candidates[0].finish_reason == 3:
                    print(f"\n\033[1;31mPlease ask a more appropriate question!\033[0m", end="")
                    chat_session.rewind()
                    break
                print(f"\033[1;34m{chunk.text}\033[0m", end="")
            print("\n")

            print_cost_in_dollars(response.usage_metadata, MODEL_NAME)

    except KeyboardInterrupt:
        print("Shutting down...")