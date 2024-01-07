import requests
import json
import pyperclip

# Function to search for papers based on a query
def search_papers(query, seen_ids=[], offset=0, limit=10):
    base_url = "http://api.semanticscholar.org/graph/v1/paper/search"
    params = {'query': query, 'fields': 'title,authors,abstract', 'offset': offset, 'limit': limit}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        fetched_data = json.loads(response.text)
        new_papers = [paper for paper in fetched_data['data'] if paper['paperId'] not in seen_ids]
        total_results = fetched_data['total']
        return new_papers, total_results
    else:
        return None, 0
    

# Function to store fetched data in a JSON file
def store_data_as_json(query, data, filename, append=False):
    stored_data = {}
    if append:
        try:
            with open(filename, 'r') as f:
                file_content = f.read().strip()
                if file_content:  # Check if file is not empty
                    stored_data = json.loads(file_content)
        except FileNotFoundError:
            pass
    if query not in stored_data:
        stored_data[query] = []
    stored_data[query].extend(data)
    with open(filename, 'w') as f:
        json.dump(stored_data, f)

# Function to fetch paper details including abstract by paper ID
def fetch_paper_details(paper_id):
    base_url = f"http://api.semanticscholar.org/graph/v1/paper/{paper_id}"
    response = requests.get(base_url)
    if response.status_code == 200:
        paper_details = json.loads(response.text)
        return paper_details
    else:
        return None


# Function to add a paper to a user-defined list
def add_paper_to_user_list(paper, user_selected_list):
    from datetime import datetime
    user_lists = {}
    try:
        with open('user_lists.json', 'r') as file:
            file_content = file.read().strip()
            if file_content:  # Check if file is not empty
                user_lists = json.loads(file_content)
    except FileNotFoundError:
        pass  # file does not exist, we'll create it later

    if user_selected_list not in user_lists:
        user_lists[user_selected_list] = []
    paper['added_at'] = datetime.now().isoformat()
    user_lists[user_selected_list].append(paper)
    
    with open('user_lists.json', 'w') as file:
        json.dump(user_lists, file)


# Main function for CLI interface
import os

def main():
    keywords = []
    completed_queries = []
    if not os.path.exists('keywords.txt'):
        with open('keywords.txt', 'w') as file:
            file.write("")
    with open('keywords.txt', 'r') as file:
        keywords = [line.strip() for line in file if line.strip()]
    if not keywords:
        print("No keywords found. Please add keywords to the 'keywords.txt' file.")
        return

    try:
        with open('seen_paper_ids.json', 'r') as file:
            seen_paper_ids = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        seen_paper_ids = {}

    try:
        with open('completed_search_queries.txt', 'r') as file:
            completed_queries = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        pass

    offset = 0
    limit = 10
    new_query = ''
    while True:
        if new_query:
            query = new_query
        else:
            query = keywords[0]
        if query in completed_queries:
            print(f"Skipping completed query: {query}")
            keywords.pop(0)
            continue
        print(f"Searching for papers on: {query}")
        offset = 0  # Resetting the offset for each new query

        new_papers, total_results = search_papers(query, seen_ids=seen_paper_ids.get(query, []), offset=offset, limit=limit)
        if len(keywords) > 1:
            print(f"Next query: {keywords[1]}")
        if new_papers is not None and len(new_papers) < limit and total_results > limit:
            offset += 10
            new_papers, total_results = search_papers(query, seen_ids=seen_paper_ids.get(query, []), offset=offset, limit=limit)
        
        if new_papers is not None:
            paper_titles = []
            for i, paper in enumerate(new_papers, 1):
                title = f"{i}. {paper['title']}"
                paper_titles.append(title)
                print(title)
                seen_paper_ids.setdefault(query, []).append(paper['paperId'])
                
            pyperclip.copy("Select papers to save by index (comma-separated):"+'\n'.join(paper_titles))
            selected_indices = input("Select papers to save by index (comma-separated): ").split(',')
            selected_papers = [new_papers[int(index) - 1] for index in selected_indices if index.isdigit()]
        
            # Load existing user lists
            user_lists = {}
            try:
                with open('user_lists.json', 'r') as file:
                    user_lists = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                # file does not exist or is empty, create it with an empty dictionary
                with open('user_lists.json', 'w') as file:
                    json.dump({}, file)
                user_lists = {}

            # Print existing list names
            if user_lists:
                print("Existing lists:")
                for list_name in user_lists.keys():
                    print(f"- {list_name}")

            list_name = input("Enter the name of the list to save the selected papers: ")
            append_data = True
        
            for paper in selected_papers:
                paper['search_query'] = query
                add_paper_to_user_list(paper, list_name)
            store_data_as_json(query, new_papers, 'new_papers.json', append=append_data)
        
        else:
            print("Failed to fetch new papers. Would you like to retry? (y/n): ")
            cont = input().lower()
            if cont == 'n':
                break
        #store_data_as_json(query, seen_paper_ids, 'seen_paper_ids.json', append=append_data)
        with open('seen_paper_ids.json', 'a') as file:
            json.dump(seen_paper_ids, file)
        with open('completed_search_queries.txt', 'a') as file:
            file.write(f"{query}\n")
        cont = input("Would you like to fetch more papers with the same query? (y/n): ").lower()
        if cont == 'y':
            offset += len(new_papers)
            seen_paper_ids[query] = seen_paper_ids.get(query, [])
            continue
        else:
            cont = input("Would you like to continue with a new query? (y/n): ").lower()
            if cont == 'y':
                query = input("Enter the new search query: ").strip()
                keywords.append(query)  # Add the new keyword to the end of the list
                offset = 0  # Resetting the offset for the new query
                new_query = query
            else:
                continue
        new_query = ''
        keywords.pop(0)


if __name__ == "__main__":
    main()
