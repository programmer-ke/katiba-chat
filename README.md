# Katiba Chat
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

Stay informed on the Kenyan Constitution

A web and command line application that powered by AI that can answer
various questions about the Kenya 2010 consitution.

## Installation

Three environment variables are needed for LLM access.

- `LLM_API_KEY`: The secret api key from your LLM provider
- `LLM_BASE_URL`: The API endpoint to your LLM provider
- `LLM_MODEL_NAME`: The name of model you want to use

Any provider that provides an API compatible with OpenAI's Chat
Completions API can be used.

The API key can be generated in their respective consoles.

Sample Values are shown below:

| Provider               | Base URL                             | Model Name Example               |
|------------------------|--------------------------------------|----------------------------------|
| [Akash Network][akash] | https://chatapi.akash.network/api/v1 | Meta-Llama-3-1-405B-Instruct-FP8 |
| [Mistral AI][mistral]  | https://api.mistral.ai/v1            | open-mistral-nemo                |
| [Ollama][ollama]       | http://localhost:11434/v1            | qwen2.5:3b                       |


[mistral]: https://mistral.ai/
[ollama]: https://ollama.com/blog/openai-compatibility
[akash]: https://chatapi.akash.network/

### Docker

The easiest way to run the app is via Docker. Pull it from docker hub:

```bash
docker pull programmerke/katiba_chat:latest
```

The app can then be executed by creating a container with the
variables above. Assuming they are specified in a file
named `.env`:

```bash
docker run --env-file .env programmerke/katiba_chat
```

The app can now be accessed at: http://localhost:7860

### Akash

One convenient way to deploy the docker image is through the [Akash][akashnet] network.

[akashnet]: https://akash.network

See detailed instructions [here](akash/README.md)

## License

- GNU AFFERO GENERAL PUBLIC LICENSE
