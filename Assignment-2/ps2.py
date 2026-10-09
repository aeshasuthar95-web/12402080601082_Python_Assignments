import re
import os

def read_products(filename):
    with open(filename, encoding="utf-8") as f:
        html = f.read()

    pattern = re.compile(
        r'<h2[^>]*>(.*?)</h2>.*?'
        r'class=["\'][^"\']*price[^"\']*["\'][^>]*>(.*?)</[^>]+>.*?'
        r'class=["\'][^"\']*rating[^"\']*["\'][^>]*>(.*?)</[^>]+>',
        re.I | re.S
    )

    products = []
    for name, price, rating in pattern.findall(html):
        name = re.sub(r"<[^>]+>", "", name).strip()
        price = float(re.sub(r"[^\d.]", "", price))
        rating = float(re.sub(r"[^\d.]", "", rating))
        products.append((name, price, rating))

    return products

def main():
    try:
        p, k = map(int, input().split())
        products = {}

        for _ in range(p):
            filename = input().strip()
            if not os.path.isfile(filename):
                print("File not found:", filename)
                return

            for name, price, rating in read_products(filename):
                if name not in products or (rating, -price) > (
                    products[name][1], -products[name][0]
                ):
                    products[name] = (price, rating)

        result = sorted(
            products.items(),
            key=lambda x: (-x[1][1], x[1][0], x[0])
        )[:k]

        for name, (price, rating) in result:
            price = int(price) if price.is_integer() else price
            print(name, price, rating)

    except ValueError:
        print("Invalid input.")

if __name__ == "__main__":
    main()