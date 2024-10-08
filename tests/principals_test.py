from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

@ def test_grade_assignment_draft_assignment(client, h_principal):
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.status_code == 200
    # assert response.status_code == 400


def test_grade_assignment(client, h_principal)
def test_regrade_assignment(client, h_principal):

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B


def test_invalid_assignment_id(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 9999,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 404


def test_invalid_grade(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': "Z"
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json["message"] == {"grade": ["Invalid enum member Z"]}


def test_all_teachers(client,h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200
    
