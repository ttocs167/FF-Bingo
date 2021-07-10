**FF Bingo**

This is the code for a Discord bot with many functions. Mostly the bot is intended to create and dispense bingo cards!
The code creates files for each server it is in so card pools and images are separated by server.


**Usage**

To use script make sure all packages in the `requirements.txt` are installed and run `main.py`. 
You will have to setup your own Discord Bot account, to get this code to run on the bot you must set an environment
variable `BINGO_BOT_TOKEN` to your Discord Bot token. This can be done in a `.env` file in the root folder. 

If you want to enable the $teanalyze command then you must also add an fflogs api key and set it to the `FFLOGS_API_KEY` variable in the `.env` file,
you can get a token by logging into fflogs.com and navigating to https://www.fflogs.com/profile, and create a v1 web api client, the generated V1 client key 
is what `FFLOGS_API_KEY` must be set to.

**3 musketeers**

Optionally if you have the following depedencies installed you can use the 3 musketeers method instead.
```
make
docker
docker-compose
```

run the following commands

```
make deps
make envfile
```
update the `BINGO_BOT_TOKEN` value in the `.env` file

```
make run
```