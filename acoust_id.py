from pydub import AudioSegment
import chromaprint
import requests
from config import ACOUST_ID_TOKEN
from log import setup_logger
logger = setup_logger(__name__)

def generate_fingerprint(file_path):
    audio = AudioSegment.from_wav(file_path)
    pcm_data = audio.raw_data
    pcm_array = bytearray(pcm_data)
    fingerprint, duration = chromaprint.decode_fingerprint(pcm_array, audio.frame_rate)
    logger.info(f"Generated fingerprint: {fingerprint}")
    logger.info(f"Generated duration: {duration}")
    return fingerprint,duration


def get_acoust_id_audio_details(file_path):
    data_dict = dict()
    fingerprint, duration = generate_fingerprint(file_path)
    api_key = ACOUST_ID_TOKEN
    try:
        url = f'https://api.acoustid.org/v2/lookup?client={api_key}&duration={duration}&fingerprint={fingerprint}'
        response = requests.get(url)
        data = response.json()
        if 'results' in data and data['results']:
            result = data['results'][0]
            recording_id = result['id']
            title = result['recordings'][0]['title']
            artist = result['recordings'][0]['artists'][0]['name']
            data_dict["Recording ID"] = recording_id
            data_dict["Title"] = title
            data_dict["Artist"] = artist
            logger.info(f"Recording ID: {recording_id}")
            logger.info(f"Title: {title}")
            logger.info(f"Artist: {artist}")
            return data_dict
        else:
            logger.info("No matching result found.")
            return data_dict
    except Exception as error:
        logger.info(f"Error: {error}")
        return error