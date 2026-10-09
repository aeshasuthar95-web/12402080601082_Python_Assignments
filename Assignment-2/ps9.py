class Product:
    def __init__(self, pid, name, stock, purchase, selling):
        self.pid = pid
        self.name = name
        self.stock = stock
        self.purchase = purchase
        self.selling = selling

    def value(self):
        return self.stock * self.selling


class Inventory:
    def __init__(self):
        self.products = {}

    def add(self, product):
        self.products[product.pid] = product

    def delete(self, pid):
        self.products.pop(pid, None)

    def update(self, pid, stock):
        if pid in self.products:
            self.products[pid].stock = stock

    def total_value(self):
        return sum(p.value() for p in self.products.values())

    def __add__(self, other):
        result = Inventory()

        for p in self.products.values():
            result.add(
                Product(
                    p.pid, p.name, p.stock,
                    p.purchase, p.selling
                )
            )

        for p in other.products.values():
            if p.pid in result.products:
                q = result.products[p.pid]
                q.stock += p.stock
                q.purchase = min(q.purchase, p.purchase)
                q.selling = max(q.selling, p.selling)
            else:
                result.add(
                    Product(
                        p.pid, p.name, p.stock,
                        p.purchase, p.selling
                    )
                )

        return result

    def __gt__(self, other):
        return self.total_value() > other.total_value()

    def display(self):
        for p in sorted(self.products.values(), key=lambda x: x.pid):
            print(
                f"{p.pid} {p.name} stock={p.stock} "
                f"purchase={p.purchase} selling={p.selling}"
            )


def main():
    a = Inventory()
    b = Inventory()

    n = int(input("Products in A: "))

    for _ in range(n):
        pid, name, stock, purchase, selling = input().split()
        a.add(Product(
            pid, name, int(stock),
            float(purchase), float(selling)
        ))

    n = int(input("Products in B: "))

    for _ in range(n):
        pid, name, stock, purchase, selling = input().split()
        b.add(Product(
            pid, name, int(stock),
            float(purchase), float(selling)
        ))

    while True:
        command = input("Operation: ").strip().split()

        if not command:
            continue

        if command[0] == "ADD":
            target = a if command[1] == "A" else b
            target.add(
                Product(
                    command[2], command[3],
                    int(command[4]),
                    float(command[5]),
                    float(command[6])
                )
            )

        elif command[0] == "DELETE":
            target = a if command[1] == "A" else b
            target.delete(command[2])

        elif command[0] == "UPDATE":
            target = a if command[1] == "A" else b
            target.update(command[2], int(command[3]))

        elif command[0] == "MERGE":
            merged = a + b
            merged.display()
            print("TOTAL", merged.total_value())

        elif command[0] == "COMPARE":
            if a.total_value() > b.total_value():
                print("A")
            elif b.total_value() > a.total_value():
                print("B")
            else:
                print("EQUAL")

        elif command[0] == "EXIT":
            break


if __name__ == "__main__":
    main()