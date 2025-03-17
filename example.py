from docorator import Docorator

def main():
    doco = Docorator(keyfile_path="service-account-key.json", email="arved.kloehn@gmail.com", document_name="Tagesschau___https-www-tagesschau-de")
    doco.wait_for_load()
    print(doco.as_markdown())
    #print(doco.document_id)
    #doco.save("# This is a headline\n\n## Part 1\n\nHello World\\!\n\nLaLaLe\nLULULU\n\n![Der designierte kanadische Regierungschef Mark Carney ](https://images.tagesschau.de/image/306b44c7-f4ea-4b7b-97dd-75a0bbe86375/AAABlZIlgWQ/AAABkZLk4K0/16x9-768/carney-108.jpg)")


if __name__ == "__main__":
    main()