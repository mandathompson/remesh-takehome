# Remesh Takehome assignment

Junior Dev take home assignment completed by Amanda Thompson

## Installation
Assuming you have [python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/) locally installed (you may need to use pip3 instead of pip), perform the following in order:

- fork/clone the repository
- in terminal, cd into the directory

```bash 
python3 -m venv venv
```
```bash 
source venv/bin/activate
```

```bash
pip3 install -r requirements.txt
```
```bash
python3
```

```python
>>>from app import db
>>>from app import Post, Message, Thought
>>>db.create_all()
>>>quit()
```

```bash
flask run
```


## Note:
I really enjoyed this learning experience. This was my first encounter with nested commenting, and you will see that I hit a couple of walls. I would also like to note that I did not worry about styling at all. I have also not encountered testing dynamic data in flask yet, but look forward to learning more about it and will welcome any and all feedback and resources you may have to give. Thank you so much for this experience!




