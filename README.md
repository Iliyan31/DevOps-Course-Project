# Course Project for Modern DevOps Practices
This repository represents the university course project for "Modern DevOps Practices" course made by Iliyan Yordanov and Tsvetelina Chakarova.

The project is distributed under GNU GENERAL PUBLIC LICENSE.

The project represents a complete automated software delivery process with pipelines using the following:


## Source control
Git is used as version control system for for source control in order to track the running history of changes to the code base, to help resolve conflicts and to make working within a shared codebase easier and more efficient.


## Branching strategies
Branching strategy is used to organize and manage the code through different GIT branches.

There is main branch which other branches are merged to when they are ready. Below the main branch there are branches for the different main tasks of the project - for example "run-unittests", "security-integration", "style-integration", etc. Some of these  branches are also splitted - for example below "style-integration" are "lint-flake8-integration", "markdown-lint-integration", etc. which are merged to "style-integration" when ready.

Moreover merching to main happens upon pull request approval.

There is Contributors guide added.s


## Building Pipelines
Pipelines are build and used for constructing, testing and deploying software code. In this project pipelines include continuous integration and continuous testing. They help for faster, easier and more correct development of the code and better maintenance of the code and it's repository as well.

GitHub Actions is used as a platform for automating pipelines. Workflows are written to be trigered when certain events occur in the repository - commits, pull requests.


## Continuous Integration with Security, Docker, Minikube and Database changes included
Continuous Integration is software development practice where developers regularly merge their code changes into a central repository, after which automated builds and tests are run.
It helps for quicker finding of mistakes and improving software quality.

There are several continuous integration pipelines made for the project. They automate the integration of new code changes into the main codebase. 

First there is the **main CI workflow - .github\workflows\ci.yml** which executes on push to any branch. It's jobs are splitted in stages with the use of the "needs" keyword in order to optimize the running time of the workflow. 

### Style Checks:
The following style checks are run on the code and the other files in the repository:
- **Check code style and lint with flake8** - the job  installs and executes the flake8 Python source linting tool. It identifies syntax errors, violations of coding conventions and other potential problems. It helps ensure that all code adheres to the same standards.
- **Check makrdown files with markdownlint-cli** - the job executes markdown linting tool. This helps maintain the quality and consistency of the markdown files.
- **Check links in markdown files** - The job checks all links in markdown files to see if they are alive or dead.
- **Editorconfig checker** - The job checks if all files are consistent to the rules specified in .editorconfig. The included .editorconfig file applies the following rules: spaces are used for identation, UTF-8 character set is used, files must end with empty line, there should be no trailing whitespaces, and more.
- **Check Python files style** - pycodestyle is a tool to check Python code against some of the style conventions in PEP8.
- **Check spelling** - This job performs spell checking on Python, Markdown and text files in the repository. It supports multiple languages. Furthermore custom dictionary -.spellcheck.yml, is added with words that are valid for the repository. but are not recognised by the action. 

### Unit tests running and Database migrations check
- **Run unit tests** - First the dependencies needed for the application src/app.py to run are installed. Then the unit tests in src/app_tests.py are run.
- **Database migrations check** - The job uses the postgres Docker image to create a PostgreSQL database container. Then it runs multiple health checks on it. If they are successful, Flyway is run to migrate a databse with the provided in the repository sql filles.

### Security Checks and Scans:
- **Snyk scan for vulnerabilities** -  The project’s dependencies are checked for vulnerabilities. They are located in src/requirement.txt.
- **SonarCloud scan** - The job scans the software code with SonarCloud to detect bugs, vulnerabilities and code smells. A "code smell" is defined as something in the code that could make it harder to maintain and evolve over time.
- **Spectral Code Scan** - The job monitors the code for exposed API keys, tokens, credentials, and high-risk security misconfiguration.
- **Bandit Vulnerability Checker** - The job runs an action for Bandit - an open-source SAST that helps identify security issues in Python code using predefined rules. It is specifically designed to find bugs in Python code that could lead to security vulnerabilities.
- **Git leaks scan** -  The job runs an action for Gitleaks - a SAST tool for detecting and preventing hardcoded secrets like passwords, API keys, and tokens in the repository.
- **Bearer Code Scanner** - The job runs an action for Bearer CLI - a SAST tool that scans the source code and analyzes data flows to discover, filter and prioritize security and privace risks.
- **Semgrep Code Scanner** - The job runs an action for Semgrep - a SAST tool used for identifying and preventing software vulnerabilities. It uses a patternt-oriented matching methodology and looks for specific patterns which may cause problems.

### Trivy Scan
The job runs an action for Trivy - a comprehensive and versatile open-source security scanner. It is used to scan for vulnerabilities in various areas including container images, file systems, git repositories, kubernetes security risks, etc.
It is recommended to be used for scanning local container image and other artifacts before pushing to a container registry or deploying the application.

### Build and publish Docker image
A Docker image is build with the help of the src/Dockerfile. The image is tagged and then uploaded to DockerHub.

Secondly, there is a workflow which executes SonarCloud scan on pull request to the main branch - **.github\workflows\merge-request.yml**.

Next, there is a workflow which executes style checks upon pull request to the main branch - **.github\workflows\pull-request-style-checks.yml**. In more detail - commit messages and branches names are expected to have name length between 10 and 100 characters. This workflow is added in order to enforce meaningful commit messages and branches names.

Last but not least, there is a workflow which checks that deplyment to Minikube is possible- **.github\workflows\ci-for-minikube.yml**. This is done by:
- starting a Minikube cluster
- checking that the pods in the cluster are working correclty
- pulling the Docker image lastly published to DockerHub from the main CI workflow
- deploying the application to the Minikube cluster with the help of the manifest files.
- checking that the deployment is successful - stoping the cluster at the end.


## Manual deployment to Minikube
Manual deployment of the Docker image to Minikube is performed in CloudShell. 
The following commands are run sequentially: \
* `docker login -u=${{ secrets.DOCKERHUB_USERNAME }} -p=${{ secrets.DOCKERHUB_PASSWORD }}`
* `docker pull ${{ secrets.DOCKERHUB_USERNAME }}/devopscourseproject:latest`
* `minikube start`
* `kubectl apply -f manifests/`
* `kubectl get pods -A`
