

class SearchManager:
    def __init__(self, db_manager, utils, client, summarier_model):
        self.db_manager = db_manager
        self.utils = utils
        self.client = client
        self.summarier_model = summarier_model

    def search_chat_history(self, search_term: str) -> list:
        """
        Searches chat history for a term, performing a case-insensitive lookup.

        Args:
            search_term (str): The keyword to search in the chat history.

        Returns:
            list: List of tuples containing matching question, answer, and timestamp.
        """
        search_term = search_term.lower()
        query = """
        SELECT question, answer, timestamp FROM chat_history
        WHERE LOWER(question) LIKE ? OR LOWER(answer) LIKE ?
        ORDER BY timestamp ASC
        LIMIT 3;
        """

        results = self.db_manager.execute_query(
            query, (f"%{search_term}%", f"%{search_term}%"), fetch_all=True)
        # Ensure the results maintain the order of question, then answer
        formatted_results = [(q, a, t) for q, a, t in results]

        num_characters = self.utils.count_number_of_characters(str(results))
        print(f"Number of characters in search results: {num_characters}")
        if num_characters > 1000:
            results = self.summarize_search_result(str(formatted_results))
            return results
        return formatted_results

    def summarize_search_result(self, search_result: str) -> str:

        response = self.client.chat.completions.create(
            model=self.summarier_model,
            messages=[{"role": "system", "content": "Summarize the following conversation within 1000 characters"},
                      {"role": "user", "content": search_result}]
        )
        response = response.choices[0].message.content
        return response
