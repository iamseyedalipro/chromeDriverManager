import requests
import os
import zipfile
import platform

class ChromeDriverManager:
    """
    A class for managing the installation and updating of the chromedriver executable.
    """

    _get_latest_version_url = "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE"
    _download_url = 'https://storage.googleapis.com/chrome-for-testing-public/{version}/win64/chromedriver-win64.zip'

    def _download_file(self, url, save_path):
        """
        Download a file from a given URL and save it to the specified path.

        Parameters:
            url (str): The URL from which to download the file.
            save_path (str): The local filesystem path where the file will be saved.
        """
        try:
            # Send a GET request to the URL
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            # Get the total file size in bytes
            total_size = int(response.headers.get('content-length', 0))
            # Define a chunk size for streaming
            chunk_size = 1024
            # Variable to keep track of downloaded bytes
            downloaded_bytes = 0

            # Open the file in binary write mode
            with open(save_path, 'wb') as file:
                # Iterate over the response content in chunks
                for data in response.iter_content(chunk_size=chunk_size):
                    # Write the chunk to the file
                    file.write(data)
                    # Update the downloaded bytes count
                    downloaded_bytes += len(data)
                    # Calculate the download progress percentage
                    progress_percent = min(100, 100 * downloaded_bytes / total_size)
                    # Calculate the number of characters to represent the progress
                    progress_chars = int(progress_percent / 2)  # Each character represents 2%
                    # Symbols for progress visualization
                    symbols = ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']
                    # Calculate the index of the symbol
                    num_symbols = min(len(symbols) - 1, int(progress_percent / (100 / len(symbols))))
                    # Print the progress line dynamically
                    progress_bar = '█' * progress_chars + symbols[num_symbols] + ' ' * (50 - progress_chars)
                    print(f"\rDownloading Chrome Driver... [{progress_bar}] {progress_percent:.2f}%", end='',
                          flush=True)

            print("\nFile downloaded successfully!")
        except Exception as e:
            print("Failed to download file:", e)

    def _extract_and_rename(self, zip_file_path, extract_folder, destination_folder):
        """
        Extract the contents of a ZIP file, remove specific files, and rename the extracted folder.

        Parameters:
            zip_file_path (str): The path to the ZIP file to be extracted.
            extract_folder (str): The folder where the contents of the ZIP file will be extracted.
            destination_folder (str): The desired name for the extracted folder.
        """
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)

            # Remove specific files from the extracted folder
            file_path = os.path.join(extract_folder, 'chromedriver-win64', 'LICENSE.chromedriver')
            os.remove(file_path)
            os.remove(zip_file_path)

            # Rename the extracted folder
            extracted_folder_path = os.path.join(extract_folder, 'chromedriver-win64')
            renamed_folder_path = os.path.join(extract_folder, destination_folder)
            os.rename(extracted_folder_path, renamed_folder_path)
        except Exception as e:
            print("Failed to extract and rename files:", e)

    def _get_last_downloaded_version(self) -> str:
        """
        Retrieve the version of the last downloaded chromedriver.

        Returns:
            str: The version of the last downloaded chromedriver if available, else None.
        """
        try:
            download_folder = self._get_download_folder()
            version_file_path = os.path.join(download_folder, 'version.txt')
            if os.path.exists(version_file_path):
                with open(version_file_path, "r") as file:
                    return file.read().strip()
            else:
                return None
        except Exception as e:
            print("Failed to retrieve last downloaded version:", e)
            return None

    def install(self) -> str:
        """
        Orchestrates the installation process of chromedriver.

        Returns:
            str: The absolute path to the installed chromedriver executable.
        """
        try:
            response = requests.get(self._get_latest_version_url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            download_folder = self._get_download_folder()
            zip_file_path = os.path.join(download_folder, 'chromedriver-win64.zip')
            extract_folder = download_folder
            destination_folder = 'chromedriver'
            if response.text == self._get_last_downloaded_version():
                print("Last version of chromedriver is already installed.")
                return os.path.abspath(os.path.join(download_folder, "chromedriver", "chromedriver.exe"))

            self._download_file(self._download_url.format(version=response.text), zip_file_path)
            self._extract_and_rename(zip_file_path, extract_folder, destination_folder)

            # Create a file to save the downloaded version for next time
            version_file_path = os.path.join(download_folder, 'version.txt')
            with open(version_file_path, "w") as file:
                file.write(response.text)

            full_path = os.path.abspath(os.path.join(download_folder, "chromedriver", "chromedriver.exe"))
            return full_path
        except Exception as e:
            print("Installation failed:", e)
            if self._get_last_downloaded_version():
                print(f"Installation failed but i found a installed version {self._get_last_downloaded_version()}")
                return self._get_download_folder()
            return None

    def _get_download_folder(self) -> str:
        """
        Get the appropriate folder for saving downloaded files based on the operating system.
        If the folder doesn't exist, create it.

        Returns:
            str: The path to the appropriate download folder.
        """
        system = platform.system()
        if system == 'Windows':
            download_folder = os.path.join(os.environ['APPDATA'], 'ChromeDriverManager')
        elif system == 'Darwin':  # macOS
            download_folder = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support',
                                           'ChromeDriverManager')
        else:  # Linux or other Unix-like systems
            download_folder = os.path.join(os.path.expanduser('~'), '.config', 'ChromeDriverManager')

        # Check if the download folder exists, if not, create it
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        return download_folder
