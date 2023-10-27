# Assassins game

This is an in-person game for 2 or more players. The objective is to make your target say a specific word. This kills them and assigns their previous target to you. Survive to the end or score the most points for victory!

## Setup

Run `server.py` on a computer. Then all players can connect to the game server and enter their name. Browsing to the site from the server will instead serve an admin panel where you can manage the list of current players.

It is essential that the server and all the players are on the same network.

Once all players have joined, you will need to start the game from the admin panel.

## Rules in detail

See `rules.html`.

## Troubleshooting

### I can access the site on localhost but not from my phone

 - Is your phone on the same network as the server?
 - Is the server listening on the correct interface and port? These can be edited at the top of `server.py`.
 - Is your phone or server using a VPN or adblocker?

### I don't know what my word means so I can't make my target say it

The admin panel has an option to assign a new word that will kill your target.

### I want to do something weird to the game state like add a new player halfway through

There is a secret emergency backdoor at `/shell` (only accessible from the server) where you can run any python command. Use at your own risk!
