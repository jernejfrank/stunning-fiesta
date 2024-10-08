import nox

def add_uv_to_environ() -> None:
    import os
    import subprocess
    from pathlib import Path

    path_to_uv_pythons = (
        subprocess.check_output(
            ["uv", "python", "dir"], env={"NO_COLOR": "1", **os.environ}
        )
        .decode()
        .strip()
    )
    paths_new = ":".join(map(str, Path(path_to_uv_pythons).glob("*/bin")))
    paths_old = os.environ["PATH"]
    os.environ["PATH"] = f"{paths_new}:{paths_old}"


add_uv_to_environ()


py_versions = ["3.12","3.11", "3.10", "3.9"]

@nox.session(python=py_versions,venv_backend="uv")
def tests(session):
    session.install(".",)
    session.install("pytest", "pytest-cov")
    session.run("pytest", "--cov")
    session.run("pytest")