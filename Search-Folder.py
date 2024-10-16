import requests
import json

try:
    api = "<Secret Server URL>/api/v1"
    token = "<TOKEN>"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Get Folder Stub (optional if it's needed for another part of the script)
    folder_stub_url = f"{api}/folders/stub"
    folder_stub_response = requests.get(folder_stub_url, headers=headers)

    if folder_stub_response.status_code != 200:
        raise Exception(f"Error: {folder_stub_response.status_code} - {folder_stub_response.text}")

    folder_stub = folder_stub_response.json()

    # Search filter
    search_text = "<Search Text>"  # Replace with actual search text
    search_filter = f"?filter.searchText={search_text}"

    # Search for folders
    search_url = f"{api}/folders{search_filter}"
    search_results_response = requests.get(search_url, headers=headers)

    if search_results_response.status_code != 200:
        raise Exception(f"Error: {search_results_response.status_code} - {search_results_response.text}")

    search_results = search_results_response.json()

    # Check if search returned any results
    if search_results.get('total', 0) > 0:
        folder = search_results['records'][0]
        print(json.dumps(search_results, indent=4))
        print(json.dumps(folder, indent=4))

        folder_name = "<Folder Name>"  # Replace with the folder name you are searching for
        if folder.get('folderName') == folder_name:
            print("\n------------------------------")
            print("-- Search Folder Successful --")
            print("------------------------------\n")
            print(json.dumps(folder, indent=4))
        else:
            print("ERROR: Folder name does not match.")
    else:
        print("ERROR: Failed to Search Folders.")

except requests.exceptions.RequestException as e:
    print("----- Exception -----")
    if e.response is not None:
        print(f"Status Code: {e.response.status_code}")
        print(f"Status Description: {e.response.reason}")
        response_body = e.response.text
        try:
            error_details = json.loads(response_body)
            print(f"{error_details.get('errorCode', 'Unknown error')} - {error_details.get('message', 'No message')}")
            model_state = error_details.get('modelState', [])
            for state in model_state:
                print(state)
        except json.JSONDecodeError:
            print("Response body is not in JSON format:", response_body)
    else:
        print(e)
