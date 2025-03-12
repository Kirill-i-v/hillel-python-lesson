from abc import ABC, abstractmethod
from time import time


class Post:
    def __init__(self, message: str, timestamp: int) -> None:
        self.message = message
        self.timestamp = timestamp


class SocialChannel(ABC):
    def __init__(self, followers: int) -> None:
        self.followers = followers

    @abstractmethod
    def post_message(self, message: str) -> None:
        pass


class YouTubeChannel(SocialChannel):
    def post_message(self, message: str) -> None:
        print(f"Posting to YouTube: {message}")


class FacebookChannel(SocialChannel):
    def post_message(self, message: str) -> None:
        print(f"Posting to Facebook: {message}")


class TwitterChannel(SocialChannel):
    def post_message(self, message: str) -> None:
        print(f"Posting to Twitter: {message}")


def process_schedule(posts: list[Post], channels: list[SocialChannel]) -> None:
    for post in posts:
        if post.timestamp <= time():
            for channel in channels:
                channel.post_message(post.message)


if __name__ == '__main__':
    posts = [Post("Hello World!", int(time()) - 1)]
    channels = [YouTubeChannel(15), FacebookChannel(50), TwitterChannel(80)]
    process_schedule(posts, channels)
