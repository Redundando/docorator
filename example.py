from docorator import Docorator

def main():
    doco = Docorator(keyfile_path="service-account-key.json", email="klojarve@audible.de", document_name="Example Document")
    doco.wait_for_load()
    print(doco.as_markdown())
    doco.save("# This is a headline\n\n## Part 1\n\nHello World\\!\n\nLaLaLe\nLULULU")


if __name__ == "__main__":
    main()