# Script to export members Telegram Groups and Channels to a CSV file and to add members to Telegram Groups or Channels.

> Exporting and adding members to channels requires the user from which the script is launched to be a Channel admin.

### Install dependencies

You'd need python3 and pip3 installed and available in your PATH.

Run `pip3 install -r requirements.txt` from the projects root directory.

### Telegram Configuration

1. To run it you need to generate API credentials for your Telegram user, you can do it [here](https://core.telegram.org/api/obtaining_api_id), and access your already created ones [here](https://my.telegram.org/apps)
2. Replace your credentials in the script
    ```python
    api_id = 000000        # YOUR API_ID
    api_hash = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'        # YOUR API_HASH
    phone = '+34000000000'        # YOUR PHONE NUMBER, INCLUDING COUNTRY CODE
    ```

### Export users
Just follow the instructions in the script after running it from your the shell.

### Add users to groups

Users can be added using:
- **Username**: Gets temporarily banned with less requests.
- **User ID**: Gets temporarily banned with more requests.

> Temporarily bans last for up to a day in my experience.

Adding users by Username expects a CSV file with one username per line.
Adding users by User ID expects a CSV file such as: `username,user_id,user_access_hash`

> No headers are expected in the CSV files

Once you have your CSV prepared, just follow the instructions in the script.

## Evn
* virtualenv -p /usr/local/bin/python3.9 venv
* . venv/bin/activate (for 3.9.6)
* pip install -r requirements.txt

## Change api :
/usr/local/lib/python3.9/dist-packages/telethon/client
```
results = await self.client(self.requests)
        print("Request .. ",self.requests)
        print("RANGE.. ", range(len(self.requests)))
        for i in reversed(range(len(self.requests))):
            print("DEBUGN..FULL ", i, results, type(results))
            # print("DEBUGN..LESS ", i, results[i])
            participants = results
            if isinstance(results, list) :
                participants = results[i]
            if self.total is None:
                # Will only get here if there was one request with a filter that matched all users.
                self.total = participants.count
            if not participants.users:
                self.requests.pop(i)
                continue
```
