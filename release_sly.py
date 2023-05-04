import os
import sys
import git
from supervisely.cli.release.run import run as run_release
from github import Github

GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN", None)

def run(slug):
    repo = git.Repo()

    GH = Github(GITHUB_ACCESS_TOKEN)
    gh_repo = GH.get_repo(slug)
    if len(gh_repo.get_releases()) > 1:
        print("Not the first release, skipping sly-releases")
        return

    key = lambda tag: [int(x) for x in tag.name[13:].split(".")]
    sorted_tags = sorted(
        [tag for tag in repo.tags if tag.name.startswith("sly-release")], key=key
    )

    for tag in sorted_tags:
        repo.git.checkout(tag)
        run_release(
            os.getcwd(),
            sub_app_directory=None,
            slug=slug,
            autoconfirm=True,
            release_version=tag.name[12:],
            release_description="",
        )


if __name__ == "__main__":
    slug = sys.argv[1]
    run(slug)
