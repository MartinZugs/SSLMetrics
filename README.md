# SSLMetrics

## How It Works
Using the [GitHub API](https://developer.github.com/v3/) we gather information about a repository, and use [pandas](https://pandas.pydata.org/) to display the information.

## Installation/Setup
### Command Line Metrics
Python script, simple_cli.py, creates .csv file of information for a single repo, using pandas.

1. Config PAT
   * In order for the command to work, you must change your config.py
    
        1. Create a file named config.py  
        Type: `access_token = "YOUR_ACCESS_TOKEN`     
        2. [If you don't already have a token, create a token using these instructions:](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
        3. Change "`YOUR_ACCESS_TOKEN`" to your actual token in config.py
       
2. Run the following commands in your terminal:

`    python3 simple_cli.py www.github.com/username/reponame
`
### Data Visualization
1. Run `npm install` to install NPM dependencies.
   
2. Run `npm run rebuild` to rebuild sqlite3 dependency for use with Electron.

3. Run `npm start sqlite_DB_filename` to start the data-vis app. 

    
   
