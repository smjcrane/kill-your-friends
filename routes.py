from html import escape

def get_homepage(rh, game, userid):
    if userid is None:
        get_admin_panel(rh, game, userid)
        return
    
    if game.status == "INIT":
        if userid in game.players:
            player = game.players[userid]
            rh.wfile.write(bytes("<p>Welcome back, %s</p><p>Please wait for the game to start.</p>" % escape(player.name), "utf-8"))
        else:
            rh.wfile.write(bytes("""<p>Pleased to meet you, what's your name?</p>
                                    <form action=add method=POST><input name=name>
                                        </input><br/><input type=submit value=SAVE></input>
                                    </form>""", "utf-8"))
    
    elif game.status == "PLAYING":
        player = game.players[userid]
        rh.wfile.write(bytes("<p>Welcome back, %s</p>" % escape(player.name), "utf-8"))
        if player.alive:
            rh.wfile.write(bytes("<p>You have made %d kills</p>" % player.kills, "utf-8"))
            rh.wfile.write(bytes("<p>Your target: %s</p>" % escape(game.players[player.targetid].name), "utf-8"))
            rh.wfile.write(bytes("<p>Your deadly weapon: \"%s\"</p>" % escape(game.players[player.targetid].killword), "utf-8"))
            rh.wfile.write(bytes("""<br><br><br><center><span center=true>
                                    <form action=kill method=POST onsubmit=\"return confirm('Death is permanent, are you sure?');\">
                                        <input type=submit value='I HAVE BEEN KILLED'>
                                    </form></span></center>""", "utf-8"))
        else:
            rh.wfile.write(bytes("<p>You are DEAD</p>", "utf-8"))

    elif game.status == "FINISHED":
        player = game.players[userid]
        rh.wfile.write(bytes("<p>Welcome back, %s</p>" % escape(player.name), "utf-8"))
        rh.wfile.write(bytes("<p>The game is over.</p>", "utf-8"))
        if player.alive:
            rh.wfile.write(bytes("<p>Congratulations, you made it to the end!</p>", "utf-8"))
        else:
            rh.wfile.write(bytes("<p>You did not win.</p>", "utf-8"))
        rh.wfile.write(bytes("<p>You made %d kills</p>" % player.kills, "utf-8"))

    rh.wfile.write(bytes("<br><br><br><center><span center=true><a href=/static/rules.html class=rules><input type=submit value=RULES></input></a></span></center>", "utf-8"))


def post_add_player(rh, game, userid, vars):
    if userid is None:
        return
    
    name = vars["name"]
    if not name:
        return
    
    if game.status != "INIT":
        rh.wfile.write(bytes("<p>You can't change your name once the game has begun!</p>", "utf-8"))
        return

    game.add_player(userid)
    player = game.players[userid]
    for p in game.players.values():
        if (p.userid != userid) and p.name == name:
            rh.wfile.write(bytes("<p>That name is already taken!</p>", "utf-8"))
            rh.wfile.write(bytes("<script>setTimeout(()=>location.href='/',1500)</script>", "utf-8"))
            return
    player.name = vars["name"]
    rh.wfile.write(bytes("<p>From now on I'll refer to you as %s</p>" % escape(player.name), "utf-8"))
    rh.wfile.write(bytes("<script>setTimeout(()=>location.href='/',1500)</script>", "utf-8"))

def post_record_kill(rh, game, userid, vars):
    if userid is None:
        return
    # possibly have to enter the word to confirm death
    game.kill(userid)
    rh.wfile.write(bytes("<p>Boom! Headshot!</p>", "utf-8"))
    rh.wfile.write(bytes("<script>setTimeout(()=>location.href='/',1500)</script>", "utf-8"))

def post_start_game(rh, game, userid, vars):
    if userid is not None:
        return
    if game.status == "INIT":
        print("starting game")
        game.begin()
        rh.wfile.write(bytes("<p>Let the game begin!</p>", "utf-8"))
    else:
        print("not starting game")
        rh.wfile.write(bytes("<p>Oops, the game wasn't in the initialisation phase</p>", "utf-8"))
    rh.wfile.write(bytes("<script>setTimeout(()=>location.href='/',1500)</script>", "utf-8"))

def post_end_game(rh, game, userid, vars):
    if userid is not None:
        return
    if game.status == "PLAYING":
        print("ending game early")
        game.status = "FINISHED"
        rh.wfile.write(bytes("<p>The game is OVER!</p>", "utf-8"))
    rh.wfile.write(bytes("<script>setTimeout(()=>location.href='/',1500)</script>", "utf-8"))

def get_admin_panel(rh, game, userid):
    if userid is not None:
        return
    rh.wfile.write(bytes("<p>You are ADMIN</p>", "utf-8"))
    if game.status == "INIT":
        rh.wfile.write(bytes("<p>Game is in setup phase.<br/>Here is a list of players:</p><table>", "utf-8"))
        for p in game.players.values():
            rh.wfile.write(bytes("""<tr>
                                 <td>%s</td>
                                 <td>
                                    <form method=POST action=\"/remove\">
                                        <input name=id type=hidden value=%s><input type=submit value=REMOVE></input>
                                    </form>
                                 </td>
                                 </tr>""" % (escape(p.name), p.userid), "utf-8"))
        rh.wfile.write(bytes("</table>", "utf-8"))
        if len(game.players) > 1:
            rh.wfile.write(bytes("<form action=start method=POST><input type=submit value=START></form>", "utf-8"))
    elif game.status == "PLAYING":
        rh.wfile.write(bytes("<p>Game is in progress.<br/>Here is a list of players:</p><table>", "utf-8"))
        for p in game.players.values():
            if p.alive:
                rh.wfile.write(bytes("""<tr>
                                     <td>%s</td>
                                     <td>Alive</td>
                                     <td>
                                        <form method=POST action=\"/remove\" onsubmit=\"return confirm('Death is permanent, are you sure?');\">
                                            <input name=id type=hidden value=%s><input type=submit value=KILL></input>
                                        </form>
                                     </td>
                                     <td>
                                        <form method=POST action=\"/reroll\" onsubmit=\"return confirm('Change what will kill this player?');\">
                                            <input name=id type=hidden value=%s><input type=submit value=REROLL></input>
                                        </form>
                                     </td>
                                     </tr>""" % (escape(p.name), p.userid, p.userid), "utf-8"))
            else:
                rh.wfile.write(bytes("<tr><td>%s</td><td>Dead</td></tr>" % escape(p.name), "utf-8"))
        rh.wfile.write(bytes("</table>", "utf-8"))
        rh.wfile.write(bytes("<form action=end method=POST><input type=submit value='END GAME NOW'></form>", "utf-8"))
    elif game.status == "FINISHED":
        rh.wfile.write(bytes("<p>The game is over.<br/>Here is a list of players:</p><table>", "utf-8"))
        for p in game.players.values():
            rh.wfile.write(bytes("<tr><td>%s</td><td>%s</td></tr>" % (escape(p.name), "Alive" if p.alive else "Dead"), "utf-8"))
        rh.wfile.write(bytes("</table>", "utf-8"))

def post_admin_remove(rh, game, userid, vars):
    if userid is not None:
        return
    if game.status == "INIT":
        print("deleting %s" %vars["id"])
        del game.players[vars["id"]]
    elif game.status == "PLAYING":
        game.kill(vars["id"])
    rh.wfile.write(bytes("<script>location.href='/'</script>", "utf-8"))

def post_admin_reroll(rh, game, userid, vars):
    if userid is not None:
        return
    if game.status == "PLAYING":
        game.reassign_word(vars["id"])
    rh.wfile.write(bytes("<script>location.href='/'</script>", "utf-8"))


def get_admin_shell(rh, game, userid):
    if userid is not None:
        return
    rh.wfile.write(bytes("""<form method=POST>
                         <p>cmd: </p><input name=cmd></input>
                         </form>""", "utf-8"))

    
def post_admin_shell(rh, game, userid, vars):
    if userid is not None:
        return
    s = str(eval(vars["cmd"]))
    rh.wfile.write(bytes("""<p>%s</p>
                         <form method=POST>
                         <p>cmd: </p><input name=cmd></input>
                         </form>""" % escape(s), "utf-8"))
