import asyncio

import argparse


from core.register import main
from core.utils.file import load_proxies


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Autoreg duck.com emails")
    parser.add_argument("--domain", type=str, help="Input domain of your mail system", required=False)
    parser.add_argument("--num_accounts", type=int, help="Specify the number of accounts to be created", required=False)
    parser.add_argument("--max_connections", type=int, help="Enter the maximum number of concurrent connections", required=False)
    parser.add_argument("--proxy_path", type=str, help="Enter the path to the proxy file", required=False)


    args = parser.parse_args()

    if args.domain is None:
        args.domain = input("Input domain your mail system: ")
    if args.num_accounts is None:
        args.num_accounts = int(input("Specify the number of accounts to be created: "))
    if args.max_connections is None:
        args.max_connections = int(input("Enter the maximum number of concurrent connections: "))
    if args.proxy_path is None:
        args.proxy_path = input("Enter the path to the proxy file: ")

    print(f"\nExample CLI Command: python {__file__} --domain {args.domain} --num_accounts {args.num_accounts} --max_connections {args.max_connections} --proxy_path {args.proxy_path}")

    asyncio.run(main(args.domain, args.num_accounts, args.max_connections, load_proxies(args.proxy_path)))
