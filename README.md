# Defectdojo-importer

DefectDojo Cli utility for importing scan findings.

## Getting started

### Installation

Using pip
```bash
pip install defectdojo-importer
```

Using docker
```
docker build -t defectdojo-importer .
```

## Usage

Command Usage

```
usage: defectdojo-importer [-h] [-f FILE] [-t {findings,languages}] [--api-url API_URL] [--api-key API_KEY] [--product-name PRODUCT_NAME]    
                           [--product-type-name PRODUCT_TYPE_NAME] [--critical-product] [--product-platform PRODUCT_PLATFORM] [--engagement-name ENGAGEMENT_NAME]
                           [--test-name TEST_NAME] [--test-type-name TEST_TYPE_NAME] [--static-tool] [--dynamic-tool] [--tool-configuration-name TOOL_CONFIGURATION_NAME] [--tool-configuration-params TOOL_CONFIGURATION_PARAMS] [--minimum-severity {Info,Low,Medium,High,Critical}]
                           [--push-to-jira] [--close-old-findings] [--reimport] [--reimport-condition {default,branch,commit,build,pull_request}] 
                           [--build-id BUILD_ID] [--commit-hash COMMIT_HASH] [--branch-tag BRANCH_TAG] [--scm-uri SCM_URI] [-v] [-i]
                            ...

Defect Dojo CI tool for importing scan findings

options:
  -h, --help            show this help message and exit

Scan Import Configuration:
  -f, --file FILE       File to import
  -t, --import-type {findings,languages}
                        Type of import: findings or languages, default is findings.

DefectDojo Configuration:
  --api-url API_URL     DefectDojo API URL
  --api-key API_KEY     DefectDojo API Key
  --product-name PRODUCT_NAME
                        Product name
  --product-type-name PRODUCT_TYPE_NAME
                        Product type name
  --critical-product    Is product critical?
  --product-platform PRODUCT_PLATFORM
                        Product platform

Test Configuration:
  --engagement-name ENGAGEMENT_NAME
                        Engagement name
  --test-name TEST_NAME
                        Test name
  --test-type-name TEST_TYPE_NAME
                        Test type name
  --static-tool         Is static tool?
  --dynamic-tool        Is dynamic tool?
  --tool-configuration-name TOOL_CONFIGURATION_NAME
                        Tool configuration name
  --tool-configuration-params TOOL_CONFIGURATION_PARAMS
                        Additional tool configuration parameters as comma-separated values. Max of 3 parameters.

Scan Settings:
  --minimum-severity {Info,Low,Medium,High,Critical}
                        Minimum severity level
  --push-to-jira        Push to Jira?
  --close-old-findings  Close old findings?
  --reimport            Reimport findings instead of creating a new test
  --reimport-condition {default,branch,commit,build,pull_request}
                        Condition for reimporting findings

Build/CI Information:
  --build-id BUILD_ID   Build ID
  --commit-hash COMMIT_HASH
                        Commit hash
  --branch-tag BRANCH_TAG
                        Branch or tag
  --scm-uri SCM_URI     SCM URI

General Options:
  -v, --verbose         Enable verbose/debug logging.
  -i, --insecure        Disable ssl verification.

Sub-commands:
  
    integration         Import findings from supported external integrations
```

### Import findings from a file
```bash
defectdojo-importer --api-url <defectdojo url> --api-key <apikey> --product-name myapp --product-type-name webapps --test-type-name "ESLint Scan" -f eslint-report.json
```

### Import findings from existing tool configuration
```bash
defectdojo-importer --api-url <defectdojo url> --api-key <apikey> --product-name myapp --product-type-name webapps --test-type-name "SonarQube API Import" --tool-configuration-name "<Sonarqube tool config name>" --tool-configuration-params "Sonar_Project-key,Sonar-org"
```

### Import lines of code report

See: https://defectdojo.github.io/django-DefectDojo/integrations/languages/

```bash
defectdojo-importer --api-url <defectdojo url> --api-key <apikey> --product-name myapp --product-type-name webapps -t languages -f cloc.json import-languages
```

All supported test types can be found here: https://github.com/DefectDojo/django-DefectDojo/tree/master/dojo/tools


## Integrations

Defectdojo importer also supports integrating with external tools to push findings into defectdojo. The only available integration at the moment is [OWASP Dependency Track](https://docs.dependencytrack.org/integrations/defectdojo/)

```bash
defectdojo-importer integration dtrack --api-url <defectdojo url> --api-key <apikey> --product-name myapp --product-type-name webapps --dtrack-api-url <dependency-track url> --dtrack-api-key <dependency-track apikey>
```

See `defectdojo-importer integration dtrack --help` for additional options. 
If you would like to support a tool you are using, please open an issue.


## Pipeline Usage

Defectdojo-importer tries to detect the following attributes when running in a CI environment:
  - branch or tag name
  - commit hash
  - pull request id
  - pipeline job/build id
  - repository url

See: [src/common/utils.py](./src/common/utils.py#L44)

### Environment variables

You can configure the importer using environment variables and dotenv files (.env, .env.defectdojo). 
The variable pattern is as follows: `DD_<cli argument with underscores>`. For example `DD_API_URL`, `DD_API_KEY`. 
For Debug mode, use `DD_DEBUG` or the `-v/--verbose` cli argument.

### Gitlab CI Usage

Set the following parameters as protected variables.
```
DD_API_URL
DD_API_KEY
```

Example usage with Gitlab SAST report
```yaml
include:
  - template: Security/SAST.gitlab-ci.yml

# some variables that can be generic
variables:
    DD_CLOSE_OLD_FINDINGS: "True"
    DD_BUILD_ID: $CI_PIPELINE_ID
    DD_COMMIT_HASH: $CI_COMMIT_SHA
    DD_BRANCH_TAG: $CI_COMMIT_REF_NAME

stages:
    - test
    - upload

semgrep-sast:
  stage: test
  script:
    - /analyzer run
  rules:
    - if: $SAST_DISABLED
      when: never
    - if: $SAST_EXCLUDED_ANALYZERS =~ /semgrep/
      when: never
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event" || $CI_COMMIT_REF_NAME == $CI_DEFAULT_BRANCH'
      exists:
        - '**/*.py'
        - '**/*.js'
        - '**/*.jsx'
        - '**/*.ts'
        - '**/*.tsx'
        - '**/*.c'
        - '**/*.go'

upload_semgrep:
  stage: upload
  image: zunni/defectdojo-importer:0.0.1-dev
  needs:
    - job: semgrep-sast
      artifacts: true  
  variables:
    GIT_STRATEGY: none
    DD_PRODUCT_TYPE_NAME: $CI_PROJECT_ROOT_NAMESPACE
    DD_PRODUCT_NAME: $CI_PROJECT_NAME 
    DD_TEST_NAME: "Semgrep Scan"
    DD_TEST_TYPE_NAME: "GitLab SAST Report"
    DD_ENGAGEMENT_NAME: "SAST Engagement"
    DD_PUSH_TO_JIRA: "False"
    DD_STATIC_TOOL: "True"
    DD_DYNAMIC_TOOL: "False"
    DD_MINIMUM_SEVERITY: "Info"
    DD_CLOSE_OLD_FINDINGS: "True"
    DD_REIMPORT: "True"
    DD_REIMPORT_CONDITION: "branch"

  script:
    - defectdojo-importer -f gl-sast-report.json -t findings

```

## Authors and acknowledgment
- Azunna Ikonne <ikonnea@gmail.com>

## Contributing

Open a pull request.

### Development Guide

#### Prerequisites

1. Install poetry

```bash
pip install poetry
```

2. Setup a python virtual environment using poetry

```bash
poetry config virtualenvs.in-project true
poetry install
```

#### Step 1: Setup Githooks

```bash
poetry add --dev autohooks autohooks-plugin-black autohooks-plugin-pylint autohooks.plugins.pytest
poetry run autohooks activate --mode poetry
poetry run autohooks plugins add autohooks.plugins.black autohooks.plugins.pylint autohooks.plugins.pytest
```

#### Step 2: Checkout to a Gitflow Branch

```bash
git checkout -b ^(feature|bugfix|hotfix|chore|support|release).*
```

#### Step 3: Commit Messages

Commit your changes using conventional commits syntax
```bash
git add .
git commit  -s -a -m "(feat:|fix:|build:|chore:|ci:|docs:|style:|refactor:|perf:|test:) <message>"
git push
```

#### Step 4: Test the cli locally

Test your changes locally
```bash
poetry install
poetry run defectdojo-importer <commands>
```

#### Step 5: Open a Merge Request

Open a merge request targeting the main branch.
