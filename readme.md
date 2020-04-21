MCDR bot 
--------
A [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) plugin for adding bots into your server

Copy `MCDR-Bot.py` and `MCDRBotUtils/` into the `plugins/` folder of MCDR, then `pip install -r requirement.txt` and that's it 

Bot (fake player) is based on [pyCraft](https://github.com/ammaraskar/pyCraft), supports up to 1.15.2 server

Bot will be automatically set to creative mode for its safety. Don't worry it wont affect the game. Also you can set the default gamemode in the plugin

Don't forget to write your server port in `MCDRBotUtils/port.ini`

## Command

```
!!bot add <name>: 召唤一个bot，名称为bot_<name>  |  summon a bot named bot_<name>
!!bot stop <name>: 让名称为<name>的bot离开游戏  |  remove the bot named <name>
!!bot tp <name>: 让bot传送到你的位置  |  teleport the bot to your position
!!bot clean: 使所有bot离开游戏  |  remove all bots
```
