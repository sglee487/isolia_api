import random
import requests

from services.s3 import S3Service

s3 = S3Service()


def generate_random_name() -> str:
    adj_list = []
    with open("utils/korean_adj.txt", "r", encoding="UTF8") as f:
        lines = f.readlines()
        for line in lines:
            adj_list.append(line.strip())

    noun_list = []
    with open("utils/korean_noun.txt", "r", encoding="UTF8") as f:
        lines = f.readlines()
        for line in lines:
            noun_list.append(line.strip())

    return f"{random.choice(adj_list)} {random.choice(noun_list)} {random.randrange(1,100)}"


def generate_profile_urls(picture_url=None) -> list[str]:
    profile_urls = []
    for i in range(1, 6):
        profile_urls.append(f"https://s3.ap-northeast-2.amazonaws.com/woowa-s3/woowa_{i}.png")
    return profile_urls