# Contributing 
when you want to contribute to this repository, please send us an email and tell us what you want to change. 

### Table Of Contents
[Purpose of Contributing](#Purpose-of-Contributing)

[Code of Conduct](#Code-of-Conduct)

[Pull Request Submission Guidelines](#Pull-Request-Submission-Guidelines)

[Style Guide](#Style-guide)

## ⛄ Purpose of Contributing
* Maintain our product quality.
* Fix bugs and problems.
* Engage the community in working toward the best possible to our product.

## ❄️ Code of Conduct
All contributors should abide by the [code of conduct](CODE-OF-CONDUCT.md). Please read this carefully before contributing.

## ⚡ Pull Request Submission Guidelines
### 💻 Install Git 
First thing first, you should install and configure the [Git](https://git-scm.com/) on your local machine.

[Set Up Git](https://docs.github.com/en/github/getting-started-with-github/quickstart) is a good source for you to set up.

### 🍴 Fork Our Repositroy
To contribute code to our product, you must have a Github account so you could push code to your own fork and open Pull Requests in the [GitHub repository](https://github.com/Shahil98/SE_Fall20_Project-1)

### 👔 Work On Your Own branch
Once done and you have the code locally on the disk, you can get started. We advice to not work directly on the master branch, but to create a separate branch for each issue you are working on. That way you can easily switch between different work, and you can update each one for latest changes on upstream master individually.
### 📝 Write Code
For writing the code just follow our Python and JavaScript style guides. If there is something unclear of the style, just look at existing code which might help you to understand it better.

## 💬 Style Guide 

### Python Style Guide
* Use [Flake8](https://flake8.pycqa.org/en/latest/) as linter for Python codes
* Give variable names as words in lowercase seperated by underscores for e.g. 'variable_name'
* Give function names as words in lowercase seperated by underscores for e.g. 'function_name'
* Use upper camel case to write class names for e.g. 'MyClass'
* Try to select class, function and variable names that are meaningful wherever possible instead of using names like x, y, a etc
* Comment as much as you can. Write comments for each function stating what it does, what are it's input parameters and what are it's outputs. An example for comments in a function can be seen below:
```
def add_function(num1, num2):
    """
    Function to add two integers.

    Parameters
    ----------
    num1: int
        first number
    num2: int
        second number

    Returns
    -------
    sum
        an integer which is the sum of input integers
    """

    sum = num1 + num2
    return(sum)
```

### JavaScript Style Guide
* Give variable names as words in lowercase seperated by underscores for e.g. 'model_json'
* Use lower camel case to write function names for e.g. 'createKerasModel'
* Try to select function and variable names that are meaningful wherever possible instead of using names like x, y, a etc
* Use [js-beautify](https://github.com/beautify-web/js-beautify) as a code formatter. We are using 'Beautify' extension in VS Code which implements js-beautify and 'HTML-CSS-JS Prettify' extension in Sublime text editor which implements js-beautify.

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less

    
 ### Documentation Style Guide  
   * Use [Markdown](https://daringfireball.net/projects/markdown/)
