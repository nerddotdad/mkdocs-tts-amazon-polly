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
        # Ensure the audio tag reflects the correct versioned URL if using Mike for versioned deployment
        site_url = config.get("site_url", "")  # Get the base site URL (including version path if Mike is used)
        versioned_audio_url = f"{site_url}/{self.config['output_dir']}/{audio_filename}"
        audio_tag = f'<audio controls><source src="{versioned_audio_url}" type="audio/mpeg"></audio>\n\n'

        # Log the markdown before modification
        logger.debug(f"[amazon-polly-tts] Original markdown: {markdown[:500]}")  # Log first 500 chars for preview

        # Determine if it's a blog page
        is_blog_page = "blog" in page.file.src_path.lower()

        if is_blog_page:
            # Only insert audio at <!-- more --> if it's a blog page
            if "<!-- more -->" in markdown:
                logger.debug(f"[amazon-polly-tts] Found <!-- more --> tag, inserting audio tag below.")
                markdown = markdown.replace("<!-- more -->", "<!-- more -->\n\n" + audio_tag, 1)
            else:
                logger.debug(f"[amazon-polly-tts] No <!-- more --> tag, inserting after first sentence.")
                first_sentence_end = markdown.find('.') + 1
                if first_sentence_end > 0:
                    markdown = markdown[:first_sentence_end] + " <!-- more -->\n\n" + audio_tag + markdown[first_sentence_end:]
                else:
                    markdown = audio_tag + markdown
        else:
            # For non-blog pages, insert the audio right below the title (first header)
            if markdown.startswith("# "):
                first_line_end = markdown.find('\n') + 1
                markdown = markdown[:first_line_end] + "\n" + audio_tag + markdown[first_line_end:]
            else:
                markdown = audio_tag + markdown

        # Log the modified markdown
        logger.debug(f"[amazon-polly-tts] Modified markdown: {markdown[:500]}")  # Log first 500 chars for preview

        return markdown
