from docorator import Docorator


def main():
    urls = ["https://en.wikipedia.org/wiki/The_Hobbit", "https://www.gradesaver.com/the-hobbit/study-guide/character-list", "https://theliteraryomnivore.wordpress.com/2010/01/31/review-the-hobbit/"]
    docos = []
    for url in urls:
        doco = Docorator(keyfile_path="service-account-key.json", email="arved.kloehn@gmail.com", document_name=url)
        doco.load()
        docos.append(doco)
    for doco in docos:
        doco.wait_for_load()
    #doco.wait_for_load()
    #print(doco.as_markdown())
    #print(doco.document_id)
    #doco.save("# This is a headline\n\n## Part 1\n\nHello World\\!\n\nLaLaLe\nLULULU\n\n![Der designierte kanadische Regierungschef Mark Carney ](https://images.tagesschau.de/image/306b44c7-f4ea-4b7b-97dd-75a0bbe86375/AAABlZIlgWQ/AAABkZLk4K0/16x9-768/carney-108.jpg)")


if __name__ == "__main__":
    main()