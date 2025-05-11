# Model Context Protocol Use Case Prototype

This repository contains a **Model Context Protocol (MCP) Use Case Prototype** to demonstrate the application of context management across models. The goal is to show how the **Model Context Protocol** can be used in real-world scenarios, allowing context to flow seamlessly between different parts of the system.

## Requirements

Before running the project, make sure you have the required dependencies installed:

```bash
pip install -r requirements.txt

Setup
1. Set up your API Key

You will need a Gemini API Key for this project. Set your API key as an environment variable:

export GEMINI_API_KEY=__YOUR_GEMINI_API_KEY__

2. Run the Server

Start the server by running the following command:

python server.py

3. Run the Client

Once the server is running, you can start the client:

python client.py

Usage

- **server.py** manages the MCP tools and resources, handling the core functionality of the Model Context Protocol.

- **client.py** communicates with the server, demonstrating how context is exchanged and utilized in real-world scenarios.
