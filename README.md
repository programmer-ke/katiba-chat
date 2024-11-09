# Katiba Chat
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

Stay informed on the Kenyan Constitution

A web and command line application that powered by AI that can answer
various questions about the Kenya 2010 consitution.

## Installation

todo: installation command

Three environment variables are needed for LLM access.

- `LLM_API_KEY`: The secret api key from your LLM provider
- `LLM_BASE_URL`: The API endpoint to your LLM provider
- `LLM_MODEL_NAME`: The name of model you want to use

For example, when using [Mistral AI][0], these could be:

```sh
LLM_API_KEY="..."  # generated on the console
LLM_BASE_URL="https://api.mistral.ai/v1"
LLM_MODEL_NAME="open-mistral-nemo"  # or whichever model selected
```

Mistral AI (at the time of writing) gives free credit on signing up, so
it may be the easiest to start with.

If using self-hosted [Ollama][1], they could be

```sh
LLM_API_KEY="ollama"
LLM_BASE_URL="http://localhost:11434/v1"  # or wherever it is serving from
LLM_MODEL_NAME=".."  # whichever model is installed via ollama
```

If using [OpenAI][2] as the provider, `LLM_BASE_URL` can be excluded.

Any provider that provides an API compatible with OpenAI's Chat
Completions API can be used.

[0]: https://mistral.ai/
[1]: https://ollama.com/
[2]: https://platform.openai.com


A `.env` file in the directory from which you run the application can
be used to provide these variables. Be sure not to share it publicly
e.g. on Github as your API key will be leaked.


## Usage

### Command Line

```sh
$ python -m katiba_chat "my question in quotes"
```
