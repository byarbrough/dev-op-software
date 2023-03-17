Our goal is to rapidly develop software that consistently delivers value to the customer. We will base our philosophy on the following three quotes:

> "**Make it correct,** make it clear, make it concise, make it fast. **In that order.**" - Wes Dyer

> I get paid for code that works, not for tests, so my philosophy is to **test as little as possible to reach a given level of confidence.** ~ [Kent Beck](https://stackoverflow.com/a/153565)

> **Anything that has hit production** to me **is legacy**. It’s out there, it’s something we have to deal with, it’s something that we have to maintain, and we have to understand, even if we don’t necessarily like that code at the end of the day. ~ Kris Brandow, [GoTime Episode 223](https://changelog.com/gotime/223)

They are all entertwined, but we'll start with "make it correct."

## Reduce Runtime Errors

A **runtime error** occurs while the program is running. Examples:
- Divide by zero
- Incorrect type
- Index out of bounds
- Undefined variables

We prefer **build time** errors (or compile time errors) because *they don't result in a crash on an operational system!*

How to convert some runtime errors to build time errors:
1. Use static analysis tools
2. Use type annotations.
3. Write unit tests.
4. Have a peer review the code.

### Static analysis tools

**Linters** flag style and syntax errors. Some even make the fixes for you. I recommend:

- [black: The uncompromising Python code formatter (github.com)](https://github.com/psf/black)
- [mypy: Optional static typing for Python (github.com)](https://github.com/python/mypy)
- [flake8: Error and style linter (github.com)](https://github.com/PyCQA/flake8)

Other static analysis tools focus on [security](https://github.com/PyCQA/bandit) or more complex analysis.

The objective should be to get as much benefit as possible with as few false positives as possible. Developers hate false positives, and will just start ignoring your tools if there are too many.

## Test your interfaces

> A good interface should perform a single mutation on a data structure, and that mutation must provide some value to the consumer. ~ Brian Yarbrough

Unit testing is hard. And misunderstood. And can be detrimental.
It is an entire discipline unto itself, but i believe that the best approach is to *test your interfaces*.

An **interface makes an agreement with an external system.** That means the other system depends on you to reliably produce the correct result. If you stop presenting the correct result, or even present a correct result in a different way, complex systems start to fail in very difficult-to-diagnose ways.

An interface - whether an API, public method, ect. - should only do one specific thing. That thing must *always* answer a customer requirement. Otherwise, it should not be an interface. That thing usually involves taking in a data structure, performing a single transformation, and returning a data structure. If you design your interfaces in this way, they will be easier to unit test and less likely to break in unexpected ways.

Often times, *internal methods should not have unit tests.* This is because internal methods are about implementation, not results. **The point of unit tests is to provide developers the confidence to make changes,** knowing that the change they make still provides the correct result to the customer.

A good example is this: if our job is to present a square, we should test that we have four equal sides and four 90 degree angles. We should not be concerned with testing internally if that square was built with two right triangles, or two rectangles. See [Why unit tests and how to make them work for you - Learn Go with tests (gitbook.io)](https://quii.gitbook.io/learn-go-with-tests/meta/why#if-unit-tests-are-so-great-why-is-there-sometimes-resistance-to-writing-them)

## Manage tech debt

> We don't make things easy to do; we make things easy to understand.

Tech debt is like when you go to make breakfast, but your kitchen is still a mess from the night before. It slows you down and makes you do things in an inefficient manner. Temporarily, a little tech debt can be a good thing because it allows for space to create! Can you imagine if you had to clean your knife after every vegetable you chopped?

In the long term, we want code to be maintainable. **Maintainable code is more likely to remain error free and allow developers to work on the project long-term.**

- Don't write code for yourself; write it for the person who comes after you.
- Tomorrow is not a guarantee, so write code for today. It can be extended later.
- Spend time making code understandable and documented, rather than performant.
- Don't be afraid to feature pause to clean up tech debt.
- Use linters.
- Use [Semantic Versioning 2.0.0 | Semantic Versioning (semver.org)](https://semver.org/)

## The Workflow

1. Developer (dev) creates feature branch from `main` branch
2. Dev implements a single feature, ideally referencing a specific issue.
3. Dev uses [pre-commit](https://pre-commit.com/) to run linters and static analysis before even committing. Unit tests also run locally, if possible.
5. Dev pushes to remote for lint checks and unit tests to run in automated pipeline.
6. Dev creates Pull Request (PR) into `main` branch.
7. A different engineer reviews the pull requests, providing feedback.
8. Dev makes necessary changes and pushes updates.
9. Once the pipeline passes **and** comments are resolved, the reviewer approves the PR.
10. Pipelines re-run on `main`
11. `main` is now updated. Depending on project philosophy, the updated feature is available immediately or with the next release (according to Semantic Versioning).

![Merge branch 'asdfasjkfdlas/alkdjf' into sdkjfls-final](https://imgs.xkcd.com/comics/git_commit.png)

    Merge branch 'asdfasjkfdlas/alkdjf' into sdkjfls-final

### Pre-Commit

A configuration file is included with your project and executes *before* the commit happens.

A developer must install pre-commit and add it to the git hooks folder. This should usually happen in a virtual environment or in a container.

See this repository's [.pre-commit-config.yaml](.pre-commit-config.yaml)

#### Setup

Each developer must run this the first time they clone the project.

```bash
## only run this once, to setup virtual environment
python -m venv env
# enter the env. It isolates packages from system pacakges
source env/bin/activate
# now we are in the virtual env, you will see a (env) before your prompt
pip install pre-commit
# add the git hook to always run
pre-commit install
```

#### Usage

Whenever a developer opens a new terminal they need to source the virtual environment. Most IDEs (VScode or Pycharm) can be configured to do this automatically.

```bash
source env/bin/activate
```

Pre-commit will always run whenever you try to `git commit`, but you can manually run it with:

```bash
pre-commit run --all-files
```

### GitHub Actions

Run automated pipelines in the cloud when code is pushed to GitHub (or on merges, or other triggers). The workflow is described in YAML files.

See this repository's [.github/workflows/lint.yml](.github/workflows/lint.yml)

#### A live delpoyment

Sample action file that builds the [ECE 281 Website](https://usafa-ece.github.io/ece281-book/intro.html):
```yaml
---
name: deploy-book

# Only run this when the main branch changes
on:
  push:
    branches:
      - main

# This job installs dependencies, builds the book, and pushes it to `gh-pages`
jobs:
  deploy-book:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      # Install dependencies
      - name: Set up Python 3.10
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      # Build the book
      - name: Build the book
        run: |
          jupyter-book build book/

      # Push the book's HTML to github-pages
      - name: GitHub Pages action
        uses: peaceiris/actions-gh-pages@v3.9.0
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./book/_build/html
```
