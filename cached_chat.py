import datetime
import time

from google.generativeai import caching

from load_env import configure_genai
from utils import safety_settings

genai = configure_genai()


path_to_video_file = 'images/Sherlock_Jr_FullMovie.mp4'

video_file = genai.upload_file(path=path_to_video_file)

while video_file.state.name == 'PROCESSING':
    print('Video is still processing...')
    time.sleep(2)
    video_file = genai.get_file(video_file.name)

print(f'Video processing complete: {video_file.uri}')


cache = caching.CachedContent.create(
    model='models/gemini-1.5-flash-001',
    display_name='sherlock',
    system_instruction=(
        'You are an expert video analyzer, and your job is to answer '
        'the user\'s query based on the video file you have access to.'
    ),
    contents=[video_file],
    ttl=datetime.timedelta(minutes=10),
)


model = genai.GenerativeModel.from_cached_content(
    cached_content=cache,
    safety_settings=safety_settings.low,
)


video_chat = model.start_chat(history=[])


if __name__ == "__main__":
    try:
        while True:
            text_query = input("\nPlease ask a question: ")

            response = video_chat.send_message(text_query, stream=True)
            for chunk in response:
                if chunk.candidates[0].finish_reason == 3:
                    print(f"\n\033[1;31mPlease ask a more appropriate question!\033[0m", end="")
                    video_chat.rewind()
                    break
                print(f"\033[1;34m{chunk.text}\033[0m", end="")
            print("\n")

            print(f"\033[93m{response.usage_metadata}\033[0m")

    except KeyboardInterrupt:
        print("Shutting down...")

    finally:
        cache.delete()
        print("Cache deleted.")