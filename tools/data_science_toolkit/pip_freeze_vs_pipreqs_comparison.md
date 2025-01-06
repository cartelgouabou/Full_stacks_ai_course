# Tutorial: Comparing pip freeze vs pipreqs

When working with Python projects, creating a requirements.txt file is essential to document the dependencies needed to run your project. Two popular tools for generating this file are pip freeze and pipreqs. This tutorial will compare the two tools and explain why pipreqs is often the better option.

## 1. What is pip freeze?

pip freeze lists all installed packages in your current Python environment, including both direct dependencies and unrelated packages.

### How to Use pip freeze
1. Run the following command:
```bash
   pip freeze > requirements.txt
   ```
2. This generates a `requirements.txt` file containing all installed packages in your environment.

### Example Output
```plaintext
   absl-py==1.3.0
   astunparse==1.6.3
   cachetools==5.2.0
   matplotlib==3.8.0
   numpy==1.23.5
   tensorflow==2.12.0
   tensorflow-datasets==4.9.2
   ```

## Limitations of `pip freeze`

- **Lists unnecessary packages**: Includes all packages in the environment, even those not used in the project.
- **Not project-specific**: If your environment contains packages installed for other projects, they will also appear in the requirements.txt.
- **Bloated file**: Results in larger, less accurate requirements.txt files.

---
## 2. What is pipreqs?

pipreqs generates a requirements.txt file by scanning your project directory and analyzing the import statements in your Python code. It only includes packages that are explicitly used in your project.

### How to Use pipreqs

1. Install pipreqs:
```bash
   pip install pipreqs
   ```
2. Run the following command in your project directory:
```bash
   pipreqs . --force
   ```
3. This generates a `requirements.txt` file with only the required dependencies.

### Example Output
```plaintext
   tensorflow==2.12.0
   tensorflow-datasets==4.9.2
   matplotlib==3.8.0
   numpy==1.23.5
   ```
### Advantages of pipreqs

- **Includes only relevant packages**: Only dependencies explicitly imported in your project are listed.
- **Project-specific**: Scans your project directory for imports, avoiding unrelated packages.
- **Cleaner**: requirements.txt: Results in a minimal, accurate dependency list.

## When use pipreqs or pip freeze?
### Use pipreqs
- When you want a minimal requirements.txt file containing only the dependencies relevant to your project.
- For smaller, well-defined projects where you are actively using specific libraries.

### Use pip freeze
- When you want to capture the entire environment for reproducibility, such as when sharing a virtual environment for development or deployment.


For most real-world projects, pipreqs is better suited, as it creates accurate, project-specific dependency files that are easy to maintain.