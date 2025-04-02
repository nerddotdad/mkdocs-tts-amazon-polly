MkDocs TTS Amazon Polly Plugin
The MkDocs TTS Amazon Polly Plugin allows you to automatically generate and embed text-to-speech audio files for your MkDocs documentation using Amazon Polly. You can control which pages will have audio generated and customize the voice, output directory, and more. It works seamlessly with versioned deployments, such as those using Mike for multiple versions of your site.

Features
Automatically generate audio for any Markdown page with the generate_audio: true tag in the front matter.

Supports Amazon Polly's text-to-speech service to generate audio.

Inserts audio players in the pages, allowing users to listen to the content directly on the site.

Works with Mike for versioned MkDocs deployments (audio paths will include the version).

Easy configuration and customization (voice selection, output directory, etc.).

Installation
1. Install the Plugin
To install the plugin, run the following command to add it to your requirements.txt:

txt
Copy
Edit
git+https://github.com/nerddotdad/mkdocs-tts-amazon-polly.git
Alternatively, install it directly via pip:

bash
Copy
Edit
pip install git+https://github.com/nerddotdad/mkdocs-tts-amazon-polly.git
2. Add the Plugin to Your mkdocs.yml
In your mkdocs.yml, add the plugin under the plugins section:

yaml
Copy
Edit
plugins:
  - tts-amazon-polly
You can also configure the plugin's options, such as the voice and the output directory:

yaml
Copy
Edit
plugins:
  - tts-amazon-polly:
      output_dir: "audio"      # Directory for saving the audio files (relative to site_dir)
      voice_id: "Matthew"      # Choose a voice from Amazon Polly (e.g., "Matthew", "Joanna")
Configuration
output_dir
Type: str

Default: audio

Description: The directory where the audio files will be saved (relative to the site_dir). It will be automatically created if it doesn't exist.

voice_id
Type: str

Default: "Matthew"

Description: The voice used for text-to-speech conversion. You can choose a voice from Amazon Polly, e.g., "Matthew", "Joanna", "Ivy", etc.

Usage
Enable Audio Generation for Pages
In the front matter of the pages you want to generate audio for, add the following tag:

yaml
Copy
Edit
---
generate_audio: true
---
This will trigger the plugin to generate the audio for that page when you build your MkDocs site.

How It Works
The plugin will automatically detect the generate_audio: true tag in the front matter of your pages.

It will send the content of the page to Amazon Polly's TTS service and generate an MP3 audio file.

The audio file will be saved in the specified output_dir.

An audio player will be automatically inserted in the Markdown page after the title or after the <!-- more --> tag (for blog posts).

The audio tag will look like this:

html
Copy
Edit
<audio controls><source src="/audio/{audio_filename}" type="audio/mpeg"></audio>
Versioned Deployments (Using Mike)
If you're using Mike to deploy multiple versions of your documentation, the plugin will automatically adjust the audio file path to include the version. For example, it will use paths like /v1/audio/filename.mp3, ensuring the audio files are correctly served in versioned deployments.

Requirements
MkDocs (version 1.x or newer)

Amazon Web Services (AWS) account with Amazon Polly enabled

Boto3 (AWS SDK for Python)

Mike (if using versioned deployments)

AWS Credentials
Ensure your AWS credentials are available in your environment. You can set up your credentials using:

AWS CLI (set up via aws configure)

Environment Variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)

IAM Role (if running in an AWS environment like EC2 or Lambda)

For CI/CD, such as with GitHub Actions, ensure your AWS credentials are provided via GitHub Secrets.

Example
Given the following Markdown content in a page:

yaml
Copy
Edit
---
generate_audio: true
---
# Welcome to MkDocs

This is a sample documentation page.
The plugin will generate an audio file and insert an audio player directly after the title:

html
Copy
Edit
<audio controls><source src="/audio/welcome-to-mkdocs.mp3" type="audio/mpeg"></audio>
Troubleshooting
Audio file not appearing: Ensure the generate_audio front matter is added correctly and check if the output directory is accessible.

Error generating audio: Check your AWS credentials and ensure Amazon Polly is enabled in your AWS account.

Audio file path issues with Mike: Ensure you're using the correct versioned paths and that site_url is properly configured.

Contributing
Feel free to fork the repository and submit pull requests! All contributions are welcome.

Here's a GitHub-compatible README for your plugin in markdown format:

markdown
Copy
Edit
# MkDocs TTS Amazon Polly Plugin

The **MkDocs TTS Amazon Polly Plugin** allows you to automatically generate and embed text-to-speech audio files for your MkDocs documentation using Amazon Polly. You can control which pages will have audio generated and customize the voice, output directory, and more. It works seamlessly with versioned deployments, such as those using **Mike** for multiple versions of your site.

## Features

- Automatically generate audio for any Markdown page with the `generate_audio: true` tag in the front matter.
- Supports Amazon Polly's text-to-speech service to generate audio.
- Inserts audio players in the pages, allowing users to listen to the content directly on the site.
- Works with **Mike** for versioned MkDocs deployments (audio paths will include the version).
- Easy configuration and customization (voice selection, output directory, etc.).

## Installation

### 1. Install the Plugin

To install the plugin, run the following command to add it to your `requirements.txt`:

```txt
git+https://github.com/nerddotdad/mkdocs-tts-amazon-polly.git
Alternatively, install it directly via pip:
```

```bash
pip install git+https://github.com/nerddotdad/mkdocs-tts-amazon-polly.git
```

### 2. Add the Plugin to Your mkdocs.yml

In your mkdocs.yml, add the plugin under the plugins section:

```yaml
plugins:
  - tts-amazon-polly
```

You can also configure the plugin's options, such as the voice and the output directory:

```yaml
plugins:
  - tts-amazon-polly:
      output_dir: "audio"      # Directory for saving the audio files (relative to site_dir)
      voice_id: "Matthew"      # Choose a voice from Amazon Polly (e.g., "Matthew", "Joanna")
```
## Configuration
`output_dir`
- Type: `str`
- Default: `audio`
- Description: The directory where the audio files will be saved (relative to the site_dir). It will be automatically created if it doesn't exist.

`voice_id`
- Type: `str`
- Default: `"Matthew"`
- Description: The voice used for text-to-speech conversion. You can choose a voice from Amazon Polly, e.g., `"Matthew"`, `"Joanna"`, `"Ivy"`, etc.

## Usage
### Enable Audio Generation for Pages
In the front matter of the pages you want to generate audio for, add the following tag:

```yaml
---
generate_audio: true
---
```
This will trigger the plugin to generate the audio for that page when you build your MkDocs site.

#### How It Works
- The plugin will automatically detect the `generate_audio: true` tag in the front matter of your pages.
- It will send the content of the page to Amazon Polly's TTS service and generate an MP3 audio file.
- The audio file will be saved in the specified `output_dir`.
- An audio player will be automatically inserted in the Markdown page after the title or after the `<!-- more -->` tag (for blog posts).

The audio tag will look like this:

```html
<audio controls><source src="/audio/{audio_filename}" type="audio/mpeg"></audio>
```

### Versioned Deployments (Using Mike)
If you're using Mike to deploy multiple versions of your documentation, the plugin will automatically adjust the audio file path to include the version. For example, it will use paths like `/v1/audio/filename.mp3`, ensuring the audio files are correctly served in versioned deployments.

## Requirements
- MkDocs (version 1.x or newer)
- Amazon Web Services (AWS) account with Amazon Polly enabled
- Boto3 (AWS SDK for Python)
- Mike (if using versioned deployments)

## AWS Credentials
Ensure your AWS credentials are available in your environment. You can set up your credentials using:

- AWS CLI (set up via `aws configure`)
- Environment Variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
- IAM Role (if running in an AWS environment like EC2 or Lambda)
- For CI/CD, such as with GitHub Actions, ensure your AWS credentials are provided via GitHub Secrets.

Example
Given the following Markdown content in a page:

```yaml
---
generate_audio: true
---
# Welcome to MkDocs

This is a sample documentation page.
```

The plugin will generate an audio file and insert an audio player directly after the title:

```html
<audio controls><source src="/audio/welcome-to-mkdocs.mp3" type="audio/mpeg"></audio>
```

## Troubleshooting

- Audio file not appearing: Ensure the generate_audio front matter is added correctly and check if the output directory is accessible.
- Error generating audio: Check your AWS credentials and ensure Amazon Polly is enabled in your AWS account.
- Audio file path issues with Mike: Ensure you're using the correct versioned paths and that site_url is properly configured.

## Contributing
Feel free to fork the repository and submit pull requests! All contributions are welcome.