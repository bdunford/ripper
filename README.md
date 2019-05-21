# riPPer
Utility for backing up web sites and possibly sanctioned phishing campagnes. Attempts to make a complete local copy of a web site, including css, scripts and images.  Removes most remaining external references.


### Install
```
pip install git+https://github.com/bdunford/ripper
```

### Usage

```
usage: run.py [-h] -u URL [-d DESTINATION] [-w] [-s]

Ripper: A utility for borrowing websites

optional arguments:
  -h, --help            show this help message and exit
  -u, --url             [URL] Url of page to be coppied
  -d, --destination     [DESTINATION] Path to write the files. Defalt: CWD
  -w, --window          Operate in Window mode
  -t, --threads         [THREADS] number of threads (processes) to use. Default: 4
  -s, --site            Rip all top level pages found on the main page (Experimental)
```
