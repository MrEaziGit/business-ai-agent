# Business AI Agent

A backend AI agent built with Python and FastAPI that connects an LLM to real business operations through tool calling.

## What It Does

- Uses LLM tool calling to execute real application functions
- Manages orders and customers through a SQLite database
- Performs business analytics and multi-step workflows
- Handles tool errors, invalid arguments, unknown tools, and duplicate calls
- Enforces business rules at the application level

## Architecture

User Request → LLM → Tool Selection → Python Function → Database → Tool Result → LLM → Response

## Tech Stack

Python • FastAPI • Groq API • SQLite • Pydantic • REST APIs

## Key Concepts

LLM Tool Calling • AI Agents • Agent Orchestration • Backend Development • Database Integration • Error Handling • Business Automation

## Example

**User:** Which customer has the highest value of shipped orders?

**Agent:** Test User has the highest shipped-order value at $45,000.

Built as a practical demonstration of integrating AI agents with real backend systems and business logic.
