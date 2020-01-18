# 100DaysOfCode Challenge `log.md` Generator

Welcome to this Log Maker.

Download the files or `git clone https://github.com/MattiooFR/log-maker-100-days` and write `python main.py` in your terminal where the files are located to generate a log.md as this [example](log.md).

### Requirements :

* Python version should be 3.6 or above as I'm using the f-string format
* Dateparser module, `pipenv|pip|conda install dateparser` if you want to chose a date other than today

If you want to generate a log from a specific date you can do it this way :

`python main.py 22 december 2019`

This will generate a log.md starting from the December 22, 2019. Check the [dateparser doc](https://dateparser.readthedocs.io/en/latest/) to see all the available date format.

Available options when running the program :
```
-o, --overwrite : overwrite if file already exist
-d, --duration : custom challenge duration
-f, --filename : custom generated filename, default is 'log.md'
-t, --type : change the generated filetype, default is 'md'(markdown), available : 'html'
-u, --update : update a log.md file that already exist by removing the missed days and adding them as new days at the end
```

### Todo :

* [x] Update existing file if days are missed during challenge
* [x] New output format (html, excel, ...)
* [ ] Make a live website log generator for challenge
* [ ] Choose any type of challenge (not just code)
* [ ] Implement ninja2 library to generate the html with a template
* [ ] Use BeautifulSoup library to parse html file
