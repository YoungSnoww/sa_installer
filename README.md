# sa_installer

This is a simple script to manage private python package in a supabase project.

## Installation

```bash
pip install sa-installer
```

## Usage

```bash
pip_sa --help
```

```
usage: pip_sa [-h] {download,build,upload,install,remove,clean} ...

Supabase Package Manager

positional arguments:
  {download,build,upload,install,remove,clean}
                        Commands
    download            Download a package
    build               Build a package
    upload              Upload a package
    install             Install a package
    remove              Remove a package
    clean               Clean temporary files

options:
  -h, --help            show this help message and exit

```

## Proper setup - For CI/CD

1. Create a new supabase project
2. Create a new schema called using the [database.sql](database.sql) file
3. Get the supabase url and key
4. Create a bucket in the storage section named `packages`

#### Install the package

```bash
python -m pip install sa-installer
```

#### Setup the environment variables

```bash
export SUPABASE_URL=YOUR_SUPABASE_URL
export SUPABASE_KEY=YOUR_SUPABASE_KEY
```

#### Create the sa_release.json file

```json
{
    "author": "Your Name",
    "description": "Your package description",
    "version": "0.0.1",
}
```

#### Run the following commands

```bash
pip_sa build
pip_sa upload PackageName
```

#### Clean the temporary files

```bash
pip_sa clean
```

#### Install the package

```bash
pip_sa download PackageName
pip_sa install PackageName
```

#### Remove the package

```bash
pip_sa remove PackageName
```

### Author Notes
The project is released under the MIT License. Feel free to use it in your projects. If you have any questions or suggestions, feel free to open an issue or a pull request.

Please **NOTE** that the project is very problem specific and may not be useful for everyone. Furthermore there is no developpement planned for this project on the long term. The project purpose is to fix a specific temporary issue.

