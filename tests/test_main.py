import requests


def test_sum() -> None:
    """ asd """
    assert 2+2 == 4

def test_request() -> None:

    #token = "${{ secrets.TKN_PR }}";
    prNumber = 1080;
    coveragePercentage = 80;
    owner = "${{ github.repository_owner }}"

    #repository = "${{ github.repository }}"

    comment = '';
    if coveragePercentage >= 80:
        comment = f':white_check_mark: Code coverage: {coveragePercentage}% - All tests passed!';
    else: 
        comment = ':x: Code coverage: {coveragePercentage}% - Please improve test coverage.';
    

    body = {
        'owner': owner,
        'repo': 'auth_poc_back_end',
        'title': 'new title',
        'pull_number': prNumber,
        'body': comment,
        'state': 'open',
        'headers': {
            'X-GitHub-Api-Version': '2022-11-28'
        }
    }
    response = requests.patch('https://api.github.com/repos/henriquepbalsimelli/auth_poc_back_end/pulls/1080', json=body ,timeout=30000)

    assert response
