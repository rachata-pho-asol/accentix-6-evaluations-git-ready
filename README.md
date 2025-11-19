# Accentix-6 Evaluations - RAG System Testing & Evaluation

A comprehensive automated testing and evaluation framework for RAG (Retrieval-Augmented Generation) chatbot systems, specifically designed to evaluate the performance of "น้องออมสุข" (Nong Aomsuk) - a Thai Social Security Office conversational AI assistant.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [System Components](#system-components)
- [Evaluation Methodology](#evaluation-methodology)
- [Output Files](#output-files)
- [Contributing](#contributing)

## 🎯 Overview

This project provides an automated testing framework for evaluating conversational AI agents that use RAG (Retrieval-Augmented Generation) systems. It specifically tests "น้องออมสุข", a Thai language AI assistant for Thailand's Social Security Office, which provides information from the "คู่มือผู้ประกันตน" (Social Security Handbook).

The framework:
1. **Runs test cases** - Executes multi-turn conversations with the AI agent
2. **Captures responses** - Records actual answers and retrieved document chunks
3. **Evaluates performance** - Uses GPT-5 to automatically evaluate response quality
4. **Generates reports** - Creates detailed CSV reports with results and failure analysis

## ✨ Features

- **Automated Multi-Turn Conversation Testing**: Tests conversational context maintenance across multiple dialogue turns
- **RAG Performance Evaluation**: Validates both retrieval accuracy (chunk IDs) and answer quality
- **AI-Powered Evaluation**: Uses OpenAI GPT-5 for intelligent, semantic evaluation of responses
- **Session-Based Testing**: Organizes test cases into sessions representing realistic user interactions
- **Comprehensive Reporting**: Generates detailed CSV reports with pass/fail results and evaluation comments
- **Flexible Architecture**: Supports multiple agent implementations and evaluation strategies
- **Jupyter Notebook Analysis**: Includes notebooks for failure analysis and performance visualization

## 📁 Project Structure

```
accentix-6-evaluations-git-ready/
├── main.py                              # Main execution script
├── requirements.txt                     # Python dependencies
├── failure_analysis.ipynb               # Jupyter notebook for analyzing test failures
├── gepa_plus.ipynb                      # Jupyter notebook for advanced evaluation metrics
│
├── src/
│   ├── Agent.py                         # AI Agent implementation using Gemini API
│   ├── auto_evaluation.py               # Automated evaluation using OpenAI GPT-5
│   ├── Database.py                      # ChromaDB integration for vector storage
│   ├── helper.py                        # Utility functions
│   ├── test.py                          # Testing utilities
│   │
│   ├── system_instructions/
│   │   ├── evaluator_instructions.md                      # Instructions for evaluation agent
│   │   ├── extract_top_reason_instructions.md            # Instructions for failure analysis
│   │   ├── session_level_failure_analysis_instructions.md # Session-level analysis instructions
│   │   └── system_instruction-origin.md                   # Original agent system instructions
│   │
│   └── test_cases/
│       ├── aax_test_cases.csv           # Input test cases with expected results
│       └── aax_data.csv                 # Source data for RAG system
│
└── aax_results/
    ├── aax_results-1.csv                # Test run results (version 1)
    ├── aax_results-2.csv                # Test run results (version 2)
    ├── aax_results-3-gepa.csv           # GEPA evaluation results (version 3)
    ├── aax_results-4-gepa.csv           # GEPA evaluation results (version 4)
    ├── aax_results-5-gepa.csv           # GEPA evaluation results (version 5)
    └── aax_results-6-gepa.csv           # GEPA evaluation results (version 6)
```

## 🔧 Prerequisites

- **Python**: 3.8 or higher
- **API Keys**: 
  - OpenAI API key (for GPT-5 evaluation)
  - Gemini API key (for agent implementation)
  - Access to Chatbotix API endpoint (for agent generation)
- **Dependencies**: Listed in `requirements.txt`

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd accentix-6-evaluations-git-ready
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## ⚙️ Configuration

### Test Cases Format

Test cases are stored in `src/test_cases/aax_test_cases.csv` with the following columns:

| Column | Description |
|--------|-------------|
| `Session ID` | Unique identifier for conversation sessions |
| `Turn` | Turn number within the session (1, 2, 3, ...) |
| `Question` | User's question/query |
| `Expected Chunk ID` | Ground truth document chunk IDs that should be retrieved |
| `Expected Answer` | Reference answer for comparison |
| `Actual Chunk ID` | (Filled by system) Actual chunks retrieved |
| `Actual Answer` | (Filled by system) Agent's generated answer |

### Agent Configuration

The agent connects to a custom RAG endpoint. Update the configuration in `src/Agent.py`:

```python
URL = "https://flowbuilderchat-genai.chatbotix.ai/api/generate_content"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Basic <your-credentials>"
}
```

## 🚀 Usage

### Running the Complete Pipeline

Execute both test case runs and evaluations:

```bash
python main.py
```

This will:
1. Run all test cases from `aax_test_cases.csv`
2. Generate agent responses
3. Save results to `aax_results/aax_results.csv`
4. Evaluate responses using GPT-5
5. Update results with evaluation scores and comments

### Running Individual Components

You can also import and run components separately:

```python
from main import run_test_cases, evaluations

# Run only test cases
run_test_cases()

# Run only evaluations (requires existing results)
evaluations()
```

### Jupyter Notebook Analysis

Open the analysis notebooks:

```bash
jupyter notebook failure_analysis.ipynb
# or
jupyter notebook gepa_plus.ipynb
```

## 🏗️ System Components

### 1. Agent (`src/Agent.py`)

The conversational AI agent that:
- Maintains conversation history across turns
- Calls RAG API to retrieve relevant information
- Generates responses based on retrieved context
- Uses Gemini 2.5 Flash Lite model

**Key Features**:
- Session-based conversation management
- Automatic history tracking
- Integration with Chatbotix RAG platform

### 2. Evaluator (`src/auto_evaluation.py`)

AI-powered evaluation system that:
- Uses OpenAI GPT-5 for semantic evaluation
- Compares actual vs expected responses
- Validates retrieval accuracy (chunk IDs)
- Generates structured feedback with pass/fail results

**Evaluation Criteria**:
- Retrieval accuracy (chunk overlap)
- Semantic correctness (meaning preservation)
- Answer completeness
- Contextual appropriateness

### 3. Database (`src/Database.py`)

ChromaDB integration for vector storage:
- Manages document embeddings
- Handles similarity search
- Uses Gemini embedding model
- Supports persistent storage

### 4. Test Runner (`main.py`)

Orchestrates the testing pipeline:
- Loads test cases from CSV
- Manages multi-turn sessions
- Saves results incrementally
- Triggers evaluation pipeline

## 📊 Evaluation Methodology

### Evaluation Process

1. **Retrieval Evaluation**:
   - Compares actual vs expected chunk IDs
   - Accepts partial matches and related chunks
   - Considers context relevance

2. **Answer Quality Evaluation**:
   - Semantic similarity assessment
   - Accepts paraphrasing and rewording
   - Checks factual accuracy
   - Validates key information preservation

3. **Scoring**:
   - `result: true` = Response is mostly accurate
   - `result: false` = Response has significant issues
   - `comments` = Detailed explanation of decision

### Evaluation Criteria

From `evaluator_instructions.md`:

✅ **Pass Criteria**:
- Semantic correctness maintained
- Key information present
- Relevant chunks retrieved
- Minor variations acceptable

❌ **Fail Criteria**:
- Factually incorrect information
- Missing essential content
- Wrong chunks retrieved
- Off-topic responses

## 📤 Output Files

### Results CSV Structure

Generated files in `aax_results/` contain:

| Column | Description |
|--------|-------------|
| `Session ID` | Conversation session identifier |
| `Turn` | Turn number in conversation |
| `Question` | User's question |
| `Expected Chunk ID` | Ground truth chunks |
| `Actual Chunk ID` | Retrieved chunks |
| `Expected Answer` | Reference answer |
| `Actual Answer` | Agent's response |
| `Result` | Pass (true) / Fail (false) |
| `Comments` | Evaluator's detailed feedback |

### Result Files

- `aax_results-1.csv`, `aax_results-2.csv` - Initial test runs
- `aax_results-*-gepa.csv` - GEPA (advanced evaluation) results
- Each file represents a different evaluation iteration or configuration

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Test thoroughly with sample data
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

## 📝 Notes

- **Language**: Primary language is Thai (ไทย) for agent responses
- **Voice-First**: Agent optimized for voice interactions (TTS/IVR)
- **Retrieval-Bounded**: Agent only answers from provided knowledge base
- **Session Continuity**: Multi-turn conversations maintain context
- **Evaluation Model**: Uses GPT-5 for advanced semantic understanding

## 🔍 Key Technologies

- **Python 3.8+**
- **OpenAI API** (GPT-5 for evaluation)
- **Google Gemini API** (Embedding and generation)
- **ChromaDB** (Vector database)
- **Pandas** (Data processing)
- **Jupyter** (Analysis notebooks)
- **Pydantic** (Data validation)