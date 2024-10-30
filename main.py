import asyncio
import argparse
from core.register import main
from core.utils.file import load_proxies

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autoreg duck.com emails")

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--domain_mode", action="store_true", help="Generate emails using domain")
    mode_group.add_argument("--dots_mode", action="store_true", help="Generate emails using dots placement")
    mode_group.add_argument("--tags_mode", action="store_true", help="Generate emails using tags")

    parser.add_argument("--domain", type=str, help="Input domain of your mail system")

    parser.add_argument("--emails_file", type=str, help="Path to file with existing emails")

    parser.add_argument("--num_accounts", type=int, help="Specify the number of accounts to be created")
    parser.add_argument("--max_connections", type=int, help="Enter the maximum number of concurrent connections")
    parser.add_argument("--proxy_path", type=str, help="Enter the path to the proxy file")
    parser.add_argument("--export", type=str, help="Export duck.com email from accounts.csv to a specified file")

    args = parser.parse_args()

    if args.export is None:
        if not any([args.domain_mode, args.dots_mode, args.tags_mode]):
            print("Select generation mode:")
            print("1. Domain mode (generate emails using domain)")
            print("2. Dots mode (generate emails using dots placement)")
            print("3. Tags mode (generate emails using tags)")
            mode = input("Enter mode number (1-3): ")

            if mode == "1":
                args.domain_mode = True
                if args.domain is None:
                    args.domain = input("Input domain your mail system: ")
            elif mode == "2":
                args.dots_mode = True
                if args.emails_file is None:
                    args.emails_file = input("Enter path to file with existing emails: ")
            elif mode == "3":
                args.tags_mode = True
                if args.emails_file is None:
                    args.emails_file = input("Enter path to file with existing emails: ")
            else:
                print("Invalid mode selected")
                exit(1)

        if args.num_accounts is None:
            args.num_accounts = int(input("Specify the number of accounts to be created: "))
        if args.max_connections is None:
            args.max_connections = int(input("Enter the maximum number of concurrent connections: "))
        if args.proxy_path is None:
            args.proxy_path = input("Enter the path to the proxy file: ")

    if args.domain_mode:
        mode_str = f"--domain_mode --domain {args.domain}"
    elif args.dots_mode:
        mode_str = f"--dots_mode --emails_file {args.emails_file}"
    elif args.tags_mode:
        mode_str = f"--tags_mode --emails_file {args.emails_file}"
    else:
        mode_str = ""

    if args.domain_mode:
        print(f"\nExample CLI Command: python {__file__} {mode_str} "
              f"--num_accounts {args.num_accounts} --max_connections {args.max_connections} "
              f"--proxy_path {args.proxy_path}")

    mode_params = {
        "mode": "domain" if args.domain_mode else "dots" if args.dots_mode else "tags",
        "domain": args.domain if args.domain_mode else None,
        "emails_file": args.emails_file if (args.dots_mode or args.tags_mode) else None
    }

    asyncio.run(main(mode_params, args.num_accounts, args.max_connections,
                     load_proxies(args.proxy_path), args.export))
