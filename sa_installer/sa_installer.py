import os
from storage3.utils import StorageException
from supabase import create_client, Client
from dotenv import load_dotenv
# COMMAND TO RUN: python3 setup.py sdist

try:
    load_dotenv()
except FileNotFoundError:
    pass

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

assert SUPABASE_URL, "SUPABASE_URL environment variable is required"
assert SUPABASE_SERVICE_KEY, "SUPABASE_SERVICE_KEY environment variable is required"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def download_package(package_name, version=None):

    if version is None:
        response = (
            supabase.table("packages")
            .select("*")
            .eq("name", package_name)
            .order("version")
            .limit(100)
            .execute()
        )
        if not response.data:
            raise ValueError(f"Package {package_name} not found")

        version = "0.0.0"

        for package in response.data:
            print(
                f"Current version: {package['version']} - Current highest version: {version}"
            )
            if package["version"] > version:
                version = package["version"]

        print(f"Latest version of {package_name} is {version}")

    response = (
        supabase.table("packages")
        .select("*")
        .eq("name", package_name)
        .eq("version", version)
        .execute()
    )
    if not response.data:
        raise ValueError(f"Package {package_name} version {version} not found")

    response = supabase.storage.from_("packages").download(
        f"{package_name}/{version}/{package_name}-{version}.tar.gz"
    )

    # create the sa-temp directory if it doesn't exist
    if not os.path.exists("sa-tmp"):
        os.makedirs("sa-tmp")

    # save the file to the sa-temp directory
    file_name = f"{package_name}-{version}.tar.gz"
    with open("sa-tmp/" + file_name, "wb") as file:
        file.write(response)
    return "sa-tmp/" + file_name, version


def build_package():
    os.system("python3 setup.py sdist")


def upload_package(file_name, package_name, author, description, version):

    # Try a relative import to setup.py to get the author and description, version

    try:
        bytes_file = open(file_name, "rb").read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_name} not found")

    response = (
        supabase.table("packages")
        .insert(
            {
                "author": author,
                "version": version,
                "description": description,
                "name": package_name,
            }
        )
        .execute()
    )

    try:
        response = supabase.storage.from_("packages").upload(
            f"{package_name}/{version}/{file_name}", bytes_file
        )
    except StorageException as e:
        print(f"Failed to upload file {file_name}: {e}")

    print(f"File {file_name} uploaded successfully")


def install_package(file_name, version=None):

    if os.path.exists("sa-tmp/" + file_name):
        os.system(f"pip install sa-tmp/{file_name}")
        return
    elif os.path.exists(file_name):
        os.system(f"pip install {file_name}")
        return
        # check if the folder exists
    if os.path.exists("sa-tmp"):
        # read the contents of the folder
        files = os.listdir("sa-tmp")
        for file in files:
            if file_name in file and file.endswith(".tar.gz"):
                os.system(f"pip install sa-tmp/{file}")
                return
    raise FileNotFoundError(f"Package {file_name} not found")


def local_remove_package(package_name):
    os.system(f"pip uninstall {package_name} -y")
