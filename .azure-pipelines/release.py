#!/usr/bin/env python3

import github
import glob
import os
import shutil
import sys

GITHUB_AUTH_TOKEN = os.environ["GITHUB_AUTH_TOKEN"]
AM_BUILD_NUMBER = os.environ["AM_BUILD_NUMBER"]
GIT_HASH = os.environ["GIT_HASH"]


def create_release_tag(repo):
    tag_name = f"refs/tags/nightly-{AM_BUILD_NUMBER}"
    author = github.InputGitAuthor(
        "angr-release-bot", "angr@lists.cs.ucsb.edu")
    repo.create_git_ref(tag_name, GIT_HASH)
    return repo.create_git_tag(tag_name, tag_name, GIT_HASH, "commit", tagger=author)


def create_release(repo, tag):
    message = f"This is an automated release based on commit {GIT_HASH}. It has not recieved any testing or validation, but may be useful to users looking to test the latest and greatest features of angr-management."
    repo.create_git_release(tag.tag, tag.tag, message, prerelease=True)


def publish_release_artifacts(release):
    for artifact in glob.glob("dist/*"):
        # Need to zip up macOS .apps
        if os.path.isdir(artifact):
            out_name = f"{artifact}.zip"
            shutil.make_archive(out_name, "zip", artifact)
            artifact = out_name
        release.upload_asset(artifact)


def main():
    g = github.Github(GITHUB_AUTH_TOKEN)
    repo = g.get_repo("angr/angr-management")
    tag = create_release_tag(repo)
    release = create_release(repo, tag)
    publish_release_artifacts(release)


if __name__ == "__main__":
    main()
