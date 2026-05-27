
## What does the agent do?

It's a conversational agent, with tool calling abilities, which means you can do some pretty powerful things it.

For this example, I have set it up as a Delivery agent that gets your name, address and creates an order, using
the tools it has.

The point is to demonstrate how to build conversation agent you can interact with in natural language, that has the
ability to call tools, and process the results from those tools to see what to do do next.

In this example, the agents goal is to:

- get your name
- check if you exist in their registry via a tool call (this is to show an example of a tool call, and will always
  return `False`)
- if you don't exist, to ask for you address
- to ask what pizza/coffee/burger you would like
- create an order with your name, address and order via a tool call

## Getting Started

### Install `uv` and Create a Virtual Environment

First, get `uv` installed. It's a modern package manager for python, and blazingly fast. I tried it out for the first
time
in this project, and was wowed with how fast it was

To install uv, run this in your terminal:

`curl -LsSf https://astral.sh/uv/install.sh | sh`

Then restart your terminal so the uv command is available.

You can check that it’s working with:

`uv --version`

Now create and initialise the virtual environment:

```bash
uv venv
source .venv/bin/activate
```

## Install Dependencies

Now install the dependencies:

```bash
uv sync
```

## Set Your Anthropic API Key

Now set your Anthropic API key as an environment variable in the .env file
(can get one from their website if you dont have one yet)

```bash
ANTHROPIC_API_KEY=
```

## Run the Agent

Now you can run the agent with:

```bash
python main.py
```

This will open up a chat interface in your terminal, where the agent will ask you questions in order to get your order and address.

The console output will show all the Tool calls and tool results the agent uses, to make it clear what is going on in
background as you chat with the agent.

To point is to show you how easy it is to setup a nicely working, conversation agent, that has tools at it disposal to
get things done as well.

