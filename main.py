import datetime
import json
import os
import threading
import time

import humanize as humanize
import psutil as psutil
import whisper

INPUT_FILE_PATH = '/input/audio.m4a'
OUTPUT_DIR = '/output'


def start_stats_thread():
    def print_stats():
        p = psutil.Process()
        p.cpu_percent()
        while True:
            print(
                f'{datetime.datetime.now().isoformat()} - {humanize.naturalsize(p.memory_info().rss)} - {p.cpu_percent()}%')
            time.sleep(10)

    t = threading.Thread(target=print_stats)
    t.daemon = True
    t.start()


def main():
    start_stats_thread()

    # Load model
    model_name = os.environ['MODEL_NAME']
    model = whisper.load_model(model_name)

    # Transcribe
    start = time.time()
    result = model.transcribe(INPUT_FILE_PATH, verbose=True)
    print(f'Transcription took {humanize.precisedelta(datetime.timedelta(seconds=time.time() - start))} ')

    # Save output
    with open(os.path.join(OUTPUT_DIR, f'{model_name}.json'), 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
