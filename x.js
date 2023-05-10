const functionn = async() => {
    try{
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

        const response = await octokit.pulls.update(`PATCH /repos/henriquepbalsimelli/auth_poc_back_end/pulls/${prNumber}`, {
            owner: 'henriquepbalsimelli',
            repo: 'auth_poc_back_end',
            pull_number:  prNumber ,
            title: 'new title',
            body: 'BODY TESTE',
            state: 'open',
            base: 'master',
            headers: {
                'X-GitHub-Api-Version': '2022-11-28'
            }
        })

        console.log(response)
    }catch(error){
        console.log(error)
    }

    
} 

functionn()