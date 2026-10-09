# ---------------------------------------------------------
# Assignment 1 - Q9
# Threaded Job Scheduler Simulation
# ---------------------------------------------------------

import heapq
import threading
from dataclasses import dataclass


@dataclass
class Job:
    arrival: int
    job_id: str
    priority: int
    duration: int
    resources: int
    order: int


def simulate(jobs, worker_count):
    """
    Simulate workers executing jobs.

    Higher priority = processed first.
    Same priority = earlier arrival first.
    """

    # Sort by arrival time first
    jobs.sort(
        key=lambda job: (
            job.arrival,
            job.order
        )
    )

    # Available jobs.
    # Negative priority makes heap behave as max-priority.
    waiting = []

    # Worker availability times.
    # (finish_time, worker_number)
    workers = [
        (0, i + 1)
        for i in range(worker_count)
    ]

    heapq.heapify(workers)

    results = []

    index = 0
    current_time = 0

    while index < len(jobs) or waiting:

        # -------------------------------------------------
        # Add jobs that have arrived
        # -------------------------------------------------

        if not waiting and index < len(jobs):
            current_time = max(
                current_time,
                jobs[index].arrival
            )

        while (
            index < len(jobs)
            and jobs[index].arrival <= current_time
        ):

            job = jobs[index]

            heapq.heappush(
                waiting,
                (
                    -job.priority,
                    job.arrival,
                    job.order,
                    job
                )
            )

            index += 1

        # -------------------------------------------------
        # Get earliest available worker
        # -------------------------------------------------

        finish_time, worker_id = heapq.heappop(
            workers
        )

        current_time = max(
            current_time,
            finish_time
        )

        # Add newly arrived jobs at current time
        while (
            index < len(jobs)
            and jobs[index].arrival <= current_time
        ):

            job = jobs[index]

            heapq.heappush(
                waiting,
                (
                    -job.priority,
                    job.arrival,
                    job.order,
                    job
                )
            )

            index += 1

        # If no job is waiting, worker remains idle
        if not waiting:

            heapq.heappush(
                workers,
                (current_time, worker_id)
            )

            continue

        # -------------------------------------------------
        # Select highest priority job
        # -------------------------------------------------

        _, _, _, job = heapq.heappop(waiting)

        start_time = max(
            current_time,
            job.arrival,
            finish_time
        )

        finish_time = (
            start_time +
            job.duration
        )

        waiting_time = (
            start_time -
            job.arrival
        )

        results.append(
            (
                job.job_id,
                worker_id,
                start_time,
                finish_time,
                waiting_time
            )
        )

        # Worker becomes available after this job
        heapq.heappush(
            workers,
            (
                finish_time,
                worker_id
            )
        )

        current_time = start_time

    return results


def main():

    # w = workers
    # n = jobs
    w, n = map(int, input().split())

    if not (1 <= w <= 64):
        raise ValueError("Workers must be between 1 and 64.")

    jobs = []

    for order in range(n):

        arrival, job_id, priority, duration, resources = (
            input().split()
        )

        job = Job(
            int(arrival),
            job_id,
            int(priority),
            int(duration),
            int(resources),
            order
        )

        jobs.append(job)

    results = simulate(
        jobs,
        w
    )

    total_wait = sum(
        result[4]
        for result in results
    )

    # -----------------------------------------------------
    # Output execution report
    # -----------------------------------------------------

    for job_id, worker_id, start, finish, wait in results:

        print(
            f"{job_id} W{worker_id} "
            f"{start} {finish}"
        )

    average_wait = (
        total_wait / len(results)
        if results
        else 0
    )

    print(
        f"AVG_WAIT {average_wait:.2f}"
    )


if __name__ == "__main__":
    main()