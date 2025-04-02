import os
import logging
import boto3
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

logger = logging.getLogger("mkdocs.plugins.tts-amazon-polly")

class AmazonPollyTTSPlugin(BasePlugin):
    config_scheme = (
        ("output_dir", config_options.Type(str, default="audio")),
        ("voice_id", config_options.Type(str, default="Matthew")),
    )

    def __init__(self):
        self.polly_client = boto3.client("polly")

def on_page_markdown(self, markdown, page, config, files):
    """Generate speech from text using Amazon Polly based on front matter configuration."""
    logger.debug(f"[amazon-polly-tts] Processing page: {page.file.src_path}")
    logger.debug(f"[amazon-polly-tts] Page metadata: {page.meta}")

    # Access the 'generate_audio' flag from front matter
    generate_audio = page.meta.get("generate_audio", False)
    if not generate_audio:
        logger.info(f"[amazon-polly-tts] Skipping TTS for {page.file.src_path} (No 'generate_audio' tag)")
        return markdown

    # Ensure output directory exists
    output_dir = os.path.join(config["site_dir"], self.config["output_dir"])
    os.makedirs(output_dir, exist_ok=True)

    # Clean content and remove <!-- more --> tag
    text_content = markdown.replace("<!-- more -->", "").strip()
    if not text_content:
        logger.warning(f"[amazon-polly-tts] Skipping page with no meaningful content: {page.file.src_path}")
        return markdown

    # Define audio filename and path
    audio_filename = f"{os.path.splitext(page.file.src_path)[0]}.mp3"
    audio_path = os.path.join(output_dir, audio_filename)

    # Ensure the directory exists before writing the file
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)

    # Generate audio if it doesn’t exist
    if not os.path.exists(audio_path):
        logger.info(f"[amazon-polly-tts] Generating audio for: {page.file.src_path}")
        try:
            response = self.polly_client.synthesize_speech(
                Text=text_content,
                OutputFormat="mp3",
                VoiceId=self.config["voice_id"]
            )

            # Debugging: Log Polly response metadata
            logger.debug(f"[amazon-polly-tts] Polly response metadata: {response['ResponseMetadata']}")

            if "AudioStream" in response:
                with open(audio_path, "wb") as audio_file:
                    audio_file.write(response["AudioStream"].read())
                logger.info(f"[amazon-polly-tts] Audio saved: {audio_path}")
            else:
                logger.error(f"[amazon-polly-tts] No AudioStream in response for {page.file.src_path}")

        except Exception as e:
            logger.error(f"[amazon-polly-tts] Amazon Polly TTS failed: {e}")
            return markdown

    # Create audio tag
    audio_tag = f'<audio controls><source src="/{self.config["output_dir"]}/{audio_filename}" type="audio/mpeg"></audio>\n\n'

    # Check if the page contains the <!-- more --> tag
    if "<!-- more -->" in markdown:
        return markdown.replace("<!-- more -->", "<!-- more -->\n\n" + audio_tag, 1)
    
    # If no <!-- more --> tag, insert it after the first sentence and place the audio tag there
    first_sentence_end = markdown.find('.') + 1
    if first_sentence_end > 0:
        markdown = markdown[:first_sentence_end] + " <!-- more -->\n\n" + audio_tag + markdown[first_sentence_end:]
    else:
        # If no sentence, just add the audio at the top
        markdown = audio_tag + markdown

    return markdown
