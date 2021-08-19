MCDR bot 
--------
A [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) plugin for adding bots into your server

Bot (fake player) is based on [pyCraft](https://github.com/ammaraskar/pyCraft), supports up to 1.17 server

Bot will be automatically set to creative mode for its safety. Don't worry it wont affect the game. Also you can set the default gamemode in the plugin

Don't forget to write your server port in `config/mcdr_pycraft_bot/config.json`

## Config

`address`: the address of the server

`port`: the port of the server

`gamemode`: the gamemode of the bot. Set it to `null` to keep the gamemode unchanged

`name_prefix`: the name prefix of the bot. Set it to an empty string if you dont want the prefix

## Command

```
!!bot add <name>: 召唤一个bot，名称为bot_<name>  |  summon a bot named bot_<name>
!!bot stop <name>: 让名称为<name>的bot离开游戏  |  remove the bot named <name>
!!bot tp <name>: 让bot传送到你的位置  |  teleport the bot to your position
!!bot list：列出当前所有的bot名称 | list all bots
!!bot clean: 使所有bot离开游戏  |  remove all bots
```
