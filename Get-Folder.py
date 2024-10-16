import requests
import json

try:
    api = "<Secret Server URL>/api/v1"
    token = "<TOKEN>"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Get Folder Stub
    folder_stub_url = f"{api}/folders/stub"
    folder_stub_response = requests.get(folder_stub_url, headers=headers)

    if folder_stub_response.status_code != 200:
        raise Exception(f"Error: {folder_stub_response.status_code} - {folder_stub_response.text}")

    folder_stub = folder_stub_response.json()

    folder_id = "<Your Secret ID>"  # Replace with actual folder ID

    # Get Folder by ID
    folder_get_url = f"{api}/folders/{folder_id}"
    folder_get_response = requests.get(folder_get_url, headers=headers)

    if folder_get_response.status_code != 200:
        raise Exception(f"Error: {folder_get_response.status_code} - {folder_get_response.text}")

    folder_get_result = folder_get_response.json()

    if folder_get_result.get('id') == folder_id:
        print("\n-----------------------")
        print("-- Get Folder Successful --")
        print("-----------------------\n")
        print(json.dumps(folder_get_result, indent=4))

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
