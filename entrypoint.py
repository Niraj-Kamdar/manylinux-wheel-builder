import logging
import os
import subprocess
import sys

VERSIONS = {"3.6": "cp36-cp36m", "3.7": "cp37-cp37m", "3.8": "cp38-cp38", "3.9": "cp39-cp39"}

if __name__ == "__main__":

    args = sys.argv
    passed_versions_str = args[1]
    if not (os.getenv("TWINE_USERNAME") and os.getenv("TWINE_PASSWORD")):
        raise EnvironmentError("You have to set your TWINE_USERNAME and TWINE_PASSWORD as environment variable")

    if passed_versions_str == "3.*":
        versions = VERSIONS.keys()
    else:
        versions = []
        for version in passed_versions_str.split(","):
            versions.append(version.strip())

    for version in versions:
        logging.info(f"Building wheel for Python {version}")
        subprocess.call([f"/opt/python/{VERSIONS[version]}/bin/python", "setup.py", "bdist_wheel"])

    logging.info("Repairing wheels")
    for file in os.listdir("dist"):
        if os.path.isfile(os.path.join(os.getcwd(), "dist", file)):
            subprocess.call(["auditwheel", "repair", os.path.join(os.getcwd(), "dist", file)])

    logging.info("Uploading built binaries to PyPI")
    subprocess.call(["/opt/python/cp37-cp37m/bin/python", "-m", "twine", "upload", "wheelhouse/*"])
