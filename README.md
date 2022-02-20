# NewBinusmaya Tools

Python project that helps you to fetch your class schedule from BinusMaya and exports it to a CSV file that can be imported to Google Calendar. You can also choose to push the schedule directly to Google Calendar, Notion and MongoDB using their respective APIs.

This project also allows you to download powerpoint files from all of your classes.

## Usage

Install requirements by running
```sh
pip install -r requirements
```

**Base Usage:**

- Login to [https://newbinusmaya.binus.ac.id](https://newbinusmaya.binus.ac.id/lms/dashboard)
- Open inspect by pressing `CTRL+SHIFT+i` or `CMD+SHIFT+i`
- Switch to the Network Tab
- Refresh the page
- Filter by `Fetch/XHR`
- Select item from the Activity Log
- Open the “Headers” tab
- View source on “Request Headers”
- Copy the values to `util.py`

```python
institution = " "
roleId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
Authorization = "Bearer xxxxxxxxxxxxxxxxxx..."
rOId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
academicCareer = " "
```

- Run `schedule_fetcher.py`
- Import `gcal_... .csv` to Google Calendar

**Uploading directly to Google Calendar:**

- Make sure you have run `schedule_fetcher.py`
- Follow [this](https://developers.google.com/workspace/guides/create-credentials) guide to obtain your OAuth credentials
- Input your email or [Calendar ID](https://support.google.com/a/answer/1626902?hl=en) in the `.env` file
- Configure your courses color in the `push_to_gcal.py`

```python
color = ""
    if "coursename" in data[i]["course"]:
        color = "5"
    #add your other courses here
    else:
        color = "2"
```

- run `push_to_gcal.py`

**Uploading to notion:**

- Make sure you have run `schedule_fetcher.py`
- Duplicate this [page](https://www.notion.so/b262d915209341599be5e6e680c636d2)
- Populate “Courses” with courses name (has to be exactly the same as course name in newbinusmaya)
- Populate “Class” with the format “XXYY - LAB” etc.
- Get your Integration token by following the Step 1 in this [doc](https://developers.notion.com/docs/getting-started)
- Input your token and database name in the `.env` file
- Run `push_to_notion.py`

**Uploading to MongoDB:**

- pretty sure you know how 🙂

**Downloading Powerpoint files:**

- Make sure you have run schedule_fetcher.py
- Run `pptDownloader.py`