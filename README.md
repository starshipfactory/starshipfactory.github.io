# Starship Factory Website

This is the new Version of the Starship-Factory Website that is intended to be easier to keep up to date and change the Styling of it.
You can view the current progress on https://starshipfactory.github.io

The Website is built with Jekyll and Github Pages and can also be run in development mode locally with docker-compose:

    docker-compose up

In development mode you will have live-reload functionality and automatic rebuilds of content when you change it. Sadly changes to the configration files will not rebuild the whole site, just restart the docker container to accomplish that.

Alternatively there is a devcontainer that automatically starts when you open the Project in vscode. To run the development server inside the devcontainer use the following command:

    bundle exec jekyll serve --livereload --watch --incremental --host 0.0.0.0 --port "8080"

---
**NOTE**

You will need to create a personal token and copy it in the variable JEKYLL_GITHUB_TOKEN in the .env file  
https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

---

# Base Theme
We used Minimal Mistakes as the theme for Jekyll to get a good base start, see their starter Repos for more information:
- [Minimal Mistakes Starter Template](https://github.com/mmistakes/mm-github-pages-starter/)
- [Minimal Mistakes Jekyll theme](https://github.com/mmistakes/minimal-mistakes)
- [Minimal Mistakes Configuration](https://mmistakes.github.io/minimal-mistakes/docs/configuration/).
