import requests
import zipfile

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


if __name__ == "__main__":
    file_id = '1ReqNwIEXvjyE3xTnvySCrhceR51lFXZQ'
    destination = 'pswd_file.zip'
    password = 'datacamp'
    download_file_from_google_drive(file_id, destination)
    print("Downloaded File!")

    try:
        with zipfile.ZipFile(destination) as file:
            print("The Zip file is not-corrupted")
    except zipfile.BadZipFile:
        print('Error: Zip file is corrupted')

    with zipfile.ZipFile(destination) as zf:
        zf.extractall(pwd=bytes(password, 'utf-8'))
        print("Extracted!")