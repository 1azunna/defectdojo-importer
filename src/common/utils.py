import os
from pathlib import Path


def get_files(filename: str | None = None, payload: bytes | None = None):
    """Return a list of file tuples for HTTP file upload."""
    if filename is None:
        return [
            (
                "file",
                (
                    None,
                    None,
                    "application/octet-stream",
                ),
            )
        ]
    with open(Path(filename).expanduser().absolute(), "rb") as file:
        contents = file.read()
        if payload is not None:
            contents = payload
        files = [
            (
                "file",
                (
                    os.path.basename(filename),
                    contents,
                    "application/octet-stream",
                ),
            )
        ]
    return files


def get_service_keys(service_keys_csv: str, position: int = 0):
    """Return the service key at the given position from a CSV string."""
    service_keys = service_keys_csv.split(",", maxsplit=2)
    if len(service_keys) >= 1 + position:
        service_key = service_keys[position]
    else:
        service_key = None

    return service_key


def get_pull_request_id():
    """Get pull request ID from environment variables."""
    pr_env_vars = [
        "PULL_REQUEST_ID",
        "PR_ID",
        "_PR_NUMBER",
        "CI_MERGE_REQUEST_IID",
        "BITBUCKET_PR_ID",
    ]
    for var in pr_env_vars:
        pr_id = os.getenv(var)
        if pr_id:
            return pr_id
    return None


def get_build_id():
    """Get build ID from environment variables."""
    build_env_vars = [
        "BUILD_ID",
        "BUILD_NUMBER",
        "CI_JOB_ID",
        "GITHUB_RUN_ID",
        "CODEBUILD_BUILD_NUMBER",
        "BITBUCKET_BUILD_NUMBER",
    ]
    for var in build_env_vars:
        build_id = os.getenv(var)
        if build_id:
            return build_id
    return None


def get_commit_hash():
    """Get commit hash from environment variables."""
    commit_env_vars = [
        "COMMIT_HASH",
        "COMMIT_SHA",
        "GIT_COMMIT",
        "CI_COMMIT_SHA",
        "GITHUB_SHA",
        "CODEBUILD_RESOLVED_SOURCE_VERSION",
        "BITBUCKET_COMMIT",
    ]
    for var in commit_env_vars:
        commit_hash = os.getenv(var)
        if commit_hash:
            return commit_hash
    return None


def get_branch_tag():
    """Get branch or tag name from environment variables."""
    branch_env_vars = [
        "BRANCH_NAME",
        "TAG_NAME",
        "GIT_BRANCH",
        "CI_COMMIT_REF_SLUG",
        "CODEBUILD_WEBHOOK_HEAD_REF",
        "GITHUB_REF_NAME",
        "BITBUCKET_BRANCH",
    ]
    for var in branch_env_vars:
        branch_tag = os.getenv(var)
        if branch_tag:
            return branch_tag
    return None


def get_scm_uri():
    """Get SCM URI from environment variables."""
    scm_env_vars = [
        "REPO_URL",
        "GIT_URL",
        "CI_PROJECT_URL",
        "CODEBUILD_SOURCE_REPO_URL",
        "BITBUCKET_GIT_HTTP_ORIGIN",
    ]
    for var in scm_env_vars:
        scm_uri = os.getenv(var)
        if scm_uri:
            return scm_uri
    return None
