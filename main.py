import subprocess
import sys


def run_script(script_name):
    print("\n========================================")
    print(f"Running {script_name}...")
    print("========================================\n")

    result = subprocess.run(
        [sys.executable, script_name],
        text=True
    )

    if result.returncode != 0:
        print(f"\nERROR: {script_name} failed.")
        sys.exit(result.returncode)


def main():
    print("========================================")
    print("      AI RESUME ANALYZER")
    print("========================================")

    # Step 1: Extract resume text
    run_script("resume_parser.py")

    # Step 2: Analyze resume with Gemini
    run_script("gemini_analyzer.py")

    print("\n========================================")
    print("   RESUME ANALYSIS COMPLETED!")
    print("========================================")
    print("\nGenerated files:")
    print("- extracted_resume.txt")
    print("- analysis_result.json")


if __name__ == "__main__":
    main()