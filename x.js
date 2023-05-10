const functionn = async() => {

    const { Octokit } = require("@octokit/rest");
    const token = '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';
    const octokit = new Octokit({ auth: token });
    const prNumber = 1080;
    const coveragePercentage = 60;
    
    let comment = '';
    if (coveragePercentage >= 80) {
        comment = `:white_check_mark: Code coverage: ${coveragePercentage}% - All tests passed!`;
    } else {
        comment = `:x: Code coverage: ${coveragePercentage}% - Please improve test coverage.`;
    }
    
    const response = await octokit.request(`PATCH /repos/henriquepbalsimelli/auth_poc_back_end/pulls/${prNumber}`, {
        owner: 'henriquepbalsimelli',
        repo: 'auth_poc_back_end',
        pull_number: { prNumber },
        title: 'new title',
        body: { comment },
        state: 'open',
        base: 'master',
        headers: {
            'X-GitHub-Api-Version': '2022-11-28'
        }
    })

    console.log(response)
} 

functionn()