# Math 214 Project 3 - Least Squares Data Fitting

This repository can be accessed at [derickson2402/Math-214-Project-4](https://github.com/derickson2402/Math-214-Project-4)

## LaTeX Setup Instructions

To edit this project on your computer, click ```Code``` in GitHub and follow the instructions to set up GitHub Desktop. On your computer, open the repo in VSCode, and edit the ```.tex``` file.

To set up your computer so you can build the PDF with LaTeX, first make sure you set up GitHub Desktop and VS Code. Then install LaTeX to your computer (```brew install mactex``` on mac, or on windows go to [the LaTeX website](https://www.latex-project.org/get/) and download it). On VS Code, install ```LaTeX Workshop``` and ```LaTeX Utilities``` extensions. Now when you save the LaTeX file, the PDF will automatically be generated.

Before adding changes, do a ```git pull```, then do your changes, then do ```git commit``` and include a message on what problem you did, then do ```git push```.

There are tags on some of the git commits, they correspond to the different deadlines outlined in the spec. So for example ```1-Initial-Proposal``` corresponds to the commit used to submit the Initial Proposal.

## Python Setup Instructions

The ```waveCompress.py``` script performs a wavelet-transform compression algorithm on an image of your choosing. To run it, open a terminal on your computer and run ```./waveCompress.py```. Then just specify an input and output file.

The script was written for Python 3.10.3, but you may be able to get it to work with other versions. The easiest way to set up your computer is to use ```pyenv```, which is a Python version manager. You can use something like the following (please Google this first because I did this a long time ago and it might need more setup...):

```bash
$ brew update && brew install pyenv
$ pyenv install 3.10.3
$ pyenv local 3.10.3
$ chmod +x ./waveCompress.py
$ pip install PyWavelets
```

If you don't want to use Homebrew and pyenv.... too bad. You should. They're excellent programs. They are simple to install. And it works on my machine :smile:.

Main point is you need to make sure you have Python installed, and you will need the ```PyWavelets``` package. This does all of the serious lifting for us, because implementing a full-scale 2-dimensional wavelet transform on our own is way too intensive for an undergrad linear algebra course.
