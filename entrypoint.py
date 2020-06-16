import os
import subprocess

versions = {"3.6": "cp36-cp36m", "3.7": "cp37-cp37m", "3.8": "cp38-cp38", "3.9": "cp39-cp39"}
for version in versions:
    print(f"Building wheel for Python {version}")
    subprocess.call([f"/opt/python/{versions[version]}/bin/python", "setup.py", "bdist_wheel"])

print("Repairing wheels")
for file in os.listdir("dist"):
    if os.path.isfile(os.path.join(os.getcwd(), "dist", file)):
        subprocess.call(["auditwheel", "repair", os.path.join(os.getcwd(), "dist", file)])
