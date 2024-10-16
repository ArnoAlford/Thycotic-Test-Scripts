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

    # Modify folder stub properties
    folder_stub['folderName'] = "<Folder Name>"  # Replace with actual folder name
    folder_stub['folderTypeId'] = 1
    folder_stub['inheritPermissions'] = False
    folder_stub['inheritSecretPolicy'] = False
    folder_stub['parentFolderId'] = "<Parent Folder ID>"  # Replace with actual parent folder ID

    # Convert the folder stub to JSON for the POST request
    folder_args = json.dumps(folder_stub)

    # Add Child Folder
    folder_add_url = f"{api}/folders"
    folder_child_add_response = requests.post(folder_add_url, data=folder_args, headers=headers)

    if folder_child_add_response.status_code != 200:
        raise Exception(f"Error: {folder_child_add_response.status_code} - {folder_child_add_response.text}")

    folder_child_add_result = folder_child_add_response.json()
    child_folder_id = folder_child_add_result.get('id')

    if child_folder_id > 1:
        print("\n-----------------------")
        print("-- Add Child Folder Successful --")
        print("-----------------------\n")
        print(json.dumps(folder_child_add_result, indent=4))

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
