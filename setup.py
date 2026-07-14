    from pathlib import Path
    from setuptools import find_packages, setup


    BASE_DIR = Path(__file__).resolve().parent


    def get_requirements() -> list[str]:
        """Read and return dependencies from requirements.txt."""
        requirements_file = BASE_DIR / "requirements.txt"

        if not requirements_file.exists():
            raise FileNotFoundError(
                f"requirements.txt was not found at: {requirements_file}"
            )

        requirements = []

        for line in requirements_file.read_text(encoding="utf-8").splitlines():
            dependency = line.strip()

            # Ignore blank lines, comments, and editable package references.
            if not dependency or dependency.startswith("#"):
                continue

            if dependency == "-e .":
                continue

            requirements.append(dependency)

        return requirements


    setup(
        name="stock-market-analysis-app",
        version="0.1.0",
        author="Anand Gajaria",
        description=(
            "A Streamlit application for stock analysis, technical indicators, "
            "forecasting, beta, and CAPM expected-return analysis."
        ),
        packages=find_packages(),
        py_modules=[],
        install_requires=get_requirements(),
        python_requires=">=3.9",
    )