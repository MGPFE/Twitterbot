from requests_html import HTMLSession
from .image_scraper import *
from PIL import Image, UnidentifiedImageError
import multiprocessing
import secrets
from io import BytesIO


class ImageScraper(Image_Scraper):

    @staticmethod
    def get_im_bytes(image):
        image = Image.open(image)
        im_bytes = BytesIO()
        image.save(im_bytes, "JPEG")
        im_bytes = int(im_bytes.tell())
        image.close()
        return im_bytes

    @staticmethod
    def optimizer(img, im_bytes):
        im = Image.open(img)
        width, height = im.size
        im = im.resize((width // 3, height // 3), Image.ANTIALIAS)
        while im_bytes > 5000000:
            im_bytes = ImageScraper.get_im_bytes(img)
            im.save(img, "JPEG", optimize=True, quality=60)

    def scrape(self, query):
        # RETRIEVE THE PAGE AND RENDER IT
        # render() is used so that potential javascript loads up
        session = HTMLSession()
        r = session.get(f"https://unsplash.com/s/photos/{query}")
        r.html.render()

        data = r.html.absolute_links

        if data:
            self.create_folder()

            threads = list()

            for link in data:
                if "@" in link:
                    continue
                else:
                    # CHECKS FOR UNIQUE FILENAME
                    while True:
                        file_name = secrets.token_hex(32)
                        if file_name not in os.listdir():
                            break
                    thr = threading.Thread(
                        target=self.download_image,
                        args=(link, file_name,)
                    )
                    threads.append(thr)
                    thr.start()

            for thread in threads:
                thread.join()

            files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f))]

            # CHECK IF FILE IS BROKEN
            # IF IT IS THEN DELETE
            for file in files:
                try:
                    im = Image.open(file)
                    im.verify()
                    im.close()
                    im = Image.open(file)
                    im.load()
                    im.transpose(Image.FLIP_LEFT_RIGHT)
                    im.close()
                # except UnidentifiedImageError as e:
                #     os.remove(file)
                except Exception:
                    os.remove(file)

            files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f))]
            processes = []

            print("\nTrying to compress images...")

            for file in files:
                file_bytes = self.get_im_bytes(file)
                if file_bytes > 5000000:
                    process = multiprocessing.Process(target=ImageScraper.optimizer, args=(file, file_bytes,))
                    process.start()
                    processes.append(process)

            for p in processes:
                p.join()
        else:
            print(f"{Fore.YELLOW}Couldn't find any images!{Style.RESET_ALL}")

        num_imgs = len(os.listdir())
        os.chdir("..")

        return num_imgs
