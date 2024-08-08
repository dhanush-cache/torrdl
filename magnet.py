import random
from typing import Generator

from py1337x import py1337x

searcher = py1337x()


class TorrentNotFoundError(Exception):
    pass


def to_bytes(size: str) -> float:
    units = {
        "KB": 1024,
        "MB": 1024 * 1024,
        "GB": 1024 * 1024 * 1024,
        "TB": 1024 * 1024 * 1024 * 1024,
    }
    size = size.strip().upper()
    for unit in units:
        if unit in size:
            size_value = size.split(unit)[0].strip()
            return float(size_value) * units[unit]

    raise ValueError(f"Invalid input: {size}")


def get_page_count(target):
    return searcher.search(target, sortBy="seeders")["pageCount"]


def search(
    target: str, pages: int = 1, min_seeders: int = 0, max_size: str = "6.5 GB"
) -> Generator:

    max_pages = get_page_count(target)
    page_nos = range(1, min(pages, max_pages) + 1)
    keys = ["name", "torrentId", "seeders", "leechers", "size"]

    return (
        {key: value for key, value in result.items() if key in keys}
        for page_no in page_nos
        for result in searcher.search(target, sortBy="seeders", page=page_no)["items"]
        if int(result["seeders"]) >= min_seeders
        and to_bytes(result["size"]) <= to_bytes(max_size)
    )


def get_url(torrent_id: int):
    torrent_info = searcher.info(torrentId=torrent_id)
    return torrent_info["magnetLink"]


def find_best_match(target: str) -> str:
    match = next(search(target))
    if not match:
        raise TorrentNotFoundError("No results!!!")
    torrent_id = match["torrentId"]
    return get_url(torrent_id)


def find_random_match(
    target: str, pages: int = 1, min_seeders: int = 0, max_size: str = "4.0 GB"
) -> str:
    torrents = list(search(target, pages, min_seeders, max_size))
    if not torrents:
        raise TorrentNotFoundError("No results!!!")
    choice = random.choice(torrents)
    return get_url(choice)


if __name__ == "__main__":
    ...
