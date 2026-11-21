# Herb CSV Processor
Upload a CSV, process using the agreed title/weight/quantity/price rules, and save an XLSX.

## Build the Windows EXE using GitHub
1. Create a new GitHub repository.
2. Upload `app.py`, `requirements.txt`, and the `.github/workflows/build-windows.yml` file (keep the folder structure).
3. Open the repository's **Actions** tab and select **Build Windows EXE**.
4. Click **Run workflow** (or wait for the push-triggered build to finish).
5. Open the completed run and download the `HerbCSVProcessor-Windows` artifact.
6. Extract the ZIP and run `HerbCSVProcessor.exe` on Windows.

Python is not required on the PC that runs the finished EXE.
