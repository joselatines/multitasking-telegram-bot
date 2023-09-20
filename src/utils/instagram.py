import instaloader
import time



def extract_post_id(port_url: str):
    return port_url.split("p/")[1].strip("/")


def download_instagram_image(post_url, save_path="") -> str:
    now_timestamp = time.time()
    print("downloading")
    L = instaloader.Instaloader()
    post_id = extract_post_id(post_url)
    post = instaloader.Post.from_shortcode(L.context, post_id)
    filename = str(now_timestamp)
    fully_path = f"{filename}"
    photo_url = post.url  # This will be the post's thumbnail (or first slide)

    try:
        L.download_pic(url=photo_url, mtime=now_timestamp, filename=fully_path)

    except Exception as e:
        print(e)

    return fully_path

def download_instagram_video(url:str):
    L = instaloader.Instaloader()
    # Replace 'https://www.instagram.com/p/-vSJNUDKKD/' with the actual URL of the Instagram post
    url = 'https://www.instagram.com/p/-vSJNUDKKD/'

    # Download the video
    L.download_video(url)
