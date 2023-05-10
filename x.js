let comment = '';
if (coveragePercentage >= 80) {
    comment = `:white_check_mark: Code coverage: ${coveragePercentage}% - All tests passed!`;
} else {
    comment = `:x: Code coverage: ${coveragePercentage}% - Please improve test coverage.`;
}

await octokit.request('PATCH /repos/henriquepbalsimelli/auth_poc_back_end/pulls/{pull_number}', {
    owner: 'henriquepbalsimelli',
    repo: 'auth_poc_back_end',
    pull_number: { prNumber },
    title: { comment },
    body: { comment },
    state: 'open',
    base: 'master',
    headers: {
        'X-GitHub-Api-Version': '2022-11-28'
    }
})