import datetime
import json
import os
from pathlib import Path
import re
from dotenv import load_dotenv
import git
from giturlparse import parse
import sys
from github import Github

from supervisely.cli.release import (
    release,
)

GITHUB_ACCESS_TOKEN = os.getenv("GH_ACCESS_TOKEN", None)


def clone_repo(repo_url):
    repo_dir = os.path.join(os.getcwd(), "repo")
    if os.path.exists(repo_dir):
        return git.Repo(repo_dir)
    else:
        return git.Repo.clone_from(repo_url, repo_dir)


def parse_app_url(app_url: str):
    app_url = app_url.removeprefix("https://").removeprefix("http://")
    parts = app_url.split("/")
    repo_url = "/".join(parts[:3])
    subapp_path = "/".join(parts[3:])
    return repo_url, subapp_path if subapp_path else None


# from cli.release.get_appKey
def get_appKey(repo_url, subapp_path, repo):
    import hashlib

    # from cli.release.get_remote_url
    p = parse(repo_url)
    repo_url = p.url2https.replace("https://", "").replace(".git", "").lower()
    #

    first_commit = next(repo.iter_commits("HEAD", reverse=True))
    key_string = repo_url + "_" + first_commit.hexsha
    appKey = hashlib.md5(key_string.encode("utf-8")).hexdigest()
    if subapp_path is not None:
        appKey += "_" + hashlib.md5(subapp_path.encode("utf-8")).hexdigest()
    appKey += "_" + hashlib.md5(first_commit.hexsha[:7].encode("utf-8")).hexdigest()

    return appKey


def get_slug(repo_url, subapp_path):
    p = parse(repo_url)
    repo_url = p.url2https.replace("https://", "").replace(".git", "").lower()
    slug = "/".join(repo_url.split("/")[1:])
    if subapp_path is not None:
        slug += "/" + subapp_path
    return slug


def join_path_with_subapp(path, subapp_path, *paths):
    if subapp_path is not None:
        path = os.path.join(path, subapp_path)
    return os.path.join(path, *paths)


def get_config(repo: git.Repo, subapp_path):
    config_path = join_path_with_subapp(repo.working_dir, subapp_path, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
    else:
        raise FileNotFoundError(f"Config file not found: {config_path}")
    return config


def get_readme(repo: git.Repo, subapp_path):
    readme_path = join_path_with_subapp(repo.working_dir, subapp_path, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme = f.read()
    else:
        raise FileNotFoundError(f"Readme file not found: {readme_path}")
    return readme


def get_modal_template(repo: git.Repo, subapp_path, config):
    if "modal_template" not in config:
        return ""
    modal_template_path = join_path_with_subapp(
        repo.working_dir, subapp_path, config["modal_template"]
    )
    if os.path.exists(modal_template_path):
        with open(modal_template_path, "r") as f:
            modal_template = f.read()
    else:
        raise FileNotFoundError(f"Modal template file not found: {modal_template_path}")
    return modal_template


def is_release_tag(tag_name):
    return re.match("v\d+\.\d+\.\d+", tag_name) != None


def sorted_releases(releases):
    key = lambda release: [int(x) for x in release.tag_name[1:].split(".")]
    return sorted(releases, key=key)


def get_created_at(repo: git.Repo, tag_name):
    print()
    print("Searching for release timestamp. Tag name", tag_name)
    print()
    if tag_name is None:
        return None
    for tag in repo.tags:
        print(tag.name)
        if tag.name == tag_name:
            print("found")
            if tag.tag is None:
                print("Tag is lightweight. Taking commit date")
                timestamp = tag.commit.committed_date
            else:
                timestamp = tag.tag.tagged_date
            print(
                "timestamp: ",
                datetime.datetime.utcfromtimestamp(timestamp).isoformat(),
                "\n",
            )
            return datetime.datetime.utcfromtimestamp(timestamp).isoformat()
        print("skip")
    return None


def get_release_name(tag):
    if tag.tag is None:
        return tag.name
    else:
        return tag.tag.message


def run_release(
    release_name,
    release_version,
    repo,
    repo_url,
    subapp_path,
    server_address,
    api_token,
    slug,
):
    print("Release_version: ", release_version)
    print("Release_name: ", release_name)
    config = get_config(repo, subapp_path)
    print(
        "Config: ",
        join_path_with_subapp(repo.working_dir, subapp_path, "config.json"),
    )
    readme = get_readme(repo, subapp_path)
    print(
        "Readme: ",
        join_path_with_subapp(repo.working_dir, subapp_path, "README.md"),
    )
    modal_template = get_modal_template(repo, subapp_path, config)
    print(
        "Modal template: ",
        join_path_with_subapp(repo.working_dir, subapp_path, config["modal_template"])
        if modal_template
        else None,
    )
    appKey = get_appKey(repo_url, subapp_path, repo)

    created_at = get_created_at(repo, f"sly-release-{release_version}")

    "Releasing version..."
    response = release(
        server_address=server_address,
        api_token=api_token,
        appKey=appKey,
        repo=repo,
        config=config,
        readme=readme,
        release_name=release_name,
        release_version=release_version,
        modal_template=modal_template,
        slug=slug,
        created_at=created_at,
    )
    print(response.json())
    if response.status_code == 200:
        print(f"Sucessfully released {release_version} ({release_name})\n")


def run(repo, slug, subapps):
    api_token = os.getenv("API_TOKEN", None)
    server_address = os.getenv("SERVER_ADDRESS", None)

    print("DEBUG: server_address:", server_address)
    print("DEBUG: api_token:", f"{api_token[:4]}****{api_token[-4:]}")
    print()

    GH = Github(GITHUB_ACCESS_TOKEN)
    gh_repo = GH.get_repo(slug)
    repo_url = f"https://github.com/{slug}"
    if gh_repo.get_releases().totalCount > 1:
        print("Not the first release, skipping sly-releases")
        return

    for subapp in subapps:
        if subapp is None:
            print("Releasing main app\n")
        else:
            print('Releasing subapp at: "', subapp, '"\n')
        if (
            not Path(next(repo.commit().tree.traverse()).abspath)
            .parent.joinpath("config.json")
            .exists
        ):
            print("config.json not found, skipping sly-releases")
            return

        key = lambda tag: [int(x) for x in tag.name[13:].split(".")]
        sorted_tags = sorted(
            [tag for tag in repo.tags if tag.name.startswith("sly-release-v")], key=key
        )

        for tag in sorted_tags:
            repo.git.checkout(tag)
            release_name = get_release_name(tag)
            run_release(
                release_name=release_name,
                release_version=tag.name[12:],
                repo=repo,
                repo_url=repo_url,
                subapp_path=None,
                api_token=api_token,
                server_address=server_address,
                slug=slug,
            )


if __name__ == "__main__":
    slug = sys.argv[1]

    # subapps = [p.lstrip(" ").rstrip(" ") for p in os.getenv("SUBAPP_PATHS", "").split(",")]
    # for i, subapp in enumerate(subapps):
    #     if subapp == "__ROOT_APP__":
    #         subapps[i] = None
    # if len(subapps) == 0:
    #     subapps.append(None)
    # print("subapps:", subapps)

    subapps = os.getenv("SUBAPP_PATHS", [])
    for i, subapp in enumerate(subapps):
        if subapp == "__ROOT_APP__":
            subapps[i] = None
    if len(subapps) == 0:
        subapps.append(None)
    print("subapps:", subapps)

    repo = git.Repo()
    run(repo, slug, [None, *subapps])
