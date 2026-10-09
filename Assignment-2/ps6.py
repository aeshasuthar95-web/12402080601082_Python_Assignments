import re
from collections import defaultdict, deque

def to_minutes(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m

def main():
    try:
        X, T = map(int, input().split())
        n = int(input())

        failures = defaultdict(deque)
        suspicious = {}

        pattern = re.compile(
            r"^(\d{2}:\d{2})\s+(\S+)\s+(\S+)\s+(FAIL|SUCCESS)$"
        )

        for _ in range(n):
            line = input().strip()
            match = pattern.match(line)

            if not match:
                continue

            timestamp, user, ip, status = match.groups()
            current = to_minutes(timestamp)

            if status == "FAIL":
                q = failures[user]

                while q and current - q[0][0] > T:
                    q.popleft()

                q.append((current, ip))

            else:
                q = failures[user]

                while q and current - q[0][0] > T:
                    q.popleft()

                if len(q) >= X and any(old_ip != ip for _, old_ip in q):
                    suspicious.setdefault(user, timestamp)

        for user in sorted(suspicious):
            print(user, suspicious[user])

    except ValueError:
        print("Invalid input.")

if __name__ == "__main__":
    main()