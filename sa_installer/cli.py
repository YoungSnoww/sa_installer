import argparse
import sys
import os

from sa_installer.sa_installer import (
    download_package,
    build_package,
    upload_package,
    install_package,
    local_remove_package,
)


class CLI:

    def __init__(self):

        self.__init_parser()

        self.commands = {
            "download": self.download,
            "build": self.build,
            "upload": self.upload,
            "install": self.install,
            "remove": self.remove,
            "clean": self.clean,
        }

        self.cwd = os.getcwd()
        self.sa_tmp = os.path.join(self.cwd, "sa-tmp")

    def __init_parser(self):
        self.parser = argparse.ArgumentParser(description="Supabase Package Manager")

        self.parser.add_argument(
            "-v", "--verbose", action="store_true", help="Verbose mode"
        )
        subparsers = self.parser.add_subparsers(dest="command", help="Commands")

        # Download command
        download_parser = subparsers.add_parser("download", help="Download a package")
        download_parser.add_argument(
            "package_name", help="Name of the package to download"
        )
        download_parser.add_argument(
            "version", nargs='?', default=None, help="Version of the package to download",
        )

        # Build command
        subparsers.add_parser("build", help="Build a package")

        # Upload command
        upload_parser = subparsers.add_parser("upload", help="Upload a package")
        upload_parser.add_argument("package_name", help="Name of the package to upload")
        upload_parser.add_argument("version", help="Version of the package to upload")

        # Install command
        install_parser = subparsers.add_parser("install", help="Install a package")
        install_parser.add_argument(
            "file_name", help="File name of the package to install"
        )

        # Remove command
        remove_parser = subparsers.add_parser("remove", help="Remove a package")
        remove_parser.add_argument("package_name", help="Name of the package to remove")

        # Clean command
        subparsers.add_parser("clean", help="Clean temporary files")

    def download(self, package_name, version=None, **kwargs):
        file_name, version = download_package(package_name, version)
        print(f"Package {package_name} version {version} downloaded to {file_name}")

    def build(self, **kwargs):
        try:
            build_package()
        except Exception as e:
            print(f"Failed to build package: {e}")
            sys.exit(1)
        print("Package built successfully")

    def upload(self, package_name, version, **kwargs):

        file_name = f"{package_name}-{version}.tar.gz"

        # Check if the file exists in the dist directory
        if os.path.exists(f"dist/{file_name}"):
            file_name = f"dist/{file_name}"
        else:
            print(f"File {file_name} not found in dist directory")
            sys.exit(1)
        try:
            upload_package(file_name, package_name)
        except Exception as e:
            print(f"Failed to upload package: {e}")
            sys.exit(1)
        print(f"Package {package_name} version {version} uploaded successfully")

    def install(self, file_name, **kwargs):
        try:
            install_package(file_name)
        except Exception as e:
            print(f"Failed to install package: {e}")
            sys.exit(1)
        print(f"Package {file_name} installed successfully")

    def remove(self, package_name, **kwargs):
        try:
            local_remove_package(package_name)
        except Exception as e:
            print(f"Failed to remove package: {e}")
            sys.exit(1)
        print(f"Package {package_name} removed successfully")

    def clean(self, **kwargs):
        try:
            os.system(f"rm -rf {self.sa_tmp}")
        except Exception as e:
            print(f"Failed to clean: {e}")
            sys.exit(1)
        print("Cleaned successfully")

    def run(self):

        args = self.parser.parse_args()
        command = args.command

        if command not in self.commands:
            print(f"Command {command} not found")
            sys.exit(1)

        from pprint import pprint

        pprint(vars(args))

        self.commands[command](**vars(args))


if __name__ == "__main__":
    cli = CLI()
    cli.run()