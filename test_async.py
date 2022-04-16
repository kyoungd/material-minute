import asyncio


async def main():
    print('1')
    task = asyncio.create_task(foo('foo-me'))
    print('0')


async def foo(text):
    print(text)
    await asyncio.sleep(1)


def run():
    asyncio.run(main())
    print('4')


if __name__ == '__main__':
    run()
