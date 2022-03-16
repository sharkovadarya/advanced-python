import asyncio
import logging
import sys

import aiofiles
import aiohttp

# added logging bc the previous h/w also asked for it
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.INFO)

log = logging.getLogger("easy")
log.setLevel(logging.INFO)


async def fetch_and_save_image(session, url, results_dir, filename):
    print('hullo')
    async with session.get(url) as response:
        if response.status == 200:
            f = await aiofiles.open(f"{results_dir}/{filename}", mode='wb')
            await f.write(await response.read())
            await f.close()
            logging.info(f"Saved image {filename} from url {url}")
        else:
            logging.error(f"Unable to download file {filename} from {url}")


async def main(n, results_dir):
    async with aiohttp.ClientSession() as session:
        print('hello')
        await asyncio.gather(*[
            fetch_and_save_image(session,
                                 'https://picsum.photos/200/300',
                                 results_dir,
                                 f"file{i + 1}.jpeg") for i in range(n)], return_exceptions=True)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: number of distinct images, path to results directory")
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(int(sys.argv[1]), sys.argv[2]))
