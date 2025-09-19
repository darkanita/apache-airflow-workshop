from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id="lab03_taskflow_xcom",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["lab03", "taskflow", "xcom"],
)
def pipeline():
    @task
    def generate_numbers(n: int = 5):
        return list(range(1, n + 1))

    @task
    def square(nums: list[int]):
        return [x * x for x in nums]

    @task
    def summarize(nums: list[int], squares: list[int]) -> str:
        total = sum(nums)
        total_sq = sum(squares)
        msg = f"sum={total}, sum_of_squares={total_sq}"
        print(msg)
        return msg

    nums = generate_numbers(10)
    squares = square(nums)
    summarize(nums, squares)

pipeline = pipeline()
