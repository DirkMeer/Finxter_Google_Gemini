from load_env import configure_genai
from utils import safety_settings

genai = configure_genai()


character = input("What is your favorite movie character? (e.g. Gollum): ")
movie = input("What movie are they from? (e.g. Lord of the Rings): ")


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings.low,
    system_instruction=f"You are helpful and provide good information but you are {character} from {movie}. You will stay in character as {character} no matter what. Make sure you find some way to relate your responses to {character}'s personality or the movie {movie} at least once every response.",
)

history = []

chat_session = model.start_chat(history=history)


if __name__ == "__main__":
    try:
        while True:
            query = input("\nPlease ask a question or use CTRL+C to exit: ")
            response = chat_session.send_message(query, stream=True)
            for chunk in response:
                if chunk.candidates[0].finish_reason == 3:
                    print(f"\n\033[1;31mPlease ask a more appropriate question!\033[0m", end="")
                    chat_session.rewind()
                    break
                print(f"\033[1;34m{chunk.text}\033[0m", end="")
            print("\n")

    except KeyboardInterrupt:
        print("Shutting down...")