# CodeTime - A time tracking plugin for text editors [G10 Project 2]
[![DOI](https://zenodo.org/badge/295515546.svg)](https://zenodo.org/badge/latestdoi/295515546)
[![Build Status](https://travis-ci.org/oaaky/SE_Fall20_Project-1.svg?branch=master)](https://travis-ci.org/oaaky/SE_Fall20_Project-1)
[![GitHub license](https://img.shields.io/github/license/oaaky/SE_Fall20_Project-1)](https://github.com/oaaky/SE_Fall20_Project-1/blob/master/LICENSE)
![GitHub issues](https://img.shields.io/github/issues/oaaky/SE_Fall20_Project-1)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/oaaky/SE_Fall20_Project-1)


## About CodeTime

- CodeTime is a plugin for Sublime Text editor which will help developers to track the amount of time spent on multiple files, programming languages and projects. The user will be able to perform the analysis of the time spent to improve the productivity by analysing the most frequently used programming language, most productive time of the day, files in project which took maximum time for development and projects which took maximum time for completion.

- The developer can add the project deadlines to the plugin and the plugin can help developers stick to their goal by predicting the finish time of the project based on the data gathered from the user. Multiple developers can compete with each other through a leaderboard where a leaderboard will display the ranking of most productive developer and admin/manager can easily monitor the productivity of each and every developer with the help of a common interface.

[![CodeTime Promo Video](https://img.youtube.com/vi/CL5W7C9Jw_c/0.jpg)](https://www.youtube.com/watch?v=Jq5fh_sGReY&feature=youtu.be)


## Installation

1. Open Sublime Text.
2. Go to Preferences -> Browse packages.
3. A new window containing Sublime packages directory will open up. Let's call this folder `SublimePackagesFolder`.
4. Open your terminal and navigate to `SublimePackagesFolder`.
5. Clone this repository inside `SublimePackagesFolder` (This makes sure that Sublime recognizes our plugin package to execute).
6. Copy the [Context.sublime-menu](code/SublimePlugin/Config/Context.sublime-menu) file to your User Packages directory. To go to User Packages directory, navigate to `SublimePackagesFolder/User` folder.
7. You are all set. The plugin is now active and is running in the background.


## Usage

1. Open Sublime Text.
2. Open a file that you wish to work on.
3. In the file pane, right click and select the option `View CodeTime Dashboard`.


## Setup (For contributors)

> <strong>Note:</strong> Please install and use Sublime Text 3 only for development.

1. Perform the steps in the [Installation](https://github.com/oaaky/SE_Fall20_Project-1#installation-for-non-contributors) section described above.
2. Install Package Control by pressing `ctrl+shift+p (Win/Linux)` or `cmd+shift+p (Mac)`.
3. Run `python setup.py install` to install all the dependencies.
4. Back in Sublime Text, Open Package Control by pressing `ctrl+shift+p (Win/Linux)` or `cmd+shift+p (Mac)`. Navigate to option `Package Control: Install Package`. Install  packages: `SublimeLinter`, `SublimeLinter-flake8`, `sublack`, `UnitTesting`.
5. Navigate to `Package Settings` option under `Preferences` in Menu bar. For `Mac` users, the `Preferences` option will be found under `Sublime Text` in Menu bar.
6. Once under Package Settings, move to `SublimeLinter > Settings`. You will see that a file with the name `SublimeLinter.sublime-settings - User` opens up. Copy the following code snippet to ignore a linting error related to Tabs vs Spaces war :)
```
// SublimeLinter Settings - User
{
    "linters": {
        "flake8": {
            "args": ["--ignore=W191"],
        }
    }
}

```

## How to Run Tests? (For contributors)

1. For local execution of the tests, make sure that the Sublime package `UnitTesting` is installed. 
2. Navigate to a test file in `tests` folder that you want to run your tests for. 
3. Open Package Control and type in `UnitTesting: Test Current Package`. 
4. The tests will run and a small output panel pops up showing that the tests are running.

For more information and guide on how to run tests, take a look at this [README.md by randy3k](https://github.com/randy3k/UnitTesting/blob/master/README.md). For examples on how to write tests for sublime plugin, take a look at this [Repo by randy3k](https://github.com/randy3k/UnitTesting-example).

## How to Contribute?

Please take a look at our CONTRIBUTING.md where we provide instructions on contributing to the repo and taking the plugin development further.
