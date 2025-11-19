def read_system_instructions(file_path: str) -> str:
    """Read system instructions from a markdown file."""
    with open(file_path, "r", encoding="utf-8") as file:
        instructions = file.read()
    return instructions

query_chroma = {
    "name": "query_chroma",
    "description": "Function to query the Chroma database for relevant data based on a given query string.",
    "parameters": {
        "type": "object",
        "properties": {
            "query_text": {
                "type": "string",
                "description": "The text query to search for relevant data in the database."
            },
        },
        "required": ["query_text"]
    }
}