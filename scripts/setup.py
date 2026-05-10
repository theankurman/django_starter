# # setup the environment for development

import secrets
import subprocess
import shutil
from pathlib import Path
import re

uv = shutil.which("uv")
bun = shutil.which("bun")
just = shutil.which("just")
git = shutil.which("git")
if not uv:
    raise Exception(
        "uv not found in path. Visit `https://github.com/astral-sh/uv` to install it."
    )
if not bun:
    raise Exception(
        "bun not found in path. Visit `https://github.com/oven-sh/bun` to install it."
    )
if not just:
    raise Exception(
        "just not found in path. You can install it with `uv tool install rust-just`"
    )
if not git:
    raise Exception("git not found in path. Please install git before continuing.")

# initialise git if not
git_inited = (
    subprocess.check_output([git, "rev-parse", "--is-inside-work-tree"], text=True)
    == "true"
)
if not git_inited:
    subprocess.run([git, "init", "-b", "main"])


# install python dependencies
subprocess.run([uv, "sync"])

# install js dependencies
subprocess.run([bun, "i"])


# create .env file if not exists
env_file = Path(".env")
example_env_file = Path(".env.example")
if not env_file.exists():
    example_env_file.copy(env_file)


# set secret key in env file if not set
env_content = env_file.read_text()
empty_secret_pattern = re.compile(r"^SECRET_KEY=\"\"$", re.MULTILINE)
new_secret = secrets.token_urlsafe(32)
env_content = empty_secret_pattern.sub(f'SECRET_KEY="{new_secret}"', env_content)
env_file.write_text(env_content)

# setup prek
prek = shutil.which("prek")
if prek:
    subprocess.run([prek, "install"])
else:
    subprocess.run(["uvx", "prek", "install"])

# build frontend assets
subprocess.run([just, "build"])
# migrate the database
subprocess.run([just, "migrate"])
