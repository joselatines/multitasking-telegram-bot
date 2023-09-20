import instaloader
import time


def extract_post_id(port_url: str):
    return port_url.split("p/")[1].strip("/")


def download_instagram_image(post_url, save_path="./public/images") -> str:
    print("downloading image")
    L = instaloader.Instaloader()
    post_id = extract_post_id(post_url)
    post = instaloader.Post.from_shortcode(L.context, post_id)

    # naming file
    now_timestamp = time.time()
    filename = str(now_timestamp)
    full_path = f"{save_path}/{filename}"

    photo_url = post.url  # This will be the post's thumbnail (or first slide)

    try:
        L.download_pic(url=photo_url, mtime=now_timestamp, filename=full_path)

    except Exception as e:
        print(e)

    return full_path


def download_instagram_video(post_id: str, save_path="./public/videos/"):
    print("downloading video")
    L = instaloader.Instaloader()
    post_id = extract_post_id(post_id)
    post = instaloader.Post.from_shortcode(L.context, post_id)

    # naming file
    now_timestamp = time.time()
    filename = str(now_timestamp)
    full_path = f"{save_path}/{filename}"

    video_url = post.video_url

    try:
        L.download_pic(filename=full_path, url=video_url, mtime=post.date_utc)

    except Exception as e:
        print(e)

    return full_path
