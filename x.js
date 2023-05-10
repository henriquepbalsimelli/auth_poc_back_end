const { Octokit } = require("@octokit/rest");
const token = ${{ secrets.TOKEN_TEST }}
const octokit = new Octokit({ auth: `{token}` })
const prNumber = context.payload.pull_request.number;
const coveragePercentage = `${{ steps.coverage.outputs.percentage }}`;

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
    title: { coveragePercentage },
    body: { comment },
    state: 'open',
    base: 'master',
    headers: {
        'X-GitHub-Api-Version': '2022-11-28'
    }
})