# Contributing to Quira

First off, thank you for considering contributing to Quira! It's people like you that make Quira such a great tool for the community.

## Where do I go from here?

If you've noticed a bug or have a feature request, make sure to check our [Issues](https://github.com/DevDarsh26/Quira/issues) first to see if someone else has already created it. If not, feel free to open a new one!

## Setting up your development environment

1. **Fork** the repo on GitHub.
2. **Clone** the project to your own machine.
3. **Set up** a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```
4. **Install** dependencies:
   ```bash
   pip install -e ".[dev,all]"
   ```

## Making Changes

- Ensure your code adheres to standard Python styling (we use `black`).
- Write tests for your changes. Run the existing tests using `pytest tests/`.
- If you're adding a new Provider (e.g., a new Vector Store or LLM), ensure you implement the abstract base classes in `quira/providers/base.py`.

## Submitting a Pull Request

1. Create a new branch: `git checkout -b my-feature-branch`
2. Commit your changes: `git commit -m 'Add some feature'`
3. Push to the branch: `git push origin my-feature-branch`
4. Submit a pull request on GitHub!

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.
