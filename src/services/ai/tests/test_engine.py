from src.services.ai.engine import IssueSolver
from src.services.ai.tests.dummy_data import test_file_list, test_issue

def test_issue_solver():
    issue_solver = IssueSolver()
    response = issue_solver.solve_issues(test_issue, test_file_list)

    assert response is not None

    print(response)

if __name__ == '__main__':
    test_issue_solver()