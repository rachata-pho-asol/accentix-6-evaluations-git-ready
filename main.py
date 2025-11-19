# from src.Database import AAXEvaluationDatabase
from src.Agent import Agent
from src.auto_evaluation import Evaluator
import pandas as pd
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# COLLECTION = "aax-evaluation-data"
# AAX_DATA_CSV_PATH = "aax_data.csv"
TEST_CASES_CSV_PATH = BASE_DIR / "src" / "test_cases" / "aax_test_cases.csv"
RESULTS_CSV_PATH = BASE_DIR / "aax_results" / "aax_results" / "aax_results.csv"

# def database_initialization():
#     try:
#         db = AAXEvaluationDatabase()
#         db.add_collection(COLLECTION)
#         if not db.contains_data(collection_name=COLLECTION):
#             db.add_data(from_csv=AAX_DATA_CSV_PATH, to_collection=COLLECTION)
#         print("Database Initialized successfully")
#         return db
#     except Exception as e:
#         print(f"Error during database initialization: {e}")
#
# def function_executer(response, db: AAXEvaluationDatabase):
#     function_call_part = None
#     for candidate in response.candidates:
#         for part in candidate.content.parts:
#             if hasattr(part, 'function_call') and part.function_call:
#                 function_call_part = part
#                 break
#         if function_call_part:
#             break
#     if function_call_part:
#         try:
#             function_call = function_call_part.function_call
#             if function_call.name == "query_chroma":
#                 result = db.query_chroma(**function_call.args, from_collection=COLLECTION)
#                 return result
#             else:
#                 raise ValueError(f"Unknown function call: {function_call.name}")
#         except Exception as e:
#             print(f"Error executing function call: {e}")
#     else:
#         print("No function call found in the response.")
#         return None

# def save_agent_result(session_id: int, turn: int, function_call_result, answer: str):
#     # Read the existing CSV
#     df = pd.read_csv(TEST_CASES_CSV_PATH)
#
#     # Add "Agent Query" column if it doesn't exist (between "Expected Chunk ID" and "Actual Chunk ID")
#     if 'Agent Query' not in df.columns:
#         # Get the position of "Expected Chunk ID"
#         expected_chunk_id_pos = df.columns.get_loc('Expected Chunk ID')
#         # Insert "Agent Query" right after it
#         df.insert(expected_chunk_id_pos + 1, 'Agent Query', None)
#
#     # Extract the agent query from function_call_result
#     agent_query = None
#     if function_call_result and 'query' in function_call_result:
#         agent_query = function_call_result['query']
#
#     # Extract the chunk IDs from function_call_result
#     actual_chunk_ids = None
#     if function_call_result:
#         retrieve_results = function_call_result['results']
#         print(f"Retrieved {len(retrieve_results)} results.")
#         # Join all IDs with comma separator
#         actual_chunk_ids = ', '.join(item['id'] for item in retrieve_results)
#
#     # Find the row matching session_id and turn
#     mask = (df['Session ID'] == session_id) & (df['Turn'] == turn)
#
#     if mask.any():
#         # Update the existing row
#         df.loc[mask, 'Agent Query'] = agent_query
#         df.loc[mask, 'Actual Chunk ID'] = actual_chunk_ids
#         df.loc[mask, 'Actual Answer'] = answer
#
#         # Save back to CSV
#         df.to_csv(TEST_CASES_CSV_PATH, index=False, encoding='utf-8')
#         print(f"Updated Session {session_id}, Turn {turn}")
#     else:
#         print(f"Warning: No matching row found for Session {session_id}, Turn {turn}")

# def run_test_cases():
#     # Initialize agent and database
#     db = database_initialization()
#
#     test_case_df = pd.read_csv(TEST_CASES_CSV_PATH)
#
#     # Split test cases into a session by "Session ID"
#     sessions = test_case_df.groupby('Session ID')
#
#     for session_id, session_df in sessions:
#         # Each session cantains multiple turns (test cases), We should loop through each turn
#         # if hash(session_id) < 11:
#         #     continue
#         print("=" * 40)
#         print(f"Processing Session ID: {session_id}")
#
#         agent = Agent()
#         for idx, row in session_df.iterrows():
#             try:
#                 print(f"Processing Turn: {row['Turn']}...")
#                 user_query = row["Question"]
#                 response = agent.generate_response(user_query)
#                 result = function_executer(response, db)
#                 if result:
#                     agent.save_function_call_response(result)
#                 else:
#                     print(f"No function call result to process for Turn {row['Turn']}. Retrying...")
#                     print("-" * 20)
#                     while True:
#                         response = agent.generate_response(query="You have to call the function to get the data. And answer this user query: " + user_query)
#                         result = function_executer(response, db)
#                         if result:
#                             agent.save_function_call_response(result)
#                             break
#             except Exception as e:
#                     print(f"Error processing Turn {row['Turn']}: {e}. Retrying...")
#                     print("-" * 20)
#             final_response = agent.generate_response(query=None)
#             save_agent_result(session_id=hash(session_id), turn=row["Turn"], function_call_result=result, answer=final_response.text)
#
# def evaluations():
#     evaluator = Evaluator()
#     test_case_df = pd.read_csv(TEST_CASES_CSV_PATH)
#
#     test_case_df.drop(columns=['AAX Review', 'Status', 'Comment'], inplace=True, errors='ignore')
#
#     # Add new column for evaluation: 'Result', 'Comments'
#     if 'Result' not in test_case_df.columns:
#         test_case_df['Result'] = ''
#     if 'Comments' not in test_case_df.columns:
#         test_case_df['Comments'] = ''
#
#     sessions = test_case_df.groupby('Session ID')
#
#     print("Starting Evaluations")
#
#     for session_id, session_df in sessions:
#         print("=" * 40)
#         print(f"Evaluating Session ID: {session_id}")
#         conversations = []
#
#         for idx, row in session_df.iterrows():
#             print(f"Processing Turn: {row['Turn']}...")
#             result = evaluator.evaluate(row, conversations)
#             # Save conversation history
#             conversations.append({
#                 'user': row['Question'],
#                 'agent': row['Actual Answer']
#             })
#
#             # Save result into DataFrame
#             test_case_df.at[idx, 'Result'] = result.result
#             test_case_df.at[idx, 'Comments'] = result.comments
#
#     # Save back to CSV
#     test_case_df.to_csv(RESULTS_CSV_PATH, index=False, encoding='utf-8')

def save_agent_result(session_id: int, turn: int, result):
    # If the results CSV does not exist, duplicate the test cases CSV to create it
    if not os.path.exists(RESULTS_CSV_PATH):
        pd.read_csv(TEST_CASES_CSV_PATH).to_csv(RESULTS_CSV_PATH, index=False, encoding='utf-8')
    # Load the results CSV
    df = pd.read_csv(RESULTS_CSV_PATH)

    # Convert the column into appropriate types
    df['Actual Chunk ID'] = df['Actual Chunk ID'].astype(str)
    df['Actual Answer'] = df['Actual Answer'].astype(str)

    # Extract the chunk IDs from result
    actual_idx = 0
    for i in range(turn-1):
        actual_idx += 2

    turn_data = result["history"][actual_idx]
    rag_metadata = turn_data["metadata"]

    if len(rag_metadata) > 0:
        rag_data = rag_metadata[0]["data"]

        # rag_data is an array contains multiple pages where each page contains a 'docs', 'docs' is also an array which contains multiple chunks.
        # We need to extract all chunk IDs from all pages. sort by "top_k_from_model" by ascending order and join them with comma.
        chunk_ids = []
        for page in rag_data:
            for doc in page["docs"]:
                chunk_ids.append((doc["chunk_id"], doc["top_k_from_model"]))
        # Sort by top_k_from_model
        chunk_ids.sort(key=lambda x: x[1])
        # Extract only chunk IDs (Top 5)
        # chunk_ids = chunk_ids[:5]
        actual_chunk_ids = ",".join([str(chunk_id) for chunk_id, _ in chunk_ids])
    else:
        actual_chunk_ids = None

    # Extract the agent's answer
    answer = result["text"]

    # Find the row matching session_id and turn
    mask = (df['Session ID'] == session_id) & (df['Turn'] == turn)

    if mask.any():
        # Update the existing row
        df.loc[mask, 'Actual Chunk ID'] = actual_chunk_ids
        df.loc[mask, 'Actual Answer'] = answer

        # Save back to CSV
        df.to_csv(RESULTS_CSV_PATH, index=False, encoding='utf-8')
        print(f"Updated Session {session_id}, Turn {turn}")
    else:
        print(f"Warning: No matching row found for Session {session_id}, Turn {turn}")

def run_test_cases():
    test_cases_df = pd.read_csv(TEST_CASES_CSV_PATH)

    # Split test cases into sessions by grouping "Session ID"
    sessions = test_cases_df.groupby('Session ID')

    for session_id, session_df in sessions:
        # Each session contains multiple turns
        agent = Agent()

        print("=" * 40)
        print(f"Processing Session ID: {session_id}")
        for idx, turn in session_df.iterrows():
            try:
                print(f"Processing Turn: {turn['Turn']}")
                user_query = turn['Question']
                response = agent.generate_response(query=user_query)
                save_agent_result(hash(session_id), turn['Turn'], response)
            except Exception as e:
                print(f"Error processing Session {session_id}, Turn {turn['Turn']}: {e}")

def evaluations():
    evaluator = Evaluator()
    result_df = pd.read_csv(RESULTS_CSV_PATH)

    # Drop insignificant columns (if they exist)
    if 'AAX Review' in result_df.columns and 'Status' in result_df.columns and 'Comment' in result_df.columns:
        result_df.drop(['AAX Review', 'Status', 'Comment'], axis=1, inplace=True)

    # Add new columns for evaluation: 'Result', 'Comments'
    if 'Result' not in result_df.columns:
        result_df['Result'] = ''
    if 'Comments' not in result_df.columns:
        result_df['Comments'] = ''

    # Split test cases into sessions by grouping "Session ID"
    sessions = result_df.groupby('Session ID')

    print("Starting Evaluations...")
    for session_id, session_df in sessions:
        print("=" * 40)
        print(f"Evaluating Session ID: {session_id}")
        for idx, turn in session_df.iterrows():
            print(f"Evaluating Turn: {turn['Turn']}")
            result = evaluator.evaluate(turn)

            # Update the DataFrame with evaluation results
            result_df.at[idx, 'Result'] = result.result
            result_df.at[idx, 'Comments'] = result.comments

    # Save back to CSV
    result_df.to_csv(RESULTS_CSV_PATH, index=False, encoding='utf-8')
    print("Evaluations completed and results saved.")

if __name__ == "__main__":
    run_test_cases()
    evaluations()